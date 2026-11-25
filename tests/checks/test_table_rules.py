"""The pairs of a narrative's table: SCAT-DRAFT-TABLE-* and SCAT-DONE-TABLE-*.

A pair has one seed set, run three times: at `stub` and `draft` (the DRAFT id, a warning) and at `done` (the DONE id,
an error), with the same message but for the id and severity. The narrative's table has its header on line 14, its
separator on line 15 and row n on line 15 + n. Test names carry the rule id of the DRAFT form (see test_coverage).
"""

import pytest
from helpers import (
    DESK,
    HEADER,
    SEP,
    choose,
    doc,
    msg,
    narrative,
    pair,
    report_of,
    row,
    rules_of,
    seeded,
    table,
)

STATUSES = pytest.mark.parametrize("status", ["stub", "draft", "done"])
F = DESK + ":"
VERBS = "(holds, is addressed by, is provided by)"
DELETE = "delete the row"


def with_rows(status, *rows, **kw):
    return {DESK: narrative(status=status, rows=rows, **kw)}


def with_section(status, section):
    return {DESK: narrative(status=status, section=section)}


# SCAT-DRAFT-TABLE-HEADER


def header(status, what):
    return pair("TABLE-HEADER", status, f"{F}14:1 table header: {what}")


GOOD = row("holds", "staff", "safe-handling")


@STATUSES
def test__scat_draft_table_header__the_old_order_type_from_to_note_says_how_to_reorder(
    make_vault, status
):
    old = "| type | from | to | note |"
    seeded(
        make_vault,
        with_section(
            status, f"## Edges told\n\n{old}\n{SEP}\n| holds | [[staff]] | [[safe-handling]] | |\n"
        ),
        msg(
            header(status, f"the header row is `{old}`, not `{HEADER}`"),
            "Fix: reorder the columns to `from`, `type`, `to`, `note`: in the header and in every row, "
            "move the cells into this order; the tool never moves cells",
        ),
    )


@STATUSES
def test__scat_draft_table_header__the_four_names_in_another_order_is_advisory(make_vault, status):
    bad = "| from | to | type | note |"
    seeded(
        make_vault,
        with_section(status, table(GOOD, header=bad)),
        msg(
            header(status, f"the header row is `{bad}`, not `{HEADER}`"),
            "Fix: reorder the columns to `from`, `type`, `to`, `note`: in the header and in every row, "
            "move the cells into this order; the tool never moves cells",
        ),
    )


@STATUSES
def test__scat_draft_table_header__a_wrong_name_is_one_exact_edit(make_vault, status):
    bad = "| from | kind | to | note |"
    r = seeded(
        make_vault,
        with_section(status, table(GOOD, header=bad)),
        msg(
            header(status, f"the header row is `{bad}`, not `{HEADER}`"),
            f"Fix: replace the line `{bad}` with `{HEADER}`",
        ),
    )
    (edit,) = r.problems[0].fix_data.options[0].edits
    assert (edit.action, edit.line, edit.find, edit.replace) == ("replace-text", 14, bad, HEADER)


@STATUSES
def test__scat_draft_table_header__a_header_with_three_columns(make_vault, status):
    bad = "| from | type | to |"
    seeded(
        make_vault,
        with_section(status, table(GOOD, header=bad)),
        msg(
            header(status, f"the header row is `{bad}`, not `{HEADER}`"),
            f"Fix: replace the line `{bad}` with `{HEADER}`",
        ),
    )


@STATUSES
def test__scat_draft_table_header__a_separator_that_is_not_one(make_vault, status):
    seeded(
        make_vault,
        with_section(status, table(GOOD, sep="| a | b |")),
        msg(
            header(status, "the line after the header row is `| a | b |`, not a separator row"),
            f"Fix: replace the line `| a | b |` with `{SEP}`",
        ),
    )


@STATUSES
def test__scat_draft_table_header__no_separator_row_the_second_line_is_a_row(make_vault, status):
    r = seeded(
        make_vault,
        with_section(status, table(GOOD, sep=None)),
        msg(
            header(status, f"the line after the header row is `{GOOD}`, not a separator row"),
            f"Fix: replace the line `{HEADER}` with two lines, `{HEADER}` then `{SEP}`",
        ),
    )
    (edit,) = r.problems[0].fix_data.options[0].edits
    assert edit.replace == f"{HEADER}\n{SEP}"  # a line break adds the separator row


