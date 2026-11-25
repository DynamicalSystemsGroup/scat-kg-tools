"""SCAT-NOEDGES: a `done` narrative whose fingerprint has no edges (MISSION G1; catalogue, "SCAT-NOEDGES")."""

from scat_kg.checks import fixes
from scat_kg.checks.ctx import Ctx, page_rule
from scat_kg.fix import FixOption
from scat_kg.vault import Page

EDGE_ARGS = "<type> <from> <to>"


@page_rule
def no_edges(ctx: Ctx, page: Page):
    if not ctx.is_narrative(page) or ctx.status_of(page) != "done":
        return []
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
            "the narrative is `done` and tells no edge: its fingerprint is empty",
            fix,
        )
    ]
