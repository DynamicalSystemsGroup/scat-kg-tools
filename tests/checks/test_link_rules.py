"""SCAT-LINK-DANGLING-BODY, SCAT-MENTION, SCAT-CAP and SCAT-CAP-CONFIG. Test names carry the rule id."""

import pytest
from helpers import (
    ACCOUNT,
    DESK,
    DESK_ROWS,
    choose,
    doc,
    msg,
    narrative,
    report_of,
    row,
    rules_of,
    seeded,
    stub,
)

C = "concern/safe-handling.md"
LINE = 8  # the first body line of a page made by `doc` with a body that starts with a blank line
TYPES = ("group", "concern", "affordance", "technology", "narrative")
ARTICLE = {
    "affordance": "an affordance",
    "concern": "a concern",
    "group": "a group",
    "narrative": "a narrative",
    "technology": "a technology",
}


def body(text):
    return {C: doc("concern", "Safe handling", body=f"\n{text}\n")}


def dangling(target, reason, *fix, file=C, line=LINE, link=None):
    return msg(
        f"error [SCAT-LINK-DANGLING-BODY] {file}:{line} link [[{target}]]: does not reach a page ({reason})",
        *fix,
    )


def stubs(name, keys=TYPES):
    return [f"run {stub(name, k)} to create {ARTICLE[k]} page" for k in keys]


def drop(literal, shown, line=LINE):
    return f"on line {line} replace `{literal}` with `{shown}` to keep the words and drop the link"


# SCAT-LINK-DANGLING-BODY


def test__scat_link_dangling_body__a_name_no_row_end_names_offers_the_five_types(make_vault):
    seeded(
        make_vault,
        body("See [[ghost]]."),
        dangling(
            "ghost", "no page is named ghost", *choose(*stubs("ghost"), drop("[[ghost]]", "ghost"))
        ),
    )


@pytest.mark.parametrize("status", ["stub", "draft", "done"])
def test__scat_link_dangling_body__links_are_checked_at_every_status(make_vault, status):
    page = doc("concern", "Safe handling", status=status, body="\nSee [[ghost]].\n")
    r = report_of(make_vault, {C: page})
    assert rules_of(r) == ["SCAT-LINK-DANGLING-BODY"] and r.problems[0].severity == "error"
    assert not r.ok


def test__scat_link_dangling_body__a_name_a_row_end_names_offers_the_layer_that_row_fixes(
    make_vault,
):
    rows = (*DESK_ROWS, row("holds", "borrowers", "ghost"))
    files = {**body("See [[ghost]]."), DESK: narrative(rows=rows)}
    r = report_of(make_vault, files)
    assert [(p.rule, p.file) for p in r.problems] == [
        ("SCAT-LINK-DANGLING-BODY", C),
        ("SCAT-DONE-END-NOPAGE", DESK),
    ]
    assert r.problems[0].render() == dangling(
        "ghost",
        "no page is named ghost",
        *choose(*stubs("ghost", ["concern"]), drop("[[ghost]]", "ghost")),
    )


def test__scat_link_dangling_body__a_name_two_row_ends_name_in_two_layers_offers_both(make_vault):
    rows = (
        *DESK_ROWS,
        row("holds", "borrowers", "ghost"),
        row("is provided by", "ghost", "booking-app"),
    )
    r = report_of(make_vault, {**body("See [[ghost]]."), DESK: narrative(rows=rows)})
    assert r.problems[0].render() == dangling(
        "ghost",
        "no page is named ghost",
        *choose(*stubs("ghost", ["affordance", "concern"]), drop("[[ghost]]", "ghost")),
    )


def test__scat_link_dangling_body__near_match_comes_first(make_vault):
    seeded(
        make_vault,
        body("See [[safe-handlin]]."),
        dangling(
            "safe-handlin",
            "no page is named safe-handlin",
            *choose(
                f"on line {LINE} replace `[[safe-handlin]]` with `[[safe-handling]]`",
                *stubs("safe-handlin"),
                drop("[[safe-handlin]]", "safe-handlin"),
            ),
        ),
    )


def test__scat_link_dangling_body__wrong_case_is_variant_c_and_replaces_with_the_derived_name(
    make_vault,
):
    seeded(
        make_vault,
        body("See [[Safe-Handling]]."),
        dangling(
            "Safe-Handling",
            "Safe-Handling is not a legal page name: it contains `S`, outside a-z, 0-9 and -",
            *choose(
                f"on line {LINE} replace `[[Safe-Handling]]` with `[[safe-handling]]`",
                drop("[[Safe-Handling]]", "Safe-Handling"),
            ),
        ),
    )


