# Asking the person (RS7): what the standards say, what is practised, why our elicitation hung, and what WP29 can choose

**Status.** Desk and local parts are done (27 Nov 2026). The client trials in Claude and inference.coop have not run;
they are the ACE's, with the chief engineer's accounts. Everything about a client below is "documented, not tried"
unless it says "tried (RS5)". Notes, variant servers, wire logs and tests exist only on branch `spike/asking`; they
are cited as `spike/asking:<path>`. "Stage" is not yet a glossary word (WP29 adds it). Here "the tool" is the Python
package; "an MCP tool" is a callable the server lists. Evidence refs such as (A:E1) point to the appendices.

## Summary

- **The standard has one mechanism for a server to ask the person mid-call, elicitation**, and it is a request from
  server to client on a stream the client is reading. The 2025-06-18 and 2025-11-25 versions allow it on the POST's
  event stream (it should relate to the originating request) or on the optional standalone GET stream (it should be
  unrelated). The 2026-07-28 version removes server-to-client requests, sessions and the GET stream, and replaces
  elicitation with an "input required" result that the client answers by retrying the call (A:S1 to S4).
- **Our trial hung because of how the server sent it, demonstrated locally; whether that is also why Claude hung is
  not shown.** The SDK's `ctx.session.elicit_form(...)`, as RS5 called it, sends the request on the GET stream. A
  client that reads only the POST stream gets no prompt, and the call waits for ever. The same client, with the same
  server and the request tied to the call (`ctx.elicit(...)`), is asked and answers in 0.1 s (B:B1, B2, B3). Claude
  opening no GET stream is unproven; one log line from the next trial settles it (C).
- **Declaring the capability is not a promise to show a prompt.** Open issues report Claude Desktop, Cowork and the
  Claude Code VS Code extension declaring elicitation and never rendering or auto-declining; the server cannot tell
  that from a person's "no" (A:S6, G2). So a server that asks must bound its wait and fall back.
- **Four patterns are in use**, and only protocol elicitation and out-of-band approval put the question in front of the
  coder without the assistant between. The assistant can answer for the coder in the other patterns, and the server
  cannot tell (G2).
- **No option is chosen for WP29.** Section G4 lists seven, with the clients each works in and what still needs the
  held trials.

## G1. The standards

All claims: A:S1 to S12, with page and version. Fetched 27 Nov 2026 through a summarising reader, so each row in the notes (`spike/asking:spike/asking/notes/g1-standards.md`) says "directly" or "summary only".

**Elicitation modes and capability.** 2025-06-18 has one mode, a form of flat primitive fields; the client declares
`elicitation: {}`. 2025-11-25 adds URL mode (out of band, nothing sensitive in the form), sub-capabilities `form` and
`url`, with `{}` meaning form only, and says servers MUST NOT send a mode the client did not declare. Both versions
give three answers (accept, decline, cancel). 2025-11-25 makes the client's duties MUST (show which server asks, give
decline and cancel). Servers MUST NOT ask for sensitive information in a form (2025-11-25 names passwords and tokens and sends those to URL mode). No page states an elicitation timeout; the
general rule is that implementations SHOULD time out requests. No page says what a server should return when the
client lacks the capability: the server decides (S1 to S5, S12).

**Where the request travels.** The server MAY send requests before the final response on the POST's event stream, and
they SHOULD relate to the originating request. The POST must then answer `text/event-stream`, not one JSON body (an
inference from the two allowed types). The client MAY open a GET stream; messages there SHOULD be unrelated to any
running request; a message goes on one stream only. The client answers a server request with a new POST, and the
server returns 202 (S6 to S8). Sessions are optional (S9); a stateless server is not discussed by name.

**2026-07-28.** No `initialize`, no session id, no GET stream, no resumability; "closing the SSE response stream"
cancels the call. Elicitation travels as an `InputRequiredResult` (`input_required`, with `inputRequests` and an
optional `requestState`); the client retries the call with `inputResponses` and a new id. The server MUST NOT assume
the client will answer or retry, and MUST treat `requestState` as attacker-controlled (S4). The client declares elicitation
per request. Sampling is deprecated there (S2 to S4, S10).

