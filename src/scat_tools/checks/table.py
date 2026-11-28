"""The pairs of a narrative's table: SCAT-DRAFT-TABLE-* and SCAT-DONE-TABLE-* (catalogue, "Pairs: the table").

A pair is one condition with two ids: a warning while the narrative is `stub` or `draft`, an error at `done`.
A table with a malformed header is reported once and its rows are read by no row rule (cascade guard).
"""

from scat_tools.checks import fixes
from scat_tools.checks.ctx import Ctx, page_rule
from scat_tools.checks.rows import (
    delete_row,
    fill_edit,
    header_text,
    node_layer,
    separator_text,
)
from scat_tools.checks.text import article, near_match
from scat_tools.fix import FixOption
from scat_tools.graph import Row, TableProblem, _bars, _cells
from scat_tools.tbox import TBOX
from scat_tools.vault import Page

NAMES = ", ".join(TBOX.table.names)  # from, type, to, note


def _spellings() -> list[str]:
    return [s for e in TBOX.edge_types.values() for s in e.spellings]


def _verbs() -> str:
    return ", ".join(e.verb for e in TBOX.edge_types.values())


def _is_row(line: str) -> bool:
    """Whether the line after a header is a row (it links something or starts with an edge type), not a bad separator."""
    cells, _, _ = _cells(line, 0)
    i = TBOX.table.index_of("edge-type")
    return "[[" in line or bool(len(cells) > i and TBOX.edge_type_named(cells[i].text))


def _joins_header(ctx: Ctx, page: Page, tp: TableProblem, headers: list[int]) -> bool:
    """Whether a "second table" starts in the lines run on from a malformed header (no blank line between):
    its first row follows a separator the reader did not take, so it is the same table."""
    return any(
        h < tp.line and all(ctx.body_text(page, n).strip() for n in range(h, tp.line))
        for h in headers
    )


def _header(ctx: Ctx, page: Page, rule: str, tp: TableProblem):
    header = ctx.body_text(page, tp.line).strip()
    names_wrong, order_wrong = tp.variant.startswith("names"), tp.variant.startswith("order")
    sep_wrong = "separator" in tp.variant
    second = None if tp.detail == "alone" else ctx.body_text(page, tp.line + 1).strip()
    right, sep = header_text(), separator_text()
    if names_wrong or order_wrong:
        what = f"the header row is `{header}`, not `{right}`"
    elif second is None:
        what = "there is no separator row after the header row"
    else:
        what = f"the line after the header row is `{second}`, not a separator row"
    if order_wrong:
        fix = fixes.single(
            FixOption(
                "advisory",
                f"reorder the columns to {', '.join(f'`{n}`' for n in TBOX.table.names)}: in the "
                "header and in every row, move the cells into this order; the tool never moves cells",
            )
        )
    elif sep_wrong and (
        second is None or _is_row(second)
    ):  # no separator row: the second line is a row
        head = right if names_wrong else header
        fix = fixes.single(
            fixes.option(
                "exact",
                f"replace the line `{header}` with two lines, `{head}` then `{sep}`",
                fixes.replace_text(page.path, tp.line, header, f"{head}\n{sep}"),
            )
        )
    elif sep_wrong:  # a separator row that is not one
        edits = [fixes.replace_text(page.path, tp.line + 1, second or "", sep)]
        text = f"replace the line `{second}` with `{sep}`"
        if names_wrong:
            edits.insert(0, fixes.replace_text(page.path, tp.line, header, right))
            text = (
                f"replace the line `{header}` with `{right}` and the line `{second}` with `{sep}`"
            )
        fix = fixes.single(fixes.option("exact", text, *edits))
    else:
        fix = fixes.single(
            fixes.option(
                "exact",
                f"replace the line `{header}` with `{right}`",
                fixes.replace_text(page.path, tp.line, header, right),
            )
        )
    return ctx.problem(rule, page.path, "table header", what, fix, line=tp.line, column=tp.column)


