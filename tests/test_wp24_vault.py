"""WP24-G6: the test vault in three copies (one per attribution mode) is conformant, the copies agree in nodes, edges
and narrative text, and the seeded structure is present: nodes linked by many narratives, a synonym pair, a decoy
pair, a duplicate-row seed, a done narrative on a merge's `a`, stubs, copied and synthesised node pages, and one group
used in two senses."""

from collections import Counter
from pathlib import Path

import pytest

import scat_kg

VAULT = Path(__file__).resolve().parents[1] / "research" / "node-pages" / "vault"
MODES = ("disallowed", "optional", "required")


@pytest.fixture(scope="module")
def graphs():
    return {m: scat_kg.load(root=VAULT / m) for m in MODES}


@pytest.fixture(scope="module")
def g(graphs):
    return graphs["disallowed"]


def linked_by(g, node):
    return {n.name for n in g.narratives if node in n.nodes}


def adjacent(g, node):
    out = set()
    for e in g.edges:
        if e.from_node == node:
            out.add(e.to_node)
        if e.to_node == node:
            out.add(e.from_node)
    return out


def narratives_of_edge_ends(g, node):
    return {t.narrative for e in g.edges if node in (e.from_node, e.to_node) for t in e.tellings}


@pytest.mark.parametrize("mode", MODES)
def test_check_has_no_errors(mode):
    result = scat_kg.check(root=VAULT / mode)
    assert result.mode == mode
    assert not result.errors, result.report.render()


@pytest.mark.parametrize("mode", MODES)
def test_loads_with_the_cap(mode, graphs):
    gr = graphs[mode]
    assert gr.ok and not gr.excluded and not gr.unreadable
    assert len(gr.nodes["group"]) == 4
    assert (VAULT / mode / "scat.toml").read_text().splitlines() == [
        f'attribution = "{mode}"',
        "stakeholder_group_cap = 4",
    ]


def test_copies_agree_in_nodes_edges_and_text(graphs):
    base = graphs["disallowed"]
    for mode in ("optional", "required"):
        other = graphs[mode]
        assert other.nodes == base.nodes
        assert {e.key: e.narratives for e in other.edges} == {
            e.key: e.narratives for e in base.edges
        }
        for n in base.narratives:
            a = (VAULT / "disallowed" / "narrative" / f"{n.name}.md").read_text()
            b = (VAULT / mode / "narrative" / f"{n.name}.md").read_text()
            body = lambda t: t.split("\n---\n", 1)[1]  # noqa: E731
            assert body(a) == body(b)


def test_attribution_by_mode(graphs):
    assert not graphs["disallowed"].contributors
    assert not (VAULT / "disallowed" / "contributor").exists()
    assert all(not n.attributed_to for n in graphs["disallowed"].narratives)
    assert len(graphs["optional"].contributors) >= 3 and len(graphs["required"].contributors) >= 3
    assert all(n.attributed_to for n in graphs["required"].narratives)
    named = [n for n in graphs["optional"].narratives if n.attributed_to]
    assert 0 < len(named) < len(graphs["optional"].narratives)


def test_size(g):
    new = len(g.narratives) - 9
    assert 12 <= new <= 16
    assert sum(len(ns) for ns in g.nodes.values()) > 27


def test_nodes_linked_by_many_narratives(g):
    hubs = {
        "ethnographers": "group",
        "closing-the-loop": "concern",
        "participatory-consent-feature": "affordance",
        "telescope": "technology",
        "durable-shared-records": "affordance",
        "direct-message-reminder": "affordance",
        "forum-bot": "technology",
    }
    for node, layer in hubs.items():
        assert g.node(node).type == layer
        assert len(linked_by(g, node)) >= 4, node
    assert len({layer for layer in hubs.values()}) >= 3
    assert len(linked_by(g, "closing-the-loop")) >= 6
    assert len(linked_by(g, "ethnographers")) >= 6


