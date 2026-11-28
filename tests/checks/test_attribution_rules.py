"""WP23-G2, G3, R2: the one mode-dependent rule, per mode and status. Test names carry the rule id.

The rule (`scat_tools.checks.attribution.MODE_RULE`): required mode names contributors, disallowed mode none,
optional mode leaves it free; to name one is to link a contributor page in `attributed_to`.
"""

import itertools

import pytest
from helpers import (
    DESK,
    KIOSK,
    base,
    choose,
    doc,
    msg,
    narrative,
    report_of,
    rules_of,
    seeded,
    set_status,
)

import scat_tools


@pytest.fixture
def make_vault(tmp_path):
    """A fresh directory for every vault written (a test that checks several vaults writes several)."""
    counter = itertools.count()

    def make(files):
        root = tmp_path / f"vault{next(counter)}"
        for rel, content in files.items():
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content.encode("utf-8"))
        return root

    return make


STATUSES = ("stub", "draft", "done")
MODES = ("required", "optional", "disallowed")
ADA, BO = "contributor/ada-quill.md", "contributor/bo-marsh.md"


def toml(mode):
    return f"attribution = '{mode}'\nstakeholder_group_cap = 3\nlink_suggestions = true\n"


def contributor(title, status="done"):
    return doc("contributor", title, status=status, description=None)


def named(page, *links):
    """`page` with an `attributed_to` list of the links (names of contributor pages) after `timeframe`."""
    line = "attributed_to: [" + ", ".join(f'"[[{n}]]"' for n in links) + "]\n"
    return page.replace("timeframe: past\n", "timeframe: past\n" + line, 1).replace(
        "timeframe: future\n", "timeframe: future\n" + line, 1
    )


def desk(mode, status, field, *, pages=True):
    """The vault of `mode` whose desk narrative has `field` (a whole frontmatter line, or None) and `status`.

    Where the mode allows them the vault holds two contributor pages and the kiosk narrative names one, so only the
    desk narrative is judged; in disallowed mode the vault holds none and the kiosk names nobody.
    """
    page = narrative(status=status)
    if field is not None:
        page = page.replace("timeframe: past\n", f"timeframe: past\n{field}\n", 1)
    files = {"scat.toml": toml(mode), DESK: page}
    if pages and mode != "disallowed":
        files[ADA], files[BO] = contributor("Ada Quill"), contributor("Bo Marsh")
        files[KIOSK] = named(base()[KIOSK], "bo-marsh")
    return files


def rules(make_vault, mode, status, field, **kw):
    return rules_of(report_of(make_vault, desk(mode, status, field, **kw)))


LINKED = 'attributed_to: ["[[ada-quill]]"]'
SLOT = '["[[<a contributor page you link>]]"]'
ADD = f"add the line `attributed_to: {SLOT}` (author)"


def test_the_fixture_is_clean_in_every_mode(make_vault):
    for mode in MODES:
        for status in STATUSES:
            field = None if mode == "disallowed" else LINKED
            assert rules(make_vault, mode, status, field) == [], (mode, status)


# ---- SCAT-ATTR-DISALLOWED


@pytest.mark.parametrize("status", STATUSES)
@pytest.mark.parametrize("field", [LINKED, "attributed_to: []", "attributed_to:"])
def test__scat_attr_disallowed__any_attributed_to_on_a_narrative_is_an_error(
    make_vault, status, field
):
    seeded(
        make_vault,
        desk("disallowed", status, field),
        msg(
            f"error [SCAT-ATTR-DISALLOWED] {DESK} field `attributed_to`: present, and the vault's "
            "attribution mode is `disallowed`",
            "Fix: delete the field `attributed_to` (all its lines): this vault's attribution mode is "
            "`disallowed`; the coder who wants contributors named changes `attribution` in scat.toml for "
            "the whole vault",
        ),
    )


@pytest.mark.parametrize("status", STATUSES)
def test__scat_attr_disallowed__a_contributor_page_is_an_error_at_every_status(make_vault, status):
    files = desk("disallowed", "done", None)
    files[ADA] = contributor("Ada Quill", status)
    report = seeded(
        make_vault,
        files,
        msg(
            f"error [SCAT-ATTR-DISALLOWED] {ADA} field `type`: `contributor` is a contributor page, and "
            "the vault's attribution mode is `disallowed`",
            f"Fix: delete the file {ADA}: this vault's attribution mode is `disallowed`, so it holds no "
            "contributor page; the coder who wants contributor pages changes `attribution` in scat.toml "
            "for the whole vault",
        ),
    )
    (edit,) = report.problems[0].fix_data.options[0].edits
    assert (edit.action, edit.file) == ("delete-file", ADA)


