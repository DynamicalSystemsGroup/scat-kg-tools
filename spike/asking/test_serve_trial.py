"""RS7-U3b tests: the trial server's wire log and key gate, on an ephemeral 127.0.0.1 port. Each test is bounded."""

from __future__ import annotations

import socket
import threading

import anyio
import httpx
import pytest
import uvicorn
from mcp import ClientSession, types
from mcp.client.streamable_http import streamable_http_client
from serve_trial import make_app


class Live:
    def __init__(self, log, key=None):
        self.sock = socket.socket()
        self.sock.bind(("127.0.0.1", 0))
        self.port = self.sock.getsockname()[1]
        self.server = uvicorn.Server(
            uvicorn.Config(make_app(log, key), log_level="critical", timeout_graceful_shutdown=1)
        )
        self.thread = threading.Thread(
            target=lambda: self.server.run(sockets=[self.sock]), daemon=True
        )

    def __enter__(self):
        self.thread.start()
        while not self.server.started:
            self.thread.join(0.02)
        return self

    def __exit__(self, *exc):
        self.server.should_exit = True
        self.thread.join(10)
        self.sock.close()


async def call_b3(url: str) -> dict:
    async def cb(ctx, params):
        return types.ElicitResult(action="accept", content={"stage": "plan"})

    async with (
        streamable_http_client(url) as (r, w, _),
        ClientSession(r, w, elicitation_callback=cb) as s,
    ):
        await s.initialize()
        return (await s.call_tool("b3_ctx", {})).structuredContent


def test_log_shows_initialize_capabilities_post_stream_request_and_response(tmp_path):
    log = tmp_path / "wire.log"
    with Live(log) as srv:

        async def go():
            with anyio.fail_after(15):
                return await call_b3(f"http://127.0.0.1:{srv.port}/mcp")

        res = anyio.run(go)
        text = log.read_text()
    assert res["elicited"] and res["content"] == {"stage": "plan"}
    lines = text.splitlines()
    init = next(ln for ln in lines if "rpc: request initialize" in ln)
    assert "capabilities=" in init and '"elicitation"' in init
    assert any("POST /mcp sse: request elicitation/create" in ln for ln in lines)
    assert any("rpc: response id=" in ln and ln.endswith("result") for ln in lines)
    assert any("rpc: request tools/call" in ln and "tool=b3_ctx" in ln for ln in lines)
    assert all(ln[2] == ":" and ln[5] == ":" for ln in lines)  # HH:MM:SS prefix


def test_get_after_initialize_is_marked(tmp_path):
    log = tmp_path / "wire.log"
    with Live(log) as srv:

        async def go():
            with anyio.fail_after(15):
                await call_b3(f"http://127.0.0.1:{srv.port}/mcp")
                await anyio.sleep(0.3)

        anyio.run(go)
        text = log.read_text()
    assert "GET /mcp  <- standalone stream opened" in text


def test_key_gate_refuses_without_key_and_logs_no_key(tmp_path):
    log = tmp_path / "wire.log"
    with Live(log, key="k-7f3a") as srv:
        base = f"http://127.0.0.1:{srv.port}/mcp"
        body = {"jsonrpc": "2.0", "id": 0, "method": "tools/list"}
        h = {"accept": "application/json, text/event-stream"}
        assert httpx.post(base, json=body, headers=h, timeout=5).status_code == 404
        assert httpx.post(base + "?key=bad-key", json=body, headers=h, timeout=5).status_code == 404
        ok = httpx.post(base + "?key=k-7f3a", json=body, headers=h, timeout=5)
        assert ok.status_code != 404
        text = log.read_text()
    assert text.count("<- 404 refused") == 2
    assert "k-7f3a" not in text and "bad-key" not in text


if __name__ == "__main__":
    pytest.main([__file__])
