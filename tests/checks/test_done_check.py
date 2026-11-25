"""The done check (catalogue section 5): `check_page_at_done` returns the problems a page would have at `done`.

The refusal itself is an operation (set-status); here is the list it is made from. Test names carry no rule id: the
refusal id SCAT-DONE-REFUSED is an operation rule and no `scat check` prints it.
"""

from helpers import DESK, doc, narrative, row, vault

from scat_kg.checks import check_page, check_page_at_done

GHOST = row("holds", "staff", "ghost")
C = "concern/safe-handling.md"


def at_done(make_vault, files, page):
    v = vault(make_vault, files)
    return v, check_page_at_done(v, page)


def test__a_draft_narrative_with_a_bad_end_and_no_description_would_fail_at_done(make_vault):
    files = {
        DESK: narrative(
            status="draft", description=None, rows=("| holds | borrowers | [[safe-handling]] | |",)
        )
    }
    v, report = at_done(make_vault, files, DESK)
    assert [(p.rule, p.severity) for p in report.errors] == [
        ("SCAT-DONE-FIELD", "error"),
        ("SCAT-DONE-END-NOLINK", "error"),
    ]
    assert not report.ok
    # at draft the same page is only warnings
    drafted = check_page(v, DESK)
    assert drafted.ok and [p.rule for p in drafted.problems] == [
        "SCAT-DRAFT-FIELD",
        "SCAT-DRAFT-END-NOLINK",
    ]
    # judged only: nothing is written
    assert "status: draft" in (v.root / DESK).read_text(encoding="utf-8")


def test__the_same_narrative_with_both_fixed_would_stand_at_done(make_vault):
    files = {DESK: narrative(status="draft")}
    _, report = at_done(make_vault, files, DESK)
    assert report.problems == () and report.ok


def test__a_node_page_with_no_description_would_fail(make_vault):
    _, report = at_done(
        make_vault, {C: doc("concern", "Safe handling", status="draft", description=None)}, C
    )
    assert [(p.rule, p.where) for p in report.errors] == [
        ("SCAT-DONE-FIELD", "field `description`")
    ]


def test__a_stub_is_judged_as_done_too(make_vault):
    files = {DESK: narrative(status="stub", timeframe=None, rows=(GHOST,))}
    _, report = at_done(make_vault, files, DESK)
    assert [p.rule for p in report.errors] == ["SCAT-DONE-FIELD", "SCAT-DONE-END-NOPAGE"]


def test__a_narrative_with_only_warnings_would_be_set(make_vault):
    page = narrative(status="draft", account="A [[staff]]. A Briefing came.\n")
    _, report = at_done(make_vault, {DESK: page}, DESK)
    assert report.errors == ()
    assert [p.rule for p in report.warnings] == ["SCAT-MENTION"]
    assert report.ok  # a warning does not block


def test__a_page_with_an_invalid_status_is_judged_as_done_and_the_status_error_is_listed(
    make_vault,
):
    page = narrative(status="finished", description=None)
    _, report = at_done(make_vault, {DESK: page}, DESK)
    assert [p.rule for p in report.errors] == ["SCAT-DONE-FIELD", "SCAT-FM-STATUS"]


def test__a_page_with_a_missing_status_is_judged_as_done_and_the_status_error_is_listed(make_vault):
    page = narrative(status=None, rows=(GHOST,))
    _, report = at_done(make_vault, {DESK: page}, DESK)
    assert [p.rule for p in report.errors] == ["SCAT-FM-REQUIRED", "SCAT-DONE-END-NOPAGE"]


def test__the_vault_wide_errors_are_not_listed_and_the_vault_check_reports_the_cap(make_vault):
    files = {
        "scat.toml": "stakeholder_group_cap = 1\n",
        "group/staff.md": doc("group", "Staff", status="draft"),
    }
    v, report = at_done(make_vault, files, "group/staff.md")
    assert report.problems == ()  # nothing else is wrong with the page
    from scat_kg.checks import check_vault

    assert [p.rule for p in check_vault(v).problems] == ["SCAT-CAP"]


def test__a_neighbor_with_a_defect_adds_nothing(make_vault):
    files = {
        DESK: narrative(status="draft"),
        "group/staff.md": doc("group", "Staff", description=None),
    }
    _, report = at_done(make_vault, files, DESK)
    assert report.problems == ()  # the staff page's own error is the staff page's


def test__the_messages_are_those_scat_check_prints_for_the_page_at_done(make_vault):
    page = narrative(status="draft", description=None, rows=(GHOST,))
    v, report = at_done(make_vault, {DESK: page}, DESK)
    done = vault(make_vault, {DESK: page.replace("status: draft", "status: done")})
    assert [p.render() for p in report.problems] == [
        p.render() for p in check_page(done, DESK).problems
    ]
    assert v is not done
