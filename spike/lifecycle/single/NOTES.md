# RS5-U3: how stage reaches a single stage-scoped server (spike notes)

SDK: `mcp` **1.30.0** (uv.lock; printed by `test_sdk_version`). All results are from the SDK's own client against a
throwaway FastMCP server over streamable HTTP on 127.0.0.1 (ephemeral port, in a thread, stopped by the fixture),
plus the in-memory transport where noted. No chat client was used: every "client support" cell below is **needs
client trial** unless it is about the SDK. Stage names and the stage table (`STAGES` in `stage_server.py`) are
placeholders; the 14 tools are stand-ins. Run: `uv run --frozen --extra mcp python -m pytest spike/lifecycle/single -q`
(pytest and ruff came with the default dev group of `uv sync --frozen --extra mcp`; nothing extra needed).

## Findings first

| Way of carrying stage | Class | One line |
|---|---|---|
| E1 header, set per connection | works (SDK) | Server reads it per request; the client sets it on the httpx client. Constant for the connection. Chat-client support: needs client trial. |
| E1 header, set per request | partly works | `ClientSession.call_tool` has no headers parameter; only an httpx event hook on the underlying client changes it per request (works, SDK-specific; no chat client will do this). |
| E1 URL query `?stage=` | works (SDK) | Same strength as the header, and it needs no custom-header support, only a connector URL. Constant per connection. |
| E1 path `/mcp/<stage>` | works (SDK) | Needs a 6-line ASGI rewrite (FastMCP routes only `/mcp`). One connector per stage, so effectively "a server per stage" without the servers. |
| E2 session value (`set_stage` tool) | works stateful; does not work stateless | Stage lives in server memory keyed by `Mcp-Session-Id`. Stateless mode forgets it; a server restart makes the client's next call fail with "Session terminated". |
| E3 argument on every call | works, with a cost | +882 bytes in tools/list for 9 tools (about 98 per tool). Omitted argument gives a clarification result. Works with every client that calls tools. |
| E4 request `_meta` | works (SDK); chat client use unlikely | SDK client sends custom keys on `call_tool(meta=...)` and `list_tools(params=...)`; the server reads `request_context.meta.model_extra`. Chat clients do not expose `_meta`: needs client trial. |
| E5 unknown stage: result | works | Structured clarification result, no protocol error. |
| E5 unknown stage: elicitation | partly works | Works only if the client declares the elicitation capability; the server must check first. |
| E6 out-of-stage call refused | works | Refusal result naming tool, stage, where it is available, who decides and how to move. |
| E7 per-session lists + list_changed | works (SDK), with 3 code details | Needs low-level handler overrides and a capability patch (below). Chat-client honouring: needs client trial. |

Five facts that decide how stage travels:

1. **A header or query value is constant for a connection.** The SDK client takes headers once, on the httpx client
   (`ClientSession.call_tool` has no headers parameter; the transport's own `headers=` argument is deprecated and
   ignored in 1.30.0). So header, query and path all mean "one stage per connection". Changing stage means a new
   connection, or an httpx event hook that no chat client offers. Whether a connector config allows a custom header
   (or only a URL): needs client trial.
2. **Session value works only on a stateful server and dies with it.** In stateless mode `set_stage` reports
   `moved: true` and the next request sees no stage (a trap: the server must refuse to offer `set_stage` when
   stateless). After a restart the client gets `McpError: Session terminated`, not a silent unknown stage; a fresh
   session starts at unknown. A stateful server is therefore required for E2 and E7.
3. **The per-session tool list is not FastMCP's out of the box.** FastMCP's tool manager is global and
   `listChanged` is advertised false. The cleanest way in 1.30.0 is: keep FastMCP for registration, then replace its
   three list handlers and `call_tool` with `@mcp._mcp_server.list_tools()` etc. (the low-level decorators; it
   uses the private `_mcp_server`) that filter by a data table; and wrap
   `_mcp_server.create_initialization_options` with `NotificationOptions(True, True, True)` so `listChanged: true`
   is advertised (in-memory and HTTP both call that method). `ctx.session.send_tool_list_changed()` then reaches that
   session only (tested with two sessions).
4. **The refusal is what makes list_changed optional.** A client that ignores the notification and calls a tool from
   its old list gets a result (not an error) saying where the tool is available and how to move. Scoping by the list
   is then a convenience and the refusal is the guarantee. The SDK client also re-lists tools silently on a call to a
   tool absent from its cache (log: "not listed by server, cannot validate"), so a re-list may happen without
   the application asking.
5. **Argument and `_meta` are the only carriers that are per request without client tricks**, and only the argument
   is something a chat client's model can supply. Argument costs schema bytes and relies on the assistant (who holds no
   authority) writing the coder's stage; the server cannot tell the assistant's guess from the coder's word, whichever
   carrier is used.

