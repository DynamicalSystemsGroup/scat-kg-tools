"""WP11-U6: the fixes of the completeness and graph rules are typed data that match their text.

Each case seeds one defect (the fixture vault of tests/checks/helpers.py), checks it, and asserts for every
problem of the named rule: the fix is data (not the legacy wrapper), its kind is the catalogue's, `field` is
set exactly when `where` names a field, the `to_dict()` validates against the schema, every command and edit
value appears in the rendered text, and every command runs on a copy (exact, not a step) or is accepted by
`scat`'s parser (a slot, or a step).

Rule to case (each distinct fix branch):
  SCAT-DONE-FIELD   done-text, done-relation, done-class, done-empty-replaced, done-timeframe-{scenario,architecture},
                    done-timeframe-empty
  SCAT-DRAFT-FIELD  draft-text, draft-timeframe-{scenario,architecture}, stub-timeframe
  SCAT-DONE-LINK    done-link-suggested, done-link-none, done-link-replace, done-link-capped
  SCAT-DRAFT-LINK   draft-link-suggested, draft-link-none
  SCAT-CONFLICT-SELF conflict-self, conflict-self-and-other
  SCAT-REL-DUPLICATE dup-no-notes, dup-add, dup-join, dup-replace-empty
  SCAT-MENTION      mention-title, mention-name
  SCAT-RAW-BACKLINK backlink-absent, backlink-block, backlink-empty-list, backlink-flow
  SCAT-RAW-UNCODED  uncoded-absent, uncoded-empty-list, uncoded-architecture
"""

import importlib.util
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from scat_kg.checks import check_vault
from scat_kg.cli import _parser

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import scat_harness

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
SC = H.SC
RAWP = "scenario-raw/desk-day.md"
ARCH = "architecture-raw/kiosk-pitch.md"
COPY = "heldby/more/zzz-copy.md"


def raw_page(extra="", **kw):
    return H.doc("scenario-raw", "Desk day", extra="timeframe: past\n" + extra, **kw)


def copy_page(notes=None):
    extra = 'group: "[[staff]]"\nconcern: "[[safe-handling]]"' + (
        f'\nnotes: "{notes}"' if notes else ""
    )
    return H.doc("heldby", "Z", extra=extra)


def uncoded_files(raw_extra=""):
    return {
        RAWP: raw_page(raw_extra),
        "scenario-raw/other-raw.md": H.doc(
            "scenario-raw",
            "Other raw",
            extra="timeframe: past\n" + H.links("coded", "desk-day-coded"),
        ),
        SC: H.coded(raw=H.links("raw", "other-raw")),
    }


def timeframe(kind, line, status="done"):
    coded = "desk-day-coded" if "scenario" in kind else "kiosk-pitch-coded"
    return H.doc(kind, "T", status=status, extra=line + H.links("coded", coded))


def class_without_description(make_vault):
    page = H.doc("class", "Concerns", status=None, description=None, extra="indexes: concern")
    return {"class/concerns.md": page + H.region_for(make_vault, "concerns")}


MANY = {f"concern/c{i}.md": H.doc("concern", f"C{i}") for i in range(10)} | {
    f"heldby/staff-holds-c{i}.md": H.doc(
        "heldby", f"H{i}", extra=f'group: "[[staff]]"\nconcern: "[[c{i}]]"'
    )
    for i in range(10)
}
HELDBY_EXTRA = 'group: "[[staff]]"\nconcern: "[[safe-handling]]"'
KEPT_NOTES = H.doc("heldby", "H", extra=HELDBY_EXTRA + '\nnotes: "kept"')
KEPT_EMPTY = H.doc("heldby", "H", extra=HELDBY_EXTRA + '\nnotes: ""')

