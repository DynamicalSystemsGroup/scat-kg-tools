"""WP16-G4, WP12-G2, D-081: docs/reference/terms.md cannot drift from the glossary or the ontology.

Two checks, both read from their source (nothing is listed here that a source could give):
- against GLOSSARY.md: the page defines exactly the glossary's terms, each in bold, uses no retired word, and is
  at most 600 words (WP12) with no prescriptive sentence (WP13-R3);
- against the ontology (`ontology/scat.ttl` through `scat_kg.tbox`): every vault name the page backticks is a page
  type, field, status, value, edge type or table name of the TBox, and the page shows every one of them.
"""

import re
from pathlib import Path

import pytest

from scat_kg.tbox import TBOX

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "docs" / "reference" / "terms.md"
GLOSSARY = ROOT / "GLOSSARY.md"
WORD_CAP = 800

# Backticked names that are not in the TBox but are real: the vault's configuration file and its key.
CONFIG_NAMES = {"scat.toml", "stakeholder_group_cap"}
# Words the glossary retired or never had for a sense it defines (D-081, D-088).
RETIRED = [
    r"\braw (page|record|scenario|architecture)",
    r"\bcoded (page|record|scenario|architecture)",
    r"\bclass pages?\b",
    r"\brelation pages?\b",
    r"\bstakeholder[- ]groups?\b",
    r"\bheldby\b",
    r"\bconflicts?\b",
]
# The same retired words, for the other pages that teach the model (the flow, consent and coding pages). The
# stakeholder-group words are left out: "SCAT" is expanded on the flow page, and the cap is worded that way.
OTHER_PAGES = ["flow.md", "data-and-consent.md", "coding.md"]
OTHER_RETIRED = [
    r"\braw (page|record|scenario|architecture)",
    r"\bcoded (page|record|scenario|architecture)",
    r"\bclass pages?\b",
    r"\brelation pages?\b",
    r"\bheldby\b",
    r"`?conflicts`? fields?\b",
]
PRESCRIPTIVE = re.compile(
    r"\b(should|must|need to|make sure|do not|don't)\b|\byou\b|^- \*\*[^*]+\*\*: (run|use|write|set) ",
    re.IGNORECASE,
)


def glossary_terms(text: str) -> set[str]:
    """Every bold term in the first column of a glossary table; `a, b, c` names three terms."""
    terms: set[str] = set()
    for cell in re.findall(r"(?m)^\| \*\*([^*|]+)\*\* \|", text):
        terms.update(t.strip() for t in cell.split(","))
    return terms


def page_terms(text: str) -> set[str]:
    terms: set[str] = set()
    for cell in re.findall(r"(?m)^- \*\*([^*]+)\*\*:", text):
        terms.update(t.strip() for t in cell.split(","))
    return terms


def tbox_names() -> dict[str, set[str]]:
    """What the TBox allows the page to backtick, by kind."""
    fields = [f for t in TBOX.page_types.values() for f in t.fields]
    values = {v for f in fields if f.value_set for v in f.value_set}
    return {
        "page type": set(TBOX.page_types),
        "field": {f.key for f in fields},
        "value": values,
        "edge type": {s for e in TBOX.edge_types.values() for s in e.spellings},
        "table name": {TBOX.table.heading, *TBOX.table.names},
        "configuration name": CONFIG_NAMES,
    }


def must_show() -> dict[str, set[str]]:
    """What the page has to name: the TBox's types, statuses, values and edge types."""
    fields = [f for t in TBOX.page_types.values() for f in t.fields]
    return {
        "page type": set(TBOX.page_types),
        "status": set(TBOX.statuses),
        "value": {v for f in fields if f.key in ("kind", "timeframe") for v in f.value_set or ()},
        "edge type": {e.verb for e in TBOX.edge_types.values()},
        "table name": {TBOX.table.heading},
    }


