"""The loader and the table-row seam (M1): the knowledge graph, the reading of a narrative's table, the builders.

The contract is `contracts/page-contracts.md` (4, "Reading the table"); every rule of it has a test here. The
loader returns problems as data and judges nothing: these tests read what it returns, never a message.
"""

import copy
from pathlib import Path

import pytest

from scat_tools.fix import Edit
from scat_tools.graph import (
    Candidate,
    EdgeKey,
    add_row,
    derived_status,
    format_row,
    load,
    read_table,
    remove_rows,
)
from scat_tools.tbox import TBOX

EXAMPLES = Path(__file__).parents[1] / "contracts" / "examples"
NBSP = " "


def node(type_, name):
    return f'---\ntype: {type_}\nstatus: done\ntitle: "{name}"\ndescription: "d."\n---\n'


def narrative(body, status="draft", extra=""):
    return f'---\ntype: narrative\n{extra}status: {status}\ntitle: "N"\n---\n{body}'


NODES = {
    "group/g.md": node("group", "g"),
    "group/g2.md": node("group", "g2"),
    "concern/c.md": node("concern", "c"),
    "concern/c2.md": node("concern", "c2"),
    "affordance/a.md": node("affordance", "a"),
    "technology/t.md": node("technology", "t"),
}
HEAD = "| from | type | to | note |\n|---|---|---|---|\n"


CODED = "\n[[c]]\n"  # a narrative that links no node page is excluded (WP21-G2): code it, after the body


def vault(make_vault, body, **more):
    return make_vault({**NODES, "narrative/n.md": narrative(body + CODED), **more})


def table_of(make_vault, body):
    g = load(vault(make_vault, body))
    return g.narrative("n")


def rows_of(make_vault, body):
    return table_of(make_vault, body).rows


def edges_of(make_vault, body):
    return table_of(make_vault, body).edges


def lines(text):
    return text.split("\n")


# ---------------------------------------------------------------------------------------------------------
# the example vault
# ---------------------------------------------------------------------------------------------------------


def test_example_vault_nodes_by_layer():
    g = load(EXAMPLES)
    assert g.ok and g.refusal is None
    assert list(g.nodes) == [
        "group",
        "concern",
        "affordance",
        "technology",
    ]  # the TBox's layer order
    assert {k: [n.name for n in v] for k, v in g.nodes.items()} == {
        "group": ["borrowers", "funders", "volunteer-staff"],
        "concern": ["careful-record-keeping", "quick-checkout", "safe-handling-of-tools"],
        "affordance": ["safety-briefing", "self-checkout"],
        "technology": ["barcode-scanner", "booking-app"],
    }
    assert g.node("funders").status == "stub" and g.node("funders").path == "group/funders.md"
    assert g.node("self-checkout").title == "Self-checkout"
    assert g.node("saturday-at-the-lending-desk") is None  # a narrative is not a node


def test_example_vault_edges_narratives_and_derived_status():
    g = load(EXAMPLES)
    got = {(e.type, e.from_node, e.to_node): (e.narratives, e.status) for e in g.edges}
    sat, pitch, meet = (
        "saturday-at-the-lending-desk",
        "self-service-kiosk-pitch",
        "funders-meeting",
    )
    assert got == {
        ("holds", "borrowers", "quick-checkout"): ((sat,), "done"),
        ("holds", "borrowers", "safe-handling-of-tools"): ((sat,), "done"),
        ("holds", "funders", "careful-record-keeping"): ((meet,), "draft"),
        ("holds", "volunteer-staff", "careful-record-keeping"): ((sat,), "done"),
        ("holds", "volunteer-staff", "safe-handling-of-tools"): ((sat,), "done"),
        ("addressed-by", "quick-checkout", "self-checkout"): ((sat, pitch), "done"),
        ("addressed-by", "safe-handling-of-tools", "safety-briefing"): ((pitch,), "done"),
        ("provided-by", "self-checkout", "barcode-scanner"): ((pitch,), "done"),
        ("provided-by", "self-checkout", "booking-app"): ((pitch,), "done"),
    }
    assert [(e.type, e.from_node, e.to_node) for e in g.edges] == list(
        got
    )  # layer order, then names
    two = g.edge("addressed-by", "quick-checkout", "self-checkout")
    assert [(t.narrative, t.note) for t in two.tellings] == [
        (sat, "Asked for, not yet there."),
        (pitch, "Would cut the queue to a scan."),
    ]  # one edge, two tellings, each with its own note
    assert g.edge("holds", "funders", "quick-checkout") is None


def test_example_vault_narratives_and_their_fingerprints():
    g = load(EXAMPLES)
    assert [n.name for n in g.narratives] == [
        "funders-meeting", "saturday-at-the-lending-desk", "self-service-kiosk-pitch",
    ]  # fmt: skip
    sat = g.narrative("saturday-at-the-lending-desk")
    assert (sat.status, sat.kind, sat.timeframe) == ("done", "scenario", "past")
    assert sat.nodes == (
        "borrowers", "volunteer-staff",
        "careful-record-keeping", "quick-checkout", "safe-handling-of-tools",
        "safety-briefing", "self-checkout",
    )  # fmt: skip
    assert len(sat.edges) == 5 and sat.problems == ()
    pitch = g.narrative("self-service-kiosk-pitch")
    assert pitch.kind == "architecture" and len(pitch.edges) == 4
    meet = g.narrative("funders-meeting")
    assert (meet.status, meet.kind, meet.timeframe) == ("draft", None, None)
    assert meet.edges == (EdgeKey("holds", "funders", "careful-record-keeping"),)


