"""WP11-U7: the fixes of the link and dangling rules are typed data that match their text and work.

Each case seeds one defect (the fixture vault of tests/checks/helpers.py) and checks it. For every problem of the
named rule: the fix is data (not the legacy wrapper), its kind is the catalogue's (a one-option fix takes its
option's kind), `field` is set exactly when `where` names one field, the `to_dict()` validates against the schema,
and every command and edit value appears in the rendered text. Then every exact option is applied to a copy of
the vault (its edits by the small applier below, then its command) and the problem it names is gone; a slot
option's command line is accepted by `scat`'s parser.
"""

import contextlib
import importlib.util
import io
import json
import re
import shutil
import tempfile
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from scat_kg import cli
from scat_kg.checks import check_vault
from scat_kg.vault import read_vault

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

SC, AC, HELDBY, ATTR = H.SC, H.AC, H.HELDBY, H.ATTR
SHAPE, UNLISTED, ENDPOINT = "SCAT-LINK-SHAPE", "SCAT-LINK-UNLISTED", "SCAT-LINK-ENDPOINT"
DISC, DISC_BODY = "SCAT-LINK-DISCOURAGED", "SCAT-LINK-DISCOURAGED-BODY"
DANG, DANG_BODY = "SCAT-LINK-DANGLING", "SCAT-LINK-DANGLING-BODY"
coded, doc, links = H.coded, H.doc, H.links


def aff(target):
    return coded(affordances=links("affordances", "self-checkout", target))


def many_offers():
    """Ten affordances attributed to booking-app: more than the eight a fix lists."""
    files = {}
    for i in range(10):
        files[f"affordance/a{i}.md"] = doc("affordance", f"A{i}")
        files[f"attributes/a{i}-attr.md"] = doc(
            "attributes",
            f"A{i} attr",
            extra=f'affordance: "[[a{i}]]"\ntechnology: "[[booking-app]]"',
        )
    return files


def arch(**override):
    parts = {
        "raw": links("raw", "kiosk-pitch"),
        "concerns": links("concerns", "quick-checkout"),
        "affordances": links("affordances", "self-checkout"),
        "technologies": links("technologies", "booking-app"),
        "groups": "",
    }
    parts.update(override)
    return doc("architecture-coded", "K", extra="".join(parts.values()))


SHARING = {
    f"addresses/a{i}.md": doc(
        "addresses", f"A{i}", extra=f'concern: "[[c{i}]]"\naffordance: "[[self-checkout]]"'
    )
    for i in range(7)
} | {f"concern/c{i}.md": doc("concern", f"C{i}") for i in range(7)}

