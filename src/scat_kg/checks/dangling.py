"""Links that reach no page: SCAT-LINK-DANGLING-BODY here, and the repairs SCAT-*-END-NOPAGE shares.

Three variants share the id (catalogue, SCAT-LINK-DANGLING-BODY): (a) a legal name and no such file; (b) a legal
name for which a Markdown file exists that has no `type`; (c) a name that is not legal.
"""

import re
from collections.abc import Callable
from dataclasses import dataclass

from scat_kg.checks import fixes
from scat_kg.checks.ctx import NARRATIVE, NODE_TYPES, Ctx, page_rule
from scat_kg.checks.linkedit import literal
from scat_kg.checks.text import (
    article,
    derived_name,
    free_name,
    name_problem,
    near_match,
    quote,
    title_from_name,
)
from scat_kg.fix import Fix, FixOption
from scat_kg.vault import Page

HAND = "choose a legal page name by hand (page contracts section 2), then write the link with it"


@dataclass(frozen=True)
class Dangle:
    kind: str  # "a", "b" or "c"
    reason: str  # the text in the brackets of the message


def classify(ctx: Ctx, target: str) -> Dangle | None:
    """None when the target reaches a page; otherwise which variant it is."""
    if target in ctx.vault.by_name:
        return None
    other = ctx.typeless.get(target)
    why = name_problem(target)
    if why is None:
        clash = next((n for n in sorted(ctx.vault.by_name) if n.lower() == target), None)
        if clash:
            return Dangle("c", f"{target} differs from the existing name `{clash}` only by case")
        if other:
            return Dangle("b", f"{other} exists but has no `type`, so it is not a page")
        return Dangle("a", f"no page is named {target}")
    reason = f"{target} is not a legal page name: {why}"
    if other:
        reason += f"; {other} exists but is not a page"
    return Dangle("c", reason)


def cap_note(ctx: Ctx) -> str:
    return (
        f"(the vault is at its cap of {ctx.vault.config.cap} groups, so a new group "
        "page would break SCAT-CAP; choose an existing group)"
    )


def typeless_edit(ctx: Ctx, path: str, type_key: str, name: str) -> FixOption:
    """Variant (b): the lines that turn a file with no `type` into a stub page, as `set-field` edits."""
    want = {"type": type_key, "status": "stub", "title": title_from_name(name)}

    def line(k: str) -> str:
        return f"`{k}: {quote(want[k]) if k == 'title' else want[k]}`"

    lines = ctx.file_lines(path)
    close = next((i for i in range(1, len(lines)) if lines[i] == "---"), None)
    if lines[0] != "---" or close is None:
        rows = ", ".join(line(k) for k in want)
        text = (
            f"put these lines in a block between two `---` lines at the very top of {path}: {rows}"
        )
        return fixes.option("exact", text, *(fixes.set_field(path, k, v) for k, v in want.items()))
    present = {}
    for ln in lines[1:close]:
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", ln)
        if m:
            present[m.group(1)] = m.group(2).strip()
    parts = []
    adds = [k for k in want if k not in present]
    if adds:
        parts.append(
            f"add these lines to the frontmatter of {path}: " + ", ".join(line(k) for k in adds)
        )
    empties = [k for k in want if present.get(k) == ""]
    for k in empties:
        parts.append(f"replace the line `{k}:` in {path} with {line(k)}")
    return fixes.option(
        "exact",
        "; ".join(parts),
        *(fixes.set_field(path, k, want[k]) for k in [*adds, *empties]),
    )


def then(first: FixOption, made: FixOption) -> FixOption:
    """Two things in one option, in order: `first`, then `made` (its edits follow, its command runs last)."""
    if first.kind == "manual":  # the replacement cannot be placed, so neither can what follows it
        return FixOption("manual", f"{first.text}, then {made.text}")
    return FixOption(
        "exact", f"{first.text}, then {made.text}", made.command, (*first.edits, *made.edits)
    )


def derive(ctx: Ctx, target: str) -> str | None:
    """The derived name of a target that is not legal; the free one when a file already has the name."""
    d = derived_name(target, ctx.taken)
    if d and d not in ctx.vault.by_name and d not in ctx.typeless and d.lower() in ctx.taken:
        return free_name(target, ctx.taken)
    return d


