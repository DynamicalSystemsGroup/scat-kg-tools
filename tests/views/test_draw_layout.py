"""Legible layouts (WP35): fewer crossings, islands apart, who tells an edge, the same bytes."""

import re
import xml.etree.ElementTree as ET
from itertools import pairwise
from pathlib import Path

import pytest
from test_draw import NS, SHOWN, columns, said, texts
from viewutil import narrative, page, row, write

from scat_kg import draw
from scat_kg.tbox import TBOX

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "contracts" / "examples"
LAB = ROOT / "research" / "range" / "koi" / "vault"  # the lab (range) vault
LAYERS = list(TBOX.layers)


def crossings(order: list[list[str]], edges: list[tuple[str, str]]) -> int:
    """Pairs of lines between neighbouring columns that cross, for columns of names top to bottom.

    Two lines that share a node do not cross. `edges` are pairs of names, in either direction.
    """
    place = {n: (c, i) for c, col in enumerate(order) for i, n in enumerate(col)}
    ends = []
    for a, b in edges:
        (ca, ia), (cb, ib) = sorted([place[a], place[b]])
        assert cb - ca == 1  # only neighbouring columns have lines
        ends.append((ca, ia, ib, a, b))
    return sum(1 for x in ends for y in ends if x[0] == y[0] and x[1] < y[1] and x[2] > y[2])


def drawn_and_named(d) -> tuple[int, int]:
    """Crossings of what is drawn, and of the same drawing with every column in name order."""
    layers = [layer for layer in LAYERS if any(lay == layer for _, lay in d.nodes())]
    by = {layer: [n for n, lay in d.nodes() if lay == layer] for layer in layers}
    edges = [(a, b) for a, b, _ in d.edges()]
    drawn = crossings([by[layer] for layer in layers], edges)
    named = crossings([sorted(by[layer]) for layer in layers], edges)
    return drawn, named


def bands_vault(tmp_path, files: dict[str, str]):
    base = {
        "scat.toml": "attribution = 'disallowed'\nstakeholder_group_cap = 3\n",
    }
    return write(tmp_path / "v", base | files)


def parallel_chains(tmp_path):
    """Two chains a1-c2-f1 and a2-c1-f2, listed so that name order crosses them (and they are two islands)."""
    return bands_vault(
        tmp_path,
        {
            "group/a1.md": page("group", "A1"),
            "group/a2.md": page("group", "A2"),
            "concern/c1.md": page("concern", "C1"),
            "concern/c2.md": page("concern", "C2"),
            "affordance/f1.md": page("affordance", "F1"),
            "affordance/f2.md": page("affordance", "F2"),
            "narrative/n.md": narrative(
                "N",
                "Two chains.",
                [
                    row("holds", "a1", "c2"),
                    row("holds", "a2", "c1"),
                    row("addressed-by", "c2", "f1"),
                    row("addressed-by", "c1", "f2"),
                ],
            ),
        },
    )


def crossed_but_joined(tmp_path):
    """One island whose name order has two crossings: a holds y and z, b holds x and z."""
    return bands_vault(
        tmp_path,
        {
            "group/a.md": page("group", "A"),
            "group/b.md": page("group", "B"),
            "concern/x.md": page("concern", "X"),
            "concern/y.md": page("concern", "Y"),
            "concern/z.md": page("concern", "Z"),
            "narrative/n.md": narrative(
                "N",
                "One island.",
                [
                    row("holds", "a", "y"),
                    row("holds", "a", "z"),
                    row("holds", "b", "x"),
                    row("holds", "b", "z"),
                ],
            ),
        },
    )


@pytest.mark.parametrize("candidates", [False, True])
@pytest.mark.parametrize("which", ["examples", "lab", "fixture"])
def test_a_real_vault_has_no_more_crossings_than_name_order(which, candidates, vault):
    root = {"examples": EXAMPLES, "lab": LAB, "fixture": vault}[which]
    d = draw.layered(candidates=candidates, root=root)
    drawn, named = drawn_and_named(d)
    assert drawn <= named


def test_name_order_has_crossings_to_remove_on_a_hand_built_vault(tmp_path):
    for build, name_count in ((parallel_chains, 2), (crossed_but_joined, 2)):
        d = draw.layered(root=build(tmp_path / build.__name__))
        drawn, named = drawn_and_named(d)
        assert named == name_count and drawn < named


def test_the_crossing_counter_counts_a_crossing_and_not_a_shared_node():
    assert crossings([["a", "b"], ["x", "y"]], [("a", "y"), ("b", "x")]) == 1
    assert crossings([["a", "b"], ["x", "y"]], [("a", "x"), ("b", "y")]) == 0
    assert crossings([["a", "b"], ["x", "y"]], [("a", "x"), ("a", "y"), ("b", "x")]) == 1
    assert crossings([["a", "b"], ["x", "y"]], [("a", "y"), ("a", "x")]) == 0


