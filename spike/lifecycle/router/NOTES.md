# RS5-U4: the chief engineer's option, a routing top-level MCP server over per-stage MCP servers

SDK: `mcp` 1.30.0 (printed by `test_sdk_version`, stored in `measurements.json`). Python 3.12.10, macOS. Everything binds 127.0.0.1 and is stopped by the tests.
Run: `uv run --frozen --extra mcp python -m pytest spike/lifecycle/router -q` (18 tests, about 28 s). Numbers below are from that run (`measurements.json`, rewritten each run; one run, single machine, so read them as orders of magnitude).
Setup: `uv sync --frozen --extra mcp` was enough; pytest, ruff, uvicorn, starlette, httpx were already in the locked set. Nothing changed in pyproject or uv.lock.

Throwaway code: `lc_stages.py` (three stand-in stage servers: plan, code, analyse; 12 distinct stand-in tools, `status` and `check` in every stage, `fingerprint` in two), `lc_router.py` (the router and its state machine), `lc_hosting.py` (the two hostings), `lc_harness.py` (processes, ps, timing), `test_rs5_u4_router.py`.
The router is a low-level `mcp.server.lowlevel.Server` and an MCP client to each stage server. State (current stage) and the upstream sessions live per client connection.

## Findings first

1. A router that proxies tools, prompts and resources to per-stage servers inside one client connection works, over memory and over streamable HTTP, on separate ports and on one port. Descriptions, schemas, results, `isError` and progress pass through unchanged.
2. It does not remove the mid-session change. With the router the client still sees a changed tool list and still needs `list_changed`. It moves the change from a stage server to the router. Only the static facade (variant B) needs no list change, at the cost of typed per-tool schemas.
3. Cost of the hop: median +1.3 ms in memory (1.97 to 3.30 ms) and about +5 ms over localhost HTTP (5.36 to 10.44 ms, 11.06 on one port). Small against an LLM turn.
4. Hosting: one ASGI app in one process is about 100 MB resident and one port; four processes are about 351 MB and four ports. The router adds about 360 lines of code (a single stage-scoped server needs none of it).
5. New failure modes that a single server does not have: a dead stage server stalls a call until the router's timeout (5 s here), and a stage server mounted on the public app can be called directly, around the state machine.

## Q1. Can one top-level server route to per-stage servers inside one connection?  Verdict: works

Tests: `test_q1_router_proxies_tools_prompts_resources[memory | http_separate_ports | http_one_port]`.
Tried: stage servers are plain FastMCP servers. The router connects to each (in-memory transport; streamable HTTP on four ports; streamable HTTP to its own mounts on one port) and forwards `tools/call`, `prompts/get`, `resources/read` and the lists for the current stage. A client over one connection lists tools, calls `status`, gets prompt `stage_guide` and reads `stage://plan/guide`, all through the router.
Found while building (not in the brief, matters): with the SDK's HTTP client, a dead stage server does not return an error. The transport's task group fails and cancels the task that holds the session, which hung the whole router connection (more than 20 s in my first version). The router now holds each upstream session in its own task and wraps every upstream request in a timeout. Any real router needs this.
Not built, so not known: pagination cursors, `_meta`, resource templates and subscriptions, completions, logging, sampling and elicitation (these would need forwarding), and a stage server sending its own `list_changed` (ignored). Output validation of structured results by the client works as normal, since schemas pass through.

## Q2. Variant A, dynamic list: does it avoid the mid-session tool-list change?  Verdict: partly works (only moves it)

Tests: `test_q2_dynamic_list_changes_and_notifies_in_memory`, `test_q2_list_changed_arrives_over_http_and_fastmcp_default_declares_none`.
Result: plan lists `stage, set_stage, status, check, stub`; after the move to code it lists `stage, set_stage, status, check, set_status, record_edge, fingerprint, progress_demo, fail_demo, block`. One stage change sends three notifications (`tools`, `prompts`, `resources` `list_changed`); a refused move sends none. The notifications arrive over HTTP too (separate ports, router in its own process).
So the client sees exactly what it would see from a single stage-scoped server that changes its list. The stage servers themselves never change; the router carries the change. The need for client support of `list_changed` is not reduced.
Also found: a plain FastMCP server (what `src/scat_kg/mcp_server` is) declares `tools.listChanged = false` (tested). A server that changes its list must declare it: the router overrides `create_initialization_options` with `NotificationOptions(tools_changed=True, ...)`. This applies to the single-server design as well.
Safety net, same as variant C: a client with a stale list that calls an out-of-stage tool gets the refusal result (Q4).
Not known (needs client trial): whether Claude, inference.coop or VS Code Copilot re-list on `list_changed`, and whether they do so mid-turn.