def test_example_vault_candidates_include_the_pair_the_readme_names():
    g = load(EXAMPLES)
    pair = Candidate(
        "saturday-at-the-lending-desk", "addressed-by", "safe-handling-of-tools", "safety-briefing"
    )
    assert pair in g.candidates
    # told by the pitch, linked in both ends by the scenario with no row there: a candidate, no message
    assert g.edge("addressed-by", "safe-handling-of-tools", "safety-briefing") is not None
    assert len(g.candidates) == 12
    assert (
        Candidate("funders-meeting", "holds", "funders", "careful-record-keeping")
        not in g.candidates
    )
    told = {(n.name, k) for n in g.narratives for k in n.edges}
    assert not any(
        (c.narrative, EdgeKey(c.type, c.from_node, c.to_node)) in told for c in g.candidates
    )
    assert list(g.candidates) == sorted(
        g.candidates,
        key=lambda c: (list(TBOX.edge_types).index(c.type), c.from_node, c.to_node, c.narrative),
    )


def test_example_vault_links_are_kept_apart_from_edges():
    g = load(EXAMPLES)
    assert len(g.links) == 37 == sum(len(p.links) for p in g.vault.pages)
    careful = [l for l in g.links if l.source == "concern/careful-record-keeping.md"]
    assert [(l.target, l.line, l.column) for l in careful] == [("quick-checkout", 8, 15)]
    assert (
        g.edge("holds", "careful-record-keeping", "quick-checkout") is None
    )  # an annotation is no edge
    assert g.summary() == {
        "nodes": {"group": 3, "concern": 3, "affordance": 2, "technology": 2},
        "narratives": 3,
        "excluded": 0,
        "edges": 9,
        "edge_status": {"stub": 0, "draft": 1, "done": 8},
        "candidates": 12,
        "links": 37,
    }


def test_example_rows_carry_what_a_fix_needs():
    g = load(EXAMPLES)
    pitch = g.narrative("self-service-kiosk-pitch")
    first = pitch.rows[0]
    assert (first.n, first.line, first.type_text, first.edge_type) == (
        1,
        16,
        "addressed-by",
        "addressed-by",
    )
    assert (first.from_text, first.to_text) == ("[[quick-checkout]]", "[[self-checkout|the kiosk]]")
    assert (first.from_target, first.to_target) == ("quick-checkout", "self-checkout")
    assert first.note == "Would cut the queue to a scan." and first.well_formed and first.closed
    text = (
        (EXAMPLES / "narrative/self-service-kiosk-pitch.md").read_text().split("\n")[first.line - 1]
    )
    assert first.text == text and text[first.column - 1] == "|"
    for cell in first.cells:  # a cell's offsets cut its content out of the line as written
        assert (
            text[cell.start : cell.end] == cell.raw and text[cell.column - 1 : cell.end] == cell.raw
        )
    assert first.cells[2].raw == r"[[self-checkout\|the kiosk]]"  # as written
    assert first.cells[2].text == "[[self-checkout|the kiosk]]"  # as read
    assert first.cells[2].links == ("self-checkout",)
    meet = g.narrative("funders-meeting").rows[0]
    assert meet.note == "Wants the counts for the annual report | audit."  # `\|` read as a bar
    assert meet.cells[3].raw.endswith(r"report \| audit.")
    assert meet.type_text == "holds" and meet.edge_type == "holds"


def test_example_vault_loads_twice_equal_and_in_order(tmp_path):
    a, b = load(EXAMPLES), load(EXAMPLES)
    assert a == b and a is not b
    assert [n.path for n in a.narratives] == sorted(n.path for n in a.narratives)
    assert [l.source for l in a.links] == sorted(l.source for l in a.links)


# ---------------------------------------------------------------------------------------------------------
# the refusal
# ---------------------------------------------------------------------------------------------------------


def test_a_missing_folder_is_a_refusal_not_an_exception(tmp_path):
    g = load(tmp_path / "nowhere")
    assert not g.ok and g.refusal.why == "the vault folder does not exist"
    assert g.nodes == {t: () for t in TBOX.layers}
    assert g.edges == g.narratives == g.candidates == g.links == ()
    assert load(str(tmp_path / "nowhere")) == g
    assert load(EXAMPLES / "README.md").refusal is not None  # a file is not a folder


def test_an_empty_vault_is_a_graph_with_nothing_in_it(tmp_path):
    g = load(tmp_path)
    assert g.ok and g.edges == () and g.narratives == () and all(v == () for v in g.nodes.values())


# ---------------------------------------------------------------------------------------------------------
# the table: the same rows however it is written
# ---------------------------------------------------------------------------------------------------------

SAME = [
    ("holds", "g", "c", "A note."),
    ("is addressed by", "c", "a", ""),
    ("is provided by", "a", "t", "Two words"),
]


def key(rows):
    return [(r.n, r.edge_type, r.from_target, r.to_target, r.note, r.well_formed) for r in rows]


def written(style):
    out = ["| from | type | to | note |", "|---|---|---|---|"]
    for verb, a, b, note in SAME:
        if style == "padded":
            out.append(f"| [[{a}]]   | {verb:<16} | [[{b}]]      | {note:<10} |")
        elif style == "compact":
            out.append(f"|[[{a}]]|{verb}|[[{b}]]|{note}|")
        elif style == "alias":
            out.append(f"| [[{a}\\|shown]] | {verb} | [[{b}\\|shown]] | {note} |")
        elif style == "slug":
            slug = TBOX.edge_type_named(verb).slug
            out.append(f"| [[{a}]] | {slug.upper()} | ![[{b}]] | {note} |")
        elif style == "spaces":
            out.append(f"\t| [[ {a} ]]{NBSP}| {verb} |{NBSP}[[ {b}  ]] |  {note}  |   ")
    return "\n".join(out) + "\n"


