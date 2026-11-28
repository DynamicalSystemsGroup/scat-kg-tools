"""WP24-R2: the MCP tool `copy_share` returns the Python document, and the CLI, Python and the tool agree."""

import json
import shutil
from pathlib import Path

import pytest
from mcputil import call, put_stage, serve, snapshot

import scat_tools
from scat_tools.cli import main

G6 = Path(__file__).resolve().parents[2] / "research" / "node-pages" / "vault" / "disallowed"


@pytest.fixture(scope="module")
def served(tmp_path_factory):
    vault = tmp_path_factory.mktemp("g6") / "vault"
    shutil.copytree(G6, vault)
    put_stage(vault, "code")
    with serve(vault) as url:
        yield url, vault


def test_the_tool_returns_the_python_document(served):
    url, vault = served
    got = call(url, "copy_share", {})
    assert got == scat_tools.copy_share(root=vault).to_dict()
    assert got["operation"] == "copy-share" and got["schema_version"] == 3
    assert got["mode"] == "disallowed" and got["pages"]
    one = call(url, "copy_share", {"node": "members-not-replying"})
    assert one == scat_tools.copy_share("members-not-replying", root=vault).to_dict()
    assert [p["name"] for p in one["pages"]] == ["members-not-replying"]


def test_the_cli_the_python_call_and_the_tool_give_one_document(served, capsys):
    url, vault = served
    assert main(["copy-share", "--root", str(vault), "--json"]) == 0
    from_cli = json.loads(capsys.readouterr().out)
    assert from_cli == scat_tools.copy_share(root=vault).to_dict() == call(url, "copy_share", {})


def test_a_refusal_is_a_result_and_nothing_is_written(served):
    url, vault = served
    before = snapshot(vault)
    for node in ("no-such-node", "forget-incident"):  # unknown; a narrative
        doc = call(url, "copy_share", {"node": node})
        assert doc == scat_tools.copy_share(node, root=vault).to_dict()
        assert doc["ok"] is False and doc["refused"][0]["fix"]
    assert snapshot(vault) == before
