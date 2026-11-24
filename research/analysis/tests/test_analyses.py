"""Concrete facts about the two committed vaults (the template's case study, the synthetic water cooperative).

The synthetic vault has its patterns planted (see synth/README.md); these tests pin that the analyses find them.
"""

import pandas as pd
import pytest

import scat_analysis as sa
from conftest import SYNTHETIC
from scat_analysis import load_graph


def counts(sg):
    return sg.summary()["count"].to_dict()


# ---- graph shape -----------------------------------------------------------------------------------------

def test_case_study_counts(case):
    assert counts(case) == {"group": 3, "concern": 3, "affordance": 3, "technology": 3, "heldby edges": 2,
                            "addresses edges": 3, "attributes edges": 3, "conflict pairs": 1, "coded records": 4}
    assert case.dangling == []


def test_synthetic_counts(synth):
    assert counts(synth) == {"group": 7, "concern": 18, "affordance": 13, "technology": 10, "heldby edges": 40,
                             "addresses edges": 31, "attributes edges": 23, "conflict pairs": 5, "coded records": 7}
    assert synth.dangling == []


def test_edges_follow_the_chain_direction(synth):
    order = {"stakeholder-group": 0, "concern": 1, "affordance": 2, "technology": 3}
    for u, v in synth.G.edges:
        assert order[synth.G.nodes[v]["layer"]] == order[synth.G.nodes[u]["layer"]] + 1


def test_status_filter(synth):
    assert counts(load_graph(SYNTHETIC, "done")) == counts(synth)
    assert counts(load_graph(SYNTHETIC, {"done"})) == counts(synth)
    empty = load_graph(SYNTHETIC, "no-such-status")
    assert empty.G.number_of_nodes() == 0 and empty.conflicts.number_of_edges() == 0


# ---- conflicts: symmetric closure ------------------------------------------------------------------------

def test_conflicts_are_the_symmetric_closure(synth, case):
    # each pair is declared on exactly one concern page, yet is reachable from both ends
    assert all(len(d["declared_by"]) == 1 for *_, d in synth.conflicts.edges(data=True))
    for a, b, d in synth.conflicts.edges(data=True):
        assert synth.conflicts.has_edge(a, b) and synth.conflicts.has_edge(b, a)
        assert d["declared_by"][0] in (a, b)
    assert sorted(synth.conflicts.neighbors("guaranteed-irrigation-allocation")) == ["environmental-flow-protection", "fair-usage-limits"]
    assert case.conflicts["attribution"]["anonymity"]["declared_by"] == ["anonymity"]
    assert case.conflicts.has_edge("anonymity", "attribution")


def test_tension_pairs_hold_both_directions_once(synth):
    pairs = sa.tension(synth)["pairs"]
    assert len(pairs) == 5
    assert (pairs.n_declarations == 1).all()
    assert {frozenset(r) for r in zip(pairs.concern_a, pairs.concern_b)} == {frozenset(e) for e in synth.conflicts.edges}


# ---- planted gaps ----------------------------------------------------------------------------------------

def test_synthetic_gaps(synth):
    g = sa.gaps(synth)
    assert g["concerns no affordance addresses"] == ["hands-on-site-visits", "predictable-maintenance-schedule", "pupil-learning-access"]
    assert g["affordances attributed to no technology"] == ["community-asset-fund", "operator-training-course", "reserve-storage-policy"]
    assert g["groups whose concerns are all unaddressed"] == ["school-liaisons"]
    assert g["groups holding no concern"] == [] and g["concerns held by no group"] == []
    assert g["affordances addressing no concern"] == [] and g["technologies attributed to no affordance"] == []


def test_synthetic_traceability(synth):
    tr = sa.traceability(synth)
    assert tr.chain.value_counts().to_dict() == {"complete": 15, "unaddressed": 3}
    assert set(tr.index[tr.chain == "unaddressed"]) == set(sa.gaps(synth)["concerns no affordance addresses"])
    cov = sa.group_coverage(synth)
    assert cov.loc["school-liaisons"].to_dict() == {"concerns_held": 2, "complete": 0, "addressed, no technology": 0, "unaddressed": 2}
    assert (cov.concerns_held.sum()) == 40  # one per heldby edge


def test_case_study_gaps(case):
    g = sa.gaps(case)
    assert g["groups holding no concern"] == ["workshop-participants"]
    assert g["concerns held by no group"] == ["attribution"]
    assert g["concerns no affordance addresses"] == ["attribution"]
    assert g["groups whose concerns are all unaddressed"] == []
    assert sa.traceability(case).chain.value_counts().to_dict() == {"complete": 2, "unaddressed": 1}


# ---- tension ---------------------------------------------------------------------------------------------

def test_groups_holding_both_sides(synth):
    both = sa.tension(synth)["both_sides"]
    assert len(both) == 4
    assert sorted(both.group) == ["board-volunteers"] * 3 + ["treatment-operators"]
    assert ("treatment-operators", "low-operating-cost", "safe-treatment-margins") in set(map(tuple, both.values))