# (case id, rule, files: a dict, or a function of make_vault)
CASES = [
    ("done-text", "SCAT-DONE-FIELD", {C: H.doc("concern", "S", description=None)}),
    (
        "done-relation",
        "SCAT-DONE-FIELD",
        {HELDBY: H.doc("heldby", "H", description=None, extra=HELDBY_EXTRA)},
    ),
    ("done-class", "SCAT-DONE-FIELD", class_without_description),
    (
        "done-empty-replaced",
        "SCAT-DONE-FIELD",
        {C: '---\ntype: concern\nstatus: done\ntitle: "S"\ndescription: ""\n---\n'},
    ),
    ("done-timeframe-scenario", "SCAT-DONE-FIELD", {RAWP: timeframe("scenario-raw", "")}),
    ("done-timeframe-architecture", "SCAT-DONE-FIELD", {ARCH: timeframe("architecture-raw", "")}),
    (
        "done-timeframe-empty",
        "SCAT-DONE-FIELD",
        {RAWP: timeframe("scenario-raw", "timeframe:\n")},
    ),
    (
        "draft-text",
        "SCAT-DRAFT-FIELD",
        {C: H.doc("concern", "S", status="draft", description=None)},
    ),
    (
        "draft-timeframe-scenario",
        "SCAT-DRAFT-FIELD",
        {RAWP: timeframe("scenario-raw", "", "draft")},
    ),
    (
        "draft-timeframe-architecture",
        "SCAT-DRAFT-FIELD",
        {ARCH: timeframe("architecture-raw", "timeframe:\n", "draft")},
    ),
    (
        "stub-timeframe",
        "SCAT-DRAFT-FIELD",
        {RAWP: timeframe("scenario-raw", "timeframe:\n", "stub")},
    ),
    ("done-link-suggested", "SCAT-DONE-LINK", {SC: H.coded(groups="")}),
    ("done-link-none", "SCAT-DONE-LINK", {SC: H.coded(affordances="")}),
    ("done-link-replace", "SCAT-DONE-LINK", {SC: H.coded(concerns="concerns: []\n")}),
    ("done-link-capped", "SCAT-DONE-LINK", MANY | {SC: H.coded(concerns="")}),
    ("draft-link-suggested", "SCAT-DRAFT-LINK", {SC: H.coded(status="draft", groups="")}),
    ("draft-link-none", "SCAT-DRAFT-LINK", {SC: H.coded(status="draft", affordances="")}),
    (
        "conflict-self",
        "SCAT-CONFLICT-SELF",
        {C: H.doc("concern", "S", extra=H.links("conflicts", "safe-handling"))},
    ),
    (
        "conflict-self-and-other",
        "SCAT-CONFLICT-SELF",
        {
            "concern/quick-checkout.md": H.doc(
                "concern", "Q", extra=H.links("conflicts", "quick-checkout", "careful-keeping")
            )
        },
    ),
    ("dup-no-notes", "SCAT-REL-DUPLICATE", {COPY: copy_page()}),
    ("dup-add", "SCAT-REL-DUPLICATE", {COPY: copy_page("my account")}),
    ("dup-join", "SCAT-REL-DUPLICATE", {HELDBY: KEPT_NOTES, COPY: copy_page("my account")}),
    (
        "dup-replace-empty",
        "SCAT-REL-DUPLICATE",
        {HELDBY: KEPT_EMPTY, COPY: copy_page("my account")},
    ),
    (
        "mention-title",
        "SCAT-MENTION",
        {SC: H.coded(body="First line.\n  We talked about quick checkout today.\n")},
    ),
    ("mention-name", "SCAT-MENTION", {SC: H.coded(body="the quick-checkout idea\n")}),
    ("backlink-absent", "SCAT-RAW-BACKLINK", {RAWP: raw_page()}),
    (
        "backlink-block",
        "SCAT-RAW-BACKLINK",
        {
            RAWP: raw_page(H.links("coded", "other")),
            "scenario-coded/other.md": H.coded(raw=H.links("raw", "desk-day")),
        },
    ),
    ("backlink-empty-list", "SCAT-RAW-BACKLINK", {RAWP: raw_page("coded: []\n")}),
    (
        "backlink-flow",
        "SCAT-RAW-BACKLINK",
        {
            RAWP: raw_page('coded: ["[[other]]"]\n'),
            "scenario-coded/other.md": H.coded(raw=H.links("raw", "desk-day")),
        },
    ),
    ("uncoded-absent", "SCAT-RAW-UNCODED", uncoded_files()),
    ("uncoded-empty-list", "SCAT-RAW-UNCODED", uncoded_files("coded: []\n")),
    (
        "uncoded-architecture",
        "SCAT-RAW-UNCODED",
        {
            ARCH: H.doc("architecture-raw", "Kiosk pitch", extra="timeframe: future\n"),
            "architecture-raw/other.md": H.doc(
                "architecture-raw",
                "Other",
                extra="timeframe: future\n" + H.links("coded", "kiosk-pitch-coded"),
            ),
            H.AC: H.doc(
                "architecture-coded",
                "K",
                extra=H.links("raw", "other")
                + H.links("concerns", "quick-checkout")
                + H.links("affordances", "self-checkout")
                + H.links("technologies", "booking-app"),
            ),
        },
    ),
]


