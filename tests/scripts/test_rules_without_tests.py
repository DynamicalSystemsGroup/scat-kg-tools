"""WP5-R1: the script that lists catalogue rules without a seeded-defect test lists nothing."""

import subprocess
import sys
from pathlib import Path

import rules_without_tests as script

SCRIPT = Path(script.__file__)


def test__r1__every_catalogue_rule_has_a_seeded_test_by_the_script():
    assert len(script.catalogue_ids()) == 35
    assert script.rules_without_tests() == []


def test__r1__the_script_prints_nothing_and_exits_zero():
    done = subprocess.run(
        [sys.executable, str(SCRIPT)], check=False, capture_output=True, text=True
    )
    assert (done.returncode, done.stdout, done.stderr) == (0, "", "")


def test__r1__a_done_id_is_covered_by_the_tests_of_its_draft_id(monkeypatch):
    have = set(script.catalogue_ids()) - {"SCAT-DONE-TABLE-ROW"}
    monkeypatch.setattr(script, "seeded_ids", lambda: have)
    assert script.rules_without_tests() == []
    monkeypatch.setattr(script, "seeded_ids", lambda: have - {"SCAT-DRAFT-TABLE-ROW"})
    assert script.rules_without_tests() == ["SCAT-DRAFT-TABLE-ROW", "SCAT-DONE-TABLE-ROW"]


def test__r1__the_script_does_list_a_rule_that_has_no_test(monkeypatch, capsys):
    monkeypatch.setattr(
        script, "seeded_ids", lambda: set(script.catalogue_ids()) - {"SCAT-MENTION"}
    )
    assert script.main() == 1
    assert capsys.readouterr().out == "SCAT-MENTION\n"