def test__scat_attr_disallowed__says_nothing_else_about_the_field(make_vault):
    # a dangling link and a wrong shape in disallowed mode: the one finding stands for both
    for field in ('attributed_to: ["[[ghost]]"]', "attributed_to: 3", 'attributed_to: ["Ada"]'):
        assert rules(make_vault, "disallowed", "done", field) == ["SCAT-ATTR-DISALLOWED"], field


def test__scat_attr_disallowed__is_silent_when_absent_and_in_the_other_modes(make_vault):
    for status in STATUSES:
        assert rules(make_vault, "disallowed", status, None) == []
        for mode in ("optional", "required"):
            assert rules(make_vault, mode, status, LINKED) == []


def test__scat_attr_disallowed__judges_narratives_and_contributors_only(make_vault):
    files = desk("disallowed", "done", None)
    files["concern/safe-handling.md"] = doc(
        "concern", "Safe handling", extra='attributed_to: ["[[ada-quill]]"]'
    )
    assert rules_of(report_of(make_vault, files)) == []


# ---- SCAT-DONE-ATTR, SCAT-DRAFT-ATTR


@pytest.mark.parametrize("status", STATUSES)
def test__scat_draft_attr__required_mode_wants_a_contributor(make_vault, status):
    want = {"stub": "SCAT-DRAFT-ATTR", "draft": "SCAT-DRAFT-ATTR", "done": "SCAT-DONE-ATTR"}
    for field in (None, "attributed_to:", "attributed_to: []", 'attributed_to: [""]'):
        assert rules(make_vault, "required", status, field) == [want[status]], field


def test__scat_done_attr__message_and_fix_at_done(make_vault):
    report = seeded(
        make_vault,
        desk("required", "done", None),
        msg(
            f"error [SCAT-DONE-ATTR] {DESK} field `attributed_to`: missing on a page with status: "
            "done (the vault's attribution mode is `required`)",
            *choose(ADD, f"run {set_status('desk-day')} if the page is not finished"),
        ),
    )
    assert not report.ok


def test__scat_draft_attr__is_a_warning_that_does_not_block(make_vault):
    for status in ("stub", "draft"):
        report = seeded(
            make_vault,
            desk("required", status, None),
            msg(
                f"warning [SCAT-DRAFT-ATTR] {DESK} field `attributed_to`: missing (required once the "
                "page is done: the vault's attribution mode is `required`)",
                f"Fix: {ADD} before you set status: done",
            ),
        )
        assert report.ok


def test__scat_done_attr__replaces_an_empty_line(make_vault):
    report = report_of(make_vault, desk("required", "done", "attributed_to: []"))
    (p,) = report.problems
    assert "replace the line `attributed_to: []` with" in p.fix


def test__scat_done_attr__a_contributor_named_or_another_mode_is_silent(make_vault):
    for status in STATUSES:
        assert rules(make_vault, "required", status, LINKED) == []
        assert rules(make_vault, "optional", status, None) == []
        assert rules(make_vault, "disallowed", status, None) == []


def test__scat_done_attr__an_entry_that_is_a_bad_link_is_one_fault_not_two(make_vault):
    assert rules(make_vault, "required", "done", 'attributed_to: ["Ada Quill"]') == [
        "SCAT-ATTR-LINK"
    ]


def test__scat_done_attr__a_wrong_shape_is_not_a_missing_contributor(make_vault):
    assert rules(make_vault, "required", "done", "attributed_to: 3") == ["SCAT-FM-SHAPE"]


def test__scat_done_attr__the_done_check_judges_the_page_as_done(make_vault):
    root = make_vault({**base(), **desk("required", "draft", None)})
    result = scat_tools.set_status("desk-day", "done", root=root)
    assert not result.ok
    assert any(p.rule == "SCAT-DONE-ATTR" for p in result.refused[0].problems)
    (root / DESK).write_text(named(narrative(status="draft"), "ada-quill"), encoding="utf-8")
    assert scat_tools.set_status("desk-day", "done", root=root).ok


