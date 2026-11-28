"""The evidence view: everything the vault says of one node page, in one document.

    scat_tools.evidence("community-members")   # narratives, paragraphs, edges and adjacent nodes of one node

For one node page it returns the narratives that link it (name, status, kind, timeframe); for each, the paragraphs
around its links, as written, with the linking sentence marked; whether the narrative tells an edge for the node;
the node's edges, each with the narratives that tell it and the row's note; and the adjacent nodes (one edge away),
by layer. It is a view of the four layers: it never reads a narrative's `attributed_to` and never lists a
contributor page. A paragraph is the coder's own text, returned as written. Writes nothing.

A paragraph is the lines between blank lines; a line that starts with `|` (a row of any table) is a block of its own,
whole, never cut into sentences. A link inside the `Edges told` table is not in a paragraph (the
table's rows show through the node's edges), and neither is a table line next to one. A sentence runs to the next
`.`, `!` or `?` that is followed by white space or the end of the paragraph (never inside a link), or to the end of
the line before a list item; a list item's marker is no part of a sentence; so an abbreviation such as `e.g.` ends
one. Each sentence that holds a link is given as `text`, with `start` and `end`: 0-based character offsets in the
paragraph, `paragraph[start:end] == text`. The text form puts `>>` before and `<<` after each such sentence. A
paragraph with several links is one entry.
"""

import re
from pathlib import Path

from scat_tools.graph import Graph, Narrative
from scat_tools.ops.result import reports_mode
from scat_tools.tbox import TBOX
from scat_tools.views import (
    Refused,
    View,
    _drawn,
    _edge,
    _edge_line,
    _excluded,
    _excluded_lines,
    _node,
    _node_line,
    _nodes,
    _open,
    _page_named,
)
from scat_tools.views import (
    _text as _guard,
)

_END = re.compile(r"[.!?][)\]\"'\u201d\u2019]*(?=\s|$)")
_MARK = re.compile(r"[ \t]*(?:[-*+]|\d+[.)])[ \t]+")  # a list item's marker, at the start of a line


def _bounds(paragraph: str) -> list[tuple[int, int]]:
    """The sentences of a paragraph as (start, end) offsets: white space and a list item's marker left out."""
    if paragraph.lstrip().startswith("|"):  # a table row is one unit, never cut across cells
        return [(len(paragraph) - len(paragraph.lstrip()), len(paragraph.rstrip()))]
    cuts, skips, i = [], {}, 0
    while i < len(paragraph):
        if (i == 0 or paragraph[i - 1] == "\n") and (m := _MARK.match(paragraph, i)):
            skips[i] = m.end()
            if i:
                cuts.append(i - 1)  # a list item starts: the line before ends a sentence
            i = m.end()
            continue
        if paragraph.startswith("[[", i) and (j := paragraph.find("]]", i)) != -1:
            i = j + 2
        elif m := _END.match(paragraph, i):
            cuts.append(m.end())
            i = m.end()
        else:
            i += 1
    out, start = [], 0
    for end in sorted({*cuts, len(paragraph)}):
        a = start
        while a < end and paragraph[a].isspace():
            a += 1
        a = max(a, next((e for s0, e in skips.items() if s0 <= a < e), a))
        z = len(paragraph[:end].rstrip())
        if a < z:
            out.append((a, z))
        start = end
    return out


def _paragraphs(nar: Narrative, name: str, body: str, body_line: int) -> list[dict]:
    """The paragraphs of a narrative's body that link `name`: each with its sentences that hold a link."""
    lines = body.split("\n")
    table = nar.table
    skip = range(table.header_line - body_line, table.last_line - body_line + 1) if table else ()
    blocks, here = [], []
    for k, ln in enumerate(lines):
        if (
            ln.lstrip().startswith("|") and k not in skip
        ):  # a row of another table: a block of its own
            if here:
                blocks.append(here)
            blocks.append([k])
            here = []
        elif ln.strip() and k not in skip:
            here.append(k)
        elif here:
            blocks.append(here)
            here = []
    if here:
        blocks.append(here)
    where = {}  # the block of each body line, and the offset of the line's start in the paragraph
    for b, ks in enumerate(blocks):
        off = 0
        for k in ks:
            where[k] = (b, off)
            off += len(lines[k]) + 1
    found: dict[int, list[int]] = {}
    for link in nar.links:
        k = link.line - body_line
        if link.target == name and k in where:
            b, off = where[k]
            found.setdefault(b, []).append(off + link.column - 1)
    out = []
    for b in sorted(found):
        paragraph = "\n".join(lines[k] for k in blocks[b])
        spans = _bounds(paragraph)
        mine = [s for s in spans if any(s[0] <= at < s[1] for at in found[b])]
        out.append(
            {
                "line": body_line + blocks[b][0],
                "paragraph": paragraph,
                "sentences": [{"text": paragraph[a:z], "start": a, "end": z} for a, z in mine],
            }
        )
    return out


