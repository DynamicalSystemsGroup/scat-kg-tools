"""WP30-G5: the skill's last section, `## Stages`, lists for every other section the stages that offer it, as the
lifecycle instance says (`scat_kg.guides.instance()`), so the skill cannot drift from the model."""

import re
from pathlib import Path

from scat_kg.guides import instance

SKILL = Path(__file__).parents[2] / "skills" / "scat-coding" / "SKILL.md"


def headings(text: str) -> list[str]:
    return re.findall(r"(?m)^## (.+)$", text)


def table(text: str) -> dict[str, list[str]]:
    body = text.split("\n## Stages\n", 1)[1]
    rows = re.findall(r"(?m)^\| (.+?) \| (.+?) \|$", body)
    return {a: [s.strip() for s in b.split(",")] for a, b in rows if a not in ("Section", "---")}


def problems(text: str) -> list[str]:
    out = []
    names = headings(text)
    if "Stages" not in names:
        return ["the Stages section is missing"]
    if names[-1] != "Stages":
        out.append("the Stages section is not the last section")
    rows = table(text)
    for name in names:
        if name == "Stages":
            continue
        want = [s for s, v in instance()["stages"].items() if name in v["skill_sections"]]
        if not want:
            out.append(f"no stage lists the section {name!r}")
        elif name not in rows:
            out.append(f"no row for the section {name!r}")
        elif rows[name] != want:
            out.append(f"{name!r}: the row says {rows[name]}, the instance says {want}")
    out += [f"row {r!r} names no section" for r in rows if r not in names]
    return out


def test_the_stages_table_equals_the_instance():
    assert not problems(SKILL.read_text())


def test_every_section_the_instance_names_is_in_the_skill():
    names = headings(SKILL.read_text())
    for stage, v in instance()["stages"].items():
        for s in v["skill_sections"]:
            assert s in names, f"{stage} lists {s!r}, which the skill lacks"


def test_a_changed_row_is_caught():
    text = SKILL.read_text().replace(
        "| Norms | plan, capture, code, analyse, report |", "| Norms | plan, code |", 1
    )
    assert problems(text)


def test_a_missing_row_and_a_missing_section_are_caught():
    text = SKILL.read_text()
    assert problems("\n".join(ln for ln in text.splitlines() if not ln.startswith("| Kind ")))
    assert problems(text.split("\n## Stages\n")[0])
    assert problems(text + "\n## Afterword\n")