# ---- SCAT-ATTR-LINK


def link_head(status, what):
    return f"error [SCAT-ATTR-LINK] {DESK} field `attributed_to`: {what}"


@pytest.mark.parametrize("mode", ["optional", "required"])
@pytest.mark.parametrize("status", STATUSES)
def test__scat_attr_link__an_entry_that_is_text_is_an_error(make_vault, mode, status):
    report = report_of(make_vault, desk(mode, status, 'attributed_to: ["Ada Quill"]'))
    (p,) = report.problems
    assert (p.rule, p.severity) == ("SCAT-ATTR-LINK", "error") and not report.ok
    assert p.what == "`Ada Quill` is not a link to a contributor page"
    assert p.fix_data.kind == "options"
    assert [o.kind for o in p.fix_data.options] == [
        "exact",
        "manual",
        "exact",
    ]  # near match, hint, drop


def test__scat_attr_link__a_near_match_is_offered_for_a_text_entry(make_vault):
    seeded_files = desk("optional", "done", 'attributed_to: ["Ada Quil"]')
    report = report_of(make_vault, seeded_files)
    (p,) = report.problems
    assert p.rule == "SCAT-ATTR-LINK"
    assert (
        'replace the line `attributed_to: ["Ada Quil"]` with `attributed_to: ["[[ada-quill]]"]` '
        "(the contributor page `ada-quill`)"
    ) in p.fix
    assert "with `attributed_to: []` (drop this entry)" in p.fix


@pytest.mark.parametrize("mode", ["optional", "required"])
@pytest.mark.parametrize("status", STATUSES)
def test__scat_attr_link__a_link_that_reaches_no_page_is_an_error(make_vault, mode, status):
    seeded(
        make_vault,
        desk(mode, status, 'attributed_to: ["[[ghost]]"]'),
        msg(
            link_head(status, "`[[ghost]]` does not reach a page (no page is named ghost)"),
            *choose(
                'run `scat stub ghost --type contributor` (REPL: `scat_tools.stub("ghost", type="contributor")`) '
                "to create the contributor page the entry links",
                'replace the line `attributed_to: ["[[ghost]]"]` with `attributed_to: []` (drop this entry)',
            ),
        ),
    )


def test__scat_attr_link__a_missing_page_gets_the_stub_command_as_an_exact_fix(make_vault):
    report = report_of(make_vault, desk("optional", "done", 'attributed_to: ["[[ghost]]"]'))
    (p,) = report.problems
    stub_it, drop = p.fix_data.options
    assert stub_it.kind == "exact" and stub_it.edits == ()
    assert stub_it.command.argv == ("stub", "ghost", "--type", "contributor")
    assert stub_it.command.repl == 'scat_tools.stub("ghost", type="contributor")'
    assert drop.kind == "exact"


def test__scat_attr_link__running_the_stub_fix_makes_the_link_resolve(make_vault):
    root = make_vault(desk("optional", "done", 'attributed_to: ["[[ghost]]"]'))
    assert scat_tools.stub("ghost", "contributor", root=root).ok
    assert "SCAT-ATTR-LINK" not in [p.rule for p in scat_tools.check(root=root).problems]


@pytest.mark.parametrize("entry", ['"Ada Quill"', '"[[safe-handling]]"'])
def test__scat_attr_link__text_and_wrong_type_keep_the_manual_hint(make_vault, entry):
    report = report_of(make_vault, desk("optional", "done", f"attributed_to: [{entry}]"))
    (p,) = report.problems
    assert [o.kind for o in p.fix_data.options][-2:] == ["manual", "exact"]


def test__scat_attr_link__a_dangling_link_with_a_near_match_offers_it(make_vault):
    report = report_of(make_vault, desk("optional", "done", 'attributed_to: ["[[ada-quil]]"]'))
    (p,) = report.problems
    assert p.what == "`[[ada-quil]]` does not reach a page (no page is named ada-quil)"
    assert 'with `attributed_to: ["[[ada-quill]]"]` (the contributor page `ada-quill`)' in p.fix
    swap = p.fix_data.options[0]
    assert swap.kind == "exact" and swap.edits[0].value == ["[[ada-quill]]"]


