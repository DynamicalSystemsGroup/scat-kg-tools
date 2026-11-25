"""Views refuse, as data, and write nothing."""

import json

import pytest
from viewutil import page, tree_hash

import scat_kg
from scat_kg.ops.result import Result

BAD_ROW = "| holds | farmers | [[water]] | |"  # the `from` end is plain text, not a link


def refused(view, subject_has=None):
    assert isinstance(view, Result) and not isinstance(view, scat_kg.View)
    assert view.ok is False
    d = view.to_dict()
    assert d["kind"] == "operation" and d["ok"] is False and d["schema_version"] == 2
    assert len(d["refused"]) == 1
    if subject_has:
        assert subject_has in d["refused"][0]["subject"]
    assert "refused" in str(view)
    return d


def bad_narrative(status):
    from viewutil import narrative

    return narrative("Bad", "The [[water]] ran out.", [BAD_ROW], status, "scenario")


# ---------------------------------------------------------------- names, types, directions, folders


def test_unknown_narrative(vault):
    d = refused(scat_kg.fingerprint("nope", root=vault), "nope")
    assert d["refused"][0]["why"] == "no narrative has this name"
    assert d["problems"] == []
    assert refused(scat_kg.layered(["dry", "nope"], root=vault), "nope")


def test_a_node_is_not_a_narrative_and_a_narrative_is_not_a_node(vault):
    refused(scat_kg.fingerprint("water", root=vault), "water")
    refused(scat_kg.layered(["water"], root=vault), "water")
    refused(scat_kg.trace("dry", root=vault), "dry")


def test_unknown_node(vault):
    d = refused(scat_kg.trace("nope", root=vault), "nope")
    assert "no node has this name" in d["refused"][0]["why"]


def test_ambiguous_name(make):
    root = make(
        {"concern/dup.md": page("concern", "Dup"), "technology/dup.md": page("technology", "Dup")}
    )
    d = refused(scat_kg.trace("dup", root=root), "dup")
    assert d["refused"][0]["why"] == (
        "more than one page has this name: concern/dup.md, technology/dup.md"
    )
    refused(scat_kg.fingerprint("dup", root=root), "dup")


def test_unknown_edge_type(vault):
    d = refused(scat_kg.edge_table("loves", root=vault), "loves")
    assert d["refused"][0]["fix"]["options"] or d["refused"][0]["fix"]
    assert "holds, addressed-by, provided-by" in str(scat_kg.edge_table("loves", root=vault))
    # the verb is not the slug
    refused(scat_kg.edge_table("is addressed by", root=vault))


def test_bad_direction(vault):
    refused(scat_kg.trace("farmers", "sideways", root=vault), "sideways")
    assert "up, down, both" in str(scat_kg.trace("farmers", "sideways", root=vault))


def test_missing_vault_folder(tmp_path):
    gone = tmp_path / "gone"
    for view in (
        scat_kg.fingerprint(root=gone),
        scat_kg.fingerprint("dry", root=gone),
        scat_kg.edge_table("holds", root=gone),
        scat_kg.layered(root=gone),
        scat_kg.trace("farmers", root=gone),
    ):
        d = refused(view, "gone")
        assert d["refused"][0]["why"] == "the vault folder does not exist"
    assert not gone.exists()


# ---------------------------------------------------------------- errors in the pages drawn


def test_a_done_narrative_with_an_error_refuses_and_carries_the_problems(make):
    root = make({"narrative/bad.md": bad_narrative("done")})
    view = scat_kg.fingerprint("bad", root=root)
    d = refused(view, "narrative/bad.md")
    assert d["problems"], "the problems travel with the refusal"
    assert {p["severity"] for p in d["problems"]} == {"error"}
    assert {p["file"] for p in d["problems"]} == {"narrative/bad.md"}
    assert "SCAT-DONE-END-NOLINK" in {p["rule"] for p in d["problems"]}
    assert all(p["fix"] for p in d["problems"])
    assert "SCAT-DONE-END-NOLINK" in str(view)
    assert d["refused"][0]["why"] == f"{len(d['problems'])} error(s) in the pages this view draws"
    json.dumps(d)


