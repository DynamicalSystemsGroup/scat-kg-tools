"""Stubs: the pages that links entail and are missing (contract section 5).

Writes only new files, never an existing page, and only when called: checks never run it. A call that
refuses creates nothing. Relation pages are made only for a pair the author names (log D-031).
"""

from pathlib import Path

from scat_kg.ops.common import find_page, open_vault, taken_names
from scat_kg.ops.files import create_files
from scat_kg.ops.names import (
    STUBBABLE,
    derive_name,
    name_problem,
    quote,
    title_from_name,
)
from scat_kg.ops.result import Refusal, Result, refused
from scat_kg.tbox import TBOX
from scat_kg.vault import Vault

GROUP = "stakeholder-group"
_OPPOSITE = {"raw": "coded", "coded": "raw"}


def stub_text(slug: str, title: str, extra: tuple[tuple[str, list[str]], ...] = ()) -> str:
    """The skeleton of section 5. `extra` lists link fields to write after the title, in order:
    (key, names); one name on a single-link field is written as a scalar, otherwise as a list."""
    out = f"---\ntype: {slug}\nstatus: stub\ntitle: {quote(title)}\n"
    for f in TBOX.page_types[slug].required:  # a value-set field: no value, the values as a comment
        if f.value_set is not None and f.required_from == "done":
            out += f"{f.key}: # {' | '.join(f.value_set)}\n"
    for key, names in extra:
        field = TBOX.page_types[slug].field(key)
        if field is not None and field.single:
            out += f'{key}: "[[{names[0]}]]"\n'
        else:
            out += f"{key}:\n" + "".join(f'  - "[[{n}]]"\n' for n in names)
    return out + "---\n"


def _holders(vault: Vault, name: str) -> list[str]:
    """Paths of every `.md` file whose name is `name`, compared without regard to case."""
    paths = [p.path for p in vault.pages if p.name.lower() == name.lower()]
    paths += [
        p
        for p in vault.non_pages
        if p.rsplit("/", 1)[-1].removesuffix(".md").lower() == name.lower()
    ]
    return sorted(paths)


def _derived_links(vault: Vault, slug: str, name: str) -> tuple[tuple[str, list[str]], ...]:
    """The opposite raw/coded link a new raw or coded page starts with (section 5), else nothing."""
    out = []
    for f in TBOX.page_types[slug].fields:
        if f.key in _OPPOSITE and f.is_link:
            back = _OPPOSITE[f.key]
            names = sorted(
                p.name
                for p in vault.of_type(f.target_type)
                if any(l.target == name for l in p.fm_links.get(back, ()))
            )
            if names:
                out.append((f.key, names))
    return tuple(out)


def _cap_refusal(vault: Vault, new: list[str]) -> Refusal | None:
    """Section 5/10: refuse when new group stubs would take the vault over its cap."""
    if not new:
        return None
    cfg, have = vault.config, len(vault.of_type(GROUP))
    wanted = ", ".join(new)
    if cfg.cap is None:
        return Refusal(
            "scat.toml field `stakeholder_group_cap`",
            f"the cap is not usable ({cfg.problem}), so a new group page ({wanted}) cannot be allowed",
            "write `stakeholder_group_cap = <number you choose>` (author) in scat.toml, a whole "
            f"number of 1 or more (the vault has {have} stakeholder-group pages now), or link an "
            "existing group instead",
        )
    if have + len(new) <= cfg.cap:
        return None
    state = "at" if have == cfg.cap else "over"
    return Refusal(
        "scat.toml field `stakeholder_group_cap`",
        f"the vault is {state} its cap of {cfg.cap} stakeholder groups, so a new group page "
        f"({wanted}) would break SCAT-CAP; choose an existing group",
        f"either link an existing group, or write `stakeholder_group_cap = {have + len(new)}` in "
        "scat.toml (the cap protects against identifying individuals; raise it only if the plan allows)",
    )


def _write(op: str, vault: Vault, pages: list[tuple[str, str]], notes=()) -> Result:
    """Create (relative path, text) pages all or none."""
    try:
        create_files([(vault.root / rel, text) for rel, text in pages])
    except OSError as e:
        return refused(op, pages[0][0], f"could not write: {e}", "check the folder's permissions")
    return Result(op, created=tuple(rel for rel, _ in pages), notes=tuple(notes))


