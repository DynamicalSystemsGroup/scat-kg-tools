"""Suggestions (catalogue section 1): pages to link that relation pages the vault already has point to.

Never required and never written; the author confirms. Sorted by name in byte order, pages already listed
left out, and only pages that exist with the type the field needs.
"""

from scat_kg.checks.ctx import Ctx
from scat_kg.tbox import TBOX
from scat_kg.vault import Page

# field to fill -> (relation, endpoint it pivots on, field of this page that holds the pivots, endpoint it gives)
S = {
    "groups": ("heldby", "concern", "concerns", "group"),
    "concerns": ("heldby", "group", "groups", "concern"),
    "affordances": ("addresses", "concern", "concerns", "affordance"),
    "technologies": ("attributes", "affordance", "affordances", "technology"),
}
# from a discouraged field of the page: the field it points at, and the row that gives suggestions
FROM_DISCOURAGED = {
    "technologies": ("affordances", ("attributes", "technology", "technologies", "affordance")),
    "groups": ("concerns", ("heldby", "group", "groups", "concern")),
}


def _via(ctx: Ctx, pivots: set[str], row: tuple, listed: set[str]) -> list[str]:
    relation, pivot, _, out = row
    want = TBOX.page_types[relation].field(out).target_type
    found = {r[out] for r in ctx.relations(relation) if r[pivot] in pivots}
    return sorted(
        (n for n in found if n not in listed and ctx.type_of(n) == want), key=lambda s: s.encode()
    )


def suggest(ctx: Ctx, page: Page, field: str) -> list[str]:
    """S(<field>) for the page."""
    if field == "raw":
        want = TBOX.page_types[page.type_key].field("raw").target_type
        listed = set(ctx.targets(page, "raw"))
        return sorted(
            (
                r.name
                for r in ctx.by_type[want]
                if page.name in ctx.targets(r, "coded") and r.name not in listed
            ),
            key=lambda s: s.encode(),
        )
    row = S[field]
    return _via(ctx, set(ctx.targets(page, row[2])), row, set(ctx.targets(page, field)))


def suggest_from_discouraged(ctx: Ctx, page: Page, field: str) -> list[str]:
    """What the pages in a discouraged field offer, as pages for the field the catalogue points to."""
    into, row = FROM_DISCOURAGED[field]
    return _via(ctx, set(ctx.targets(page, field)), row, set(ctx.targets(page, into)))


def offered_by(ctx: Ctx, target: str, class_key: str) -> list[str]:
    """The affordances a technology offers, or the concerns a group holds (for a body link)."""
    row = FROM_DISCOURAGED["technologies" if class_key == "technology" else "groups"][1]
    return _via(ctx, {target}, row, set())