@pytest.mark.parametrize("style", ["padded", "compact", "alias", "slug", "spaces"])
def test_padded_compact_alias_and_other_tables_give_identical_rows(make_vault, style):
    base = key(rows_of(make_vault, "## Edges told\n\n" + written("compact")))
    assert [r[:4] for r in base] == [(1, "holds", "g", "c"), (2, "addressed-by", "c", "a"),
                                     (3, "provided-by", "a", "t")]  # fmt: skip
    got = key(rows_of(make_vault, "## Edges told\n\n" + written(style)))
    assert got == base
    assert edges_of(make_vault, "## Edges told\n\n" + written(style)) == (
        EdgeKey("holds", "g", "c"),
        EdgeKey("addressed-by", "c", "a"),
        EdgeKey("provided-by", "a", "t"),
    )


def test_obsidian_repadding_changes_nothing(make_vault):
    compact = "## Edges told\n\n" + written("compact")
    padded = "## Edges told\n\n" + written("padded")
    a = table_of(make_vault, compact)
    b = table_of(make_vault, padded)
    assert a.edges == b.edges and a.problems == b.problems == ()
    assert [r.note for r in a.rows] == [r.note for r in b.rows]


# ---------------------------------------------------------------------------------------------------------
# the table: where it is read
# ---------------------------------------------------------------------------------------------------------

ROW = "| [[g]] | holds | [[c]] | |\n"
EDGE = (EdgeKey("holds", "g", "c"),)


@pytest.mark.parametrize("level", range(1, 7))
def test_where_the_heading_is_at_any_level(make_vault, level):
    assert edges_of(make_vault, f"{'#' * level} Edges told\n\n{HEAD}{ROW}") == EDGE


@pytest.mark.parametrize(
    "heading", ["## edges TOLD", "##   Edges told   ", "## Edges told ##", "###\tEdges told"]
)
def test_where_the_name_is_compared_without_case_and_ignoring_spaces_at_its_ends(
    make_vault, heading
):
    assert edges_of(make_vault, f"{heading}\n\n{HEAD}{ROW}") == EDGE


@pytest.mark.parametrize(
    "heading",
    [
        "## Edges",
        "## Edge told",
        "## Edges tolds",
        "## Edges  told",
        "Edges told",
        "## Edges told now",
    ],
)
def test_where_a_heading_spelled_otherwise_is_not_read_and_nothing_is_reported(make_vault, heading):
    n = table_of(make_vault, f"{heading}\n\n{HEAD}{ROW}")
    assert n.table is None and n.edges == () and n.problems == ()


def test_where_no_heading_or_no_table_tells_no_edge_and_reports_nothing(make_vault):
    for body in ["Just text [[g]] and [[c]].\n", "## Edges told\n\nNo table here.\n", ""]:
        n = table_of(make_vault, body)
        assert n.table is None and n.rows == () and n.edges == () and n.problems == ()


def test_where_under_means_before_the_next_heading_of_the_same_or_a_higher_level(make_vault):
    # a deeper heading does not end the section; a heading of the same level does
    deeper = f"## Edges told\n\n### Notes\n\n{HEAD}{ROW}"
    assert edges_of(make_vault, deeper) == EDGE
    same = f"## Edges told\n\n## Other\n\n{HEAD}{ROW}"
    assert table_of(make_vault, same).table is None
    higher = f"## Part\n\n### Edges told\n\n#### Sub\n\n{HEAD}{ROW}"
    assert edges_of(make_vault, higher) == EDGE
    ended = f"### Edges told\n\ntext\n\n## Other\n\n{HEAD}{ROW}"
    assert table_of(make_vault, ended).table is None


def test_where_the_first_table_is_the_one_read(make_vault):
    body = f"intro\n\n| x | y |\n|---|---|\n| 1 | 2 |\n\n## Edges told\n\n{HEAD}{ROW}"
    assert edges_of(make_vault, body) == EDGE  # a table above the heading is no part of it
    body = f"## Edges told\n\ntext, then the table:\n\n{HEAD}{ROW}"
    assert edges_of(make_vault, body) == EDGE


def test_where_a_table_on_a_page_that_is_not_a_narrative_is_not_read(make_vault):
    root = make_vault({
        **NODES,
        "concern/x.md": node("concern", "x") + f"## Edges told\n\n{HEAD}{ROW}",
    })  # fmt: skip
    g = load(root)
    assert g.narratives == () and g.edges == ()


def test_where_a_heading_or_a_table_inside_a_fence_is_not_read(make_vault):
    fenced_heading = f"```\n## Edges told\n```\n\n{HEAD}{ROW}"
    assert table_of(make_vault, fenced_heading).table is None
    fenced_table = f"## Edges told\n\n```\n{HEAD}{ROW}```\n"
    n = table_of(make_vault, fenced_table)
    assert n.table is None and n.problems == ()
    fenced_second = f"## Edges told\n\n{HEAD}{ROW}\n~~~\n## Edges told\n{HEAD}{ROW}~~~\n"
    n = table_of(make_vault, fenced_second)
    assert n.edges == EDGE and n.problems == ()  # no second heading: it is in a fence


def test_where_a_table_is_the_contiguous_lines_that_start_with_a_bar(make_vault):
    body = f"## Edges told\n\n{HEAD}{ROW}| [[g2]] | holds | [[c2]] | |\n\nafter\n| [[g]] | holds | [[c2]] | |\n"
    n = table_of(make_vault, body)
    assert [r.n for r in n.rows] == [1, 2] and len(n.edges) == 2
    assert n.table.last_line == n.rows[-1].line  # the blank line ends it
    body = f"## Edges told\n\n{HEAD}{ROW}   | [[g2]] | holds | [[c2]] | |\n"
    assert len(table_of(make_vault, body).rows) == 2  # a row may start after spaces


# ---------------------------------------------------------------------------------------------------------
# the table: a second table or heading
# ---------------------------------------------------------------------------------------------------------


