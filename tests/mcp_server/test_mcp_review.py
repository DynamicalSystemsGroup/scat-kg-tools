"""WP24-R4: the MCP tool `review` returns the Python document, and the CLI, Python and the tool agree."""

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
    got = call(url, "review", {})
    assert got == scat_tools.review(root=vault).to_dict()
    assert got["operation"] == "review" and got["schema_version"] == 3
    assert got["mode"] == "disallowed" and len(got["proposals"]) == 9 and len(got["reread"]) == 4


def test_the_cli_the_python_call_and_the_tool_give_one_document(served, capsys):
    url, vault = served
    assert main(["review", "--root", str(vault), "--json"]) == 0
    from_cli = json.loads(capsys.readouterr().out)
    assert from_cli == scat_tools.review(root=vault).to_dict() == call(url, "review", {})


def test_the_tool_writes_nothing(served):
    url, vault = served
    before = snapshot(vault)
    call(url, "review", {})
    assert snapshot(vault) == before
