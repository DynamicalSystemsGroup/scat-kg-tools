import os
from pathlib import Path

EXAMPLES = Path(__file__).parents[2] / "contracts" / "examples"


def snapshot(root: Path) -> dict[str, tuple]:
    """Every file and folder under root: bytes, size and mtime, so a rewrite with equal bytes shows."""
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for n in dirnames:
            out[str(Path(dirpath, n).relative_to(root))] = ("dir",)
        for n in filenames:
            p = Path(dirpath, n)
            out[str(p.relative_to(root))] = ("file", p.stat().st_mtime_ns, p.read_bytes())
    return out


def changes(before: dict, after: dict) -> dict[str, str]:
    """What differs between two snapshots: path -> created / removed / changed."""
    out = {}
    for k in before.keys() | after.keys():
        if k not in before:
            out[k] = "created"
        elif k not in after:
            out[k] = "removed"
        elif before[k] != after[k]:
            out[k] = "changed"
    return out


def fm(type_: str, title: str, status: str = "draft", extra: str = "", body: str = "") -> str:
    return f'---\ntype: {type_}\nstatus: {status}\ntitle: "{title}"\n{extra}---\n{body}'
