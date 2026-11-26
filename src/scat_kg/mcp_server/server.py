"""The tools, prompts and resource of the MCP server: one tool per operation of the tool, one vault, no authority.

Each tool returns `to_dict()` of the call it wraps (the machine-interface document). A refusal is a result,
not an exception. Nothing here writes a vault except the tool's own operations.
"""

from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

import scat_kg
from scat_kg.mcp_server import prompts
from scat_kg.ops.result import refused, stamp

CITE = prompts.CITE
VIEWS_FOLDER = "views"
_OWN = f"The tool owns conformance, the coder owns interpretation, the assistant holds no authority ({CITE}). "


def build(vault: str | Path, **settings) -> FastMCP:
    """The server for the vault folder `vault`, read afresh on each call. `settings` go to FastMCP (host, port)."""
    root = Path(vault)
    mcp = FastMCP("scat-kg", **settings)

    def _doc(result) -> dict[str, Any]:
        """The document of a result, with the vault's attribution mode (every result reports it)."""
        return stamp(result, root).to_dict()

    @mcp.tool(
        description=_OWN
        + "Check the whole vault; or one page (`page`: a name or a path); or a page and every page one link "
        "away (`neighborhood`, needs `page`). Writes nothing. The check tests structure only: a clean check "
        "does not mean a narrative is correct. Returns the check document."
    )
    def check(page: str | None = None, neighborhood: bool = False) -> dict[str, Any]:
        return _doc(scat_kg.check(page, neighborhood=neighborhood, root=root))

    @mcp.tool(
        description=_OWN
        + "Show each page's status and the counts: the vault, one page, or a page and every page one link "
        "away (`neighborhood`). Writes nothing. Returns the status document."
    )
    def status(page: str | None = None, neighborhood: bool = False) -> dict[str, Any]:
        return _doc(scat_kg.status(page, neighborhood=neighborhood, root=root))

    @mcp.tool(
        description=_OWN
        + "Set a page's status to `stub` or `draft`. Refused when the new status is `done` and refused "
        "when the page is `done` now: the coder sets `done`, and moves a page out of it, in Obsidian "
        "(A7). Returns the operation document."
    )
    def set_status(page: str, status: str) -> dict[str, Any]:
        if status == "done":
            return _doc(
                refused(
                    "set-status",
                    page,
                    "this server never sets a page to `done`: that is the coder's act",
                    "the coder reads the narrative, then sets `status: done` in Obsidian "
                    f"(see {CITE}, A7)",
                )
            )
        now = scat_kg.status(page, root=root)
        if now.ok and any(r.status == "done" for r in getattr(now, "rows", ())):
            return _doc(
                refused(
                    "set-status",
                    page,
                    "this page is `done`, and this server never moves a page out of `done`: "
                    "that is the coder's act",
                    f"the coder sets `status: draft` in Obsidian to reopen it (see {CITE}, A7)",
                )
            )
        return _doc(scat_kg.set_status(page, status, root=root))

    @mcp.tool(
        description=_OWN
        + "Create a stub page of `type` (group, concern, affordance, technology, narrative, or contributor "
        "where the vault's attribution mode is required or optional) named `name` "
        "(a-z, 0-9 and hyphens). Writes a stub only, never a narrative's text (A8). Returns the operation "
        "document."
    )
    def stub(name: str, type: str) -> dict[str, Any]:
        return _doc(scat_kg.stub(name, type, root=root))

    @mcp.tool(
        description=_OWN
        + "Create the node pages that links in the vault (or in one `page`) name and the vault lacks. "
        "Returns the operation document."
    )
    def stub_links(page: str | None = None) -> dict[str, Any]:
        return _doc(scat_kg.stub_links(page, root=root))

    @mcp.tool(
        description=_OWN
        + "Record an edge of `type` from node `from_node` to node `to_node`: adds its row to each narrative in "
        "`told_by` (never hand-write a row, A9), stubbing what is missing. Refuses a narrative that is "
        "`done`; the coder sets it back to `draft` in Obsidian. Returns the operation document."
    )
    def record_edge(
        type: str, from_node: str, to_node: str, told_by: list[str], note: str = ""
    ) -> dict[str, Any]:
        return _doc(scat_kg.record_edge(type, from_node, to_node, told_by, note, root=root))

    @mcp.tool(
        description=_OWN
        + "Remove an edge between `from_node` and `to_node`: deletes its rows from the narratives in "
        "`told_by`, or from every narrative that tells it. Refuses a narrative that is `done`; the coder "
        "sets it back to `draft` in Obsidian. Returns the operation document."
    )
    def remove_edge(
        from_node: str, to_node: str, told_by: list[str] | None = None
    ) -> dict[str, Any]:
        return _doc(scat_kg.remove_edge(from_node, to_node, told_by, root=root))

    @mcp.tool(
        description=_OWN
        + "Show the plan of folding node page `a` into node page `b` (two pages of one type): the files that "
        "would change, the links that would be rewritten, the `done` narratives whose text would change, "
        "or why it is refused. Writes nothing. Applying a merge is refused here (`plan` false): the coder "
        "runs `scat merge a b`. Returns the operation document."
    )
    def merge(a: str, b: str, plan: bool = True) -> dict[str, Any]:
        if not isinstance(a, str) or not isinstance(b, str):
            return _doc(
                refused(
                    "merge", repr((a, b)), "a page is named by a string", "pass the two page names"
                )
            )
        if plan is not True:
            return _doc(
                refused(
                    "merge",
                    f"{a} and {b}",
                    "this server never applies a merge: that is the coder's act",
                    f"the coder looks at the plan, then runs `scat merge {a} {b}` (see {CITE})",
                )
            )
        return _doc(scat_kg.merge(a, b, plan=True, root=root))

    @mcp.tool(
        description=_OWN
        + "Show what must be re-linked to split node page `a`: the narratives that link it, with every link "
        "and every Edges told row that names it. The coder assigns each narrative. Writes nothing. Returns "
        "the operation document."
    )
    def split_plan(a: str) -> dict[str, Any]:
        if not isinstance(a, str):
            return _doc(
                refused("split-plan", repr(a), "a page is named by a string", "pass the page name")
            )
        return _doc(scat_kg.split_plan(a, root=root))

    @mcp.tool(
        description=_OWN
        + "Write the index page of each type that has none. Never rewrites one. Returns the operation document."
    )
    def index() -> dict[str, Any]:
        return _doc(scat_kg.index(root=root))

    @mcp.tool(
        description=_OWN
        + "View: a narrative's fingerprint (its nodes by layer and the edges its rows tell; with `candidates` "
        "true, also the links with no row); without `narrative`, every narrative. Writes nothing. "
        "Returns the view document."
    )
    def fingerprint(narrative: str | None = None, candidates: bool = False) -> dict[str, Any]:
        return _doc(scat_kg.fingerprint(narrative, candidates=candidates, root=root))

    @mcp.tool(
        description=_OWN
        + "View: every edge of one `type` (holds, addressed-by or provided-by), with the narratives that tell "
        "it and its status. Writes nothing. Returns the view document."
    )
    def edge_table(type: str) -> dict[str, Any]:
        return _doc(scat_kg.edge_table(type, root=root))

    @mcp.tool(
        description=_OWN
        + "View: the layered view, the union of the fingerprints of `narratives`, or of every narrative. "
        "Writes nothing. Returns the view document."
    )
    def layered(narratives: list[str] | None = None) -> dict[str, Any]:
        return _doc(scat_kg.layered(narratives, root=root))

    @mcp.tool(
        description=_OWN
        + "View: follow edges from `node` up toward the groups, down toward the technologies, or both "
        "(`direction`: up, down or both). Writes nothing. Returns the view document."
    )
    def trace(node: str, direction: str = "both") -> dict[str, Any]:
        return _doc(scat_kg.trace(node, direction, root=root))

    @mcp.tool(
        description=_OWN
        + "View: everything the vault says of one `node` (a group, concern, affordance or technology page): "
        "the narratives that link it with the paragraph around each link and the linking sentence marked, "
        "its edges with the narratives that tell them and each row's note, and its adjacent nodes by "
        "layer. Writes nothing. Returns the view document."
    )
    def evidence(node: str) -> dict[str, Any]:
        return _doc(scat_kg.evidence(node, root=root))

    @mcp.tool(
        description=_OWN
        + "View: for each node page (or the one `node` named), the share of its five-word runs that appear "
        "word for word in a narrative, and the narratives they come from, the most repeated first. A prompt "
        "to look, not a fault. Writes nothing. Returns the view document."
    )
    def copy_share(node: str | None = None) -> dict[str, Any]:
        return _doc(scat_kg.copy_share(node, root=root))

    @mcp.tool(
        description=_OWN
        + "View: the narratives by contributor, each contributor page with the narratives that name it, and "
        "the narratives that name none. Refused where the vault's attribution mode is disallowed. Writes "
        "nothing. Returns the view document."
    )
    def attribution() -> dict[str, Any]:
        return _doc(scat_kg.attribution(root=root))

    @mcp.tool(
        description=_OWN
        + f"Write the three edge tables as CSV and Markdown view files into `{VIEWS_FOLDER}/` of the vault "
        f"(or a folder under it, `folder`), through the tool's export operation only. Refuses where "
        f"edge_table would. Returns the operation document."
    )
    def export_edges(folder: str = VIEWS_FOLDER) -> dict[str, Any]:
        parts = Path(folder).parts
        out = (root / folder).resolve()
        inside = (
            out == (root.resolve() / VIEWS_FOLDER) or (root.resolve() / VIEWS_FOLDER) in out.parents
        )
        if (
            Path(folder).is_absolute()
            or ".." in parts
            or not parts
            or parts[0] != VIEWS_FOLDER
            or not inside
        ):
            return _doc(
                refused(
                    "export-edges",
                    folder,
                    f"view files go in `{VIEWS_FOLDER}/` of the vault, and nowhere else",
                    f"use `{VIEWS_FOLDER}` or a folder under it, such as `{VIEWS_FOLDER}/v1`",
                )
            )
        return _doc(scat_kg.export_edges(root / folder, root=root))

    @mcp.prompt(
        name="code-a-narrative",
        description=f"The coding loop for one narrative; done is the coder's ({CITE}).",
    )
    def code_a_narrative(narrative: str = "(the coder will name it)") -> str:
        return prompts.CODE_A_NARRATIVE.format(narrative=narrative)

    @mcp.prompt(
        name="explain-a-problem",
        description=f"Explain a problem the tool reported, quoting it as reported ({CITE}).",
    )
    def explain_a_problem(problem: str = "(the problem the coder points at)") -> str:
        return prompts.EXPLAIN_A_PROBLEM.format(problem=problem)

    @mcp.prompt(
        name="review-before-done",
        description=f"Review a narrative before the coder sets it to done ({CITE}).",
    )
    def review_before_done(narrative: str = "(the coder will name it)") -> str:
        return prompts.REVIEW_BEFORE_DONE.format(narrative=narrative)

    @mcp.prompt(
        name="draft-a-node-page",
        description=f"Draft one node page as text for the coder to write in ({CITE}).",
    )
    def draft_a_node_page(node: str = "(the coder will name it)") -> str:
        return prompts.DRAFT_A_NODE_PAGE.format(node=node)

    @mcp.prompt(
        name="fill-in-node-pages",
        description=f"Walk the stub node pages, one page per step, each handed back ({CITE}).",
    )
    def fill_in_node_pages() -> str:
        return prompts.FILL_IN_NODE_PAGES

    @mcp.resource(
        "scat://assistant-rules",
        name="assistant-rules",
        description=f"What the assistant may and may not do ({CITE}).",
        mime_type="text/plain",
    )
    def assistant_rules() -> str:
        return prompts.RULES

    return mcp