def test_without_ordering_the_counter_sees_the_old_crossing(tmp_path, monkeypatch):
    # removing the behaviour (no sweeps, so the start order stays) makes this test's claim fail
    root = crossed_but_joined(tmp_path)
    monkeypatch.setattr(draw, "PASSES", 0)
    drawn, named = drawn_and_named(draw.layered(root=root))
    assert drawn == named == 2


def test_nodes_lists_each_column_top_to_bottom_as_drawn(tmp_path):
    d = draw.layered(root=parallel_chains(tmp_path))
    cols = columns(d.svg())
    for layer in LAYERS:
        if cols.get(layer):
            assert [n for n, lay in d.nodes() if lay == layer] == [
                t.split(" (")[0] for _, t in cols[layer]
            ]


# ---------------------------------------------------------------------------------------------------------
# Islands (R2)
# ---------------------------------------------------------------------------------------------------------


def islands(tmp_path):
    """Island one: farmers, water, sensor (3 nodes). Island two: towns, cost (2). `idle` has no line."""
    return bands_vault(
        tmp_path,
        {
            "group/farmers.md": page("group", "Farmers"),
            "group/towns.md": page("group", "Towns"),
            "concern/water.md": page("concern", "Water"),
            "concern/cost.md": page("concern", "Cost"),
            "affordance/sensor.md": page("affordance", "Sensor"),
            "technology/idle.md": page("technology", "Idle"),
            "narrative/one.md": narrative(
                "One",
                "Farmers and water.",
                [row("holds", "farmers", "water"), row("addressed-by", "water", "sensor")],
            ),
            "narrative/two.md": narrative(
                "Two", "Towns and cost.", [row("holds", "towns", "cost")]
            ),
            "narrative/lone.md": narrative("Lone", "Nothing but [[idle]] is said."),
        },
    )


def separators(svg: str) -> list[float]:
    """The y of each thin separator line (a LineCollection that is not a key sample)."""
    out = []
    for g in ET.fromstring(svg).iter(NS + "g"):
        if g.get("id", "").startswith("LineCollection"):
            for p in g.iter(NS + "path"):
                nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", p.get("d"))]
                if "#bbbbbb" in p.get("style"):
                    out.append(nums[1])
    return out


def test_islands_are_bands_one_above_the_other_and_the_lone_nodes_are_last(tmp_path):
    d = draw.layered(root=islands(tmp_path))
    svg = d.svg()
    cols = columns(svg)
    ys = {t.split(" (")[0]: y for col in cols.values() for y, t in col}
    big, small, lone = ["farmers", "water", "sensor"], ["towns", "cost"], ["idle"]
    for band_a, band_b in ((big, small), (small, lone), (big, lone)):
        # in every column that holds nodes of both, a is above b; and no row of a is below a row of b anywhere
        assert max(ys[n] for n in band_a) < min(ys[n] for n in band_b)
    assert len(separators(svg)) == 2
    seps = sorted(separators(svg))
    assert max(ys[n] for n in big) < seps[0] < min(ys[n] for n in small)
    assert max(ys[n] for n in small) < seps[1] < min(ys[n] for n in lone)


def test_the_band_order_is_stable_and_follows_the_rule(tmp_path):
    # two islands of two nodes: the one holding the smaller (layer, name) first
    v = bands_vault(
        tmp_path,
        {
            "group/g1.md": page("group", "G1"),
            "group/g2.md": page("group", "G2"),
            "concern/c1.md": page("concern", "C1"),
            "concern/c2.md": page("concern", "C2"),
            "narrative/n.md": narrative(
                "N", "Two.", [row("holds", "g2", "c1"), row("holds", "g1", "c2")]
            ),
        },
    )
    d = draw.layered(root=v)
    assert [n for n, lay in d.nodes() if lay == "group"] == ["g1", "g2"]
    assert [n for n, lay in d.nodes() if lay == "concern"] == ["c2", "c1"]
    assert d.svg() == draw.layered(root=v).svg()


def test_one_island_has_no_separator_and_the_rows_of_the_ordering_alone(tmp_path):
    svg = draw.layered(root=crossed_but_joined(tmp_path)).svg()
    assert separators(svg) == []
    ys = [y for col in columns(svg).values() for y, _ in col]
    # rows are 0.3 inch apart at 96 px per inch (the svg is in points: 72 per inch), as before
    step = 0.3 * 72
    for col in [c for c in columns(svg).values() if len(c) > 1]:
        gaps = {round(b - a, 1) for (a, _), (b, _) in pairwise(col)}
        assert gaps == {round(step, 1)}
    assert len(ys) == 5


