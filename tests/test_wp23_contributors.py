"""WP23-G2 and G3, R2 and R3: contributor pages are in the knowledge graph and never in the layered graph; a link to
one is no node link; the mode rule's wording is the catalogue's.

The vault is the example vault (three groups at its cap of three), put in `optional` mode and given three contributor
pages and `attributed_to` links, and compared with the same vault in the same mode without them.
"""

import re
import shutil
from pathlib import Path

import pytest

import scat_kg
from scat_kg.checks.attribution import MODE_RULE
from scat_kg.graph import load

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "contracts" / "examples"
CATALOGUE = ROOT / "contracts" / "rule-catalogue.md"
NARRATIVES = sorted((EXAMPLES / "narrative").glob("*.md"))
PEOPLE = ("ada-quill", "bo-marsh", "cy-reed")


def shape(g):
    """The edges as data without the file lines (the attributed vault's pages are one line longer)."""
    return [
        (e.key, e.status, [(t.narrative, t.row, t.note, t.status) for t in e.tellings])
        for e in g.edges
    ]


def vault(tmp_path, name, mode="optional", *, contributors=False, names=False) -> Path:
    """The example vault in `mode`; with `contributors` three contributor pages, with `names` each narrative
    attributed to all three."""
    root = tmp_path / name
    shutil.copytree(EXAMPLES, root)
    (root / "scat.toml").write_text(f'attribution = "{mode}"\nstakeholder_group_cap = 3\n', "utf-8")
    if contributors:
        for who in PEOPLE:
            page = root / "contributor" / f"{who}.md"
            page.parent.mkdir(exist_ok=True)
            page.write_text(
                f'---\ntype: contributor\nstatus: done\ntitle: "{who.title()}"\n---\n', "utf-8"
            )
    if names:
        line = "attributed_to: [" + ", ".join(f'"[[{w}]]"' for w in PEOPLE) + "]\n"
        for path in (root / "narrative").glob("*.md"):
            text = path.read_text("utf-8")
            path.write_text(text.replace("\n---\n", "\n" + line + "---\n", 1), "utf-8")
    return root


def views(root):
    """Every view the tool makes, as data."""
    out = {"layered": scat_kg.layered(root=root).to_dict()}
    for t in ("holds", "addressed-by", "provided-by"):
        out[t] = scat_kg.edge_table(t, root=root).to_dict()
    out["fingerprints"] = scat_kg.fingerprint(root=root, candidates=True).to_dict()
    for n in NARRATIVES:
        out[n.stem] = scat_kg.fingerprint(n.stem, candidates=True, root=root).to_dict()
    for node in ("borrowers", "safe-handling-of-tools", "booking-app"):
        out["trace-" + node] = scat_kg.trace(node, root=root).to_dict()
    return out


@pytest.fixture
def pair(tmp_path):
    return (
        vault(tmp_path, "plain"),
        vault(tmp_path, "attributed", contributors=True, names=True),
    )


def test_the_attributed_vault_checks_clean_and_so_does_the_plain_one(pair):
    for root in pair:
        report = scat_kg.check(root=root)
        assert [p.rule for p in report.errors] == [], root


def test_contributor_pages_change_no_view(pair):
    plain, attributed = pair
    assert views(attributed) == views(plain)


def test_contributor_pages_are_not_in_the_layered_graph_or_the_cap(pair):
    plain, attributed = pair
    a, p = load(attributed), load(plain)
    assert shape(a) == shape(p) and a.candidates == p.candidates and a.nodes == p.nodes
    assert a.summary() == p.summary()
    assert sum(len(ns) for ns in a.nodes.values()) == sum(len(ns) for ns in p.nodes.values())
    assert not any(n.name in PEOPLE for ns in a.nodes.values() for n in ns)
    assert not any(
        PEOPLE_NAME in (e.from_node, e.to_node) for e in a.edges for PEOPLE_NAME in PEOPLE
    )
    # three contributor pages beside three groups at a cap of three: no SCAT-CAP
    assert scat_kg.check(root=attributed).problems == scat_kg.check(root=plain).problems


def test_contributor_pages_are_in_the_knowledge_graph(pair):
    _, attributed = pair
    g = load(attributed)
    assert [c.name for c in g.contributors] == sorted(PEOPLE)
    assert all(c.path == f"contributor/{c.name}.md" and c.status == "done" for c in g.contributors)
    assert all(n.attributed_to == PEOPLE for n in g.narratives)
    assert all(PEOPLE_NAME in g.vault.by_name for PEOPLE_NAME in PEOPLE)  # a link target resolves


def test_attributed_to_links_are_no_link_of_the_page_and_change_no_fingerprint(pair):
    plain, attributed = pair
    a, p = load(attributed), load(plain)
    assert [(n.name, n.nodes, n.edges, n.status) for n in a.narratives] == [
        (n.name, n.nodes, n.edges, n.status) for n in p.narratives
    ]
    # the field adds a line to the frontmatter, so the lines move by one and nothing else changes
    assert [[(l.target, l.line - 1) for l in n.links] for n in a.narratives] == [
        [(l.target, l.line) for l in n.links] for n in p.narratives
    ]
    assert [(l.source, l.target) for l in a.links] == [(l.source, l.target) for l in p.links]
    assert a.excluded == p.excluded
    assert not any(l.target in PEOPLE for l in a.links)
    assert all(
        b.source.startswith("narrative/") is False for who in PEOPLE for b in a.vault.inbound(who)
    )


