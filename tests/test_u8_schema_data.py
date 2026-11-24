"""WP5-U8 (D-035 ruling 2, R-13): class page names, titles, `indexes` values and relation verbs come
from the TBox, and equal the contract's section 8 table and section 5 verbs."""

import re
from pathlib import Path

from scat_kg.checks import text
from scat_kg.ops import names, stub
from scat_kg.tbox import TBOX

CONTRACT = Path(__file__).parents[1] / "contracts" / "page-contracts.md"


def section8_rows():
    body = CONTRACT.read_text(encoding="utf-8").split("## 8. Class pages and their index tables")[1]
    body = body.split("## 9.")[0]
    rows = re.findall(
        r'^\| `([a-z-]+)` \| `([a-z-]+)` \| "([^"]+)" \| "([^"]+)" \|$', body, re.MULTILINE
    )
    assert len(rows) == 7
    return rows


def test_class_pages_equal_the_contract_section_8_table():
    rows = section8_rows()
    assert {n: (i, t) for n, i, t, _ in rows} == {
        n: (c.indexes, c.title) for n, c in TBOX.class_pages.items()
    }
    for name, indexes, _title, description in rows:
        assert TBOX.page_types[indexes].description == description


def test_the_tools_hold_no_copy_of_their_own():
    assert names.CLASS_PAGES == {n: (c.indexes, c.title) for n, c in TBOX.class_pages.items()}
    assert text.CLASS_PAGES == {n: c.indexes for n, c in TBOX.class_pages.items()}
    assert text.CLASS_TITLES == {n: c.title for n, c in TBOX.class_pages.items()}
    assert set(TBOX.class_pages) <= names.RESERVED and set(TBOX.class_pages) <= text.RESERVED
    assert not hasattr(stub, "_VERBS")


def test_relation_verbs_equal_the_contract_section_5_wording():
    assert {r: TBOX.page_types[r].verb for r in TBOX.relations} == {
        "heldby": "holds",
        "addresses": "addresses",
        "attributes": "attributed to",
    }
    assert all(t.verb is None for s, t in TBOX.page_types.items() if s not in TBOX.relations)
