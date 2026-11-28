"""WP33-R1 to R3: a view tool runs its query once per call and renders what `output` asks from that one result;
`both` is the plot, then the table, and the two agree. The default call is the view document, as before."""

import base64
import json
import sys

import pytest
from mcp.shared.memory import create_connected_server_and_client_session as connected
from mcputil import copy_vault

import scat_tools
from scat_tools import draw, views
from scat_tools.mcp_server.server import build
from scat_tools.ops.result import stamp

PNG = b"\x89PNG\r\n\x1a\n"
EVIDENCE = sys.modules["scat_tools.evidence"]  # `scat_tools.evidence` the name is the function

# (tool, arguments, the view it runs, the local call on the same vault)
CALLS = [
    ("fingerprint", {"narrative": "funders-meeting"}, "fingerprint"),
    ("fingerprint", {"narrative": "funders-meeting", "candidates": True}, "fingerprint"),
    ("layered", {}, "layered"),
    ("layered", {"narratives": ["funders-meeting", "saturday-at-the-lending-desk"]}, "layered"),
    ("trace", {"node": "self-checkout"}, "trace"),
    ("trace", {"node": "self-checkout", "direction": "up"}, "trace"),
]


@pytest.fixture(scope="module")
def vault(tmp_path_factory):
    return copy_vault(tmp_path_factory.mktemp("views") / "vault")


def run_tool(vault, name, args):
    """The whole result of `tools/call` on a real server session (in this process), as the client sees it."""

    async def go():
        async with connected(build(vault)._mcp_server) as s:
            return await s.call_tool(name, args)

    import asyncio

    return asyncio.run(go())


@pytest.fixture
def counted(monkeypatch):
    """Every view query and evidence read that runs, by name (the server calls `scat_tools.<view>`, draw calls `views`)."""
    calls: list[str] = []
    for name in ("fingerprint", "layered", "trace", "edge_table", "attribution"):
        real = getattr(views, name)

        def spy(*a, _n=name, _real=real, **k):
            calls.append(_n)
            return _real(*a, **k)

        monkeypatch.setattr(views, name, spy)
        monkeypatch.setattr(scat_tools, name, spy)
    real_ev = EVIDENCE.evidence

    def ev_spy(*a, **k):
        calls.append("evidence")
        return real_ev(*a, **k)

    monkeypatch.setattr(EVIDENCE, "evidence", ev_spy)
    monkeypatch.setattr(scat_tools, "evidence", ev_spy)
    return calls


@pytest.mark.parametrize("output", ["table", "plot", "both"])
@pytest.mark.parametrize("name,args,view", CALLS)
def test_one_call_runs_the_query_once(vault, counted, name, args, view, output):  # WP33-R1
    res = run_tool(vault, name, {**args, "output": output})
    assert not res.isError and res.content
    assert counted == [view]


def test_a_refused_or_unrendered_call_still_runs_the_query_once(vault, counted):
    for output in ("table", "plot", "both"):
        counted.clear()
        run_tool(vault, "fingerprint", {"narrative": "no-such-page", "output": output})
        assert counted == ["fingerprint"]
    counted.clear()
    run_tool(
        vault, "fingerprint", {"output": "plot"}
    )  # every narrative: the view runs, the plot is refused
    assert counted == ["fingerprint"]


def table_of(doc: dict, drawing) -> tuple[set, set, set, set]:
    """(table nodes, table edges, drawn nodes, drawn edges) as (name, layer) and (from, to, dashed).

    A fingerprint drops its kind's layer (`draw.DROPPED`): drawn = table minus that layer's nodes and the edges and
    candidates that touch them. A trace's starting node is in the drawing, not in the document's lists.
    """
    if doc["operation"] == "fingerprint":
        n = doc["narratives"][0]
        drop = draw.DROPPED.get(n["kind"])
        nodes = {(x["name"], x["type"]) for x in n["nodes"] if x["type"] != drop}
        gone = {x["name"] for x in n["nodes"] if x["type"] == drop}
        edges = {(e["from"], e["to"], False) for e in n["edges"]}
        edges |= {(c["from"], c["to"], True) for c in n.get("candidates", ())}
        edges = {e for e in edges if not ({e[0], e[1]} & gone)}
    elif doc["operation"] == "layered":
        nodes = {(x["name"], layer) for layer, xs in doc["nodes"].items() for x in xs}
        edges = {(e["from"], e["to"], False) for e in doc["edges"]}
    else:
        nodes = {(x["name"], x["type"]) for x in [*doc["up"], *doc["down"]]}
        drawn = {n for n in drawing.nodes() if n[0] == doc["node"]}
        assert len(drawn) == 1  # the starting node is drawn, in its own column
        nodes |= drawn
        edges = {(e["from"], e["to"], False) for e in doc["edges"]}
    return nodes, edges, set(drawing.nodes()), set(drawing.edges())


