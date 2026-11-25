"""WP11-R1 and WP11-R2 harness: validate every check result the suite produces, and try every fix command.

`tests/checks/conftest.py` wraps the one function every check goes through and hands each Report to `observe`.
The two checks are plain functions so a unit test can call them directly:

- `validate_report` (R1): every Problem, and the whole check document, validates against the schema.
- `check_closing` (the closing guards G1..G5, run on every Problem `guard_report` hands it): the fix is typed data,
  its text is generated from the data, its kind is the catalogue's (bar the named `DEVIATIONS`), `field` follows
  `where`, and each command and edit value appears in the text. G6 is `validate_report`.
- `assert_option_works` (R2): an exact option's command, run as given on a copy of the vault, exits 0 and the
  problem is gone on a re-check; a slot option's, an option with edits', or any sequence step's argv is accepted by `scat`'s parser.
"""

import contextlib
import io
import json
import re
import shutil
import tempfile
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator

import scat_kg
from scat_kg import cli
from scat_kg.checks import run as checks_run
from scat_kg.checks.problem import Problem, Report
from scat_kg.vault import read_vault

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / "contracts" / "machine-interface.schema.json").read_text("utf-8"))
SAMPLES_PER_KEY = 3

_DOC = Draft202012Validator(SCHEMA)
_PROBLEM = Draft202012Validator({"$ref": "#/$defs/Problem", "$defs": SCHEMA["$defs"]})

CATALOGUE = ROOT / "contracts" / "rule-catalogue.md"

# Where a Problem's fix kind is not the catalogue table's kind for its rule: (rule, observed kind) -> why.
# A pair outside this table that differs from the catalogue fails G3; a pair here that is not observed fails
# the coverage test, so the table is exactly what the suite produces.
_SINGLE = "a single-option fix takes its option's kind"
_NEAR = "a near match to a value set is one exact edit"
_PAIR = ("DRAFT", "DONE")
DEVIATIONS: dict[tuple[str, str], str] = {
    ("SCAT-FM-REQUIRED", "exact"): _SINGLE,
    ("SCAT-FM-TYPE", "exact"): _NEAR,
    ("SCAT-FM-STATUS", "exact"): _NEAR,
    ("SCAT-FM-TIMEFRAME", "exact"): _NEAR,
    ("SCAT-FM-SHAPE", "exact"): "a one-item list, a boolean or a number has its one exact reading",
    ("SCAT-NAME", "manual"): "no legal name can be derived, so the author chooses one",
    (
        "SCAT-LINK-DANGLING-BODY",
        "exact",
    ): "no page can replace the link: dropping it is the only option",
}
for _p in _PAIR:
    DEVIATIONS[(f"SCAT-{_p}-TABLE-HEADER", "exact")] = (
        "a wrong name or a missing separator has one exact fix"
    )
    DEVIATIONS[(f"SCAT-{_p}-TABLE-ROW", "exact")] = (
        "a missing note or closing bar has one exact fix"
    )
    DEVIATIONS[(f"SCAT-{_p}-TABLE-SECOND", "advisory")] = "a second table has the one advisory fix"
    DEVIATIONS[(f"SCAT-{_p}-END-NOPAGE", "exact")] = (
        "the cap withholds the stub: deleting the row is all that is left"
    )

# What the session saw (read by tests/machine/test_harness_coverage.py).
tests_seen: set[str] = set()  # node ids of the check tests that ran
rules_validated: set[str] = set()
pairs_seen: set[tuple[str, str]] = set()  # (rule id, fix kind) of the problems validated
rules_guarded: set[str] = set()
problems_guarded = 0
options_with_edits = 0  # options (of the problems guarded) that carry edits
severities_seen: dict[str, str] = {}  # rule id -> severity of the problems validated
problems_validated = 0
commands_run = 0
commands_parsed = 0
commands_unbuilt = (
    0  # always 0 now: every operation is built (kept for test_harness_coverage's report line)
)
_samples: Counter = Counter()
_tmp: tempfile.TemporaryDirectory | None = None
_busy = False  # True while the harness itself runs a check or a command


def validate_report(report: Report) -> None:
    """R1. Raise AssertionError, naming the rule id, when a Problem or the check document breaks the schema."""
    global problems_validated
    for p in report.problems:
        errors = sorted(_PROBLEM.iter_errors(p.to_dict()), key=lambda e: list(e.path))
        if errors:
            e = errors[0]
            raise AssertionError(
                f"schema: {p.rule} in {p.file}: {e.message} at /{'/'.join(map(str, e.path))}"
            )
        rules_validated.add(p.rule)
        severities_seen.setdefault(p.rule, p.severity)
        if severities_seen[p.rule] != p.severity:
            severities_seen[p.rule] = f"{p.severity} (and {severities_seen[p.rule]})"
        problems_validated += 1
    errors = sorted(
        _DOC.iter_errors(scat_kg.CheckResult(report).to_dict()), key=lambda e: list(e.path)
    )
    if errors:
        e = errors[0]
        raise AssertionError(
            f"schema: check document: {e.message} at /{'/'.join(map(str, e.path))}"
        )


def guard_report(report: Report) -> None:
    """G1..G5 on every Problem of a Report, and the counts the coverage test reads (what `wrap` calls)."""
    global problems_guarded, options_with_edits
    for p in report.problems:
        check_closing(p)
        pairs_seen.add((p.rule, p.fix_data.kind))
        rules_guarded.add(p.rule)
        problems_guarded += 1
        options_with_edits += sum(1 for o in p.fix_data.options if o.edits)


