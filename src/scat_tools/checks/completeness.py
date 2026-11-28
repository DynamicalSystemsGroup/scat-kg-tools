"""What `draft` and `done` require (and a stub, for a field with a value set): SCAT-DONE-FIELD, SCAT-DRAFT-FIELD."""

from scat_tools.checks import fixes
from scat_tools.checks.ctx import Ctx, page_rule
from scat_tools.checks.text import is_missing
from scat_tools.fix import Fix
from scat_tools.tbox import TBOX
from scat_tools.vault import Page


@page_rule
def done_and_draft(ctx: Ctx, page: Page):
    if not ctx.typed(page):
        return []
    status = ctx.status_of(
        page
    )  # None when the status is missing or invalid: the page is not judged
    if status is None:
        return []
    done = status == "done"
    out = []
    for f in TBOX.page_types[page.type_key].required:
        if f.key == "type" or f.required_from != "done" or not is_missing(page.fields.get(f.key)):
            continue
        if status == "stub" and f.value_set is None:
            continue  # a stub is silent about a field it has not reached, except one with a value set
        later = fixes.run_option(fixes.set_status(page.name), suffix=" if the page is not finished")
        if f.value_set is not None:
            # the author picks one value; each pick is the whole field written, so it is exact data
            picks = [
                fixes.put_field(ctx, page, f.key, v, f"{f.key}: {v}", tail=" (author)")
                for v in f.value_set
            ]
            if done:
                fix = Fix.choose("slot", [*picks, later])
            else:
                fix = Fix.choose("slot", picks, head="Fix, choose one before you set status: done:")
        else:
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
            fix = Fix.choose("slot", [edit, later] if done else [edit])
        rule, what = (
            ("SCAT-DONE-FIELD", "missing on a page with status: done")
            if done
            else ("SCAT-DRAFT-FIELD", "missing (required once the page is done)")
        )
        out.append(
            ctx.problem(
                rule,
                page.path,
                f"field `{f.key}`",
                what,
                fix,
                pos=ctx.pos(page, f.key),
                on=f.key,
            )
        )
    return out
