"""Generate GLOSSARY.md and docs/reference/terms.md from glossary.yml, the single source.

    python3 scripts/glossary.py            write both files
    python3 scripts/glossary.py --check    write nothing; exit 1 if either committed file differs

glossary.yml holds a `preface`, a `sections` list (id, title, blurb) and the `entries` (term, section, definition,
example, formal). Validation, all of it reported at once:
- the section ids are `core` plus stage ids read from the ```yaml lifecycle block of contracts/lifecycle.md;
- every entry has exactly the five fields, each a string, and a section that is declared;
- terms are unique;
- a definition has no "e.g.", "i.e." or "etc." (their full stops would end the first sentence).

The terms page shows the first sentence of each definition. The first sentence is the text up to the first full
stop that is followed by a space or the end of the text, ignoring full stops inside backticks (`scat.toml`) and
inside numbers (1.9). So a definition's first sentence must stand alone.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "glossary.yml"
LIFECYCLE = ROOT / "contracts" / "lifecycle.md"
GLOSSARY = ROOT / "GLOSSARY.md"
TERMS = ROOT / "docs" / "reference" / "terms.md"

FIELDS = ("term", "section", "definition", "example", "formal")
SECTION_FIELDS = ("id", "title", "blurb")
ABBREVIATIONS = re.compile(r"\b(e\.g\.|i\.e\.|etc\.)", re.IGNORECASE)
TERMS_INTRO = "Each word in one sense, as the glossary fixes it. See [Coding](../coding.md)."
HEADER = ("Term", "Definition", "Example use", "Formal concept and source")


class GlossaryError(Exception):
    """The source is invalid; `problems` lists every reason."""

    def __init__(self, problems: list[str]):
        super().__init__("\n".join(problems))
        self.problems = problems


def stage_ids(lifecycle: Path = LIFECYCLE) -> list[str]:
    """The stage ids, in order, from the ```yaml lifecycle block of contracts/lifecycle.md."""
    match = re.search(
        r"```yaml lifecycle\n(.*?)```", lifecycle.read_text(encoding="utf-8"), re.DOTALL
    )
    if not match:
        raise GlossaryError([f"{lifecycle} has no `yaml lifecycle` block"])
    return list(yaml.safe_load(match.group(1))["stages"])


def first_sentence(definition: str) -> str:
    """Up to the first full stop followed by a space or the end, outside backticks; whitespace folded."""
    text = " ".join(definition.split())
    in_code = False
    for i, ch in enumerate(text):
        if ch == "`":
            in_code = not in_code
        elif ch == "." and not in_code and (i + 1 == len(text) or text[i + 1] == " "):
            return text[: i + 1]
    return text


def validate(data: object, stages: list[str]) -> list[str]:
    """Every reason the source is invalid; empty when it is valid."""
    if not isinstance(data, dict):
        return ["glossary.yml is not a mapping"]
    found = []
    for key in ("preface", "sections", "entries"):
        if key not in data:
            found.append(f"glossary.yml has no `{key}`")
    if found:
        return found
    if not isinstance(data["preface"], str) or not data["preface"].strip():
        found.append("`preface` is not text")
    allowed = ["core", *stages]
    ids = []
    for s in data["sections"] if isinstance(data["sections"], list) else []:
        if not isinstance(s, dict) or set(s) != set(SECTION_FIELDS):
            found.append(
                f"a section does not have exactly the fields {', '.join(SECTION_FIELDS)}: {s}"
            )
            continue
        ids.append(s["id"])
        if s["id"] not in allowed:
            found.append(f"section `{s['id']}` is neither core nor a stage ({', '.join(stages)})")
    found += [
        f"section `{i}` is declared twice" for i in sorted({i for i in ids if ids.count(i) > 1})
    ]
    seen: set[str] = set()
    for e in data["entries"] if isinstance(data["entries"], list) else []:
        if not isinstance(e, dict):
            found.append(f"an entry is not a mapping: {e}")
            continue
        name = e.get("term", "?")
        missing = [f for f in FIELDS if f not in e]
        extra = [f for f in e if f not in FIELDS]
        if missing or extra:
            found.append(
                f"entry `{name}`: missing {missing or 'nothing'}, unknown {extra or 'nothing'}"
            )
            continue
        for f in FIELDS:
            if not isinstance(e[f], str):
                found.append(f"entry `{name}`: `{f}` is not text")
            elif not e[f].strip() and f != "formal":
                found.append(f"entry `{name}`: `{f}` is empty")
        if not isinstance(e["definition"], str):
            continue
        if e["section"] not in ids:
            found.append(f"entry `{name}`: section `{e['section']}` is not a declared section")
        if name in seen:
            found.append(f"term `{name}` is defined twice")
        seen.add(name)
        if ABBREVIATIONS.search(e["definition"]):
            found.append(f"entry `{name}`: the definition has an abbreviation with a full stop")
    return found


def _cell(text: str) -> str:
    return " ".join(text.split()).replace("|", "\\|")


def glossary_md(data: dict) -> str:
    lines = ["# Glossary", ""]
    for paragraph in re.split(r"\n\s*\n", data["preface"].strip()):
        lines += [" ".join(paragraph.split()), ""]
    for s in data["sections"]:
        lines += [
            f"## {s['title']}",
            "",
            s["blurb"],
            "",
            "| " + " | ".join(HEADER) + " |",
            "|---|---|---|---|",
        ]
        for e in (e for e in data["entries"] if e["section"] == s["id"]):
            example = f'"{_cell(e["example"])}"'
            lines.append(
                f"| **{_cell(e['term'])}** | {_cell(e['definition'])} | {example} | {_cell(e['formal'])} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def terms_md(data: dict) -> str:
    lines = ["# Terms", "", TERMS_INTRO, ""]
    for s in data["sections"]:
        lines += [f"## {s['title']}", ""]
        lines += [
            f"- **{e['term']}**: {first_sentence(e['definition'])}"
            for e in data["entries"]
            if e["section"] == s["id"]
        ]
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def load(source: Path = SOURCE, lifecycle: Path = LIFECYCLE) -> dict:
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    problems = validate(data, stage_ids(lifecycle))
    if problems:
        raise GlossaryError(problems)
    return data


def generate(source: Path = SOURCE, lifecycle: Path = LIFECYCLE) -> dict[Path, str]:
    """The two files as they would be written."""
    data = load(source, lifecycle)
    return {GLOSSARY: glossary_md(data), TERMS: terms_md(data)}


def main(argv: list[str]) -> int:
    check = "--check" in argv
    try:
        files = generate()
    except GlossaryError as err:
        print("glossary.yml is invalid:\n  " + "\n  ".join(err.problems), file=sys.stderr)
        return 1
    stale = [
        p for p, text in files.items() if not p.exists() or p.read_text(encoding="utf-8") != text
    ]
    if check:
        for p in stale:
            print(
                f"{p.relative_to(ROOT)} differs from glossary.yml; run `python3 scripts/glossary.py`",
                file=sys.stderr,
            )
        return 1 if stale else 0
    for p, text in files.items():
        p.write_text(text, encoding="utf-8")
        print(f"wrote {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
