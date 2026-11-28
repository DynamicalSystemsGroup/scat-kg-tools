"""WP29-R2, R3: the lifecycle instance in contracts/lifecycle.md agrees with the server, the skill and itself.

Read from their sources: the instance (the `yaml lifecycle` block), the server's tools and prompts (listed by a real
in-process session), and the skill's section headings. The diagram in the document must be the one the data generates.
"""

import asyncio
import re
import sys
from collections import deque
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "contracts" / "lifecycle.md"
SKILL = ROOT / "skills" / "scat-coding" / "SKILL.md"
sys.path.insert(0, str(ROOT / "tests" / "mcp_server"))

ROLES = {"organiser", "coder", "setup person"}
DIRS = {"start", "forward", "backward"}
# Tools that change narrative, node or contributor pages; a stage whose work does not edit lists none of them (D-178).
WRITERS = {"set_status", "stub", "stub_links", "record_edge", "remove_edge", "merge", "split_plan"}
NO_EDIT_STAGES = {"capture", "analyse", "report"}
STAGES = {"plan", "capture", "code", "analyse", "report"}
GLOSSARY = ROOT / "GLOSSARY.md"
TERMS = ROOT / "docs" / "reference" / "terms.md"
# The backward moves WP29-G2 requires: Analyse to Code, and Code to Plan when the cap is met.
REQUIRED_BACKWARD = {("analyse", "code"), ("code", "plan")}


def instance() -> dict:
    text = DOC.read_text(encoding="utf-8")
    m = re.search(r"```yaml lifecycle\n(.*?)```", text, re.DOTALL)
    assert m, "contracts/lifecycle.md has no `yaml lifecycle` block"
    return yaml.safe_load(m.group(1))


def diagram_in_doc() -> list[str]:
    text = DOC.read_text(encoding="utf-8")
    m = re.search(r"```mermaid\n(.*?)```", text, re.DOTALL)
    assert m, "contracts/lifecycle.md has no mermaid diagram"
    return [line.strip() for line in m.group(1).strip().splitlines()]


def diagram_from_data(data: dict) -> list[str]:
    lines = ["stateDiagram-v2", "[*] --> unknown"]
    for t in data["transitions"]:
        targets = list(data["stages"]) if t["to"] == "any" else [t["to"]]
        for to in targets:
            lines.append(f"{t['from']} --> {to}: {t['id']} {t['predicate']['kind']}")
    return lines


@pytest.fixture(scope="module")
def server_names(tmp_path_factory):
    from mcp.shared.memory import create_connected_server_and_client_session as connected
    from mcputil import copy_vault

    from scat_kg.mcp_server.server import build

    vault = copy_vault(tmp_path_factory.mktemp("lifecycle") / "vault")

    async def go():
        async with connected(build(vault)._mcp_server) as s:
            tools = {t.name for t in (await s.list_tools()).tools}
            prompts = {p.name for p in (await s.list_prompts()).prompts}
            return tools, prompts

    return asyncio.run(go())


def test_every_stage_names_only_what_exists(server_names):
    tools, prompts = server_names
    sections = set(re.findall(r"^## (.+)$", SKILL.read_text(encoding="utf-8"), re.MULTILINE))
    for name, stage in instance()["stages"].items():
        assert set(stage["tools"]) <= tools, (name, set(stage["tools"]) - tools)
        assert set(stage["prompts"]) <= prompts, (name, set(stage["prompts"]) - prompts)
        assert set(stage["skill_sections"]) <= sections, (
            name,
            set(stage["skill_sections"]) - sections,
        )


def test_every_tool_and_prompt_belongs_to_a_stage(server_names):
    tools, prompts = server_names
    data = instance()
    stages = data["stages"].values()
    assert tools == {t for s in stages for t in s["tools"]} | set(data["stage_tools"])
    assert prompts <= {p for s in stages for p in s["prompts"]}