def stub(name: str, type: str, *, root: str | Path = ".") -> Result:
    """Create one stub page of the given type (the four class keys and the four record keys)."""
    op = "stub"
    vault, bad = open_vault(op, root)
    if bad:
        return bad
    if type not in STUBBABLE:
        why = (
            "a relation page is made only by naming its pair"
            if type in TBOX.relations
            else "a class page is made only by the index operation"
            if type == "class"
            else "this is not a page type"
        )
        fix = (
            "run `scat stub-pair <relation> <endpoint-a> <endpoint-b>` "
            '(REPL: `scat_kg.stub_pair("<relation>", "<endpoint-a>", "<endpoint-b>")`)'
            if type in TBOX.relations
            else "run `scat index` (REPL: `scat_kg.index()`)"
            if type == "class"
            else f"use one of: {', '.join(STUBBABLE)}"
        )
        return refused(op, f"type `{type}`", why, fix)
    if problem := name_problem(name):
        hint = derive_name(name, taken_names(vault))
        fix = (
            f"use the name `{hint}` (made from it by the contract's section 2)"
            if hint
            else ("choose a name by hand: only a-z, 0-9 and hyphens")
        )
        return refused(op, f"name `{name}`", problem, fix)
    if held := _holders(vault, name):
        return refused(
            op,
            f"name `{name}`",
            f"a Markdown file already has this name ({', '.join(held)}); names are compared without regard to case",
            "link to the existing page, or choose another name",
        )
    if cap := _cap_refusal(vault, [name] if type == GROUP else []):
        return Result(op, refused=(cap,))
    text = stub_text(type, title_from_name(name), _derived_links(vault, type, name))
    return _write(op, vault, [(f"{type}/{name}.md", text)])


def stub_links(ref: str | None = None, *, root: str | Path = ".") -> Result:
    """Create the pages that link fields entail and are missing, from one page or the whole vault.

    A link field entails a page of the field's target type (section 5, from the TBox). A target that
    exists (of any type), is not a legal name, or is taken in another case entails nothing and is noted.
    """
    op = "stub-links"
    vault, bad = open_vault(op, root)
    if bad:
        return bad
    pages = vault.pages
    if ref is not None:
        page, bad = find_page(op, vault, ref)
        if bad:
            return bad
        pages = (page,)
    wants: dict[str, dict[str, list[str]]] = {}  # target name -> type -> where it was linked
    notes, refusals = [], []
    for page in pages:
        ptype = TBOX.page_types.get(page.type) if isinstance(page.type, str) else None
        if ptype is None or page.frontmatter_error:
            continue
        for key, links in page.fm_links.items():
            field = ptype.field(key)
            if field is None or not field.is_link:
                continue  # an unlisted link field entails nothing
            for link in links:
                where = f"{page.path}:{link.line} field `{key}`"
                if link.target in vault.by_name:
                    continue
                if problem := name_problem(link.target):
                    notes.append(
                        f"{where}: [[{link.target}]] is not a legal name ({problem}); correct the link, nothing created"
                    )
                elif held := _holders(vault, link.target):
                    notes.append(
                        f"{where}: [[{link.target}]] is taken by {', '.join(held)}; nothing created"
                    )
                else:
                    wants.setdefault(link.target, {}).setdefault(field.target_type, []).append(
                        where
                    )
    plan: list[tuple[str, str, str]] = []  # (path, text, group name or "")
    for target in sorted(wants):
        types = wants[target]
        if len(types) > 1:
            refusals.append(
                Refusal(
                    f"name `{target}`",
                    "links name it as different types: "
                    + "; ".join(f"{t} ({', '.join(w)})" for t, w in sorted(types.items())),
                    f"fix the links so that one type remains, or run `scat stub {target} --type <type-key>`",
                )
            )
            continue
        (slug,) = types
        text = stub_text(slug, title_from_name(target), _derived_links(vault, slug, target))
        plan.append((f"{slug}/{target}.md", text, target if slug == GROUP else ""))
    if cap := _cap_refusal(vault, [g for _, _, g in plan if g]):
        return Result(op, refused=(cap, *refusals), notes=tuple(notes))
    if not plan:
        return Result(op, refused=tuple(refusals), notes=tuple(notes))
    made = _write(op, vault, [(p, t) for p, t, _ in plan])
    return Result(
        op,
        created=made.created,
        refused=made.refused + tuple(refusals),
        notes=tuple(notes),
    )