def test_a_draft_narrative_with_the_same_row_only_warns(make):
    root = make({"narrative/bad.md": bad_narrative("draft")})
    # the row tells no edge; the view no longer leaves it out silently but refuses, naming the row
    # (the check stays a warning: no problems travel with this refusal)
    d = refused(scat_kg.fingerprint("bad", root=root), "narrative/bad.md row 1")
    assert d["problems"] == []
    refused(scat_kg.layered(root=root), "narrative/bad.md row 1")
    assert scat_kg.fingerprint("dry", root=root).ok


def test_the_whole_vault_refuses_on_any_narrative_error_but_a_named_view_does_not(make):
    root = make({"narrative/bad.md": bad_narrative("done")})
    refused(scat_kg.fingerprint(root=root), "narrative/bad.md")
    refused(scat_kg.layered(root=root), "narrative/bad.md")
    # the error is in a page these views do not draw
    assert scat_kg.fingerprint("dry", root=root).ok
    assert scat_kg.layered(["dry", "wet"], root=root).ok
    # the edge table and the trace draw every narrative, so they refuse too
    refused(scat_kg.edge_table("holds", root=root), "narrative/bad.md")
    refused(scat_kg.trace("farmers", root=root), "narrative/bad.md")


def test_an_error_on_a_node_page_in_the_result_refuses(make):
    root = make({"concern/water.md": page("concern", "Water", "bogus")})
    d = refused(scat_kg.trace("farmers", root=root), "concern/water.md")
    assert [p["rule"] for p in d["problems"]] == ["SCAT-FM-STATUS"]
    refused(scat_kg.fingerprint("dry", root=root))
    refused(scat_kg.edge_table("holds", root=root))
    refused(scat_kg.layered(["dry"], root=root))
    # views whose result does not hold `water` still work
    assert scat_kg.trace("towns", root=root).ok
    assert scat_kg.fingerprint("split", root=root).ok
    assert scat_kg.edge_table("provided-by", root=root).ok


def test_a_warning_on_a_node_page_does_not_refuse(make):
    # a draft page missing its description only warns
    root = make({"concern/water.md": page("concern", "Water", "draft")})
    assert scat_kg.trace("farmers", root=root).ok


# ---------------------------------------------------------------- views write nothing

CALLS = {
    "fingerprint": lambda r: scat_kg.fingerprint(root=r),
    "fingerprint-one": lambda r: scat_kg.fingerprint("dry", root=r),
    "edge-table": lambda r: scat_kg.edge_table("holds", root=r),
    "layered": lambda r: scat_kg.layered(root=r),
    "layered-some": lambda r: scat_kg.layered(["split"], root=r),
    "trace": lambda r: scat_kg.trace("farmers", root=r),
    "refusal-name": lambda r: scat_kg.trace("nope", root=r),
    "refusal-type": lambda r: scat_kg.edge_table("loves", root=r),
}


@pytest.mark.parametrize("name", CALLS)
def test_a_view_writes_nothing(vault, name):
    before = tree_hash(vault)
    CALLS[name](vault)
    assert tree_hash(vault) == before


@pytest.mark.parametrize("name", ["fingerprint", "layered", "trace"])
def test_a_refusal_for_errors_writes_nothing(make, name):
    root = make(
        {
            "narrative/bad.md": bad_narrative("done"),
            "concern/water.md": page("concern", "W", "bogus"),
        }
    )
    before = tree_hash(root)
    CALLS[name](root)
    assert tree_hash(root) == before


def test_the_tree_hash_sees_a_new_empty_folder(vault):
    before = tree_hash(vault)
    (vault / "views").mkdir()
    assert tree_hash(vault) != before
