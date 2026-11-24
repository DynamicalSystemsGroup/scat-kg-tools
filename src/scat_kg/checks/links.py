"""The rules about links in frontmatter fields: shape, unlisted, endpoint, discouraged; and discouraged in the body."""

import re

from scat_kg.checks import fixes
from scat_kg.checks.ctx import Ctx, page_rule
from scat_kg.checks.suggest import offered_by, suggest_from_discouraged
from scat_kg.checks.text import (
    LINK_ITEM,
    article,
    capped,
    is_missing,
)
from scat_kg.fix import Edit, Fix, FixOption
from scat_kg.tbox import TBOX
from scat_kg.vault import Link, Page

SLOT = "<one page you choose>"  # the author's placeholder in a link value
PLACEHOLDER = f'- "[[{SLOT}]]"'


def offer(opts: list[FixOption], notes: tuple[str, ...] = ()) -> Fix:
    """Alternatives (kind `options`), or one option told as `Fix: <text>`; the notes follow either way."""
    if len(opts) == 1:
        return Fix.choose(opts[0].kind, opts, None, notes)
    return Fix.choose("options", opts, None, notes)


def link_value(target: str) -> str:
    return f"[[{target}]]"


def list_with(page: Page, key: str, link: Link, replacement: str | None = None) -> list[str]:
    """The link items of `key` as written back whole, `link` replaced by `replacement` or left out when None."""
    out = []
    for l in page.fm_links.get(key, ()):
        if l is not link:
            out.append(link_value(l.target))
        elif replacement is not None:
            out.append(link_value(replacement))
    return out


def set_or_delete(page: Page, key: str, items: list[str]) -> Edit:
    """Write `items` as the whole field, or delete the field when nothing is left."""
    if items:
        return fixes.set_field(page.path, key, items)
    return fixes.delete_field(page.path, key)


def _name_of(item) -> str | None:
    """The page name in a link item as far as it can be read, or None when it names nothing."""
    while isinstance(item, list) and len(item) == 1:  # an unquoted [[x]] is a nested list
        item = item[0]
    if not isinstance(item, str):
        return None
    m = re.fullmatch(r"\s*\[\[(.*)\]\]\s*", item, re.DOTALL)
    inner = m.group(1) if m else item
    return re.split(r"[|#^]", inner, maxsplit=1)[0].strip() or None


@page_rule
def link_shape(ctx: Ctx, page: Page):
    if not ctx.typed(page):
        return []
    t = TBOX.page_types[page.type_key]
    out = []
    for f in t.fields:
        v = page.fields.get(f.key)
        if not f.is_link or is_missing(v):
            continue
        if f.single:
            if isinstance(v, str) and LINK_ITEM.fullmatch(v):
                continue
        elif isinstance(v, list) and all(isinstance(i, str) and LINK_ITEM.fullmatch(i) for i in v):
            continue
        items = v if isinstance(v, list) else [] if isinstance(v, dict) else [v]
        names = [_name_of(i) for i in items]
        unreadable = any(n is None for n in names) or not names
        if f.single:
            if isinstance(v, list):
                reason = "a single link is one quoted `[[page-name]]` line, not a list"
            else:
                reason = "the value is not exactly one quoted `[[page-name]]` link"
        elif isinstance(v, list):
            reason = "an item is not a quoted `[[page-name]]` link"
        else:
            reason = "the value is one line, not a list"
        values = [link_value(n or SLOT) for n in names] or [link_value(SLOT)]
        if f.single and len(names) > 1:
            reason += (
                "; a relation page holds one pair, to relate more pairs create more relation pages"
            )
            fix = fixes.alternatives(
                [
                    fixes.option(
                        "exact" if n else "slot",
                        f'keep this one: replace the whole field with the line `{f.key}: "{v}"`',
                        fixes.set_field(page.path, f.key, v, author_slot=None if n else SLOT),
                    )
                    for n, v in zip(names, values, strict=True)
                ]
            )
        elif f.single:
            tail = " (author)" if unreadable else ""
            fix = fixes.single(
                fixes.option(
                    "slot" if unreadable else "exact",
                    f'replace the whole field with the line `{f.key}: "{values[0]}"`{tail}',
                    fixes.set_field(
                        page.path, f.key, values[0], author_slot=SLOT if unreadable else None
                    ),
                )
            )
        else:
            rows = [f"{f.key}:"] + [
                f"  {PLACEHOLDER} (author)" if SLOT in v else f'  - "{v}"' for v in values
            ]
            fix = fixes.single(
                fixes.option(
                    "slot" if unreadable else "exact",
                    "replace the whole field with\n" + "\n".join("       " + r for r in rows),
                    fixes.set_field(
                        page.path, f.key, values, author_slot=SLOT if unreadable else None
                    ),
                )
            )
        if unreadable and names:
            reason += "; an item could not be read, so it is replaced by a placeholder"
        out.append(
            ctx.problem(
                "SCAT-LINK-SHAPE",
                page.path,
                f"field `{f.key}`",
                reason,
                fix,
                line=page.field_lines.get(f.key),
                pos=ctx.pos(page, f.key),
                on=f.key,
            )
        )
    return out


