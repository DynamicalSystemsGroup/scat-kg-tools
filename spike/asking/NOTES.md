# RS7-U3: why an elicitation hung in claude.ai (local reproduction only)

Everything here ran on 127.0.0.1 with the `mcp` SDK 1.30.0 (printed by `run_variants.py`). No chat service was contacted.
The SDK clients and the raw client below are **not claude.ai**. Whether claude.ai opens the GET stream is **not known**.

## Findings

1. **Demonstrated (local):** the RS5 baseline (`ctx.session.elicit_form(...)`, no `related_request_id`) sends the
   server request to the *standalone GET stream*. A client that never opens a GET stream (A4 raw, A4s SDK with GET
   refused) receives no prompt and the call hangs. The SDK server does not fail: it logs
   `Request stream _GET_stream not found for message` at DEBUG and drops the message.
2. **Demonstrated (local):** `ctx.session.elicit_form(..., related_request_id=ctx.request_id)` (B2) and
   `ctx.elicit(...)` (B3) put the request on the *POST response stream* of the `tools/call`. The same POST-only
   clients see the prompt, answer by POSTing a JSON-RPC response (HTTP 202), and the call returns in ~0.1 s.
3. A client that opens the GET stream (A1, the SDK default) gets B1 on the GET stream and B2/B3 on the POST stream;
   all work. So B1 is not broken everywhere: it works only for clients that read the GET stream.
4. `json_response=True` (B5): a related request (B2/B3) is **discarded** by the SDK (`received: elicitation/create`
   debug line, nothing on the wire), so even the SDK client that holds a GET stream hangs. B1 still works for a
   client that holds a GET stream, because it is not related to the POST.
5. Stateless HTTP (B4): the capability check always fails (no initialize state), so the tool answers
   "did not declare elicitation". With the check bypassed, B2/B3 reach the client on the POST stream, but the
   client's answer POST lands on a fresh per-request transport (202, then nothing): the call hangs. B1 is dropped.
6. A client that declares elicitation but never answers (A2, A4q) hangs the call for as long as the server waits.
   A server-side `anyio.fail_after` plus a fallback result (B9) frees the call for both routes (B9 rows).
7. Capability check (B8): the SDK client declares `{form:{}, url:{}}` only when given a callback, else nothing.
   `check_client_capability(ClientCapabilities(elicitation=ElicitationCapability()))` is true for any declared
   `elicitation` value, including `{url:{}}` (sub-capabilities are not compared). By the spec an empty `{}` means
   form mode, so a form-only test needs `form_by_spec` (see `b8_caps`).
8. Without a capability check (`b8_nocheck`), the SDK client with no callback answers with JSON-RPC error
   -32600 "Elicitation not supported"; `ctx.elicit` raises `McpError`, which the tool can catch.
9. B6 URL mode exists in 1.30.0 (`ctx.elicit_url`); it behaves like B3 for routing (POST stream, works for POST-only).
10. B7: a log and a progress notification before the request change nothing; routing depends only on
    `related_request_id`.
11. B10 two-step (preview returns a token, apply needs it; replay refused) and the instruct-the-assistant result
    both need no client support. B11: `tools/list` carries `readOnlyHint`/`destructiveHint`/`idempotentHint` as set.

Spec (2025-06-18 and 2025-11-25 transports pages): on a POST's SSE stream, the server "MAY send JSON-RPC requests and
notifications before sending the JSON-RPC response. These messages SHOULD relate to the originating client request."
On the GET stream: "SHOULD be unrelated to any concurrently-running JSON-RPC request". The client "MAY issue an HTTP
GET", so a client is allowed never to open it. B1 uses the route the spec reserves for unrelated messages.

## Table (condensed; every row, with wall time, is in `logs/table.txt`; raw wire logs in `logs/*.txt`)

Clients: A1 SDK, answers; A2 SDK, callback never answers (see unknowns); A3 SDK, no callback; A4 raw httpx, POST
only, answers; A4s SDK with GET answered 405 by a transport wrapper, answers; A4q raw, POST only, never answers.