# (case id, rule, files, rule's problems expected)
CASES = [
    ("shape-scalar", SHAPE, {SC: coded(concerns='concerns: "[[safe-handling]]"\n')}),
    ("shape-nested-list", SHAPE, {SC: coded(concerns="concerns: [[safe-handling]]\n")}),
    ("shape-alias-item", SHAPE, {SC: coded(concerns='concerns:\n  - "[[safe-handling|x]]"\n')}),
    ("shape-number-item", SHAPE, {SC: coded(concerns="concerns:\n  - 5\n")}),
    ("shape-list-mapping", SHAPE, {SC: coded(concerns="concerns:\n  a: b\n")}),
    (
        "shape-single-one-item-list",
        SHAPE,
        {HELDBY: doc("heldby", "H", extra='group:\n  - "[[staff]]"\nconcern: "[[safe-handling]]"')},
    ),
    (
        "shape-single-two-item-list",
        SHAPE,
        {
            HELDBY: doc(
                "heldby",
                "H",
                extra='group:\n  - "[[staff]]"\n  - "[[borrowers]]"\nconcern: "[[safe-handling]]"',
            )
        },
    ),
    (
        "shape-single-two-items-one-unreadable",
        SHAPE,
        {
            HELDBY: doc(
                "heldby",
                "H",
                extra='group:\n  - "[[staff]]"\n  - 5\nconcern: "[[safe-handling]]"',
            )
        },
    ),
    (
        "shape-single-mapping",
        SHAPE,
        {HELDBY: doc("heldby", "H", extra='group:\n  a: b\nconcern: "[[safe-handling]]"')},
    ),
    (
        "shape-single-unquoted-pair",
        SHAPE,
        {HELDBY: doc("heldby", "H", extra='group: staff\nconcern: "[[safe-handling]]"')},
    ),
    (
        "unlisted-groups-on-concern",
        UNLISTED,
        {"concern/quick-checkout.md": doc("concern", "Q", extra=links("groups", "staff"))},
    ),
    ("unlisted-concern-on-scenario", UNLISTED, {SC: coded(extra='concern: "[[safe-handling]]"\n')}),
    (
        "endpoint-move-into-block",
        ENDPOINT,
        {SC: coded(concerns=links("concerns", "safe-handling", "briefing"))},
    ),
    (
        "endpoint-move-into-missing-key-flow",
        ENDPOINT,
        {SC: coded(concerns='concerns: ["[[safe-handling]]", "[[briefing]]"]\n', affordances="")},
    ),
    (
        "endpoint-move-into-empty-list",
        ENDPOINT,
        {
            SC: coded(
                concerns=links("concerns", "safe-handling", "briefing"),
                affordances="affordances: []\n",
            )
        },
    ),
    (
        "endpoint-two-tiers-then-delete",
        ENDPOINT,
        {
            SC: coded(
                concerns=links("concerns", "safe-handling", "self-checkout"),
                body="See [[careful-keeping]].\n",
            )
        },
    ),
    (
        "endpoint-more-than-five",
        ENDPOINT,
        SHARING | {SC: coded(concerns=links("concerns", "safe-handling", "self-checkout"))},
    ),
    (
        "endpoint-relation-replaced",
        ENDPOINT,
        {
            ATTR: doc(
                "attributes",
                "A",
                extra='affordance: "[[booking-app]]"\ntechnology: "[[booking-app]]"',
            ),
            "attributes/briefing-attributed-to-booking-app.md": doc(
                "attributes",
                "B",
                extra='affordance: "[[briefing]]"\ntechnology: "[[booking-app]]"',
            ),
        },
    ),
    (
        "endpoint-relation-by-hand",
        ENDPOINT,
        {
            ATTR: doc(
                "attributes",
                "A",
                extra='affordance: "[[booking-app]]"\ntechnology: "[[booking-app]]"',
            )
        },
    ),
    (
        "endpoint-swap",
        ENDPOINT,
        {HELDBY: doc("heldby", "H", extra='group: "[[safe-handling]]"\nconcern: "[[staff]]"')},
    ),
    (
        "endpoint-swap-order-in-file",
        ENDPOINT,
        {HELDBY: doc("heldby", "H", extra='concern: "[[staff]]"\ngroup: "[[safe-handling]]"')},
    ),
    (
        "endpoint-no-candidates-only-delete",
        ENDPOINT,
        {SC: coded(raw=links("raw", "desk-day", "kiosk-pitch"))},
    ),
    (
        "endpoint-done-page-only-good-item-no-candidate",
        ENDPOINT,
        {SC: coded(concerns=links("concerns", "briefing"))},
    ),
    (
        "endpoint-done-page-only-good-item-with-candidate",
        ENDPOINT,
        SHARING | {SC: coded(concerns=links("concerns", "self-checkout"))},
    ),
    (
        "discouraged-technologies-suggestion",
        DISC,
        {
            SC: coded(
                affordances=links("affordances", "briefing"),
                extra=links("technologies", "booking-app"),
            )
        },
    ),
    (
        "discouraged-technologies-none",
        DISC,
        {SC: coded(extra=links("technologies", "booking-app"))},
    ),
    (
        "discouraged-groups-suggestion",
        DISC,
        {AC: arch(groups=links("groups", "staff"))},
    ),
    ("discouraged-groups-none", DISC, {AC: arch(groups=links("groups", "borrowers"))}),
    (
        "discouraged-technologies-capped",
        DISC,
        many_offers() | {SC: coded(extra=links("technologies", "booking-app"))},
    ),
    (
        "discouraged-body-offered",
        DISC_BODY,
        {SC: coded(body="It runs on [[booking-app]].\n")},
    ),
    (
        "discouraged-body-group-in-architecture",
        DISC_BODY,
        {
            AC: doc(
                "architecture-coded",
                "K",
                extra=arch().split("---\n")[1],
                body="Staff like [[staff]].\n",
            )
        },
    ),
    (
        "discouraged-body-capped",
        DISC_BODY,
        many_offers() | {SC: coded(body="It runs on [[booking-app]].\n")},
    ),
    (
        "discouraged-body-none-offered",
        DISC_BODY,
        {SC: coded(body="Staff like [[borrowers]].\n")}
        | {
            AC: doc(
                "architecture-coded",
                "K",
                extra=arch().split("---\n")[1],
                body="Stakeholders: [[borrowers]].\n",
            )
        },
    ),
    (
        "dangling-near-and-stub",
        DANG,
        {
            "affordance/safety-briefing.md": doc("affordance", "Safety briefing"),
            SC: aff("safety-briefings"),
        },
    ),
    ("dangling-stub-only", DANG, {SC: aff("zzzzzz")}),
    (
        "dangling-wrong-case",
        DANG,
        {
            "affordance/safety-briefing.md": doc("affordance", "Safety briefing"),
            SC: aff("Safety-Briefing"),
        },
    ),
    ("dangling-illegal-replace-then-stub", DANG, {SC: aff("Safety briefing")}),
    ("dangling-derived-is-another-type", DANG, {SC: aff("Quick-Checkout")}),
    ("dangling-non-latin-by-hand", DANG, {SC: aff("Привет")}),
    ("dangling-typeless-no-frontmatter", DANG, {SC: aff("notes"), "notes.md": "just words\n"}),
    (
        "dangling-typeless-some-keys",
        DANG,
        {SC: aff("notes"), "notes.md": "---\nauthor: me\ntitle:\n---\nwords\n"},
    ),
    (
        "dangling-group-at-cap",
        DANG,
        {
            "stakeholder-group/third.md": doc("stakeholder-group", "Third"),
            SC: coded(groups=links("groups", "staff", "funders")),
        },
    ),
    ("dangling-group-stub", DANG, {SC: coded(groups=links("groups", "staff", "funders"))}),
    (
        "dangling-single-field",
        DANG,
        {HELDBY: doc("heldby", "H", extra='group: "[[funders]]"\nconcern: "[[safe-handling]]"')},
    ),
    (
        "dangling-single-field-near",
        DANG,
        {HELDBY: doc("heldby", "H", extra='group: "[[staf]]"\nconcern: "[[safe-handling]]"')},
    ),
    ("dangling-illegal-next-to-typeless", DANG, {SC: aff("Notes"), "Notes.md": "words\n"}),
    (
        "dangling-illegal-derived-is-typeless",
        DANG,
        {SC: aff("Notes"), "notes.md": "words\n"},
    ),
    (
        "dangling-body-one-type",
        DANG_BODY,
        {
            "concern/careful-keeping.md": doc(
                "concern", "C", extra=links("conflicts", "ghost-concern")
            ),
            SC: coded(body="See [[ghost-concern]].\n"),
        },
    ),
    ("dangling-body-class-types", DANG_BODY, {SC: coded(body="See [[nothing-here]].\n")}),
    ("dangling-body-near-match", DANG_BODY, {SC: coded(body="See [[quick-chekout]].\n")}),
    (
        "dangling-body-illegal-replace-then-stub",
        DANG_BODY,
        {SC: coded(body="See [[Safety briefing]].\n")},
    ),
    (
        "dangling-body-illegal-derived-is-a-page",
        DANG_BODY,
        {
            "affordance/safety-briefing.md": doc("affordance", "Safety briefing"),
            SC: coded(body="See [[Safety-Briefing]].\n"),
        },
    ),
    ("dangling-body-non-latin-by-hand", DANG_BODY, {SC: coded(body="See [[Привет]].\n")}),
    (
        "dangling-body-group-at-cap",
        DANG_BODY,
        {
            "stakeholder-group/third.md": doc("stakeholder-group", "Third"),
            SC: coded(body="See [[nothing-here]].\n"),
        },
    ),
    (
        "dangling-body-typeless",
        DANG_BODY,
        {SC: coded(body="See [[notes]].\n"), "notes.md": "words\n"},
    ),
    (
        "dangling-body-twice-on-a-line",
        DANG_BODY,
        {SC: coded(body="See [[ghost]] and [[ghost]].\n")},
    ),
    (
        "discouraged-body-alias",
        DISC_BODY,
        {SC: coded(body="It runs on [[booking-app|the app]].\n")},
    ),
    (
        "dangling-body-alias",
        DANG_BODY,
        {SC: coded(body="See [[ghost|spooky]] now.\n")},
    ),
    ("dangling-body-heading", DANG_BODY, {SC: coded(body="See [[ghost#Part]] now.\n")}),
    ("dangling-body-anchor", DANG_BODY, {SC: coded(body="See [[ghost^abc123]] now.\n")}),
    (
        "dangling-body-alias-twice-on-a-line",
        DANG_BODY,
        {SC: coded(body="See [[ghost|a]] and [[ghost|a]].\n")},
    ),
    (
        "dangling-body-two-spellings-on-a-line",
        DANG_BODY,
        {SC: coded(body="See [[ghost]] and [[ghost|g]].\n")},
    ),
    (
        "dangling-body-illegal-with-alias",
        DANG_BODY,
        {SC: coded(body="See [[Safety briefing|sb]].\n")},
    ),
]
IDS = [c[0] for c in CASES]


