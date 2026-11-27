"""WP25-G4: the planning page is organised by kind of event, stays light, and keeps its attribution anchors."""

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parents[2] / "docs"
PLANNING = DOCS / "planning.md"
HEADINGS = (
    "A one-off online discussion",
    "A recurring discussion",
    "An in-person meetup",
    "A multi-day workshop",
    "Who takes field notes",
    "Compiling several sets of field notes",
)


def slug(heading: str) -> str:
    return re.sub(r"[^a-z0-9_ -]", "", heading.lower()).replace(" ", "-")


def test_the_six_headings_exist():
    text = PLANNING.read_text(encoding="utf-8")
    found = re.findall(r"(?m)^## (.+?)\s*$", text)
    for heading in HEADINGS:
        assert heading in found, heading


def test_the_page_stays_light():
    assert len(PLANNING.read_text(encoding="utf-8").split()) <= 1500


def test_the_attribution_anchors_resolve():
    text = PLANNING.read_text(encoding="utf-8")
    anchors = {slug(h) for h in re.findall(r"(?m)^#{2,3} (.+?)\s*$", text)}
    assert "choose-the-attribution-mode" in anchors
    for page in DOCS.glob("*.md"):
        for target in re.findall(r"planning\.md#([\w-]+)", page.read_text(encoding="utf-8")):
            assert target in anchors, (page.name, target)