def test__scat_link_dangling_body__illegal_name_with_no_page_replaces_then_stubs(make_vault):
    seeded(
        make_vault,
        body("See [[Safety briefing]]."),
        dangling(
            "Safety briefing",
            "Safety briefing is not a legal page name: it contains `S`, outside a-z, 0-9 and -",
            *choose(
                *[
                    f"on line {LINE} replace `[[Safety briefing]]` with `[[safety-briefing]]`, then "
                    f"{s}"
                    for s in stubs("safety-briefing")
                ],
                drop("[[Safety briefing]]", "Safety briefing"),
            ),
        ),
    )


def test__scat_link_dangling_body__a_derived_name_that_is_a_page_is_a_plain_replacement(make_vault):
    seeded(
        make_vault,
        body("See [[Careful keeping]]."),
        dangling(
            "Careful keeping",
            "Careful keeping is not a legal page name: it contains `C`, outside a-z, 0-9 and -",
            *choose(
                f"on line {LINE} replace `[[Careful keeping]]` with `[[careful-keeping]]`",
                drop("[[Careful keeping]]", "Careful keeping"),
            ),
        ),
    )


def test__scat_link_dangling_body__non_latin_name_needs_a_hand_choice(make_vault):
    seeded(
        make_vault,
        body("See [[Привет]]."),
        dangling(
            "Привет",
            "Привет is not a legal page name: it contains `П`, outside a-z, 0-9 and -",
            "Fix: " + drop("[[Привет]]", "Привет"),
            "choose a legal page name by hand (page contracts section 2), then write the link with it",
        ),
    )


def test__scat_link_dangling_body__file_without_type_is_variant_b(make_vault):
    files = {**body("See [[notes]]."), "notes.md": "no type\n"}
    seeded(
        make_vault,
        files,
        dangling(
            "notes",
            "notes.md exists but has no `type`, so it is not a page",
            *choose(
                *[
                    "put these lines in a block between two `---` lines at the very top of notes.md: "
                    f'`type: {k}`, `status: stub`, `title: "Notes"`'
                    for k in TYPES
                ],
                drop("[[notes]]", "notes"),
            ),
        ),
    )


def test__scat_link_dangling_body__file_with_frontmatter_but_no_type_lists_the_missing_keys(
    make_vault,
):
    files = {**body("See [[notes]]."), "notes.md": "---\ntitle: Notes\n---\n"}
    r = report_of(make_vault, files)
    (p,) = r.problems
    assert (
        "add these lines to the frontmatter of notes.md: `type: concern`, `status: stub`" in p.fix
    )
    assert '`title: "Notes"`' not in p.fix  # the key it has stays


def test__scat_link_dangling_body__group_at_the_cap_withholds_the_group_option(make_vault):
    files = {**body("See [[ghost]]."), "group/third.md": doc("group", "Third")}
    r = report_of(make_vault, files)
    (p,) = r.problems
    assert [o.text for o in p.fix_data.options] == [
        *stubs("ghost", [k for k in TYPES if k != "group"]),
        drop("[[ghost]]", "ghost"),
    ]
    assert p.fix.split("\n")[-1] == (
        "(the vault is at its cap of 3 groups, so a new group page would break SCAT-CAP; "
        "choose an existing group)"
    )


def test__scat_link_dangling_body__group_under_the_cap_offers_the_group_option(make_vault):
    (p,) = report_of(make_vault, body("See [[ghost]].")).problems
    assert any("--type group" in o.text for o in p.fix_data.options)


def test__scat_link_dangling_body__a_link_in_a_note_cell_is_a_body_link(make_vault):
    rows = (*DESK_ROWS, row("holds", "staff", "quick-checkout", "See [[ghost]]"))
    r = report_of(make_vault, {DESK: narrative(rows=rows)})
    assert [(p.rule, p.file, p.line) for p in r.problems] == [("SCAT-LINK-DANGLING-BODY", DESK, 19)]


def test__scat_link_dangling_body__a_row_end_is_graded_by_the_end_rule_and_not_this_one(make_vault):
    rows = (*DESK_ROWS, row("holds", "staff", "ghost"))
    assert rules_of(report_of(make_vault, {DESK: narrative(rows=rows)})) == ["SCAT-DONE-END-NOPAGE"]


