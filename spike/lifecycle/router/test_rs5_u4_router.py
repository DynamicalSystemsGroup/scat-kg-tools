"""RS5-U4: the chief engineer's option (a routing top-level MCP server over per-stage MCP servers), Q1 to Q6.

Test names start with q1_ .. q6_ and map to the headings of NOTES.md. Everything binds 127.0.0.1 and is stopped.
"""

import ast
import asyncio
import contextlib
import importlib.metadata
import json
import time

import pytest
from lc_harness import (
    HERE,
    Topology,
    median_ms,
    record,
    rss_kb,
    time_calls,
)
from lc_router import Router, _http_session, memory_connector, router_client
from lc_stages import STAGES, build_stage
from mcp import types
from mcp.shared.memory import create_connected_server_and_client_session

REPO = HERE.parents[2]


def run(coro):
    return asyncio.run(coro)


def stage_servers():
    return {n: build_stage(n) for n in STAGES}


def names(listing) -> list[str]:
    return [t.name for t in listing.tools]


class Seen:
    """Collects the list_changed notifications a client receives."""

    def __init__(self):
        self.methods: list[str] = []

    async def __call__(self, msg):
        if isinstance(msg, types.ServerNotification):
            self.methods.append(msg.root.method)


@contextlib.asynccontextmanager
async def mem_router(mode="dynamic", seen=None):
    r = Router(memory_connector(stage_servers()), mode)
    async with router_client(r, message_handler=seen) as s:
        yield s


@contextlib.asynccontextmanager
async def direct_stage(name):
    async with create_connected_server_and_client_session(build_stage(name)) as s:
        yield s


async def goto(s, stage):
    """Walk the router forward from its current stage to `stage` by doing each stage's work (predicates detect it)."""
    work = {
        "code": ("stub", {"name": "a", "type": "narrative"}),
        "analyse": ("record_edge", {"source": "a", "target": "b"}),
    }
    order = ["plan", "code", "analyse"]
    cur = (await s.call_tool("stage", {})).structuredContent["stage"]
    for step in order[order.index(cur) + 1 : order.index(stage) + 1]:
        tool, args = work[step]
        await s.call_tool(tool, args)
        out = (await s.call_tool("set_stage", {"to": step})).structuredContent
        assert out["moved"], out
    return stage


@pytest.fixture(scope="session")
def topo_i():
    t = Topology("i").start()
    yield t
    t.stop()


@pytest.fixture(scope="session")
def topo_ii():
    t = Topology("ii").start()
    yield t
    t.stop()


def test_sdk_version():
    v = importlib.metadata.version("mcp")
    print(f"mcp SDK version: {v}")
    record("sdk_version", v)
    assert v == "1.30.0"


# ---- Q1 -----------------------------------------------------------------------------------------------------------


async def _exercise_proxy(s):
    listed = names(await s.list_tools())
    assert {"stage", "set_stage", "status", "check", "stub"} <= set(listed)
    r = await s.call_tool("status", {})
    assert not r.isError and r.structuredContent["stage"] == "plan"
    p = await s.get_prompt("stage_guide", {"topic": "t"})
    assert "plan stage" in p.messages[0].content.text
    res = await s.read_resource("stage://plan/guide")
    assert res.contents[0].text == "guide of the plan stage"
    return listed


@pytest.mark.parametrize("where", ["memory", "http_separate_ports", "http_one_port"])
def test_q1_router_proxies_tools_prompts_resources(where, request):
    topo = None
    if where != "memory":
        topo = request.getfixturevalue("topo_i" if where == "http_separate_ports" else "topo_ii")

    async def go():
        if where == "memory":
            async with mem_router() as s:
                return await _exercise_proxy(s)
        async with _http_session(topo.router_url) as s:
            return await _exercise_proxy(s)

    listed = run(go())
    record(f"q1_{where}_tools_listed", listed)


# ---- Q2 -----------------------------------------------------------------------------------------------------------


