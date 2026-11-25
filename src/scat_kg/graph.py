"""The public loader (M1): a vault folder in, the knowledge graph out; and the table-row seam.

`load(root)` reads every page as written (`vault.read_vault`), reads each narrative's table of edges under the
page contracts' reading rules (section 4), and builds the knowledge graph: nodes by layer, one edge per (type,
from, to) naming the narratives that tell it, narratives with their fingerprints, links kept apart from edges, and
the candidates of rule 4. The graph is derived and never held: every call reads the Markdown again (architecture
section 1).

Nothing here judges. A table that is malformed, a row with the wrong number of cells, an end that is no link or
no node: all are returned as data (`TableProblem`, the cells of a `Row`) for the checks to grade. A row tells an
edge only when it is a well-formed row (four cells, a closing `|`) in a well-formed table, with a type that is one
of the edge types and two ends that are each one link to a node of the layer the type fixes; anything else tells no
edge. The column names, their order, the heading and the edge types come from the TBox (R-13), never from here.

The same reading serves the row-edit builders (`add_row`, `remove_rows`), which return the new text of the file
and the edit data and leave every other line of an existing table byte-identical, so the operations and the fixes
share the one seam that knows how a table is stored.
"""

import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from scat_kg.fix import Edit
from scat_kg.tbox import TBOX
from scat_kg.vault import (
    _BODY_LINK,
    _CODE_SPAN,
    Link,
    Page,
    Vault,
    _lines,
    _split,
    fenced_lines,
    link_target,
    read_vault,
)

_HEADING = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?))?[ \t]*$")
_CLOSING_HASHES = re.compile(r"[ \t]+#+$")
_SEPARATOR_CELL = re.compile(r":?-+:?")
_ONE_LINK = re.compile(r"!?\[\[([^\[\]]*)\]\]")


def _spaces(text: str) -> str:
    """Whitespace of any kind at the ends dropped, a run inside read as one space."""
    return re.sub(r"\s+", " ", text.strip())


# ---------------------------------------------------------------------------------------------------------
# The table: data
# ---------------------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Cell:
    raw: str  # the content as written, trimmed (`\|` as written)
    text: str  # as read: `\|` is a bar, whitespace runs are one space
    line: int  # 1-based file line
    column: int  # 1-based column of the first character of `raw` (of the cell's start when empty)
    start: int  # 0-based offset in the line of the first character of `raw`
    end: int  # 0-based offset in the line after the last character of `raw`
    links: tuple[str, ...]  # the page links in the cell, as names, in order (code is not read)
    target: str | None  # the name, when the cell is exactly one link and nothing else; else None


@dataclass(frozen=True)
class Row:
    n: int  # 1-based, in the order written, the separator excluded
    line: int  # 1-based file line
    column: int  # 1-based column of the row's first `|`
    text: str  # the line as written
    cells: tuple[Cell, ...]
    closed: bool  # the row ends with an unescaped `|`
    type_text: str  # the `type` cell as read ("" when missing)
    edge_type: str | None  # the slug of the edge type the cell names (its verb or slug), else None
    from_text: str
    to_text: str
    from_target: str | None  # the name, when the `from` cell is exactly one link
    to_target: str | None
    note: str

    @property
    def well_formed(self) -> bool:
        """Four cells and a closing `|` (the number of columns is the TBox's)."""
        return self.closed and len(self.cells) == len(TBOX.table.columns)

    def cell(self, holds: str) -> Cell | None:
        """The cell of the column that holds `holds` ("edge-type", "from", "to", "note"), if the row has it."""
        i = TBOX.table.index_of(holds)
        return self.cells[i] if i < len(self.cells) else None


@dataclass(frozen=True)
class TableProblem:
    """A problem of the table's shape, as data: the catalogue grades it (U6), the loader does not."""

    kind: str  # "header", "second" or "row"
    line: int  # 1-based file line the catalogue anchors the message on
    column: int  # 1-based column (of the line's first `|` or first character)
    variant: str
    # header: "names", "order", "separator", "names+separator" or "order+separator"
    # second: "heading" (a second `Edges told` heading) or "table" (a second table under the first heading)
    # row:    "too-few" (under 3 cells), "missing-note" (3 cells, closed), "missing-note-unclosed" (3, no
    #         closing bar), "unclosed" (4 cells, no closing bar), "extra-cells" (more than 4)
    detail: str = (
        ""  # header with a separator problem: "alone" (nothing follows) or "row" (a row follows)
    )
    row: int | None = None  # kind "row": the row's number


