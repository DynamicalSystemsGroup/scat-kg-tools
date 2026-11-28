"""The key gate over a real HTTP server, and the start rules (WP18-R1)."""

import subprocess
import sys

import httpx
import pytest
from mcputil import KEY, call, copy_vault, env_with, free_port, headers, serve, with_session
from test_mcp_tools import SEQUENCE, TOOLS

from scat_tools.mcp_server.gate import key_given, key_ok, start_refusal


@pytest.fixture(scope="module")
def url(tmp_path_factory):
    vault = copy_vault(tmp_path_factory.mktemp("gate") / "v")
    with serve(vault) as u:
        yield u


def _rpc(tool: str) -> dict:
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool, "arguments": {}},
    }


WRONG = {
    "none": {},
    "wrong bearer": {"Authorization": "Bearer nope"},
    "wrong x-api-key": {"X-API-Key": "nope"},
    "prefix of the key": {"Authorization": f"Bearer {KEY[:-1]}"},
    "the key with more": {"Authorization": f"Bearer {KEY}x"},
    "empty bearer": {"Authorization": "Bearer"},
    "key without the scheme": {"Authorization": KEY},
    "non-ascii": {"X-API-Key": "kéy".encode("latin-1")},
}
BASE = {"Accept": "application/json, text/event-stream", "Content-Type": "application/json"}


@pytest.mark.parametrize("tool", sorted(TOOLS))
@pytest.mark.parametrize("which", sorted(WRONG))
def test_every_tool_is_refused_without_the_right_key(url, tool, which):
    r = httpx.post(url, json=_rpc(tool), headers=BASE | WRONG[which])
    assert r.status_code == 401


def test_the_other_routes_and_methods_are_refused_too(url):
    for method in ("GET", "DELETE", "POST"):
        assert httpx.request(method, url, headers=BASE).status_code == 401
    assert httpx.get(url.replace("/mcp", "/"), headers=BASE).status_code == 401


@pytest.mark.parametrize("how", ["bearer", "x-api-key"])
def test_the_key_in_either_header_is_accepted(url, how):
    doc = call(url, "status", {}, hdrs=headers(KEY, how))
    assert doc["kind"] == "status"


def test_the_client_cannot_open_a_session_without_the_key_or_with_a_wrong_one(url):
    async def go(s):
        return await s.list_tools()

    for hdrs in ({}, headers("wrong")):
        with pytest.raises((Exception, BaseExceptionGroup)):
            with_session(url, go, hdrs)


def test_no_tool_is_reachable_with_a_wrong_key_through_the_client(url):
    for tool, args, _ in SEQUENCE[:3]:
        with pytest.raises((Exception, BaseExceptionGroup)):
            call(url, tool, args, hdrs=headers("wrong"))


def test_key_helpers():
    assert key_ok("abc", "abc") and not key_ok("abd", "abc") and not key_ok("", "abc")
    assert not key_ok("kéy", "key")
    assert key_given([(b"authorization", b"Bearer  k ")]) == "k"
    assert key_given([(b"x-api-key", b"k")]) == "k"
    assert key_given([(b"authorization", b"Basic k")]) == ""
    assert key_given([]) == ""


def test_no_key_is_served_on_the_loopback_address_only(tmp_path):
    vault = copy_vault(tmp_path / "v")
    with serve(vault, key=None) as url:
        assert call(url, "status", {}, hdrs={})["kind"] == "status"
    assert start_refusal(None, "127.0.0.1") is None
    assert start_refusal(None, "0.0.0.0")
    assert start_refusal("", "192.168.1.5")
    assert start_refusal("k", "0.0.0.0") is None


@pytest.mark.parametrize("host", ["0.0.0.0", "192.168.0.10", "::"])
def test_it_refuses_to_start_on_a_non_loopback_host_without_a_key(tmp_path, host):
    vault = copy_vault(tmp_path / "v")
    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "scat_tools.mcp_server",
            "--vault",
            str(vault),
            "--host",
            host,
            "--port",
            str(free_port()),
        ],
        env=env_with(None),
        capture_output=True,
        check=False,
        text=True,
        timeout=30,
    )
    assert p.returncode != 0
    assert "SCAT_MCP_KEY" in p.stderr and "refusing" in p.stderr


def test_an_empty_key_counts_as_no_key(tmp_path):
    vault = copy_vault(tmp_path / "v")
    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "scat_tools.mcp_server",
            "--vault",
            str(vault),
            "--host",
            "0.0.0.0",
            "--port",
            str(free_port()),
        ],
        env=env_with(""),
        capture_output=True,
        check=False,
        text=True,
        timeout=30,
    )
    assert p.returncode != 0 and "refusing" in p.stderr


def test_it_refuses_a_missing_vault(tmp_path):
    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "scat_tools.mcp_server",
            "--vault",
            str(tmp_path / "nope"),
            "--stdio",
        ],
        env=env_with(None),
        capture_output=True,
        check=False,
        text=True,
        timeout=30,
    )
    assert p.returncode != 0 and "does not exist" in p.stderr


def test_stdio_needs_no_key(tmp_path):
    import json

    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from mcputil import run

    vault = copy_vault(tmp_path / "v")
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "scat_tools.mcp_server", "--vault", str(vault), "--stdio"],
        env=env_with(None),
    )

    async def go():
        async with stdio_client(params) as (r, w), ClientSession(r, w) as s:
            await s.initialize()
            res = await s.call_tool("status", {})
            return json.loads(res.content[0].text)

    assert run(go())["kind"] == "status"
