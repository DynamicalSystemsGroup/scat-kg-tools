"""RS5-U3 experiments E1 to E8. Test names start with the experiment id; NOTES.md headings use the same ids."""

from __future__ import annotations

import asyncio
import inspect
import json
import logging
import tempfile
from importlib.metadata import version

import pytest
from livehttp import LiveServer, connect, text
from mcp import ClientSession
from mcp.shared.memory import create_connected_server_and_client_session
from mcp.types import ElicitResult, PaginatedRequestParams
from stage_server import ALWAYS, CARRIERS, STAGES, build, scope

logging.disable(logging.CRITICAL)
SET = {"stage": None, "coder_word": "the coder said so"}


def run(coro):
    return asyncio.run(asyncio.wait_for(coro, 60))


def names(res) -> set[str]:
    return {t.name for t in res.tools}


def doc(res) -> dict:
    return json.loads(text(res))


async def settle():
    await asyncio.sleep(0.3)


def test_sdk_version():
    assert version("mcp") == "1.30.0"
    print("mcp", version("mcp"))


# ---------------------------------------------------------------- E1 header, query, path
def test_e1_header_per_connection():
    async def go(url):
        async with connect(url, headers={"X-Scat-Stage": "plan"}) as (s, _):
            assert doc(await s.call_tool("which_stage", {})) == {
                "stage": "plan",
                "carrier": "header",
                "raw": "plan",
            }
            assert "stub" in names(await s.list_tools()) and "record_edge" not in names(
                await s.list_tools()
            )

    with LiveServer(build(("header",))) as srv:
        run(go(srv.url))


def test_e1_header_per_request_needs_httpx_event_hook():
    cur = {"v": "plan"}

    async def hook(request):
        request.headers["x-scat-stage"] = cur["v"]

    async def go(url):
        async with connect(url, hooks=[hook]) as (s, _):
            seen = []
            for stage in ["plan", "code", "analyse"]:
                cur["v"] = stage  # same MCP session, header changes between requests
                seen.append(doc(await s.call_tool("which_stage", {}))["stage"])
            assert seen == ["plan", "code", "analyse"]
            assert "record_edge" not in names(await s.list_tools())  # analyse list

    with LiveServer(build(("header",))) as srv:
        run(go(srv.url))


def test_e1_sdk_call_tool_has_no_per_request_header_parameter():
    params = set(inspect.signature(ClientSession.call_tool).parameters)
    assert not params & {"headers", "header", "extra_headers"}
    print("call_tool parameters:", sorted(params))


def test_e1_query_parameter():
    async def go(url):
        async with connect(url + "?stage=code") as (s, _):
            assert doc(await s.call_tool("which_stage", {}))["carrier"] == "query"
            assert "record_edge" in names(await s.list_tools())

    with LiveServer(build(("query",))) as srv:
        run(go(srv.url))


def test_e1_path_variant():
    async def go(url):
        async with connect(url + "/analyse") as (s, _):
            assert doc(await s.call_tool("which_stage", {})) == {
                "stage": "analyse",
                "carrier": "path",
                "raw": "analyse",
            }
            assert "trace" in names(await s.list_tools())

    with LiveServer(build(("path",))) as srv:
        run(go(srv.url))


# ---------------------------------------------------------------- E2 session value
def test_e2_session_value_stateful():
    async def go(url):
        async with connect(url) as (s, _):
            assert doc(await s.call_tool("which_stage", {}))["stage"] is None
            r = doc(
                await s.call_tool("set_stage", {"stage": "code"})
            )  # no coder word: request only
            assert r["moved"] is False
            assert doc(await s.call_tool("which_stage", {}))["stage"] is None
            await s.call_tool("set_stage", {"stage": "code", "coder_word": "go"})
            assert doc(await s.call_tool("which_stage", {})) == {
                "stage": "code",
                "carrier": "session",
                "raw": "code",
            }

    with LiveServer(build(("session",))) as srv:
        run(go(srv.url))


def test_e2_session_value_lost_in_stateless_mode():
    async def go(url):
        async with connect(url) as (s, _):
            r = doc(await s.call_tool("set_stage", {"stage": "code", "coder_word": "go"}))
            assert r["moved"] is True  # the server says moved ...
            assert doc(await s.call_tool("which_stage", {}))["stage"] is None  # ... and forgets it
            assert names(await s.list_tools()) == set(ALWAYS)

    with LiveServer(build(("session",), stateless=True)) as srv:
        run(go(srv.url))


