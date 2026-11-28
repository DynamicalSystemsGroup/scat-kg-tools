"""The `guide` and `stage` kinds of the machine-interface schema: sample documents that must validate, and
mutations that must not. The `stage` samples are the documents the server returns (design section 2)."""

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

SCHEMA = json.loads(
    (Path(__file__).resolve().parents[2] / "contracts" / "machine-interface.schema.json").read_text(
        encoding="utf-8"
    )
)
VALIDATOR = Draft202012Validator(SCHEMA)

PERSON = {"kind": "person", "says": "the organiser says the sessions are planned"}
DETECT_FALSE = {
    "kind": "detect",
    "check": "every narrative is done and the whole-vault check has no errors",
    "holds": False,
    "detail": "3 of 4 narratives done; the check has 0 errors",
}
DETECT_TRUE = {
    "kind": "detect",
    "check": "the stakeholder-group count is at the cap",
    "holds": True,
    "detail": "6 groups, cap 6",
}


def exit_(id_, to, dir_, trigger, decides, predicate):
    return {
        "id": id_,
        "to": to,
        "dir": dir_,
        "trigger": trigger,
        "decides": decides,
        "predicate": predicate,
    }


L2 = exit_("L2", "capture", "forward", "the sessions are planned", "organiser", PERSON)
L5 = exit_("L5", "analyse", "forward", "the narratives are coded", "coder", DETECT_FALSE)
L7 = exit_("L7", "plan", "backward", "the cap refuses a new group", "organiser", PERSON)
L1 = exit_(
    "L1",
    "any",
    "start",
    "the first call on a vault with no stage recorded",
    "coder",
    {"kind": "person", "says": "the person names the stage"},
)


def stage_doc(operation, **more):
    return {
        "schema_version": 3,
        "kind": "stage",
        "operation": operation,
        "ok": True,
        "mode": "optional",
    } | more


GUIDE = {
    "schema_version": 3,
    "kind": "guide",
    "operation": "guide",
    "ok": True,
    "mode": None,
    "stage": "code",
    "text": "# code\n...",
    "docs": "docs/coding.md",
    "tools": ["check", "status"],
    "exits": ["L5", "L7", "L8"],
}
INDEX = GUIDE | {
    "stage": "index",
    "docs": None,
    "tools": ["which_stage", "set_stage"],
    "exits": ["L1"],
}
WHICH = stage_doc(
    "which-stage",
    stage="code",
    set_by="Ana",
    work="Go round the coding loop for each narrative.",
    required_inputs=["field notes", "a set-up vault"],
    tools=["check", "status"],
    prompts=["explain-a-problem"],
    exits=[L5, L7],
    text="The project is in the code stage, set by Ana.",
    guide="scat://guide/code",
)
WHICH_UNKNOWN = stage_doc(
    "which-stage",
    stage="unknown",
    set_by=None,
    work="No stage is recorded.",
    stages=[
        {"name": "plan", "work": "Set the terms."},
        {"name": "capture", "work": "Gather notes."},
    ],
    exits=[L1],
    text="No stage is recorded; the person decides.",
    guide="scat://guide/index",
)
SET_MOVED = stage_doc(
    "set-stage",
    moved=True,
    **{"from": "code"},
    to="analyse",
    transition="L5",
    decides="coder",
    advisory=["L5 is a detect predicate and does not hold now: 3 of 4 narratives done"],
    exits=[exit_("L6", "code", "backward", "reading shows something to revisit", "coder", PERSON)],
    text="Moved from code to analyse.",
    stage="analyse",
)
SAMPLES = {
    "guide": GUIDE,
    "index": INDEX,
    "which_stage": WHICH,
    "which_stage unknown": WHICH_UNKNOWN,
    "set_stage moved": SET_MOVED,
}


@pytest.mark.parametrize("name", SAMPLES)
def test_sample_validates(name):
    VALIDATOR.validate(SAMPLES[name])


def test_a_refused_stage_call_is_an_operation_result():
    refusal = {
        "schema_version": 3,
        "kind": "operation",
        "operation": "fingerprint",
        "ok": False,
        "mode": None,
        "created": [],
        "changed": [],
        "unchanged": [],
        "notes": [],
        "refused": [
            {
                "subject": "fingerprint",
                "why": "`fingerprint` is not offered in the plan stage",
                "fix": {
                    "kind": "advisory",
                    "options": [{"kind": "advisory", "text": "ask"}],
                    "notes": [],
                },
            }
        ],
    }
    VALIDATOR.validate(refusal)


def mutated(base, fn):
    d = copy.deepcopy(base)
    fn(d)
    return d


MALFORMED = {
    "guide without text": mutated(GUIDE, lambda d: d.pop("text")),
    "guide with a mode": mutated(GUIDE, lambda d: d.update(mode="required")),
    "guide not ok": mutated(GUIDE, lambda d: d.update(ok=False)),
    "guide with a string exits": mutated(GUIDE, lambda d: d.update(exits="L5")),
    "guide at version 4": mutated(GUIDE, lambda d: d.update(schema_version=4)),
    "stage of another kind": mutated(WHICH, lambda d: d.update(kind="state")),
    "which_stage without exits": mutated(WHICH, lambda d: d.pop("exits")),
    "which_stage without guide": mutated(WHICH, lambda d: d.pop("guide")),
    "an exit without a decider": mutated(WHICH, lambda d: d["exits"][0].pop("decides")),
    "a detect exit with no holds": mutated(
        WHICH, lambda d: d["exits"][0]["predicate"].pop("holds")
    ),
    "a person exit with a check": mutated(
        WHICH, lambda d: d["exits"][0].update(predicate={"kind": "person", "check": "x"})
    ),
    "an exit with a bad direction": mutated(WHICH, lambda d: d["exits"][0].update(dir="sideways")),
    "set_stage without moved": mutated(SET_MOVED, lambda d: d.pop("moved")),
    "a moved set_stage without a transition": mutated(SET_MOVED, lambda d: d.pop("transition")),
    "a moved set_stage without advisory": mutated(SET_MOVED, lambda d: d.pop("advisory")),
    "set_stage with a bad transition id": mutated(SET_MOVED, lambda d: d.update(transition="five")),
    "a stage operation that is not one of the two": mutated(
        WHICH, lambda d: d.update(operation="stage")
    ),
}


@pytest.mark.parametrize("name", MALFORMED)
def test_malformed_is_rejected(name):
    assert not VALIDATOR.is_valid(MALFORMED[name]), name


def test_no_new_kind_needed_a_version_bump():
    assert SCHEMA["$defs"]["SchemaVersion"] == {"const": 3}
    for name in ("GuideResult", "StageResult"):
        assert name in SCHEMA["$defs"]