def test__scat_link_dangling_body__links_in_a_table_with_a_malformed_header_are_body_links(
    make_vault,
):
    page = narrative(status="draft").replace(
        "| from | type | to | note |", "| from | kind | to | note |"
    )
    page = page.replace("[[safe-handling]] | |", "[[ghost]] | |")
    r = report_of(make_vault, {DESK: page})
    assert rules_of(r) == ["SCAT-DRAFT-TABLE-HEADER", "SCAT-LINK-DANGLING-BODY"]


@pytest.mark.parametrize(
    "text",
    [
        "[[photo.png]]",
        "[[v1.2-notes]]",
        "[[#Heading]]",
        "[[folder/file]]",
        "`[[ghost]]`",
        "[[^blk]]",
        "[ghost](ghost)",
    ],
)
def test__scat_link_dangling_body__names_that_are_not_page_links_give_none(make_vault, text):
    seeded(make_vault, body(f"See {text}."))


def test__scat_link_dangling_body__a_link_in_a_fenced_code_block_gives_none(make_vault):
    seeded(make_vault, body("```\n[[ghost]]\n```"))


def test__scat_link_dangling_body__block_reference_names_the_page_before_the_caret(make_vault):
    r = report_of(make_vault, body("See [[ghost^abc123]]."))
    assert [p.where for p in r.problems] == ["link [[ghost]]"]
    assert r.problems[0].fix_data.options[-1].edits[0].find == "[[ghost^abc123]]"


def test__scat_link_dangling_body__an_alias_is_kept_by_a_replacement_and_a_drop_keeps_the_alias_words(
    make_vault,
):
    r = report_of(make_vault, body("See [[safe-handlin|the briefing]]."))
    (p,) = r.problems
    first, *_, last = p.fix_data.options
    assert first.edits[0].find == "[[safe-handlin|the briefing]]"
    assert first.edits[0].replace == "[[safe-handling|the briefing]]"
    assert last.edits[0].replace == "the briefing"
    assert (first.edits[0].line, first.edits[0].column) == (LINE, 5)


def test__scat_link_dangling_body__same_link_twice_on_a_line_is_one_message_with_a_count(
    make_vault,
):
    r = report_of(make_vault, body("See [[ghost]] and [[ghost]]."))
    assert len(r.problems) == 1 and r.problems[0].repeat == 2
    assert "(x2)" in r.problems[0].render().split("\n")[0]


# SCAT-MENTION


def mention(file, line, column, written, name, kind, link=None):
    link = link or (f"[[{name}]]" if written == name else f"[[{name}|{written}]]")
    return msg(
        f"warning [SCAT-MENTION] {file}:{line}:{column} text `{written}`: names the {kind} page "
        f"[[{name}]] but does not link it",
        f"Fix: on line {line} replace `{written}` with `{link}`",
    )


def test__scat_mention__title_in_plain_text_on_a_narrative(make_vault):
    seeded(
        make_vault,
        {DESK: narrative(account=ACCOUNT + "\nThe volunteers gave a Briefing first.\n")},
        mention(DESK, 12, 23, "Briefing", "briefing", "affordance"),
    )


def test__scat_mention__a_node_page_mentioning_another_nodes_title(make_vault):
    seeded(
        make_vault,
        body("Needs a briefing before use."),
        mention(C, 8, 9, "briefing", "briefing", "affordance"),
    )


def test__scat_mention__case_is_ignored_and_the_text_is_kept_as_written(make_vault):
    seeded(
        make_vault,
        body("Needs a BRIEFING."),
        mention(C, 8, 9, "BRIEFING", "briefing", "affordance", "[[briefing|BRIEFING]]"),
    )


def test__scat_mention__the_page_name_gets_a_plain_link_and_the_title_an_alias(make_vault):
    page = doc("concern", "Safe handling", body="\nSee booking-app and the Booking App.\n")
    r = report_of(make_vault, {C: page})
    assert [p.fix.split("`") for p in r.problems] == [
        ["Fix: on line 8 replace ", "booking-app", " with ", "[[booking-app]]", ""]
    ]


def test__scat_mention__a_title_with_a_space_is_matched_as_written(make_vault):
    seeded(
        make_vault,
        body("Use the booking app."),
        mention(C, 8, 9, "booking app", "booking-app", "technology"),
    )


