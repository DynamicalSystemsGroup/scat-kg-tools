"""WP23-U3b, G3, R3, R4: the attribution view (`scat attribution`) and the contributor stub, per mode.

The view lists narratives by contributor, in the knowledge graph and not in the layered graph; it refuses where the
mode allows no attribution; Python, the CLI and the MCP tool give the same document; `stub` makes a contributor page
only where the mode enables attribution.
"""

import json
import shutil
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from mcp_server.mcputil import call, put_stage, serve
from test_wp23_contributors import NARRATIVES, PEOPLE, vault, views
from views.viewutil import tree_hash

import scat_kg
from scat_kg.cli import main

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "contracts" / "machine-interface.schema.json").read_text("utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)
ALL = [p.stem for p in NARRATIVES]


def valid(doc):
    return [e.message for e in VALIDATOR.iter_errors(doc)] == []


def narrative_text(root, name, extra=""):
    return (
        (root / "narrative" / f"{name}.md")
        .read_text("utf-8")
        .replace("\n---\n", f"\n{extra}---\n", 1)
    )


# ---- the view, per mode


@pytest.mark.parametrize("mode", ["optional", "required"])
def test_every_narrative_by_every_contributor(tmp_path, mode):
    root = vault(tmp_path, "v", mode, contributors=True, names=True)
    view = scat_kg.attribution(root=root)
    assert view.ok and view.mode == mode
    d = view.to_dict()
    assert (d["kind"], d["operation"], d["ok"], d["mode"], d["schema_version"]) == (
        "view",
        "attribution",
        True,
        mode,
        3,
    )
    assert [c["name"] for c in d["contributors"]] == sorted(PEOPLE)
    assert all(c["narratives"] == sorted(ALL) for c in d["contributors"])
    assert d["contributors"][0] == {
        "name": "ada-quill",
        "title": "Ada-Quill",
        "status": "done",
        "narratives": sorted(ALL),
    }
    assert d["unattributed"] == [] and d["excluded"] == []
    assert valid(d)


def test_a_narrative_naming_none_is_shown_plainly_and_a_contributor_with_none_too(tmp_path):
    root = vault(tmp_path, "v", "optional", contributors=True)
    one = root / "narrative" / f"{ALL[0]}.md"
    one.write_text(narrative_text(root, ALL[0], 'attributed_to: ["[[bo-marsh]]"]\n'), "utf-8")
    d = scat_kg.attribution(root=root).to_dict()
    by = {c["name"]: c["narratives"] for c in d["contributors"]}
    assert by == {"ada-quill": [], "bo-marsh": [ALL[0]], "cy-reed": []}
    assert d["unattributed"] == ALL[1:]
    text = str(scat_kg.attribution(root=root))
    assert "  ada-quill [done]\n    no narrative names this contributor\n" in text
    assert (
        "  narratives that name no contributor\n" + "".join(f"    {n}\n" for n in ALL[1:])
        in text + "\n"
    )
    assert valid(d)


def test_no_contributor_page_and_no_name_is_an_empty_but_real_view_in_optional_mode(tmp_path):
    root = vault(tmp_path, "v", "optional")
    d = scat_kg.attribution(root=root).to_dict()
    assert d["contributors"] == [] and d["unattributed"] == ALL and valid(d)


def test_an_uncoded_narrative_is_excluded_as_in_every_view(tmp_path):
    root = vault(tmp_path, "v", "optional", contributors=True, names=True)
    (root / "narrative" / "loose.md").write_text(
        '---\ntype: narrative\nstatus: stub\ntitle: "Loose"\nattributed_to: ["[[ada-quill]]"]\n---\nNo node here.\n',
        "utf-8",
    )
    d = scat_kg.attribution(root=root).to_dict()
    assert [x["name"] for x in d["excluded"]] == ["loose"]
    assert all("loose" not in c["narratives"] for c in d["contributors"])
    assert "loose" not in d["unattributed"] and valid(d)


def test_disallowed_refuses_in_plain_words_and_is_not_an_empty_list(tmp_path):
    root = vault(tmp_path, "v", "disallowed")
    r = scat_kg.attribution(root=root)
    assert not r.ok and r.mode == "disallowed"
    (ref,) = r.refused
    assert "attribution mode is `disallowed`" in ref.why and "allows no attribution" in ref.why
    assert "scat.toml" in ref.fix
    d = r.to_dict()
    assert d["kind"] == "operation" and d["ok"] is False and "contributors" not in d and valid(d)


def test_a_vault_with_no_usable_mode_refuses_too(tmp_path):
    root = vault(tmp_path, "v", "optional", contributors=True)
    (root / "scat.toml").write_text("stakeholder_group_cap = 3\n", "utf-8")
    r = scat_kg.attribution(root=root)
    assert not r.ok and r.mode is None
    assert "declares no usable attribution mode" in r.refused[0].why
    assert 'attribution = "required"' in r.refused[0].fix and valid(r.to_dict())


def test_switching_the_mode_changes_the_answer(tmp_path):
    root = vault(tmp_path, "v", "optional", contributors=True, names=True)
    assert scat_kg.attribution(root=root).ok
    (root / "scat.toml").write_text(
        'attribution = "disallowed"\nstakeholder_group_cap = 3\n', "utf-8"
    )
    assert not scat_kg.attribution(root=root).ok


def test_the_view_refuses_on_an_error_in_a_page_it_draws(tmp_path):
    # required mode, narratives at `done` that name nobody: SCAT-DONE-ATTR on each
    root = vault(tmp_path, "v", "required", contributors=True)
    r = scat_kg.attribution(root=root)
    assert not r.ok and r.mode == "required"
    assert {p.rule for p in r.problems} == {"SCAT-DONE-ATTR"}
    assert {p.file for p in r.problems} == {
        "narrative/saturday-at-the-lending-desk.md",
        "narrative/self-service-kiosk-pitch.md",
    }  # the draft one only warns
    assert valid(r.to_dict()) and r.to_dict()["problems"][0]["rule"] == "SCAT-DONE-ATTR"
    assert "fix the problems below" in r.refused[0].fix


def test_the_view_refuses_on_an_error_in_a_contributor_page(tmp_path):
    root = vault(tmp_path, "v", "optional", contributors=True, names=True)
    page = root / "contributor" / "ada-quill.md"
    page.write_text(page.read_text("utf-8").replace("status: done", "status: finished"), "utf-8")
    r = scat_kg.attribution(root=root)
    assert not r.ok and "contributor/ada-quill.md" in {p.file for p in r.problems}


def test_an_error_on_a_page_the_view_does_not_draw_does_not_refuse(tmp_path):
    root = vault(tmp_path, "v", "optional", contributors=True, names=True)
    page = root / "concern" / "quick-checkout.md"
    page.write_text(page.read_text("utf-8").replace("status: ", "status: finished #", 1), "utf-8")
    assert scat_kg.attribution(root=root).ok


def test_the_view_writes_nothing(tmp_path):
    root = vault(tmp_path, "v", "optional", contributors=True, names=True)
    before = tree_hash(root)
    scat_kg.attribution(root=root)
    main(["attribution", "--root", str(root)])
    assert tree_hash(root) == before


def test_contributor_pages_are_in_no_layered_view_and_the_views_do_not_change(tmp_path):
    plain = vault(tmp_path, "plain", "optional")
    named = vault(tmp_path, "named", "optional", contributors=True, names=True)
    assert views(named) == views(plain)
    assert scat_kg.attribution(root=plain).to_dict() != scat_kg.attribution(root=named).to_dict()
    assert not any(p in json.dumps(views(named)) for p in PEOPLE)


# ---- CLI and MCP give the Python result


@pytest.mark.parametrize("mode", ["optional", "required", "disallowed"])
def test_the_cli_equals_python(tmp_path, capsys, mode):
    root = vault(tmp_path, "v", mode, contributors=mode != "disallowed", names=mode != "disallowed")
    want = scat_kg.attribution(root=root)
    code = main(["attribution", "--root", str(root), "--json"])
    assert json.loads(capsys.readouterr().out) == want.to_dict() and code == (0 if want.ok else 1)
    code = main(["attribution", "--root", str(root)])
    assert capsys.readouterr().out == str(want) + "\n" and code == (0 if want.ok else 1)


def test_the_mcp_tool_equals_python_in_each_mode(tmp_path):
    for mode in ("optional", "required", "disallowed"):
        on = mode != "disallowed"
        root = vault(tmp_path, f"mcp-{mode}", mode, contributors=on, names=on)
        put_stage(root, "code")
        with serve(root) as url:
            assert call(url, "attribution") == scat_kg.attribution(root=root).to_dict()


# ---- stub makes a contributor page only where the mode enables attribution


@pytest.mark.parametrize("mode", ["optional", "required"])
def test_stub_makes_a_contributor_page_where_the_mode_allows_it(tmp_path, mode):
    root = vault(tmp_path, "v", mode)
    r = scat_kg.stub("dee-park", "contributor", root=root)
    assert r.ok and r.created == ("contributor/dee-park.md",) and r.mode == mode
    assert (root / "contributor" / "dee-park.md").read_text("utf-8") == (
        '---\ntype: contributor\nstatus: stub\ntitle: "Dee park"\n---\n'
    )
    again = scat_kg.stub("dee-park", "contributor", root=root)
    assert again.ok and again.unchanged == ("contributor/dee-park.md",) and not again.created
    if mode == "optional":  # in required mode the done narratives name nobody, so the view refuses
        listed = scat_kg.attribution(root=root).to_dict()
        assert [c["name"] for c in listed["contributors"]] == ["dee-park"]


def test_a_contributor_page_takes_no_part_in_the_group_cap(tmp_path):
    root = vault(tmp_path, "v", "optional")  # three groups at a cap of three
    for name in ("ann-a", "ben-b", "cat-c", "dan-d"):
        assert scat_kg.stub(name, "contributor", root=root).ok
    assert scat_kg.check(root=root).ok
    assert scat_kg.stub("new-group", "group", root=root).refused  # the cap still holds for groups


def test_stub_refuses_a_contributor_page_in_disallowed_mode_and_writes_nothing(tmp_path):
    root = vault(tmp_path, "v", "disallowed")
    before = tree_hash(root)
    r = scat_kg.stub("dee-park", "contributor", root=root)
    assert not r.ok and r.created == () and r.mode == "disallowed"
    (ref,) = r.refused
    assert "attribution mode is `disallowed`" in ref.why and "holds no contributor page" in ref.why
    assert "changes `attribution` in scat.toml" in ref.fix
    assert tree_hash(root) == before and valid(r.to_dict())


def test_stub_refuses_a_contributor_page_where_no_mode_is_declared(tmp_path):
    root = vault(tmp_path, "v", "optional")
    (root / "scat.toml").write_text("stakeholder_group_cap = 3\n", "utf-8")
    r = scat_kg.stub("dee-park", "contributor", root=root)
    assert not r.ok and not (root / "contributor" / "dee-park.md").exists()
    assert "declares no usable attribution mode" in r.refused[0].why


def test_other_stubs_are_the_same_in_every_mode(tmp_path):
    for mode in ("optional", "required", "disallowed"):
        root = vault(tmp_path, f"s-{mode}", mode)
        assert scat_kg.stub("a-concern", "concern", root=root).ok
        assert scat_kg.stub("a-narrative", "narrative", root=root).ok


def test_a_bad_contributor_name_gets_the_derived_stub_command(tmp_path):
    root = vault(tmp_path, "v", "optional")
    r = scat_kg.stub("Dee Park", "contributor", root=root)
    assert not r.ok
    assert "scat stub dee-park --type contributor" in r.refused[0].fix


def test_the_cli_stub_equals_python_in_each_mode(tmp_path, capsys):
    for mode in ("optional", "disallowed"):
        a, b = vault(tmp_path, f"a-{mode}", mode), vault(tmp_path, f"b-{mode}", mode)
        want = scat_kg.stub("dee-park", "contributor", root=a)
        code = main(["stub", "dee-park", "--type", "contributor", "--root", str(b), "--json"])
        assert json.loads(capsys.readouterr().out) == want.to_dict() and code == (
            0 if want.ok else 1
        )


def test_the_mcp_stub_equals_python_in_each_mode(tmp_path):
    for mode in ("optional", "disallowed"):
        a, b = vault(tmp_path, f"ma-{mode}", mode), vault(tmp_path, f"mb-{mode}", mode)
        shutil.rmtree(a / ".gitkeep", ignore_errors=True)
        want = scat_kg.stub("dee-park", "contributor", root=a)
        put_stage(b, "code")
        with serve(b) as url:
            assert call(url, "stub", {"name": "dee-park", "type": "contributor"}) == want.to_dict()
