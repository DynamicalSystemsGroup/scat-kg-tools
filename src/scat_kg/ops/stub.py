"""The stub operations: pages that a link or a row end entails (page contracts 6).

Writes only new files, never an existing page (a stub of a page that exists with the same type is a
no-op, as stub-pair is), and only when called: checks never run it. A call that
refuses creates nothing. The end of a row entails a node of the layer its type fixes; any other link entails
a page but not its type, so `stub` makes it only when it is given the type.
"""

from pathlib import Path

from scat_kg.fix import FixOption
from scat_kg.graph import read_table
from scat_kg.ops.common import find_page, open_vault, taken_names
from scat_kg.ops.files import create_files
from scat_kg.ops.names import (
    CONTRIBUTOR,
    STUBBABLE,
    derive_name,
    name_problem,
    quote,
    title_from_name,
)
from scat_kg.ops.result import Refusal, Result, refusal, refused, reports_mode, run_option
from scat_kg.tbox import TBOX
from scat_kg.vault import Page, Vault

GROUP = TBOX.layers[0]
NARRATIVE = TBOX.table_type.slug


def stub_text(slug: str, title: str) -> str:
    """The skeleton of page contracts 6: `type`, `status: stub`, `title`, and for a type with a value-set field
    required from `done` (a narrative's `timeframe`) the key with no value."""
    out = f"---\ntype: {slug}\nstatus: stub\ntitle: {quote(title)}\n"
    for f in TBOX.page_types[slug].required:
        if f.value_set is not None and f.required_from == "done":
            out += f"{f.key}:\n"
    return out + "---\n"


def holders(vault: Vault, name: str) -> list[str]:
    """Paths of every `.md` file whose name is `name`, compared without regard to case."""
    paths = [p.path for p in vault.pages if p.name.lower() == name.lower()]
    paths += [
        p
        for p in vault.non_pages
        if p.rsplit("/", 1)[-1].removesuffix(".md").lower() == name.lower()
    ]
    return sorted(paths)


def name_refusal(
    vault: Vault, name: str, subject: str | None = None, type: str | None = None
) -> Refusal | None:
    """Why `name` cannot be the name of a new page: not legal, or a Markdown file already has it."""
    subject = subject or f"name `{name}`"
    if problem := name_problem(name):
        hint = derive_name(name, taken_names(vault))
        if hint and type:
            return refusal(
                subject,
                problem,
                f"run `scat stub {hint} --type {type}` (the name `{hint}` is made from it by the contract's section 2)",
                run_option(
                    f"run `scat stub {hint} --type {type}`",
                    ("stub", hint, "--type", type),
                    f'scat_kg.stub("{hint}", type="{type}")',
                ),
            )
        fix = (
            f"use the name `{hint}` (made from it by the contract's section 2)"
            if hint
            else "choose a name by hand: only a-z, 0-9 and hyphens"
        )
        return Refusal(subject, problem, fix)
    if held := holders(vault, name):
        return Refusal(
            subject,
            f"a Markdown file already has this name ({', '.join(held)}); names are compared without regard to case",
            "link to the existing page, or choose another name",
        )
    return None


def cap_refusal(vault: Vault, new: list[str]) -> Refusal | None:
    """Page contracts 6 and 10: refuse when new group stubs would take the vault over its cap."""
    if not new:
        return None
    cfg, have = vault.config, len(vault.of_type(GROUP))
    wanted = ", ".join(new)
    if cfg.cap is None:
        return Refusal(
            "scat.toml field `stakeholder_group_cap`",
            f"the cap is not usable ({cfg.problem}), so a new group page ({wanted}) cannot be allowed",
            "write `stakeholder_group_cap = <number you choose>` (author) in scat.toml, a whole "
            f"number of 1 or more (the vault has {have} group pages now), or link an existing group instead",
        )
    if have + len(new) <= cfg.cap:
        return None
    state = "at" if have == cfg.cap else "over"
    return Refusal(
        "scat.toml field `stakeholder_group_cap`",
        f"the vault is {state} its cap of {cfg.cap} groups, so a new group page ({wanted}) "
        "would break SCAT-CAP; choose an existing group",
        f"either link an existing group, or write `stakeholder_group_cap = {have + len(new)}` in "
        "scat.toml (the cap protects against identifying individuals; raise it only if the plan allows)",
    )


