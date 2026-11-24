"""The machine-interface contract (WP11-G1): the schema, sample documents, and the page that describes them."""

import copy
import json
import re
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

CONTRACTS = Path(__file__).resolve().parent.parent / "contracts"
SCHEMA = json.loads((CONTRACTS / "machine-interface.schema.json").read_text(encoding="utf-8"))
PAGE = (CONTRACTS / "machine-interface.md").read_text(encoding="utf-8")
VALIDATOR = Draft202012Validator(SCHEMA)


def valid(doc) -> bool:
    return VALIDATOR.is_valid(doc)


def cmd(argv, repl):
    return {"argv": argv, "repl": repl}


def option(kind, text, **more):
    return {"kind": kind, "text": text, **more}


def fix(kind, options, head=None, notes=(), **more):
    out = {"kind": kind, "options": options, "notes": list(notes), **more}
    if head:
        out["head"] = head
    return out


def problem(rule, severity, fix_, **more):
    base = {
        "rule": rule,
        "severity": severity,
        "file": "concern/a.md",
        "line": 3,
        "column": 1,
        "field": "status",
        "where": "field `status`",
        "what": "missing",
        "repeat": 1,
        "fix": fix_,
        "text": f"{severity} [{rule}] concern/a.md:3:1 field `status`: missing\n  Fix: ...",
    }
    return base | more


def doc(kind, operation, ok, **more):
    return {"schema_version": 1, "kind": kind, "operation": operation, "ok": ok} | more


SET_DRAFT = cmd(["set-status", "a", "draft"], 'scat_kg.set_status("a", "draft")')
EXACT = fix(
    "exact",
    [
        option(
            "exact",
            'replace the field with the line `title: "A"`',
            edits=[{"action": "set-field", "file": "concern/a.md", "field": "title", "value": "A"}],
        )
    ],
)
OPTIONS = fix(
    "options",
    [
        option("exact", "run `scat set-status a draft`", command=SET_DRAFT),
        option(
            "exact",
            "delete `group:` and its list items",
            edits=[{"action": "delete-field", "file": "concern/a.md", "field": "group"}],
        ),
    ],
    head="Fix, choose one:",
)
SLOT = fix(
    "slot",
    [
        option(
            "slot",
            'add the line `description: "<one sentence you write>"` (author)',
            edits=[
                {
                    "action": "set-field",
                    "file": "concern/a.md",
                    "field": "description",
                    "value": "<one sentence you write>",
                    "author_slot": "<one sentence you write>",
                }
            ],
        )
    ],
)
ADVISORY = fix("advisory", [option("advisory", "nothing is required")])
MANUAL = fix("manual", [option("manual", "repair the frontmatter by hand")])
STEPS = fix(
    "exact",
    [
        option(
            "exact",
            "delete the file",
            edits=[{"action": "delete-file", "file": "heldby/x.md"}],
            command=cmd(["index"], "scat_kg.index()"),
        ),
        option(
            "exact",
            "rename it",
            edits=[{"action": "rename-file", "file": "a.md", "to": "b.md"}],
        ),
        option(
            "exact",
            "replace the link",
            edits=[
                {
                    "action": "replace-text",
                    "file": "a.md",
                    "line": 9,
                    "column": 2,
                    "find": "[[x]]",
                    "replace": "[[y]]",
                }
            ],
        ),
    ],
    head="Fix, three steps:",
    sequence=True,
)

