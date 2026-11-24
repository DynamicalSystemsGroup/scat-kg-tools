"""Seeded defects for the link rules on frontmatter fields: shape, unlisted, endpoint, discouraged."""

import pytest
from helpers import (
    AC,
    ATTR,
    HELDBY,
    SC,
    choose,
    coded,
    doc,
    line_of,
    lines,
    links,
    region_for,
    report_of,
    seeded,
)

SHAPE = "SCAT-LINK-SHAPE"
FIELD = "field `concerns`"


def rebuilt(*items):
    return "Fix: replace the whole field with\n" + lines("concerns:", *[f"  {i}" for i in items])


def test__scat_link_shape__scalar_value(make_vault):
    seeded(
        make_vault,
        {SC: coded(concerns='concerns: "[[safe-handling]]"\n')},
        (SHAPE, SC, FIELD, rebuilt('- "[[safe-handling]]"')),
    )


def test__scat_link_shape__unquoted_wikilink_is_a_nested_list(make_vault):
    seeded(
        make_vault,
        {SC: coded(concerns="concerns:\n  - [[safe-handling]]\n")},
        (SHAPE, SC, FIELD, rebuilt('- "[[safe-handling]]"')),
    )


def test__scat_link_shape__alias_item(make_vault):
    seeded(
        make_vault,
        {SC: coded(concerns='concerns:\n  - "[[safe-handling|Safe]]"\n')},
        (SHAPE, SC, FIELD, rebuilt('- "[[safe-handling]]"')),
    )


def test__scat_link_shape__heading_item(make_vault):
    seeded(
        make_vault,
        {SC: coded(concerns='concerns:\n  - "[[safe-handling#Part]]"\n')},
        (SHAPE, SC, FIELD, rebuilt('- "[[safe-handling]]"')),
    )


def test__scat_link_shape__number_item_cannot_be_read(make_vault):
    r = seeded(
        make_vault,
        {SC: coded(concerns="concerns:\n  - 5\n")},
        (SHAPE, SC, FIELD, rebuilt('- "[[<one page you choose>]]" (author)')),
    )
    assert "could not be read" in r.problems[0].what


def test__scat_link_shape__line_is_the_field_line(make_vault):
    text = coded(concerns='concerns: "[[safe-handling]]"\n')
    r = seeded(make_vault, {SC: text}, (SHAPE, SC, FIELD, rebuilt('- "[[safe-handling]]"')))
    assert r.problems[0].line == line_of(text, "concerns:")


def test__scat_link_shape__single_field_as_one_item_list_is_exact(make_vault):
    page = doc("heldby", "H", extra='group:\n  - "[[staff]]"\nconcern: "[[safe-handling]]"')
    fix = 'Fix: replace the whole field with the line `group: "[[staff]]"`'
    seeded(make_vault, {HELDBY: page}, (SHAPE, HELDBY, "field `group`", fix))


def test__scat_link_shape__single_field_as_two_item_list_is_a_choice(make_vault):
    page = doc(
        "heldby",
        "H",
        extra='group:\n  - "[[staff]]"\n  - "[[borrowers]]"\nconcern: "[[safe-handling]]"',
    )
    fix = choose(
        'keep this one: replace the whole field with the line `group: "[[staff]]"`',
        'keep this one: replace the whole field with the line `group: "[[borrowers]]"`',
    )
    r = seeded(make_vault, {HELDBY: page}, (SHAPE, HELDBY, "field `group`", fix))
    assert "create more relation pages" in r.problems[0].what


UNLISTED = "SCAT-LINK-UNLISTED"


def test__scat_link_unlisted__groups_on_a_concern_page(make_vault):
    path = "concern/quick-checkout.md"
    page = doc("concern", "Q", extra=links("groups", "staff"))
    r = seeded(
        make_vault,
        {path: page},
        (UNLISTED, path, "field `groups`", "Fix: delete `groups:` and its list items"),
    )
    assert "its link fields are: conflicts" in r.problems[0].what
    assert r.problems[0].line == line_of(page, "groups:")


def test__scat_link_unlisted__concern_on_a_coded_scenario(make_vault):
    page = coded(extra='concern: "[[safe-handling]]"\n')
    r = seeded(
        make_vault,
        {SC: page},
        (UNLISTED, SC, "field `concern`", "Fix: delete `concern:` and its list items"),
    )
    assert "affordances, concerns, groups, raw, technologies" in r.problems[0].what


