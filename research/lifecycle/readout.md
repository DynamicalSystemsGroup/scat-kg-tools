# Lifecycle readout (RS5): the stage machine, what the evidence says and what WP29 must decide

**Status.** Desk and server experiments are done (27 Nov 2026). Client trials (RS5-R3, and the client parts of G4 and
R3b) are **HELD** for the chief engineer's accounts and the ACE; their plan is `spike/lifecycle/TRIAL-PLAN.md` on branch
`spike/lifecycle` of `scat-kg-tools` (written in parallel; not read for this readout). Nothing here was tried in Claude,
inference.coop's chat or VS Code's Copilot. Every client statement is "documented, not tried" or "source read, not run".
The spike code and notes live only on that branch; paths below are branch paths. "Stage" and "transition" are not yet
glossary words (WP29 adds them); here "stage" means a state of the lifecycle, and nothing else is meant. Evidence refs
such as (B:E7) point to the appendices.

## Recommendation / summary

No option is chosen for WP29. What the evidence says:

- **A flat machine is enough** (G1): stages, named moves, named predicates, one current stage, a reserved `unknown`.
- **The sources carry five groupings** of the lifecycle plus a "finished model" condition (G2); they nest and disagree
  on the unit (vault, narrative, page). No stage is stored today.
- **Stage cannot ride on a per-request header from a chat client**: header, query and path are fixed per connection
  (B:E1, D:b3). Per-request carriers that work are an argument (any client, at a byte cost) and `_meta` (SDK only).
- **A per-session tool-list change works in the SDK, with overrides**, and a refusal makes it optional (B:E6, E7).
  Client honouring is documented for three of four and unknown for claude.ai (D:a1); the latest spec reportedly
  removes what it needs (G4).
- **A router does not remove the list change**; only its static facade does, at a price (B:Q2, Q3).
- **Most predicates are evaluable or the coder's word**; no tool reads `scat.toml` (G5).

**Closed by evidence:** a per-request stage header on the chat path; session value or `list_changed` on a stateless
server; "a router avoids the list change" (except the facade); elicitation as the only clarification path. **Stay open:** the unit of stage, granularity, whether to rely on `list_changed`, single
server versus router, the spec era to design for, every trigger and predicate choice, and all client behaviour.

## G1. Smallest sufficient form (literature)

Sources: A:S1 to S21 (read for principles; S9, Harel's original and Cooper are second-hand, A:F3).

- Loops are the norm and the stop is a person's judgement (S1 to S9): "enough" is a *request* predicate, a backward move
  is ordinary.
- Workflow engines give explicit moves, a separate move for going back, guards, a default when none fires, and a
  person or program as trigger (S10 to S13, S15, S16). Predicates stay pure; soundness is a reachability check (S14).
- Harness-side tool restriction lasts one turn (S19), so stage must live in server data or in the request. MCP servers
  may announce a changed tool list; execution errors travel in results (S18).

**The form:** a list of stages (plus `unknown`), each with expected inputs, outputs, tools, prompt and skill sections as
plain lists; a list of moves (from, to, direction, name, predicates); predicates in two modes, `detect` (tool evaluates,
read-only) and `request` (returns a question to the coder); one current stage; a clarification result in `unknown` or
for a disallowed call. Hierarchy, concurrency, history, timers and guards with side effects were each judged not needed.

**Not known:** the right stage count; the unit of stage; formal literature on tool restriction as an enabling constraint
(one search found none); whether this helps weaker models (F12).

## G2. Raw material (no choice)

Source: `research/lifecycle/notes/g2-raw-material.md`. The server has 19 tools, 6 prompts, 1 resource.

**Candidate groupings** (each an offer):
1. G-A: the flow and journeys J1 to J10, the same ten names: Discover, Try, Decide, Set terms, Set up, Plan, Capture,
   Code, Analyse, Hand over (solo order 5, 2, 8).
2. G-B: the coder's loop: interpret, author, code, review (G-B' adds Analyse). G-C: the status cycle, stub, draft,
   done, and done back to draft.
3. G-D: a SCAT Chat session. G-E: assistant modes (code a narrative, explain a problem, review, draft a node page,
   sweep stubs, look for duplicates). G-F: "finished model" as a condition.

Alternatives: ten stages with G-B and G-C as per-narrative sub-machines; a flat machine on the loop's five activities
with Set up and Plan before it; ten with Code and Analyse split by assistant mode; status only.

**Tools by stage.** `check` fits seven columns; most of the 19 tools cluster in Code and Analyse; stages 1, 3, 4 and 7
have no tool; Plan has only `check`. **Transitions:** twenty (T1 to T20): forward; backward (review to interpret, author
or code; Analyse to Code; done to draft, refused by the server; Code to Plan when the group cap refuses; Hand over to
Code); lateral (a node needs a page, or may duplicate another).

