import shutil

from opsutil import EXAMPLES, fm

from scat_kg.ops import index
from scat_kg.ops.index import TYPES, base_text
from scat_kg.tbox import TBOX
from scat_kg.vault import read_vault

BASES = [f"index/{t}.base" for t in TYPES]


def test_one_base_per_type_in_the_ontologys_order():
    assert TYPES == ("group", "concern", "affordance", "technology", "narrative")
    assert set(TYPES) == set(TBOX.page_types) - {"index"}


def test_index_creates_every_base_in_a_vault_with_none(make_vault, snap, diff):
    root = make_vault({"concern/a.md": fm("concern", "A"), "README.md": "hi\n"})
    before = snap(root)
    r = index(root=root)
    assert r.ok and r.created == tuple(BASES) and not r.unchanged and not r.changed
    assert set(diff(before, snap(root))) == {"index", *BASES}


def test_the_example_bases_are_what_the_tool_writes(example_vault):
    shutil.rmtree(example_vault / "index")
    assert index(root=example_vault).ok
    for rel in BASES:
        mine = (example_vault / rel).read_text(encoding="utf-8")
        assert mine == (EXAMPLES / rel).read_text(encoding="utf-8"), rel


def test_base_text_is_lf_with_one_final_newline_and_the_columns_of_the_contract():
    text = base_text("concern", "templates")
    assert text.endswith("direction: ASC\n") and "\r" not in text and not text.endswith("\n\n")
    assert 'name: "Concerns"' in text and "note.kind" not in text
    n = base_text("narrative", "templates")
    assert n.index("note.description") < n.index("note.kind") < n.index("note.timeframe")
    assert 'name: "Technologies"' in base_text("technology", "templates")


def test_the_filter_follows_the_templates_folder_of_scat_toml(make_vault):
    root = make_vault({"scat.toml": 'stakeholder_group_cap = 3\ntemplates_folder = "skel"\n'})
    index(root=root)
    assert '!file.inFolder("skel")' in (root / "index/group.base").read_text(encoding="utf-8")


def test_an_existing_base_is_never_rewritten(make_vault, snap):
    mine = "filters:\n  and:\n    - 'note.type == \"concern\"'\n"
    root = make_vault({"index/concern.base": mine})
    before = snap(root)
    r = index(root=root)
    assert r.ok and "index/concern.base" in r.unchanged and len(r.created) == 4
    assert (root / "index/concern.base").read_text(encoding="utf-8") == mine
    assert snap(root)["index/concern.base"] == before["index/concern.base"]


def test_index_twice_changes_nothing_the_second_time(make_vault, snap):
    root = make_vault({"concern/a.md": fm("concern", "A")})
    index(root=root)
    before = snap(root)
    r = index(root=root)
    assert r.ok and not r.created and len(r.unchanged) == 5
    assert snap(root) == before


def test_the_current_example_vault_changes_nothing(example_vault, snap):
    before = snap(example_vault)
    r = index(root=example_vault)
    assert r.ok and not r.created and len(r.unchanged) == 5
    assert snap(example_vault) == before


def test_the_bases_are_not_read_as_pages(make_vault):
    root = make_vault({"concern/a.md": fm("concern", "A")})
    index(root=root)
    assert [p.path for p in read_vault(root).pages] == ["concern/a.md"]


def test_a_file_named_index_refuses_and_writes_nothing(make_vault, snap):
    root = make_vault({"index": "a file\n"})
    before = snap(root)
    r = index(root=root)
    assert not r.ok and "rename or move" in str(r) and "Fix:" in str(r)
    assert snap(root) == before


def test_a_folder_in_place_of_a_base_refuses_and_writes_nothing(make_vault, snap):
    root = make_vault({"index/concern.base/x": "y"})
    before = snap(root)
    r = index(root=root)
    assert not r.ok and "index/concern.base" in str(r)
    assert snap(root) == before


def test_a_missing_vault_folder_is_a_refusal(tmp_path):
    r = index(root=tmp_path / "nowhere")
    assert not r.ok and "does not exist" in str(r)