def inferred_types(ctx: Ctx, name: str) -> tuple[list[str], bool]:
    """The types a body link to `name` may be stubbed as (catalogue, "Inferred types"), and whether they
    are inferred from the row ends that name it (else the five the stub operation makes)."""
    found = ctx.row_layers.get(name)
    if found:
        return sorted(found), True
    return [*NODE_TYPES, NARRATIVE], False  # the types `scat stub` makes: never a contributor page


def creations(ctx: Ctx, name: str, types: list[str]) -> tuple[list[FixOption], list[str]]:
    """What creates a page `name`: one option per type, and the notes (the cap withholds a group)."""
    notes = []
    types = list(types)
    if NODE_TYPES[0] in types and ctx.at_cap:
        types.remove(NODE_TYPES[0])
        notes.append(cap_note(ctx))
    if name in ctx.typeless:
        return [typeless_edit(ctx, ctx.typeless[name], k, name) for k in types], notes
    return [
        fixes.run_option(fixes.stub(name, k), suffix=f" to create {article(k)} {k} page")
        for k in types
    ], notes


def repairs(
    ctx: Ctx,
    target: str,
    d: Dangle,
    *,
    pool: list[str],
    types: list[str],
    only_types: set[str] | None,
    swap: Callable[[str], FixOption],
) -> tuple[list[FixOption], list[str]]:
    """The replacement and creation options for a link to `target` that reaches no page (variants a, b, c).

    `pool` is where the near match is looked for; `types` the types a page may be created as; `only_types`, when
    given, the types of an existing page a replacement may name (a page of another type would link the wrong page).
    """
    opts: list[FixOption] = []
    notes: list[str] = []
    near = near_match(target, pool)

    def fits(name: str) -> bool:
        if only_types is None:
            return True
        page = ctx.page(name)
        return page is not None and ctx.type_key(page) in only_types

    if d.kind in ("a", "b"):
        if near and fits(near):
            opts.append(swap(near))
        made, more = creations(ctx, target, types)
        opts += made
        notes += more
    else:
        names = [n for n in dict.fromkeys([near, derive(ctx, target)]) if n]
        if not names:
            notes.append(HAND)
        for n in names:
            if n in ctx.vault.by_name:
                if fits(n):
                    opts.append(swap(n))
            elif n in ctx.typeless or n.lower() not in ctx.taken:
                made, more = creations(ctx, n, types)
                opts += [then(swap(n), m) for m in made]
                notes += more
    return opts, notes


def fix_of(opts: list[FixOption], notes: list[str]) -> Fix:
    """Alternatives (kind `options`), or manual when there is nothing to offer; the notes follow, once each."""
    notes = list(dict.fromkeys(notes))
    if opts:
        return fixes.alternatives(opts, None, tuple(notes))
    return fixes.single(FixOption("manual", " ".join(notes) or HAND))


@page_rule
def link_dangling_body(ctx: Ctx, page: Page):
    out = []
    pool = sorted(ctx.vault.by_name, key=lambda s: s.encode())
    ends = ctx.row_ends(page)
    for link in page.body_links:
        if (link.line, link.column) in ends and ctx.is_narrative(page):
            continue  # a row end: SCAT-*-END-NOPAGE grades it
        d = classify(ctx, link.target)
        if d is None:
            continue
        target = link.target
        lit = literal(ctx, page, link)

        def swap(name: str, link=link, lit=lit) -> FixOption:
            new = lit.with_name(name)
            return fixes.option(
                "exact",
                f"on line {link.line} replace `{lit.text}` with `{new}`",
                fixes.replace_text(page.path, link.line, lit.text, new, column=link.column),
            )

        types, inferred = inferred_types(ctx, target)
        opts, notes = repairs(
            ctx,
            target,
            d,
            pool=pool,
            types=types,
            only_types=set(types) if inferred else None,
            swap=swap,
        )
        opts.append(
            fixes.option(
                "exact",
                f"on line {link.line} replace `{lit.text}` with `{lit.shown}` to keep the words and drop the link",
                fixes.replace_text(page.path, link.line, lit.text, lit.shown, column=link.column),
            )
        )
        out.append(
            ctx.problem(
                "SCAT-LINK-DANGLING-BODY",
                page.path,
                f"link [[{target}]]",
                f"does not reach a page ({d.reason})",
                fix_of(opts, notes),
                line=link.line,
                pos=link.column,
                target=target,
            )
        )
    return out
