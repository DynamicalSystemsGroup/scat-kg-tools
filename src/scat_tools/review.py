"""The review view: where to look next, never what is true.

    scat_tools.review()      # pages that may be one node, and pages to re-read

Two lists, both proposals for a coder to read and decide on. The view writes nothing, reads no narrative's
`attributed_to` and lists no contributor page. An uncoded narrative is left out and listed under `excluded`, as in
the other views. Names are never compared: a proposal comes from what the vault says around a page, not from how
its name is spelled.

Possible duplicates. Two pages of one type are proposed when any of these holds:
  - their adjacent nodes (the nodes one edge away) overlap by 0.5 or more (Jaccard: shared over all), and each page
    has two or more adjacent nodes;
  - their descriptions overlap by 0.5 or more (cosine of word counts: words of three letters or more, a short list
    of common words dropped; a page with no description has no cosine);
  - a narrative tells the same edge type to the same other end for both pages (a twin row), and the narratives that
    link the two pages overlap by 0.5 or more (Jaccard).
Each proposal gives both pages, the three overlaps, the twin rows (narrative, file and the line of each row), the
shared adjacent nodes with the hubs among them marked, a one-line reason, and the link texts coders wrote for each
page (`[[node|text]]` in a narrative). Link text is shown beside a proposal and is never scored. A hub is a node page
adjacent to at least 4 pages and to more than a tenth of all node pages; sharing a hub says little, so the shared
adjacent nodes show which ones are not.

Pages to re-read. A page whose edges are told by 4 or more narratives, where at most 0.3 of the pairs of those
narratives tell the page to a common other end. The narratives are grouped: two are in one group when they tell the
page to a common other end, directly or through others. The groups are shown; the view does not say what they mean.

Order is deterministic: proposals by the sum of the three overlaps, highest first, then by name; pages to re-read by
the share of narrative pairs with a common end, lowest first, then by name.
"""

import itertools
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

from scat_tools.graph import Graph, Node
from scat_tools.ops.result import reports_mode
from scat_tools.vault import _BODY_LINK, blank_code, link_target
from scat_tools.views import (
    Refused,
    View,
    _drawn,
    _excluded,
    _excluded_lines,
    _open,
)

# The thresholds, in one place. A change here changes which pages are proposed.
ADJACENT_JACCARD = 0.5  # adjacent-node overlap that proposes a pair ...
MIN_ADJACENT = 2  # ... when both pages have at least this many adjacent nodes
DESCRIPTION_COSINE = 0.5  # description overlap that proposes a pair
NARRATIVE_JACCARD = 0.5  # narrative overlap that proposes a pair with a twin row
HUB_MIN_PAGES = 4  # a hub is adjacent to at least this many node pages ...
HUB_SHARE = 0.1  # ... and to more than this share of all node pages
REREAD_MIN_NARRATIVES = 4  # narratives that tell a page's edges, at least
REREAD_COMMON_END = 0.3  # share of those narrative pairs with a common other end, at most

_WORD = re.compile(r"[a-z]+")
_COMMON = frozenset(
    (
        "the",
        "a",
        "an",
        "and",
        "or",
        "of",
        "to",
        "in",
        "on",
        "for",
        "with",
        "by",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "it",
        "its",
        "that",
        "this",
        "as",
        "at",
        "from",
        "their",
        "they",
        "them",
        "his",
        "her",
        "he",
        "she",
        "not",
        "but",
        "which",
        "who",
        "what",
        "when",
        "where",
        "how",
        "than",
        "then",
        "so",
        "such",
        "into",
        "out",
        "up",
        "one",
        "two",
        "also",
        "here",
        "there",
        "has",
        "have",
        "had",
        "can",
        "could",
        "would",
        "may",
        "more",
        "most",
        "only",
        "own",
        "same",
        "other",
        "no",
        "do",
        "does",
        "did",
        "if",
        "about",
        "over",
        "after",
        "before",
        "between",
        "both",
        "each",
        "across",
        "through",
    )
)


class ReviewView(View):
    """The review view: the data of `View`, and a text form that begins with the vault's attribution mode."""

    def __str__(self) -> str:
        head = f"attribution mode: {self.mode or 'not declared'}"
        return "\n".join([head, *_lines(self.data)])

    __repr__ = __str__


def _jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a | b else 0.0


def _vector(text: str) -> Counter:
    return Counter(w for w in _WORD.findall(text.lower()) if w not in _COMMON and len(w) > 2)


def _cosine(a: Counter, b: Counter) -> float:
    num = sum(v * b.get(k, 0) for k, v in a.items())
    den = math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values()))
    return num / den if den else 0.0


