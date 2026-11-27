# RS5-G2: raw material for the lifecycle model (nothing is chosen here)

Worktree `rs5-u2`, 27 Nov 2026. Counts verified by listing from the code (`build(...).list_tools()/list_prompts()/list_resources()`): **19 tools, 6 prompts, 1 resource** (`src/scat_kg/mcp_server/server.py`). Paths are relative to the worktree unless `ace-org/` is named. Words follow GLOSSARY.md; "stage" is used loosely for any candidate state, and every grouping below is an offer, not a pick.

## Findings first

1. The sources already carry **five groupings** that cut the same journey differently (table 1). None is marked as the model. They nest: the coder's loop sits inside flow step 8, and a narrative's status (stub, draft, done) is a third, per-page cycle.
2. **Flow steps and journeys J1 to J10 are the same ten names in the same order** (flow.md:15-24; `ace-org/MISSION.md:418-433`). The choice is not between them, but between them and the finer or coarser groupings.
3. **The server is only useful from Set up onward and serves one vault.** Discover, Decide, Set terms and Capture have no tool; Plan has only `check`. Most of the 19 tools cluster in Code and Analyse.
4. **Two predicates the sources lean on have no tool**: the stakeholder-group cap (no tool reads `scat.toml`; run record leave-no-trace-run.md:19) and "the coder says the model is finished" (`ace-org/MISSION.md:85`, "A finished model"; flow.md:22). See g5.
5. **Backward moves are the coder's act, not a tool's.** Done to draft is refused by the server (`set_status`, server.py:53-76) and by `record_edge`/`remove_edge` on a `done` narrative (run on a copy, g5). Analyse to Code is "reading can send the coder back" (flow.md:21).

## 1. Candidate stages and groupings

Actor key: org = organiser; coder; setup = whoever set the tools up (D-159, `ace-org/decisions/log.md:2837`); asst = assistant (no authority); tool.

| Id | Grouping and candidate | Actor | Comes from |
|---|---|---|---|
| G-A | **Flow / journey, ten steps**: 1 Discover, 2 Try, 3 Decide, 4 Set terms, 5 Set up, 6 Plan, 7 Capture, 8 Code, 9 Analyse, 10 Hand over | org (1-7), coder (8-10), asst optional in 8-9 | flow.md:15-24; `ace-org/MISSION.md:418-433` |
| G-A' | Same ten, solo order 5, 2, 8 (no 4, no 7) | org alone | flow.md:7 |
| G-B | **Coder's loop**: interpreting, authoring, coding, reviewing; then analysing | coder owns; asst helps; tool checks | coding.md:116-123; analysis (flow.md:21); `ace-org/MISSION.md:79`; chat-path.md:412-432 (steps 99-107); prompt `code-a-narrative` steps 1-4 (prompts.py:25) |
| G-B' | Loop with Analyse as the fifth activity ("support: call tools that draw, help interpret, revisit the coded data") | coder, asst | D-160 (`ace-org/decisions/log.md:2848`) |
| G-C | **Page status cycle**: stub, draft, done; and done back to draft | coder sets done; tool/asst may set stub, draft | norms.md:77-84; coding.md:355-430; server.py:53 |
| G-D | **SCAT Chat session**: install once, start, connect, skill and agent, use, stop, clean up | org/setup | chat-path.md headings 166-513; leave-no-trace-run.md:13-23 |
| G-E | **Assistant modes** (sub-activities): code a narrative, explain a problem, review before done, draft a node page, sweep stub node pages, look for duplicates, end of session | asst for coder | prompts.py:25-104; SKILL.md:85-131 |
| G-F | **Finished model** as a condition, not a step: conformant graph, vault navigable, views generated, coder's statement | coder | `ace-org/MISSION.md:85-92`; flow.md:22 |

