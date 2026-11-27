# RS5 client trial plan (G4, R3, R3b)

Run by the ACE as coder, with the chief engineer's accounts and keys, against a throwaway spike server. Question per client: **is a mid-session change of tools honoured, and what does the assistant see when it is not?** The coder decides each verdict; the assistant only reports.

## 0. Before you start

Server commands were run with the SDK client on 127.0.0.1; client menu steps and Funnel commands were not run.

**Clients.** Claude (claude.ai or Desktop, custom connector); inference.coop's chat (LibreChat); VS Code GitHub Copilot, agent mode. Note each client's version and the date in the grid's Note column.

**Evidence folder, outside the repo:** `export EV=$HOME/rs5-trial-evidence/$(date +%F); mkdir -p $EV`. Screenshots and logs go only there.

**Key.** One key for the whole sitting, kept in the server terminal's shell only: `export SCAT_MCP_KEY=$(openssl rand -hex 24)`. Copy it with `printf %s "$SCAT_MCP_KEY" | pbcopy`, then copy any word to clear the clipboard. Never type it in a chat or file. Restart servers in this same shell.

**Wrapper.** The spike servers have no start command, key gate or request log (section 7). Save this wrapper as `$EV/serve.py`; it edits nothing in the repo. It serves the single server (`single`) or the router (`a` dynamic, `b` facade, `c` all tools) on 127.0.0.1 behind the repo's key gate, and logs one line per request (never the key).

```python
import os, sys, time
R = os.environ["REPO"]
sys.path[:0] = [R + "/spike/lifecycle/" + d for d in ("single", "router")]
import uvicorn
from scat_kg.mcp_server.gate import gated
mode, key = sys.argv[1], os.environ["SCAT_MCP_KEY"]
if mode == "single":
    import stage_server as S
    app = S.asgi_app(S.build(("header", "query", "path", "session"), is_error=os.environ.get("ISERR") == "1",
                             scoped_list=os.environ.get("SCOPED", "1") == "1"))
else:
    import lc_hosting as H
    from contextlib import asynccontextmanager
    from lc_router import Router, memory_connector
    from lc_stages import STAGES, build_stage
    from starlette.applications import Starlette
    routes, mgr = H.router_routes(Router(memory_connector({n: build_stage(n) for n in STAGES}),
                                         {"a": "dynamic", "b": "facade", "c": "all"}[mode]))
    @asynccontextmanager
    async def life(_):
        async with mgr.run():
            yield
    app = Starlette(routes=routes, lifespan=life)
def logged(inner):
    async def run(scope, receive, send):
        if scope["type"] == "http":
            h = {k.decode(): v.decode() for k, v in scope["headers"]}
            print(time.strftime("%H:%M:%S"), scope["method"], scope["path"], scope["query_string"].decode() or "-",
                  "x-scat-stage=" + h.get("x-scat-stage", "-"), "session=" + h.get("mcp-session-id", "-")[:8], flush=True)
        await inner(scope, receive, send)
    return run
uvicorn.run(logged(gated(app, key)), host="127.0.0.1", port=8791, log_level="warning")
```

**Start** (from the repo checkout, after `uv sync --frozen --extra mcp`), one server at a time, logging to the evidence folder:

```
cd <your checkout of spike/lifecycle>; export REPO=$PWD
uv run --frozen --extra mcp python $EV/serve.py single 2>&1 | tee $EV/server.log
```

Prefix `SCOPED=0` or `ISERR=1` where a run says so; for the router replace `single` with `a`, `b` or `c`. **Smoke check** (other terminal): `curl -s -o /dev/null -w "%{http_code}\n" -X POST http://127.0.0.1:8791/mcp` prints 401. **Read the log**: `grep '^[0-9][0-9]:' $EV/server.log` gives time, method, path, query, `x-scat-stage` as received, session prefix; other lines are noise.

**Exposure.** Claude and inference.coop call the server from their cloud, so port 8791 needs a public https address. VS Code is local and needs none. Use only the existing approved route (`research/chat-path/readout.md`, `docs/chat-path.md`): Tailscale Funnel to this port, short-lived, key-gated by the wrapper, torn down in section 5. The ACE decides how; this plan exposes nothing. The connector address is the https address plus `/mcp`.

**Run order** (one server at a time; same address and key throughout; new conversation after each change of run):

| Run | Start | Tests |
|---|---|---|
| A | `single` | T1 T2 T5 T6 T7 |
| B | `SCOPED=0 single` (all tools listed) | T3 T4 T9 |
| C | `SCOPED=0 ISERR=1 single` | T4 (error variant) |
| D, E, F | router `a`, `b`, `c` | T8 T10 |

