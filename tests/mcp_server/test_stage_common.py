"""Helpers for the stage tests (WP30-U2): an in-process session on a vault, sample calls, vault states, a validator."""

import asyncio
import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator
from mcp.shared.memory import create_connected_server_and_client_session as connected
from mcputil import copy_vault, put_stage

from scat_tools import guides
from scat_tools.mcp_server.server import build

SCHEMA = json.loads(
    (Path(__file__).parents[2] / "contracts" / "machine-interface.schema.json").read_text("utf-8")
)
VALIDATOR = Draft202012Validator(SCHEMA)

INST = guides.instance()
STAGES = list(INST["stages"])
STAGE_TOOLS = list(INST["stage_tools"])
UNION = sorted({t for s in INST["stages"].values() for t in s["tools"]})

# A valid call of each of the 19 tools on the example vault (with its cap raised, see `vault`).
SAMPLES: dict[str, dict] = {
    "check": {},
    "status": {},
    "set_status": {"page": "funders", "status": "draft"},
    "stub": {"name": "fresh-group", "type": "group"},
    "stub_links": {},
    "record_edge": {
        "type": "holds",
        "from_node": "funders",
        "to_node": "quick-checkout",
        "told_by": ["funders-meeting"],
    },
    "remove_edge": {"from_node": "funders", "to_node": "quick-checkout"},
    "merge": {"a": "funders", "b": "borrowers"},
    "split_plan": {"a": "funders"},
    "index": {},
    "fingerprint": {},
    "edge_table": {"type": "holds"},
    "layered": {},
    "trace": {"node": "borrowers"},
    "evidence": {"node": "borrowers"},
    "copy_share": {},
    "review": {},
    "attribution": {},
    "export_edges": {},
}


def vault(dest: Path, stage: str | None = "code", cap: int | None = 10) -> Path:
    """A copy of the example vault in `stage` (None: no lifecycle.toml), its group cap set to `cap`."""
    root = copy_vault(dest, stage=stage)
    toml = root / "scat.toml"
    text = toml.read_text(encoding="utf-8")
    if cap is None:
        text = re.sub(r"^stakeholder_group_cap.*\n", "", text, flags=re.MULTILINE)
    else:
        text = re.sub(
            r"^stakeholder_group_cap = .*$",
            f"stakeholder_group_cap = {cap}",
            text,
            flags=re.MULTILINE,
        )
    toml.write_text(text, encoding="utf-8")
    return root


def all_done(root: Path) -> None:
    """Every narrative `done` and the check clean (the example's one draft narrative is finished)."""
    page = root / "narrative" / "funders-meeting.md"
    text = page.read_text(encoding="utf-8")
    page.write_text(
        text.replace(
            "status: draft\n", 'status: done\ndescription: "A meeting."\ntimeframe: past\n'
        ),
        encoding="utf-8",
    )


def go(vault_root: Path, steps):
    """Run `steps(session)` (an async function) against a fresh in-process server on the vault."""

    async def inner():
        async with connected(build(vault_root)._mcp_server) as s:
            return await steps(s)

    return asyncio.run(inner())


def call_all(vault_root: Path, calls: list[tuple[str, dict]]) -> list[dict]:
    """Each call's document, in order. Nothing may set isError."""

    async def steps(s):
        out = []
        for tool, args in calls:
            res = await s.call_tool(tool, args)
            assert not res.isError, (tool, res.content)
            out.append(json.loads(res.content[0].text))
        return out

    return go(vault_root, steps)


def call_one(vault_root: Path, tool: str, args: dict | None = None) -> dict:
    return call_all(vault_root, [(tool, args or {})])[0]


def is_stage_refusal(doc: dict, tool: str) -> bool:
    """The stage layer's refusal of `tool` (a tool's own refusal names a page or a field, not the tool)."""
    return (
        doc.get("kind") == "operation"
        and doc.get("ok") is False
        and bool(doc.get("refused"))
        and doc["refused"][0]["subject"] == f"tool `{tool}`"
    )


def fix_text(doc: dict) -> str:
    """The text of a refusal's fix: its options' texts, in order."""
    return "\n".join(o["text"] for o in doc["refused"][0]["fix"]["options"])


def valid(doc: dict) -> bool:
    return VALIDATOR.is_valid(doc)


__all__ = ["put_stage"]
