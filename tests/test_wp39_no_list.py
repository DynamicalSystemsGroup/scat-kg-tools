"""WP39 R1: the "Linked beyond the text" list is retired; no guide or example may suggest it."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCANNED = ["contracts", "docs"]
EXCLUDED = {ROOT / "contracts" / "rule-catalogue.md"}
PHRASES = ("linked beyond the text", "beyond the text")


def test_no_list_beyond_the_text():
    found = []
    for top in SCANNED:
        for path in sorted((ROOT / top).rglob("*")):
            if not path.is_file() or path in EXCLUDED:
                continue
            try:
                text = path.read_text(encoding="utf-8").lower()
            except UnicodeDecodeError:
                continue
            found += [f"{path.relative_to(ROOT)}: {p}" for p in PHRASES if p in text]
    assert not found, found
