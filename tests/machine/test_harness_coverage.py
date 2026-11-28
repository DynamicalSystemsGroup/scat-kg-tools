"""WP11-R1: the harness validated a result for every rule in the catalogue (only when the whole check suite ran)."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scat_harness as h

CATALOGUE = h.ROOT / "contracts" / "rule-catalogue.md"
CHECKS = h.ROOT / "tests" / "checks"


def skip_reason(collected: set[str], ran: set[str], files: set[str]) -> str | None:
    """Why the check suite did not run whole in this session, or None when it did.

    `collected` are the session's node ids, `ran` the check tests that reached the fixture, `files` the
    `tests/checks/test_*.py` paths (as in node ids).
    """
    checks = {n for n in collected if n.startswith("tests/checks/")}
    absent = sorted(f for f in files if not any(n.startswith(f + "::") for n in checks))
    if absent:
        return f"only part of the check suite is collected in this session (no tests from {', '.join(absent)})"
    missing = checks - ran
    if missing:
        return f"only part of the check suite ran in this session ({len(missing)} of {len(checks)} did not)"
    return None


def test_skip_logic():
    files = {"tests/checks/test_a.py", "tests/checks/test_b.py"}
    a, b = "tests/checks/test_a.py::t1", "tests/checks/test_b.py::t2"
    assert skip_reason({a, b, "tests/x.py::t"}, {a, b}, files) is None
    assert "test_b.py" in skip_reason({a}, {a}, files)  # a subset of files
    assert "1 of 2" in skip_reason({a, b}, {a}, files)  # collected but not run
    assert skip_reason(set(), set(), files) is not None  # nothing collected


def catalogue_rows() -> dict[str, str]:
    text = CATALOGUE.read_text(encoding="utf-8")
    rows = re.findall(r"^\| (SCAT-[A-Z-]+) \| (error|warning) \|", text, re.MULTILINE)
    return dict(rows)


def test__every_catalogue_rule_was_validated(request, capsys):
    files = {f"tests/checks/{p.name}" for p in CHECKS.glob("test_*.py")}
    reason = skip_reason({i.nodeid for i in request.session.items}, h.tests_seen, files)
    if reason:
        pytest.skip(reason + "; run `pytest tests` to cover every rule")
    rows = catalogue_rows()
    assert len(rows) == 42
    with capsys.disabled():
        print(
            f"\nharness: {len(h.rules_validated & set(rows))} of {len(rows)} rule ids validated; "
            f"{h.problems_validated} problems validated; fix commands: "
            f"{h.commands_run} run, {h.commands_parsed} parsed; closing guards: "
            f"{len(h.rules_guarded)} rules, {h.problems_guarded} problems, "
            f"{h.options_with_edits} options with edits, {len(h.DEVIATIONS)} named kind deviations"
        )
    assert sorted(set(rows) - h.rules_validated) == []
    # WP11-R2 closing guards: every rule's problems went through h.check_closing, and the deviation table is
    # exactly the observed (rule, kind) pairs that differ from the catalogue.
    kinds = h.catalogue_kinds()
    assert len(kinds) == 42
    assert sorted(set(rows) - h.rules_guarded) == []
    observed = {pair for pair in h.pairs_seen if kinds[pair[0]] != pair[1]}
    assert sorted(observed - set(h.DEVIATIONS)) == []
    assert sorted(set(h.DEVIATIONS) - observed) == []
    assert {r: s for r, s in h.severities_seen.items() if rows.get(r) != s} == {}