@pytest.mark.parametrize("name,args,view", CALLS)
def test_both_is_the_plot_then_a_table_that_agrees(vault, name, args, view):  # WP33-R2
    res = run_tool(vault, name, {**args, "output": "both"})
    assert not res.isError
    plot, table = res.content
    assert plot.type == "image" and plot.mimeType == "image/png"
    assert base64.b64decode(plot.data).startswith(PNG)
    assert table.type == "text"
    doc = json.loads(table.text)
    assert (
        doc == run_tool(vault, name, args).structuredContent
    )  # the table is the table output's document
    local = {
        "fingerprint": scat_tools.fingerprint,
        "layered": scat_tools.layered,
        "trace": scat_tools.trace,
    }
    drawing = draw.render(local[view](**_local_args(name, args), root=vault))
    assert base64.b64decode(plot.data) == drawing.png()
    t_nodes, t_edges, d_nodes, d_edges = table_of(doc, drawing)
    assert t_nodes == d_nodes and t_edges == d_edges and d_nodes and d_edges


def _local_args(name, args):
    if name == "fingerprint":
        return {"narrative": args["narrative"], "candidates": args.get("candidates", False)}
    if name == "layered":
        return {"narratives": args.get("narratives")}
    return {"node": args["node"], "direction": args.get("direction", "both")}


def test_the_agreement_check_fails_when_the_table_and_the_plot_differ(vault):
    doc = run_tool(vault, "layered", {}).structuredContent
    drawing = draw.render(scat_tools.layered(root=vault))
    t_nodes, t_edges, d_nodes, d_edges = table_of(doc, drawing)
    assert (t_nodes, t_edges) == (d_nodes, d_edges)
    doc["edges"] = doc["edges"][1:]
    t_nodes, t_edges, d_nodes, d_edges = table_of(doc, drawing)
    assert t_edges != d_edges


@pytest.mark.parametrize("name,args,view", CALLS)
def test_table_is_the_document_and_only_it(vault, name, args, view):  # WP33-R3
    local = {
        "fingerprint": scat_tools.fingerprint,
        "layered": scat_tools.layered,
        "trace": scat_tools.trace,
    }
    doc = stamp(local[view](**_local_args(name, args), root=vault), vault).to_dict()
    for extra in ({}, {"output": "table"}, {"output": "table", "format": "svg"}):
        res = run_tool(vault, name, {**args, **extra})
        assert not res.isError
        assert [c.type for c in res.content] == ["text"]
        assert res.structuredContent == doc
        assert json.loads(res.content[0].text) == doc


@pytest.mark.parametrize("name,args,view", CALLS)
def test_plot_is_only_the_picture(vault, name, args, view):  # WP33-R3
    res = run_tool(vault, name, {**args, "output": "plot"})
    assert [c.type for c in res.content] == ["image"] and res.structuredContent is None
    res = run_tool(vault, name, {**args, "output": "plot", "format": "svg"})
    assert [c.type for c in res.content] == ["text"] and res.structuredContent is None
    assert res.content[0].text.lstrip().startswith(("<?xml", "<svg"))
    both = run_tool(vault, name, {**args, "output": "both", "format": "svg"}).content
    assert [c.type for c in both] == ["text", "text"] and both[0].text == res.content[0].text
    assert json.loads(both[1].text)["operation"] == view


def test_a_plot_of_no_narrative_is_the_refusal_not_an_image(vault):
    for output in ("plot", "both"):
        res = run_tool(vault, "fingerprint", {"output": output})
        assert [c.type for c in res.content] == ["text"]
        doc = json.loads(res.content[0].text)
        assert doc["ok"] is False and doc["refused"]
    table = run_tool(vault, "fingerprint", {})  # as a table it is every narrative's view, as before
    assert table.structuredContent["ok"] is True and len(table.structuredContent["narratives"]) > 1


def test_a_missing_matplotlib_is_the_refusal_document(vault, monkeypatch):
    monkeypatch.setitem(sys.modules, "matplotlib", None)
    monkeypatch.setitem(sys.modules, "matplotlib.pyplot", None)
    for output in ("plot", "both"):
        res = run_tool(vault, "layered", {"output": output})
        assert [c.type for c in res.content] == ["text"]
        assert json.loads(res.content[0].text)["ok"] is False
    assert run_tool(vault, "layered", {}).structuredContent["ok"] is True
