"""The rules about a page's own frontmatter and file name: SCAT-FM-* and SCAT-NAME."""

import datetime

from scat_kg.checks.ctx import Ctx, page_rule
from scat_kg.checks.text import (
    CLASS_PAGES,
    CLASS_TITLES,
    article,
    choose,
    free_name,
    is_missing,
    name_problem,
    near_match,
    one,
    quote,
    set_status_cmd,
    title_from_name,
)
from scat_kg.tbox import TBOX
from scat_kg.vault import Page

TEXT_KEYS = ("status", "title", "description", "indexes", "timeframe", "notes")
# Contract section 5: the title a relation page's stub gets.
RELATION_TITLE = {
    r: (keys[0], TBOX.page_types[r].verb, keys[1]) for r, keys in TBOX.relations.items()
}


def put_line(ctx: Ctx, page: Page, key: str, line: str) -> str:
    """The catalogue's add-or-replace: add the line when the key is absent, replace it when empty."""
    if key not in page.fields:
        return f"add the line `{line}`"
    return f"replace the line `{f'{key}: {ctx.current(page, key)}'.rstrip()}` with `{line}`"


@page_rule
def fm_parse(ctx: Ctx, page: Page):
    e = page.frontmatter_error
    if e is None:
        return []
    fix = one(
        "make the frontmatter a block of `key: value` lines between two lines containing only `---`, "
        "at the very top of the file; start from the first line the parser rejected"
    )
    return [ctx.problem("SCAT-FM-PARSE", page.path, "frontmatter", e.reason, fix, line=e.line)]


def default_title(ctx: Ctx, page: Page) -> tuple[str, str]:
    """The title a missing `title` should get, and where it comes from."""
    if page.type_key == "class" and page.name in CLASS_TITLES:
        return CLASS_TITLES[page.name], f"the default title of the `{page.name}` class page"
    if page.type_key in RELATION_TITLE:
        first, verb, second = RELATION_TITLE[page.type_key]
        titles = []
        for f in (first, second):
            links = ctx.links(page, f)
            p = ctx.page(links[0].target) if len(links) == 1 else None
            t = p.fields.get("title") if p else None
            titles.append(t if isinstance(t, str) and t.strip() else None)
        if all(titles):
            return f"{titles[0]} {verb} {titles[1]}", "the title a stub of this pair gets"
    return (
        title_from_name(page.name),
        (
            "the page name with each - replaced by a space and the first letter upper case; "
            "reword it if you like"
        ),
    )


@page_rule
def fm_required(ctx: Ctx, page: Page):
    if not ctx.typed(page):
        return []
    t = TBOX.page_types[page.type_key]
    out = []
    for f in t.required:
        if f.key == "type" or f.is_link or f.required_from != "stub":
            continue
        if not is_missing(page.fields.get(f.key)):
            continue
        key, pos = f.key, ctx.pos(page, f.key)
        if key == "status":
            fix = one(
                f"run {set_status_cmd(page.name)}; use `stub` or `done` instead of `draft` "
                "if that is the truth"
            )
        elif key == "title":
            title, why = default_title(ctx, page)
            fix = one(f"{put_line(ctx, page, 'title', f'title: {quote(title)}')} ({why})")
        else:  # indexes
            if page.name in CLASS_PAGES:
                fix = one(put_line(ctx, page, key, f"indexes: {CLASS_PAGES[page.name]}"))
            else:
                fix = choose([put_line(ctx, page, key, f"indexes: {k}") for k in f.value_set])
        out.append(
            ctx.problem("SCAT-FM-REQUIRED", page.path, f"field `{key}`", "missing", fix, pos=pos)
        )
    return out


@page_rule
def fm_type(ctx: Ctx, page: Page):
    v = page.type
    empty = "type" in page.fields and is_missing(
        v
    )  # present but null or blank (log D-035 ruling 3)
    if page.frontmatter_error or not (empty or isinstance(v, str)) or v in TBOX.page_types:
        return []
    near = None if empty else near_match(v, TBOX.page_types)
    if near:
        fix = one(f"change it to `type: {near}`")
    else:
        fix = choose(
            [f"`type: {k}` ({t.description})" for k, t in sorted(TBOX.page_types.items())],
            head="Fix, choose the one that describes this page:",
        )
    what = "the value is empty, which is not a page type" if empty else f"`{v}` is not a page type"
    return [
        ctx.problem("SCAT-FM-TYPE", page.path, "field `type`", what, fix, pos=ctx.pos(page, "type"))
    ]


@page_rule
def fm_required_link(ctx: Ctx, page: Page):
    if not ctx.typed(page):
        return []
    t = TBOX.page_types[page.type_key]
    out = []
    for key in t.endpoint_order or ():
        if not is_missing(page.fields.get(key)):
            continue
        expected = t.field(key).target_type
        what = f"missing; {article(t.slug)} {t.slug} page names exactly one {expected} page here, at every status"
        line = f'{key}: "[[<one {expected} page you choose>]]"'
        fix = one(f"{put_line(ctx, page, key, line)} (author)")
        out.append(
            ctx.problem(
                "SCAT-FM-REQUIRED-LINK",
                page.path,
                f"field `{key}`",
                what,
                fix,
                pos=ctx.pos(page, key),
            )
        )
    return out