def test__scat_link_unlisted__empty_value_and_stale_first_member_key_give_none(make_vault):
    seeded(
        make_vault,
        {
            "concern/quick-checkout.md": doc("concern", "Q", extra="groups: []\n"),
            "stakeholder-group/staff.md": doc(
                "stakeholder-group", "Staff", extra=links("heldby", "x")
            ),
        },
    )


ENDPOINT = "SCAT-LINK-ENDPOINT"


def test__scat_link_endpoint__affordance_under_concerns_offers_a_move(make_vault):
    page = coded(concerns=links("concerns", "safe-handling", "briefing"))
    fix = (
        choose(
            'move the item line `- "[[briefing]]"` from `concerns` to `affordances`: delete it from `concerns`, '
            'then add under `affordances:` the line `- "[[briefing]]"`',
            'delete the item line `- "[[briefing]]"` under `concerns`',
        )
        + "\n(no existing concern page was found to replace it with)"
    )
    r = seeded(make_vault, {SC: page}, (ENDPOINT, SC, FIELD, fix))
    assert r.problems[0].line == line_of(page, "briefing")


def test__scat_link_endpoint__move_into_a_missing_key_and_a_flow_list(make_vault):
    page = coded(concerns='concerns: ["[[safe-handling]]", "[[briefing]]"]\n', affordances="")
    r = report_of(make_vault, {SC: page})
    fix = next(p.fix for p in r.problems if p.rule == ENDPOINT)
    assert (
        'move the item line `- "[[briefing]]"` from `concerns` to `affordances`: delete it from `concerns` '
        "(in a flow list delete that one entry and its comma, leaving `[]` if it was the only one), "
        'then add `affordances:` and under it the line `- "[[briefing]]"`'
    ) in fix


def test__scat_link_endpoint__move_into_an_empty_list(make_vault):
    page = coded(
        concerns=links("concerns", "safe-handling", "briefing"), affordances="affordances: []\n"
    )
    r = report_of(make_vault, {SC: page})
    fix = next(p.fix for p in r.problems if p.rule == ENDPOINT)
    assert (
        "then replace the line `affordances: []` with `affordances:` and under it "
        'the line `- "[[briefing]]"`'
    ) in fix


def test__scat_link_endpoint__replacements_in_two_tiers_then_delete(make_vault):
    # self-checkout is already under `affordances`, so there is no move. quick-checkout shares an
    # `addresses` page with it (tier 1); careful-keeping is linked from the body (tier 2).
    page = coded(
        concerns=links("concerns", "safe-handling", "self-checkout"),
        body="See [[careful-keeping]].\n",
    )
    fix = choose(
        'replace `- "[[self-checkout]]"` with `- "[[quick-checkout]]"`',
        'replace `- "[[self-checkout]]"` with `- "[[careful-keeping]]"`',
        'delete the item line `- "[[self-checkout]]"` under `concerns`',
    )
    seeded(make_vault, {SC: page}, (ENDPOINT, SC, FIELD, fix))


def test__scat_link_endpoint__more_than_five_replacements_are_counted(make_vault):
    files = {f"concern/c{i}.md": doc("concern", f"C{i}") for i in range(7)}
    files |= {
        f"addresses/a{i}.md": doc(
            "addresses", f"A{i}", extra=f'concern: "[[c{i}]]"\naffordance: "[[self-checkout]]"'
        )
        for i in range(7)
    }
    files[SC] = coded(concerns=links("concerns", "safe-handling", "self-checkout"))
    r = report_of(make_vault, files)
    fix = next(p.fix for p in r.problems if p.rule == ENDPOINT)
    options = [ln for ln in fix.split("\n") if ln.startswith("  ") and "replace" in ln]
    assert [o.split("[[")[2].split("]]")[0] for o in options] == ["c0", "c1", "c2", "c3", "c4"]
    assert fix.endswith("\n(+3 more not shown)")  # c5, c6 and quick-checkout


def test__scat_link_endpoint__relation_endpoint_replaced_through_a_sharing_page(make_vault):
    # `affordance` holds a technology. briefing shares an `attributes` page with that technology.
    other = "attributes/briefing-attributed-to-booking-app.md"
    files = {
        ATTR: doc(
            "attributes", "A", extra='affordance: "[[booking-app]]"\ntechnology: "[[booking-app]]"'
        ),
        other: doc(
            "attributes", "B", extra='affordance: "[[briefing]]"\ntechnology: "[[booking-app]]"'
        ),
    }
    fix = 'Fix: replace `affordance: "[[booking-app]]"` with `affordance: "[[briefing]]"`'
    seeded(make_vault, files, (ENDPOINT, ATTR, "field `affordance`", fix))


