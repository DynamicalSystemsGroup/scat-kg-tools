"""record-edge and remove-edge: an edge is a row of a narrative's table, so these add and delete rows.

Recording stubs a missing end node or narrative, adds a row only where the narrative has none, and leaves every link
as it is. Removing deletes rows and leaves the links. Both refuse, writing nothing, when a narrative they would change
is `done`: the coder sets it to `draft` first. The refusals carry no rule id (rule catalogue, section 8).
"""

import json
from collections.abc import Sequence
from pathlib import Path

from scat_kg.fix import Command, FixOption
from scat_kg.graph import add_row, load, read_table, remove_rows
from scat_kg.ops.common import open_vault
from scat_kg.ops.files import create_files, replace_file
from scat_kg.ops.names import title_from_name
from scat_kg.ops.result import (
    EdgeRef,
    EdgeResult,
    Refusal,
    Result,
    RowRef,
    refusal,
    reports_mode,
    run_option,
)
from scat_kg.ops.stub import cap_refusal, name_refusal, stub_text
from scat_kg.tbox import TBOX
from scat_kg.vault import Page, Vault, _lines, _split

NARRATIVE = TBOX.table_type.slug
SLUGS = ", ".join(TBOX.edge_types)
LAYERS = "; ".join(f"{s}: {e.from_type} to {e.to_type}" for s, e in TBOX.edge_types.items())


def _names(value: str | Sequence[str] | None) -> list[str]:
    if value is None:
        return []
    items = [value] if isinstance(value, str) else list(value)
    return list(dict.fromkeys(items))


def _py(text: str) -> str:
    return json.dumps(text, ensure_ascii=False)


def _what(page: Page) -> str:
    return f"a `{page.type}` page" if page.type_key else "a page with no valid `type`"


def _read(vault: Vault, page: Page) -> str | Refusal:
    try:
        data = (vault.root / page.path).read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        return Refusal(
            page.path, "the file is not valid UTF-8", "save the file as UTF-8, then run this again"
        )
    return data


def _rows_for(text: str, slug: str, from_: str, to: str):
    """The well-formed rows of the narrative's table that tell (slug, from_, to), and the whole reading."""
    lines = _lines(text.removeprefix("﻿"))
    close, opens = _split(lines)
    if not opens or close is None:
        return [], None
    table = read_table(lines[close + 1 :], close + 2).table
    rows = [
        r
        for r in (table.rows if table else ())
        if r.well_formed and (r.edge_type, r.from_target, r.to_target) == (slug, from_, to)
    ]
    return rows, table


def _done_refusal(page: Page, what: str) -> Refusal:
    cmd = Command(("set-status", page.name, "draft"), f'scat_kg.set_status("{page.name}", "draft")')
    text = (
        f"set the narrative to `draft` with `scat set-status {page.name} draft` "
        f"(REPL: `{cmd.repl}`), run this again, then set it to `done` again; the page is checked then"
    )
    return refusal(
        page.path,
        f"the narrative is `done` and {what} would change it; changing a `done` narrative is your step",
        text,
        FixOption("exact", text, cmd),
    )


def _write(changes: list[tuple[Path, bytes, bytes]], new: list[tuple[Path, str]]) -> Refusal | None:
    """Create the new files, then replace the changed ones; on a failure put everything back."""
    done: list[tuple[Path, bytes]] = []
    try:
        create_files(new)
        for path, was, now in changes:
            replace_file(path, now)
            done.append((path, was))
    except OSError as e:
        for path, was in done:
            replace_file(path, was)
        for path, _ in new:
            path.unlink(missing_ok=True)
        return Refusal("the vault", f"could not write: {e}", "check the files' permissions")
    return None


def _sorted(names) -> tuple[str, ...]:
    return tuple(sorted(set(names), key=lambda s: s.encode()))


def _after(root, slug: str, from_: str, to: str) -> EdgeRef:
    edge = load(root).edge(slug, from_, to)
    return EdgeRef(slug, from_, to, _sorted(edge.narratives) if edge else ())