| variant | client | what the client saw | stream the request used | outcome |
|---|---|---|---|---|
| B1 session, no related id | A1 | prompt, accept | GET | returned 0.1 s |
| B1 | A2 | prompt, never answered | GET | hung (cut at 3 s) |
| B1 | A3 | no prompt, "not declared" | none (not asked) | returned |
| B1 | A4, A4s | no prompt | none: routed to GET, none open, dropped | **hung** |
| B2 related id | A1, A4, A4s | prompt, accept | POST | returned 0.1 s |
| B2 | A4q, A2 | prompt, no answer | POST | hung (client never answered) |
| B3 ctx.elicit | A1, A4, A4s | prompt, accept | POST | returned 0.1 s |
| B3 | A4q, A2 | prompt, no answer | POST | hung |
| B2/B3/B1 | A3 | no prompt, "not declared" | none | returned |
| B4 stateless, check on | A1, A4 | no prompt, "not declared" | none | returned |
| B4 stateless, check off, B1 | A1, A4 | no prompt | none: dropped | hung |
| B4 stateless, check off, B2/B3 | A1, A4 | prompt, answer POSTed | POST | **hung** (answer lost) |
| B5 json, B1 | A1 / A4 | prompt, accept / none | GET / none: dropped | returned / hung |
| B5 json, B2/B3 | A1, A4 | no prompt | none: discarded by SDK | hung |
| B6 url | A1, A4 | prompt, accept | POST | returned |
| B7 after log+progress, ctx | A1, A4 | prompt, accept | POST | returned |
| B7 after log+progress, session | A1 / A4 | prompt / none | GET / dropped | returned / hung |
| B8 caps | see `b8_caps` rows | declared value and check results | n/a | returned |
| B8 nocheck | A3 / A1 / A4 | McpError -32600 / prompt / prompt | POST | returned |
| B9 timeout, session (wait 3 s) | A1 / A4q | prompt, accept / no prompt, fallback | GET / dropped | returned 0.1 s / 3.1 s |
| B9 timeout, ctx (wait 3 s) | A1 / A4q | prompt, accept / prompt, fallback | POST | returned 0.1 s / 3.1 s |
| B10 two-step, instruct | A3 | token, apply once, replay refused | none | returned |
| B11 annotations | A3, A4 | 13 tools; hints on `b10_*` | none | returned |

## Cause of the hang

- **Demonstrated, locally:** with an SDK server, `ctx.session.elicit_form` without `related_request_id` is routed to
  the GET stream; if the client holds no GET stream the request is dropped and the call waits forever. Evidence: wire
  logs `logs/b1-b1-session-a4-raw-postonly-stateful-sse.txt` (POST `tools/call` answered with an open SSE response that
  never carries `elicitation/create`; no GET exchange at all; SDK line `Request stream _GET_stream not found`), against
  `logs/b2-b2-related-a4-raw-postonly-stateful-sse.txt` (same client, `elicitation/create` is the first SSE event on the
  POST response, the answer POST gets 202, then the result). This reproduces the symptom seen in claude.ai ("server
  logged that it sent the request, no prompt, call hangs"): the server's log line is its intent, not a delivery.
- **Not demonstrated for claude.ai:** that claude.ai opens no GET stream. If it does open one, B1 would have been
  delivered there and the cause is something else (client does not render form elicitation, a proxy buffering the
  long-lived GET, or the prompt shown elsewhere). The local result shows the baseline *can* hang for a POST-only
  client; it does not show claude.ai is one.

## What a server must do (supported by the rows above)

- Send the request on the POST stream: `ctx.elicit(...)` or `related_request_id=ctx.request_id` (spec-aligned too).
- Stateful and SSE: not `stateless_http`, not `json_response` (both break the related request locally).
- Always bound the wait (`anyio.fail_after`) and return a fallback that tells the assistant to ask the coder in chat
  (B9), because a client may declare the capability and never show or answer the prompt.
- Do not rely on the SDK capability check for form vs url (B8).
- For writes that must not run unconfirmed, B10 works with any client.

## Unknowns

- Whether claude.ai opens `GET /mcp` after initialize. **Evidence that would settle it:** the key-gated route's request
  log (chief engineer's trial): did a `GET /mcp` with `Accept: text/event-stream` and the session id arrive? Then run
  `b3_ctx` (POST route) from claude.ai: a prompt shown there, with B1 still hanging, would confirm the cause for it.
- What claude.ai declares in `capabilities.elicitation` (empty, `form`, or `url`): log the initialize body.
- A2's hang in B9 is an SDK client artefact: the SDK awaits the callback inside its receive loop, so a callback that
  never returns also blocks the client from reading the server's fallback result. B9 therefore uses the raw client A4q.
- B4's mechanism (answer POST goes to a fresh per-request transport) is read from the SDK code and the wire log
  (202, then silence), not traced inside the SDK.
- Not tried: resumability (event store) replaying a dropped GET message to a late GET; an HTTP proxy in between.

## Rerun

SDK version: `mcp 1.30.0`. From this folder (`spike/asking`), with `RS5` set to the RS5 checkout (its environment is used read-only) (about 90 s; each hung case
is cut at 3 s, B9 at 6 s):

```
uv run --project $RS5 --frozen --extra mcp python run_variants.py
uv run --project $RS5 --frozen --extra mcp python run_variants.py --only B1,B4
uv run --project $RS5 --frozen --extra mcp python -m pytest -q test_asking.py
uv run --project $RS5 --frozen --extra mcp ruff check . && uv run --project $RS5 --frozen --extra mcp ruff format --check .
```

Files: `asking_server.py` (one tool per variant), `harness.py` (live server on 127.0.0.1, wire log, clients),
`run_variants.py` (table and logs), `test_asking.py`.