def delete_option(page: Page, key: str) -> FixOption:
    edit = fixes.delete_field(page.path, key)
    return fixes.option("exact", f"delete `{edit.field}:` and its list items", edit)


@page_rule
def link_unlisted(ctx: Ctx, page: Page):
    if not ctx.typed(page):
        return []
    from scat_kg.vault import LINK_KEYS

    t = TBOX.page_types[page.type_key]
    listed = {f.key for f in t.fields}
    own = sorted(f.key for f in t.fields if f.is_link)
    out = []
    for key in sorted(LINK_KEYS - listed):
        if is_missing(page.fields.get(key)):
            continue
        what = (
            f"{article(t.slug)} {t.slug} page does not take `{key}` "
            f"(its link fields are: {', '.join(own) if own else 'none'})"
        )
        out.append(
            ctx.problem(
                "SCAT-LINK-UNLISTED",
                page.path,
                f"field `{key}`",
                what,
                fixes.single(delete_option(page, key)),
                line=page.field_lines.get(key),
                pos=ctx.pos(page, key),
                on=key,
            )
        )
    return out


def _candidates(ctx: Ctx, page: Page, field_key: str, wrong: Page, want: str) -> list[str]:
    """Pages of type `want` to replace a wrong target with, in the catalogue's two tiers."""
    listed = set(ctx.targets(page, field_key)) | {page.name, wrong.name}
    near: set[str] = {
        b.source.rsplit("/", 1)[-1].removesuffix(".md") for b in ctx.vault.inbound(wrong.name)
    }
    near |= {l.target for l in wrong.links}
    for slug in TBOX.relations:
        for pair in ctx.relations(slug):
            if wrong.name in pair.values():
                near |= set(pair.values())
    first = sorted(
        (n for n in near if n not in listed and ctx.type_of(n) == want), key=lambda s: s.encode()
    )
    second = sorted(
        {
            l.target
            for l in page.body_links
            if l.target not in listed and l.target not in first and ctx.type_of(l.target) == want
        },
        key=lambda s: s.encode(),
    )
    return first + second


def _swap(ctx: Ctx, page: Page, t) -> tuple | None:
    """A relation page whose two endpoint fields hold each other's type: (field-a, field-b, w1, w2)."""
    if not t.endpoint_order:
        return None
    keys = sorted(t.endpoint_order, key=lambda k: page.field_lines.get(k, 0))
    ends = []
    for k in keys:
        ls = ctx.links(page, k)
        w = (
            ctx.page(ls[0].target)
            if len(ls) == 1 and page.fields.get(k) == f"[[{ls[0].target}]]"
            else None
        )
        if w is None:
            return None
        ends.append(w)
    (ka, kb), (w1, w2) = keys, ends
    if w1.type_key == t.field(kb).target_type and w2.type_key == t.field(ka).target_type:
        return ka, kb, w1, w2
    return None


def _wrong_type(ctx: Ctx, target: str, expected: str) -> bool:
    w = ctx.page(target)
    return w is not None and w.type_key is not None and w.type_key != expected


