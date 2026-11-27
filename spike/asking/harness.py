"""RS7-U3 harness: a live server on 127.0.0.1 with a wire log, and the clients that talk to it. Not shipped.

Wire log: an ASGI wrapper logs every HTTP exchange (method, path, Accept, Content-Type, session id), every
request body, and every SSE event or JSON body written back, so we can say which HTTP exchange carried the
server's `elicitation/create` request. Only 127.0.0.1 is used.
"""

from __future__ import annotations

import json
import logging
import socket
import threading
import time
from dataclasses import dataclass, field
from typing import Any

import anyio
import httpx
import uvicorn
from asking_server import build
from mcp import ClientSession, types
from mcp.client.streamable_http import streamable_http_client
from mcp.shared.context import RequestContext

HANG = 3.0  # seconds a client waits before we call a call hung
ANSWER = {"action": "accept", "content": {"stage": "plan"}}


# --- wire log ----------------------------------------------------------------------------------------
def summarise(raw: str) -> str:
    """One line for a JSON-RPC message: kind, method or id, a short excerpt."""
    try:
        d = json.loads(raw)
    except ValueError:
        return f"non-json {raw[:60]!r}"
    if isinstance(d, list):
        return "batch " + "; ".join(summarise(json.dumps(x)) for x in d)
    if "method" in d:
        kind = "request" if "id" in d else "notification"
        return f"{kind} {d['method']} id={d.get('id')} {json.dumps(d.get('params', {}))[:110]}"
    if "result" in d:
        return f"response id={d.get('id')} result={json.dumps(d['result'])[:110]}"
    if "error" in d:
        return f"error id={d.get('id')} {json.dumps(d['error'])[:110]}"
    return raw[:80]


class Wire:
    """ASGI wrapper: logs into `lines`. Tag is METHOD#n, one per HTTP exchange."""

    def __init__(self, app, lines: list[str], t0: float):
        self.app, self.lines, self.t0, self.n = app, lines, t0, 0

    def log(self, tag: str, text: str) -> None:
        self.lines.append(f"[{time.monotonic() - self.t0:6.2f}s] {tag:7} {text}")

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        self.n += 1
        tag = f"{scope['method']}#{self.n}"
        h = {k.decode(): v.decode() for k, v in scope["headers"]}
        self.log(
            tag,
            f"-> {scope['path']} accept={h.get('accept')!r} content-type={h.get('content-type')!r} "
            f"session={'yes' if 'mcp-session-id' in h else 'no'}",
        )
        body = bytearray()

        async def recv():
            m = await receive()
            if m["type"] == "http.request":
                body.extend(m.get("body", b""))
                if not m.get("more_body") and body:
                    self.log(tag, "   body: " + summarise(body.decode()))
                    body.clear()
            elif m["type"] == "http.disconnect":
                self.log(tag, "   client disconnected")
            return m

        buf = ""
        sse = False

        async def snd(m):
            nonlocal buf, sse
            if m["type"] == "http.response.start":
                ct = dict(m["headers"]).get(b"content-type", b"").decode()
                sse = ct.startswith("text/event-stream")
                self.log(tag, f"<- {m['status']} content-type={ct!r}")
            elif m["type"] == "http.response.body":
                chunk = m.get("body", b"").decode()
                if sse:
                    buf += chunk.replace("\r\n", "\n")
                    while "\n\n" in buf:
                        ev, buf = buf.split("\n\n", 1)
                        data = [ln[5:].strip() for ln in ev.split("\n") if ln.startswith("data:")]
                        if data:
                            self.log(tag, "   sse: " + summarise(data[0]))
                elif chunk:
                    self.log(tag, "   json: " + summarise(chunk))
            await send(m)

        await self.app(scope, recv, snd)
        self.log(tag, "   exchange ended")


class SdkLog(logging.Handler):
    def __init__(self, lines: list[str], t0: float):
        super().__init__(logging.DEBUG)
        self.lines, self.t0 = lines, t0

    def emit(self, record: logging.LogRecord) -> None:
        msg = " ".join(record.getMessage().split())
        if "not found" in msg or "stream" in msg.lower() or msg.startswith("received:"):
            self.lines.append(f"[{time.monotonic() - self.t0:6.2f}s] sdk     {msg[:150]}")


