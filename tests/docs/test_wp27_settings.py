"""WP27-U2: the docs say who changes the cap, and none gives 3 as the template's cap."""

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parents[2] / "docs"
PHRASE = "set up your tools"


def section(text: str, heading: str) -> str:
    match = re.search(rf"(?ms)^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text)
    assert match, heading
    return match.group(1)


def test_planning_and_chat_path_say_who_changes_a_setting():
    for name in ("planning.md", "chat-path.md"):
        text = (DOCS / name).read_text(encoding="utf-8")
        sentences = re.split(r"(?<=[.;])\s+", text)
        assert any(
            PHRASE in s and re.search(r"chang(e|es|ed)\b|raise", s) and re.search(r"cap|setting", s)
            for s in sentences
        ), name


def test_the_problems_table_covers_the_cap():
    text = (DOCS / "chat-path.md").read_text(encoding="utf-8")
    rows = [r for r in section(text, "When something goes wrong").splitlines() if r.startswith("|")]
    assert any("cap" in r and "stakeholder_group_cap" in r and PHRASE in r for r in rows)


def test_no_page_gives_3_as_the_templates_cap():
    for name in ("planning.md", "getting-started.md"):
        text = (DOCS / name).read_text(encoding="utf-8")
        assert not re.search(r"stakeholder_group_cap\s*=\s*3\b", text), name
        for s in re.split(r"(?<=[.;])\s+", text):
            if re.search(
                r"template|example vault|by default|default", s, re.IGNORECASE
            ) and re.search(r"\bcap\b", s, re.IGNORECASE):
                assert not re.search(r"\b(3|three)\b", s, re.IGNORECASE), (name, s)
