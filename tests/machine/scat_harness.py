"""WP11-R1 and WP11-R2 harness: validate every check result the suite produces, and try every fix command.

`tests/checks/conftest.py` wraps the one function every check goes through and hands each Report to `observe`.
The two checks are plain functions so a unit test can call them directly:

- `validate_report` (R1): every Problem, and the whole check document, validates against the schema.
- `assert_option_works` (R2): an exact option's command, run as given on a copy of the vault, exits 0 and the
  problem is gone on a re-check; a slot option's (or any sequence step's) argv is accepted by `scat`'s parser.
"""

import contextlib
import io
import json
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

# What the session saw (read by tests/machine/test_harness_coverage.py).
tests_seen: set[str] = set()  # node ids of the check tests that ran
rules_validated: set[str] = set()
severities_seen: dict[str, str] = {}  # rule id -> severity of the problems validated
problems_validated = 0
commands_run = 0
commands_parsed = 0
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
    if opt.kind != "exact" or cmd.author_slot is not None or fix.sequence:
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
            observe(Path(vault.root), report)
        return report

    return run