def test_groups_on_opposite_sides(synth):
    opp = sa.tension(synth)["opposite_sides"]
    assert len(opp) == 14                                                         # 14 rows of (group, concern, group, concern)
    assert len({frozenset((r.group_x, r.group_y)) for r in opp.itertuples()}) == 8   # covering 8 distinct unordered group pairs
    assert (opp.group_x != opp.group_y).all()
    pairs = {(r.group_x, r.group_y) for r in opp.itertuples()}
    assert ("farm-irrigators", "household-members") in pairs                      # detailed visibility vs privacy
    assert ("watershed-stewards", "farm-irrigators") in pairs                     # flow protection vs irrigation allocation
    assert not ((opp.group_x == "farm-irrigators") & (opp.group_y == "farm-irrigators")).any()


def test_case_study_tension(case):
    t = sa.tension(case)
    assert len(t["pairs"]) == 1 and t["both_sides"].empty and t["opposite_sides"].empty
    rec = sa.conflict_records(case)
    assert rec.record.tolist() == ["notes-at-a-chatham-house-session-coded"]


# ---- hubs, projections, provenance -----------------------------------------------------------------------

def test_hub_nodes(synth):
    c = sa.centrality(synth)
    assert c.loc["usage-dashboard", ["concerns_carried", "groups_behind"]].tolist() == [8, 6]
    assert c.loc["member-portal", "concerns_carried"] == 13
    assert c[c.layer == "affordance"].concerns_carried.max() == 8
    assert c.concerns_carried.max() == 13 and c.concerns_carried.idxmax() == "member-portal"
    assert c.loc["sensor-telemetry-platform", "concerns_carried"] == 9


def test_case_study_carriage_is_flat(case):
    c = sa.centrality(case)
    assert (c.concerns_carried == 1).all() and len(c) == 6


def test_projections(synth, case):
    p = sa.projections(synth)
    groups = p[p.projection == "groups by shared concern"]
    assert len(groups) == 13
    assert "school-liaisons" not in set(groups.node_a) | set(groups.node_b)   # shares no concern
    assert set(p.projection) == {"groups by shared concern", "concerns by shared affordance"}
    assert sa.projections(case).empty


def test_provenance(synth, case):
    long = sa.provenance(synth)
    assert synth.records.shape[0] == 7 and long.record.nunique() == 7
    assert set(long.role) <= {"groups", "concerns", "affordances", "technologies"}
    assert long.groupby("role").size().to_dict() == {"affordances": 17, "concerns": 24, "groups": 12, "technologies": 11}
    m = sa.provenance_matrix(synth)
    assert m.shape == (7, 18) and int(m.values.sum()) == 24
    assert case.records.record.nunique() == 4


# ---- no ranking, determinism -----------------------------------------------------------------------------

FORBIDDEN = ("rank", "score", "best", "worst", "better", "importance", "priority", "rating")


def all_frames(sg):  # provenance_matrix is left out: its columns are node names, not measures
    out = {"traceability": sa.traceability(sg), "group_coverage": sa.group_coverage(sg), "projections": sa.projections(sg),
           "centrality": sa.centrality(sg), "communities": sa.communities(sg), "provenance": sa.provenance(sg),
           "conflict_records": sa.conflict_records(sg), "summary": sg.summary(),
           "records": sg.records}
    out.update({f"tension.{k}": v for k, v in sa.tension(sg).items()})
    return out


@pytest.mark.parametrize("which", ["case", "synth"])
def test_no_analysis_output_carries_a_rank_or_score(which, request):
    sg = request.getfixturevalue(which)
    for name, df in all_frames(sg).items():
        assert isinstance(df, pd.DataFrame), name
        for col in [df.index.name or "", *map(str, df.columns)]:
            assert not any(w in col.lower() for w in FORBIDDEN), f"{name}: column {col!r}"
    for label in sa.gaps(sg):
        assert not any(w in label.lower() for w in FORBIDDEN)


@pytest.mark.parametrize("which", ["case", "synth"])
def test_outputs_are_alphabetical_not_ordered_by_a_measure(which, request):
    sg = request.getfixturevalue(which)
    for name in ("traceability", "group_coverage", "centrality"):
        df = getattr(sa, name)(sg)
        assert list(df.index) == sorted(df.index), name


def test_communities_are_deterministic(synth, case):
    for sg in (synth, case):
        first = sa.communities(sg, seed=1)
        for _ in range(3):
            pd.testing.assert_frame_equal(first, sa.communities(sg, seed=1))
    c = sa.communities(synth)
    assert c.greedy_modularity.nunique() == 7 and c.louvain.nunique() == 6
    assert sa.community_agreement(c) == pytest.approx(0.31, abs=0.005)
    assert 0.0 <= sa.community_agreement(c) <= 1.0


def test_communities_same_on_a_fresh_load():
    a = sa.communities(load_graph(SYNTHETIC), seed=1)
    b = sa.communities(load_graph(SYNTHETIC), seed=1)
    pd.testing.assert_frame_equal(a, b)
