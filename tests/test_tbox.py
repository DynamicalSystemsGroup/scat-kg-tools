import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest
from rdflib import Graph

from scat_tools import tbox
from scat_tools.tbox import TBOX

REPO = Path(__file__).parents[1]
TTL = REPO / "ontology" / "scat.ttl"


def test_page_type_slugs():
    assert set(TBOX.page_types) == {
        "group", "concern", "affordance", "technology", "narrative", "contributor", "index",
    }  # fmt: skip


def test_descriptions_come_from_the_ttl():
    g = Graph().parse(TTL)
    descriptions = {str(o) for o in g.objects(None, tbox.SCAT.pageDescription)}
    assert {t.description for t in TBOX.page_types.values()} == descriptions
    assert all(t.definition for t in TBOX.page_types.values())


def test_required_and_optional_fields():
    concern = TBOX.page_types["concern"]
    assert [f.key for f in concern.required] == ["description", "status", "title", "type"]
    assert concern.optional == ()
    narrative = TBOX.page_types["narrative"]
    assert [f.key for f in narrative.required] == [
        "description", "status", "timeframe", "title", "type",
    ]  # fmt: skip
    assert [f.key for f in narrative.optional] == ["attributed_to", "kind"]
    link = narrative.field("attributed_to")
    assert (link.required_from, link.value_set, link.target_type) == ("done", None, "contributor")
    assert all(
        f.target_type is None for t in TBOX.page_types.values() for f in t.fields if f is not link
    )
    contributor = TBOX.page_types["contributor"]  # outside the four layers: no node, no edge type
    assert [f.key for f in contributor.required] == ["status", "title", "type"]
    assert contributor.optional == () and contributor.table is None
    assert "contributor" not in TBOX.layers
    assert narrative.field("kind").value_set == ("scenario", "architecture")
    assert narrative.field("timeframe").value_set == ("past", "future", "mixed")


def test_required_from():
    concern = TBOX.page_types["concern"]
    from_ = {f.key: f.required_from for f in concern.required}
    assert from_ == {"type": "stub", "status": "stub", "title": "stub", "description": "done"}
    narrative = TBOX.page_types["narrative"]
    assert narrative.field("timeframe").required_from == "done"


def test_status_values_and_order():
    assert TBOX.statuses == ("stub", "draft", "done")
    assert TBOX.page_types["index"].carries_status is False
    assert TBOX.page_types["concern"].carries_status is True
    assert TBOX.page_types["index"].fields == ()


def test_edge_types_with_slug_verb_and_ends():
    assert {s: (e.verb, e.from_type, e.to_type, e.label) for s, e in TBOX.edge_types.items()} == {
        "holds": ("holds", "group", "concern", "holds"),
        "addressed-by": ("is addressed by", "concern", "affordance", "is addressed by"),
        "provided-by": ("is provided by", "affordance", "technology", "is provided by"),
    }
    assert list(TBOX.edge_types) == ["holds", "addressed-by", "provided-by"]  # in layer order
    assert TBOX.layers == ("group", "concern", "affordance", "technology")
    assert TBOX.edge_type_named("IS  addressed by") is None  # a spelling is exact but for case
    assert TBOX.edge_type_named("Is Addressed By").slug == "addressed-by"
    assert TBOX.edge_type_named("provided-by").verb == "is provided by"
    assert TBOX.edge_type_named("owns") is None
    assert TBOX.edge_type_between("concern", "affordance").slug == "addressed-by"
    assert TBOX.edge_type_between("group", "affordance") is None


def test_the_table_is_read_from_the_narrative():
    assert TBOX.table_type.slug == "narrative"
    assert TBOX.table.heading == "Edges told"
    assert [(c.name, c.holds) for c in TBOX.table.columns] == [
        ("from", "from"), ("type", "edge-type"), ("to", "to"), ("note", "note"),
    ]  # fmt: skip
    assert [t.slug for t in TBOX.page_types.values() if t.table] == ["narrative"]


def test_loader_reads_the_repo_file_in_a_checkout():
    assert tbox.ttl_text() == TTL.read_text(encoding="utf-8")


def test_wheel_ships_the_repo_file(tmp_path):
    uv = shutil.which("uv")
    if uv is None:
        pytest.skip("uv not available")
    subprocess.run([uv, "build", "--wheel", "--out-dir", str(tmp_path)], cwd=REPO, check=True)
    (wheel,) = tmp_path.glob("*.whl")
    with zipfile.ZipFile(wheel) as z:
        assert z.read("scat_tools/scat.ttl") == TTL.read_bytes()