@STATUSES
def test__scat_draft_table_header__a_header_row_alone(make_vault, status):
    seeded(
        make_vault,
        with_section(status, table(sep=None)),
        msg(
            header(status, "there is no separator row after the header row"),
            f"Fix: replace the line `{HEADER}` with two lines, `{HEADER}` then `{SEP}`",
        ),
    )


@STATUSES
def test__scat_draft_table_header__a_wrong_name_and_a_missing_separator_are_one_fix(
    make_vault, status
):
    bad = "| from | kind | to | note |"
    r = seeded(
        make_vault,
        with_section(status, table(GOOD, header=bad, sep=None)),
        msg(
            header(status, f"the header row is `{bad}`, not `{HEADER}`"),
            f"Fix: replace the line `{bad}` with two lines, `{HEADER}` then `{SEP}`",
        ),
    )
    assert len(r.problems) == 1


@STATUSES
def test__scat_draft_table_header__a_wrong_name_and_a_wrong_separator_are_two_edits_of_one_fix(
    make_vault, status
):
    bad = "| from | kind | to | note |"
    r = seeded(
        make_vault,
        with_section(status, table(GOOD, header=bad, sep="| a | b |")),
        msg(
            header(status, f"the header row is `{bad}`, not `{HEADER}`"),
            f"Fix: replace the line `{bad}` with `{HEADER}` and the line `| a | b |` with `{SEP}`",
        ),
    )
    edits = r.problems[0].fix_data.options[0].edits
    assert [(e.line, e.find, e.replace) for e in edits] == [
        (14, bad, HEADER),
        (15, "| a | b |", SEP),
    ]


@STATUSES
def test__scat_draft_table_header__the_rows_of_a_malformed_table_are_checked_by_no_row_rule(
    make_vault, status
):
    rows = ("| [[staff]] | owns | [[safe-handling]] | |", "| staff | holds | [[safe-handling]]")
    r = report_of(
        make_vault, with_section(status, table(*rows, header="| from | to | type | note |"))
    )
    assert rules_of(r) == [f"SCAT-{'DONE' if status == 'done' else 'DRAFT'}-TABLE-HEADER"]


@pytest.mark.parametrize(
    "compact",
    ["|from|type|to|note|", "| FROM | Type | To | Note |", "|  from |type | to  |   note|"],
)
def test__scat_draft_table_header__spacing_and_case_are_not_defects(make_vault, compact):
    seeded(make_vault, with_section("done", table(GOOD, header=compact)))


# SCAT-DRAFT-TABLE-ROW


def row_head(status, n, what, line=None):
    return pair("TABLE-ROW", status, f"{F}{line or 15 + n}:1 row {n}: {what}")


ROW_CELLS = "the row has {k} cells, not 4 (from, type, to, note)"


@STATUSES
def test__scat_draft_table_row__three_cells_and_a_closing_bar_add_an_empty_note(make_vault, status):
    r = seeded(
        make_vault,
        with_rows(status, "| [[staff]] | holds | [[safe-handling]] |"),
        msg(
            row_head(status, 1, ROW_CELLS.format(k=3)),
            "Fix: add an empty note: replace the final `|` with `| |`",
        ),
    )
    (edit,) = r.problems[0].fix_data.options[0].edits
    assert (edit.line, edit.column, edit.find, edit.replace) == (16, 41, "|", "| |")


@STATUSES
def test__scat_draft_table_row__four_cells_and_no_closing_bar(make_vault, status):
    seeded(
        make_vault,
        with_rows(status, "| [[staff]] | holds | [[safe-handling]] | n"),
        msg(
            row_head(status, 1, "the row does not end with `|`"),
            "Fix: write ` |` after the last cell: replace `n` with `n |`",
        ),
    )


@STATUSES
def test__scat_draft_table_row__three_cells_and_no_closing_bar(make_vault, status):
    seeded(
        make_vault,
        with_rows(status, "| [[staff]] | holds | [[safe-handling]]"),
        msg(
            row_head(status, 1, ROW_CELLS.format(k=3)),
            "Fix: write ` | |` after the last cell, which adds the empty note and the closing bar: "
            "replace `[[safe-handling]]` with `[[safe-handling]] | |`",
        ),
    )


@STATUSES
def test__scat_draft_table_row__more_than_four_cells_offers_the_escape_or_the_delete(
    make_vault, status
):
    r = seeded(
        make_vault,
        with_rows(status, "| [[staff]] | holds | [[safe-handling]] | x | y |"),
        msg(
            row_head(status, 1, ROW_CELLS.format(k=5)),
            *choose(
                "a `|` inside the note is written `\\|`: replace the `|` that opens cell 5 and the "
                "ones after it with `\\|`",
                DELETE,
            ),
        ),
    )
    first = r.problems[0].fix_data.options[0]
    assert [(e.column, e.find, e.replace) for e in first.edits] == [(45, "|", "\\|")]


