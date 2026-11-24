"""WP12-G2, WP12-R2: every vault name docs/reference/terms.md puts in backticks exists in the TBox, under
exactly that name, and the page names the full set of page types, statuses and timeframe values.

The page backticks vault names and nothing else, so each backticked token must be a page type, a field
key, a status value or a `timeframe` value of the TBox."""

import re
from pathlib import Path

import pytest

from scat_kg.tbox import TBOX

PAGE = Path(__file__).resolve().parents[2] / "docs" / "reference" / "terms.md"

CLASS_TYPES = {"stakeholder-group", "concern", "affordance", "technology"}
RECORD_TYPES = {"scenario-raw", "scenario-coded", "architecture-raw", "architecture-coded"}
RELATION_TYPES = {"heldby", "addresses", "attributes"}
STATUSES = {"stub", "draft", "done"}
TIMEFRAMES = {"past", "future", "mixed"}


def _timeframe_field():
    fields = [f for t in TBOX.page_types.values() for f in t.fields if f.key == "timeframe"]
    return fields[0]


def _names():
    """What the TBox allows the page to backtick: page types, field keys, statuses, timeframe values."""
    return {
        "page type": set(TBOX.page_types),
        "field": {f.key for t in TBOX.page_types.values() for f in t.fields},
        "status": set(TBOX.statuses),
        "timeframe value": set(_timeframe_field().value_set),
    }


def problems(text: str) -> list[str]:
    """Everything in the page text that drifts from the TBox; empty when it agrees."""
    found = []
    tokens = set(re.findall(r"`([^`]+)`", text))
    allowed = set().union(*_names().values())
    for token in sorted(tokens - allowed):
        found.append(f"`{token}` is not a page type, field, status or timeframe value in the TBox")
    for label, required in [
        ("class type", CLASS_TYPES),
        ("record type", RECORD_TYPES),
        ("relation type", RELATION_TYPES),
        ("status", STATUSES),
        ("timeframe value", TIMEFRAMES),
    ]:
        for name in sorted(required - tokens):
            found.append(f"the page does not name the {label} `{name}`")
    # Each relation page's endpoint fields, in the TBox's order, as the page lists them.
    for slug, (first, second) in TBOX.relations.items():
        if f"`{slug}`, with `{first}` and `{second}`" not in text:
            found.append(f"the page does not give `{slug}` with endpoints `{first}` and `{second}`")
    # `timeframe` belongs to exactly the page types the TBox gives it to.
    holders = sorted(s for s, t in TBOX.page_types.items() if t.field("timeframe"))
    if holders != ["architecture-raw", "scenario-raw"]:
        found.append(f"the TBox gives `timeframe` to {holders}; update the page and this test")
    if "the `timeframe` field on `scenario-raw` and `architecture-raw`" not in text:
        found.append(
            "the page does not say `timeframe` is on `scenario-raw` and `architecture-raw`"
        )
    return found


def _page() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_the_tbox_has_the_names_this_test_expects():
    assert STATUSES == set(TBOX.statuses)
    assert TIMEFRAMES == set(_timeframe_field().value_set)
    assert CLASS_TYPES | RECORD_TYPES | RELATION_TYPES | {"class"} == set(TBOX.page_types)


def test_terms_page_agrees_with_the_tbox():
    found = problems(_page())
    assert not found, "docs/reference/terms.md drifted from ontology/scat.ttl:\n" + "\n".join(found)


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ("`heldby`", "`held-by`"),
        ("`done`", "`finished`"),
        ("`mixed`", "`both`"),
        ("`conflicts`", "`conflict`"),
        ("`scenario-raw`", "`scenario_raw`"),
    ],
)
def test_a_renamed_term_is_reported(old, new):
    text = _page()
    assert old in text, f"{old} is not on the page, so this mutation proves nothing"
    found = problems(text.replace(old, new))
    assert found, f"renaming {old} to {new} went unnoticed"
    assert any(new.strip("`") in line for line in found)
