"""WP11-U5: the fixes of the front-matter, vault-wide and index rules are typed data that match their text.

Each case seeds one defect (the fixture vault of tests/checks/helpers.py), checks it, and asserts for every
problem of the named rule: the fix is data (not the legacy wrapper), its kind is the catalogue's (a one-option
fix takes its option's kind), `field` is set exactly when `where` names a field, the `to_dict()` validates
against the schema, and every command and edit value appears in the rendered text.
"""

import importlib.util
import json
import re
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from scat_kg.checks import check_vault
from scat_kg.cli import _parser

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "seed_helpers", ROOT / "tests" / "checks" / "helpers.py"
)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)
VALIDATOR = Draft202012Validator(
    json.loads((ROOT / "contracts" / "machine-interface.schema.json").read_text(encoding="utf-8"))
)
CATALOGUE_KIND = dict(
    re.findall(
        r"^\| (SCAT-[A-Z-]+) \| \w+ \| [^|]+ \| [^|]+ \| (\w+) \|",
        (ROOT / "contracts" / "rule-catalogue.md").read_text(encoding="utf-8"),
        re.MULTILINE,
    )
)

C = "concern/safe-handling.md"
HELDBY = "heldby/staff-holds-safe-handling.md"
RAW = "scenario-raw/desk-day.md"
CLS = "class/concerns.md"


def fm(body: str) -> str:
    return f"---\n{body}---\n"


def class_page(make_vault, indexes="concern"):
    return doc_class(indexes) + H.region_for(make_vault, "concerns")


def doc_class(indexes):
    return H.doc("class", "Concerns", status=None, extra=f"indexes: {indexes}")


GROUPS = {
    f"stakeholder-group/{n}.md": H.doc("stakeholder-group", n.title()) for n in ("g-one", "g-two")
}

# (case id, rule, files, removed) where files may be a callable of make_vault
CASES = [
    ("parse", "SCAT-FM-PARSE", {C: "---\ntype: concern\nstatus: done\ntitle: x\n"}, ()),
    (
        "required-status",
        "SCAT-FM-REQUIRED",
        {C: fm('type: concern\ntitle: "Safe handling"\ndescription: "D"\n')},
        (),
    ),
    (
        "required-title",
        "SCAT-FM-REQUIRED",
        {C: fm("type: concern\nstatus: stub\ndescription: D\n")},
        (),
    ),
    (
        "required-title-relation",
        "SCAT-FM-REQUIRED",
        {
            HELDBY: fm(
                'type: heldby\nstatus: stub\ngroup: "[[staff]]"\nconcern: "[[safe-handling]]"\n'
            )
        },
        (),
    ),
    (
        "required-title-empty-replaced",
        "SCAT-FM-REQUIRED",
        {C: fm("type: concern\nstatus: stub\ntitle:\n")},
        (),
    ),
    (
        "required-indexes-class",
        "SCAT-FM-REQUIRED",
        lambda mv: {CLS: fm('type: class\ntitle: "Concerns"\n') + H.region_for(mv, "concerns")},
        (),
    ),
    (
        "required-indexes-choice",
        "SCAT-FM-REQUIRED",
        {"class/foo.md": fm('type: class\ntitle: "Foo"\n')},
        (),
    ),
    ("type-near", "SCAT-FM-TYPE", {C: H.doc("Concern", "Safe handling")}, ()),
    ("type-list", "SCAT-FM-TYPE", {C: H.doc("gadget", "Safe handling")}, ()),
    (
        "type-empty",
        "SCAT-FM-TYPE",
        {C: fm('type:\nstatus: done\ntitle: "S"\n')},
        (),
    ),
    (
        "required-link",
        "SCAT-FM-REQUIRED-LINK",
        {HELDBY: H.doc("heldby", "H", extra='group: "[[staff]]"')},
        (),
    ),
    (
        "required-link-empty",
        "SCAT-FM-REQUIRED-LINK",
        {HELDBY: H.doc("heldby", "H", extra='group: "[[staff]]"\nconcern: ')},
        (),
    ),
    ("status-near", "SCAT-FM-STATUS", {C: H.doc("concern", "S", status="Done")}, ()),
    ("status-choice", "SCAT-FM-STATUS", {C: H.doc("concern", "S", status="finished")}, ()),
    (
        "indexes-near",
        "SCAT-FM-INDEXES",
        lambda mv: {CLS: class_page(mv, "concerns")},
        (),
    ),
    (
        "indexes-choice",
        "SCAT-FM-INDEXES",
        lambda mv: {CLS: class_page(mv, "widgets")},
        (),
    ),
    (
        "timeframe-near",
        "SCAT-FM-TIMEFRAME",
        {
            RAW: H.doc(
                "scenario-raw", "T", extra="timeframe: Past\n" + H.links("coded", "desk-day-coded")
            )
        },
        (),
    ),
    (
        "timeframe-choice",
        "SCAT-FM-TIMEFRAME",
        {
            RAW: H.doc(
                "scenario-raw", "T", extra="timeframe: soon\n" + H.links("coded", "desk-day-coded")
            )
        },
        (),
    ),
    (
        "shape-one-item-list",
        "SCAT-FM-SHAPE",
        {C: fm('type: concern\nstatus: done\ntitle:\n  - "Safe handling"\ndescription: "D"\n')},
        (),
    ),
    (
        "shape-scalar",
        "SCAT-FM-SHAPE",
        {C: fm('type: concern\nstatus: done\ntitle: "S"\ndescription: 42\n')},
        (),
    ),
    (
        "shape-mapping",
        "SCAT-FM-SHAPE",
        {C: fm('type: concern\nstatus: done\ntitle:\n  a: b\ndescription: "D"\n')},
        (),
    ),
    ("name-rename", "SCAT-NAME", {"concern/Bad Name.md": H.doc("concern", "Bad name")}, ()),
    (
        "name-duplicate",
        "SCAT-NAME",
        {"affordance/quick-checkout.md": H.doc("affordance", "Quick checkout")},
        (),
    ),
    (
        "name-class-wrong",
        "SCAT-NAME",
        {"class/foo.md": H.doc("class", "Concerns", status=None, extra="indexes: concern")},
        (),
    ),
    ("name-by-hand", "SCAT-NAME", {"concern/Привет.md": H.doc("concern", "Привет")}, ()),
    ("cap", "SCAT-CAP", GROUPS, ()),
    ("cap-config-missing", "SCAT-CAP-CONFIG", {}, ("scat.toml",)),
    ("cap-config-toml", "SCAT-CAP-CONFIG", {"scat.toml": "stakeholder_group_cap = \n"}, ()),
    ("cap-config-key", "SCAT-CAP-CONFIG", {"scat.toml": "other = 1\n"}, ()),
    ("cap-config-bad", "SCAT-CAP-CONFIG", {"scat.toml": "stakeholder_group_cap = 0\n"}, ()),
    (
        "index-no-markers",
        "SCAT-INDEX-STALE",
        {CLS: doc_class("concern")},
        (),
    ),
    ("index-missing", "SCAT-INDEX-STALE", {CLS: ""}, (CLS,)),
]