Alternatives the sources support, offered not chosen: (a) one vault-level machine of ten (G-A) with G-B/G-C as per-narrative sub-machines; (b) a flat machine of G-B's five activities, with Set up and Plan as pre-stages; (c) G-A with Code and Analyse each split by G-E modes (node pages and duplicates as their own stage); (d) G-C only, with stage a property of a page. Which unit carries the stage (vault, narrative, session) is open: status is stored per page only (status counts: `{'stub','draft','done','other'}`, g5).

## 2. Per candidate: inputs, outputs, tools, prompts, skill

Candidates are G-A's steps with Code split by G-B and the node-page work of G-E shown apart. Inputs and outputs are what the sources name; "(inferred)" marks mine.

| Candidate | Inputs | Outputs | Tools | Prompts / resource | Skill and doc sections |
|---|---|---|---|---|---|
| 1 Discover | nothing | interest | none | none | index.md |
| 2 Try | own notes, a vault set up | one coded narrative, its fingerprint, `done` | `stub`, `record_edge`, `fingerprint`, `check`, `set_status` (via CLI, solo path) | none | getting-started.md:209 |
| 3 Decide | the trial | a go decision | none | none | flow.md |
| 4 Set terms | nine choices | answers, attribution mode, AI answer, storage | none | none | data-and-consent.md:22,52; planning.md "Choose the attribution mode" |
| 5 Set up | template repo, tool install | vault with `scat.toml` (cap, attribution), clean check | `check` (first run) | none | getting-started.md:67-208; ide.md; chat-path.md; ide-run.md:11 |
| 6 Plan | steps 4 and 5 | `plan.txt` (not read by the check), groups within cap, mode | `check` ("Check the vault passes", planning.md:101) | none | planning.md |
| 7 Capture | terms, plan | plain-text field notes | none | none | narratives.md, facilitate-*.md |
| 8a Interpreting | field notes (later the views) | the coder's decision; asst questions | `status` (inferred) | `code-a-narrative` step 1; resource | SKILL.md:8-29, "One step per reply" 85 |
| 8b Authoring | interpretation | account on a narrative page (the coder pastes, A8) | `stub` (page), `set_status` stub/draft | `code-a-narrative` step 2 | SKILL.md A1, A8 |
| 8c Coding | account | links, stub node pages, one row per edge | `stub`, `stub_links`, `record_edge`, `remove_edge` | `code-a-narrative` step 3 | SKILL.md:65-83 (edges, kind) |
| 8d Reviewing | coded page | check result, fingerprint with candidates, `done` (coder) | `check`, `status`, `fingerprint`, `set_status` (refuses `done`) | `review-before-done`, `explain-a-problem`, `code-a-narrative` step 4 | SKILL.md "Offering a description" 90; norms.md "What done needs" |
| 8e Node pages | evidence for a node | node page text (coder writes in) | `evidence`, `copy_share`, `status` | `draft-a-node-page`, `fill-in-node-pages`; resource | SKILL.md:95-112 |
| 8f Duplicates | `review` output | merge (coder runs `scat merge`) or split | `review`, `merge` (plan only), `split_plan`, `check` | `look-for-duplicates`; resource | SKILL.md:114-125 |
| 9 Analyse | conformant vault, coder's allowed uses | views read; a revisit list | `fingerprint`, `edge_table`, `layered`, `trace`, `evidence`, `copy_share`, `review`, `attribution`, `export_edges` | none (D-160 wants drawing and interpretation) | analysis.md:7-25, 49-59 |
| 10 Hand over | steps 8, 9, release answers | clean check, indexes, commit, push, tag | `check`, `index`, `export_edges` (inferred) | none | coding.md:962-1000; flow.md:22 |

## 3. Tool-to-stage matrix

x = the sources place the call there (basis column); (x) = inferred from tool description only. Columns: S5 Set up, S6 Plan, 8a-8d loop, 8e node pages, 8f duplicates, S9 Analyse, S10 Hand over.

