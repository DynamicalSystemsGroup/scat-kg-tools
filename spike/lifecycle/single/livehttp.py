"""Test helpers: a server on 127.0.0.1 in a thread (ephemeral port), and an SDK client connection."""

from __future__ import annotations

import socket
import threading
from contextlib import asynccontextmanager

import uvicorn
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.shared._httpx_utils import create_mcp_http_client
from stage_server import asgi_app


class LiveServer:
    def __init__(self, mcp, port: int = 0):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("127.0.0.1", port))
        self.port = self.sock.getsockname()[1]
        cfg = uvicorn.Config(asgi_app(mcp), log_level="warning")
        self.server = uvicorn.Server(cfg)
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

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}/mcp"


@asynccontextmanager
async def connect(url: str, headers=None, hooks=None, **session_kw):
    """An initialised SDK ClientSession over streamable HTTP. Yields (session, initialize result)."""
    client = create_mcp_http_client(headers=headers)
    if hooks:
        client.event_hooks["request"].extend(hooks)
    async with (
        client,
        streamable_http_client(url, http_client=client) as (r, w, _),
        ClientSession(r, w, **session_kw) as s,
    ):
        yield s, await s.initialize()


def text(result) -> str:
    return result.content[0].text
