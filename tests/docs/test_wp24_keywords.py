"""WP24-R10 (D-139): the upper-case keywords SHALL NOT, SHALL, SHOULD and MAY stand only in the assistant's contract,
the skill (its body is the contract's) and the catalogue's mode rule. This test reads every place a user reads: the
docs pages, every command's `--help`, the text of the MCP prompts and the descriptions of the MCP tools.

EXCEPTIONS lists a place that legitimately holds one, with the reason. It is empty: no user page holds one today.
A page WP26's sweep must still clear would be listed here with a comment, and the list kept as short as possible.
"""

import argparse
import asyncio
import re
from pathlib import Path

import pytest

from scat_tools.cli import _parser
from scat_tools.mcp_server import prompts
from scat_tools.mcp_server.server import build

ROOT = Path(__file__).resolve().parents[2]
KEYWORDS = re.compile(r"\b(SHALL NOT|SHALL|SHOULD|MAY)\b")
EXCEPTIONS: dict[str, str] = {}  # source label -> reason


def _helps(parser: argparse.ArgumentParser, name: str = "scat"):
    yield name, parser.format_help()
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            for sub_name, sub in action.choices.items():
                yield from _helps(sub, f"{name} {sub_name}")


def _sources() -> dict[str, str]:
    out = {
        str(p.relative_to(ROOT)): p.read_text(encoding="utf-8")
        for pattern in ("docs/*.md", "docs/reference/*.md")
        for p in sorted(ROOT.glob(pattern))
    }
    out.update({f"help: {n}": t for n, t in _helps(_parser())})
    out.update(
        {f"prompts.{n}": v for n, v in vars(prompts).items() if n.isupper() and isinstance(v, str)}
    )
    mcp = build(ROOT / "contracts" / "examples")
    out.update({f"tool {t.name}": t.description or "" for t in asyncio.run(mcp.list_tools())})
    out.update({f"prompt {p.name}": p.description or "" for p in asyncio.run(mcp.list_prompts())})
    return out


SOURCES = _sources()


def test_the_scan_covers_the_places_it_names():
    labels = set(SOURCES)
    assert "docs/norms.md" in labels and "docs/reference/mcp.md" in labels
    assert "help: scat stub" in labels and "prompts.RULES" in labels
    assert "prompts.DRAFT_A_NODE_PAGE" in labels and "tool evidence" in labels
    assert len(labels) > 40


@pytest.mark.parametrize("label", sorted(SOURCES))
def test_no_upper_case_keyword(label):
    if label in EXCEPTIONS:
        pytest.skip(EXCEPTIONS[label])
    hits = KEYWORDS.findall(SOURCES[label])
    assert not hits, f"{label} holds {sorted(set(hits))}: write plain words (can, must, is refused)"


def test_the_exceptions_are_real_places():
    assert set(EXCEPTIONS) <= set(SOURCES)


# WP25-R6 (D-146): no test or work status in a user page.
STATUS = re.compile(
    r"not been tried|untested|lab run|not recorded|nobody has yet|your first run is the real test",
    re.IGNORECASE,
)


def _status_hits(label: str) -> list[str]:
    return [ln.strip() for ln in SOURCES[label].splitlines() if STATUS.search(ln)]


@pytest.mark.parametrize("label", sorted(k for k in SOURCES if k.startswith("docs/")))
def test_no_status_wording_in_a_user_page(label):
    assert not _status_hits(label), f"{label}: state what a coder does, not what was tried"


def test_status_pattern_catches_each_phrase():
    for phrase in (
        "has not been tried",
        "is untested",
        "a lab run",
        "not recorded",
        "nobody has yet",
        "Your first run is the real test",
    ):
        assert STATUS.search(phrase), phrase
