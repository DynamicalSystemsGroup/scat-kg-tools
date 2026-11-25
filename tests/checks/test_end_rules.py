"""The mismatches at a row's end: SCAT-DRAFT-END-* and SCAT-DONE-END-*, and rule 4, which has no rule.

A pair has one seed set run three times (`stub`, `draft`, `done`): the same message but for the id and severity.
The narrative's table has its header on line 14 and row n on line 15 + n. Test names carry the rule id of the
DRAFT form (see test_coverage).
"""

import pytest
from helpers import (
    DESK,
    choose,
    doc,
    msg,
    narrative,
    pair,
    report_of,
    rules_of,
    row,
    seeded,
    stub,
    table,
)

STATUSES = pytest.mark.parametrize("status", ["stub", "draft", "done"])
F = DESK + ":"
DELETE = "delete the row"
NOT_LINK = "each end of a row is one link, `[[page-name]]`"


def with_rows(status, *rows, **kw):
    return {DESK: narrative(status=status, rows=rows, **kw)}


def end_head(stem, status, n, col, holds, what):
    return pair(stem, status, f"{F}{15 + n}:{col} row {n} cell `{holds}`: {what}")


# SCAT-DRAFT-END-NOLINK


def nolink(status, col, holds, text, n=1):
    return end_head("END-NOLINK", status, n, col, holds, f"`{text}` is not a link; {NOT_LINK}")


@STATUSES
def test__scat_draft_end_nolink__text_that_is_the_name_of_a_page_of_the_layer(make_vault, status):
    seeded(
        make_vault,
        with_rows(status, "| holds | borrowers | [[safe-handling]] | |"),
        msg(
            nolink(status, 11, "from", "borrowers"),
            *choose(
                "replace `borrowers` with `[[borrowers]]`",
                "replace `borrowers` with `[[staff]]`",
                DELETE,
            ),
        ),
    )


@STATUSES
def test__scat_draft_end_nolink__text_that_is_no_page_replaces_then_stubs(make_vault, status):
    seeded(
        make_vault,
        with_rows(status, "| holds | Sandra's crew | [[safe-handling]] | |"),
        msg(
            nolink(status, 11, "from", "Sandra's crew"),
            *choose(
                "replace `Sandra's crew` with `[[borrowers]]`",
                "replace `Sandra's crew` with `[[staff]]`",
                "replace `Sandra's crew` with `[[sandra-s-crew]]`, then run "
                f"{stub('sandra-s-crew', 'group')} to create a group page",
                DELETE,
            ),
        ),
    )


@STATUSES
def test__scat_draft_end_nolink__an_empty_cell_has_an_author_slot(make_vault, status):
    line = "| holds |  | [[safe-handling]] | |"
    r = seeded(
        make_vault,
        with_rows(status, line),
        msg(
            end_head(
                "END-NOLINK",
                status,
                1,
                11,
                "from",
                f"the cell is empty; {NOT_LINK}",
            ),
            *choose("replace the empty cell with `[[<node you choose>]]` (author)", DELETE),
        ),
    )
    edit = r.problems[0].fix_data.options[0].edits[0]
    assert (edit.find, edit.replace, edit.author_slot) == (
        line,
        "| holds | [[<node you choose>]] | [[safe-handling]] | |",
        "<node you choose>",
    )


@STATUSES
def test__scat_draft_end_nolink__more_than_one_link_offers_each(make_vault, status):
    seeded(
        make_vault,
        with_rows(status, "| holds | [[staff]] and [[borrowers]] | [[safe-handling]] | |"),
        msg(
            nolink(status, 11, "from", "[[staff]] and [[borrowers]]"),
            *choose(
                "replace the cell with `[[staff]]`; any text beside it belongs in the `note` cell by hand",
                "replace the cell with `[[borrowers]]`; any text beside it belongs in the `note` cell by hand",
                DELETE,
            ),
        ),
    )


