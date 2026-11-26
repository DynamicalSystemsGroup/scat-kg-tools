"""The copy-share view: how much of each node page repeats a narrative.

    scat_kg.copy_share()                   # every node page, the most repeated first
    scat_kg.copy_share("community-members")   # one node page

For a node page it reports the share of the page's five-word runs that appear word for word in any narrative. A
page that pastes one narrative's paragraph scores near 1; a page written across narratives scores low. A high share
is a prompt to look at the page (`scat evidence <node>` shows the narratives), not a fault.

What is compared. The page's text is its `description` and its body, without the `Edges told` section if it has one.
A narrative's text is its body. Both are lower-cased and cut into words (letters, digits and apostrophes): a link
counts as its shown text (its name when it shows none), and punctuation, line breaks and table bars count for
nothing, so a run may span a sentence or a list item. A run is five words in a row; a repeated run counts once.
A narrative that links no node page is excluded: its text is not compared, and it is listed under `excluded` as in
the other views.

Each entry gives the page's `name`, `type`, `status`, the number of `words` in its text, the `share` (0 to 1, or
null when the page has fewer than five words, as a stub has), and the `narratives` the repeated runs come from, the
one with most runs first (then by name). Entries are sorted by share, highest first, a null share last, then by
name. The view reads no narrative's `attributed_to` and lists no contributor page. Writes nothing.
"""

import re
from pathlib import Path

from scat_kg.graph import Graph, Node
from scat_kg.ops.result import reports_mode
from scat_kg.views import (
    Refused,
    View,
    _check,
    _excluded,
    _excluded_lines,
    _open,
    _page_named,
    _unreadable,
)
from scat_kg.views import (
    _text as _guard,
)

RUN = 5  # words in a run

_LINK = re.compile(r"\[\[([^\]|]*)(?:\|([^\]]*))?\]\]")
_HEADING = re.compile(r"(?m)^(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$")
_WORD = re.compile(r"[a-z0-9']+")


def _without_edges_told(body: str) -> str:
    """The body without its `Edges told` section: from that heading to the next heading of the same or a higher level."""
    found = next((m for m in _HEADING.finditer(body) if m.group(2).lower() == "edges told"), None)
    if found is None:
        return body
    level = len(found.group(1))
    after = next(
        (m for m in _HEADING.finditer(body, found.end()) if len(m.group(1)) <= level), None
    )
    return body[: found.start()] + (body[after.start() :] if after else "")


def _words(text: str) -> list[str]:
    shown = _LINK.sub(lambda m: m.group(2) if m.group(2) is not None else m.group(1), text)
    return _WORD.findall(shown.lower().replace("’", "'"))


def _runs(words: list[str]) -> set[tuple[str, ...]]:
    return {tuple(words[i : i + RUN]) for i in range(len(words) - RUN + 1)}


def _entry(node: Node, words: list[str], corpus: dict[str, set]) -> dict:
    mine = _runs(words)
    counts = {name: len(mine & runs) for name, runs in corpus.items()}
    repeated = set().union(*(mine & runs for runs in corpus.values())) if corpus else set()
    return {
        "name": node.name,
        "type": node.type,
        "status": node.status,
        "words": len(words),
        "share": round(len(repeated) / len(mine), 3) if mine else None,
        "narratives": [n for n in sorted(counts, key=lambda n: (-counts[n], n)) if counts[n]],
    }


class CopyShareView(View):
    """The copy-share view: the data of `View`, and a text form that begins with the vault's attribution mode."""

    def __str__(self) -> str:
        head = f"attribution mode: {self.mode or 'not declared'}"
        return "\n".join([head, *_lines(self.data)])

    __repr__ = __str__


@reports_mode
def copy_share(node: str | None = None, *, root: str | Path = ".") -> View | Refused:
    """The share of each node page's five-word runs that appear word for word in a narrative; one node page
    when `node` is named, else every node page."""
    op = "copy-share"
    if node is not None and (bad := _guard(op, node, "a node name")):
        return bad
    g, bad = _open(op, root)
    if bad:
        return bad
    if node is not None and (bad := _page_named(op, g, node, "node")):
        return bad
    nodes = [n for ns in g.nodes.values() for n in ns if node in (None, n.name)]
    bad = _check(op, g, [n.name for n in g.narratives], nodes, ()) or (
        _unreadable(op, g) if node is None else None
    )
    if bad:
        return bad
    pages = {p.path: p for p in g.vault.pages}
    corpus = {n.name: _runs(_words(pages[n.path].body)) for n in g.narratives}
    return CopyShareView(op, {"pages": _pages(g, nodes, pages, corpus), "excluded": _excluded(g)})


def _pages(g: Graph, nodes: list[Node], pages: dict, corpus: dict[str, set]) -> list[dict]:
    out = []
    for n in nodes:
        page = pages[n.path]
        desc = page.fields.get("description")
        text = (desc if isinstance(desc, str) else "") + "\n\n" + _without_edges_told(page.body)
        out.append(_entry(n, _words(text), corpus))
    # the highest share first, a null share last, then by name
    return sorted(out, key=lambda e: (e["share"] is None, -(e["share"] or 0), e["name"]))


# ---------------------------------------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------------------------------------


def _line(e: dict) -> str:
    head = f"    {e['name']} ({e['type']}, {e['status']}): {e['words']} words, "
    if e["share"] is None:
        return head + f"no share (fewer than {RUN} words)"
    from_ = f"; from {', '.join(e['narratives'])}" if e["narratives"] else ""
    return head + f"share {e['share']:.2f}{from_}"


def _lines(d: dict) -> list[str]:
    n = len(d["pages"])
    out = [f"copy-share: {n} node page{'' if n == 1 else 's'}"]
    out += [_line(e) for e in d["pages"]] or ["    none"]
    return out + _excluded_lines(d)
