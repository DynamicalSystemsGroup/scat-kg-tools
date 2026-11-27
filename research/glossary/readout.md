# Glossary readout (RS6): what the words are, what is wrong with them, what the cleanup must decide

**Status.** Desk research, 27 Nov 2026, branch `spike/glossary`. No term, entry or page was changed; nothing is chosen
for the cleanup package. The sections down to "Not known" are 2,356 words by `wc -w` (table markup counts; about 2,000 of prose); Appendices A to C are
data-like tables and add about 2,150 more. Data, in `research/glossary/data/` on that branch: `glossary-terms.csv` (59 words), `app-terms-missing.csv`
(85), `glossary-terms-unused.csv` (13), `inconsistencies.csv` (41), each with a `.NOTES.txt`. `origin/dev` has moved since the
spike began (D-169 re-pinned the template); the template was read as `tpl-pin3`, at the pin of the spike's base.

**Limits.** Class (ORG, ASST, RED), level and journey are the spike's **judgements**, not computed. Page and use counts
are **regex word hits**, not sense hits ("tool", "model", "page", "session", "link" are inflated). J1 to J7 is the chief
engineer's frame (scope and policies; planning and soliciting; facilitating; gathering field notes; coding; analysing;
reporting out) until WP29's stages replace it; the journey tags are the spike's mapping. Page sets: **[G]** = the 22 docs
files of `glossary-terms.csv` (`docs/*.md` plus `api.md`, `cli.md`, `mcp.md`; no `terms.md`); **[M]** = the 22 of
`app-terms-missing.csv` (`docs/*.md` plus `cli.md`, `mcp.md`, `terms.md`; no `api.md`); **[23]** = all 23 files, which I
recomputed. Compare counts only within one set. Not checked: the rendered site and Obsidian strings; the MCP server at
run time; `contracts/`, `ORG.md`, `MISSION.md` (grep only); template example pages; rule-message wording; the skill file
(hits only). Source hits include docstrings.

## Summary

- **Inventory.** `GLOSSARY.md` has 53 rows (59 words once 4 compound rows are split); `docs/reference/terms.md` has 53
  bullets, 52 of 53 headwords equal. Definitions total 1,516 words (median 27, range 4 to 79) against 745 in `terms.md`,
  which is at its test cap of 910 words.
- **The app uses 85 words the glossary lacks:** 25 need an entry, 54 do not, 6 are assistant material.
- **Classes.** ORG 52, RED 5, ASST 2. By level: model 21, journey 14, vault 9, policy 8, tool 6, formal 1. The mixing is
  mostly levels inside ORG; 17 formal-concept cells use graph-theory or OWL words.
- **Journeys are uneven.** 37 ORG words touch J5 (coding), 14 touch J6. No word belongs to J2, J3 or J4 alone; the only
  J7-only word, `a finished model`, is on 1 page [G]. "Solicit" appears in no docs page or glossary row.
- **Inconsistencies:** 41 (high 2, medium 26, low 13); all are in Appendix B. Both high ones are about what a word covers
  (contributor; inputs and model). `session` has three senses on 18 pages [23] and no entry.
- **Cost.** Four organisations, 3 to 8 units; term-fixing touches 6 to 23 pages per word [23].

## G1. Inventory

- **In the glossary:** 53 rows, 59 words. In `terms.md`: 56 yes, 2 partial (inputs, analysis), 1 no (`model` is a row of
  its own, missing from the triple). Appendix A lists every word.
- **Unused or rare** (`glossary-terms-unused.csv`, 64 words checked). Unused in docs, template, CLI help, MCP text, skills:
  `element`, `analysing`, `range vault`, `life cycle`. On 3 pages or fewer, none in template, CLI or MCP: `a finished
  model`, `layered graph`, `mismatch`, `inputs`, `saved agent`, `session key`, `collection`, `organiser`, `server entry`.
- **Missing:** `app-terms-missing.csv`, 85 rows: workflow word 14, concept 14, command 11, flag 10, tool 9, page type 8,
  message 7, policy word 4, field 4, value 3, command-and-workflow 1 (`the check`).