**Conflicts and gaps (ten, in the note):** no stage is stored; three units use the word; Try is numbered before Set up but
depends on it; node-page and duplicate work belongs to no stage; no tool for `scat.toml`, set-up, git, terms or field
notes; one skill, with no sections for stages 5 to 7 and 10.

**Not known:** which unit carries the stage; whether 8 to 7 and 9 to 7 exist (inferred, no source).

## G3. How stage reaches the server (RS5-R2)

Tried in a throwaway FastMCP server on 127.0.0.1 with the SDK's own client; SDK `mcp` **1.30.0**; 44 spike tests pass
(re-run for this readout). Notes: `spike/lifecycle/single/NOTES.md`. Classes are about the SDK; chat-client support is
not tried for any row.

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
stage per connection. Documentation agrees: claude.ai sends up to four fixed approved header names, VS Code and Claude
Code static headers, the co-op's form one API-key header; only an administrator's LibreChat YAML sends a header per chat
request (D:b1, b3). Whatever the carrier, the server cannot tell the coder's word from the assistant's claim of it
(B:E2).

**Clarification.** An unknown or missing stage returns a normal result (the stages, who decides, how to move), no
protocol error, in the SDK and the router (B:E5, Q4). Elicitation works only if the client declares it; the SDK test
did. Documented: Claude Code, VS Code Copilot sessions; unknown: claude.ai; none seen in LibreChat's code read (D:c1).
**Out of stage.** A call outside the stage returns a result naming the tool, the stage, where it is available and how
to move (B:E6). `isError` true or false differ only in that flag; which a client shows is not tried (D:c3).

**Not known:** whether any chat connector can set a custom header; how reliably an assistant carries an argument.

## G4. Scoping what the server exposes (RS5-R3b, R3 held)

**Per-session `list_changed` (SDK).** Works with three code details: replace FastMCP's list handlers and `call_tool`
via the low-level server (private `_mcp_server`), patch the initialisation options so `listChanged` is advertised
(default FastMCP says false and lists 12 tools to everyone), and keep the server stateful. A move notifies its own session
only; two sessions saw different lists; stateless mode delivered 0 notices (B:E7). Prompts and resources: lists scoped, gets not gated.

**Client support, documented, not tried** (D:a1): Claude Code and LibreChat re-list (documented); VS Code Copilot re-lists
on it and after each tool call (source read; a stale-picker issue is open); claude.ai and Desktop: nothing documented,
and a user issue says the apps keep the first list (closed, not planned). LibreChat is upstream `main`, not the co-op's
build.

**The spec.** The latest revision, 2026-07-28, reportedly removes `initialize`, `Mcp-Session-Id` and the standalone
stream, and says a tool list MUST NOT vary per connection or as a side effect of other requests, though it MAY vary by
the authorization on each request (D:f). Python `mcp` 1.30.0 implements only up to 2025-11-25, where a server may keep
session state. Sourcing: spec pages read by a summarising fetch tool, wording unchecked, not re-fetched here; Claude
Code's docs mention a 2026-07-28 runtime; no other client's revision is known (F2). If correct, a server-held stage with a changing list is legal in the older era and against
the newer; a stage the client names in each request (an argument or a handle in a result) is legal in both.