def _body_text(raw: str) -> tuple[str, bool]:
    return raw.removeprefix("﻿"), raw.startswith("﻿")


def _ends_refusals(vault: Vault, et, from_: str, to: str) -> tuple[list[Refusal], dict[str, str]]:
    """Refusals for the two ends, and {name: layer} of the ends to stub."""
    refusals: list[Refusal] = []
    new: dict[str, str] = {}
    if from_ == to:
        return [
            Refusal(
                f"`{from_}`", "both ends are the same name", "give two nodes of different layers"
            )
        ], new
    pages: dict[str, Page | None] = {}
    for label, name, layer in (("from", from_, et.from_type), ("to", to, et.to_type)):
        found = vault.by_name.get(name, ())
        if len(found) > 1:
            refusals.append(
                Refusal(
                    f"{label} `{name}`",
                    "more than one page has this name: " + ", ".join(p.path for p in found),
                    "rename one of them in Obsidian, then run this again",
                )
            )
        elif found:
            pages[name] = found[0]
            if found[0].type != layer:
                refusals.append(_layer_refusal(vault, et, label, name, found[0], from_, to))
        elif bad := name_refusal(vault, name, f"{label} `{name}`"):
            refusals.append(bad)
        else:
            new[name] = layer
    return refusals, new


def _a(word: str) -> str:
    return f"an {word}" if word[:1] in "aeiou" else f"a {word}"


def _layer_refusal(
    vault: Vault, et, label: str, name: str, page: Page, from_: str, to: str
) -> Refusal:
    want = et.from_type if label == "from" else et.to_type
    why = f"{page.path} is {_what(page)}, and `{et.slug}` needs {_a(want)} at its {label} end"
    a, b = vault.by_name.get(from_), vault.by_name.get(to)
    ta, tb = (a[0].type if a and len(a) == 1 else None), (b[0].type if b and len(b) == 1 else None)
    if (ta, tb) == (et.to_type, et.from_type):
        return Refusal(
            f"{label} `{name}`",
            why,
            f"give the ends the other way round: `{to}` first, then `{from_}`",
        )
    other = TBOX.edge_type_between(ta, tb) if ta and tb else None
    if other is not None:
        return Refusal(
            f"{label} `{name}`",
            why,
            f"these ends fit `{other.slug}`: use that type instead of `{et.slug}`",
        )
    return Refusal(
        f"{label} `{name}`",
        why,
        f"give a {want} here, or another type of edge ({LAYERS})",
    )


