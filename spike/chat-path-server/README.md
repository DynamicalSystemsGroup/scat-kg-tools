# chat-path-server (throwaway spike)

An MCP server with two read-only `scat-kg` operations, both returning the machine-interface JSON
(`contracts/machine-interface.md`). The tool owns conformance; the server holds no authority and writes nothing.

| Tool | Does |
|---|---|
| `check_page(page)` | `scat_kg.check(page)`: one page, by name or path |
| `check_vault()` | `scat_kg.check()`: the whole vault |

Vault: `--vault DIR` or env `SCAT_VAULT` (default `/Users/z/Documents/GitHub/scat-kg-template`).

## Run (from this directory)

    uv run server.py                   # streamable HTTP, http://127.0.0.1:8765/mcp
    uv run server.py --port 9000 --vault /path/to/vault
    uv run server.py --stdio           # local testing
    uv run pytest                      # 4 tests, on a temp copy of the vault

## Adding it to a co-op LibreChat

LibreChat's server calls the endpoint, so it must be reachable from the co-op's host (a tunnel or public host
passing its `allowedDomains`/`allowedAddresses` rules; not localhost). Serve with `--host 0.0.0.0` only behind
TLS and auth: this server has none. An admin adds, in `librechat.yaml`:

    mcpServers:
      scat-kg:
        type: streamable-http
        url: https://<public-host>/mcp

(or a user adds it under MCP Settings, if the role allows), then attaches it to an agent. Unconfirmed: whether
the co-op's instance offers MCP to members. Page-level check needs no extra interface: `check(page)` exists.
