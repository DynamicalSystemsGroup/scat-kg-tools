"""Small vaults for the view tests: pages written under a folder, and a hash of the whole tree."""

import hashlib
import os
from pathlib import Path


def page(type_: str, title: str, status: str = "draft", extra: str = "", body: str = "") -> str:
    return f'---\ntype: {type_}\nstatus: {status}\ntitle: "{title}"\n{extra}---\n{body}'


def narrative(
    title: str,
    account: str,
    rows: list[str] | None = None,
    status: str = "draft",
    kind: str | None = None,
) -> str:
    """A narrative page: an account, and a table of edges when `rows` (whole row lines) is given."""
    table = ""
    if rows is not None:
        table = "\n## Edges told\n\n| type | from | to | note |\n|---|---|---|---|\n" + "".join(
            r + "\n" for r in rows
        )
    extra = f"kind: {kind}\n" if kind else ""
    return page("narrative", title, status, extra, account + "\n" + table)


def row(edge_type: str, a: str, b: str) -> str:
    return f"| {edge_type} | [[{a}]] | [[{b}]] | |"


def write(root: Path, files: dict[str, str]) -> Path:
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(text.encode("utf-8"))
    return root


def base_files() -> dict[str, str]:
    """The small vault every view is computed over by hand.

    Edges (type, from, to, told by):
      holds        farmers -> cost     diamond
      holds        farmers -> water    dry, wet
      holds        towns   -> cost     split
      addressed-by cost    -> sensor   diamond
      addressed-by water   -> alert    wet
      addressed-by water   -> sensor   dry
      provided-by  alert   -> radio    split
      provided-by  sensor  -> probe    dry
    `idle` is a technology no narrative links; `water` carries a relationship annotation to `cost`.
    """
    return {
        "scat.toml": "stakeholder_group_cap = 3\n",
        "group/farmers.md": page("group", "Farmers", "draft"),
        "group/towns.md": page("group", "Towns", "stub"),
        "concern/water.md": page("concern", "Water", "draft", body="Pulls against [[cost]].\n"),
        "concern/cost.md": page("concern", "Cost", "stub"),
        "affordance/sensor.md": page("affordance", "Sensor", "draft"),
        "affordance/alert.md": page("affordance", "Alert", "stub"),
        "technology/probe.md": page("technology", "Probe", "draft"),
        "technology/radio.md": page("technology", "Radio", "stub"),
        "technology/idle.md": page("technology", "Idle", "stub"),
        "narrative/dry.md": narrative(
            "Dry",
            "The [[farmers]] and the [[towns]] worry about [[water]].",
            [
                row("holds", "farmers", "water"),
                row("addressed-by", "water", "sensor"),
                row("provided-by", "sensor", "probe"),
            ],
            "draft",
            "scenario",
        ),
        "narrative/wet.md": narrative(
            "Wet",
            "Rain came.",
            [row("holds", "farmers", "water"), row("addressed-by", "water", "alert")],
            "stub",
            "architecture",
        ),
        "narrative/empty.md": narrative("Empty", "Only the [[farmers]] spoke."),
        "narrative/split.md": narrative(
            "Split",
            "Two separate matters.",
            [row("holds", "towns", "cost"), row("provided-by", "alert", "radio")],
            "draft",
            "scenario",
        ),
        "narrative/diamond.md": narrative(
            "Diamond",
            "Two routes to one tool.",
            [row("holds", "farmers", "cost"), row("addressed-by", "cost", "sensor")],
            "draft",
            "scenario",
        ),
    }


def tree_hash(root: Path) -> str:
    """One hash over every file and folder under root: path, kind, mtime, size and bytes."""
    h = hashlib.sha256()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for n in dirnames:
            p = Path(dirpath, n)
            h.update(f"dir {p.relative_to(root)}\n".encode())
        for n in sorted(filenames):
            p = Path(dirpath, n)
            st = p.stat()
            h.update(f"file {p.relative_to(root)} {st.st_mtime_ns} {st.st_size}\n".encode())
            h.update(p.read_bytes())
    return h.hexdigest()
