"""WP24-R7: the split plan names every link and row a coder must re-link, and writes nothing."""

import pytest
from mergeutil import MODES, copy_of, tree

import scat_kg


@pytest.fixture(params=MODES)
def vault(request, tmp_path):
    return copy_of(request.param, tmp_path)


def test_the_plan_names_every_narrative_link_and_row(vault):
    before = tree(vault)
    g = scat_kg.load(vault)
    node = "community-members"
    plan = scat_kg.split_plan(node, root=vault)
    assert plan.ok and plan.node == node and plan.node_type == "group" and plan.mode in MODES
    assert tree(vault) == before
    listed = {p.name: p for p in plan.pages}
    linking = {n.name for n in g.narratives if node in n.nodes}
    assert set(listed) == linking and len(linking) == 8
    for n in g.narratives:
        if n.name not in linking:
            continue
        page = listed[n.name]
        assert [ln for ln, _ in page.links] == sorted(l.line for l in n.links if l.target == node)
        rows = [r for r in n.rows if node in (r.from_target, r.to_target)]
        assert [(r, ln) for r, ln, _ in page.rows] == [(r.n, r.line) for r in rows]
        assert [t for _, _, t in page.rows] == [r.text for r in rows]
    assert sum(len(p.rows) for p in plan.pages) == 10
    text = str(plan)
    for name in linking:
        assert name in text
    d = plan.to_dict()
    assert d["operation"] == "split-plan" and d["ok"] and d["node"] == node
    assert {p["name"] for p in d["pages"]} == linking
    assert "assign each narrative" in " ".join(d["notes"])
    assert any("stakeholder_group_cap" in n for n in d["notes"])  # the cap of a group is noted


def test_a_contributor_page_is_never_listed(tmp_path):
    root = copy_of("required", tmp_path)
    page = root / "contributor" / "lab-member-a.md"
    page.write_text(
        page.read_text(encoding="utf-8").rstrip("\n") + "\n\nAlso [[community-members]].\n",
        encoding="utf-8",
    )
    plan = scat_kg.split_plan("community-members", root=root)
    assert plan.ok
    assert all(not p.file.startswith("contributor/") for p in plan.pages)
    assert "lab-member-a" not in str([p.to_dict() for p in plan.pages])  # never a place to re-link
    assert any("contributor/lab-member-a.md" in n and "never changed" in n for n in plan.notes)


@pytest.mark.parametrize(
    "ref,why",
    [
        ("lab-member-a", "contributor page"),
        ("weekly-digest-trial", "narrative"),
        ("nobody", "no page has this name"),
        (3, "string"),
    ],
)
def test_it_refuses_what_is_not_a_node_page(ref, why, tmp_path):
    root = copy_of("required", tmp_path)
    before = tree(root)
    r = scat_kg.split_plan(ref, root=root)
    assert not r.ok and why in str(r)
    assert tree(root) == before


def test_a_page_with_no_group_cap_note_for_a_concern(vault):
    plan = scat_kg.split_plan("data-retention", root=vault)
    assert plan.ok and not any("stakeholder_group_cap" in n for n in plan.notes)
