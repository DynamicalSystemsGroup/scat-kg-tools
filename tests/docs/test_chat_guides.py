"""WP21-R7: the chat-path life-cycle guide and the leave-no-trace walkthrough exist, have their headings, name
a place in every numbered step, say who the walkthrough is for, and are linked and in the nav."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
CHAT = DOCS / "chat-path.md"
LNT = DOCS / "leave-no-trace.md"
# Where a step is done: the page defines these places, and each numbered step opens with one.
PLACES = (
    "In the chat",
    "In SCATLAB",
    "In the menu bar",
    "In Finder",
    "In GitHub Desktop",
    "In Obsidian",
    "In a web browser",
    "In Tailscale",
    "In a terminal",
    "In any app",
    "In Claude",
    "In Copilot",
    "In Open WebUI",
    "In Docker",
    "In an editor",
)
STEP = re.compile(r"^\s*\d+\. (.*)$")
# One place per step (D-119: a step names where it is done and one outcome).
LABEL = re.compile(r"\*\*(In [^*:]+):\*\*")
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


def test_chat_path_uses_colima_and_names_docker_desktop_in_one_plain_line():
    """The launcher uses Colima when it is installed and Docker Desktop otherwise (deploy/scatlab.sh)."""
    text = CHAT.read_text(encoding="utf-8")
    assert text.index("Colima") < text.index("Docker Desktop")
    flat = " ".join(text.split())
    assert (
        "If Docker Desktop is already installed and Colima is not, SCATLAB uses Docker Desktop instead"
        in flat
    )
    assert "untested" not in text


def test_numbered_steps_run_continuously_through_each_guide():
    for path in (CHAT, LNT):
        numbers = [
            int(m.group(1))
            for ln in path.read_text(encoding="utf-8").splitlines()
            if (m := re.match(r"^(\d+)\. ", ln))
        ]
        assert numbers == list(range(1, len(numbers) + 1)), path.name


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
    ):
        steps = _steps(CHAT, start, end)
        assert steps, start
        bad = [s for s in steps if not MARK.match(s)]
        assert not bad, f"{start}: steps with no place: {bad}"


def _one_action(steps):
    """Steps that carry two different place labels."""
    return [s for s in steps if len(set(LABEL.findall(s))) > 1]


def test_leave_no_trace_steps_name_a_place():
    steps = _steps(LNT, "The walkthrough", "What is removed and what stays")
    assert len(steps) >= 30
    bad = [s for s in steps if not MARK.match(s)]
    assert not bad, f"steps with no place: {bad}"
    assert not _one_action(steps)


def test_leave_no_trace_says_who_it_is_for():
    text = LNT.read_text(encoding="utf-8")
    assert "For a strict data policy" in text
    assert "do not need it" in text


def test_no_prompt_residue_in_the_guides():
    """D-139: no deontic keywords and no meta-talk about options or recommendations in the coder's pages."""
    deontic = re.compile(r"\b(MAY|SHALL|SHOULD|MUST)\b")
    meta = re.compile(r"(?i)policy option|not a recommendation|not a default|a MAY")
    for path in (CHAT, LNT, ROOT / "acceptance" / "walkthrough-chat.md"):
        text = path.read_text(encoding="utf-8")
        assert not deontic.search(text), (path.name, deontic.search(text).group(0))
        assert not meta.search(text), (path.name, meta.search(text).group(0))


def test_stop_is_an_alert_with_its_titles():
    chat = CHAT.read_text(encoding="utf-8")
    for title in ("SCATLAB stopped", "SCATLAB has a problem"):
        assert f'"{title}"' in chat


def test_leave_no_trace_covers_setup_and_removal():
    text = LNT.read_text(encoding="utf-8").lower()
    for word in (
        "temporary chat",
        "attach your field notes",
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


def test_every_numbered_step_in_the_chat_path_names_a_place():
    steps = _steps(CHAT, "What the chat path is, and what it needs", "What leaves your machine")
    assert len(steps) >= 60
    bad = [s for s in steps if not MARK.match(s)]
    assert not bad, f"steps with no place: {bad}"
    assert not _one_action(steps)


def test_no_step_refers_to_a_step_of_another_page():
    """D-119: a step refers to no step on another page by number or range."""
    ref = re.compile(r"\bsteps? \d+", re.IGNORECASE)
    steps = _steps(LNT, "The walkthrough", "What is removed and what stays")
    assert not [s for s in steps if ref.search(s) or "same section" in s]
    assert not ref.search(LNT.read_text(encoding="utf-8"))
    assert not re.search(r"(?i)steps? \d+ (and|to) \d+ of", CHAT.read_text(encoding="utf-8"))


def _all_steps(path):
    return [
        m.group(1) for ln in path.read_text(encoding="utf-8").splitlines() if (m := STEP.match(ln))
    ]


def test_no_guide_calls_scatlab_a_window():
    """WP22 (D-130): SCATLAB is a menu-bar app with no window; no stale launcher-window wording."""
    stale = re.compile(
        r"(?i)copy key and stop|leave the window|the window that says|the window says|launcher window"
        r"|scatlab window|in its window|in the window"
    )
    for path in (CHAT, LNT, ROOT / "acceptance" / "walkthrough-chat.md"):
        text = path.read_text(encoding="utf-8")
        assert not stale.search(text), (path.name, stale.search(text).group(0))
    for path in (CHAT, LNT):
        bad = [
            s
            for s in _all_steps(path)
            if re.match(r"\*\*In (SCATLAB|the menu bar):\*\*", s) and "window" in s
        ]
        assert not bad, bad


def test_menu_bar_steps_use_the_decided_labels():
    for path in (CHAT, LNT):
        text = path.read_text(encoding="utf-8")
        for label in (
            "Copy address",
            "Copy key",
            "Stop",
            "Use it",
            "Choose another",
            "Serve <vault>?",
        ):
            assert label in text, (path.name, label)
    assert "Change vault" in CHAT.read_text(encoding="utf-8")
    assert "Problem:" in CHAT.read_text(encoding="utf-8")


def _has_step(path, *words):
    return any(all(w in s for w in words) for s in _all_steps(path))


def test_the_chats_required_forms_are_in_numbered_steps():
    """L4, L5: the consent, the header format, Connect and the connected check, and the skill's Description."""
    for path in (CHAT, LNT):
        assert _has_step(path, "I trust this application"), path.name
        assert _has_step(path, "header format"), path.name
        assert _has_step(path, "**Connect**"), path.name
        assert _has_step(path, "shows connected"), path.name
        assert _has_step(path, "**Description**", "description:"), path.name


def test_step_for_the_file_library_says_why():
    """L8: field notes attached to a temporary chat stay in the file library after the chat is deleted."""
    steps = [
        s
        for s in _all_steps(LNT)
        if "file library" in s and s.startswith("**In the chat:** in the file library, delete")
    ]
    assert len(steps) == 1
    assert "stay after the temporary chat is deleted" in steps[0]


def test_the_saved_agents_tool_is_added_again():
    """L10, revised by D-141: editing the entry's key keeps the agent's tool; deleting the entry breaks it."""
    chat = CHAT.read_text(encoding="utf-8")
    assert "Editing that entry's key keeps the tie" in chat
    assert "Deleting the entry breaks it" in chat
    assert "add the tool again" in LNT.read_text(encoding="utf-8")