def test_e2_session_value_lost_when_server_restarts():
    async def go():
        srv = LiveServer(build(("session",)))
        srv.__enter__()
        port, url = srv.port, srv.url
        async with connect(url) as (s, _):
            await s.call_tool("set_stage", {"stage": "code", "coder_word": "go"})
            srv.__exit__()
            srv2 = LiveServer(build(("session",)), port)  # same address, new process state
            srv2.__enter__()
            try:
                with pytest.raises(
                    Exception, match="Session terminated"
                ):  # McpError: old session id unknown
                    await s.call_tool("which_stage", {})
            finally:
                srv2.__exit__()
        with LiveServer(
            build(("session",)), port
        ) as srv3:  # a fresh session starts with stage unknown
            async with connect(srv3.url) as (s2, _):
                assert doc(await s2.call_tool("which_stage", {}))["stage"] is None

    run(go())


# ---------------------------------------------------------------- E3 argument
def test_e3_argument_on_each_call_and_omitted():
    async def go(url):
        async with connect(url) as (s, _):
            ok = await s.call_tool("check", {"stage": "plan"})
            assert not ok.isError and doc(ok)["tool"] == "check"
            omitted = await s.call_tool("check", {})
            assert omitted.structuredContent["refused"] is True and omitted.isError is False
            assert "plan" in text(omitted) and "coder" in text(omitted)
            bad = await s.call_tool("check", {"stage": "nope"})
            assert bad.structuredContent["value_received"] == "nope"

    with LiveServer(build(("argument",), stage_argument=True)) as srv:
        run(go(srv.url))


def test_e3_argument_schema_cost():
    async def sizes(url_kw):
        with LiveServer(build(("argument",), **url_kw)) as srv:
            async with connect(srv.url, headers={}) as (s, _):
                tools = (await s.call_tool("which_stage", {}), (await s.list_tools()).tools)[1]
                return len(
                    json.dumps([t.model_dump(by_alias=True, exclude_none=True) for t in tools])
                )

    async def go():
        base = await sizes({"scoped_list": False})
        arg = await sizes({"scoped_list": False, "stage_argument": True})
        print("tools/list bytes without stage argument:", base, "with:", arg, "extra:", arg - base)
        assert arg > base

    run(go())


# ---------------------------------------------------------------- E4 _meta
def test_e4_meta_on_call_tool():
    async def go(url):
        async with connect(url) as (s, _):
            r = await s.call_tool("which_stage", {}, meta={"scat-stage": "code"})
            assert doc(r) == {"stage": "code", "carrier": "meta", "raw": "code"}
            assert (
                doc(await s.call_tool("which_stage", {}))["stage"] is None
            )  # per request, not remembered

    with LiveServer(build(("meta",))) as srv:
        run(go(srv.url))


def test_e4_meta_on_list_tools_and_in_memory():
    async def go(url):
        async with connect(url) as (s, _):
            p = PaginatedRequestParams(_meta={"scat-stage": "analyse"})
            assert "trace" in names(await s.list_tools(params=p))
            assert "trace" not in names(await s.list_tools())  # no meta: unknown stage
        async with create_connected_server_and_client_session(
            build(("meta",))
        ) as m:  # in-memory transport
            assert (
                doc(await m.call_tool("which_stage", {}, meta={"scat-stage": "plan"}))["carrier"]
                == "meta"
            )

    with LiveServer(build(("meta",))) as srv:
        run(go(srv.url))


# ---------------------------------------------------------------- E5 unknown stage
def check_clarification(res, *, is_error: bool):
    assert res.isError is is_error
    d = res.structuredContent
    assert d["refused"] is True
    assert set(d["known_stages"]) == set(STAGES)
    assert all(STAGES[s]["about"] in d["known_stages"][s] for s in STAGES)
    assert "coder decides" in d["who_decides"]
    assert "coder" in text(res) and all(s in text(res) for s in STAGES)


@pytest.mark.parametrize("is_error", [False, True])
def test_e5_unknown_stage_returns_result_not_protocol_error(is_error):
    async def go(url):
        async with connect(url) as (s, _):  # no header at all
            check_clarification(
                await s.call_tool("check", {}), is_error=is_error
            )  # no exception raised
        async with connect(url, headers={"X-Scat-Stage": "bogus"}) as (s, _):
            res = await s.call_tool("check", {})
            check_clarification(res, is_error=is_error)
            assert res.structuredContent["value_received"] == "bogus"
            assert names(await s.list_tools()) == set(ALWAYS)

    with LiveServer(build(("header",), is_error=is_error)) as srv:
        run(go(srv.url))