def test_a_narrative_that_only_names_contributors_is_uncoded_and_excluded(tmp_path):
    root = vault(tmp_path, "v", contributors=True)
    (root / "narrative" / "only-people.md").write_text(
        '---\ntype: narrative\nstatus: draft\ntitle: "Only people"\n'
        'attributed_to: ["[[ada-quill]]"]\n---\n\nTold by [[bo-marsh]] and [[cy-reed|Cy]].\n',
        "utf-8",
    )
    g = load(root)
    assert "only-people" in [e.narrative for e in g.excluded]
    assert "only-people" not in [n.name for n in g.narratives]
    report = scat_kg.check(root=root)
    mine = {p.rule for p in report.problems if p.file.endswith("only-people.md")}
    assert "SCAT-UNCODED" in mine and mine <= {"SCAT-UNCODED", "SCAT-DRAFT-FIELD"}
    assert report.ok


def test_adding_attributed_to_does_not_code_or_uncode_a_narrative(tmp_path):
    coded = vault(tmp_path, "coded", contributors=True, names=True)
    assert [e.narrative for e in load(coded).excluded] == []
    # an uncoded narrative stays uncoded with the field; a coded one stays coded without it
    bare = vault(tmp_path, "bare", contributors=True)
    page = bare / "narrative" / "ghosts.md"
    page.write_text(
        '---\ntype: narrative\nstatus: stub\ntitle: "Ghosts"\n---\n\nNothing.\n', "utf-8"
    )
    before = load(bare)
    page.write_text(
        '---\ntype: narrative\nstatus: stub\ntitle: "Ghosts"\nattributed_to: ["[[ada-quill]]"]\n---\n\nNothing.\n',
        "utf-8",
    )
    after = load(bare)
    assert (
        [e.narrative for e in before.excluded]
        == [e.narrative for e in after.excluded]
        == ["ghosts"]
    )
    assert before.edges == after.edges and before.nodes == after.nodes


def test_a_dangling_entry_is_in_no_link_and_names_no_contributor(tmp_path):
    root = vault(tmp_path, "v", contributors=True, names=True)
    page = root / "narrative" / "funders-meeting.md"
    page.write_text(
        page.read_text("utf-8").replace('"[[cy-reed]]"', '"[[nobody]]", "Plain Text"'), "utf-8"
    )
    g = load(root)
    n = g.narrative("funders-meeting")
    assert n.attributed_to == ("ada-quill", "bo-marsh")
    assert not any(l.target == "nobody" for l in g.links)
    assert sorted(
        {
            p.rule
            for p in scat_kg.check(root=root).problems
            if p.file == page.relative_to(root).as_posix()
        }
        - {"SCAT-DRAFT-FIELD"}
    ) == ["SCAT-ATTR-LINK"]


@pytest.mark.parametrize("mode", ["required", "optional"])
def test_the_knowledge_graph_holds_contributors_only_where_the_mode_allows(tmp_path, mode):
    g = load(vault(tmp_path, "v", mode, contributors=True, names=True))
    assert [c.name for c in g.contributors] == sorted(PEOPLE)


def test_in_disallowed_mode_the_graph_holds_no_contributor_and_no_attribution(tmp_path):
    root = vault(tmp_path, "v", "disallowed", contributors=True, names=True)
    g = load(root)
    assert g.contributors == () and all(n.attributed_to == () for n in g.narratives)
    rules = {p.rule for p in scat_kg.check(root=root).problems}
    assert "SCAT-ATTR-DISALLOWED" in rules
    # the views are refused on errors, as for any error in the pages they draw: no attribution leaks through
    assert views_text_has_no_names(root)


def views_text_has_no_names(root) -> bool:
    text = str(scat_kg.layered(root=root).to_dict()) + str(scat_kg.fingerprint(root=root).to_dict())
    return not any(w in text for w in PEOPLE)


# ---- the wording


def catalogue_wording() -> str:
    text = CATALOGUE.read_text("utf-8")
    section = text.split("### The mode rule", 1)[1].split("###", 1)[0]
    quoted = re.findall(r"^> (.+)$", section, re.MULTILINE)
    assert len(quoted) == 1, quoted
    return quoted[0]


def test_the_catalogue_quotes_the_mode_rule_byte_for_byte():
    assert catalogue_wording() == MODE_RULE


def test_the_mode_rule_says_what_the_chief_engineer_said():
    assert MODE_RULE == (
        "In required mode a narrative SHALL name its contributors; in disallowed mode it SHALL NOT; "
        "in optional mode it MAY. To name a contributor is to link a contributor page in the "
        "narrative's `attributed_to` field."
    )
    assert MODE_RULE.count("SHALL") == 2 and MODE_RULE.count("MAY") == 1


def test_status_lists_a_contributor_page_on_its_own_row_and_count(tmp_path):
    root = vault(tmp_path, "v", contributors=True, names=True)
    report = scat_kg.status(root=root)
    rows = [r for r in report.rows if r.type == "contributor"]
    assert sorted(r.name for r in rows) == sorted(PEOPLE)
    plain = scat_kg.status(root=vault(tmp_path, "p")).counts
    counts = report.counts
    assert counts.pop("contributors") == 3 and counts == plain  # not folded into the status counts
    assert "3 contributors" in str(report).splitlines()[-1]
    assert "contributors" not in plain