def test_every_stage_lists_its_parts_and_a_review_loop_per_output():
    data = instance()
    assert set(data["stages"]) == STAGES
    for name, stage in data["stages"].items():
        for key in (
            "work",
            "required_inputs",
            "allowed_outputs",
            "tools",
            "prompts",
            "skill_sections",
        ):
            assert stage.get(key), (name, key)
        for out in stage["allowed_outputs"]:
            assert len(str(out.get("output", "")).split()) >= 2, (name, out)
            assert len(str(out.get("review", "")).split()) >= 2, (name, out)
            assert str(out.get("produced_by", "")).strip(), (name, out)


def test_tool_limits_name_tools_of_their_stage():
    for name, stage in instance()["stages"].items():
        assert set(stage.get("tool_limits", {})) <= set(stage["tools"]), name


def test_stages_that_do_not_edit_offer_no_writing_tool():
    for name in NO_EDIT_STAGES:
        assert not set(instance()["stages"][name]["tools"]) & WRITERS, name


def test_the_stage_tools_are_kept_apart(server_names):
    data = instance()
    assert data["stage_tools"] == ["which_stage", "set_stage"]
    assert set(data["stage_tools"]) <= server_names[0]
    for stage in data["stages"].values():
        assert not set(stage["tools"]) & set(data["stage_tools"])


def test_every_transition_names_trigger_predicate_and_who_decides():
    data = instance()
    stages = set(data["stages"]) | {"unknown"}
    for t in data["transitions"]:
        assert t["from"] in stages and (t["to"] in stages or t["to"] == "any"), t
        assert t["dir"] in DIRS and t["trigger"] and t["decides"] in ROLES, t
        p = t["predicate"]
        assert p["kind"] in {"detect", "person"}, t
        if p["kind"] == "detect":
            assert p["check"] in data["detects"], t
        else:
            assert p["says"], t


def test_every_detect_names_its_reader_and_is_used():
    data = instance()
    used = {
        t["predicate"]["check"] for t in data["transitions"] if t["predicate"]["kind"] == "detect"
    }
    assert used == set(data["detects"])
    for check, how in data["detects"].items():
        assert how["reader"], check


def test_the_required_backward_moves_are_present():
    moves = {(t["from"], t["to"]) for t in instance()["transitions"] if t["dir"] == "backward"}
    assert REQUIRED_BACKWARD <= moves


def test_every_stage_is_reachable_without_the_start_move_and_can_be_left():
    data = instance()
    stages = list(data["stages"])
    edges = {s: set() for s in stages + ["unknown"]}
    for t in data["transitions"]:
        if t["dir"] != "start":
            edges[t["from"]].add(t["to"])
    seen, todo = {"plan"}, deque(["plan"])
    while todo:
        for nxt in edges[todo.popleft()] - seen:
            seen.add(nxt)
            todo.append(nxt)
    assert set(stages) <= seen
    assert all(edges[s] for s in stages), "a stage with no way out"


def test_the_glossary_and_terms_page_define_stage_and_transition():
    glossary, terms = GLOSSARY.read_text(encoding="utf-8"), TERMS.read_text(encoding="utf-8")
    for word in ("stage", "transition"):
        assert f"| **{word}** |" in glossary, word
        assert f"- **{word}**:" in terms, word


def test_the_diagram_is_generated_from_the_data():
    assert diagram_in_doc() == diagram_from_data(instance())


def test_no_value_is_split_by_a_comma():
    """A comma in an unquoted flow value splits it (D-192): every transition has exactly its keys, and no listed
    item opens a parenthesis it does not close."""
    data = instance()
    keys = {"id", "from", "to", "dir", "trigger", "predicate", "decides"}
    for t in data["transitions"]:
        assert set(t) == keys, (t["id"], set(t) ^ keys)
    for name, stage in data["stages"].items():
        for key in ("required_inputs", "tools", "prompts", "skill_sections"):
            for item in stage[key]:
                assert item.count("(") == item.count(")"), (name, key, item)
