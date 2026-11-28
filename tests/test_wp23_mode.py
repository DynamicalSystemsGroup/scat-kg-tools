"""WP23-G1, R1: the attribution mode is reported by `check`, by every view, and in every machine-interface
document, the MCP server's included. A vault with no mode, or an unknown one, is refused by the check."""

import asyncio
import json
import shutil
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

import scat_tools
from scat_tools.cli import main
from scat_tools.mcp_server.server import build

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "contracts" / "examples"
VALIDATOR = Draft202012Validator(
    json.loads((ROOT / "contracts" / "machine-interface.schema.json").read_text("utf-8"))
)
MODES = ("required", "optional", "disallowed")


def vault_with(tmp_path, toml: str | None) -> Path:
    """The example vault, its scat.toml replaced by `toml` (None: removed)."""
    dest = tmp_path / "vault"
    shutil.copytree(EXAMPLES, dest)
    if toml is None:
        (dest / "scat.toml").unlink()
    else:
        (dest / "scat.toml").write_text(toml, encoding="utf-8")
    return dest


def declared(mode: str) -> str:
    return f'attribution = "{mode}"\nstakeholder_group_cap = 3\n'


def test_the_example_vault_declares_disallowed():
    assert scat_tools.check(root=EXAMPLES).mode == "disallowed"
    assert 'attribution = "disallowed"' in (EXAMPLES / "scat.toml").read_text("utf-8")


@pytest.mark.parametrize("mode", MODES)
def test_each_valid_mode_is_accepted_and_reported_by_check(tmp_path, mode):
    root = vault_with(tmp_path, declared(mode))
    result = scat_tools.check(root=root)
    rules = {p.rule for p in result.problems}
    assert "SCAT-MODE-CONFIG" not in rules
    if (
        mode == "required"
    ):  # the example narratives name nobody: the mode's own rule (WP23-G2), not a config fault
        assert {r for r in rules if "ATTR" in r} == {"SCAT-DONE-ATTR", "SCAT-DRAFT-ATTR"}
    else:
        assert result.ok
    assert result.mode == result.to_dict()["mode"] == mode
    assert str(result).splitlines()[0] == f"attribution mode: {mode}"


@pytest.mark.parametrize(
    "toml,why",
    [
        ("stakeholder_group_cap = 3\n", "the key is missing"),
        (
            'attribution = "public"\nstakeholder_group_cap = 3\n',
            "not one of `required`, `optional`, `disallowed`",
        ),
    ],
    ids=["missing", "unknown"],
)
def test_no_mode_or_an_unknown_one_is_refused_by_check_naming_the_three_choices(
    tmp_path, toml, why
):
    result = scat_tools.check(root=vault_with(tmp_path, toml))
    (problem,) = result.errors
    assert not result.ok and problem.rule == "SCAT-MODE-CONFIG" and problem.file == "scat.toml"
    assert why in problem.what
    for mode in MODES:
        assert f'`attribution = "{mode}"`' in problem.fix
    assert result.mode is None and result.to_dict()["mode"] is None
    assert str(result).splitlines()[0] == "attribution mode: not declared"
    assert VALIDATOR.is_valid(result.to_dict())


