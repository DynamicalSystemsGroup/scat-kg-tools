"""What `draft` and `done` require: SCAT-DONE-FIELD, SCAT-DONE-LINK, SCAT-DRAFT-FIELD, SCAT-DRAFT-LINK."""

from scat_kg.checks.ctx import Ctx, page_rule
from scat_kg.checks.frontmatter import put_line
from scat_kg.checks.suggest import suggest
from scat_kg.checks.text import capped, choose, is_missing, one, set_status_cmd, yaml_list
from scat_kg.tbox import TBOX
from scat_kg.vault import Page


@page_rule
def done_and_draft(ctx: Ctx, page: Page):
    if not ctx.typed(page):
        return []
    status = ctx.status_of(
        page
    )  # `done` for a class page; None when the status is missing or invalid
    if status not in ("draft", "done"):
        return []
    t = TBOX.page_types[page.type_key]
    done = status == "done"
    out = []
    for f in t.required:
        if f.key == "type" or f.required_from != "done" or not is_missing(page.fields.get(f.key)):
            continue
        pos = ctx.pos(page, f.key)
        if not f.is_link:
            edit = put_line(ctx, page, f.key, f'{f.key}: "<one sentence you write>"') + " (author)"
            if not done:
                out.append(
                    ctx.problem(
                        "SCAT-DRAFT-FIELD",
                        page.path,
                        f"field `{f.key}`",
                        "missing (required once the page is done)",
                        one(f"{edit} before you set status: done"),
                        pos=pos,
                    )
                )
                continue
            options = [edit] + (
                [f"run {set_status_cmd(page.name)} if the page is not finished"]
                if t.carries_status
                else []
            )
            what = "missing on a page with status: done" if t.carries_status else "missing"
            out.append(
                ctx.problem(
                    "SCAT-DONE-FIELD", page.path, f"field `{f.key}`", what, choose(options), pos=pos
                )
            )
            continue
        names, more = capped(suggest(ctx, page, f.key))
        if names:
            lines = yaml_list(f.key, names, more)
            note = "suggestions found from relation pages; you decide"
        else:
            lines = yaml_list(f.key, [f"<one {f.target_type} page you choose>"]) + " (author)"
            note = "no suggestions found; you decide"
        verb = (
            "add this to the frontmatter"
            if f.key not in page.fields
            else f"replace the line `{f'{f.key}: {ctx.current(page, f.key)}'.rstrip()}` with this"
        )
        edit = f"{verb}, keeping the lines that fit ({note}):\n{lines}"
        if done:
            what = "required link field is missing or empty on a page with status: done"
            fix = choose([edit, f"run {set_status_cmd(page.name)} if the page is not finished"])
            rule = "SCAT-DONE-LINK"
        else:
            what = "required link field is missing or empty (required once the page is done)"
            fix = one(edit)
            rule = "SCAT-DRAFT-LINK"
        out.append(ctx.problem(rule, page.path, f"field `{f.key}`", what, fix, pos=pos))
    return out
