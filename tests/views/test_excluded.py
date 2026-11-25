"""WP21-G2: an uncoded narrative (it links no node page) is excluded from the graph and every view, and says so.

One test for each case: uncoded and excluded everywhere; coded by a row end; coded by an account link alone
(conformant, its node in the fingerprint); adding one link includes it; the machine interface carries the record.
"""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from viewutil import narrative, row, tree_hash

import scat_kg
from scat_kg import cli, draw
from scat_kg.graph import load

SCHEMA = json.loads(
    (Path(__file__).resolve().parents[2] / "contracts" / "machine-interface.schema.json").read_text(
        encoding="utf-8"
    )
)
VALIDATOR = Draft202012Validator(SCHEMA)
GHOST = "narrative/ghost.md"
HOW = "link one node page"


def ghost(account="Nothing here names a node.", rows=None, status="draft"):
    return {GHOST: narrative("Ghost", account, rows, status, "scenario")}


def excluded_of(view):
    return {x["name"]: x for x in view.to_dict()["excluded"]}


def every_view(root):
    return [
        scat_kg.fingerprint(root=root),
        scat_kg.edge_table("holds", root=root),
        scat_kg.layered(root=root),
        scat_kg.trace("farmers", root=root),
    ]


# --- uncoded: left out of the graph and every view, and reported


def test_an_uncoded_narrative_is_left_out_of_the_graph_and_recorded_as_excluded(make):
    g = load(make(ghost()))
    assert g.narrative("ghost") is None and "ghost" not in {n.name for n in g.narratives}
    assert [(x.narrative, x.path) for x in g.excluded] == [("ghost", GHOST)]
    assert g.summary()["excluded"] == 1


def test_an_uncoded_narrative_is_in_no_view_and_every_view_that_draws_all_reports_it(make):
    plain = every_view(make())
    root = make(ghost())
    for before, view in zip(plain, every_view(root), strict=True):
        assert view.ok, str(view)
        d, d0 = view.to_dict(), before.to_dict()
        assert d.pop("excluded") == [
            {"name": "ghost", "file": GHOST, "fix": excluded_of(view)["ghost"]["fix"]}
        ]
        assert HOW in excluded_of(view)["ghost"]["fix"]
        assert (
            d0.pop("excluded") == [] and d == d0
        )  # the rest of the view is as if the page were not there
        text = str(view)
        assert "excluded" in text and "ghost" in text and HOW in text
        assert "ghost" not in str(before)


def test_an_uncoded_narrative_is_named_by_check_as_excluded(make):
    root = make(ghost())
    found = [p for p in scat_kg.check(root=root).problems if p.rule == "SCAT-UNCODED"]
    assert [(p.file, p.severity) for p in found] == [(GHOST, "warning")]
    assert "excluded" in found[0].what and "node page" in found[0].fix
    assert scat_kg.check(root=root).ok  # a warning: it never blocks


def test_naming_an_uncoded_narrative_in_a_view_is_refused_and_says_how_to_include_it(make):
    root = make(ghost())
    for out in (scat_kg.fingerprint("ghost", root=root), scat_kg.layered(["ghost"], root=root)):
        assert not out.ok
        r = out.to_dict()["refused"][0]
        assert r["subject"] == "ghost" and "excluded" in r["why"]
        assert HOW in r["fix"]["options"][0]["text"]


def test_a_row_of_an_uncoded_narrative_holds_no_edge_up(make):
    # its rows link no node page (a page that is not a node, a page that does not exist): no edge, no refusal
    rows = [row("holds", "dry", "ghost-two"), "| farmers | holds | water | |"]
    root = make(ghost(rows=rows))
    g = load(root)
    assert [x.narrative for x in g.excluded] == ["ghost"]
    assert g.skipped == () and {e.key for e in g.edges} == {e.key for e in load(make()).edges}
    assert scat_kg.edge_table("holds", root=root).ok


def test_an_export_leaves_out_an_uncoded_narrative_and_notes_it(make, tmp_path):
    out = tmp_path / "tables"
    with_ghost = scat_kg.export_edges(out, root=make(ghost()))
    assert with_ghost.ok and any("excluded ghost" in n and HOW in n for n in with_ghost.notes)
    assert "ghost" not in "".join(p.read_text() for p in out.iterdir())


def test_a_drawing_names_the_excluded_narratives_and_a_named_one_is_refused(make, tmp_path):
    root = make(ghost())
    drawing = draw.layered(root=root)
    assert (
        isinstance(drawing, draw.Drawing)
        and "excluded" in drawing.svg()
        and "ghost" in drawing.svg()
    )
    assert not draw.fingerprint("ghost", root=root).ok


def test_the_check_and_the_cli_text_report_the_exclusion(make, capsys):
    root = make(ghost())
    assert cli.main(["check", "--root", str(root)]) == 0
    assert "SCAT-UNCODED" in capsys.readouterr().out
    assert cli.main(["fingerprint", "--root", str(root)]) == 0
    assert "excluded" in capsys.readouterr().out


# --- coded by a row end, or by an account link alone: included