def test_a_second_table_under_the_heading_is_not_read_and_is_reported(make_vault):
    body = f"## Edges told\n\n{HEAD}{ROW}\ntext\n\n{HEAD}| [[g2]] | holds | [[c2]] | |\n"
    n = table_of(make_vault, body)
    assert n.edges == EDGE and len(n.rows) == 1  # the rows of the second tell no edge
    (p,) = n.problems
    assert (p.kind, p.variant) == ("second", "table")
    assert p.line == n.table.header_line + 6 and p.column == 1  # the header row of the second table


def test_a_second_heading_is_not_read_and_is_reported(make_vault):
    body = f"## Edges told\n\n{HEAD}{ROW}\n## Edges told\n\n{HEAD}| [[g2]] | holds | [[c2]] | |\n"
    n = table_of(make_vault, body)
    assert n.edges == EDGE
    (p,) = n.problems
    assert (p.kind, p.variant, p.line) == ("second", "heading", n.table.header_line + 4)
    # the same, at another level and another spelling of the name
    body = f"## Edges told\n\n{HEAD}{ROW}\n#### EDGES TOLD\n\n{HEAD}{ROW}"
    # (a deeper heading is still under the first, so its table is also a second table there)
    assert [(p.kind, p.variant) for p in table_of(make_vault, body).problems] == [
        ("second", "heading"),
        ("second", "table"),
    ]


def test_a_second_heading_with_no_table_under_the_first_still_reads_the_first_only(make_vault):
    body = f"## Edges told\n\ntext\n\n## Edges told\n\n{HEAD}{ROW}"
    n = table_of(make_vault, body)
    assert n.table is None and [(p.kind, p.variant) for p in n.problems] == [("second", "heading")]


# ---------------------------------------------------------------------------------------------------------
# the table: the header
# ---------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "header",
    [
        "| FROM | Type | TO | Note |",
        "|from|type|to|note|",
        "|  from  | type |to| note|",
        "| from | type | to | note",
    ],
)
def test_header_names_are_compared_without_case_and_ignoring_spaces(make_vault, header):
    n = table_of(make_vault, f"## Edges told\n\n{header}\n|---|---|---|---|\n{ROW}")
    assert n.edges == EDGE and n.problems == ()


@pytest.mark.parametrize(
    "separator",
    ["|---|---|---|---|", "| --- | --- | --- | --- |", "|:--|:-:|--:|---|", "|---|", "|-|-|"],
)
def test_separator_rows_with_or_without_alignment_colons_are_accepted(make_vault, separator):
    n = table_of(make_vault, f"## Edges told\n\n| from | type | to | note |\n{separator}\n{ROW}")
    assert n.edges == EDGE and n.problems == ()


HEADER_CASES = [
    # (header, separator line or None for none, variant, detail, what the problem is about)
    ("| from | to | type | note |", "|---|---|---|---|", "order", ""),
    ("| from | kind | to | note |", "|---|---|---|---|", "names", ""),
    ("| from | type | to |", "|---|---|---|", "names", ""),
    ("| from | type | to | note | extra |", "|---|---|---|---|---|", "names", ""),
    ("| from | type | to | note |", "| a | b |", "separator", "row"),
    ("| from | type | to | note |", None, "separator", "row"),  # the second line is a row
    ("| from | type | to | note |", "", "separator", "alone"),  # a header row alone
    ("| from | to | type | note |", None, "order+separator", "row"),
    ("| from | kind | to | note |", "| a | b |", "names+separator", "row"),
]


@pytest.mark.parametrize("header,separator,variant,detail", HEADER_CASES)
def test_a_malformed_header_is_one_problem_and_its_rows_tell_no_edge(
    make_vault, header, separator, variant, detail
):
    seplines = "" if separator in (None, "") else separator + "\n"
    body = f"## Edges told\n\n{header}\n{seplines}{ROW}"
    if separator == "":
        body = f"## Edges told\n\n{header}\n"
    n = table_of(make_vault, body)
    (p,) = n.problems
    assert (p.kind, p.variant, p.detail) == ("header", variant, detail)
    assert p.line == 8 and p.column == 1  # the header row (the body starts at file line 6)
    assert n.table is not None and not n.table.well_formed
    assert n.rows == () and n.edges == ()


def test_a_header_row_alone_at_the_end_of_the_file_is_a_malformed_table(make_vault):
    n = table_of(make_vault, "## Edges told\n\n| from | type | to | note |")
    assert [(p.variant, p.detail) for p in n.problems] == [("separator", "alone")]


def test_a_malformed_header_does_not_hide_a_second_table(make_vault):
    body = f"## Edges told\n\n| a | b |\n|---|---|\n\ntext\n\n{HEAD}{ROW}"
    n = table_of(make_vault, body)
    assert [(p.kind, p.variant) for p in n.problems] == [("header", "names"), ("second", "table")]


# ---------------------------------------------------------------------------------------------------------
# the table: rows and cells
# ---------------------------------------------------------------------------------------------------------


def row_problems(make_vault, row):
    n = table_of(make_vault, f"## Edges told\n\n{HEAD}{row}\n")
    return n, [(p.variant, p.row) for p in n.problems if p.kind == "row"]


