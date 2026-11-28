# WP38 cleanup ledger

Part 1 says what became of every word; part 2 says what became of the 41 inconsistencies. The glossary is
`glossary.yml`; `GLOSSARY.md` and `docs/reference/terms.md` are generated from it (`python3 scripts/glossary.py`).

## Part 1. The words

The glossary now has 53 entries: core 22, plan 7, capture 5, code 12, analyse 6, report 1. Sections are `core` (words
met across the work) and the stages of `contracts/lifecycle.md`, each holding the words first met in that stage's
work. The terms page has 854 words; the test's cap is 940 (854 plus 10%, rounded up), below the old 960.

Counting rule for added words (WP38 default): pages among `docs/*.md` and `docs/reference/*.md` (22 files) other
than `docs/reference/terms.md`, case-insensitive and word-bounded, as RS6 did; 6 or more pages keeps a word.

### Today's 59 words

GLOSSARY.md on `dev` had 55 rows, which hold 61 words once "coded, uncoded", "coder, assistant, tool", "inputs, model,
analysis" and "rule, norm" are split (RS6 counted 59 because it missed `stage` and `transition`, which WP29 added,
and listed `model` twice). Every one of the 61 is here.

| Word | Disposition | Section | Reason |
|---|---|---|---|
| SCAT | kept | core | R2 word. |
| node | kept | core | R2 word. Absorbs "node page" (10 pages). |
| edge | kept | core | R2 word. Absorbs the edge-type spellings: its first sentence names `holds`, `is addressed by`, `is provided by`. |
| element | moved to docs/architecture.md | | RS6: redundant, unused in the docs; an assistant and builder word. |
| layer | kept | core | R2 word. |
| layered graph | moved to docs/architecture.md | | Builder word; RS6: 3 pages or fewer. |
| knowledge graph | moved to docs/architecture.md | | The ABox the tool builds; a builder word. The organiser meets the vault, the page and the view. |
| narrative | kept | core | R2 word. Its second sentence carries what "coded" and "excluded" said (a narrative that links no node page is left out of the views and reported). |
| coded | folded into narrative | | Not R2; the word is retired, the sense is "links a node page". |
| uncoded | folded into narrative | | As "coded". |
| excluded | dropped | | Not R2; the behaviour is in the narrative entry, and the tool's report says it. |
| timeframe | kept | capture | R2 word; the facilitating guide asks it (`facilitate-timeframe.md`). |
| scenario | kept | capture | R2 word; first met in the scenario session guide. |
| architecture | kept | capture | R2 word; first met in the architecture session guide. |
| fingerprint | kept | analyse | R2 word; a view. |
| edge table | kept | analyse | R2 word; a view. |
| layered view | kept | analyse | R2 word; a view. |
| trace | kept | analyse | R2 word; a view. |
| view | kept | analyse | R2 word. |
| relationship annotation | moved to contracts/page-contracts.md | | Not R2; a page-contract detail, in no view. |
| type | kept | core | R2 word. |
| the ontology | moved to docs/architecture.md | | Assistant and builder word; definitions say "the rules" instead. |
| entry | moved to docs/architecture.md | | Builder word (RS6: materially different on the terms page). Definitions say "page". |
| model | moved to docs/architecture.md | | Four senses (RS6 I3); the architecture page keeps the one it needs. |
| conformant | folded into check | | Not R2; "a clean check" and "the check passes" say it. |
| vault | kept | core | R2 word. |
| page | kept | core | R2 word. |
| field | kept | core | R2 word. |
| Edges told | kept | code | R2 word; the test needs the heading. |
| link | kept | code | R2 word; a link is never an edge. |
| cap | kept | plan | R2 word. |
| attribution mode | kept | plan | R2 word. |
| attribution | kept | code | R2 word. |
| contributor page | kept | code | R2 word. |
| index page | kept | report | R2 word; the report stage's output. |
| status | kept | core | R2 word. |
| stage | kept | core | WP38 scope: stage word from WP29. |
| transition | kept | core | WP38 scope: stage word from WP29. |
| mismatch | kept | code | The nine mutation tests of `tests/docs/test_terms.py` need `mismatch` on the terms page (and RS6 found it on 2 pages), so it stays although it is not R2. |
| organiser | folded into coder | | Not R2. The coder entry says the organiser, who runs the elicitation, may also be the coder. Flagged: see "Flagged". |
| coder | kept | core | R2 word; owns interpretation. |
| assistant | kept | core | R2 word; helps, holds no authority. |
| tool | kept | core | R2 word; owns conformance. |
| inputs | moved to docs/architecture.md | | Not R2; RS6 I2 (material kinds disagree). |
| model (the material) | moved to docs/architecture.md | | As "model" above. |
| analysis | moved to docs/architecture.md | | Not R2; four senses (RS6 I4). |
| field notes | kept | capture | R2 word; gathered in capture. |
| interpreting | folded into coding | | Not R2; a step of the coding loop, named in the coding entry. |
| authoring | folded into coding | | As "interpreting". |
| coding | kept | code | R2 word. |
| reviewing | kept | code | R2 word. |
| the coding loop | folded into coding | | Not R2; the coding entry names the loop's four steps. |
| analysing | dropped | | RS6: unused in docs, template, CLI help, MCP text, skills. |
| a finished model | dropped | | RS6: on 1 page; the report stage covers the hand-over. |
| rule | kept | code | R2 word. |
| norm | moved to docs/architecture.md | | Not R2; guidance for the assistant. |
| skill | moved to docs/architecture.md | | Assistant word. |
| saved agent | moved to docs/architecture.md | | Assistant word; RS6: on 2 pages. |
| session key | moved to docs/architecture.md | | Assistant and builder word; RS6: on 2 pages. |
| leave no trace | dropped | | Not R2; `docs/leave-no-trace.md` defines it where it is used. |
| range vault | moved to docs/architecture.md | | A test fixture; RS6 class ASST. |

