"""What the table rules share: the row as the checks look at it, the edits that change a cell, the candidates."""

import re
from dataclasses import dataclass

from scat_kg.checks import fixes
from scat_kg.checks.ctx import NODE_TYPES, Ctx
from scat_kg.checks.linkedit import Literal
from scat_kg.checks.text import near_match, stem
from scat_kg.fix import FixOption
from scat_kg.graph import Cell, Row, _bars
from scat_kg.tbox import TBOX
from scat_kg.vault import Page

_LITERAL = re.compile(r"!?(\[\[([^\[\]\n]*)\]\])")
SHOWN = 5  # candidates shown for a row end


def header_text() -> str:
    return "| " + " | ".join(TBOX.table.names) + " |"


def separator_text() -> str:
    return "|" + "---|" * len(TBOX.table.columns)


@dataclass(frozen=True)
class End:
    """One end of a row: the cell, which column it is, and the layer the row's type fixes for it."""

    row: Row
    cell: Cell
    holds: str  # "from" or "to"
    layer: str | None  # None when the row's `type` is not an edge type

    @property
    def where(self) -> str:
        return f"row {self.row.n} cell `{self.holds}`"


def ends_of(row: Row) -> list[End]:
    et = TBOX.edge_types.get(row.edge_type or "")
    out = []
    for holds in ("from", "to"):
        cell = row.cell(holds)
        if cell is not None:
            layer = None if et is None else (et.from_type if holds == "from" else et.to_type)
            out.append(End(row, cell, holds, layer))
    return out


def node_layer(ctx: Ctx, name: str | None) -> str | None:
    """The layer of the node page named `name`: None unless exactly one page has the name and it is a node."""
    if name is None:
        return None
    page = ctx.page(name)
    kind = ctx.type_key(page) if page else None
    return kind if kind in NODE_TYPES else None


def literal_in(cell: Cell) -> Literal | None:
    """The first link written in a cell, with its place in the line (an embed's `!` is left out)."""
    m = _LITERAL.search(cell.raw)
    if m is None:
        return None
    return Literal(cell.column + m.start(1), m.group(1), m.group(2))


def literals_in(cell: Cell) -> list[Literal]:
    return [
        Literal(cell.column + m.start(1), m.group(1), m.group(2))
        for m in _LITERAL.finditer(cell.raw)
    ]


def delete_row(page: Page, row: Row) -> FixOption:
    return fixes.option("exact", "delete the row", fixes.delete_line(page.path, row.line, row.text))


def cell_edit(
    page: Page, cell: Cell, replace: str, find: str | None = None, column: int | None = None
):
    """Replace the content of a cell (`find` is its content as written, trimmed) at its column."""
    return fixes.replace_text(
        page.path,
        cell.line,
        cell.raw if find is None else find,
        replace,
        column=column or cell.column,
    )


def filled_row(row: Row, index: int, content: str) -> str:
    """The row line with the (empty) cell number `index` (0-based) holding `content`, padded by one space each side."""
    bars = _bars(row.text)
    a = bars[index] + 1
    b = bars[index + 1] if index + 1 < len(bars) else len(row.text.rstrip())
    return row.text[:a] + " " + content + " " + row.text[b:]


def fill_edit(page: Page, row: Row, index: int, content: str, slot: str | None = None):
    """An empty cell has no content to find: the whole row line is `find`, written again with the cell filled."""
    return fixes.replace_text(
        page.path, row.line, row.text, filled_row(row, index, content), author_slot=slot
    )


def candidates(ctx: Ctx, page: Page, text: str, layer: str | None) -> list[str]:
    """Candidates for a row end of `layer` (catalogue section 1): the near match of `text` among the pages of
    the layer's type (the node pages of every layer when it is not known), the name `text` derives when a page has
    it, then the other such pages the narrative links elsewhere, in byte order; each once."""
    types = (layer,) if layer else NODE_TYPES
    pool = ctx.names_of_type(*types)
    out = [near_match(text, pool)]
    d = stem(text)
    if d in pool:
        out.append(d)
    linked = {l.target for l in page.links}
    out += sorted((n for n in linked if n in pool), key=lambda s: s.encode())
    return [n for n in dict.fromkeys(out) if n]


def shown(names: list[str]) -> tuple[list[str], tuple[str, ...]]:
    """At most SHOWN candidates, and the note that says how many more there are."""
    if len(names) <= SHOWN:
        return names, ()
    return names[:SHOWN], (f"(+{len(names) - SHOWN} more not shown)",)