**Related mechanisms.** Tools: "there SHOULD always be a human in the loop with the ability to deny tool invocations",
and clients SHOULD prompt on sensitive operations. Annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`,
`openWorldHint`) are hints; clients MUST treat them as untrusted unless the server is trusted; the 2025-11-25 defaults
are `destructiveHint` true and `readOnlyHint` false. Sampling asks the client's model, not the coder.  Results with `isError` carry tool failures to the assistant (S10, S11).

**The Python SDK 1.30.0** (read through summaries and then tested): `Context.elicit` ties the request to the call;
`ServerSession.elicit_form` ties it only if `related_request_id` is passed; its documentation recommends
`stateless_http=True` and `json_response=True` for production, which break mid-call elicitation (B:B4, B5).

## G2. The practice

Sources: A:P1 to P20. Every row names a product or document (R2).

| Pattern | Who sees it | Who answers | Recorded | Can the server tell the coder's word? | Used by |
|---|---|---|---|---|---|
| 1. The assistant asks in its reply | The coder, as chat text | The coder types; the assistant writes the next call, so it can answer for the coder | The transcript | No. A `confirm: true` flag was filled by the model itself | A shop-inventory MCP write-up (A:P1) |
| 2. Client approval of a call | The coder, in the client's dialog: tool and arguments | The coder, or a rule ("Always allow", auto modes, hooks) | Client settings and transcript; the server sees an ordinary call | No | Claude Code permissions; Claude.ai connector permissions; VS Code; Cursor; OpenAI `mcp_approval_request` |
| 3. Confirm then write (preview, then apply) | The coder, only if the assistant relays it, or on a page the server owns | Whoever holds the token | Server state | Only if approval happens out of the assistant's reach (Stripe's Dashboard approval, a human running `terraform apply` on a saved plan) | Stripe MCP; Terraform `plan -out`; filesystem MCP `dryRun` (advice only); iCloud Mail MCP's `confirmToken` fallback (A:P2) |
| 4. Protocol elicitation | The coder, in a dialog naming the server | The coder (accept, decline, cancel); some clients auto-answer by hook | Client side; the server gets `{action, content}` | Strongest signal, but a client that never shows the form looks like a decline | Claude Code terminal; VS Code Copilot; Cursor; Open WebUI; MCP spec |

Also in use: Claude Code's `AskUserQuestion` and plan mode, MCP prompts as slash commands the coder starts (Claude Code yes; Copilot sessions no),  a confirm-by-retry call (a merged Todoist change) and a custom confirmation envelope the client intercepts (an unmerged LibreChat change), both kin to, not instances of, the 2026-07-28 input-required result, and out-of-band URL approval.

**Documented, not tried.** Claude Code shows elicitation dialogs in the terminal, and declares only `elicitation: {}` to
claude.ai connectors; it cancels without a dialog in print and Agent SDK runs and in the VS Code and desktop apps unless
a hook accepts. For claude.ai and Desktop, Anthropic's builder page lists sampling and resource subscriptions as
unsupported, lists "advanced or draft capabilities" as unsupported without naming elicitation, and gives a 240-second limit per tool call; an open request for elicitation
(`claude-ai-mcp#153`) has no Anthropic reply, and open issues report capability declared and form never shown (A:P8 to
P12). Tool permissions (Always allow, Needs approval, Blocked) are documented for connectors. LibreChat's docs list
tools only; elicitation requests are open (`#11526`, `#13267`), and an unmerged change adds a confirmation envelope.
VS Code Copilot documents form and URL elicitation, cancelled in Autopilot. Open WebUI documents elicitation (A:P13 to P18).

## G3. What went wrong in our trial

