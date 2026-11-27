"""What the figures hide, shown (WP34): orphan pages, candidates in the layered view, the no-account flag."""

from test_draw import lines, said
from viewutil import narrative, page, row

import scat_kg
from scat_kg import draw, graph, views

BARE = narrative(
    "Bare", "", [row("holds", "farmers", "water"), row("addressed-by", "water", "alert")]
)


def candidates_of(vault, names):
    return [
        {"type": c.type, "from": c.from_node, "to": c.to_node, "narrative": c.narrative}
        for c in graph.load(vault).candidates
        if c.narrative in names
    ]


def dashed(svg):
    return sum(1 for *_, d in lines(svg) if d)


# --- R1: orphans -----------------------------------------------------------------------------------------


def test_the_layered_result_lists_the_node_pages_no_row_tells(vault):
    d = scat_kg.layered(root=vault).to_dict()
    assert d["orphans"] == [{"name": "idle", "type": "technology", "status": "stub"}]
    # vault-wide, whichever narratives were chosen
    assert scat_kg.layered(["dry"], root=vault).to_dict()["orphans"] == d["orphans"]
    assert scat_kg.layered([], root=vault).to_dict()["orphans"] == d["orphans"]


def test_both_renderings_show_the_orphans(vault):
    view = scat_kg.layered(root=vault)
    assert "orphans" in str(view) and "idle (technology) [stub]" in str(view)
    assert "no row tells these node pages: idle." in said(draw.render(view).svg())


def test_a_node_page_told_by_a_row_is_not_an_orphan(make):
    vault = make({"technology/idle.md": None})
    d = scat_kg.layered(root=vault).to_dict()
    assert "orphans" not in d
    assert "orphans" not in str(scat_kg.layered(root=vault))
    assert "no row tells" not in said(draw.layered(root=vault).svg())


def test_more_than_ten_orphans_are_named_ten_then_and_n_more(make):
    extra = {f"technology/o{i:02d}.md": page("technology", f"O{i}") for i in range(12)}
    vault = make(extra)
    view = scat_kg.layered(root=vault)
    names = [o["name"] for o in view.to_dict()["orphans"]]
    assert len(names) == 13 and names == sorted(names)
    text = str(view)
    assert all(n in text for n in names)  # the text form lists them all
    footer = said(draw.render(view).svg())
    assert "no row tells these node pages: " + ", ".join(names[:10]) + " and 3 more." in footer
    assert names[10] not in footer


def test_exactly_ten_orphans_have_no_more(make):
    vault = make({f"technology/o{i:02d}.md": page("technology", f"O{i}") for i in range(9)})
    footer = said(draw.layered(root=vault).svg())
    assert " more" not in footer and "o08" in footer


# --- R2: candidates in the layered view ----------------------------------------------------------------


def test_layered_with_candidates_holds_each_rule_4_candidate_of_the_chosen_narratives(vault):
    for names in (["dry"], ["dry", "wet"], None):
        d = scat_kg.layered(names, candidates=True, root=vault).to_dict()
        chosen = names or d["narratives"]
        assert d["candidates"] == candidates_of(vault, chosen)
    assert scat_kg.layered(["dry"], candidates=True, root=vault).to_dict()["candidates"]


def test_the_same_pair_told_by_two_narratives_is_listed_once_each(make):
    twin = narrative("Twin", "The [[farmers]] and [[towns]] and [[water]].", [])
    vault = make({"narrative/twin.md": twin, "narrative/twin2.md": twin})
    got = scat_kg.layered(["twin", "twin2"], candidates=True, root=vault).to_dict()["candidates"]
    pair = [c for c in got if (c["from"], c["to"]) == ("farmers", "water")]
    assert sorted(c["narrative"] for c in pair) == ["twin", "twin2"]


