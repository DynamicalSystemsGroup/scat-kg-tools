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


def cmd(argv, repl, **more):
    return {"argv": argv, "repl": repl, **more}


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
    return {"schema_version": 2, "kind": kind, "operation": operation, "ok": ok} | more


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
            edits=[{"action": "delete-file", "file": "narrative/x.md"}],
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

# SCAT-DRAFT-TABLE-DUPLICATE: the notes merge (author), then delete the file, then run index, then fix the links
TABLE_DUPLICATE = fix(
    "exact",
    [
        option(
            "slot",
            "put the text of `notes` into the kept page",
            edits=[
                {
                    "action": "set-field",
                    "file": "narrative/kept.md",
                    "field": "notes",
                    "value": "<the two notes, joined>",
                    "author_slot": "<the two notes, joined>",
                }
            ],
        ),
        option(
            "exact",
            "delete the page",
            edits=[{"action": "delete-file", "file": "narrative/dup.md"}],
        ),
        option("exact", "run `scat index`", command=cmd(["index"], "scat_kg.index()")),
        option(
            "exact",
            "change the link",
            edits=[
                {
                    "action": "replace-text",
                    "file": "concern/a.md",
                    "line": 12,
                    "find": "[[dup]]",
                    "replace": "[[kept]]",
                }
            ],
        ),
    ],
    head="Fix, steps in this order:",
    sequence=True,
)
# SCAT-DRAFT-TABLE-TYPE: the author chooses the name that appears in the command
TABLE_TYPE_SLOT = fix(
    "slot",
    [
        option(
            "slot",
            "name the node the row end links to (author: choose the name)",
            edits=[
                {
                    "action": "set-field",
                    "file": "narrative/n.md",
                    "field": "description",
                    "value": "<node-name>",
                    "author_slot": "<node-name>",
                }
            ],
        ),
        option(
            "slot",
            "run `scat stub <node-name> --type concern`",
            command=cmd(
                ["stub", "<node-name>", "--type", "concern"],
                'scat_kg.stub("<node-name>", type="concern")',
                author_slot="<node-name>",
            ),
        ),
    ],
    head="Fix, two steps, in this order:",
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
        problem("SCAT-DRAFT-TABLE-DUPLICATE", "warning", STEPS),
        problem("SCAT-DRAFT-TABLE-DUPLICATE", "warning", TABLE_DUPLICATE, file="narrative/dup.md"),
        problem("SCAT-DRAFT-TABLE-TYPE", "warning", TABLE_TYPE_SLOT, file="narrative/n.md"),
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
    "wrong schema_version": mutated(CLEAN, lambda d: d.update(schema_version=1)),
    "string schema_version": mutated(CLEAN, lambda d: d.update(schema_version="2")),
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
    "slot with no author slot anywhere": mutated(
        CHECK,
        lambda d: d["problems"][-1]["fix"]["options"][1]["command"].pop("author_slot"),
    ),
    "empty command author slot": mutated(
        CHECK,
        lambda d: d["problems"][-1]["fix"]["options"][1]["command"].update(author_slot=""),
    ),
    "refusal without fix": mutated(REFUSED_STUB, lambda d: d["refused"][0].pop("fix")),
}


@pytest.mark.parametrize("name", MALFORMED)
def test_malformed_is_rejected(name):
    assert not valid(MALFORMED[name])


@pytest.mark.parametrize(
    "path,ok",
    [
        ("a.md", True),
        ("concern/a.md", True),
        ("scat.toml", True),
        ("my..notes.md", True),
        ("a/..b/c.md", True),
        ("/a.md", False),
        ("../a.md", False),
        ("a/../b.md", False),
        ("a/..", False),
        ("..", False),
        ("a\\b.md", False),
        ("", False),
    ],
)
def test_vault_paths(path, ok):
    d = copy.deepcopy(OPERATION)
    d["changed"] = [path]
    assert valid(d) is ok


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


def def_properties(*names: str) -> set[str]:
    out: set[str] = set()
    for name in names:
        out |= set(SCHEMA["$defs"][name].get("properties", {}))
    return out