@dataclass(frozen=True)
class Table:
    heading_line: int
    heading_level: int
    header_line: int
    header_column: int
    header: tuple[Cell, ...]
    separator_line: int | None  # None when the line after the header is not a separator row
    last_line: int  # the last line of the table: the contiguous lines that start with `|`
    well_formed: bool  # the header has the TBox's columns in order and a separator row follows
    rows: tuple[Row, ...]  # empty unless well formed


@dataclass(frozen=True)
class TableReading:
    table: Table | None  # None: no heading, or no table under it: the narrative tells no edge
    problems: tuple[TableProblem, ...]
    first_heading_line: int | None  # where the first `Edges told` heading is (for an insertion)
    first_heading_end: int | None  # the last line of that heading's section


# ---------------------------------------------------------------------------------------------------------
# The table: reading
# ---------------------------------------------------------------------------------------------------------


def _bars(line: str) -> list[int]:
    """Offsets of the `|` that end a cell: not escaped, not inside `[[ ]]`."""
    out, i, n = [], 0, len(line)
    while i < n:
        c = line[i]
        if c == "\\" and line.startswith("|", i + 1):
            i += 2
            continue
        if line.startswith("[[", i):
            j = line.find("]]", i + 2)
            if j != -1:
                i = j + 2
                continue
        if c == "|":
            out.append(i)
        i += 1
    return out


def _cell(line: str, a: int, b: int, number: int) -> Cell:
    """The cell between offsets a (after a bar) and b (the next bar, or the end of the line)."""
    raw = line[a:b]
    lead = len(raw) - len(raw.lstrip())
    content = raw.strip()
    start = a + lead if content else min(a + 1, b)
    text = _spaces(content.replace("\\|", "|"))
    blanked = _CODE_SPAN.sub(lambda m: " " * len(m.group(0)), text)
    links = tuple(
        t for m in _BODY_LINK.finditer(blanked) if (t := link_target(m.group(1))) is not None
    )
    one = _ONE_LINK.fullmatch(blanked)
    return Cell(
        raw=content,
        text=text,
        line=number,
        column=start + 1,
        start=start,
        end=start + len(content),
        links=links,
        target=link_target(one.group(1)) if one else None,
    )


def _cells(line: str, number: int) -> tuple[list[Cell], bool, int]:
    """(the cells of a table line, whether it ends with its closing bar, offset of its first bar)."""
    bars = _bars(line)
    if not bars:
        return [], False, 0
    end = len(line.rstrip())
    closed = bars[-1] == end - 1
    cells = [_cell(line, bars[k] + 1, bars[k + 1], number) for k in range(len(bars) - 1)]
    if not closed:
        cells.append(_cell(line, bars[-1] + 1, end, number))
    return cells, closed, bars[0]


def _row(n: int, line: str, number: int) -> Row:
    cells, closed, first = _cells(line, number)
    spec = TBOX.table

    def at(holds: str) -> Cell | None:
        i = spec.index_of(holds)
        return cells[i] if i < len(cells) else None

    type_cell, from_cell, to_cell, note_cell = (
        at("edge-type"),
        at("from"),
        at("to"),
        at("note"),
    )
    edge = TBOX.edge_type_named(type_cell.text) if type_cell else None
    return Row(
        n=n,
        line=number,
        column=first + 1,
        text=line,
        cells=tuple(cells),
        closed=closed,
        type_text=type_cell.text if type_cell else "",
        edge_type=edge.slug if edge else None,
        from_text=from_cell.text if from_cell else "",
        to_text=to_cell.text if to_cell else "",
        from_target=from_cell.target if from_cell else None,
        to_target=to_cell.target if to_cell else None,
        note=note_cell.text if note_cell else "",
    )


