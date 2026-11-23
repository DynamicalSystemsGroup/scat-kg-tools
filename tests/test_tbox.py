import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest
from rdflib import Graph

from scat_kg import tbox
from scat_kg.tbox import TBOX

REPO = Path(__file__).parents[1]
TTL = REPO / "ontology" / "scat.ttl"


def test_page_type_slugs():
    assert set(TBOX.page_types) == {
        "stakeholder-group", "concern", "affordance", "technology",
        "heldby", "addresses", "attributes",
        "scenario-raw", "scenario-coded", "architecture-raw", "architecture-coded", "class",
    }  # fmt: skip


def test_descriptions_come_from_the_ttl():
    g = Graph().parse(TTL)
    descriptions = {str(o) for o in g.objects(None, tbox.SCAT.pageDescription)}
    assert {t.description for t in TBOX.page_types.values()} == descriptions
    assert all(t.definition for t in TBOX.page_types.values())


def test_required_optional_discouraged_fields():
    concern = TBOX.page_types["concern"]
    assert [f.key for f in concern.required] == ["description", "status", "title", "type"]
    assert [f.key for f in concern.optional] == ["conflicts"]
    assert concern.field("conflicts").target_type == "concern"
    scenario = TBOX.page_types["scenario-coded"]
    assert [f.key for f in scenario.discouraged] == ["technologies"]
    assert scenario.discouraged_body_links == ("technology",)
    assert TBOX.page_types["architecture-coded"].discouraged_body_links == ("stakeholder-group",)


def test_required_from():
    concern = TBOX.page_types["concern"]
    from_ = {f.key: f.required_from for f in concern.required}
    assert from_ == {"type": "stub", "status": "stub", "title": "stub", "description": "done"}


def test_status_values_and_order():
    assert TBOX.statuses == ("stub", "draft", "done")
    assert TBOX.page_types["class"].carries_status is False
    assert TBOX.page_types["concern"].carries_status is True


def test_link_rules():
    assert TBOX.unlisted_link_level == "error"
    assert TBOX.wrong_target_level == "error"
    group = TBOX.page_types["heldby"].field("group")
    assert (group.is_link, group.single, group.target_type) == (True, True, "stakeholder-group")
    groups = TBOX.page_types["scenario-coded"].field("groups")
    assert (groups.is_link, groups.single) == (True, False)
    assert not TBOX.page_types["concern"].field("title").is_link


def test_relation_endpoint_order():
    assert TBOX.relations == {
        "heldby": ("group", "concern"),
        "addresses": ("concern", "affordance"),
        "attributes": ("affordance", "technology"),
    }
    for slug, (first, second) in TBOX.relations.items():
        relation = TBOX.page_types[slug]
        assert relation.field(first).single and relation.field(second).single
    assert TBOX.page_types["concern"].endpoint_order is None


def test_class_page_indexes_value_set():
    values = TBOX.page_types["class"].field("indexes").value_set
    assert values == (
        "stakeholder-group", "concern", "affordance", "technology",
        "heldby", "addresses", "attributes",
    )  # fmt: skip


def test_loader_reads_the_repo_file_in_a_checkout():
    assert tbox.ttl_text() == TTL.read_text(encoding="utf-8")


def test_wheel_ships_the_repo_file(tmp_path):
    uv = shutil.which("uv")
    if uv is None:
        pytest.skip("uv not available")
    subprocess.run([uv, "build", "--wheel", "--out-dir", str(tmp_path)], cwd=REPO, check=True)
    (wheel,) = tmp_path.glob("*.whl")
    with zipfile.ZipFile(wheel) as z:
        assert z.read("scat_kg/scat.ttl") == TTL.read_bytes()