def problems_of(make_vault, case_id):
    """The problems of the case's rule, from a vault in a directory of its own (a test may seed several)."""
    _, rule, files = next(c for c in CASES if c[0] == case_id)
    fresh = Path(tempfile.mkdtemp(dir=make_vault({}).parent))

    def make_vault(files, root=fresh):
        for rel, content in files.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(content, encoding="utf-8")
        return root

    v = H.vault(make_vault, files(make_vault) if callable(files) else files)
    return [p for p in check_vault(v).problems if p.rule == rule], v.root


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
        assert opt.command.repl in text
        _parser().parse_args(list(opt.command.argv))  # scat accepts the command line
        if opt.command.author_slot:
            assert opt.command.author_slot in text
    for e in opt.edits:
        if e.action == "set-field":
            items = e.value if isinstance(e.value, list) else [e.value]
            if e.field == "conflicts":
                items = []  # the text names the line to delete; the value is what remains
            elif e.field == "coded" and not e.author_slot:
                items = items[-1:]  # the text names only the line to add
            for item in items:
                item = item[2:-2] if item.startswith("[[") else item
                for part in item.split(e.author_slot) if e.author_slot else [item]:
                    assert part in text, (part, text)
            if e.author_slot:
                assert e.author_slot in text
        if e.action == "replace-text":
            assert e.find in text and e.replace in text
        if e.action == "delete-file":
            assert e.file in text


@pytest.mark.parametrize("case", CASES, ids=[c[0] for c in CASES])
def test_the_fix_is_typed_data_that_matches_its_text(make_vault, case, tmp_path):
    case_id, rule, _ = case
    found, root = problems_of(make_vault, case_id)
    assert found, f"the seed gave no {rule}"
    for p in found:
        fix = p.fix_data
        assert fix.verbatim is None
        assert fix.kind == CATALOGUE_KIND[rule]
        if fix.kind == "options":
            assert len(fix.options) >= 2
        assert fix.sequence == (rule in ("SCAT-REL-DUPLICATE", "SCAT-RAW-UNCODED"))
        for i, o in enumerate(fix.options):
            assert o.kind != "manual" or (o.command is None and not o.edits)
            if o.kind == "exact":
                assert o.command or o.edits
            if o.kind == "slot":
                assert o.command.author_slot if o.command else any(e.author_slot for e in o.edits)
            assert_matches_text(o, p.fix)
            if o.command is not None:  # run on a copy when exact and not a step, else parsed
                copy = tmp_path / f"copy{i}"
                shutil.copytree(root, copy)
                scat_harness.assert_option_works(p, i, copy)
        assert (p.field is not None) == p.where.startswith("field `")
        if p.field:
            assert p.where == f"field `{p.field}`"
        d = p.to_dict()
        assert d["fix"]["options"] and d["text"] == p.render()
        check_doc(p)


def only(make_vault, case_id):
    found, _ = problems_of(make_vault, case_id)
    (p,) = found
    return p


def edit_of(make_vault, case_id, option=0):
    return only(make_vault, case_id).fix_data.options[option].edits[0]


def test_text_field_fix_is_a_slot_edit_and_the_done_fix_adds_set_status(make_vault):
    p = only(make_vault, "done-text")
    put, later = p.fix_data.options
    assert put.kind == "slot"
    e = put.edits[0]
    assert (e.action, e.file, e.field) == ("set-field", C, "description")
    assert (e.value, e.author_slot) == ("<one sentence you write>",) * 2
    assert later.kind == "exact" and later.command.argv == ("set-status", "safe-handling", "draft")
    assert p.field == "description"
    assert [o.kind for o in only(make_vault, "done-class").fix_data.options] == ["slot"]
    assert [o.kind for o in only(make_vault, "draft-text").fix_data.options] == ["slot"]


