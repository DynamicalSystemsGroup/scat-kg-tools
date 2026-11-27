# Lifecycle readout (RS5): the stage machine, what the evidence says and what WP29 must decide

**Status.** Desk and server experiments are done (27 Nov 2026). The client trials ran the same day in Claude and
inference.coop's chat, with the ACE as coder (D-176); VS Code's Copilot was passed by the chief engineer (D-180). Their
results are in "Client trials" below; the evidence (notes, request log, screenshots) is kept outside the repository.
Statements about Copilot remain "documented, not tried". The spike notes and code exist only
on that branch; they are cited as `spike/lifecycle:<path>`, and every finding the readout needs is repeated in the
appendices. "Stage" and "transition" are not yet glossary words (WP29 adds them); here "stage" means a state of the
lifecycle. Evidence refs such as (B:E7) point to the appendices.

## Summary

No option is chosen for WP29. What the evidence says:

- **A flat machine is enough for one machine** (G1): stages, named moves, named predicates, one current stage, a
  reserved `unknown`. Per-narrative sub-machines are an alternative, not something G1 needs (Q1).
- **The sources carry five groupings** of the lifecycle plus a "finished model" condition (G2, App. G); they nest and
  disagree on the unit (vault, narrative, page). No stage is stored today.
- **Header, query and path are fixed per connection** in the SDK client (B:E1). Per-request carriers that work are an
  argument (any client, at a byte cost) and `_meta` (SDK only). No documented way exists from a user-added connector in
  claude.ai, VS Code or the co-op's form to send a changing header; admin-edited LibreChat YAML can; nothing tried (D:b3).
- **A per-session tool-list change works in the SDK, with overrides**, and a refusal makes it optional (B:E6, E7). Of
  the three trial clients, one documents re-listing (LibreChat), one is source-read (VS Code), one unknown (claude.ai); the trials found LibreChat re-lists and claude.ai does not
  (D:a1). The latest spec limits it (G4).
- **A router does not remove the list change**; only its static facade does, at a price (B:Q2, Q3).
- **Most predicates are evaluable or the coder's word**; no tool reads `scat.toml` (G5).

**Closed by evidence:** session value or `list_changed` on a stateless server; "a router avoids the list change" (except
the facade); elicitation as the only clarification path. **Stay open:** the unit, granularity, relying on `list_changed`,
single server versus router, the spec era, triggers and predicates, whether any chat client can send a stage header,
and all client behaviour.

## G1. Smallest sufficient form (literature)

Sources: A:S1 to S21 (F3 lists the weak ones); note `spike/lifecycle:research/lifecycle/notes/g1-literature.md`.

- Loops are the norm and the stop is a person's judgement (S1 to S9): "enough" is a *request* predicate; a backward move
  is ordinary.
- Workflow engines give explicit moves, a separate move for going back, guards, a default when none fires, and a
  person or program as trigger (S10 to S13, S15, S16). Predicates stay pure; soundness is a reachability check (S14).
- Harness-side tool restriction lasts one turn (S19), so stage must live in server data or in the request (S18).

**The form:** a list of stages (plus `unknown`), each with expected inputs, outputs, tools, prompt and skill sections as
plain lists; a list of moves (from, to, direction, name, predicates); predicates in two modes, `detect` (tool evaluates,
read-only) and `request` (returns a question to the coder); one current stage; a clarification result in `unknown` or
for a disallowed call. Hierarchy, concurrency, history, timers and guards with side effects were each judged not needed.
"Flat" describes one such machine; per-narrative copies of it (concurrency) are needed only if stages differ per
narrative at once.

**Not known:** the right stage count; the unit of stage; formal literature on tool restriction as an enabling constraint
(one search found none); whether this helps weaker models (F12).

## G2. Raw material (no choice)

Note: `spike/lifecycle:research/lifecycle/notes/g2-raw-material.md`; condensed in Appendix G. The server has 19 tools,
6 prompts, 1 resource.

- **Groupings** (G:1): the flow's ten steps; the coder's loop (interpret, author, code, review); the page status cycle;
  a SCAT Chat session; assistant modes; "finished model" as a condition. Alternatives: ten stages with the loop and status
  as per-narrative sub-machines; a flat machine on the loop; ten with Code and Analyse split by assistant mode; status only.
- **Tools by stage** (G:2): `check` fits six stage columns; most tools cluster in Code and Analyse; stages 1, 3, 4, 7 have
  no tool. **Transitions** (G:3): twenty, forward, backward (done to draft, refused by the server; Analyse to Code; Code
  to Plan when the group cap refuses) and lateral. **Conflicts and gaps** (G:4): ten, headed by "no stage is stored"
  and "three units use the word".

**Not known:** which unit carries the stage; whether the inferred moves back to Capture exist (no source).

## G3. How stage reaches the server (RS5-R2)

Tried in a throwaway FastMCP server on 127.0.0.1 with the SDK's own client; SDK `mcp` **1.30.0**; 44 spike tests pass
(re-run for this readout). Note: `spike/lifecycle:spike/lifecycle/single/NOTES.md`. Classes are about the SDK; chat-client
support is not tried for any row.