def test__scat_mention__reported_once_at_the_first_occurrence(make_vault):
    r = report_of(make_vault, body("A briefing, then a briefing."))
    assert [(p.line, p.column) for p in r.problems] == [(8, 3)]


def test__scat_mention__in_a_note_cell_one_message(make_vault):
    rows = (
        *DESK_ROWS[:2],
        row("is addressed by", "quick-checkout", "self-checkout", "after a briefing"),
    )
    seeded(
        make_vault,
        {DESK: narrative(rows=rows)},
        mention(DESK, 18, 70, "briefing", "briefing", "affordance"),
    )


def test__scat_mention__plain_text_in_a_from_cell_is_not_this_rules(make_vault):
    rows = (*DESK_ROWS, "| briefing | holds | [[quick-checkout]] | |")
    r = report_of(make_vault, {DESK: narrative(rows=rows)})
    assert "SCAT-MENTION" not in rules_of(r)


@pytest.mark.parametrize(
    "text",
    [
        "A briefing, see [[briefing]].",
        "`briefing` in code",
        "```\nbriefing\n```",
        "[[quick-checkout|briefing]]",
        "the brief",
        "booking-apps",
    ],
)
def test__scat_mention__linked_in_code_in_a_wikilink_or_not_a_whole_word_gives_none(
    make_vault, text
):
    seeded(make_vault, body(text))


def test__scat_mention__the_pages_own_title_gives_none(make_vault):
    seeded(make_vault, body("Safe handling matters; so does safe-handling."))


def test__scat_mention__short_names_are_not_matched(make_vault):
    files = {"technology/app.md": doc("technology", "App"), **body("Open the app.")}
    seeded(make_vault, files)


def test__scat_mention__a_warning_does_not_block_at_any_status(make_vault):
    for status in ("stub", "draft", "done"):
        r = report_of(
            make_vault, {DESK: narrative(status=status, account=ACCOUNT + "\nA Briefing.\n")}
        )
        assert rules_of(r) == ["SCAT-MENTION"] and r.ok


# SCAT-MENTION: the page type (D-100, W10a) and a hyphenated title (W10b)

GROUPED = "The Volunteers met afterwards.\n"  # `volunteers` is a group page the desk narrative does not link
TECHNICAL = "They used the Booking App at the desk.\n"  # `booking-app` is a technology page


def mentions_of(make_vault, **kw):
    files = {"group/volunteers.md": doc("group", "Volunteers")}
    r = report_of(make_vault, {DESK: narrative(account=kw.pop("account"), **kw), **files})
    return [
        p.render().split("page [[")[1].split("]]")[0]
        for p in r.problems
        if p.rule == "SCAT-MENTION"
    ]


def test__scat_mention__an_architecture_is_not_offered_a_link_to_a_group(make_vault):
    got = mentions_of(make_vault, kind="architecture", account=GROUPED)
    assert "volunteers" not in got


def test__scat_mention__a_scenario_is_not_offered_a_link_to_a_technology(make_vault):
    assert "booking-app" not in mentions_of(make_vault, kind="scenario", account=TECHNICAL)


def test__scat_mention__a_scenario_naming_a_group_keeps_the_warning(make_vault):
    assert "volunteers" in mentions_of(make_vault, kind="scenario", account=GROUPED)


def test__scat_mention__an_architecture_naming_a_technology_keeps_the_warning(make_vault):
    assert "booking-app" in mentions_of(make_vault, kind="architecture", account=TECHNICAL)


def test__scat_mention__a_narrative_with_no_kind_keeps_both(make_vault):
    assert {"volunteers", "booking-app"} <= set(
        mentions_of(make_vault, kind=None, account=GROUPED + TECHNICAL)
    )


def test__scat_mention__a_node_page_naming_a_group_keeps_the_warning(make_vault):
    seeded(
        make_vault,
        {C: doc("concern", "Safe handling", body="\nAsk the Staff.\n")},
        mention(C, 8, 9, "Staff", "staff", "group"),
    )


GROUP_PAGE = {"group/walk-in-customers.md": doc("group", "Walk in customers")}