## Q3. Variant B (static facade) and variant C (all tools, refuse out of stage)

Tests: `test_q3_variant_b_static_facade`, `test_q3_variant_c_all_tools_listed_out_of_stage_refused`.
Variant B: the router lists four fixed tools: `stage`, `set_stage`, `stage_tools`, `call(tool, args)`. Verdict: works. No list change (zero notifications across a stage move; the listing is identical before and after). The real tools are discovered through the `stage_tools` result (name, description, input schema) and called through `call`.
Lost: (a) typed schemas per tool in the listing: `call` has only `tool` and `args`; a wrong argument set is caught by the stage server and comes back as an error text (`Field required ...`), not by the client's schema check or the model's tool-calling grammar. (b) Client-side approval granularity: a client that approves per tool name can only approve `call` for all stage tools (by construction; not tried in a client). (c) How an LLM sees it: an indirect call it must learn from a result; this is the least natural form for tool-calling models. Needs client trial.
Gained: no dependence on `list_changed`; the smallest listing (1070 bytes against 1819 to 2707 for variant A, and 4962 for variant C), so less context per turn.
Prompts and resources are not facaded (the router lists none in this mode); each would need its own facade tool. Not built.
Variant C: works as a null baseline. The router lists the union of all stage tools (12 tools, 4962 bytes) at all times; no notification; an out-of-stage call returns a refusal naming the stages that have it. Name collisions: `status`, `check`, `fingerprint` are in several stages; the union is honest only when the schemas are identical (asserted). Different schemas under one name would need prefixes.

## Q4. State machine in the router  Verdict: works

Tests: `test_q4_unknown_stage_and_undefined_transition`, `test_q4_predicates_detect_or_need_the_coders_word`, `test_q4_out_of_stage_call_refused_unknown_tool_clarified_and_state_is_per_connection`.
- `set_stage(to, confirm=false)` with a table `(from, to) -> predicate`. A predicate returns `Outcome(detected, needs_word, why)`. Placeholder predicates read counts of successful tool calls: plan to code needs one `stub`, code to analyse needs one `record_edge`; backward moves and re-plan need the coder's word (`confirm=true`).
- Unknown stage (`review`, empty string): result with `needs_clarification`, the stage list and a question; nothing moves.
- Undefined transition (plan to analyse): `refused`, with the allowed targets. Predicate not met: `refused`, with the reason and a hint. Detected: moves (`via: detected`). Word: moves (`via: word`).
- Out-of-stage tool: `refused`, with the tools of this stage and the stages that have the tool. Unknown tool: `needs_clarification`. These are results, not errors, as in the real server.
- State is per connection (a second connection starts in plan). Whether stage should live per connection, per vault or in a file is WP29's question.
- Prompts and resources have no result form: an out-of-stage prompt or resource can only be a protocol error (clarification is not possible there). Not tested beyond the facade returning an error.

## Q5. Hosting cost

Tests: `test_q5_hosting_cost_separate_processes_vs_one_asgi_app`, `test_q5_failure_modes_one_stage_down_one_stage_blocking_whole_process_gone`, `test_q5_deploy_facts_from_the_repo_files`.

| | (i) 4 processes, 4 ports | (ii) one ASGI app, one port |
|---|---|---|
| processes | 4 (3 stages + router) | 1 |
| listening ports | 4 | 1 |
| startup to a ready router | 1.44 s (started in parallel) | 1.37 s |
| resident memory (ps rss, after use) | 351 MB (84, 88, 87, 101 MB) | 100 MB |
| code (non-blank lines) | hosting-only 13 + shared 10 | hosting-only 17 + shared 10 |
| the router itself | 362 lines (`lc_router.py`), stand-in stages 65 | same |

