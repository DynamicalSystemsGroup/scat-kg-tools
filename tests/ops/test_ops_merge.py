"""WP24-R5: `merge` plans, refuses with nothing written, and otherwise folds one node page into another."""

import json

import pytest
from mergeutil import (
    CLEAN,
    DUPLICATE_SEED,
    MODES,
    RANGE_CLEAN,
    WITH_BODY,
    assert_graph_equal,
    copy_of,
    tree,
)

import scat_kg
from scat_kg.ops.merge import rewrite_body


@pytest.fixture(params=MODES)
def vault(request, tmp_path):
    return copy_of(request.param, tmp_path)


def link_targets_left(root, name):
    return [
        (p.path, l.line)
        for p in scat_kg.load(root).vault.pages
        if p.type != "contributor"
        for l in p.links
        if l.target == name
    ]


def test_the_duplicate_row_seed_is_refused_and_writes_nothing(vault):
    before = tree(vault)
    for plan in (True, False):
        r = scat_kg.merge(*DUPLICATE_SEED, plan=plan, root=vault)
        assert not r.ok and r.mode
        why = " ".join(x.why for x in r.refused)
        assert "two rows tell one edge" in why
        assert "[[weekly-digest]]" in why and "[[digest-email]]" in why  # both rows are listed
        assert "line " in why
        assert tree(vault) == before


def test_a_clean_merge_in_every_mode(vault):
    g0 = scat_kg.load(vault)
    a, b = CLEAN
    status_b = g0.node(b).status
    done = {n.name for n in g0.narratives if n.status == "done" and a in n.nodes}
    assert done  # the seed: a done narrative links a
    r = scat_kg.merge(a, b, root=vault)
    assert r.ok, str(r)
    assert not (vault / f"concern/{a}.md").exists()
    assert r.removed == (f"concern/{a}.md",) and r.plan is False
    assert set(r.done_narratives) == done
    assert {n.name: n.status for n in scat_kg.load(vault).narratives if n.name in done} == {
        n: "done" for n in done
    }
    assert scat_kg.load(vault).node(b).status == status_b
    assert not scat_kg.check(root=vault).errors
    assert_graph_equal(g0, vault, a, b)
    assert link_targets_left(vault, a) == []
    assert (vault / "index" / "concern.base").is_file()
    assert sum(n for _, n in r.links_rewritten) == len(
        [l for l in g0.links if l.target == a and not l.source.startswith("contributor/")]
    )
    assert "created" not in str(r) or not r.created


def test_a_merge_with_a_body_appends_it_under_a_heading(vault):
    a, b = WITH_BODY
    g0 = scat_kg.load(vault)
    body_a = next(p for p in g0.vault.pages if p.name == a).body.strip()
    assert body_a
    before_b = (vault / f"technology/{b}.md").read_text(encoding="utf-8")
    r = scat_kg.merge(a, b, root=vault)
    assert r.ok, str(r)
    after_b = (vault / f"technology/{b}.md").read_text(encoding="utf-8")
    assert after_b.startswith(before_b.split("---\n", 2)[0] + "---\n")  # the frontmatter is kept
    assert before_b.split("---\n", 2)[1] == after_b.split("---\n", 2)[1]
    assert f"## From {a}\n" in after_b and f"[[{a}" not in after_b
    assert body_a.splitlines()[0] in after_b
    assert_graph_equal(g0, vault, a, b)
    assert not scat_kg.check(root=vault).errors


def test_the_range_vault(tmp_path):
    root = copy_of("range", tmp_path)
    g0 = scat_kg.load(root)
    a, b = RANGE_CLEAN
    r = scat_kg.merge(a, b, root=root)
    assert r.ok, str(r)
    assert not scat_kg.check(root=root).errors
    assert_graph_equal(g0, root, a, b)
    assert link_targets_left(root, a) == []
    # and the pair that would make a duplicate row is refused with nothing written
    before = tree(root)
    bad = scat_kg.merge("obsidian", "telescope", root=root)
    assert not bad.ok and tree(root) == before


