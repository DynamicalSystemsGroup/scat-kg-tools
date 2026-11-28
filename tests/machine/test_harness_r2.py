"""The harness's R1 and R2 checks work: they pass a right fix and fail a wrong one (WP11-R1, WP11-R2)."""

import dataclasses
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "checks"))
import scat_harness as h
from helpers import doc, vault

from scat_tools.checks import check_vault
from scat_tools.fix import Command, Fix, FixOption

C = "concern/safe-handling.md"


@pytest.fixture
def problem(make_vault):
    """A done concern with no description: SCAT-DONE-FIELD, which `set-status ... draft` clears."""
    v = vault(make_vault, {C: doc("concern", "Safe handling", description=None)})
    found = [p for p in check_vault(v).problems if p.rule == "SCAT-DONE-FIELD"]
    assert len(found) == 1
    return found[0], v.root


def with_command(problem, kind, argv, slot=None):
    cmd = Command(tuple(argv), "scat_tools.set_status(...)", slot)
    return dataclasses.replace(problem, fix_data=Fix.one(kind, FixOption(kind, "x", cmd)))


@pytest.fixture
def fresh_copy(tmp_path_factory):
    def copy_of(root, _unused=None):
        dest = tmp_path_factory.mktemp("copy")
        shutil.copytree(root, dest, dirs_exist_ok=True)
        return dest

    return copy_of


def test_a_right_exact_command_passes(problem, fresh_copy):
    p, root = problem
    p = with_command(p, "exact", ["set-status", "safe-handling", "draft"])
    assert h.assert_option_works(p, 0, fresh_copy(root)) == "ran"


def test_a_wrong_exact_command_fails_naming_rule_option_and_command(problem, fresh_copy):
    p, root = problem
    p = with_command(p, "exact", ["set-status", "safe-handling", "done"])
    with pytest.raises(
        AssertionError, match=r"SCAT-DONE-FIELD option 1 `scat set-status safe-handling done`"
    ):
        h.assert_option_works(p, 0, fresh_copy(root))


def test_a_command_that_exits_nonzero_fails(problem, fresh_copy):
    p, root = problem
    p = with_command(p, "exact", ["set-status", "no-such-page", "draft"])
    with pytest.raises(AssertionError, match="exited 1"):
        h.assert_option_works(p, 0, fresh_copy(root))


def test_the_run_changed_only_the_copy(problem, fresh_copy):
    p, root = problem
    before = (root / C).read_text(encoding="utf-8")
    h.assert_option_works(
        with_command(p, "exact", ["set-status", "safe-handling", "draft"]),
        0,
        fresh_copy(root),
    )
    assert (root / C).read_text(encoding="utf-8") == before


def test_a_slot_command_is_parsed_not_run(problem, fresh_copy):
    p, root = problem
    ok = with_command(p, "slot", ["stub", "<name>", "--type", "concern"], slot="<name>")
    assert h.assert_option_works(ok, 0, fresh_copy(root)) == "parsed"
    bad = with_command(p, "slot", ["stub", "<name>", "--kind", "concern"], slot="<name>")
    with pytest.raises(AssertionError, match="not accepted"):
        h.assert_option_works(bad, 0, fresh_copy(root))


def test_r1_passes_a_real_report_and_fails_a_malformed_document(problem, monkeypatch):
    p, root = problem
    report = check_vault(vault_of(root))
    h.validate_report(report)
    broken = dataclasses.replace(p, severity="fatal")
    with pytest.raises(AssertionError, match="schema: SCAT-DONE-FIELD"):
        h.validate_report(dataclasses.replace(report, problems=(broken,)))
    # a document-level error: the problem list itself is fine, the document's `ok` is not a boolean
    monkeypatch.setattr(h.scat_tools.CheckResult, "ok", property(lambda self: "yes"))
    with pytest.raises(AssertionError, match="schema: check document"):
        h.validate_report(report)


def vault_of(root):
    from scat_tools.vault import read_vault

    return read_vault(root)


def test_observe_samples_at_most_three_per_key_and_leaves_the_vault_alone(problem, monkeypatch):
    p, root = problem
    p = with_command(p, "exact", ["set-status", "safe-handling", "draft"])
    monkeypatch.setattr(h, "_samples", h.Counter())
    monkeypatch.setattr(h, "commands_run", 0)
    before = (root / C).read_text(encoding="utf-8")
    h.observe(root, h.Report((p,) * 5))
    assert h.commands_run == 3
    assert (root / C).read_text(encoding="utf-8") == before
