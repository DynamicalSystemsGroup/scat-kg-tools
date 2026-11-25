"""The drawings: what is drawn (read back from the SVG), not pixels alone (WP17 G3, R3)."""

import re
import struct
import sys
import xml.etree.ElementTree as ET

from viewutil import narrative, row, tree_hash

import scat_kg
from scat_kg import draw
from scat_kg.tbox import TBOX

NS = "{http://www.w3.org/2000/svg}"
PNG = b"\x89PNG\r\n\x1a\n"


def texts(svg: str) -> list[tuple[float, float, str]]:
    root = ET.fromstring(svg)
    return [(float(t.get("x")), float(t.get("y")), t.text or "") for t in root.iter(NS + "text")]


def lines(svg: str) -> list[tuple[float, float, bool]]:
    """The edges drawn: (x of one end, x of the other, dashed)."""
    out = []
    for g in ET.fromstring(svg).iter(NS + "g"):
        if not g.get("id", "").startswith("line2d_"):
            continue
        for p in g.iter(NS + "path"):
            nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", p.get("d"))]
            out.append((nums[0], nums[2], "stroke-dasharray" in p.get("style")))
    return out


def columns(svg: str) -> dict[str, list[tuple[float, str]]]:
    """{layer: [(y, label) top to bottom]}, read by the x of each layer's label at the top."""
    ts = texts(svg)
    heads = {t: x for x, _, t in ts if t in TBOX.layers}
    assert list(heads) == list(TBOX.layers)
    assert list(heads.values()) == sorted(heads.values())  # columns in layer order, left to right
    out = {layer: [] for layer in TBOX.layers}
    for x, y, t in ts:
        for layer, hx in heads.items():
            if x == hx and t != layer:
                out[layer].append((y, t))
    return {k: sorted(v) for k, v in out.items()}


def xs(svg: str) -> list[float]:
    return sorted({x for x, _, t in texts(svg) if t in TBOX.layers})


def label(node: dict) -> str:
    return node["name"] if node["status"] == "done" else f"{node['name']} ({node['status']})"


def test_layered_draws_each_node_in_its_layer_column_by_name(vault):
    d = draw.layered(root=vault)
    view = scat_kg.layered(root=vault).to_dict()
    cols = columns(d.svg())
    for layer in TBOX.layers:
        assert [t for _, t in cols[layer]] == [label(n) for n in view["nodes"][layer]]
        names = [n["name"] for n in view["nodes"][layer]]
        assert names == sorted(names)
    assert sum(map(len, cols.values())) == 8  # `idle` has no narrative: not drawn
    assert not any("idle" in t for _, t in [c for col in cols.values() for c in col])


def test_each_edge_is_one_line_between_neighbouring_columns(vault):
    d = draw.layered(root=vault)
    svg = d.svg()
    view = scat_kg.layered(root=vault).to_dict()
    col_x = xs(svg)
    drawn = lines(svg)
    assert len(drawn) == len(view["edges"]) == 8
    for a, b, dashed in drawn:
        assert not dashed
        assert abs(col_x.index(a) - col_x.index(b)) == 1


def test_fingerprint_shows_name_status_and_candidates_dashed(vault):
    d = draw.fingerprint("dry", root=vault)
    svg = d.svg()
    view = scat_kg.fingerprint("dry", root=vault).to_dict()["narratives"][0]
    assert "dry (draft)" in [t for _, _, t in texts(svg)]
    assert "dashed line" in " ".join(t for _, _, t in texts(svg))
    drawn = lines(svg)
    assert len(view["candidates"]) == 1 and len(view["edges"]) == 3
    assert sum(1 for *_, dashed in drawn if dashed) == len(view["candidates"])
    assert sum(1 for *_, dashed in drawn if not dashed) == len(view["edges"])
    col_x = xs(svg)
    assert all(abs(col_x.index(a) - col_x.index(b)) == 1 for a, b, _ in drawn)
    cols = columns(svg)
    assert [t for _, t in cols["group"]] == ["farmers (draft)", "towns (stub)"]


def test_status_is_text_in_the_label_unless_done():
    assert draw._label({"name": "a", "status": "done"}) == "a"
    assert draw._label({"name": "a", "status": "draft"}) == "a (draft)"
    assert draw._label({"name": "a", "status": "stub"}) == "a (stub)"


def test_an_empty_drawing_is_a_labelled_frame_saying_no_nodes(vault):
    for d in (draw.layered([], root=vault), draw.fingerprint("empty", root=vault)):
        svg = d.svg()
        t = [x for _, _, x in texts(svg)]
        assert all(layer in t for layer in TBOX.layers)
    assert "no nodes" in [x for _, _, x in texts(draw.layered([], root=vault).svg())]