def _entry(g: Graph, nar: Narrative, name: str, pages: dict) -> dict:
    page = pages[nar.path]
    return {
        "name": nar.name,
        "status": nar.status,
        "kind": nar.kind,
        "timeframe": nar.timeframe,
        "tells_edge": any(name in (k.from_node, k.to_node) for k in nar.edges),
        "paragraphs": _paragraphs(nar, name, page.body, page.body_line),
    }


class EvidenceView(View):
    """The evidence view: the data of `View`, and a text form that begins with the vault's attribution mode."""

    def __str__(self) -> str:
        head = f"attribution mode: {self.mode or 'not declared'}"
        return "\n".join([head, *_lines(self.data)])

    __repr__ = __str__


@reports_mode
def evidence(node: str, *, root: str | Path = ".") -> View | Refused:
    """Everything the vault says of one node page: the narratives that link it with the paragraph of each
    link, its edges with the narratives that tell them, and its adjacent nodes."""
    op = "evidence"
    if bad := _guard(op, node, "a node name"):
        return bad
    g, bad = _open(op, root)
    if bad:
        return bad
    if bad := _page_named(op, g, node, "node"):
        return bad
    pages = {p.path: p for p in g.vault.pages}
    linking = [n for n in g.narratives if node in n.nodes]
    edges = [e for e in g.edges if node in (e.from_node, e.to_node)]
    near = {x for e in edges for x in (e.from_node, e.to_node)} - {node}
    names = [n.name for n in linking]
    bad = _drawn(op, g, names, _nodes(g, near | {node}), edges, names, True)
    if bad:
        return bad
    me = g.node(node)
    adjacent = _nodes(g, near)
    return EvidenceView(
        op,
        {
            "node": node,
            "node_type": me.type,
            "node_status": me.status,
            "narratives": [_entry(g, n, node, pages) for n in linking],
            "edges": [
                {
                    **_edge(e),
                    "tellings": [{"narrative": t.narrative, "note": t.note} for t in e.tellings],
                }
                for e in edges
            ],
            "adjacent": {
                layer: [_node(n) for n in adjacent if n.type == layer] for layer in TBOX.layers
            },
            "excluded": _excluded(g),
        },
    )


# ---------------------------------------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------------------------------------


def _marked(p: dict) -> str:
    """The paragraph with `>>` before and `<<` after each marked sentence."""
    text = p["paragraph"]
    for s in reversed(p["sentences"]):
        text = text[: s["start"]] + ">>" + s["text"] + "<<" + text[s["end"] :]
    return text


def _lines(d: dict) -> list[str]:
    says = f"{d['node_type']}, {d['node_status']}"
    n, e = len(d["narratives"]), len(d["edges"])
    counts = f"{n} narrative{'' if n == 1 else 's'}, {e} edge{'' if e == 1 else 's'}"
    out = [f"evidence {d['node']} ({says}): {counts}"]
    out.append("  narratives (the sentence with the link is between >> and <<)")
    for n in d["narratives"]:
        says = ", ".join(x for x in (n["status"], n["kind"], n["timeframe"]) if x)
        flag = "" if n["tells_edge"] else "; tells no edge for this node"
        out.append(f"    {n['name']} [{says}]{flag}")
        for p in n["paragraphs"]:
            out.append(f"      line {p['line']}")
            out += ["        " + ln for ln in _marked(p).split("\n")]
    if not d["narratives"]:
        out.append("    none")
    out.append("  edges")
    for e in d["edges"]:
        out.append(_edge_line(e))
        out += [f"        {t['narrative']}: {t['note'] or '(no note)'}" for t in e["tellings"]]
    if not d["edges"]:
        out.append("    none")
    out.append("  adjacent nodes")
    for layer in TBOX.layers:
        if d["adjacent"][layer]:
            out += [f"    {layer}", *("  " + _node_line(n) for n in d["adjacent"][layer])]
    if not any(d["adjacent"].values()):
        out.append("    none")
    return out + _excluded_lines(d)
