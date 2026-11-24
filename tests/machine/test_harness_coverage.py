"""WP11-R1: the harness validated a result for every rule in the catalogue (only when the whole check suite ran)."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scat_harness as h

CATALOGUE = h.ROOT / "contracts" / "rule-catalogue.md"


def test__every_catalogue_rule_was_validated(request, capsys):
    checks = {i.nodeid for i in request.session.items if i.nodeid.startswith("tests/checks/")}
    missing = checks - h.tests_seen
    if not checks or missing:
        pytest.skip(
            f"only part of the check suite ran in this session ({len(missing)} of {len(checks)} "
            "check tests did not); run `pytest tests` to cover every rule"
        )
    text = CATALOGUE.read_text(encoding="utf-8")
    ids = re.findall(r"^\| (SCAT-[A-Z-]+) \| (?:error|warning) \|", text, re.MULTILINE)
    assert len(ids) == 28
    with capsys.disabled():
        print(
            f"\nharness: {len(h.rules_validated & set(ids))} of {len(ids)} rule ids validated; "
            f"{h.problems_validated} problems validated; fix commands: "
            f"{h.commands_run} run, {h.commands_parsed} parsed"
        )
    assert sorted(set(ids) - h.rules_validated) == []
