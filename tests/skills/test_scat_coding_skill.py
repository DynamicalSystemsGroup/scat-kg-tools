"""WP21-G4: the `scat-coding` skill carries the assistant's rules verbatim and the G4 items, and cannot drift.

The rules text is the body of `contracts/assistant.md` (after its title). In SKILL.md it is the text under the
title `# SCAT coding: the assistant's skill`, after the blank line under the title, up to the blank line before
the first G4 heading `## Edges told` (the rules hold `## ` headings of their own, so that heading is the end).
The file carries no HTML comments. The edge grammar is read against the TBox through the package, not against literals.
"""

import re
from pathlib import Path

import pytest
import yaml

from scat_tools.tbox import load

ROOT = Path(__file__).parents[2]
SKILL = ROOT / "skills" / "scat-coding" / "SKILL.md"
SOURCE = ROOT / "contracts" / "assistant.md"
TITLE = "# SCAT coding: the assistant's skill\n\n"
END = "\n## Edges told"

# One distinctive heading for each G4 item.
G4_HEADINGS = {
    "edge grammar": "## Edges told",
    "kind": "## Kind",
    "one step per reply": "## One step per reply",
    "offering a description": "## Offering a description",
    "drafting a node page": "## Drafting a node page",
    "sweeping the stub node pages": "## Sweeping the stub node pages",
    "possible duplicates and merging": "## Possible duplicates and merging",
    "pages to tag at the end": "## At the end of a session",
    "norms pointer": "## Norms",
}


def source_rules() -> str:
    """The assistant's rules: the source file after its title line and the blank line under it."""
    return SOURCE.read_text().split("\n", 2)[2]


def skill_rules(text: str) -> str:
    assert TITLE in text and END in text, "the rules anchors are missing from SKILL.md"
    return text.split(TITLE, 1)[1].split(END, 1)[0]


def rules_drift(text: str) -> bool:
    return skill_rules(text) != source_rules()


def test_rules_text_equals_the_contract():
    assert not rules_drift(SKILL.read_text()), (
        "the rules in skills/scat-coding/SKILL.md differ from contracts/assistant.md: "
        "copy the file's body (after its title) under the skill's title again"
    )


def test_a_mutated_rules_text_is_caught():
    text = SKILL.read_text()
    assert rules_drift(text.replace("That is the coder's act.", "That is the assistant's act.", 1))
    assert rules_drift(text.replace("**A11.**", "**A11x.**", 1))


def test_frontmatter_parses_with_name_and_description():
    parts = SKILL.read_text().split("---\n", 2)
    assert parts[0] == "", "the file must open with the frontmatter"
    meta = yaml.safe_load(parts[1])
    assert meta["name"] == "scat-coding" == SKILL.parent.name
    assert isinstance(meta["description"], str) and meta["description"].strip()


@pytest.mark.parametrize("item", G4_HEADINGS)
def test_g4_item_present(item):
    lines = SKILL.read_text().splitlines()
    assert G4_HEADINGS[item] in lines, f"G4 item missing: {item}"


def test_norms_pointer_names_the_file():
    text = SKILL.read_text().split("## Norms", 1)[1]
    assert "docs/norms.md" in text


def test_edge_grammar_agrees_with_the_tbox():
    tbox = load()
    section = SKILL.read_text().split("## Edges told", 1)[1].split("\n## ", 1)[0]
    columns = " | ".join(tbox.table.names)
    assert f"`{columns}`" in section, f"column order is not the TBox's: {columns}"
    rows = re.findall(r"^\| (.+?) \| (\w+) \| (\w+) \|$", section, re.MULTILINE)
    rows = [r for r in rows if r[0] not in ("type", "---")]
    found = {verb: (frm, to) for verb, frm, to in rows}
    expected = {e.verb: (e.from_type, e.to_type) for e in tbox.edge_types.values()}
    assert found == expected
