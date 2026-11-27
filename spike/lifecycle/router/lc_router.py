"""A throwaway router: one top-level MCP server that holds the stage state machine and proxies to per-stage servers.

It is an MCP client to each stage server (in-memory or streamable HTTP) and a low-level MCP server to the one client.
State (the current stage) and the upstream sessions live in the lifespan, so they are per client connection.
Modes: "dynamic" (A: lists only the current stage's tools, list_changed on a stage change), "facade" (B: a fixed set
of four tools, the real tools reached through `call`), "all" (C: lists every stage's tools, refuses out-of-stage calls).
"""

import asyncio
import base64
import contextlib
import functools
import json
from collections import Counter
from collections.abc import Awaitable, Callable
from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import dataclass, field
from typing import Any

from lc_stages import STAGES
from mcp import types
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.lowlevel.helper_types import ReadResourceContents
from mcp.shared.memory import create_connected_server_and_client_session

CALL_TIMEOUT = 5.0
CONNECT_TIMEOUT = 5.0


# ---- the state machine ----------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Outcome:
    """What a predicate says: the tool's own facts show the evidence (detected), or only the coder's word can pass it."""

    detected: bool
    needs_word: bool
    why: str


def _count(tool: str, label: str) -> Callable[[Counter], Outcome]:
    def pred(calls: Counter) -> Outcome:
        n = calls[tool]
        return Outcome(n >= 1, False, f"{label}: {n} successful `{tool}` call(s), needs 1")

    return pred


def _word(label: str) -> Callable[[Counter], Outcome]:
    return lambda calls: Outcome(False, True, f"{label}: only the coder's word passes it")


TRANSITIONS: dict[tuple[str, str], Callable[[Counter], Outcome]] = {
    ("plan", "code"): _count("stub", "plan done"),
    ("code", "analyse"): _count("record_edge", "code done"),
    ("analyse", "code"): _word("backward move"),
    ("code", "plan"): _word("re-plan"),
    ("analyse", "plan"): _word("re-plan"),
}


def result(d: dict[str, Any], is_error: bool = False) -> types.CallToolResult:
    return types.CallToolResult(
        content=[types.TextContent(type="text", text=json.dumps(d))],
        structuredContent=d,
        isError=is_error,
    )


class Machine:
    """The current stage, the facts the predicates read (successful tool calls), and the transition table."""

    def __init__(self, start: str, table=TRANSITIONS, stages=STAGES):
        self.stage, self.table, self.stages = start, table, tuple(stages)
        self.calls: Counter = Counter()

    def allowed(self) -> list[str]:
        return [d for (s, d) in self.table if s == self.stage]

    def request(self, to: str, confirm: bool = False) -> dict[str, Any]:
        base = {"stage": self.stage, "stages": list(self.stages)}
        if to not in self.stages:
            return {
                **base,
                "ok": False,
                "needs_clarification": True,
                "reason": f"unknown stage {to!r}",
                "ask": f"which stage did you mean? one of {list(self.stages)}",
            }
        if to == self.stage:
            return {**base, "ok": True, "moved": False, "reason": "already there"}
        pred = self.table.get((self.stage, to))
        if pred is None:
            return {
                **base,
                "ok": False,
                "refused": True,
                "reason": f"no transition {self.stage} -> {to}",
                "allowed": self.allowed(),
            }
        out = pred(self.calls)
        if out.detected or (out.needs_word and confirm):
            frm, self.stage = self.stage, to
            via = "detected" if out.detected else "word"
            return {"ok": True, "moved": True, "from": frm, "to": to, "via": via, "stage": to}
        hint = (
            "pass confirm=true with the coder's word"
            if out.needs_word
            else "do the stage's work first"
        )
        return {**base, "ok": False, "refused": True, "reason": out.why, "hint": hint}


# ---- connectors: how the router reaches a stage server ----------------------------------------------------------

Connector = Callable[[AsyncExitStack, str], Awaitable[ClientSession]]


def memory_connector(servers: dict[str, Any]) -> Connector:
    async def connect(stack: AsyncExitStack, name: str) -> ClientSession:
        return await stack.enter_async_context(
            create_connected_server_and_client_session(servers[name])
        )

    return connect


@asynccontextmanager
async def _http_session(url: str, message_handler=None):
    async with (
        streamable_http_client(url) as (r, w, _),
        ClientSession(r, w, message_handler=message_handler) as session,
    ):
        await session.initialize()
        yield session


def http_connector(urls: dict[str, str]) -> Connector:
    async def connect(stack: AsyncExitStack, name: str) -> ClientSession:
        return await stack.enter_async_context(_http_session(urls[name]))

    return connect


# ---- the router -------------------------------------------------------------------------------------------------


@dataclass
class Conn:
    """Per client connection: the machine, one upstream session per stage (None when it would not connect)."""

    machine: Machine
    sessions: dict[str, ClientSession | None]
    errors: dict[str, str] = field(default_factory=dict)
    tools: dict[str, list[types.Tool]] = field(default_factory=dict)