@STATUSES
def test__scat_draft_table_row__each_extra_bar_is_escaped_right_to_left(make_vault, status):
    r = report_of(
        make_vault, with_rows(status, "| [[staff]] | holds | [[safe-handling]] | a | b | c |")
    )
    first = r.problems[0].fix_data.options[0]
    assert [e.column for e in first.edits] == [49, 45]  # right to left, so each column stays right


@STATUSES
def test__scat_draft_table_row__fewer_than_three_cells_offers_the_delete_or_a_new_row(
    make_vault, status
):
    seeded(
        make_vault,
        with_rows(status, "| [[staff]] | holds |"),
        msg(
            row_head(status, 1, ROW_CELLS.format(k=2)),
            *choose(
                DELETE,
                "write the row again with four cells and a closing `|`: `| from | type | to | note |`",
            ),
        ),
    )


@STATUSES
def test__scat_draft_table_row__a_bar_in_a_link_or_escaped_is_no_cell(make_vault, status):
    rows = ("| [[staff\\|the crew]] | holds | [[safe-handling]] | a \\| b |",)
    seeded(make_vault, with_rows(status, *rows))


# SCAT-DRAFT-TABLE-TYPE


def type_head(status, n, value, col=15, what=None):
    what = what or f"`{value}` is not an edge type {VERBS}"
    return pair("TABLE-TYPE", status, f"{F}{15 + n}:{col} row {n} cell `type`: {what}")


@STATUSES
def test__scat_draft_table_type__a_group_and_a_concern_give_the_verb_of_that_type(
    make_vault, status
):
    seeded(
        make_vault,
        with_rows(status, "| [[staff]] | owns | [[safe-handling]] | |"),
        msg(
            type_head(status, 1, "owns"),
            *choose("replace `owns` with `holds`", DELETE),
        ),
    )


@STATUSES
def test__scat_draft_table_type__a_near_match_among_the_six_spellings(make_vault, status):
    seeded(
        make_vault,
        with_rows(status, "| [[staff]] | addresed-by | [[safe-handling]] | |"),
        msg(
            type_head(status, 1, "addresed-by"),
            *choose(
                "replace `addresed-by` with `holds`",
                "replace `addresed-by` with `addressed-by`",
                DELETE,
            ),
        ),
    )


@STATUSES
def test__scat_draft_table_type__a_near_match_that_is_the_layer_verb_is_offered_once(
    make_vault, status
):
    seeded(
        make_vault,
        with_rows(status, "| [[staff]] | holdz | [[safe-handling]] | |"),
        msg(type_head(status, 1, "holdz"), *choose("replace `holdz` with `holds`", DELETE)),
    )


@STATUSES
def test__scat_draft_table_type__an_empty_cell_takes_the_whole_row_line(make_vault, status):
    line = "| [[staff]] |  | [[safe-handling]] | |"
    r = seeded(
        make_vault,
        with_rows(status, line),
        msg(
            type_head(status, 1, "", what=f"the value is empty, which is not an edge type {VERBS}"),
            *choose("replace the empty cell with `holds`", DELETE),
        ),
    )
    (edit,) = r.problems[0].fix_data.options[0].edits
    assert (edit.find, edit.replace) == (line, "| [[staff]] | holds | [[safe-handling]] | |")


@STATUSES
def test__scat_draft_table_type__ends_that_fit_no_type_offer_the_three_verbs(make_vault, status):
    seeded(
        make_vault,
        with_rows(status, "| [[staff]] | owns | [[self-checkout]] | |"),
        msg(
            type_head(status, 1, "owns"),
            *choose(
                "replace `owns` with `holds`",
                "replace `owns` with `is addressed by`",
                "replace `owns` with `is provided by`",
                DELETE,
            ),
        ),
    )


@STATUSES
def test__scat_draft_table_type__a_row_of_two_unresolved_ends_offers_the_three_verbs(
    make_vault, status
):
    r = report_of(make_vault, with_rows(status, "| [[ghost]] | owns | [[nowhere]] | |"))
    types = [p for p in r.problems if p.rule.endswith("TABLE-TYPE")]
    assert [o.text for o in types[0].fix_data.options] == [
        "replace `owns` with `holds`",
        "replace `owns` with `is addressed by`",
        "replace `owns` with `is provided by`",
        DELETE,
    ]
    # the row's ends are still checked by the end rules; its layers are not judged
    assert sorted(x.split("-", 2)[2] for x in rules_of(r)) == [
        "END-NOPAGE",
        "END-NOPAGE",
        "TABLE-TYPE",
    ]