@pytest.mark.parametrize("mode", ["optional", "required"])
def test_contributor_pages_are_byte_identical(mode, tmp_path):
    root = copy_of(mode, tmp_path)
    before = tree(root)
    assert scat_kg.merge(*CLEAN, root=root).ok
    after = tree(root)
    people = [p for p in before if p.startswith("contributor/")]
    assert people and all(after[p] == before[p] for p in people)


@pytest.mark.parametrize("mode", ["optional", "required"])
def test_attributed_to_lines_survive(mode, tmp_path):
    root = copy_of(mode, tmp_path)

    def front(root):
        out = {}
        for p in (root / "narrative").glob("*.md"):
            out[p.name] = p.read_text(encoding="utf-8").split("\n---\n", 1)[0]
        return out

    before = front(root)
    assert scat_kg.merge(*CLEAN, root=root).ok
    assert front(root) == before


def test_a_contributor_page_that_links_a_stops_the_merge(tmp_path):
    root = copy_of("required", tmp_path)
    page = root / "contributor" / "lab-member-a.md"
    page.write_text(
        page.read_text(encoding="utf-8").rstrip("\n") + f"\n\nLooks after [[{CLEAN[0]}]].\n",
        encoding="utf-8",
    )
    before = tree(root)
    r = scat_kg.merge(*CLEAN, root=root)
    assert not r.ok
    assert "contributor/lab-member-a.md" in str(r)
    assert tree(root) == before


@pytest.mark.parametrize(
    "a,b,why",
    [
        ("right-to-be-forgotten", "digest-email", "of one type"),  # cross-type
        ("lab-member-a", "data-retention", "contributor page"),
        ("data-retention", "lab-member-a", "contributor page"),
        ("weekly-digest-trial", "data-retention", "narrative"),
        ("data-retention", "weekly-digest-trial", "narrative"),
        ("no-such-page", "data-retention", "no page has this name"),
        ("data-retention", "no-such-page", "no page has this name"),
        ("data-retention", "data-retention", "same page"),
    ],
)
def test_refusals_write_nothing(a, b, why, tmp_path):
    root = copy_of("required", tmp_path)
    before = tree(root)
    for plan in (True, False):
        r = scat_kg.merge(a, b, plan=plan, root=root)
        assert not r.ok and why in str(r), str(r)
        assert tree(root) == before


@pytest.mark.parametrize("bad", [None, 3, ["a"], {"a": 1}])
def test_non_text_arguments_are_refused(bad, tmp_path):
    root = copy_of("disallowed", tmp_path)
    before = tree(root)
    assert not scat_kg.merge(bad, "data-retention", root=root).ok
    assert not scat_kg.merge("data-retention", bad, root=root).ok
    assert not scat_kg.merge("data-retention", "data-retention-schedule", plan="yes", root=root).ok
    assert not scat_kg.split_plan(bad, root=root).ok
    assert tree(root) == before


def test_a_vault_with_an_error_in_a_page_it_reads_is_refused(tmp_path):
    root = copy_of("disallowed", tmp_path)
    page = root / "concern" / "data-retention.md"
    page.write_text(
        page.read_text(encoding="utf-8") + "\nA [[nowhere-at-all]] link.\n", encoding="utf-8"
    )
    before = tree(root)
    r = scat_kg.merge("data-retention-schedule", "data-retention", root=root)
    assert not r.ok and "concern/data-retention.md" in str(r)
    assert tree(root) == before


def test_the_plan_is_what_apply_then_does(vault):
    plan = scat_kg.merge(*CLEAN, plan=True, root=vault)
    assert plan.ok and plan.plan is True
    before = tree(vault)
    assert scat_kg.merge(*CLEAN, plan=True, root=vault).to_dict() == plan.to_dict()
    assert tree(vault) == before  # a plan writes nothing
    done = scat_kg.merge(*CLEAN, root=vault)
    after = tree(vault)
    changed = {p for p in before if p in after and before[p] != after[p]}
    removed = {p for p in before if p not in after}
    created = {p for p in after if p not in before}
    assert changed == set(plan.changed) == set(done.changed)
    assert removed == set(plan.removed) == set(done.removed)
    assert created == set(plan.created) == set(done.created) == set()
    d0, d1 = plan.to_dict(), done.to_dict()
    d0.pop("plan"), d1.pop("plan")
    assert d0 == d1