### Added words

| Word | Disposition | Section | Reason |
|---|---|---|---|
| session | kept | plan | (d), 17 pages. One sense: a facilitated event. "Start" and "Stop" are not folded in (see below); a chat run is named "a chat run". |
| account | kept | code | (d), 19 pages. Ruling: the narrative's prose, with a link wherever it names a node; no list of links beyond the text (D-205). Absorbs "account text". |
| group | kept | core | (d), 16 pages. |
| concern | kept | core | (d), 15 pages. |
| affordance | kept | core | (d), 13 pages. |
| technology | kept | core | (d), 12 pages. |
| check | kept | core | (d), 21 pages. One entry for the command and the gate; absorbs "clean" (11 pages) and "conformant". |
| clean | folded into check | | (d), 11 pages; "a clean check has no errors" is simpler than an entry. |
| refused | kept | core | (d), 13 pages. |
| coding path | kept | plan | (d), 6 pages. |
| problem | kept | core | (d), 12 pages. Absorbs "error" (10) and "warning" (7). |
| participant | kept | plan | (d), 8 pages. Anyone who takes part in the elicitation. |
| contributor | kept | code | (d), 10 pages. Ruling: a participant whose name a narrative is attributed to; two entries, the simpler. |
| facilitating | kept | capture | (d), 10 pages. |
| node page | folded into node | | (d), 10 pages; "its page is a node page" in the node entry. |
| consent | kept | plan | (d), 10 pages. |
| MCP server | kept | plan | (d), 6 pages; set up with the coding path. |
| Start and Stop | dropped | | (d), 4 and 2 pages (case-sensitive), under 6 pages. Not folded into `session`: the ruling gives `session` one sense. |
| edge type (holds, is addressed by, is provided by) | folded into edge | | (d), 17, 6 and 5 pages; the three verbs are in the edge entry's first sentence, as the test needs. |
| evidence | kept | analyse | (d), 7 pages; a view. |
| REPL | kept | code | (d), 6 pages. |
| mismatch | kept | code | WP38 scope (c); see the first table. |

### The five candidate words (C19)

| Word | Pages | Decision |
|---|---|---|
| orphan | 4 | Not an entry (under 6). |
| plot | 2 | Not an entry (under 6). |
| query result | 1 | Not an entry (under 6). |
| candidate | 7 | Entry, section `code`: two nodes a narrative links that have no row in its `Edges told` table. |
| account text | 3 | Not an entry (under 6); the sense is covered by `account`. |

### Words the moved words need