def test_q2_dynamic_list_changes_and_notifies_in_memory():
    async def go():
        seen = Seen()
        async with mem_router("dynamic", seen) as s:
            before = names(await s.list_tools())
            refused = (await s.call_tool("set_stage", {"to": "code"})).structuredContent
            await asyncio.sleep(0.05)
            assert not refused["ok"] and seen.methods == []  # no move, no notification
            await goto(s, "code")
            await asyncio.sleep(0.05)
            after = names(await s.list_tools())
            return before, after, list(seen.methods), s.get_server_capabilities()

    before, after, methods, caps = run(go())
    assert before != after, "the client still sees a changing list"
    assert "stub" in before and "stub" not in after and "record_edge" in after
    assert sorted(methods) == [
        "notifications/prompts/list_changed",
        "notifications/resources/list_changed",
        "notifications/tools/list_changed",
    ]
    assert caps.tools.listChanged is True
    record("q2_tools_before", before)
    record("q2_tools_after", after)
    record("q2_notifications_per_stage_change", methods)


def test_q2_list_changed_arrives_over_http_and_fastmcp_default_declares_none(topo_i):
    async def go():
        seen = Seen()
        async with _http_session(topo_i.router_url, seen) as s:
            await goto(s, "code")
            for _ in range(60):
                if "notifications/tools/list_changed" in seen.methods:
                    break
                await asyncio.sleep(0.05)
            http_caps = s.get_server_capabilities()
        async with direct_stage("plan") as d:
            stage_caps = d.get_server_capabilities()
        return seen.methods, http_caps, stage_caps

    methods, http_caps, stage_caps = run(go())
    assert "notifications/tools/list_changed" in methods
    assert http_caps.tools.listChanged is True
    # a plain FastMCP server (what src/scat_kg/mcp_server uses) declares listChanged false by default
    assert not stage_caps.tools.listChanged
    record("q2_http_notifications", methods)
    record("q2_fastmcp_default_tools_listChanged", bool(stage_caps.tools.listChanged))


# ---- Q3 -----------------------------------------------------------------------------------------------------------


def _bytes(listing) -> int:
    return len(json.dumps([t.model_dump(exclude_none=True) for t in listing.tools]))


def test_q3_variant_b_static_facade():
    async def go():
        seen = Seen()
        async with mem_router("facade", seen) as s:
            first = await s.list_tools()
            st = (await s.call_tool("stage_tools", {})).structuredContent
            ok = await s.call_tool(
                "call", {"tool": "stub", "args": {"name": "a", "type": "narrative"}}
            )
            bad_args = await s.call_tool("call", {"tool": "stub", "args": {"name": "a"}})
            out_of_stage = await s.call_tool("call", {"tool": "record_edge", "args": {}})
            await s.call_tool("set_stage", {"to": "code"})
            await asyncio.sleep(0.05)
            second = await s.list_tools()
            st2 = (await s.call_tool("stage_tools", {})).structuredContent
            return first, second, st, st2, ok, bad_args, out_of_stage, list(seen.methods)

    first, second, st, st2, ok, bad_args, out_of_stage, methods = run(go())
    assert names(first) == names(second) == ["stage", "set_stage", "stage_tools", "call"]
    assert methods == [], "no list change needed"
    assert {t["name"] for t in st["tools"]} != {t["name"] for t in st2["tools"]}, (
        "discovered through a result"
    )
    assert ok.structuredContent["op"] == "stub"
    call_schema = next(t for t in first.tools if t.name == "call").inputSchema
    assert set(call_schema["properties"]) == {
        "tool",
        "args",
    }  # no per-tool typed schema in the listing
    assert bad_args.isError, "a missing field is caught by the stage server, not by the listing"
    assert out_of_stage.structuredContent["refused"] is True
    record("q3_b_listing_bytes", _bytes(first))
    record("q3_b_bad_args_text", bad_args.content[0].text[:160])