- **The 25 `yes` words** (pages [M]; sense in a line):
  1. session (17): a facilitated event; a chat-path run; a browser session.
  2. account (17): the narrative's text; what a person or group offers, attributed.
  3. group, concern, affordance, technology (15): the four node kinds; used in `SCAT` and `node`, defined nowhere.
  4. the check (13): the command, and the pass/fail gate before `done`.
  5. refused (13): an operation the tool will not do; writes nothing.
  6. coding path (13): by hand, chat, AI IDE, local LLM.
  7. problem, error, warning (11): an error blocks; a warning is a to-do.
  8. participant vs contributor (11): synonyms; the glossary fixes one.
  9. facilitating (10): the organiser's job at an event; the facilitator is not the note-taker.
  10. node page (10): a page of a node type.
  11. clean (10): no errors; warnings may remain.
  12. consent (9): participants' consent; a chat platform's checkbox.
  13. MCP server (8): a program the chat calls; "connector", "server entry" are platform names.
  14. Start, Stop (7): ends of a chat session; Stop deletes the key.
  15. edge-type spellings (6): "is addressed by" in tables, `addressed-by` in commands.
  16. evidence (6): the view and command for one node page.
  17. REPL (6): a Python session; each command has a "twin".
  18. data policy (5): what an AI platform may keep; triggers leave no trace.
  19. participation terms (5): what participants are told first.
  20. candidate (5): a link with no row; also a release candidate.
  21. review (5): the command for pages that may be one node; not the coder's step.
  22. note-taker, compiler (4): event roles.
  23. SCAT Chat (3): the menu-bar app for the chat path.
  24. notebook (3): the template's Jupyter notebook that draws views.
  25. the nine choices (2): the questions answered before the first session.

## G2. Classification

| Class | model | journey | vault | policy | tool | formal | total |
|---|---|---|---|---|---|---|---|
| ORG | 17 | 14 | 7 | 8 | 6 | 0 | 52 |
| RED | 4 | 0 | 1 | 0 | 0 | 0 | 5 |
| ASST | 0 | 0 | 1 | 0 | 0 | 1 | 2 |

**RED in `glossary-terms.csv` (5):**
- `element`: 0 uses outside the glossary; "node or edge" says it.
- `layered graph`: 2 pages [G], one the builders' `docs/architecture.md`; `docs/reference/cli.md:2004` carries it, `scat --help` does not. Other definitions use it: `GLOSSARY.md:21` (node), `:26` (knowledge graph), `:35` (layered view); `terms.md:8`, `:13`.
- `entry`: rare in docs. Other definitions use it: `GLOSSARY.md:38` (relationship annotation), `:63` (index page), `:64` (status); `terms.md:25`, `:46`, `:47`. (`:86` uses "server entry", another sense.)
- `model`, two rows: **class disputed.** The CSV says it is met only as "finished model" (`docs/flow.md` step 10); the reviewer found J1 use: `docs/data-and-consent.md:7-8,10,40` defines the model as one of three kinds of material (the git repository, with the knowledge graph) and the data choices turn on it. It has three or more senses (I3). The CSV class is unchanged.

**ASST (2):** `the ontology` (met only as what `scat check` obeys; `contracts/`, `docs/architecture.md`); `range vault`
(0 uses; a test fixture, `MISSION.md`). Of the 85 missing words, 6 are ASST (MCP prompt, assistant's rules and
contracts, `--json`, the machine interface contract, the six MCP prompts, MCP tool) and 8 RED.