**Connector entries** (add as needed): `spike` (address `/mcp`, key header); `spike-hdr` (same, plus header `x-scat-stage: code`); `spike-q` (`/mcp?stage=analyse`); `spike-p` (`/mcp/plan`).
- Claude: Plugins, Add, Add custom connector; "No sign-in"; Request headers `x-api-key` = key. A connector cannot be edited: remove and re-add.
- inference.coop: MCP Settings, Add; Streamable HTTPS; API key, Bearer; tick the consent; Connect; add it as an agent tool in Agent Builder if needed.
- VS Code: command "MCP: Open User Configuration", then:
  `{"servers":{"spike":{"type":"http","url":"http://127.0.0.1:8791/mcp","headers":{"x-api-key":"${input:k}"}}},"inputs":[{"id":"k","type":"promptString","password":true}]}`. VS Code asks for the key at start. `spike-hdr` adds `"x-scat-stage":"code"` to headers; `spike-q`, `spike-p` change the URL. The picker is "Configure Tools" in Copilot Chat.

**Human pace (inference.coop is a small co-op).** One conversation at a time, one tab, no regenerating, no parallel or batch use, 30 seconds or more between messages, short outputs, one client at a time. Message budget, every message counted: **Claude 40; inference.coop 35; VS Code 40**. At the budget stop and record "not run".

**Screenshots** (`$EV/<client>-T<n>-<what>.png`): connector form with header names (key empty); the tool list or picker at T1, T2 before and after, T8 (each run), T10; each refusal, clarification, approval or elicitation prompt, and error banner. Never one showing the key.

## 1. Tests

Run each test once per client. "Ask": send exactly the quoted text. Read the reply and the tool list; record the verdict (works / partly / does not) in the grid. "Result:" is the box to fill in.

**T1 connect and list tools (run A, entry `spike`).** Open a new conversation with the connector on.
Ask: `List every tool you have from the spike server, by name, and nothing else.`
Look for: exactly `set_stage`, `which_stage`, `ask_stage` (stage unknown, so only the always-on tools).

Outcomes (observed = verdict): Those three, in reply and picker = works; Three in one place, other in the other = partly; Connect fails, or no tools = does not (record the message).

Result: ______

**T2 stage change by tool call, then list_changed (run A, `spike`).** Same conversation as T1.
Ask 1: `Call set_stage with stage "code" and coder_word "ace". Report the result.`
Ask 2: `Without calling any tool, list the tool names you have now.`
Ask 3: `Call which_stage and report it.`
Look for: after Ask 2, `status check stub record_edge set_status` plus the three always-on tools. Check the picker. If the list is unchanged, Ask 4: `Call stub with name "x" and type "node".` and note the reply. Then open a new conversation; Ask: `Call which_stage, then list your tools.` Stage `code` there means the session persisted; the list shows what the client re-fetched.

Outcomes (observed = verdict): Assistant and picker both show the code tools in the same conversation = works; Only the assistant, or only the picker, or only in a new conversation = partly (say which); Never changes = does not.

Result: ______

**T3 out-of-stage call from a stale list (run B, `spike`).** This run lists all tools at every stage, so every client holds out-of-stage tools.
Ask 1: `Call set_stage with stage "plan" and coder_word "ace".`
Ask 2: `Call record_edge with no arguments. Quote the full text of the result you receive.`
Look for: result text beginning "`record_edge` is not available at stage `plan`; it is available at: code", naming the stages and saying the coder decides. Note whether the client marks the call failed.

Outcomes (observed = verdict): assistant quotes the refusal and defers to the coder = works; sees it but ignores it or retries blindly = partly; text hidden or generic error = does not.

Result: ______

**T4 unknown stage, clarification result (run B, then run C).** New conversation each run; do not call set_stage.
Ask: `Call status with no arguments. Quote the full text of the result.`
Look for: "No stage was supplied. Known stages: ...". Run B returns a normal result; run C (restart with `SCOPED=0 ISERR=1`) returns `isError: true`. Record for each: what the assistant says, whether you see the text or only a failure marker, and whether it asks you which stage.

Outcomes (observed = verdict): relays the text and asks the coder in B and C = works; B only, or a bare error shown in C = partly; text unseen or a stage invented = does not.

Result B: ______  Result C: ______

**T5 custom header (run A, entry `spike-hdr`).** Try to add the header `x-scat-stage` with value `code`, next to the key header.
Look for: whether the form accepts the name. Then, new conversation, Ask: `Call which_stage and report the result exactly.` Expect `carrier: header`, `stage: code`, and log lines with `x-scat-stage=code`. Ask: `Call set_stage with stage "plan" and coder_word "ace", then which_stage.` The header still wins (carrier order). If the form refuses the name or has no room, record what it offered.

Outcomes (observed = verdict): log and `which_stage` show it on every request = works; accepted but not on every request = partly; not accepted = does not.

Result: ______

**T6 query and path fallbacks (run A, entries `spike-q`, `spike-p`).** New conversation each.
Ask: `Call which_stage and report the result exactly, then list your tools.`
Look for: `spike-q`: `carrier: query`, `stage: analyse`, tools `status check fingerprint layered trace export_edges` plus the three; `spike-p`: `carrier: path`, `stage: plan`, tools `status check stub` plus the three.

Outcomes (observed = verdict): both work = works; one = partly; neither = does not.

Result q: ______  Result p: ______

**T7 elicitation (run A, `spike`).** New conversation; leave the stage unknown.
Ask: `Call ask_stage.`
Look for: a prompt to you listing plan, code, analyse (answer "code"), then `elicited: true` in the reply. Without support: `elicited: false`.