def problems_of(make_vault, files, remove, rule):
    if callable(files):
        files = files(make_vault)
    v = H.vault(make_vault, files, remove)
    return [p for p in check_vault(v).problems if p.rule == rule]


def check_doc(p):
    d = {
        "schema_version": 1,
        "kind": "check",
        "operation": "check",
        "ok": p.severity != "error",
        "problems": [p.to_dict()],
    }
    assert VALIDATOR.is_valid(d), [e.message for e in VALIDATOR.iter_errors(d)]


def assert_matches_text(opt, text):
    if opt.command is not None:
        assert f"`scat {' '.join(opt.command.argv)}`" in text
        _parser().parse_args(list(opt.command.argv))  # scat accepts the command line
        assert opt.command.repl in text
    for e in opt.edits:
        if e.action == "set-field" and e.value is not None:
            v = str(e.value)
            for part in v.split(e.author_slot) if e.author_slot else [v]:
                assert part in text, (part, text)
            if e.author_slot:
                assert e.author_slot in text
        if e.action == "rename-file":
            assert e.to.rsplit("/", 1)[-1] in text


@pytest.mark.parametrize("case", CASES, ids=[c[0] for c in CASES])
def test_the_fix_is_typed_data_that_matches_its_text(make_vault, case):
    _, rule, files, remove = case
    found = problems_of(make_vault, files, remove, rule)
    assert found, f"the seed gave no {rule}"
    for p in found:
        fix = p.fix_data
        assert (
            fix.verbatim is None or rule == "SCAT-FM-STATUS"
        )  # the one-line choice, see fixes.inline
        assert not (len(fix.options) == 1 and fix.options[0].text == fix.verbatim)  # not legacy
        if len(fix.options) == 1:
            assert fix.kind == fix.options[0].kind
            assert fix.kind in (CATALOGUE_KIND[rule], "exact", "manual", "slot")
        else:
            assert fix.kind == CATALOGUE_KIND[rule] == "options"
        for o in fix.options:
            assert o.kind != "manual" or (o.command is None and not o.edits)
            if o.kind == "exact":
                assert o.command or o.edits
            if o.kind == "slot":
                assert o.command.author_slot if o.command else any(e.author_slot for e in o.edits)
            assert_matches_text(o, p.fix)
        assert (p.field is not None) == p.where.startswith("field `")
        if p.field:
            assert p.where == f"field `{p.field}`"
        d = p.to_dict()
        assert d["fix"]["options"] and d["text"] == p.render()
        check_doc(p)


def only(make_vault, case_id):
    c = next(c for c in CASES if c[0] == case_id)
    (p,) = problems_of(make_vault, c[2], c[3], c[1])
    return p


def test_command_branches_are_runnable_argv(make_vault):
    p = only(make_vault, "required-status")
    cmd = p.fix_data.options[0].command
    assert cmd.argv == ("set-status", "safe-handling", "draft")
    assert cmd.repl == 'scat_kg.set_status("safe-handling", "draft")'
    assert only(make_vault, "index-no-markers").fix_data.options[0].command.argv == ("index",)


def test_edit_branches_carry_the_value_to_write(make_vault):
    e = only(make_vault, "required-title").fix_data.options[0].edits[0]
    assert (e.action, e.file, e.field, e.value) == ("set-field", C, "title", "Safe handling")
    e = only(make_vault, "required-link").fix_data.options[0].edits[0]
    assert e.value == "[[<one concern page you choose>]]"
    assert e.author_slot == "<one concern page you choose>"
    e = only(make_vault, "cap").fix_data.options[1].edits[0]
    assert (e.file, e.field, e.value) == ("scat.toml", "stakeholder_group_cap", 4)
    e = only(make_vault, "cap-config-bad").fix_data.options[0].edits[0]
    assert e.author_slot == "<number you choose>"
    e = only(make_vault, "name-rename").fix_data.options[0].edits[0]
    assert (e.action, e.file, e.to) == ("rename-file", "concern/Bad Name.md", "concern/bad-name.md")


def test_manual_branches_carry_no_command_or_edit(make_vault):
    for case_id in ("parse", "shape-mapping", "name-by-hand"):
        (o,) = only(make_vault, case_id).fix_data.options
        assert o.kind == "manual" and o.command is None and not o.edits
    o = only(make_vault, "cap").fix_data.options[0]
    assert o.kind == "manual"