@STATUSES
def test__scat_draft_end_nolink__the_same_defect_on_the_to_cell(make_vault, status):
    seeded(
        make_vault,
        with_rows(status, "| holds | [[staff]] | quick checkout | |"),
        msg(
            nolink(status, 23, "to", "quick checkout"),
            *choose(
                "replace `quick checkout` with `[[quick-checkout]]`",
                "replace `quick checkout` with `[[safe-handling]]`",
                DELETE,
            ),
        ),
    )


@STATUSES
def test__scat_draft_end_nolink__an_embed_and_an_alias_are_each_one_link(make_vault, status):
    seeded(make_vault, with_rows(status, "| holds | ![[staff]] | [[safe-handling\\|safe]] | |"))


@STATUSES
def test__scat_draft_end_nolink__a_layer_not_known_offers_existing_pages_only(make_vault, status):
    r = report_of(make_vault, with_rows(status, "| owns | borrowers | [[safe-handling]] | |"))
    nolinks = [p for p in r.problems if p.rule.endswith("END-NOLINK")]
    assert [o.text for o in nolinks[0].fix_data.options] == [
        *[
            f"replace `borrowers` with `[[{n}]]`"
            for n in ("borrowers", "quick-checkout", "safe-handling", "self-checkout", "staff")
        ],
        DELETE,
    ]
    assert not any("scat stub" in o.text for o in nolinks[0].fix_data.options)


@STATUSES
def test__scat_draft_end_nolink__a_group_stub_is_withheld_at_the_cap(make_vault, status):
    files = {
        **with_rows(status, "| holds | Sandra's crew | [[safe-handling]] | |"),
        "group/third.md": doc("group", "Third"),
    }
    (p,) = report_of(make_vault, files).problems
    assert [o.text for o in p.fix_data.options] == [
        "replace `Sandra's crew` with `[[borrowers]]`",
        "replace `Sandra's crew` with `[[staff]]`",
        DELETE,
    ]
    assert p.fix.split("\n")[-1] == (
        "(the vault is at its cap of 3 groups, so a new group page would break SCAT-CAP; "
        "choose an existing group)"
    )


@STATUSES
def test__scat_draft_end_nolink__more_than_five_candidates_are_counted(make_vault, status):
    names = [f"c-{i}" for i in range(7)]
    pages = {f"concern/{n}.md": doc("concern", f"C {n}") for n in names}
    account = "A [[staff]]. " + " ".join(f"[[{n}]]" for n in names) + "\n"
    files = {**pages, **with_rows(status, "| holds | [[staff]] | zzz | |", account=account)}
    (p,) = report_of(make_vault, files).problems
    assert len(p.fix_data.options) == 5 + 1 + 1  # five shown, the stub of the derived name `zzz`, the delete
    assert p.fix.split("\n")[-1] == "(+2 more not shown)"


# SCAT-DRAFT-END-NOPAGE


def nopage(status, col, holds, target, reason, n=1):
    return end_head(
        "END-NOPAGE", status, n, col, holds, f"[[{target}]] does not reach a page ({reason})"
    )


@STATUSES
def test__scat_draft_end_nopage__a_name_no_page_has_is_stubbed_as_the_layer(make_vault, status):
    seeded(
        make_vault,
        with_rows(status, "| holds | [[staff]] | [[ghost]] | |"),
        msg(
            nopage(status, 23, "to", "ghost", "no page is named ghost"),
            *choose(f"run {stub('ghost', 'concern')} to create a concern page", DELETE),
        ),
    )


@STATUSES
def test__scat_draft_end_nopage__a_near_match_among_the_pages_of_the_layer(make_vault, status):
    seeded(
        make_vault,
        with_rows(status, "| holds | [[borrower]] | [[safe-handling]] | |"),
        msg(
            nopage(status, 11, "from", "borrower", "no page is named borrower"),
            *choose(
                "replace `[[borrower]]` with `[[borrowers]]`",
                f"run {stub('borrower', 'group')} to create a group page",
                DELETE,
            ),
        ),
    )