_SEEDS = tempfile.TemporaryDirectory(prefix="scat-u7-")  # removed when the interpreter exits


def seed(make_vault, case):
    """Check the case in a vault of its own (make_vault's directory is shared inside one test)."""
    _, rule, files = case
    root = Path(tempfile.mkdtemp(dir=_SEEDS.name))

    def fresh(extra):
        for rel, content in extra.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(content, encoding="utf-8")
        return root

    v = H.vault(fresh, files)
    return v, [p for p in check_vault(v).problems if p.rule == rule]


# the applier: the edits of the contract, on a copy of the vault


def _render(key, value):
    if isinstance(value, list):
        return [f"{key}:", *[f'  - "{x}"' for x in value]]
    if isinstance(value, int):
        return [f"{key}: {value}"]
    return [f'{key}: "{value}"']


def _span(lines, key):
    """First and one-past-last index of `key`'s lines inside the front matter, or None."""
    close = next((i for i in range(1, len(lines)) if lines[i] == "---"), len(lines))
    for i in range(1, close):
        if re.match(rf"^{re.escape(key)}:", lines[i]):
            j = i + 1
            while j < close and re.match(r"^(\s|-)", lines[j]):
                j += 1
            return i, j, close
    return None, None, close


def apply_edit(root, e):
    path = root / e["file"]
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    if e["action"] == "replace-text":
        n = e["line"] - 1
        assert e["find"] in lines[n], (e, lines[n])
        if e.get("column"):  # one place: the literal must stand exactly there
            c = e["column"] - 1
            assert lines[n][c : c + len(e["find"])] == e["find"], (e, lines[n])
            lines[n] = lines[n][:c] + e["replace"] + lines[n][c + len(e["find"]) :]
        else:  # no column: every occurrence on the line (one message stands for a repeated link, `repeat`)
            lines[n] = lines[n].replace(e["find"], e["replace"])
    else:
        if lines[0] != "---":
            lines = ["---", "---", *lines]
        i, j, close = _span(lines, e["field"])
        if e["action"] == "delete-field":
            del lines[i:j]
        else:
            new = _render(e["field"], e["value"])
            if i is None:
                lines[close:close] = new
            else:
                lines[i:j] = new
    path.write_text("\n".join(lines), encoding="utf-8")


