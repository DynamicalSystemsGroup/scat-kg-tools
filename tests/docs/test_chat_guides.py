"""WP21-R7: the chat-path life-cycle guide and the leave-no-trace walkthrough exist, have their headings, name
a place in every numbered step, say the walkthrough is an option, and are linked and in the nav."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
CHAT = DOCS / "chat-path.md"
LNT = DOCS / "leave-no-trace.md"
# Where a step is done: the page defines these places, and each numbered step opens with one.
PLACES = (
    "In the chat",
    "In SCAT Chat",
    "In Finder",
    "In GitHub Desktop",
    "In Obsidian",
    "In a web browser",
    "In Tailscale",
    "In a terminal",
    "In the chat and in Obsidian",
)
STEP = re.compile(r"^\s*\d+\. (.*)$")
MARK = re.compile(r"^\*\*(" + "|".join(re.escape(p) for p in PLACES) + r"):\*\* \S")
CHAT_HEADINGS = [
    "Install once",
    "Start a session",
    "Connect the chat",
    "Set up the skill and the saved agent",
    "Use",
    "The session key",
    "Stop",
    "Clean up",
]


def _headings(path):
    return re.findall(r"(?m)^#{2,3} (.+?)\s*$", path.read_text(encoding="utf-8"))


def _steps(path, start, end):
    """Numbered step lines (and their text) of the sections from heading `start` up to heading `end`."""
    text = path.read_text(encoding="utf-8")
    a = text.index(f"## {start}\n")
    b = text.index(f"## {end}\n", a) if end else len(text)
    return [m.group(1) for ln in text[a:b].splitlines() if (m := STEP.match(ln))]


def test_both_pages_exist():
    assert CHAT.is_file()
    assert LNT.is_file()


def test_chat_path_has_the_life_cycle_headings_in_order():
    found = [h for h in _headings(CHAT) if h in CHAT_HEADINGS]
    assert found == CHAT_HEADINGS


def test_chat_path_leads_with_colima_and_says_docker_desktop_is_untested():
    text = CHAT.read_text(encoding="utf-8")
    assert text.index("Colima") < text.index("Docker Desktop")
    assert "Docker Desktop is the untested alternative" in text


def test_chat_path_session_key_wording():
    text = CHAT.read_text(encoding="utf-8")
    assert "the key was deleted" in text
    assert "Copy key" in text
    assert "replaced" not in text


def test_chat_path_steps_name_a_place():
    for start, end in (
        ("Start a session", "Connect the chat"),
        ("Connect the chat", "Set up the skill and the saved agent"),
        ("Set up the skill and the saved agent", "Use"),
        ("Stop", "Clean up"),
        ("Clean up", "What leaves your machine"),
    ):
        steps = _steps(CHAT, start, end)
        assert steps, start
        bad = [s for s in steps if not MARK.match(s)]
        assert not bad, f"{start}: steps with no place: {bad}"


def test_leave_no_trace_steps_name_a_place():
    steps = _steps(LNT, "The walkthrough", "What is removed and what stays")
    assert len(steps) >= 20
    bad = [s for s in steps if not MARK.match(s)]
    assert not bad, f"steps with no place: {bad}"


def test_leave_no_trace_says_it_is_an_option_not_a_recommendation():
    text = LNT.read_text(encoding="utf-8")
    assert "This is one policy option, a MAY" in text
    assert "not a recommendation" in text
    assert "not a default" in text


def test_leave_no_trace_covers_setup_and_removal():
    text = LNT.read_text(encoding="utf-8").lower()
    for word in (
        "temporary chat",
        "collection",
        "saved agent",
        "skill",
        "server entry",
        "local cop",
    ):
        assert word in text, word


def test_links_exist():
    for name in ("chat-path.md", "data-and-consent.md"):
        assert "](leave-no-trace.md" in (DOCS / name).read_text(encoding="utf-8"), name
    lnt = LNT.read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^)#]+\.md)(?:#[^)]*)?\)", lnt):
        assert (DOCS / target).is_file(), target
    # an anchor into the chat path must name a heading that exists
    chat_slugs = {re.sub(r"[^a-z0-9 -]", "", h.lower()).replace(" ", "-") for h in _headings(CHAT)}
    for anchor in re.findall(r"\(chat-path\.md#([^)]+)\)", lnt):
        assert anchor in chat_slugs, anchor


def test_nav_lists_both_pages():
    nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    for page in ("chat-path.md", "leave-no-trace.md"):
        assert re.search(rf"(?m)^\s+- [^:]+: {re.escape(page)}\s*$", nav), page