**Words a small organiser glossary would hold, by the evidence.** Rule R1: ORG in `glossary-terms.csv` with at least 6
docs pages [G], or any CLI command, or an MCP file. That gives **42 of 52** ORG words. Not meeting it (10): uncoded,
mismatch, organiser, inputs, analysing, a finished model, norm, skill, saved agent, session key. Rule R2, narrower: R1
and at least 12 pages [G] or a named CLI command: **32** words. The options below are sized at R2 (32) plus whichever
of the 25 `yes` words the package takes; all 25 would make 57. By journey (R1 words; `r` = R1 only; `*` = a `yes` word):
- *Every step:* SCAT, vault, page, field, link, type.
- *J1 scope and policies:* attribution mode, attribution, cap, leave no trace (r), analysis (r); consent*, data policy*, the nine choices*.
- *J2 planning, soliciting:* scenario, architecture; participation terms*, note-taker*, facilitating*, session*. None is J2 alone.
- *J3 facilitating, J4 field notes:* field notes, timeframe, narrative.
- *J5 coding:* node, edge, layer, status, Edges told, contributor page, coder, assistant, tool, rule, coding, interpreting (r), reviewing, coded (r), excluded (r), conformant (r), relationship annotation (r), authoring (r), the coding loop (r), knowledge graph (r); node page*, the check*, refused*, error*, edge spellings*, account*, coding path*.
- *J6 analysing:* fingerprint, trace, edge table, layered view, view; evidence*, notebook*.
- *J7 reporting out:* index page. No entry names a report or the hand-over except `a finished model` (1 page).

**Flags, not actions.** ORG words on 3 pages or fewer [G] with no CLI or MCP use: organiser (3), inputs (3), mismatch (2),
a finished model (1), saved agent (2), session key (2), analysing (0). Words whose row joins several: coded/uncoded,
coder/assistant/tool, inputs/model/analysis, rule/norm. The tests need `mismatch` on the page (G4).

## G3. Inconsistencies (RS6-R2)

41 rows, each naming at least two places; **Appendix B lists all 41** with their places. Kind letters are not defined in
the files; my reading: **a** one word, several senses (15); **b** uneven scope or depth (8); **c** glossary vs `terms.md`
(6); **d** docs or messages against the entry (12). Severity: high 2, medium 26, low 13. The two high ones:

- **I1 contributor.** `GLOSSARY.md:62` fixes it as a participant; `docs/coding.md:656`, `src/scat_kg/views.py:534`, `scat attribution --help`, MCP tool `attribution` and `skills/scat-coding/SKILL.md:55` use it for the person a narrative is attributed to.
- **I2 inputs, model.** `GLOSSARY.md:73` puts only the field notes in inputs; `docs/data-and-consent.md:7` adds the narratives, and `:8` also puts them in the model; `terms.md:54` drops `model`.

