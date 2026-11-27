"""Stand-in stage servers: one small FastMCP server per stage, each unaware of the others and of any state machine.

Tools are small functions returning dicts (like src/scat_kg/mcp_server/server.py). `status` and `check` are in every
stage with the same schema, so a union listing has name collisions to resolve.
"""

import time
from typing import Any

from mcp.server.fastmcp import Context, FastMCP

STAGES = ("plan", "code", "analyse")


def build_stage(name: str, **settings) -> FastMCP:
    """The stand-in server of stage `name`. `settings` go to FastMCP (host, port)."""
    mcp = FastMCP(f"scat-stage-{name}", **settings)

    def doc(**kw) -> dict[str, Any]:
        return {"ok": True, "stage": name, **kw}

    @mcp.tool(description="Show each page's status and the counts. Writes nothing.")
    def status(page: str | None = None, neighborhood: bool = False) -> dict[str, Any]:
        return doc(op="status", page=page, neighborhood=neighborhood, rows=[])

    @mcp.tool(description="Check the vault, or one page. Tests structure only. Writes nothing.")
    def check(page: str | None = None) -> dict[str, Any]:
        return doc(op="check", page=page, problems=[])

    if name == "plan":

        @mcp.tool(description="Create a stub page of `type` named `name`. Writes a stub only.")
        def stub(name: str, type: str) -> dict[str, Any]:
            return doc(op="stub", created=name, type=type)

    if name == "code":

        @mcp.tool(description="Set a page's status to `stub` or `draft`; never `done`.")
        def set_status(page: str, status: str) -> dict[str, Any]:
            return doc(op="set-status", page=page, status=status)

        @mcp.tool(description="Record one edge of type `type` from element `source` to `target`.")
        def record_edge(source: str, target: str, type: str = "relates") -> dict[str, Any]:
            return doc(op="record-edge", source=source, target=target, type=type)

        @mcp.tool(description="The fingerprint of a page's narrative.")
        def fingerprint(page: str) -> dict[str, Any]:
            return doc(op="fingerprint", page=page, fingerprint="0" * 8)

        @mcp.tool(description="Report progress `steps` times, then finish.")
        async def progress_demo(steps: int, ctx: Context) -> dict[str, Any]:
            for i in range(steps):
                await ctx.report_progress(i + 1, steps, f"step {i + 1}")
            return doc(op="progress-demo", steps=steps)

        @mcp.tool(description="Always raises (to see how a failed call travels).")
        def fail_demo() -> dict[str, Any]:
            raise ValueError("fail_demo always fails")

        @mcp.tool(description="Block the server's thread for `seconds` (a synchronous tool).")
        def block(seconds: float) -> dict[str, Any]:
            time.sleep(seconds)
            return doc(op="block", seconds=seconds)

    if name == "analyse":

        @mcp.tool(description="The layers of the vault, or of one page.")
        def layered(page: str | None = None) -> dict[str, Any]:
            return doc(op="layered", page=page, layers=[])

        @mcp.tool(description="The trace of an element: where it comes from.")
        def trace(element: str) -> dict[str, Any]:
            return doc(op="trace", element=element, steps=[])

        @mcp.tool(description="Export every edge of the vault.")
        def export_edges() -> dict[str, Any]:
            return doc(op="export-edges", edges=[])

        @mcp.tool(description="The fingerprint of a page's narrative.")
        def fingerprint(page: str) -> dict[str, Any]:
            return doc(op="fingerprint", page=page, fingerprint="0" * 8)

    @mcp.prompt(name="stage_guide", description=f"What to do in the {name} stage.")
    def stage_guide(topic: str = "") -> str:
        return f"You are in the {name} stage. {topic}".strip()

    @mcp.resource(f"stage://{name}/guide", name=f"{name}_guide", description=f"The {name} guide.")
    def guide() -> str:
        return f"guide of the {name} stage"

    return mcp
