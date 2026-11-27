"""WP18-R1: every MCP tool returns the same data as the tool's own call, over a real HTTP server with a key."""

import re
from pathlib import Path

import pytest
from mcputil import call, changed, copy_vault, offer, serve, snapshot, with_session

import scat_kg

TOOLS = {
    "check",
    "status",
    "set_status",
    "stub",
    "stub_links",
    "record_edge",
    "remove_edge",
    "merge",
    "split_plan",
    "index",
    "fingerprint",
    "edge_table",
    "layered",
    "trace",
    "evidence",
    "copy_share",
    "review",
    "attribution",
    "export_edges",
}

STAGE_TOOLS = {"which_stage", "set_stage"}  # the stage layer's two tools, tested in test_stage_*.py


@pytest.fixture(scope="module")
def vaults(tmp_path_factory):
    """Two identical vaults: the server's, and the one the tool's own calls run on."""
    base = tmp_path_factory.mktemp("mcp")
    return copy_vault(base / "served"), copy_vault(base / "own"), base / "server.log"


@pytest.fixture(scope="module")
def url(vaults):
    served, _, log = vaults
    with serve(served, log=log) as u:
        yield u


def test_the_tools_listed(url):
    async def names(s):
        return {t.name for t in (await s.list_tools()).tools}

    assert with_session(url, names) == TOOLS | STAGE_TOOLS


def test_the_reference_page_states_the_number_of_tools(url):
    words = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
    ]
    words += [
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
        "twenty",
        "twenty-one",
        "twenty-two",
        "twenty-three",
        "twenty-four",
    ]
    page = (Path(__file__).parents[2] / "docs" / "reference" / "mcp.md").read_text("utf-8")
    said = re.search(r"^(\w[\w-]*) tools\.", page, re.MULTILINE)
    assert said and said.group(1).lower() in words

    async def count(s):
        return len((await s.list_tools()).tools)

    assert words.index(said.group(1).lower()) == with_session(url, count)


def test_every_tool_description_says_who_owns_what(url):
    async def tools(s):
        return (await s.list_tools()).tools

    for t in with_session(url, tools):
        assert "contracts/assistant.md" in t.description, t.name
        assert "holds no authority" in t.description, t.name


