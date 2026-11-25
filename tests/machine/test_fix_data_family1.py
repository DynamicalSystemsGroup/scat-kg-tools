"""WP11-U5: the fixes of the front-matter, field, name, mention and vault-wide rules are typed data that match their text.

Each case seeds one defect (the fixture vault of tests/checks/helpers.py), checks it, and holds every problem of the
named rule to the machine interface (see fixcases.verify): the fix is data, its kind is the catalogue's (or a named
deviation), `field` follows `where`, the `to_dict()` validates against the schema, every command and edit value
appears in the text, and the exact options that carry edits clear their problem when the edits are applied.
"""

import fixcases as fc
import helpers as H

C = "concern/safe-handling.md"
K = "concern/careful-keeping.md"
D = H.DESK


def fm(body: str) -> str:
    return f"---\n{body}---\n"


GROUPS = {f"group/g-{n}.md": H.doc("group", f"Group {n}") for n in ("one", "two")}

# (case id, rule, files, removed)
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
        "required-title-empty",
        "SCAT-FM-REQUIRED",
        {C: fm("type: concern\nstatus: stub\ntitle:\n")},
        (),
    ),
    ("type-near", "SCAT-FM-TYPE", {K: H.doc("Concern", "Careful keeping")}, ()),
    ("type-list", "SCAT-FM-TYPE", {K: H.doc("gadget", "Careful keeping")}, ()),
    ("type-empty", "SCAT-FM-TYPE", {K: fm('type:\nstatus: done\ntitle: "S"\n')}, ()),
    ("type-index", "SCAT-FM-TYPE", {K: H.doc("index", "Careful keeping")}, ()),
    ("status-near", "SCAT-FM-STATUS", {C: H.doc("concern", "S", status="Done")}, ()),
    ("status-choice", "SCAT-FM-STATUS", {C: H.doc("concern", "S", status="finished")}, ()),
    ("timeframe-near", "SCAT-FM-TIMEFRAME", {D: H.narrative(timeframe="Past")}, ()),
    ("timeframe-choice", "SCAT-FM-TIMEFRAME", {D: H.narrative(timeframe="soon")}, ()),
    ("kind-near", "SCAT-FM-KIND", {D: H.narrative(kind="Scenario")}, ()),
    ("kind-choice", "SCAT-FM-KIND", {D: H.narrative(kind="story")}, ()),
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
        "name-rename-links",
        "SCAT-NAME",
        {
            "concern/Bad Name.md": H.doc("concern", "Bad name"),
            K: H.doc("concern", "Careful keeping", body="\nSee [[Bad Name|it]].\n"),
        },
        (),
    ),
    (
        "name-duplicate",
        "SCAT-NAME",
        {"affordance/quick-checkout.md": H.doc("affordance", "Quick checkout")},
        (),
    ),
    ("name-by-hand", "SCAT-NAME", {"concern/Привет.md": H.doc("concern", "Привет")}, ()),
    ("done-field-description", "SCAT-DONE-FIELD", {C: H.doc("concern", "S", description=None)}, ()),
    ("done-field-timeframe", "SCAT-DONE-FIELD", {D: H.narrative(timeframe=None)}, ()),
    (
        "draft-field-description",
        "SCAT-DRAFT-FIELD",
        {C: H.doc("concern", "S", status="draft", description=None)},
        (),
    ),
    (
        "draft-field-timeframe",
        "SCAT-DRAFT-FIELD",
        {D: H.narrative(status="stub", timeframe=None)},
        (),
    ),
    (
        "noedges",
        "SCAT-NOEDGES",
        {D: H.narrative(rows=())},
        (),
    ),
    ("cap", "SCAT-CAP", GROUPS, ()),
    ("cap-config-missing", "SCAT-CAP-CONFIG", {}, ("scat.toml",)),
    ("cap-config-toml", "SCAT-CAP-CONFIG", {"scat.toml": "stakeholder_group_cap = \n"}, ()),
    ("cap-config-key", "SCAT-CAP-CONFIG", {"scat.toml": "other = 1\n"}, ()),
    ("cap-config-bad", "SCAT-CAP-CONFIG", {"scat.toml": "stakeholder_group_cap = 0\n"}, ()),
    ("mention", "SCAT-MENTION", {C: H.doc("concern", "S", body="\nNeeds a briefing.\n")}, ()),
    (
        "mention-name",
        "SCAT-MENTION",
        {C: H.doc("concern", "S", body="\nOpen booking-app now.\n")},
        (),
    ),
]


@fc.family(CASES)
def test_the_fix_is_typed_data_that_matches_its_text(make_vault, tmp_path, case):
    _, rule, files, remove = case
    fc.verify(make_vault, tmp_path, rule, files, remove)


def only(make_vault, case_id):
    c = next(c for c in CASES if c[0] == case_id)
    _, found = fc.problems_of(make_vault, c[2], c[3], c[1])
    (p,) = found
    return p


def test_command_branches_are_runnable_argv(make_vault):
    p = only(make_vault, "required-status")
    cmd = p.fix_data.options[0].command
    assert cmd.argv == ("set-status", "safe-handling", "draft")
    assert cmd.repl == 'scat_kg.set_status("safe-handling", "draft")'
    p = only(make_vault, "done-field-description")
    assert p.fix_data.options[1].command.argv == ("set-status", "safe-handling", "draft")


def test_edit_branches_carry_the_value_to_write(make_vault):
    e = only(make_vault, "required-title").fix_data.options[0].edits[0]
    assert (e.action, e.file, e.field, e.value) == ("set-field", C, "title", "Safe handling")
    e = only(make_vault, "done-field-description").fix_data.options[0].edits[0]
    assert (e.value, e.author_slot) == ("<one sentence you write>", "<one sentence you write>")
    e = only(make_vault, "cap").fix_data.options[1].edits[0]
    assert (e.file, e.field, e.value) == ("scat.toml", "stakeholder_group_cap", 4)
    e = only(make_vault, "cap-config-bad").fix_data.options[0].edits[0]
    assert e.author_slot == "<number you choose>"
    e = only(make_vault, "name-rename").fix_data.options[0].edits[0]
    assert (e.action, e.file, e.to) == ("rename-file", "concern/Bad Name.md", "concern/bad-name.md")
    e = only(make_vault, "kind-choice").fix_data.options[2].edits[0]
    assert (e.action, e.file, e.field) == ("delete-field", D, "kind")
    e = only(make_vault, "mention").fix_data.options[0].edits[0]
    assert (e.action, e.find, e.replace, e.line, e.column) == (
        "replace-text",
        "briefing",
        "[[briefing]]",
        8,
        9,
    )


def test_the_rename_edits_the_links_that_meant_the_page(make_vault):
    edits = only(make_vault, "name-rename-links").fix_data.options[0].edits
    assert [(e.action, e.file) for e in edits] == [
        ("rename-file", "concern/Bad Name.md"),
        ("replace-text", K),
    ]
    assert (edits[1].find, edits[1].replace) == ("[[Bad Name|it]]", "[[bad-name|it]]")


def test_a_duplicate_name_renames_the_file_and_edits_no_link(make_vault):
    dup = only(make_vault, "name-duplicate").fix_data.options[0].edits
    assert [e.action for e in dup] == ["rename-file"]


def test_manual_branches_carry_no_command_or_edit(make_vault):
    for case_id in ("parse", "shape-mapping", "name-by-hand"):
        (o,) = only(make_vault, case_id).fix_data.options
        assert o.kind == "manual" and o.command is None and not o.edits
    o = only(make_vault, "cap").fix_data.options[0]
    assert o.kind == "manual"
