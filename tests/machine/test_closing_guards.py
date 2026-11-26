"""WP11-R2 closing guards (G1..G5, scat_harness.check_closing): each one fails loudly, naming rule id and file,
on a deliberately broken Problem, and a good Problem passes."""

import dataclasses
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scat_harness as h

from scat_kg.checks.problem import Problem
from scat_kg.fix import Command, Edit, Fix, FixOption

CMD = Command(
    ("set-status", "safe-handling", "draft"), 'scat_kg.set_status("safe-handling", "draft")'
)
TEXT = f"run `scat set-status safe-handling draft` (REPL: `{CMD.repl}`)"
EDIT = Edit("set-field", "concern/safe-handling.md", field="status", value="draft")


def good() -> Problem:
    option = FixOption("exact", TEXT, CMD, (EDIT,))
    return Problem(
        rule="SCAT-FM-STATUS",
        severity="error",
        file="concern/safe-handling.md",
        where="field `status`",
        what="`status` is not stub, draft or done",
        fix="",
        fix_data=Fix.one("exact", option),
        field="status",
    )


def swap(p: Problem, **changes) -> Problem:
    return dataclasses.replace(p, **changes)


def option_of(p: Problem, **changes) -> Problem:
    return swap(p, fix_data=Fix.one("exact", dataclasses.replace(p.fix_data.options[0], **changes)))


def test_a_good_problem_passes():
    h.check_closing(good())


def test_g1_a_legacy_wrapper_fails():
    p = swap(good(), fix_data=Fix.legacy("run something"))
    with pytest.raises(AssertionError, match=r"G1.*SCAT-FM-STATUS.*concern/safe-handling.md"):
        h.check_closing(p)


def test_g2_text_that_is_not_the_render_fails():
    p = good()
    object.__setattr__(p, "fix", "Fix: something else")
    with pytest.raises(AssertionError, match=r"G2.*SCAT-FM-STATUS.*concern/safe-handling.md"):
        h.check_closing(p)


def test_g2_rendered_lines_that_are_not_the_fix_fail(monkeypatch):
    monkeypatch.setattr(Problem, "render", lambda self: "error [X] f where: what\n  Fix: other")
    with pytest.raises(AssertionError, match=r"G2.*SCAT-FM-STATUS"):
        h.check_closing(good())


def test_g3_a_wrong_kind_fails_and_a_named_deviation_passes():
    p = swap(good(), rule="SCAT-FM-PARSE")  # the catalogue says manual; the data says exact
    with pytest.raises(AssertionError, match=r"G3.*SCAT-FM-PARSE.*concern/safe-handling.md"):
        h.check_closing(p)
    h.check_closing(p, deviations={("SCAT-FM-PARSE", "exact"): "a reason"})


def test_g3_every_deviation_has_a_reason_and_differs_from_the_catalogue():
    kinds = h.catalogue_kinds()
    assert len(kinds) == 36
    for (rule, kind), reason in h.DEVIATIONS.items():
        assert reason.strip(), (rule, kind)
        assert kinds[rule] != kind, f"{rule} {kind} is the catalogue's own kind, not a deviation"


@pytest.mark.parametrize(
    "changes",
    [
        {"field": None},  # a field problem with no field
        {"field": "title"},  # the wrong field
        {"where": "link [[x]]"},  # a field set on a problem that is not about one
    ],
)
def test_g4_field_that_does_not_follow_where_fails(changes):
    with pytest.raises(AssertionError, match=r"G4.*SCAT-FM-STATUS.*concern/safe-handling.md"):
        h.check_closing(swap(good(), **changes))


def test_g5_a_command_missing_from_the_text_fails():
    for text in ("run `scat set-status safe-handling draft`", f"(REPL: `{CMD.repl}`)"):
        with pytest.raises(AssertionError, match=r"G5.*SCAT-FM-STATUS.*concern/safe-handling.md"):
            h.check_closing(option_of(good(), text=text))


def test_g5_an_argv_word_missing_from_the_text_fails():
    cmd = Command(("set-status", "safe-handling", "done"), CMD.repl)
    with pytest.raises(AssertionError, match=r"G5.*`done`"):
        h.check_closing(option_of(good(), command=cmd))


def test_g5_an_edit_value_missing_from_the_text_fails_but_an_author_slot_is_excused():
    bad = Edit("set-field", "concern/safe-handling.md", field="status", value="finished")
    with pytest.raises(AssertionError, match=r"G5.*`finished`.*SCAT-FM-STATUS"):
        h.check_closing(option_of(good(), edits=(bad,)))
    slot = Edit(
        "set-field",
        "concern/safe-handling.md",
        field="status",
        value="<status>",
        author_slot="<status>",
    )
    h.check_closing(option_of(good(), edits=(slot,)))
    half = dataclasses.replace(slot, value="draft<status>")
    h.check_closing(option_of(good(), edits=(half,)))