def test__scat_link_endpoint__relation_endpoint_with_no_candidate_is_by_hand(make_vault):
    page = doc(
        "attributes", "A", extra='affordance: "[[booking-app]]"\ntechnology: "[[booking-app]]"'
    )
    r = seeded(
        make_vault,
        {ATTR: page},
        (
            ENDPOINT,
            ATTR,
            "field `affordance`",
            (
                "Fix: change the pair by hand: no existing affordance page was found, and "
                "`affordance` is required at every status"
            ),
        ),
    )
    assert not r.ok


def test__scat_link_endpoint__swapped_relation_endpoints_are_one_message(make_vault):
    page = doc("heldby", "H", extra='group: "[[safe-handling]]"\nconcern: "[[staff]]"')
    fix = (
        "Fix: replace the two lines\n"
        + lines('group: "[[safe-handling]]"', 'concern: "[[staff]]"')
        + "\n     with\n"
        + lines('group: "[[staff]]"', 'concern: "[[safe-handling]]"')
    )
    r = seeded(make_vault, {HELDBY: page}, (ENDPOINT, HELDBY, "fields `group` and `concern`", fix))
    assert r.problems[0].line == line_of(page, "group:")


def test__scat_link_endpoint__swap_names_the_field_that_comes_first_in_the_file(make_vault):
    page = doc("heldby", "H", extra='concern: "[[staff]]"\ngroup: "[[safe-handling]]"')
    r = report_of(make_vault, {HELDBY: page})
    assert [p.where for p in r.problems] == ["fields `concern` and `group`"]


@pytest.mark.parametrize("status", ["stub", "draft", "done"])
def test__scat_link_endpoint__same_message_at_each_status(make_vault, status):
    page = coded(status=status, concerns=links("concerns", "safe-handling", "briefing"))
    r = report_of(make_vault, {SC: page})
    assert [(p.rule, p.severity) for p in r.problems] == [(ENDPOINT, "error")]


def test__scat_link_endpoint__class_page_is_a_page_of_type_class(make_vault):
    files = {
        "class/concerns.md": doc("class", "Concerns", status=None, extra="indexes: concern")
        + region_for(make_vault, "concerns"),
        SC: coded(concerns=links("concerns", "safe-handling", "concerns")),
    }
    # the class page now carries its table, so the replacements the rule collects are no longer empty
    fix = choose(
        'replace `- "[[concerns]]"` with `- "[[careful-keeping]]"`',
        'replace `- "[[concerns]]"` with `- "[[quick-checkout]]"`',
        'delete the item line `- "[[concerns]]"` under `concerns`',
    )
    r = seeded(make_vault, files, (ENDPOINT, SC, FIELD, fix))
    assert "is a class page" in r.problems[0].what


def test__scat_link_endpoint__target_with_an_invalid_type_is_not_endpoint_checked(make_vault):
    files = {"concern/safe-handling.md": doc("gadget", "S")}
    r = report_of(make_vault, files)
    assert [p.rule for p in r.problems] == ["SCAT-FM-TYPE"]


def test__scat_link_endpoint__no_candidates_leaves_the_delete(make_vault):
    page = coded(raw=links("raw", "desk-day", "kiosk-pitch"))
    fix = (
        'Fix: delete the item line `- "[[kiosk-pitch]]"` under `raw`\n'
        "(no existing scenario-raw page was found to replace it with)"
    )
    seeded(make_vault, {SC: page}, (ENDPOINT, SC, "field `raw`", fix))


DISC = "SCAT-LINK-DISCOURAGED"
GROUP_WHY = "an architecture relates concerns, affordances and technologies; stakeholders are abstracted away"
TECH_WHY = (
    "a scenario relates groups, concerns and affordances; technologies stay in the background"
)


def test__scat_link_discouraged__technologies_on_a_coded_scenario_with_suggestions(make_vault):
    page = coded(
        affordances=links("affordances", "briefing"), extra=links("technologies", "booking-app")
    )
    fix = choose(
        "delete `technologies:` and its list items",
        "keep the point by linking what they offer, in `affordances` (suggestions you confirm): "
        'add under `affordances:` the line `- "[[self-checkout]]"`',
    )
    r = seeded(make_vault, {SC: page}, (DISC, SC, "field `technologies`", fix))
    assert r.ok and r.problems[0].severity == "warning" and TECH_WHY in r.problems[0].what
    assert r.problems[0].line == line_of(page, "technologies:")