def _obj(props: dict, required: list[str]) -> dict:
    return {"type": "object", "properties": props, "required": required}


ROUTER_TOOLS = {
    "stage": types.Tool(
        name="stage",
        description="The current stage, the stages one move away, and the stage's tool names. Writes nothing.",
        inputSchema=_obj({}, []),
        outputSchema={"type": "object"},
    ),
    "set_stage": types.Tool(
        name="set_stage",
        description="Request a move to stage `to`. Moves when the transition's predicate passes, "
        "or when it needs the coder's word and `confirm` is true; otherwise returns the refusal.",
        inputSchema=_obj(
            {"to": {"type": "string"}, "confirm": {"type": "boolean", "default": False}}, ["to"]
        ),
        outputSchema={"type": "object"},
    ),
    "stage_tools": types.Tool(
        name="stage_tools",
        description="The tools of the current stage with their descriptions and input schemas.",
        inputSchema=_obj({}, []),
        outputSchema={"type": "object"},
    ),
    "call": types.Tool(
        name="call",
        description="Call `tool` of the current stage with `args` (see stage_tools).",
        inputSchema=_obj({"tool": {"type": "string"}, "args": {"type": "object"}}, ["tool"]),
    ),
}


class Router:
    def __init__(
        self, connector: Connector, mode: str = "dynamic", start: str = "plan", stages=STAGES
    ):
        assert mode in ("dynamic", "facade", "all")
        self.connector, self.mode, self.start, self.stages = connector, mode, start, tuple(stages)
        self.server = Server("scat-router", lifespan=self._lifespan)
        # declare listChanged (the SDK default declares none); both the memory helper and the HTTP manager use this
        self.server.create_initialization_options = functools.partial(
            self.server.create_initialization_options,
            NotificationOptions(tools_changed=True, prompts_changed=True, resources_changed=True),
        )
        self._register()

    async def _hold(
        self, name: str, conn: "Conn", ready: asyncio.Event, stop: asyncio.Event
    ) -> None:
        """Hold one upstream session in its own task: a dead stage server cancels the task that holds its transport
        (the SDK's HTTP client does that), so it must not be the router's request task."""
        try:
            async with AsyncExitStack() as st:
                conn.sessions[name] = await self.connector(st, name)
                ready.set()
                await stop.wait()
        except Exception as e:  # noqa: BLE001 - includes the ExceptionGroup of a failed transport
            conn.sessions[name], conn.errors[name] = None, repr(e)[:200]
        finally:
            conn.sessions.setdefault(name, None)
            ready.set()

    @asynccontextmanager
    async def _lifespan(self, _server):
        conn = Conn(Machine(self.start, stages=self.stages), {})
        stop = asyncio.Event()
        tasks = []
        for name in self.stages:
            ready = asyncio.Event()
            tasks.append(asyncio.create_task(self._hold(name, conn, ready, stop)))
            try:
                await asyncio.wait_for(ready.wait(), CONNECT_TIMEOUT)
            except TimeoutError:
                conn.sessions[name], conn.errors[name] = None, "connect timeout"
        try:
            yield conn
        finally:
            stop.set()
            await asyncio.gather(*tasks, return_exceptions=True)

    # -- helpers

    @property
    def _conn(self) -> Conn:
        return self.server.request_context.lifespan_context

    async def _tools_of(self, stage: str) -> list[types.Tool]:
        c = self._conn
        if stage not in c.tools:
            s = c.sessions.get(stage)
            if s is None:
                return []
            try:
                c.tools[stage] = (await asyncio.wait_for(s.list_tools(), CALL_TIMEOUT)).tools
            except Exception as e:  # noqa: BLE001 - the stage server went away: mark it down, list nothing
                c.sessions[stage], c.errors[stage] = None, repr(e)[:200]
                return []
        return c.tools[stage]

    def _unavailable(self, stage: str, detail: str = "") -> types.CallToolResult:
        c = self._conn
        d = {
            "ok": False,
            "stage_server_unavailable": True,
            "stage": stage,
            "detail": detail or c.errors.get(stage, "not connected"),
        }
        return result(d, is_error=True)

    async def _forward(self, stage: str, name: str, args: dict | None) -> types.CallToolResult:
        c = self._conn
        s = c.sessions.get(stage)
        if s is None:
            return self._unavailable(stage)
        ctx = self.server.request_context
        token = ctx.meta.progressToken if ctx.meta else None

        async def on_progress(progress: float, total: float | None, message: str | None) -> None:
            if token is not None:
                await ctx.session.send_progress_notification(token, progress, total, message)

        try:
            res = await asyncio.wait_for(
                s.call_tool(name, args or {}, progress_callback=on_progress), CALL_TIMEOUT
            )
        except Exception as e:  # noqa: BLE001 - any failure of the upstream is a stage server problem
            c.sessions[stage] = None
            c.errors[stage] = repr(e)[:200]
            return self._unavailable(stage, repr(e)[:200])
        if not res.isError:
            c.machine.calls[name] += 1
        return res

    async def _call_in_stage(self, name: str, args: dict | None) -> types.CallToolResult:
        c = self._conn
        here = [t.name for t in await self._tools_of(c.machine.stage)]
        if c.sessions.get(c.machine.stage) is None:
            return self._unavailable(c.machine.stage)
        if name in here:
            return await self._forward(c.machine.stage, name, args)
        elsewhere = [
            s
            for s in self.stages
            if s != c.machine.stage and name in [t.name for t in await self._tools_of(s)]
        ]
        base = {"ok": False, "stage": c.machine.stage, "tools_here": here}
        if elsewhere:
            return result(
                {
                    **base,
                    "refused": True,
                    "reason": f"`{name}` is not a tool of stage `{c.machine.stage}`",
                    "in_stages": elsewhere,
                    "ask": "request the stage with set_stage, or pick a tool of this stage",
                }
            )
        return result({**base, "needs_clarification": True, "reason": f"unknown tool {name!r}"})

    async def _notify_changed(self) -> None:
        sess = self.server.request_context.session
        await sess.send_tool_list_changed()
        await sess.send_prompt_list_changed()
        await sess.send_resource_list_changed()

    # -- handlers

    def _register(self) -> None:
        srv = self.server

        @srv.list_tools()
        async def list_tools() -> list[types.Tool]:
            c = self._conn
            if self.mode == "facade":
                return [ROUTER_TOOLS[n] for n in ("stage", "set_stage", "stage_tools", "call")]
            own = [ROUTER_TOOLS["stage"], ROUTER_TOOLS["set_stage"]]
            if self.mode == "dynamic":
                return own + await self._tools_of(c.machine.stage)
            seen: dict[str, types.Tool] = {}
            for st in self.stages:
                for t in await self._tools_of(st):
                    seen.setdefault(t.name, t)
            return own + list(seen.values())

        @srv.call_tool(validate_input=False)
        async def call_tool(name: str, arguments: dict) -> types.CallToolResult:
            c = self._conn
            m = c.machine
            if name == "stage":
                here = [t.name for t in await self._tools_of(m.stage)]
                down = [n for n, v in c.sessions.items() if v is None]
                return result(
                    {
                        "ok": True,
                        "stage": m.stage,
                        "allowed": m.allowed(),
                        "tools": here,
                        "down": down,
                    }
                )
            if name == "set_stage":
                out = m.request(str(arguments.get("to", "")), bool(arguments.get("confirm", False)))
                if out.get("moved") and self.mode == "dynamic":
                    await self._notify_changed()
                return result(out)
            if self.mode == "facade" and name == "stage_tools":
                tools = [t.model_dump(exclude_none=True) for t in await self._tools_of(m.stage)]
                return result({"ok": True, "stage": m.stage, "tools": tools})
            if self.mode == "facade" and name == "call":
                return await self._call_in_stage(
                    str(arguments.get("tool", "")), arguments.get("args")
                )
            if self.mode == "facade":
                return result(
                    {"ok": False, "needs_clarification": True, "reason": f"unknown tool {name!r}"}
                )
            return await self._call_in_stage(name, arguments)

        @srv.list_prompts()
        async def list_prompts() -> list[types.Prompt]:
            c = self._conn
            if self.mode == "facade":
                return []
            s = c.sessions.get(c.machine.stage)
            return (
                []
                if s is None
                else (await asyncio.wait_for(s.list_prompts(), CALL_TIMEOUT)).prompts
            )

        @srv.get_prompt()
        async def get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
            c = self._conn
            s = c.sessions.get(c.machine.stage)
            if s is None or self.mode == "facade":
                raise ValueError(f"no prompt {name!r} in stage {c.machine.stage!r}")
            return await asyncio.wait_for(s.get_prompt(name, arguments), CALL_TIMEOUT)

        @srv.list_resources()
        async def list_resources() -> list[types.Resource]:
            c = self._conn
            if self.mode == "facade":
                return []
            s = c.sessions.get(c.machine.stage)
            return (
                []
                if s is None
                else (await asyncio.wait_for(s.list_resources(), CALL_TIMEOUT)).resources
            )

        @srv.read_resource()
        async def read_resource(uri) -> list[ReadResourceContents]:
            c = self._conn
            s = c.sessions.get(c.machine.stage)
            if s is None or self.mode == "facade":
                raise ValueError(f"no resource {uri} in stage {c.machine.stage!r}")
            res = await asyncio.wait_for(s.read_resource(uri), CALL_TIMEOUT)
            out = []
            for item in res.contents:
                body = (
                    item.text
                    if isinstance(item, types.TextResourceContents)
                    else base64.b64decode(item.blob)
                )
                out.append(ReadResourceContents(content=body, mime_type=item.mimeType))
            return out


@contextlib.asynccontextmanager
async def router_client(router: Router, **kw):
    """A client session connected to `router` in memory (the router's lifespan runs for this connection)."""
    async with create_connected_server_and_client_session(router.server, **kw) as session:
        yield session