EDITS = ("SetField", "DeleteField", "ReplaceText", "DeleteLine", "RenameFile", "DeleteFile")
# the table's first column -> the schema objects whose properties its fields must be among
OBJECTS = {
    "every document": ["CheckResult", "StatusResult", "OperationResult"],
    "check": ["CheckResult"],
    "problem": ["Problem"],
    "status": ["StatusResult"],
    "status row": ["StatusRow"],
    "operation": ["OperationResult"],
    "record-edge, remove-edge result": ["OperationResult"],
    "edge": ["EdgeRef"],
    "row": ["RowRef"],
    "refusal": ["Refusal"],
    "fix": ["Fix"],
    "option": ["FixOption"],
    "command": ["Command"],
    "edit": list(EDITS),
}


def promised() -> dict[str, set[str]]:
    section = PAGE.split("## Fields you may rely on", 1)[1].split("\n## ", 1)[0]
    out: dict[str, set[str]] = {}
    for row in section.splitlines():
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        is_row = row.startswith("|") and len(cells) == 2 and not set(cells[0]) <= {"-", " "}
        if is_row and cells[0] != "Object":
            out[cells[0]] = set(re.findall(r"`([^`]+)`", re.sub(r"\([^)]*\)", "", cells[1])))
    return out


def test_every_promised_field_exists_under_its_own_object():
    table = promised()
    assert set(table) == set(OBJECTS)
    for obj, fields in table.items():
        assert fields, obj
        if obj == "every document":  # each of the three result kinds has all of them
            for name in OBJECTS[obj]:
                assert fields <= def_properties(name), (name, fields - def_properties(name))
        elif obj == "edit":  # an edit uses some of them; every field belongs to one action
            assert fields == def_properties(*EDITS)
        else:
            assert fields <= def_properties(*OBJECTS[obj]), (obj, fields)
        for name in fields:
            assert f"`{name}`" in PAGE


def test_page_rule_id_pattern_is_the_schemas():
    assert f"`{SCHEMA['$defs']['RuleId']['pattern']}`" in PAGE


def test_promised_fields_the_schema_requires_are_all_promised():
    """The required properties of each object are a subset of what the page promises for it."""
    table = promised()
    for obj, names in OBJECTS.items():
        if obj in ("every document", "edit", "record-edge, remove-edge result"):
            continue  # the last: an operation plus fields; its required ones are the operation row's
        required = set()
        for name in names:
            required |= set(SCHEMA["$defs"][name].get("required", []))
        assert required <= table[obj] | table["every document"], (obj, required - table[obj])


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


def test_page_states_the_replace_text_promise():
    flat = " ".join(PAGE.split())
    for phrase in (
        "the literal text as written in the file at that line",
        "Without `column`, `find` is replaced everywhere on `line`",
        "only the occurrence at that column",
    ):
        assert phrase in flat, phrase


def test_page_states_that_edits_are_computed_from_the_file_as_checked():
    flat = " ".join(PAGE.split())
    for phrase in (
        "Edits are computed from the file as checked",
        "`set-field` carries the whole new value",
        "two fixes for one field do not compose",
        "apply one, then re-check",
    ):
        assert phrase in flat, phrase


def test_page_states_that_a_slot_fix_may_choose_among_exact_values():
    flat = " ".join(PAGE.split())
    for phrase in (
        "chooses among exact values (no `author_slot`)",
        "`timeframe`",
        "e.g. the missing `timeframe` of a page (SCAT-DONE-FIELD)",
        "An option may only add (a suggestion you confirm) without clearing the problem on its own",
        "read its `text`",
    ):
        assert phrase in flat, phrase


def test_schema_descriptions_restate_the_clarifications():
    defs = SCHEMA["$defs"]
    assert "literal text as written in the file" in defs["ReplaceText"]["description"]
    assert "everywhere on the line" in defs["ReplaceText"]["description"]
    assert "do not compose" in defs["SetField"]["description"]
    assert "suggestion you confirm" in defs["FixOption"]["properties"]["text"]["description"]


def test_page_keeps_the_definitions_the_compression_must_not_drop():
    flat = " ".join(PAGE.split())
    for phrase in (
        "`neighborhood`, a page and its linked pages",
        "already right, nothing written",
        "sentences for a person",
        "the message as `scat check` prints it",
        "exactly one JSON document",
    ):
        assert phrase in flat, phrase
