"""SCAT-DONE-* and SCAT-DRAFT-*, and how every status behaves (R-3)."""

import pytest
from helpers import choose, coded, doc, got, lines, links, report_of, seeded, set_status

C = "concern/safe-handling.md"
H = "heldby/staff-holds-safe-handling.md"
SC = "scenario-coded/desk-day-coded.md"
DESC = 'add the line `description: "<one sentence you write>"` (author)'


def done_field_fix(name):
    return choose(DESC, f"run {set_status(name)} if the page is not finished")


def test__scat_done_field__description_missing_at_done(make_vault):
    seeded(
        make_vault,
        {C: doc("concern", "S", description=None)},
        ("SCAT-DONE-FIELD", C, "field `description`", done_field_fix("safe-handling")),
    )


def test__scat_done_field__on_a_relation_page(make_vault):
    page = doc(
        "heldby", "H", description=None, extra='group: "[[staff]]"\nconcern: "[[safe-handling]]"'
    )
    seeded(
        make_vault,
        {H: page},
        ("SCAT-DONE-FIELD", H, "field `description`", done_field_fix("staff-holds-safe-handling")),
    )


def test__scat_done_field__class_page_always_and_one_option(make_vault):
    path = "class/concerns.md"
    page = doc("class", "Concerns", status=None, description=None, extra="indexes: concern")
    r = seeded(
        make_vault,
        {path: page},
        ("SCAT-DONE-FIELD", path, "field `description`", f"Fix: {DESC}"),
    )
    assert r.problems[0].what == "missing"


def test__scat_done_field__present_but_empty_is_replaced(make_vault):
    page = '---\ntype: concern\nstatus: done\ntitle: "S"\ndescription: ""\n---\n'
    fix = choose(
        'replace the line `description: ""` with `description: "<one sentence you write>"` (author)',
        f"run {set_status('safe-handling')} if the page is not finished",
    )
    seeded(make_vault, {C: page}, ("SCAT-DONE-FIELD", C, "field `description`", fix))


@pytest.mark.parametrize("status", ["stub", "draft"])
def test__scat_done_field__not_before_done(make_vault, status):
    r = report_of(make_vault, {C: doc("concern", "S", status=status, description=None)})
    assert "SCAT-DONE-FIELD" not in [p.rule for p in r.problems]


def test__scat_draft_field__warning_at_draft(make_vault):
    r = seeded(
        make_vault,
        {C: doc("concern", "S", status="draft", description=None)},
        (
            "SCAT-DRAFT-FIELD",
            C,
            "field `description`",
            f"Fix: {DESC} before you set status: done",
        ),
    )
    assert r.ok and r.problems[0].severity == "warning"


def test__scat_draft_field__nothing_at_stub(make_vault):
    seeded(make_vault, {C: doc("concern", "S", status="stub", description=None)})


# the link fields of a coded scenario, removed in turn at `done`: with suggestions, then without


def done_link_fix(
    field, suggestion, replace=None, note="suggestions found from relation pages; you decide"
):
    verb = (
        "add this to the frontmatter"
        if replace is None
        else f"replace the line `{field}: {replace}` with this"
    )
    tail = " (author)" if suggestion.startswith("<") else ""
    block = lines(f"{field}:", f'  - "[[{suggestion}]]"{tail}')
    return choose(
        f"{verb}, keeping the lines that fit ({note}):\n{block}",
        f"run {set_status('desk-day-coded')} if the page is not finished",
    )


def test__scat_done_link__with_suggestions(make_vault):
    # relation pages say staff holds safe-handling, so `groups` and `concerns` have a suggestion each
    seeded(
        make_vault,
        {SC: coded(groups="")},
        ("SCAT-DONE-LINK", SC, "field `groups`", done_link_fix("groups", "staff")),
    )


def test__scat_done_link__concerns_suggested_from_groups(make_vault):
    seeded(
        make_vault,
        {SC: coded(concerns="")},
        ("SCAT-DONE-LINK", SC, "field `concerns`", done_link_fix("concerns", "safe-handling")),
    )


def test__scat_done_link__raw_suggested_from_a_raw_page_that_lists_it(make_vault):
    seeded(
        make_vault,
        {SC: coded(raw="")},
        ("SCAT-DONE-LINK", SC, "field `raw`", done_link_fix("raw", "desk-day")),
    )


def test__scat_done_link__without_suggestions(make_vault):
    note = "no suggestions found; you decide"
    seeded(
        make_vault,
        {SC: coded(affordances="")},
        (
            "SCAT-DONE-LINK",
            SC,
            "field `affordances`",
            done_link_fix("affordances", "<one affordance page you choose>", note=note),
        ),
    )


