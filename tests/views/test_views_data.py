"""Every view over the small vault, computed by hand: each expected value is written out here."""

import json

import pytest

import scat_kg


def n(name, type_, status):
    return {"name": name, "type": type_, "status": status}


def e(type_, a, b, narratives, status):
    return {"type": type_, "from": a, "to": b, "narratives": narratives, "status": status}


FARMERS = n("farmers", "group", "draft")
TOWNS = n("towns", "group", "stub")
WATER = n("water", "concern", "draft")
COST = n("cost", "concern", "stub")
SENSOR = n("sensor", "affordance", "draft")
ALERT = n("alert", "affordance", "stub")
PROBE = n("probe", "technology", "draft")
RADIO = n("radio", "technology", "stub")

F_COST = e("holds", "farmers", "cost", ["diamond"], "draft")
F_WATER = e("holds", "farmers", "water", ["dry", "wet"], "stub")  # told twice: the less advanced
T_COST = e("holds", "towns", "cost", ["split"], "draft")
C_SENSOR = e("addressed-by", "cost", "sensor", ["diamond"], "draft")
W_ALERT = e("addressed-by", "water", "alert", ["wet"], "stub")
W_SENSOR = e("addressed-by", "water", "sensor", ["dry"], "draft")
A_RADIO = e("provided-by", "alert", "radio", ["split"], "draft")
S_PROBE = e("provided-by", "sensor", "probe", ["dry"], "draft")


def lines(*xs):
    return "\n".join(xs)


def doc(view, operation):
    d = view.to_dict()
    assert view.ok is True
    assert d["schema_version"] == 2
    assert d["kind"] == "view"
    assert d["operation"] == operation
    assert d["ok"] is True
    return d


# ---------------------------------------------------------------- fingerprint


def test_fingerprint_of_a_narrative_with_edges_and_a_candidate(vault):
    d = doc(scat_kg.fingerprint("dry", root=vault), "fingerprint")
    assert d["narratives"] == [
        {
            "name": "dry",
            "kind": "scenario",
            "status": "draft",
            "nodes": [FARMERS, TOWNS, WATER, SENSOR, PROBE],
            "edges": [F_WATER, W_SENSOR, S_PROBE],
            # rule 4: the account links towns and water, and no row says towns holds water
            "candidates": [{"type": "holds", "from": "towns", "to": "water"}],
        }
    ]


def test_fingerprint_of_a_narrative_with_no_edges(vault):
    d = doc(scat_kg.fingerprint("empty", root=vault), "fingerprint")
    assert d["narratives"] == [
        {
            "name": "empty",
            "kind": None,
            "status": "draft",
            "nodes": [FARMERS],
            "edges": [],
            "candidates": [],
        }
    ]


def test_fingerprint_that_is_disconnected(vault):
    d = doc(scat_kg.fingerprint("split", root=vault), "fingerprint")
    (f,) = d["narratives"]
    assert f["nodes"] == [TOWNS, COST, ALERT, RADIO]
    # two groups of nodes, {towns, cost} and {alert, radio}, with no edge between them
    assert f["edges"] == [T_COST, A_RADIO]
    # linked on both ends, no row: a candidate, not an edge
    assert f["candidates"] == [{"type": "addressed-by", "from": "cost", "to": "alert"}]


def test_an_edge_told_by_two_narratives_is_in_both_fingerprints(vault):
    dry = scat_kg.fingerprint("dry", root=vault).to_dict()["narratives"][0]
    wet = scat_kg.fingerprint("wet", root=vault).to_dict()["narratives"][0]
    assert F_WATER in dry["edges"] and F_WATER in wet["edges"]
    assert wet["nodes"] == [FARMERS, WATER, ALERT]
    assert wet["edges"] == [F_WATER, W_ALERT]
    assert wet["candidates"] == []
    assert wet["kind"] == "architecture" and wet["status"] == "stub"


def test_fingerprint_of_every_narrative_in_path_order(vault):
    d = doc(scat_kg.fingerprint(root=vault), "fingerprint")
    assert [f["name"] for f in d["narratives"]] == ["diamond", "dry", "empty", "split", "wet"]
    diamond = d["narratives"][0]
    assert diamond["nodes"] == [FARMERS, COST, SENSOR]
    assert diamond["edges"] == [F_COST, C_SENSOR]
    assert diamond["candidates"] == []