def run_command(root, argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        code = cli.main([*argv, "--root", str(root)])
    assert code == 0, out.getvalue()


def parses(argv, root):
    cli._parser().parse_args([*argv, "--root", str(root)])


def left_of(root, p):
    return [
        q
        for q in check_vault(read_vault(root)).problems
        if (q.rule, q.file, q.where, q.what) == (p.rule, p.file, p.where, p.what)
    ]


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
    for e in opt.edits:
        if e.action == "replace-text":
            # the text names the link as `[[target]]`; `find` is the literal written (alias, heading, anchor)
            assert re.split(r"[|#^\]]", e.find[2:], maxsplit=1)[0] in text and e.replace in text
        if e.action == "delete-field":
            assert f"`{e.field}:`" in text
        if e.action != "set-field" or e.value is None:
            continue
        items = e.value if isinstance(e.value, list) else [e.value]
        # a list that is written back whole shows only the lines that change, so one item must show
        shown = [i for i in items if all(part in text for part in _parts(i, e.author_slot))]
        if isinstance(e.value, list):
            assert shown or opt.text.startswith(("move", "delete the item")), (e.value, text)
        else:
            assert shown, (e.value, text)
        if e.author_slot:
            assert e.author_slot in text


def _parts(item, slot):
    return [p for p in item.split(slot)] if slot and slot in item else [item]


@pytest.mark.parametrize("case", CASES, ids=IDS)
def test_the_fix_is_typed_data_that_matches_its_text(make_vault, case):
    _, rule, _ = case
    _, found = seed(make_vault, case)
    assert found, f"the seed gave no {rule}"
    for p in found:
        fix = p.fix_data
        assert fix.verbatim is None
        if len(fix.options) == 1:
            assert fix.kind == fix.options[0].kind
            assert fix.kind in (CATALOGUE_KIND[rule], "exact", "manual", "slot")
        else:
            assert fix.kind == "options"
            # the catalogue calls SHAPE exact; its one choice (a single field holding several items) is options
            assert CATALOGUE_KIND[rule] == "options" or rule == SHAPE
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


KEEP_THE_POINT = "keep the point by linking"


@pytest.mark.parametrize("case", CASES, ids=IDS)
def test_every_option_works_on_a_copy(make_vault, tmp_path_factory, case):
    v, found = seed(make_vault, case)
    for n, p in enumerate(found):
        for i, o in enumerate(p.fix_data.options):
            if o.kind == "manual":
                continue
            copy = tmp_path_factory.mktemp(f"copy{n}-{i}") / "vault"
            shutil.copytree(v.root, copy)
            if o.kind == "slot":
                if o.command:
                    parses(o.command.argv, copy)
                continue
            for e in o.edits:
                apply_edit(copy, e.to_dict() if hasattr(e, "to_dict") else e)
            if o.command:
                run_command(copy, o.command.argv)
            if o.text.startswith(KEEP_THE_POINT):
                # it adds the suggestions; the warning stays until the field is deleted (as its text says)
                assert left_of(copy, p)
                (e,) = o.edits
                assert read_vault(copy).by_name[Path(p.file).stem][0].fields[e.field]
            else:
                assert not left_of(copy, p), (p.rule, i + 1, o.text)


# data of the branches


def only(make_vault, case_id):
    case = next(c for c in CASES if c[0] == case_id)
    _, found = seed(make_vault, case)
    assert len(found) == 1, [p.what for p in found]
    return found[0].fix_data


def edit_dicts(opt):
    return [e.to_dict() for e in opt.edits]


def test_shape_branches(make_vault):
    (o,) = only(make_vault, "shape-scalar").options
    assert (o.kind, edit_dicts(o)) == (
        "exact",
        [{"action": "set-field", "file": SC, "field": "concerns", "value": ["[[safe-handling]]"]}],
    )
    (o,) = only(make_vault, "shape-number-item").options
    assert o.kind == "slot"
    assert edit_dicts(o)[0]["value"] == ["[[<one page you choose>]]"]
    assert edit_dicts(o)[0]["author_slot"] == "<one page you choose>"
    (o,) = only(make_vault, "shape-single-one-item-list").options
    assert edit_dicts(o)[0]["value"] == "[[staff]]" and o.kind == "exact"
    fix = only(make_vault, "shape-single-two-item-list")
    assert [edit_dicts(o)[0]["value"] for o in fix.options] == ["[[staff]]", "[[borrowers]]"]
    assert fix.kind == "options"
    fix = only(make_vault, "shape-single-two-items-one-unreadable")
    assert [o.kind for o in fix.options] == ["exact", "slot"]
    (o,) = only(make_vault, "shape-single-mapping").options
    assert o.kind == "slot" and edit_dicts(o)[0]["value"] == "[[<one page you choose>]]"


def test_unlisted_branch(make_vault):
    (o,) = only(make_vault, "unlisted-groups-on-concern").options
    assert o.kind == "exact"
    assert edit_dicts(o) == [
        {"action": "delete-field", "file": "concern/quick-checkout.md", "field": "groups"}
    ]


def test_endpoint_branches(make_vault):
    fix = only(make_vault, "endpoint-move-into-block")
    move, delete = fix.options
    assert edit_dicts(move) == [
        {"action": "set-field", "file": SC, "field": "concerns", "value": ["[[safe-handling]]"]},
        {
            "action": "set-field",
            "file": SC,
            "field": "affordances",
            "value": ["[[self-checkout]]", "[[briefing]]"],
        },
    ]
    assert edit_dicts(delete) == [
        {"action": "set-field", "file": SC, "field": "concerns", "value": ["[[safe-handling]]"]}
    ]
    assert fix.notes == ("(no existing concern page was found to replace it with)",)
    fix = only(make_vault, "endpoint-two-tiers-then-delete")
    assert [edit_dicts(o)[0]["value"] for o in fix.options[:2]] == [
        ["[[safe-handling]]", "[[quick-checkout]]"],
        ["[[safe-handling]]", "[[careful-keeping]]"],
    ]
    assert fix.options[2].text.startswith("delete the item line")
    fix = only(make_vault, "endpoint-more-than-five")
    assert len(fix.options) == 6 and fix.notes == ("(+3 more not shown)",)
    fix = only(make_vault, "endpoint-relation-replaced")
    (o,) = fix.options
    assert edit_dicts(o) == [
        {"action": "set-field", "file": ATTR, "field": "affordance", "value": "[[briefing]]"}
    ]
    (o,) = only(make_vault, "endpoint-relation-by-hand").options
    assert o.kind == "manual"
    (o,) = only(make_vault, "endpoint-swap").options
    assert [(e["field"], e["value"]) for e in edit_dicts(o)] == [
        ("group", "[[staff]]"),
        ("concern", "[[safe-handling]]"),
    ]
    (o,) = only(make_vault, "endpoint-no-candidates-only-delete").options
    assert edit_dicts(o) == [
        {"action": "set-field", "file": SC, "field": "raw", "value": ["[[desk-day]]"]}
    ]
    (o,) = only(make_vault, "endpoint-done-page-only-good-item-no-candidate").options
    assert o.kind == "manual" and "scat set-status desk-day-coded draft" in o.text
    fix = only(make_vault, "endpoint-done-page-only-good-item-with-candidate")
    assert all(o.kind == "exact" for o in fix.options) and "SCAT-DONE-LINK" in fix.notes[-1]


def test_discouraged_branches(make_vault):
    fix = only(make_vault, "discouraged-technologies-suggestion")
    drop, keep = fix.options
    assert edit_dicts(drop) == [{"action": "delete-field", "file": SC, "field": "technologies"}]
    assert edit_dicts(keep) == [
        {
            "action": "set-field",
            "file": SC,
            "field": "affordances",
            "value": ["[[briefing]]", "[[self-checkout]]"],
        }
    ]
    (o,) = only(make_vault, "discouraged-technologies-none").options
    assert o.kind == "exact"
    fix = only(make_vault, "discouraged-technologies-capped")
    assert len(edit_dicts(fix.options[1])[0]["value"]) == 9 and fix.notes == ("(+2 more)",)
    drop, keep = only(make_vault, "discouraged-body-offered").options
    assert edit_dicts(drop) == [
        {
            "action": "replace-text",
            "file": SC,
            "line": 15,
            "column": 12,
            "find": "[[booking-app]]",
            "replace": "booking-app",
        }
    ]
    assert edit_dicts(keep)[0]["replace"] == "[[self-checkout]]"
    fix = only(make_vault, "discouraged-body-capped")
    assert len(fix.options) == 9 and fix.notes == ("(+3 more)",)
    (o,) = only(make_vault, "discouraged-body-none-offered").options
    assert o.edits[0].replace == "borrowers"


def test_dangling_branches(make_vault):
    near, stub = only(make_vault, "dangling-near-and-stub").options
    assert edit_dicts(near)[0]["value"] == ["[[self-checkout]]", "[[safety-briefing]]"]
    assert stub.command.argv == ("stub", "safety-briefings", "--type", "affordance")
    assert stub.command.repl == 'scat_kg.stub("safety-briefings", type="affordance")'
    (o,) = only(make_vault, "dangling-illegal-replace-then-stub").options
    assert [e["value"] for e in edit_dicts(o)] == [["[[self-checkout]]", "[[safety-briefing]]"]]
    assert o.command.argv == ("stub", "safety-briefing", "--type", "affordance")
    for case_id in (
        "dangling-derived-is-another-type",
        "dangling-non-latin-by-hand",
        "dangling-group-at-cap",
    ):
        (o,) = only(make_vault, case_id).options
        assert o.kind == "manual"
    (o,) = only(make_vault, "dangling-typeless-no-frontmatter").options
    assert [(e["field"], e["value"]) for e in edit_dicts(o)] == [
        ("type", "affordance"),
        ("status", "stub"),
        ("title", "Notes"),
    ]
    (o,) = only(make_vault, "dangling-typeless-some-keys").options
    assert [e["field"] for e in edit_dicts(o)] == ["type", "status", "title"]
    (o,) = only(make_vault, "dangling-single-field").options
    assert o.command.argv == ("stub", "funders", "--type", "stakeholder-group")
    near, _ = only(make_vault, "dangling-single-field-near").options
    assert edit_dicts(near)[0]["value"] == "[[staff]]"
    (o,) = only(make_vault, "dangling-illegal-derived-is-typeless").options
    assert o.command is None and [e["field"] for e in edit_dicts(o)] == ["group"][:0] + [
        "affordances",
        "type",
        "status",
        "title",
    ]


def test_dangling_body_branches(make_vault):
    fix = only(make_vault, "dangling-body-class-types")
    stubs, drop = fix.options[:-1], fix.options[-1]
    assert [o.command.argv[-1] for o in stubs] == ["stakeholder-group", "concern", "affordance"]
    assert drop.edits[0].replace == "nothing-here" and drop.kind == "exact"
    assert len(fix.notes) == 2
    near = only(make_vault, "dangling-body-near-match").options[0]
    assert (near.edits[0].find, near.edits[0].replace) == (
        "[[quick-chekout]]",
        "[[quick-checkout]]",
    )
    fix = only(make_vault, "dangling-body-illegal-replace-then-stub")
    then = fix.options[1]
    assert then.edits[0].replace == "[[safety-briefing]]" and then.command.argv[-1] == "concern"
    fix = only(make_vault, "dangling-body-illegal-derived-is-a-page")
    assert (
        fix.options[0].command is None and fix.options[0].edits[0].replace == "[[safety-briefing]]"
    )
    (o,) = only(make_vault, "dangling-body-non-latin-by-hand").options
    assert o.kind == "exact" and o.edits[0].replace == "Привет"
    fix = only(make_vault, "dangling-body-typeless")
    assert [e["field"] for e in edit_dicts(fix.options[0])] == ["type", "status", "title"]
    _, found = seed(make_vault, next(c for c in CASES if c[0] == "dangling-body-twice-on-a-line"))
    assert found[0].repeat == 2


def test_body_edits_name_the_literal_written_on_the_line(make_vault):
    def edits(case_id):
        return [e for o in only(make_vault, case_id).options for e in o.edits]

    (e, *_) = edits("discouraged-body-alias")
    assert (e.find, e.column) == ("[[booking-app|the app]]", 12) and e.line == 15
    for case_id, literal in (
        ("dangling-body-alias", "[[ghost|spooky]]"),
        ("dangling-body-heading", "[[ghost#Part]]"),
        ("dangling-body-anchor", "[[ghost^abc123]]"),
    ):
        es = edits(case_id)
        assert es and all((e.find, e.column) == (literal, 5) for e in es), case_id
    # the same literal twice: no column, so the edit replaces every occurrence on its line
    for case_id, literal in (
        ("dangling-body-twice-on-a-line", "[[ghost]]"),
        ("dangling-body-alias-twice-on-a-line", "[[ghost|a]]"),
    ):
        es = edits(case_id)
        assert es and all((e.find, e.column) == (literal, None) for e in es), case_id
    es = edits("dangling-body-illegal-with-alias")
    assert es and all(e.find == "[[Safety briefing|sb]]" and e.column == 5 for e in es)
    # two spellings of one target on a line cannot be named by one edit: every option is manual
    fix = only(make_vault, "dangling-body-two-spellings-on-a-line")
    on_line = [o for o in fix.options if o.text.startswith("on line")]
    assert on_line and all(o.kind == "manual" and not o.edits and not o.command for o in on_line)