def stub_pair(relation: str, endpoint_a: str, endpoint_b: str, *, root: str | Path = ".") -> Result:
    """Create the relation page for a named pair, and stub an endpoint that does not exist.

    Creates nothing when a page of that relation already has exactly this pair, under any name.
    """
    op = "stub-pair"
    vault, bad = open_vault(op, root)
    if bad:
        return bad
    if relation not in TBOX.relations:
        return refused(
            op,
            f"relation `{relation}`",
            "this is not a relation",
            f"use one of: {', '.join(TBOX.relations)}",
        )
    keys = TBOX.relations[relation]  # endpoint fields, in the order the names are given
    rtype = TBOX.page_types[relation]
    names = (endpoint_a, endpoint_b)
    order = " then ".join(f"{k} (a {rtype.field(k).target_type})" for k in keys)
    if endpoint_a == endpoint_b:
        return refused(
            op, f"`{endpoint_a}`", "both endpoints are the same name", f"give two pages: {order}"
        )
    for page in vault.of_type(relation):
        got = tuple(tuple(l.target for l in page.fm_links.get(k, ())) for k in keys)
        if got == ((endpoint_a,), (endpoint_b,)):
            return Result(
                op,
                unchanged=(page.path,),
                notes=(f"{page.path} already states this pair, so nothing was created",),
            )
    refusals, new, titles = [], [], {}  # new: (type, name) endpoint stubs to create
    for key, name in zip(keys, names):
        want = rtype.field(key).target_type
        subject = f"{relation} {key} `{name}`"
        existing = vault.by_name.get(name, ())
        if len(existing) > 1:
            refusals.append(
                Refusal(
                    subject,
                    "more than one page has this name: " + ", ".join(p.path for p in existing),
                    "rename one of them in Obsidian, then run this again",
                )
            )
        elif existing:
            page = existing[0]
            title = page.fields.get("title")
            if page.type != want:
                refusals.append(
                    Refusal(
                        subject,
                        f"{page.path} is a `{page.type}` page, and `{key}` needs a `{want}`",
                        f"give a {want} page here (order: {order}), or run `scat stub <page-name> --type {want}` for a new one",
                    )
                )
            elif not isinstance(title, str) or not title.strip():
                refusals.append(
                    Refusal(
                        subject,
                        f"{page.path} has no title, and the relation page's title is made from it",
                        f'add the line `title: "{title_from_name(name)}"` to {page.path}, then run this again',
                    )
                )
            else:
                titles[name] = title.strip()
        elif problem := name_problem(name):
            hint = derive_name(name, taken_names(vault))
            fix = (
                f"use the name `{hint}`"
                if hint
                else "choose a name by hand: only a-z, 0-9 and hyphens"
            )
            refusals.append(
                Refusal(
                    subject, f"`{name}` does not exist and is not a legal name ({problem})", fix
                )
            )
        elif held := _holders(vault, name):
            refusals.append(
                Refusal(
                    subject,
                    f"`{name}` does not exist as a page, but {', '.join(held)} has the name",
                    "choose another name, or rename that file",
                )
            )
        else:
            new.append((want, name))
            titles[name] = title_from_name(name)
    if cap := _cap_refusal(vault, [n for t, n in new if t == GROUP]):
        refusals.append(cap)
    if refusals:
        return Result(op, refused=tuple(refusals))
    taken = taken_names(vault) | {n for _, n in new}
    title = f"{titles[endpoint_a]} {TBOX.page_types[relation].verb} {titles[endpoint_b]}"
    page_name = derive_name(title, taken)
    if page_name is None:
        return refused(
            op,
            f"title `{title}`",
            "it has no Latin letter or digit to make a name from",
            "choose a name by hand",
        )
    pages = [(f"{t}/{n}.md", stub_text(t, titles[n])) for t, n in new]
    pages.append(
        (
            f"{relation}/{page_name}.md",
            stub_text(relation, title, tuple((k, [n]) for k, n in zip(keys, names))),
        )
    )
    return _write(
        op,
        vault,
        pages,
        [
            f"write `description`, `notes` and the body in {relation}/{page_name}.md; the endpoints are filled"
        ],
    )