def _link_texts(g: Graph) -> dict[str, list[str]]:
    """For each node page, the texts coders gave its links in narratives (`[[node|text]]`), each once, sorted."""
    found: dict[str, set[str]] = defaultdict(set)
    pages = {p.path: p for p in g.vault.pages}
    for nar in g.narratives:
        for m in _BODY_LINK.finditer(blank_code(pages[nar.path].body)):
            target = link_target(m.group(1))
            if target is not None and "|" in m.group(1):
                text = " ".join(m.group(1).split("|", 1)[1].split())
                if text:
                    found[target].add(text)
    return {k: sorted(v) for k, v in found.items()}


def _twin_rows(g: Graph, by_key: dict, a: str, b: str) -> list[dict]:
    """The rows in which one narrative tells the same edge type between each of the two pages and one other end."""
    out = []
    for e in g.edges:
        if a not in (e.from_node, e.to_node):
            continue
        forward = e.from_node == a
        other = e.to_node if forward else e.from_node
        twin = by_key.get((e.type, b, other) if forward else (e.type, other, b))
        if twin is None:
            continue
        lines = {t.narrative: t.line for t in twin.tellings}
        out += [
            {
                "narrative": t.narrative,
                "file": t.path,
                "edge_type": e.type,
                "other_end": other,
                "lines": [t.line, lines[t.narrative]],
            }
            for t in e.tellings
            if t.narrative in lines
        ]
    return sorted(out, key=lambda r: (r["narrative"], r["edge_type"], r["other_end"]))


def _reason(
    shared: int, union: int, cosine: float, twins: int, why: tuple[bool, bool, bool]
) -> str:
    parts = []
    if why[0]:
        parts.append(f"{shared} of {union} adjacent nodes shared")
    if why[1]:
        parts.append(f"descriptions share {cosine:.2f} of their words")
    if why[2]:
        parts.append(f"a narrative tells the same row for both ({twins}x)")
    return "may be one node: " + "; ".join(parts)


def _page(n: Node, texts: dict[str, list[str]]) -> dict:
    return {**_entry(n), "link_texts": texts.get(n.name, [])}


def _entry(n: Node) -> dict:
    return {"name": n.name, "type": n.type, "status": n.status}


def _proposals(g: Graph, texts: dict[str, list[str]]) -> list[dict]:
    nodes = {n.name: n for ns in g.nodes.values() for n in ns}
    linked: dict[str, set] = defaultdict(set)  # narratives that link the page
    adjacent: dict[str, set] = defaultdict(set)
    for nar in g.narratives:
        for x in nar.nodes:
            linked[x].add(nar.name)
    for e in g.edges:
        adjacent[e.from_node].add(e.to_node)
        adjacent[e.to_node].add(e.from_node)
    by_key = {(e.type, e.from_node, e.to_node): e for e in g.edges}
    pages = {p.path: p for p in g.vault.pages}
    vectors = {}
    for name, n in nodes.items():
        description = pages[n.path].fields.get("description")
        vectors[name] = _vector(description if isinstance(description, str) else "")
    reach = len(nodes) * HUB_SHARE
    hubs = {x for x, ends in adjacent.items() if len(ends) >= HUB_MIN_PAGES and len(ends) > reach}
    out = []
    for layer_nodes in g.nodes.values():
        for na, nb in itertools.combinations(sorted(layer_nodes, key=lambda n: n.name), 2):
            a, b = na.name, nb.name
            adj, nar, cos = (
                _jaccard(adjacent[a], adjacent[b]),
                _jaccard(linked[a], linked[b]),
                _cosine(vectors[a], vectors[b]),
            )
            twins = _twin_rows(g, by_key, a, b)
            why = (
                adj >= ADJACENT_JACCARD and min(len(adjacent[a]), len(adjacent[b])) >= MIN_ADJACENT,
                cos >= DESCRIPTION_COSINE,
                bool(twins) and nar >= NARRATIVE_JACCARD,
            )
            if not any(why):
                continue
            both, either = adjacent[a] & adjacent[b], adjacent[a] | adjacent[b]
            out.append(
                {
                    "type": na.type,
                    "pages": [_page(na, texts), _page(nb, texts)],
                    "narrative_jaccard": round(nar, 3),
                    "adjacent_jaccard": round(adj, 3),
                    "description_cosine": round(cos, 3),
                    "twin_rows": twins,
                    "shared_adjacent": [
                        {**_entry(nodes[x]), "hub": x in hubs}
                        for x in sorted(both, key=lambda x: (list(g.nodes).index(nodes[x].type), x))
                    ],
                    "reason": _reason(len(both), len(either), cos, len(twins), why),
                }
            )
    return sorted(
        out,
        key=lambda p: (
            -(p["narrative_jaccard"] + p["adjacent_jaccard"] + p["description_cosine"]),
            p["pages"][0]["name"],
            p["pages"][1]["name"],
        ),
    )


