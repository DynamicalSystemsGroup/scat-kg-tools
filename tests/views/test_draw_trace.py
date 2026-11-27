"""The trace drawing: what is drawn is the trace view's nodes and edges, and the traced node in its own column."""

import json
import sys

import pytest
from test_draw import PNG, columns, lines, texts, xs
from viewutil import tree_hash

import scat_kg
from scat_kg import draw
from scat_kg.cli import main
from scat_kg.tbox import TBOX


def names(svg: str) -> dict[str, list[str]]:
    """{layer: [name, ...]} of the boxes drawn, labels cut back to the name."""
    return {layer: [t.split(" (")[0] for _, t in col] for layer, col in columns(svg).items()}


def reached(vault, node: str, direction: str = "both") -> dict[str, list[str]]:
    """What the trace view says is reached, by layer, with the traced node added in its own layer."""
    data = scat_kg.trace(node, direction, root=vault).to_dict()
    me = scat_kg.evidence(node, root=vault).to_dict()
    out = {layer: [] for layer in TBOX.layers}
    for n in [*data["up"], *data["down"]]:
        out[n["type"]].append(n["name"])
    out[me["node_type"]].append(node)
    return {k: sorted(v) for k, v in out.items()}


@pytest.mark.parametrize("node", ["water", "farmers", "probe", "idle"])
@pytest.mark.parametrize("direction", ["up", "down", "both"])
def test_the_drawing_is_the_views_nodes_and_edges(vault, node, direction):
    svg = draw.trace(node, direction, root=vault).svg()
    view = scat_kg.trace(node, direction, root=vault).to_dict()
    assert names(svg) == reached(vault, node, direction)
    col_x = xs(svg)
    drawn = lines(svg)
    assert len(drawn) == len(view["edges"])
    assert not any(dashed for *_, dashed in drawn)
    assert all(abs(col_x.index(a) - col_x.index(b)) == 1 for a, b, _ in drawn)


def test_a_concern_traces_groups_up_affordances_down_and_technologies_two_down(vault):
    got = names(draw.trace("water", root=vault).svg())
    assert got == {
        "group": ["farmers"],
        "concern": ["water"],
        "affordance": ["alert", "sensor"],
        "technology": ["probe", "radio"],
    }


def test_a_group_traces_concerns_affordances_and_technologies_down(vault):
    got = names(draw.trace("farmers", root=vault).svg())
    assert got == {
        "group": ["farmers"],
        "concern": ["cost", "water"],
        "affordance": ["alert", "sensor"],
        "technology": ["probe", "radio"],
    }


def test_a_technology_traces_affordances_concerns_and_groups_up(vault):
    got = names(draw.trace("probe", root=vault).svg())
    assert got == {
        "group": ["farmers", "towns"],
        "concern": ["cost", "water"],
        "affordance": ["sensor"],
        "technology": ["probe"],
    }


def test_the_traced_node_is_in_its_layers_column_with_its_status_and_the_title_names_it(vault):
    svg = draw.trace("water", root=vault).svg()
    assert [t for _, t in columns(svg)["concern"]] == ["water (draft)"]
    said = [t for _, _, t in texts(svg)]
    assert "trace of concern water, up and down" in said
    assert "trace of concern water, up" in [
        t for _, _, t in texts(draw.trace("water", "up", root=vault).svg())
    ]
    assert "trace of concern water, down" in [
        t for _, _, t in texts(draw.trace("water", "down", root=vault).svg())
    ]


def test_direction_restricts_the_drawing(vault):
    assert names(draw.trace("water", "up", root=vault).svg()) == {
        "group": ["farmers"],
        "concern": ["water"],
        "affordance": [],
        "technology": [],
    }
    assert names(draw.trace("water", "down", root=vault).svg()) == {
        "group": [],
        "concern": ["water"],
        "affordance": ["alert", "sensor"],
        "technology": ["probe", "radio"],
    }
    assert names(draw.trace("idle", root=vault).svg())["technology"] == ["idle"]


@pytest.mark.parametrize(
    "args",
    [("nope",), ("dry",), ("water", "sideways"), ("farmers", "")],
)
def test_a_refusal_is_the_views_refusal(vault, args):
    got = draw.trace(*args, root=vault)
    assert not isinstance(got, draw.Drawing) and not got.ok
    assert got.to_dict() == scat_kg.trace(*args, root=vault).to_dict()


def test_a_missing_vault_is_the_views_refusal(vault):
    got = draw.trace("water", root=vault / "gone")
    assert not got.ok and got.to_dict() == scat_kg.trace("water", root=vault / "gone").to_dict()


def test_same_call_twice_gives_equal_bytes(vault):
    assert draw.trace("water", root=vault).png() == draw.trace("water", root=vault).png()
    assert draw.trace("water", root=vault).svg() == draw.trace("water", root=vault).svg()
    assert draw.trace("water", root=vault).png().startswith(PNG)


def test_without_matplotlib_the_refusal_says_how_to_get_it(vault, monkeypatch):
    monkeypatch.setitem(sys.modules, "matplotlib", None)
    r = draw.trace("water", root=vault)
    assert not r.ok
    assert r.to_dict()["refused"][0]["fix"]["options"][0]["text"] == 'pip install "scat-kg[draw]"'


def run(capsys, argv):
    code = main(argv)
    return code, capsys.readouterr().out


@pytest.mark.parametrize("suffix", ["png", "svg"])
def test_the_cli_writes_the_file_the_twin_draws_and_its_json_document(vault, capsys, suffix):
    out = vault / "img" / f"t.{suffix}"
    argv = ["draw", "trace", "water", "--out", str(out), "--root", str(vault), "--json"]
    code, text = run(capsys, argv)
    doc = json.loads(text)
    assert code == 0 and doc["operation"] == "draw" and doc["ok"] is True
    assert doc["created"] == [f"img/t.{suffix}"]
    d = draw.trace("water", root=vault)
    assert out.read_bytes() == (d.png() if suffix == "png" else d.svg().encode())
    code, text = run(capsys, argv)
    assert json.loads(text)["unchanged"] == [f"img/t.{suffix}"]


def test_the_cli_direction_flag_defaults_to_both(vault, tmp_path, capsys):
    a, b = tmp_path / "a.svg", tmp_path / "b.svg"
    assert run(capsys, ["draw", "trace", "water", "--out", str(a), "--root", str(vault)])[0] == 0
    argv = ["draw", "trace", "water", "--direction", "up", "--out", str(b), "--root", str(vault)]
    assert run(capsys, argv)[0] == 0
    assert a.read_text() == draw.trace("water", root=vault).svg()
    assert b.read_text() == draw.trace("water", "up", root=vault).svg()


@pytest.mark.parametrize(
    "argv",
    [
        ["draw", "trace", "nope", "--out", "{tmp}/a.png"],
        ["draw", "trace", "dry", "--out", "{tmp}/a.png"],
        ["draw", "trace", "water", "--direction", "sideways", "--out", "{tmp}/a.png"],
    ],
)
def test_the_cli_refuses_with_exit_1_and_writes_nothing(vault, tmp_path, capsys, argv):
    argv = [a.replace("{tmp}", str(tmp_path)) for a in argv]
    before = tree_hash(vault), sorted(p.name for p in tmp_path.iterdir())
    code, text = run(capsys, [*argv, "--root", str(vault)])
    assert code == 1 and "Fix:" in text
    assert (tree_hash(vault), sorted(p.name for p in tmp_path.iterdir())) == before