| Item | S5 | S6 | 8a | 8b | 8c | 8d | 8e | 8f | S9 | S10 | Basis |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T `check` (server.py:36) | x | x | | | | x | | x | x | x | getting-started.md:90; planning.md; prompts.py:25-37,91-103; analysis.md:11; coding.md:966 |
| T `status` (44) | | | (x) | | | x | x | | | (x) | prompts.py:49, 76; SKILL.md:110 |
| T `set_status` (53) | | | | x | | x | | | | | refuses `done`; SKILL.md:129 |
| T `stub` (84) | | | | x | x | | | | | | SKILL.md A3; prompts.py:25 |
| T `stub_links` (92) | | | | | x | | | | | | prompts.py:25 |
| T `record_edge` (101) | | | | | x | | | | | | SKILL.md A9 |
| T `remove_edge` (112) | | | | | x | | | | x (revisit) | | skill A3; D-160 |
| T `merge` plan (124) | | | | | | | | x | | | SKILL.md A18 |
| T `split_plan` (148) | | | | | | | | x | | | SKILL.md A18 |
| T `index` (159) | | | | | | | | | | x | flow.md:22 |
| T `fingerprint` (168) | | | | | | x | | | x | | prompts.py:49; analysis.md:13 |
| T `edge_table` (176) | | | | | | | | | x | | analysis.md |
| T `layered` (184) | | | | | | | | | x | | analysis.md |
| T `trace` (192) | | | | | | | | | x | | analysis.md |
| T `evidence` (202) | | | | | | | x | x | x | | prompts.py:62,91 |
| T `copy_share` (211) | | | | | | | x | | x | | prompts.py:62,76 |
| T `review` (221) | | | | | | | | x | x | | prompts.py:91; analysis.md:25 |
| T `attribution` (230) | | | | | | | | | (x) | | not named in analysis.md; refused in `disallowed` |
| T `export_edges` (239) | | | | | | | | | x | (x) | chat-path.md:434 |
| P `code-a-narrative` (262) | | | x | x | x | x | | | | | prompts.py:25 |
| P `explain-a-problem` (269) | | | | | | x | | | | | prompts.py:39 (any stage with a problem, inferred) |
| P `review-before-done` (276) | | | | | | x | | | | | prompts.py:49 |
| P `draft-a-node-page` (283) | | | | | | | x | | | | prompts.py:62 |
| P `fill-in-node-pages` (290) | | | | | | | x | | | | prompts.py:76 |
| P `look-for-duplicates` (297) | | | | | | | | x | | | prompts.py:91 |
| R `scat://assistant-rules` (304) | | | x | x | x | x | x | x | (x) | | text embedded in 4 prompts (prompts.py:25,62,76,91); not in `explain-a-problem` or `review-before-done` |

**Shared across stages:** `check` (7 columns) and `status`, then `evidence`. `check` and `status` read the whole vault, a page, or a page plus neighbours (`neighborhood`). Every result carries `mode` (server.py:27, `stamp`).

## 4. Transitions

Who decides: **tool** = a call returns the evidence; **coder** = only the coder's word; **either** = tool can show it, coder confirms.

