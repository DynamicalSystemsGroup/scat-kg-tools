"""RS7-U3 spike server: one tool per elicitation variant. Not shipped.

Every tool that elicits first checks the client declared `elicitation` (as RS5's `ask_stage` did), except
`b8_nocheck`. The tool result says what the server saw, so a client can tell "asked" from "not asked".
"""

from __future__ import annotations

import secrets
from typing import Any

import anyio
from mcp import types
from mcp.server.fastmcp import Context, FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import ClientCapabilities, ElicitationCapability
from pydantic import BaseModel

MSG = "Which stage are we in? The coder decides."
SCHEMA = {
    "type": "object",
    "properties": {"stage": {"type": "string", "enum": ["plan", "code", "analyse"]}},
}
WAIT = 3.0  # B9: seconds the server waits for an answer before it returns a fallback


class StagePick(BaseModel):
    stage: str


def declared(ctx: Context, check: bool = True) -> bool:
    """RS5's capability check. `check=False` skips it (stateless HTTP has no initialize, so it always fails)."""
    return not check or ctx.session.check_client_capability(
        ClientCapabilities(elicitation=ElicitationCapability())
    )


def not_declared() -> dict[str, Any]:
    return {"elicited": False, "reason": "client did not declare elicitation"}


def answer(res: Any) -> dict[str, Any]:
    """ElicitResult has `content`; ctx.elicit's AcceptedElicitation has `data`."""
    data = getattr(res, "data", None)
    content = data.model_dump() if data is not None else getattr(res, "content", None)
    return {"elicited": True, "action": res.action, "content": content}


def fallback(seconds: float) -> dict[str, Any]:
    return {
        "elicited": False,
        "reason": f"no answer in {seconds:g} s",
        "assistant_instruction": "Ask the coder which stage in chat, then call again with their word. Do not choose.",
    }


