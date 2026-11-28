"""The mismatches at a row's end: SCAT-DRAFT-END-* and SCAT-DONE-END-* (catalogue, "Pairs: the mismatches").

A mismatch (R-23) is a link and an edge that should agree and do not. In the row model it is a row end that is
not one link, one that reaches no page, or one that reaches a page that is not a node. SCAT-*-LINK-NOTINTABLE is
the converse: a node the account links that no row ends at. Rule 4 (an account that links both ends of a pair and has no row for it) has no rule: nothing here, or anywhere, reports it (section 4).
"""

from scat_tools.checks import fixes
from scat_tools.checks.ctx import NODE_TYPES, Ctx, page_rule
from scat_tools.checks.dangling import cap_note, classify, derive, fix_of, repairs
from scat_tools.checks.noedges import EDGE_ARGS
from scat_tools.checks.rows import (
    End,
    candidates,
    cell_edit,
    delete_row,
    ends_of,
    fill_edit,
    literal_in,
    literals_in,
    shown,
)
from scat_tools.checks.text import article, is_missing
from scat_tools.fix import FixOption
from scat_tools.graph import account_links
from scat_tools.tbox import TBOX
from scat_tools.vault import Page

OWN = "<node you choose>"


def _swap(page: Page, end: End, old: str, new: str, column: int) -> FixOption:
    return fixes.option(
        "exact",
        f"replace `{old}` with `{new}`",
        fixes.replace_text(page.path, end.cell.line, old, new, column=column),
    )


def _nolink(ctx: Ctx, page: Page, rule: str, end: End):
    cell, row = end.cell, end.row
    text = cell.raw
    opts: list[FixOption] = []
    notes: tuple[str, ...] = ()
    if not text:
        what = "the cell is empty; each end of a row is one link, `[[page-name]]`"
        index = TBOX.table.index_of(end.holds)
        opts.append(
            fixes.option(
                "slot",
                f"replace the empty cell with `[[{OWN}]]` (author)",
                fill_edit(page, row, index, f"[[{OWN}]]", OWN),
            )
        )
    else:
        what = f"`{text}` is not a link; each end of a row is one link, `[[page-name]]`"
        if cell.links:  # (c) more than one link, or a link beside other text
            for lit in literals_in(cell):
                opts.append(
                    fixes.option(
                        "exact",
                        f"replace the cell with `{lit.text}`; any text beside it belongs in the "
                        "`note` cell by hand",
                        cell_edit(page, cell, lit.text),
                    )
                )
        else:  # (b) text and no link
            names, notes = shown(candidates(ctx, page, text, end.layer))
            for n in names:
                opts.append(_swap(page, end, text, f"[[{n}]]", cell.column))
            d = derive(ctx, text)
            if end.layer and d and d.lower() not in ctx.taken:
                if end.layer == NODE_TYPES[0] and ctx.at_cap:
                    notes = (*notes, cap_note(ctx))
                else:
                    first = _swap(page, end, text, f"[[{d}]]", cell.column)
                    made = fixes.run_option(
                        fixes.stub(d, end.layer),
                        suffix=f" to create {article(end.layer)} {end.layer} page",
                    )
                    opts.append(
                        FixOption(
                            "exact",
                            f"{first.text}, then {made.text}",
                            made.command,
                            first.edits,
                        )
                    )
    opts.append(delete_row(page, row))
    return ctx.problem(
        rule,
        page.path,
        end.where,
        what,
        fixes.alternatives(opts, None, tuple(dict.fromkeys(notes))),
        line=cell.line,
        column=cell.column,
    )


def _nopage(ctx: Ctx, page: Page, rule: str, end: End, target: str):
    d = classify(ctx, target)
    cell = end.cell
    lit = literal_in(cell)

    def swap(name: str) -> FixOption:
        new = lit.with_name(name)
        return _swap(page, end, lit.text, new, lit.column)

    layer = end.layer
    pool = ctx.names_of_type(*((layer,) if layer else NODE_TYPES))
    opts, notes = repairs(
        ctx,
        target,
        d,
        pool=pool,
        types=[layer] if layer else [],
        only_types={layer} if layer else set(NODE_TYPES),
        swap=swap,
    )
    opts.append(delete_row(page, end.row))
    return ctx.problem(
        rule,
        page.path,
        end.where,
        f"[[{target}]] does not reach a page ({d.reason})",
        fix_of(opts, notes),
        line=cell.line,
        column=cell.column,
    )


