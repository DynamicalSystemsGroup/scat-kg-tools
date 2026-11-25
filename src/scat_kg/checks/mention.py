"""SCAT-MENTION: a body that names an existing node page in plain text and does not link it."""

import re

from scat_kg.checks import fixes
from scat_kg.checks.ctx import NODE_TYPES, Ctx, page_rule
from scat_kg.vault import Page, blank_code

_WIKILINK = re.compile(r"!?\[\[[^\[\]\n]*\]\]")


def _mentions(ctx: Ctx) -> list[tuple[Page, list[str]]]:
    """The pages a body could mention, with the texts (title, name; 4 characters or more) that name them."""
    rows = []
    for slug in NODE_TYPES:
        for p in ctx.by_type[slug]:
            title = p.fields.get("title")
            texts = [x for x in (title if isinstance(title, str) else "", p.name) if len(x) >= 4]
            rows.append((p, list(dict.fromkeys(texts))))
    return rows


def _plain(ctx: Ctx, page: Page) -> str:
    """The body with code, links and the `from` and `to` cells of the table turned to spaces (line breaks kept)."""
    plain = _WIKILINK.sub(lambda m: re.sub(r"[^\n]", " ", m.group()), blank_code(page.body))
    reading = ctx.reading(page)
    if reading is None or reading.table is None:
        return plain
    lines = plain.split("\n")
    for row in reading.table.rows:
        for holds in ("from", "to"):
            cell = row.cell(holds)
            if cell is not None:
                i = cell.line - page.body_line
                lines[i] = lines[i][: cell.start] + " " * len(cell.raw) + lines[i][cell.end :]
    return "\n".join(lines)


@page_rule
def mention(ctx: Ctx, page: Page):
    if not ctx.typed(page) or not page.body:
        return []
    plain = _plain(ctx, page)
    low = plain.lower()
    linked = {l.target for l in page.body_links}
    out = []
    for target, texts in _mentions(ctx):
        if target is page or target.name in linked:
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
