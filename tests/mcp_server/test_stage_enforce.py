"""WP30-R1, R2, R3: the stage layer lists, refuses and limits as the lifecycle instance says (generated from it)."""

import json
import re

import pytest
from mcputil import changed, snapshot
from test_stage_common import (
    INST,
    SAMPLES,
    STAGE_TOOLS,
    STAGES,
    UNION,
    all_done,
    call_all,
    call_one,
    fix_text,
    go,
    is_stage_refusal,
    valid,
    vault,
)

from scat_tools import guides
from scat_tools.mcp_server import server, stage
from scat_tools.mcp_server.server import build


def test_the_samples_cover_every_tool():
    assert set(SAMPLES) == set(UNION) and len(SAMPLES) == 19


# ---- R1: no stage recorded


def _no_file(root):
    pass


def _no_stage(root):
    (root / "lifecycle.toml").write_text('set_by = "someone"\n', encoding="utf-8")


def _unknown_name(root):
    (root / "lifecycle.toml").write_text('stage = "launch"\nset_by = "x"\n', encoding="utf-8")


def _malformed(root):
    (root / "lifecycle.toml").write_text('stage = "code\n[[\n', encoding="utf-8")


@pytest.mark.parametrize("make", [_no_file, _no_stage, _unknown_name, _malformed])
def test_with_no_usable_stage_every_tool_gives_the_clarification_and_writes_nothing(tmp_path, make):
    root = vault(tmp_path / "v", stage=None)
    make(root)
    before = snapshot(root)
    docs = call_all(root, [(t, SAMPLES[t]) for t in UNION])
    assert snapshot(root) == before
    for tool, doc in zip(UNION, docs, strict=True):
        assert is_stage_refusal(doc, tool), (tool, doc)
        assert valid(doc), tool
        text = json.dumps(doc)
        for name in STAGES:
            assert f"{name}: " in fix_text(doc), (tool, name)
        assert "the person decides" in fix_text(doc)
        assert "set_stage" in text and "not recorded" in text
    if make is _malformed:
        assert "not valid TOML" in docs[0]["refused"][0]["why"]
    if make is _unknown_name:
        assert "'launch'" in docs[0]["refused"][0]["why"]


# ---- R2: the lists, generated from the instance


@pytest.fixture(scope="module")
def listings(tmp_path_factory):
    out = {}
    for name in STAGES:
        root = vault(tmp_path_factory.mktemp(f"list-{name}") / "v", stage=name)

        async def steps(s):
            tools = (await s.list_tools()).tools
            prompts = (await s.list_prompts()).prompts
            resources = (await s.list_resources()).resources
            texts = {str(r.uri): (await s.read_resource(r.uri)).contents[0].text for r in resources}
            return tools, prompts, resources, texts

        out[name] = go(root, steps)
    return out


def test_the_lists_are_the_same_in_every_stage_and_equal_the_instances_union(listings):
    names = {
        n: ([t.name for t in v[0]], [p.name for p in v[1]], [str(r.uri) for r in v[2]])
        for n, v in listings.items()
    }
    assert len({json.dumps(v) for v in names.values()}) == 1
    tools, prompts, resources = names[STAGES[0]]
    assert sorted(tools) == sorted([*UNION, *STAGE_TOOLS]) and len(tools) == 21
    assert sorted(prompts) == sorted({p for s in INST["stages"].values() for p in s["prompts"]})
    assert "scat://assistant-rules" in resources
    assert "scat://guide/index" in resources
    assert all(f"scat://guide/{n}" in resources for n in STAGES)


def _offered(kind, name):
    """The stages whose `tools` or `prompts` list `name`, from the instance."""
    return [n for n, s in INST["stages"].items() if name in s[kind]]


def _said(description):
    m = re.search(r"Stages: (.+?)\.$", description.rstrip())
    assert m, description
    return STAGES if m.group(1) == "all" else m.group(1).split(", ")


def test_each_description_names_exactly_the_stages_that_offer_it(listings):
    tools, prompts, _, _ = listings["code"]
    for t in tools:
        want = STAGES if t.name in STAGE_TOOLS else _offered("tools", t.name)
        assert _said(t.description) == want, t.name
    for p in prompts:
        assert _said(p.description) == _offered("prompts", p.name), p.name
    # the phrase is "all" only for a thing every stage offers, and never repeated
    assert next(t for t in tools if t.name == "check").description.count("Stages:") == 1