| Id | From to | Dir | Trigger | Decides | Source |
|---|---|---|---|---|---|
| T1 | 1 to 2 to 3 | fwd | interest; trial done | coder/org | flow.md:15-17 |
| T2 | 3 to 4 to 5 to 6 to 7 | fwd | each step's "Depends on" | org | flow.md:18-22 |
| T3 | 5 to 2 to 8 (solo) | fwd | no participants, so no 4 or 7 | org | flow.md:7 |
| T4 | 7 to 8a | fwd | field notes exist | org (no tool) | flow.md:22 |
| T5 | 8a to 8b to 8c to 8d | fwd | each step handed back to the coder | coder | prompts.py:25-37; SKILL.md:85 |
| T6 | 8d to 8a/8b/8c | back | check reports a problem; coder doubts account or coding | either | coding.md:118-123 |
| T7 | stub to draft | fwd | coder or asst sets it | either (`set_status`) | norms.md:77 |
| T8 | stub to done | fwd | allowed in one sitting | coder | norms.md:82 |
| T9 | draft to done | fwd | check passes and coder confirms both | coder; tool refuses with SCAT-DONE-REFUSED | coding.md:355-370 |
| T10 | done to draft | back | coder reopens to edit | coder in Obsidian; server refuses | server.py:68-76; coding.md:389 |
| T11 | 8d to 9 | fwd | clean check, content signed off | either | analysis.md:11-13 |
| T12 | 9 to 8 | back | reading the views sends the coder to notes or pages | coder | flow.md:21; `ace-org/MISSION.md:426` (J9) |
| T13 | 9 to 8a, revisit list | back | assistant interprets the images, hands back | coder | D-160 |
| T14 | 8 to 6 | back | stakeholder-group cap refuses a new group; raise it or link an existing group | tool refuses on `stub`; setup decides | planning.md "Groups and the cap"; leave-no-trace-run.md:19; D-159 |
| T15 | 8 to 6/4 | back | attribution mode changed; pages flag | coder | planning.md "Choose the attribution mode" |
| T16 | 8, 9 to 10 | fwd | clean check, views, commit, push | tool shows check; coder says | flow.md:22 |
| T17 | 10 to 8 | back | work continues after a hand-over, toward the next | coder | `ace-org/MISSION.md:427` (J10) |
| T18 | 10 to follow-through | fwd | commitments to participants | org | flow.md:24 |
| T19 | 8c to 8e/8f | lateral | a node needs a page, or two pages may be one | either (`review`) | SKILL.md:95,114 |
| T20 | G-D session | fwd | start, connect, use, stop, clean up | org/setup | chat-path.md:253-513 |

Inferred, not sourced: 8 to 7 (more field notes needed) and 9 to 7. The sources say "back to the field notes" (coding.md:121) but name no step.

## 5. Conflicts and gaps

1. **No stage is stored.** Status is per page; nothing records the vault's stage. A server needing stage must derive it (g5) or be told.
2. **Unit conflict.** Flow is the organiser's journey (one vault); the loop is per narrative; `done` is per page. The sources use "stage" at all three.
3. **Order conflict.** J2 Try is numbered before J5 Set up but depends on it (flow.md:15,19; the "First try" order 5, 2, 8, flow.md:7).
4. **Node-page and duplicate work** (`evidence`, `copy_share`, `review`, `merge`, `split_plan`) is "views" in analysis.md:25 but loop work in coding.md:129 and in skill A16-A20. No stage owns it.
5. **`attribution`** appears in no guide's list of views; **`export_edges`** is placed under views in chat-path.md:434 but "views generated" in flow is also met by on-demand views.
6. **`index`**: flow step 10 lists `scat index`; the template ships all five and `merge` runs it, so it does little at hand-over (coding.md:903).
7. **No tool for**: reading or writing `scat.toml`; set-up (install, `uv sync`); commit, push, tag; terms and consent; field-notes intake; drawings (no tool returns an image, WP28-WP31-inputs.md:14; D-160). Stages with no tool: 1, 3, 4, 7.
8. **Assistant behaviour vs stage.** Probes (WP28-WP31-inputs.md:23-36; only the summary is in the repository, the P and V logs are outside it): it listed nodes before an account was drafted (against the 8b to 8c order), recorded unconfirmed edges (P1, a coder decision), ruled on a duplicate without `review` (P6), misreported statuses and the cap (P6, P8, V3), did not know `mode` (P7; chatbot-run.md:21), and drew Mermaid itself (V1, V2). These are the failures a stage scope would target.
9. **Skill coverage.** One skill in `skills/`, `scat-coding`; the IDE run also read a setup skill and `AGENTS.md` from the template (ide-run.md:11), not in this worktree. Sections for stages 5 to 7, 9 (beyond views) and 10 do not exist.
10. **Resource**: `assistant-rules` text is inside four prompts, not the other two.

## Where alternatives were offered

Section 1 (G-A to G-F and alternatives a to d), section 2 intro ("Code split by G-B and G-E" is one of several), section 3 (columns follow G-A plus G-B/G-E, one option), section 4 (T19, T20 lateral and session-level), section 5 items 1, 2, 4. No stage model is recommended.
