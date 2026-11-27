"""WP34-R3: the CLI, the API and the server's tool give the same result for the same question about the layered view."""

import base64
import json
import sys
from pathlib import Path

import pytest
from viewutil import base_files, narrative, row, write

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "mcp_server"))
from mcputil import call, put_stage, serve, with_session

import scat_kg
from scat_kg import draw
from scat_kg.cli import main
from scat_kg.ops.result import stamp

BARE = narrative(
    "Bare", "", [row("holds", "farmers", "water"), row("addressed-by", "water", "alert")]
)


@pytest.fixture(scope="module")
def root(tmp_path_factory):
    base = tmp_path_factory.mktemp("parity")
    return write(base / "vault", base_files() | {"narrative/bare.md": BARE})


@pytest.fixture(scope="module")
def url(root):
    put_stage(root, "code")
    with serve(root) as u:
        yield u


def by_cli(capsys, root, argv):
    code = main([*argv, "--root", str(root), "--json"])
    assert code == 0
    return json.loads(capsys.readouterr().out)


# (CLI arguments, the API's result, the server tool and its arguments)
QUESTIONS = {
    "layered": (
        ["layered"],
        lambda r: scat_kg.layered(root=r),
        ("layered", {}),
    ),
    "layered-candidates": (
        ["layered", "--candidates"],
        lambda r: scat_kg.layered(candidates=True, root=r),
        ("layered", {"candidates": True}),
    ),
    "layered-some-candidates": (
        ["layered", "--narrative", "dry", "--narrative", "bare", "--candidates"],
        lambda r: scat_kg.layered(["dry", "bare"], candidates=True, root=r),
        ("layered", {"narratives": ["dry", "bare"], "candidates": True}),
    ),
    "layered-some": (
        ["layered", "--narrative", "dry", "--narrative", "bare"],
        lambda r: scat_kg.layered(["dry", "bare"], root=r),
        ("layered", {"narratives": ["dry", "bare"]}),
    ),
    "fingerprint-no-account": (
        ["fingerprint", "bare", "--candidates"],
        lambda r: scat_kg.fingerprint("bare", candidates=True, root=r),
        ("fingerprint", {"narrative": "bare", "candidates": True}),
    ),
}


@pytest.mark.parametrize("name", QUESTIONS)
def test_cli_api_and_server_give_one_document(capsys, root, url, name):
    argv, api, (tool, args) = QUESTIONS[name]
    want = stamp(api(root), root).to_dict()
    assert by_cli(capsys, root, argv) == want
    assert call(url, tool, args) == want


def test_the_options_change_the_answer(root):
    plain = scat_kg.layered(root=root).to_dict()
    asked = scat_kg.layered(candidates=True, root=root).to_dict()
    assert "candidates" not in plain and asked["candidates"] and asked["no_account"] == ["bare"]
    assert "orphans" in plain and plain["orphans"] == asked["orphans"]
    flagged = scat_kg.fingerprint("bare", candidates=True, root=root).to_dict()["narratives"][0]
    assert flagged["no_account"] is True


def plot_of(url, args):
    async def go(s):
        res = await s.call_tool("layered", {"output": "plot", **args})
        assert not res.isError, res.content
        assert len(res.content) == 1 and res.content[0].type == "image"
        return base64.b64decode(res.content[0].data)

    return with_session(url, go)


@pytest.mark.parametrize("candidates", [False, True])
def test_the_three_plots_are_byte_identical(capsys, tmp_path, root, url, candidates):
    out = tmp_path / "cli.png"
    flag = ["--candidates"] if candidates else []
    assert main(["draw", "layered", *flag, "--out", str(out), "--root", str(root)]) == 0
    capsys.readouterr()
    api = draw.layered(candidates=candidates, root=root).png()
    assert out.read_bytes() == api
    assert plot_of(url, {"candidates": candidates}) == api


def test_the_candidate_plot_differs_from_the_plain_one(root):
    assert draw.layered(candidates=True, root=root).svg() != draw.layered(root=root).svg()