def test_the_guides_are_resources_and_the_instructions_are_the_index(listings, tmp_path):
    _, _, _, texts = listings["analyse"]
    for name in ("index", *STAGES):
        assert texts[f"scat://guide/{name}"] == guides.guide_text(name), name
    assert "scat://assistant-rules" in texts
    root = vault(tmp_path / "v")
    assert build(root).instructions == guides.guide_text("index")
    assert build(
        root
    )._mcp_server.create_initialization_options().instructions == guides.guide_text("index")


@pytest.mark.parametrize("name", STAGES)
def test_in_each_stage_the_instances_tools_run_and_every_other_is_refused(tmp_path, name):
    root = vault(tmp_path / "v", stage=name)
    offered = set(INST["stages"][name]["tools"])
    for tool in UNION:
        if tool in offered:
            doc = call_one(root, tool, SAMPLES[tool])
            assert not is_stage_refusal(doc, tool), (name, tool, doc)
            assert valid(doc) or doc["kind"] == "view", (name, tool)
        else:
            before = snapshot(root)
            doc = call_one(root, tool, SAMPLES[tool])
            assert is_stage_refusal(doc, tool), (name, tool)
            assert snapshot(root) == before
    for tool in STAGE_TOOLS:  # the stage tools work in every stage
        assert call_one(root, "which_stage")["stage"] == name


def test_the_input_schemas_are_byte_identical_before_and_after_apply(tmp_path, monkeypatch):
    root = vault(tmp_path / "v")

    def schemas(mcp):
        return {
            n: json.dumps(t.parameters)
            for n, t in mcp._tool_manager._tools.items()
            if n not in STAGE_TOOLS
        }

    with monkeypatch.context() as m:
        m.setattr(stage, "apply", lambda mcp, root: None)
        before = schemas(server.build(root))
    after = schemas(build(root))
    assert before and before == after and len(after) == 19


# ---- R3: out of stage


@pytest.mark.parametrize("name", STAGES)
def test_an_out_of_stage_call_writes_nothing_and_names_the_stages_and_exits(tmp_path, name):
    root = vault(tmp_path / "v", stage=name)
    before = snapshot(root)
    out = [t for t in UNION if t not in INST["stages"][name]["tools"]]
    docs = call_all(root, [(t, SAMPLES[t]) for t in out])
    assert changed(before, snapshot(root)) == set()
    exits = [t["id"] for t in INST["transitions"] if t["from"] == name]
    for tool, doc in zip(out, docs, strict=True):
        assert valid(doc)
        why, fix = doc["refused"][0]["why"], fix_text(doc)
        assert f"`{tool}` is not offered in the {name} stage" in why
        assert ", ".join(_offered("tools", tool)) in fix
        assert "the person's say-so" in fix
        for eid in exits:
            assert eid in fix, (tool, eid)


def test_there_is_no_tool_limit_and_stub_in_plan_makes_any_type(tmp_path):
    assert not hasattr(stage, "LIMITS")
    assert all("tool_limits" not in s for s in INST["stages"].values())
    for n, kind in enumerate(("concern", "group")):
        root = vault(tmp_path / f"v{n}", stage="plan")
        doc = call_one(root, "stub", {"name": f"fresh-{kind}", "type": kind})
        assert doc["ok"] is True and doc["created"] == [f"{kind}/fresh-{kind}.md"]
        assert (root / kind / f"fresh-{kind}.md").is_file()


def test_the_refusals_are_results_not_errors_and_carry_the_mode(tmp_path):
    root = vault(tmp_path / "v", stage="capture")

    async def steps(s):
        res = await s.call_tool("stub", {"name": "x", "type": "group"})
        return res

    res = go(root, steps)
    assert res.isError is False and res.structuredContent == json.loads(res.content[0].text)
    assert res.structuredContent["mode"] == "disallowed"


def test_an_all_done_vault_changes_nothing_here(tmp_path):
    root = vault(tmp_path / "v")
    all_done(root)
    assert call_one(root, "check")["ok"] is True