@page_rule
def link_endpoint(ctx: Ctx, page: Page):
    if not ctx.typed(page):
        return []
    t = TBOX.page_types[page.type_key]
    out = []
    swap = _swap(ctx, page, t)
    skip = set()
    if swap:
        ka, kb, w1, w2 = swap
        skip = {ka, kb}
        ea, eb = t.field(ka).target_type, t.field(kb).target_type
        what = (
            f"[[{w1.name}]] is a {w1.type_key} page and [[{w2.name}]] is a {w2.type_key} page, "
            f"but `{ka}` must link {ea} pages and `{kb}` {eb} pages"
        )

        edits = (
            fixes.set_field(page.path, ka, link_value(w2.name)),
            fixes.set_field(page.path, kb, link_value(w1.name)),
        )

        def rows(a: str, b: str) -> str:
            return f'       {ka}: "{link_value(a)}"\n       {kb}: "{link_value(b)}"'

        fix = fixes.single(
            fixes.option(
                "exact",
                f"replace the two lines\n{rows(w1.name, w2.name)}\n     with\n{rows(w2.name, w1.name)}",
                *edits,
            )
        )
        out.append(
            ctx.problem(
                "SCAT-LINK-ENDPOINT",
                page.path,
                f"fields `{ka}` and `{kb}`",
                what,
                fix,
                line=ctx.links(page, ka)[0].line,
                pos=ctx.pos(page, ka),
            )
        )
    for f in t.fields:
        if not f.is_link or f.key in skip:
            continue
        for link in ctx.links(page, f.key):
            w = ctx.page(link.target)
            if w is None or w.type_key is None or w.type_key == f.target_type:
                continue
            item = ctx.item(page, f.key, link.target)
            opts: list[FixOption] = []
            # Taking the only good item out of a field a `done` page requires would trade this error
            # for SCAT-DONE-LINK, so then no move or delete is offered.
            emptied = (
                f.required_from == "done"
                and ctx.status_of(page) == "done"
                and all(
                    o is link or _wrong_type(ctx, o.target, f.target_type)
                    for o in page.fm_links.get(f.key, ())
                )
            )
            if not f.single and not emptied:
                flow = ctx.current(page, f.key) != ""
                for g in t.required + t.optional:
                    if (
                        g.is_link
                        and not g.single
                        and g.target_type == w.type_key
                        and g.key != f.key
                    ):
                        if link.target in ctx.targets(page, g.key):
                            continue
                        gone = f"delete it from `{f.key}`" + (
                            " (in a flow list delete that one entry and its comma, leaving `[]` "
                            "if it was the only one)"
                            if flow
                            else ""
                        )
                        into = [link_value(x) for x in ctx.targets(page, g.key)]
                        opts.append(
                            fixes.option(
                                "exact",
                                f"move the item line `{item}` from `{f.key}` to `{g.key}`: {gone}, "
                                f"then {ctx.add_items(page, g.key, [link.target])}",
                                set_or_delete(page, f.key, list_with(page, f.key, link)),
                                fixes.set_field(page.path, g.key, [*into, link_value(link.target)]),
                            )
                        )
            cands = _candidates(ctx, page, f.key, w, f.target_type)
            shown, more = cands[:5], max(0, len(cands) - 5)
            for c in shown:
                new = link_value(c) if f.single else list_with(page, f.key, link, c)
                opts.append(
                    fixes.option(
                        "exact",
                        f"replace `{item}` with `{ctx.item(page, f.key, c)}`",
                        fixes.set_field(page.path, f.key, new),
                    )
                )
            required = any(r.key == f.key and r.required_from == "stub" for r in t.required)
            if not required and not emptied:
                gone_edit = (
                    fixes.delete_field(page.path, f.key)
                    if f.single
                    else set_or_delete(page, f.key, list_with(page, f.key, link))
                )
                opts.append(
                    fixes.option(
                        "exact", f"delete the item line `{item}` under `{f.key}`", gone_edit
                    )
                )
            notes = []
            if more:
                notes.append(f"(+{more} more not shown)")
            if not cands:
                notes.append(f"(no existing {f.target_type} page was found to replace it with)")
            if emptied:
                notes.append(
                    f"(`{f.key}` is required on a page with status: done and this is its only good "
                    "item, so deleting or moving the item alone would trade this error for "
                    f"SCAT-DONE-LINK; to delete or move it, run {fixes.phrase(fixes.set_status(page.name))} first, "
                    "or add a right-typed item first)"
                )
            if opts:
                fix = offer(opts, tuple(notes))
            elif emptied:
                fix = fixes.single(
                    FixOption(
                        "manual",
                        f"`{f.key}` is required on a page with status: done and this is its only good "
                        f"item, and no existing {f.target_type} page was found to replace it with: run "
                        f"{fixes.phrase(fixes.set_status(page.name))} first, then change the item by hand",
                    )
                )
            else:
                fix = fixes.single(
                    FixOption(
                        "manual",
                        f"change the pair by hand: no existing {f.target_type} page was found, and "
                        f"`{f.key}` is required at every status",
                    )
                )
            what = (
                f"[[{link.target}]] is {article(w.type_key)} {w.type_key} page, but `{f.key}` must link "
                f"{f.target_type} pages"
            )
            out.append(
                ctx.problem(
                    "SCAT-LINK-ENDPOINT",
                    page.path,
                    f"field `{f.key}`",
                    what,
                    fix,
                    line=link.line,
                    pos=ctx.pos(page, f.key),
                    target=link.target,
                    on=f.key,
                )
            )
    return out


