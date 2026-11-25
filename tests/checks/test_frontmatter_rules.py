"""Seeded defects for the SCAT-FM-* rules and SCAT-NAME. Test names carry the rule id (see test_coverage)."""

import pytest
from helpers import DESK, choose, doc, msg, narrative, report_of, rules_of, seeded, set_status

C = "concern/safe-handling.md"
K = "concern/careful-keeping.md"  # no row of the fixture narratives names it
PARSE_FIX = (
    "Fix: make the frontmatter a block of `key: value` lines between two lines containing only `---`, "
    "at the very top of the file; start from the first line the parser rejected"
)
FIVE = (
    "`type: affordance` (One page per affordance: what is offered. The technologies that provide it "
    "are told by narratives.)",
    "`type: concern` (One page per concern: what the interest is. Who holds it and what addresses it "
    "are told by narratives.)",
    "`type: group` (One page per group: who the group is, in the group's own terms. The concerns it "
    "holds are told by narratives.)",
    "`type: narrative` (A narrative: the account in the page body, with links where names appear, "
    "and under the heading Edges told a table with one row for each edge the account tells.)",
    "`type: technology` (One page per technology: what the part is.)",
)


def head(rule, file, where, what, line=None):
    place = file if line is None else f"{file}:{line}"
    return f"error [{rule}] {place} {where}: {what}"


# SCAT-FM-PARSE


def test__scat_fm_parse__closing_line_missing(make_vault):
    seeded(
        make_vault,
        {C: "---\ntype: concern\nstatus: done\ntitle: x\n"},
        msg(head("SCAT-FM-PARSE", C, "frontmatter", "the closing --- line is missing"), PARSE_FIX),
    )


def test__scat_fm_parse__tab_indented_key(make_vault):
    bad = "---\ntype: concern\n\tstatus: done\n---\n"
    r = seeded(
        make_vault,
        {C: bad},
        msg(
            head(
                "SCAT-FM-PARSE",
                C,
                "frontmatter",
                "found character '\\t' that cannot start any token",
                3,
            ),
            PARSE_FIX,
        ),
    )
    assert r.problems[0].line == 3  # the line the parser rejected


def test__scat_fm_parse__colon_in_title(make_vault):
    bad = "---\ntype: concern\nstatus: done\ntitle: a: b\n---\n"
    r = report_of(make_vault, {C: bad})
    assert rules_of(r) == ["SCAT-FM-PARSE"]
    assert r.problems[0].line == 4 and r.problems[0].fix == PARSE_FIX


def test__scat_fm_parse__clean_cases_give_none(make_vault):
    crlf = (
        '---\r\ntype: concern\r\nstatus: done\r\ntitle: "S"\r\ndescription: "D"\r\n---\r\nbody\r\n'
    )
    seeded(make_vault, {C: crlf, "README.md": "# Not a page\n", "notes/loose.md": "no frontmatter\n"})
    # frontmatter with no `type` is no page either
    seeded(make_vault, {"notes/typeless.md": "---\ntitle: x\n---\n"})


def test__scat_fm_parse__an_unreadable_page_is_no_source_for_any_other_rule(make_vault):
    bad = "---\ntype: concern\n\tstatus: done\n---\n"
    assert rules_of(report_of(make_vault, {C: bad})) == ["SCAT-FM-PARSE"]


# SCAT-FM-REQUIRED

TITLE = (
    "the page name with each - replaced by a space and the first letter upper case; "
    "reword it if you like"
)
STATUS_FIX = (
    f"Fix: run {set_status('safe-handling')}; use `stub` or `done` instead of `draft` if that is the truth"
)


def test__scat_fm_required__status_missing(make_vault):
    seeded(
        make_vault,
        {C: doc("concern", "Safe handling", status=None)},
        msg(head("SCAT-FM-REQUIRED", C, "field `status`", "missing"), STATUS_FIX),
    )


