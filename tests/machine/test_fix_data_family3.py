"""WP11-U5: the fixes of the table rules (SCAT-*-TABLE-*) are typed data that match their text, and the exact options
that carry edits clear their problem when applied (see fixcases.verify): the line, the column and the `find` of every
edit, the right-to-left escapes of a row with extra cells, the line break that adds a separator row, the whole row line
of an empty cell, and the guarded `delete-line`."""

import fixcases as fc
import helpers as H

D = H.DESK
R = H.row
GOOD = R("holds", "staff", "safe-handling")


def with_rows(status, *rows):
    return {D: H.narrative(status=status, rows=rows)}


def with_section(status, section):
    return {D: H.narrative(status=status, section=section)}


CASES = []
for stem, status in (("DRAFT", "draft"), ("DONE", "done")):
    t = f"SCAT-{stem}-TABLE-"
    again = f"\n## Edges told\n\n{H.HEADER}\n{H.SEP}\n{GOOD}\n"
    CASES += [
        (
            f"{stem}-header-order",
            t + "HEADER",
            with_section(status, H.table(GOOD, header="| from | to | type | note |")),
            (),
        ),
        (
            f"{stem}-header-name",
            t + "HEADER",
            with_section(status, H.table(GOOD, header="| kind | from | to | note |")),
            (),
        ),
        (
            f"{stem}-header-separator",
            t + "HEADER",
            with_section(status, H.table(GOOD, sep="| a | b |")),
            (),
        ),
        (
            f"{stem}-header-no-separator",
            t + "HEADER",
            with_section(status, H.table(GOOD, sep=None)),
            (),
        ),
        (f"{stem}-header-alone", t + "HEADER", with_section(status, H.table(sep=None)), ()),
        (
            f"{stem}-header-name-and-separator",
            t + "HEADER",
            with_section(
                status, H.table(GOOD, header="| kind | from | to | note |", sep="| a | b |")
            ),
            (),
        ),
        (
            f"{stem}-row-note",
            t + "ROW",
            with_rows(status, "| holds | [[staff]] | [[safe-handling]] |"),
            (),
        ),
        (
            f"{stem}-row-bar",
            t + "ROW",
            with_rows(status, "| holds | [[staff]] | [[safe-handling]] | n"),
            (),
        ),
        (
            f"{stem}-row-both",
            t + "ROW",
            with_rows(status, "| holds | [[staff]] | [[safe-handling]]"),
            (),
        ),
        (
            f"{stem}-row-extra",
            t + "ROW",
            with_rows(status, "| holds | [[staff]] | [[safe-handling]] | a | b | c |"),
            (),
        ),
        (f"{stem}-row-few", t + "ROW", with_rows(status, "| holds | [[staff]] |"), ()),
        (
            f"{stem}-type-verb",
            t + "TYPE",
            with_rows(status, "| owns | [[staff]] | [[safe-handling]] | |"),
            (),
        ),
        (
            f"{stem}-type-near",
            t + "TYPE",
            with_rows(status, "| addresed-by | [[staff]] | [[safe-handling]] | |"),
            (),
        ),
        (
            f"{stem}-type-empty",
            t + "TYPE",
            with_rows(status, "|  | [[staff]] | [[safe-handling]] | |"),
            (),
        ),
        (
            f"{stem}-type-three",
            t + "TYPE",
            with_rows(status, "| owns | [[staff]] | [[self-checkout]] | |"),
            (),
        ),
        (
            f"{stem}-layers-swap",
            t + "LAYERS",
            with_rows(status, R("holds", "safe-handling", "staff")),
            (),
        ),
        (
            f"{stem}-layers-retype",
            t + "LAYERS",
            with_rows(status, R("holds", "safe-handling", "self-checkout")),
            (),
        ),
        (
            f"{stem}-layers-none",
            t + "LAYERS",
            with_rows(status, R("holds", "staff", "self-checkout")),
            (),
        ),
        (f"{stem}-second-heading", t + "SECOND", with_section(status, H.table(GOOD) + again), ()),
        (
            f"{stem}-second-table",
            t + "SECOND",
            with_section(status, H.table(GOOD) + f"\n{H.HEADER}\n{H.SEP}\n{GOOD}\n"),
            (),
        ),
        (f"{stem}-duplicate", t + "DUPLICATE", with_rows(status, GOOD, GOOD), ()),
        (
            f"{stem}-duplicate-note",
            t + "DUPLICATE",
            with_rows(status, GOOD, R("holds", "staff", "safe-handling", "said twice")),
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


def test_the_order_of_the_columns_is_advisory_and_a_wrong_name_is_exact(make_vault):
    (o,) = only(make_vault, "DRAFT-header-order").fix_data.options
    assert o.kind == "advisory" and not o.edits
    p = only(make_vault, "DRAFT-header-name")
    assert p.fix_data.kind == "exact"


def test_a_missing_separator_is_added_by_a_line_break_in_replace(make_vault):
    e = only(make_vault, "DONE-header-no-separator").fix_data.options[0].edits[0]
    assert (e.line, e.find, e.replace) == (14, H.HEADER, f"{H.HEADER}\n{H.SEP}")


def test_a_row_with_extra_cells_escapes_each_extra_bar_right_to_left(make_vault):
    first = only(make_vault, "DRAFT-row-extra").fix_data.options[0]
    assert [(e.line, e.column, e.find, e.replace) for e in first.edits] == [
        (16, 49, "|", "\\|"),
        (16, 45, "|", "\\|"),
    ]


def test_an_empty_type_cell_is_the_whole_row_line_written_again(make_vault):
    e = only(make_vault, "DONE-type-empty").fix_data.options[0].edits[0]
    assert (e.find, e.replace) == (
        "|  | [[staff]] | [[safe-handling]] | |",
        "| holds | [[staff]] | [[safe-handling]] | |",
    )


def test_the_swap_and_the_retype_edit_the_cells_at_their_columns(make_vault):
    e = only(make_vault, "DRAFT-layers-swap").fix_data.options[0].edits[0]
    assert (e.line, e.column, e.find, e.replace) == (
        16,
        11,
        "[[safe-handling]] | [[staff]]",
        "[[staff]] | [[safe-handling]]",
    )
    e = only(make_vault, "DONE-layers-retype").fix_data.options[0].edits[0]
    assert (e.line, e.column, e.find, e.replace) == (16, 3, "holds", "is addressed by")


def test_a_second_heading_has_a_slot_option_and_a_second_table_only_an_advisory_one(make_vault):
    p = only(make_vault, "DRAFT-second-heading")
    assert [o.kind for o in p.fix_data.options] == ["advisory", "slot"]
    e = p.fix_data.options[1].edits[0]
    assert (e.find, e.replace, e.author_slot) == (
        "## Edges told",
        "## <heading you choose>",
        "<heading you choose>",
    )
    p = only(make_vault, "DONE-second-table")
    assert [o.kind for o in p.fix_data.options] == ["advisory"] and p.fix_data.kind == "advisory"


def test_a_duplicate_is_deleted_by_a_delete_line_guarded_by_the_row(make_vault):
    e = only(make_vault, "DRAFT-duplicate").fix_data.options[0].edits[0]
    assert (e.action, e.line, e.find) == ("delete-line", 17, GOOD)
