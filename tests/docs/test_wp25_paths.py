"""WP25: the coding-paths navigation, the provider field, image alt text and the planning page's shape."""

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
WALKTHROUGHS = {
    "coding.md": "none",
    "chat-path.md": "Claude",
    "leave-no-trace.md": "inference.coop",
    "ide.md": "Copilot",
    "local-llm.md": "Ollama",
}


class _Loader(yaml.SafeLoader):
    pass


def _nav() -> list:
    # mkdocs.yml may carry python tags in other keys; only `nav` is read.
    _Loader.add_multi_constructor("", lambda loader, suffix, node: None)
    return yaml.load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"), Loader=_Loader)["nav"]


def _entry(items: list, title: str):
    for item in items:
        if isinstance(item, dict) and title in item:
            return item[title]
    raise AssertionError(f"no nav entry {title!r}")


def _front(name: str) -> dict:
    text = (DOCS / name).read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else {}


def test_r1_nav_shape():
    section = _entry(_nav(), "Coding paths")
    assert section[0] == {"Overview": "coding-paths.md"}
    assert section[1] == {"By hand": "coding.md"}
    chatbot = _entry(section, "An AI chatbot")
    assert chatbot == [{"The chat path": "chat-path.md"}, {"Leave no trace": "leave-no-trace.md"}]
    assert section[3] == {"An AI IDE": "ide.md"}
    assert section[4] == {"A local LLM": "local-llm.md"}
    assert len(section) == 5


def test_r1_flat_coding_entries_are_gone():
    top = [next(iter(i.values())) for i in _nav() if isinstance(i, dict)]
    for page in ("coding.md", "chat-path.md", "leave-no-trace.md", "ide.md"):
        assert page not in top


def test_r1_facilitating_opens_with_narratives():
    if not (DOCS / "narratives.md").exists():
        pytest.skip("docs/narratives.md has not landed")
    assert _entry(_nav(), "Facilitating")[0] == {"Narratives": "narratives.md"}


@pytest.mark.parametrize("name", sorted(WALKTHROUGHS))
def test_r3_provider_field(name):
    assert _front(name).get("provider") == WALKTHROUGHS[name]


def test_r3_ai_paths_name_different_providers():
    names = [_front(n).get("provider") for n in ("chat-path.md", "ide.md", "leave-no-trace.md")]
    assert all(names)
    assert len(set(names)) == 3


def test_r3_overview_links_every_walkthrough():
    text = (DOCS / "coding-paths.md").read_text(encoding="utf-8")
    for name in WALKTHROUGHS:
        assert f"]({name})" in text, name


IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)[^)]*\)")
HTML_IMAGE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)


def _images():
    for page in sorted(DOCS.rglob("*.md")):
        text = page.read_text(encoding="utf-8")
        for alt, src in IMAGE.findall(text):
            yield page, alt, src
        for tag in HTML_IMAGE.findall(text):
            alt = re.search(r'alt="([^"]*)"', tag)
            src = re.search(r'src="([^"]*)"', tag)
            yield page, alt.group(1) if alt else "", src.group(1) if src else ""


def test_r4_every_image_has_alt_text_and_exists():
    bad = []
    for page, alt, src in _images():
        if not alt.strip():
            bad.append((page.name, src, "no alt text"))
        if not src.startswith(("http://", "https://")) and not (page.parent / src).is_file():
            bad.append((page.name, src, "file missing"))
    assert not bad, bad


def test_r4_the_image_scan_sees_a_bad_reference():
    assert IMAGE.findall("![](x.png)") == [("", "x.png")]


def _planning() -> str:
    return (DOCS / "planning.md").read_text(encoding="utf-8")


def _planning_landed() -> bool:
    return bool(re.search(r"(?mi)^#{2,3} .*one-off", _planning()))


def _body_words(text: str) -> int:
    return len(re.sub(r"(?s)\A---\n.*?\n---\n", "", text).split())


def test_r5_planning_word_budget():
    if not _planning_landed():
        pytest.skip("planning.md has not been rewritten")
    assert _body_words(_planning()) <= 1500


@pytest.mark.parametrize(
    "kind",
    ["one-off online discussion", "recurring discussion", "in-person meetup", "multi-day workshop"],
)
def test_r5_planning_has_a_heading_per_event_kind(kind):
    if not _planning_landed():
        pytest.skip("planning.md has not been rewritten")
    assert re.search(rf"(?mi)^#{{2,3}} .*{re.escape(kind)}", _planning())


@pytest.mark.parametrize("topic", ["field notes", "compil"])
def test_r5_planning_has_field_notes_and_compiling_sections(topic):
    if not _planning_landed():
        pytest.skip("planning.md has not been rewritten")
    assert re.search(rf"(?mi)^#{{2,3}} .*{topic}", _planning())


NEEDS = "## What this path needs"
EXAMPLE = re.compile(r"(?m)^## Worked example: \S")


@pytest.mark.parametrize("name", sorted(WALKTHROUGHS))
def test_walkthrough_shape(name):
    text = (DOCS / name).read_text(encoding="utf-8")
    needs = re.search(rf"(?m)^{re.escape(NEEDS)}\s*$", text)
    example = EXAMPLE.search(text)
    if not needs and not example:
        pytest.skip("the walkthrough has not been rewritten to the shared shape")
    assert needs, f"{name} has no '{NEEDS}' heading"
    assert example, f"{name} has no '## Worked example: <name>' heading"
    assert needs.start() < example.start(), f"{name}: 'What this path needs' comes first"


def test_walkthrough_shape_detects_wrong_order():
    text = "## Worked example: X\n\n## What this path needs\n"
    assert re.search(rf"(?m)^{NEEDS}", text).start() > EXAMPLE.search(text).start()


def test_overview_says_each_example_is_an_example():
    text = (DOCS / "coding-paths.md").read_text(encoding="utf-8")
    assert "is an example" in text
    assert not re.search(
        r"(?i)\b(recommend|we choose|best choice|prefer(red)? provider|the default)\b", text
    )
    for example in ("Claude", "inference.coop", "Copilot", "Ollama"):
        assert example in text
