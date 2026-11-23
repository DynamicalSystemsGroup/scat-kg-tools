"""The rules that read more than one page: conflicts, duplicate relation pages, mentions, raw and coded."""

import re

from scat_kg.checks.ctx import Ctx, page_rule
from scat_kg.checks.text import is_missing, one, quote, steps, stub_cmd
from scat_kg.tbox import TBOX
from scat_kg.vault import Page, _blank_code

CODED = ("scenario-coded", "architecture-coded")
RAW = ("scenario-raw", "architecture-raw")


def _conflicts(ctx: Ctx) -> dict[frozenset, set[str]]:
    """The conflict relation: pair -> names of the concern pages that declare it (self pairs left out)."""
    if "conflicts" not in ctx.cache:
        pairs: dict[frozenset, set[str]] = {}
        for c in ctx.by_type["concern"]:
            for other in ctx.targets(c, "conflicts"):
                if other != c.name:
                    pairs.setdefault(frozenset((c.name, other)), set()).add(c.name)
        ctx.cache["conflicts"] = pairs
    return ctx.cache["conflicts"]


@page_rule
def conflict_both(ctx: Ctx, page: Page):
    if page.type_key not in CODED:
        return []
    held = sorted({n for n in ctx.targets(page, "concerns") if ctx.type_of(n) == "concern"})
    pairs = _conflicts(ctx)
    out = []
    for i, a in enumerate(held):
        for b in held[i + 1 :]:
            declared = pairs.get(frozenset((a, b)))
            if not declared:
                continue
            by = ", ".join(f"[[{n}]]" for n in sorted(declared))
            fix = one(
                "none needed if both belong in this record. Holding both sides is allowed and is what "
                "the warning marks, a place where two concerns pull apart. If one was coded here by "
                f'mistake, delete its line `- "[[{a}]]"` or `- "[[{b}]]"` under `concerns`.'
            )
            out.append(
                ctx.problem(
                    "SCAT-CONFLICT-BOTH",
                    page.path,
                    "field `concerns`",
                    f"this record holds both [[{a}]] and [[{b}]], which conflict (declared on {by})",
                    fix,
                    line=page.field_lines.get("concerns"),
                    pos=ctx.pos(page, "concerns"),
                    target=a + " " + b,
                )
            )
    return out


@page_rule
def conflict_self(ctx: Ctx, page: Page):
    if page.type_key != "concern":
        return []
    return [
        ctx.problem(
            "SCAT-CONFLICT-SELF",
            page.path,
            "field `conflicts`",
            f"[[{page.name}]] is this page; a concern cannot conflict with itself",
            one(f'delete the line `- "[[{page.name}]]"` under `conflicts`'),
            line=link.line,
            pos=ctx.pos(page, "conflicts"),
            target=link.target,
        )
        for link in ctx.links(page, "conflicts")
        if link.target == page.name
    ]


def _duplicates(ctx: Ctx) -> dict[str, Page]:
    """Page path -> the page it duplicates (the first by name, byte order), for each duplicate."""
    if "dups" not in ctx.cache:
        groups: dict[tuple, list[Page]] = {}
        for slug, keys in TBOX.relations.items():
            for p in ctx.by_type[slug]:
                ends = [ctx.links(p, k) for k in keys]
                if all(len(e) == 1 for e in ends):
                    groups.setdefault((slug, *(e[0].target for e in ends)), []).append(p)
        dups = {}
        for pages in groups.values():
            pages.sort(key=lambda p: (p.name.encode(), p.path.encode()))
            dups.update({p.path: pages[0] for p in pages[1:]})
        ctx.cache["dups"] = dups
    return ctx.cache["dups"]


@page_rule
def rel_duplicate(ctx: Ctx, page: Page):
    kept = _duplicates(ctx).get(page.path)
    if kept is None:
        return []
    t = TBOX.page_types[page.type_key]
    fa, fb = sorted(t.endpoint_order, key=lambda k: kept.field_lines.get(k, 0))
    a, b = ctx.targets(kept, fa)[0], ctx.targets(kept, fb)[0]
    mine = page.fields.get("notes")
    text = mine.strip() if isinstance(mine, str) else ""
    body = f"copy any part of the body of {page.path} you want to keep"
    if text:
        theirs = kept.fields.get("notes")
        cur = f"`{f'notes: {ctx.current(kept, "notes")}'.rstrip()}`"
        if isinstance(theirs, str) and theirs.strip():
            put = f"replace the line {cur} with `notes: {quote(theirs.strip() + ' ' + text)}`"
        elif "notes" in kept.fields:
            put = f"replace the line {cur} with `notes: {quote(text)}`"
        else:
            put = f"add the line `notes: {quote(text)}`"
        first = f"in {kept.path}: {put}, and {body}"
    else:
        first = f"in {kept.path}: {body} (`notes` of {page.path} has no text to move)"
    second = (
        f"delete {page.path}, then run `scat index` (REPL: `scat_kg.index()`) and change every link "
        f"that named `{page.name}` to `[[{kept.name}]]` (each shows as SCAT-LINK-DANGLING-BODY on "
        "the next check)"
    )
    what = (
        f"this {t.slug} page states the same pair as [[{kept.name}]] "
        f"(`{fa}` [[{a}]], `{fb}` [[{b}]]); a pair has one page"
    )
    return [
        ctx.problem("SCAT-REL-DUPLICATE", page.path, "frontmatter", what, steps([first, second]))
    ]