def test__scat_fm_required__status_present_but_empty(make_vault):
    page = '---\ntype: concern\nstatus:\ntitle: "Safe handling"\ndescription: "D"\n---\n'
    seeded(
        make_vault,
        {C: page},
        msg(head("SCAT-FM-REQUIRED", C, "field `status`", "missing"), STATUS_FIX),
    )


@pytest.mark.parametrize("status", ["stub", "draft", "done"])
def test__scat_fm_required__title_missing_at_each_status(make_vault, status):
    page = f"---\ntype: concern\nstatus: {status}\ndescription: D\n---\n"
    seeded(
        make_vault,
        {C: page},
        msg(
            head("SCAT-FM-REQUIRED", C, "field `title`", "missing"),
            f'Fix: add the line `title: "Safe handling"` ({TITLE})',
        ),
    )


def test__scat_fm_required__title_empty_is_replaced(make_vault):
    page = "---\ntype: concern\nstatus: stub\ntitle:\n---\n"
    seeded(
        make_vault,
        {C: page},
        msg(
            head("SCAT-FM-REQUIRED", C, "field `title`", "missing"),
            f'Fix: replace the line `title:` with `title: "Safe handling"` ({TITLE})',
        ),
    )


def test__scat_fm_required__a_narrative_as_well_as_a_node_page(make_vault):
    page = narrative(status="draft").replace('title: "Desk day"\n', "")
    seeded(
        make_vault,
        {DESK: page},
        msg(
            head("SCAT-FM-REQUIRED", DESK, "field `title`", "missing"),
            f'Fix: add the line `title: "Desk day"` ({TITLE})',
        ),
    )


# SCAT-FM-TYPE


def test__scat_fm_type__near_match_is_exact(make_vault):
    seeded(
        make_vault,
        {K: doc("Concern", "Careful keeping")},
        msg(
            head("SCAT-FM-TYPE", K, "field `type`", "`Concern` is not a page type"),
            "Fix: change it to `type: concern`",
        ),
    )


def test__scat_fm_type__no_near_match_lists_the_five(make_vault):
    seeded(
        make_vault,
        {K: doc("gadget", "Careful keeping")},
        msg(
            head("SCAT-FM-TYPE", K, "field `type`", "`gadget` is not a page type"),
            *choose(*FIVE, head="Fix, choose the one that describes this page:"),
        ),
    )


@pytest.mark.parametrize("line", ["type:", "type: null", 'type: ""', 'type: "   "'])
def test__scat_fm_type__an_empty_type_lists_the_five(make_vault, line):
    page = f"---\n{line}\nstatus: done\ntitle: Careful keeping\ndescription: D\n---\n"
    seeded(
        make_vault,
        {K: page},
        msg(
            head(
                "SCAT-FM-TYPE",
                K,
                "field `type`",
                "the value is empty, which is not a page type",
            ),
            *choose(*FIVE, head="Fix, choose the one that describes this page:"),
        ),
    )


def test__scat_fm_type__index_is_a_wrong_type_and_the_note_says_where_an_index_comes_from(make_vault):
    page = doc("index", "Safe handling")
    r = report_of(make_vault, {K: page})
    first = r.problems[0]
    assert first.rule == "SCAT-FM-TYPE" and first.what == "`index` is not a page type"
    assert first.fix.split("\n")[-1] == (
        "(an index is generated by `scat index`; it is a Base file and not a page)"
    )
    assert first.fix.split("\n")[0] == "Fix, choose the one that describes this page:"


def test__scat_fm_type__an_invalid_type_is_checked_by_no_rule_that_needs_it(make_vault):
    # no title, no description, a status error: the page has no usable type, so only its type is reported
    page = "---\ntype: gadget\nstatus: finished\n---\n"
    r = report_of(make_vault, {"affordance/odd.md": page})
    assert [(p.rule, p.file) for p in r.problems] == [("SCAT-FM-TYPE", "affordance/odd.md")]


