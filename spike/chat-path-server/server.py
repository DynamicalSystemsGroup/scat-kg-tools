"""Throwaway MCP server: two read-only scat-kg checks. The tool owns conformance; this holds no authority."""

import argparse
import json
import os

from mcp.server.fastmcp import FastMCP

import scat_kg

DEFAULT_VAULT = "/Users/z/Documents/GitHub/scat-kg-template"
VAULT = os.environ.get("SCAT_VAULT", DEFAULT_VAULT)


def build(vault: str | None = None, **settings) -> FastMCP:
    root = vault or VAULT
    mcp = FastMCP("scat-kg", **settings)

    @mcp.tool()
    def check_page(page: str) -> str:
        """Check one page of the vault against the rules. PAGE is a page name (or its path).
        Returns the machine-interface JSON document (problems with rule, severity, where, what, fix)."""
        return json.dumps(scat_kg.check(page, root=root).to_dict(), ensure_ascii=False)

    @mcp.tool()
    def check_vault() -> str:
        """Check the whole vault against the rules. Returns the machine-interface JSON document."""
        return json.dumps(scat_kg.check(root=root).to_dict(), ensure_ascii=False)

    return mcp


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--vault", default=VAULT, help="vault folder (env SCAT_VAULT; default: %(default)s)"
    )
    ap.add_argument("--stdio", action="store_true", help="serve over stdio instead of HTTP")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    mcp = build(a.vault, host=a.host, port=a.port)
    key = os.environ.get("SCAT_MCP_KEY")
    if a.stdio or not key:
        mcp.run("stdio" if a.stdio else "streamable-http")
        return
    serve_with_key(mcp, key, a.host, a.port)


def serve_with_key(mcp: FastMCP, key: str, host: str, port: int) -> None:
    """Serve streamable HTTP, refusing any request without the API key (Bearer or X-API-Key)."""
    import hmac

    import uvicorn
    from starlette.responses import PlainTextResponse

    inner = mcp.streamable_http_app()

    async def app(scope, receive, send):
        if scope["type"] == "http":
            headers = {k.decode().lower(): v.decode() for k, v in scope.get("headers", [])}
            given = headers.get("x-api-key") or headers.get("authorization", "").removeprefix("Bearer ").strip()
            if not hmac.compare_digest(given, key):
                await PlainTextResponse("unauthorised", status_code=401)(scope, receive, send)
                return
        await inner(scope, receive, send)

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