# (tool, arguments, the tool's own call on the twin vault). Run in order: the writes build on each other.
SEQUENCE = [
    ("check", {}, lambda r: scat_kg.check(root=r)),
    ("check", {"page": "funders-meeting"}, lambda r: scat_kg.check("funders-meeting", root=r)),
    (
        "check",
        {"page": "funders-meeting", "neighborhood": True},
        lambda r: scat_kg.check("funders-meeting", neighborhood=True, root=r),
    ),
    ("check", {"neighborhood": True}, lambda r: scat_kg.check(neighborhood=True, root=r)),
    ("check", {"page": "no-such-page"}, lambda r: scat_kg.check("no-such-page", root=r)),
    ("status", {}, lambda r: scat_kg.status(root=r)),
    ("status", {"page": "funders"}, lambda r: scat_kg.status("funders", root=r)),
    (
        "status",
        {"page": "funders-meeting", "neighborhood": True},
        lambda r: scat_kg.status("funders-meeting", neighborhood=True, root=r),
    ),
    ("fingerprint", {}, lambda r: scat_kg.fingerprint(root=r)),
    (
        "fingerprint",
        {"narrative": "funders-meeting"},
        lambda r: scat_kg.fingerprint("funders-meeting", root=r),
    ),
    (
        "fingerprint",
        {"narrative": "funders-meeting", "candidates": True},
        lambda r: scat_kg.fingerprint("funders-meeting", candidates=True, root=r),
    ),
    ("fingerprint", {"narrative": "nope"}, lambda r: scat_kg.fingerprint("nope", root=r)),
    ("edge_table", {"type": "holds"}, lambda r: scat_kg.edge_table("holds", root=r)),
    ("edge_table", {"type": "bogus"}, lambda r: scat_kg.edge_table("bogus", root=r)),
    ("layered", {}, lambda r: scat_kg.layered(root=r)),
    (
        "layered",
        {"narratives": ["funders-meeting"]},
        lambda r: scat_kg.layered(["funders-meeting"], root=r),
    ),
    ("trace", {"node": "borrowers"}, lambda r: scat_kg.trace("borrowers", root=r)),
    (
        "trace",
        {"node": "booking-app", "direction": "up"},
        lambda r: scat_kg.trace("booking-app", "up", root=r),
    ),
    ("evidence", {"node": "borrowers"}, lambda r: scat_kg.evidence("borrowers", root=r)),
    (
        "evidence",
        {"node": "funders-meeting"},
        lambda r: scat_kg.evidence("funders-meeting", root=r),
    ),
    (
        "merge",
        {"a": "funders", "b": "borrowers"},
        lambda r: scat_kg.merge("funders", "borrowers", plan=True, root=r),
    ),
    ("split_plan", {"a": "funders"}, lambda r: scat_kg.split_plan("funders", root=r)),
    ("copy_share", {}, lambda r: scat_kg.copy_share(root=r)),
    ("copy_share", {"node": "borrowers"}, lambda r: scat_kg.copy_share("borrowers", root=r)),
    ("review", {}, lambda r: scat_kg.review(root=r)),
    (
        "stub",
        {"name": "new-concern", "type": "concern"},
        lambda r: scat_kg.stub("new-concern", "concern", root=r),
    ),
    (
        "stub",
        {"name": "new-concern", "type": "concern"},
        lambda r: scat_kg.stub("new-concern", "concern", root=r),
    ),
    (
        "stub",
        {"name": "Bad Name", "type": "concern"},
        lambda r: scat_kg.stub("Bad Name", "concern", root=r),
    ),
    (
        "stub",
        {"name": "ada-quill", "type": "contributor"},
        lambda r: scat_kg.stub("ada-quill", "contributor", root=r),
    ),
    ("attribution", {}, lambda r: scat_kg.attribution(root=r)),
    ("stub_links", {}, lambda r: scat_kg.stub_links(root=r)),
    (
        "stub_links",
        {"page": "funders-meeting"},
        lambda r: scat_kg.stub_links("funders-meeting", root=r),
    ),
    (
        "record_edge",
        {
            "type": "holds",
            "from_node": "funders",
            "to_node": "new-concern",
            "told_by": ["funders-meeting"],
            "note": "from the call",
        },
        lambda r: scat_kg.record_edge(
            "holds", "funders", "new-concern", ["funders-meeting"], "from the call", root=r
        ),
    ),
    (
        "record_edge",
        {
            "type": "holds",
            "from_node": "funders",
            "to_node": "new-concern",
            "told_by": ["funders-meeting"],
        },
        lambda r: scat_kg.record_edge(
            "holds", "funders", "new-concern", ["funders-meeting"], root=r
        ),
    ),
    (
        "remove_edge",
        {"from_node": "funders", "to_node": "new-concern"},
        lambda r: scat_kg.remove_edge("funders", "new-concern", None, root=r),
    ),
    (
        "remove_edge",
        {"from_node": "funders", "to_node": "new-concern", "told_by": ["funders-meeting"]},
        lambda r: scat_kg.remove_edge("funders", "new-concern", ["funders-meeting"], root=r),
    ),
    (
        "set_status",
        {"page": "new-concern", "status": "draft"},
        lambda r: scat_kg.set_status("new-concern", "draft", root=r),
    ),
    (
        "set_status",
        {"page": "new-concern", "status": "draft"},
        lambda r: scat_kg.set_status("new-concern", "draft", root=r),
    ),
    (
        "set_status",
        {"page": "new-concern", "status": "bogus"},
        lambda r: scat_kg.set_status("new-concern", "bogus", root=r),
    ),
    (
        "set_status",
        {"page": "no-such", "status": "draft"},
        lambda r: scat_kg.set_status("no-such", "draft", root=r),
    ),
    ("index", {}, lambda r: scat_kg.index(root=r)),
    ("export_edges", {}, lambda r: scat_kg.export_edges(r / "views", root=r)),
    ("export_edges", {}, lambda r: scat_kg.export_edges(r / "views", root=r)),
    (
        "export_edges",
        {"folder": "views/v1"},
        lambda r: scat_kg.export_edges(r / "views" / "v1", root=r),
    ),
    ("check", {}, lambda r: scat_kg.check(root=r)),
]


