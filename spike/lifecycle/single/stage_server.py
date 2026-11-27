"""Throwaway spike server (RS5-U3): how a request carries the lifecycle stage and how a server scopes itself.

Not shipped. Stage names and the stage table are placeholders. Every tool is a stand-in returning a small dict.
Scoping is data: STAGES maps a stage to the tools, prompts and resources it lists.
"""

from __future__ import annotations

import functools
from typing import Any

from mcp import types
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.lowlevel.server import NotificationOptions

# --- the data: one row per stage (placeholders) -------------------------------------------------------
STAGES: dict[str, dict[str, Any]] = {
    "plan": {
        "about": "decide what to read and which nodes to stub",
        "allows": "look at status and check; create stub pages",
        "tools": ["status", "check", "stub"],
        "prompts": ["plan_guide"],
        "resources": ["scat://glossary", "scat://plan-notes"],
    },
    "code": {
        "about": "the coder writes narratives; the tool records edges",
        "allows": "status and check; stubs; record edges; set a page to stub or draft",
        "tools": ["status", "check", "stub", "record_edge", "set_status"],
        "prompts": ["code_guide"],
        "resources": ["scat://glossary"],
    },
    "analyse": {
        "about": "read the vault through views",
        "allows": "status and check; views (fingerprint, layered, trace); export edge tables",
        "tools": ["status", "check", "fingerprint", "layered", "trace", "export_edges"],
        "prompts": ["analyse_guide"],
        "resources": ["scat://glossary"],
    },
}
ALWAYS = (
    "set_stage",
    "which_stage",
    "ask_stage",
)  # listed at every stage, and when the stage is unknown
HEADER = "x-scat-stage"
META_KEY = "scat-stage"
SESSIONS: dict[str, str] = {}  # session key -> stage (E2)


def scope(names: list[str], stage: str | None, kind: str = "tools") -> list[str]:
    """The names of one kind that `stage` lists: data only. Unknown stage lists only ALWAYS (tools)."""
    if stage not in STAGES:
        return [n for n in names if kind == "tools" and n in ALWAYS]
    return [n for n in names if n in STAGES[stage][kind] or (kind == "tools" and n in ALWAYS)]


def stages_where(tool: str) -> list[str]:
    return [s for s, row in STAGES.items() if tool in row["tools"]]


# --- carriers: each returns the raw stage value or None -----------------------------------------------
def from_argument(rc, args):
    return (args or {}).get("stage")


def from_meta(rc, args):
    extra = (rc.meta.model_extra or {}) if rc.meta else {}
    return extra.get(META_KEY)


def from_header(rc, args):
    return rc.request.headers.get(HEADER) if rc.request else None


def from_query(rc, args):
    return rc.request.query_params.get("stage") if rc.request else None


def from_path(rc, args):
    return rc.request.scope.get("scat_stage") if rc.request else None


def session_key(rc) -> str:
    sid = rc.request.headers.get("mcp-session-id") if rc.request else None
    return sid or f"mem-{id(rc.session)}"


def from_session(rc, args):
    return SESSIONS.get(session_key(rc))


CARRIERS = {
    "argument": from_argument,
    "meta": from_meta,
    "header": from_header,
    "query": from_query,
    "path": from_path,
    "session": from_session,
}