def test_a_fingerprint_with_no_nodes_says_so(make):
    v = make({"narrative/bare.md": narrative("Bare", "Nothing is linked.")})
    svg = draw.fingerprint("bare", root=v).svg()
    assert "no nodes" in [x for _, _, x in texts(svg)]
    assert PNG == draw.fingerprint("bare", root=v).png()[:8]


def test_same_call_twice_gives_equal_bytes(vault):
    for call in (
        lambda: draw.layered(root=vault),
        lambda: draw.fingerprint("dry", root=vault),
        lambda: draw.layered([], root=vault),
    ):
        assert call().png() == call().png()
        assert call().svg() == call().svg()


def test_no_date_in_either_image(vault):
    d = draw.layered(root=vault)
    assert not re.search(r"<dc:date>", d.svg())
    png = d.png()
    assert png[:8] == PNG
    assert b"tIME" not in png and b"Software" not in png and b"Creation Time" not in png


def test_png_has_the_expected_size(vault):
    png = draw.layered(root=vault).png()
    w, h = struct.unpack(">II", png[16:24])
    assert (w, h) == (
        1200,
        290,
    )  # four columns of 3 inches; 1.7 inches of margins and a 1.2 inch body


def test_the_figure_grows_with_the_largest_column(make):
    rows = [row("provided-by", "sensor", f"tech-{i:02d}") for i in range(12)]
    v = make({"narrative/many.md": narrative("Many", "Many.", rows, "draft", "scenario")})
    for i in range(12):
        scat_kg.stub(f"tech-{i:02d}", "technology", root=v)
    d = draw.fingerprint("many", root=v)
    w, h = struct.unpack(">II", d.png()[16:24])
    assert w == 1200 and h == round(100 * (1.7 + 0.3 * 12))
    cols = columns(d.svg())
    assert len(cols["technology"]) == 12
    ys = [y for y, _ in cols["technology"]]
    assert len(set(ys)) == 12  # no two labels on one row


def test_a_refusal_is_the_views_refusal(vault):
    for got, want in (
        (draw.fingerprint("nope", root=vault), scat_kg.fingerprint("nope", root=vault)),
        (draw.layered(["nope"], root=vault), scat_kg.layered(["nope"], root=vault)),
        (draw.layered("dry", root=vault), scat_kg.layered("dry", root=vault)),
        (
            draw.fingerprint("dry", root=vault / "gone"),
            scat_kg.fingerprint("dry", root=vault / "gone"),
        ),
    ):
        assert not got.ok and got.to_dict() == want.to_dict()
    assert not draw.fingerprint(None, root=vault).ok


def test_without_matplotlib_the_refusal_says_how_to_get_it(vault, monkeypatch):
    monkeypatch.setitem(sys.modules, "matplotlib", None)  # `import matplotlib` now fails
    for r in (draw.fingerprint("dry", root=vault), draw.layered(root=vault)):
        assert not r.ok
        refused = r.to_dict()["refused"][0]
        assert refused["fix"]["options"][0]["text"] == 'pip install "scat-kg[draw]"'
        assert "pip install" in str(r)


def test_drawing_writes_nothing_but_save(vault, tmp_path):
    before = tree_hash(vault)
    for d in (draw.layered(root=vault), draw.fingerprint("dry", root=vault)):
        d.png(), d.svg(), d._repr_png_()
    assert tree_hash(vault) == before
    out = tmp_path / "out"
    assert not out.exists()
    d.save(out / "a.png")
    assert tree_hash(vault) == before and (out / "a.png").exists()


def test_save_writes_creates_leaves_alone_and_changes(vault, tmp_path):
    d = draw.layered(root=vault)
    f = tmp_path / "x" / "l.svg"
    r = d.save(f)
    assert r.created == (f.as_posix(),) and f.read_text(encoding="utf-8") == d.svg()
    assert d.save(f).unchanged == (f.as_posix(),)
    f.write_text("old")
    assert d.save(f).changed == (f.as_posix(),)
    p = tmp_path / "l.PNG"
    d.save(p)
    assert p.read_bytes() == d.png()


def test_save_shows_a_path_inside_the_vault_from_the_vault(vault):
    r = draw.layered(root=vault).save(vault / "out" / "l.png")
    assert r.created == ("out/l.png",)


def test_save_refuses_with_a_fix(vault, tmp_path):
    d = draw.layered(root=vault)
    (tmp_path / "folder").mkdir()
    (tmp_path / "file").write_text("x")
    for target in (
        tmp_path / "folder",
        tmp_path / "l.pdf",
        tmp_path / "noext",
        tmp_path / "file" / "l.png",  # its parent is a file: not writable
    ):
        r = d.save(target)
        assert not r.ok and "Fix: " in str(r), target
    assert not (tmp_path / "l.pdf").exists() and (tmp_path / "file").read_text() == "x"
