"""WP38-R3, R4: GLOSSARY.md and docs/reference/terms.md are generated from glossary.yml and cannot drift from it.

Read from their sources: the data (`glossary.yml`), the generator (`scripts/glossary.py`) and the stages
(the ```yaml lifecycle block of contracts/lifecycle.md). The validation is shown to reject bad data by mutation.
"""

import copy
import importlib.util
import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]

_spec = importlib.util.spec_from_file_location("glossary_script", ROOT / "scripts" / "glossary.py")
assert _spec and _spec.loader
glossary = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(glossary)

# WP38-R4: words and phrases the glossary dropped, moved out or folded away (research/glossary/cleanup-ledger.md).
# Matched word-bounded and case-insensitively in every definition (examples are not checked). Common words are
# listed only in the sense that matters: "model" and "entry" appear as the full phrase or the dropped form.
DROPPED = [
    r"knowledge graphs?",
    r"\banalysis\b",
    r"layered graphs?",
    r"\bcoded\b",
    r"\buncoded\b",
    r"\bexcluded\b",
    r"\belements?\b",
    r"\bentry\b",
    r"\bentries\b",
    r"\bontolog(?:y|ies)\b",
    r"\bnorms?\b",
    r"\bconformant\b",
    r"\b(?:the|a) (?:finished )?model\b",
    r"\binputs\b",
    r"\banalysing\b",
    r"relationship annotations?",
    r"range vaults?",
    r"saved agents?",
    r"session keys?",
    r"leave no trace",
    r"\bskills?\b",
]


def _data() -> dict:
    return yaml.safe_load((ROOT / "glossary.yml").read_text(encoding="utf-8"))


def _stages() -> list[str]:
    return glossary.stage_ids()


def test_the_committed_files_equal_what_the_source_generates():
    for path, text in glossary.generate().items():
        assert path.read_text(encoding="utf-8") == text, (
            f"{path.relative_to(ROOT)} differs from glossary.yml; run `python3 scripts/glossary.py`"
        )


def test_every_section_is_core_or_a_stage_of_the_lifecycle():
    data = _data()
    allowed = {"core", *_stages()}
    assert {s["id"] for s in data["sections"]} <= allowed
    assert {e["section"] for e in data["entries"]} <= allowed
    assert data["sections"][0]["id"] == "core"


def test_the_committed_source_is_valid():
    assert glossary.validate(_data(), _stages()) == []


def _mutations():
    def unknown_section(d):
        d["entries"][0]["section"] = "elsewhere"

    def duplicate(d):
        d["entries"].append(copy.deepcopy(d["entries"][0]))

    def missing_field(d):
        del d["entries"][0]["example"]

    def extra_field(d):
        d["entries"][0]["note"] = "x"

    def undeclared_stage(d):
        d["sections"].append({"id": "party", "title": "Party", "blurb": "x"})

    def abbreviation(d):
        d["entries"][0]["definition"] = "A thing, e.g. this one."

    return [
        (unknown_section, "not a declared section"),
        (duplicate, "defined twice"),
        (missing_field, "missing"),
        (extra_field, "unknown"),
        (undeclared_stage, "neither core nor a stage"),
        (abbreviation, "abbreviation"),
    ]


@pytest.mark.parametrize(("mutate", "message"), _mutations())
def test_validation_rejects_bad_data(mutate, message, tmp_path):
    data = _data()
    mutate(data)
    found = glossary.validate(data, _stages())
    assert any(message in f for f in found), found
    source = tmp_path / "glossary.yml"
    source.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(glossary.GlossaryError):
        glossary.load(source)


def test_a_renamed_term_makes_the_generated_files_differ(tmp_path):
    data = _data()
    data["entries"][0]["term"] = data["entries"][0]["term"] + "s"
    source = tmp_path / "glossary.yml"
    source.write_text(yaml.safe_dump(data), encoding="utf-8")
    generated = glossary.generate(source)
    assert any(path.read_text(encoding="utf-8") != text for path, text in generated.items())


@pytest.mark.parametrize(
    ("definition", "first"),
    [
        ("One. Two.", "One."),
        ("Set in `scat.toml` (a file). More.", "Set in `scat.toml` (a file)."),
        ("An Obsidian Base, 1.9 or later. More.", "An Obsidian Base, 1.9 or later."),
        ("Only one", "Only one"),
        ("Folded\n  over two lines. Next.", "Folded over two lines."),
    ],
)
def test_the_first_sentence_rule(definition, first):
    assert glossary.first_sentence(definition) == first


def test_no_definition_uses_a_dropped_word():
    hits = [
        f"{e['term']}: {m.group(0)}"
        for e in _data()["entries"]
        for pattern in DROPPED
        for m in re.finditer(pattern, e["definition"], re.IGNORECASE)
    ]
    assert not hits, f"definitions use dropped words: {hits}"


def test_a_dropped_word_in_a_definition_is_reported():
    text = "The knowledge graph, coded narratives and an entry."
    hits = [m.group(0) for p in DROPPED for m in re.finditer(p, text, re.IGNORECASE)]
    assert len(hits) == 3, hits
