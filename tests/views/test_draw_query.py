"""The query is its own layer (WP33): a drawing is made from a query result, never by a second query, and what it
draws is what the same result's table (`to_dict()`) says."""

import sys

import pytest

import scat_kg
from scat_kg import draw, views
from scat_kg.ops.result import Result
from scat_kg.tbox import TBOX

EVIDENCE = sys.modules["scat_kg.evidence"]  # `scat_kg.evidence` the name is the function


def table_of(view: views.View) -> tuple[set, set]:
    """What the table of a result says is drawn, by the rule: nodes (name, layer) and edges (from, to, dashed).

    A fingerprint drops its kind's layer (draw.DROPPED): drawn = table minus that layer's nodes and the edges and
    candidates that touch them. A trace's starting node is the result's `traced`; the document leaves it out.
    """
    d = view.to_dict()
    if view.operation == "fingerprint":
        n = d["narratives"][0]
        drop = draw.DROPPED.get(n["kind"])
        nodes = {(x["name"], x["type"]) for x in n["nodes"] if x["type"] != drop}
        gone = {x["name"] for x in n["nodes"] if x["type"] == drop}
        edges = {(e["from"], e["to"], False) for e in n["edges"]}
        edges |= {(c["from"], c["to"], True) for c in n.get("candidates", ())}
        return nodes, {e for e in edges if not ({e[0], e[1]} & gone)}
    if view.operation == "layered":
        nodes = {(x["name"], layer) for layer, xs in d["nodes"].items() for x in xs}
    else:
        nodes = {(x["name"], x["type"]) for x in [*d["up"], *d["down"], view.traced]}
    return nodes, {(e["from"], e["to"], False) for e in d["edges"]}


def disagreements(view: views.View, drawing: draw.Drawing) -> list[str]:
    """Where the drawing and the table of the same result differ (empty: they agree)."""
    nodes, edges = table_of(view)
    got_n, got_e = set(drawing.nodes()), set(drawing.edges())
    return (
        [f"drawn, not in the table: node {n}" for n in sorted(got_n - nodes)]
        + [f"in the table, not drawn: node {n}" for n in sorted(nodes - got_n)]
        + [f"drawn, not in the table: edge {e}" for e in sorted(got_e - edges)]
        + [f"in the table, not drawn: edge {e}" for e in sorted(edges - got_e)]
    )


def queries(vault) -> list[views.View]:
    out = [
        scat_kg.fingerprint(n, candidates=c, root=vault)
        for n in ("dry", "wet", "split", "diamond", "empty")
        for c in (False, True)
    ]
    out += [scat_kg.layered(root=vault), scat_kg.layered(["dry", "wet"], root=vault)]
    out += [
        scat_kg.trace(n, d, root=vault)
        for n in ("water", "farmers", "probe", "idle")
        for d in ("up", "down", "both")
    ]
    assert all(isinstance(v, views.View) for v in out)
    return out


def test_every_drawing_is_its_tables_nodes_and_edges(vault):
    for view in queries(vault):
        drawing = draw.render(view)
        assert disagreements(view, drawing) == [], (view.operation, view.data.get("node"))


def test_the_dropped_layer_and_candidates_are_accounted_for(vault):
    # wet is an architecture (no stakeholder column), dry a scenario (no technology column), dry has a candidate
    wet = draw.render(scat_kg.fingerprint("wet", root=vault))
    assert {layer for _, layer in wet.nodes()} == {"concern", "affordance"}  # farmers is not drawn
    assert ("farmers", "water", False) not in wet.edges()
    dry = draw.render(scat_kg.fingerprint("dry", candidates=True, root=vault))
    assert {layer for _, layer in dry.nodes()} == set(TBOX.layers) - {
        "technology"
    }  # probe is not drawn
    assert any(dashed for *_, dashed in dry.edges())
    plain = draw.render(scat_kg.fingerprint("dry", root=vault))
    assert not any(dashed for *_, dashed in plain.edges())