@STATUSES
def test__scat_draft_table_type__the_slug_and_the_verb_in_any_case_are_types(make_vault, status):
    rows = (
        "| [[staff]] | Holds | [[safe-handling]] | |",
        "| [[quick-checkout]] | IS ADDRESSED BY | [[self-checkout]] | |",
        "| [[self-checkout]] | provided-by | [[booking-app]] | |",
    )
    seeded(make_vault, with_rows(status, *rows))


# SCAT-DRAFT-TABLE-LAYERS


def layers_head(status, n, what):
    return pair("TABLE-LAYERS", status, f"{F}{15 + n}:1 row {n}: {what}")


@STATUSES
def test__scat_draft_table_layers__a_pair_written_the_wrong_way_round_is_swapped(
    make_vault, status
):
    r = seeded(
        make_vault,
        with_rows(status, row("holds", "safe-handling", "staff")),
        msg(
            layers_head(
                status,
                1,
                "`holds` joins a group to a concern, but [[safe-handling]] is a concern page, and "
                "[[staff]] is a group page",
            ),
            *choose(
                "swap the two ends: replace `[[safe-handling]] | holds | [[staff]]` with `[[staff]] | holds | [[safe-handling]]`",
                DELETE,
            ),
        ),
    )
    (edit,) = r.problems[0].fix_data.options[0].edits
    assert (edit.line, edit.column) == (16, 3)


@STATUSES
def test__scat_draft_table_layers__the_swap_keeps_the_padding_between_the_ends(make_vault, status):
    line = "| [[safe-handling]] |   holds   |   [[staff]] | |"
    r = report_of(make_vault, with_rows(status, line))
    edit = r.problems[0].fix_data.options[0].edits[0]
    assert edit.find == "[[safe-handling]] |   holds   |   [[staff]]"
    assert edit.replace == "[[staff]] |   holds   |   [[safe-handling]]"


@STATUSES
def test__scat_draft_table_layers__two_layers_that_are_those_of_another_type_retype_the_row(
    make_vault, status
):
    seeded(
        make_vault,
        with_rows(status, row("holds", "safe-handling", "self-checkout")),
        msg(
            layers_head(
                status,
                1,
                "`holds` joins a group to a concern, but [[safe-handling]] is a concern page, and "
                "[[self-checkout]] is an affordance page",
            ),
            *choose("replace `holds` with `is addressed by`", DELETE),
        ),
    )


@STATUSES
def test__scat_draft_table_layers__layers_that_are_not_neighbours_have_no_exact_fix(
    make_vault, status
):
    seeded(
        make_vault,
        with_rows(status, row("holds", "staff", "self-checkout")),
        msg(
            layers_head(
                status,
                1,
                "`holds` joins a group to a concern, but [[self-checkout]] is an affordance page",
            ),
            *choose(
                "none of the three edge types joins a group to an affordance: tell it as two rows "
                "through a node between them",
                DELETE,
            ),
        ),
    )


@STATUSES
def test__scat_draft_table_layers__one_end_wrong_and_the_other_unresolved_names_only_the_wrong_end(
    make_vault, status
):
    r = report_of(make_vault, with_rows(status, row("holds", "self-checkout", "briefing-gone")))
    first = r.problems[0]
    assert first.rule.endswith("TABLE-LAYERS")
    assert first.what == (
        "`holds` joins a group to a concern, but [[self-checkout]] is an affordance page"
    )


@STATUSES
def test__scat_draft_table_layers__a_row_of_the_right_layers_or_an_unresolved_end_is_not_judged(
    make_vault, status
):
    rows = (row("holds", "staff", "safe-handling"), row("holds", "staff", "ghost"))
    r = report_of(make_vault, with_rows(status, *rows))
    assert [x for x in rules_of(r) if "LAYERS" in x] == []


# SCAT-DRAFT-TABLE-SECOND


def second_head(status, line, col, what):
    return pair("TABLE-SECOND", status, f"{F}{line}:{col} table: {what}")


TAIL = "only the first table under the first `Edges told` is read, so its rows tell no edge"