def catalogue_kinds() -> dict[str, str]:
    """Rule id -> the "Fix kind" column of the catalogue's table."""
    text = CATALOGUE.read_text(encoding="utf-8")
    pat = r"^\| (SCAT-[A-Z-]+) \| (?:error|warning) \|.*\| (\w+) \|$"
    return dict(re.findall(pat, text, re.MULTILINE))


def check_closing(p: Problem, kinds: dict[str, str] | None = None, deviations=None) -> None:
    """G1..G5 for one Problem. Raise AssertionError naming rule id and file on the first that fails.

    `kinds` is the catalogue's rule -> kind (read from the file by default), `deviations` the named table.
    """
    kinds = catalogue_kinds() if kinds is None else kinds
    deviations = DEVIATIONS if deviations is None else deviations
    fix = p.fix_data
    at = f"{p.rule} in {p.file}"
    if fix.verbatim is not None:
        raise AssertionError(f"G1 legacy fix wrapper, not typed data: {at}")
    if fix.render() != p.fix:
        raise AssertionError(f"G2 fix text is not the data's render: {at}")
    if "\n".join(p.render().split("\n")[1:]) != "\n".join(
        "  " + ln for ln in fix.render().split("\n")
    ):
        raise AssertionError(f"G2 rendered fix lines are not the data's render: {at}")
    pair = (p.rule, fix.kind)
    if fix.kind != kinds.get(p.rule) and pair not in deviations:
        raise AssertionError(
            f"G3 fix kind `{fix.kind}` is not the catalogue's `{kinds.get(p.rule)}` and is not a named deviation: {at}"
        )
    want = p.where.split("`")[1] if p.where.startswith("field `") else None
    if p.field != want:
        raise AssertionError(f"G4 field {p.field!r} does not follow where {p.where!r}: {at}")
    for i, opt in enumerate(fix.options, 1):
        if opt.command is not None:
            for word in (opt.command.repl, *opt.command.argv):
                if word not in opt.text:
                    raise AssertionError(
                        f"G5 option {i} text lacks command part `{word}`: {at}\n{opt.text}"
                    )
        for e in opt.edits:
            # A string value is what the fix writes, so its text says it. A list is the field's whole new
            # contents (it also holds items the fix leaves alone, or is what remains after a delete), so it is
            # not checked against the text.
            if isinstance(e.value, str):
                for piece in e.value.split(e.author_slot) if e.author_slot else [e.value]:
                    if piece and piece not in fix.render():
                        raise AssertionError(
                            f"G5 edit value `{piece}` is not in the fix text: {at}\n{fix.render()}"
                        )


def _where(problem: Problem, i: int, argv) -> str:
    return f"{problem.rule} option {i + 1} `scat {' '.join(argv)}`"


def _parses(problem: Problem, i: int, argv, root) -> None:
    try:
        cli._parser().parse_args([*argv, "--root", str(root)])
    except SystemExit as e:
        raise AssertionError(
            f"command not accepted (exit {e.code}): {_where(problem, i, argv)}"
        ) from None


def assert_option_works(problem: Problem, i: int, copy: Path) -> str:
    """R2 for option `i` of the problem's fix, against `copy` (a copy of the vault the problem came from).

    Returns "ran" or "parsed". Raises AssertionError naming rule id, option index and command.
    """
    global _busy, commands_run, commands_parsed
    fix, opt = problem.fix_data, problem.fix_data.options[i]
    cmd = opt.command
    argv = list(cmd.argv)
    # An option with edits is parse-only for its command: the harness does not apply edits, so the command
    # alone need not clear the problem.
    if opt.kind != "exact" or cmd.author_slot is not None or fix.sequence or opt.edits:
        _parses(problem, i, argv, copy)
        commands_parsed += 1
        return "parsed"
    was, _busy = _busy, True
    try:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = cli.main([*argv, "--root", str(copy)])
        if code != 0:
            raise AssertionError(
                f"command exited {code}: {_where(problem, i, argv)}\n{out.getvalue()}"
            )
        left = [
            q
            for q in checks_run.check_vault(read_vault(copy)).problems
            if (q.rule, q.file, q.where) == (problem.rule, problem.file, problem.where)
        ]
    finally:
        _busy = was
    if left:
        raise AssertionError(
            f"command does not clear the problem ({problem.rule} in {problem.file}, {problem.where}): "
            f"{_where(problem, i, argv)}"
        )
    commands_run += 1
    return "ran"


def _copy_of(vault_root: Path) -> Path:
    global _tmp
    if _tmp is None:
        _tmp = tempfile.TemporaryDirectory(prefix="scat-harness-")
    dest = Path(tempfile.mkdtemp(dir=_tmp.name))
    shutil.copytree(vault_root, dest, dirs_exist_ok=True)
    return dest


def observe(vault_root: Path, report: Report) -> None:
    """What the conftest calls for every Report: R1 on all of it, R2 on a few samples per (rule, kind, verb)."""
    validate_report(report)
    todo = []
    for p in report.problems:
        for i, opt in enumerate(p.fix_data.options):
            if opt.command is None:
                continue
            key = (p.rule, opt.kind, opt.command.argv[0])
            if _samples[key] < SAMPLES_PER_KEY:
                _samples[key] += 1
                todo.append((p, i))
    if not todo:
        return
    pristine = _copy_of(vault_root)  # before anything runs
    for p, i in todo:
        assert_option_works(p, i, _copy_of(pristine))


def wrap(original):
    """The function that replaces `scat_kg.checks.run._run`: the same result, observed."""

    def run(vault, *args, **kwargs):
        report = original(vault, *args, **kwargs)
        if not _busy:
            guard_report(report)
            observe(Path(vault.root), report)
        return report

    return run