@pytest.mark.parametrize(
    "row,variant,cells,closed",
    [
        ("| [[g]] | holds | [[c]] |", "missing-note", 3, True),
        ("| [[g]] | holds | [[c]] | n", "unclosed", 4, False),
        ("| [[g]] | holds | [[c]]", "missing-note-unclosed", 3, False),
        ("| [[g]] | holds | [[c]] | x | y |", "extra-cells", 5, True),
        ("| [[g]] | holds |", "too-few", 2, True),
        ("| [[g]] | holds", "too-few", 2, False),
        ("|", "too-few", 0, True),
        (
            "| [[g]] | holds | [[c]] | a \\|",
            "unclosed",
            4,
            False,
        ),  # an escaped bar is no closing bar
    ],
)
def test_wrong_cell_counts_and_unclosed_rows_are_data(make_vault, row, variant, cells, closed):
    n, problems = row_problems(make_vault, row)
    assert problems == [(variant, 1)]
    (r,) = n.rows
    assert (len(r.cells), r.closed, r.well_formed) == (cells, closed, False)
    assert n.edges == ()  # a row that is not well formed tells no edge
    (p,) = n.problems
    assert (p.line, p.column) == (r.line, r.column)


def test_a_well_formed_row_has_no_problem_and_rows_are_numbered_in_order(make_vault):
    body = (
        f"## Edges told\n\n{HEAD}{ROW}| [[g2]] | holds | [[c2]] |\n| [[g]] | holds | [[c2]] | |\n"
    )
    n = table_of(make_vault, body)
    assert [(r.n, r.well_formed) for r in n.rows] == [(1, True), (2, False), (3, True)]
    assert [(p.variant, p.row) for p in n.problems] == [("missing-note", 2)]
    assert n.edges == (EdgeKey("holds", "g", "c"), EdgeKey("holds", "g", "c2"))


def test_a_bar_in_a_note_written_escaped_is_text(make_vault):
    n, problems = row_problems(make_vault, r"| [[g]] | holds | [[c]] | a \| b \|\| c |")
    assert problems == [] and n.rows[0].note == "a | b || c" and len(n.rows[0].cells) == 4
    assert n.rows[0].cells[3].raw == r"a \| b \|\| c"


def test_an_unescaped_bar_in_a_note_makes_a_fifth_cell(make_vault):
    n, problems = row_problems(make_vault, "| [[g]] | holds | [[c]] | a | b |")
    assert problems == [("extra-cells", 1)] and n.edges == ()


@pytest.mark.parametrize(
    "cell",
    [r"[[g|shown]]", r"[[g\|shown]]", r"[[ g | shown ]]", r"![[g]]", "[[g#Head]]", "[[g^blk]]"],
)
def test_a_bar_inside_double_brackets_never_ends_a_cell(make_vault, cell):
    n, problems = row_problems(make_vault, f"| {cell} | holds | [[c]] | |")
    assert problems == [] and n.rows[0].from_target == "g" and len(n.rows[0].cells) == 4
    assert n.edges == EDGE


def test_a_bar_escaped_inside_a_code_span_is_one_bar_in_the_cell_text(make_vault):
    n, problems = row_problems(make_vault, r"| [[g]] | holds | [[c]] | the `a \| b` form |")
    assert problems == [] and n.rows[0].note == "the `a | b` form"


def test_a_link_in_a_code_span_is_not_an_end(make_vault):
    n, _ = row_problems(make_vault, "| `[[g]]` | holds | [[c]] | |")
    assert n.rows[0].from_target is None and n.rows[0].cells[1].links == () and n.edges == ()


def test_whitespace_of_any_kind_is_dropped_at_the_ends_and_one_run_inside_is_one_space(make_vault):
    n, problems = row_problems(
        make_vault,
        f"|{NBSP}[[ c ]]{NBSP}|\t is{NBSP}{NBSP}addressed \t by {NBSP}|\t[[ a\t]] |   word \t\t word   |",
    )
    assert problems == []
    r = n.rows[0]
    assert (r.type_text, r.edge_type, r.from_target, r.to_target) == (
        "is addressed by", "addressed-by", "c", "a",
    )  # fmt: skip
    assert r.note == "word word" and r.cells[1].raw.startswith("is")
    assert n.edges == (EdgeKey("addressed-by", "c", "a"),)


def test_the_note_may_be_empty_and_a_link_in_it_is_a_link_of_the_narrative(make_vault):
    n, problems = row_problems(make_vault, "| [[g]] | holds | [[c]] | |")
    assert problems == [] and n.rows[0].note == ""
    n, _ = row_problems(make_vault, "| [[g]] | holds | [[c]] | see [[c2]] |")
    assert "c2" in n.nodes and n.rows[0].note == "see [[c2]]"
    assert n.edges == EDGE  # the link in the note tells no edge


# ---------------------------------------------------------------------------------------------------------
# the type cell and the ends
# ---------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "cell,slug",
    [
        ("holds", "holds"), ("HOLDS", "holds"), ("Is Addressed By", "addressed-by"),
        ("addressed-by", "addressed-by"), ("PROVIDED-BY", "provided-by"),
        ("is provided by", "provided-by"), ("owns", None), ("", None), ("is addressed", None),
        ("holdz", None),
    ],
)  # fmt: skip
def test_the_type_cell_is_the_verb_or_the_slug_without_regard_to_case(make_vault, cell, slug):
    n, _ = row_problems(make_vault, f"| [[g]] | {cell} | [[c]] | |")
    assert n.rows[0].edge_type == slug
    assert n.rows[0].type_text == cell
    if slug != "holds":
        assert n.edges == ()  # the layers say holds; another type or none: no edge here


@pytest.mark.parametrize(
    "from_cell,to_cell,from_target,to_target",
    [
        ("[[g]]", "[[c]]", "g", "c"),
        ("[[g|a]]", "![[c]]", "g", "c"),
        ("g", "[[c]]", None, "c"),  # text, no link
        ("", "[[c]]", None, "c"),
        ("[[g]] and [[g2]]", "[[c]]", None, "c"),  # more than one link
        ("[[g]] (the people)", "[[c]]", None, "c"),  # a link beside text
        ("[[g]]", "[[#Heading]]", "g", None),  # not a page link
        ("[[photo.png]]", "[[dir/x]]", None, None),
        ("[[|alias]]", "[[^blk]]", None, None),
        (
            "[[ghost]]",
            "[[c]]",
            "ghost",
            "c",
        ),  # a name; whether it is a page is the graph's business
    ],
)
def test_each_end_is_exactly_one_link_and_nothing_else(
    make_vault, from_cell, to_cell, from_target, to_target
):
    n, _ = row_problems(make_vault, f"| {from_cell} | holds | {to_cell} | |")
    r = n.rows[0]
    assert (r.from_target, r.to_target) == (from_target, to_target)
    assert r.from_text == from_cell.strip() or "|" in from_cell