@STATUSES
def test__scat_draft_end_nopage__an_illegal_name_is_replaced_then_stubbed(make_vault, status):
    seeded(
        make_vault,
        with_rows(status, "| holds | [[staff]] | [[Safety briefing]] | |"),
        msg(
            nopage(
                status,
                23,
                "to",
                "Safety briefing",
                "Safety briefing is not a legal page name: it contains `S`, outside a-z, 0-9 and -",
            ),
            *choose(
                "replace `[[Safety briefing]]` with `[[safety-briefing]]`, then run "
                f"{stub('safety-briefing', 'concern')} to create a concern page",
                DELETE,
            ),
        ),
    )


@STATUSES
def test__scat_draft_end_nopage__a_file_without_a_type_gets_the_lines_that_make_it_a_page_of_the_layer(
    make_vault, status
):
    files = {**with_rows(status, "| holds | [[staff]] | [[notes]] | |"), "notes.md": "no type\n"}
    seeded(
        make_vault,
        files,
        msg(
            nopage(status, 23, "to", "notes", "notes.md exists but has no `type`, so it is not a page"),
            *choose(
                "put these lines in a block between two `---` lines at the very top of notes.md: "
                '`type: concern`, `status: stub`, `title: "Notes"`',
                DELETE,
            ),
        ),
    )


@STATUSES
def test__scat_draft_end_nopage__a_group_stub_is_withheld_at_the_cap(make_vault, status):
    files = {**with_rows(status, "| holds | [[ghost]] | [[safe-handling]] | |"), "group/third.md": doc("group", "Third")}
    (p,) = report_of(make_vault, files).problems
    assert [o.text for o in p.fix_data.options] == [DELETE]
    assert p.fix.split("\n")[-1].startswith("(the vault is at its cap of 3 groups")


@STATUSES
def test__scat_draft_end_nopage__a_row_whose_type_is_unknown_gets_the_variants_without_a_stub(
    make_vault, status
):
    r = report_of(make_vault, with_rows(status, "| owns | [[borrower]] | [[safe-handling]] | |"))
    nopages = [p for p in r.problems if p.rule.endswith("END-NOPAGE")]
    assert [o.text for o in nopages[0].fix_data.options] == [
        "replace `[[borrower]]` with `[[borrowers]]`",
        DELETE,
    ]


# SCAT-DRAFT-END-NOTNODE


def notnode(status, col, holds, target, what, n=1):
    return end_head(
        "END-NOTNODE", status, n, col, holds, f"[[{target}]] is {what}, not a node; a row joins two nodes"
    )


@STATUSES
def test__scat_draft_end_notnode__a_narrative_with_candidates_the_narrative_links_elsewhere(make_vault, status):
    seeded(
        make_vault,
        with_rows(status, "| holds | [[kiosk-pitch]] | [[safe-handling]] | |"),
        msg(
            notnode(status, 11, "from", "kiosk-pitch", "a narrative page"),
            *choose(
                "replace `[[kiosk-pitch]]` with `[[borrowers]]`",
                "replace `[[kiosk-pitch]]` with `[[staff]]`",
                DELETE,
            ),
        ),
    )


@STATUSES
def test__scat_draft_end_notnode__a_narrative_with_no_candidate_offers_an_author_slot(make_vault, status):
    page = narrative(status=status, rows=("| holds | [[kiosk-pitch]] | [[safe-handling]] | |",), account="A [[safe-handling]].\n")
    r = seeded(
        make_vault,
        {DESK: page},
        msg(
            notnode(status, 11, "from", "kiosk-pitch", "a narrative page"),
            *choose("replace `[[kiosk-pitch]]` with `[[<node you choose>]]` (author)", DELETE),
        ),
    )
    option = r.problems[0].fix_data.options[0]
    assert (option.kind, option.edits[0].author_slot) == ("slot", "<node you choose>")


@STATUSES
def test__scat_draft_end_notnode__a_page_with_an_invalid_type_is_this_message_and_its_own_error(
    make_vault, status
):
    odd = "concern/odd.md"
    files = {odd: doc("gadget", "Odd"), **with_rows(status, "| holds | [[staff]] | [[odd]] | |")}
    r = report_of(make_vault, files)
    assert [p.rule for p in r.problems] == [
        "SCAT-FM-TYPE",
        pair("END-NOTNODE", status, "").split(" ")[1].strip("[]"),
    ]
    assert r.problems[1].what == (
        "[[odd]] is a page with the invalid type `gadget`, not a node; a row joins two nodes"
    )


