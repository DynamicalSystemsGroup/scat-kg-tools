"""record-edge and remove-edge: an edge is a row of a narrative's table."""

import pytest
from opsutil import CAP3, fm, narrative
from tests_schema import VALIDATOR

import scat_kg
from scat_kg.graph import load
from scat_kg.ops import record_edge, remove_edge

D = 'description: "d"\n'


@pytest.fixture
def vault(make_vault):
    return make_vault(
        {
            **CAP3,
            "group/g.md": fm("group", "G", "done", D),
            "concern/c.md": fm("concern", "C", "done", D),
            "affordance/a.md": fm("affordance", "A", "done", D),
            "technology/t.md": fm("technology", "T", "done", D),
            "narrative/n1.md": narrative("N1", ["| [[g]] | holds | [[c]] | first |"], "draft"),
            "narrative/n2.md": narrative("N2", None, "stub"),
            "narrative/done.md": narrative("Done", ["| [[g]] | holds | [[c]] | |"], "done", 'description: "d"\ntimeframe: past\n'),
        }
    )  # fmt: skip


def told(root, type_, a, b):
    e = load(root).edge(type_, a, b)
    return e.narratives if e else ()


# record-edge


def test_record_adds_a_row_where_there_is_none_and_leaves_everything_else(vault, snap, diff):
    before = snap(vault)
    old = (vault / "narrative/n1.md").read_text()
    r = record_edge("addressed-by", "c", "a", "n1", "Covers it.", root=vault)
    assert r.ok and r.changed == ("narrative/n1.md",) and not r.created and not r.unchanged
    assert diff(before, snap(vault)) == {"narrative/n1.md": "changed"}
    assert (
        vault / "narrative/n1.md"
    ).read_text() == old + "| [[c]] | is addressed by | [[a]] | Covers it. |\n"
    assert told(vault, "addressed-by", "c", "a") == ("n1",)
    assert [x.line for x in r.rows_added] == [13] and r.rows_added[0].note == "Covers it."
    assert r.edge.narratives == ("n1",) and not r.rows_removed


def test_record_leaves_the_links_alone(vault):
    record_edge("holds", "g", "c", "n2", root=vault)
    text = (vault / "narrative/n2.md").read_text()
    assert text.startswith("---\ntype: narrative\nstatus: stub\n") and "The account.\n" in text
    assert text.count("[[") == 2  # only the row's two ends: no link was added to the account


def test_record_twice_is_unchanged_the_second_time(vault, snap):
    record_edge("holds", "g", "c", "n2", root=vault)
    before = snap(vault)
    r = record_edge("holds", "g", "c", "n2", root=vault)
    assert r.ok and r.unchanged == ("narrative/n2.md",) and not r.changed and not r.rows_added
    assert snap(vault) == before


def test_two_narratives_each_get_their_own_row_with_their_own_note(vault):
    r = record_edge("holds", "g", "c", ["n1", "n2"], "mine", root=vault)
    assert r.unchanged == ("narrative/n1.md",) and r.changed == ("narrative/n2.md",)
    assert r.edge.narratives == ("done", "n1", "n2")
    assert "| [[g]] | holds | [[c]] | mine |" in (vault / "narrative/n2.md").read_text()
    assert "mine" not in (vault / "narrative/n1.md").read_text()  # nothing is copied or overwritten


def test_record_stubs_a_missing_end_and_a_missing_narrative(vault):
    r = record_edge("is provided by", "a", "newtech", "fresh-story", root=vault)
    assert r.ok and set(r.created) == {"technology/newtech.md", "narrative/fresh-story.md"}
    assert (vault / "technology/newtech.md").read_text() == (
        '---\ntype: technology\nstatus: stub\ntitle: "Newtech"\n---\n'
    )
    page = (vault / "narrative/fresh-story.md").read_text()
    assert page.startswith(
        '---\ntype: narrative\nstatus: stub\ntitle: "Fresh story"\ntimeframe: # past | future | mixed\n---\n'
    )
    assert "| [[a]] | is provided by | [[newtech]] | |" in page
    assert r.edge.type == "provided-by" and r.edge.narratives == ("fresh-story",)
    assert r.changed == ()


def test_record_keeps_crlf_and_bom_of_an_existing_narrative(make_vault):
    text = narrative("N", ["| [[g]] | holds | [[c]] | |"]).replace("\n", "\r\n")
    root = make_vault(
        {
            **CAP3,
            "group/g.md": fm("group", "G"),
            "concern/c.md": fm("concern", "C"),
            "concern/c2.md": fm("concern", "C2"),
            "narrative/n.md": b"\xef\xbb\xbf" + text.encode(),
        }
    )
    assert record_edge("holds", "g", "c2", "n", root=root).ok
    data = (root / "narrative/n.md").read_bytes()
    assert data.startswith(b"\xef\xbb\xbf---") and data.replace(b"\r\n", b"").count(b"\n") == 0
    assert data.endswith(b"| [[g]] | holds | [[c2]] | |\r\n")


