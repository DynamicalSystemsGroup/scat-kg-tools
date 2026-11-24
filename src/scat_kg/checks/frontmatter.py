"""The rules about a page's own frontmatter and file name: SCAT-FM-* and SCAT-NAME."""

import datetime
import posixpath

from scat_kg.checks import fixes
from scat_kg.checks.ctx import Ctx, page_rule
from scat_kg.checks.fixes import put_line as put_line  # noqa: PLC0414  (completeness.py imports it from here)
from scat_kg.checks.text import (
    CLASS_PAGES,
    CLASS_TITLES,
    article,
    free_name,
    is_missing,
    name_problem,
    near_match,
    quote,
    title_from_name,
)
from scat_kg.fix import FixOption
from scat_kg.tbox import TBOX
from scat_kg.vault import Page

TEXT_KEYS = ("status", "title", "description", "indexes", "timeframe", "notes")
# Contract section 5: the title a relation page's stub gets.
RELATION_TITLE = {
    r: (keys[0], TBOX.page_types[r].verb, keys[1]) for r, keys in TBOX.relations.items()
}


@page_rule
def fm_parse(ctx: Ctx, page: Page):
    e = page.frontmatter_error
    if e is None:
        return []
    fix = fixes.single(
        FixOption(
            "manual",
            "make the frontmatter a block of `key: value` lines between two lines containing only "
            "`---`, at the very top of the file; start from the first line the parser rejected",
        )
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
            fix = fixes.single(
                fixes.run_option(
                    fixes.set_status(page.name),
                    suffix="; use `stub` or `done` instead of `draft` if that is the truth",
                )
            )
        elif key == "title":
            title, why = default_title(ctx, page)
            line = f"title: {quote(title)}"
            fix = fixes.single(fixes.put_field(ctx, page, "title", title, line, tail=f" ({why})"))
        else:  # indexes
            if page.name in CLASS_PAGES:
                value = CLASS_PAGES[page.name]
                fix = fixes.single(fixes.put_field(ctx, page, key, value, f"indexes: {value}"))
            else:
                fix = fixes.alternatives(
                    [fixes.put_field(ctx, page, key, k, f"indexes: {k}") for k in f.value_set]
                )
        out.append(
            ctx.problem(
                "SCAT-FM-REQUIRED",
                page.path,
                f"field `{key}`",
                "missing",
                fix,
                pos=pos,
                on=key,
            )
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
        fix = fixes.single(_change_to(page, "type", near))
    else:
        fix = fixes.alternatives(
            [
                fixes.option(
                    "exact",
                    f"`type: {k}` ({t.description})",
                    fixes.set_field(page.path, "type", k),
                )
                for k, t in sorted(TBOX.page_types.items())
            ],
            head="Fix, choose the one that describes this page:",
        )
    what = "the value is empty, which is not a page type" if empty else f"`{v}` is not a page type"
    return [
        ctx.problem(
            "SCAT-FM-TYPE",
            page.path,
            "field `type`",
            what,
            fix,
            pos=ctx.pos(page, "type"),
            on="type",
        )
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
        slot = f"<one {expected} page you choose>"
        fix = fixes.single(
            fixes.put_field(ctx, page, key, f"[[{slot}]]", line, tail=" (author)", slot=slot)
        )
        out.append(
            ctx.problem(
                "SCAT-FM-REQUIRED-LINK",
                page.path,
                f"field `{key}`",
                what,
                fix,
                pos=ctx.pos(page, key),
                on=key,
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
        fix = fixes.single(_change_to(page, "status", near))
    else:
        fix = fixes.inline(
            [
                fixes.option(
                    "exact", f"`status: {s}` ({why})", fixes.set_field(page.path, "status", s)
                )
                for s, why in (
                    ("stub", "just started"),
                    ("draft", "being written"),
                    ("done", "finished"),
                )
            ]
        )
    return [
        ctx.problem(
            "SCAT-FM-STATUS",
            page.path,
            "field `status`",
            f"`{v}` is not a status",
            fix,
            pos=ctx.pos(page, "status"),
            on="status",
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
        fixes.single(_change_to(page, "indexes", near))
        if near
        else fixes.alternatives([_pick(page, "indexes", k) for k in keys])
    )
    return [
        ctx.problem(
            "SCAT-FM-INDEXES",
            page.path,
            "field `indexes`",
            f"`{v}` is not a class",
            fix,
            pos=ctx.pos(page, "indexes"),
            on="indexes",
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
        fixes.single(_change_to(page, "timeframe", near))
        if near
        else fixes.alternatives([_pick(page, "timeframe", k) for k in f.value_set])
    )
    return [
        ctx.problem(
            "SCAT-FM-TIMEFRAME",
            page.path,
            "field `timeframe`",
            f"`{v}` is not a timeframe",
            fix,
            pos=ctx.pos(page, "timeframe"),
            on="timeframe",
        )
    ]


def _change_to(page: Page, key: str, value: str) -> FixOption:
    return fixes.option(
        "exact", f"change it to `{key}: {value}`", fixes.set_field(page.path, key, value)
    )


def _pick(page: Page, key: str, value: str) -> FixOption:
    return fixes.option("exact", f"`{key}: {value}`", fixes.set_field(page.path, key, value))


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


def _one_line(page: Page, key: str, text: str) -> FixOption:
    return fixes.option(
        "exact",
        f"replace the field with the line `{key}: {quote(text)}`",
        fixes.set_field(page.path, key, text),
    )


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
            fix = fixes.single(_one_line(page, key, v[0]))
        elif not isinstance(v, list | dict):
            fix = fixes.single(_one_line(page, key, ctx.current(page, key)))
        else:
            fix = fixes.single(
                FixOption("manual", "replace the field with one line of text you write")
            )
        what = f"expected one line of text, found {kind}"
        out.append(
            ctx.problem(
                "SCAT-FM-SHAPE",
                page.path,
                f"field `{key}`",
                what,
                fix,
                pos=ctx.pos(page, key),
                on=key,
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
        fix = fixes.single(FixOption("manual", "choose a legal name by hand (contract section 2)"))
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
        to = posixpath.join(posixpath.dirname(page.path), f"{new}.md")
        fix = fixes.single(fixes.option("exact", text, fixes.rename_file(page.path, to)))
    return [ctx.problem("SCAT-NAME", page.path, "frontmatter", what, fix)]