@STATUSES
def test__scat_draft_end_notnode__a_page_that_is_not_a_node_in_a_row_of_an_unknown_type_has_no_candidates(
    make_vault, status
):
    r = report_of(make_vault, with_rows(status, "| owns | [[kiosk-pitch]] | [[safe-handling]] | |"))
    notnodes = [p for p in r.problems if p.rule.endswith("NOTNODE")]
    assert [o.kind for o in notnodes[0].fix_data.options] == ["slot", "exact"]


# the status behaviour of a pair, and rule 4


def test__a_pair_is_a_warning_before_done_and_an_error_at_done(make_vault):
    row_ = "| holds | [[staff]] | [[ghost]] | |"
    for status, severity, ok in (("stub", "warning", True), ("draft", "warning", True), ("done", "error", False)):
        r = report_of(make_vault, with_rows(status, row_))
        assert [(p.severity, p.rule.split("-")[1]) for p in r.problems] == [
            (severity, "DONE" if status == "done" else "DRAFT")
        ]
        assert r.ok is ok


def test__a_narrative_with_no_status_or_an_invalid_one_gets_the_status_error_and_no_pair_rule(make_vault):
    ghost = row("holds", "staff", "ghost")
    for status, rule in ((None, "SCAT-FM-REQUIRED"), ("finished", "SCAT-FM-STATUS")):
        r = report_of(make_vault, {DESK: narrative(status=status, rows=(ghost,))})
        assert rules_of(r) == [rule]


def test__a_mismatch_in_a_page_that_is_not_a_narrative_is_not_read(make_vault):
    page = doc("concern", "Safe handling", body=f"\n{table(row('holds', 'staff', 'ghost'))}")
    r = report_of(make_vault, {"concern/safe-handling.md": page})
    assert rules_of(r) == ["SCAT-LINK-DANGLING-BODY"]  # a link like any other, and no row


@STATUSES
@pytest.mark.parametrize("scope", ["vault", "page", "neighborhood"])
def test__rule_4_a_narrative_that_links_both_ends_of_a_pair_and_has_no_row_gets_no_message(
    make_vault, status, scope
):
    # the account links staff and quick-checkout; no row joins them, and nothing says so at any status or scope
    page = narrative(status=status)
    assert "[[staff]]" in page and "[[quick-checkout|" in page
    assert "| holds | [[staff]] | [[quick-checkout]]" not in page
    seeded(make_vault, {DESK: page}, scope=scope, page=DESK)


@STATUSES
def test__rule_4_a_narrative_with_no_row_at_all_tells_no_edge_and_gets_no_message(make_vault, status):
    seeded(make_vault, {DESK: narrative(status=status, rows=())})
    seeded(make_vault, {DESK: narrative(status=status, section="")})  # no table, no heading


def test__rule_4_the_fingerprint_view_lists_the_pair_as_a_candidate_and_the_check_does_not(make_vault):
    from helpers import vault

    from scat_kg.graph import load

    v = vault(make_vault)
    assert rules_of(report_of(make_vault)) == []
    seen = {(c.narrative, c.type, c.from_node, c.to_node) for c in load(v.root).candidates}
    assert ("desk-day", "holds", "staff", "quick-checkout") in seen
    assert ("desk-day", "holds", "staff", "safe-handling") not in seen  # a row tells it


def test__rule_4_a_row_alone_with_both_ends_linked_is_conformant(make_vault):
    page = narrative(account="A [[staff]], and [[safe-handling]].\n", rows=(row("holds", "staff", "safe-handling"),))
    seeded(make_vault, {DESK: page})
    only_the_row = narrative(account="No links in the account.\n", rows=(row("holds", "staff", "safe-handling"),))
    seeded(make_vault, {DESK: only_the_row})