def test_the_type_is_the_slug_or_the_verb(vault):
    assert record_edge("holds", "g", "c", "n2", root=vault).ok
    assert record_edge("Is Addressed By", "c", "a", "n2", root=vault).ok


@pytest.mark.parametrize(
    "args, word",
    [
        (("owns", "g", "c", "n1"), "not an edge type"),
        (("holds", "g", "c", []), "no narrative is named"),
        (("holds", "c", "g", "n1"), "the other way round"),
        (("holds", "g", "a", "n1"), "needs a concern at its to end"),
        (("addressed-by", "g", "c", "n1"), "these ends fit `holds`"),
        (("holds", "t", "g", "n1"), "needs a group at its from end"),
        (("holds", "g", "g", "n1"), "same name"),
        (("holds", "g", "c", "c"), "only a narrative tells an edge"),
        (("holds", "Bad Name", "c", "n1"), "a-z"),
        (("holds", "g", "newc", "Bad Name"), "a-z"),
        (("holds", "g", "n1", "n2"), "needs a concern at its to end"),
    ],
)
def test_record_refusals_write_nothing_and_carry_no_rule(vault, snap, args, word):
    before = snap(vault)
    r = record_edge(*args, root=vault)
    assert not r.ok and word in str(r) and "Fix:" in str(r)
    assert all(x.rule is None for x in r.refused)
    assert snap(vault) == before
    assert VALIDATOR.is_valid(r.to_dict()) and "edge" not in r.to_dict()


def test_record_into_a_done_narrative_refuses_and_names_the_coders_step(vault, snap):
    before = snap(vault)
    r = record_edge(
        "holds", "g", "newc", ["n2", "done"], root=vault
    )  # n2 would be written, not done's
    assert not r.ok and snap(vault) == before  # nothing at all, not even n2 or the stub
    (ref,) = r.refused
    assert ref.rule is None and ref.subject == "narrative/done.md"
    assert (
        "`scat set-status done draft`" in ref.fix
        and 'scat_kg.set_status("done", "draft")' in ref.fix
    )
    assert ref.fix_data.options[0].command.argv == ("set-status", "done", "draft")


def test_record_into_a_done_narrative_that_already_has_the_row_is_unchanged(vault):
    r = record_edge("holds", "g", "c", "done", root=vault)
    assert r.ok and r.unchanged == ("narrative/done.md",)


def test_after_set_status_draft_the_record_goes_through(vault):
    assert not record_edge("holds", "g", "newc", "done", root=vault).ok
    assert scat_kg.set_status("done", "draft", root=vault).ok
    assert record_edge("holds", "g", "newc", "done", root=vault).ok


def test_record_over_the_cap_creates_nothing(make_vault, snap):
    root = make_vault({**CAP3, **{f"group/g{i}.md": fm("group", f"G{i}") for i in range(3)}})
    before = snap(root)
    r = record_edge("holds", "g4", "newc", "story", root=root)
    assert not r.ok and "cap of 3" in str(r) and "SCAT-CAP" in str(r)
    assert snap(root) == before
    assert record_edge("holds", "g1", "newc", "story", root=root).ok  # an existing group is fine


def test_record_refuses_a_malformed_table_and_says_where(make_vault, snap):
    bad = fm("narrative", "N", "draft", "", "## Edges told\n\n| a | b |\n|---|---|\n| x | y |\n")
    root = make_vault(
        {"group/g.md": fm("group", "G"), "concern/c.md": fm("concern", "C"), "narrative/n.md": bad}
    )
    before = snap(root)
    r = record_edge("holds", "g", "c", "n", root=root)
    assert not r.ok and "narrative/n.md" in str(r) and snap(root) == before


def test_record_a_note_with_a_bar_and_a_line_break_stays_one_row(vault):
    record_edge("holds", "g", "c", "n2", "a | b\nc", root=vault)
    assert "| [[g]] | holds | [[c]] | a \\| b c |" in (vault / "narrative/n2.md").read_text()
    assert load(vault).edge("holds", "g", "c")


def test_record_json_is_valid_and_has_the_edge_and_the_rows(vault):
    doc = record_edge("holds", "g", "c", "n2", root=vault).to_dict()
    assert VALIDATOR.is_valid(doc), list(VALIDATOR.iter_errors(doc))[:1]
    assert doc["operation"] == "record-edge" and doc["edge"]["from"] == "g"
    assert doc["rows_added"][0]["narrative"] == "n2" and doc["rows_removed"] == []