class LiveServer:
    def __init__(self, **cfg):
        self.lines: list[str] = []
        self.t0 = time.monotonic()
        mcp = build(**cfg)
        app = Wire(mcp.streamable_http_app(), self.lines, self.t0)
        self.sock = socket.socket()
        self.sock.bind(("127.0.0.1", 0))
        self.port = self.sock.getsockname()[1]
        c = uvicorn.Config(app, log_level="critical", timeout_graceful_shutdown=1)
        self.server = uvicorn.Server(c)
        self.thread = threading.Thread(
            target=lambda: self.server.run(sockets=[self.sock]), daemon=True
        )
        self.handler = SdkLog(self.lines, self.t0)
        self.sdk_logger = logging.getLogger("mcp.server.streamable_http")

    def __enter__(self):
        self.sdk_logger.addHandler(self.handler)
        self.sdk_logger.setLevel(logging.DEBUG)
        for name in (
            "mcp",
            "httpx",
        ):  # keep library chatter off the console; our handler still gets the records
            logging.getLogger(name).propagate = False
        self.thread.start()
        while not self.server.started:
            self.thread.join(0.02)
        return self

    def __exit__(self, *exc):
        self.server.should_exit = True
        self.thread.join(10)
        self.sock.close()
        self.sdk_logger.removeHandler(self.handler)

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}/mcp"


# --- clients -----------------------------------------------------------------------------------------
@dataclass
class Seen:
    """What a client saw."""

    prompts: list[str] = field(
        default_factory=list
    )  # server elicitation requests the client received
    result: Any = None  # the tool result (dict) or an error string
    tools: list[types.Tool] = field(default_factory=list)
    note: str = ""


class BlockGet(httpx.AsyncBaseTransport):
    """Answers GET with 405 (the spec's 'no standalone stream here'); the GET never reaches the server."""

    def __init__(self):
        self.inner = httpx.AsyncHTTPTransport()
        self.blocked = 0

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        if request.method == "GET":
            self.blocked += 1
            return httpx.Response(405, headers={"allow": "POST"}, request=request)
        return await self.inner.handle_async_request(request)


def tool_dict(res: types.CallToolResult) -> Any:
    if res.isError:
        return "tool error: " + res.content[0].text[:120]
    return res.structuredContent if res.structuredContent is not None else res.content[0].text


async def sdk_client(
    url: str, kind: str, tool: str, args: dict | None, seen: Seen, *, list_tools=False
):
    """kind: answers | silent | nocap | answers-noget | silent-noget (SDK ClientSession; -noget: GET stream refused)."""
    cb = None if kind == "nocap" else kind.split("-")[0]

    async def elicitation_callback(ctx: RequestContext, params: types.ElicitRequestParams):
        seen.prompts.append(type(params).__name__ + ": " + (params.message or ""))
        if cb == "silent":
            await anyio.sleep_forever()
        return (
            types.ElicitResult(**ANSWER)
            if params.mode != "url"
            else types.ElicitResult(action="accept")
        )

    transport = BlockGet() if kind.endswith("-noget") else None
    client = httpx.AsyncClient(
        transport=transport,
        timeout=httpx.Timeout(30, read=300),
        headers={"accept": "application/json, text/event-stream"},
    )

    async def progress(p, total, msg):
        seen.note += "progress "

    async with (
        client,
        streamable_http_client(url, http_client=client) as (r, w, _),
        ClientSession(r, w, elicitation_callback=elicitation_callback if cb else None) as s,
    ):
        await s.initialize()
        if list_tools:
            seen.tools = (await s.list_tools()).tools
            return
        if tool == "b10_flow":
            seen.result = await b10_flow(s)
            return
        seen.result = tool_dict(await s.call_tool(tool, args or {}, progress_callback=progress))
    if transport:
        seen.note += f"GET refused x{transport.blocked}"