def test_a_narrative_coded_by_a_row_end_is_included(make):
    root = make(ghost(rows=[row("holds", "towns", "water")]))
    g = load(root)
    assert g.excluded == () and g.narrative("ghost").nodes == ("towns", "water")
    assert [e.key.from_node for e in g.edges if "ghost" in e.narratives] == ["towns"]
    assert "SCAT-UNCODED" not in {p.rule for p in scat_kg.check(root=root).problems}
    assert excluded_of(scat_kg.fingerprint(root=root)) == {}


def test_a_narrative_coded_by_an_account_link_alone_is_included_and_conformant(make):
    page = narrative("Ghost", "Only the [[towns]] spoke.", None, "done", "scenario")
    page = page.replace('title: "Ghost"\n', 'title: "Ghost"\ndescription: "D"\ntimeframe: past\n')
    root = make({GHOST: page})
    g = load(root)
    assert g.excluded == () and g.narrative("ghost").nodes == ("towns",)
    assert g.narrative("ghost").edges == ()
    report = scat_kg.check("ghost", root=root)
    assert report.errors == () and {p.rule for p in report.problems} <= {"SCAT-NOEDGES"}
    one = scat_kg.fingerprint("ghost", root=root).to_dict()["narratives"][0]
    assert [n["name"] for n in one["nodes"]] == ["towns"] and one["edges"] == []
    assert scat_kg.set_status("ghost", "done", root=root).ok


def test_a_link_in_a_list_beyond_the_text_codes_a_narrative(make):
    root = make(ghost("No names.\n\n## Linked beyond the text\n\n- [[cost]]\n"))
    assert load(root).narrative("ghost").nodes == ("cost",)


def test_a_link_to_a_page_that_is_not_a_node_or_in_a_code_span_does_not_code(make):
    root = make(ghost("See [[dry]], [[nowhere]], [[photo.png]] and `[[farmers]]`."))
    assert [x.narrative for x in load(root).excluded] == ["ghost"]


def test_adding_one_link_includes_an_excluded_narrative(make, tmp_path):
    root = make(ghost())
    assert [x.narrative for x in load(root).excluded] == ["ghost"]
    page = root / GHOST
    page.write_text(
        page.read_text(encoding="utf-8").replace("names a node", "names [[cost]], a node")
    )
    g = load(root)
    assert g.excluded == () and g.narrative("ghost").nodes == ("cost",)
    for view in every_view(root):
        assert view.to_dict()["excluded"] == []
    assert "ghost" in [n["name"] for n in scat_kg.fingerprint(root=root).to_dict()["narratives"]]
    assert "SCAT-UNCODED" not in {p.rule for p in scat_kg.check(root=root).problems}


def test_an_edge_never_waits_on_an_excluded_narrative(make):
    # whatever is written, an edge's narratives are all coded: a row tells an edge only through node links
    rows = [row("holds", "farmers", "water"), "| [[farmers\\|F]] | holds | ![[water]] | |"]
    root = make(ghost(rows=rows))
    g = load(root)
    assert g.excluded == ()
    gone = load(make({GHOST: None}))
    coded = {n.name for n in g.narratives}
    assert all(set(e.narratives) <= coded for e in g.edges) and gone.excluded == ()


# --- the machine interface


@pytest.mark.parametrize("which", range(4))
def test_the_view_documents_with_an_excluded_record_validate(make, which):
    doc = every_view(make(ghost()))[which].to_dict()
    assert doc["excluded"] and doc["schema_version"] == 2
    assert list(VALIDATOR.iter_errors(doc)) == []


def test_the_schema_requires_each_part_of_the_excluded_record(make):
    doc = scat_kg.fingerprint(root=make(ghost())).to_dict()
    for field in ("name", "file", "fix"):
        broken = json.loads(json.dumps(doc))
        del broken["excluded"][0][field]
        assert not VALIDATOR.is_valid(broken), field
    broken = json.loads(json.dumps(doc))
    broken["excluded"][0]["file"] = "/abs/path.md"
    assert not VALIDATOR.is_valid(broken)
    broken = json.loads(json.dumps(doc))
    broken["excluded"] = "ghost"
    assert not VALIDATOR.is_valid(broken)


def test_a_view_document_without_the_field_still_validates_and_the_version_is_unchanged(make):
    doc = scat_kg.fingerprint(root=make()).to_dict()
    del doc["excluded"]
    assert VALIDATOR.is_valid(doc)  # adding a field keeps the version (R-16)
    assert doc["schema_version"] == 2


def test_json_on_the_command_line_carries_the_excluded_record(make, capsys):
    root = make(ghost())
    assert cli.main(["layered", "--root", str(root), "--json"]) == 0
    doc = json.loads(capsys.readouterr().out)
    assert doc["excluded"] == [{"name": "ghost", "file": GHOST, "fix": doc["excluded"][0]["fix"]}]
    assert VALIDATOR.is_valid(doc)


def test_the_checking_leaves_the_vault_as_it_was(make):
    root = make(ghost())
    before = tree_hash(root)
    every_view(root)
    scat_kg.check(root=root)
    assert tree_hash(root) == before
