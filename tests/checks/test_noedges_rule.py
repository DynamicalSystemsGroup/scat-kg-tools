"""SCAT-NOEDGES (MISSION G1): a `done` narrative whose fingerprint has no edges gets a warning, never an error."""

import pytest
from helpers import DESK, base, narrative, report_of, rules_of, seeded, set_status

import scat_tools
from scat_tools import cli

NAME = "desk-day"
RECORD = (
    f"`scat record-edge <type> <from> <to> --told-by {NAME}` "
    f'(REPL: `scat_tools.record_edge("<type>", "<from>", "<to>", ["{NAME}"])`)'
)
ONE = (
    f"    1. record its edges: run {set_status(NAME)}, then {RECORD} for each edge the account tells, "
    f"then {set_status(NAME, 'done')}"
)
TWO = (
    "    2. or leave it as intended: a narrative may tell no edge, and this warning does not block; "
    "nothing to change"
)
GOLDEN = "\n".join(
    [
        f"warning [SCAT-NOEDGES] {DESK} table: the narrative is `done` and tells no edge: its fingerprint has no edges",
        "  Fix, choose one:",
        ONE,
        TWO,
    ]
)

# A narrative that links a node and tells no edge also gets SCAT-DONE-LINK-NOTINTABLE for the link (an error at
# `done`): the table is the coding of record, so a link no row ends at is its own problem.
ACCOUNT = "Only the [[staff]] spoke.\n"
NOTIN = "\n".join(
    [
        f"error [SCAT-DONE-LINK-NOTINTABLE] {DESK}:10:10 link [[staff]]: the account links it but no row of the "
        "table has it as an end; the table is the coding of record",
        "  Fix, choose one:",
        f"    1. record the row for it: run {RECORD}, with `staff` as `<from>` or `<to>`",
        "    2. or take the link out of the account: write `staff` without its brackets and keep the words",
    ]
)
NO_TABLE = narrative(section="", account=ACCOUNT)
EMPTY_TABLE = narrative(rows=(), account=ACCOUNT)


@pytest.mark.parametrize(
    "page", [NO_TABLE, EMPTY_TABLE], ids=["no-table", "header-and-separator-only"]
)
def test__scat_noedges__a_done_narrative_with_no_row_gets_the_warning(make_vault, page):
    r = seeded(make_vault, {DESK: page}, GOLDEN, NOTIN)
    assert r.problems[0].severity == "warning"
    assert [p.rule for p in r.errors] == ["SCAT-DONE-LINK-NOTINTABLE"]


@pytest.mark.parametrize("scope", ["vault", "page", "neighborhood"])
def test__scat_noedges__the_same_message_at_every_scope(make_vault, scope):
    seeded(make_vault, {DESK: EMPTY_TABLE}, GOLDEN, NOTIN, scope=scope, page=DESK)


@pytest.mark.parametrize("status", ["stub", "draft"])
def test__scat_noedges__silent_before_done(make_vault, status):
    assert "SCAT-NOEDGES" not in rules_of(
        report_of(make_vault, {DESK: narrative(status=status, rows=())})
    )


def test__scat_noedges__silent_when_a_row_tells_an_edge(make_vault):
    assert "SCAT-NOEDGES" not in rules_of(report_of(make_vault))


def test__scat_noedges__silent_when_the_table_is_malformed(make_vault):
    page = narrative(section="## Edges told\n\n| from | type | to |\n|---|---|---|\n")
    r = report_of(make_vault, {DESK: page})
    assert "SCAT-NOEDGES" not in rules_of(r) and "SCAT-DONE-TABLE-HEADER" in rules_of(r)


def test__scat_noedges__does_not_refuse_set_status_done(make_vault):
    # the warning does not block; the account's link no row ends at does (SCAT-DONE-LINK-NOTINTABLE)
    files = base()
    files[DESK] = narrative(status="draft", rows=(), account=ACCOUNT)
    root = make_vault(files)
    result = scat_tools.set_status(NAME, "done", root=root)
    (refusal,) = result.refused
    assert not result.ok and [p.rule for p in refusal.problems] == ["SCAT-DONE-LINK-NOTINTABLE"]
    files[DESK] = narrative(status="draft", rows=(), account="Only the staff spoke.\n")
    root = make_vault(files)
    result = scat_tools.set_status(NAME, "done", root=root)
    assert result.ok, str(result)
    assert (root / DESK).read_text(encoding="utf-8").count("status: done") == 1


def test__scat_noedges__the_repl_and_the_cli_print_the_same_message(make_vault, capsys):
    files = base()
    files[DESK] = EMPTY_TABLE
    root = make_vault(files)
    result = scat_tools.check(root=root)
    code = cli.main(["check", "--root", str(root)])
    out = capsys.readouterr().out
    assert code == 1 and not result.ok
    assert out == str(result) + "\n"
    assert GOLDEN in out
    assert out.rstrip().endswith("1 error, 1 warning")