def _row_problem(row: Row) -> TableProblem | None:
    want = len(TBOX.table.columns)
    k = len(row.cells)
    if k == want and row.closed:
        return None
    if k > want:
        variant = "extra-cells"
    elif k == want:
        variant = "unclosed"
    elif k == want - 1:
        variant = "missing-note" if row.closed else "missing-note-unclosed"
    else:
        variant = "too-few"
    return TableProblem("row", row.line, row.column, variant, row=row.n)


def _is_separator(line: str) -> bool:
    cells, _, _ = _cells(line, 0)
    return bool(cells) and all(_SEPARATOR_CELL.fullmatch(c.text) for c in cells)


def _headings(lines: list[str], fenced: list[bool]) -> list[tuple[int, int, str]]:
    """(index, level, name) of every ATX heading outside a fence."""
    out = []
    for i, line in enumerate(lines):
        if fenced[i]:
            continue
        m = _HEADING.match(line)
        if m:
            out.append((i, len(m.group(1)), _CLOSING_HASHES.sub("", m.group(2) or "").strip()))
    return out


def read_table(body_lines: list[str], first_line: int) -> TableReading:
    """Read the table of edges in a narrative's body, by page contracts 4 ("Reading the table").

    `body_lines` are the lines of the body without line ends; `first_line` is the file line of the first.
    """
    spec = TBOX.table
    fenced = fenced_lines(body_lines)
    named = [h for h in _headings(body_lines, fenced) if h[2].casefold() == spec.heading.casefold()]
    if not named:
        return TableReading(None, (), None, None)
    problems: list[TableProblem] = []
    for i, _, _ in named[1:]:
        problems.append(TableProblem("second", first_line + i, 1, "heading"))
    h_index, level, _ = named[0]
    section_end = len(body_lines)
    for i, lv, _ in _headings(body_lines, fenced):
        if i > h_index and lv <= level:
            section_end = i
            break
    # the runs of table lines (contiguous, first non-space character `|`) in the first heading's section
    runs: list[tuple[int, int]] = []
    i = h_index + 1
    while i < section_end:
        if not fenced[i] and body_lines[i].lstrip().startswith("|"):
            j = i
            while (
                j + 1 < section_end
                and not fenced[j + 1]
                and body_lines[j + 1].lstrip().startswith("|")
            ):
                j += 1
            runs.append((i, j))
            i = j + 1
        else:
            i += 1
    heading_line = first_line + h_index
    if not runs:
        return TableReading(None, tuple(problems), heading_line, first_line + section_end - 1)
    for a, _ in runs[1:]:
        _, _, first = _cells(body_lines[a], first_line + a)
        problems.append(TableProblem("second", first_line + a, first + 1, "table"))
    a, b = runs[0]
    header, _, first = _cells(body_lines[a], first_line + a)
    names = [c.text.casefold() for c in header]
    want = [n.casefold() for n in spec.names]
    header_part = ""
    if names != want:
        header_part = "order" if sorted(names) == sorted(want) else "names"
    sep_ok = a + 1 <= b and _is_separator(body_lines[a + 1])
    detail = "" if sep_ok else ("row" if a + 1 <= b else "alone")
    well_formed = not header_part and sep_ok
    if not well_formed:
        variant = "+".join(v for v in (header_part, "" if sep_ok else "separator") if v)
        problems.append(TableProblem("header", first_line + a, first + 1, variant, detail=detail))
    rows: list[Row] = []
    if well_formed:
        for k, idx in enumerate(range(a + 2, b + 1), start=1):
            row = _row(k, body_lines[idx], first_line + idx)
            rows.append(row)
            p = _row_problem(row)
            if p:
                problems.append(p)
    table = Table(
        heading_line=heading_line,
        heading_level=level,
        header_line=first_line + a,
        header_column=first + 1,
        header=tuple(header),
        separator_line=first_line + a + 1 if sep_ok else None,
        last_line=first_line + b,
        well_formed=well_formed,
        rows=tuple(rows),
    )
    problems.sort(key=lambda p: (p.line, p.column, p.kind, p.variant))
    return TableReading(table, tuple(problems), heading_line, first_line + section_end - 1)