def test_fingerprint_text_groups_by_layer(vault):
    text = str(scat_kg.fingerprint("dry", root=vault))
    assert text == lines(
        "fingerprint dry (scenario, draft)",
        "  group",
        "    farmers [draft]",
        "    towns [stub]",
        "  concern",
        "    water [draft]",
        "  affordance",
        "    sensor [draft]",
        "  technology",
        "    probe [draft]",
        "  edges",
        "    holds: farmers -> water [stub; told by dry, wet]",
        "    addressed-by: water -> sensor [draft; told by dry]",
        "    provided-by: sensor -> probe [draft; told by dry]",
        "  candidates (linked, no row)",
        "    holds: towns -> water",
    )


# ---------------------------------------------------------------- edge tables


def test_edge_table_holds(vault):
    d = doc(scat_kg.edge_table("holds", root=vault), "edges")
    assert d["edge_type"] == "holds"
    assert (d["from_layer"], d["to_layer"]) == ("group", "concern")
    assert d["rows"] == [F_COST, F_WATER, T_COST]


def test_edge_table_addressed_by(vault):
    d = doc(scat_kg.edge_table("addressed-by", root=vault), "edges")
    assert (d["from_layer"], d["to_layer"]) == ("concern", "affordance")
    assert d["rows"] == [C_SENSOR, W_ALERT, W_SENSOR]


def test_edge_table_provided_by(vault):
    d = doc(scat_kg.edge_table("provided-by", root=vault), "edges")
    assert (d["from_layer"], d["to_layer"]) == ("affordance", "technology")
    assert d["rows"] == [A_RADIO, S_PROBE]


def test_edge_table_with_no_rows(make):
    root = make({k: None for k in ("narrative/dry.md", "narrative/wet.md", "narrative/diamond.md")})
    d = doc(scat_kg.edge_table("addressed-by", root=root), "edges")
    assert d["rows"] == []
    assert str(scat_kg.edge_table("addressed-by", root=root)) == (
        "edges addressed-by (concern -> affordance): 0"
    )


# ---------------------------------------------------------------- layered view


def test_layered_view_of_two_narratives(vault):
    d = doc(scat_kg.layered(["wet", "dry"], root=vault), "layered")
    assert d["narratives"] == ["dry", "wet"]
    assert d["nodes"] == {
        "group": [FARMERS, TOWNS],
        "concern": [WATER],
        "affordance": [ALERT, SENSOR],
        "technology": [PROBE],
    }
    assert list(d["nodes"]) == ["group", "concern", "affordance", "technology"]
    # every narrative that tells an edge is named, even one outside the chosen set; no candidates
    assert d["edges"] == [F_WATER, W_ALERT, W_SENSOR, S_PROBE]
    assert "candidates" not in d


def test_layered_view_of_a_disconnected_narrative(vault):
    d = doc(scat_kg.layered(["split"], root=vault), "layered")
    assert d["nodes"] == {
        "group": [TOWNS],
        "concern": [COST],
        "affordance": [ALERT],
        "technology": [RADIO],
    }
    assert d["edges"] == [T_COST, A_RADIO]


def test_layered_view_of_a_narrative_with_no_edges(vault):
    d = doc(scat_kg.layered(["empty"], root=vault), "layered")
    assert d["nodes"] == {"group": [FARMERS], "concern": [], "affordance": [], "technology": []}
    assert d["edges"] == []


def test_layered_view_of_the_whole_vault(vault):
    d = doc(scat_kg.layered(root=vault), "layered")
    assert d["narratives"] == ["diamond", "dry", "empty", "split", "wet"]
    # `idle` is linked by no narrative, so it is in no fingerprint
    assert d["nodes"] == {
        "group": [FARMERS, TOWNS],
        "concern": [COST, WATER],
        "affordance": [ALERT, SENSOR],
        "technology": [PROBE, RADIO],
    }
    assert d["edges"] == [F_COST, F_WATER, T_COST, C_SENSOR, W_ALERT, W_SENSOR, A_RADIO, S_PROBE]