def test_e5_elicitation_needs_client_callback():
    asked = []

    async def cb(ctx, params):
        asked.append(params.message)
        return ElicitResult(action="accept", content={"stage": "code"})

    async def go(url):
        async with connect(url, elicitation_callback=cb) as (s, _):
            d = doc(await s.call_tool("ask_stage", {}))
            assert d == {"elicited": True, "action": "accept", "content": {"stage": "code"}}
        async with connect(url) as (s, _):  # a client with no callback declares no elicitation
            d = doc(await s.call_tool("ask_stage", {}))
            assert d["elicited"] is False
        assert len(asked) == 1

    with LiveServer(build(("header",))) as srv:
        run(go(srv.url))


# ---------------------------------------------------------------- E6 out-of-stage call
def test_e6_out_of_stage_call_refused_with_where_and_how():
    async def go(url):
        async with connect(url, headers={"X-Scat-Stage": "plan"}) as (s, _):
            listed = names(await s.list_tools())
            assert "record_edge" not in listed
            res = await s.call_tool("record_edge", {})  # a client that never refreshed its list
            d = res.structuredContent
            assert res.isError is False and d["refused"] is True and d["tool"] == "record_edge"
            assert (
                "`record_edge`" in d["problem"]
                and "`plan`" in d["problem"]
                and "code" in d["problem"]
            )
            assert "set_stage" in d["how_to_move"] and "coder" in d["who_decides"]
            assert (
                (await s.call_tool("export_edges", {}))
                .structuredContent["problem"]
                .endswith("analyse.")
            )

    with LiveServer(build(("header",))) as srv:
        run(go(srv.url))


# ---------------------------------------------------------------- E7 list-changed and scoped lists
def test_e7_capabilities_advertise_list_changed_only_when_configured():
    async def go(url_on, url_off):
        async with connect(url_on) as (_, init):
            c = init.capabilities
            assert (c.tools.listChanged, c.prompts.listChanged, c.resources.listChanged) == (
                True,
                True,
                True,
            )
        async with connect(url_off) as (_, init):
            assert init.capabilities.tools.listChanged is False  # FastMCP default

    with LiveServer(build()) as on, LiveServer(build(list_changed=False)) as off:
        run(go(on.url, off.url))


def test_e7_tools_prompts_resources_scoped_per_stage_and_unscoped_default():
    async def lists(s):
        return (
            names(await s.list_tools()),
            {p.name for p in (await s.list_prompts()).prompts},
            {str(r.uri) for r in (await s.list_resources()).resources},
        )

    async def go(url, url_all):
        async with connect(url, headers={"X-Scat-Stage": "plan"}) as (s, _):
            t, p, r = await lists(s)
            assert t == set(STAGES["plan"]["tools"]) | set(ALWAYS)
            assert p == {"plan_guide"} and r == {"scat://glossary", "scat://plan-notes"}
        async with connect(url, headers={"X-Scat-Stage": "analyse"}) as (s, _):
            t, p, r = await lists(s)
            assert t == set(STAGES["analyse"]["tools"]) | set(ALWAYS) and p == {"analyse_guide"}
            assert r == {"scat://glossary"}
        async with connect(url_all, headers={"X-Scat-Stage": "plan"}) as (
            s,
            _,
        ):  # FastMCP default: global
            assert (
                len(names(await s.list_tools())) == 12
                and len((await s.list_prompts()).prompts) == 3
            )

    with (
        LiveServer(build(("header",))) as a,
        LiveServer(build(("header",), scoped_list=False)) as b,
    ):
        run(go(a.url, b.url))


def test_e7_set_stage_notifies_that_session_only_and_relist_shows_new_tools():
    async def go(url):
        got_a, got_b = [], []

        async def ha(m):
            got_a.append(getattr(m, "root", m).method if hasattr(m, "root") else None)

        async def hb(m):
            got_b.append(getattr(m, "root", m).method if hasattr(m, "root") else None)

        async with (
            connect(url, message_handler=ha) as (a, _),
            connect(url, message_handler=hb) as (b, _),
        ):
            assert names(await a.list_tools()) == set(ALWAYS)
            await a.call_tool("set_stage", {"stage": "code", "coder_word": "go"})
            await settle()
            assert sorted(got_a) == [
                "notifications/prompts/list_changed",
                "notifications/resources/list_changed",
                "notifications/tools/list_changed",
            ]
            assert got_b == []  # session B heard nothing
            assert "record_edge" in names(await a.list_tools())
            assert names(await b.list_tools()) == set(ALWAYS)

    with LiveServer(build(("session",))) as srv:
        run(go(srv.url))