# ---------------------------------------------------------------------------------------------------------
# The knowledge graph
# ---------------------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Node:
    name: str
    type: str  # the layer: a node type of the TBox
    status: str | None
    title: str | None
    path: str


@dataclass(frozen=True)
class EdgeKey:
    type: str  # the edge type's slug
    from_node: str
    to_node: str


@dataclass(frozen=True)
class Telling:
    """One narrative's row for an edge."""

    narrative: str  # the narrative's name
    path: str
    row: int  # the row's number
    line: int
    note: str
    status: str | None  # the narrative's status as written


@dataclass(frozen=True)
class Edge:
    type: str  # slug
    from_node: str
    to_node: str
    tellings: tuple[Telling, ...]  # by narrative path, then row
    status: str  # derived: `done` when every telling narrative is `done`, else the least advanced

    @property
    def key(self) -> EdgeKey:
        return EdgeKey(self.type, self.from_node, self.to_node)

    @property
    def narratives(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(t.narrative for t in self.tellings))


@dataclass(frozen=True)
class Narrative:
    name: str
    path: str
    title: str | None
    status: str | None  # as written (None when absent)
    kind: str | None
    timeframe: str | None
    table: Table | None
    problems: tuple[TableProblem, ...]
    links: tuple[
        Link, ...
    ]  # every page link of the page: the account, the list, the table, the notes
    nodes: tuple[
        str, ...
    ]  # fingerprint: the names of the nodes it links, in layer order then by name
    edges: tuple[EdgeKey, ...]  # fingerprint: the edges its rows tell, in graph order

    @property
    def rows(self) -> tuple[Row, ...]:
        return self.table.rows if self.table else ()


@dataclass(frozen=True)
class Candidate:
    """Rule 4: a narrative links both ends of a pair and has no row for it. No message; a view lists it."""

    narrative: str
    type: str  # the edge type whose layers the pair fits
    from_node: str
    to_node: str


@dataclass(frozen=True)
class GraphLink:
    """A link, kept apart from the edges: the page that holds it and where."""

    source: str  # the page's path
    target: str
    line: int
    column: int


@dataclass(frozen=True)
class Skipped:
    """A row of a narrative's table that tells no edge, and why (a repeat of an earlier row is not one)."""

    narrative: str  # the narrative's name
    path: str
    row: int  # the row's number
    line: int
    reason: str  # plain text, no links
    fix: str | None = None  # what to do, when the reason has its own fix; else the view's usual one


@dataclass(frozen=True)
class Unreadable:
    """A page whose frontmatter cannot be read: its type is unknown, so the graph leaves it out."""

    path: str
    reason: str  # the parser's reason


@dataclass(frozen=True)
class Graph:
    root: str
    nodes: dict[str, tuple[Node, ...]]  # by layer, in the TBox's layer order; each by name
    edges: tuple[Edge, ...]
    narratives: tuple[Narrative, ...]  # by path
    candidates: tuple[Candidate, ...]
    links: tuple[GraphLink, ...]  # every link of every page, by source path and place
    vault: Vault | None = field(default=None, compare=False, repr=False)
    refusal: Any = None  # a `Refusal` (scat_kg.ops.result) when the folder is missing; else None
    skipped: tuple[Skipped, ...] = ()  # rows that tell no edge, by narrative path, then row
    unreadable: tuple[Unreadable, ...] = ()  # pages left out for frontmatter that cannot be read

    @property
    def ok(self) -> bool:
        return self.refusal is None

    def node(self, name: str) -> Node | None:
        return next((n for ns in self.nodes.values() for n in ns if n.name == name), None)

    def narrative(self, name: str) -> Narrative | None:
        return next((n for n in self.narratives if n.name == name), None)

    def edge(self, type: str, from_node: str, to_node: str) -> Edge | None:
        return next((e for e in self.edges if e.key == EdgeKey(type, from_node, to_node)), None)

    def summary(self) -> dict:
        """Counts and the edges, for a quick look."""
        return {
            "nodes": {layer: len(ns) for layer, ns in self.nodes.items()},
            "narratives": len(self.narratives),
            "edges": len(self.edges),
            "edge_status": {s: sum(e.status == s for e in self.edges) for s in TBOX.statuses},
            "candidates": len(self.candidates),
            "links": len(self.links),
        }