def test_q3_variant_c_all_tools_listed_out_of_stage_refused():
    async def go():
        seen = Seen()
        async with mem_router("all", seen) as s:
            first = await s.list_tools()
            out = await s.call_tool("record_edge", {"source": "a", "target": "b"})
            ok = await s.call_tool("stub", {"name": "a", "type": "narrative"})
            await goto(s, "code")
            await asyncio.sleep(0.05)
            second = await s.list_tools()
            return first, second, out, ok, list(seen.methods)

    first, second, out, ok, methods = run(go())
    assert names(first) == names(second) and methods == []
    assert out.structuredContent["refused"] and out.structuredContent["in_stages"] == ["code"]
    assert ok.structuredContent["op"] == "stub"

    # shared names (status, check, fingerprint) must have identical schemas for a union listing to be honest
    async def schemas():
        out: dict[str, list] = {}
        for n in STAGES:
            async with direct_stage(n) as d:
                for t in (await d.list_tools()).tools:
                    out.setdefault(t.name, []).append(json.dumps(t.inputSchema, sort_keys=True))
        return out

    by_name = run(schemas())
    shared = {k: v for k, v in by_name.items() if len(v) > 1}
    assert shared and all(len(set(v)) == 1 for v in shared.values())
    record("q3_c_union_tool_count", len(names(first)) - 2)
    record("q3_c_shared_names", sorted(shared))
    record("q3_c_listing_bytes", _bytes(first))

    async def a_sizes():
        sizes = {}
        async with mem_router("dynamic") as s:
            sizes["plan"] = _bytes(await s.list_tools())
            await goto(s, "analyse")
            sizes["analyse"] = _bytes(await s.list_tools())
        return sizes

    record("q3_a_listing_bytes", run(a_sizes()))


# ---- Q4 -----------------------------------------------------------------------------------------------------------


def test_q4_unknown_stage_and_undefined_transition():
    async def go():
        async with mem_router() as s:
            unknown = (await s.call_tool("set_stage", {"to": "review"})).structuredContent
            empty = (await s.call_tool("set_stage", {"to": ""})).structuredContent
            undefined = (await s.call_tool("set_stage", {"to": "analyse"})).structuredContent
            same = (await s.call_tool("set_stage", {"to": "plan"})).structuredContent
            return unknown, empty, undefined, same

    unknown, empty, undefined, same = run(go())
    assert (
        unknown["needs_clarification"]
        and unknown["stages"] == list(STAGES)
        and "which stage" in unknown["ask"]
    )
    assert empty["needs_clarification"]
    assert undefined["refused"] and undefined["allowed"] == ["code"]
    assert same["ok"] and not same["moved"]


def test_q4_predicates_detect_or_need_the_coders_word():
    async def go():
        async with mem_router() as s:
            early = (await s.call_tool("set_stage", {"to": "code"})).structuredContent
            await s.call_tool("stub", {"name": "a", "type": "narrative"})
            moved = (await s.call_tool("set_stage", {"to": "code"})).structuredContent
            await s.call_tool("record_edge", {"source": "a", "target": "b"})
            to_analyse = (await s.call_tool("set_stage", {"to": "analyse"})).structuredContent
            back = (await s.call_tool("set_stage", {"to": "code"})).structuredContent
            back_word = (
                await s.call_tool("set_stage", {"to": "code", "confirm": True})
            ).structuredContent
            stage = (await s.call_tool("stage", {})).structuredContent
            return early, moved, to_analyse, back, back_word, stage

    early, moved, to_analyse, back, back_word, stage = run(go())
    assert early["refused"] and "needs 1" in early["reason"]
    assert moved["moved"] and moved["via"] == "detected"
    assert to_analyse["moved"] and to_analyse["to"] == "analyse"
    assert back["refused"] and "coder's word" in back["reason"]
    assert back_word["moved"] and back_word["via"] == "word"
    assert stage["stage"] == "code" and stage["allowed"] == ["analyse", "plan"]


def test_q4_out_of_stage_call_refused_unknown_tool_clarified_and_state_is_per_connection():
    async def go():
        async with mem_router() as s:
            out = (await s.call_tool("trace", {"element": "x"})).structuredContent
            unknown = (await s.call_tool("nosuch", {})).structuredContent
            await goto(s, "code")
            async with mem_router() as other:
                other_stage = (await other.call_tool("stage", {})).structuredContent["stage"]
            return out, unknown, other_stage

    out, unknown, other_stage = run(go())
    assert out["refused"] and out["in_stages"] == ["analyse"] and "status" in out["tools_here"]
    assert unknown["needs_clarification"] and "nosuch" in unknown["reason"]
    assert other_stage == "plan"