def test__scat_done_link__empty_list_is_replaced(make_vault):
    seeded(
        make_vault,
        {SC: coded(concerns="concerns: []\n")},
        (
            "SCAT-DONE-LINK",
            SC,
            "field `concerns`",
            done_link_fix("concerns", "safe-handling", replace="[]"),
        ),
    )


def test__scat_done_link__suggestions_leave_out_listed_pages_and_show_eight(make_vault):
    files = {f"concern/c{i}.md": doc("concern", f"C{i}") for i in range(10)} | {
        f"heldby/staff-holds-c{i}.md": doc(
            "heldby", f"H{i}", extra=f'group: "[[staff]]"\nconcern: "[[c{i}]]"'
        )
        for i in range(10)
    }
    files[SC] = coded(concerns="")
    r = report_of(make_vault, files)
    fix = next(p.fix for p in r.problems if p.rule == "SCAT-DONE-LINK")
    shown = [ln for ln in fix.split("\n") if '- "[[' in ln]
    assert len(shown) == 8 and "(+3 more)" in fix  # 10 new + safe-handling = 11 offered, 8 shown
    assert shown == sorted(shown)


def test__scat_draft_link__warning_at_draft_not_done_or_stub(make_vault):
    fix = (
        "Fix: add this to the frontmatter, keeping the lines that fit "
        "(suggestions found from relation pages; you decide):\n"
        + lines("groups:", '  - "[[staff]]"')
    )
    r = seeded(
        make_vault,
        {SC: coded(status="draft", groups="")},
        ("SCAT-DRAFT-LINK", SC, "field `groups`", fix),
    )
    assert r.ok


def test__scat_done_link__nothing_at_stub(make_vault):
    seeded(make_vault, {SC: coded(status="stub", groups="", concerns="", raw="", affordances="")})


def test__scat_done_link__architecture_requires_its_four_lists(make_vault):
    path = "architecture-coded/kiosk-pitch-coded.md"
    page = doc(
        "architecture-coded",
        "K",
        extra=links("raw", "kiosk-pitch") + links("concerns", "quick-checkout"),
    )
    r = report_of(make_vault, {path: page})
    assert [(p.rule, p.where) for p in r.problems] == [
        ("SCAT-DONE-LINK", "field `affordances`"),
        ("SCAT-DONE-LINK", "field `technologies`"),
    ]


# R-3: the same defects, at each status


STATUSES = {
    "stub": [],
    "draft": ["SCAT-DRAFT-FIELD", "SCAT-DRAFT-LINK"],
    "done": ["SCAT-DONE-FIELD", "SCAT-DONE-LINK"],
}


@pytest.mark.parametrize(("status", "rules"), STATUSES.items())
def test__scat_done_link__per_status_unfinished_is_never_an_error_before_done(
    make_vault, status, rules
):
    page = doc(
        "scenario-coded", "T", status=status, description=None, extra=links("raw", "desk-day")
    )
    r = report_of(make_vault, {SC: page})
    assert sorted({p.rule for p in r.problems}) == rules
    assert all(p.severity == ("error" if status == "done" else "warning") for p in r.problems)
    assert r.ok == (status != "done")


@pytest.mark.parametrize("status", ["stub", "draft", "done"])
def test__scat_link_dangling__per_status_links_are_checked_at_every_status(make_vault, status):
    r = report_of(make_vault, {SC: coded(status=status, groups=links("groups", "ghost"))})
    assert [p.rule for p in r.problems] == ["SCAT-LINK-DANGLING"]
    assert not r.ok


@pytest.mark.parametrize("status", ["stub", "draft", "done"])
def test__scat_fm_required__per_status_title_is_required_at_every_status(make_vault, status):
    page = f"---\ntype: concern\nstatus: {status}\ndescription: D\n---\n"
    assert [p.rule for p in report_of(make_vault, {C: page}).problems] == ["SCAT-FM-REQUIRED"]


def test__scat_done_field__a_class_page_has_no_status_and_counts_as_done(make_vault):
    path = "class/concerns.md"
    page = doc("class", "Concerns", status=None, description=None, extra="indexes: concern")
    assert got(report_of(make_vault, {path: page}))[0][0] == "SCAT-DONE-FIELD"


@pytest.mark.parametrize("status", [None, "finished"])
def test__scat_fm_status__missing_or_invalid_status_gets_no_needs_status_rule(make_vault, status):
    page = doc("concern", "S", status=status, description=None)
    rules = {p.rule for p in report_of(make_vault, {C: page}).problems}
    assert rules and not rules & {"SCAT-DONE-FIELD", "SCAT-DRAFT-FIELD"}