def _row_problem(ctx: Ctx, page: Page, rule: str, tp: TableProblem, row: Row):
    k, v = len(row.cells), tp.variant
    what = (
        "the row does not end with `|`"
        if v == "unclosed"
        else f"the row has {k} cells, not {len(TBOX.table.columns)} ({NAMES})"
    )
    delete = delete_row(page, row)
    if v == "missing-note":
        end = len(row.text.rstrip())  # the column of the final `|`
        fix = fixes.single(
            fixes.option(
                "exact",
                "add an empty note: replace the final `|` with `| |`",
                fixes.replace_text(page.path, row.line, "|", "| |", column=end),
            )
        )
    elif v in ("unclosed", "missing-note-unclosed"):
        last = row.cells[-1].raw
        tail, why = (
            (" |", "")
            if v == "unclosed"
            else (" | |", ", which adds the empty note and the closing bar")
        )
        fix = fixes.single(
            fixes.option(
                "exact",
                f"write `{tail}` after the last cell{why}: replace `{last}` with `{last}{tail}`",
                fixes.replace_text(
                    page.path, row.line, last, last + tail, column=row.cells[-1].column
                ),
            )
        )
    elif v == "extra-cells":
        bars = _bars(row.text)
        extra = bars[len(TBOX.table.columns) :]
        if row.closed:
            extra = extra[:-1]
        edits = [
            fixes.replace_text(page.path, row.line, "|", "\\|", column=b + 1)
            for b in reversed(extra)
        ]
        fix = fixes.alternatives(
            [
                fixes.option(
                    "exact",
                    "a `|` inside the note is written `\\|`: replace the `|` that opens cell "
                    f"{len(TBOX.table.columns) + 1} and the ones after it with `\\|`",
                    *edits,
                ),
                delete,
            ]
        )
    else:  # too few cells
        fix = fixes.alternatives(
            [
                delete,
                FixOption(
                    "advisory",
                    "write the row again with four cells and a closing `|`: "
                    f"`| {' | '.join(TBOX.table.names)} |`",
                ),
            ]
        )
    return ctx.problem(rule, page.path, f"row {row.n}", what, fix, line=row.line, column=row.column)


def _second(ctx: Ctx, page: Page, rule: str, tp: TableProblem, first_line: int):
    heading = tp.variant == "heading"
    thing = f"heading `{TBOX.table.heading}`" if heading else "table"
    what = (
        f"a second {thing} on this narrative; only the first table under the first "
        f"`{TBOX.table.heading}` is read, so its rows tell no edge"
    )
    opts = [
        FixOption(
            "advisory",
            f"move the rows you want into the first table (line {first_line}), then delete this "
            f"{'heading and table' if heading else 'table'}",
        )
    ]
    if heading:
        written = ctx.body_text(page, tp.line).strip()
        hashes = written.split(" ")[0]
        slot = "<heading you choose>"
        opts.append(
            fixes.option(
                "slot",
                f"replace the heading `{written}` with `{hashes} {slot}` (author), so it is no longer "
                f"an `{TBOX.table.heading}` heading",
                fixes.replace_text(
                    page.path, tp.line, written, f"{hashes} {slot}", author_slot=slot
                ),
            )
        )
    fix = fixes.alternatives(opts)
    return ctx.problem(rule, page.path, "table", what, fix, line=tp.line, column=tp.column)


def _type(ctx: Ctx, page: Page, rule: str, row: Row):
    cell = row.cell("edge-type")
    value = cell.raw
    what = (
        f"`{value}` is not an edge type ({_verbs()})"
        if value
        else f"the value is empty, which is not an edge type ({_verbs()})"
    )
    spec = TBOX.table

    def put(verb: str) -> FixOption:
        if value:
            edit = fixes.replace_text(page.path, cell.line, value, verb, column=cell.column)
            return fixes.option("exact", f"replace `{value}` with `{verb}`", edit)
        index = spec.index_of("edge-type")
        return fixes.option(
            "exact", f"replace the empty cell with `{verb}`", fill_edit(page, row, index, verb)
        )

    a, b = node_layer(ctx, row.from_target), node_layer(ctx, row.to_target)
    spelled = []
    et = TBOX.edge_type_between(a, b) if a and b else None
    if et is not None:
        spelled.append(et.verb)
    near = near_match(value, _spellings()) if value else None
    if near:
        spelled.append(near)
    if not spelled:
        spelled = [e.verb for e in TBOX.edge_types.values()]
    opts = [put(v) for v in dict.fromkeys(spelled)]
    opts.append(delete_row(page, row))
    return ctx.problem(
        rule,
        page.path,
        f"row {row.n} cell `type`",
        what,
        fixes.alternatives(opts),
        line=cell.line,
        column=cell.column,
    )