@pytest.mark.parametrize("mode", ["optional", "required"])
@pytest.mark.parametrize("status", STATUSES)
def test__scat_attr_link__a_link_to_a_page_of_another_type_is_an_error(make_vault, mode, status):
    report = report_of(make_vault, desk(mode, status, 'attributed_to: ["[[staff]]"]'))
    (p,) = report.problems
    assert p.rule == "SCAT-ATTR-LINK" and p.severity == "error" and not report.ok
    assert p.what == "`[[staff]]` reaches a page that is not a contributor (it is a group page)"


def test__scat_attr_link__only_the_bad_entries_are_reported_and_the_good_kept(make_vault):
    field = 'attributed_to: ["[[ada-quill]]", "[[ghost]]", "[[bo-marsh|Bo]]"]'
    report = report_of(make_vault, desk("optional", "done", field))
    (p,) = report.problems
    assert p.what.startswith("`[[ghost]]` does not reach a page")
    drop = next(o for o in p.fix_data.options if "drop this entry" in o.text)
    assert drop.edits[0].value == ["[[ada-quill]]", "[[bo-marsh|Bo]]"]


def test__scat_attr_link__a_link_is_read_as_text_and_is_no_link_of_the_page(make_vault):
    report = report_of(make_vault, desk("optional", "done", 'attributed_to: ["[[ghost]]"]'))
    assert [p.rule for p in report.problems] == [
        "SCAT-ATTR-LINK"
    ]  # not also SCAT-LINK-DANGLING-BODY


def test__scat_fm_shape__an_unquoted_attributed_to_link_gets_an_exact_quoted_fix(make_vault):
    report = report_of(make_vault, desk("optional", "done", "attributed_to: [[ada-quill]]"))
    (p,) = report.problems
    assert p.rule == "SCAT-FM-SHAPE"
    assert (
        p.what
        == 'expected a list of links (text), found a list inside a list: a link must be written in quotes, `"[[name]]"`'
    )
    assert p.fix_data.kind == "exact" and p.fix_data.options[0].edits[0].value == ["[[ada-quill]]"]
    assert 'replace the field with the line `attributed_to: ["[[ada-quill]]"]`' in p.fix
    report = report_of(make_vault, desk("optional", "done", 'attributed_to: "[[ada-quill]]"'))
    (p,) = report.problems
    assert p.rule == "SCAT-FM-SHAPE" and 'attributed_to: ["[[ada-quill]]"]' in p.fix
    assert p.what == "expected a list of links (text), found one line of text"


def test__scat_attr_link__says_nothing_when_the_mode_is_disallowed_or_unknown(make_vault):
    assert rules(make_vault, "disallowed", "done", 'attributed_to: ["Ada"]') == [
        "SCAT-ATTR-DISALLOWED"
    ]
    files = desk("optional", "done", 'attributed_to: ["Ada"]')
    files["scat.toml"] = "stakeholder_group_cap = 3\nlink_suggestions = true\n"
    assert rules_of(report_of(make_vault, files)) == ["SCAT-MODE-CONFIG"]


# ---- contributor pages in the other rules


def test_a_contributor_page_needs_type_status_and_title_and_nothing_else(make_vault):
    files = desk("optional", "done", LINKED)
    files[BO] = doc("contributor", "Bo Marsh", status="stub", description=None)
    assert rules_of(report_of(make_vault, files)) == []
    files[BO] = "---\ntype: contributor\nstatus: stub\n---\n"
    assert rules_of(report_of(make_vault, files)) == ["SCAT-FM-REQUIRED"]


def test_fm_type_offers_contributor_only_where_the_mode_allows_it(make_vault):
    for mode, offered in (("optional", True), ("required", True), ("disallowed", False)):
        files = desk(mode, "done", None if mode == "disallowed" else LINKED)
        files["concern/odd.md"] = doc("concern", "Odd").replace("type: concern", "type: gadget")
        report = report_of(make_vault, files)
        (p,) = [p for p in report.problems if p.rule == "SCAT-FM-TYPE"]
        assert ("`type: contributor`" in p.fix) is offered, mode


def test_a_body_link_to_a_missing_page_never_offers_a_contributor_stub(make_vault):
    files = desk("optional", "done", LINKED)
    files[DESK] = files[DESK].replace("The [[staff]]", "The [[staff]] and [[ghost]]", 1)
    (p,) = report_of(make_vault, files).problems
    assert p.rule == "SCAT-LINK-DANGLING-BODY" and "contributor" not in p.fix