def test_candidates_are_dashed_in_the_plot_and_listed_in_the_text(vault):
    view = scat_kg.layered(["dry"], candidates=True, root=vault)
    cands = view.to_dict()["candidates"]
    svg = draw.render(view).svg()
    assert dashed(svg) == len(cands) >= 1
    assert "dashed line: a link with no row (a candidate)." in said(svg)
    text = str(view)
    assert "candidates (linked, no row)" in text
    assert all(f"{c['from']} -> {c['to']}" in text for c in cands)


def test_without_candidates_nothing_changes(vault):
    plain = scat_kg.layered(root=vault)
    assert plain.to_dict() == scat_kg.layered(candidates=False, root=vault).to_dict()
    assert not {"candidates", "no_account"} & set(plain.to_dict())
    svg = draw.layered(root=vault).svg()
    assert dashed(svg) == 0 and "dashed" not in said(svg)
    assert svg == draw.layered(candidates=False, root=vault).svg()
    assert "candidates" not in str(plain)


def test_draw_layered_takes_candidates_and_draws_them(vault):
    d = draw.layered(["dry"], candidates=True, root=vault)
    assert any(dashed_ for *_, dashed_ in d.edges())
    assert d.svg() == draw.render(scat_kg.layered(["dry"], candidates=True, root=vault)).svg()
    assert (
        d.png() == draw.layered(["dry"], candidates=True, root=vault).png()
    )  # same call, same bytes


def test_candidates_must_be_a_bool(vault):
    got = scat_kg.layered(candidates="yes", root=vault)
    want = scat_kg.fingerprint("dry", candidates="yes", root=vault)
    assert got.refused and got.refused[0].why == want.refused[0].why
    assert not isinstance(got, views.View)


# --- R2b: the no-account flag ------------------------------------------------------------------------


def test_a_narrative_with_no_account_carries_the_flag_when_candidates_are_asked(make):
    vault = make({"narrative/bare.md": BARE})
    fp = scat_kg.fingerprint("bare", candidates=True, root=vault).to_dict()["narratives"][0]
    assert fp["no_account"] is True
    lay = scat_kg.layered(candidates=True, root=vault).to_dict()
    assert lay["no_account"] == ["bare"]  # the others have account text
    # both renderings
    assert "no account text" in str(scat_kg.fingerprint("bare", candidates=True, root=vault))
    assert "no account text: bare;" in str(scat_kg.layered(candidates=True, root=vault))
    one = said(draw.fingerprint("bare", candidates=True, root=vault).svg())
    assert "no account text: every candidate for it is just an adjacent pair, not evidence." in one
    many = said(draw.layered(candidates=True, root=vault).svg())
    assert "no account text: bare; every candidate for them is just an adjacent pair" in many


def test_headings_and_whitespace_are_no_account(make):
    body = "# Bare\n\n   \n## Notes\n"
    vault = make(
        {"narrative/bare.md": BARE.replace("\n\n## Edges told", f"\n{body}\n## Edges told", 1)}
    )
    assert "bare" in scat_kg.layered(candidates=True, root=vault).to_dict()["no_account"]


def test_a_narrative_with_account_text_has_no_flag(vault):
    assert (
        "no_account"
        not in scat_kg.fingerprint("dry", candidates=True, root=vault).to_dict()["narratives"][0]
    )
    assert "no_account" not in scat_kg.layered(candidates=True, root=vault).to_dict()
    assert "no account text" not in said(draw.layered(candidates=True, root=vault).svg())


def test_text_after_the_table_section_is_account_text(make):
    vault = make({"narrative/bare.md": BARE + "\n# After\nA word at the end.\n"})
    assert "no_account" not in scat_kg.layered(["bare"], candidates=True, root=vault).to_dict()


def test_not_asked_no_flag(make):
    vault = make({"narrative/bare.md": BARE})
    assert "no_account" not in scat_kg.fingerprint("bare", root=vault).to_dict()["narratives"][0]
    assert "no_account" not in scat_kg.layered(root=vault).to_dict()
    assert "no account text" not in said(draw.layered(root=vault).svg())
    assert "no account text" not in said(draw.fingerprint("bare", root=vault).svg())
