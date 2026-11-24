"""R2 treats an option that carries edits as parse-only for its command (WP11-R2); command-only options keep the full check."""

import dataclasses
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "checks"))
import scat_harness as h
from helpers import doc, vault

from scat_kg.checks import check_vault
from scat_kg.fix import Command, Edit, Fix, FixOption

C = "concern/safe-handling.md"
EDIT = Edit("set-field", C, field="status", value="draft")


@pytest.fixture
def problem(make_vault):
    v = vault(make_vault, {C: doc("concern", "Safe handling", description=None)})
    found = [p for p in check_vault(v).problems if p.rule == "SCAT-DONE-FIELD"]
    assert len(found) == 1
    return found[0], v.root


def option(problem, argv, edits=()):
    cmd = Command(tuple(argv), "scat_kg.set_status(...)")
    opt = FixOption("exact", "x", cmd, tuple(edits))
    return dataclasses.replace(problem, fix_data=Fix.one("exact", opt))


@pytest.fixture
def fresh_copy(tmp_path_factory):
    def copy_of(root):
        dest = tmp_path_factory.mktemp("copy")
        shutil.copytree(root, dest, dirs_exist_ok=True)
        return dest

    return copy_of


def test_edits_plus_command_is_parsed_not_run(problem, fresh_copy):
    p, root = problem
    # `set-status ... done` alone would not clear the problem: no failure, because it is not run.
    p = option(p, ["set-status", "safe-handling", "done"], [EDIT])
    before = (root / C).read_text(encoding="utf-8")
    copy = fresh_copy(root)
    assert h.assert_option_works(p, 0, copy) == "parsed"
    assert (copy / C).read_text(encoding="utf-8") == before


def test_edits_plus_command_must_still_parse(problem, fresh_copy):
    p, root = problem
    p = option(p, ["set-status", "--no-such-flag"], [EDIT])
    with pytest.raises(AssertionError, match="not accepted"):
        h.assert_option_works(p, 0, fresh_copy(root))


def test_a_command_only_wrong_option_still_fails(problem, fresh_copy):
    p, root = problem
    p = option(p, ["set-status", "safe-handling", "done"])
    with pytest.raises(AssertionError, match="does not clear the problem"):
        h.assert_option_works(p, 0, fresh_copy(root))


def test_a_command_only_right_option_passes(problem, fresh_copy):
    p, root = problem
    p = option(p, ["set-status", "safe-handling", "draft"])
    assert h.assert_option_works(p, 0, fresh_copy(root)) == "ran"