Most useful medium ones: **I5 session** (an event, `docs/planning.md:120`; a chat run, `GLOSSARY.md:85`; a browser session, `docs/analysis.md:37`; no entry). **I6 type, kind** (`GLOSSARY.md:44` lists scenario and architecture as types; `terms.md:18` and `docs/coding.md:190` carry them in `kind`). **I9 status** (`GLOSSARY.md:64` signed off by the coder; `src/scat_kg/graph.py:381` derives an edge status nobody signs). **I13 review** (`GLOSSARY.md:78` the coder's step; `scat review --help` a command). **I17** (`GLOSSARY.md:59-60` and `docs/planning.md:49`: the person who set up the tools writes `scat.toml`; `src/scat_kg/views.py:417` and `checks/attribution.py:75` tell the coder to). **I18 organiser** (`GLOSSARY.md:71`; `docs/index.md:70` "facilitator-analyst"; "you" on most pages; `src/` "coder" 86 uses, skills 42 more, organiser 0). **I29, I31** (five rows over 50 words carry rules; seven rows cite WP, D- or R- IDs).

## G4. What binds the options

`tests/docs/test_terms.py` is the only test that reads `GLOSSARY.md` or `terms.md` by name. It checks:
- `terms.md`'s bold terms equal the glossary's first-column bold terms (`a, b, c` counts as three);
- no retired word (`raw page`, `coded page`, `class page`, `relation page`, `stakeholder group`, `heldby`, `conflict`);
- at most 910 words (`WORD_CAP`; the test's docstring still says 820);
- no prescriptive line: `should`, `must`, `need to`, `make sure`, `do not`, `don't`, `you`, or a bullet opening `run`, `use`, `write` or `set`;
- every backticked name is in the ontology, and the page names every page type, status, `kind` and `timeframe` value, edge verb and the table heading; `GLOSSARY.md` uses each edge verb;
- nine mutation tests rename a term and need it on the page: **fingerprint**, **mismatch**, **coding**, **link**, `` `narrative` page``, `holds`, `done`, `Edges told`, and `mixed` (or `stub`);
- `flow.md`, `data-and-consent.md`, `coding.md` use no retired word.

Other tests read `terms.md` only as one page among all: `test_wp24_keywords.py:36`, `test_docs_code_agreement.py:42` (globs of `docs/*.md` and `docs/reference/*.md`), `test_docs.py:12`, `test_wp25_paths.py:89`. A new page needs only a nav line (`mkdocs.yml:69`, `strict: true`). `MISSION.md:66,532` commit the glossary to mapping each word to a formal concept.

Sweep: seven docs pages link `reference/terms.md` (analysis, architecture, chat-path, coding, data-and-consent, flow, index; no anchors). `MISSION.md`, `ORG.md`, `contracts/page-contracts.md`, three `.claude/agents` files and a comment in `src/scat_kg/checks/mention.py` name `GLOSSARY.md`; `acceptance/`, `work-packages/` and `decisions/log.md` cite it too (history; the sweep decides). Term-fixing common to all options, not costed below, in pages [23]: contributor 11, session 18, status 13, model 12, review or reviewing 11 (the command `scat review`: 6), narrative 23, organiser 4, node page 11.

## Options for the cleanup package, with costs

Units on the 1, 2, 3, 5, 8 scale are my estimates. "Files" counts structure only. Size is in words (terms): A, B and D
at about the R2 size (32) plus chosen `yes` words; C core the same, the builders' page the rest.

| Option | What it is | Where ASST, RED, formal words live | `terms.md` and tests | Files | Units |
|---|---|---|---|---|---|
| A. By journey | sections J1 to J7 (or WP29's stages) plus an "every step" lead | ASST to `docs/architecture.md` and `contracts/`; RED words dropped or folded; formal column dropped or moved | `terms.md` mirrors the sections; the row regex still works; cap lowered; keep the nine mutation terms and ontology names; amend `MISSION.md` 66, 532 | `GLOSSARY.md`, `terms.md`, `test_terms.py`, `architecture.md`, `MISSION.md` = 5 | 5 |
| B. Model first, then the work | part 1 node, edge, layer, type, narrative, view, status; part 2 coding and analysing; part 3 policy | as A | as A | 5 | 5 |
| C. Short core plus "for builders" page | core organiser words; a second page holds ontology, formal column, contract words, `range vault` | the new page | `test_terms.py` split: sync and ontology checks on the core, a new check for the companion; nav line | `GLOSSARY.md`, `terms.md`, new page, `test_terms.py`, `mkdocs.yml`, `MISSION.md` = 6 | 8 |
| D. One alphabetical list, short core | rows A to Z, no sections | ASST and RED words removed; formal column dropped | smallest: shrink both files, same test, cap lowered, keep the nine mutation terms | `GLOSSARY.md`, `terms.md`, `test_terms.py`, `MISSION.md` = 4 | 3 |

None of the four gives J2 or J7 a word of its own; that needs terms WP29 defines.

## Not known

- Whether `docs/reference/api.md` is generated; whether any counted hit is the right sense (none was read).
- How the rendered site, the Obsidian UI and the MCP tools word these terms at run time.
- Whether an organiser reads tool, assistant and rule as organiser terms (L-tool words met on the chat and IDE paths).
- How WP29's stages map onto J1 to J7; the unit estimates have no history behind them.
- `inconsistencies.csv` rows I7 and I27 carry a mislabeled "node page 137 hits on 11 pages" (it is all 23 files; `docs/*.md` alone has 37 on 7 pages). The CSV was not edited; this is the correction.

## Appendix A. Every glossary word (59)

Journeys and level from `glossary-terms.csv`; issues are inconsistency IDs (Appendix B), matched by term and row; "terms.md" is the CSV's by-eye comparison.

| term | class | level | journeys | issues | terms.md vs glossary |
|---|---|---|---|---|---|
| SCAT | ORG | journey | J1 | I14,I16,I27,I33,I36 | differs slightly |
| node | ORG | model | J5,J6 | I7,I27,I28,I33,I34 | same |
| edge | ORG | model | J5,J6 | I8,I9,I26,I33,I34 | same |
| element | RED | model | - | I30,I33,I34 | same |
| layer | ORG | model | J5,J6 | I28,I33,I34 | same |
| layered graph | RED | model | - | I33,I34 | differs slightly |
| knowledge graph | ORG | model | J5,J6 | I33,I34 | differs |
| narrative | ORG | journey | J3,J4,J5 | I20,I33 | differs slightly |
| coded | ORG | model | J5 | I29,I31,I33 | same |
| uncoded | ORG | model | J5 | I29,I31,I33 | same |
| excluded | ORG | model | J5 | I31,I33 | same |
| timeframe | ORG | model | J3,J4 | I33 | differs slightly |
| scenario | ORG | journey | J2,J3 | I6,I33 | same |
| architecture | ORG | journey | J2,J3 | I6,I33 | same |
| fingerprint | ORG | model | J5,J6 | I33,I34 | differs |
| edge table | ORG | model | J6 | I26,I33,I34 | same |
| layered view | ORG | model | J6 | I33,I34 | same |
| trace | ORG | model | J6 | I30,I33,I34 | same |
| view | ORG | model | J6 | I12,I16,I33,I34 | differs slightly |
| relationship annotation | ORG | model | J5 | I33 | differs slightly |
| type | ORG | model | J5 | I6,I26,I28,I33,I34 | same |
| the ontology | ASST | formal | - | I33,I34 | differs slightly |
| entry | RED | vault | - | I10,I11,I27,I33,I34 | differs materially |
| model | RED | model | - | I2,I3,I19,I33,I34 | matches |
| conformant | ORG | model | J5,J7 | I33,I34 | same |
| vault | ORG | vault | J2,J5 | I3,I23,I30,I33 | same |
| page | ORG | vault | J5 | I4,I7,I27,I30,I33 | same |
| field | ORG | vault | J5 | I21,I30,I33 | same |
| Edges told | ORG | vault | J5 | I33 | same |
| link | ORG | vault | J5 | I33 | same |
| cap | ORG | policy | J1,J2 | I17,I33 | differs slightly |
| attribution mode | ORG | policy | J1 | I17,I31,I33 | differs slightly |
| attribution | ORG | policy | J1,J5 | I1,I16,I17,I31,I33 | same |
| contributor page | ORG | policy | J5 | I29,I31,I33 | same |
| index page | ORG | vault | J5,J7 | I33 | differs materially |
| status | ORG | vault | J5 | I9,I25,I33 | same |
| mismatch | ORG | model | J5 | I31,I33 | same |
| organiser | ORG | journey | J1,J2,J3,J4,J5,J6,J7 | I18,I33 | same |
| coder | ORG | journey | J5,J6 | I18,I29,I33 | same |
| assistant | ORG | tool | J5 | I19,I29,I33 | same |
| tool | ORG | tool | J5 | I15,I29,I33 | same |
| inputs | ORG | policy | J1 | I2,I21,I33 | differs materially |
| model | RED | model | - | I2,I3,I19,I33,I34 | not in row |
| analysis | ORG | policy | J1,J6 | I2,I4,I33 | differs materially |
| field notes | ORG | journey | J3,J4,J5 | I21,I30,I33 | same |
| interpreting | ORG | journey | J5,J6 | I33 | same |
| authoring | ORG | journey | J5 | I33 | same |
| coding | ORG | journey | J5 | I33 | same |
| reviewing | ORG | journey | J5 | I13,I33 | same |
| the coding loop | ORG | journey | J5 | I33 | differs slightly |
| analysing | ORG | journey | J6 | I33 | same |
| a finished model | ORG | journey | J7 | I29,I33 | differs |
| rule | ORG | tool | J5 | I29,I33 | differs slightly |
| norm | ORG | policy | J5 | I29,I33 | differs slightly |
| skill | ORG | tool | J5 | I33 | same |
| saved agent | ORG | tool | J5 | I33 | same |
| session key | ORG | tool | J5 | I33,I34 | same |
| leave no trace | ORG | policy | J1 | I31,I33 | differs slightly |
| range vault | ASST | vault | - | I33 | same |

## Appendix B. All 41 inconsistencies

Kind: a senses, b depth, c glossary vs `terms.md`, d against the entry (my reading). Places are locators only (first six); `inconsistencies.csv` holds the quotes. I29 lists six rows in the CSV; five exceed 50 words.

| ID | kind | term | sev | places that disagree |
|---|---|---|---|---|
| I1 | a | contributor (vs participant, attribution) | high | GLOSSARY.md:62; docs/coding.md:656; src/scat_kg/views.py:534; scat attribution --help; MCP tool attribution; skills/scat-coding/SKILL.md:55; ... |
| I2 | a | inputs, model, analysis (what is in each) | high | GLOSSARY.md:73; docs/data-and-consent.md:7; docs/data-and-consent.md:8; docs/reference/terms.md:54 |
| I3 | a | model (ontology+vault, repository, LLM, example) | medium | GLOSSARY.md:47; docs/chat-path.md:162; docs/local-llm.md:10; docs/leave-no-trace.md:91; docs/getting-started.md:177; docs/flow.md:22 |
| I4 | a | analysis (material, step, page, notebook) | medium | GLOSSARY.md:73; GLOSSARY.md:80; docs/data-and-consent.md:8; docs/analysis.md:1; tpl-pin3/README.md:58 |
| I5 | a | session (workshop, chat run, browser) | medium | GLOSSARY.md:60; GLOSSARY.md:85; docs/chat-path.md:9; docs/planning.md:120; docs/analysis.md:37; docs/chat-path.md:96 |
| I6 | a | type vs kind (scenario, architecture; "kinds of" | medium | GLOSSARY.md:44; GLOSSARY.md:31; docs/reference/terms.md:18; docs/coding.md:190; docs/index.md:20; docs/data-and-consent.md:7; ... |
| I7 | a | node ("node" as a page) | medium | GLOSSARY.md:21; tpl-pin3/README.md:66; docs/coding.md:1038; docs/analysis.md:25 |
| I8 | d | edge ("an edge is a row") | medium | GLOSSARY.md:22; tpl-pin3/README.md:66; docs/architecture.md:137; docs/architecture.md:70; docs/coding.md:114 |
| I9 | a | status (edge status; status vs done vs finished) | medium | GLOSSARY.md:64; src/scat_kg/graph.py:381; scat edges --help; docs/architecture.md:137; GLOSSARY.md:81; docs/coding.md:33 |
| I10 | c | entry (what an entry is stored as) | medium | GLOSSARY.md:46; docs/reference/terms.md:31; docs/coding.md:626; docs/architecture.md:137 |
| I11 | a | entry (server entry, "the entry" in the chat) | medium | GLOSSARY.md:46; docs/chat-path.md:128; docs/chat-path.md:289; docs/chat-path.md:308; docs/leave-no-trace.md:29 |
| I12 | a | view (four views, more views, graph view, view d | medium | GLOSSARY.md:37; docs/analysis.md; MCP tool review; MCP tool attribution; docs/coding.md:1038; docs/architecture.md:144 |
| I13 | a | review / reviewing | medium | GLOSSARY.md:78; scat review --help; docs/coding.md:129; MCP prompt review-before-done |
| I14 | a | check (the two checks, both checks, scat check) | medium | GLOSSARY.md:48; GLOSSARY.md:79; scat check --help; docs/architecture.md:55 |
| I15 | a | tool (the package, MCP tools, "Ask User tool") | medium | GLOSSARY.md:72; docs/local-llm.md:17; docs/chat-path.md:312; docs/chat-path.md:381; tpl-pin3/README.md:66 |
| I16 | a | attribution (people, mode, view, scat.toml key) | medium | GLOSSARY.md:61; GLOSSARY.md:60; tpl-pin3/scat.toml:2; scat attribution --help; docs/coding.md:710 |
| I17 | d | who sets the attribution mode and the cap | medium | GLOSSARY.md:60; src/scat_kg/views.py:417; src/scat_kg/checks/attribution.py:75; docs/coding.md:714; docs/planning.md:49 |
| I18 | d | organiser / you / coder / facilitator-analyst /  | medium | GLOSSARY.md:71; docs/index.md:70; docs/flow.md:7; docs/planning.md:120; src, skills/, tpl-pin3 README/AGENTS/skills: |
| I19 | d | assistant / agent / chatbot / AI / LLM / model | medium | GLOSSARY.md:72; GLOSSARY.md:84; docs/ide.md:18; docs/chat-path.md:111; docs/coding-paths.md:6; docs/architecture.md:14 |
| I20 | d | narrative / story / account | medium | GLOSSARY.md:27; docs/narratives.md:45; docs/facilitate-scenarios.md:24; docs/coding.md:12; docs/analysis.md:6 |
| I21 | d | field notes / notes / inputs / transcript | low | GLOSSARY.md:74; docs/chat-path.md:96; docs/planning.md:53; docs/data-and-consent.md:27; docs/architecture.md:127 |
| I22 | d | group / stakeholder group / stakeholder | low | GLOSSARY.md:20; GLOSSARY.md:21; GLOSSARY.md:59; docs/reference/terms.md:42; tpl-pin3/narrative/false-start-and-clean-restart.md:13 |
| I23 | d | vault / project / repository / repo / folder | low | GLOSSARY.md:54; GLOSSARY.md:47; docs/ide.md:24; docs/chat-path.md:20; docs/flow.md:17 |
| I24 | d | check / validate / verify | low | GLOSSARY.md:48; docs/norms.md:65; src/scat_kg/vault.py:17 |
| I25 | d | stub / draft (status vs act) | low | GLOSSARY.md:64; MCP prompt draft-a-node-page; skills/scat-coding/SKILL.md:26; docs/architecture.md:57; GLOSSARY.md:76 |
| I26 | d | edge type names and the edge table command | low | GLOSSARY.md:22; scat record-edge --help; MCP tool edge_table; scat edges --help; GLOSSARY.md:34 |
| I27 | d | used everywhere, no entry (node page, SCAT Chat, | low | docs/*.md; docs/chat-path.md:13; docs/planning.md:120; docs/facilitate-scenarios.md:4; GLOSSARY.md:1-87 (none of these words appears as a term |
| I28 | a | layer vs type (node categories) | low | GLOSSARY.md:24; GLOSSARY.md:44; docs/reference/terms.md:11; tpl-pin3/README.md:66 |
| I29 | b | longest definitions (coded,uncoded; rule,norm; c | medium | GLOSSARY.md:28; GLOSSARY.md:82; GLOSSARY.md:62; GLOSSARY.md:81; GLOSSARY.md:72; GLOSSARY.md:86 |
| I30 | b | shortest definitions (element, field notes, page | low | GLOSSARY.md:23; GLOSSARY.md:74; GLOSSARY.md:55; GLOSSARY.md:36; GLOSSARY.md:54; GLOSSARY.md:56 |
| I31 | b | decision-log, work-package and review IDs in row | medium | GLOSSARY.md:28; GLOSSARY.md:29; GLOSSARY.md:60; GLOSSARY.md:61; GLOSSARY.md:62; GLOSSARY.md:65; ... |
| I32 | b | process text in the glossary (Changing this glos | medium | GLOSSARY.md:12; GLOSSARY.md:13; GLOSSARY.md:14 |
| I33 | b | rows that mix levels or join terms | medium | GLOSSARY.md:47; GLOSSARY.md:73; GLOSSARY.md:72; GLOSSARY.md:28; GLOSSARY.md:82 |
| I34 | b | Formal concept column needs a specialist | medium | GLOSSARY.md:21; GLOSSARY.md:33; GLOSSARY.md:34; GLOSSARY.md:46; GLOSSARY.md:82; GLOSSARY.md:85 |
| I35 | b | "The work" section mixes steps, platform feature | medium | GLOSSARY.md:75; GLOSSARY.md:79; GLOSSARY.md:83; GLOSSARY.md:85; GLOSSARY.md:86; GLOSSARY.md:87 |
| I36 | b | SCAT definition | low | GLOSSARY.md:20; docs/reference/terms.md:7; GLOSSARY.md:44 |
| I37 | c | glossary vs terms.md: set of entries | medium | GLOSSARY.md:73; docs/reference/terms.md:54; GLOSSARY.md: 53 rows; docs/reference/terms.md: 53 bullets |
| I38 | c | glossary vs terms.md: timeframe | low | GLOSSARY.md:30; docs/reference/terms.md:17 |
| I39 | c | glossary vs terms.md: who chooses cap and mode | low | GLOSSARY.md:59; docs/reference/terms.md:42; GLOSSARY.md:60; docs/reference/terms.md:43 |
| I40 | c | glossary vs terms.md: extra clauses in one file  | low | docs/reference/terms.md:46; GLOSSARY.md:63; docs/reference/terms.md:25; GLOSSARY.md:38 |
| I41 | c | glossary vs terms.md: duplication | medium | GLOSSARY.md: 53 rows, definitions 1516 words (median 27; docs/reference/terms.md: 53 bullets, 745 words (median ; GLOSSARY.md:12 |

## Appendix C. Re-checks I ran (27 Nov 2026)

| # | Claim (source) | Check | Result |
|---|---|---|---|
| 1 | 53 glossary rows | `grep -c '^\| \*\*' GLOSSARY.md` | confirmed |
| 2 | 53 `terms.md` bullets, 745 words | grep; script | confirmed |
| 3 | definitions 1,516 words, median 27, 4 to 79 | script | confirmed (first parse gave 1,501: 7 rows hold a `\|` in code; fixed) |
| 4 | `terms.md` at the cap | `wc -w`; `WORD_CAP` | 910 and 910 (not in the data) |
| 5 | 59 rows; class 52/5/2; levels | Python over the CSV | confirmed |
| 6 | 85 missing: yes 25, no 54, assistant 6 | Python | confirmed |
| 7 | 41 rows: a15 b8 c6 d12; high 2, medium 26, low 13 | Python | confirmed |
| 8 | 20 CLI commands | `uv run scat --help` | confirmed |
| 9 | 7 rows cite WP/D-/R- IDs | regex | same 7 rows |
| 10 | `element` unused | `grep -rniw` in `docs` | only `terms.md:10`; confirmed |
| 11 | pages: session 17, contributor 10, participant 8, node 16, narrative 22, vault 20, organiser 3 | script, sets G and M | confirmed per set; on [23]: 18, 11, 9, 17, 23, 21, 4 |
| 12 | I27: "node page" 137 hits on 11 pages in `docs/*.md` | script | **wrong label**: all 23 files; `docs/*.md` alone 37 on 7 pages. Corrected above; CSV not edited |
| 13 | I29: six rows over 50 words | script | **five** (79, 71, 66, 57, 51); `leave no trace` has 50. Corrected |
| 14 | RED `model`: "met only as finished model" | read `docs/data-and-consent.md:7-10,40` | **false**; J1 use found; class marked disputed |
| 15 | I17 quote, I18 counts | `sed`, grep | quote at `GLOSSARY.md:60` (and `:59` for cap); coder 86 in `src/`, skills 42 more |
| 16 | "solicit" absent; only `test_terms.py` reads the glossary by name | grep over docs, `tests/` | confirmed |