| Carrier | Class | Condition |
|---|---|---|
| Header, per connection | works | Constant for the connection |
| Header, per request | partly works | Only an httpx event hook on the client; no chat client offers one |
| Query `?stage=` | works | Constant per connection; needs only a connector URL |
| Path `/mcp/<stage>` | works | 6-line ASGI rewrite; one connector per stage |
| Session value (`set_stage` tool) | works stateful; does not work stateless | Lost on restart ("Session terminated") |
| Argument on each call | works, with a cost | tools/list 2518 to 3400 bytes (+882) for 9 tools; about 1.9 KB for 19 |
| `_meta` on each request | works (SDK) | Chat clients are not expected to expose it; not verified |
| None: stable list plus refusals | works | The call reaches the handler whether or not the list is current |

**Key fact:** the SDK client takes headers once; `call_tool` has no headers parameter, so header, query and path mean one
stage per connection. Documentation: claude.ai sends up to four fixed approved header names, VS Code static headers, the co-op's
form one API-key header; only an administrator's LibreChat YAML sends a header per chat request (D:b1, b3). Whatever the carrier, the server cannot tell the coder's word from the assistant's claim of it
(B:E2).

**Clarification.** An unknown or missing stage returns a normal result (the stages, who decides, how to move), no
protocol error (B:E5, Q4). Elicitation works only if the client declares it; the SDK test did. Documented in VS Code Copilot sessions; unknown for
claude.ai; none seen in LibreChat's code read (D:c1). **Out of stage.** A call outside
the stage returns a result naming the tool, the stage, where it is available and how to move (B:E6). `isError` true or
false differ only in that flag; in the trials Claude marked it "Failed" and inference.coop did not pass the flag on (T4).

**Not known:** whether any chat connector can set a custom header; how reliably an assistant carries an argument.

## G4. Scoping what the server exposes (RS5-R3b; R3 in Client trials)

**Per-session `list_changed` (SDK).** Works with three code details: replace FastMCP's list handlers and `call_tool`
via the low-level server (private `_mcp_server`), patch the initialisation options so `listChanged` is advertised
(default FastMCP says false and lists 12 tools to everyone), and keep the server stateful. A move notifies its own
session only; two sessions saw different lists; stateless mode delivered 0 notices (B:E7). Prompts and resources: lists
scoped, gets not gated.