def problems(text: str, glossary: str | None = None) -> list[str]:
    """Everything in the page text that drifts from the glossary or the TBox; empty when it agrees."""
    glossary = GLOSSARY.read_text(encoding="utf-8") if glossary is None else glossary
    found = []
    want, have = glossary_terms(glossary), page_terms(text)
    found += [f"the glossary term **{t}** is not defined on the page" for t in sorted(want - have)]
    found += [
        f"**{t}** is defined on the page but is not a glossary term" for t in sorted(have - want)
    ]
    for pattern in RETIRED:
        for hit in re.finditer(pattern, text, re.IGNORECASE):
            found.append(f"the page uses the retired word `{hit.group(0)}`")
    words = len(text.split())
    if words > WORD_CAP:
        found.append(f"the page has {words} words; the cap is {WORD_CAP}")
    for line in text.splitlines():
        if PRESCRIPTIVE.search(line):
            found.append(f"a prescriptive sentence (describe, do not instruct): {line.strip()}")
    allowed = set().union(*tbox_names().values())
    for token in sorted(t for t in set(re.findall(r"`([^`]+)`", text)) - allowed if "[[" not in t):
        found.append(f"`{token}` is not a name in the TBox")
    tokens = set(re.findall(r"`([^`]+)`", text))
    for label, names in must_show().items():
        found += [f"the page does not name the {label} `{n}`" for n in sorted(names - tokens)]
    for slug, edge in TBOX.edge_types.items():
        if edge.verb not in glossary:
            found.append(f"GLOSSARY.md does not use the verb `{edge.verb}` of the {slug} edge type")
    return found


def _page() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_terms_page_agrees_with_the_glossary_and_the_ontology():
    found = problems(_page())
    assert not found, "docs/reference/terms.md drifted:\n" + "\n".join(found)


def test_the_page_is_within_its_word_cap():
    assert len(_page().split()) <= WORD_CAP


@pytest.mark.parametrize(
    ("old", "new", "mentions"),
    [
        ("**fingerprint**", "**fingerprints**", "fingerprint"),  # a glossary term renamed
        ("**mismatch**", "**divergence**", "divergence"),
        ("`narrative` page", "`account` page", "account"),  # a page type renamed
        ("`holds`", "`held-by`", "held-by"),  # an edge type renamed
        ("`done`", "`finished`", "finished"),  # a status renamed
        ("`mixed`" if "`mixed`" in _page() else "`stub`", "`both`", "both"),
        ("`Edges told`", "`Edges recorded`", "Edges recorded"),  # the table heading renamed
        ("**coding**", "**tagging**", "tagging"),
        ("**link**", "**wikilink**", "wikilink"),
    ],
)
def test_a_renamed_term_is_reported(old, new, mentions):
    text = _page()
    assert old in text, f"{old} is not on the page, so this mutation proves nothing"
    found = problems(text.replace(old, new))
    assert found, f"renaming {old} to {new} went unnoticed"
    assert any(mentions in line for line in found), found


def test_a_retired_word_and_a_prescriptive_sentence_are_reported():
    text = _page()
    assert any("raw page" in p for p in problems(text + "\nA raw page holds notes.\n"))
    assert any("prescriptive" in p for p in problems(text + "\nYou should run the check.\n"))


def test_a_renamed_glossary_verb_is_reported():
    glossary = GLOSSARY.read_text(encoding="utf-8").replace("is addressed by", "is solved by")
    assert any("is addressed by" in p for p in problems(_page(), glossary))


@pytest.mark.parametrize("name", OTHER_PAGES)
def test_the_other_model_pages_use_no_retired_word(name):
    text = (ROOT / "docs" / name).read_text(encoding="utf-8")
    hits = [m.group(0) for p in OTHER_RETIRED for m in re.finditer(p, text, re.IGNORECASE)]
    assert not hits, f"docs/{name} uses retired words: {hits}"


def test_a_retired_word_on_another_page_is_reported():
    text = "Coded pages name groups. A relation page holds the `conflicts` field."
    hits = [m.group(0) for p in OTHER_RETIRED for m in re.finditer(p, text, re.IGNORECASE)]
    assert len(hits) == 3, hits