async def b10_flow(s: ClientSession) -> dict:
    """B10: preview -> token -> apply (twice: the second must be refused); and the instruct variant."""
    pre = (await s.call_tool("b10_preview", {"note": "hello"})).structuredContent
    one = (await s.call_tool("b10_apply", {"token": pre["token"]})).structuredContent
    two = (await s.call_tool("b10_apply", {"token": pre["token"]})).structuredContent
    ins = (await s.call_tool("b10_instruct", {})).structuredContent
    return {
        "preview_applied": pre["applied"],
        "apply": one["applied"],
        "replay": two["applied"],
        "instruct": ins["needs_coder"],
    }


def sse_data(text: str) -> list[str]:
    out = []
    for ev in text.replace("\r\n", "\n").split("\n\n"):
        d = [ln[5:].strip() for ln in ev.split("\n") if ln.startswith("data:")]
        if d:
            out.append(d[0])
    return out


async def raw_client(
    url: str,
    caps: dict,
    tool: str,
    args: dict | None,
    seen: Seen,
    *,
    answers=True,
    list_tools=False,
    call_twice=None,
):
    """No GET stream, ever: initialize, initialized, then POST tools/call and read that POST's response.

    A server request on the POST's SSE stream is answered by POSTing a JSON-RPC response (if `answers`).
    """
    h = {"accept": "application/json, text/event-stream", "content-type": "application/json"}
    async with httpx.AsyncClient(timeout=None) as c:
        init = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "initialize",
            "params": {
                "protocolVersion": types.LATEST_PROTOCOL_VERSION,
                "capabilities": caps,
                "clientInfo": {"name": "raw-postonly", "version": "0"},
            },
        }
        r = await c.post(url, json=init, headers=h)
        msg = json.loads(
            sse_data(r.text)[0] if "event-stream" in r.headers["content-type"] else r.text
        )
        if sid := r.headers.get("mcp-session-id"):
            h["mcp-session-id"] = sid
        h["mcp-protocol-version"] = msg["result"]["protocolVersion"]
        await c.post(url, json={"jsonrpc": "2.0", "method": "notifications/initialized"}, headers=h)
        if list_tools:
            r = await c.post(
                url, json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"}, headers=h
            )
            body = sse_data(r.text)[0] if "event-stream" in r.headers["content-type"] else r.text
            seen.tools = [types.Tool(**t) for t in json.loads(body)["result"]["tools"]]
            return
        call = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": tool, "arguments": args or {}},
        }
        async with c.stream("POST", url, json=call, headers=h) as resp:
            ct = resp.headers["content-type"]
            seen.note = f"POST->{resp.status_code} {ct.split(';')[0]}"
            buf = ""
            async for chunk in resp.aiter_text():
                buf += chunk.replace("\r\n", "\n")
                if "event-stream" not in ct:
                    continue
                while "\n\n" in buf:
                    ev, buf = buf.split("\n\n", 1)
                    for data in [ln[5:].strip() for ln in ev.split("\n") if ln.startswith("data:")][
                        :1
                    ]:
                        m = json.loads(data)
                        if "method" in m and "id" in m:  # a server-to-client request
                            seen.prompts.append(m["method"] + ": " + m["params"].get("message", ""))
                            if answers:
                                body = (
                                    {"action": "accept"}
                                    if m["params"].get("mode") == "url"
                                    else ANSWER
                                )
                                await c.post(
                                    url,
                                    json={"jsonrpc": "2.0", "id": m["id"], "result": body},
                                    headers=h,
                                )
                        elif m.get("id") == 1:
                            res = types.CallToolResult(**m["result"]) if "result" in m else None
                            seen.result = tool_dict(res) if res else f"jsonrpc error {m['error']}"
                            return
            if "event-stream" not in ct and buf:
                m = json.loads(buf)
                seen.result = (
                    tool_dict(types.CallToolResult(**m["result"]))
                    if "result" in m
                    else f"jsonrpc error {m['error']}"
                )