## E1 stage by header, query, path

Tried: `X-Scat-Stage` read in `tools/list` and `tools/call` handlers via `request_context.request.headers` (works in
the low-level handler and in a FastMCP tool: `ctx.request_context.request`); `?stage=` via `request.query_params`;
`/mcp/<stage>` via an ASGI wrapper that rewrites the path to `/mcp` and stores the stage on the scope.
Tests: `test_e1_header_per_connection`, `test_e1_header_per_request_needs_httpx_event_hook`,
`test_e1_sdk_call_tool_has_no_per_request_header_parameter`, `test_e1_query_parameter`, `test_e1_path_variant`.

- Per connection: `create_mcp_http_client(headers=...)` passed as `http_client` to `streamable_http_client`. Works.
- Per request: a request event hook that sets the header from a variable, on the same MCP session, gave plan, code,
  analyse in turn; the server saw each. Works but is client-code, not an SDK parameter.
- In a stateful session the header is read on every request, so a header still present overrides a stage set by
  `set_stage` when the carriers are tried header first (order is a server setting; first carrier with a value wins).
- A static header implies one stage per connector entry; changing stage means editing the entry or adding another.
- Not known: whether Claude, inference.coop or VS Code Copilot let a connector set a custom header (needs client
  trial); `Mcp-Session-Id` and `MCP-Protocol-Version` are sent by the SDK on every request after initialize.

## E2 stage by session value

Tried: `set_stage(stage, coder_word)` stores stage under the `Mcp-Session-Id` header value (or a per-object key in
memory); later calls and list requests read it. Without `coder_word` it records a request and moves nothing (the
server cannot verify the word; this is a convention only).
Tests: `test_e2_session_value_stateful`, `test_e2_session_value_lost_in_stateless_mode`,
`test_e2_session_value_lost_when_server_restarts`.

- Stateful: works; `which_stage` reports carrier `session`.
- Stateless (`FastMCP(stateless_http=True)`): each request gets a new session, no id; stage is unknown on the next
  request and list_changed notifications never arrive (0 received). `set_stage` still said moved: true.
- Restart (same address, new server object): the old session id is unknown to the new server and the next
  `call_tool` raised `McpError: Session terminated`. A reconnect is a fresh session at unknown stage.
- Not known: whether chat clients reconnect after that error without the user noticing (needs client trial);
  persistence of stage across sessions is not tried (not needed to answer the question).

## E3 stage by argument

Tried: `stage` enum property injected into every non-always tool's schema in tools/list; handler reads and strips
it. Tests: `test_e3_argument_on_each_call_and_omitted`, `test_e3_argument_schema_cost`.

- Present and valid: runs the tool. Omitted or invalid: clarification result (E5), no exception.
- Cost: tools/list 2518 bytes without, 3400 with, for the 9 scoped stand-in tools (+882, about 98 bytes per tool;
  scales with tool count, so about 1.9 KB for 19 tools). The argument also appears in every tool's description of
  parameters that the assistant must fill each call.
- Not known: how reliably an assistant carries the stage across calls (needs client trial).

## E4 per-request _meta

Tried: `call_tool(..., meta={"scat-stage": "code"})` and `list_tools(params=PaginatedRequestParams(_meta=...))`.
Tests: `test_e4_meta_on_call_tool`, `test_e4_meta_on_list_tools_and_in_memory`.

- The SDK client accepts arbitrary keys (`RequestParams.Meta` allows extras) and sends them; the server reads
  `ctx.request_context.meta.model_extra["scat-stage"]` in handlers and tools. Per request, not remembered.
  Works over HTTP and in-memory.
- Only an application built on the SDK can set it; chat clients are not expected to expose `_meta` (needs client trial).

## E5 unknown stage