def test_e7_concurrent_sessions_see_different_lists():
    async def go(url):
        async with connect(url) as (a, _), connect(url) as (b, _):
            await a.call_tool("set_stage", {"stage": "code", "coder_word": "go"})
            await b.call_tool("set_stage", {"stage": "analyse", "coder_word": "go"})
            ta, tb = names(await a.list_tools()), names(await b.list_tools())
            assert "record_edge" in ta and "record_edge" not in tb
            assert "trace" in tb and "trace" not in ta

    with LiveServer(build(("session",))) as srv:
        run(go(srv.url))


def test_e7_client_that_ignores_notification_hits_the_refusal():
    async def go(url):
        async with connect(url) as (s, _):  # default message handler: ignores list_changed
            await s.call_tool("set_stage", {"stage": "code", "coder_word": "go"})
            listed = names(await s.list_tools())  # the list a non-refreshing client keeps
            assert "record_edge" in listed
            assert doc(await s.call_tool("record_edge", {}))["ok"] is True
            await s.call_tool("set_stage", {"stage": "analyse", "coder_word": "go"})
            res = await s.call_tool("record_edge", {})  # listed a moment ago at stage code, not now
            assert (
                res.structuredContent["refused"] is True
                and "`analyse`" in res.structuredContent["problem"]
            )

    with LiveServer(build(("session",))) as srv:
        run(go(srv.url))


def test_e7_in_memory_transport_same_behaviour():
    async def go():
        got = []

        async def h(m):
            got.append(m)

        async with create_connected_server_and_client_session(
            build(("session",)), message_handler=h
        ) as s:
            await s.call_tool("set_stage", {"stage": "plan", "coder_word": "go"})
            await settle()
            assert any("ToolListChanged" in type(getattr(m, "root", m)).__name__ for m in got)
            assert names(await s.list_tools()) >= {"stub", "set_stage"} and "trace" not in names(
                await s.list_tools()
            )

    run(go())


def test_e7_stateless_mode_cannot_scope_by_session():
    async def go(url):
        got = []

        async def h(m):
            got.append(m)

        async with connect(url, message_handler=h) as (s, _):
            await s.call_tool("set_stage", {"stage": "code", "coder_word": "go"})
            await settle()
            assert names(await s.list_tools()) == set(ALWAYS)  # nothing remembered
            print("notifications received in stateless mode:", len(got))

    with LiveServer(build(("session",), stateless=True)) as srv:
        run(go(srv.url))


# ---------------------------------------------------------------- E8 cost
def test_e8_carrier_cost_in_lines():
    cost = {n: len(inspect.getsource(f).strip().splitlines()) for n, f in CARRIERS.items()}
    print("lines per carrier function:", cost)
    assert max(cost.values()) <= 5
    import stage_server

    src = inspect.getsource(stage_server).splitlines()
    print("stage_server.py lines:", len(src))


def test_e8_real_server_tools_can_be_scoped_by_data_only():
    from scat_kg.mcp_server import server as real

    with tempfile.TemporaryDirectory() as d:
        mcp = real.build(d)
        real_names = [t.name for t in run(mcp.list_tools())]
    assert len(real_names) == 19
    # a placeholder table over the real names: data only, no code change
    table = {
        "plan": ["status", "check", "stub", "stub_links", "index", "review"],
        "code": [
            "status",
            "check",
            "stub",
            "stub_links",
            "record_edge",
            "remove_edge",
            "set_status",
            "merge",
            "split_plan",
        ],
        "analyse": [
            n
            for n in real_names
            if n
            not in (
                "record_edge",
                "remove_edge",
                "set_status",
                "stub",
                "stub_links",
                "index",
                "merge",
                "split_plan",
            )
        ],
    }
    covered = {n for ns in table.values() for n in ns}
    assert covered == set(real_names)  # every real tool lands in at least one stage
    import stage_server

    saved = dict(stage_server.STAGES)
    try:
        stage_server.STAGES.clear()
        stage_server.STAGES.update(
            {s: {"tools": ns, "prompts": [], "resources": []} for s, ns in table.items()}
        )
        for s, ns in table.items():
            assert set(scope(real_names, s)) == set(ns)
    finally:
        stage_server.STAGES.clear()
        stage_server.STAGES.update(saved)
