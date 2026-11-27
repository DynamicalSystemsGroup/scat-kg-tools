# RS5-U5 / G4 desk part: what MCP clients document, and what the spec allows

Access date for every source: 2026-11-27. Nothing here was tried in a client. "Documented" means a page says so;
"source" means the client's public code was read (not run); "issue" means a tracker or search result. Where docs and
issues disagree, the cell says so.

## Findings first

1. **The latest spec has no stage-holding server.** Revision 2026-07-28 removes `initialize`, `Mcp-Session-Id` and the
   standalone GET stream. Its tools page says a server's tool list MUST NOT vary per connection or as a side effect of
   other requests, though it MAY vary by the authorization on each request [S1, S4, S5]. Python `mcp` 1.30.0 speaks
   only up to 2025-11-25 [S7], where a server may keep session state. A stage held in the server, with `tools/list`
   changing as the stage moves, is legal only in the older era and runs against the new one. A stage the client names in
   each request (an argument, or a handle in a result) is legal in both.
2. **`list_changed` cannot be relied on.** VS Code's source re-lists on it and after every tool call [V6]; LibreChat's
   docs and code do [L2, L3]; Claude Code does in interactive sessions [K1]. For claude.ai and Desktop nothing is
   documented, and a user issue reports the mobile and desktop apps keep the first list (closed, not planned) [C4].
   Keep the tool list stable and let a wrong-stage call return a clarification.
3. **No client sends a per-request stage header from its settings.** claude.ai sends up to four fixed, Anthropic-approved
   header names [C2]; VS Code sends static `headers` with `${input:}` and `${env:}` values [V2]; Claude Code sends
   static headers or one `headersHelper` result per connection [K1]; the co-op's UI form offers one API-key header
   [L1]. LibreChat YAML can send `requestHeaders` with `{{LIBRECHAT_BODY_conversationId}}` per chat request [L2], but
   only an administrator edits that file. Headers carry the key; stage cannot ride in them on the chat path.
4. **The lowest common denominator for clarification is an ordinary tool result.** Elicitation is documented in Claude
   Code and VS Code's Copilot sessions [K1, V3]; claude.ai is unknown; LibreChat's code shows no elicitation
   capability in the part read [L3].
5. **The server's own defaults matter.** The repo builds `FastMCP("scat-kg", ...)` with no stateless or JSON-response
   setting and no `NotificationOptions` (grep of `src/scat_kg/mcp_server/`), so it is stateful and declares no
   `listChanged` capability: a server that wants `list_changed` must opt in [S7]. VS Code's Local harness caps a
   request at 128 tools [V5]. The chat-path lab run saw a 404 after a container restart, then the co-op's chat
   re-initialised on its own [L6].

## Matrix

<!-- matrix:start -->

Status words: **DS** documented supported; **DN** documented not supported; **IO** issue open; **IC** issue closed
(not fixed); **SRC** supported in source read, not run; **UNK** unknown (nothing found). "Not tried" applies to every
cell. Keys are in the source table below.