def test__scat_fm_type__a_row_end_that_links_the_page_gives_no_end_message_for_its_type(make_vault):
    # the end rules judge a page that is not a node: SCAT-*-END-NOTNODE, once; the page's own error is separate
    rows = ("| holds | [[staff]] | [[odd]] | |",)
    odd = "concern/odd.md"
    r = report_of(
        make_vault,
        {odd: doc("gadget", "Odd"), DESK: narrative(rows=rows, status="draft")},
    )
    assert sorted(rules_of(r)) == ["SCAT-DRAFT-END-NOTNODE", "SCAT-FM-TYPE"]


# SCAT-FM-STATUS


def test__scat_fm_status__near_match_is_exact(make_vault):
    seeded(
        make_vault,
        {C: doc("concern", "Safe handling", status="Done")},
        msg(
            head("SCAT-FM-STATUS", C, "field `status`", "`Done` is not a status"),
            "Fix: change it to `status: done`",
        ),
    )


def test__scat_fm_status__no_near_match_is_a_choice(make_vault):
    seeded(
        make_vault,
        {C: doc("concern", "Safe handling", status="finished")},
        msg(
            head("SCAT-FM-STATUS", C, "field `status`", "`finished` is not a status"),
            "Fix, choose one: `status: stub` (just started), `status: draft` (being written), "
            "`status: done` (finished)",
        ),
    )


def test__scat_fm_status__a_narrative_with_an_invalid_status_gets_none_of_the_needs_status_rules(
    make_vault,
):
    page = narrative(status="finished", description=None, timeframe=None).replace(
        "| holds | [[staff]] | [[safe-handling]] | |", "| holds | [[staff]] | [[ghost]] | |"
    )
    r = report_of(make_vault, {DESK: page})
    assert rules_of(r) == ["SCAT-FM-STATUS"]


# SCAT-FM-TIMEFRAME and SCAT-FM-KIND

VALUES = ("past", "future", "mixed")


@pytest.mark.parametrize("value", VALUES)
def test__scat_fm_timeframe__each_valid_value_is_clean_at_each_status(make_vault, value):
    for status in ("stub", "draft", "done"):
        seeded(make_vault, {DESK: narrative(status=status, timeframe=value)})


@pytest.mark.parametrize("status", ["stub", "draft", "done"])
def test__scat_fm_timeframe__near_match_is_exact(make_vault, status):
    seeded(
        make_vault,
        {DESK: narrative(status=status, timeframe="Past")},
        msg(
            head("SCAT-FM-TIMEFRAME", DESK, "field `timeframe`", "`Past` is not a timeframe"),
            "Fix: change it to `timeframe: past`",
        ),
    )


@pytest.mark.parametrize("status", ["stub", "draft", "done"])
def test__scat_fm_timeframe__no_near_match_lists_the_three(make_vault, status):
    r = seeded(
        make_vault,
        {DESK: narrative(status=status, timeframe="soon")},
        msg(
            head("SCAT-FM-TIMEFRAME", DESK, "field `timeframe`", "`soon` is not a timeframe"),
            *choose(*[f"`timeframe: {v}`" for v in VALUES]),
        ),
    )
    assert not r.ok


def test__scat_fm_timeframe__only_a_narrative_has_the_field(make_vault):
    seeded(make_vault, {C: doc("concern", "Safe handling", extra="timeframe: soon")})


def test__scat_fm_kind__near_match_offers_the_change_and_the_delete(make_vault):
    seeded(
        make_vault,
        {DESK: narrative(kind="Scenario")},
        msg(
            head("SCAT-FM-KIND", DESK, "field `kind`", "`Scenario` is not a kind"),
            *choose(
                "change it to `kind: scenario`",
                "delete the line `kind: Scenario`: a narrative that is neither a scenario nor an "
                "architecture leaves `kind` out",
            ),
        ),
    )


def test__scat_fm_kind__no_near_match_offers_the_two_values_and_the_delete(make_vault):
    seeded(
        make_vault,
        {DESK: narrative(kind="story")},
        msg(
            head("SCAT-FM-KIND", DESK, "field `kind`", "`story` is not a kind"),
            *choose(
                "`kind: scenario`",
                "`kind: architecture`",
                "delete the line `kind: story`: a narrative that is neither a scenario nor an "
                "architecture leaves `kind` out",
            ),
        ),
    )


