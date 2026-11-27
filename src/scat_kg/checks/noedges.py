"""SCAT-UNCODED: a narrative that links no node page, so it is excluded; SCAT-NOEDGES: a `done` coded
narrative whose fingerprint has no edges. Catalogue, "SCAT-UNCODED" and "SCAT-NOEDGES"."""

from scat_kg.checks import fixes
from scat_kg.checks.ctx import NODE_TYPES, Ctx, page_rule
from scat_kg.fix import FixOption
from scat_kg.vault import Page

EDGE_ARGS = "<type> <from> <to>"


def coded(ctx: Ctx, page: Page) -> bool:
    """Whether the page links at least one node page anywhere in its body (the graph's own reading)."""
    return any(ctx.type_of(l.target) in NODE_TYPES for l in page.links)


@page_rule
def uncoded(ctx: Ctx, page: Page):
    if not ctx.is_narrative(page) or coded(ctx, page):
        return []
    fix = fixes.alternatives(
        [
            FixOption(
                "advisory",
                "link a node page where the account names one, as `[[<node-name>]]` (or list it under "
                "a heading such as `Linked beyond the text`); a node the account names with no edge "
                "needs only this link",
            ),
            FixOption(
                "advisory",
                "or tell an edge: a row of the table whose ends are links to node pages; if the "
                "node has no page, `scat stub <name> --type <type>` makes one",
            ),
        ]
    )
    return [
        ctx.problem(
            "SCAT-UNCODED",
            page.path,
            "body",
            "the narrative links no node page, so it is excluded from the knowledge graph and every view",
            fix,
        )
    ]


@page_rule
def no_edges(ctx: Ctx, page: Page):
    if not ctx.is_narrative(page) or ctx.status_of(page) != "done" or not coded(ctx, page):
        return []  # an uncoded narrative is reported once, by SCAT-UNCODED
    reading = ctx.reading(page)
    table = reading.table if reading else None
    if table is not None and (not table.well_formed or table.rows):
        return []  # a malformed table is reported once, by its own rule; a row tells an edge
    draft = fixes.set_status(page.name, "draft")
    done = fixes.set_status(page.name, "done")
    record = (
        f'`scat record-edge {EDGE_ARGS} --told-by {page.name}` (REPL: `scat_kg.record_edge("<type>", '
        f'"<from>", "<to>", ["{page.name}"])`)'
    )
    fix = fixes.alternatives(
        [
            FixOption(
                "advisory",
                f"record its edges: run {fixes.phrase(draft)}, then {record} for each edge the "
                f"account tells, then {fixes.phrase(done)}",
            ),
            FixOption(
                "advisory",
                "or leave it as intended: a narrative may tell no edge, and this warning does not "
                "block; nothing to change",
            ),
        ]
    )
    return [
        ctx.problem(
            "SCAT-NOEDGES",
            page.path,
            "table",
            "the narrative is `done` and tells no edge: its fingerprint has no edges",
            fix,
        )
    ]