@pytest.mark.parametrize("case_id", ["done-timeframe-scenario", "draft-timeframe-architecture"])
def test_value_set_fix_has_one_exact_option_per_value(make_vault, case_id):
    p = only(make_vault, case_id)
    picks = [o for o in p.fix_data.options if not o.command]
    assert [o.edits[0].value for o in picks] == ["past", "future", "mixed"]
    assert all(o.kind == "exact" and o.edits[0].author_slot is None for o in picks)
    assert (p.fix_data.options[-1].command is not None) == case_id.startswith("done")


def test_link_fix_writes_the_whole_list(make_vault):
    e = edit_of(make_vault, "done-link-suggested")
    assert (e.field, e.value, e.author_slot) == ("groups", ["[[staff]]"], None)
    assert only(make_vault, "done-link-suggested").fix_data.options[0].kind == "exact"
    e = edit_of(make_vault, "done-link-none")
    assert e.value == ["[[<one affordance page you choose>]]"]
    assert e.author_slot == "<one affordance page you choose>"
    assert only(make_vault, "done-link-none").fix_data.options[0].kind == "slot"
    assert (
        len(edit_of(make_vault, "done-link-capped").value) == 8
    )  # the 8 shown; "(+3 more)" is text
    assert [o.kind for o in only(make_vault, "draft-link-none").fix_data.options] == ["slot"]


def test_conflict_self_writes_the_list_without_the_self_link(make_vault):
    assert edit_of(make_vault, "conflict-self").value == []
    e = edit_of(make_vault, "conflict-self-and-other")
    assert (e.field, e.value) == ("conflicts", ["[[careful-keeping]]"])


def test_duplicate_steps(make_vault):
    first, second = only(make_vault, "dup-join").fix_data.options
    assert first.edits[0].action == "set-field" and first.edits[0].file == HELDBY
    assert (first.edits[0].field, first.edits[0].value) == ("notes", "kept my account")
    assert edit_of(make_vault, "dup-add").value == "my account"
    assert edit_of(make_vault, "dup-replace-empty").value == "my account"
    adv = only(make_vault, "dup-no-notes").fix_data.options[0]
    assert adv.kind == "advisory" and adv.command is None and not adv.edits
    assert second.edits[0].action == "delete-file" and second.edits[0].file == COPY
    assert second.command.argv == ("index",)


def test_mention_replaces_text_at_the_place(make_vault):
    p = only(make_vault, "mention-title")
    e = p.fix_data.options[0].edits[0]
    assert (e.action, e.file, e.line, e.column) == ("replace-text", SC, p.line, p.column)
    assert (e.find, e.replace) == ("quick checkout", "[[quick-checkout|quick checkout]]")
    assert edit_of(make_vault, "mention-name").replace == "[[quick-checkout]]"
    assert p.field is None


def test_backlink_writes_the_whole_coded_list(make_vault):
    assert edit_of(make_vault, "backlink-absent").value == ["[[desk-day-coded]]"]
    assert edit_of(make_vault, "backlink-block").value == ["[[other]]", "[[desk-day-coded]]"]
    assert edit_of(make_vault, "backlink-empty-list").value == ["[[desk-day-coded]]"]
    assert edit_of(make_vault, "backlink-flow").value == ["[[other]]", "[[desk-day-coded]]"]


def test_uncoded_steps_are_slots(make_vault):
    for case_id, key in (
        ("uncoded-absent", "scenario-coded"),
        ("uncoded-empty-list", "scenario-coded"),
        ("uncoded-architecture", "architecture-coded"),
    ):
        p = only(make_vault, case_id)
        first, second = p.fix_data.options
        assert p.fix_data.sequence and p.fix_data.kind == "slot"
        e = first.edits[0]
        assert (e.field, e.value, e.author_slot) == (
            "coded",
            ["[[<coded-page-name>]]"],
            "<coded-page-name>",
        )
        assert second.command.argv == ("stub", "<coded-page-name>", "--type", key)
        assert second.command.author_slot == "<coded-page-name>"
        assert p.field == "coded"