CHECK = doc(
    "check",
    "check",
    False,
    problems=[
        problem("SCAT-FM-SHAPE", "error", EXACT),
        problem("SCAT-FM-STATUS", "error", OPTIONS),
        problem("SCAT-DONE-FIELD", "error", SLOT, field="description"),
        problem("SCAT-NOTE-X", "warning", ADVISORY, line=None, column=None, field=None),
        problem("SCAT-FM-PARSE", "error", MANUAL, repeat=2),
        problem("SCAT-REL-DUPLICATE", "warning", STEPS),
    ],
)
CLEAN = doc("check", "check", True, problems=[])
WARNING_ONLY = doc("check", "check", True, problems=[problem("SCAT-MENTION", "warning", EXACT)])
STATUS = doc(
    "status",
    "status",
    True,
    scope="vault",
    rows=[
        {"path": "concern/a.md", "name": "a", "type": "concern", "status": "draft"},
        {"path": "concerns.md", "name": "concerns", "type": "class", "status": None},
        {"path": "x.md", "name": "x", "type": None, "status": None},
    ],
    counts={"stub": 0, "draft": 1, "done": 0, "other": 1, "none": 1},
    notes=[],
)
OPERATION = doc(
    "operation",
    "set-status",
    True,
    created=[],
    changed=["concern/a.md"],
    unchanged=[],
    refused=[],
    notes=["`status` set to draft (was stub)"],
)
EMPTY_OP = {"created": [], "changed": [], "unchanged": [], "notes": []}
REFUSED_CHECK = doc(
    "operation",
    "check",
    False,
    refused=[
        {
            "subject": "nowhere",
            "why": "the vault folder does not exist",
            "fix": fix("advisory", [option("advisory", "pass the vault folder")], head=None),
        }
    ],
    **EMPTY_OP,
)
REFUSED_STUB = doc(
    "operation",
    "stub",
    False,
    refused=[
        {
            "subject": "name `A b`",
            "why": "not a legal name",
            "fix": fix(
                "exact",
                [
                    option(
                        "exact",
                        "run `scat stub a-b --type concern`",
                        command=cmd(
                            ["stub", "a-b", "--type", "concern"],
                            'scat_kg.stub("a-b", type="concern")',
                        ),
                    )
                ],
            ),
        }
    ],
    **EMPTY_OP,
)

SAMPLES = {
    "check with problems": CHECK,
    "clean check": CLEAN,
    "check with warnings only": WARNING_ONLY,
    "status": STATUS,
    "operation": OPERATION,
    "refused check": REFUSED_CHECK,
    "refused stub": REFUSED_STUB,
}


def test_schema_is_a_valid_draft_2020_12_schema():
    Draft202012Validator.check_schema(SCHEMA)
    assert SCHEMA["$schema"] == "https://json-schema.org/draft/2020-12/schema"


@pytest.mark.parametrize("name", SAMPLES)
def test_sample_validates(name):
    VALIDATOR.validate(SAMPLES[name])


def test_samples_cover_every_fix_kind_and_edit_action():
    text = json.dumps(CHECK)
    for kind in ("exact", "options", "slot", "advisory", "manual"):
        assert f'"kind": "{kind}"' in text
    for action in ("set-field", "delete-field", "replace-text", "rename-file", "delete-file"):
        assert action in text


def mutated(base, fn):
    d = copy.deepcopy(base)
    fn(d)
    return d


MALFORMED = {
    "missing schema_version": mutated(CLEAN, lambda d: d.pop("schema_version")),
    "wrong schema_version": mutated(CLEAN, lambda d: d.update(schema_version=2)),
    "string schema_version": mutated(CLEAN, lambda d: d.update(schema_version="1")),
    "wrong kind": mutated(CLEAN, lambda d: d.update(kind="report")),
    "missing ok": mutated(CLEAN, lambda d: d.pop("ok")),
    "unknown severity": mutated(CHECK, lambda d: d["problems"][0].update(severity="fatal")),
    "bad fix kind": mutated(CHECK, lambda d: d["problems"][0]["fix"].update(kind="auto")),
    "bad option kind": mutated(
        CHECK, lambda d: d["problems"][0]["fix"]["options"][0].update(kind="options")
    ),
    "bad edit action": mutated(
        CHECK, lambda d: d["problems"][0]["fix"]["options"][0]["edits"][0].update(action="sed")
    ),
    "bad rule id": mutated(CHECK, lambda d: d["problems"][0].update(rule="fm-shape")),
    "line zero": mutated(CHECK, lambda d: d["problems"][0].update(line=0)),
    "missing text": mutated(CHECK, lambda d: d["problems"][0].pop("text")),
    "absolute file": mutated(CHECK, lambda d: d["problems"][0].update(file="/tmp/a.md")),
    "backslash file": mutated(CHECK, lambda d: d["problems"][0].update(file="concern\\a.md")),
    "ok true with an error": mutated(CHECK, lambda d: d.update(ok=True)),
    "ok false with only warnings": mutated(WARNING_ONLY, lambda d: d.update(ok=False)),
    "ok true with a refusal": mutated(REFUSED_STUB, lambda d: d.update(ok=True)),
    "ok false with no refusal": mutated(OPERATION, lambda d: d.update(ok=False)),
    "status without other": mutated(STATUS, lambda d: d["counts"].pop("other")),
    "options fix with one option": mutated(
        CHECK,
        lambda d: d["problems"][1]["fix"].update(options=d["problems"][1]["fix"]["options"][:1]),
    ),
    "slot without an author slot": mutated(
        CHECK, lambda d: d["problems"][2]["fix"]["options"][0]["edits"][0].pop("author_slot")
    ),
    "exact without command or edits": mutated(
        CHECK, lambda d: d["problems"][0]["fix"]["options"][0].pop("edits")
    ),
    "advisory with a command": mutated(
        CHECK, lambda d: d["problems"][3]["fix"]["options"][0].update(command=SET_DRAFT)
    ),
    "command without repl": mutated(
        CHECK, lambda d: d["problems"][1]["fix"]["options"][0]["command"].pop("repl")
    ),
    "set-field without value": mutated(
        CHECK, lambda d: d["problems"][0]["fix"]["options"][0]["edits"][0].pop("value")
    ),
    "refusal without fix": mutated(REFUSED_STUB, lambda d: d["refused"][0].pop("fix")),
}