def test_a_row_tells_an_edge_only_between_nodes_of_the_layers_its_type_fixes(make_vault):
    cases = [
        ("holds", "[[g]]", "[[c]]", True),
        ("holds", "[[c]]", "[[g]]", False),  # the wrong direction
        ("holds", "[[g]]", "[[a]]", False),  # not neighbouring layers
        ("holds", "[[g]]", "[[ghost]]", False),  # reaches no page
        ("holds", "[[g]]", "[[n]]", False),  # reaches a page that is not a node
        ("holds", "[[g]]", "c", False),  # not a link
        ("is addressed by", "[[c]]", "[[a]]", True),
        ("is provided by", "[[a]]", "[[t]]", True),
        ("is provided by", "[[t]]", "[[a]]", False),
        ("owns", "[[g]]", "[[c]]", False),
    ]
    for verb, a, b, tells in cases:
        got = edges_of(make_vault, f"## Edges told\n\n{HEAD}| {a} | {verb} | {b} | |\n")
        assert bool(got) is tells, (verb, a, b)


def test_two_rows_of_one_narrative_for_one_pair_are_one_telling(make_vault):
    body = f"## Edges told\n\n{HEAD}| [[g]] | holds | [[c]] | first |\n| [[g]] | HOLDS | [[c]] | again |\n"
    g = load(vault(make_vault, body))
    (e,) = g.edges
    assert [(t.row, t.note) for t in e.tellings] == [(1, "first")]
    assert len(g.narrative("n").rows) == 2 and g.narrative("n").edges == EDGE


def test_a_name_that_two_pages_share_reaches_no_node(make_vault):
    root = vault(
        make_vault, f"## Edges told\n\n{HEAD}{ROW}", **{"other/c.md": node("affordance", "c")}
    )
    g = load(root)
    assert g.edges == ()
    assert len(g.narrative("n").edges) == 0


# ---------------------------------------------------------------------------------------------------------
# the graph: statuses, fingerprints, candidates
# ---------------------------------------------------------------------------------------------------------


def two_narratives(make_vault, s1, s2):
    t = f"## Edges told\n\n{HEAD}{ROW}"
    return load(
        make_vault(
            {**NODES, "narrative/a.md": narrative(t, s1), "narrative/b.md": narrative(t, s2)}
        )
    )


@pytest.mark.parametrize(
    "s1,s2,derived",
    [
        ("done", "done", "done"),
        ("done", "draft", "draft"),
        ("draft", "stub", "stub"),
        ("stub", "done", "stub"),
        ("draft", "draft", "draft"),
    ],
)
def test_an_edges_status_is_done_when_every_telling_narrative_is_done_else_the_least_advanced(
    make_vault, s1, s2, derived
):
    g = two_narratives(make_vault, s1, s2)
    (e,) = g.edges
    assert e.narratives == ("a", "b") and e.status == derived


def test_a_missing_or_invalid_status_is_the_least_advanced():
    assert derived_status(["done", "soon"]) == "stub"
    assert derived_status(["done", None]) == "stub"
    assert derived_status(["done"]) == "done"
    assert derived_status(["draft", "done"]) == "draft"


def test_an_edge_told_by_an_invalid_status_narrative_is_not_done(make_vault):
    g = two_narratives(make_vault, "done", "finished")
    assert g.edges[0].status == "stub"


def test_candidates_are_pairs_of_neighbouring_layers_both_linked_with_no_row(make_vault):
    body = "[[g]] [[c]] [[c2]] [[a]] [[t]] [[g2]]\n\n## Edges told\n\n" + HEAD + ROW
    g = load(vault(make_vault, body))
    got = {(c.type, c.from_node, c.to_node) for c in g.candidates}
    assert got == {
        ("holds", "g", "c2"), ("holds", "g2", "c"), ("holds", "g2", "c2"),
        ("addressed-by", "c", "a"), ("addressed-by", "c2", "a"),
        ("provided-by", "a", "t"),
    }  # fmt: skip
    assert ("holds", "g", "c") not in got  # it has a row


def test_a_pair_with_a_row_in_any_form_is_no_candidate(make_vault):
    # a row for the pair that is malformed, or written the wrong way round, is still a row there
    body = f"[[g]] [[c]]\n\n## Edges told\n\n{HEAD}| [[g]] | holds | [[c]]\n"
    assert load(vault(make_vault, body)).candidates == ()
    body = f"[[g]] [[c]]\n\n## Edges told\n\n{HEAD}| [[c]] | holds | [[g]] | |\n"
    assert load(vault(make_vault, body)).candidates == ()


def test_a_see_also_link_counts_and_a_pair_across_two_layers_does_not(make_vault):
    body = "[[g]] and [[a]] and [[t]]\n\n## See also\n\n- [[c]]\n"
    g = load(vault(make_vault, body))
    assert {(c.from_node, c.to_node) for c in g.candidates} == {("g", "c"), ("c", "a"), ("a", "t")}
    assert ("g", "a") not in {(c.from_node, c.to_node) for c in g.candidates}


def test_links_to_pages_that_are_not_nodes_are_in_no_fingerprint(make_vault):
    n = table_of(make_vault, "[[ghost]] [[c]] [[n]] [[photo.png]]\n")
    assert n.nodes == ("c",)
    assert sorted({l.target for l in n.links}) == ["c", "ghost", "n"]