Tried: no stage, and an invalid stage (`bogus`), on a tool call. The server returns a `CallToolResult` with text and
`structuredContent` holding the known stages (one line each: what it is, what it allows), who decides ("the coder
decides the stage; the assistant asks the coder") and how to move. Variants `isError` false and true. Elicitation
by `session.elicit_form` in an `ask_stage` tool.
Tests: `test_e5_unknown_stage_returns_result_not_protocol_error[False/True]`,
`test_e5_elicitation_needs_client_callback`.

- Both variants arrive as a normal tool result: the SDK client raises nothing, `isError` is the only difference.
  With the unknown stage, tools/list shows only the always-on tools (`set_stage`, `which_stage`, `ask_stage`).
- Which an LLM-facing client surfaces: not tested. Reasoning only: the spec puts tool failures the model can act on
  in results with `isError: true` precisely so the model sees them, so `isError: true` is likely at least as visible;
  some hosts may render `isError` as a failure state and some may drop structured content. Needs client trial for
  Claude, inference.coop and VS Code Copilot. The text alone carries the full clarification so either variant is
  usable.
- Elicitation: the SDK client advertises the capability only when given an `elicitation_callback`; with a callback
  `ask_stage` got `accept` and the chosen stage; without, the server's `check_client_capability` is false and the tool
  returns a result saying so (if it sent the request anyway the SDK default callback answers with an error). Many chat
  clients may not support elicitation: needs client trial. Elicitation asks the user, which fits "the coder decides",
  but it is a second path; the result path is the one that always works.

## E6 out-of-stage call

Tried: at stage `plan` call `record_edge` (not listed) and `export_edges`. Test:
`test_e6_out_of_stage_call_refused_with_where_and_how`.

- Result (isError false, configurable): names the tool, the current stage, the stages where it is available, the
  known stages, who decides, and how to move (`set_stage` on the coder's word). This is also the answer for clients
  that never refresh their list (the call goes straight to the handler; the list does not gate it).
- Not known: what the assistant does after reading it (needs client trial).

## E7 list-changed and per-session scoping

Tried: low-level `list_tools`, `list_prompts`, `list_resources` handlers filtering by the table (tools, prompts,
resources); `set_stage` sends tools, prompts and resources `list_changed` to its own session; capability patch.
Tests: `test_e7_capabilities_advertise_list_changed_only_when_configured`,
`test_e7_tools_prompts_resources_scoped_per_stage_and_unscoped_default`,
`test_e7_set_stage_notifies_that_session_only_and_relist_shows_new_tools`,
`test_e7_concurrent_sessions_see_different_lists`, `test_e7_client_that_ignores_notification_hits_the_refusal`,
`test_e7_in_memory_transport_same_behaviour`, `test_e7_stateless_mode_cannot_scope_by_session`.

- Default FastMCP: `tools.listChanged` false, and the list is global (12 tools for every client). Overridden as in
  fact 3: works.
- Notifications arrive at the SDK client's `message_handler` on the standalone GET stream (HTTP) and in-memory; session
  B got none when A moved; a re-list after the notification shows the new stage's tools. Two concurrent sessions at
  different stages see different lists.
- `get_prompt` and `read_resource` stay FastMCP's own and are not gated by stage (only the lists are). Gating them
  would be a call-time refusal like E6; not built.
- Stateless: no notifications reach the client; per-session scoping is impossible.
- Not known: whether Claude, inference.coop and VS Code Copilot honour `list_changed` or re-list (needs client
  trial; this is RS5-R3). The refusal (E6) is the fallback.

## E8 cost

Tests: `test_e8_carrier_cost_in_lines`, `test_e8_real_server_tools_can_be_scoped_by_data_only`.

| Variant | Code |
|---|---|
| header, query, path, argument, meta, session (reader function each) | 2 to 3 lines each; path adds a 6-line ASGI wrapper; session adds the `set_stage` tool (about 12 lines) |
| Scoped lists (tools, prompts, resources) and list_changed patch | about 45 lines, shared by all carriers |
| Clarification and refusal result | about 20 lines, shared |
| Argument carrier | extra 12 lines for schema injection, and +98 bytes per tool in tools/list |
| Whole spike server (`stage_server.py`) | 300 lines with stand-in tools, prompts and resources |

The real server (`src/scat_kg/mcp_server/server.py`) registers 19 tools. The test builds it on an empty temp
folder, lists the 19 names and shows that a stage table of names alone (data, no code change to the server's
tools) gives each stage its set via `scope()`, with every real tool in at least one stage (a lint a real table
should keep). The scoping code itself would be new to the real server (the handler overrides and capability
patch), and the real server's tools would need no edit. The stage table in the test is a placeholder, not a
proposal.

## What a chat client must support, per option

| Option | Client must |
|---|---|
| Header | let a connector set a custom request header (static); nothing else |
| Query / path | take a connector URL with that query or path; nothing else |
| Session value | call `set_stage` when told by the coder; keep one MCP session (stateful server) |
| Argument | include `stage` in every call, from the tool schema |
| `_meta` | expose per-request `_meta` to the user or the model (unlikely) |
| Per-session list scoping | re-list tools after `notifications/tools/list_changed` (else the E6 refusal catches stale calls) |
| Elicitation | declare the elicitation capability and show the form to the user |
| Clarification result | nothing beyond reading a tool result (every client) |

All cells about real clients: **needs client trial**.

## Flagged

- Uses the private `FastMCP._mcp_server` and `_tool_manager`-adjacent paths (`mcp._mcp_server`, `request_context`);
  fine for a spike, an SDK upgrade could move them.
- Stateless `set_stage` returns `moved: true` though nothing is kept (left as observed).
- `coder_word` is a convention, not authentication: the server cannot tell the coder's word from the assistant's
  claim of it.