def test_a_row_end_that_links_a_contributor_page_is_not_a_node(make_vault):
    files = desk("optional", "done", LINKED)
    files[DESK] = files[DESK].replace(
        "[[staff]] | holds | [[safe-handling]]", "[[ada-quill]] | holds | [[safe-handling]]"
    )
    report = report_of(make_vault, files)
    (p,) = [p for p in report.problems if p.rule == "SCAT-DONE-END-NOTNODE"]
    assert "[[ada-quill]] is a contributor page, not a node" in p.what


# ---- no bleed between the modes


def vault_named(mode):
    """Every narrative names a contributor, two contributor pages exist (what `required` and `optional` allow)."""
    files = desk("optional", "done", LINKED)
    files["scat.toml"] = toml(mode)
    return files


def vault_unnamed(mode):
    """No narrative names anyone, no contributor page exists (what `disallowed` and `optional` allow)."""
    files = base()
    files["scat.toml"] = toml(mode)
    return files


EXPECT = {
    # (vault, mode): the rules that fire. Each mode grades only its own sentence of the mode rule.
    ("named", "required"): [],
    ("named", "optional"): [],
    ("named", "disallowed"): ["SCAT-ATTR-DISALLOWED"]
    * 4,  # two contributor pages and the two narratives' fields
    ("unnamed", "required"): ["SCAT-DONE-ATTR"] * 2,  # both narratives are `done`
    ("unnamed", "optional"): [],
    ("unnamed", "disallowed"): [],
}


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("which", ["named", "unnamed"])
def test_no_bleed__each_mode_grades_only_its_own_sentence(make_vault, mode, which):
    files = (vault_named if which == "named" else vault_unnamed)(mode)
    files.setdefault(KIOSK, base()[KIOSK])
    if which == "named":
        files[KIOSK] = named(base()[KIOSK], "bo-marsh")
    got = sorted(rules_of(report_of(make_vault, files)))
    assert got == EXPECT[(which, mode)]


def test_no_bleed__a_rule_of_one_mode_never_fires_in_another(make_vault):
    fired = {}
    for mode in MODES:
        for which in ("named", "unnamed"):
            files = (vault_named if which == "named" else vault_unnamed)(mode)
            if which == "named":
                files[KIOSK] = named(base()[KIOSK], "bo-marsh")
            fired.setdefault(mode, set()).update(rules_of(report_of(make_vault, files)))
    assert fired["required"] <= {"SCAT-DONE-ATTR", "SCAT-DRAFT-ATTR", "SCAT-ATTR-LINK"}
    assert fired["optional"] <= {"SCAT-ATTR-LINK"}
    assert fired["disallowed"] <= {"SCAT-ATTR-DISALLOWED"}


def test_switching_the_mode_rechecks_the_whole_vault_against_the_new_mode(make_vault):
    """One seeded vault, three modes: no code switches the mode, `check` reads the current one over every page."""
    files = {**base(), **vault_named("optional")}
    files[KIOSK] = named(base()[KIOSK], "bo-marsh")
    root = make_vault(files)
    assert scat_tools.check(root=root).problems == ()
    (root / "scat.toml").write_text(toml("disallowed"), encoding="utf-8")
    after = scat_tools.check(root=root)
    assert sorted((p.file, p.rule) for p in after.problems) == sorted(
        [(DESK, "SCAT-ATTR-DISALLOWED"), (KIOSK, "SCAT-ATTR-DISALLOWED")]
        + [(ADA, "SCAT-ATTR-DISALLOWED"), (BO, "SCAT-ATTR-DISALLOWED")]
    )
    assert not after.ok and after.mode == "disallowed"
    (root / "scat.toml").write_text(toml("required"), encoding="utf-8")
    assert scat_tools.check(root=root).problems == ()
    (root / DESK).write_text(narrative(), encoding="utf-8")  # the desk names nobody now
    required = scat_tools.check(root=root)
    assert [(p.file, p.rule) for p in required.problems] == [(DESK, "SCAT-DONE-ATTR")]
    (root / "scat.toml").write_text(toml("optional"), encoding="utf-8")
    assert scat_tools.check(root=root).problems == ()