| Row | Claude (claude.ai, Desktop) | Claude Code (reference) | inference.coop chat (LibreChat) | VS Code Copilot agent |
|---|---|---|---|---|
| **a1** honours `tools/list_changed` | UNK in docs [C1, C2]. IC: apps keep the first list, web re-fetches per new conversation [C4]; stale in-chat tool index [C5] | DS, interactive: fetches new list; on failure keeps old; `-p` mode tools only [K1] | DS [L2]; SRC: `ToolListChangedNotificationSchema` handler calls `refreshToolList` [L3] | SRC: `onDidChangeToolList` calls `updateTools` [V6, V7]. Docs say verify per client [V3]. IO: Configure Tools picker stale after change #349603 [V9] |
| a2 prompts/resources list_changed | UNK; resource subscriptions DN [C1] | DS: "tools, prompts, or resources" [K1] | SRC: resources handler [L3]; prompts UNK | SRC prompts yes; resources list-changed not handled [V6] |
| a3 re-lists on its own at other times | UNK; web: each new conversation (issue claim) [C4] | DS: on reconnect, `/mcp reconnect`; discovery retried 3 times [K1] | UNK; DS: idle connection closes after 15 min, reopens on next use [L1] | SRC: on connect, from cache first, and after each tool call (`awaitToolRefresh`) [V6] |
| **b1** static custom headers | DS, beta, limited orgs, max four, names approved by Anthropic, same value for all users [C2] | DS `--header`, `.mcp.json` `headers` [K1] | DS: UI API key with Bearer/Basic/Custom name [L1]; YAML `headers` [L2] | DS `headers` in `mcp.json` [V2] |
| b2 per-user placeholders | DN: one shared value; per-user needs OAuth [C2] | DS `${VAR}`, `${VAR:-d}`; credential names read empty [K1] | DS YAML only: `{{LIBRECHAT_USER_*}}`, `customUserVars`; stripped on UI-created servers [L1, L2] | DS `${input:}` (prompted once), `${env:}` [V2] |
| b3 per-request headers | DN (fixed) [C2] | DS `headersHelper` runs per connection, not per call [K1] | DS YAML `requestHeaders`, per chat request, with body placeholders; omitted at discovery [L2] | UNK (not documented) |
| b4 sends/handles `Mcp-Session-Id`, 404 | UNK. Stateless servers reported working [C5] | UNK ("not covered" in visible text) [K1] | SRC: SDK transport; DELETE on close; 404 "no dedicated reconnect branch" then reconnect, 3 tries [L3]. Lab run: re-initialised [L6] | UNK: transport file not located; handler has no 404 logic [V7] |
| b5 transports | DS Streamable HTTP and legacy SSE; `/sse` URL picks SSE [C1, C2] | DS HTTP, SSE (deprecated, auto-fallback), stdio, ws [K1] | DS `streamable-http`, `sse`, `websocket` [L2]; UI: Streamable HTTPS or SSE [L1, L6] | DS `http` then SSE fallback [V2] |
| **c1** elicitation | UNK (only sampling and subscriptions listed as unsupported [C1]) | DS form and url; dialog in terminal [K1] | UNK in docs [L1, L2]; SRC: no elicitation capability in code read [L3] | DS in Copilot sessions: form and url, cancelled in Autopilot, declined with no active turn [V3, V4]; SRC capability declared if handler set [V7] |
| c2 sampling | DN [C1] | UNK | UNK; SRC none declared [L3] | DS with per-server approval [V3] |
| c3 `isError: true` treated differently | UNK. Spec: SHOULD reach the model [S2] | DS: text becomes the error message; over about 11,000 characters middle cut [K1] | SRC: no special formatting; flag only in a hash [L4] | SRC: read into `details.isError`, content unchanged [V8] |
| c4 prompts shown | DS "exposable" [C1]; how shown UNK | DS `/mcp__server__prompt` [K1] | UNK (the guide assumes the chat may offer them [L6]) | DN in Copilot sessions; DS in Local harness `/mcp.server.prompt` [V3, V4] |
| c5 resources shown | DS text and binary exposable [C1]; how shown UNK | DS `@` mentions [K1] | UNK | DN in Copilot sessions except MCP Apps; Local harness browser [V3, V4] |
| **d** images in tool results | DS "image-based" results [C1] | DS PNG/JPEG/GIF/WebP inline, original saved to a file [K1] | SRC: becomes `image_url`; 10 MiB cap; non-listed providers get no vision input [L4] | SRC: image/audio become inline data, resized [V8]; docs silent |
| **e1** tool-count limit | UNK; Claude Code tool-search default on [K1] | DS no fixed cap; tool search defers definitions [K1] | UNK | DS 128 per request, Local harness; virtual tools setting [V5]; Copilot harness UNK |
| e2 approvals | DS per-tool Always allow, Blocked [C2] | DS permissions, ask rules [K1] | UNK for general tools; DS only for MCP Apps [L1] | SRC: confirm unless `readOnlyHint`; `openWorldHint` asks about results [V8] |
| **f** protocol revision spoken | Auth specs 2025-03-26, 2025-06-18, 2025-11-25 [C1] | 2026-07-28 "v2 runtime" and earlier [K1] | UNK (SDK version not seen) | UNK; docs link 2025-06-18, 2025-11-25 [V3] |

