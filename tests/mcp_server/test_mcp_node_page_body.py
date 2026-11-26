"""WP24-R3 (A17): no tool of the MCP server writes the body of a node page.

Every tool runs, with plausible arguments, on a copy of the node-page test vault. The body of every node page that
was there before is the same after. A page a tool creates (a stub) has an empty body.
"""

import shutil
from pathlib import Path

import pytest
from mcputil import call, serve, with_session

VAULT = Path(__file__).parents[2] / "research" / "node-pages" / "vault" / "required"
NODE_FOLDERS = ("group", "concern", "affordance", "technology")
NARRATIVE = "consent-emoji-at-the-spring-forum"
EXISTING = {"from_node": "ethnographers", "to_node": "attention-limit-on-participation"}

# One entry per tool, in the order they run. A new tool without an entry fails the coverage test below.
CALLS: list[tuple[str, dict]] = [
    ("check", {}),
    ("check", {"page": "ethnographers", "neighborhood": True}),
    ("status", {}),
    ("set_status", {"page": "scheduler", "status": "draft"}),  # a stub node page: the write runs
    ("set_status", {"page": "scheduler", "status": "stub"}),
    ("set_status", {"page": "ethnographers", "status": "draft"}),  # `done`: refused
    ("stub", {"name": "fresh-concern", "type": "concern"}),
    ("stub_links", {}),
    (
        "record_edge",
        {
            "type": "holds",
            "from_node": "ethnographers",
            "to_node": "fresh-concern",
            "told_by": [NARRATIVE],
        },
    ),
    ("remove_edge", {**EXISTING, "told_by": [NARRATIVE]}),
    ("remove_edge", {"from_node": "ethnographers", "to_node": "fresh-concern"}),
    ("merge", {"a": "forum-bot", "b": "scheduler", "plan": True}),  # a plan: nothing is written
    ("merge", {"a": "forum-bot", "b": "scheduler", "plan": False}),  # applying is refused
    ("split_plan", {"a": "ethnographers"}),
    ("index", {}),
    ("fingerprint", {"narrative": NARRATIVE, "candidates": True}),
    ("edge_table", {"type": "holds"}),
    ("layered", {}),
    ("trace", {"node": "ethnographers"}),
    ("evidence", {"node": "ethnographers"}),
    ("copy_share", {}),
    ("attribution", {}),
    ("export_edges", {}),
]


def _split(text: str) -> tuple[str, str]:
    """The front matter and the body of a page."""
    _, front, body = text.split("---\n", 2)
    return front, body


def _node_pages(root: Path) -> dict[str, str]:
    return {
        str(p.relative_to(root)): p.read_text(encoding="utf-8")
        for folder in NODE_FOLDERS
        for p in sorted((root / folder).glob("*.md"))
        if p.name != "index.md"
    }


def _tool_names(url) -> set[str]:
    async def go(s):
        return {t.name for t in (await s.list_tools()).tools}

    return with_session(url, go)


@pytest.fixture(scope="module")
def run(tmp_path_factory):
    vault = tmp_path_factory.mktemp("body") / "v"
    shutil.copytree(VAULT, vault)
    before = _node_pages(vault)
    with serve(vault) as url:
        names = _tool_names(url)
        for tool, args in CALLS:
            call(url, tool, args)
    return names, before, _node_pages(vault)


def test_every_tool_is_walked(run):
    names, _, _ = run
    assert names == {tool for tool, _ in CALLS}, "a tool has no entry in CALLS (or one was removed)"


def test_no_node_page_body_changes(run):
    _, before, after = run
    assert before
    for path, text in before.items():
        assert _split(after[path])[1] == _split(text)[1], path


def test_a_page_a_tool_creates_has_no_body(run):
    _, before, after = run
    created = set(after) - set(before)
    assert "concern/fresh-concern.md" in created
    for path in created:
        assert _split(after[path])[1].strip() == "", path
