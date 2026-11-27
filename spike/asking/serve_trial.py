"""RS7-U3b trial server: the baseline variant server (stateful, SSE) on 127.0.0.1 with a one-line-per-event wire log.

    python serve_trial.py [--port 8765] [--log PATH] [--key K]

Binds 127.0.0.1 only. Opens no public route and starts no tunnel; how to expose the port is the operator's decision.
Log: one line per HTTP request (HH:MM:SS METHOD PATH, session header present?, Accept, JSON-RPC method; for
`initialize` the client's `capabilities` verbatim), one line per SSE event or JSON body the server writes, and one
per JSON-RPC response the client POSTs back. Tool arguments are never logged, only the tool name. The `key` query
value is never logged. Not shipped.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from urllib.parse import parse_qs

import uvicorn
from asking_server import build

DEFAULT_LOG = "/private/tmp/claude-501/-Users-z-Documents-GitHub/b40c0a13-b60e-4132-b167-1824838bc4cf/scratchpad/trial-wire.log"


def rpc(d: object) -> str:
    """Describe one JSON-RPC message without tool arguments."""
    if isinstance(d, list):
        return "batch [" + "; ".join(rpc(x) for x in d) + "]"
    if not isinstance(d, dict):
        return "non-jsonrpc"
    if "method" in d:
        kind = "request" if "id" in d else "notification"
        out = f"{kind} {d['method']}"
        if "id" in d:
            out += f" id={d['id']}"
        params = d.get("params") or {}
        if d["method"] == "initialize":
            out += " capabilities=" + json.dumps(params.get("capabilities"))
        elif d["method"] == "tools/call":
            out += f" tool={params.get('name')}"
        return out
    if "result" in d:
        return f"response id={d.get('id')} result"
    if "error" in d:
        return f"response id={d.get('id')} error"
    return "non-jsonrpc"


def parse(raw: str) -> str:
    try:
        return rpc(json.loads(raw))
    except ValueError:
        return "non-json"


class WireFile:
    """ASGI wrapper: appends to `path`. Optional key gate: 404 unless the query has key=K."""

    def __init__(self, app, path: str | Path, key: str | None = None):
        self.app, self.path, self.key = app, Path(path), key
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, text: str) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%H:%M:%S')} {text}\n")

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        method, path = scope["method"], scope["path"]
        h = {k.decode().lower(): v.decode() for k, v in scope["headers"]}
        if self.key is not None:
            given = parse_qs(scope.get("query_string", b"").decode()).get("key", [])
            if self.key not in given:
                self.log(f"{method} {path}  <- 404 refused (key missing or invalid)")
                await send({"type": "http.response.start", "status": 404, "headers": []})
                await send({"type": "http.response.body", "body": b""})
                return
        sess = "yes" if "mcp-session-id" in h else "no"
        head = f"{method} {path} session={sess} accept={h.get('accept')!r}"
        if method != "POST":
            self.log(head)
        body = bytearray()

        async def recv():
            m = await receive()
            if m["type"] == "http.request":
                body.extend(m.get("body", b""))
                if method == "POST" and not m.get("more_body"):
                    self.log(f"{head} rpc: {parse(body.decode(errors='replace'))}")
                    body.clear()
            return m

        buf = ""
        sse = False

        async def snd(m):
            nonlocal buf, sse
            if m["type"] == "http.response.start":
                ct = dict(m["headers"]).get(b"content-type", b"").decode()
                sse = ct.startswith("text/event-stream")
                if method == "GET" and m["status"] == 200 and sse:
                    self.log(f"{method} {path}  <- standalone stream opened")
                elif method == "GET":
                    self.log(f"{method} {path}  <- {m['status']}")
            elif m["type"] == "http.response.body":
                chunk = m.get("body", b"").decode(errors="replace")
                if sse:
                    buf += chunk.replace("\r\n", "\n")
                    while "\n\n" in buf:
                        ev, buf = buf.split("\n\n", 1)
                        data = [ln[5:].strip() for ln in ev.split("\n") if ln.startswith("data:")]
                        if data:
                            self.log(f"  {method} {path} sse: {parse(data[0])}")
                elif chunk:
                    self.log(f"  {method} {path} json: {parse(chunk)}")
            await send(m)

        await self.app(scope, recv, snd)


def make_app(log: str | Path, key: str | None = None) -> WireFile:
    return WireFile(
        build().streamable_http_app(), log, key
    )  # build() = stateful, SSE (the baseline)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--log", default=DEFAULT_LOG)
    ap.add_argument("--key", default=None, help="require ?key=K on every request, else 404")
    a = ap.parse_args(argv)
    print(
        f"serving http://127.0.0.1:{a.port}/mcp  log={a.log}  key={'set' if a.key else 'off'}",
        file=sys.stderr,
    )
    uvicorn.run(make_app(a.log, a.key), host="127.0.0.1", port=a.port, log_level="warning")


if __name__ == "__main__":
    main()