_WIKILINK = re.compile(r"!?\[\[[^\[\]\n]*\]\]")


def _mentions(ctx: Ctx) -> list[tuple[Page, list[str]]]:
    """The pages a body could mention, with the texts (title, name; 4 characters or more) that name them."""
    if "mentions" not in ctx.cache:
        rows = []
        for slug in ("stakeholder-group", "concern", "affordance", "technology"):
            for p in ctx.by_type[slug]:
                title = p.fields.get("title")
                texts = [
                    x for x in (title if isinstance(title, str) else "", p.name) if len(x) >= 4
                ]
                rows.append((p, list(dict.fromkeys(texts))))
        ctx.cache["mentions"] = rows
    return ctx.cache["mentions"]


@page_rule
def mention(ctx: Ctx, page: Page):
    if not ctx.typed(page) or page.type_key in (*RAW, "class") or not page.body:
        return []
    t = TBOX.page_types[page.type_key]
    plain = _WIKILINK.sub(lambda m: re.sub(r"[^\n]", " ", m.group()), _blank_code(page.body))
    low = plain.lower()
    linked = {l.target for l in page.body_links}
    out = []
    for target, texts in _mentions(ctx):
        if target is page or target.name in linked or target.type_key in t.discouraged_body_links:
            continue
        best = None
        for text in texts:
            if text.lower() not in low:
                continue
            m = re.search(rf"(?<!\w){re.escape(text)}(?!\w)", plain, re.IGNORECASE)
            if m and (best is None or m.start() < best.start()):
                best = m
        if best is None:
            continue
        line = page.body_line + plain.count("\n", 0, best.start())
        column = best.start() - (plain.rfind("\n", 0, best.start()) + 1) + 1
        written = best.group()
        link = f"[[{target.name}]]" if written == target.name else f"[[{target.name}|{written}]]"
        out.append(
            ctx.problem(
                "SCAT-MENTION",
                page.path,
                f"text `{written}`",
                f"names the {target.type_key} page [[{target.name}]] but does not link it",
                one(f"on line {line} replace `{written}` with `{link}`"),
                line=line,
                column=column,
                target=target.name,
            )
        )
    return out


@page_rule
def raw_backlink(ctx: Ctx, page: Page):
    if page.type_key not in RAW:
        return []
    want = TBOX.page_types[page.type_key].field("coded").target_type
    listed = set(ctx.targets(page, "coded"))
    out = []
    for c in sorted({b.source for b in ctx.vault.inbound(page.name) if b.field == "raw"}):
        coded = ctx.page_at(c)
        if coded is None or coded.type_key != want or coded.name in listed:
            continue
        out.append(
            ctx.problem(
                "SCAT-RAW-BACKLINK",
                page.path,
                "field `coded`",
                f"[[{coded.name}]] lists this page in `raw`, but this page does not list it",
                one(ctx.add_items(page, "coded", [coded.name], in_file=True)),
                pos=ctx.pos(page, "coded"),
                target=coded.name,
            )
        )
    return out


@page_rule
def raw_uncoded(ctx: Ctx, page: Page):
    if page.type_key not in RAW or ctx.status_of(page) != "done":
        return []
    if not is_missing(page.fields.get("coded")):
        return []
    if any(b.field == "raw" for b in ctx.vault.inbound(page.name)):
        return []
    key = TBOX.page_types[page.type_key].field("coded").target_type
    line = '`coded:` and under it the line `- "[[<coded-page-name>]]"` (author: choose the name)'
    if "coded" in page.fields:
        cur = f"coded: {ctx.current(page, 'coded')}".rstrip()
        first = f"in {page.path}: replace the line `{cur}` with {line}"
    else:
        first = f"in {page.path}: add {line}"
    second = (
        f"run {stub_cmd('<coded-page-name>', key)}; the operation writes `raw` on the new page itself, "
        "listing this page (until it runs, the new `coded` link shows as SCAT-LINK-DANGLING)"
    )
    return [
        ctx.problem(
            "SCAT-RAW-UNCODED",
            page.path,
            "field `coded`",
            "status is done but no coded page derives from this page",
            steps([first, second], head="Fix, two steps, in this order:"),
            pos=ctx.pos(page, "coded"),
        )
    ]