DISCOURAGED_REASON = {
    "scenario-coded": "a scenario relates groups, concerns and affordances; technologies stay in the background",
    "architecture-coded": "an architecture relates concerns, affordances and technologies; stakeholders are abstracted away",
}
DISCOURAGED_INTO = {"technologies": "affordances", "groups": "concerns"}


@page_rule
def link_discouraged(ctx: Ctx, page: Page):
    if not ctx.typed(page):
        return []
    t = TBOX.page_types[page.type_key]
    out = []
    for f in t.discouraged:
        if not f.is_link or is_missing(page.fields.get(f.key)):
            continue
        targets = ctx.targets(page, f.key)
        what = (
            f"{DISCOURAGED_REASON.get(t.slug, 'a ' + t.slug + ' record')}, so linking "
            f"{f.target_type} pages here is discouraged: " + ", ".join(f"[[{x}]]" for x in targets)
        )
        opts = [delete_option(page, f.key)]
        notes = []
        names, more = capped(suggest_from_discouraged(ctx, page, f.key))
        into = DISCOURAGED_INTO[f.key]
        if names:
            kept = [link_value(x) for x in [*ctx.targets(page, into), *names]]
            opts.append(
                fixes.option(
                    "exact",
                    f"keep the point by linking what they offer, in `{into}` (suggestions you confirm): "
                    + ctx.add_items(page, into, names),
                    fixes.set_field(page.path, into, kept),
                )
            )
            if more:
                notes.append(f"(+{more} more)")
        out.append(
            ctx.problem(
                "SCAT-LINK-DISCOURAGED",
                page.path,
                f"field `{f.key}`",
                what,
                offer(opts, tuple(notes)),
                line=page.field_lines.get(f.key),
                pos=ctx.pos(page, f.key),
                on=f.key,
            )
        )
    return out


def body_swap(page: Page, link: Link, replacement: str, tail: str = "") -> FixOption:
    """On the link's line, replace `[[target]]` by `replacement`: an exact `replace-text`."""
    edit = fixes.replace_text(page.path, link.line, link_value(link.target), replacement)
    return fixes.option(
        "exact", f"on line {edit.line} replace `{edit.find}` with `{edit.replace}`{tail}", edit
    )


@page_rule
def link_discouraged_body(ctx: Ctx, page: Page):
    if not ctx.typed(page):
        return []
    t = TBOX.page_types[page.type_key]
    out = []
    for link in page.body_links:
        w = ctx.page(link.target)
        if w is None or w.type_key not in t.discouraged_body_links:
            continue
        opts = [body_swap(page, link, link.target, " to keep the words and drop the link")]
        names, more = capped(offered_by(ctx, link.target, w.type_key))
        opts += [body_swap(page, link, link_value(n), "") for n in names]
        out.append(
            ctx.problem(
                "SCAT-LINK-DISCOURAGED-BODY",
                page.path,
                f"link [[{link.target}]]",
                f"the body of {article(t.slug)} {t.slug} page should not link to "
                f"{article(w.type_key)} {w.type_key} page",
                offer(opts, (f"(+{more} more)",) if more else ()),
                line=link.line,
                target=link.target,
            )
        )
    return out
