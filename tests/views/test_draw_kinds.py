"""A fingerprint drawing follows the narrative's kind; every drawing labels the first column "stakeholder" (WP32)."""

import struct

from test_draw import columns, lines, said, texts
from viewutil import narrative, row

import scat_kg
from scat_kg import draw

ALL = [
    row("holds", "farmers", "water"),
    row("addressed-by", "water", "sensor"),
    row("provided-by", "sensor", "probe"),
]


def heads(svg: str) -> list[str]:
    return list(columns(svg))


def test_an_architecture_has_no_stakeholder_column(vault):
    svg = draw.fingerprint("wet", root=vault).svg()
    assert heads(svg) == ["concern", "affordance", "technology"]
    assert "stakeholder" not in [t for _, _, t in texts(svg)]
    assert struct.unpack(">II", draw.fingerprint("wet", root=vault).png()[16:24])[0] == 900


def test_a_scenario_has_no_technology_column(vault):
    svg = draw.fingerprint("dry", root=vault).svg()
    assert heads(svg) == ["group", "concern", "affordance"]
    assert "technology" not in [t for _, _, t in texts(svg)]
    assert struct.unpack(">II", draw.fingerprint("dry", root=vault).png()[16:24])[0] == 900


def test_a_narrative_with_no_kind_has_all_four_columns_and_no_note(make):
    v = make({"narrative/plain.md": narrative("Plain", "All four.", ALL, "draft")})
    svg = draw.fingerprint("plain", root=v).svg()
    assert heads(svg) == ["group", "concern", "affordance", "technology"]
    assert "column" not in said(svg)
    assert struct.unpack(">II", draw.fingerprint("plain", root=v).png()[16:24])[0] == 1200


def test_a_dropped_columns_nodes_are_still_in_the_views_data(vault):
    wet = scat_kg.fingerprint("wet", root=vault).to_dict()["narratives"][0]
    dry = scat_kg.fingerprint("dry", root=vault).to_dict()["narratives"][0]
    assert [n["name"] for n in wet["nodes"] if n["type"] == "group"] == ["farmers"]
    assert [n["name"] for n in dry["nodes"] if n["type"] == "technology"] == ["probe"]
    assert len(dry["edges"]) == 3


def test_edges_to_a_dropped_column_are_not_drawn(vault):
    assert len(lines(draw.fingerprint("wet", root=vault).svg())) == 1  # holds is not drawn
    assert len(lines(draw.fingerprint("dry", root=vault).svg())) == 2  # provided-by is not drawn


def test_candidates_to_a_dropped_column_are_not_drawn(make):
    # the account links the group `towns` and the concern `water`, but no row joins them: a candidate
    v = make(
        {
            "narrative/arch.md": narrative(
                "Arch",
                "The [[towns]] care about [[water]], met by [[alert]].",
                [row("addressed-by", "water", "alert")],
                "draft",
                "architecture",
            )
        }
    )
    view = scat_kg.fingerprint("arch", candidates=True, root=v).to_dict()["narratives"][0]
    assert any(c["from"] == "towns" for c in view["candidates"])
    svg = draw.fingerprint("arch", candidates=True, root=v).svg()
    assert not any(dashed for *_, dashed in lines(svg))
    assert len(lines(svg)) == 1


def test_the_footer_says_how_many_nodes_were_left_out_and_why(vault, make):
    wet = said(draw.fingerprint("wet", root=vault).svg())
    assert (
        "no stakeholder column: an architecture. 1 stakeholder the narrative links is not drawn."
        in wet
    )
    dry = said(draw.fingerprint("dry", root=vault).svg())
    assert "no technology column: a scenario. 1 technology the narrative links is not drawn." in dry
    v = make(
        {
            "narrative/two.md": narrative(
                "Two",
                "Two.",
                [
                    row("holds", "farmers", "water"),
                    row("holds", "towns", "water"),
                    row("addressed-by", "water", "sensor"),
                    row("provided-by", "sensor", "probe"),
                    row("provided-by", "sensor", "radio"),
                ],
                "draft",
                "scenario",
            ),
            "narrative/two-a.md": narrative(
                "Two a",
                "Two.",
                [row("holds", "farmers", "water"), row("holds", "towns", "water")],
                "draft",
                "architecture",
            ),
        }
    )
    assert "2 technologies the narrative links are not drawn." in said(
        draw.fingerprint("two", root=v).svg()
    )
    assert "2 stakeholders the narrative links are not drawn." in said(
        draw.fingerprint("two-a", root=v).svg()
    )


def test_with_nothing_to_leave_out_the_footer_still_says_there_is_no_such_column(make):
    v = make(
        {
            "narrative/arch.md": narrative(
                "Arch",
                "No group.",
                [row("addressed-by", "water", "alert")],
                "draft",
                "architecture",
            ),
            "narrative/scen.md": narrative(
                "Scen", "No tech.", [row("holds", "farmers", "water")], "draft", "scenario"
            ),
        }
    )
    a = said(draw.fingerprint("arch", root=v).svg())
    s = said(draw.fingerprint("scen", root=v).svg())
    assert "no stakeholder column: an architecture." in a and "not drawn" not in a
    assert "no technology column: a scenario." in s and "not drawn" not in s


def test_a_footer_of_several_lines_has_room_below_the_nodes(vault):
    svg = draw.fingerprint("dry", candidates=True, root=vault).svg()
    ts = texts(svg)
    notes = [(y, t) for _, y, t in ts if "line" in t or "drawn" in t or "column" in t]
    assert len(notes) >= 2  # wrapped
    ys = [y for y, _ in notes]
    assert len(set(ys)) == len(ys)
    nodes = [y for col in columns(svg).values() for y, _ in col]
    assert min(ys) > max(nodes)
    height = float(svg.split('height="')[1].split("pt")[0]) * 96 / 72  # the svg's own height, in px
    assert max(ys) < height


def test_all_three_drawings_label_the_first_column_stakeholder(vault):
    for d in (
        draw.layered(root=vault),
        draw.trace("water", root=vault),
        draw.fingerprint("dry", root=vault),
    ):
        said_ = [t for _, _, t in texts(d.svg())]
        assert said_.count("stakeholder") == 1
        assert "group" not in said_
        assert heads(d.svg())[0] == "group"  # the layer's name inside the code is unchanged
