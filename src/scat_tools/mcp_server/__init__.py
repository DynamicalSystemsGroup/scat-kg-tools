"""The MCP server (M8): the tool's calls for a chat with no terminal. A front end; it holds no authority.

    python -m scat_tools.mcp_server --vault PATH --host 127.0.0.1 --port 8765     # streamable HTTP
    scat-mcp --vault PATH --stdio                                               # stdio

Needs the extra `mcp`: `pip install "scat-tools[mcp]"`. `import scat_tools` never imports this package.
The assistant's file, `contracts/assistant.md`, states what the assistant may and may not do.
"""
