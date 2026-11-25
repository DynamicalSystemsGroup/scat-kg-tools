# RS3: live check (light), 24 November

Driven by the ACE in the browser pane, signed in by the chief engineer. One sitting, no messages sent to any model,
nothing created or saved; only the interface was inspected. No field material.

## Findings

- **Members can add their own MCP servers.** MCP Settings has an "Add MCP" form: name, description, icon, **MCP Server
  URL** (an `https://` address), **Transport: Streamable HTTPS or SSE**, **Authentication: None (auto-detect), API Key
  or OAuth**, and an "I trust this application" box ("Custom connectors are not verified by LibreChat"). This confirms
  the documented LibreChat route: the co-op's chat server calls a remote MCP server over HTTPS. Two co-op servers are
  listed already (an image server and a docs server).
- **Agent Builder is available to members:** name, description, model, category, **instructions** (a system prompt),
  **tools** (add, including MCP servers), **skills** (off, all or selected), and **file context** (files can be added
  once the agent is created). A separate Skills and Prompts area is in the side bar. Code execution was not offered.
- **Files** can be attached to a conversation (paperclip, drag and drop). Downloads of files the chat makes were not
  tested (it would need a message to a model).

## What this means for the route

A coder's MCP server must be reachable at a public `https://` address with an API key or OAuth: the chat cannot reach a
server on the coder's own machine without a public tunnel. So the route needs a running service: either hosted (for
example on DSG's governed compute) or tunnelled from the coder's machine. Whatever the MCP server reads or returns also
passes through the co-op's chat server and the chosen model provider, as the chat already does for uploaded files.