def test_the_figure_is_as_tall_as_the_tallest_column_with_the_gaps(tmp_path):
    import struct

    d = draw.layered(root=islands(tmp_path))
    svg = d.svg()
    ys = [y for col in columns(svg).values() for y, _ in col]
    rows = 3 + 2 * draw.GAP  # three bands of one row each (chains), two gaps
    assert abs((max(ys) - min(ys)) - 0.3 * 72 * (rows - 1)) < 0.5
    _, h = struct.unpack(">II", d.png()[16:24])
    # head 1.1 inch, the body, a footer of two lines (`idle` is an orphan) of 0.6 + 0.17 inch
    assert h == round(100 * (1.1 + max(1.2, 0.3 * rows) + 0.6 + 0.17))


# ---------------------------------------------------------------------------------------------------------
# Marks (R3)
# ---------------------------------------------------------------------------------------------------------


def style(path) -> dict[str, str]:
    """The `style` attribute of an svg path as a dict."""
    return dict(kv.strip().split(": ") for kv in path.get("style").split(";") if ": " in kv)


def line_marks(svg: str) -> list[tuple[float, float, float, float, str, str, str]]:
    """Each edge line as (x1, y1, x2, y2, colour, dash, width); the key's samples are not among them."""
    out = []
    for g in ET.fromstring(svg).iter(NS + "g"):
        if not g.get("id", "").startswith("line2d_"):
            continue
        for p in g.iter(NS + "path"):
            nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", p.get("d"))]
            st = style(p)
            out.append(
                (
                    *nums[:4],
                    st["stroke"].lower(),
                    st.get("stroke-dasharray", "none"),
                    st["stroke-width"],
                )
            )
    return out


def samples(svg: str) -> set[tuple[str, str]]:
    """The (colour, dash) of each key sample: the LineCollections other than separators."""
    out = set()
    for g in ET.fromstring(svg).iter(NS + "g"):
        if g.get("id", "").startswith("LineCollection"):
            for p in g.iter(NS + "path"):
                st = style(p)
                if st["stroke"].lower() != "#bbbbbb":
                    out.add((st["stroke"].lower(), st.get("stroke-dasharray", "none")))
    return out


def ends_of(svg: str, mark) -> tuple[str, str]:
    """The names at the two ends of a line: the nearest label in the column at each end."""
    cols = columns(svg)
    x_of = {}
    for x, _, t in texts(svg):
        for layer in cols:
            if t == SHOWN.get(layer, layer):
                x_of[layer] = x
    names = []
    for x, y in ((mark[0], mark[1]), (mark[2], mark[3])):
        layer = min(x_of, key=lambda lay: abs(x_of[lay] - x))
        names.append(min(cols[layer], key=lambda c: abs(c[0] - y))[1])
    return names[0], names[1]


def marked_by_edge(vault_root, **kw):
    d = draw.layered(mark_narratives=True, root=vault_root, **kw)
    svg = d.svg()
    got = {}
    for m in line_marks(svg):
        a, b = ends_of(svg, m)
        got[frozenset((a.split(" (")[0], b.split(" (")[0]))] = m[4:]
    return d, svg, got


def test_each_edge_has_the_mark_of_the_narrative_that_tells_it(vault):
    from scat_kg import layered

    _, _, got = marked_by_edge(vault)
    view = layered(root=vault).to_dict()
    told = {frozenset((e["from"], e["to"])): e["narratives"] for e in view["edges"]}
    assert set(got) == set(told) and len(got) == 8
    names = sorted(view["narratives"])
    single = {n: set() for n in names}
    for pair, tellers in told.items():
        if len(tellers) == 1:
            single[tellers[0]].add(got[pair])
    for n, marks in single.items():
        assert len(marks) <= 1, n  # every edge of one narrative has one mark
    one = {next(iter(m)) for m in single.values() if m}
    assert len(one) == len([m for m in single.values() if m])  # marks differ between narratives
    shared = {got[p] for p, t in told.items() if len(t) > 1}
    assert len(shared) == 1 and not shared & one  # farmers-water (dry, wet): one shared mark
    colour, dash, width = next(iter(shared))
    assert colour == "#000000" and dash == "none" and float(width) > max(float(m[2]) for m in one)
    # the colours and styles come from the fixed lists
    assert {m[0] for m in one} <= {c.lower() for c in draw.LINE_COLOURS}
    assert all(m[1] != draw.DASH and m[1] != "none" or m[1] == "none" for m in one)