def test_every_tool_returns_the_data_of_the_tools_own_call(url, vaults):
    served, own, _ = vaults
    seen = set()
    for tool, args, own_call in SEQUENCE:
        offer(served, tool)
        offer(own, tool)
        got = call(url, tool, args)
        want = own_call(own).to_dict()
        assert got == want, (tool, args)
        seen.add(tool)
    assert seen == TOOLS
    assert snapshot(served) == snapshot(own)


def test_a_refusal_is_a_result_not_an_error(url):
    doc = call(url, "check", {"page": "no-such-page"})
    assert doc["ok"] is False and doc["refused"][0]["why"] and doc["refused"][0]["fix"]


def test_a_call_names_no_vault(url):
    async def schemas(s):
        return (await s.list_tools()).tools

    for t in with_session(url, schemas):
        props = set(t.inputSchema.get("properties", {}))
        assert not props & {"root", "vault", "path"}, t.name


def test_the_server_reads_the_vault_afresh_on_each_call(tmp_path):
    vault = copy_vault(tmp_path / "v")
    with serve(vault) as url:
        before = call(url, "status", {"page": "funders"})
        page = vault / "group" / "funders.md"
        page.write_text(page.read_text().replace("status: stub", "status: draft"))
        after = call(url, "status", {"page": "funders"})
    assert before["rows"][0]["status"] == "stub" and after["rows"][0]["status"] == "draft"


def test_the_prompts_and_the_resource_are_listed(url):
    async def go(s):
        prompts = {p.name for p in (await s.list_prompts()).prompts}
        text = (
            (await s.get_prompt("code-a-narrative", {"narrative": "funders-meeting"}))
            .messages[0]
            .content.text
        )
        res = [str(r.uri) for r in (await s.list_resources()).resources]
        return prompts, text, res

    prompts, text, res = with_session(url, go)
    assert {
        "code-a-narrative",
        "explain-a-problem",
        "review-before-done",
        "draft-a-node-page",
        "fill-in-node-pages",
        "look-for-duplicates",
    } <= prompts
    assert "funders-meeting" in text
    assert "scat://assistant-rules" in res


def test_a_read_only_call_leaves_the_tree_as_it_was(tmp_path):
    vault = copy_vault(tmp_path / "v")
    before = snapshot(vault)
    with serve(vault) as url:
        for tool, args in [
            ("check", {}),
            ("check", {"page": "funders-meeting", "neighborhood": True}),
            ("status", {}),
            ("fingerprint", {}),
            ("edge_table", {"type": "holds"}),
            ("layered", {}),
            ("trace", {"node": "borrowers"}),
            ("attribution", {}),
            ("stub", {"name": "ada-quill", "type": "contributor"}),
            ("check", {"page": "nope"}),
            ("stub", {"name": "Bad Name", "type": "concern"}),
            ("export_edges", {"folder": "../outside"}),
        ]:
            call(url, tool, args)
    assert snapshot(vault) == before


def test_after_an_operation_only_the_files_it_reports_changed(tmp_path):
    vault = copy_vault(tmp_path / "v")
    with serve(vault) as url:
        for tool, args in [
            ("stub", {"name": "new-concern", "type": "concern"}),
            (
                "record_edge",
                {
                    "type": "holds",
                    "from_node": "funders",
                    "to_node": "new-concern",
                    "told_by": ["funders-meeting"],
                },
            ),
            (
                "remove_edge",
                {"from_node": "funders", "to_node": "new-concern"},
            ),
            ("set_status", {"page": "new-concern", "status": "draft"}),
            ("index", {}),
            ("export_edges", {}),
            ("stub_links", {}),
        ]:
            offer(vault, tool)
            before = snapshot(vault)
            doc = call(url, tool, args)
            assert doc["ok"], (tool, doc)
            reported = set(doc["created"]) | set(doc["changed"])
            moved = {
                p
                for p in changed(before, snapshot(vault))
                if before.get(p, "-") is not None or p in reported
            }
            moved = {p for p in moved if not (vault / p).is_dir()}
            assert moved == reported, (tool, moved, reported)


def test_export_writes_only_under_views(tmp_path):
    vault = copy_vault(tmp_path / "v", stage="analyse")
    before = snapshot(vault)
    with serve(vault) as url:
        for folder in ["narrative", "..", "../outside", "/tmp/x", ".", "views/../group", ""]:
            doc = call(url, "export_edges", {"folder": folder})
            assert doc["ok"] is False, folder
    assert snapshot(vault) == before