| Spec row f | 2025-11-25 (what SDK 1.30.0 implements) | 2026-07-28 (latest) |
|---|---|---|
| listChanged | `tools.listChanged` capability; `notifications/tools/list_changed` SHOULD be sent; client re-lists [S2] | Only on a `subscriptions/listen` stream; tool list MUST NOT vary per connection [S1, S4] |
| `_meta` | Field present on SDK request, result and notification types [S7] | Required on every request: protocolVersion, clientInfo, clientCapabilities [S1] |
| HTTP headers | `Mcp-Session-Id` from server, echoed by client; 404 means re-initialise; `MCP-Protocol-Version` [S3] | No session; `MCP-Protocol-Version`, `Mcp-Method`, `Mcp-Name`; `Mcp-Param-*` from `x-mcp-header` [S4] |
| elicitation | Server request on a stream; form and url modes (url added 2025-11-25) [S6] | Returned as `input_required` result; client retries with answers [S1, S6] |
| clarification as normal result | Spec silent; ordinary result [S2] | Same; `input_required` is the structured alternative [S1] |
| SDK 1.30.0 | `SUPPORTED_PROTOCOL_VERSIONS` 2024-11-05 to 2025-11-25; `Context.elicit`, `elicit_url`; `listChanged` off unless `NotificationOptions` set [S7] | Not implemented |

**Sources** (O = opened and read; S = seen only as a search result; L = local file)

| Key | URL or path | How |
|---|---|---|
| S1 | https://modelcontextprotocol.io/specification/latest/server/tools | O |
| S2 | https://modelcontextprotocol.io/specification/2025-11-25/server/tools | O |
| S3 | https://modelcontextprotocol.io/specification/2025-11-25/basic/transports | O |
| S4 | https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | O |
| S5 | https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning | O |
| S6 | https://modelcontextprotocol.io/specification/latest/client/elicitation | O |
| S7 | /Users/z/Documents/GitHub/scat-wt/rs5-u5/.venv/lib/python3.12/site-packages/mcp (1.30.0) | L, read |
| C1 | https://claude.com/docs/connectors/building.md | O |
| C2 | https://claude.com/docs/connectors/custom/remote-mcp.md | O |
| C4 | https://github.com/anthropics/claude-code/issues/38324 | O |
| C5 | https://github.com/anthropics/claude-ai-mcp/issues/552 | O |
| K1 | https://code.claude.com/docs/en/mcp | O (all but a middle slice) |
| L1 | https://www.librechat.ai/docs/features/mcp | O |
| L2 | https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/mcp_servers | O |
| L3 | https://raw.githubusercontent.com/danny-avila/LibreChat/main/packages/api/src/mcp/connection.ts | O (first 100,000 of 121,365 characters) |
| L4 | https://raw.githubusercontent.com/danny-avila/LibreChat/main/packages/api/src/mcp/parsers.ts | O |
| L5 | https://docs.inference.coop/operations/infrastructure | O |
| L6 | research/chat-path/readout.md, docs/chat-path.md (this worktree) | L |
| V2 | https://code.visualstudio.com/docs/copilot/reference/mcp-configuration | O |
| V3 | https://code.visualstudio.com/api/extension-guides/ai/mcp | O |
| V4 | https://code.visualstudio.com/docs/copilot/guides/mcp-developer-guide | O |
| V5 | https://code.visualstudio.com/docs/agents/run/tools | O |
| V6 | https://raw.githubusercontent.com/microsoft/vscode/main/src/vs/workbench/contrib/mcp/common/mcpServer.ts | O |
| V7 | .../mcp/common/mcpServerRequestHandler.ts (same repo and branch) | O |
| V8 | .../mcp/common/mcpLanguageModelToolContribution.ts | O |
| V9 | https://github.com/microsoft/vscode/issues/349603 | S (GitHub search API listing; not opened) |
| (also read, no cell) | https://code.visualstudio.com/docs/copilot/customization/mcp-servers; https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp | O |

