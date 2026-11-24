"""Links that reach no page: SCAT-LINK-DANGLING (frontmatter) and SCAT-LINK-DANGLING-BODY (body).

Three variants share the id (catalogue, SCAT-LINK-DANGLING): (a) a legal name and no such file; (b) a legal
name for which a Markdown file exists that has no `type`; (c) a name that is not legal.
"""

import re
from dataclasses import dataclass

from scat_kg.checks import fixes
from scat_kg.checks.ctx import Ctx, page_rule
from scat_kg.checks.links import body_swap, link_value, list_with, offer
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
from scat_kg.tbox import TBOX
from scat_kg.vault import Link, Page

CLASS_KEYS = ("stakeholder-group", "concern", "affordance", "technology")
HAND = "choose a legal page name by hand (contract section 2), then write the link with it"


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
        f"(the vault is at its cap of {ctx.vault.config.cap} stakeholder groups, so a new group "
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


def _fix(opts: list[FixOption], notes: list[str]) -> Fix:
    notes = list(dict.fromkeys(notes))
    if opts:
        return offer(opts, tuple(notes))
    return fixes.single(FixOption("manual", " ".join(notes) or HAND))


def then(first: FixOption, made: FixOption) -> FixOption:
    """Two things in one option, in order: `first`, then `made` (its edits follow, its command runs last)."""
    return FixOption(
        "exact", f"{first.text}, then {made.text}", made.command, (*first.edits, *made.edits)
    )


def derive(ctx: Ctx, target: str) -> str | None:
    """The derived name of a target that is not legal; the free one when a file already has the name."""
    d = derived_name(target, ctx.taken)
    if d and d not in ctx.vault.by_name and d not in ctx.typeless and d.lower() in ctx.taken:
        return free_name(target, ctx.taken)
    return d


@page_rule
def link_dangling(ctx: Ctx, page: Page):
    if not ctx.typed(page):
        return []
    out = []
    for f in TBOX.page_types[page.type_key].fields:
        if not f.is_link:
            continue
        for link in ctx.links(page, f.key):
            d = classify(ctx, link.target)
            if d is not None:
                out.append(_front_problem(ctx, page, f.key, f.target_type, link, d))
    return out


def _front_problem(ctx: Ctx, page: Page, key: str, expected: str, link: Link, d: Dangle):
    target = link.target
    item = ctx.item(page, key, target)
    single = TBOX.page_types[page.type_key].field(key).single
    group_capped = expected == "stakeholder-group" and ctx.at_cap
    opts: list[FixOption] = []
    notes: list[str] = []
    near = near_match(target, ctx.names_of_type(expected))

    def swap(name: str, tail: str = "") -> FixOption:
        value = link_value(name) if single else list_with(page, key, link, name)
        return fixes.option(
            "exact",
            f"replace `{item}` with `{ctx.item(page, key, name)}`{tail}",
            fixes.set_field(page.path, key, value),
        )

    def create(name: str) -> FixOption | None:
        """What creates a page `name` of the expected type; None when the cap withholds it."""
        if group_capped:
            notes.append(cap_note(ctx))
            return None
        if name in ctx.typeless:
            return typeless_edit(ctx, ctx.typeless[name], expected, name)
        return fixes.run_option(fixes.stub(name, expected), suffix=" to create it as a stub")

    if d.kind in ("a", "b"):
        if near:
            opts.append(swap(near, f" (the closest existing {expected} page)"))
        made = create(target)
        if made:
            opts.append(made)
    else:
        derived = derive(ctx, target)
        names = [n for n in dict.fromkeys([near, derived]) if n]
        if not names:
            notes.append(HAND)
        for n in names:
            existing = ctx.page(n)
            if existing is not None:
                if existing.type_key == expected:
                    opts.append(swap(n))
                else:
                    notes.append(
                        f"(`{n}` is {article(existing.type_key)} {existing.type_key} page, so replacing the link with it "
                        "would only trade this error for SCAT-LINK-ENDPOINT)"
                    )
            elif n in ctx.typeless or n.lower() not in ctx.taken:
                made = create(n)
                if made:
                    opts.append(then(swap(n), made))
    return ctx.problem(
        "SCAT-LINK-DANGLING",
        page.path,
        f"field `{key}`",
        f"[[{target}]] does not reach a page ({d.reason})",
        _fix(opts, notes),
        line=link.line,
        pos=ctx.pos(page, key),
        target=target,
        on=key,
    )


def inferred_types(ctx: Ctx, page: Page, name: str) -> tuple[list[str], list[str]]:
    """The class types a body link to `name` may be stubbed as, and those left out (catalogue decision 3)."""
    found = set()
    for p in ctx.vault.pages:
        if not ctx.typed(p):
            continue
        for key, links in p.fm_links.items():
            f = TBOX.page_types[p.type_key].field(key)
            if f and f.target_type in CLASS_KEYS and any(l.target == name for l in links):
                found.add(f.target_type)
    types = sorted(found) if found else list(CLASS_KEYS)
    discouraged = TBOX.page_types[page.type_key].discouraged_body_links if ctx.typed(page) else ()
    return [k for k in types if k not in discouraged], [k for k in types if k in discouraged]


def _creations(ctx: Ctx, page: Page, name: str) -> tuple[list[FixOption], list[str]]:
    """What creates a page `name` from a body link: one option per inferred type, and the notes."""
    types, left = inferred_types(ctx, page, name)
    ptype = page.type_key
    notes = [f"({k} left out: {article(ptype)} {ptype} page should not link to it)" for k in left]
    if "stakeholder-group" in types and ctx.at_cap:
        types.remove("stakeholder-group")
        notes.append(cap_note(ctx))
    if name in ctx.typeless:
        return [typeless_edit(ctx, ctx.typeless[name], k, name) for k in types], notes
    return [
        fixes.run_option(fixes.stub(name, k), suffix=f" to create {article(k)} {k} page")
        for k in types
    ], notes


@page_rule
def link_dangling_body(ctx: Ctx, page: Page):
    out = []
    pool = sorted(ctx.vault.by_name, key=lambda s: s.encode())
    for link in page.body_links:
        d = classify(ctx, link.target)
        if d is None:
            continue
        target, line = link.target, link.line

        def swap(name: str, link: Link = link) -> FixOption:
            return body_swap(page, link, link_value(name))

        opts: list[FixOption] = []
        notes: list[str] = []
        near = near_match(target, pool)
        if d.kind in ("a", "b"):
            if near:
                opts.append(swap(near))
            made, more = _creations(ctx, page, target)
            opts += made
            notes += more
        else:
            names = [n for n in dict.fromkeys([near, derive(ctx, target)]) if n]
            if not names:
                notes.append(HAND)
            for n in names:
                if n in ctx.vault.by_name:
                    opts.append(swap(n))
                elif n in ctx.typeless or n.lower() not in ctx.taken:
                    made, more = _creations(ctx, page, n)
                    opts += [then(swap(n), m) for m in made]
                    notes += more
        opts.append(body_swap(page, link, target, " to keep the words and drop the link"))
        notes.append(
            "(you can also name the page in the right link field of this page, which entails its "
            "stub with that type)"
        )
        out.append(
            ctx.problem(
                "SCAT-LINK-DANGLING-BODY",
                page.path,
                f"link [[{target}]]",
                f"does not reach a page ({d.reason})",
                _fix(opts, notes),
                line=line,
                target=target,
            )
        )
    return out
