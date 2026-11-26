"""WP24-R1: the MCP tool `evidence` returns the Python document, on the range vault, over a real HTTP server."""

import json
import shutil
from pathlib import Path

import pytest
from mcputil import call, serve, snapshot

import scat_kg
from scat_kg.cli import main

RANGE = Path(__file__).resolve().parents[2] / "research" / "range" / "koi" / "vault"
NODES = ("community-members", "forget-signal", "ethnographers", "closing-the-loop")


@pytest.fixture(scope="module")
def served(tmp_path_factory):
    vault = tmp_path_factory.mktemp("range") / "vault"
    shutil.copytree(RANGE, vault)
    with serve(vault) as url:
        yield url, vault


@pytest.mark.parametrize("node", NODES)
def test_the_tool_returns_the_python_document(served, node):
    url, vault = served
    got = call(url, "evidence", {"node": node})
    want = scat_kg.evidence(node, root=vault).to_dict()
    assert got == want
    assert (
        got["operation"] == "evidence"
        and got["schema_version"] == 3
        and got["mode"] == "disallowed"
    )
    assert got["narratives"]


def test_the_cli_the_python_call_and_the_tool_give_one_document(served, capsys):
    url, vault = served
    assert main(["evidence", "community-members", "--root", str(vault), "--json"]) == 0
    from_cli = json.loads(capsys.readouterr().out)
    assert from_cli == scat_kg.evidence("community-members", root=vault).to_dict()
    assert from_cli == call(url, "evidence", {"node": "community-members"})


def test_a_refusal_is_a_result_and_nothing_is_written(served):
    url, vault = served
    before = snapshot(vault)
    for node in ("no-such-node", "forget-incident"):  # unknown; a narrative
        doc = call(url, "evidence", {"node": node})
        assert doc == scat_kg.evidence(node, root=vault).to_dict()
        assert doc["ok"] is False and doc["refused"][0]["fix"]
    assert snapshot(vault) == before
