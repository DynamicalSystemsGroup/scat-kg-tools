"""The rules that read more than one page: conflicts, duplicate relation pages, mentions, raw and coded."""

import re

from scat_kg.checks import fixes
from scat_kg.checks.ctx import Ctx, page_rule
from scat_kg.checks.text import LINK_ITEM, is_missing, quote
from scat_kg.fix import Fix
from scat_kg.tbox import TBOX
from scat_kg.vault import Page, blank_code

CODED = ("scenario-coded", "architecture-coded")
RAW = ("scenario-raw", "architecture-raw")


@page_rule
def conflict_self(ctx: Ctx, page: Page):
    if page.type_key != "concern":
        return []
    value = page.fields.get("conflicts")
    items = value if isinstance(value, list) else [value]
    # the whole new list: every item but the ones that are exactly this page's own link
    kept = [
        i
        for i in items
        if not (isinstance(i, str) and (m := LINK_ITEM.fullmatch(i)) and m[1] == page.name)
    ]
    fix = fixes.single(
        fixes.option(
            "exact",
            f'delete the line `- "[[{page.name}]]"` under `conflicts`',
            fixes.set_field(page.path, "conflicts", kept),
        )
    )
    return [
        ctx.problem(
            "SCAT-CONFLICT-SELF",
            page.path,
            "field `conflicts`",
            f"[[{page.name}]] is this page; a concern cannot list itself under `conflicts`",
            fix,
            line=link.line,
            pos=ctx.pos(page, "conflicts"),
            target=link.target,
            on="conflicts",
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
            joined = theirs.strip() + " " + text
            put = f"replace the line {cur} with `notes: {quote(joined)}`"
        elif "notes" in kept.fields:
            joined = text
            put = f"replace the line {cur} with `notes: {quote(text)}`"
        else:
            joined = text
            put = f"add the line `notes: {quote(text)}`"
        first = fixes.option(
            "exact",
            f"in {kept.path}: {put}, and {body}",
            fixes.set_field(kept.path, "notes", joined),
        )
    else:  # nothing to write; what to keep of the body is the author's reading
        first = fixes.option(
            "advisory", f"in {kept.path}: {body} (`notes` of {page.path} has no text to move)"
        )
    second = fixes.option(
        "exact",
        f"delete {page.path}, then run {fixes.phrase(fixes.index())} and change every link "
        f"that named `{page.name}` to `[[{kept.name}]]` (each shows as SCAT-LINK-DANGLING-BODY on "
        "the next check)",
        fixes.delete_file(page.path),
        command=fixes.index(),
    )
    what = (
        f"this {t.slug} page states the same pair as [[{kept.name}]] "
        f"(`{fa}` [[{a}]], `{fb}` [[{b}]]); a pair has one page"
    )
    return [
        ctx.problem(
            "SCAT-REL-DUPLICATE",
            page.path,
            "frontmatter",
            what,
            Fix.steps("exact", [first, second]),
        )
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
    plain = _WIKILINK.sub(lambda m: re.sub(r"[^\n]", " ", m.group()), blank_code(page.body))
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
                fixes.single(
                    fixes.option(
                        "exact",
                        f"on line {line} replace `{written}` with `{link}`",
                        fixes.replace_text(page.path, line, written, link, column=column),
                    )
                ),
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
                fixes.single(
                    fixes.option(
                        "exact",
                        ctx.add_items(page, "coded", [coded.name], in_file=True),
                        fixes.set_field(
                            page.path,
                            "coded",
                            [f"[[{t}]]" for t in (*ctx.targets(page, "coded"), coded.name)],
                        ),
                    )
                ),
                pos=ctx.pos(page, "coded"),
                target=coded.name,
                on="coded",
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
    slot = "<coded-page-name>"
    line = f'`coded:` and under it the line `- "[[{slot}]]"` (author: choose the name)'
    if "coded" in page.fields:
        cur = f"coded: {ctx.current(page, 'coded')}".rstrip()
        text = f"in {page.path}: replace the line `{cur}` with {line}"
    else:
        text = f"in {page.path}: add {line}"
    first = fixes.option(
        "slot", text, fixes.set_field(page.path, "coded", [f"[[{slot}]]"], author_slot=slot)
    )
    second = fixes.run_option(
        fixes.stub(slot, key, slot=slot),
        suffix="; the operation writes `raw` on the new page itself, listing this page "
        "(until it runs, the new `coded` link shows as SCAT-LINK-DANGLING)",
    )
    return [
        ctx.problem(
            "SCAT-RAW-UNCODED",
            page.path,
            "field `coded`",
            "status is done but no coded page derives from this page",
            Fix.steps("slot", [first, second], head="Fix, two steps, in this order:"),
            pos=ctx.pos(page, "coded"),
            on="coded",
        )
    ]
