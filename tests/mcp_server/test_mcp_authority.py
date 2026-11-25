"""WP18-R1 (never `done`) and WP18-R3: the chat path holds no authority, and agrees with `contracts/assistant.md`."""

import re

import pytest
from mcputil import ASSISTANT, call, copy_vault, serve, snapshot, with_session

from scat_kg.mcp_server import prompts

DONE_NARRATIVE = "saturday-at-the-lending-desk"  # done in the examples
DRAFT_NARRATIVE = "funders-meeting"  # draft


def _statuses(url) -> dict[str, str | None]:
    doc = call(url, "status", {})
    return {r["path"]: r["status"] for r in doc["rows"]}


def test_no_tool_or_sequence_of_tools_crosses_done(tmp_path):
    vault = copy_vault(tmp_path / "v")
    with serve(vault) as url:
        before = _statuses(url)
        done_before = {p for p, s in before.items() if s == "done"}
        assert done_before and DRAFT_NARRATIVE in " ".join(before)
        files = snapshot(vault)

        # set_status, both ways, in every spelling
        for page, target in [
            (DRAFT_NARRATIVE, "done"),
            ("funders", "done"),
            (DRAFT_NARRATIVE, "Done"),
            (DRAFT_NARRATIVE, " done"),
            (DONE_NARRATIVE, "draft"),
            (DONE_NARRATIVE, "stub"),
            (DONE_NARRATIVE, "done"),
            ("narrative/" + DONE_NARRATIVE + ".md", "draft"),
            ("group/borrowers.md", "stub"),
        ]:
            doc = call(url, "set_status", {"page": page, "status": target})
            assert doc["ok"] is False and doc["refused"], (page, target)
        assert snapshot(vault) == files

        # a refusal for `done` says that the coder sets it, in Obsidian
        doc = call(url, "set_status", {"page": DRAFT_NARRATIVE, "status": "done"})
        r = doc["refused"][0]
        assert "coder" in r["why"] and "Obsidian" in str(r["fix"]) and r["fix"]
        doc = call(url, "set_status", {"page": DONE_NARRATIVE, "status": "draft"})
        assert "coder" in doc["refused"][0]["why"] and "Obsidian" in str(doc["refused"][0]["fix"])

        # a narrative that is `done` cannot be changed through its edge rows
        for tool, args in [
            (
                "record_edge",
                {
                    "type": "holds",
                    "from_node": "funders",
                    "to_node": "quick-checkout",
                    "told_by": [DONE_NARRATIVE],
                },
            ),
            ("remove_edge", {"from_node": "borrowers", "to_node": "quick-checkout"}),
            (
                "remove_edge",
                {
                    "from_node": "borrowers",
                    "to_node": "quick-checkout",
                    "told_by": [DONE_NARRATIVE],
                },
            ),
        ]:
            doc = call(url, tool, args)
            assert doc["ok"] is False and doc["refused"], tool
        assert snapshot(vault) == files

        # every other tool, with a draft narrative in play: the done set stays the done set
        for tool, args in [
            ("stub", {"name": "fresh-narrative", "type": "narrative"}),
            ("stub", {"name": "fresh-concern", "type": "concern"}),
            ("stub_links", {}),
            ("index", {}),
            ("export_edges", {}),
            (
                "record_edge",
                {
                    "type": "holds",
                    "from_node": "funders",
                    "to_node": "fresh-concern",
                    "told_by": [DRAFT_NARRATIVE, "fresh-narrative"],
                },
            ),
            ("remove_edge", {"from_node": "funders", "to_node": "fresh-concern"}),
            ("set_status", {"page": "fresh-narrative", "status": "draft"}),
            ("set_status", {"page": "fresh-narrative", "status": "stub"}),
            ("check", {}),
        ]:
            call(url, tool, args)
        after = _statuses(url)
        assert {p for p, s in after.items() if s == "done"} == done_before
        assert all(after[p] == before[p] for p in before if p in after and p != "group/funders.md")
        assert not any(s == "done" for p, s in after.items() if p not in done_before)


def test_the_files_of_done_pages_are_byte_identical_after_every_tool(tmp_path):
    vault = copy_vault(tmp_path / "v")
    done_files = {}
    with serve(vault) as url:
        for p, s in _statuses(url).items():
            if s == "done":
                done_files[p] = (vault / p).read_bytes()
        for tool, args in [
            ("stub_links", {}),
            ("index", {}),
            ("export_edges", {}),
            ("stub", {"name": "zz-new", "type": "technology"}),
        ]:
            call(url, tool, args)
    assert {p: (vault / p).read_bytes() for p in done_files} == done_files


def _tools(url):
    async def go(s):
        return (await s.list_tools()).tools

    return with_session(url, go)


@pytest.fixture(scope="module")
def tools(tmp_path_factory):
    with serve(copy_vault(tmp_path_factory.mktemp("auth") / "v")) as url:
        yield _tools(url)