def _notnode(ctx: Ctx, page: Page, rule: str, end: End, target: Page):
    cell = end.cell
    lit = literal_in(cell)
    kind = target.type_key
    if kind is not None:
        why = f"a {kind} page"
    elif is_missing(target.type):
        why = "a page with an empty `type`"
    else:
        why = f"a page with the invalid type `{target.type}`"
    names, notes = shown(candidates(ctx, page, target.name, end.layer)) if end.layer else ([], ())
    opts = [_swap(page, end, lit.text, lit.with_name(n), lit.column) for n in names]
    if not opts:
        opts.append(
            fixes.option(
                "slot",
                f"replace `{lit.text}` with `[[{OWN}]]` (author)",
                fixes.replace_text(
                    page.path, cell.line, lit.text, f"[[{OWN}]]", column=lit.column, author_slot=OWN
                ),
            )
        )
    opts.append(delete_row(page, end.row))
    return ctx.problem(
        rule,
        page.path,
        end.where,
        f"[[{target.name}]] is {why}, not a node; a row joins two nodes",
        fixes.alternatives(opts, None, tuple(notes)),
        line=cell.line,
        column=cell.column,
    )


@page_rule
def row_ends(ctx: Ctx, page: Page):
    reading = ctx.reading(page)
    if reading is None or reading.table is None or not reading.table.well_formed:
        return []
    out = []
    for row in reading.table.rows:
        if not row.well_formed:
            continue
        for end in ends_of(row):
            target = end.cell.target
            if target is None:
                rule = ctx.pair(page, "END-NOLINK")
                if rule:
                    out.append(_nolink(ctx, page, rule, end))
                continue
            found = ctx.vault.by_name.get(target, ())
            if not found:
                rule = ctx.pair(page, "END-NOPAGE")
                if rule:
                    out.append(_nopage(ctx, page, rule, end, target))
            elif (
                len(found) == 1
                and found[0].frontmatter_error is None
                and ctx.type_key(found[0]) not in NODE_TYPES
            ):
                rule = ctx.pair(page, "END-NOTNODE")
                if rule:
                    out.append(_notnode(ctx, page, rule, end, found[0]))
    return out


@page_rule
def link_notintable(ctx: Ctx, page: Page):
    """SCAT-*-LINK-NOTINTABLE: a node page the account links that is no end of a row of the table (the table is
    the coding of record). A narrative with no table has no row ends; a malformed table is reported by its own
    rules, and this one is silent then. A row that is malformed, or whose end is not one link, counts for nothing."""
    rule = ctx.pair(page, "LINK-NOTINTABLE") if ctx.is_narrative(page) else None
    reading = ctx.reading(page)
    if (
        rule is None
        or reading is None
        or (reading.table is not None and not reading.table.well_formed)
    ):
        return []
    ends = {
        end.cell.target
        for row in (reading.table.rows if reading.table else ())
        if row.well_formed
        for end in ends_of(row)
        if end.cell.target is not None
    }
    out, seen = [], set()
    for link in account_links(page):
        target = link.target
        if target in seen or target in ends:
            continue
        found = ctx.vault.by_name.get(target, ())
        if len(found) != 1 or found[0].frontmatter_error is not None:
            continue
        if ctx.type_key(found[0]) not in NODE_TYPES:
            continue
        seen.add(target)
        out.append(_notintable(ctx, page, rule, link))
    return out


def _notintable(ctx: Ctx, page: Page, rule: str, link):
    target = link.target
    record = (
        f"`scat record-edge {EDGE_ARGS} --told-by {page.name}` (REPL: "
        f'`scat_tools.record_edge("<type>", "<from>", "<to>", ["{page.name}"])`)'
    )
    fix = fixes.alternatives(
        [
            FixOption(
                "advisory",
                f"record the row for it: run {record}, with `{target}` as `<from>` or `<to>`",
            ),
            FixOption(
                "advisory",
                f"or take the link out of the account: write `{target}` without its brackets and "
                "keep the words",
            ),
        ]
    )
    return ctx.problem(
        rule,
        page.path,
        f"link [[{target}]]",
        "the account links it but no row of the table has it as an end; the table is the coding of record",
        fix,
        line=link.line,
        column=link.column,
        pos=link.column,
        target=target,
    )