@page_rule
def fm_status(ctx: Ctx, page: Page):
    if not ctx.typed(page) or not TBOX.page_types[page.type_key].carries_status:
        return []
    v = page.status
    if not isinstance(v, str) or v in TBOX.statuses or is_missing(v):
        return []
    near = near_match(v, TBOX.statuses)
    if near:
        fix = one(f"change it to `status: {near}`")
    else:
        fix = (
            "Fix, choose one: `status: stub` (just started), `status: draft` (being written), "
            "`status: done` (finished)"
        )
    return [
        ctx.problem(
            "SCAT-FM-STATUS",
            page.path,
            "field `status`",
            f"`{v}` is not a status",
            fix,
            pos=ctx.pos(page, "status"),
        )
    ]


@page_rule
def fm_indexes(ctx: Ctx, page: Page):
    if page.type_key != "class":
        return []
    v = page.fields.get("indexes")
    keys = TBOX.page_types["class"].field("indexes").value_set
    if not isinstance(v, str) or is_missing(v) or v in keys:
        return []
    near = near_match(v, keys)
    fix = (
        one(f"change it to `indexes: {near}`")
        if near
        else choose([f"`indexes: {k}`" for k in keys])
    )
    return [
        ctx.problem(
            "SCAT-FM-INDEXES",
            page.path,
            "field `indexes`",
            f"`{v}` is not a class",
            fix,
            pos=ctx.pos(page, "indexes"),
        )
    ]


@page_rule
def fm_timeframe(ctx: Ctx, page: Page):
    if not ctx.typed(page):
        return []
    f = TBOX.page_types[page.type_key].field("timeframe")
    v = page.fields.get("timeframe")
    if f is None or not isinstance(v, str) or is_missing(v) or v in f.value_set:
        return []
    near = near_match(v, f.value_set)
    fix = (
        one(f"change it to `timeframe: {near}`")
        if near
        else choose([f"`timeframe: {k}`" for k in f.value_set])
    )
    return [
        ctx.problem(
            "SCAT-FM-TIMEFRAME",
            page.path,
            "field `timeframe`",
            f"`{v}` is not a timeframe",
            fix,
            pos=ctx.pos(page, "timeframe"),
        )
    ]


def _kind(v) -> str:
    if isinstance(v, bool):
        return "a boolean"
    if isinstance(v, int | float):
        return "a number"
    if isinstance(v, list):
        return "a list"
    if isinstance(v, dict):
        return "a mapping"
    if isinstance(v, datetime.date):
        return "a date"
    return "a value that is not text"


@page_rule
def fm_shape(ctx: Ctx, page: Page):
    if page.frontmatter_error:
        return []
    keys = ["type"]
    if page.type_key:
        listed = {f.key for f in TBOX.page_types[page.type_key].fields}
        keys += [k for k in TEXT_KEYS if k in listed]
    out = []
    for key in keys:
        v = page.fields.get(key)
        if is_missing(v) or isinstance(v, str):
            continue
        kind = _kind(v)
        if isinstance(v, list) and len(v) == 1 and isinstance(v[0], str):
            fix = one(f"replace the field with the line `{key}: {quote(v[0])}`")
        elif not isinstance(v, list | dict):
            fix = one(f"replace the field with the line `{key}: {quote(ctx.current(page, key))}`")
        else:
            fix = one("replace the field with one line of text you write")
        what = f"expected one line of text, found {kind}"
        out.append(
            ctx.problem(
                "SCAT-FM-SHAPE", page.path, f"field `{key}`", what, fix, pos=ctx.pos(page, key)
            )
        )
    return out


@page_rule
def name_rule(ctx: Ctx, page: Page):
    if page.frontmatter_error:
        return []
    t, name = page.type_key, page.name
    # a class page name is a reserved name the class page is entitled to; with no valid type, not checked
    reason = name_problem(name, reserved_ok=name in CLASS_PAGES and t in ("class", None))
    same = ctx.vault.by_name[name]
    indexes = page.fields.get("indexes")
    table = {v: k for k, v in CLASS_PAGES.items()}
    if reason:
        what, new_is_table = f"is not legal ({reason})", None
    elif len(same) > 1 and page is not same[0]:
        what, new_is_table = f"is also the name of {same[0].path}", None
    elif t == "class" and isinstance(indexes, str) and indexes in table and name != table[indexes]:
        what, new_is_table = f"is not the name of the {indexes} class page", table[indexes]
    else:
        return []
    what = f"the page name `{name}` {what}"
    new = new_is_table
    if new is None:
        title = page.fields.get("title")
        taken = set(ctx.taken)
        if not ctx.shares_name(page):
            taken.discard(name.lower())  # renaming this file only frees its own name
        new = free_name(title, taken) if isinstance(title, str) else None
    if new is None:
        fix = one("choose a legal name by hand (contract section 2)")
    else:
        text = (
            f"change the file name to `{new}.md`, then change the links that meant this page "
            f"from `[[{name}]]` to `[[{new}]]`"
        )
        if len(same) > 1:
            text += (
                f" (two pages share the name: change only the links that meant this page; "
                f"the links meant for the other page keep `[[{name}]]`)"
            )
        fix = one(text)
    return [ctx.problem("SCAT-NAME", page.path, "frontmatter", what, fix)]