def test_the_cli_prints_the_mode_and_the_json_carries_it(tmp_path, capsys):
    root = vault_with(tmp_path, declared("optional"))
    assert main(["check", "--root", str(root)]) == 0
    assert capsys.readouterr().out.splitlines()[0] == "attribution mode: optional"
    assert main(["check", "--root", str(root), "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["mode"] == "optional"


def documents(root):
    """One result of every kind, from the same vault."""
    return {
        "check": scat_tools.check(root=root),
        "check page": scat_tools.check("quick-checkout", root=root),
        "status": scat_tools.status(root=root),
        "fingerprint": scat_tools.fingerprint(root=root),
        "edges": scat_tools.edge_table("holds", root=root),
        "layered": scat_tools.layered(root=root),
        "trace": scat_tools.trace("borrowers", root=root),
        "set-status": scat_tools.set_status("quick-checkout", "stub", root=root),
        "set-status refused": scat_tools.set_status("no-such-page", "stub", root=root),
        "index": scat_tools.index(root=root),
        "stub": scat_tools.stub("fresh-idea", "concern", root=root),
        "stub-links": scat_tools.stub_links(root=root),
        "record-edge": scat_tools.record_edge(
            "holds", "borrowers", "careful-record-keeping", ["funders-meeting"], root=root
        ),
        "remove-edge": scat_tools.remove_edge("funders", "quick-checkout", root=root),
        "export-edges": scat_tools.export_edges(root / "out", root=root),
    }


@pytest.mark.parametrize("mode", MODES)
def test_every_document_and_the_views_carry_the_mode_and_validate(tmp_path, mode):
    root = vault_with(tmp_path, declared(mode))
    for name, result in documents(root).items():
        doc = result.to_dict()
        assert doc["mode"] == mode, name
        VALIDATOR.validate(doc)


def test_a_view_of_a_vault_with_no_mode_reports_null_and_validates(tmp_path):
    root = vault_with(tmp_path, "stakeholder_group_cap = 3\n")
    for name in ("fingerprint", "edges", "layered", "trace", "status"):
        doc = documents(root)[name].to_dict()
        assert doc["mode"] is None, name
        VALIDATOR.validate(doc)


def test_a_refusal_with_no_vault_reports_a_null_mode(tmp_path):
    doc = scat_tools.check(root=tmp_path / "nowhere").to_dict()
    assert doc["kind"] == "operation" and doc["ok"] is False and doc["mode"] is None
    VALIDATOR.validate(doc)


def test_the_mode_is_read_afresh_on_each_call(tmp_path):
    root = vault_with(tmp_path, declared("required"))
    assert scat_tools.check(root=root).mode == "required"
    (root / "scat.toml").write_text(declared("disallowed"), encoding="utf-8")
    assert scat_tools.check(root=root).mode == "disallowed"


def call(server, tool, **args):
    async def go():
        out = await server.call_tool(tool, args)
        blocks = out[0] if isinstance(out, tuple) else out
        blocks = getattr(blocks, "content", blocks)  # a view tool returns a CallToolResult
        return json.loads(blocks[0].text)

    return asyncio.run(go())


@pytest.mark.parametrize("mode", MODES)
def test_every_mcp_result_carries_the_mode(tmp_path, mode):
    root = vault_with(tmp_path, declared(mode))
    server = build(root)
    calls = [
        ("check", {}),
        ("status", {}),
        ("fingerprint", {}),
        ("edge_table", {"type": "holds"}),
        ("layered", {}),
        ("trace", {"node": "borrowers"}),
        ("set_status", {"page": "quick-checkout", "status": "stub"}),
        ("set_status", {"page": "quick-checkout", "status": "done"}),  # the server's own refusal
        ("index", {}),
        ("stub", {"name": "fresh-idea", "type": "concern"}),
        ("stub_links", {}),
        (
            "record_edge",
            {
                "type": "holds",
                "from_node": "borrowers",
                "to_node": "careful-record-keeping",
                "told_by": ["funders-meeting"],
            },
        ),
        ("remove_edge", {"from_node": "funders", "to_node": "quick-checkout"}),
        ("export_edges", {"folder": "views"}),
    ]
    for tool, args in calls:
        doc = call(server, tool, **args)
        assert doc["mode"] == mode, tool
        VALIDATOR.validate(doc)


def test_the_reader_holds_the_mode_with_the_config_before_any_page(tmp_path):
    from scat_tools.vault import read_mode, read_vault

    root = vault_with(tmp_path, declared("optional"))
    cfg = read_vault(root).config
    assert (cfg.attribution, cfg.attribution_problem) == ("optional", None)
    assert read_mode(root) == "optional"
    (root / "scat.toml").write_text('attribution = "x"\n', encoding="utf-8")
    cfg = read_vault(root).config
    assert (cfg.attribution, cfg.attribution_problem, cfg.attribution_detail) == (
        None,
        "bad-value",
        "'x'",
    )
    assert read_mode(root / "nowhere") is None