Failure of one stage server (tested): (i) a killed stage process: the call that was in flight or next returns `stage_server_unavailable` (isError) after 5.01 s (the router's timeout; the SDK client gives no error of its own); other stages keep working; a new connection starts at once (0.15 s) with that stage listed as `down`. (ii) a tool that raises comes back as `isError` and the app goes on; a synchronous blocking tool (1.5 s) in one stage stalled another connection's call for 1.24 s (against 0.013 s in (i)), because all stages share one event loop; a crash or kill of the process ends everything (`ClosedResourceError` on the next call).
Bypass (tested): in (ii) each mounted stage server answers directly at `/stage/<name>/mcp` with no stage check, so whoever can reach the port can skip the state machine. In (i) the same is true for anyone who can reach a stage port, but those ports need not be published. A (ii) that keeps the stage servers off the public app (the router reaching them in memory) has no such mounts and no ports; not measured as a hosting, only for latency (Q6).

What SCAT Chat would need, from the repo files only (nothing deployed):
- Today (`deploy/Dockerfile`, `deploy/scat-chat.sh`, `src/scat_kg/mcp_server/__main__.py`): one image with one ENTRYPOINT (`scat-mcp ... --port 8765`); the launcher publishes `127.0.0.1:8765:8765` only; `tailscale funnel --bg 8765` makes one public https address on 443 that forwards to that one port; the session key goes in with `--env-file /dev/stdin` as `SCAT_MCP_KEY`, and `gated(app, key)` wraps the single ASGI app (header `x-api-key` or Bearer). `start_refusal` demands a key on any non-loopback host. `docs/chat-path.md` has the coder paste one address and one key into the chat's server form (the address ends in `/mcp`).
- (i): public address count unchanged (the router on 8765 is the only published port); key handling unchanged for the router, but the stage servers would have no key unless one is passed to each (they listen only inside the container); the container needs a supervisor of four processes where the Dockerfile has one ENTRYPOINT, and the launcher's liveness check (`/mcp` on the one port) would not see a dead stage server. Ports: three more, container-internal.
- (ii): one process, one port, one public address, one key gate in front of everything: no change to the launcher or the Funnel step; the ENTRYPOINT and the `scat-mcp` command change to build the combined app. The bypass above applies to anyone holding the key, so mounts should not be public.
- Neither changes what the coder pastes into the chat. The chat still sees one server.

## Q6. Does proxying preserve what matters?  Verdict: works

Tests: `test_q6_listing_matches_stage_server_field_by_field`, `test_q6_results_errors_and_progress_are_preserved`, `test_q6_extra_hop_latency_median_of_200`.
- Listing: for each of the three stages, the router's tools (minus its own `stage`, `set_stage`) equal the stage server's listing in every field of the model dump (`name, title, description, inputSchema, outputSchema, annotations, icons, execution, meta`): no diffs. Prompts and resources equal as well.
- Results: for `status`, a good call, an invalid call (missing `target`), `fail_demo` (raises) and `progress_demo`, `content`, `structuredContent` and `isError` are identical to calling the stage server directly (memory).
- Progress: `progress_demo(3)` gives the same three events (1/3, 2/3, 3/3, with messages) through the router; the router re-sends them with the client's progress token.
- Extra hop, median of 200 `status` calls after 10 warm-ups: memory 1.97 ms direct, 3.30 ms via the router; HTTP 5.36 ms direct to a stage server, 10.44 ms via the router (separate ports), 11.06 ms via the router (one port). The router caches each stage's tool list for the connection, so the hop is one upstream call.
- Not known: cost under many connections (each client connection opens one upstream session per stage; 0.15 s to connect with three stages over HTTP); cancellation propagation; large results.

## Not known (needs client trial)

Whether Claude, inference.coop or VS Code Copilot honour `list_changed` (A), or handle a facade tool well and keep per-call approval usable (B); whether a model picks tools better from a short stage list (A), a union (C) or `stage_tools` plus `call` (B). No chat client was used.

## Router vs single stage-scoped server

The single-server column is reasoning only (another worker owns that experiment) and is not tested here.

| | Router over per-stage servers | Single stage-scoped server (reasoned, not tested) |
|---|---|---|
| client support needed | A: `list_changed`. B: none, but an indirect `call`. C: none, long list | the same three choices; `list_changed` or a refusal result; no facade needed |
| routing | proxy per call, plus a state machine, timeouts and isolation of dead upstreams | one registry of tools tagged by stage; a stage check in front of each call |
| hosting cost | 100 MB and 1 port (ii), or 351 MB and 4 ports (i); an entrypoint change either way | as today: one process, one port, one key gate |
| code size | router 362 lines plus hosting 23 to 27 lines (throwaway, stand-ins) | a stage field per tool and one check; the real server's 19 tools stay in one file |
| latency | +1.3 ms memory, +5 ms HTTP | none |
| failure modes | dead stage stalls until timeout; shared loop in (ii); direct stage mounts bypass the state machine; the router must isolate upstream sessions | one process: a tool error is an `isError`; a crash ends everything; no bypass |
| what it gives | stage servers are separate, plain, individually testable | one place to read |