def test_record_in_a_missing_vault_is_a_refusal(tmp_path):
    assert not record_edge("holds", "g", "c", "n", root=tmp_path / "x").ok


# remove-edge


def test_remove_deletes_the_rows_of_every_narrative_that_tells_it_and_keeps_the_links(
    make_vault, snap, diff
):
    root = make_vault(
        {
            "group/g.md": fm("group", "G"),
            "concern/c.md": fm("concern", "C"),
            "narrative/n1.md": narrative("N1", ["| [[g]] | holds | [[c]] | a |", "| [[g]] | holds | [[c]] | dup |"]),
            "narrative/n2.md": narrative("N2", ["| [[g]] | holds | [[c]] | |"], "stub"),
        }
    )  # fmt: skip
    before = snap(root)
    r = remove_edge("g", "c", root=root)
    assert r.ok and set(r.changed) == {"narrative/n1.md", "narrative/n2.md"}
    assert diff(before, snap(root)) == {"narrative/n1.md": "changed", "narrative/n2.md": "changed"}
    assert [(x.narrative, x.line, x.note) for x in r.rows_removed] == [
        ("n1", 12, "a"), ("n1", 13, "dup"), ("n2", 12, ""),
    ]  # fmt: skip
    assert r.edge.narratives == () and told(root, "holds", "g", "c") == ()
    assert "| holds |" not in (root / "narrative/n1.md").read_text()
    assert (
        "| from | type | to | note |" in (root / "narrative/n1.md").read_text()
    )  # the table stays


def test_remove_with_told_by_touches_only_those_narratives(vault):
    record_edge("holds", "g", "c", "n2", root=vault)
    r = remove_edge("g", "c", ["n2", "n1"], root=vault)
    assert r.ok and set(r.changed) == {"narrative/n1.md", "narrative/n2.md"}
    assert r.edge.narratives == ("done",)  # the done narrative still tells it


def test_remove_told_by_a_narrative_without_a_row_is_unchanged(vault, snap):
    before = snap(vault)
    r = remove_edge("g", "c", "n2", root=vault)
    assert r.ok and r.unchanged == ("narrative/n2.md",) and not r.rows_removed
    assert snap(vault) == before


def test_remove_nothing_to_remove_is_ok(vault, snap):
    before = snap(vault)
    r = remove_edge("c", "a", root=vault)
    assert r.ok and not r.changed and "nothing was removed" in str(r) and r.edge.narratives == ()
    assert snap(vault) == before


def test_remove_refuses_a_done_narrative_and_writes_nothing(vault, snap):
    before = snap(vault)
    r = remove_edge("g", "c", root=vault)  # n1 would change, done would too
    assert not r.ok and snap(vault) == before
    assert [x.subject for x in r.refused] == ["narrative/done.md"]
    assert "scat set-status done draft" in r.refused[0].fix


@pytest.mark.parametrize(
    "args, word",
    [
        (("nope", "c"), "no page has this name"),
        (("g", "n1"), "not a node"),
        (("c", "g"), "wrong way round"),
        (("g", "a"), "no edge joins a group and a affordance"),
        (("g", "c", "nope"), "no page has this name"),
        (("g", "c", "t"), "not a narrative"),
    ],
)
def test_remove_refusals_write_nothing(vault, snap, args, word):
    before = snap(vault)
    r = remove_edge(*args, root=vault)
    assert not r.ok and word in str(r) and snap(vault) == before
    assert VALIDATOR.is_valid(r.to_dict())


def test_the_wrong_way_round_fix_is_the_command_that_works(vault):
    r = remove_edge("c", "g", root=vault)
    cmd = r.refused[0].fix_data.options[0].command
    assert cmd.argv == ("remove-edge", "g", "c")


def test_remove_json_is_valid(vault):
    doc = remove_edge("g", "c", "n1", root=vault).to_dict()
    assert VALIDATOR.is_valid(doc), list(VALIDATOR.iter_errors(doc))[:1]
    assert doc["operation"] == "remove-edge" and doc["rows_removed"][0]["line"] == 12
    assert doc["edge"] == {"type": "holds", "from": "g", "to": "c", "narratives": ["done"]}


def test_record_then_remove_gives_back_the_file(vault):
    old = (vault / "narrative/n1.md").read_bytes()
    record_edge("addressed-by", "c", "a", "n1", root=vault)
    remove_edge("c", "a", root=vault)
    assert (vault / "narrative/n1.md").read_bytes() == old