Placed in unit U2: the first nine and the four assistant words in `docs/architecture.md` (section "Words this page uses"), relationship annotation in `contracts/page-contracts.md` section 7. The four assistant words were first put in `contracts/assistant.md`, but `skills/scat-coding/SKILL.md` copies that file's body verbatim under a test and `skills/` is outside this package's blast radius, so the PM moved them to the architecture page.

| Word | Where | One-line definition |
|---|---|---|
| element | docs/architecture.md | A node or an edge. |
| layered graph | docs/architecture.md | The nodes and edges only, in their four layers: the knowledge graph without narratives and relationship annotations. |
| knowledge graph | docs/architecture.md | The nodes, edges and narratives the tool builds from a vault and checks against the ontology, with the contributor pages where the attribution mode allows them. |
| the ontology | docs/architecture.md | The project's fixed definitions of the types and their rules, which the tool checks against; the TBox, in Turtle. |
| entry | docs/architecture.md | One node, edge, narrative or relationship annotation as stored in the vault: a page, a table row or a body line. |
| model | docs/architecture.md | The ontology plus a conformant vault; also, as a kind of material, the git repository that holds them. |
| inputs | docs/architecture.md | The field notes: the supplied material. |
| analysis | docs/architecture.md | The reports derived from the model; also the step that reads the views. |
| range vault | docs/architecture.md | A vault that rebuilds a published case with groups, not named people, to test the tools; it is not field data. |
| relationship annotation | contracts/page-contracts.md | A free-text remark between two entries of the same type, written as a body line with a link; not an edge, in no view. |
| norm | docs/architecture.md | Guidance to coders and assistants, the same for a person as for an LLM, carried in the docs and skill files; the tool does not enforce it. |
| skill | docs/architecture.md | A package of instructions that an assistant loads and follows; the assistant is still the actor and holds no authority. |
| saved agent | docs/architecture.md | The chat's feature that keeps an assistant set up for a purpose, so a new chat starts from it. |
| session key | docs/architecture.md | The key the coder pastes into the chat for one chat run so the chat reaches the tool; kept in the login keychain and deleted at Stop. |

### Flagged

- `organiser` is not in RS6's R2 set and is not an entry; the coder entry defines the organiser in one clause. The
  glossary is for the organiser, so the chief engineer may want it back as an entry.
