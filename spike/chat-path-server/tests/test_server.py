import json
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

SERVER = Path(__file__).parent.parent / "server.py"
TEMPLATE = Path("/Users/z/Documents/GitHub/scat-kg-template")


@pytest.fixture(scope="module")
def vault(tmp_path_factory):
    dest = tmp_path_factory.mktemp("vault") / "v"
    shutil.copytree(TEMPLATE, dest, ignore=shutil.ignore_patterns(".git", ".venv", ".obsidian"))
    return dest


@pytest.fixture(scope="module")
def url(vault):
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    p = subprocess.Popen(
        [sys.executable, str(SERVER), "--vault", str(vault), "--port", str(port)],
        stderr=subprocess.DEVNULL,
    )
    for _ in range(100):
        try:
            socket.create_connection(("127.0.0.1", port), 0.2).close()
            break
        except OSError:
            time.sleep(0.1)
    yield f"http://127.0.0.1:{port}/mcp"
    p.terminate()
    p.wait()


async def call(url, tool, args):
    async with streamablehttp_client(url) as (r, w, _), ClientSession(r, w) as s:
        await s.initialize()
        res = await s.call_tool(tool, args)
        return json.loads(res.content[0].text)


async def test_tools_listed(url):
    async with streamablehttp_client(url) as (r, w, _), ClientSession(r, w) as s:
        await s.initialize()
        names = {t.name for t in (await s.list_tools()).tools}
    assert names == {"check_page", "check_vault"}


async def test_check_vault(url):
    doc = await call(url, "check_vault", {})
    assert doc["kind"] == "check" and doc["operation"] == "check" and "problems" in doc


async def test_check_page_by_name(url, vault):
    name = next(vault.joinpath("concern").glob("*.md")).stem
    doc = await call(url, "check_page", {"page": name})
    assert doc["kind"] == "check" and "problems" in doc
    assert all(p["file"].endswith(f"{name}.md") for p in doc["problems"])


async def test_check_page_unknown_is_refusal_json(url):
    doc = await call(url, "check_page", {"page": "no-such-page"})
    assert doc["kind"] == "operation" and doc["ok"] is False
