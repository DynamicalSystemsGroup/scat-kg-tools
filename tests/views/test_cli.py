"""The CLI twins of the views and of the export: `--json` equals `to_dict()`, the text equals `str()` (R-3, R-8)."""

import json

import pytest
from viewutil import tree_hash

import scat_tools
from scat_tools.cli import main

# (the command line, without --root and --json) -> the REPL call it is the twin of
TWINS = {
    "fingerprint": (["fingerprint"], lambda r: scat_tools.fingerprint(root=r)),
    "fingerprint-one": (["fingerprint", "dry"], lambda r: scat_tools.fingerprint("dry", root=r)),
    "fingerprint-candidates": (
        ["fingerprint", "dry", "--candidates"],
        lambda r: scat_tools.fingerprint("dry", candidates=True, root=r),
    ),
    "fingerprint-all-candidates": (
        ["fingerprint", "--candidates"],
        lambda r: scat_tools.fingerprint(candidates=True, root=r),
    ),
    "edges": (["edges", "holds"], lambda r: scat_tools.edge_table("holds", root=r)),
    "layered": (["layered"], lambda r: scat_tools.layered(None, root=r)),
    "layered-some": (
        ["layered", "--narrative", "dry", "--narrative", "split"],
        lambda r: scat_tools.layered(["dry", "split"], root=r),
    ),
    "trace": (["trace", "farmers"], lambda r: scat_tools.trace("farmers", root=r)),
    "trace-up": (
        ["trace", "sensor", "--direction", "up"],
        lambda r: scat_tools.trace("sensor", "up", root=r),
    ),
    "refusal-name": (["fingerprint", "nope"], lambda r: scat_tools.fingerprint("nope", root=r)),
    "refusal-type": (["edges", "loves"], lambda r: scat_tools.edge_table("loves", root=r)),
    "refusal-direction": (
        ["trace", "farmers", "--direction", "sideways"],
        lambda r: scat_tools.trace("farmers", "sideways", root=r),
    ),
}


def run(capsys, argv):
    code = main(argv)
    return code, capsys.readouterr().out


@pytest.mark.parametrize("name", TWINS)
def test_json_equals_to_dict_and_text_equals_str(vault, capsys, name):
    argv, twin = TWINS[name]
    want = twin(vault)
    code, out = run(capsys, [*argv, "--root", str(vault), "--json"])
    assert json.loads(out) == want.to_dict()
    assert code == (0 if want.ok else 1)
    code, out = run(capsys, [*argv, "--root", str(vault)])
    assert out == str(want) + "\n"
    assert code == (0 if want.ok else 1)


def test_fingerprint_candidates_only_with_the_flag(vault, capsys):
    _, out = run(capsys, ["fingerprint", "dry", "--root", str(vault), "--json"])
    assert "candidates" not in json.loads(out)["narratives"][0]
    assert "candidate" not in run(capsys, ["fingerprint", "dry", "--root", str(vault)])[1]
    _, out = run(capsys, ["fingerprint", "dry", "--candidates", "--root", str(vault), "--json"])
    assert json.loads(out)["narratives"][0]["candidates"] == [
        {"type": "holds", "from": "towns", "to": "water"}
    ]
    assert (
        "candidates (linked, no row)"
        in run(capsys, ["fingerprint", "dry", "--candidates", "--root", str(vault)])[1]
    )


def test_layered_without_the_flag_is_the_whole_vault_not_an_empty_view(vault, capsys):
    _, out = run(capsys, ["layered", "--root", str(vault), "--json"])
    names = json.loads(out)["narratives"]
    assert names == [n.name for n in scat_tools.load(vault).narratives]
    assert len(names) == 5


def test_export_edges_json_equals_to_dict(tmp_path, vault, capsys):
    out = tmp_path / "tables"
    code, text = run(capsys, ["export-edges", "--out", str(out), "--root", str(vault), "--json"])
    first = json.loads(text)
    assert code == 0 and len(first["created"]) == 6
    # the same call again, through the REPL: nothing is written, and the document is the CLI's
    again = scat_tools.export_edges(out, root=vault)
    code, text = run(capsys, ["export-edges", "--out", str(out), "--root", str(vault), "--json"])
    assert json.loads(text) == again.to_dict()
    assert again.to_dict()["unchanged"] == first["created"]


def test_export_edges_needs_out(vault, capsys):
    with pytest.raises(SystemExit) as e:
        main(["export-edges", "--root", str(vault)])
    assert e.value.code == 2


@pytest.mark.parametrize("name", [n for n in TWINS if not n.startswith("export")])
def test_a_view_command_writes_nothing(vault, capsys, name):
    before = tree_hash(vault)
    run(capsys, [*TWINS[name][0], "--root", str(vault), "--json"])
    run(capsys, [*TWINS[name][0], "--root", str(vault)])
    assert tree_hash(vault) == before


def test_export_edges_refusal_writes_nothing_through_the_cli(make, tmp_path, capsys):
    from viewutil import page

    root = make({"concern/water.md": page("concern", "W", "bogus")})
    out = tmp_path / "tables"
    before = tree_hash(root)
    code, text = run(capsys, ["export-edges", "--out", str(out), "--root", str(root), "--json"])
    assert code == 1 and json.loads(text)["ok"] is False
    assert not out.exists()
    assert tree_hash(root) == before