def test_layered_view_of_an_empty_vault(make):
    root = make({k: None for k in base_narratives()})
    d = doc(scat_kg.layered(root=root), "layered")
    assert d["narratives"] == []
    assert d["edges"] == []
    assert str(scat_kg.layered(root=root)) == "layered view of no narratives"


def base_narratives():
    return ["narrative/" + s + ".md" for s in ("dry", "wet", "empty", "split", "diamond")]


# ---------------------------------------------------------------- trace

DOWN_FROM_FARMERS = (
    [COST, WATER, ALERT, SENSOR, PROBE, RADIO],
    [F_COST, F_WATER, C_SENSOR, W_ALERT, W_SENSOR, A_RADIO, S_PROBE],
)


@pytest.mark.parametrize(
    "node, direction, up, down, edges",
    [
        # a group: nothing above; everything below, reached by two paths to `sensor`
        ("farmers", "up", [], [], []),
        ("farmers", "down", [], DOWN_FROM_FARMERS[0], DOWN_FROM_FARMERS[1]),
        ("farmers", "both", [], DOWN_FROM_FARMERS[0], DOWN_FROM_FARMERS[1]),
        # a concern
        ("water", "up", [FARMERS], [], [F_WATER]),
        ("water", "down", [], [ALERT, SENSOR, PROBE, RADIO], [W_ALERT, W_SENSOR, A_RADIO, S_PROBE]),
        (
            "water",
            "both",
            [FARMERS],
            [ALERT, SENSOR, PROBE, RADIO],
            [F_WATER, W_ALERT, W_SENSOR, A_RADIO, S_PROBE],
        ),
        # an affordance
        ("alert", "up", [FARMERS, WATER], [], [F_WATER, W_ALERT]),
        ("alert", "down", [], [RADIO], [A_RADIO]),
        ("alert", "both", [FARMERS, WATER], [RADIO], [F_WATER, W_ALERT, A_RADIO]),
        # a technology: nothing below
        ("radio", "up", [FARMERS, WATER, ALERT], [], [F_WATER, W_ALERT, A_RADIO]),
        ("radio", "down", [], [], []),
        ("radio", "both", [FARMERS, WATER, ALERT], [], [F_WATER, W_ALERT, A_RADIO]),
    ],
)
def test_trace_reaches_exactly_the_nodes_and_walks_the_edges(
    vault, node, direction, up, down, edges
):
    d = doc(scat_kg.trace(node, direction, root=vault), "trace")
    assert d["node"] == node and d["direction"] == direction
    assert d["up"] == up
    assert d["down"] == down
    assert d["edges"] == edges
    assert node not in [x["name"] for x in d["up"] + d["down"]]


def test_trace_where_two_paths_reach_one_node(vault):
    # farmers -> cost -> sensor and farmers -> water -> sensor: `sensor` once, and both edges into it walked
    d = scat_kg.trace("farmers", "down", root=vault).to_dict()
    assert [x["name"] for x in d["down"]].count("sensor") == 1
    assert C_SENSOR in d["edges"] and W_SENSOR in d["edges"]
    # and upward from `sensor`, `farmers` is reached by two paths and listed once
    u = scat_kg.trace("sensor", "up", root=vault).to_dict()
    assert u["up"] == [FARMERS, TOWNS, COST, WATER]
    assert u["edges"] == [F_COST, F_WATER, T_COST, C_SENSOR, W_SENSOR]
    assert u["down"] == []


def test_trace_both_directions_from_the_middle_of_two_paths(vault):
    d = scat_kg.trace("sensor", "both", root=vault).to_dict()
    assert d["up"] == [FARMERS, TOWNS, COST, WATER]
    assert d["down"] == [PROBE]
    assert d["edges"] == [F_COST, F_WATER, T_COST, C_SENSOR, W_SENSOR, S_PROBE]


def test_trace_default_direction_is_both(vault):
    assert (
        scat_kg.trace("alert", root=vault).to_dict()
        == scat_kg.trace("alert", "both", root=vault).to_dict()
    )