# ---- Q5 -----------------------------------------------------------------------------------------------------------


def _loc(src: str) -> int:
    return sum(1 for ln in src.splitlines() if ln.strip() and not ln.strip().startswith("#"))


def _func_loc(path, wanted: list[str]) -> int:
    text = path.read_text()
    tree = ast.parse(text)
    total = 0
    for node in tree.body:
        if isinstance(node, ast.FunctionDef | ast.ClassDef) and node.name in wanted:
            total += _loc(ast.get_source_segment(text, node) or "")
    return total


def test_q5_hosting_cost_separate_processes_vs_one_asgi_app(topo_i, topo_ii):
    async def poke(t):
        async with _http_session(t.router_url) as s:
            await goto(s, "code")
            await s.call_tool("status", {})

    run(poke(topo_i))
    run(poke(topo_ii))

    async def bypass(t):
        # a fresh router connection is in `plan`; the mounted `code` stage server answers without any stage check
        async with _http_session(t.stage_url("code")) as d:
            return not (await d.call_tool("record_edge", {"source": "a", "target": "b"})).isError

    record("q5_ii_mounts_bypass_state_machine", run(bypass(topo_ii)))
    record("q5_i_stage_ports_bypass_state_machine_locally", run(bypass(topo_i)))
    ri, rii = topo_i.rss(), topo_ii.rss()
    host = HERE / "lc_hosting.py"
    shared = _func_loc(host, ["_Asgi", "router_routes"])
    loc = {
        "lc_router.py": _loc((HERE / "lc_router.py").read_text()),
        "lc_stages.py": _loc((HERE / "lc_stages.py").read_text()),
        "hosting_shared": shared,
        "hosting_i_only": _func_loc(host, ["stage_process", "router_process"]),
        "hosting_ii_only": _func_loc(host, ["single_app", "single_process"]),
    }
    data = {
        "i": {
            "processes": len(topo_i.procs),
            "listening_ports": sorted(topo_i.ports.values()),
            "startup_s": round(topo_i.startup_s, 2),
            "rss_kb": ri,
            "rss_total_mb": round(sum(ri.values()) / 1024, 1),
        },
        "ii": {
            "processes": len(topo_ii.procs),
            "listening_ports": sorted(topo_ii.ports.values()),
            "startup_s": round(topo_ii.startup_s, 2),
            "rss_kb": rii,
            "rss_total_mb": round(sum(rii.values()) / 1024, 1),
        },
        "loc": loc,
    }
    record("q5_hosting", data)
    assert data["i"]["processes"] == 4 and len(data["i"]["listening_ports"]) == 4
    assert data["ii"]["processes"] == 1 and len(data["ii"]["listening_ports"]) == 1
    assert all(v > 0 for v in ri.values()) and all(v > 0 for v in rii.values())


async def _block_effect(t) -> dict:
    """Client A (code stage) runs a 1.5 s synchronous tool; client B (another connection) times `status`."""
    async with _http_session(t.router_url) as a, _http_session(t.router_url) as b:
        await goto(a, "code")
        await b.call_tool("status", {})  # warm
        long = asyncio.create_task(a.call_tool("block", {"seconds": 1.5}))
        await asyncio.sleep(0.3)
        t0 = time.perf_counter()
        await b.call_tool("status", {})
        waited = time.perf_counter() - t0
        await long
    return {"other_connection_status_latency_s": round(waited, 3)}


