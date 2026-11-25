"""A page whose frontmatter cannot be read is named by every whole-vault view, never silently left out."""

import pytest
from viewutil import base_files, tree_hash, write

import scat_kg
from scat_kg.graph import load

PATH = "narrative/broken.md"
BROKEN = "---\ntype: narrative\ntitle: [unclosed\n---\nThe [[water]] ran out.\n"

VIEWS = {
    "edge_table": lambda r: scat_kg.edge_table("holds", root=r),
    "layered": lambda r: scat_kg.layered(root=r),
    "trace": lambda r: scat_kg.trace("farmers", root=r),
    "fingerprint": lambda r: scat_kg.fingerprint(root=r),
}


def build(tmp_path):
    return write(tmp_path / "v", base_files() | {PATH: BROKEN})


def test_the_graph_records_the_unreadable_page(tmp_path):
    g = load(build(tmp_path))
    assert [u.path for u in g.unreadable] == [PATH]
    assert g.unreadable[0].reason
    assert load(write(tmp_path / "ok", base_files())).unreadable == ()


@pytest.mark.parametrize("view", VIEWS)
def test_whole_vault_views_refuse_naming_the_file(tmp_path, view):
    root = build(tmp_path)
    before = tree_hash(root)
    out = VIEWS[view](root)
    assert not out.ok
    refused = out.to_dict()["refused"]
    assert [r["subject"] for r in refused] == [PATH]
    assert "frontmatter cannot be read" in refused[0]["why"]
    assert PATH in refused[0]["fix"]["options"][0]["text"]
    assert tree_hash(root) == before


def test_a_view_of_named_narratives_is_not_a_whole_vault_view(tmp_path):
    root = write(tmp_path / "v", base_files() | {PATH: BROKEN})
    assert scat_kg.layered(["dry"], root=root).ok
