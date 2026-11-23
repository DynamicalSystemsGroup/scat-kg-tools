"""The rules about links in frontmatter fields: shape, unlisted, endpoint, discouraged; and discouraged in the body."""

import re

from scat_kg.checks.ctx import Ctx, page_rule
from scat_kg.checks.suggest import offered_by, suggest_from_discouraged
from scat_kg.checks.text import (
    LINK_ITEM,
    article,
    capped,
    choose,
    is_missing,
    one,
)
from scat_kg.tbox import TBOX
from scat_kg.vault import Page

PLACEHOLDER = '- "[[<one page you choose>]]"'


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
        lines = [f'{f.key}: "[[{n or "<one page you choose>"}]]"' for n in names] or [
            f'{f.key}: "[[<one page you choose>]]"'
        ]
        if f.single and len(names) > 1:
            reason += (
                "; a relation page holds one pair, to relate more pairs create more relation pages"
            )
            fix = choose(
                [f"keep this one: replace the whole field with the line `{ln}`" for ln in lines]
            )
        elif f.single:
            tail = " (author)" if unreadable else ""
            fix = one(f"replace the whole field with the line `{lines[0]}`{tail}")
        else:
            rows = [f"{f.key}:"] + [
                f'  - "[[{n}]]"' if n else f"  {PLACEHOLDER} (author)" for n in names
            ]
            if not names:
                rows.append(f"  {PLACEHOLDER} (author)")
            fix = one("replace the whole field with\n" + "\n".join("       " + r for r in rows))
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
            )
        )
    return out


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
                one(f"delete `{key}:` and its list items"),
                line=page.field_lines.get(key),
                pos=ctx.pos(page, key),
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

        def rows(a: str, b: str) -> str:
            return f'       {ka}: "[[{a}]]"\n       {kb}: "[[{b}]]"'

        fix = one(
            f"replace the two lines\n{rows(w1.name, w2.name)}\n     with\n{rows(w2.name, w1.name)}"
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
            opts = []
            if not f.single:
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
                        opts.append(
                            f"move the item line `{item}` from `{f.key}` to `{g.key}`: {gone}, "
                            f"then {ctx.add_items(page, g.key, [link.target])}"
                        )
            cands = _candidates(ctx, page, f.key, w, f.target_type)
            shown, more = cands[:5], max(0, len(cands) - 5)
            opts += [f"replace `{item}` with `{ctx.item(page, f.key, c)}`" for c in shown]
            required = any(r.key == f.key and r.required_from == "stub" for r in t.required)
            if not required:
                opts.append(f"delete the item line `{item}` under `{f.key}`")
            notes = []
            if more:
                notes.append(f"(+{more} more not shown)")
            if not cands:
                notes.append(f"(no existing {f.target_type} page was found to replace it with)")
            if opts:
                fix = choose(opts, tuple(notes))
            else:
                fix = one(
                    f"change the pair by hand: no existing {f.target_type} page was found, and "
                    f"`{f.key}` is required at every status"
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
        opts = [f"delete `{f.key}:` and its list items"]
        notes = []
        names, more = capped(suggest_from_discouraged(ctx, page, f.key))
        into = DISCOURAGED_INTO[f.key]
        if names:
            opts.append(
                f"keep the point by linking what they offer, in `{into}` (suggestions you confirm): "
                + ctx.add_items(page, into, names)
            )
            if more:
                notes.append(f"(+{more} more)")
        out.append(
            ctx.problem(
                "SCAT-LINK-DISCOURAGED",
                page.path,
                f"field `{f.key}`",
                what,
                choose(opts, tuple(notes)),
                line=page.field_lines.get(f.key),
                pos=ctx.pos(page, f.key),
            )
        )
    return out


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
        opts = [
            f"on line {link.line} replace `[[{link.target}]]` with `{link.target}` to keep the words and drop the link"
        ]
        names, more = capped(offered_by(ctx, link.target, w.type_key))
        opts += [f"on line {link.line} replace `[[{link.target}]]` with `[[{n}]]`" for n in names]
        out.append(
            ctx.problem(
                "SCAT-LINK-DISCOURAGED-BODY",
                page.path,
                f"link [[{link.target}]]",
                f"the body of {article(t.slug)} {t.slug} page should not link to "
                f"{article(w.type_key)} {w.type_key} page",
                choose(opts, (f"(+{more} more)",) if more else ()),
                line=link.line,
                target=link.target,
            )
        )
    return out