def test_a_table_that_disagrees_with_its_plot_fails(vault):
    view = scat_kg.layered(root=vault)
    drawing = draw.render(view)
    assert disagreements(view, drawing) == []
    lost = views.View("layered", {**view.data, "edges": view.data["edges"][1:]})
    assert any("drawn, not in the table: edge" in m for m in disagreements(lost, drawing))
    more = {**view.data, "edges": [*view.data["edges"], {"from": "towns", "to": "probe"}]}
    assert any(
        "in the table, not drawn: edge" in m
        for m in disagreements(views.View("layered", more), drawing)
    )
    nodes = {**view.data["nodes"], "group": []}
    assert any(
        "drawn, not in the table: node" in m
        for m in disagreements(views.View("layered", {**view.data, "nodes": nodes}), drawing)
    )


def test_rendering_a_result_never_runs_a_query(vault, monkeypatch):
    results = [
        scat_kg.fingerprint("dry", candidates=True, root=vault),
        scat_kg.layered(root=vault),
        scat_kg.trace("water", root=vault),
    ]

    def boom(*a, **k):
        raise AssertionError("the query ran")

    for name in ("fingerprint", "edge_table", "layered", "trace", "attribution", "_open", "load"):
        monkeypatch.setattr(views, name, boom)
    monkeypatch.setattr("scat_kg.graph.load", boom)
    monkeypatch.setattr(EVIDENCE, "evidence", boom)
    monkeypatch.setattr(scat_kg, "evidence", boom)
    for result in results:
        d = draw.render(result)
        assert d.png().startswith(b"\x89PNG") and "<svg" in d.svg()


@pytest.mark.parametrize(
    "call",
    [
        lambda v: draw.fingerprint("dry", candidates=True, root=v),
        lambda v: draw.layered(["dry"], root=v),
        lambda v: draw.trace("water", root=v),
    ],
)
def test_each_convenience_runs_its_query_once(vault, monkeypatch, call):
    calls = []
    for name in ("fingerprint", "layered", "trace"):
        real = getattr(views, name)

        def spy(*a, _n=name, _real=real, **k):
            calls.append(_n)
            return _real(*a, **k)

        monkeypatch.setattr(views, name, spy)
    real_ev = EVIDENCE.evidence

    def ev_spy(*a, **k):
        calls.append("evidence")
        return real_ev(*a, **k)

    monkeypatch.setattr(EVIDENCE, "evidence", ev_spy)
    monkeypatch.setattr(scat_kg, "evidence", ev_spy)
    drawing = call(vault)
    assert isinstance(drawing, draw.Drawing)
    assert len(calls) == 1 and "evidence" not in calls


def test_a_result_it_cannot_draw_is_refused_not_raised(vault):
    bare = {"node": "x", "direction": "both", "up": [], "down": [], "edges": []}
    for result in (
        scat_kg.edge_table("holds", root=vault),
        scat_kg.fingerprint(None, root=vault),  # every narrative
        views.View("fingerprint", {"narratives": []}),  # none
        views.View("trace", bare),  # a trace that does not carry its starting node
    ):
        got = draw.render(result)
        assert isinstance(got, Result) and got.refused and got.operation == "draw"
    refusal = scat_kg.fingerprint("nope", root=vault)
    assert draw.render(refusal) is refusal  # a refusal passes through unchanged


def test_the_table_of_a_result_is_its_document(vault):
    view = scat_kg.trace("water", root=vault)
    assert view.to_dict()["kind"] == "view" and "traced" not in view.to_dict()
    assert view.traced == {"name": "water", "type": "concern", "status": "draft"}


def test_the_twin_rule_every_drawing_has_a_view():
    drawings = [
        n
        for n, f in vars(draw).items()
        if not n.startswith("_")
        and callable(f)
        and getattr(f, "__module__", "") == draw.__name__
        and not isinstance(f, type)
        and n != "render"
    ]
    assert {"fingerprint", "layered", "trace"} <= set(drawings)
    for name in drawings:
        assert callable(getattr(views, name, None)), f"draw.{name} has no views.{name}"
