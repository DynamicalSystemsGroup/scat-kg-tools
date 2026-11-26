"""WP24-G1, R1: the evidence view of one node page.

Built vaults (viewutil) give hand-computed answers: the narratives that link the node, the paragraph around each
link with its sentences marked, the narratives that tell no edge for the node, edges with notes, adjacent nodes.
Refusals, the string guard, the schema, and that nothing is written.
"""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from viewutil import base_files, narrative, page, row, tree_hash, write

import scat_kg
from scat_kg.cli import main
from scat_kg.ops.result import Result

ROOT = Path(__file__).resolve().parents[2]
RANGE = ROOT / "research" / "range" / "koi" / "vault"
SCHEMA = json.loads((ROOT / "contracts" / "machine-interface.schema.json").read_text("utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)

LONG = (
    "Pumps came first.\n\n"
    "The [[farmers]] spoke first. They blamed the delay on the pumps, and the [[water]] stayed.\n"
    "A second line of the same paragraph. Later the [[water]] fell! Was it enough?\n\n"
    "- a list item about [[water]]\n"
    "- another about nothing\n"
    "1. a third, about [[water]]\n\n"
    "Last paragraph, also [[water]]; `code [[cost]]` is not read."
)


def files() -> dict[str, str]:
    return base_files() | {
        "narrative/long.md": narrative(
            "Long", LONG, [row("holds", "farmers", "water")], "draft", "scenario"
        ),
        "narrative/ghost.md": narrative("Ghost", "No links here.", None, "stub"),
    }


@pytest.fixture
def built(tmp_path):
    return write(tmp_path / "built", files())


def doc(root, node):
    view = scat_kg.evidence(node, root=root)
    assert view.ok, str(view)
    return view.to_dict()


def by_name(d):
    return {n["name"]: n for n in d["narratives"]}


def test_the_document_of_a_node(built):
    d = doc(built, "water")
    assert (d["schema_version"], d["kind"], d["operation"], d["ok"], d["mode"]) == (
        3,
        "view",
        "evidence",
        True,
        "disallowed",
    )
    assert (d["node"], d["node_type"], d["node_status"]) == ("water", "concern", "draft")
    assert [n["name"] for n in d["narratives"]] == ["dry", "long", "wet"]  # path order
    assert [(e["type"], e["from"], e["to"]) for e in d["edges"]] == [
        ("holds", "farmers", "water"),
        ("addressed-by", "water", "alert"),
        ("addressed-by", "water", "sensor"),
    ]
    assert {k: [n["name"] for n in v] for k, v in d["adjacent"].items()} == {
        "group": ["farmers"],
        "concern": [],
        "affordance": ["alert", "sensor"],
        "technology": [],
    }
    assert list(d["adjacent"]) == ["group", "concern", "affordance", "technology"]
    assert [x["name"] for x in d["excluded"]] == ["ghost"]  # reported as the other views do


def test_a_narrative_with_its_status_kind_and_timeframe(built):
    n = by_name(doc(built, "water"))["dry"]
    assert (n["status"], n["kind"], n["timeframe"]) == ("draft", "scenario", None)
    assert n["tells_edge"] is True


def test_every_edge_has_the_narratives_that_tell_it_and_the_rows_note(tmp_path):
    root = write(
        tmp_path / "v",
        base_files()
        | {
            "narrative/dry.md": narrative(
                "Dry",
                "The [[farmers]] worry about [[water]].",
                ["| [[farmers]] | holds | [[water]] | a note, with `code` |"],
                "draft",
                "scenario",
            )
        },
    )
    e = doc(root, "water")["edges"][0]
    assert e["narratives"] == ["dry", "wet"]
    assert e["tellings"] == [
        {"narrative": "dry", "note": "a note, with `code`"},
        {"narrative": "wet", "note": ""},
    ]
    assert e["status"] == "stub"  # the least advanced of the narratives that tell it


def test_the_whole_paragraph_is_returned_and_the_sentence_that_links_is_marked(built):
    paragraphs = by_name(doc(built, "farmers"))["long"]["paragraphs"]
    assert len(paragraphs) == 1  # the link is in one paragraph only
    p = paragraphs[0]
    assert p["paragraph"] == (
        "The [[farmers]] spoke first. They blamed the delay on the pumps, and the [[water]] stayed.\n"
        "A second line of the same paragraph. Later the [[water]] fell! Was it enough?"
    )
    # the link is not on the sentence that matters: the paragraph carries the next sentence
    assert "They blamed the delay on the pumps" in p["paragraph"]
    assert [s["text"] for s in p["sentences"]] == ["The [[farmers]] spoke first."]
    lines = (built / "narrative" / "long.md").read_text("utf-8").split("\n")
    assert lines[p["line"] - 1].startswith("The [[farmers]] spoke first.")  # the file line, 1-based


def test_a_paragraph_with_several_links_is_one_entry_with_each_sentence_that_links(built):
    paragraphs = by_name(doc(built, "water"))["long"]["paragraphs"]
    assert [p["paragraph"].split("\n")[0][:20] for p in paragraphs] == [
        "The [[farmers]] spok",
        "- a list item about ",
        "Last paragraph, also",
    ]
    first, items, last = paragraphs
    assert [s["text"] for s in first["sentences"]] == [
        "They blamed the delay on the pumps, and the [[water]] stayed.",
        "Later the [[water]] fell!",
    ]
    assert [s["text"] for s in items["sentences"]] == [
        "a list item about [[water]]",
        "a third, about [[water]]",
    ]
    assert [s["text"] for s in last["sentences"]] == [
        "Last paragraph, also [[water]]; `code [[cost]]` is not read."
    ]


def test_offsets_find_each_sentence_in_its_paragraph(built):
    for node in ("water", "farmers", "cost"):
        for n in doc(built, node)["narratives"]:
            for p in n["paragraphs"]:
                assert p["sentences"]
                for s in p["sentences"]:
                    assert p["paragraph"][s["start"] : s["end"]] == s["text"]


def test_a_link_inside_the_edges_table_is_not_a_paragraph_and_shows_through_the_edges(built):
    n = by_name(doc(built, "water"))["wet"]  # `wet` links water only in its table
    assert n["paragraphs"] == [] and n["tells_edge"] is True
    assert "wet" in doc(built, "water")["edges"][0]["narratives"]


def test_a_narrative_that_links_the_node_and_tells_no_edge_for_it_is_flagged(built):
    d = doc(built, "farmers")
    flags = {n["name"]: n["tells_edge"] for n in d["narratives"]}
    assert flags == {"diamond": True, "dry": True, "empty": False, "long": True, "wet": True}
    text = str(scat_kg.evidence("farmers", root=built))
    assert "\n    empty [draft]; tells no edge for this node\n" in text
    assert text.count("tells no edge for this node") == 1


def test_the_text_form_starts_with_the_mode_and_marks_the_sentence(built):
    text = str(scat_kg.evidence("farmers", root=built))
    lines = text.split("\n")
    assert lines[0] == "attribution mode: disallowed"
    assert lines[1] == "evidence farmers (group, draft): 5 narratives, 2 edges"
    assert (
        str(scat_kg.evidence("cost", root=built)).split("\n")[1].endswith(": 2 narratives, 3 edges")
    )
    assert (
        str(scat_kg.evidence("idle", root=built)).split("\n")[1].endswith(": 0 narratives, 0 edges")
    )
    assert (
        str(scat_kg.evidence("radio", root=built)).split("\n")[1].endswith(": 1 narrative, 1 edge")
    )
    assert (
        "        >>The [[farmers]] spoke first.<< They blamed the delay on the pumps, and" in text
    )
    assert (
        "        A second line of the same paragraph. Later the [[water]] fell! Was it enough?"
        in text
    )
    assert "  adjacent nodes\n    concern\n      cost [stub]\n      water [draft]\n" in text + "\n"
    assert text.endswith(
        "excluded (no node page linked; link one node page to include it)\n    ghost (narrative/ghost.md)"
    )


def test_a_node_no_narrative_links_has_nothing_and_says_so(built):
    d = doc(built, "idle")
    assert d["narratives"] == [] and d["edges"] == []
    assert all(v == [] for v in d["adjacent"].values())
    assert "    none\n  edges\n    none\n  adjacent nodes\n    none" in str(
        scat_kg.evidence("idle", root=built)
    )


def test_it_writes_nothing(built):
    before = tree_hash(built)
    scat_kg.evidence("water", root=built)
    assert tree_hash(built) == before


# ---- refusals


def contributor_vault(tmp_path):
    root = write(tmp_path / "opt", base_files())
    (root / "scat.toml").write_text(
        "attribution = 'optional'\nstakeholder_group_cap = 3\n", "utf-8"
    )
    write(root, {"contributor/ada-quill.md": page("contributor", "Ada Quill", "done")})
    return root


@pytest.mark.parametrize(
    ("name", "why"),
    [
        ("nope", "no node has this name"),
        ("dry", "no node has this name"),  # a narrative
        ("ada-quill", "no node has this name"),  # a contributor page
        ("concern", "no node has this name"),  # not a page: an index page is not a note
    ],
)
def test_a_name_that_is_not_a_node_page_is_refused_with_a_fix(tmp_path, name, why):
    r = scat_kg.evidence(name, root=contributor_vault(tmp_path))
    assert not r.ok and isinstance(r, Result) and not isinstance(r, scat_kg.View)
    d = r.to_dict()
    assert d["kind"] == "operation" and d["operation"] == "evidence" and d["ok"] is False
    assert why in d["refused"][0]["why"]
    assert "Fix: give the name of a page" in str(r)


def test_a_name_carried_by_two_pages_is_refused(tmp_path):
    root = write(tmp_path / "v", base_files() | {"concern/other/water.md": page("concern", "Twin")})
    r = scat_kg.evidence("water", root=root)
    assert not r.ok and "more than one page has this name" in str(r)
    assert "Fix: rename one of the pages" in str(r)


@pytest.mark.parametrize("value", [5, None, ["water"], b"water", {"water"}])
def test_a_value_that_is_not_text_is_refused_with_a_fix(built, value):
    r = scat_kg.evidence(value, root=built)
    assert not r.ok
    d = r.to_dict()
    assert d["kind"] == "operation" and len(d["refused"]) == 1
    assert "Fix: pass a node name as a string" in str(r)


def test_a_vault_with_an_error_in_a_page_it_draws_is_refused_with_the_problems(tmp_path):
    bad = narrative("Bad", "Only [[water]] here.", ["| farmers | holds | [[water]] | |"])
    root = write(tmp_path / "v", base_files() | {"narrative/bad.md": bad})
    r = scat_kg.evidence("water", root=root)
    assert not r.ok and "bad.md row 1" in str(r)
    assert scat_kg.evidence("idle", root=root).ok  # a page it does not draw is not its business


def test_a_missing_vault_folder_is_refused(tmp_path):
    r = scat_kg.evidence("water", root=tmp_path / "gone")
    assert not r.ok and "the vault folder does not exist" in str(r)


# ---- the schema


NODES = ("water", "farmers", "cost", "idle", "probe")


@pytest.mark.parametrize("node", NODES)
def test_the_evidence_document_validates(built, node):
    assert list(VALIDATOR.iter_errors(doc(built, node))) == []


def test_the_range_vault_documents_validate():
    for node in ("community-members", "forget-signal", "ethnographers"):
        assert list(VALIDATOR.iter_errors(doc(RANGE, node))) == []


def test_a_refusal_validates(built):
    assert list(VALIDATOR.iter_errors(scat_kg.evidence("nope", root=built).to_dict())) == []


@pytest.mark.parametrize(
    "break_it",
    [
        lambda d: d.pop("adjacent"),
        lambda d: d.pop("node_type"),
        lambda d: d["narratives"][0].pop("tells_edge"),
        lambda d: d["narratives"][0]["paragraphs"][0].pop("sentences"),
        lambda d: d["narratives"][0]["paragraphs"][0]["sentences"][0].pop("end"),
        lambda d: d["edges"][0].pop("tellings"),
        lambda d: d["edges"][0]["tellings"][0].pop("note"),
        lambda d: d.update(schema_version=2),
    ],
)
def test_the_schema_requires_each_part(built, break_it):
    d = doc(built, "water")
    break_it(d)
    assert list(VALIDATOR.iter_errors(d)) != []


# ---- the front ends agree


def cli_json(capsys, *argv):
    code = main(["evidence", *argv, "--json"])
    return code, json.loads(capsys.readouterr().out)


def test_the_cli_json_is_the_python_document(built, capsys):
    for node in NODES:
        code, got = cli_json(capsys, node, "--root", str(built))
        assert code == 0 and got == doc(built, node)


def test_on_the_range_vault_the_cli_json_is_the_python_document(capsys):
    code, got = cli_json(capsys, "community-members", "--root", str(RANGE))
    d = doc(RANGE, "community-members")
    assert code == 0 and got == d
    assert len(d["narratives"]) >= 4 and d["edges"] and d["adjacent"]["concern"]


def test_the_cli_prints_the_text_and_exits_1_on_a_refusal(built, capsys):
    assert main(["evidence", "water", "--root", str(built)]) == 0
    assert capsys.readouterr().out.startswith("attribution mode: disallowed\nevidence water")
    assert main(["evidence", "dry", "--root", str(built)]) == 1
    assert "refused dry: no node has this name" in capsys.readouterr().out


def test_a_row_of_another_table_is_its_own_block_and_is_not_cut_across_cells(tmp_path):
    account = (
        "Before the table. Still [[water]] here\n"
        "| who | said. what |\n|---|---|\n"
        "| [[farmers]]. Yes | [[water]]. No |\n"
        "After the table."
    )
    root = write(
        tmp_path / "v", base_files() | {"narrative/t.md": narrative("T", account, None, "draft")}
    )
    ps = by_name(doc(root, "water"))["t"]["paragraphs"]
    assert [p["paragraph"] for p in ps] == [
        "Before the table. Still [[water]] here",
        "| [[farmers]]. Yes | [[water]]. No |",
    ]
    assert [s["text"] for s in ps[0]["sentences"]] == ["Still [[water]] here"]
    assert [s["text"] for s in ps[1]["sentences"]] == ["| [[farmers]]. Yes | [[water]]. No |"]
    assert all(
        p["paragraph"][s["start"] : s["end"]] == s["text"] for p in ps for s in p["sentences"]
    )