<!-- matrix:end -->

## What the sources do not say about the inference.coop chat

inference.coop's page names LibreChat as the member chat and gives no version [L5]. It does not mention MCP [L5]. Every
LibreChat statement above is therefore about upstream LibreChat's current `main` and docs, not about the co-op's
build. The co-op's own admin settings (allowed addresses, whether the "Add MCP" form is the only path) are unknown.

## Clarification mechanisms and the lowest common denominator

The protocol offers three ways to ask the user something:

- **Elicitation** (a server request for a form or url). It needs the client to declare the capability and, in
  2025-11-25, a connection on which the server may send requests. Claude Code and VS Code's Copilot sessions declare
  it [K1, V3, V7]; claude.ai is unknown; LibreChat's code shows none [L3]. A stateless server cannot use it, by
  inference from the 2025-11-25 transport text [S3].
- **A normal tool result** whose text states the question and the allowed answers. The model puts it to the user. Spec
  text is silent; it is an ordinary result [S2]. Every client above passes result text to the model.
- **A prompt** (a user-chosen template). Not model-reachable, and VS Code's Copilot sessions do not expose prompts
  [V3].

The lowest common denominator is the normal result. A result marked `isError` also reaches the model, but only Claude
Code documents how [K1]; for a question that is not a fault, use a normal result. Elicitation is a bonus where a
client declares it, and the server must work without it.

## Needs a client trial

**Claude (claude.ai, Desktop).**
- Does it re-list after `notifications/tools/list_changed`, within a conversation and in a new one? Does the answer
  differ between web and Desktop [C4]?
- Is elicitation declared, and does a form show?
- Does an `isError` result differ from a normal one in what the model sees?
- Does it send `Mcp-Session-Id`, and re-initialise after a 404?
- Are prompts and resources visible to the user or only the assistant?
- Is the request-header feature present on this account (beta)? Is a stage-named header accepted?

**inference.coop chat (LibreChat).**
- Which LibreChat version runs, and is the "Add MCP" form the only path?
- Does an agent in a running conversation see a changed tool list, or only after reconnect?
- After a session loss, does it re-initialise on every call or only after a restart (the lab run saw one case)?
- Is elicitation declared? Are prompts and resources shown? Do `isError` results look different?
- Are MCP tool calls approved per call? Does an image result reach a vision model, per provider?

**VS Code Copilot agent.**
- Which harness (Copilot or Local) and VS Code version does the user have, and is the main-branch source what ships?
- Does a changed tool list reach the model mid-turn, or only the next turn?
- What happens to a 404 on a stale session?
- Do approvals prompt for each stage-changing call? How does the tool count behave in the Copilot harness?
- Does a Copilot-session elicitation form appear, and is the answer returned?

**Claude Code (reference).**
- Does `list_changed` still work over Streamable HTTP on the installed version (regression reports exist as search
  results only)?
- Is the session ID re-initialised after loss? Does tool search hide a newly listed tool?

## What was not done

Sources in the matrix marked O were read through a summarising fetch tool, so exact wording was not checked
line by line; the LibreChat code read stopped before tool calls. VS Code's HTTP transport file was not found, so
session handling there is unknown. No search for an open LibreChat or VS Code issue on session loss succeeded;
GitHub issue search returned an error for LibreChat.