**Client support, documented, not tried** (D:a1). Of the three trial clients: LibreChat documents re-listing (upstream
`main`, not the co-op's build); VS Code Copilot re-lists in source read, with a stale-picker issue seen only in a search
listing; claude.ai documents nothing, and a user issue says the apps keep the first list (closed, not planned). Claude
Code documents it but is a reference only.

**The spec.** The 2026-07-28 revision's tools page says a tool list MUST NOT vary per connection or as a side effect of
other requests (it MAY vary by the authorization on each request), sends `list_changed` only to clients holding a
`subscriptions/listen` stream, has no protocol-level session, and recommends explicit handles passed by the model.
Sourcing: read by U5's summarising fetch and by a reviewer's fetch (relayed by the PM, 27 Nov 2026); this writer
re-fetched neither. Single-sourced (U5): the transports page, that `initialize`, `Mcp-Session-Id` and the standalone
stream are removed. So `list_changed` is still allowed, but only over a subscription, and a server-held
stage that moves the list is legal in 2025-11-25 and against 2026-07-28. Python `mcp` 1.30.0 implements only up to
2025-11-25. A stage the client names in each request (an argument or a handle in a result) is legal in both (F2).

**Router (the chief engineer's option) versus single server.** The router proxies tools, prompts, resources, results and
progress unchanged over three transports (B:Q1, Q6); stage servers stay plain and separately testable. The single
column is reasoned; B:E7 tests the single server, not as a head-to-head:

| | Router over per-stage servers | Single stage-scoped server |
|---|---|---|
| List change | Not removed (variant A); only the static facade B avoids it: 4 fixed tools, 1070 bytes, untyped `call` | Same choices; refusal as the net |
| Hosting | One app: about 100 MB, 1 port; four processes: about 351 MB, 4 ports; entrypoint changes | As today: one process, one port, one key gate |
| Code | Router 362 lines plus 23 to 27 hosting | About 45 lines scoping plus about 20 for the clarification |
| Latency | +1.3 ms memory, +5 ms HTTP | None |
| Failure | Dead stage stalls 5.01 s; shared loop stalls others about 1.2 s; mounts bypass the machine | Tool error is a result; a crash ends all |

The chat sees one server either way (B:Q5). Listing sizes: 1070 (B), 1819 to 2707 (A), 4962 (C: 14 tools, all listed,
refuse out of stage). Facade B's costs for a model are not tried.

**Not known:** Copilot's behaviour (not tried, D-180; Claude and inference.coop in Client trials); router cost under many connections (F5).

## G5. Predicates

Note: `spike/lifecycle:research/lifecycle/notes/g5-predicates.md`. Of 17 predicates classified (13 run on a copy of the
contract examples; 14 to 17 not run) (E): 7 are fully evaluable by the tools (folder exists, `scat.toml` cap and mode
present, a narrative's status, narrative coded, check passes, views run clean); 1 only on the CLI (would-`done`); 5
partly (set up, cap met, all done, views generated, done changed); 4 are the coder's word (terms, field notes, model
finished, committed). **Gaps:** no tool reads `scat.toml`, so "cap met" shows only as a refused write; no stored or
derived stage; check covers structure, not interpretation. **Not known:** git-side predicates.

## Client trials (27 Nov 2026; RS5-R3, client parts of G4 and R3b)

Plan: `spike/lifecycle:spike/lifecycle/TRIAL-PLAN.md`, all ten tests, the ACE as coder, the chief engineer's accounts,
human-paced. Claude: claude.ai custom connector, Opus 5.5, 24 of 40 messages. inference.coop: LibreChat,
tinfoil/deepseek-v4-1-flash, 28 of 35 messages. Copilot: not run (D-180).

| Test | Claude | inference.coop |
|---|---|---|
| T1 list tools | works | works |
| T2 list changes mid-session (R3) | does not: the list is fixed when a conversation opens its session; only the connector's "Refresh tools list" updates the catalogue | works: the client re-lists on `list_changed`; the new tools apply from the next turn |
| T3 out-of-stage call | works: refusal quoted, the move left to the coder | works |
| T4 unknown stage (normal / `isError`) | works / works, marked "Failed" | works / works, the error flag not passed to the model |
| T5 stage in a header | works only under an approved header name (`x-environment`); custom names need Anthropic's approval | does not apply: one header slot, used by the key |
| T6 stage in query / path | works / works | works / works (a new entry needed a second Initialize) |
| T7 elicitation | does not: the call hangs (the client declares support, shows no prompt) | does not, cleanly: `elicited: false` |
| T8 router D / E / F (R3b) | as T2 / works / works | works / works / works |
| T9 server restart | works: silent re-initialise; a session-held stage is lost without notice | works: all entries re-initialise; the stage is lost without notice |
| T10 tool count | 3 to 14, no limit seen | 3 to 14, no limit seen |

Findings for WP29 beyond the grid:
- **Sessions differ by client.** Claude opens an MCP session per conversation; inference.coop keeps one session per
  server across all chats, so a session-held stage leaked from one chat into a new one. A stage held only in the
  session is unsafe in both: it leaks (inference.coop) or is lost on restart (both).
- **Static carriers work in both chat clients:** a URL query or path per connector entry, and in Claude an approved
  header name. Claude allows one connector per URL, so entries per stage need distinct URLs.
- **The refusal and the clarification text are relayed in full by both,** and both left the stage to the coder.
- **The model's account of its own tools is unreliable** (inference.coop): after a stage move it recited stale tool
  lists, then disowned a real call; the client's tool set was right. WP31's habits, not the server, must handle this.
- **Elicitation cannot be relied on:** it hangs in Claude and is absent in inference.coop.

## Questions WP29 must decide (RS5-R4)

**Q1. The unit of stage and where it lives.** (a) One stage per vault, held as server data. Fits the flow; needs a stored
value, since none exists. (b) Per narrative (sub-machines): fits the loop and `done`; costs concurrency, needed only if
stages differ per narrative at once (A:S10). (c) Per session, the coder names it: nothing stored, one stage per
connection; restart gives `unknown` (B:E2). Cost: (a) and (b) need persistence across sessions, not tried (F4).

**Q2. How stage travels.** (a) Per-connection header, query or path: works, one connector per stage, the coder edits the
entry to move (B:E1; D:b1); the trials found Claude accepts one only under an approved header name and inference.coop has no slot (T5). (b) Session value by a
tool: needs a stateful server; breaks on restart or on the newer spec (B:E2; G4). (c) Argument: works everywhere, +98
bytes a tool, the assistant must carry it (B:E3). (d) None: the server holds stage; the list stays stable and
out-of-stage calls are refused (B:E6). `_meta` is not expected from chat clients (B:E4).

**Q3. Rely on `list_changed`, or keep the list stable and refuse?** (a) Rely: documented for LibreChat, source-read for
VS Code, unknown for claude.ai (D:a1); needs overrides, a stateful server, private SDK APIs (B:E7, F10); the newer spec
limits it (G4). (b) Stable list plus refusal: no client support needed, longest list (4962 bytes in variant C) and the
model may try out-of-stage tools (B:Q3). (c) Both: list scoping as convenience, refusal as the guarantee (B:E7). Cost:
(c) is the tested shape and carries (a)'s overrides.

**Q4. Single stage-scoped server, or a router?** (a) Single: as today's deployment, nothing new to host (B:Q5). (b) Router
with dynamic list (A): same client need as (a), 362 more lines, 5 ms, new failure modes (B:Q2, Q5). (c) Router with
facade (B): no list change, smallest listing, untyped `call`, per-tool approval lost (B:Q3). Cost of (b) and (c): a
supervisor for four processes or a combined app, and a bypass if mounts are public.

**Q5. Answers to unknown and out-of-stage.** (a) Normal result: works in every client read. (b) `isError` true:
documented only for Claude Code (D:c3). (c) Elicitation: asks the coder directly, support partial (D:c1); must still
fall back to (a).

**Q6. Granularity of stages.** Options are G2's groupings (G:1): ten flow stages; the loop's five activities with
pre-stages; ten with Code and Analyse split by assistant mode; status only. Evidence: the tool-to-stage matrix (G:2);
stages 1, 3, 4, 7 have no tool (F7). Cost: every tool and prompt must sit in at least one stage (a lint the spike
showed, B:E8).

**Q7. Who triggers each move.** (a) Coder only. (b) The tool may suggest a move when every `detect` predicate holds and
refuses it when one fails (B:Q4 placeholder). Evaluable now: E:1, 3, 4, 6, 7, 8, 12; partly E:2, 5, 10, 11, 13; the
coder's word E:14 to 17. New tool candidates: a `scat.toml` reader (E:3, 5), an "all narratives done" count (E:10), a
stored stage. Cost: server work; without them "cap met" and "all done" stay the coder's word.

**Q8. Prompts and resources.** (a) Scope the lists only, as built (B:E7). (b) Also refuse a get or read out of stage: a
protocol error only (B:Q4). (c) Leave them unscoped. VS Code's Copilot sessions do not expose them (D:c4, c5).

**Q9. Stage word and status.** Must stage be one of the glossary words, or new? Status (stub, draft, done) is per page data
and `done` is the coder's attestation (E:9). Options: stage independent of status; derived from page statuses; status as
the only stage. Cost: derivation needs aggregate tools that do not exist (E:10).

**Q10. Which spec era to design for.** (a) 2025-11-25 and SDK 1.30.0: server-held stage and list changes are legal. (b)
Name the stage in each request so the design survives 2026-07-28 (D:f). (c) Wait for the SDK and clients. Evidence:
two reads of the tools page, one of the transports page (F2).

**Q11. Authority of the stage word.** The server cannot tell the coder's word from the assistant's claim (B:E2). Options:
accept as convention; gate moves behind elicitation where declared (D:c1); require a connector edit.

**Q12. Tool names shared across stages.** `status`, `check`, `fingerprint` recur; one schema per name (a lint) or stage
prefixes (B:Q3).

---

## Appendix A. Sources

**A1. Literature (G1), accessed 2026-11-27.** Principle taken is in `spike/lifecycle:research/lifecycle/notes/g1-literature.md`.

| Tag | Source | URL |
|---|---|---|
| S1 | Hermeneutics, SEP | https://plato.stanford.edu/entries/hermeneutics/ |
| S2 | Saldaña, Coding Manual (excerpt), 2009 | https://cfacaa.human.cornell.edu/dea.arl/linked docs/Coding Manual_excerpts.pdf |
| S3 | Bowen, saturation research note, 2008 | https://study.sagepub.com/sites/default/files/Bowen_2008.pdf |
| S4 | Braun and Clarke, Doing reflexive TA | https://www.thematicanalysis.net/doing-reflexive-ta/ |
| S5 | Kolb, Experiential Learning ch. 2, 2014 | https://astec.arizona.edu/sites/default/files/2024-08/Kolb_ProcessOfExperientialLearning.pdf |
| S6 | Hevner et al., Design Science in IS Research, 2004 | https://www.in.th-nuernberg.de/professors/Holl/Personal/Hevner_DesignScience_ISRes.pdf |
| S7 | Peffers et al., DSR Methodology, 2007/08 | https://wise.vub.ac.be/sites/default/files/thesis_info/Design_Science_Research_Methodology_2008.pdf |
| S8 | Coghlan, Action Research in the Academy, 2004 | https://mural.maynoothuniversity.ie/id/eprint/20206/1/2004%20issue%202%20article%201.pdf |
| S9 | Susman and Evered, 1978 (not read; search summary) | https://sswm.info/node/4959 |
| S10 | statecharts.dev, What is a statechart | https://statecharts.dev/what-is-a-statechart.html |
| S11 | Atlassian, Jira workflows | https://support.atlassian.com/jira-cloud-administration/docs/work-with-issue-workflows/ |
| S12 | Flowable, CMMN | https://www.flowable.com/open-source/docs/cmmn/ch06-cmmn |
| S13 | Flowable, BPMN exclusive gateway | https://documentation.flowable.com/latest/model/bpmn/reference/exclusive-gateway |
| S14 | van der Aalst, Petri Nets in workflow management, 1998 | https://users.cs.northwestern.edu/~robby/courses/395-495-2017-winter/Van Der Aalst 1998 The Application of Petri Nets to Workflow Management.pdf |
| S15 | AIWG REF-010, summary of Cooper 1990 | https://unpkg.com/aiwg@2026.2.11/docs/references/REF-010-stage-gate-systems.md |
| S16 | LangGraph Graph API overview | https://docs.langchain.com/oss/python/langgraph/graph-api |
| S17 | Anthropic, Building effective agents, 2024 | https://www.anthropic.com/engineering/building-effective-agents |
| S18 | MCP spec 2025-06-18, Tools | https://modelcontextprotocol.io/specification/2025-06-18/server/tools |
| S19 | Claude Code docs, Skills | https://code.claude.com/docs/en/skills |
| S20 | Kamath et al., arXiv 2512.23738 (abstract only) | https://arxiv.org/abs/2512.23738 |
| S21 | Doshi et al., arXiv 2601.08012 (abstract only) | https://arxiv.org/abs/2601.08012 |

**A2. Protocol and client sources (G4 desk part), accessed 2026-11-27**, from `spike/lifecycle:research/lifecycle/notes/g4-client-docs.md`.
O = opened through a summarising fetch tool; S = search result only; L = local file read.

| Key | Source | How |
|---|---|---|
| M1 | https://modelcontextprotocol.io/specification/latest/server/tools | O |
| M2 | https://modelcontextprotocol.io/specification/2025-11-25/server/tools | O |
| M3 | https://modelcontextprotocol.io/specification/2025-11-25/basic/transports | O |
| M4 | https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | O |
| M5 | https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning | O |
| M6 | https://modelcontextprotocol.io/specification/latest/client/elicitation | O |
| M8 | https://modelcontextprotocol.io/specification/2026-07-28/server/tools | fetched by a reviewer, relayed by the PM (not by U5) |
| M7 | Python `mcp` 1.30.0, site-packages of the spike worktree | L |
| C1, C2 | https://claude.com/docs/connectors/building.md ; https://claude.com/docs/connectors/custom/remote-mcp.md | O |
| C4, C5 | https://github.com/anthropics/claude-code/issues/38324 ; https://github.com/anthropics/claude-ai-mcp/issues/552 | O |
| K1 | https://code.claude.com/docs/en/mcp | O (not a middle slice) |
| L1, L2 | https://www.librechat.ai/docs/features/mcp ; https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/mcp_servers | O |
| L3, L4 | LibreChat `packages/api/src/mcp/connection.ts` (first 100,000 of 121,365 characters) and `parsers.ts`, on raw.githubusercontent.com | O |
| L5 | https://docs.inference.coop/operations/infrastructure | O |
| V2 to V5 | VS Code docs: copilot/reference/mcp-configuration; api/extension-guides/ai/mcp; copilot/guides/mcp-developer-guide; agents/run/tools (all on code.visualstudio.com) | O |
| V6 to V8 | VS Code source `src/vs/workbench/contrib/mcp/common/`: `mcpServer.ts`, `mcpServerRequestHandler.ts`, `mcpLanguageModelToolContribution.ts` (microsoft/vscode, main) | O |
| V9 | https://github.com/microsoft/vscode/issues/349603 | S only |

## Appendix B. Experiments (spike server, SDK `mcp` 1.30.0, all in-process, 127.0.0.1)

Branch `spike/lifecycle`: single server `spike/lifecycle/single/` (`test_experiments.py`, `NOTES.md`); router `spike/lifecycle/router/` (`test_rs5_u4_router.py`, `NOTES.md`, `measurements.json`).

| Id | What | Verdict | Tests |
|---|---|---|---|
| E1 | Header per connection | works | `test_e1_header_per_connection` |
| E1 | Header per request | partly works (httpx hook only) | `test_e1_header_per_request_needs_httpx_event_hook`, `test_e1_sdk_call_tool_has_no_per_request_header_parameter` |
| E1 | Query `?stage=` | works | `test_e1_query_parameter` |
| E1 | Path `/mcp/<stage>` | works | `test_e1_path_variant` |
| E2 | Session value | works stateful; lost stateless; "Session terminated" after restart | `test_e2_session_value_stateful`, `..._lost_in_stateless_mode`, `..._lost_when_server_restarts` |
| E3 | Argument | works; +882 bytes for 9 tools | `test_e3_argument_on_each_call_and_omitted`, `test_e3_argument_schema_cost` |
| E4 | `_meta` | works (SDK); chat clients unlikely | `test_e4_meta_on_call_tool`, `test_e4_meta_on_list_tools_and_in_memory` |
| E5 | Unknown stage: result | works, no protocol error | `test_e5_unknown_stage_returns_result_not_protocol_error[False/True]` |
| E5 | Unknown stage: elicitation | partly works (client must declare it) | `test_e5_elicitation_needs_client_callback` |
| E6 | Out-of-stage call | works, refusal names tool, stage, where, who, how | `test_e6_out_of_stage_call_refused_with_where_and_how` |
| E7 | Per-session lists and `list_changed` | works with overrides; stateless cannot | `test_e7_*` (7 tests: capabilities, scoped lists, notify one session, concurrent sessions, ignoring client, in-memory, stateless) |
| E8 | Cost | 2 to 3 lines per carrier; scoping about 45; clarification about 20; spike server 300 lines; the real server's 19 tools can be scoped by a table of names | `test_e8_carrier_cost_in_lines`, `test_e8_real_server_tools_can_be_scoped_by_data_only` |
| Q1 | Router proxies tools, prompts, resources | works (memory, separate ports, one port) | `test_q1_router_proxies_tools_prompts_resources[...]` |
| Q2 | Dynamic list (A) avoids the change? | partly works (moves it) | `test_q2_dynamic_list_changes_and_notifies_in_memory`, `test_q2_list_changed_arrives_over_http_and_fastmcp_default_declares_none` |
| Q3 | Static facade (B); all tools plus refusal (C) | both work | `test_q3_variant_b_static_facade`, `test_q3_variant_c_all_tools_listed_out_of_stage_refused` |
| Q4 | State machine in the router; unknown, undefined move, unmet predicate, out-of-stage | works | `test_q4_unknown_stage_and_undefined_transition`, `test_q4_predicates_detect_or_need_the_coders_word`, `test_q4_out_of_stage_call_refused_unknown_tool_clarified_and_state_is_per_connection` |
| Q5 | Hosting cost and failure | measured (App. C) | `test_q5_hosting_cost_separate_processes_vs_one_asgi_app`, `test_q5_failure_modes_...`, `test_q5_deploy_facts_from_the_repo_files` |
| Q6 | Proxy preserves listing, results, errors, progress | works | `test_q6_listing_matches_stage_server_field_by_field`, `test_q6_results_errors_and_progress_are_preserved`, `test_q6_extra_hop_latency_median_of_200` |

Re-run for this readout: `uv run --frozen --extra mcp python -m pytest spike/lifecycle -q` gave 44 passed (46 s).

## Appendix C. Numbers

| Id | Number | Source |
|---|---|---|
| 1 | Real server: 19 tools, 6 prompts, 1 resource | `spike/lifecycle:research/lifecycle/notes/g2-raw-material.md`, header |
| 2 | Default FastMCP: `listChanged` false; 12 tools listed to every client | `spike/lifecycle:spike/lifecycle/single/NOTES.md`, E7; `spike/lifecycle:spike/lifecycle/router/NOTES.md`, Q2 |
| 3 | Argument carrier: tools/list 2518 bytes without, 3400 with (+882, 9 tools, about 98 per tool; about 1.9 KB for 19) | `spike/lifecycle:spike/lifecycle/single/NOTES.md`, E3 |
| 4 | Listing sizes, router: facade B 1070; A 1819 (plan) to 2707 (analyse); C 4962 (14 tools: 12 stage tools plus `stage` and `set_stage`) | `spike/lifecycle:spike/lifecycle/router/NOTES.md`, Q3 |
| 5 | Hosting: four processes and four ports about 351 MB; one app one port about 100 MB; start 1.44 s and 1.37 s | `spike/lifecycle:spike/lifecycle/router/NOTES.md`, Q5 |
| 6 | Code: router 362 lines, stand-in stages 65, hosting 13 or 17 plus 10 shared | `spike/lifecycle:spike/lifecycle/router/NOTES.md`, Q5 |
| 7 | Latency, median of 200 `status` calls: memory 1.97 to 3.30 ms; HTTP 5.36 to 10.44 ms (11.06 on one port) | `spike/lifecycle:spike/lifecycle/router/NOTES.md`, Q6 |
| 8 | Dead stage: error after 5.01 s; new connection 0.15 s; blocking tool stalls another connection 1.24 s (vs 0.013 s with separate processes) | `spike/lifecycle:spike/lifecycle/router/NOTES.md`, Q5 |
| 9 | One stage change sends 3 notifications (tools, prompts, resources); stateless: 0 received | `spike/lifecycle:spike/lifecycle/router/NOTES.md`, Q2; `spike/lifecycle:spike/lifecycle/single/NOTES.md`, E2 |
| 10 | VS Code request cap 128 tools (Local harness) | `spike/lifecycle:research/lifecycle/notes/g4-client-docs.md`, row e1 |
| 11 | Spike code: single server 300 lines; scoping about 45; clarification about 20 | `spike/lifecycle:spike/lifecycle/single/NOTES.md`, E8 |

The numbers in rows 5, 7 and 8 come from the router note's run. A re-run for this readout (one machine) gave about 367
MB and 95 MB, 1.94 to 4.78 ms in memory, 5.33 to 10.65 ms over HTTP, 1.2 s and 0.011 s: the same orders of magnitude,
different digits; read them as orders of magnitude.

## Appendix D. What clients document (condensed; documented, not tried)

Cell codes: DS documented supported; DN documented not supported; SRC source read, not run; IO issue open; IC issue
closed, not fixed; UNK nothing found. Keys in A2. **Nothing in this table was tried.** Full matrix:
`spike/lifecycle:research/lifecycle/notes/g4-client-docs.md`.

| Row | claude.ai, Desktop | Claude Code (reference) | inference.coop chat (LibreChat) | VS Code Copilot |
|---|---|---|---|---|
| a1 re-lists on `tools/list_changed` | UNK; IC: apps keep first list [C4] | DS interactive [K1] | DS [L2]; SRC [L3] | SRC [V6, V7]; IO picker stale [V9] |
| a2 prompts and resources `list_changed` | UNK | DS [K1] | resources SRC; prompts UNK | prompts SRC; resources not handled |
| b1 static custom headers | DS beta, max four, approved names [C2] | DS [K1] | DS one API-key header [L1]; YAML [L2] | DS [V2] |
| b3 per-request headers | DN [C2] | per connection only [K1] | YAML only, admin [L2] | UNK |
| b4 session id and 404 | UNK | UNK | SRC re-initialise, 3 tries [L3]; lab run re-initialised once | UNK |
| c1 elicitation | UNK | DS [K1] | UNK; SRC none [L3] | DS in Copilot sessions [V3, V4] |
| c3 `isError` shown differently | UNK | DS [K1] | SRC no [L4] | SRC no [V8] |
| c4, c5 prompts, resources shown | DS exposable [C1] | DS [K1] | UNK | DN in Copilot sessions; DS Local harness [V3, V4] |
| e1 tool-count limit | UNK | none; tool search [K1] | UNK | 128 Local harness [V5] |
| f revision spoken | auth specs to 2025-11-25 [C1] | 2026-07-28 and earlier [K1] | UNK | UNK; docs link to 2025-11-25 [V3] |

Spec row f: 2025-11-25 allows server state (`Mcp-Session-Id`) and `tools.listChanged`, which SDK 1.30.0 implements
[M2, M3, M7]. 2026-07-28, as read: a tool list MUST NOT vary per connection or as a side effect of other requests (MAY vary by request authorization), `list_changed` only on a `subscriptions/listen` stream, handles passed by the model recommended [M1, M8]; no sessions, `initialize` and `Mcp-Session-Id` removed [M4, M5] (transports page, single-sourced); elicitation as `input_required` result [M6]. The co-op's page names LibreChat, gives no version, does not mention MCP [L5].

## Appendix E. Predicates (17), tried on copies of the contract examples

Source: `spike/lifecycle:research/lifecycle/notes/g5-predicates.md`. 17 classified, 13 run (1 to 13). C complete; P partial; W the coder's word.

| # | Predicate | Evaluator | Verdict |
|---|---|---|---|
| 1 | Vault folder exists | `check` | C |
| 2 | Vault set up | `check` (not install, Obsidian, git) | P |
| 3 | `scat.toml` has the cap | `check` (presence; value unreadable) | C |
| 4 | `scat.toml` has attribution mode | `check`; `mode` in every result | C |
| 5 | Stakeholder-group cap met | none direct; `stub` refuses at cap | P |
| 6 | Narrative exists; stub, draft or done | `status` | C |
| 7 | Narrative coded | `check` (SCAT-UNCODED), `fingerprint` | C |
| 8 | Check passes | `check` | C (structure only) |
| 9 | Narrative may be set to done | `set-status X done` (CLI); MCP never sets `done` | C on CLI only |
| 10 | All narratives done | none; caller aggregates `status` | P |
| 11 | Views generated | views are computed on demand; `export_edges` writes files | P |
| 12 | Views can be trusted | views refuse on page errors | C for drawn pages |
| 13 | Done narrative changed or reopened | `record_edge` and `remove_edge` refuse; no history | P |
| 14 | Terms set | none | W |
| 15 | Field notes taken | none | W |
| 16 | Model finished | none | W |
| 17 | Committed, pushed, tagged | git, not run | W |

Counts (17 classified, 13 run): complete 7 (1, 3, 4, 6, 7, 8, 12); CLI only 1 (9); partial 5 (2, 5, 10, 11, 13); word 4 (14 to 17). Gaps: no
server read of `scat.toml`; no stored or derived stage; check is structure only; git and chat calls not run.

## Appendix F. What is not known or not done

| Id | Item |
|---|---|
| F1 | Copilot's behaviour: not tried (D-180). Claude and inference.coop were tried (see Client trials). |
| F2 | 2026-07-28 spec: the tools-page claims were read twice (U5's summarising fetch; a reviewer's fetch); the transports-page claims (no `initialize`, no `Mcp-Session-Id`, no standalone stream) only by U5; this writer re-fetched neither; which clients speak it is unknown except Claude Code's docs. |
| F3 | Weak sources: Susman and Evered (S9) not read; Harel's original not read; Stage-Gate is a summary of Cooper; hermeneutics authors not checked; S20 and S21 abstract only. |
| F4 | Persistence of stage across sessions or restarts: not tried. |
| F5 | Router: cost under many connections, cancellation, large results, pagination, completions, elicitation and sampling passthrough, stage servers' own `list_changed`: not built. |
| F6 | Prompts and resource gets are not gated by stage in the spike; gating would be a protocol error only. |
| F7 | Stages 1, 3, 4, 7 have no tool; no tool for `scat.toml`, set-up, git, terms, field notes or images. |
| F8 | LibreChat claims are about upstream `main`, not the co-op's build; its admin settings are unknown; the co-op's allowed-address rules too. |
| F9 | Facade B's fit for a tool-calling model and for per-tool approval; whether tool selection improves with a short list. |
| F10 | The spike uses private SDK paths (`_mcp_server`); an SDK upgrade could move them. |
| F11 | The probe logs behind the G2 assistant-failure list are outside the repository; only a summary is in it. |
| F12 | Whether the structure helps weaker models stay on track: no evidence for our case. |

## Appendix G. G2 raw material, condensed

From `spike/lifecycle:research/lifecycle/notes/g2-raw-material.md` (counts listed from the code: 19 tools, 6 prompts, 1
resource, `src/scat_kg/mcp_server/server.py`). Nothing is chosen. Abbreviations: org organiser; coder; setup the person who
set the tools up; asst assistant (no authority). Transitions are numbered TR1 to TR20 here, to keep them apart from the
trial tests T1 to T10.

**G:1 Candidate groupings.**

| Id | Grouping | Actor | Comes from |
|---|---|---|---|
| G-A | Flow and journeys, ten steps: 1 Discover, 2 Try, 3 Decide, 4 Set terms, 5 Set up, 6 Plan, 7 Capture, 8 Code, 9 Analyse, 10 Hand over (solo order 5, 2, 8) | org (1 to 7), coder (8 to 10) | flow guide; mission journeys J1 to J10 |
| G-B | Coder's loop: interpreting, authoring, coding, reviewing; then analysing (G-B': Analyse as the fifth activity, D-160) | coder owns; asst helps; tool checks | coding guide; `code-a-narrative` prompt steps 1 to 4 |
| G-C | Page status cycle: stub, draft, done; done back to draft | coder sets done | norms; `set_status` |
| G-D | SCAT Chat session: install once, start, connect, skill and agent, use, stop, clean up | org, setup | chat-path guide; leave-no-trace run |
| G-E | Assistant modes: code a narrative, explain a problem, review before done, draft a node page, sweep stub node pages, look for duplicates, end of session | asst for coder | prompts; skill |
| G-F | "Finished model" as a condition: conformant graph, navigable vault, views generated, coder's statement | coder | mission; flow |

Alternatives the sources support: (a) a vault-level machine of ten (G-A) with G-B and G-C as per-narrative sub-machines;
(b) a flat machine on G-B's five activities with Set up and Plan as pre-stages; (c) G-A with Code and Analyse split by G-E
modes; (d) G-C only, stage as a property of a page. Which unit carries the stage (vault, narrative, session) is open.

**G:2 Tool, prompt and resource to stage.** Stage columns: 5 Set up, 6 Plan, 8a interpret, 8b author, 8c code, 8d review,
8e node pages, 8f duplicates, 9 Analyse, 10 Hand over. Parentheses mark placement inferred from the tool's description.

| Item | Stages |
|---|---|
| T `check` | 5, 6, 8d, 8f, 9, 10 |
| T `status` | 8d, 8e, (8a), (10) |
| T `set_status` (refuses `done`) | 8b, 8d |
| T `stub` | 8b, 8c |
| T `stub_links` | 8c |
| T `record_edge` | 8c |
| T `remove_edge` | 8c, 9 (revisit) |
| T `merge` (plan only) | 8f |
| T `split_plan` | 8f |
| T `index` | 10 |
| T `fingerprint` | 8d, 9 |
| T `edge_table`, `layered`, `trace` | 9 |
| T `evidence` | 8e, 8f, 9 |
| T `copy_share` | 8e, 9 |
| T `review` | 8f, 9 |
| T `attribution` | (9) |
| T `export_edges` | 9, (10) |
| P `code-a-narrative` | 8a, 8b, 8c, 8d |
| P `explain-a-problem` | 8d (any stage with a problem, inferred) |
| P `review-before-done` | 8d |
| P `draft-a-node-page`, `fill-in-node-pages` | 8e |
| P `look-for-duplicates` | 8f |
| R `scat://assistant-rules` | 8a to 8f, (9); text embedded in four prompts |

Shared across stages: `check` (six columns) and `status`, then `evidence`. Stages 1, 3, 4 and 7
have no tool; Plan has only `check`. Every result carries the attribution `mode`.

**G:3 Transitions.** Decides: tool = a call returns the evidence; coder = only the coder's word; either = tool can show it,
the coder confirms.

| Id | From to | Dir | Trigger | Decides |
|---|---|---|---|---|
| TR1 | 1 to 2 to 3 | fwd | interest; trial done | coder or org |
| TR2 | 3 to 4 to 5 to 6 to 7 | fwd | each step's "depends on" | org |
| TR3 | 5 to 2 to 8 (solo) | fwd | no participants, so no 4 or 7 | org |
| TR4 | 7 to 8a | fwd | field notes exist | org (no tool) |
| TR5 | 8a to 8b to 8c to 8d | fwd | each step handed back to the coder | coder |
| TR6 | 8d to 8a, 8b or 8c | back | check reports a problem; coder doubts the account or the coding | either |
| TR7 | stub to draft | fwd | coder or asst sets it | either (`set_status`) |
| TR8 | stub to done | fwd | allowed in one sitting | coder |
| TR9 | draft to done | fwd | check passes and coder confirms | coder; tool refuses with SCAT-DONE-REFUSED |
| TR10 | done to draft | back | coder reopens to edit | coder in Obsidian; server refuses |
| TR11 | 8d to 9 | fwd | clean check, content signed off | either |
| TR12 | 9 to 8 | back | reading the views sends the coder to notes or pages | coder |
| TR13 | 9 to 8a, revisit list | back | assistant interprets the images, hands back | coder |
| TR14 | 8 to 6 | back | the stakeholder-group cap refuses a new group; raise it or link an existing group | tool refuses on `stub`; setup decides |
| TR15 | 8 to 6 or 4 | back | attribution mode changed; pages flag | coder |
| TR16 | 8, 9 to 10 | fwd | clean check, views, commit, push | tool shows check; coder says |
| TR17 | 10 to 8 | back | work continues after a hand-over | coder |
| TR18 | 10 to follow-through | fwd | commitments to participants | org |
| TR19 | 8c to 8e or 8f | lateral | a node needs a page, or two pages may be one | either (`review`) |
| TR20 | G-D session | fwd | start, connect, use, stop, clean up | org, setup |

Inferred, not sourced: 8 to 7 (more field notes needed) and 9 to 7; the sources say "back to the field notes" and name no step.

**G:4 Conflicts and gaps (ten).**

1. No stage is stored: status is per page; a server needing stage must derive it or be told.
2. Unit conflict: the flow is the organiser's journey (one vault), the loop is per narrative, `done` is per page; the sources use "stage" at all three.
3. Order conflict: Try (2) is numbered before Set up (5) but depends on it.
4. Node-page and duplicate work (`evidence`, `copy_share`, `review`, `merge`, `split_plan`) is "views" in one guide and loop work in another; no stage owns it.
5. `attribution` is in no guide's view list; `export_edges` sits under views in one guide while "views generated" is also met on demand.
6. `index`: the flow lists it at hand-over, but the template ships all five and `merge` runs it, so it does little there.
7. No tool for reading or writing `scat.toml`, set-up, commit, push or tag, terms and consent, field-notes intake, or drawings (no tool returns an image).
8. Assistant behaviour in probes (a summary only is in the repository): listed nodes before an account was drafted, recorded unconfirmed edges, ruled on a duplicate without `review`, misreported statuses and the cap, did not know `mode`, drew diagrams itself; these are the failures a stage scope would target.
9. Skill coverage: one skill, `scat-coding`; no sections for stages 5 to 7, 9 beyond views, and 10.
10. The `assistant-rules` resource text sits inside four prompts, not the other two.