def build(
    carriers: tuple[str, ...] = ("session",),
    *,
    stateless: bool = False,
    is_error: bool = False,
    list_changed: bool = True,
    scoped_list: bool = True,
    stage_argument: bool = False,
) -> FastMCP:
    """A FastMCP server. `carriers` are tried in order, the first that supplies a value wins."""
    mcp = FastMCP("spike-stage", host="127.0.0.1", stateless_http=stateless)
    low = mcp._mcp_server

    def resolve(args=None) -> tuple[str | None, str | None, str | None]:
        """(valid stage or None, carrier that supplied the value, the raw value)."""
        rc = low.request_context
        for name in carriers:
            raw = CARRIERS[name](rc, args)
            if raw:
                return (raw if raw in STAGES else None), name, raw
        return None, None, None

    def clarify(problem: str, raw: str | None, tool: str | None = None) -> types.CallToolResult:
        doc = {
            "refused": True,
            "problem": problem,
            "tool": tool,
            "value_received": raw,
            "known_stages": {s: f"{r['about']}; allows: {r['allows']}" for s, r in STAGES.items()},
            "who_decides": "the coder decides the stage; the assistant asks the coder and does not choose",
            "how_to_move": "ask the coder which stage; on the coder's word call set_stage(stage, coder_word)",
        }
        text = (
            problem + " Known stages: " + "; ".join(f"{s}: {r['about']}" for s, r in STAGES.items())
        )
        text += ". The coder decides the stage: ask the coder, then call set_stage with the coder's word."
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=text)],
            structuredContent=doc,
            isError=is_error,
        )

    # stand-in tools: same shape as the real server (name, description, small dict result)
    def stand_in(name: str) -> None:
        mcp.tool(name=name, description=f"Stand-in for the real `{name}` tool.")(
            lambda: {"tool": name, "ok": True}
        )

    for n in ["status", "check", "stub", "record_edge", "set_status"]:
        stand_in(n)
    for n in ["fingerprint", "layered", "trace", "export_edges"]:
        stand_in(n)

    @mcp.tool(
        description="Set this session's stage on the coder's word. Without `coder_word` it only records a request."
    )
    async def set_stage(stage: str, ctx: Context, coder_word: str = "") -> dict[str, Any]:
        if stage not in STAGES:
            return clarify(f"`{stage}` is not a stage.", stage, "set_stage").structuredContent
        if not coder_word:
            return {
                "moved": False,
                "requested": stage,
                "next": "ask the coder; call again with coder_word",
            }
        SESSIONS[session_key(ctx.request_context)] = stage
        if list_changed:  # to this session only
            await ctx.session.send_tool_list_changed()
            await ctx.session.send_prompt_list_changed()
            await ctx.session.send_resource_list_changed()
        return {"moved": True, "stage": stage}

    @mcp.tool(
        description="Report the stage this request resolves to and the carrier that supplied it."
    )
    async def which_stage(ctx: Context) -> dict[str, Any]:
        stage, carrier, raw = resolve()
        return {"stage": stage, "carrier": carrier, "raw": raw}

    @mcp.tool(
        description="Ask the coder which stage, by an elicitation request (needs client support)."
    )
    async def ask_stage(ctx: Context) -> dict[str, Any]:
        from mcp.types import ClientCapabilities, ElicitationCapability

        sess = ctx.session
        if not sess.check_client_capability(
            ClientCapabilities(elicitation=ElicitationCapability())
        ):
            return {"elicited": False, "reason": "client did not declare elicitation"}
        res = await sess.elicit_form(
            "Which stage are we in? The coder decides.",
            {"type": "object", "properties": {"stage": {"type": "string", "enum": list(STAGES)}}},
        )
        return {"elicited": True, "action": res.action, "content": res.content}

    @mcp.prompt()
    def plan_guide() -> str:
        return "plan stage: stand-in prompt"

    @mcp.prompt()
    def code_guide() -> str:
        return "code stage: stand-in prompt"

    @mcp.prompt()
    def analyse_guide() -> str:
        return "analyse stage: stand-in prompt"

    @mcp.resource("scat://glossary")
    def glossary() -> str:
        return "stand-in glossary"

    @mcp.resource("scat://plan-notes")
    def plan_notes() -> str:
        return "stand-in plan notes"

    all_tools = mcp.list_tools  # FastMCP's own (global) lister, kept as the source

    # --- scoped handlers (E7): replace FastMCP's registered handlers on the low-level server ---
    @low.list_tools()
    async def _list_tools() -> list[types.Tool]:
        tools = await all_tools()
        if scoped_list:
            keep = scope([t.name for t in tools], resolve()[0])
            tools = [t for t in tools if t.name in keep]
        if stage_argument:  # E3: every tool gets an optional `stage` argument
            for t in tools:
                if t.name not in ALWAYS:
                    t.inputSchema = {
                        **t.inputSchema,
                        "properties": {
                            **t.inputSchema.get("properties", {}),
                            "stage": {
                                "type": "string",
                                "enum": list(STAGES),
                                "description": "lifecycle stage",
                            },
                        },
                    }
        return tools

    @low.call_tool(validate_input=False)
    async def _call_tool(name: str, arguments: dict[str, Any]):
        args = dict(arguments or {})
        if name in ALWAYS:
            return await mcp.call_tool(name, args)
        stage, _carrier, raw = resolve(args)
        args.pop("stage", None)
        if stage is None:
            why = "No stage was supplied." if raw is None else f"`{raw}` is not a stage."
            return clarify(why, raw, name)
        if name not in STAGES[stage]["tools"]:
            where = stages_where(name)
            return clarify(
                f"`{name}` is not available at stage `{stage}`; it is available at: {', '.join(where) or 'no stage'}.",
                raw,
                name,
            )
        return await mcp.call_tool(name, args)

    @low.list_prompts()
    async def _list_prompts() -> list[types.Prompt]:
        prompts = await mcp.list_prompts()
        if not scoped_list:
            return prompts
        keep = scope([p.name for p in prompts], resolve()[0], "prompts")
        return [p for p in prompts if p.name in keep]

    @low.list_resources()
    async def _list_resources() -> list[types.Resource]:
        res = await mcp.list_resources()
        if not scoped_list:
            return res
        keep = scope([str(r.uri) for r in res], resolve()[0], "resources")
        return [r for r in res if str(r.uri) in keep]

    if list_changed:  # E7: advertise listChanged: FastMCP's own options leave it False
        orig = low.create_initialization_options
        low.create_initialization_options = functools.partial(
            orig, notification_options=NotificationOptions(True, True, True)
        )
    return mcp


def asgi_app(mcp: FastMCP):
    """The streamable HTTP app; `/mcp/<stage>` is rewritten to `/mcp` and the stage kept on the scope (E1 path)."""
    inner = mcp.streamable_http_app()

    async def app(scope, receive, send):
        if scope["type"] == "http" and scope["path"].startswith("/mcp/"):
            scope = {
                **scope,
                "scat_stage": scope["path"].split("/")[2],
                "path": "/mcp",
                "raw_path": b"/mcp",
            }
        await inner(scope, receive, send)

    return app