def _rule(n: int) -> str:
    text = ASSISTANT.read_text()
    m = re.search(rf"^- \*\*A{n}\.\*\* (.*?)(?=^- \*\*A|\n\n|\Z)", text, re.DOTALL | re.MULTILINE)
    assert m, f"A{n} not found in contracts/assistant.md"
    return " ".join(m.group(1).split())


def test_the_assistants_file_has_the_may_not_rules_this_server_is_built_to():
    key = {
        7: "Set a narrative to `done`, or move one out of `done`.",
        8: "Write a narrative's text through the tool.",
        9: 'Hand-write a row of an "Edges told" table.',
        10: "Resolve doubt about an interpretation.",
        11: "Claim a narrative is correct because the check passed.",
        12: "Touch the inputs (the field notes)",
    }
    for n, start in key.items():
        assert _rule(n).startswith(start), n
    assert "never crosses `done` (A7, A8)" in " ".join(ASSISTANT.read_text().split())


def test_A7_no_tool_sets_done(tools):
    for t in tools:
        assert "done" not in t.name.lower(), t.name
        for name, prop in t.inputSchema.get("properties", {}).items():
            assert "done" not in name.lower()
            assert "done" not in str(prop.get("enum", "")).lower()
    set_status = next(t for t in tools if t.name == "set_status")
    assert (
        "refused" in set_status.description.lower()
        and "coder sets `done`" in set_status.description
    )


def test_A8_no_tool_takes_a_narratives_text(tools):
    banned = {
        "text",
        "body",
        "content",
        "account",
        "markdown",
        "narrative_text",
        "notes",
        "field_notes",
    }
    for t in tools:
        assert not set(t.inputSchema.get("properties", {})) & banned, t.name
    assert not any(re.search(r"write_?(page|narrative|file)|edit|put|save", t.name) for t in tools)


def test_A9_no_tool_takes_a_row_and_record_edge_is_the_way(tools):
    names = {t.name for t in tools}
    assert {"record_edge", "remove_edge"} <= names
    for t in tools:
        assert not set(t.inputSchema.get("properties", {})) & {"row", "rows", "table", "line"}, (
            t.name
        )
    rec = next(t for t in tools if t.name == "record_edge")
    assert "never hand-write a row" in rec.description


def test_A10_to_A12_the_prompts_say_it(tools):
    rules = " ".join(prompts.RULES.split())
    assert (
        "resolve doubt about an interpretation (state the doubt and hand it back to the coder)"
        in rules
    )  # A10
    assert "claim a narrative is correct because the check passed" in rules  # A11
    assert "the check tests structure only" in rules
    assert "touch the field notes, other than reading what the coder gave you" in rules  # A12
    assert "RULES" not in prompts.CODE_A_NARRATIVE  # the loop carries the rules text itself
    assert rules in " ".join(prompts.CODE_A_NARRATIVE.split())
    review = " ".join(prompts.REVIEW_BEFORE_DONE.split())
    assert "not that the narrative is correct" in review and "hand it back to the coder" in review
    check = next(t for t in tools if t.name == "check")
    assert "structure only" in check.description


def test_prompts_and_tools_cite_the_assistants_file_and_say_the_coder_sets_done(tools):
    for t in tools:
        assert "contracts/assistant.md" in t.description, t.name
    for p in (
        prompts.CODE_A_NARRATIVE,
        prompts.EXPLAIN_A_PROBLEM,
        prompts.REVIEW_BEFORE_DONE,
        prompts.RULES,
    ):
        assert "contracts/assistant.md" in p
        flat = " ".join(p.split())
        assert "coder" in flat and "`done`" in flat
        assert "coder sets `done`, in Obsidian" in flat


def test_the_prompts_through_the_server(tmp_path):
    async def go(s):
        listed = (await s.list_prompts()).prompts
        out = {}
        for p in listed:
            args = {a.name: "x" for a in (p.arguments or [])}
            out[p.name] = (await s.get_prompt(p.name, args)).messages[0].content.text
        return out

    with serve(copy_vault(tmp_path / "v")) as url:
        got = with_session(url, go)
    assert {"code-a-narrative", "explain-a-problem", "review-before-done"} <= set(got)
    for name, text in got.items():
        assert "contracts/assistant.md" in text, name
        assert "coder" in text and "done" in text, name


def test_importing_the_core_does_not_import_the_server_or_mcp():
    import subprocess
    import sys

    code = (
        "import sys, scat_kg; "
        "assert not [m for m in sys.modules if m == 'mcp' or m.startswith('mcp.') or 'mcp_server' in m]"
    )
    assert subprocess.run([sys.executable, "-c", code], check=False).returncode == 0


def test_w9_the_review_prompt_asks_the_fingerprint_for_its_candidates():
    assert "Call fingerprint with candidates true" in prompts.REVIEW_BEFORE_DONE