def _rank(status: Any) -> int:
    """Position in the lifecycle; a missing or invalid status is the least advanced."""
    return TBOX.statuses.index(status) if status in TBOX.statuses else -1


def derived_status(statuses: Iterable[Any]) -> str:
    """`done` when every status is `done`, else the least advanced (an invalid one counts as `stub`)."""
    least = min(statuses, key=_rank)
    return least if _rank(least) >= 0 else TBOX.statuses[0]


def _text_field(page: Page, key: str) -> str | None:
    v = page.fields.get(key)
    return v if isinstance(v, str) else None


def _empty(root: str, refusal: Any) -> Graph:
    return Graph(root, {t: () for t in TBOX.layers}, (), (), (), (), None, refusal)


RENAME_FIX = "rename one of the pages so the name is carried by one page (`scat check` names them), then run this again"


def _end_problem(vault: Vault, nodes: dict, end: str, target: str | None) -> str | None:
    """Why a row's end reaches no node, in plain words; None when it reaches exactly one node page."""
    if target is None:
        return f"the `{end}` cell is empty or is not exactly one link"
    found = vault.by_name.get(target, ())
    if not found:
        return f"the `{end}` end `{target}` reaches no page"
    if len(found) > 1:
        paths = ", ".join(sorted(p.path for p in found))
        return f"the `{end}` end `{target}` is carried by more than one page: {paths}"
    if found[0].type not in nodes:
        return f"the `{end}` end `{target}` reaches a page that is not a node"
    return None