# ---------------------------------------------------------------------------------------------------------
# determinism
# ---------------------------------------------------------------------------------------------------------


def test_two_loads_are_equal_whatever_order_the_files_were_written_in(make_vault, tmp_path):
    files = {**NODES,
             "narrative/b.md": narrative(f"## Edges told\n\n{HEAD}| [[g2]] | holds | [[c2]] | |\n"),
             "narrative/a.md": narrative(f"## Edges told\n\n{HEAD}{ROW}| [[a]] | is provided by | [[t]] | |\n")}  # fmt: skip
    first = make_vault(files)
    second = tmp_path.parent / (tmp_path.name + "-reversed")
    for rel in reversed(list(files)):
        (second / rel).parent.mkdir(parents=True, exist_ok=True)
        (second / rel).write_text(files[rel])
    a, b = load(first), load(second)
    assert load(first) == a
    assert copy.deepcopy(a.summary()) == b.summary()
    assert [(e.type, e.from_node, e.to_node) for e in a.edges] == [
        (e.type, e.from_node, e.to_node) for e in b.edges
    ]
    assert a.edges == tuple(
        sorted(a.edges, key=lambda e: (list(TBOX.edge_types).index(e.type), e.from_node, e.to_node))
    )
    assert [n.path for n in a.narratives] == ["narrative/a.md", "narrative/b.md"]
    assert [n.name for ns in a.nodes.values() for n in ns] == ["g", "g2", "c", "c2", "a", "t"]


# ---------------------------------------------------------------------------------------------------------
# the builders
# ---------------------------------------------------------------------------------------------------------


def apply(text, edits):
    """Apply edit data to a text the way a tool applying fixes does (one at a time, on the text as it stands)."""
    ls = text.split("\n")
    for e in sorted(edits, key=lambda e: -e.line):
        i = e.line - 1
        if e.action == "delete-line":
            assert ls[i].removesuffix("\r") == e.find
            del ls[i]
        else:
            assert e.action == "replace-text" and ls[i].removesuffix("\r") == e.find
            ls[i : i + 1] = e.replace.split("\n")
    return "\n".join(ls)


TEXT = narrative(
    f"The account [[g]].\n\n## Edges told\n\n{HEAD}| [[g]] | holds | [[c]] | one |\n| [[g2]] | holds | [[c]] | two |\n\nAfter the table.\n"
)


def test_add_row_to_an_existing_table_keeps_every_other_line_byte_identical():
    r = add_row(TEXT, "narrative/n.md", "is addressed by", "c", "a", "Said | twice")
    assert r.ok and r.changed
    old, new = lines(TEXT), lines(r.text)
    i = old.index("| [[g2]] | holds | [[c]] | two |") + 1
    assert new == old[:i] + ["| [[c]] | is addressed by | [[a]] | Said \\| twice |"] + old[i:]
    assert apply(TEXT, r.edits) == r.text
    (e,) = r.edits
    assert isinstance(e, Edit) and e.action == "replace-text" and e.file == "narrative/n.md"


def test_add_row_writes_the_verb_even_when_given_the_slug(make_vault):
    r = add_row(TEXT, "p.md", "provided-by", "a", "t")
    assert "| [[a]] | is provided by | [[t]] | |" in r.text
    assert format_row("holds", "g", "c", "  a\n b ") == "| [[g]] | holds | [[c]] | a b |"


def test_add_row_to_a_padded_table_leaves_the_padding_alone(make_vault):
    text = narrative("## Edges told\n\n" + written("padded"))
    r = add_row(text, "p.md", "holds", "g2", "c2")
    assert lines(r.text)[: len(lines(text)) - 1] == lines(text)[:-1]
    assert apply(text, r.edits) == r.text


def test_add_row_round_trips_through_the_loader(make_vault):
    root = make_vault({**NODES, "narrative/n.md": TEXT})
    r = add_row(TEXT, "narrative/n.md", "holds", "g", "c2", "A note; with | a bar")
    (root / "narrative/n.md").write_text(r.text)
    n = load(root).narrative("n")
    assert [x.note for x in n.rows] == ["one", "two", "A note; with | a bar"]
    assert EdgeKey("holds", "g", "c2") in n.edges and n.problems == ()


def test_add_row_with_no_table_writes_the_heading_header_and_separator_at_the_end():
    text = narrative("Just the account [[g]] [[c]].\n")
    r = add_row(text, "n.md", "holds", "g", "c")
    assert (
        r.text
        == text
        + "\n## Edges told\n\n| from | type | to | note |\n|---|---|---|---|\n| [[g]] | holds | [[c]] | |\n"
    )
    assert apply(text, r.edits) == r.text
    nofinal = text.rstrip("\n")  # no newline at the end: none is added
    r = add_row(nofinal, "n.md", "holds", "g", "c")
    assert r.text.startswith(nofinal + "\n\n## Edges told") and not r.text.endswith("\n")
    assert apply(nofinal, r.edits) == r.text
    assert read_table(lines(r.text), 1).table.well_formed


def test_add_row_with_a_heading_and_no_table_puts_the_table_under_the_heading():
    text = narrative("Account.\n\n## Edges told\n\nNo edges yet.\n")
    r = add_row(text, "n.md", "holds", "g", "c")
    assert lines(r.text)[-8:] == [
        "## Edges told",
        "",
        "| from | type | to | note |",
        "|---|---|---|---|",
        "| [[g]] | holds | [[c]] | |",
        "",
        "No edges yet.",
        "",
    ]
    assert apply(text, r.edits) == r.text
    t = read_table(lines(r.text)[5:], 6)  # the body starts at file line 6
    assert t.table.well_formed and len(t.table.rows) == 1 and "No edges yet." in r.text
    # text right under the heading gets a blank line after the new table, so it is not read as a row
    tight = narrative("## Edges told\nNo edges yet.\n")
    r2 = add_row(tight, "n.md", "holds", "g", "c")
    assert (
        apply(tight, r2.edits) == r2.text and len(read_table(lines(r2.text)[5:], 6).table.rows) == 1
    )


