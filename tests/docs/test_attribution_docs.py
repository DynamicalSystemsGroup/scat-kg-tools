"""WP23-R7: the planning, consent and coding pages cover the attribution modes: planning has the mode choice
section and a script for each mode, consent names the three modes, coding shows `attributed_to`."""

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parents[2] / "docs"
MODES = ("required", "optional", "disallowed")


def read(name: str) -> str:
    return (DOCS / name).read_text(encoding="utf-8")


def headings(markdown: str) -> list[str]:
    return re.findall(r"(?m)^#{2,3} (.+?)\s*$", markdown)


def test_planning_has_the_mode_choice_and_a_script_for_each_mode():
    text = read("planning.md")
    assert "Choose the attribution mode" in headings(text)
    assert 'attribution = "disallowed"' in text
    section = text.split("## State the participation terms", 1)[1]
    for mode in MODES:
        assert f"`{mode}`" in section, mode
    scripts = [
        b
        for b in re.findall(r"```text\n(.*?)```", section, re.DOTALL)
        if "Whatever is said here" in b
    ]
    assert len(scripts) == 3
    assert any("Nobody is named" in b for b in scripts)
    assert any("name of the person who gave it" in b for b in scripts)
    assert any("If you want your name" in b for b in scripts)
    assert "Chatham House" in text and "`scat.toml`" in text


def test_consent_page_names_the_three_modes_and_where_contributor_pages_exist():
    text = read("data-and-consent.md")
    assert "Attribution mode" in headings(text)
    for mode in MODES:
        assert f"| `{mode}` |" in text, mode
    assert "Contributor pages exist only in `required` and `optional`" in text


def test_coding_guide_shows_contributor_pages_and_the_field():
    text = read("coding.md")
    assert "Contributor pages and `attributed_to`" in headings(text)
    assert 'attributed_to: ["[[ada-quill]]"]' in text
    assert "scat stub ada-quill --type contributor" in text
    for rule in ("SCAT-DRAFT-ATTR", "SCAT-DONE-ATTR", "SCAT-ATTR-DISALLOWED"):
        assert rule in text, rule
    assert "scat attribution" in text and "reference/cli.md" in text


def test_the_pages_link_to_each_other_by_headings_that_exist():
    planning, coding = read("planning.md"), read("coding.md")
    assert "planning.md#choose-the-attribution-mode" in read("data-and-consent.md")
    assert "coding.md#contributor-pages-and-attributed_to" in read("data-and-consent.md")
    assert "choose-the-attribution-mode" in read("facilitate-scenarios.md")
    assert "choose-the-attribution-mode" in read("facilitate-architectures.md")
    assert "Choose the attribution mode" in headings(planning)
    assert "Contributor pages and `attributed_to`" in headings(coding)


def test_getting_started_names_the_mode_key_beside_the_cap():
    text = read("getting-started.md")
    assert "`attribution`" in text and "`stakeholder_group_cap`" in text


def test_python_reference_shows_attribution():
    text = read("reference/api.md")
    assert "## scat_kg.attribution" in text