def load(root: str | Path) -> Graph:
    """Read the vault at `root` into its knowledge graph. A missing folder is a refusal, not an exception."""
    path = Path(root)
    if not path.is_dir():
        from scat_kg.ops.result import Refusal  # not at import: the operations import this module

        return _empty(
            str(root),
            Refusal(
                str(path),
                "the vault folder does not exist",
                "pass the vault folder (the one that holds `scat.toml`), or run from inside it",
            ),
        )
    vault = read_vault(path)
    layers = TBOX.layers
    layer_index = {t: i for i, t in enumerate(layers)}
    type_index = {s: i for i, s in enumerate(TBOX.edge_types)}

    nodes: dict[str, list[Node]] = {t: [] for t in layers}
    for p in vault.pages:
        if p.type in nodes:
            nodes[p.type].append(
                Node(p.name, p.type, _text_field(p, "status"), _text_field(p, "title"), p.path)
            )
    for ns in nodes.values():
        ns.sort(key=lambda n: (n.name, n.path))

    def node_of(name: str | None) -> Node | None:
        """The node a name reaches: one page of that name, and it is a node page."""
        found = vault.by_name.get(name or "", ())
        if len(found) != 1 or found[0].type not in nodes:
            return None
        return next(n for n in nodes[found[0].type] if n.path == found[0].path)

    narratives: list[Narrative] = []
    told: dict[EdgeKey, list[Telling]] = {}
    candidates: list[Candidate] = []
    skipped: list[Skipped] = []
    table_type = TBOX.table_type.slug
    for p in vault.pages:
        if p.type != table_type or p.frontmatter_error is not None:
            continue
        reading = read_table(p.body.split("\n"), p.body_line)
        table = reading.table
        status = _text_field(p, "status")
        own: dict[EdgeKey, Telling] = {}
        for row in table.rows if table else ():
            et = TBOX.edge_types.get(row.edge_type or "")
            a = b = None
            why = None
            if not row.well_formed:
                why = "the row is not well-formed (four cells and a closing bar)"
            elif et is None:
                why = f"`{row.type_text}` is not an edge type"
            else:
                for end, target in (("from", row.from_target), ("to", row.to_target)):
                    why = _end_problem(vault, nodes, end, target)
                    if why:
                        break
                if why is None:
                    a, b = node_of(row.from_target), node_of(row.to_target)
                    if (a.type, b.type) != (et.from_type, et.to_type):
                        why = (
                            f"the ends are a {a.type} and a {b.type}, in the wrong direction or "
                            f"between layers that do not neighbour; `{et.slug}` joins a "
                            f"{et.from_type} to a {et.to_type}"
                        )
            if why:
                fix = RENAME_FIX if "is carried by more than one page" in why else None
                skipped.append(Skipped(p.name, p.path, row.n, row.line, why, fix))
                continue
            key = EdgeKey(et.slug, a.name, b.name)
            own.setdefault(key, Telling(p.name, p.path, row.n, row.line, row.note, status))
        for key, telling in own.items():
            told.setdefault(key, []).append(telling)
        linked = {n.name: n for l in p.links if (n := node_of(l.target)) is not None}
        fingerprint = sorted(linked.values(), key=lambda n: (layer_index[n.type], n.name))
        edge_keys = tuple(sorted(own, key=lambda k: (type_index[k.type], k.from_node, k.to_node)))
        narratives.append(
            Narrative(
                name=p.name,
                path=p.path,
                title=_text_field(p, "title"),
                status=status,
                kind=_text_field(p, "kind"),
                timeframe=_text_field(p, "timeframe"),
                table=table,
                problems=reading.problems,
                links=p.links,
                nodes=tuple(n.name for n in fingerprint),
                edges=edge_keys,
            )
        )
        # rule 4: both ends of a pair linked, no row for it (a row of the pair, either way round, is a row)
        rowed = {(r.from_target, r.to_target) for r in (table.rows if table else ())}
        rowed |= {(b, a) for a, b in rowed}
        for et in TBOX.edge_types.values():
            for a in (n for n in fingerprint if n.type == et.from_type):
                for b in (n for n in fingerprint if n.type == et.to_type):
                    if (
                        EdgeKey(et.slug, a.name, b.name) not in own
                        and (a.name, b.name) not in rowed
                    ):
                        candidates.append(Candidate(p.name, et.slug, a.name, b.name))
    edges = tuple(
        Edge(
            key.type,
            key.from_node,
            key.to_node,
            tuple(sorted(ts, key=lambda t: (t.path, t.row))),
            derived_status(t.status for t in ts),
        )
        for key, ts in sorted(
            told.items(), key=lambda kv: (type_index[kv[0].type], kv[0].from_node, kv[0].to_node)
        )
    )
    candidates.sort(key=lambda c: (type_index[c.type], c.from_node, c.to_node, c.narrative))
    links = tuple(
        GraphLink(p.path, l.target, l.line, l.column)
        for p in vault.pages
        for l in sorted(p.links, key=lambda l: (l.line, l.column, l.target))
    )
    return Graph(
        root=str(root),
        nodes={t: tuple(ns) for t, ns in nodes.items()},
        edges=edges,
        narratives=tuple(narratives),
        candidates=tuple(candidates),
        links=links,
        vault=vault,
        skipped=tuple(skipped),
        unreadable=tuple(
            Unreadable(p.path, p.frontmatter_error.reason)
            for p in vault.pages
            if p.frontmatter_error is not None
        ),
    )


# ---------------------------------------------------------------------------------------------------------
# Row-edit builders: the one seam that writes a table, for the operations and the fixes
# ---------------------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class RowEdit:
    """The result of a builder: the new text of the file and the edits that make it, or why it cannot."""

    text: str | None  # the new file text; None when refused
    edits: tuple[Edit, ...] = ()
    refusal: str | None = None

    @property
    def ok(self) -> bool:
        return self.refusal is None

    @property
    def changed(self) -> bool:
        return self.ok and bool(self.edits)


def _refuse(why: str) -> RowEdit:
    return RowEdit(None, (), why)


def _cell_text(text: str) -> str:
    return " ".join(text.replace("|", "\\|").split())


def format_row(edge_type: str, from_node: str, to_node: str, note: str = "") -> str:
    """A row as the tools write it: the verb, both ends as links, the note with its bars escaped."""
    et = TBOX.edge_type_named(edge_type)
    verb = et.verb if et else edge_type
    row = f"| {verb} | [[{from_node}]] | [[{to_node}]] | {_cell_text(note)} |"
    return row.replace("|  |", "| |")


def _header_lines() -> list[str]:
    cols = TBOX.table.names
    return ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]


