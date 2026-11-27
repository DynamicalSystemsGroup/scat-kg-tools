"""WP25-U8: the Facilitating section opens with Narratives; each page links on to its neighbours; the attribution
anchors the other pages pin still resolve."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
PAGES = [
    "narratives.md",
    "facilitate-scenarios.md",
    "facilitate-architectures.md",
    "facilitate-timeframe.md",
]
WORD_CAP = 900


def read(name: str) -> str:
    return (DOCS / name).read_text(encoding="utf-8")


def slugs(markdown: str) -> set[str]:
    return {
        re.sub(r"[^a-z0-9_ -]", "", h.lower()).replace(" ", "-")
        for h in re.findall(r"(?m)^#{1,3} (.+?)\s*$", markdown)
    }


def test_the_pages_exist_and_stay_light():
    for name in PAGES:
        assert len(read(name).split()) <= WORD_CAP, name


def test_nav_lists_the_section_in_order():
    nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    block = nav.split("  - Facilitating:\n", 1)[1].split("\n  - ", 1)[0]
    assert re.findall(r": (\S+\.md)", block) == PAGES


def test_each_page_links_the_next_and_related_ones():
    links = {
        "narratives.md": [
            "facilitate-scenarios.md",
            "facilitate-architectures.md",
            "facilitate-timeframe.md",
        ],
        "facilitate-scenarios.md": [
            "narratives.md",
            "facilitate-architectures.md",
            "facilitate-timeframe.md",
        ],
        "facilitate-architectures.md": ["narratives.md", "facilitate-timeframe.md"],
        "facilitate-timeframe.md": [
            "narratives.md",
            "facilitate-scenarios.md",
            "facilitate-architectures.md",
        ],
    }
    for page, targets in links.items():
        text = read(page)
        for target in targets:
            assert f"]({target}" in text, (page, target)


def test_links_into_the_section_resolve():
    for path in DOCS.glob("*.md"):
        for target, anchor in re.findall(
            r"\]\(((?:narratives|facilitate-[a-z]+)\.md)#([^)]+)\)", path.read_text("utf-8")
        ):
            assert anchor in slugs(read(target)), (path.name, target, anchor)


def test_the_attribution_anchors_resolve():
    planning = slugs(read("planning.md"))
    assert "choose-the-attribution-mode" in planning
    for page in PAGES[:3]:
        assert "planning.md#choose-the-attribution-mode" in read(page), page
    assert "attribution-mode" in slugs(read("data-and-consent.md"))
    assert "data-and-consent.md#attribution-mode" in read("narratives.md")


def test_the_narratives_page_names_each_mode():
    text = read("narratives.md")
    for mode in ("required", "optional", "disallowed"):
        assert f"| `{mode}` |" in text, mode
