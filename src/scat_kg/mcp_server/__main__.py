"""`python -m scat_kg.mcp_server` and the `scat-mcp` command."""

import argparse
import os
import sys
from pathlib import Path

from scat_kg.mcp_server.gate import gated, start_refusal


def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="scat-mcp",
        description="Serve one SCAT vault to a chat over MCP. The server holds no authority: it calls the "
        "tool's operations and never sets a narrative to done (contracts/assistant.md). Over HTTP, "
        "env SCAT_MCP_KEY, when set, is required of every request (Bearer or X-API-Key).",
    )
    ap.add_argument(
        "--vault", default=os.environ.get("SCAT_VAULT"), help="the vault folder (env SCAT_VAULT)"
    )
    ap.add_argument("--stdio", action="store_true", help="serve over stdio (no key)")
    ap.add_argument("--host", default="127.0.0.1", help="HTTP host (default: %(default)s)")
    ap.add_argument("--port", type=int, default=8765, help="HTTP port (default: %(default)s)")
    return ap


def main(argv: list[str] | None = None) -> int:
    ap = _parser()
    a = ap.parse_args(argv)
    if not a.vault:
        ap.error("give --vault PATH (or set SCAT_VAULT)")
    if not Path(a.vault).is_dir():
        print(f"scat-mcp: the vault folder does not exist: {a.vault}", file=sys.stderr)
        return 2
    key = os.environ.get("SCAT_MCP_KEY") or None
    if not a.stdio:
        why = start_refusal(key, a.host)
        if why:
            print(f"scat-mcp: {why}", file=sys.stderr)
            return 2
    try:
        from scat_kg.mcp_server.server import build
    except ImportError as e:
        print(
            f'scat-mcp: the extra is missing ({e}); install it: pip install "scat-kg[mcp]"',
            file=sys.stderr,
        )
        return 2
    server = build(a.vault, host=a.host, port=a.port)
    if a.stdio:
        server.run("stdio")
        return 0
    import uvicorn

    app = server.streamable_http_app()
    uvicorn.run(gated(app, key) if key else app, host=a.host, port=a.port, log_level="warning")
    return 0


if __name__ == "__main__":
    sys.exit(main())