@pytest.mark.parametrize(
    "written", ["Walk-in customers", "walk in customers", "walk-in-customers", "WALK-IN CUSTOMERS"]
)
def test__scat_mention__words_match_across_a_space_or_a_hyphen(make_vault, written):
    page = doc("concern", "Safe handling", body=f"\nSee {written} today.\n")
    r = report_of(make_vault, {C: page, **GROUP_PAGE})
    link = (
        "[[walk-in-customers]]"
        if written == "walk-in-customers"
        else f"[[walk-in-customers|{written}]]"
    )
    assert [p.render() for p in r.problems] == [
        mention(C, 8, 5, written, "walk-in-customers", "group", link)
    ]


def test__scat_mention__a_hyphen_or_space_mix_matches_and_other_cuts_do_not(make_vault):
    for body_, hit in (
        ("walk-in customers", True),
        ("walk - in customers", True),
        ("walkin customers", False),
        ("walk-in customer", False),
        ("a walk-in-customerss", False),
    ):
        page = doc("concern", "Safe handling", body=f"\n{body_}\n")
        r = report_of(make_vault, {C: page, **GROUP_PAGE})
        assert ("SCAT-MENTION" in rules_of(r)) is hit, body_


def test__scat_mention__a_title_with_no_word_characters_names_nothing(make_vault):
    files = {"group/dashes.md": doc("group", "-----"), **body("A line ----- and more.")}
    r = report_of(make_vault, files)
    assert "SCAT-MENTION" not in rules_of(r)


# SCAT-CAP and SCAT-CAP-CONFIG

CAP_HEAD = "error [SCAT-CAP] scat.toml field `stakeholder_group_cap`: the vault holds {n} group pages, over the cap of {cap}: {names}"
CAP_FIX = choose(
    "cluster {k} group(s) into the others, by shared standpoint: move their standpoints into another "
    "group's `description`, change every link to them to point at that group, and delete those pages",
    "or, only if the plan allows more groups, write `stakeholder_group_cap = {n}` in scat.toml "
    "(the cap protects against identifying individuals)",
)


def cap_message(n, cap, names):
    fix = [line.format(k=n - cap, n=n) for line in CAP_FIX]
    return msg(CAP_HEAD.format(n=n, cap=cap, names=names), *fix)


GROUPS = {f"group/g-{n}.md": doc("group", f"Group {n}") for n in ("one", "two")}  # with the two: 4


def test__scat_cap__four_groups_over_a_cap_of_three(make_vault):
    seeded(make_vault, GROUPS, cap_message(4, 3, "borrowers, g-one, g-two, staff"))


def test__scat_cap__a_stub_group_still_counts(make_vault):
    files = {"group/third.md": doc("group", "Third", status="stub", description=None), **GROUPS}
    files.pop("group/g-two.md")
    seeded(make_vault, files, cap_message(4, 3, "borrowers, g-one, staff, third"))


def test__scat_cap__at_the_cap_gives_none(make_vault):
    seeded(make_vault, {"group/third.md": doc("group", "Third")})


def test__scat_cap__runs_at_page_scope_only_for_a_group_page(make_vault):
    from scat_kg.checks import check_page

    v = vault_with(make_vault, GROUPS)
    assert rules_of(check_page(v, "group/staff.md")) == ["SCAT-CAP"]
    assert rules_of(check_page(v, "concern/safe-handling.md")) == []


def vault_with(make_vault, files):
    from helpers import vault

    return vault(make_vault, files)


CONFIG_HEAD = "error [SCAT-CAP-CONFIG] scat.toml field `stakeholder_group_cap`: {what}"


def config_fix(verb, groups=2):
    least = f", so choose at least {groups}" if groups >= 1 else ""
    return (
        f"Fix: {verb} `stakeholder_group_cap = <number you choose>` (author) in scat.toml; choose a whole "
        f"number of 1 or more (the vault has {groups} group pages now{least})"
    )


def test__scat_cap_config__file_missing(make_vault):
    seeded(
        make_vault,
        {},
        msg(CONFIG_HEAD.format(what="the file is missing"), config_fix("add the line")),
        remove=("scat.toml",),
    )


def test__scat_cap_config__invalid_toml(make_vault):
    r = report_of(make_vault, {"scat.toml": "stakeholder_group_cap = \n"})
    (p,) = r.problems
    assert p.rule == "SCAT-CAP-CONFIG" and p.what.startswith("the file is not valid TOML: ")
    assert p.fix == config_fix("add the line")


def test__scat_cap_config__key_missing(make_vault):
    seeded(
        make_vault,
        {"scat.toml": "other = 1\n"},
        msg(CONFIG_HEAD.format(what="the key is missing"), config_fix("add the line")),
    )