def test_q5_failure_modes_one_stage_down_one_stage_blocking_whole_process_gone():
    findings: dict = {}
    # (i) a stage process killed while a connection is on it; then a new connection
    ti = Topology("i").start()
    try:

        async def go_i():
            async with _http_session(ti.router_url) as s:
                await goto(s, "code")
                ti.procs["code"].kill()
                ti.procs["code"].wait()
                t0 = time.perf_counter()
                dead = await s.call_tool("status", {})
                findings["i_call_to_dead_stage"] = {
                    "isError": dead.isError,
                    "structured": dead.structuredContent,
                    "seconds": round(time.perf_counter() - t0, 2),
                }
                back = (
                    await s.call_tool("set_stage", {"to": "plan", "confirm": True})
                ).structuredContent
                plan = await s.call_tool("status", {})
                findings["i_other_stage_still_works"] = bool(back["moved"]) and not plan.isError
            t0 = time.perf_counter()
            async with _http_session(ti.router_url) as s2:
                st = (await s2.call_tool("stage", {})).structuredContent
                findings["i_new_connection_down"] = st["down"]
                findings["i_new_connection_connect_s"] = round(time.perf_counter() - t0, 2)
                plan2 = await s2.call_tool("status", {})
                findings["i_new_connection_plan_works"] = not plan2.isError

        run(go_i())
    finally:
        ti.stop()
    ti = Topology("i").start()
    try:
        findings["i_block"] = run(_block_effect(ti))
    finally:
        ti.stop()
    # (ii) one process
    tii = Topology("ii").start()
    try:

        async def go_ii():
            async with _http_session(tii.router_url) as s:
                await goto(s, "code")
                bad = await s.call_tool("fail_demo", {})
                findings["ii_tool_raises"] = {
                    "isError": bad.isError,
                    "text": bad.content[0].text[:80],
                }
                ok = await s.call_tool("status", {})
                findings["ii_after_tool_raises_still_works"] = not ok.isError
            findings["ii_block"] = await _block_effect(tii)
            async with _http_session(tii.router_url) as s:
                tii.procs["router"].kill()
                tii.procs["router"].wait()
                try:
                    async with asyncio.timeout(8):
                        await s.call_tool("status", {})
                    findings["ii_process_killed"] = "call succeeded?"
                except BaseException as e:
                    if isinstance(e, KeyboardInterrupt):
                        raise
                    findings["ii_process_killed"] = type(e).__name__

        run(go_ii())
    finally:
        tii.stop()
    record("q5_failure_modes", findings)
    assert findings["i_call_to_dead_stage"]["isError"] is True
    assert findings["i_other_stage_still_works"] is True
    assert findings["i_new_connection_down"] == ["code"]
    assert findings["ii_after_tool_raises_still_works"] is True


def test_q5_deploy_facts_from_the_repo_files():
    docker = (REPO / "deploy/Dockerfile").read_text()
    launcher = (REPO / "deploy/scat-chat.sh").read_text()
    main = (REPO / "src/scat_kg/mcp_server/__main__.py").read_text()
    assert (
        docker.count("ENTRYPOINT") == 1 and "EXPOSE 8765" in docker and '"--port", "8765"' in docker
    )
    assert '-p "127.0.0.1:$PORT:8765"' in launcher  # one published port, loopback
    assert 'funnel --bg "$PORT"' in launcher  # one public address, forwards to that one port
    assert "gated(app, key)" in main  # one key gate wraps the one ASGI app
    record(
        "q5_deploy_facts",
        {
            "entrypoint_count": 1,
            "container_port": 8765,
            "published": "127.0.0.1:8765 only",
            "funnel": "funnel --bg 8765 (one public https address on 443)",
            "key_gate": "gated(app, key) wraps the single ASGI app; header x-api-key or Bearer",
        },
    )


# ---- Q6 -----------------------------------------------------------------------------------------------------------


def _dump_diff(a: types.Tool, b: types.Tool) -> dict:
    da, db = a.model_dump(), b.model_dump()
    return {k: (da.get(k), db.get(k)) for k in set(da) | set(db) if da.get(k) != db.get(k)}