- `reviewing` (the coder's step) shares a stem with the `review` command (RS6 candidate 21); only the step is defined.
- `contributor` and `participant` are two entries, as the simpler of the two options in the brief.

## Part 2. The 41 inconsistencies

FIXED 24, ACCEPTED 17. "Part 4" lists what lies outside the blast radius.

| ID | Term | Disposition | What changed and where, or the reason |
| --- | --- | --- | --- |
| I1 | contributor / participant | FIXED | `docs/flow.md:7,17`, `docs/data-and-consent.md:44,50`: "contributors" meaning people who take part now "participants". The attribution pages (`coding.md`, `norms.md`, `planning.md`) already used contributor for the named person. `src/` and CLI help agree with the entry. |
| I2 | inputs, model, analysis | FIXED | `docs/data-and-consent.md:7-10,20,30,40,43-44,50`: the three sorts of material are the field notes, the vault (the narratives, nodes and edges) and the reports; narratives are no longer inputs and no longer in two sorts. Words defined in `docs/architecture.md` for builders. |
| I3 | model | FIXED | The vault sense said in plain words: `docs/flow.md:22`, `chat-path.md:467`, `coding.md:991,998`, `getting-started.md:177,324,327`, `data-and-consent.md`. "Language model" and "the assistant's model" stay (a different thing, named so in `architecture.md`). |
| I4 | analysis | ACCEPTED | `docs/analysis.md` is the page of the analyse stage and keeps its title; the reports sense is now "reports" (`data-and-consent.md`), the step sense is the stage. Template README is outside the blast radius (Part 4). |
| I5 | session | FIXED | One sense, a facilitated event. A run of the chat is "a chat run": about 45 lines in `chat-path.md`, `local-llm.md`, `leave-no-trace.md`, `path-pros-and-cons.md:45,57`; `analysis.md:39` (browser tab), `ide.md:73`. Kept: the headings "Start a session" and "The session key" (a test fixes them; `session key` is a moved word), the REPL as "a Python session", file names in `acceptance/`. |
| I6 | type / kind | FIXED | Node categories are types: `index.md:20`, `getting-started.md:14`, `planning.md:8`, `coding.md:12` ("four node types"); "kinds of material" is "sorts of material" (`data-and-consent.md`). `kind` stays for scenario and architecture (`planning.md` "two kinds of session" matches it). |
| I7 | node as a page | ACCEPTED | The docs already say a node page is a node's page; only the template README (`tpl-pin3`) says a node is a page. Outside the blast radius (Part 4). |
| I8 | edge is a row | FIXED | `docs/architecture.md` section 6: "A narrative tells an edge in one row". The wording "it is a row" in `contracts/page-contracts.md:13` and `ontology/scat.ttl:7` is outside the changes allowed (Part 4). |
| I9 | status, done, finished | FIXED | `docs/coding.md:33` "finished narrative" is "`done` narrative". "The vault is finished" at hand-over is a statement, not a status. A derived edge status is kept in `architecture.md` and `coding.md:114`; `src/` derives it (the entry says page status). |
| I10 | entry stored as | FIXED | The glossary no longer holds `entry`. Its builder definition (`architecture.md`) says page, table row or body line. This ledger's one-line definition ("a field on a page") was wrong and is corrected in part 1. |
| I11 | entry (server entry) | ACCEPTED | `chat-path.md`, `leave-no-trace.md`: "the server entry" is the chat platform's record of the MCP server; the glossary no longer defines `entry`, so no clash. `coding.md:626` ("two entries" meaning pages) is fixed: "pages". |
| I12 | view | ACCEPTED | `docs/analysis.md` says four views plus evidence and copy-share, as the `view` and `evidence` entries say. "View:" in MCP text and "graph view" (Obsidian) are `src/` and Obsidian's names; `node` says the Obsidian sense. |
| I13 | review / reviewing | ACCEPTED | The docs write the command as `scat review` and the step as "reviewing" (`coding.md:123`, `chat-path.md:427`); "git review" is another act. Flagged in part 1. |
| I14 | check | ACCEPTED | One entry for the command and the gate. `architecture.md` "rules 1 and 2" are builder text; docs say "the check". |
| I15 | tool | ACCEPTED | The entry covers "the tools" and says the MCP server is a front end. Chat-platform "tool" (the agent's tool) is the platform's word; the template README is outside. |
| I16 | attribution | ACCEPTED | The entry is the people; the mode has its own entry (`attribution mode`); the `attribution` key and command are code names that the docs mark as such. |
| I17 | who sets mode and cap | ACCEPTED | The docs (`planning.md:49`, `coding.md:714`, `data-and-consent.md`) agree with the entries. `src/scat_kg/views.py:417`, `checks/attribution.py:75` tell the coder; Part 4. |
| I18 | organiser / facilitator-analyst / you | FIXED | `docs/index.md:70` "facilitator-analyst" is "organiser". "You" in guides is the reader. The facilitator and the note-taker stay two roles (`planning.md:120,124`). `src/` and skills say "coder"; Part 4. |
| I19 | assistant / agent / chatbot | ACCEPTED | "An AI chatbot" and "an AI IDE" are names of coding paths, not of the actor; the actor is the assistant. "Agent" is the IDE's or chat's name (`saved agent` is in the assistant contract). |
| I20 | narrative / story / account | FIXED | A narrative is one story; its prose is the account: `docs/coding.md:12`, `narratives.md:6,45`, `facilitate-scenarios.md:24,46`. Residual: guides call what a group tells at the event "an account" (ordinary English; flagged). |
| I21 | field notes / notes / inputs | FIXED | "Inputs" is gone from the guides but for `architecture.md:127` (defined there); "notes" is the short form of field notes. |
| I22 | group / stakeholder group | FIXED | `docs/narratives.md:24` "stakeholder group" is "group". The acronym expansion keeps it. |
| I23 | vault / project / repository | ACCEPTED | The vault entry says one git repository; "repository" is used for the GitHub copy and "project" for the organiser's work; no page uses them as the folder's name against the entry. |
| I24 | check / validate / verify | FIXED | `docs/norms.md:65` "validation" is "your confirmation" (the coder's act). |
| I25 | stub / draft | ACCEPTED | `stub` and `draft` are status values in the entry; "draft" as a verb is ordinary English and is the assistant's act (`assistant` entry). |
| I26 | edge type names | ACCEPTED | The `edge` entry names the three phrases; `coding.md:108-113` gives the slugs beside them. The CLI names are code. |
| I27 | no entry | FIXED | `node page` (folded into `node`), `session`, `account`, `participant`, `coding path`, `check` and others now have entries. `SCAT Chat`, `note-taker`, `workshop` stay without (under 6 pages or ordinary English). |
| I28 | layer vs type | ACCEPTED | Two entries, each one sense: `layer` is the group of nodes of one type; `type` the category. The entries say so. |
| I29 | longest definitions | FIXED | U1: longest definition is 50 words (narrative), 53 entries one term each. |
| I30 | shortest definitions | FIXED | U1: `element` moved; `field notes`, `page`, `vault`, `trace` are one sentence with an example. |
| I31 | IDs in rows | FIXED | U1: no WP, D- or R- ID in `glossary.yml`. |
| I32 | process text | FIXED | U1: the preface has no process paragraph. |
| I33 | rows that mix levels | FIXED | U1: one term per entry; mixed words moved or folded (part 1). |
| I34 | formal column | ACCEPTED | Deliberate: the formal column stays in `GLOSSARY.md` (MISSION.md lines 66 and 532 commit to it) and is empty or short for most words; `terms.md` omits it. |
| I35 | "The work" section | FIXED | U1: sections are the stages, platform and test words moved. |
| I36 | SCAT definition | FIXED | U1: the entry names the four types in order. |
| I37 | glossary vs terms.md, entries | FIXED | U1: both are generated from one file; the entry sets are equal. |
| I38 | timeframe wording | FIXED | U1: one definition, one sentence for both files. |
| I39 | who chooses cap and mode | ACCEPTED | `terms.md` carries the first sentence only by design; `GLOSSARY.md` and `planning.md:49` say who. |
| I40 | extra clauses in one file | ACCEPTED | As I39: the terms page is the first sentence of the same definition, so differences in length are by design. |
| I41 | duplication | FIXED | U1: one source, two generated files; a test checks them. |

Other word fixes in the same pass (not inconsistencies of their own): `docs/coding.md:114,136,145,147,208,662` and `docs/norms.md:8-23` no longer define "coded", "excluded" or "knowledge graph" as terms; they say a narrative that links no node page is left out of the graph and the views, and quote the tool's word "excluded" once. The heading "A coded narrative" in `norms.md` is now "A narrative that links a node page" and `tests/docs/test_norms.py` (its heading list) follows.

## Part 3. Re-run of RS6's checks

Counts of occurrences / pages over `docs/*.md` and `docs/reference/*.md` without `terms.md` (case-insensitive, word-bounded), before and after. `docs/architecture.md` now holds the builders' words, so "element", "range vault" and the ontology rise there.

| Word | Before | After |
|---|---|---|
| contributor (not page) | 56 / 9 | 52 / 9 |
| participant | 103 / 8 | 107 / 8 |
| session | 155 / 17 | 107 / 14 |
| status | 249 / 12 | 249 / 12 |
| finished | 18 / 8 | 17 / 8 |
| done | 367 / 19 | 368 / 19 |
| type | 265 / 13 | 270 / 15 |
| kind | 96 / 14 | 85 / 13 |
| review (cmd) | 11 / 5 | 11 / 5 |
| review/reviewing | 43 / 10 | 43 / 10 |
| reviewing | 5 / 5 | 5 / 5 |
| node page | 141 / 10 | 143 / 10 |
| organiser | 12 / 3 | 14 / 5 |
| facilitator | 31 / 4 | 30 / 3 |
| facilitator-analyst | 1 / 1 | 0 / 0 |
| knowledge graph | 20 / 7 | 15 / 5 |
| element | 0 / 0 | 1 / 1 |
| entry/entries | 43 / 6 | 43 / 5 |
| model | 94 / 13 | 86 / 10 |
| layered graph | 3 / 2 | 4 / 2 |
| inputs | 8 / 3 | 3 / 2 |
| analysis | 26 / 7 | 23 / 8 |
| coded/uncoded | 22 / 6 | 17 / 6 |
| excluded | 36 / 6 | 33 / 6 |
| analysing | 0 / 0 | 0 / 0 |
| leave no trace | 12 / 6 | 12 / 6 |
| range vault | 0 / 0 | 1 / 1 |
| the ontology | 4 / 2 | 5 / 2 |
| relationship annotation | 7 / 6 | 9 / 6 |
| norm | 25 / 4 | 25 / 4 |
| saved agent | 18 / 2 | 18 / 2 |
| session key | 9 / 2 | 9 / 2 |
| Linked beyond the text | 2 / 1 | 2 / 1 |
| stakeholder group | 4 / 4 | 3 / 3 |

Reading: contributor (apart from "contributor page") falls where it meant participant; session falls by the chat-run lines; model, knowledge graph, inputs, coded and excluded fall in the guides and stay in `architecture.md`, `reference/` (tool output quoted as it prints) and the contracts. "facilitator-analyst" is gone. The rises in type and participant are the fixes above. The remaining "excluded" and "coded" are in `docs/reference/` and `docs/coding.md` output blocks, which print the tool's own messages.

## Part 4. Outside the blast radius

| Where | Why | Change needed |
|---|---|---|
| `ORG.md` (the line that says GLOSSARY.md is changed by hand) | GLOSSARY.md is generated | Say it is regenerated from `glossary.yml` by `scripts/glossary.py` |
| `.claude/agents/*.md` (three files name GLOSSARY.md) | Same | Same wording |
| `src/scat_kg/views.py:417`, `src/scat_kg/checks/attribution.py:75` | Fix text tells the coder to edit `scat.toml`; the entry says the person who set up the tools writes it | "the person who set up the tools" |
| `src/scat_kg/views.py:534`, `scat attribution --help`, MCP tool `attribution` | "contributor" as the person a narrative is attributed to: this agrees with the contributor entry; no change | none |
| `src/scat_kg/checks/mention.py` (comment naming GLOSSARY.md), `src/` messages "excluded from the knowledge graph" | Dropped words in tool messages; docs quote them | Say "left out of the graph" when the messages are next changed; tests `tests/checks/helpers.py:203`, `tests/independent/test_seeded_defects.py` quote them |
| `tpl-pin3/README.md:66`, `tpl-pin3/narrative/false-start-and-clean-restart.md:13` | Template says a node is a page and an edge is a row; "stakeholder conversation" | "A node page is one page ..."; "an edge is told by a row" |
| `contracts/page-contracts.md:13`, `ontology/scat.ttl:7` | "An edge ... is a row" | "is told by a row" |
| `acceptance/walkthroughs/leave-no-trace-run.md:40-43` | Names the chat run section "Set up for the session" (history); the heading is now "Set up for the chat run" | none (history) |
| `MISSION.md:66,532` | Commit the glossary to a formal-concept column; the column stays in `GLOSSARY.md`, so both lines remain true | none |

## Part 5. Review fixes (PM)

The fresh reviewer's findings, each fixed or accepted:

- `docs/flow.md` links to words the terms page no longer defines: unlinked or relinked to a kept word (`check`, `view`).
- The `SCAT` first sentence had no verb: it now says what SCAT is.
- `candidate`'s first sentence: now a pair of nodes in neighbouring layers that a narrative links but tells in no row.
- The R4 test lacked `analysis`: added (the ledger moves it to the architecture page).
- `docs/coding.md` and `docs/narratives.md` used "account" for a whole narrative or a group's story: changed to "narrative" and "story". `contracts/rule-catalogue.md` said "a coded narrative": now "a narrative that links a node page".
- Accepted: the headings "Start a session" and "The session key" in `docs/chat-path.md` and the app's own dialog ("when you start a session", `deploy/SCAT Chat.applescript`) keep the app's word, which `tests/docs/test_chat_guides.py` also fixes; the `session` entry is about the facilitated event only. The rename of the app and its words belongs to WP37.
- Accepted: Start and Stop are dropped on a case-sensitive count (4 and 2 pages; the other counts are case-insensitive). Counted case-insensitively they are common words ("start", "stop"), so the case-sensitive count is the one that measures the buttons.
- Accepted: `plot` is on 3 pages by a recount, 2 in part 1; under 6 either way.
- Flagged for the ACE: `organiser` is used in six definitions and is not an entry (the `coder` entry names it in one clause).