def write_new(op: str, vault: Vault, pages: list[tuple[str, str]], notes=()) -> Result:
    """Create (relative path, text) pages, all or none."""
    try:
        create_files([(vault.root / rel, text) for rel, text in pages])
    except OSError as e:
        return refused(op, pages[0][0], f"could not write: {e}", "check the folder's permissions")
    return Result(op, created=tuple(rel for rel, _ in pages), notes=tuple(notes))


def mode_refusal(vault: Vault, type: str) -> Result | None:
    """The refusal of a contributor page where the vault's mode does not enable attribution (else None)."""
    if type != CONTRIBUTOR or vault.config.attribution in ("required", "optional"):
        return None
    if vault.config.attribution == "disallowed":
        return refused(
            "stub",
            f"type `{type}`",
            "this vault's attribution mode is `disallowed`, so it holds no contributor page (SCAT-ATTR-DISALLOWED)",
            "the coder who wants contributor pages changes `attribution` in scat.toml for the whole vault; "
            "the tool does not change it",
        )
    return refused(
        "stub",
        f"type `{type}`",
        "the vault declares no usable attribution mode, so it is not known whether it may hold a contributor page",
        'write `attribution = "required"`, `"optional"` or `"disallowed"` in scat.toml '
        "(`scat check` says which problem it has), then run this again",
    )


def _wrong_type(type: str) -> Result | None:
    """The refusal for a `type` that is not one a stub may have, with the command that does what was meant."""
    if type in STUBBABLE:
        return None
    if type == "index":
        why = "an index page is made only by the index operation"
        text = "run `scat index` (REPL: `scat_kg.index()`)"
        return Result(
            "stub",
            refused=(
                refusal(
                    f"type `{type}`", why, text, run_option(text, ("index",), "scat_kg.index()")
                ),
            ),
        )
    if TBOX.edge_type_named(type) is not None:
        return refused(
            "stub",
            f"type `{type}`",
            "an edge is a row of a narrative, not a page",
            "run `scat record-edge <type> <from> <to> --told-by <narrative>` "
            '(REPL: `scat_kg.record_edge("<type>", "<from>", "<to>", ["<narrative>"])`)',
        )
    return refused(
        "stub", f"type `{type}`", "this is not a page type", f"use one of: {', '.join(STUBBABLE)}"
    )


@reports_mode
def stub(name: str, type: str | None = None, *, root: str | Path = ".") -> Result:
    """Create one stub page of the given type (a node type, `narrative`, or `contributor` where the mode allows it)."""
    op = "stub"
    vault, bad = open_vault(op, root)
    if bad:
        return bad
    if type is None:
        return refused(
            op,
            f"name `{name}`",
            "a stub needs its type: a link says a page is wanted, not what it is",
            f"give the type, one of: {', '.join(STUBBABLE)}",
        )
    if wrong := _wrong_type(type) or mode_refusal(vault, type):
        return wrong
    same = vault.by_name.get(name, ())
    if len(same) == 1 and same[0].type == type:
        return Result(
            op,
            unchanged=(same[0].path,),
            notes=(f"{same[0].path} already exists, so nothing was written",),
        )
    if bad_name := name_refusal(vault, name, type=type):
        return Result(op, refused=(bad_name,))
    if cap := cap_refusal(vault, [name] if type == GROUP else []):
        return Result(op, refused=(cap,))
    return write_new(op, vault, [(f"{type}/{name}.md", stub_text(type, title_from_name(name)))])