def test__scat_link_discouraged__technologies_without_suggestions(make_vault):
    page = coded(extra=links("technologies", "booking-app"))
    seeded(
        make_vault,
        {SC: page},
        (DISC, SC, "field `technologies`", "Fix: delete `technologies:` and its list items"),
    )


def test__scat_link_discouraged__groups_on_a_coded_architecture_with_suggestions(make_vault):
    page = doc(
        "architecture-coded",
        "K",
        extra=links("raw", "kiosk-pitch")
        + links("concerns", "quick-checkout")
        + links("affordances", "self-checkout")
        + links("technologies", "booking-app")
        + links("groups", "staff"),
    )
    fix = choose(
        "delete `groups:` and its list items",
        "keep the point by linking what they offer, in `concerns` (suggestions you confirm): "
        'add under `concerns:` the line `- "[[safe-handling]]"`',
    )
    r = seeded(make_vault, {AC: page}, (DISC, AC, "field `groups`", fix))
    assert GROUP_WHY in r.problems[0].what


def test__scat_link_discouraged__groups_without_suggestions(make_vault):
    page = doc(
        "architecture-coded",
        "K",
        extra=links("raw", "kiosk-pitch")
        + links("concerns", "quick-checkout")
        + links("affordances", "self-checkout")
        + links("technologies", "booking-app")
        + links("groups", "borrowers"),
    )
    seeded(
        make_vault,
        {AC: page},
        (DISC, AC, "field `groups`", "Fix: delete `groups:` and its list items"),
    )


def test__scat_link_discouraged__the_allowed_direction_gives_none(make_vault):
    # technologies on a coded architecture and groups on a coded scenario are what those types are for
    seeded(make_vault, {})


def test__scat_link_discouraged__still_dangling_checked(make_vault):
    page = coded(extra=links("technologies", "ghost"))
    rules = [p.rule for p in report_of(make_vault, {SC: page}).problems]
    assert rules == [
        "SCAT-LINK-DISCOURAGED",
        "SCAT-LINK-DANGLING",
    ]  # by line: the key, then the item


BODY = "SCAT-LINK-DISCOURAGED-BODY"


def test__scat_link_discouraged_body__technology_in_a_coded_scenario_body(make_vault):
    page = coded(body="It runs on [[booking-app]].\n")
    n = line_of(page, "It runs")
    fix = choose(
        f"on line {n} replace `[[booking-app]]` with `booking-app` to keep the words and drop the link",
        f"on line {n} replace `[[booking-app]]` with `[[self-checkout]]`",
    )
    seeded(make_vault, {SC: page}, (BODY, SC, "link [[booking-app]]", fix))


def test__scat_link_discouraged_body__technology_in_a_raw_scenario_body(make_vault):
    path = "scenario-raw/desk-day.md"
    page = doc(
        "scenario-raw",
        "D",
        extra=links("coded", "desk-day-coded"),
        body="It runs on [[booking-app]].\n",
    )
    n = line_of(page, "It runs")
    fix = choose(
        f"on line {n} replace `[[booking-app]]` with `booking-app` to keep the words and drop the link",
        f"on line {n} replace `[[booking-app]]` with `[[self-checkout]]`",
    )
    seeded(make_vault, {path: page}, (BODY, path, "link [[booking-app]]", fix))


@pytest.mark.parametrize(
    ("path", "page"),
    [
        (
            AC,
            doc(
                "architecture-coded",
                "K",
                extra=links("raw", "kiosk-pitch")
                + links("concerns", "quick-checkout")
                + links("affordances", "self-checkout")
                + links("technologies", "booking-app"),
                body="Staff like [[staff]].\n",
            ),
        ),
        (
            "architecture-raw/kiosk-pitch.md",
            doc(
                "architecture-raw",
                "K",
                extra=links("coded", "kiosk-pitch-coded"),
                body="Staff like [[staff]].\n",
            ),
        ),
    ],
)
def test__scat_link_discouraged_body__group_in_an_architecture_body(make_vault, path, page):
    n = line_of(page, "Staff like")
    fix = choose(
        f"on line {n} replace `[[staff]]` with `staff` to keep the words and drop the link",
        f"on line {n} replace `[[staff]]` with `[[safe-handling]]`",
    )
    seeded(make_vault, {path: page}, (BODY, path, "link [[staff]]", fix))


def test__scat_link_discouraged_body__the_same_links_on_a_concern_page_give_none(make_vault):
    page = doc("concern", "S", body="[[booking-app]] and [[staff]]\n")
    seeded(make_vault, {"concern/safe-handling.md": page})
