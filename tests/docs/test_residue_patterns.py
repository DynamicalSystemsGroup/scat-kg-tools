"""WP26-R6: the residue sweep's pattern list (`acceptance/residue-sweep.md`) finds no unmarked hit in a user page.

Places read: every docs page, the launcher's messages, the skill, the assistant's contract (its deontic keywords are
its rules) and every command's `--help`. KEPT lists a hit that stays, as (label, line text) with the reason.
"""

import re
from pathlib import Path

import pytest
from test_wp24_keywords import SOURCES

ROOT = Path(__file__).resolve().parents[2]
PATTERNS = {
    "P2": re.compile(r"recommend|one option|policy option|you may prefer", re.IGNORECASE),
    "P3": re.compile(r"as instructed|as asked|as requested|you were told", re.IGNORECASE),
    "P4": re.compile(
        r"\bD-\d{3}\b|decision log|as decided|\bACE\b|chief engineer|\bWP\d+", re.IGNORECASE
    ),
    "P5": re.compile(
        r"not been tried|untested|lab run|not recorded|nobody has yet|first run is the real test"
        r"|stand-in|not yet (run|tried|tested)",
        re.IGNORECASE,
    ),
    "P6": re.compile(
        r"we decided|we chose|in this release|reviewer|the sitting|UA-[AM]|cold read|\bspike\b",
        re.IGNORECASE,
    ),
}
# (label, pattern id): reason. A kept hit is a whole label and pattern, so keep the list short.
KEPT: dict[tuple[str, str], str] = {}


def _places() -> dict[str, str]:
    out = {k: v for k, v in SOURCES.items() if k.startswith(("docs/", "help: "))}
    for rel in ("deploy/scatlab.sh", "deploy/README.md", "skills/scat-coding/SKILL.md"):
        out[rel] = (ROOT / rel).read_text(encoding="utf-8")
    return out


PLACES = _places()


@pytest.mark.parametrize("label", sorted(PLACES))
def test_no_residue_pattern(label):
    for pid, rx in PATTERNS.items():
        if (label, pid) in KEPT:
            continue
        hits = [ln.strip() for ln in PLACES[label].splitlines() if rx.search(ln)]
        assert not hits, f"{label} {pid}: {hits[:3]}"


def test_kept_hits_are_real():
    for label, pid in KEPT:
        assert label in PLACES
        assert any(PATTERNS[pid].search(ln) for ln in PLACES[label].splitlines()), (label, pid)


def test_the_pattern_list_is_the_records():
    record = (ROOT / "acceptance" / "residue-sweep.md").read_text(encoding="utf-8")
    for pid in PATTERNS:
        assert f"| {pid} |" in record
