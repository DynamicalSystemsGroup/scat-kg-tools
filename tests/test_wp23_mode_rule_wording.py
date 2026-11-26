"""WP23-G4/R4 (D-133, D-134, D-139): the mode rule is the same words in three places, the keywords stand only in the
assistant's contract, the skill and the catalogue's mode rule, and each assistant rule carries its decided word."""

import re
from pathlib import Path

import pytest

from scat_kg.checks.attribution import MODE_RULE
from scat_kg.mcp_server import prompts

ROOT = Path(__file__).resolve().parents[1]
ASSISTANT = (ROOT / "contracts" / "assistant.md").read_text(encoding="utf-8")
CATALOGUE = (ROOT / "contracts" / "rule-catalogue.md").read_text(encoding="utf-8")
SKILL = (ROOT / "skills" / "scat-coding" / "SKILL.md").read_text(encoding="utf-8")
NORMS = " ".join((ROOT / "docs" / "norms.md").read_text(encoding="utf-8").split())
KEYWORDS = r"\b(SHALL NOT|SHALL|SHOULD|MAY)\b"


def _item(n: int) -> str:
    m = re.search(rf"^- \*\*A{n}\.\*\* (.*?)(?=^- \*\*A|\n\n|\Z)", ASSISTANT, re.DOTALL | re.MULTILINE)
    assert m, n
    return " ".join(m.group(1).split())


def test_the_mode_rule_is_the_same_words_in_catalogue_assistant_and_skill():
    assert MODE_RULE in CATALOGUE
    assert MODE_RULE in ASSISTANT
    assert MODE_RULE in SKILL  # the skill's rules text is the contract's body, held by the drift test
    assert "every result carries `mode`" in ASSISTANT


def test_the_norms_page_states_the_three_cases_in_plain_words():
    assert not re.search(r"SHALL|MAY|SHOULD", NORMS)
    for mode in ("required", "disallowed", "optional"):
        assert f"In {mode} mode" in NORMS
    assert MODE_RULE not in NORMS
    assert "no narrative names a contributor" in NORMS


def test_the_prompts_point_at_the_vaults_mode_without_keywords():
    assert "the `mode` field in every result" in prompts.RULES
    assert not re.search(KEYWORDS, prompts.RULES)


def test_the_keywords_are_defined_once():
    assert len(re.findall(r"RFC 2119", ASSISTANT)) == 1
    for line in ("SHALL: required.", "SHALL NOT: forbidden.", "SHOULD:", "MAY: allowed"):
        assert ASSISTANT.count(line) == 1, line


@pytest.mark.parametrize(
    ("ns", "word"),
    [
        ([1, 2, 3, 4, 6], "MAY"),
        ([5], "SHOULD"),
        ([7, 8, 9, 10, 11, 12], "SHALL NOT"),
        ([13, 14, 15], "SHALL"),
    ],
)
def test_each_rule_carries_its_decided_word(ns, word):
    for n in ns:
        found = re.findall(KEYWORDS, _item(n))
        assert found and found[0] == word, (n, found)


def test_a10_states_the_doubt_and_hands_it_back():
    assert "SHALL state the doubt" in _item(10)
