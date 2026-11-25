"""SCAT-DONE-FIELD and SCAT-DRAFT-FIELD, and how every status behaves (R-3). Test names carry the rule id."""

import pytest
from helpers import DESK, choose, doc, msg, narrative, report_of, rules_of, seeded, set_status

C = "concern/safe-handling.md"
DESC = 'add the line `description: "<one sentence you write>"` (author)'
VALUES = ("past", "future", "mixed")


def done_head(file, field):
    return f"error [SCAT-DONE-FIELD] {file} field `{field}`: missing on a page with status: done"


def draft_head(file, field):
    return f"warning [SCAT-DRAFT-FIELD] {file} field `{field}`: missing (required once the page is done)"


def done_description(name):
    return choose(DESC, f"run {set_status(name)} if the page is not finished")


def test__scat_done_field__description_missing_at_done_on_a_node_page(make_vault):
    seeded(
        make_vault,
        {C: doc("concern", "Safe handling", description=None)},
        msg(done_head(C, "description"), *done_description("safe-handling")),
    )


def test__scat_done_field__description_missing_at_done_on_a_narrative(make_vault):
    seeded(
        make_vault,
        {DESK: narrative(description=None)},
        msg(done_head(DESK, "description"), *done_description("desk-day")),
    )


def test__scat_done_field__present_but_empty_is_replaced(make_vault):
    page = '---\ntype: concern\nstatus: done\ntitle: "S"\ndescription: ""\n---\n'
    seeded(
        make_vault,
        {C: page},
        msg(
            done_head(C, "description"),
            *choose(
                'replace the line `description: ""` with `description: "<one sentence you write>"` (author)',
                f"run {set_status('safe-handling')} if the page is not finished",
            ),
        ),
    )


@pytest.mark.parametrize("empty", [None, "", "# past | future | mixed"])
def test__scat_done_field__timeframe_missing_or_empty_at_done_offers_the_three_values(
    make_vault, empty
):
    page = narrative(timeframe=None)
    if empty is not None:
        page = page.replace(
            'description: "D"\n', f'description: "D"\ntimeframe: {empty}\n'.replace(": \n", ":\n")
        )
    shown = "" if empty in (None, "") else f" {empty}"
    verb = "add the line" if empty is None else f"replace the line `timeframe:{shown}` with"
    seeded(
        make_vault,
        {DESK: page},
        msg(
            done_head(DESK, "timeframe"),
            *choose(
                *[f"{verb} `timeframe: {v}` (author)" for v in VALUES],
                f"run {set_status('desk-day')} if the page is not finished",
            ),
        ),
    )


@pytest.mark.parametrize("status", ["stub", "draft"])
def test__scat_done_field__not_before_done(make_vault, status):
    r = report_of(make_vault, {C: doc("concern", "S", status=status, description=None)})
    assert "SCAT-DONE-FIELD" not in rules_of(r)
    r = report_of(make_vault, {DESK: narrative(status=status, description=None, timeframe=None)})
    assert "SCAT-DONE-FIELD" not in rules_of(r)


def test__scat_draft_field__description_missing_at_draft_is_a_warning(make_vault):
    r = seeded(
        make_vault,
        {C: doc("concern", "S", status="draft", description=None)},
        msg(
            draft_head(C, "description"),
            f"Fix: {DESC} before you set status: done",
        ),
    )
    assert r.ok and r.problems[0].severity == "warning"


@pytest.mark.parametrize("status", ["stub", "draft"])
def test__scat_draft_field__timeframe_missing_before_done_is_a_warning(make_vault, status):
    r = seeded(
        make_vault,
        {DESK: narrative(status=status, timeframe=None)},
        msg(
            draft_head(DESK, "timeframe"),
            *choose(
                *[f"add the line `timeframe: {v}` (author)" for v in VALUES],
                head="Fix, choose one before you set status: done:",
            ),
        ),
    )
    assert r.ok and r.problems[0].severity == "warning"


def test__scat_draft_field__a_freshly_stubbed_narrative_gives_exactly_the_timeframe_message(
    make_vault,
):
    page = '---\ntype: narrative\nstatus: stub\ntitle: "Desk day"\ntimeframe: # past | future | mixed\n---\n'
    seeded(
        make_vault,
        {DESK: page},
        msg(
            draft_head(DESK, "timeframe"),
            *choose(
                *[
                    f"replace the line `timeframe: # past | future | mixed` with `timeframe: {v}` (author)"
                    for v in VALUES
                ],
                head="Fix, choose one before you set status: done:",
            ),
        ),
    )


def test__scat_draft_field__a_stub_stays_silent_about_description(make_vault):
    seeded(make_vault, {C: doc("concern", "S", status="stub", description=None)})


def test__scat_draft_field__a_page_without_a_status_is_judged_by_neither_field_rule(make_vault):
    r = report_of(make_vault, {C: doc("concern", "S", status=None, description=None)})
    assert rules_of(r) == ["SCAT-FM-REQUIRED"]


def test__scat_draft_field__every_valid_combination_is_clean(make_vault):
    for status in ("stub", "draft", "done"):
        seeded(make_vault, {DESK: narrative(status=status)})


# R-3: the same defects, at each status

STATUSES = {
    "stub": [
        "SCAT-DRAFT-FIELD"
    ],  # a stub is silent about a missing description; the empty timeframe is shown
    "draft": ["SCAT-DRAFT-FIELD", "SCAT-DRAFT-FIELD"],
    "done": ["SCAT-DONE-FIELD", "SCAT-DONE-FIELD"],
}


@pytest.mark.parametrize(("status", "rules"), STATUSES.items())
def test__scat_done_field__per_status_unfinished_is_never_an_error_before_done(
    make_vault, status, rules
):
    r = report_of(make_vault, {DESK: narrative(status=status, description=None, timeframe=None)})
    assert rules_of(r) == rules
    assert all(p.severity == ("error" if status == "done" else "warning") for p in r.problems)
    assert r.ok == (status != "done")


@pytest.mark.parametrize("status", ["stub", "draft", "done"])
def test__scat_fm_required__per_status_title_is_required_at_every_status(make_vault, status):
    page = f"---\ntype: concern\nstatus: {status}\ndescription: D\n---\n"
    assert rules_of(report_of(make_vault, {C: page})) == ["SCAT-FM-REQUIRED"]


@pytest.mark.parametrize("status", [None, "finished"])
def test__scat_fm_status__missing_or_invalid_status_gets_no_needs_status_rule(make_vault, status):
    page = doc("concern", "S", status=status, description=None)
    rules = set(rules_of(report_of(make_vault, {C: page})))
    assert rules and not rules & {"SCAT-DONE-FIELD", "SCAT-DRAFT-FIELD"}