def _groups(names: list[str], ends: dict[str, set]) -> list[list[str]]:
    """The narratives grouped: joined when they tell the page to a common other end, directly or through others."""
    seen: set[str] = set()
    out = []
    for first in names:
        if first in seen:
            continue
        group, todo = set(), [first]
        while todo:
            x = todo.pop()
            if x not in group:
                group.add(x)
                todo += [y for y in names if y not in group and ends[x] & ends[y]]
        seen |= group
        out.append(sorted(group))
    return sorted(out, key=lambda grp: (-len(grp), grp))


def _reread(g: Graph) -> list[dict]:
    out = []
    for n in (n for ns in g.nodes.values() for n in ns):
        ends = {}
        for nar in g.narratives:
            mine = {
                k.to_node if k.from_node == n.name else k.from_node
                for k in nar.edges
                if n.name in (k.from_node, k.to_node)
            }
            if mine:
                ends[nar.name] = mine
        if len(ends) < REREAD_MIN_NARRATIVES:
            continue
        names = sorted(ends)
        pairs = list(itertools.combinations(names, 2))
        share = sum(bool(ends[x] & ends[y]) for x, y in pairs) / len(pairs)
        if share <= REREAD_COMMON_END:
            out.append(
                {
                    **_entry(n),
                    "narratives": len(names),
                    "common_end_share": round(share, 3),
                    "groups": _groups(names, ends),
                    "reason": "these accounts tell this page to different other ends; read them together",
                }
            )
    return sorted(out, key=lambda r: (r["common_end_share"], r["name"]))


@reports_mode
def review(*, root: str | Path = ".") -> View | Refused:
    """Pages that may be one node, and pages whose accounts tell it to different other ends: where to read next."""
    op = "review"
    g, bad = _open(op, root)
    if bad:
        return bad
    names = [n.name for n in g.narratives]
    nodes = [n for ns in g.nodes.values() for n in ns]
    if bad := _drawn(op, g, names, nodes, g.edges, names, True):
        return bad
    texts = _link_texts(g)
    return ReviewView(
        op,
        {"proposals": _proposals(g, texts), "reread": _reread(g), "excluded": _excluded(g)},
    )


# ---------------------------------------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------------------------------------


def _proposal_lines(p: dict) -> list[str]:
    a, b = p["pages"]
    overlaps = (
        f"        narratives {p['narrative_jaccard']:.2f}, adjacent nodes {p['adjacent_jaccard']:.2f}, "
        f"descriptions {p['description_cosine']:.2f}"
    )
    out = [
        f"    {a['name']} ~ {b['name']} ({p['type']}; {a['status']}, {b['status']}): {p['reason']}",
        overlaps,
    ]
    for t in p["twin_rows"]:
        out.append(
            f"        twin row: {t['narrative']} ({t['file']} lines {t['lines'][0]} and {t['lines'][1]}) "
            f"tells {t['edge_type']} with {t['other_end']}"
        )
    if p["shared_adjacent"]:
        shared = ", ".join(x["name"] + (" (hub)" if x["hub"] else "") for x in p["shared_adjacent"])
        out.append(f"        shared adjacent nodes: {shared}")
    for page in p["pages"]:
        if page["link_texts"]:
            shown = ", ".join(f'"{t}"' for t in page["link_texts"])
            out.append(f"        link texts for {page['name']}: {shown}")
    return out


def _reread_lines(r: dict) -> list[str]:
    n = r["narratives"]
    head = (
        f"    {r['name']} ({r['type']}, {r['status']}): {n} narratives, "
        f"{r['common_end_share']:.2f} of pairs share an other end; {r['reason']}"
    )
    return [head] + [f"        group: {', '.join(grp)}" for grp in r["groups"]]


def _lines(d: dict) -> list[str]:
    n = len(d["proposals"])
    out = [f"review: {n} page pair{'' if n == 1 else 's'} that may be one node"]
    for p in d["proposals"]:
        out += _proposal_lines(p)
    if not d["proposals"]:
        out.append("    none")
    out.append(f"pages to re-read: {len(d['reread'])}")
    for r in d["reread"]:
        out += _reread_lines(r)
    if not d["reread"]:
        out.append("    none")
    return out + _excluded_lines(d)