def test_trace_of_an_isolated_node(vault):
    d = doc(scat_kg.trace("idle", root=vault), "trace")
    assert d["up"] == [] and d["down"] == [] and d["edges"] == []
    assert str(scat_kg.trace("idle", root=vault)) == "trace idle (both)"


def test_a_direction_not_asked_is_an_empty_list(vault):
    d = scat_kg.trace("water", "up", root=vault).to_dict()
    assert d["down"] == []


def test_trace_text_groups_by_layer(vault):
    assert str(scat_kg.trace("alert", "both", root=vault)) == lines(
        "trace alert (both)",
        " up",
        "  group",
        "    farmers [draft]",
        "  concern",
        "    water [draft]",
        " down",
        "  technology",
        "    radio [stub]",
        "  edges",
        "    holds: farmers -> water [stub; told by dry, wet]",
        "    addressed-by: water -> alert [stub; told by wet]",
        "    provided-by: alert -> radio [draft; told by split]",
    )


# ---------------------------------------------------------------- annotations, text, determinism


def test_a_relationship_annotation_appears_in_no_view(vault):
    # water's page says "Pulls against [[cost]]": a link, not an edge
    assert COST not in scat_kg.trace("water", "both", root=vault).to_dict()["down"]
    assert COST not in scat_kg.trace("water", "both", root=vault).to_dict()["up"]
    d = scat_kg.layered(["dry", "wet"], root=vault).to_dict()
    assert COST not in d["nodes"]["concern"]
    assert not any({x["from"], x["to"]} == {"water", "cost"} for x in d["edges"])
    for view in (
        scat_kg.fingerprint(root=vault),
        scat_kg.layered(root=vault),
        scat_kg.edge_table("holds", root=vault),
    ):
        text = json.dumps(view.to_dict())
        assert "annotation" not in text and "Pulls against" not in text
        assert not any(
            {x["from"], x["to"]} == {"water", "cost"}
            for x in view.to_dict().get("edges", view.to_dict().get("rows", []))
        )


def test_the_text_never_holds_a_link(vault):
    for view in (
        scat_kg.fingerprint(root=vault),
        scat_kg.edge_table("holds", root=vault),
        scat_kg.layered(root=vault),
        scat_kg.trace("farmers", root=vault),
    ):
        assert "[[" not in str(view) and "[[" not in json.dumps(view.to_dict())


def test_a_view_prints_as_its_text(vault):
    v = scat_kg.edge_table("provided-by", root=vault)
    assert (
        repr(v)
        == str(v)
        == lines(
            "edges provided-by (affordance -> technology): 2",
            "    provided-by: alert -> radio [draft; told by split]",
            "    provided-by: sensor -> probe [draft; told by dry]",
        )
    )


CALLS = [
    lambda r: scat_kg.fingerprint(root=r),
    lambda r: scat_kg.fingerprint("dry", root=r),
    lambda r: scat_kg.edge_table("holds", root=r),
    lambda r: scat_kg.layered(root=r),
    lambda r: scat_kg.layered(["dry", "split"], root=r),
    lambda r: scat_kg.trace("farmers", root=r),
    lambda r: scat_kg.trace("radio", "up", root=r),
]


@pytest.mark.parametrize("call", CALLS)
def test_two_calls_give_the_same_bytes(vault, call):
    a, b = call(vault), call(vault)
    assert a.to_dict() == b.to_dict()
    assert json.dumps(a.to_dict()) == json.dumps(b.to_dict())
    assert str(a) == str(b)


def test_the_order_does_not_depend_on_how_the_vault_was_written(tmp_path, vault):
    # the same pages written in the reverse order give the same document
    from viewutil import base_files, write

    files = base_files()
    other = write(tmp_path / "rev", dict(reversed(list(files.items()))))
    for call in CALLS:
        assert json.dumps(call(vault).to_dict()) == json.dumps(call(other).to_dict())


def test_the_public_names(vault):
    assert scat_kg.load(vault).summary()["edges"] == 8
    assert scat_kg.load(vault) == scat_kg.graph.load(vault)
    for name in ("load", "fingerprint", "edge_table", "layered", "trace", "View"):
        assert name in scat_kg.__all__