def paragraph_with(path: Path, needle: str) -> str:
    body = path.read_text().split("\n---\n", 1)[1].split("## Edges told")[0]
    return next(p for p in body.split("\n\n") if needle in p)


def test_link_paragraphs_are_longer_than_a_sentence_and_one_link_is_off_the_key_sentence():
    nar = VAULT / "disallowed" / "narrative"
    p = paragraph_with(nar / "reminders-and-the-quiet-inbox.md", "[[closing-the-loop|")
    sentences = [s for s in p.split(". ") if s]
    assert len(sentences) > 1
    key = next(s for s in sentences if s.startswith("Nothing was written up"))
    assert "[[" not in key and "[[closing-the-loop|" in p


def test_synonym_pair(g):
    a, b = "members-not-replying", "unanswered-direct-messages"
    assert g.node(a).type == g.node(b).type == "concern"
    assert a != b
    shared = linked_by(g, a) & linked_by(g, b)
    assert len(shared) >= 2
    assert adjacent(g, a) == adjacent(g, b) == {"ethnographers", "direct-message-reminder"}
    assert len(linked_by(g, a) ^ linked_by(g, b)) <= 2


def test_decoy_pair(g):
    a, b = "data-retention", "data-retention-schedule"
    assert g.node(a).type == g.node(b).type == "concern"
    assert b.startswith(a)
    assert not linked_by(g, a) & linked_by(g, b)
    assert not narratives_of_edge_ends(g, a) & narratives_of_edge_ends(g, b)
    assert not adjacent(g, a) & adjacent(g, b)
    assert adjacent(g, a) and adjacent(g, b)


def test_duplicate_row_seed(g):
    a, b = "weekly-digest", "digest-email"
    assert g.node(a).type == g.node(b).type == "affordance"
    nar = g.narrative("weekly-digest-trial")
    ends = Counter(
        (k.type, k.from_node) for k in nar.edges if k.type == "addressed-by" and k.to_node in (a, b)
    )
    assert any(c == 2 for c in ends.values()), (
        "one narrative tells the same other end for both pages"
    )


def test_done_narrative_on_a_merge_a(g):
    nar = g.narrative("weekly-digest-trial")
    assert nar.status == "done" and "weekly-digest" in nar.nodes
    assert len(linked_by(g, "weekly-digest")) >= 3
    assert any(n.status == "draft" for n in g.narratives)


def test_stubs_and_descriptions(g):
    stubs = [n for ns in g.nodes.values() for n in ns if n.status == "stub"]
    assert len(stubs) >= 3
    for n in stubs:
        text = (VAULT / "disallowed" / n.path.split("vault/disallowed/")[-1]).read_text()
        assert "description" not in text and text.rstrip().endswith("---")
    node_dir = VAULT / "disallowed"
    reminder = (node_dir / "affordance" / "direct-message-reminder.md").read_text()
    narrative = (node_dir / "narrative" / "reminders-and-the-quiet-inbox.md").read_text()
    assert "sent by the [[forum-bot|forum bot]] three days after the first one" in reminder
    assert "sent by the [[forum-bot|forum bot]] three days after the first one" in narrative
    synthesis = (node_dir / "technology" / "forum-bot.md").read_text()
    assert "Where accounts differ" in synthesis
    for n in g.narratives:
        assert (
            synthesis.split("\n---\n", 1)[1].strip()
            not in (node_dir / "narrative" / f"{n.name}.md").read_text()
        )


def test_homonym_group(g):
    texts = {
        n: (VAULT / "disallowed" / "narrative" / f"{n}.md").read_text()
        for n in ("members-as-the-site-sees-them", "member-organisations-and-the-renewal")
    }
    assert all("[[community-members|community members]]" in t for t in texts.values())
    site, orgs = (
        g.narrative("members-as-the-site-sees-them"),
        g.narrative("member-organisations-and-the-renewal"),
    )
    held = lambda nar: {k.to_node for k in nar.edges if k.from_node == "community-members"}  # noqa: E731
    assert held(site) and held(orgs) and not held(site) & held(orgs)
