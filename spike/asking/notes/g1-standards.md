# RS7-U1 / G1: what the standards say about a server asking the coder mid-call

Fetched 2026-11-27 with WebFetch/WebSearch only. Nothing was tried against any chat service. All client rows are "documented, not tried".

Reading convention. "Read directly" means the page text came back and the quoted words were on it. WebFetch passes each page through a small model, so every row is at best a machine-extracted reading of the page; where the tool said it only saw a truncated part or gave a summary, the row says "summary only". Quotes are under 15 words. MUST/SHOULD/MAY are as printed on the page.

Spec URL bases:
- 2025-06-18: https://modelcontextprotocol.io/specification/2025-06-18/
- 2025-11-25: https://modelcontextprotocol.io/specification/2025-11-25/
- 2026-07-28: https://modelcontextprotocol.io/specification/2026-07-28/ (exists, published; its changelog lists it as the revision after 2025-11-25)
- 2025-03-26 (optional context): not fetched; only referenced from other pages.

Abbreviations: E1 = elicitation page (client/elicitation), T = basic/transports (2026: basic/transports/streamable-http), MRTR = 2026 basic/patterns/mrtr.

---

## Q1. Elicitation

| Claim | Version | Page URL | Quote / paraphrase | Read |
|---|---|---|---|---|
| Only one mode: form (no `mode` field) | 2025-06-18 | .../2025-06-18/client/elicitation | Request is `elicitation/create` with `message` and `requestedSchema`. No `mode`, no url mode. | directly |
| Capability: client MUST declare `elicitation`, as `{}`, at initialize | 2025-06-18 | same | "Clients that support elicitation MUST declare the `elicitation` capability" | directly |
| Two modes: form and url | 2025-11-25 | .../2025-11-25/client/elicitation | "Form mode" (data exposed to client) and "URL mode" (out-of-band, data not exposed to client). | directly |
| Sub-capabilities `form`, `url`; empty object means form only | 2025-11-25 | same | "an empty capabilities object is equivalent to declaring support for `form` mode only" | directly |
| Client declaring `elicitation` must support one mode; server must not send an undeclared mode | 2025-11-25 | same | "Servers MUST NOT send elicitation requests with modes that are not supported by the client." Client returns -32602 for an undeclared mode. | directly |
| `mode` optional for form; clients treat missing mode as form | 2025-11-25 | same | "Clients MUST treat requests without a `mode` field as form mode." | directly |
| Form schema: flat object, primitives only | 2025-06-18 | .../2025-06-18/client/elicitation | "limited to flat objects with primitive properties only"; string (format email/uri/date/date-time), number/integer, boolean, enum with `enumNames`. | directly |
| Form schema adds `default` on all primitives, `pattern`, titled single enum (`oneOf` const/title), multi-select enum (array of enum / `anyOf`) | 2025-11-25 | .../2025-11-25/client/elicitation | "Clients that support defaults SHOULD pre-populate form fields with these values." | directly |
| 2026: schema limited to strings, numbers, booleans, enums; only array allowed is multi-select enum | 2026-07-28 | .../2026-07-28/client/elicitation | "The only array properties allowed are multi-select enums." | directly |
| Three actions: accept / decline / cancel | all three | E1 of each version | accept = "User explicitly approved and submitted with data"; decline = explicitly declined; cancel = dismissed without explicit choice (closed dialog, Escape). Server "should handle each state appropriately". | directly |
| What a client MUST show (2025-06-18 uses SHOULD) | 2025-06-18 | .../2025-06-18/client/elicitation | Applications SHOULD: make clear which server asks; let users review and modify answers; "provide clear decline and cancel options". | directly |
| What a client MUST show (strengthened to MUST) | 2025-11-25, 2026-07-28 | E1 of each | "MCP clients MUST: Provide UI that makes it clear which server is requesting information"; "clear decline and cancel options"; for form mode "allow users to review and modify". | directly |
| Servers MUST NOT ask sensitive information via form | 2025-06-18 | E1 | "Servers MUST NOT use elicitation to request sensitive information" | directly |
| Same, narrowed and with a MUST for URL mode; name/email/username not categorically prohibited | 2025-11-25, 2026-07-28 | E1 | "MUST NOT use form mode elicitation to request sensitive information such as passwords, API keys, access tokens"; "MUST use URL mode" for such. | directly |
| Clients SHOULD allow decline at any time; SHOULD rate limit | 2025-06-18, 2025-11-25 | E1 Security Considerations | "Clients SHOULD allow users to decline elicitation requests at any time". 2026 drops the rate-limiting line. | directly |
| URL mode: requires `url`, `elicitationId` (2025-11-25 only) | 2025-11-25 | E1 | "URL mode elicitation requests MUST specify `mode: "url"`" with `url` and `elicitationId`. `accept` means consent to open, not completion. | directly |
| URL mode: `notifications/elicitation/complete` (server MAY send; must be sent only to the client that asked) | 2025-11-25 | E1 | "Servers MAY send a `notifications/elicitation/complete` notification" | directly |
| URL mode: error `-32042` URLElicitationRequiredError returned instead of a result | 2025-11-25 | E1 | "The server MUST NOT return this error except when URL mode elicitation is required." | directly |
| URL mode client rules | 2025-11-25, 2026-07-28 | E1 | Clients MUST NOT pre-fetch the URL, MUST NOT open it without explicit consent, MUST show the full URL. Servers MUST NOT put sensitive data or a pre-authenticated URL in it. | directly |
| 2026: `notifications/elicitation/complete` and `elicitationId` REMOVED | 2026-07-28 | .../2026-07-28/changelog | "Remove the `notifications/elicitation/complete` notification and the `elicitationId` field" | directly |
| Timeouts: no elicitation-specific timeout stated | all three | E1 of each | Not found on any E1 page. General rule only: "Implementations SHOULD establish timeouts for all sent requests" (lifecycle, 2025-06-18: .../2025-06-18/basic/lifecycle#timeouts), then SHOULD send cancellation. | directly (general rule) |
| Elicitation is "nested inside other MCP server features" | 2025-06-18, 2025-11-25, 2026-07-28 | E1 "User Interaction Model" | "enabling user input requests to occur *nested* inside other MCP server features." | directly |
| Which stream/request an elicitation is sent on: E1 says nothing about streams | 2025-06-18, 2025-11-25 | E1 | Not found on the elicitation page. The rule is in transports (see Q2). | directly |
| 2026: elicitation is no longer a server-to-client request; it is an `InputRequiredResult` containing `elicitation/create` | 2026-07-28 | .../2026-07-28/client/elicitation | "Servers MAY request information from a user ... by sending an `InputRequiredResult`"; client answers in `inputResponses` on a retried request. | directly |
| 2026: capability declared per request, not at initialize | 2026-07-28 | same | "declare the `elicitation` capability in `_meta.io.modelcontextprotocol/clientCapabilities` on each request"; empty object still means form only. | directly |
| 2026: server must handle failure | 2026-07-28 | same | "Servers SHOULD NOT assume that elicitation requests will always succeed, and MUST handle cases where the user declines or cancels ... or where the client fails to process the request." | directly |
| 2026: URL mode accept does not mean done; server learns on retry | 2026-07-28 | same | "the server determines from the echoed `requestState` (or its own stored state) whether the out-of-band interaction has completed" | directly |

## Q2. Transport

| Claim | Version | Page URL | Quote / paraphrase | Read |
|---|---|---|---|---|
| Server may send requests on a POST's SSE stream before the response; they SHOULD relate to the originating request | 2025-06-18, 2025-11-25 | .../2025-06-18/basic/transports ; .../2025-11-25/basic/transports ("Sending Messages to the Server", item 6) | "The server MAY send JSON-RPC *requests* and *notifications* before sending the JSON-RPC *response*. These messages SHOULD relate to the originating client *request*." | directly |
| POST response must be `text/event-stream` for that to happen; the server chooses per request | both | same, item 5 | "the server MUST either return `Content-Type: text/event-stream`, to initiate an SSE stream, or `Content-Type: application/json`, to return one JSON object. The client MUST support both." Server requests can only ride an SSE stream; a single JSON object can carry only the response. (The second sentence is my inference from the two options; the page does not say it in one line.) | directly (inference marked) |
| Client MUST send Accept listing both content types | both | same, item 2 | "listing both `application/json` and `text/event-stream`" | directly |
| GET stream: client MAY open it; server MAY send requests/notifications on it; they SHOULD be unrelated to any running request | both | same, "Listening for Messages from the Server" | "These messages SHOULD be unrelated to any concurrently-running JSON-RPC *request* from the client." Server either returns text/event-stream or "HTTP 405 Method Not Allowed". | directly |
| Client is not required to open the GET stream | both | same | "The client MAY issue an HTTP GET to the MCP endpoint." (MAY) | directly |
| A message goes on one stream only | both | same, "Multiple Connections" | "MUST send each of its JSON-RPC messages on only one of the connected streams" | directly |
| Server MUST NOT send a JSON-RPC response on the GET stream unless resuming | both | same | "MUST NOT send a JSON-RPC *response* on the stream unless resuming" | directly |
| Client answers a server request by a new POST whose body is a JSON-RPC response; server returns 202, no body | both | same, items 1, 3, 4 | "If the server accepts the input, the server MUST return HTTP status code 202 Accepted with no body." | directly |
| Disconnect is not cancel (2025 versions) | both | same | "Disconnection SHOULD NOT be interpreted as the client cancelling its request." | directly |
| Resumability: server MAY attach SSE event ids; resume via GET with Last-Event-ID, on the stream that was disconnected | both | same, "Resumability and Redelivery" | "MUST NOT replay messages that would have been delivered on a different stream." | directly |
| 2025-11-25 adds polling: prime event, `retry` field, server may close the connection and client reconnects | 2025-11-25 | .../2025-11-25/basic/transports | "The client MUST respect the `retry` field" | directly |
| Session id is optional; server MAY assign `Mcp-Session-Id` (2025-06-18) / `MCP-Session-Id` (2025-11-25) at initialize; if assigned, client MUST echo it | both | same, "Session Management" | "MAY assign a session ID at initialization time" | directly |
| Stateless server (no session id) is allowed; request/response routing is by stream, not by session | both | same | Session ID is "MAY". The routing rules above mention no session. The spec does not discuss "stateless" by name and does not say a stateless server may or may not send server requests. | directly (absence noted) |
| Capability use is bounded by negotiation | 2025-06-18 | .../2025-06-18/basic/lifecycle | "Only use capabilities that were successfully negotiated" | directly |
| Server SHOULD NOT send requests (other than ping/logging) before `initialized` | 2025-06-18 | same | quoted from lifecycle | directly |
| 2026: no protocol-level sessions, no GET stream, no `Mcp-Session-Id` | 2026-07-28 | .../2026-07-28/changelog (items 1, 2, 4) ; .../2026-07-28/basic/transports/streamable-http (top notes) | "Remove protocol-level sessions and the `Mcp-Session-Id` header"; "remove the `initialize`/`notifications/initialized` handshake"; "Replace the HTTP GET endpoint ... with `subscriptions/listen`". The RS5 readout is confirmed. | directly |
| 2026: server MUST NOT send independent requests on any stream | 2026-07-28 | .../2026-07-28/basic/transports/streamable-http, "Receiving Messages" | "The server MUST NOT send independent JSON-RPC *requests* on this stream." Elicitation etc. "embedded in results as input requests" per MRTR. | directly |
| 2026: SSE response stream carries only request-related notifications then the response | 2026-07-28 | same | notifications "MUST relate to the originating client request" | directly |
| 2026: closing the SSE response stream = cancellation | 2026-07-28 | same, "Cancellation" | "Closing the SSE response stream MUST be treated by the server as cancellation of that request." | directly |
| 2026: no resumability | 2026-07-28 | same + changelog item 9 | "Resumable SSE streams via `Last-Event-ID` are not supported." Broken stream loses the call; client re-issues with a new id. | directly |
| 2026: `subscriptions/listen` is a long-lived POST response stream for list-changed / resource notifications, opt-in | 2026-07-28 | same + changelog item 4 | Request-scoped notifications do NOT go on it. | directly |
| 2026 MRTR: what replaces server-to-client requests | 2026-07-28 | .../2026-07-28/basic/patterns/mrtr | "Servers MUST send server-to-client requests ... using the MRTR pattern. The previous pattern ... is no longer supported." Applies to `tools/call`, `prompts/get`, `resources/read` only. Client retries with a new JSON-RPC id, `inputResponses`, and echoes `requestState`. | directly |
| 2026 MRTR: server MUST NOT ask for a capability the client did not declare | 2026-07-28 | same, Server Requirements 7 | "if a client does not declare support for `elicitation`, the server MUST NOT include any `elicitation/create` requests" | directly |
| 2026 MRTR: server must not assume the client will answer or retry | 2026-07-28 | same, Server Requirements 8 | "Servers MUST NOT assume that clients will fulfill the `inputRequests` or retry the original request." | directly |
| 2026 MRTR: `requestState` is attacker-controlled; integrity-protect it; SHOULD carry principal, short TTL, request digest | 2026-07-28 | same, Server Requirements 4, 5 | "MUST treat `requestState` as an attacker-controlled input" | directly |
| 2026: missing client capability error `-32021` MissingRequiredClientCapabilityError, HTTP 400 | 2026-07-28 | .../2026-07-28/schema (first 100k chars only) | "Returned when processing a request requires a capability the client did not declare." Example uses `elicitation`. | summary only (schema page 115k chars unread) |
| 2026 dual-era: older clients (initialize + sessions) still reach a server that implements both; "server-initiated" requests belong to those revisions | 2026-07-28 | .../2026-07-28/basic/versioning (compat matrix), .../2026-07-28/basic/transports/streamable-http ("Earlier Streamable HTTP Revisions") | A modern-only server answers GET with 405 and ignores `Mcp-Session-Id`. A dual-era server selects behaviour by how the client opens: per-request `_meta` = modern; `initialize` = legacy. | directly |
| Legacy HTTP+SSE (2024-11-05): deprecated; clients fall back after POST fails with 4xx and GET returns `endpoint` event | 2025-06-18, 2025-11-25, 2026-07-28 | transports pages, "Backwards Compatibility"; 2026 reclassified Deprecated | The 2024-11-05 page itself was not fetched. | directly (compat section only) |

## Q3. Related mechanisms, and the Python SDK

| Claim | Version | Page URL | Quote / paraphrase | Read |
|---|---|---|---|---|
| Sampling: client controls model; human in the loop | 2025-06-18, 2025-11-25, 2026-07-28 | .../client/sampling of each | "there SHOULD always be a human in the loop with the ability to deny sampling requests." Client "maintain[s] control over model access, selection, and permissions"; hints are advisory ("Clients MAY"...). Schema: "The client has full discretion over which model to select." (2025-11-25 schema) | directly (schema: partly via persisted fetch) |
| Sampling capability `sampling`; 2025-11-25 adds `sampling.tools`, `sampling.context` | 2025-11-25 | .../2025-11-25/client/sampling | "Servers MUST NOT send tool-enabled sampling requests to Clients that have not declared ... `sampling.tools`" | directly |
| Sampling is DEPRECATED in 2026-07-28, moves to MRTR | 2026-07-28 | .../2026-07-28/client/sampling ; changelog "Deprecated" 1 | "New implementations SHOULD NOT adopt it" | directly |
| Roots: capability `roots`; `roots/list` server request; error -32601 if unsupported | 2025-11-25 | .../2025-11-25/client/roots | Clients "MUST declare the `roots` capability". 2026: deprecated, `notifications/roots/list_changed` removed. | directly (2025-11-25); 2026 via changelog |
| Tools: human in the loop | 2025-06-18, 2025-11-25, 2026-07-28 | .../server/tools of each, "User Interaction Model" | "there SHOULD always be a human in the loop with the ability to deny tool invocations." Apps SHOULD "Present confirmation prompts to the user for operations". | directly |
| Tools: clients should prompt on sensitive operations | all three | same, Security Considerations | Clients SHOULD "Prompt for user confirmation on sensitive operations" and "Show tool inputs to the user before calling the server". | directly |
| Tool annotations are hints, untrusted unless from trusted server | all three | tools page "Tool" data type; schema | "clients MUST consider tool annotations to be untrusted unless they come from trusted servers." | directly |
| `ToolAnnotations` fields and defaults | 2025-11-25 | .../2025-11-25/schema (ToolAnnotations) | `title`; `readOnlyHint` default false; `destructiveHint` default true (meaningful only if readOnlyHint false); `idempotentHint` default false; `openWorldHint` default true. "all properties in ToolAnnotations are hints"; "Clients should never make tool use decisions based on ToolAnnotations received from untrusted servers." | directly (via a fetch that returned the 2025-11-25 schema text) |
| `ToolAnnotations` in 2025-06-18 | 2025-06-18 | .../2025-06-18/schema | Page confirms "ToolAnnotations are **hints**"; the full field text was not captured line by line. | summary only (heading + hint statement seen) |
| `ToolAnnotations` in 2026-07-28 | 2026-07-28 | .../2026-07-28/server/tools | Tool lists `annotations` and "untrusted" warning. Field-level text was not seen (schema fetch truncated before Tools). | not found (field text) |
| `isError`: tool failures go in the result, not as protocol errors | all three | tools "Error Handling"; 2025-11-25 schema CallToolResult | "Any errors that originate from the tool SHOULD be reported inside the result object, with `isError` set to true" | directly |
| 2025-11-25/2026: input validation errors are tool execution errors; clients SHOULD feed them to the model | 2025-11-25, 2026-07-28 | tools "Error Handling" | "Clients SHOULD provide tool execution errors to language models to enable self-correction." | directly |
| "Confirmation"/"approval" on prompts, resources, other pages | all | prompts/resources pages not fetched | Not found (not fetched). | not found |
| MRTR example is a booking confirmation using a boolean field in a form | 2026-07-28 | https://modelcontextprotocol.io/docs/2026-07-28/learn/client-concepts | Server "needs the user to confirm the booking" and returns `input_required` with an elicitation form (`confirmBooking` boolean). A confirm-by-elicitation pattern, in a non-normative guide. | directly |
| Python SDK `Context.elicit` passes `related_request_id=self.request_id`; `Context.elicit_url` likewise | v1.30.0 source | https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/v1.30.0/src/mcp/server/fastmcp/server.py | Both call `elicit_with_validation` / `_elicit_url` with `related_request_id=self.request_id`. | summary only (small-model reading of source) |
| Python SDK `ServerSession.elicit_form(message, requestedSchema, related_request_id=None)` | v1.30.0 source | .../v1.30.0/src/mcp/server/session.py | `related_request_id` is optional; passed as `ServerMessageMetadata(related_request_id=...)`. `elicit` there is deprecated alias for `elicit_form`. | summary only |
| Python SDK routing: untied messages go to the standalone GET stream; tied ones to that POST's stream | v1.30.0 source | .../v1.30.0/src/mcp/server/streamable_http.py | `request_stream_id = target_request_id if target_request_id is not None else GET_STREAM_KEY`; "# Special key for the standalone GET stream". | summary only |
| Python SDK with `json_response=True`: POST returns one JSON body; server requests tied to it are not sent | v1.30.0 source | same | Loop breaks on response/error only; "For notifications and request, keep waiting" (logged at debug). | summary only |
| Python SDK `session.elicit_form/elicit_url` do not check client capability themselves | v1.30.0 source | .../v1.30.0/src/mcp/server/session.py | `check_client_capability` only tests that `client_caps.elicitation` is not None; `{}` passes; no form/url distinction. Unsupported-client behaviour of `send_request` not shown. | summary only |
| SDK docs for 1.30.0: `ctx.elicit`, `ctx.elicit_url`; `ctx.session.send_elicit_complete`; no mention of `elicit_form`, capability checks, transport | v1.30.0 docs | https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/v1.30.0/docs/server.md | "Use `stateless_http=True` and `json_response=True` for optimal scalability" (recommended production setting). Says stateless "keeps no sessions". The page does not discuss elicitation under those settings. | summary only |
| Newer SDK docs (not shown to be 1.30.0): `ctx.elicit` is server-to-client, "work only on a legacy connection"; on 2026-07-28 "these calls fail"; use the Resolve/Elicit path | unversioned (page names protocol versions, no SDK version) | https://py.sdk.modelcontextprotocol.io/handlers/elicitation/ ; .../protocol-versions/ | "If the client registered no callback ... fails with a protocol error, `Elicitation not supported`." "Design every elicitation with a fallback for when asking isn't possible." Uses `Client(..., mode="legacy")`, which looks newer than 1.30.0; do not assume it describes 1.30.0. | summary only |

## Q4. Clients that do not implement elicitation: what is said

| Claim | Version | Page URL | Quote / paraphrase | Read |
|---|---|---|---|---|
| Server MUST NOT send what the client did not declare | 2025-11-25 | .../2025-11-25/client/elicitation | "Servers MUST NOT send elicitation requests with modes that are not supported by the client." | directly |
| Same, for the whole `inputRequests` | 2026-07-28 | MRTR, Server Requirements 7 | see Q2 | directly |
| No spec text tells a server what to put in a tool result when elicitation is unavailable | 2025-06-18, 2025-11-25, 2026-07-28 | all E1 pages, MRTR | Not found. The nearest: 2026 E1 "Servers SHOULD NOT assume that elicitation requests will always succeed". 2026 versioning: for extensions, "the supporting party MUST either revert to core protocol behavior or reject the request" (extensions only). | directly (absence) |
| SDK docs say design a fallback | unversioned newer SDK docs | https://py.sdk.modelcontextprotocol.io/handlers/elicitation/ | "Design every elicitation with a fallback for when asking isn't possible." | summary only |
| Client-side no-support behaviour for roots is specified (-32601); for elicitation only the -32602 (undeclared mode) and 2026 -32021 are specified | 2025-11-25, 2026-07-28 | roots page; E1; 2026 schema | | directly / summary only |

## Q5. Clients: official statements (all "documented, not tried")

MCP clients matrix at /clients: NOT FOUND. https://modelcontextprotocol.io/clients (fetched 2026-11-27) and /clients.md return the generic "What is MCP" landing page; /example-clients returned HTTP 404. https://modelcontextprotocol.io/extensions/client-matrix.md exists but covers extensions only (Apps, OAuth client credentials, Enterprise auth, Skills, Tasks, Events), with no elicitation column and empty cells for Claude (web), Claude Desktop, Claude Code and VS Code GitHub Copilot; LibreChat has no row. So no per-client elicitation row can be quoted from modelcontextprotocol.io as fetched.

| Client | Claim | Page URL | Quote / paraphrase | Fetched | Read |
|---|---|---|---|---|---|
| Claude Code | Shows form dialog or URL-mode prompt in the terminal; "No configuration is required"; Elicitation hook can auto-answer | https://code.claude.com/docs/en/mcp (section "Respond to MCP elicitation requests") | "Claude Code displays an interactive dialog in the terminal and passes your response back to the server." | 2026-11-27 | directly |
| Claude Code | Declares `elicitation: {form: {}, url: {}}` on connections using protocol revision 2026-07-28, and on 2025-11-25-and-older connections to stdio/sse/http/ws servers in the user's own MCP config (needs v2.1.287+) | same ("Elicitation modes Claude Code declares") | "Claude Code declares the bare `elicitation: {}`, which permits ... form mode only" on its other earlier-revision connections, "such as to claude.ai connectors". | 2026-11-27 | directly |
| Claude Code | In `claude -p` runs and Agent SDK sessions it asks the server to cancel without running Elicitation hooks; in VS Code/desktop app cancels unless a hook accepts (this passage is in the MCP tasks text) | same | "asks the server to cancel the task" | 2026-11-27 | directly (tasks context only) |
| Claude Code | Cloud sessions: answer on a card at claude.ai/code, "If you see no card ... you can't answer the request there." | same | | 2026-11-27 | directly |
| Claude Code | Hooks `Elicitation`, `ElicitationResult`; exit 2 on Elicitation declines | https://code.claude.com/docs/en/hooks | "When an MCP server requests user input during a tool call" | 2026-11-27 | summary only (page 300k chars, first 100k read) |
| Claude (claude.ai, Desktop, mobile) | Builder doc lists unsupported MCP features: "Resource subscriptions", "Sampling", "Advanced or draft capabilities"; elicitation is not named in either the supported or unsupported list | https://claude.com/docs/connectors/building | "Claude implements a subset of the MCP specification" | 2026-11-27 | directly |
| Claude (claude.ai, Desktop) | Tool call limit: "240 seconds per tool call" (Claude Code: `MCP_TOOL_TIMEOUT`) | same | | 2026-11-27 | directly |
| Claude (claude.ai, Desktop) | Transports: Streamable HTTP; legacy HTTP+SSE "being deprecated" | same | | 2026-11-27 | directly |
| claude.ai | Open feature request for elicitation support: opened 2026-04-06, state open, assigned 2026-04-27; no Anthropic statement or timeline on the page. Commenters (third-party claims, unverified) say claude.ai does not declare `elicitation` and that an `elicitation/create` produced `MCP error -32000: Anthropic proxy: MCP server connection lost`. | https://github.com/anthropics/claude-ai-mcp/issues/153 | page snapshot shows a comment dated 2026-11-24 | 2026-11-27 | summary only |
| Claude Desktop | Feature request exists | https://claudeissues.com/issue/41347-feature-mcp-elicitation-support-in-claude-desktop-app | host not reachable by WebFetch; known only from a search result title | 2026-11-27 | not fetched |
| Claude support (custom connectors) | No elicitation text found | support.claude.com articles (search results only) | availability, OAuth, public reachability; nothing on elicitation | 2026-11-27 | search summary only |
| LibreChat | MCP docs mention transports "Streamable HTTPS or SSE", idle connection closed "after 15 minutes by default", OAuth sign-in 10 minutes; no mention of elicitation, sampling or roots | https://www.librechat.ai/docs/features/mcp | | 2026-11-27 | directly (small page) |
| LibreChat | GitHub search found no elicitation issue; #13401 is about OAuth `audience`, not elicitation | https://github.com/danny-avila/LibreChat/issues/13401 | | 2026-11-27 | directly (that issue only) |
| VS Code / GitHub Copilot | Not fetched except a search hit: GitHub blog "Building smarter interactions with MCP elicitation" | https://github.blog/ai-and-ml/github-copilot/building-smarter-interactions-with-mcp-elicitation-from-clunky-tool-calls-to-seamless-user-experiences/ | | 2026-11-27 | not fetched |

---

## What this implies for a server that asks mid-call

Facts only; each tied to a row above.

1. Legacy-era elicitation is a JSON-RPC request from server to client; its only home is an SSE stream, and the spec says such messages on a POST stream "SHOULD relate to the originating client request" (Q2 rows 1, 2). A single `application/json` reply cannot carry it. The server must have returned `text/event-stream` for that POST.
2. The same spec allows a request on the GET stream, but says those messages "SHOULD be unrelated to any concurrently-running" request, and the client "MAY" open that stream (Q2, GET rows). So a server that puts a mid-call request on the GET stream relies on an optional client behaviour and on a mismatch with the SHOULD.
3. In the Python SDK 1.30.0 source as summarised: `Context.elicit` passes `related_request_id=self.request_id` (stays on the POST stream); `ctx.session.elicit_form(...)` without that argument has `related_request_id=None`, and the router then sends it to the standalone GET stream (`GET_STREAM_KEY`) (Q3, SDK rows). This matches the observed symptom (client declared elicitation, no prompt, hang) but the cause is not proven: it needs a test, and a client that never opens a GET stream would never see the request. This is a hypothesis built from a small-model reading of source, not a test result.
4. With `json_response=True` the SDK returns one JSON body and does not deliver tied server requests (Q3, SDK rows); the SDK docs recommend `stateless_http=True, json_response=True` for production. If the server runs that way, mid-call elicitation cannot work (summary only; verify in code).
5. Every version requires the server to ask only what the client declared (Q1, Q4 rows). A client that declares nothing gets no elicitation. The spec text does not say what to put in the tool result then; the server decides (Q4: not found).
6. Declaring `elicitation` is not proof the client shows a prompt in every surface. Claude Code's own docs describe cases where it cancels without a dialog (`-p`, Agent SDK, VS Code/desktop without a hook) and a cloud case where "you can't answer the request there" (Q5, Claude Code rows). The spec's own rule is that servers "MUST handle ... where the client fails to process the request" (2026, Q1).
7. Claude Code declares only `elicitation: {}` (form only) on claude.ai connectors (Q5). A server asking URL mode there would break the "MUST NOT send ... modes not supported" rule.
8. Claude's builder doc gives 240 seconds per tool call on claude.ai and Desktop (Q5). A server that waits on an unanswered request will run into that limit; the spec's general rule is that implementations SHOULD time out requests (Q1 timeouts row).
9. 2026-07-28 removes server-to-client requests, sessions, the GET stream and resumability (Q2 rows). The replacement for "ask mid-call" is: end the call with `InputRequiredResult` (`resultType: "input_required"`, `inputRequests` with `elicitation/create`, optional `requestState`), and the client retries the same `tools/call` with `inputResponses` and a new id. No server state is needed, but `requestState` must be integrity-protected (MRTR rows). It applies to `tools/call`, `prompts/get`, `resources/read`, and the server must not send it for an elicitation the client did not declare. It also means the server must not assume the retry happens.
10. A decision-confirmation need has a spec-neutral form that needs no client feature: tools annotated with hints (untrusted, "hints") and clients that SHOULD ask a human before tool calls (Q3 rows). The spec says the human-in-the-loop prompt is the client's job, not the server's.
11. A tool-result fallback exists in the spec for tool failures (`isError: true`, text the model can use) (Q3). Using it to say "choose a stage and call again with `stage=...`" is a design choice, not a spec requirement; the spec text is silent on elicitation fallbacks (Q4).

## Not found / unknown

- Per-client elicitation rows on modelcontextprotocol.io: not found (/clients is the landing page; /example-clients is 404; the extensions matrix has no elicitation column).
- Any statement in the spec on which stream an elicitation uses, in the elicitation pages themselves: not found; it exists only through the transports page rule on "related to the originating request".
- Spec text on timeouts specific to elicitation: not found.
- Spec text on how a server should degrade when the client lacks elicitation: not found.
- 2025-03-26 page, 2024-11-05 HTTP+SSE page: not fetched.
- 2026-07-28 and 2025-06-18 `ToolAnnotations` field text: not captured; 2025-11-25 field text read.
- 2026-07-28 schema page: only first 100k of 215k characters read; `MissingRequiredClientCapabilityError` text comes from that part.
- Claude Code hooks page: only first 100k of 300k characters read.
- claude.ai elicitation: no Anthropic statement found; only the open issue.
- Claude Desktop / claude.ai help-centre text on elicitation: not found (only search result summaries).
- LibreChat elicitation support: nothing found in docs or issues searched; not the same as "does not support".
- VS Code / GitHub Copilot: page not fetched.
- Python SDK 1.30.0: only the README, docs/server.md, and three source files via small-model summaries. No test run. The newer py.sdk.modelcontextprotocol.io docs may describe a later SDK than 1.30.0.
- Whether claude.ai opens a GET stream: not found in any fetched page.