@STATUSES
def test__scat_draft_table_second__a_second_heading_offers_the_move_or_a_new_heading(
    make_vault, status
):
    again = f"\n## Edges told\n\n{HEADER}\n{SEP}\n{GOOD}\n"
    r = seeded(
        make_vault,
        with_section(status, table(GOOD) + again),
        msg(
            second_head(status, 18, 1, f"a second heading `Edges told` on this narrative; {TAIL}"),
            *choose(
                "move the rows you want into the first table (line 14), then delete this heading and table",
                "replace the heading `## Edges told` with `## <heading you choose>` (author), so it "
                "is no longer an `Edges told` heading",
            ),
        ),
    )
    option = r.problems[0].fix_data.options[1]
    assert (option.kind, option.edits[0].author_slot) == ("slot", "<heading you choose>")


@STATUSES
def test__scat_draft_table_second__a_second_table_under_one_heading(make_vault, status):
    again = f"\n{HEADER}\n{SEP}\n{GOOD}\n"
    seeded(
        make_vault,
        with_section(status, table(GOOD) + again),
        msg(
            second_head(status, 18, 1, f"a second table on this narrative; {TAIL}"),
            "Fix: move the rows you want into the first table (line 14), then delete this table",
        ),
    )


@STATUSES
def test__scat_draft_table_second__a_misspelled_heading_and_a_table_on_a_concern_page_give_none(
    make_vault, status
):
    section = table(GOOD) + f"\n## Edges tolds\n\n{HEADER}\n{SEP}\n{GOOD}\n"
    page = doc("concern", "Safe handling", body=f"\n{HEADER}\n{SEP}\n{GOOD}\n")
    seeded(make_vault, {**with_section(status, section), "concern/safe-handling.md": page})


# SCAT-DRAFT-TABLE-DUPLICATE


def dup_head(status, n, of=1):
    return pair(
        "TABLE-DUPLICATE",
        status,
        f"{F}{15 + n}:1 row {n}: tells the same edge as row {of} (`holds`, [[staff]], "
        "[[safe-handling]]); a narrative tells an edge once",
    )


@STATUSES
def test__scat_draft_table_duplicate__two_identical_rows(make_vault, status):
    seeded(
        make_vault,
        with_rows(status, GOOD, GOOD),
        msg(dup_head(status, 2), f"Fix: delete the row `{GOOD}`"),
    )


@STATUSES
def test__scat_draft_table_duplicate__the_verb_and_the_slug_are_one_type_and_a_note_is_kept_by_hand(
    make_vault, status
):
    again = "| [[staff]] | holds | [[safe-handling]] | said twice |"
    seeded(
        make_vault,
        with_rows(status, GOOD, again),
        msg(
            dup_head(status, 2),
            f"Fix: delete the row `{again}` (if its note `said twice` is worth keeping, put it in the "
            "note of row 1 first)",
        ),
    )


@STATUSES
def test__scat_draft_table_duplicate__a_third_copy_is_a_second_message_against_the_first(
    make_vault, status
):
    seeded(
        make_vault,
        with_rows(status, GOOD, GOOD, GOOD),
        msg(dup_head(status, 2), f"Fix: delete the row `{GOOD}`"),
        msg(dup_head(status, 3), f"Fix: delete the row `{GOOD}`"),
    )


def test__scat_draft_table_duplicate__the_same_pair_in_two_narratives_is_two_tellings_and_no_defect(
    make_vault,
):
    seeded(
        make_vault, {}
    )  # the fixture tells quick-checkout is addressed by self-checkout in both narratives


@STATUSES
def test__scat_draft_table_duplicate__a_row_whose_ends_are_not_links_is_not_compared(
    make_vault, status
):
    r = report_of(
        make_vault,
        with_rows(
            status, "| staff | holds | safe-handling | |", "| staff | holds | safe-handling | |"
        ),
    )
    assert not [x for x in rules_of(r) if "DUPLICATE" in x]


def test__scat_draft_table_duplicate__the_delete_edit_is_a_delete_line_guarded_by_the_row(
    make_vault,
):
    r = report_of(make_vault, with_rows("draft", GOOD, GOOD))
    edit = r.problems[0].fix_data.options[0].edits[0]
    assert (edit.action, edit.line, edit.find) == ("delete-line", 17, GOOD)


@STATUSES
def test__scat_draft_table_header__a_separator_with_no_leading_bar_is_one_message(
    make_vault, status
):
    r = report_of(
        make_vault,
        with_section(status, table(GOOD, header="| from | type | to |", sep="---|---|---|---")),
    )
    assert rules_of(r) == [f"SCAT-{'DONE' if status == 'done' else 'DRAFT'}-TABLE-HEADER"]
