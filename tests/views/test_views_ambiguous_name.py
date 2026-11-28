"""A name carried by more than one page behind a row end is reported, not dropped: SCAT-NAME names the duplicate,
and the graph and every view name the row, the name and both files."""

import pytest
from viewutil import base_files, narrative, page, row, tree_hash, write

import scat_tools
from scat_tools.checks import check_neighborhood, check_page, check_vault
from scat_tools.graph import load
from scat_tools.vault import read_vault

PATH = "narrative/bad.md"
ROW_AT = 2  # the row with the ambiguous end
ORIGINAL = "concern/water.md"

# name: (the second page, the page SCAT-NAME is reported on: the later-sorting one)
DUPLICATES = {
    "same-type-sorts-before": ("concern/extra/water.md", ORIGINAL),
    "same-type-sorts-after": ("concern/zzz/water.md", "concern/zzz/water.md"),
    "other-node-type": ("technology/water.md", "technology/water.md"),
    "not-a-node": ("narrative/water.md", "narrative/water.md"),
}


def dup_page(path):
    kind = path.split("/")[0]
    return (
        narrative("Dup", "x [[farmers]]", None, "draft", "scenario")  # coded: else it is excluded
        if kind == "narrative"
        else page(kind, "Dup")
    )


def build(tmp_path, dup, status="draft", end="to"):
    ok = row("holds", "farmers", "cost")
    ambiguous = (
        row("holds", "farmers", "water") if end == "to" else row("addressed-by", "water", "sensor")
    )
    files = base_files() | {
        dup: dup_page(dup),
        PATH: narrative(
            "Bad",
            "The [[water]] ran out, said the [[farmers]], at a [[cost]], with a [[sensor]].",
            [ok, ambiguous],
            status,
            "scenario",
        ),
    }
    return write(tmp_path / "v", files)


def name_problems(report):
    return [p for p in report.problems if p.rule == "SCAT-NAME"]


@pytest.mark.parametrize("status", ["draft", "done"])
@pytest.mark.parametrize("case", DUPLICATES)
def test_check_vault_reports_scat_name_on_the_later_page(tmp_path, case, status):
    dup, reported = DUPLICATES[case]
    found = name_problems(check_vault(read_vault(build(tmp_path, dup, status))))
    assert [(p.file, p.severity) for p in found] == [(reported, "error")]


@pytest.mark.parametrize("status", ["draft", "done"])
def test_the_neighborhood_of_the_narrative_includes_the_duplicates(tmp_path, status):
    vault = read_vault(build(tmp_path, "concern/extra/water.md", status))
    found = name_problems(check_neighborhood(vault, PATH))
    assert [(p.file, p.severity) for p in found] == [(ORIGINAL, "error")]


def test_page_scope_of_the_narrative_alone_is_silent_about_the_row(tmp_path):
    vault = read_vault(build(tmp_path, "concern/extra/water.md"))
    # the catalogue reports SCAT-NAME on the duplicate page, so `check_page` of the narrative says nothing here
    assert [
        p for p in check_page(vault, PATH).problems if "END" in p.rule or p.rule == "SCAT-NAME"
    ] == []
    assert name_problems(check_page(vault, ORIGINAL))


@pytest.mark.parametrize("case", DUPLICATES)
@pytest.mark.parametrize("end", ["to", "from"])
def test_the_graph_names_the_row_the_name_and_both_files(tmp_path, case, end):
    dup = DUPLICATES[case][0]
    g = load(build(tmp_path, dup, end=end))
    mine = [k for k in g.skipped if k.path == PATH]
    assert [(k.row, k.line) for k in mine] == [(ROW_AT, g.narrative("bad").table.rows[1].line)]
    both = ", ".join(sorted([dup, ORIGINAL]))
    assert mine[0].reason == f"the `{end}` end `water` is carried by more than one page: {both}"
    assert mine[0].fix is not None and "rename" in mine[0].fix
    assert g.edge("holds", "farmers", "water") is None


VIEWS = {
    "edge_table": lambda r: scat_tools.edge_table("holds", root=r),
    "layered": lambda r: scat_tools.layered(root=r),
    "layered-named": lambda r: scat_tools.layered(["bad"], root=r),
    "trace": lambda r: scat_tools.trace("farmers", root=r),
    "fingerprint": lambda r: scat_tools.fingerprint(root=r),
    "fingerprint-named": lambda r: scat_tools.fingerprint("bad", root=r),
}


@pytest.mark.parametrize("view", VIEWS)
@pytest.mark.parametrize("case", DUPLICATES)
def test_views_refuse_naming_the_row_and_both_files(tmp_path, case, view):
    dup = DUPLICATES[case][0]
    root = build(tmp_path, dup)
    before = tree_hash(root)
    out = VIEWS[view](root)
    assert not out.ok
    refused = {r["subject"]: r for r in out.to_dict()["refused"]}
    if case == "not-a-node" and view in ("layered", "fingerprint"):
        # these draw the duplicate narrative itself, whose SCAT-NAME error refuses first
        assert any(p["rule"] == "SCAT-NAME" for p in out.to_dict()["problems"])
        return
    mine = refused[f"{PATH} row {ROW_AT}"]
    assert "`water`" in mine["why"]
    assert dup in mine["why"] and ORIGINAL in mine["why"]
    assert "rename one of the pages" in mine["fix"]["options"][0]["text"]
    assert tree_hash(root) == before


def test_other_reasons_keep_their_fix(tmp_path):
    root = write(
        tmp_path / "v",
        base_files()
        | {PATH: narrative("Bad", "x", [row("holds", "farmers", "ghost")], "draft", "scenario")},
    )
    fix = scat_tools.fingerprint("bad", root=root).to_dict()["refused"][0]["fix"]["options"][0][
        "text"
    ]
    assert fix == f"fix the row (`scat check {PATH}` says how), then run this again"


@pytest.mark.parametrize("case", DUPLICATES)
def test_a_clean_narrative_still_draws(tmp_path, case):
    root = build(tmp_path, DUPLICATES[case][0])
    assert scat_tools.fingerprint("diamond", root=root).ok
    assert scat_tools.layered(["diamond"], root=root).ok


def test_the_edge_appears_once_one_duplicate_is_renamed(tmp_path):
    root = build(tmp_path, "concern/extra/water.md")
    (root / "concern/extra/water.md").rename(root / "concern/extra/rain.md")
    g = load(root)
    assert g.skipped == ()
    assert g.edge("holds", "farmers", "water") is not None
    assert [t.path for t in g.edge("holds", "farmers", "water").tellings if t.path == PATH] == [
        PATH
    ]
    assert scat_tools.fingerprint("bad", root=root).ok