**Router (the chief engineer's option) versus single server.** The router proxies tools, prompts, resources, results and
progress unchanged over three transports (B:Q1, Q6); stage servers stay plain and separately testable. The single
column is reasoned, not tested as a comparison (B:E7 tests the single server):

| | Router over per-stage servers | Single stage-scoped server |
|---|---|---|
| List change | Not removed (variant A); only the static facade B avoids it: 4 fixed tools, 1070 bytes, untyped `call` | Same choices; refusal as the net |
| Hosting | One app: about 100 MB, 1 port; four processes: about 351 MB, 4 ports; entrypoint changes | As today: one process, one port, one key gate |
| Code | Router 362 lines plus 23 to 27 hosting | About 45 lines scoping plus about 20 for the clarification |
| Latency | +1.3 ms memory, +5 ms HTTP | None |
| Failure | Dead stage stalls 5.01 s; shared loop stalls others about 1.2 s; mounts bypass the machine | Tool error is a result; a crash ends all |

The chat still sees one server either way (B:Q5). Listing sizes: 1070 (B), 1819 to 2707 (A), 4962 (C, all tools listed,
refuse out of stage). Facade B's costs for a model are not tried in a client.

**Not known:** every client's behaviour (held); router cost under many connections (F5).

## G5. Predicates

Of 17 predicates tried on a copy of the contract examples (E): 7 are fully evaluable by the tools (folder exists,
`scat.toml` cap and mode present, a narrative's status, narrative coded, check passes, views run clean); 1 only on the
CLI (would-`done`); 5 partly (set up, cap met, all done, views generated, done changed); 4 are the coder's word (terms,
field notes, model finished, committed). **Gaps:** no tool reads `scat.toml`, so "cap met" shows only as a refused
write; no stored or derived stage; check covers structure, not interpretation. **Not known:** git-side predicates.

## What is held for the client trials

Per client: `list_changed` honoured within and across conversations; a custom header accepted; elicitation shown;
`isError` read differently; session loss; how the facade and the refusal read to a model. Plan: `TRIAL-PLAN.md` above.

## Questions WP29 must decide (RS5-R4)

**Q1. The unit of stage and where it lives.** (a) One stage per vault, held as server data. Fits the flow; needs a stored value, since none exists. (b) Per narrative: fits the loop and `done`; costs concurrency, needed only if stages differ per narrative at once
(A:S10). (c) Per session, the coder names it: nothing stored, one stage per
connection; restart gives `unknown` (B:E2). Cost: (a) and (b) need persistence across sessions, not tried (F:4).

**Q2. How stage travels.** (a) Per-connection header, query or path: works, one connector per stage, coder edits the
entry to move (B:E1; D:b1). (b) Session value by a tool: needs a stateful server; breaks on restart or on the newer spec (B:E2; G4). (c) Argument: works everywhere, +98 bytes a tool, the assistant must carry it
(B:E3). (d) None: the server holds stage; the list stays stable and out-of-stage calls are refused (B:E6). `_meta` and
a per-request header are not reachable from chat clients (B:E4; D:b3).

**Q3. Rely on `list_changed`, or keep the list stable and refuse?** (a) Rely: documented in three of four clients
(D:a1); needs overrides, a stateful server, private SDK APIs (B:E7, F10); spec direction against it (D:f). (b) Stable list plus refusal: no client support needed, longest list (4962 bytes in the spike's variant C) and
the model may try out-of-stage tools (B:Q3). (c) Both: list scoping as convenience, refusal as the guarantee (B:E7).
Cost: (c) is the tested shape and carries (a)'s overrides.

**Q4. Single stage-scoped server, or a router?** (a) Single: as today's deployment, nothing new to host (B:Q5). (b) Router
with dynamic list (A): same client need as (a), 362 more lines, 5 ms, new failure modes (B:Q2, Q5). (c) Router with
facade (B): no list change, smallest listing, untyped `call`, per-tool approval lost (B:Q3). Cost of (b) and (c): a
supervisor for four processes or a combined app, and a bypass if mounts are public.

**Q5. Answers to unknown and out-of-stage.** (a) Normal result: works in every client read; (b) result with `isError`
true: documented to reach the model in Claude Code only; look unknown elsewhere (D:c3); (c) elicitation: asks the coder
directly, but support is partial (D:c1).  Cost: (c) must still fall back to (a).

**Q6. Granularity of stages.** Options are G2's groupings: ten flow stages; the loop's five activities with pre-stages; ten
with Code and Analyse split by assistant mode; status only. Evidence: tool-to-stage matrix (G2 note, section 3); stages 1, 3, 4, 7
have no tool (F7). Cost: every tool and prompt must sit in at least one stage (a lint the spike showed, B:E8).

**Q7. Who triggers each move.** (a) Coder only. (b) The tool may suggest a move when every `detect` predicate holds and
refuses it when one fails (B:Q4 placeholder). Evaluable now: E:1, 3, 4, 6, 7, 8, 12; partly E:2, 5, 10, 11, 13; the coder's word E:14 to 17. New tool candidates: a
`scat.toml` reader (E:3, 5), an "all narratives done" count (E:10), a stored stage. Cost: server work; without them
"cap met" and "all done" stay the coder's word.

**Q8. Prompts and resources.** (a) Scope the lists only, as built (B:E7). (b) Also refuse a get or read out of stage: a protocol error only, no
clarification (B:Q4). (c) Leave them unscoped. Evidence: VS Code's Copilot sessions do not expose
prompts or resources (D:c4, c5).

**Q9. Stage word and status.** Must stage be one of the glossary words, or new? Status (stub, draft, done) is per page data and `done` is the coder's attestation (E:9). Options: stage
independent of status; derived from page statuses; status as the only stage. Cost: derivation needs aggregate tools
that do not exist (E:10).

**Q10. Which spec era to design for.** (a) 2025-11-25 and SDK 1.30.0: server-held stage and list changes are legal. (b) Name the
stage in each request so the design survives 2026-07-28 (D:f). (c) Wait for the SDK and clients. Evidence is
single-sourced (F2).

**Q11. Authority of the stage word.** The server cannot tell the coder's word from the assistant's claim (B:E2). Options:
accept as convention; gate moves behind elicitation where declared (D:c1); require a connector edit. Cost: each narrows
who can move the stage.

**Q12. Tool names shared across stages.** `status`, `check`, `fingerprint` recur; one schema per name (a lint) or
stage prefixes (B:Q3).

---

## Appendix A. Sources

**A1. Literature (G1), accessed 2026-11-27.** Principle taken is in `research/lifecycle/notes/g1-literature.md`.

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

**A2. Protocol and client sources (G4 desk part), accessed 2026-11-27**, from `research/lifecycle/notes/g4-client-docs.md`.
O = opened through a summarising fetch tool; S = search result only; L = local file read.

| Key | Source | How |
|---|---|---|
| M1 | https://modelcontextprotocol.io/specification/latest/server/tools | O |
| M2 | https://modelcontextprotocol.io/specification/2025-11-25/server/tools | O |
| M3 | https://modelcontextprotocol.io/specification/2025-11-25/basic/transports | O |
| M4 | https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | O |
| M5 | https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning | O |
| M6 | https://modelcontextprotocol.io/specification/latest/client/elicitation | O |
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

Single server: `spike/lifecycle/single/` (`test_experiments.py`). Router: `spike/lifecycle/router/` (`test_rs5_u4_router.py`).

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
| 1 | Real server: 19 tools, 6 prompts, 1 resource | g2 note, header |
| 2 | Default FastMCP: `listChanged` false; 12 tools listed to every client | single NOTES, E7; router NOTES, Q2 |
| 3 | Argument carrier: tools/list 2518 bytes without, 3400 with (+882, 9 tools, about 98 per tool; about 1.9 KB for 19) | single NOTES, E3 |
| 4 | Listing sizes, router: facade B 1070; A 1819 (plan) to 2707 (analyse); C 4962 (12 tools) | router NOTES, Q3 |
| 5 | Hosting: four processes and four ports about 351 MB; one app one port about 100 MB; start 1.44 s and 1.37 s | router NOTES, Q5 |
| 6 | Code: router 362 lines, stand-in stages 65, hosting 13 or 17 plus 10 shared | router NOTES, Q5 |
| 7 | Latency, median of 200 `status` calls: memory 1.97 to 3.30 ms; HTTP 5.36 to 10.44 ms (11.06 on one port) | router NOTES, Q6 |
| 8 | Dead stage: error after 5.01 s; new connection 0.15 s; blocking tool stalls another connection 1.24 s (vs 0.013 s with separate processes) | router NOTES, Q5 |
| 9 | One stage change sends 3 notifications (tools, prompts, resources); stateless: 0 received | router NOTES, Q2; single NOTES, E2 |
| 10 | VS Code request cap 128 tools (Local harness) | g4 note, row e1 |
| 11 | Spike code: single server 300 lines; scoping about 45; clarification about 20 | single NOTES, E8 |

The numbers in rows 5, 7 and 8 come from the router note's run. A re-run for this readout (one machine) gave about 367
MB and 95 MB, 1.94 to 4.78 ms in memory, 5.33 to 10.65 ms over HTTP, 1.2 s and 0.011 s: the same orders of magnitude,
different digits; read them as orders of magnitude.

## Appendix D. What clients document (condensed; documented, not tried)

Cell codes: DS documented supported; DN documented not supported; SRC source read, not run; IO issue open; IC issue
closed, not fixed; UNK nothing found. Keys in A2. **Nothing in this table was tried.** Full matrix:
`research/lifecycle/notes/g4-client-docs.md`.

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
[M2, M3, M7]. 2026-07-28, as read: no sessions; a tool list MUST NOT vary per connection; elicitation as
`input_required` result [M1, M4, M5, M6]. The co-op's page names LibreChat, gives no version, does not mention MCP [L5].

## Appendix E. Predicates (17), tried on copies of the contract examples

Source: `research/lifecycle/notes/g5-predicates.md`. C complete; P partial; W the coder's word.

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

Counts: complete 7 (1, 3, 4, 6, 7, 8, 12); CLI only 1 (9); partial 5 (2, 5, 10, 11, 13); word 4 (14 to 17). Gaps: no
server read of `scat.toml`; no stored or derived stage; check is structure only; git and chat calls not run.

## Appendix F. What is not known or not done

| Id | Item |
|---|---|
| F1 | Every client behaviour: held for the trials (R3, and client parts of G4 and R3b). |
| F2 | The 2026-07-28 spec claims rest on pages read through a summarising fetch tool, wording unchecked, not re-fetched for this readout; which clients speak it is unknown except Claude Code's docs. |
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