RS5's `ask_stage` checked the capability, then awaited `ctx.session.elicit_form(...)`. In Claude, by the ACE's trial note (kept outside the repository, as RS5's evidence is), the server logged the send at 14:41:18 and the call hung 4 minutes with no prompt; the repository's RS5 readout records only "hangs". In inference.coop the client declared nothing and
the tool returned `elicited: false`: that part is not a fault, it is what the check is for.

**Demonstrated (SDK 1.30.0, 127.0.0.1, B:B1 to B3).** `elicit_form` without a related request id is routed to the GET
stream. A client that opens no GET stream (a raw client; an SDK client whose GET got 405) gets nothing: the SDK logs
`Request stream _GET_stream not found` and drops the message, and the call waits. With `related_request_id` or
`ctx.elicit`, the first event on the POST's response stream is `elicitation/create`, the client answers by POST (202)
and the call finishes in 0.1 s. The PM reran B1 and B2 and got the same table.

**Also demonstrated.** `json_response=True` discards a related request, so even a client with a GET stream hangs (B5). Stateless HTTP fails the capability check, and with the check removed the answer is lost (B4). URL mode works on the POST route (B6). A server-side bound with a fallback frees the call in 3.1 s (B9). The SDK's check passes `{url: {}}` too, so it cannot tell form from URL (B8).

**Not demonstrated: that Claude opens no GET stream.** If it does, B1 reached it and the cause is something else (the
client not rendering a form, or the public route buffering a long GET). The 4-minute figure is consistent with Claude's documented 240-second tool limit (A:P8); it does not show it. A third-party server's change (`infranodus#29`) says claude.ai connectors open no GET stream and its call timed out at 60 s: unreproduced support for the cause, and a different duration. What would settle it is in the first minute of the next trial's
request log: does `GET /mcp` arrive after initialize, what did `initialize` declare, and does a `ctx.elicit` call show
a prompt where `elicit_form` did not (C). So the stated cause is: **the server's request used the stream the standard
reserves for unrelated messages, which a client may never open; shown to hang a POST-only client; unconfirmed for Claude.**

## G4. Options for WP29

No choice is made. "Tried" means RS5's trials; "local" means B:rows here; "held" needs the client trials in C.

| Option | How the coder is asked | Claude | inference.coop | Evidence | Cost | Held trial? |
|---|---|---|---|---|---|---|
| O1. The result tells the assistant to ask in chat | A refusal or clarification result names the stages; the coder answers in chat; the assistant calls `set_stage` with the coder's word | Works (tried RS5 T3, T4: text relayed, move left to the coder) | Works (same) | RS5 trials; G2 pattern 1 | The assistant can answer for the coder; the server cannot tell. No code beyond text | No |
| O2. Elicitation sent correctly, with fallback to O1 | `ctx.elicit`, stateful and SSE, wait bounded, fallback result | Unknown: may show a prompt if Claude renders forms and reads the POST stream | Absent today (client declares nothing, tried RS5); fallback to O1 | Local B2, B3, B9; spec S6 to S8 | Server must be stateful and SSE, against the SDK's production advice; a timeout; two paths to test; 2026 spec replaces it | Yes: whether Claude shows it |
| O3. Confirm then write | Preview returns a token; apply needs the token | Not tried; shape works locally (B10) | Not tried; shape works locally (B10) | Local B10; Stripe, Terraform | Two calls per write. The token is held by the assistant, so it adds no proof of the coder's word | Yes: that the assistant relays the preview |
| O4. Out-of-band approval | The coder approves where the assistant cannot (a link, or a change in the vault the coder makes) | Not tried | Not tried | Stripe's flow; URL mode B6 (local, SDK only); the coder already edits Markdown in Obsidian | The most to build; the only form where the coder's word is distinguishable (G2). How the vault holds it is WP29's design | Yes |
| O5. Client approval plus annotations | Mark the writing MCP tool `destructiveHint`; the client asks before each call | Documented: connectors can be Always allow or Needs approval; annotations declared | No general tool-approval setting in the LibreChat docs | Spec S10; Claude connector docs; local B11 | The server cannot see who approved; "Always allow" removes it | Yes: whether Claude prompts |
| O6. The coder starts the move | An MCP prompt the coder invokes as a command, carrying the stage | Documented for Claude Code only | Not found | Claude Code docs (A:P6) | Needs a client that shows prompts to the coder | Yes |
| O7. Input-required result (2026-07-28) | The call ends with an input request; the client retries | Not today (an open Cowork issue reports it dropped) | Not today (no client documented) | Spec S2 to S4; G2 | Needs both clients to speak 2026-07-28; none documented | Not yet testable |

O1 is the only option already tried and working in both clients. Whether it is enough depends on whether the coder's word must be provable, which C17 deferred.

## Appendix A. Sources

**Standards (fetched 27 Nov 2026; base `https://modelcontextprotocol.io/specification/<version>/`).**
S1 `client/elicitation`, 2025-06-18: one form mode; `elicitation` declared. S2 same page, 2025-11-25: form and URL, `{}`
is form only, MUST NOT send undeclared modes, MUST duties, sensitive-data rule. S3 same page, 2026-07-28: `InputRequiredResult`,
per-request capability, "Servers SHOULD NOT assume" success. S4 `basic/patterns/mrtr`, 2026-07-28: MRTR rules, `requestState`.
S5 `changelog`, 2026-07-28: removal of sessions, `initialize`, GET stream, `elicitationId`, resumability. S6 `basic/transports`,
2025-06-18: POST stream and "SHOULD relate", GET stream "SHOULD be unrelated", client MAY open it. S7 same, 2025-11-25:
same rules plus polling and `retry`. S8 `basic/transports/streamable-http`, 2026-07-28: no independent requests on any
stream; stream closure is cancellation. S9 session text, S6 and S7. S10 `server/tools`, 2025-06-18, 2025-11-25, 2026-07-28:
human in the loop, annotations untrusted; `schema` 2025-11-25 for annotation defaults. S11 `client/sampling`, all three;
deprecated 2026-07-28. S12 `basic/lifecycle`, 2025-06-18: timeouts SHOULD. Python SDK: `python-sdk` tag v1.30.0
(`server/fastmcp/server.py`, `server/session.py`, `server/streamable_http.py`), read through summaries and then tested.
Unread or partial: the 2026 schema page (first 100k of 215k characters), 2025-03-26, the modelcontextprotocol.io clients
matrix (not found), the 2026 and 2025-06-18 annotation field text. Full table: `spike/asking:spike/asking/notes/g1-standards.md`.

**Practice (fetched 27 Nov 2026, GitHub state read by API).** P1 `https://dev.to/sunnatulla_dev/my-mcp-servers-confirm-true-flag-was-written-by-the-model-so-i-moved-the-approval-to-the-user-5dnh`. P2 `leolesimple/icloud-mail-mcp#75`, "fix(confirm): bound elicitation with timeout and client cancellation" (merged). P3 `https://docs.stripe.com/mcp`. P4 Terraform `plan`.
P5 `modelcontextprotocol/servers` filesystem README (`dryRun`). P6 `https://code.claude.com/docs/en/permissions`, `mcp`,
`hooks` (first 100k of about 300k characters), `permission-modes`. P7 `https://claude.com/docs/connectors/custom/add-unlisted.md`
and `https://support.claude.com/en/articles/11176164`. P8 `claude.com/docs/connectors/building` (unsupported features,
240 s). P9 `anthropics/claude-ai-mcp` #153, #1046, #1085, #1356. P10 `anthropics/claude-code` #105334, #88901, #96043
(Desktop), #98256, #112463, #111077 (Code). P11 `infranodus/mcp-server-infranodus#29`. P12 `todoist/mcp-core#20`.
P13 `https://www.librechat.ai/docs/features/mcp`. P14 LibreChat #11526, #13267, #17666, PR #13304. P15
`https://code.visualstudio.com/api/extension-guides/ai/mcp` and `docs/agents/run/approvals`. P16 `https://cursor.com/docs/context/mcp`.
P17 `https://docs.openwebui.com/features/extensibility/mcp`, PR #27158, #34153. P18 `https://developers.openai.com`
MCP guide (`mcp_approval_request`). P19 `https://code.claude.com/docs/en/agent-sdk/user-input` (`AskUserQuestion`).
P20 `gofastmcp.com` elicitation. Not found: any Anthropic statement on claude.ai elicitation; a LibreChat elicitation
statement beyond open requests; Goose docs (404). Full table: `spike/asking:spike/asking/notes/g2-practice.md`.

## Appendix B. Local variant results (G3)

Server `spike/asking:spike/asking/asking_server.py`, one MCP tool per variant; clients: A1 SDK answers; A2 SDK callback
never answers; A3 SDK declares nothing; A4 raw POST-only, answers; A4s SDK with GET refused (405), answers; A4q raw
POST-only, never answers. SDK `mcp` 1.30.0, 127.0.0.1 only. Rerun: `run_variants.py` (about 90 s) and `pytest`
(13 passed in 24 s; with the trial runner, 16 passed). Raw wire logs: `spike/asking:spike/asking/logs/`.

| Variant | Client | Saw | Stream used | Outcome |
|---|---|---|---|---|
| B1 `elicit_form`, no related id (RS5's call) | A1 | prompt; accept | GET | returned |
| B1 | A4, A4s | nothing | none: routed to GET, none open, dropped | **hung** |
| B1 | A3 | no prompt, "not declared" | none | returned |
| B2 `elicit_form(related_request_id=...)` | A1, A4, A4s | prompt; accept | POST | returned, 0.1 s |
| B3 `ctx.elicit` | A1, A4, A4s | prompt; accept | POST | returned, 0.1 s |
| B2, B3 | A2, A4q | prompt, no answer | POST | hung (the client never answered) |
| B4 stateless, check kept | A1, A4 | "not declared" | none | returned |
| B4 stateless, check removed, B2/B3 | A1, A4 | prompt; answer POSTed (202) | POST | **hung**, answer lost |
| B5 `json_response`, B1 | A1 / A4 | prompt / nothing | GET / dropped | returned / hung |
| B5 `json_response`, B2/B3 | A1, A4 | nothing | discarded by the SDK | **hung** |
| B6 URL mode (`ctx.elicit_url`) | A1, A4 | prompt; accept | POST | returned |
| B7 after a log and a progress notice | A1, A4 | as B1 or B3 by route | GET / POST | as B1 / B3 |
| B8 capability variants | R | `{}` and `{form:{}}` count as form; `{url:{}}` passes the SDK's check | n/a | returned |
| B9 bounded wait with fallback, POST route | A4q | prompt; fallback result | POST | returned, 3.1 s |
| B10 preview and apply; instruct result | A3 | token; apply once; replay refused | none | returned |
| B11 annotations in `tools/list` | A3, A4 | `destructiveHint` on apply; hints on preview | none | returned |

Flagged: A2 hangs even in B9, an SDK-client artefact (it awaits the callback in its receive loop). The "stream used"
column is from the server's wire log and the SDK's debug lines, not a client capture. B4's mechanism is read from code
and logs, not traced inside the SDK. Not tried: event-store replay to a late GET; a proxy in between.

## Appendix C. Client-trial plan (for the ACE; human-paced)

Run later with the chief engineer's accounts, the ACE as coder, RS5's setup (key gate, short-lived public route, torn
down afterwards). The runner `spike/asking:spike/asking/serve_trial.py` serves the variant tools on 127.0.0.1 and writes
a request log (initialize capabilities, whether `GET /mcp` arrives, each stream's events, each answer POST); start it with `uv run --project <RS5 checkout> --frozen --extra mcp python serve_trial.py --port 8765 --log <file> [--key K]` from `spike/asking/`; the public route and its teardown are RS5's procedure, and nothing here starts one. Record for each step what the person saw and
what the log shows (R6). One prompt per message, wait for the answer, no parallel use. **Budget: Claude 16 messages;
inference.coop 12 messages** (gentle load, small co-op).

| Step | Say to the assistant | Look for in the client | Look for in the log |
|---|---|---|---|
| 0 | Connect; list the tools | Which tools appear | The `initialize` capabilities (was `elicitation` declared, with which sub-keys); did `GET /mcp` arrive |
| 1 (O1) | "Call `b10_instruct`" | The assistant asks you in chat; you answer | Result text delivered |
| 2 (O2) | "Call `b3_ctx` and tell me exactly what you see" | A prompt or nothing; a 240 s hang | `elicitation/create` on the POST stream; your answer POSTed |
| 3 | "Call `b1_session`" (RS5's call) | Same as before: hang | A request under a `GET` line used the GET stream; no `elicitation/create` line anywhere means it was dropped; compare with step 2 |
| 4 | "Call `b2_related`" | As step 2 | Same |
| 5 (O2 fallback) | "Call `b9_timeout_ctx`" | Prompt, or the fallback text after 3 s without an answer | Request and fallback |
| 6 (O2, URL) | "Call `b6_url`" | A link prompt or nothing | Capability `url` declared? |
| 7 (O3) | "Call `b10_preview`, show me the result, then wait for me" | Does the assistant show the preview and wait; does it call `b10_apply` on its own | Apply call arrives only after your word? |
| 8 (O5) | "Call `b10_apply` with the token" | Does the client ask before the call; are tool settings offered | Call arrives after your approval |
| 9 (O6) | Look for the server's prompts in the client's menus | Whether the coder can start one | `prompts/get` arrives |

If step 2 shows a prompt and step 3 hangs, the cause is confirmed for that client. If both hang and the log shows a
`GET /mcp` after initialize, the cause is not the stream; note whether the declared `elicitation` was form, url or empty.
In inference.coop, steps 2 to 6 need only one try each (the capability is expected absent, tried RS5): check `initialize`.
Stop if any step shows a leak of keys or the page shows another person's data; tear the route down afterwards.

## Appendix D. Not known

Whether Claude opens a GET stream (C, step 0). What `initialize` declares from claude.ai and inference.coop now. Whether
Claude shows a form on the POST stream.  2026-07-28 behaviour in any client. The Python SDK's
behaviour after 1.30.0. Sources read only in part are listed in A.
