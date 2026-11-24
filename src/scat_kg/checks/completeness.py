"""What `draft` and `done` require (and a stub, for a field with a value set): SCAT-DONE-FIELD, SCAT-DONE-LINK, SCAT-DRAFT-FIELD, SCAT-DRAFT-LINK."""

from scat_kg.checks import fixes
from scat_kg.checks.ctx import Ctx, page_rule
from scat_kg.checks.suggest import suggest
from scat_kg.checks.text import capped, is_missing, yaml_list
from scat_kg.fix import Fix
from scat_kg.tbox import TBOX
from scat_kg.vault import Page


@page_rule
def done_and_draft(ctx: Ctx, page: Page):
    if not ctx.typed(page):
        return []
    status = ctx.status_of(
        page
    )  # `done` for a class page; None when the status is missing or invalid
    if status is None:
        return []
    t = TBOX.page_types[page.type_key]
    done = status == "done"
    out = []
    for f in t.required:
        if f.key == "type" or f.required_from != "done" or not is_missing(page.fields.get(f.key)):
            continue
        if status == "stub" and f.value_set is None:
            continue  # a stub is silent about a field it has not reached, except one with a value set
        pos = ctx.pos(page, f.key)
        later = fixes.run_option(fixes.set_status(page.name), suffix=" if the page is not finished")
        if f.value_set is not None:
            # the author picks one value; each pick is the whole field written, so it is exact data
            picks = [
                fixes.put_field(ctx, page, f.key, v, f"{f.key}: {v}", tail=" (author)")
                for v in f.value_set
            ]
            if not done:
                fix = Fix.choose("slot", picks, head="Fix, choose one before you set status: done:")
                rule, what = "SCAT-DRAFT-FIELD", "missing (required once the page is done)"
            else:
                fix = Fix.choose("slot", [*picks, later])
                rule, what = "SCAT-DONE-FIELD", "missing on a page with status: done"
            out.append(
                ctx.problem(rule, page.path, f"field `{f.key}`", what, fix, pos=pos, on=f.key)
            )
            continue
        if not f.is_link:
            slot = "<one sentence you write>"
            edit = fixes.put_field(
                ctx,
                page,
                f.key,
                slot,
                f'{f.key}: "{slot}"',
                tail=" (author)" if done else " (author) before you set status: done",
                slot=slot,
            )
            if not done:
                out.append(
                    ctx.problem(
                        "SCAT-DRAFT-FIELD",
                        page.path,
                        f"field `{f.key}`",
                        "missing (required once the page is done)",
                        Fix.choose("slot", [edit]),
                        pos=pos,
                        on=f.key,
                    )
                )
                continue
            options = [edit, *([later] if t.carries_status else [])]
            what = "missing on a page with status: done" if t.carries_status else "missing"
            out.append(
                ctx.problem(
                    "SCAT-DONE-FIELD",
                    page.path,
                    f"field `{f.key}`",
                    what,
                    Fix.choose("slot", options),
                    pos=pos,
                    on=f.key,
                )
            )
            continue
        names, more = capped(suggest(ctx, page, f.key))
        slot = None
        if names:
            lines = yaml_list(f.key, names, more)
            note = "suggestions found from relation pages; you decide"
        else:
            slot = f"<one {f.target_type} page you choose>"
            names = [slot]
            lines = yaml_list(f.key, names) + " (author)"
            note = "no suggestions found; you decide"
        verb = (
            "add this to the frontmatter"
            if f.key not in page.fields
            else f"replace the line `{f'{f.key}: {ctx.current(page, f.key)}'.rstrip()}` with this"
        )
        # suggestions are written as they stand (the author prunes them); with none, the slot is the author's
        edit = fixes.option(
            "slot" if slot else "exact",
            f"{verb}, keeping the lines that fit ({note}):\n{lines}",
            fixes.set_field(page.path, f.key, [f"[[{n}]]" for n in names], author_slot=slot),
        )
        if done:
            what = "required link field is missing or empty on a page with status: done"
            fix = Fix.choose("slot", [edit, later])
            rule = "SCAT-DONE-LINK"
        else:
            what = "required link field is missing or empty (required once the page is done)"
            fix = Fix.choose("slot", [edit])
            rule = "SCAT-DRAFT-LINK"
        out.append(ctx.problem(rule, page.path, f"field `{f.key}`", what, fix, pos=pos, on=f.key))
    return out
