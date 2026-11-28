"""WP21-R3: docs/norms.md has its sections, is linked from the coding and chat-path guides and the nav, and names
only rule ids that the rule catalogue holds. WP24-R2 changed it from six sections to seven: "What a node page holds"."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
PAGE = DOCS / "norms.md"
CATALOGUE = ROOT / "contracts" / "rule-catalogue.md"
HEADINGS = [
    "A narrative that links a node page",
    "Links in the account",
    "Descriptions",
    "What a node page holds",
    "Writing together",
    "Status when you leave a page",
    "What `done` needs",
]


def test_page_has_exactly_the_seven_headings_in_order():
    assert PAGE.is_file()
    text = PAGE.read_text(encoding="utf-8")
    assert re.findall(r"(?m)^## (.+?)\s*$", text) == HEADINGS


def test_coding_and_chat_path_link_to_it():
    for name in ("coding.md", "chat-path.md"):
        assert "](norms.md" in (DOCS / name).read_text(encoding="utf-8"), name


def test_nav_lists_it():
    assert re.search(
        r"(?m)^\s+- [^:]+: norms\.md\s*$", (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    )


def test_every_rule_id_is_in_the_catalogue():
    ids = set(re.findall(r"SCAT-[A-Z-]+[A-Z]", PAGE.read_text(encoding="utf-8")))
    assert ids
    catalogue = CATALOGUE.read_text(encoding="utf-8")
    missing = sorted(
        i
        for i in ids
        if not re.search(rf"(?m)^\| {re.escape(i)}[ ,|]|^### {re.escape(i)}$", catalogue)
    )
    assert not missing, f"not in contracts/rule-catalogue.md: {missing}"