def _open(text: str) -> tuple[list[str], int, TableReading] | str:
    """(the file's lines with their `\\r` kept, the index of the first body line, the table reading) or why not."""
    raw = text.split("\n")
    plain = _lines(text)
    close, opens = _split(plain)
    if not opens or close is None:
        return "the file has no readable frontmatter, so it is not a page"
    body = plain[close + 1 :]
    return raw, close + 1, read_table(body, close + 2)


def add_row(
    text: str, path: str, edge_type: str, from_node: str, to_node: str, note: str = ""
) -> RowEdit:
    """The file with one row added to its table of edges (written as `format_row` does).

    A table with a well-formed header gets the row after its last line. With a heading and no table, the table
    (header, separator, the row) goes under the heading. With no heading, the heading `## Edges told` and the table
    go at the end of the file. A table whose header is malformed is refused: its rows are not read, so a row added
    to it would tell no edge. Every other line is kept byte-identical.
    """
    if TBOX.edge_type_named(edge_type) is None:
        return _refuse(f"`{edge_type}` is not an edge type")
    opened = _open(text)
    if isinstance(opened, str):
        return _refuse(opened)
    raw, _, reading = opened
    eol = "\r\n" if "\r\n" in text else "\n"
    row = format_row(edge_type, from_node, to_node, note)
    table = reading.table
    if table is not None and not table.well_formed:
        return _refuse("the table's header or separator row is malformed; correct it first")
    if table is not None:
        at = table.last_line  # 1-based: append after the last line of the table
        anchor = raw[at - 1].removesuffix("\r")
        lines = raw[:at] + [row + ("\r" if eol == "\r\n" else "")] + raw[at:]
        edit = Edit(
            "replace-text", path, line=at, column=1, find=anchor, replace=anchor + "\n" + row
        )
        return RowEdit("\n".join(lines), (edit,))
    block = [*_header_lines(), row]
    if reading.first_heading_line is not None:  # a heading, no table under it
        at = reading.first_heading_line
        anchor = raw[at - 1].removesuffix("\r")
        after = raw[at] if at < len(raw) else ""
        tail = "" if not after.strip() else "\n"  # a blank line before the text that follows
        new = [anchor, "", *block]
        lines = (
            raw[: at - 1]
            + [x + ("\r" if eol == "\r\n" else "") for x in new]
            + ([("\r" if eol == "\r\n" else "")] if tail else [])
            + raw[at:]
        )
        edit = Edit(
            "replace-text", path, line=at, column=1, find=anchor,
            replace="\n".join(new) + tail,
        )  # fmt: skip
        return RowEdit("\n".join(lines), (edit,))
    heading = "## " + TBOX.table.heading
    ends_nl = text.endswith("\n")
    body = raw[:-1] if ends_nl else raw
    last = len(body)
    anchor = body[-1].removesuffix("\r") if body else ""
    added = ["", heading, "", *block]
    cr = "\r" if eol == "\r\n" else ""
    lines = body + [x + cr for x in added] + ([""] if ends_nl else [])
    edit = Edit(
        "replace-text", path, line=max(last, 1), column=1, find=anchor,
        replace=anchor + "".join("\n" + x for x in added),
    )  # fmt: skip
    return RowEdit("\n".join(lines), (edit,))


def remove_rows(text: str, path: str, rows: Iterable[int]) -> RowEdit:
    """The file with the rows numbered `rows` (as `Row.n`) deleted; every other line is kept byte-identical.

    The heading, the header and the separator stay even when no row is left. A number that is no row is refused.
    """
    wanted = sorted(set(rows))
    opened = _open(text)
    if isinstance(opened, str):
        return _refuse(opened)
    raw, _, reading = opened
    have = {r.n: r for r in (reading.table.rows if reading.table else ())}
    missing = [n for n in wanted if n not in have]
    if missing:
        return _refuse("no such row in the table: " + ", ".join(map(str, missing)))
    drop = {have[n].line for n in wanted}
    edits = tuple(Edit("delete-line", path, line=have[n].line, find=have[n].text) for n in wanted)
    return RowEdit("\n".join(x for i, x in enumerate(raw, start=1) if i not in drop), edits)