# --- scenario ----------------------------------------------------------------------------------------
CLIENTS = {
    "A1 sdk-answers": lambda u, t, a, s, **k: sdk_client(u, "answers", t, a, s, **k),
    "A2 sdk-silent": lambda u, t, a, s, **k: sdk_client(u, "silent", t, a, s, **k),
    "A3 sdk-nocap": lambda u, t, a, s, **k: sdk_client(u, "nocap", t, a, s, **k),
    "A4 raw-postonly": lambda u, t, a, s, **k: raw_client(u, {"elicitation": {}}, t, a, s, **k),
    "A4s sdk-postonly": lambda u, t, a, s, **k: sdk_client(u, "answers-noget", t, a, s, **k),
    "R none": lambda u, t, a, s, **k: raw_client(u, {}, t, a, s, **k),
    "R {elicitation:{}}": lambda u, t, a, s, **k: raw_client(u, {"elicitation": {}}, t, a, s, **k),
    "R {form:{}}": lambda u, t, a, s, **k: raw_client(
        u, {"elicitation": {"form": {}}}, t, a, s, **k
    ),
    "R {url:{}}": lambda u, t, a, s, **k: raw_client(u, {"elicitation": {"url": {}}}, t, a, s, **k),
    "A4q raw-silent": lambda u, t, a, s, **k: raw_client(
        u, {"elicitation": {}}, t, a, s, answers=False, **k
    ),
}


@dataclass
class Row:
    variant: str
    config: str
    client: str
    saw: str
    stream: str
    outcome: str
    wall: float
    server: str
    log: list[str]


def stream_of(lines: list[str]) -> str:
    """Which HTTP exchange carried the server's elicitation request: from the wire log."""
    for ln in lines:
        if "request elicitation/create" in ln:
            kind = ln.split("]")[1].split()[0].split("#")[0]
            return {
                "GET": "GET stream (standalone)",
                "POST": "POST stream (tools/call response)",
            }.get(kind, kind)
    if any("_GET_stream not found" in ln for ln in lines):
        return "none: routed to GET stream, none open, dropped"
    if any("received: elicitation/create" in ln for ln in lines):
        return "none: routed to POST stream, JSON mode discards it"
    return "none sent"


async def run(variant: str, tool: str, client: str, *, args=None, hang: float = HANG, **cfg) -> Row:
    seen = Seen()
    t = time.monotonic()
    outcome = ""
    with LiveServer(**cfg) as srv:
        try:
            with anyio.fail_after(hang):
                kw = {"list_tools": True} if tool == "tools/list" else {}
                await CLIENTS[client](srv.url, tool, args, seen, **kw)
            outcome = "returned"
        except TimeoutError:
            outcome = f"HUNG (client gave up after {hang:g}s)"
        except BaseException as e:  # noqa: BLE001 - a spike records whatever happened
            outcome = f"client error {type(e).__name__}: {str(e)[:80]}"
        wall = time.monotonic() - t
        await anyio.sleep(0.1)
        lines = list(srv.lines)
    conf = ", ".join(k + "=" + str(v) for k, v in cfg.items()) or "stateful, SSE"
    if tool == "tools/list":
        saw = f"{len(seen.tools)} tools; annotations: " + "; ".join(
            f"{t.name}={t.annotations.model_dump(exclude_none=True)}"
            for t in seen.tools
            if t.annotations
        )
    else:
        asks = tool.split("_")[0] in ("b1", "b2", "b3", "b6", "b7", "b9") or tool == "b8_nocheck"
        saw = ("prompt shown; " if seen.prompts else "no prompt; " if asks else "") + (
            f"result {json.dumps(seen.result)[:110]}" if seen.result is not None else "no result"
        )
    text = " ".join(lines)
    if "request elicitation/create" in text:
        server = (
            "asked; answer POSTed"
            if any("body: response" in ln for ln in lines)
            else "asked; no answer POSTed"
        )
    elif "_GET_stream not found" in text:
        server = "asked, dropped by SDK"
    elif "received: elicitation/create" in text:
        server = "asked, discarded by SDK"
    else:
        server = "did not ask"
    return Row(variant, conf, client, saw, stream_of(lines), outcome, wall, server, lines)
