"""`scat draw`: the CLI twin of the drawings; its result is an ordinary operation document (R-3, R-8)."""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from viewutil import tree_hash

from scat_kg import draw
from scat_kg.cli import main

SCHEMA = json.loads(
    (Path(__file__).resolve().parents[2] / "contracts" / "machine-interface.schema.json").read_text(
        encoding="utf-8"
    )
)


def run(capsys, argv):
    code = main(argv)
    return code, capsys.readouterr().out


def test_draw_fingerprint_candidates_flag_draws_the_dashed_lines(vault, capsys):
    plain, dashed = vault / "img" / "plain.svg", vault / "img" / "dashed.svg"
    for out, extra in ((plain, []), (dashed, ["--candidates"])):
        code, _ = run(
            capsys,
            ["draw", "fingerprint", "dry", *extra, "--out", str(out), "--root", str(vault)],
        )
        assert code == 0
    assert plain.read_text() == draw.fingerprint("dry", root=vault).svg()
    assert dashed.read_text() == draw.fingerprint("dry", candidates=True, root=vault).svg()
    assert "stroke-dasharray" not in plain.read_text()
    assert "stroke-dasharray" in dashed.read_text()


def valid(doc):
    errors = [e.message for e in Draft202012Validator(SCHEMA).iter_errors(doc)]
    assert not errors, errors


@pytest.mark.parametrize("suffix", ["png", "svg"])
def test_fingerprint_writes_the_file_the_twin_draws(vault, tmp_path, capsys, suffix):
    out = (
        vault / "img" / f"fp.{suffix}"
    )  # inside the vault: the path is vault-relative (the schema)
    code, text = run(
        capsys, ["draw", "fingerprint", "dry", "--out", str(out), "--root", str(vault), "--json"]
    )
    doc = json.loads(text)
    valid(doc)
    assert code == 0 and doc["kind"] == "operation" and doc["operation"] == "draw"
    assert doc["created"] == [f"img/fp.{suffix}"]
    d = draw.fingerprint("dry", root=vault)
    assert out.read_bytes() == (d.png() if suffix == "png" else d.svg().encode())
    # again: nothing changes, and the document says so
    code, text = run(
        capsys, ["draw", "fingerprint", "dry", "--out", str(out), "--root", str(vault), "--json"]
    )
    again = json.loads(text)
    valid(again)
    assert again["unchanged"] == [f"img/fp.{suffix}"] and again["created"] == []
    assert again == d.save(out).to_dict()


def test_layered_with_and_without_the_flag(vault, tmp_path, capsys):
    a, b = tmp_path / "all.svg", tmp_path / "some.svg"
    assert run(capsys, ["draw", "layered", "--out", str(a), "--root", str(vault)])[0] == 0
    argv = ["draw", "layered", "--narrative", "dry", "--narrative", "split"]
    assert run(capsys, [*argv, "--out", str(b), "--root", str(vault)])[0] == 0
    assert a.read_text(encoding="utf-8") == draw.layered(root=vault).svg()
    assert b.read_text(encoding="utf-8") == draw.layered(["dry", "split"], root=vault).svg()


def test_text_is_the_twins_text(vault, tmp_path, capsys):
    out = tmp_path / "l.png"
    _, text = run(capsys, ["draw", "layered", "--out", str(out), "--root", str(vault)])
    assert text == f"created {out.as_posix()}\n"


@pytest.mark.parametrize(
    "argv",
    [
        ["draw", "fingerprint", "nope", "--out", "{tmp}/a.png"],
        ["draw", "layered", "--narrative", "nope", "--out", "{tmp}/a.png"],
        ["draw", "layered", "--out", "{tmp}/a.pdf"],
        ["draw", "layered", "--out", "{tmp}"],
    ],
)
def test_a_refusal_has_a_fix_and_exit_1_and_writes_nothing(vault, tmp_path, capsys, argv):
    argv = [a.replace("{tmp}", str(tmp_path)) for a in argv]
    before = tree_hash(vault), sorted(p.name for p in tmp_path.iterdir())
    code, text = run(capsys, [*argv, "--root", str(vault), "--json"])
    doc = json.loads(text)
    valid(doc)
    assert code == 1 and doc["ok"] is False and doc["refused"]
    code, text = run(capsys, [*argv, "--root", str(vault)])
    assert "Fix:" in text
    assert (tree_hash(vault), sorted(p.name for p in tmp_path.iterdir())) == before


def test_out_is_required(vault, capsys):
    for argv in (["draw", "fingerprint", "dry"], ["draw", "layered"]):
        with pytest.raises(SystemExit) as e:
            main([*argv, "--root", str(vault)])
        assert e.value.code == 2
