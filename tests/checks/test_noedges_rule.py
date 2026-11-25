"""SCAT-NOEDGES (MISSION G1): a `done` narrative whose fingerprint has no edges gets a warning, never an error."""

import pytest
from helpers import DESK, base, narrative, report_of, rules_of, seeded, set_status

import scat_kg
from scat_kg import cli

NAME = "desk-day"
RECORD = (
    f"`scat record-edge <type> <from> <to> --told-by {NAME}` "
    f'(REPL: `scat_kg.record_edge("<type>", "<from>", "<to>", ["{NAME}"])`)'
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

NO_TABLE = narrative(section="")
EMPTY_TABLE = narrative(rows=())


@pytest.mark.parametrize(
    "page", [NO_TABLE, EMPTY_TABLE], ids=["no-table", "header-and-separator-only"]
)
def test__scat_noedges__a_done_narrative_with_no_row_gets_the_warning(make_vault, page):
    r = seeded(make_vault, {DESK: page}, GOLDEN)
    assert r.ok and r.problems[0].severity == "warning" and not r.errors


@pytest.mark.parametrize("scope", ["vault", "page", "neighborhood"])
def test__scat_noedges__the_same_message_at_every_scope(make_vault, scope):
    seeded(make_vault, {DESK: EMPTY_TABLE}, GOLDEN, scope=scope, page=DESK)


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
    files = base()
    files[DESK] = narrative(status="draft", rows=())
    root = make_vault(files)
    result = scat_kg.set_status(NAME, "done", root=root)
    assert result.ok, str(result)
    assert (root / DESK).read_text(encoding="utf-8").count("status: done") == 1


def test__scat_noedges__the_repl_and_the_cli_print_the_same_message(make_vault, capsys):
    files = base()
    files[DESK] = EMPTY_TABLE
    root = make_vault(files)
    result = scat_kg.check(root=root)
    code = cli.main(["check", "--root", str(root)])
    out = capsys.readouterr().out
    assert code == 0 and result.ok
    assert out == str(result) + "\n"
    assert GOLDEN in out
    assert out.rstrip().endswith("0 errors, 1 warning")