def _wants(vault: Vault, pages: tuple[Page, ...]):
    """What the pages' links ask for: ({name: {layer: [where]}}, notes). Only a row end names a layer."""
    wants: dict[str, dict[str, list[str]]] = {}
    notes: list[str] = []
    typed: set[str] = set()  # names some row end gives a layer, so they are not reported as untyped
    untyped: list[tuple[str, str, int]] = []  # (target, path, line) of a link that reaches no page
    for page in pages:
        if page.frontmatter_error:
            continue
        ends: set[tuple[int, int]] = set()
        if page.type == NARRATIVE:
            table = read_table(page.body.split("\n"), page.body_line).table
            for row in table.rows if table else ():
                et = TBOX.edge_types.get(row.edge_type or "")
                if et is None or not row.well_formed:
                    continue  # an unknown type entails nothing; a malformed row is graded by the check
                for holds, layer in (("from", et.from_type), ("to", et.to_type)):
                    cell = row.cell(holds)
                    if cell is None or cell.target is None:
                        continue  # an end that is not one link entails nothing
                    ends.add((cell.line, cell.column))
                    target, where = cell.target, f"{page.path}:{cell.line} row {row.n}"
                    if target in vault.by_name:
                        continue  # a page that exists, of whatever type, is the check's business
                    typed.add(target)
                    if problem := name_problem(target):
                        notes.append(
                            f"{where}: [[{target}]] is not a legal name ({problem}); correct the link, nothing created"
                        )
                    elif held := holders(vault, target):
                        notes.append(
                            f"{where}: [[{target}]] is taken by {', '.join(held)}; nothing created"
                        )
                    else:
                        wants.setdefault(target, {}).setdefault(layer, []).append(where)
        for link in page.links:
            if link.target not in vault.by_name and (link.line, link.column) not in ends:
                untyped.append((link.target, page.path, link.line))
    for target, path, line in untyped:
        if target not in typed and not name_problem(target) and not holders(vault, target):
            notes.append(
                f"{path}:{line}: [[{target}]] reaches no page, and nothing says what it is; "
                f'run `scat stub {target} --type <type>` (REPL: `scat_kg.stub("{target}", type="<type>")`)'
            )
    return wants, list(dict.fromkeys(notes))


@reports_mode
def stub_links(page: str | None = None, *, root: str | Path = ".") -> Result:
    """Create the node pages that the ends of rows link and the vault lacks, from one page or the whole vault.

    The end of a row entails a node of the layer its type fixes (page contracts 6). Any other link entails a page
    but not its type, so it is only reported. A link that is not a legal name, or is taken by a Markdown file that
    is not a page, entails nothing and is noted.
    """
    op = "stub-links"
    vault, bad = open_vault(op, root)
    if bad:
        return bad
    pages = vault.pages
    if page is not None:
        found, bad = find_page(op, vault, page)
        if bad:
            return bad
        pages = (found,)
    wants, notes = _wants(vault, pages)
    refusals: list[Refusal] = []
    plan: list[tuple[str, str, str]] = []  # (path, text, group name or "")
    for target in sorted(wants):
        layers = wants[target]
        if len(layers) > 1:
            refusals.append(
                refusal(
                    f"name `{target}`",
                    "rows name it as different types: "
                    + "; ".join(f"{t} ({', '.join(w)})" for t, w in sorted(layers.items())),
                    f"fix the rows so that one type remains, or run `scat stub {target} --type <type>`",
                    FixOption("manual", "fix the rows so that one type remains"),
                    run_option(
                        f"run `scat stub {target} --type <type>`",
                        ("stub", target, "--type", "<type>"),
                        f'scat_kg.stub("{target}", type="<type>")',
                        "<type>",
                    ),
                )
            )
            continue
        (layer,) = layers
        plan.append(
            (
                f"{layer}/{target}.md",
                stub_text(layer, title_from_name(target)),
                target if layer == GROUP else "",
            )
        )
    if cap := cap_refusal(vault, [g for _, _, g in plan if g]):
        nothing = Refusal(
            cap.subject,
            f"{cap.why}; the group stubs are all or none, so nothing created",
            cap.fix,
            cap.fix_data,
        )
        return Result(op, refused=(nothing, *refusals), notes=tuple(notes))
    if not plan:
        return Result(op, refused=tuple(refusals), notes=tuple(notes))
    made = write_new(op, vault, [(p, t) for p, t, _ in plan])
    return Result(
        op, created=made.created, refused=made.refused + tuple(refusals), notes=tuple(notes)
    )