@pytest.mark.parametrize("kind", ["scenario", "architecture", None])
def test__scat_fm_kind__a_value_of_the_set_and_no_kind_at_all_are_clean(make_vault, kind):
    seeded(make_vault, {DESK: narrative(kind=kind)})


def test__scat_fm_kind__an_empty_kind_is_no_defect(make_vault):
    page = narrative().replace("kind: scenario", "kind:")
    seeded(make_vault, {DESK: page})


# SCAT-FM-SHAPE


def test__scat_fm_shape__one_item_list_is_exact(make_vault):
    page = '---\ntype: concern\nstatus: done\ntitle:\n  - "Safe handling"\ndescription: "D"\n---\n'
    seeded(
        make_vault,
        {C: page},
        msg(
            head(
                "SCAT-FM-SHAPE",
                C,
                "field `title`",
                "expected one line of text, found a list",
            ),
            'Fix: replace the field with the line `title: "Safe handling"`',
        ),
    )


def test__scat_fm_shape__mapping_has_no_exact_fix(make_vault):
    page = '---\ntype: concern\nstatus: done\ntitle:\n  a: b\ndescription: "D"\n---\n'
    seeded(
        make_vault,
        {C: page},
        msg(
            head(
                "SCAT-FM-SHAPE",
                C,
                "field `title`",
                "expected one line of text, found a mapping",
            ),
            "Fix: replace the field with one line of text you write",
        ),
    )


def test__scat_fm_shape__unquoted_yes_is_quoted(make_vault):
    page = '---\ntype: concern\nstatus: done\ntitle: yes\ndescription: "D"\n---\n'
    seeded(
        make_vault,
        {C: page},
        msg(
            head(
                "SCAT-FM-SHAPE",
                C,
                "field `title`",
                "expected one line of text, found a boolean",
            ),
            'Fix: replace the field with the line `title: "yes"`',
        ),
    )


def test__scat_fm_shape__a_number_is_quoted(make_vault):
    page = '---\ntype: concern\nstatus: done\ntitle: "S"\ndescription: 42\n---\n'
    seeded(
        make_vault,
        {C: page},
        msg(
            head(
                "SCAT-FM-SHAPE",
                C,
                "field `description`",
                "expected one line of text, found a number",
            ),
            'Fix: replace the field with the line `description: "42"`',
        ),
    )


def test__scat_fm_shape__timeframe_and_kind_on_a_narrative_are_checked_too(make_vault):
    page = narrative().replace("timeframe: past", "timeframe: 1").replace("kind: scenario", "kind: yes")
    r = report_of(make_vault, {DESK: page})
    assert [(p.rule, p.where) for p in r.problems] == [
        ("SCAT-FM-SHAPE", "field `kind`"),
        ("SCAT-FM-SHAPE", "field `timeframe`"),
    ]


def test__scat_fm_shape__null_is_missing_not_shape(make_vault):
    page = '---\ntype: concern\nstatus: done\ntitle: "S"\ndescription: ~\n---\n'
    assert rules_of(report_of(make_vault, {C: page})) == ["SCAT-DONE-FIELD"]


# SCAT-NAME


def name_fix(old, new):
    return (
        f"Fix: change the file name to `{new}.md`, then change the links that meant this page "
        f"from `[[{old}]]` to `[[{new}]]`"
    )


def name_head(path, old, why):
    return head("SCAT-NAME", path, "frontmatter", f"the page name `{old}` {why}")


def test__scat_name__space_and_capital(make_vault):
    path = "concern/Safe Tool.md"
    seeded(
        make_vault,
        {path: doc("concern", "Safe Tool")},
        msg(
            name_head(path, "Safe Tool", "is not legal (it contains `S`, outside a-z, 0-9 and -)"),
            name_fix("Safe Tool", "safe-tool"),
        ),
    )