def test_merging_twice_is_refused(vault):
    assert scat_kg.merge(*CLEAN, root=vault).ok
    before = tree(vault)
    r = scat_kg.merge(*CLEAN, root=vault)
    assert not r.ok and "no page has this name" in str(r)
    assert tree(vault) == before


def test_the_document_carries_the_mode_and_the_new_fields(vault):
    d = scat_kg.merge(*CLEAN, plan=True, root=vault).to_dict()
    assert d["operation"] == "merge" and d["ok"] and d["plan"] is True
    assert d["mode"] in MODES
    assert d["removed"] and d["links_rewritten"] and "done_narratives" in d
    json.dumps(d)


# ---------------------------------------------------------------------------------------------------------
# How a link is rewritten
# ---------------------------------------------------------------------------------------------------------

TABLE = [
    "## Edges told",
    "",
    "| from | type | to | note |",
    "|---|---|---|---|",
    "| [[g]] | holds | [[a]] | see [[a]] and [[a|x]] |",
]


def test_links_in_prose_keep_what_the_reader_saw():
    body = [
        "Plain [[a]] and [[a|alias]] and [[a#Heading]] and [[a#^block]] and [[ a ]] here.",
        "Embedded: ![[a]] and ![[a|200]].",
        "Not this one: [[ab]] or [[a.png]] or [[x/a]].",
    ]
    out, n = rewrite_body(body, "a", "b", narrative=False)
    assert n == 7
    assert out[0] == (
        "Plain [[b|a]] and [[b|alias]] and [[b#Heading]] and [[b#^block]] and [[ b |a]] here."
    )
    assert out[1] == "Embedded: ![[b]] and ![[b|200]]."
    assert out[2] == body[2]


def test_a_row_end_stays_bare_and_a_bar_in_a_cell_is_escaped():
    out, n = rewrite_body(TABLE, "a", "b", narrative=True)
    assert n == 3
    assert out[-1] == "| [[g]] | holds | [[b]] | see [[b\\|a]] and [[b|x]] |"


def test_a_table_line_outside_the_edges_table_gets_an_escaped_alias():
    body = ["| name | what |", "|---|---|", "| [[a]] | [[a\\|shown]] |"]
    out, n = rewrite_body(body, "a", "b", narrative=True)
    assert out[2] == "| [[b\\|a]] | [[b\\|shown]] |" and n == 2


def test_code_is_not_rewritten():
    body = ["```", "[[a]]", "```", "A span `[[a]]` and a link [[a]].", "~~~~", "[[a]]", "~~~~"]
    out, n = rewrite_body(body, "a", "b", narrative=False)
    assert n == 1
    assert (
        out[1] == "[[a]]" and out[3] == "A span `[[a]]` and a link [[b|a]]." and out[5] == "[[a]]"
    )


def test_frontmatter_and_code_in_a_real_merge(tmp_path, make_vault):
    root = make_vault(
        {
            "scat.toml": "attribution = 'disallowed'\nstakeholder_group_cap = 4\n",
            "concern/a.md": '---\ntype: concern\nstatus: draft\ntitle: "A"\n'
            'description: "see [[a]] in frontmatter"\n---\nA body.\n',
            "concern/b.md": '---\ntype: concern\nstatus: draft\ntitle: "B"\n'
            'description: "B"\nrelated: "[[a]]"\n---\nB body.\n\n```\n[[a]]\n```\n',
            "narrative/n.md": '---\ntype: narrative\nstatus: draft\ntitle: "N"\n'
            'kind: scenario\ntimeframe: past\ndescription: "[[a]]"\n---\n'
            "The account of [[a]], then [[b]].\n\n```\n[[a]]\n```\n",
        }
    )
    r = scat_kg.merge("a", "b", root=root)
    assert r.ok, str(r)
    b = (root / "concern/b.md").read_text(encoding="utf-8")
    assert 'related: "[[a]]"' in b  # frontmatter untouched
    assert "```\n[[a]]\n```" in b  # code untouched
    assert b.endswith("## From a\n\nA body.\n")
    n = (root / "narrative/n.md").read_text(encoding="utf-8")
    assert 'description: "[[a]]"' in n and "The account of [[b|a]], then [[b]]." in n
    assert "```\n[[a]]\n```" in n
