"""WP11-U2: the fix data model renders today's text and serialises to the machine-interface schema."""

import dataclasses
import importlib.util
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

import scat_kg
from scat_kg.checks.problem import Problem
from scat_kg.checks.text import choose, one, steps
from scat_kg.contract import SCHEMA_VERSION
from scat_kg.fix import Command, Edit, Fix, FixOption

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "seed_helpers", ROOT / "tests" / "checks" / "helpers.py"
)
_helpers = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_helpers)
base = _helpers.base
SCHEMA = json.loads(
    (ROOT / "contracts" / "machine-interface.schema.json").read_text(encoding="utf-8")
)
VALIDATOR = Draft202012Validator(SCHEMA)

TEXTS = [
    ["add the line `a: b`"],
    ["first", "second"],
    ["one\n       multi\n       line", "two"],
    ["x\n  y", "z\n  w\n  v", "last"],
]
NOTES = [(), ("A note.",), ("A note.", "Another\n  note.")]
HEADS = [None, "Fix, choose a way:"]


def opts(texts):
    return [FixOption("manual", t) for t in texts]


@pytest.mark.parametrize("texts", TEXTS)
@pytest.mark.parametrize("notes", NOTES)
@pytest.mark.parametrize("head", HEADS)
def test_choose_matches_the_old_helper(texts, notes, head):
    assert Fix.choose("options", opts(texts), head, notes).render() == choose(texts, notes, head)


@pytest.mark.parametrize("text", ["do it", "do it\n  more"])
def test_one_matches_the_old_helper(text):
    assert Fix.one("manual", FixOption("manual", text)).render() == one(text)


@pytest.mark.parametrize("texts", TEXTS)
@pytest.mark.parametrize("head", HEADS)
def test_steps_match_the_old_helper(texts, head):
    new = Fix.steps("exact", opts(texts), head).render()
    assert new == (steps(texts) if head is None else steps(texts, head))


def test_legacy_round_trip():
    text = "Fix, choose one:\n  1. a\n  2. b\nnote"
    f = Fix.legacy(text)
    assert f.render() == text
    assert f.to_dict() == {
        "kind": "manual",
        "options": [{"kind": "manual", "text": text}],
        "notes": [],
    }


def check_doc(result):
    d = result.to_dict()
    assert VALIDATOR.is_valid(d), [e.message for e in VALIDATOR.iter_errors(d)]
    return d


def test_clean_check_validates(make_vault):
    root = _helpers.vault(make_vault).root
    d = check_doc(scat_kg.check(root=root))
    assert d["problems"] == [] and d["ok"] is True


PROBLEM = Draft202012Validator({"$ref": "#/$defs/Problem", "$defs": SCHEMA["$defs"]})


def assert_problem_json_matches(p, q):
    """True whether the fix is the legacy one-option wrapper or typed: the JSON carries the fix data, and the
    rendered text carries the whole fix block (each line indented two spaces)."""
    assert p["text"] == q.render()
    assert p["fix"] == q.fix_data.to_dict()
    assert q.fix == q.fix_data.render()
    assert "\n".join("  " + ln for ln in q.fix.split("\n")) in p["text"]


def test_seeded_defect_validates(make_vault):
    files = base()
    files["concern/safe-handling.md"] = files["concern/safe-handling.md"].replace(
        'description: "D"\n', ""
    )
    root = _helpers.vault(make_vault, files).root
    result = scat_kg.check(root=root)
    d = check_doc(result)
    assert d["problems"], "the seeded defect must produce a problem"
    for p, q in zip(d["problems"], result.problems):
        assert_problem_json_matches(p, q)


def test_typed_fix_validates_and_renders():
    cmd = Command(("set-status", "x", "draft"), 'scat_kg.set_status("x", "draft")')
    edit = Edit("set-field", "concern/x.md", field="status", value="draft")
    fix = Fix.choose(
        "options",
        [
            FixOption("exact", "run it", command=cmd),
            FixOption("exact", "write it", edits=(edit,)),
        ],
    )
    assert fix.render() == "Fix, choose one:\n  1. run it\n  2. write it"
    doc = {
        "schema_version": SCHEMA_VERSION,
        "kind": "check",
        "operation": "check",
        "ok": False,
        "problems": [
            {
                "rule": "SCAT-FM-STATUS",
                "severity": "error",
                "file": "concern/x.md",
                "line": 3,
                "column": None,
                "field": "status",
                "where": "field `status`",
                "what": "bad",
                "repeat": 1,
                "fix": fix.to_dict(),
                "text": "t",
            }
        ],
    }
    assert VALIDATOR.is_valid(doc), [e.message for e in VALIDATOR.iter_errors(doc)]
    assert fix.to_dict()["options"][0]["command"] == {
        "argv": ["set-status", "x", "draft"],
        "repl": 'scat_kg.set_status("x", "draft")',
    }


def test_problem_json_matches_for_a_typed_multi_option_fix():
    legacy = Problem("SCAT-DONE-FIELD", "error", "concern/x.md", "field `d`", "missing", "Fix: x")
    cmd = Command(("set-status", "x", "draft"), 'scat_kg.set_status("x", "draft")')
    fix = Fix.choose(
        "options",
        [
            FixOption("exact", "run it\n       twice", command=cmd),
            FixOption("manual", "write it"),
        ],
        notes=("A note.",),
    )
    q = dataclasses.replace(legacy, fix_data=fix)
    p = q.to_dict()
    assert PROBLEM.is_valid(p), [e.message for e in PROBLEM.iter_errors(p)]
    assert (
        p["fix"]["options"][0]["text"] != q.fix
    )  # what the old assertion got wrong for typed fixes
    assert_problem_json_matches(p, q)
    # and for the legacy wrapper
    assert_problem_json_matches(legacy.to_dict(), legacy)
