"""The index operation: the Base files of the generated index pages (page contracts 9).

One Obsidian Base per type, `index/<type>.base`, a view of the pages whose `type` matches, leaving out the pages
under the template folder. Written once: a file that exists is never touched (an author may add columns).
"""

from pathlib import Path

from scat_kg.ops.common import open_vault
from scat_kg.ops.files import create_files
from scat_kg.ops.result import Refusal, Result, reports_mode
from scat_kg.tbox import TBOX

TYPES = (*TBOX.layers, TBOX.table_type.slug)
EXTRA = {
    TBOX.table_type.slug: ("kind", "timeframe")
}  # columns after `description`, beyond the common ones
FOLDER = "index"


def _plural(label: str) -> str:
    return label[:-1] + "ies" if label.endswith("y") else label + "s"


def _quoted(expr: str) -> str:
    return "'" + expr.replace("'", "''") + "'"


def base_text(type_: str, templates_folder: str) -> str:
    """The Base file of one type: LF, one final newline."""
    folder = templates_folder.replace("\\", "\\\\").replace('"', '\\"')
    columns = ["file.name", "note.title", "note.status", "note.description"]
    columns += [f"note.{k}" for k in EXTRA.get(type_, ())]
    lines = [
        "filters:",
        "  and:",
        "    - " + _quoted(f'note.type == "{type_}"'),
        "    - " + _quoted(f'!file.inFolder("{folder}")'),
        "views:",
        "  - type: table",
        f'    name: "{_plural(TBOX.page_types[type_].label)}"',
        "    order:",
        *(f"      - {c}" for c in columns),
        "    sort:",
        "      - property: file.name",
        "        direction: ASC",
    ]
    return "\n".join(lines) + "\n"


@reports_mode
def index(*, root: str | Path = ".") -> Result:
    """Write `index/<type>.base` for each type that has none."""
    op = "index"
    vault, bad = open_vault(op, root)
    if bad:
        return bad
    folder = vault.root / FOLDER
    if folder.exists() and not folder.is_dir():
        return Result(
            op,
            refused=(
                Refusal(
                    FOLDER,
                    "a file has the name of the folder the index files go in",
                    f"rename or move `{FOLDER}`, then run `scat index` again",
                ),
            ),
        )
    new, unchanged, refusals = [], [], []
    for t in TYPES:
        rel = f"{FOLDER}/{t}.base"
        path = vault.root / rel
        if path.is_file():
            unchanged.append(rel)
        elif path.exists():
            refusals.append(
                Refusal(
                    rel,
                    "something that is not a file has this name",
                    "rename or move it, then run `scat index` again",
                )
            )
        else:
            new.append((rel, base_text(t, vault.config.templates_folder)))
    if refusals:
        return Result(op, refused=tuple(refusals))
    try:
        create_files([(vault.root / rel, text) for rel, text in new])
    except OSError as e:
        return Result(
            op,
            refused=(Refusal(FOLDER, f"could not write: {e}", "check the folder's permissions"),),
        )
    return Result(op, created=tuple(r for r, _ in new), unchanged=tuple(unchanged))
