"""R-13: the edge types, the table of edges and the field tables of the page contracts are the TBox's.

The contract (section 4, section 8, section 11) states the edge types with their slugs, verbs and ends, and each
type's fields with the level they are required from. This reads those tables out of the contract and compares them
with `TBOX`, which is read from the ontology: the tools hold no copy of their own.
"""

import re
from pathlib import Path

from scat_kg import graph
from scat_kg.ops import names
from scat_kg.tbox import TBOX

CONTRACT = (Path(__file__).parents[1] / "contracts" / "page-contracts.md").read_text(
    encoding="utf-8"
)


def section(start: str, end: str) -> str:
    return CONTRACT.split(start)[1].split(end)[0]


def test_edge_types_equal_the_contract_section_4_table():
    body = section("The `type` cell* is the verb", "The tools write the verb")
    rows = re.findall(
        r"^ *\| ([a-z ]+) \| `([a-z-]+)` \| `([a-z ]+)` \| `([a-z]+)` \| `([a-z]+)` \|$",
        body,
        re.MULTILINE,
    )
    assert len(rows) == 3
    assert {slug: (verb, a, b) for _, slug, verb, a, b in rows} == {
        s: (e.verb, e.from_type, e.to_type) for s, e in TBOX.edge_types.items()
    }
    assert all(label == TBOX.edge_types[slug].label for label, slug, *_ in rows)


def test_the_table_heading_and_columns_equal_the_contract():
    body = section("### `narrative`", "### `index`")
    assert f"The page's heading of the table is `{TBOX.table.heading}`" in body
    cols = ", ".join(f"`{n}`" for n in TBOX.table.names)
    assert f"its columns are {cols}." in body
    assert f"## {TBOX.table.heading}" in body


def field_tables():
    body = section("## 8. Types: fields", "## 9. Index pages")
    out = {}
    for slug, text in re.findall(r"### `([a-z]+)`\n(.*?)(?=\n### |\Z)", body, re.DOTALL):
        rows = re.findall(r"^\| `([a-z]+)` \| .* \| (stub|done|optional) \|$", text, re.MULTILINE)
        out[slug] = dict(rows)
    return out


def test_field_tables_equal_the_tbox_field_for_field():
    tables = field_tables()
    assert set(tables) == set(TBOX.page_types)
    for slug, t in TBOX.page_types.items():
        want = {f.key: f.required_from for f in t.required} | {
            f.key: "optional" for f in t.optional
        }
        assert tables[slug] == want, slug


def test_the_tools_hold_no_copy_of_their_own():
    assert names.STUBBABLE == (*TBOX.layers, "narrative")
    assert not hasattr(graph, "EDGE_TYPES") and not hasattr(graph, "COLUMNS")
    assert {n for n in names.RESERVED} == {"con", "prn", "aux", "nul"} | {
        f"{p}{i}" for p in ("com", "lpt") for i in range(10)
    }
