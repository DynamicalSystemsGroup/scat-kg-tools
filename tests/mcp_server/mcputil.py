"""Helpers for the MCP server tests: a vault copy, a real server on a free port, a client, a tree snapshot."""

import asyncio
import contextlib
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import tomllib
from pathlib import Path

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

EXAMPLES = Path(__file__).parents[2] / "contracts" / "examples"
ASSISTANT = Path(__file__).parents[2] / "contracts" / "assistant.md"
KEY = "test-key-0123456789"


def put_stage(vault: Path, stage: str) -> None:
    """Record `stage` for the vault, as `set_stage` would (a test that walks tools sets the stage it needs)."""
    (vault / "lifecycle.toml").write_text(
        f'stage = "{stage}"\nset_by = "the test"\nset_at = "2026-01-01T00:00:00Z"\n',
        encoding="utf-8",
    )


def offer(vault: Path, tool: str) -> None:
    """Put the vault in the first stage that offers `tool`, unless its stage does already."""
    from scat_kg import guides

    stages = guides.instance()["stages"]
    now = tomllib.loads((vault / "lifecycle.toml").read_text(encoding="utf-8"))["stage"]
    if tool not in stages[now]["tools"]:
        put_stage(vault, next(n for n, s in stages.items() if tool in s["tools"]))


def copy_vault(dest: Path, stage: str | None = "code") -> Path:
    """A copy of the example vault. It is in the `code` stage (a `lifecycle.toml`), which offers the tools most
    tests use; `stage=None` leaves no `lifecycle.toml`, the vault whose stage is unknown."""
    shutil.copytree(EXAMPLES, dest)
    if stage is not None:
        put_stage(dest, stage)
    return dest


def snapshot(root: Path) -> dict[str, bytes | None]:
    """Every file (its bytes) and folder (None) under root."""
    out: dict[str, bytes | None] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for n in dirnames:
            out[str(Path(dirpath, n).relative_to(root))] = None
        for n in filenames:
            p = Path(dirpath, n)
            out[str(p.relative_to(root))] = p.read_bytes()
    return out


def changed(before: dict, after: dict) -> set[str]:
    return {k for k in before.keys() | after.keys() if before.get(k, "-") != after.get(k, "-")}


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def env_with(key: str | None) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k != "SCAT_MCP_KEY"}
    if key is not None:
        env["SCAT_MCP_KEY"] = key
    return env


@contextlib.contextmanager
def serve(vault: Path, key: str | None = KEY, log: Path | None = None):
    """A real `python -m scat_kg.mcp_server` over HTTP on 127.0.0.1; yields its URL; always torn down."""
    port = free_port()
    with open(log or os.devnull, "wb") as sink:
        proc = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "scat_kg.mcp_server",
                "--vault",
                str(vault),
                "--port",
                str(port),
            ],
            env=env_with(key),
            stdout=sink,
            stderr=sink,
        )
        try:
            for _ in range(150):
                if proc.poll() is not None:
                    raise RuntimeError(f"the server exited with {proc.returncode}")
                try:
                    socket.create_connection(("127.0.0.1", port), 0.2).close()
                    break
                except OSError:
                    time.sleep(0.1)
            else:
                raise RuntimeError("the server did not start")
            yield f"http://127.0.0.1:{port}/mcp"
        finally:
            proc.terminate()
            try:
                proc.wait(5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()


def headers(key: str | None = KEY, how: str = "bearer") -> dict[str, str]:
    if key is None:
        return {}
    return {"Authorization": f"Bearer {key}"} if how == "bearer" else {"X-API-Key": key}


def run(coro):
    return asyncio.run(coro)


async def _session_call(url: str, hdrs: dict, fn):
    async with streamablehttp_client(url, headers=hdrs) as (r, w, _), ClientSession(r, w) as s:
        await s.initialize()
        return await fn(s)


def with_session(url: str, fn, hdrs: dict | None = None):
    return run(_session_call(url, headers() if hdrs is None else hdrs, fn))


def call(url: str, tool: str, args: dict | None = None, hdrs: dict | None = None) -> dict:
    async def go(s):
        res = await s.call_tool(tool, args or {})
        assert not res.isError, res.content
        return json.loads(res.content[0].text)

    return with_session(url, go, hdrs)