@pytest.mark.parametrize("name", MALFORMED)
def test_malformed_is_rejected(name):
    assert not valid(MALFORMED[name])


def test_unknown_extra_fields_are_allowed_everywhere():
    d = copy.deepcopy(CHECK)
    d["extra"] = 1
    d["problems"][0]["extra"] = 1
    d["problems"][0]["fix"]["extra"] = 1
    d["problems"][0]["fix"]["options"][0]["extra"] = 1
    d["problems"][0]["fix"]["options"][0]["edits"][0]["extra"] = 1
    assert valid(d)
    s = copy.deepcopy(STATUS)
    s["rows"][0]["extra"] = 1
    s["extra"] = 1
    assert valid(s)
    r = copy.deepcopy(REFUSED_STUB)
    r["refused"][0]["extra"] = 1
    assert valid(r)


def test_schema_does_not_enumerate_rule_ids():
    rule = SCHEMA["$defs"]["RuleId"]
    assert "enum" not in rule and "const" not in rule and "pattern" in rule
    assert "enum" not in SCHEMA["$defs"]["OperationName"]


def test_contract_page_is_at_most_600_words():
    assert len(PAGE.split()) <= 600


def schema_property_names(node) -> set[str]:
    names: set[str] = set()
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "properties" and isinstance(value, dict):
                names.update(value)
            names |= schema_property_names(value)
    elif isinstance(node, list):
        for item in node:
            names |= schema_property_names(item)
    return names


def promised_fields() -> set[str]:
    section = PAGE.split("## Fields you may rely on", 1)[1].split("\n## ", 1)[0]
    out: set[str] = set()
    for row in section.splitlines():
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if row.startswith("|") and len(cells) == 2 and not set(cells[0]) <= {"-", " "}:
            out |= set(re.findall(r"`([^`]+)`", re.sub(r"\([^)]*\)", "", cells[1])))
    out.discard("Fields")
    return out


def test_every_promised_field_is_named_on_the_page_and_exists_in_the_schema():
    fields = promised_fields()
    assert len(fields) >= 40
    known = schema_property_names(SCHEMA)
    assert fields <= known, sorted(fields - known)
    for name in fields:
        assert f"`{name}`" in PAGE


def test_page_states_the_rules_of_the_interface():
    for phrase in (
        "schema_version",
        "Adding a field keeps the version",
        "bumps",
        "never renamed, only retired",
        "stdout",
        "stderr",
        "to_dict()",
        "0 when `ok`",
        "2 for a command line",
        "author_slot",
    ):
        assert phrase.lower() in PAGE.lower(), phrase
    for action in SCHEMA["$defs"]["Edit"]["oneOf"]:
        name = action["$ref"].rsplit("/", 1)[1]
        const = SCHEMA["$defs"][name]["properties"]["action"]["const"]
        assert f"`{const}`" in PAGE