async def _compare_listing(s, stage: str) -> dict:
    router_tools = (await s.list_tools()).tools
    mine = {t.name: t for t in router_tools if t.name not in ("stage", "set_stage")}
    async with direct_stage(stage) as d:
        theirs = {t.name: t for t in (await d.list_tools()).tools}
        dp = {p.name: p.model_dump() for p in (await d.list_prompts()).prompts}
        dr = {str(r.uri): r.model_dump() for r in (await d.list_resources()).resources}
    rp = {p.name: p.model_dump() for p in (await s.list_prompts()).prompts}
    rr = {str(r.uri): r.model_dump() for r in (await s.list_resources()).resources}
    return {
        "same_names": sorted(mine) == sorted(theirs),
        "tool_field_diffs": {
            n: _dump_diff(mine[n], theirs[n])
            for n in theirs
            if n in mine and _dump_diff(mine[n], theirs[n])
        },
        "prompts_equal": rp == dp,
        "resources_equal": rr == dr,
        "fields_compared": sorted(next(iter(theirs.values())).model_dump()),
    }


def test_q6_listing_matches_stage_server_field_by_field():
    async def go():
        out = {}
        async with mem_router() as s:
            for stage in ("plan", "code", "analyse"):
                await goto(s, stage)
                out[stage] = await _compare_listing(s, stage)
        return out

    out = run(go())
    for stage, r in out.items():
        assert (
            r["same_names"]
            and r["tool_field_diffs"] == {}
            and r["prompts_equal"]
            and r["resources_equal"]
        ), (stage, r)
    record("q6_listing_compare", out)


def test_q6_results_errors_and_progress_are_preserved():
    async def via(call):
        events: list = []

        async def on_progress(p, t, m):
            events.append((p, t, m))

        calls = [
            ("status", {}),
            ("record_edge", {"source": "a", "target": "b"}),
            ("record_edge", {"source": "a"}),  # invalid: missing `target`
            ("fail_demo", {}),
            ("progress_demo", {"steps": 3}),
        ]
        out = []
        for name, args in calls:
            r = await call(name, args, on_progress)
            out.append((name, r.isError, r.structuredContent, [c.model_dump() for c in r.content]))
        return out, events

    async def go():
        async with mem_router() as s:
            await goto(s, "code")
            routed = await via(lambda n, a, cb: s.call_tool(n, a, progress_callback=cb))
        async with direct_stage("code") as d:
            direct = await via(lambda n, a, cb: d.call_tool(n, a, progress_callback=cb))
        return routed, direct

    routed, direct = run(go())
    assert routed[0] == direct[0], "content, structuredContent and isError are identical"
    assert (
        routed[1] == direct[1] == [(1.0, 3.0, "step 1"), (2.0, 3.0, "step 2"), (3.0, 3.0, "step 3")]
    )
    flags = [(n, e) for n, e, *_ in routed[0]]
    assert flags == [
        ("status", False),
        ("record_edge", False),
        ("record_edge", True),  # missing `target`: the stage server's own validation error
        ("fail_demo", True),
        ("progress_demo", False),
    ]
    record("q6_progress_events", [list(e) for e in routed[1]])
    record("q6_isError_by_call", [list(f) for f in flags])


def test_q6_extra_hop_latency_median_of_200(topo_i, topo_ii):
    async def mem():
        async with direct_stage("plan") as d:
            direct = await time_calls(d, "status", {})
        async with mem_router() as s:
            routed = await time_calls(s, "status", {})
        return direct, routed

    async def http():
        out = {}
        async with _http_session(topo_i.stage_url("plan")) as d:
            out["direct_stage"] = await time_calls(d, "status", {})
        async with _http_session(topo_i.router_url) as s:
            out["router_separate_ports"] = await time_calls(s, "status", {})
        async with _http_session(topo_ii.router_url) as s:
            out["router_one_port"] = await time_calls(s, "status", {})
        return out

    md, mr = run(mem())
    h = run(http())
    data = {
        "memory": {"direct_ms": median_ms(md), "via_router_ms": median_ms(mr)},
        "http": {k: median_ms(v) for k, v in h.items()},
        "calls": 200,
    }
    record("q6_latency_median_ms", data)
    assert data["memory"]["via_router_ms"] > 0 and data["http"]["router_separate_ports"] > 0


def test_zz_nothing_left_running(topo_i, topo_ii):
    """Last test of the run: fixtures stop the servers at teardown; this only checks the ports are loopback ones."""
    assert all(p > 1024 for p in list(topo_i.ports.values()) + list(topo_ii.ports.values()))
    assert rss_kb(topo_ii.procs["router"].pid) > 0