def test__scat_name__over_64_characters(make_vault):
    old = "a" * 65
    path = f"concern/{old}.md"
    seeded(
        make_vault,
        {path: doc("concern", "Long thing")},
        msg(
            name_head(path, old, "is not legal (it is longer than 64 characters)"),
            name_fix(old, "long-thing"),
        ),
    )


def test__scat_name__reserved_name(make_vault):
    path = "concern/con.md"
    seeded(
        make_vault,
        {path: doc("concern", "Con")},
        msg(
            name_head(path, "con", "is not legal (it is a reserved name)"),
            name_fix("con", "con-2"),
        ),
    )


def test__scat_name__doubled_hyphen(make_vault):
    path = "concern/a--b.md"
    seeded(
        make_vault,
        {path: doc("concern", "A b")},
        msg(
            name_head(path, "a--b", "is not legal (it has two hyphens in a row)"),
            name_fix("a--b", "a-b"),
        ),
    )


def test__scat_name__accented_title_derives_ascii(make_vault):
    path = "concern/Café menu.md"
    seeded(
        make_vault,
        {path: doc("concern", "Café menu")},
        msg(
            name_head(path, "Café menu", "is not legal (it contains `C`, outside a-z, 0-9 and -)"),
            name_fix("Café menu", "cafe-menu"),
        ),
    )


def test__scat_name__non_latin_title_needs_a_hand_choice(make_vault):
    path = "concern/Привет.md"
    seeded(
        make_vault,
        {path: doc("concern", "Привет")},
        msg(
            name_head(path, "Привет", "is not legal (it contains `П`, outside a-z, 0-9 and -)"),
            "Fix: choose a legal name by hand (contract section 2)",
        ),
    )


def test__scat_name__names_that_differ_only_by_case_are_one_message_on_the_illegal_name(make_vault):
    seeded(
        make_vault,
        {
            "concern/safety.md": doc("concern", "Safety"),
            "affordance/Safety.md": doc("affordance", "Safety"),
        },
        msg(
            name_head(
                "affordance/Safety.md", "Safety", "is not legal (it contains `S`, outside a-z, 0-9 and -)"
            ),
            name_fix("Safety", "safety-2"),
        ),
    )


def test__scat_name__same_name_in_two_folders_reports_the_later_path(make_vault):
    path, other = "concern/quick-checkout.md", "affordance/quick-checkout.md"  # `affordance/` sorts first
    seeded(
        make_vault,
        {other: doc("affordance", "Quick checkout")},
        msg(
            name_head(path, "quick-checkout", f"is also the name of {other}"),
            name_fix("quick-checkout", "quick-checkout-2")
            + " (two pages share the name: change only the links that meant this page; "
            "the links meant for the other page keep `[[quick-checkout]]`)",
        ),
    )


def test__scat_name__the_edits_rename_the_file_then_every_link_of_the_old_name(make_vault):
    path = "concern/Safe Tool.md"
    page = doc("concern", "Safe Tool")
    link_page = doc("concern", "Other thing", body="\nSee [[Safe Tool|the tool]] and [[ Safe Tool ]].\n")
    r = report_of(make_vault, {path: page, "concern/other-thing.md": link_page})
    (p,) = [p for p in r.problems if p.rule == "SCAT-NAME"]
    (option,) = p.fix_data.options
    assert [(e.action, e.file) for e in option.edits] == [
        ("rename-file", path),
        ("replace-text", "concern/other-thing.md"),
        ("replace-text", "concern/other-thing.md"),
    ]
    assert option.edits[0].to == "concern/safe-tool.md"
    assert [(e.find, e.replace, e.line, e.column) for e in option.edits[1:]] == [
        ("[[Safe Tool|the tool]]", "[[safe-tool|the tool]]", 8, 5),
        ("[[ Safe Tool ]]", "[[ safe-tool ]]", 8, 32),
    ]


def test__scat_name__two_pages_with_a_clean_name_each_give_none(make_vault):
    seeded(make_vault, {"concern/careful-handling.md": doc("concern", "Careful handling")})