@pytest.mark.parametrize("written", ['"three"', "0", "2.5", "3.0", "-1", "true"])
def test__scat_cap_config__bad_value_is_replaced(make_vault, written):
    seeded(
        make_vault,
        {"scat.toml": f"stakeholder_group_cap = {written}\n"},
        msg(
            CONFIG_HEAD.format(what=f"the value `{written}` is not a TOML integer of 1 or more"),
            config_fix(f"replace the line `stakeholder_group_cap = {written}` with"),
        ),
    )


def test__scat_cap_config__no_groups_drops_the_at_least_clause(make_vault):
    files = {p: t for p, t in base_files().items() if not p.startswith("group/")}
    r = report_of(
        make_vault,
        {},
        remove=[p for p in base_files() if p.startswith("group/")]
        + [DESK, "narrative/kiosk-pitch.md"],
    )
    assert r.problems == () or rules_of(r) == []
    del files
    r = report_of(
        make_vault,
        {"scat.toml": "stakeholder_group_cap = 0\n"},
        remove=[p for p in base_files() if p.startswith("group/")]
        + [DESK, "narrative/kiosk-pitch.md"],
    )
    (p,) = r.problems
    assert p.fix.endswith("(the vault has 0 group pages now)")


def base_files():
    from helpers import base

    return base()


def test__scat_link_dangling_body__two_links_on_one_line_are_listed_in_position_order(make_vault):
    r = report_of(make_vault, body("[[zeta]] then [[alpha]]."))
    assert [p.where for p in r.problems] == ["link [[zeta]]", "link [[alpha]]"]


def test__scat_mention__in_a_table_cell_the_alias_bar_is_escaped(make_vault):
    rows = (
        *DESK_ROWS[:2],
        row("is addressed by", "quick-checkout", "self-checkout", "after a BRIEFING"),
    )
    r = report_of(make_vault, {DESK: narrative(rows=rows)})
    (p,) = r.problems
    assert p.fix == "Fix: on line 18 replace `BRIEFING` with `[[briefing\\|BRIEFING]]`"
    assert p.fix_data.options[0].edits[0].replace == "[[briefing\\|BRIEFING]]"


# SCAT-MENTION is a link suggestion: off unless scat.toml says `link_suggestions = true` (WP21-G9, R10)

SUGGEST = "link_suggestions = true\n"


def test__scat_mention__is_off_by_default_and_reported_with_the_switch_on(make_vault):
    files = {DESK: narrative(account=ACCOUNT + "\nThe volunteers gave a Briefing first.\n")}
    default = {"scat.toml": "stakeholder_group_cap = 3\n", **files}
    assert "SCAT-MENTION" not in rules_of(report_of(make_vault, default))
    for off in ("link_suggestions = false\n", ""):
        text = {"scat.toml": "stakeholder_group_cap = 3\n" + off, **files}
        assert "SCAT-MENTION" not in rules_of(report_of(make_vault, text))
    on = {"scat.toml": "stakeholder_group_cap = 3\n" + SUGGEST, **files}
    assert rules_of(report_of(make_vault, on)) == ["SCAT-MENTION"]


SUGGEST_HEAD = "error [SCAT-SUGGEST-CONFIG] scat.toml field `link_suggestions`: {what}"


@pytest.mark.parametrize("written", ['"yes"', "1", "0", "'true'"])
def test__scat_suggest_config__a_value_that_is_not_a_boolean_is_refused(make_vault, written):
    seeded(
        make_vault,
        {"scat.toml": f"stakeholder_group_cap = 3\nlink_suggestions = {written}\n"},
        msg(
            SUGGEST_HEAD.format(
                what=f"the value `{written}` is not a TOML boolean, `true` or `false`"
            ),
            *choose(
                f"replace the line `link_suggestions = {written}` with `link_suggestions = true` "
                "(show the link suggestions)",
                "or with `link_suggestions = false` (the default: no link suggestions)",
            ),
        ),
    )


def test__scat_suggest_config__a_boolean_or_no_key_is_not_a_problem(make_vault):
    for text in ("link_suggestions = true\n", "link_suggestions = false\n", ""):
        r = report_of(make_vault, {"scat.toml": f"stakeholder_group_cap = 3\n{text}"})
        assert "SCAT-SUGGEST-CONFIG" not in rules_of(r)