def build(
    *, stateless: bool = False, json_response: bool = False, check: bool = True, wait: float = WAIT
) -> FastMCP:
    mcp = FastMCP(
        "spike-asking", host="127.0.0.1", stateless_http=stateless, json_response=json_response
    )
    pending: dict[str, str] = {}  # B10 preview tokens

    @mcp.tool(
        description="B1 baseline: ctx.session.elicit_form (no related_request_id), as in RS5."
    )
    async def b1_session(ctx: Context) -> dict[str, Any]:
        if not declared(ctx, check):
            return not_declared()
        return answer(await ctx.session.elicit_form(MSG, SCHEMA))

    @mcp.tool(description="B2: ctx.session.elicit_form with related_request_id=ctx.request_id.")
    async def b2_related(ctx: Context) -> dict[str, Any]:
        if not declared(ctx, check):
            return not_declared()
        return answer(await ctx.session.elicit_form(MSG, SCHEMA, related_request_id=ctx.request_id))

    @mcp.tool(description="B3: ctx.elicit(message, schema=PydanticModel).")
    async def b3_ctx(ctx: Context) -> dict[str, Any]:
        if not declared(ctx, check):
            return not_declared()
        return answer(await ctx.elicit(MSG, schema=StagePick))

    @mcp.tool(description="B6: URL mode, ctx.elicit_url.")
    async def b6_url(ctx: Context) -> dict[str, Any]:
        if not declared(ctx, check):
            return not_declared()
        res = await ctx.elicit_url("Open the page to choose.", "http://127.0.0.1:9/choose", "e-1")
        return {"elicited": True, "action": res.action}

    @mcp.tool(
        description="B7: a log notification and a progress notification first, then ctx.elicit."
    )
    async def b7_after_ctx(ctx: Context) -> dict[str, Any]:
        if not declared(ctx, check):
            return not_declared()
        await ctx.info("working")
        await ctx.report_progress(1, 2)
        return answer(await ctx.elicit(MSG, schema=StagePick))

    @mcp.tool(description="B7: the same, then ctx.session.elicit_form (baseline route).")
    async def b7_after_session(ctx: Context) -> dict[str, Any]:
        if not declared(ctx, check):
            return not_declared()
        await ctx.info("working")
        await ctx.report_progress(1, 2)
        return answer(await ctx.session.elicit_form(MSG, SCHEMA))

    @mcp.tool(description="B8: what the client declared, and what check_client_capability says.")
    async def b8_caps(ctx: Context) -> dict[str, Any]:
        sess = ctx.session
        el = sess.client_params.capabilities.elicitation if sess.client_params else None
        return {
            "declared": el.model_dump(exclude_none=True) if el else None,
            "check_empty": sess.check_client_capability(
                ClientCapabilities(elicitation=ElicitationCapability())
            ),
            "check_form": sess.check_client_capability(
                ClientCapabilities(
                    elicitation=ElicitationCapability(form=types.FormElicitationCapability())
                )
            ),
            "check_url": sess.check_client_capability(
                ClientCapabilities(
                    elicitation=ElicitationCapability(url=types.UrlElicitationCapability())
                )
            ),
            # spec: an empty `elicitation: {}` means form mode only
            "form_by_spec": bool(el) and (el.form is not None or el.url is None),
        }

    @mcp.tool(
        description="B8: ctx.elicit with no capability check; reports the error if the client refuses."
    )
    async def b8_nocheck(ctx: Context) -> dict[str, Any]:
        try:
            return answer(await ctx.elicit(MSG, schema=StagePick))
        except McpError as e:
            return {"elicited": False, "mcp_error": f"{e.error.code}: {e.error.message}"}

    @mcp.tool(
        description="B9: ctx.session.elicit_form (baseline route) with a server-side timeout and a fallback."
    )
    async def b9_timeout_session(ctx: Context) -> dict[str, Any]:
        if not declared(ctx, check):
            return not_declared()
        try:
            with anyio.fail_after(wait):
                return answer(await ctx.session.elicit_form(MSG, SCHEMA))
        except TimeoutError:
            return fallback(wait)

    @mcp.tool(description="B9: ctx.elicit with a server-side timeout and a fallback.")
    async def b9_timeout_ctx(ctx: Context) -> dict[str, Any]:
        if not declared(ctx, check):
            return not_declared()
        try:
            with anyio.fail_after(wait):
                return answer(await ctx.elicit(MSG, schema=StagePick))
        except TimeoutError:
            return fallback(wait)

    @mcp.tool(
        description="B10 step 1: preview the change; returns a token. Writes nothing.",
        annotations=types.ToolAnnotations(
            readOnlyHint=True, destructiveHint=False, idempotentHint=True
        ),
    )
    def b10_preview(note: str) -> dict[str, Any]:
        token = secrets.token_hex(4)
        pending[token] = note
        return {
            "applied": False,
            "preview": f"would write: {note}",
            "token": token,
            "next": "show this preview to the coder; only on the coder's word call b10_apply with the token",
        }

    @mcp.tool(
        description="B10 step 2: apply a previewed change. Needs the token from b10_preview.",
        annotations=types.ToolAnnotations(
            readOnlyHint=False, destructiveHint=True, idempotentHint=False
        ),
    )
    def b10_apply(token: str) -> dict[str, Any]:
        note = pending.pop(token, None)
        if note is None:
            return {
                "applied": False,
                "problem": "unknown or already used token; call b10_preview first",
            }
        return {"applied": True, "wrote": note}

    @mcp.tool(
        description="B10 variant: no client support needed; the result tells the assistant to ask the coder.",
        annotations=types.ToolAnnotations(readOnlyHint=True),
    )
    def b10_instruct() -> types.CallToolResult:
        text = "Stop. The coder decides the stage. Ask the coder which of: plan, code, analyse. Do not choose."
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=text)],
            structuredContent={
                "needs_coder": True,
                "ask": "which stage",
                "options": ["plan", "code", "analyse"],
            },
        )

    return mcp