def _layers(ctx: Ctx, page: Page, rule: str, row: Row):
    et = TBOX.edge_types[row.edge_type]
    want = {"from": et.from_type, "to": et.to_type}
    have = {"from": node_layer(ctx, row.from_target), "to": node_layer(ctx, row.to_target)}
    wrong = [h for h in ("from", "to") if have[h] is not None and have[h] != want[h]]
    if not wrong:
        return None
    ends = {"from": row.from_target, "to": row.to_target}
    said = [f"[[{ends[h]}]] is {article(have[h])} {have[h]} page" for h in wrong]
    what = (
        f"`{et.verb}` joins {article(et.from_type)} {et.from_type} to {article(et.to_type)} "
        f"{et.to_type}, but {', and '.join(said)}"
    )
    opts: list[FixOption] = []
    a, b = have["from"], have["to"]
    swap = (a is None or a == want["to"]) and (b is None or b == want["from"])
    f_cell, t_cell = row.cell("from"), row.cell("to")
    if swap:
        find = row.text[f_cell.start : t_cell.end]
        new = t_cell.raw + row.text[f_cell.end : t_cell.start] + f_cell.raw
        opts.append(
            fixes.option(
                "exact",
                f"swap the two ends: replace `{find}` with `{new}`",
                fixes.replace_text(page.path, row.line, find, new, column=f_cell.column),
            )
        )
    other = TBOX.edge_type_between(a, b) if a and b else None
    if other is not None and not swap:
        tc = row.cell("edge-type")
        opts.append(
            fixes.option(
                "exact",
                f"replace `{tc.raw}` with `{other.verb}`",
                fixes.replace_text(page.path, tc.line, tc.raw, other.verb, column=tc.column),
            )
        )
    if not opts:
        x, y = a or want["from"], b or want["to"]
        opts.append(
            FixOption(
                "advisory",
                f"none of the three edge types joins {article(x)} {x} to {article(y)} {y}: "
                "tell it as two rows through a node between them",
            )
        )
    opts.append(delete_row(page, row))
    return ctx.problem(
        rule,
        page.path,
        f"row {row.n}",
        what,
        fixes.alternatives(opts),
        line=row.line,
        column=row.column,
    )


def _duplicate(ctx: Ctx, page: Page, rule: str, row: Row, first: Row):
    et = TBOX.edge_types[row.edge_type]
    what = (
        f"tells the same edge as row {first.n} (`{et.verb}`, [[{row.from_target}]], "
        f"[[{row.to_target}]]); a narrative tells an edge once"
    )
    text = f"delete the row `{row.text.strip()}`"
    if row.note:
        text += f" (if its note `{row.note}` is worth keeping, put it in the note of row {first.n} first)"
    fix = fixes.single(
        fixes.option("exact", text, fixes.delete_line(page.path, row.line, row.text))
    )
    return ctx.problem(rule, page.path, f"row {row.n}", what, fix, line=row.line, column=row.column)


@page_rule
def table_rules(ctx: Ctx, page: Page):
    reading = ctx.reading(page)
    if reading is None:
        return []
    out = []
    table = reading.table
    first_line = table.header_line if table else reading.first_heading_line
    rows = {r.n: r for r in table.rows} if table else {}
    headers = [tp.line for tp in reading.problems if tp.kind == "header"]
    for tp in reading.problems:
        if (
            tp.kind == "second"
            and tp.variant != "heading"
            and _joins_header(ctx, page, tp, headers)
        ):
            continue  # the table with the malformed header is reported once (header message first)
        stem_ = {"header": "TABLE-HEADER", "row": "TABLE-ROW", "second": "TABLE-SECOND"}[tp.kind]
        rule = ctx.pair(page, stem_)
        if rule is None:
            continue
        if tp.kind == "header":
            out.append(_header(ctx, page, rule, tp))
        elif tp.kind == "row":
            out.append(_row_problem(ctx, page, rule, tp, rows[tp.row]))
        else:
            out.append(_second(ctx, page, rule, tp, first_line))
    if table is None or not table.well_formed:
        return out
    seen: dict[tuple, Row] = {}
    for row in table.rows:
        if not row.well_formed:
            continue
        if row.edge_type is None:
            rule = ctx.pair(page, "TABLE-TYPE")
            if rule:
                out.append(_type(ctx, page, rule, row))
            continue
        rule = ctx.pair(page, "TABLE-LAYERS")
        if rule:
            problem = _layers(ctx, page, rule, row)
            if problem:
                out.append(problem)
        if row.from_target and row.to_target:
            key = (row.edge_type, row.from_target, row.to_target)
            if key not in seen:
                seen[key] = row
            else:
                rule = ctx.pair(page, "TABLE-DUPLICATE")
                if rule:
                    out.append(_duplicate(ctx, page, rule, row, seen[key]))
    return out