@reports_mode
def record_edge(
    type: str,
    from_: str,
    to: str,
    told_by: str | Sequence[str],
    note: str = "",
    *,
    root: str | Path = ".",
) -> EdgeResult | Result:
    """Record an edge: add its row to each narrative in `told_by` that has none, stubbing what is missing."""
    op = "record-edge"
    vault, bad = open_vault(op, root)
    if bad:
        return bad
    et = TBOX.edge_type_named(type) if isinstance(type, str) else None
    if et is None:
        return Result(
            op,
            refused=(
                Refusal(
                    f"type `{type}`",
                    "this is not an edge type",
                    f"use one of: {SLUGS} ({LAYERS})",
                ),
            ),
        )
    narratives = _names(told_by)
    if not narratives:
        return Result(
            op,
            refused=(
                Refusal(
                    "told-by",
                    "no narrative is named",
                    "name the narrative that tells this edge, e.g. `--told-by saturday-at-the-lending-desk`",
                ),
            ),
        )
    refusals, new_nodes = _ends_refusals(vault, et, from_, to)
    plan_new: list[tuple[str, str]] = []  # (path, text)
    changes: list[tuple[Path, bytes, bytes]] = []
    rows_for: list[tuple[str, str, str]] = []  # (narrative, path, text after) of the rows added
    unchanged: list[str] = []
    changed_paths: list[str] = []
    for n in narratives:
        found = vault.by_name.get(n, ())
        if len(found) > 1:
            refusals.append(
                Refusal(
                    f"narrative `{n}`",
                    "more than one page has this name: " + ", ".join(p.path for p in found),
                    "rename one of them in Obsidian, then run this again",
                )
            )
            continue
        if not found:
            if bad_name := name_refusal(vault, n, f"narrative `{n}`"):
                refusals.append(bad_name)
                continue
            path = f"{NARRATIVE}/{n}.md"
            made = add_row(stub_text(NARRATIVE, title_from_name(n)), path, et.slug, from_, to, note)
            plan_new.append((path, made.text))
            rows_for.append((n, path, made.text))
            continue
        page = found[0]
        if page.type != NARRATIVE or page.frontmatter_error:
            why = (
                f"its frontmatter cannot be read ({page.frontmatter_error.reason})"
                if page.frontmatter_error
                else f"it is {_what(page)}, and only a narrative tells an edge"
            )
            refusals.append(
                Refusal(
                    f"narrative `{n}`",
                    f"{page.path}: {why}",
                    "name a narrative with `--told-by`, or make one with "
                    f"`scat stub <name> --type {NARRATIVE}`",
                )
            )
            continue
        raw = _read(vault, page)
        if isinstance(raw, Refusal):
            refusals.append(raw)
            continue
        text, bom = _body_text(raw)
        if _rows_for(text, et.slug, from_, to)[0]:
            unchanged.append(page.path)
            continue
        if page.status == "done":
            refusals.append(_done_refusal(page, "this row"))
            continue
        made = add_row(text, page.path, et.slug, from_, to, note)
        if not made.ok:
            refusals.append(
                Refusal(
                    page.path,
                    made.refusal,
                    f"correct the table by hand (`scat check {page.name}` names the fix), then run this again",
                )
            )
            continue
        after = ("﻿" if bom else "") + made.text
        changes.append((vault.root / page.path, raw.encode("utf-8"), after.encode("utf-8")))
        changed_paths.append(page.path)
        rows_for.append((n, page.path, made.text))
    if cap := cap_refusal(vault, [n for n, layer in new_nodes.items() if layer == TBOX.layers[0]]):
        refusals.append(cap)
    if refusals:
        return Result(op, refused=tuple(refusals))
    for name, layer in new_nodes.items():
        plan_new.append((f"{layer}/{name}.md", stub_text(layer, title_from_name(name))))
    if bad := _write(changes, [(vault.root / p, t) for p, t in plan_new]):
        return Result(op, refused=(bad,))
    added, notes = [], []
    for n, path, text in rows_for:
        rows, _ = _rows_for(text, et.slug, from_, to)
        row = rows[-1]
        added.append(RowRef(n, path, row.line, row.note))
        notes.append(f"added `{row.text.strip()}` to {path} at line {row.line}")
    notes += [f"{p} already has this row, so nothing was written" for p in unchanged]
    created = tuple(sorted(p for p, _ in plan_new))
    return EdgeResult(
        op,
        created=created,
        changed=tuple(changed_paths),
        unchanged=tuple(unchanged),
        notes=tuple(notes),
        edge=_after(root, et.slug, from_, to),
        rows_added=tuple(added),
    )