def test_the_key_names_each_narrative_and_the_shared_mark(vault):
    _, svg, got = marked_by_edge(vault)
    keyed = [t for _, _, t in texts(svg)]
    for n in ("diamond", "dry", "split", "wet"):  # `empty` tells no edge
        assert keyed.count(n) == 1, n
    assert "told by more than one narrative" in keyed
    assert "empty" not in keyed
    # the samples in the key are the marks the edges have
    assert {(c, d_) for c, d_, _ in got.values()} <= samples(svg)


def test_marks_are_apart_and_from_the_fixed_lists_for_eight_narratives(tmp_path):
    files = {"group/g.md": page("group", "G")}
    for i in range(8):
        files[f"concern/c{i}.md"] = page("concern", f"C{i}")
        files[f"narrative/n{i}.md"] = narrative(f"N{i}", "One.", [row("holds", "g", f"c{i}")])
    v = bands_vault(tmp_path, files)
    _, _, got = marked_by_edge(v)
    assert len(got) == 8 and len(set(got.values())) == 8
    for colour, _, _ in got.values():
        assert colour in {c.lower() for c in draw.LINE_COLOURS}
    assert {m[1] for m in draw.MARKS} == set(draw.LINE_STYLES)
    assert draw.DASH not in draw.LINE_STYLES
    assert len(set(draw.MARKS)) == len(draw.MARKS) >= 8


def test_a_narrative_gets_the_same_mark_in_name_order_and_the_marks_wrap(tmp_path):
    n = len(draw.MARKS) + 1
    files = {"group/g.md": page("group", "G")}
    for i in range(n):
        files[f"concern/c{i:02d}.md"] = page("concern", f"C{i:02d}")
        files[f"narrative/n{i:02d}.md"] = narrative(
            f"N{i:02d}", "One.", [row("holds", "g", f"c{i:02d}")]
        )
    _, svg, got = marked_by_edge(bands_vault(tmp_path, files))
    assert (
        got[frozenset(("g", "c00"))] == got[frozenset(("g", f"c{n - 1:02d}"))]
    )  # the first mark again
    keyed = [t for _, _, t in texts(svg)]
    assert all(keyed.count(f"n{i:02d}") == 1 for i in range(n))  # the key still names each


def test_marking_is_off_by_default_and_candidates_stay_grey_and_dashed(vault):
    plain = draw.layered(root=vault)
    svg = plain.svg()
    assert not any(t in said(svg) for t in ("told by more than one", "line colour and style"))
    assert {m[4] for m in line_marks(svg)} == {"#4d4d4d"}
    assert samples(svg) == set()
    marked = draw.layered(mark_narratives=True, candidates=True, root=vault)
    cand = [m for m in line_marks(marked.svg()) if m[4] == "#4d4d4d"]
    assert cand and all(m[5] != "none" for m in cand)  # grey lines are the dashed candidates
    assert len(cand) == sum(1 for *_, dashed in marked.edges() if dashed)


def test_the_key_stays_inside_the_figure_and_the_footer_grows(tmp_path, vault):
    import struct

    plain = struct.unpack(">II", draw.layered(root=vault).png()[16:24])
    marked = struct.unpack(">II", draw.layered(mark_narratives=True, root=vault).png()[16:24])
    assert marked[1] > plain[1]
    svg = draw.layered(mark_narratives=True, root=vault).svg()
    height = float(svg.split('height="')[1].split("pt")[0])
    assert all(0 < y < height for _, y, _ in texts(svg))
    body_bottom = max(y for col in columns(svg).values() for y, _ in col)
    key = [y for _, y, t in texts(svg) if t in ("diamond", "dry", "split", "wet")]
    assert min(key) > body_bottom  # the key is under the nodes


def test_marking_does_not_change_a_fingerprint_or_a_trace(vault):
    from scat_kg import fingerprint, trace

    fp = fingerprint("dry", root=vault)
    assert draw.render(fp, mark_narratives=True).svg() == draw.render(fp).svg()
    tr = trace("water", root=vault)
    assert draw.render(tr, mark_narratives=True).svg() == draw.render(tr).svg()


def test_mark_narratives_must_be_true_or_false(vault):
    assert not draw.layered(mark_narratives="yes", root=vault).ok


# ---------------------------------------------------------------------------------------------------------
# Determinism (R4)
# ---------------------------------------------------------------------------------------------------------


def test_the_same_vault_and_call_give_the_same_bytes_with_bands_and_marks(tmp_path):
    for root in (islands(tmp_path / "i"), crossed_but_joined(tmp_path / "c"), EXAMPLES):
        for kw in ({}, {"mark_narratives": True}, {"candidates": True}):
            a, b = draw.layered(root=root, **kw), draw.layered(root=root, **kw)
            assert a.png() == b.png() and a.svg() == b.svg()