def test_add_row_keeps_crlf_endings():
    text = TEXT.replace("\n", "\r\n")
    r = add_row(text, "n.md", "holds", "g", "c2")
    assert r.text.count("\r\n") == text.count("\r\n") + 1 and "\n" not in r.text.replace("\r\n", "")
    assert apply(text, r.edits).replace("\r", "") == r.text.replace("\r", "")
    bare = narrative("Account.\n").replace("\n", "\r\n")
    r = add_row(bare, "n.md", "holds", "g", "c")
    assert "\n" not in r.text.replace("\r\n", "") and r.text.endswith(
        "| [[g]] | holds | [[c]] | |\r\n"
    )


def test_add_row_refuses_what_it_cannot_do_and_writes_nothing():
    bad_header = narrative("## Edges told\n\n| a | b |\n|---|---|\n| 1 | 2 |\n")
    for text, why in [
        (bad_header, "malformed"),
        (narrative("x\n"), None),  # fine: not refused
        ("no frontmatter\n", "frontmatter"),
    ]:
        r = add_row(text, "n.md", "holds", "g", "c")
        assert r.ok is (why is None)
        if why:
            assert why in r.refusal and r.text is None and r.edits == () and not r.changed
    r = add_row(TEXT, "n.md", "owns", "g", "c")
    assert not r.ok and "not an edge type" in r.refusal


def test_remove_rows_deletes_whole_lines_and_keeps_the_others_byte_identical():
    r = remove_rows(TEXT, "narrative/n.md", [1])
    old = lines(TEXT)
    i = old.index("| [[g]] | holds | [[c]] | one |")
    assert lines(r.text) == old[:i] + old[i + 1 :]
    assert [(e.action, e.line, e.find) for e in r.edits] == [
        ("delete-line", i + 1, "| [[g]] | holds | [[c]] | one |")
    ]
    assert apply(TEXT, r.edits) == r.text
    both = remove_rows(TEXT, "n.md", [2, 1, 2])
    assert (
        len(both.edits) == 2 and "| holds |" not in both.text.split("After")[0].split("---|\n")[-1]
    )
    assert apply(TEXT, both.edits) == both.text
    still = read_table(lines(both.text)[5:], 6)
    assert still.table.well_formed and still.table.rows == ()  # the table is kept, with no row


def test_remove_rows_refuses_a_row_that_is_not_there():
    r = remove_rows(TEXT, "n.md", [3])
    assert not r.ok and "3" in r.refusal and r.text is None
    assert not remove_rows(narrative("no table\n"), "n.md", [1]).ok
    assert remove_rows(TEXT, "n.md", []).text == TEXT and not remove_rows(TEXT, "n.md", []).changed


def test_a_removed_row_leaves_the_links_and_removes_the_edge(make_vault):
    root = make_vault({**NODES, "narrative/n.md": TEXT})
    assert len(load(root).edges) == 2
    (root / "narrative/n.md").write_text(remove_rows(TEXT, "n.md", [2]).text)
    g = load(root)
    assert [(e.from_node, e.to_node) for e in g.edges] == [("g", "c")]
    assert g.narrative("n").nodes == ("g", "c")  # the removed row held the only link to g2


def test_read_table_is_the_seam_the_builders_and_the_loader_share():
    body = lines(f"## Edges told\n\n{HEAD}{ROW}")
    reading = read_table(body, 10)
    assert reading.table.heading_line == 10 and reading.table.header_line == 12
    assert reading.table.separator_line == 13 and reading.table.rows[0].line == 14
    assert reading.table.last_line == 14 and reading.problems == ()


# ---------------------------------------------------------------------------------------------------------
# WP21-G1: the columns are `from | type | to | note`, and only that order is read or written
# ---------------------------------------------------------------------------------------------------------

OLD_ORDER = "| type | from | to | note |\n|---|---|---|---|\n| holds | [[g]] | [[c]] | |\n"


def test_the_columns_come_from_the_tbox_in_the_order_from_type_to_note():
    assert TBOX.table.names == ("from", "type", "to", "note")
    assert [c.holds for c in TBOX.table.columns] == ["from", "edge-type", "to", "note"]


@pytest.mark.parametrize(
    "slug,a,b,verb",
    [
        ("holds", "g", "c", "holds"),
        ("addressed-by", "c", "a", "is addressed by"),
        ("provided-by", "a", "t", "is provided by"),
    ],
)
def test_each_edge_type_is_written_and_read_in_the_new_order(make_vault, slug, a, b, verb):
    row = format_row(slug, a, b, "n")
    assert row == f"| [[{a}]] | {verb} | [[{b}]] | n |"
    n = table_of(make_vault, f"## Edges told\n\n{HEAD}{row}\n")
    assert n.problems == () and n.edges == (EdgeKey(slug, a, b),)


def test_a_table_in_the_old_order_is_refused_and_its_rows_tell_no_edge(make_vault):
    n = table_of(make_vault, "## Edges told\n\n" + OLD_ORDER)
    (p,) = n.problems
    assert (p.kind, p.variant) == ("header", "order")
    assert n.rows == () and n.edges == ()


def test_add_row_refuses_a_table_in_the_old_order_and_writes_nothing():
    text = narrative("Account [[g]] [[c]].\n\n## Edges told\n\n" + OLD_ORDER)
    r = add_row(text, "n.md", "holds", "g", "c")
    assert r.text is None and r.edits == ()
