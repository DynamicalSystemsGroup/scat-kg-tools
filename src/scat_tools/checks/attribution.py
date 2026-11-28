"""The one mode-dependent rule: what the vault's attribution mode makes of contributors.

The TBox says only that a narrative's `attributed_to` is optional and that a `contributor` page is a page type;
the mode is the vault's (`scat.toml`), so the grading is stated here and nowhere else. `MODE_RULE` is its wording,
quoted byte for byte in the catalogue.

`disallowed`: any `attributed_to` on a narrative and any contributor page is an error at every status
(SCAT-ATTR-DISALLOWED). `required`: a narrative with no entry gets a warning before `done`, an error at `done`
(SCAT-DRAFT-ATTR, SCAT-DONE-ATTR). `optional`: both allowed, nothing required. In the two modes that allow them, each
entry must be a link to a contributor page (SCAT-ATTR-LINK). A vault with no usable mode gets only SCAT-MODE-CONFIG:
these rules say nothing until the mode is known. Nothing here is read at any other mode: the three are disjoint.
"""

from scat_tools.checks import fixes
from scat_tools.checks.ctx import Ctx, page_rule
from scat_tools.checks.dangling import classify
from scat_tools.checks.text import near_match, quote, stem
from scat_tools.fix import Fix
from scat_tools.vault import ATTRIBUTED_KEY, CONTRIBUTOR, Page, entry_target, link_entries

MODE_RULE = (
    "In required mode a narrative SHALL name its contributors; in disallowed mode it SHALL NOT; "
    "in optional mode it MAY. To name a contributor is to link a contributor page in the narrative's "
    "`attributed_to` field."
)

KEY = ATTRIBUTED_KEY


def entries(page: Page) -> list[str] | None:
    """The field's entries as written, blank ones dropped; None when it is not a list of text (a shape problem)."""
    return link_entries(page, KEY)


def mode_of(ctx: Ctx, page: Page, *modes: str) -> bool:
    """Whether the page is a narrative and the vault's mode is one of `modes` (never when no mode is known)."""
    return ctx.is_narrative(page) and ctx.vault.config.attribution in modes


def _list_line(values: list[str]) -> str:
    return f"{KEY}: [{', '.join(quote(v) for v in values)}]"


@page_rule
def attr_disallowed(ctx: Ctx, page: Page):
    if ctx.vault.config.attribution != "disallowed":
        return []
    if ctx.typed(page) and page.type_key == CONTRIBUTOR:
        fix = fixes.single(
            fixes.option(
                "exact",
                f"delete the file {page.path}: this vault's attribution mode is `disallowed`, so it holds no "
                "contributor page; the coder who wants contributor pages changes `attribution` in scat.toml "
                "for the whole vault",
                fixes.delete_file(page.path),
            )
        )
        return [
            ctx.problem(
                "SCAT-ATTR-DISALLOWED",
                page.path,
                "field `type`",
                "`contributor` is a contributor page, and the vault's attribution mode is `disallowed`",
                fix,
                pos=ctx.pos(page, "type"),
                on="type",
            )
        ]
    if not ctx.is_narrative(page) or KEY not in page.fields:
        return []
    fix = fixes.single(
        fixes.option(
            "exact",
            f"delete the field `{KEY}` (all its lines): this vault's attribution mode is `disallowed`; "
            "the coder who wants contributors named changes `attribution` in scat.toml for the whole vault",
            fixes.delete_field(page.path, KEY),
        )
    )
    return [
        ctx.problem(
            "SCAT-ATTR-DISALLOWED",
            page.path,
            f"field `{KEY}`",
            "present, and the vault's attribution mode is `disallowed`",
            fix,
            pos=ctx.pos(page, KEY),
            on=KEY,
        )
    ]


@page_rule
def attr_missing(ctx: Ctx, page: Page):
    if not mode_of(ctx, page, "required"):
        return []
    rule = ctx.pair(page, "ATTR")
    found = entries(page)
    if rule is None or found is None or found:
        return []  # not judged, or the shape (SCAT-FM-SHAPE) is wrong, or a contributor is named
    done = rule.startswith("SCAT-DONE")
    slot = "<a contributor page you link>"
    edit = fixes.put_field(
        ctx,
        page,
        KEY,
        [f"[[{slot}]]"],
        f'{KEY}: ["[[{slot}]]"]',
        tail=" (author)" if done else " (author) before you set status: done",
        slot=f"[[{slot}]]",
    )
    later = fixes.run_option(fixes.set_status(page.name), suffix=" if the page is not finished")
    fix = Fix.choose("slot", [edit, later] if done else [edit])
    what = (
        "missing on a page with status: done (the vault's attribution mode is `required`)"
        if done
        else "missing (required once the page is done: the vault's attribution mode is `required`)"
    )
    return [
        ctx.problem(rule, page.path, f"field `{KEY}`", what, fix, pos=ctx.pos(page, KEY), on=KEY)
    ]


@page_rule
def attr_link(ctx: Ctx, page: Page):
    """Each entry is a link that resolves to a contributor page: three variants, one id."""
    if not mode_of(ctx, page, "required", "optional"):
        return []
    found = entries(page)
    if not found:
        return []
    pool = ctx.names_of_type(CONTRIBUTOR)
    out = []
    for entry in found:
        target = entry_target(entry)
        bad = None  # (what, the name a swap may use)
        if target is None:
            bad = f"`{entry.strip()}` is not a link to a contributor page", stem(entry)
        elif target not in ctx.vault.by_name:
            d = classify(ctx, target)
            bad = f"`[[{target}]]` does not reach a page ({d.reason})", target
        else:
            pages = ctx.vault.by_name[target]
            kind = ctx.type_key(pages[0]) if len(pages) == 1 else None
            if kind is not None and kind != CONTRIBUTOR:
                bad = (
                    f"`[[{target}]]` reaches a page that is not a contributor (it is {_a(kind)})",
                    target,
                )
        if bad is None:
            continue
        what, name = bad
        near = near_match(name, pool) if name else None
        opts = []
        if near:
            swapped = [f"[[{near}]]" if e is entry else e for e in found]
            opts.append(
                fixes.put_field(
                    ctx,
                    page,
                    KEY,
                    swapped,
                    _list_line(swapped),
                    tail=f" (the contributor page `{near}`)",
                )
            )
        gone = classify(ctx, target) if target is not None else None
        if gone is not None and gone.kind == "a":
            # a legal name and no such file: the stub makes the page, and the link then resolves
            opts.append(
                fixes.run_option(
                    fixes.stub(target, CONTRIBUTOR),
                    suffix=" to create the contributor page the entry links",
                )
            )
        else:
            opts.append(_manual())
        rest = [e for e in found if e is not entry]
        opts.append(
            fixes.put_field(ctx, page, KEY, rest, _list_line(rest), tail=" (drop this entry)")
        )
        out.append(
            ctx.problem(
                "SCAT-ATTR-LINK",
                page.path,
                f"field `{KEY}`",
                what,
                fixes.alternatives(opts),
                pos=ctx.pos(page, KEY),
                target=entry,
                on=KEY,
            )
        )
    return out


def _manual():
    return fixes.option(
        "manual",
        f"link the entry to a contributor page: write `[[<name>]]` of an existing page of type `{CONTRIBUTOR}`, "
        f"or make one (`type: {CONTRIBUTOR}`, `status: stub`, `title`) and link it",
    )


def _a(kind: str) -> str:
    return f"{'an' if kind[0] in 'aeiou' else 'a'} {kind} page"
