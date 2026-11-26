"""WP23-G1, R1: the attribution mode is reported by `check`, by every view, and in every machine-interface
document, the MCP server's included. A vault with no mode, or an unknown one, is refused by the check."""

import asyncio
import json
import shutil
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

import scat_kg
from scat_kg.cli import main
from scat_kg.mcp_server.server import build

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
    assert scat_kg.check(root=EXAMPLES).mode == "disallowed"
    assert 'attribution = "disallowed"' in (EXAMPLES / "scat.toml").read_text("utf-8")


@pytest.mark.parametrize("mode", MODES)
def test_each_valid_mode_is_accepted_and_reported_by_check(tmp_path, mode):
    root = vault_with(tmp_path, declared(mode))
    result = scat_kg.check(root=root)
    assert result.ok and "SCAT-MODE-CONFIG" not in [p.rule for p in result.problems]
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
    result = scat_kg.check(root=vault_with(tmp_path, toml))
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
        "check": scat_kg.check(root=root),
        "check page": scat_kg.check("quick-checkout", root=root),
        "status": scat_kg.status(root=root),
        "fingerprint": scat_kg.fingerprint(root=root),
        "edges": scat_kg.edge_table("holds", root=root),
        "layered": scat_kg.layered(root=root),
        "trace": scat_kg.trace("borrowers", root=root),
        "set-status": scat_kg.set_status("quick-checkout", "stub", root=root),
        "set-status refused": scat_kg.set_status("no-such-page", "stub", root=root),
        "index": scat_kg.index(root=root),
        "stub": scat_kg.stub("fresh-idea", "concern", root=root),
        "stub-links": scat_kg.stub_links(root=root),
        "record-edge": scat_kg.record_edge(
            "holds", "borrowers", "careful-record-keeping", ["funders-meeting"], root=root
        ),
        "remove-edge": scat_kg.remove_edge("funders", "quick-checkout", root=root),
        "export-edges": scat_kg.export_edges(root / "out", root=root),
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
    doc = scat_kg.check(root=tmp_path / "nowhere").to_dict()
    assert doc["kind"] == "operation" and doc["ok"] is False and doc["mode"] is None
    VALIDATOR.validate(doc)


def test_the_mode_is_read_afresh_on_each_call(tmp_path):
    root = vault_with(tmp_path, declared("required"))
    assert scat_kg.check(root=root).mode == "required"
    (root / "scat.toml").write_text(declared("disallowed"), encoding="utf-8")
    assert scat_kg.check(root=root).mode == "disallowed"


def call(server, tool, **args):
    async def go():
        out = await server.call_tool(tool, args)
        blocks = out[0] if isinstance(out, tuple) else out
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
    from scat_kg.vault import read_mode, read_vault

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
