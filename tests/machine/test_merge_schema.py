"""WP24-R8: the schema validates a real merge document, a plan, a refusal and a split plan; each says what it adds."""

import json
import shutil
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

import scat_tools

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / "contracts" / "machine-interface.schema.json").read_text())
PAGE = (ROOT / "contracts" / "machine-interface.md").read_text()
V = Draft202012Validator(SCHEMA)
SOURCE = ROOT / "research" / "node-pages" / "vault" / "required"


@pytest.fixture
def vault(tmp_path):
    shutil.copytree(SOURCE, tmp_path / "v")
    return tmp_path / "v"


def test_the_schema_says_version_3_and_names_the_operations():
    assert SCHEMA["$defs"]["SchemaVersion"]["const"] == 3
    desc = SCHEMA["$defs"]["OperationName"]["description"]
    assert "merge" in desc and "split-plan" in desc


def test_a_plan_and_a_real_merge_validate(vault):
    plan = scat_tools.merge(
        "right-to-be-forgotten", "data-retention", plan=True, root=vault
    ).to_dict()
    V.validate(plan)
    assert plan["plan"] is True and plan["mode"] == "required" and plan["done_narratives"]
    done = scat_tools.merge("right-to-be-forgotten", "data-retention", root=vault).to_dict()
    V.validate(done)
    assert done["plan"] is False and done["removed"] == ["concern/right-to-be-forgotten.md"]
    assert done["links_rewritten"] and done["changed"]


def test_a_refusal_validates(vault):
    d = scat_tools.merge("weekly-digest", "digest-email", root=vault).to_dict()
    V.validate(d)
    assert d["ok"] is False and d["refused"] and "plan" not in d


def test_a_split_plan_validates(vault):
    d = scat_tools.split_plan("community-members", root=vault).to_dict()
    V.validate(d)
    assert d["operation"] == "split-plan" and len(d["pages"]) == 6
    refused = scat_tools.split_plan("nobody", root=vault).to_dict()
    V.validate(refused)


def test_a_document_that_leaves_out_what_merge_adds_is_rejected(vault):
    d = scat_tools.merge("right-to-be-forgotten", "data-retention", plan=True, root=vault).to_dict()
    for key in ("plan", "removed", "done_narratives", "links_rewritten"):
        assert not V.is_valid({k: v for k, v in d.items() if k != key}), key
    s = scat_tools.split_plan("community-members", root=vault).to_dict()
    for key in ("node", "node_type", "pages"):
        assert not V.is_valid({k: v for k, v in s.items() if k != key}), key


def test_the_page_names_every_field_the_schema_adds():
    row = next(r for r in PAGE.splitlines() if r.startswith("| merge, split-plan result"))
    for key in (
        "plan",
        "removed",
        "done_narratives",
        "links_rewritten",
        "node",
        "node_type",
        "pages",
    ):
        assert f"`{key}`" in row
        assert key in SCHEMA["$defs"]["OperationResult"]["properties"]
