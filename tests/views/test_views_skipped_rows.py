"""A row that tells no edge is named by the check and refused by every view that draws its narrative."""

import pytest
from viewutil import base_files, narrative, row, tree_hash, write

import scat_kg
from scat_kg.checks import check_vault
from scat_kg.graph import load
from scat_kg.vault import read_vault

GOOD = row("holds", "farmers", "water")
PATH = "narrative/bad.md"

# name: (the row at number 2, the rule's ending, text the reason holds)
CASES = {
    "end-not-a-link": ("| holds | farmers | [[water]] | |", "END-NOLINK", "not exactly one link"),
    "end-reaches-no-page": (row("holds", "farmers", "ghost"), "END-NOPAGE", "reaches no page"),
    "end-is-not-a-node": (row("holds", "farmers", "dry"), "END-NOTNODE", "not a node"),
    "wrong-direction": (row("holds", "water", "farmers"), "TABLE-LAYERS", "wrong direction"),
    "unknown-type": (row("owns", "farmers", "water"), "TABLE-TYPE", "`owns` is not an edge type"),
    "malformed-row": ("| holds | [[farmers]] | [[water]] |", "TABLE-ROW", "not well-formed"),
}


def build(tmp_path, bad_row, status="draft"):
    files = base_files() | {
        PATH: narrative("Bad", "The [[water]] ran out.", [GOOD, bad_row], status, "scenario")
    }
    return write(tmp_path / "v", files)


@pytest.mark.parametrize("status", ["draft", "done"])
@pytest.mark.parametrize("case", CASES)
def test_check_vault_reports_the_row(tmp_path, case, status):
    bad_row, rule, _ = CASES[case]
    root = build(tmp_path, bad_row, status)
    found = [
        p
        for p in check_vault(read_vault(root)).problems
        if p.rule.endswith(rule) and p.file == PATH
    ]
    assert len(found) == 1
    assert found[0].where.startswith("row 2")
    assert found[0].severity == ("error" if status == "done" else "warning")


@pytest.mark.parametrize("case", CASES)
def test_the_graph_records_the_skipped_row(tmp_path, case):
    bad_row, _, reason = CASES[case]
    g = load(build(tmp_path, bad_row))
    assert [(k.narrative, k.path, k.row) for k in g.skipped] == [("bad", PATH, 2)]
    assert reason in g.skipped[0].reason
    assert "[[" not in g.skipped[0].reason
    assert g.skipped[0].line == g.narrative("bad").table.rows[1].line


VIEWS = {
    "edge_table": lambda r: scat_kg.edge_table("holds", root=r),
    "layered": lambda r: scat_kg.layered(root=r),
    "trace": lambda r: scat_kg.trace("farmers", root=r),
    "fingerprint": lambda r: scat_kg.fingerprint(root=r),
    "fingerprint-named": lambda r: scat_kg.fingerprint("bad", root=r),
    "layered-named": lambda r: scat_kg.layered(["bad"], root=r),
}


@pytest.mark.parametrize("view", VIEWS)
@pytest.mark.parametrize("case", CASES)
def test_views_refuse_naming_path_and_row(tmp_path, case, view):
    bad_row, _, reason = CASES[case]
    root = build(tmp_path, bad_row)
    before = tree_hash(root)
    out = VIEWS[view](root)
    assert not out.ok
    refused = out.to_dict()["refused"]
    assert [r["subject"] for r in refused] == [f"{PATH} row 2"]
    assert reason in refused[0]["why"]
    assert refused[0]["fix"]["options"][0]["text"] == (
        f"fix the row (`scat check {PATH}` says how), then run this again"
    )
    assert tree_hash(root) == before


@pytest.mark.parametrize("case", CASES)
def test_an_error_page_refuses_once_with_its_problems(tmp_path, case):
    root = build(tmp_path, CASES[case][0], "done")
    out = scat_kg.fingerprint("bad", root=root)
    assert not out.ok
    assert len(out.to_dict()["refused"]) == 1
    assert out.to_dict()["problems"]


@pytest.mark.parametrize("case", CASES)
def test_a_clean_narrative_still_draws(tmp_path, case):
    root = build(tmp_path, CASES[case][0])
    assert scat_kg.fingerprint("dry", root=root).ok
    assert scat_kg.layered(["dry"], root=root).ok


def test_one_refusal_for_each_skipped_row(tmp_path):
    root = build(tmp_path, CASES["end-reaches-no-page"][0])
    extra = narrative("Bad2", "x", [CASES["unknown-type"][0]], "draft", "scenario")
    write(root, {"narrative/bad2.md": extra})
    out = scat_kg.layered(root=root)
    assert [r["subject"] for r in out.to_dict()["refused"]] == [
        f"{PATH} row 2",
        "narrative/bad2.md row 1",
    ]


def test_a_repeated_row_is_not_skipped(tmp_path):
    root = write(
        tmp_path / "v",
        base_files()
        | {PATH: narrative("Bad", "The [[water]] ran out.", [GOOD, GOOD], "draft", "scenario")},
    )
    assert load(root).skipped == ()
    assert scat_kg.fingerprint("bad", root=root).ok
    assert scat_kg.edge_table("holds", root=root).ok


def test_the_base_vault_skips_nothing(tmp_path):
    assert load(write(tmp_path / "v", base_files())).skipped == ()