Outcomes (observed = verdict): Prompt shown, answer returned = works; prompt shown, answer lost = partly; `elicited: false` = does not.

Result: ______

**T8 the router (runs D, E, F; entry `spike`).** One new conversation per run. Router stages start at `plan`; plan to code needs one successful `stub` first.
Run D (dynamic, A), Ask 1: `List your tools from the spike server.` Ask 2: `Call stub with name "x" and type "node", then call set_stage with to "code".` Ask 3: `List your tools again.` Look for: before `stage set_stage status check stub`; after `stage set_stage status check set_status record_edge fingerprint progress_demo fail_demo block`.
Run E (facade, B), Ask 1: `Call stage_tools and report it.` Ask 2: `Use the call tool to run status with args {}.` Look for: only `stage set_stage stage_tools call` listed, no list change; whether `call` works; whether approval covers `call` once for all stage tools.
Run F (all tools, C), Ask 1: `List your tools.` Ask 2: `Call record_edge with source "a" and target "b".` Look for: 14 tools; the refusal quoted (as T3). In every run note approval prompts: per call, per tool or once.

Outcomes (observed = verdict): D follows the stage, E's `call` works, F refuses cleanly = works; one of these fails = partly; router does not connect = does not.

Result D: ______  Result E: ______  Result F: ______

**T9 session loss (run B, `spike`).** In a conversation where you called `which_stage` once, stop the server (Ctrl-C), restart it with the same command and shell, then wait 10 seconds.
Ask: `Call which_stage again and report exactly what happens.`
Look for: reconnect without help, or an error such as "Session terminated". Then Ask: `Call which_stage once more.` Note whether you must reconnect the connector or start a new conversation.

Outcomes (observed = verdict): next call works unaided = works; only after reconnecting or a new conversation = partly; stays broken = does not.

Result: ______

**T10 tool count and cap (from T1, run A, T8 run F).** Count the tools in the picker (expected: 3 in T1; 8 after T2; 14 in run F) and note any limit, truncation or "too many tools" text. A cap above 14 cannot be tested (section 7).
Result: ______

## 2. Where clients differ

T5: Claude offers approved header names only (beta, may be absent); inference.coop's form may have one header slot (the key); VS Code takes any. T7: documented for VS Code; unknown for Claude; none seen in LibreChat code. Where a client lacks what a test needs, record what it offers and mark "does not apply".

## 3. Results grid (fill after each client)

| Test | Claude | inference.coop | VS Code | Note |
|---|---|---|---|---|
| T1 list | | | | |
| T2 list_changed | | | | |
| T3 stale call | | | | |
| T4 unknown stage (normal / isError) | | | | |
| T5 header | | | | |
| T6 query / path | | | | |
| T7 elicitation | | | | |
| T8 D / E / F | | | | |
| T9 session loss | | | | |
| T10 count, cap | | | | |

## 4. What each result decides for WP29

- **T2 (R3).** Works: a stage-scoped server may rely on `list_changed` in that client. Partly or does not: keep the list stable and let the refusal carry it (T3). The readout reports it per client.
- **T3, T4.** Works: the assistant relays the refusal or clarification, so WP29 may rest "ask the coder for stage" on it. If `isError` (run C) is hidden or alarming, WP29 uses the normal result.
- **T5, T6.** Works: stage may ride in a static header or URL, one stage per connector entry. Neither: a session value or an argument.
- **T7.** Works means elicitation may be a bonus path; it is never the only one.
- **T8, T10 (R3b).** D behaves as T2: the router gives no client-side gain over a single server. D fails and E works: the facade is that client's only option, at E's approval and typing cost. F is the baseline. Hosting cost is already measured; this adds the client side.
- **T9.** Decides whether a session-held stage is safe, or must survive a restart.

## 5. Safety and tear-down

The key is the chief engineer's: never in the repo, a chat, a screenshot or the log. Nothing is public except the short-lived, key-gated route.
1. Stop the server (Ctrl-C). 2. Funnel off: `tailscale funnel --https=443 off`, then `tailscale funnel reset`; confirm `tailscale funnel status` shows no address. 3. Remove the `spike*` entries in Claude (Plugins, three dots, Remove), inference.coop (MCP Settings; delete the entry and any agent tool) and VS Code (`mcp.json`). 4. Clear the clipboard; `unset SCAT_MCP_KEY`. 5. Check `git status` in the repo is clean. 

## 6. Time estimate

Setup 30 minutes; Claude 90, inference.coop 120, VS Code 60; tear-down 15: about 5.5 hours, one client per sitting.

## 7. Spike server gaps (for the PM; nothing was edited)

- No start command or key gate: the single server has a test helper only; `lc_hosting.py` has no gate and mounts stage servers on the public app. The wrapper fills both (it borrows `scat_kg.mcp_server.gate`; the router runs on in-memory stage servers).
- No header or request log: the wrapper adds one. Inside the server, only `which_stage` reports the carrier.
- The router has no header, query, path stage or elicitation: T5 to T7 apply to the single server only.
- No hook to pad the tool list: a cap above 14 is untestable (T10).