@reports_mode
def remove_edge(
    from_: str,
    to: str,
    told_by: str | Sequence[str] | None = None,
    *,
    root: str | Path = ".",
) -> EdgeResult | Result:
    """Remove an edge: delete its rows from the narratives in `told_by`, or from every narrative that tells it."""
    op = "remove-edge"
    vault, bad = open_vault(op, root)
    if bad:
        return bad
    refusals: list[Refusal] = []
    pages: list[Page] = []
    for label, name in (("from", from_), ("to", to)):
        found = vault.by_name.get(name, ())
        if not found:
            refusals.append(
                Refusal(
                    f"{label} `{name}`",
                    "no page has this name",
                    "give the names of the two nodes the edge joins",
                )
            )
        elif len(found) > 1:
            refusals.append(
                Refusal(
                    f"{label} `{name}`",
                    "more than one page has this name: " + ", ".join(p.path for p in found),
                    "rename one of them in Obsidian, then run this again",
                )
            )
        elif found[0].type not in TBOX.layers:
            refusals.append(
                Refusal(
                    f"{label} `{name}`",
                    f"{found[0].path} is {_what(found[0])}, not a node",
                    "give the names of the two nodes the edge joins",
                )
            )
        else:
            pages.append(found[0])
    if refusals:
        return Result(op, refused=tuple(refusals))
    et = TBOX.edge_type_between(pages[0].type, pages[1].type)
    if et is None:
        back = TBOX.edge_type_between(pages[1].type, pages[0].type)
        if back is not None:
            text = f"run `scat remove-edge {to} {from_}` (REPL: `scat_kg.remove_edge({_py(to)}, {_py(from_)})`)"
            return Result(
                op,
                refused=(
                    refusal(
                        f"`{from_}` and `{to}`",
                        f"the ends are the wrong way round: `{back.slug}` goes from a {back.from_type} to a {back.to_type}",
                        text,
                        run_option(
                            text,
                            ("remove-edge", to, from_),
                            f"scat_kg.remove_edge({_py(to)}, {_py(from_)})",
                        ),
                    ),
                ),
            )
        return Result(
            op,
            refused=(
                Refusal(
                    f"`{from_}` and `{to}`",
                    f"no edge joins a {pages[0].type} and a {pages[1].type}",
                    f"give two nodes in neighbouring layers ({LAYERS})",
                ),
            ),
        )
    named = _names(told_by)
    if named:
        candidates: list[Page] = []
        for n in named:
            found = vault.by_name.get(n, ())
            if len(found) != 1 or found[0].type != NARRATIVE or found[0].frontmatter_error:
                why = (
                    "no page has this name"
                    if not found
                    else "more than one page has this name"
                    if len(found) > 1
                    else f"{found[0].path} is not a narrative with readable frontmatter"
                )
                refusals.append(
                    Refusal(
                        f"narrative `{n}`",
                        why,
                        "name a narrative that tells the edge with `--told-by`",
                    )
                )
            else:
                candidates.append(found[0])
    else:
        candidates = [p for p in vault.of_type(NARRATIVE) if not p.frontmatter_error]
    changes: list[tuple[Path, bytes, bytes]] = []
    removed: list[RowRef] = []
    unchanged: list[str] = []
    notes: list[str] = []
    changed: list[str] = []
    for page in candidates:
        raw = _read(vault, page)
        if isinstance(raw, Refusal):
            refusals.append(raw)
            continue
        text, bom = _body_text(raw)
        rows, _ = _rows_for(text, et.slug, from_, to)
        if not rows:
            if named:
                unchanged.append(page.path)
                notes.append(f"{page.path} has no row for this edge, so nothing was written")
            continue
        if page.status == "done":
            refusals.append(_done_refusal(page, "removing this row"))
            continue
        made = remove_rows(text, page.path, [r.n for r in rows])
        if not made.ok:
            refusals.append(
                Refusal(page.path, made.refusal, "correct the table by hand, then run this again")
            )
            continue
        after = ("﻿" if bom else "") + made.text
        changes.append((vault.root / page.path, raw.encode("utf-8"), after.encode("utf-8")))
        changed.append(page.path)
        for r in rows:
            removed.append(RowRef(page.name, page.path, r.line, r.note))
            notes.append(f"removed the row at line {r.line} of {page.path}")
    if refusals:
        return Result(op, refused=tuple(refusals))
    if bad := _write(changes, []):
        return Result(op, refused=(bad,))
    if not changed and not named:
        notes.append("no narrative tells this edge, so nothing was removed")
    if changed:
        notes.append(
            "the links stay in the narratives; remove one by hand if the account no longer names it"
        )
    return EdgeResult(
        op,
        changed=tuple(changed),
        unchanged=tuple(unchanged),
        notes=tuple(notes),
        edge=_after(root, et.slug, from_, to),
        rows_removed=tuple(removed),
    )
