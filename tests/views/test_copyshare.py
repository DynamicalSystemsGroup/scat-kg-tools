"""WP24-G2, R2: the copy-share view: the share of a node page's five-word runs found word for word in a narrative.

Built vaults give hand-computed answers: a page that copies a paragraph scores high and names the narrative, an
honest synthesis scores low, a stub scores null; CLI, Python and the schema agree; refusals; nothing is written; on
the G6 vault the copy-heavy pages score above the synthesised ones.
"""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from viewutil import base_files, narrative, page, row, tree_hash, write

import scat_tools
from scat_tools.cli import main
from scat_tools.ops.result import Result

ROOT = Path(__file__).resolve().parents[2]
G6 = ROOT / "research" / "node-pages" / "vault" / "disallowed"
SCHEMA = json.loads((ROOT / "contracts" / "machine-interface.schema.json").read_text("utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)

PARA = (
    "The [[farmers]] told us that the pump broke every dry July, and nobody came to mend it until the "
    "[[towns]] complained to the council."
)
OTHER = "Rain fell on the fields in March, and the river rose past the old stone bridge."


def files() -> dict[str, str]:
    return base_files() | {
        "narrative/pump.md": narrative("Pump", PARA, [row("holds", "farmers", "water")], "draft"),
        "narrative/river.md": narrative("River", OTHER, [row("holds", "towns", "cost")], "draft"),
        # copied: the paragraph of `pump`, with the links shown as text and the case changed
        "concern/water.md": page(
            "concern",
            "Water",
            "draft",
            'description: "What the farmers fear."\n',
            "The Farmers told us that the pump broke every dry July, and nobody came to mend it "
            "until the towns complained to the council.\n",
        ),
        # a synthesis: no five words in a row are in a narrative
        "concern/cost.md": page(
            "concern",
            "Cost",
            "draft",
            'description: "Money, again."\n',
            "Two accounts disagree about who pays. One says the council; the other blames the "
            "[[farmers]]. Neither says what mending costs.\n",
        ),
        "narrative/empty.md": narrative("Empty", "Only the [[farmers]] spoke."),
    }


@pytest.fixture
def built(tmp_path):
    return write(tmp_path / "built", files())


def doc(root, node=None):
    view = scat_tools.copy_share(node, root=root)
    assert view.ok, str(view)
    return view.to_dict()


def entries(d):
    return {e["name"]: e for e in d["pages"]}


def test_the_document(built):
    d = doc(built)
    assert (d["schema_version"], d["kind"], d["operation"], d["ok"], d["mode"]) == (
        3,
        "view",
        "copy-share",
        True,
        "disallowed",
    )
    assert sorted(entries(d)) == sorted(
        n.name for ns in scat_tools.load(root=built).nodes.values() for n in ns
    )
    assert VALIDATOR.is_valid(d), list(VALIDATOR.iter_errors(d))[:3]


def test_a_copied_page_scores_high_and_names_the_narrative(built):
    e = entries(doc(built))["water"]
    assert e["share"] > 0.8 and e["narratives"] == ["pump"]
    assert (e["type"], e["status"]) == ("concern", "draft")


def test_a_synthesis_scores_low(built):
    e = entries(doc(built))["cost"]
    assert e["share"] == 0.0 and e["narratives"] == []
    assert e["words"] > 5


def test_a_stub_scores_null(built):
    e = entries(doc(built))["towns"]
    assert e["words"] == 0 and e["share"] is None and e["narratives"] == []


def test_sorted_by_share_highest_first_null_last_then_name(built):
    shares = [e["share"] for e in doc(built)["pages"]]
    known = [s for s in shares if s is not None]
    assert known == sorted(known, reverse=True)
    assert shares[: len(known)] == known and all(s is None for s in shares[len(known) :])
    zeros = [e["name"] for e in doc(built)["pages"] if e["share"] == 0.0]
    assert zeros == sorted(zeros)


def test_a_run_may_span_a_sentence_and_punctuation_counts_for_nothing(tmp_path):
    root = write(
        tmp_path / "v",
        base_files()
        | {
            "narrative/pump.md": narrative(
                "Pump", "It broke. Nobody came; the [[farmers]] waited."
            ),
            "concern/cost.md": page(
                "concern", "Cost", "draft", "", "it broke - nobody came, THE FARMERS waited\n"
            ),
        },
    )
    assert entries(doc(root))["cost"]["share"] == 1.0


def test_a_link_counts_as_its_shown_text_or_its_name(tmp_path):
    root = write(
        tmp_path / "v",
        base_files()
        | {
            "narrative/pump.md": narrative(
                "Pump", "Some [[farmers|hill farmers]] came to see the [[water]]."
            ),
            "concern/cost.md": page(
                "concern", "Cost", "draft", "", "some hill farmers came to see the water\n"
            ),
        },
    )
    assert entries(doc(root))["cost"]["share"] == 1.0


def test_the_edges_told_section_of_a_page_is_ignored(tmp_path):
    root = write(
        tmp_path / "v",
        base_files()
        | {
            "narrative/pump.md": narrative(
                "Pump", "Plain words that are not repeated anywhere else."
            ),
            "concern/cost.md": page(
                "concern",
                "Cost",
                "draft",
                "",
                "Nothing here is told by any narrative at all, so none of it is.\n\n"
                "## Edges told\n\n| from | type | to | note |\n|---|---|---|---|\n"
                "| [[farmers]] | holds | [[cost]] | plain words that are not repeated anywhere |\n",
            ),
        },
    )
    e = entries(doc(root))["cost"]
    assert e["share"] == 0.0 and e["words"] == 14


def test_the_narratives_are_named_most_runs_first(tmp_path):
    root = write(
        tmp_path / "v",
        base_files()
        | {
            "narrative/aa.md": narrative("Aa", "one two three four five six [[farmers]]."),
            "narrative/bb.md": narrative(
                "Bb", "alpha beta gamma delta epsilon zeta eta theta [[farmers]]."
            ),
            "concern/cost.md": page(
                "concern",
                "Cost",
                "draft",
                "",
                "alpha beta gamma delta epsilon zeta eta theta and one two three four five six\n",
            ),
        },
    )
    assert entries(doc(root))["cost"]["narratives"] == ["bb", "aa"]


def test_an_uncoded_narrative_is_not_narrative_text_and_is_listed(tmp_path):
    root = write(
        tmp_path / "v",
        base_files()
        | {
            "narrative/loose.md": narrative(
                "Loose", "unique words that only the loose account has."
            ),
            "concern/cost.md": page(
                "concern", "Cost", "draft", "", "unique words that only the loose account has\n"
            ),
        },
    )
    d = doc(root)
    assert entries(d)["cost"]["share"] == 0.0
    assert [x["name"] for x in d["excluded"]] == ["loose"]


def test_one_node(built):
    d = doc(built, "water")
    assert [e["name"] for e in d["pages"]] == ["water"]
    assert d["pages"][0] == entries(doc(built))["water"]
    assert VALIDATOR.is_valid(d)


def test_text_form_begins_with_the_mode(built):
    text = str(scat_tools.copy_share(root=built))
    assert text.startswith("attribution mode: disallowed\ncopy-share: ")
    assert "water (concern, draft)" in text and "no share" in text and "from pump" in text


def test_the_cli_json_equals_python(built, capsys):
    assert main(["copy-share", "--root", str(built), "--json"]) == 0
    assert json.loads(capsys.readouterr().out) == scat_tools.copy_share(root=built).to_dict()
    assert main(["copy-share", "water", "--root", str(built), "--json"]) == 0
    assert (
        json.loads(capsys.readouterr().out) == scat_tools.copy_share("water", root=built).to_dict()
    )


@pytest.mark.parametrize("name", ["no-such-node", "dry", "contributor-name"])
def test_refusals(built, name):
    before = tree_hash(built)
    r = scat_tools.copy_share(name, root=built)
    assert isinstance(r, Result) and not r.ok
    assert "no node has this name" in str(r)
    assert VALIDATOR.is_valid(r.to_dict())
    assert tree_hash(built) == before


def test_a_name_that_is_not_text_is_refused(built):
    assert not scat_tools.copy_share(3, root=built).ok  # type: ignore[arg-type]


def test_a_missing_vault_is_refused(tmp_path):
    r = scat_tools.copy_share(root=tmp_path / "nowhere")
    assert not r.ok


def test_an_error_in_a_page_drawn_refuses(tmp_path):
    root = write(
        tmp_path / "v",
        base_files() | {"concern/water.md": page("concern", "Water", "done", "", "Body.\n")},
    )
    r = scat_tools.copy_share(root=root)
    assert not r.ok and "error" in str(r)


def test_it_writes_nothing(built):
    before = tree_hash(built)
    scat_tools.copy_share(root=built)
    scat_tools.copy_share("water", root=built)
    assert tree_hash(built) == before


def test_on_the_g6_vault_copy_heavy_pages_beat_the_synthesised_ones():
    shares = {e["name"]: e["share"] for e in doc(G6)["pages"]}
    heavy = ("direct-message-reminder", "members-not-replying")
    synthesised = ("forum-bot", "members-lose-the-thread")
    assert min(shares[n] for n in heavy) > max(shares[n] for n in synthesised)
    assert min(shares[n] for n in heavy) > 0.5
    stubs = [e for e in doc(G6)["pages"] if e["status"] == "stub"]
    assert stubs and all(e["share"] is None for e in stubs)
