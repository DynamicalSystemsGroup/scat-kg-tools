# Audit: the first-time organiser on the chat path

Reviewer persona: first-time organiser of a community elicitation, not a programmer, coding through a chat assistant with the SCAT tools and reading in Obsidian. Read-only: I ran `uv run scat check/layered/review/copy-share` against `../tpl-pin3` (clean, 0 problems) and changed nothing. Paths are relative to `wp40-audit/` unless they begin `tpl-pin3`. I am unsure where I say so; where I say "I believe" I am inferring from outside this repo.

Verdict words: keep / simplify / cut. Lens throughout: the coder's job is to find abstract patterns in concrete accounts (a few reusable concerns, affordances and technologies that many stories point at), label them, and organise the data under them. Heuristics: "make the right way the easy way" and "as simple as possible but no simpler".

---

## 1. Explanation

### SYNTAX: what makes a vault well-formed

- **Seven page types.** Four node types (group, concern, affordance, technology), plus narrative, contributor and index (`ontology/scat.ttl:4-6`, classes at 71-187). Six are Markdown files with YAML frontmatter; an index is an Obsidian Base file with no frontmatter (`scat.ttl:5-6`, `187-196`).
- **Fields.** `type`, `status`, `title` on every page; `description` required once `done`; narratives also need `timeframe` at `done` and may carry `kind` and `attributed_to` (`scat.ttl:244-290`, `166-176`).
- **Status.** `stub`, `draft`, `done` (`scat.ttl:304-330`). Unfinished is never an error until `done` (`scat.ttl:311-315`). The coder alone sets `done`, in Obsidian; the chat server refuses (`src/scat_tools/mcp_server/server.py:61-90`).
- **Edges are not pages.** An edge is one row of a narrative's `Edges told` table with four columns: from, type, to, note (`scat.ttl:166-176`, `206-232`). There are three edge types joining neighbouring layers only: group-holds-concern, concern-is-addressed-by-affordance, affordance-is-provided-by-technology (`scat.ttl:128-163`). The row's type is already fixed by the layers of its two ends (`scat.ttl:9-10`; `contracts/page-contracts.md:259`).
- **File names** are lowercase slugs, at most 64 characters (`contracts/rule-catalogue.md:352-362`). `scat.toml` must hold a group cap and an attribution mode (`rule-catalogue.md:497-520`; `tpl-pin3/scat.toml`).
- **The check.** About 50 rule ids in a 904-line catalogue (`rule-catalogue.md:137-190`). Most come in a DRAFT (warning) and DONE (error) pair (`rule-catalogue.md:573-577`, `659-667`).

### SEMANTICS: what the parts mean

- **Group** = a stakeholder group, never a person; **Concern** = "any interest in a system"; **Affordance** = what a technology offers those in the situation; **Technology** = a discrete part of a system (`scat.ttl:71-115`). The definitions are adopted from SEBoK, ISO 42010 and Gibson, and the file marks them `unverified` (`scat.ttl:74-80`).
- **A narrative** is one account from the field notes. A scenario is behavioural (groups, concerns, affordances); an architecture is structural (concerns, affordances, technologies) (`MISSION.md`, "Narratives" section). `timeframe` (past/future/mixed) is a mark on the narrative only (`scat.ttl:272-277`).
- **An edge is "told" by a narrative.** The graph holds one edge per (type, from, to) and lists every narrative that tells it; two narratives telling the same edge are two tellings (`scat.ttl:121-126`, `rule-catalogue.md:649`). Recurrence across narratives is the evidence of a pattern: "Its worth shows in recurrence across narratives" (`docs/norms.md:25-29`).
- **Disagreement is held, not resolved.** A remark between two nodes is a plain body line and "the tool gives it no meaning" (`tpl-pin3/README.md`, "What this is").
- **A link is not an edge.** Mentioning two nodes without a row has told nothing (`docs/coding.md:145`; `rule-catalogue.md:713-721`).

### PRAGMATICS: how a person gets from accounts to patterns

The intended loop (`docs/coding.md:116-131`): interpret the field notes, author a narrative page, code it (link the nodes it names, record the edges it tells), review it, set `done`. Then read the views, which can send you round again.

On the chat path:

1. A **setup person** builds SCATLAB.app, and you install Colima, Tailscale and the app; each chat run starts a container and a public link, and you re-add the connector with a fresh key (`docs/chat-path.md:128`, `178-179`, `195-206`).
2. You attach field notes. The assistant drafts the account **as chat text**; you paste it into Obsidian (steps 100-101, `chat-path.md:~395-400`). It cannot write narrative or node text through the tool (`contracts/assistant.md:28-30`).
3. The assistant proposes nodes and links; you confirm; it calls `stub`, `stub_links` and `record_edge` (`server.py:98-130`).
4. It runs `check` and quotes each problem as reported. You read the page and set `status: done` by hand.
5. Views come back as data in chat. To keep them you ask for `export_edges` (CSV and Markdown into `views/`) (`chat-path.md:~425-430`). The layered picture needs plot output in chat or the Jupyter notebook, which is started from a terminal (`docs/analysis.md:4`, `34`).
6. Possible duplicate nodes are found with `review`. To merge, **you run `scat merge A B` yourself**; the server refuses to apply it (`server.py:138-155`, `chat-path.md:413`).

The tool has four jobs bolted together: a Markdown linter (the rules), a graph builder, a set of views, and an MCP server wrapped in a lifecycle-stage gate. Only the middle two are the pattern-finding. The first and last are most of the code and most of what the organiser has to learn.

---

## 2. Verdict table

Pairs are reported once as "(pair)": the DRAFT id is a warning and the DONE id an error. "Fam" abbreviates a family I recommend collapsing.

### 2a. Rules (`contracts/rule-catalogue.md`)

| Item | S/Sem/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| SCAT-FM-PARSE | Syntax | simplify | Broken YAML will happen to a person typing in Obsidian, so something must say so. Merge with FM-SHAPE into one "frontmatter is unreadable" message. | rule-catalogue.md:265 |
| SCAT-FM-REQUIRED | Syntax | keep | status and title are what every view needs; `scat stub` writes them so it rarely fires. | rule-catalogue.md:276 |
| SCAT-FM-TYPE | Syntax | simplify | One of six values; fold into a single "value not allowed" rule with STATUS, TIMEFRAME, KIND. Four ids for one idea. | rule-catalogue.md:289 |
| SCAT-FM-STATUS | Syntax | simplify | As FM-TYPE. | rule-catalogue.md:302 |
| SCAT-FM-TIMEFRAME | Syntax | simplify | As FM-TYPE; and see timeframe field below. | rule-catalogue.md:314 |
| SCAT-FM-KIND | Syntax | simplify | As FM-TYPE; `kind` is optional and only changes which columns a fingerprint draws (analysis.md says so). | rule-catalogue.md:326 |
| SCAT-FM-SHAPE | Syntax | simplify | "Expected one line of text, found a boolean": real but merge with FM-PARSE. | rule-catalogue.md:340 |
| SCAT-NAME | Syntax | keep | Names are the identity of every node; a duplicate or odd name silently breaks links. `stub` derives a legal name for you, so the right way is easy. | rule-catalogue.md:352 |
| SCAT-DONE-FIELD / SCAT-DRAFT-FIELD (pair) | Syntax | simplify | `description` on a node page is the label of the pattern: keep. On a narrative it repeats the account and `timeframe` has no consumer (see below): drop both from the `done` gate. | rule-catalogue.md:364, 378; norms.md:30-36 |
| Mode rule (one sentence, three modes) | Sem | simplify | A policy statement about who may be named; see attribution cut. | rule-catalogue.md:394 |
| SCAT-ATTR-DISALLOWED | Sem | keep | The one rule that enforces a promise to participants ("keep the commitments made"). Cheap and checkable. | rule-catalogue.md:415; MISSION.md "Core heuristics" |
| SCAT-ATTR-LINK | Syntax | cut | Only exists because contributors are pages with a link field; cut with the field (see top five). | rule-catalogue.md:428 |
| SCAT-DONE-ATTR / SCAT-DRAFT-ATTR (pair) | Syntax | cut | "Required" attribution is a project policy the organiser can hold in a sentence; blocking `done` on it is machinery for a non-synthesis concern. | rule-catalogue.md:443, 456 |
| SCAT-LINK-DANGLING-BODY | Syntax | keep | A link to nothing is the commonest slip in Obsidian; the fix offers a stub. This is the "make the right way easy" rule. | rule-catalogue.md:467 |
| SCAT-CAP | Sem | keep | The cap forces participants to be clustered into groups, which is itself an abstraction step toward patterns. But make it a gentle warning, not a vault error. | rule-catalogue.md:484; planning.md:16-24 |
| SCAT-MODE-CONFIG | Syntax | simplify | Config errors: merge the three config rules into one "scat.toml is unreadable, here is the line to write". | rule-catalogue.md:497 |
| SCAT-CAP-CONFIG | Syntax | simplify | Same; an absent file is an error (rule-catalogue.md:511) so a deleted `scat.toml` blocks everything. | rule-catalogue.md:511 |
| SCAT-SUGGEST-CONFIG | Syntax | cut | Validates a switch (`link_suggestions`) that should not exist. | rule-catalogue.md:522 |
| SCAT-MENTION | Pragmatic | cut | Off by default; suggests links where plain text names a node. Obsidian has "unlinked mentions" built in (I believe), and the assistant proposes links anyway (assistant.md:A2). | rule-catalogue.md:535 |
| SCAT-NOEDGES | Pragmatic | simplify | A warning only. Keep as a line in `status`, not a rule: it is the only prompt that a "done" account tells nothing. | rule-catalogue.md:547 |
| SCAT-UNCODED | Sem | keep | A narrative with no node link silently vanishes from every view; saying so is essential. Clearest message in the set (coding.md:226-236). | rule-catalogue.md:560 |
| SCAT-DRAFT/DONE-TABLE-HEADER (pair) | Syntax | simplify | Pipe-table hygiene. Needed only because rows are typed; if the assistant writes rows (A9) and the header is generated, this almost never fires. Fold with ROW and SECOND into "table is unreadable at line N". | rule-catalogue.md:579 |
| SCAT-DRAFT/DONE-TABLE-ROW (pair) | Syntax | simplify | As HEADER. Five variants of "wrong number of cells". | rule-catalogue.md:594 |
| SCAT-DRAFT/DONE-TABLE-TYPE (pair) | Syntax | cut | Exists only because the person writes the edge type, which the layers of the two ends already determine. Infer it. | rule-catalogue.md:606; scat.ttl:9-10 |
| SCAT-DRAFT/DONE-TABLE-LAYERS (pair) | Sem | simplify | Keep the one real check, "these two layers are not neighbours" (group to affordance). Swap/retype options disappear once type and direction are inferred. | rule-catalogue.md:621 |
| SCAT-DRAFT/DONE-TABLE-SECOND (pair) | Syntax | cut | Guards against a second `Edges told` heading; a coder who has one table will almost never write two. Fold into TABLE-HEADER at most. | rule-catalogue.md:636 |
| SCAT-DRAFT/DONE-TABLE-DUPLICATE (pair) | Syntax | cut | Merge duplicate rows silently; a repeat adds nothing. A warning is more than needed. | rule-catalogue.md:649 |
| SCAT-DRAFT/DONE-END-NOLINK (pair) | Syntax | simplify | The end must be one link. Useful; but one rule "every end links an existing node page" could carry all three END rules. | rule-catalogue.md:669 |
| SCAT-DRAFT/DONE-END-NOPAGE (pair) | Syntax | simplify | Same message as DANGLING-BODY restated for a row cell. | rule-catalogue.md:686 |
| SCAT-DRAFT/DONE-END-NOTNODE (pair) | Syntax | simplify | Same family; a narrative in a table cell. | rule-catalogue.md:700 |
| SCAT-DONE-REFUSED (an operation, not a check) | Pragmatic | keep | The one honest gate: you cannot say `done` with errors. But it only exists when `scat set-status` is used; setting `status: done` by hand in Obsidian (the chat path's only way) bypasses it, and `check` reports afterwards. | rule-catalogue.md:723-752; chat-path.md:~405 |
| Rule 4 "has no rule" (candidates) | Sem | keep | Right call: the tool does not judge content. Link-without-row is shown as a candidate in a view. | rule-catalogue.md:713-721 |
| Retired rule ids (about a dozen) | n/a | cut | Dead history in the live catalogue; move to the log. | rule-catalogue.md:171-188 |

### 2b. CLI commands (`uv run scat --help`; `src/scat_tools/cli.py`)

| Item | S/Sem/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| check | Syntax | keep | The conformance authority; the assistant runs it for you in chat. | cli.py:47 |
| status | Pragmatic | keep | "Where am I": counts by status. Should absorb NOEDGES/UNCODED as lines. | cli.py:58 |
| set-status | Pragmatic | simplify | Only useful for `draft`/`stub`; `done` is by hand on the chat path. | cli.py:69; server.py:61-90 |
| index | Pragmatic | cut | The template ships all five index Bases already; "never rewrites one". A first organiser never needs it. | cli.py:76; tpl-pin3/index/ |
| stub | Pragmatic | keep | Makes a legal page with right frontmatter. The core "right way is easy". | cli.py:81 |
| stub-links | Pragmatic | simplify | Creates node stubs for row ends; the assistant's `record_edge` already stubs a missing node (cli help for record-edge). Merge into record-edge. | cli.py:94, 100 |
| record-edge | Pragmatic | keep | The way an edge gets coded without hand-typing pipes. | cli.py:100 |
| remove-edge | Pragmatic | keep | The undo for the above. | cli.py:122 |
| merge | Pragmatic | keep | The pattern-forming act itself: fold two concrete nodes into one abstract one. But it is unreachable without a terminal on the chat path. | cli.py:136; server.py:138-155 |
| split-plan | Pragmatic | simplify | The inverse (one node becomes two). Writes nothing; the coder re-links by hand. Rare; fold into `evidence`. | cli.py:151; server.py:162 |
| fingerprint | Pragmatic | keep | What one narrative touches. Useful when reviewing one account. | cli.py:159 |
| edges (edge_table) | Pragmatic | simplify | One table per edge type; the `layered` view lists the same edges with the narratives that tell them (observed output, layered). | cli.py:171 |
| layered | Pragmatic | keep | The big picture across narratives: the synthesis view. | cli.py:182 |
| trace | Pragmatic | keep | Follow one concern up to the groups and down to the technologies. Useful and simple. | cli.py:200 |
| evidence | Pragmatic | keep | Every narrative that links a node, with the surrounding paragraph: the way back from pattern to concrete. | cli.py:215 |
| copy-share | Pragmatic | cut | Share of five-word runs a node page repeats from narratives; guards against pasting accounts into node pages. A non-programmer will not understand "5-word share 0.18"; the node-page norm covers it. | cli.py:225; copyshare.py:95 |
| review | Pragmatic | simplify | Finding candidate duplicates is the most useful pattern-finding aid in the tool (observed: proposed gated-approval ~ revert-with-history-kept). But it uses Jaccard, cosine and "twin rows" (review.py:155-230), so the explanation will not land. Show "these two nodes are told with the same neighbours". | cli.py:239; review.py:340 |
| attribution | Pragmatic | cut | Lists narratives by contributor. An Obsidian Base over `attributed_to` does it. | cli.py:247 |
| export-edges | Pragmatic | keep | The route out to a spreadsheet or a report; works in chat. | cli.py:254 |
| guide | Pragmatic | cut | Five stage guides (plan, capture, code, analyse, report) duplicate the docs site and the skill. | cli.py:264; guides/__init__.py |
| draw | Pragmatic | simplify | Pictures of fingerprint, layered, trace; needs an optional extra. Keep layered only. | cli.py:271 |

### 2c. MCP tools, prompts, resources (`src/scat_tools/mcp_server/`)

| Item | S/Sem/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| check, status | Syntax | keep | As CLI. | server.py:50, 58 |
| set_status | Pragmatic | simplify | Cannot set or leave `done`; so it only toggles stub/draft. | server.py:61-90 |
| stub, stub_links, record_edge, remove_edge | Pragmatic | keep / simplify | As CLI: merge stub_links into record_edge. | server.py:98, 106, 115, 126 |
| merge | Pragmatic | simplify | Plan only; applying is refused and the coder must run a terminal command. Either allow apply with a plan the coder confirms in chat, or drop the tool. | server.py:138-155 |
| split_plan | Pragmatic | simplify | See CLI. | server.py:162 |
| index | Pragmatic | cut | See CLI. | server.py:173 |
| fingerprint, layered, trace | Pragmatic | keep | Each takes `output` (table/plot/both) and `format`; a lot of options for a picture. Default to the table. | server.py:228, 256, 271; analysis.md:"Drawings" |
| edge_table | Pragmatic | simplify | See CLI. | server.py:245 |
| evidence | Pragmatic | keep | See CLI. | server.py:283 |
| copy_share | Pragmatic | cut | See CLI. | server.py:292 |
| review | Pragmatic | keep | See CLI. | server.py:302 |
| attribution | Pragmatic | cut | See CLI. | server.py:311 |
| export_edges | Pragmatic | keep | See CLI. | server.py:320 |
| which_stage, set_stage | Pragmatic | cut | With no stage recorded, every other call is refused until you name one (chat-path.md:450; lifecycle.md:22). Five stages the organiser must learn, stored in `lifecycle.toml`. A first-timer asking for a check should get a check. | stage.py:384-410; lifecycle.md:45-120 |
| Prompts: code-a-narrative | Pragmatic | keep | The coding loop in one prompt; the one a first organiser will use. | server.py:344 |
| Prompts: explain-a-problem | Pragmatic | keep | Plain-words rule explanations. | server.py:351 |
| Prompts: review-before-done | Pragmatic | simplify | Overlaps code-a-narrative step 4. | server.py:358 |
| Prompts: draft-a-node-page, fill-in-node-pages | Pragmatic | simplify | Node-page drafting is the labelling step but demands four-part pages (what it is / how told / where differs / what is thin), a lot of text per node. One prompt, shorter page. | server.py:365, 372; norms.md:38-62 |
| Prompts: look-for-duplicates | Pragmatic | keep | The pattern-merge loop. | server.py:379 |
| Resource: assistant-rules + stage guides (6 resources) | Pragmatic | simplify | One rules text; stage guides go with the stages. | server.py:387; stage.py:410-425 |

### 2d. Views and exports

| Item | S/Sem/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| Fingerprint view | Pragmatic | keep | One account's nodes and edges. | views.py:262 |
| Edge-table view | Pragmatic | simplify | Redundant with layered. | views.py:311 |
| Layered view (with orphans, candidates) | Pragmatic | keep | The synthesis view. Orphans and "links without rows" are the useful extras. | views.py; analysis.md |
| Trace view | Pragmatic | keep | | |
| Evidence view | Pragmatic | keep | | evidence.py:152 |
| Copy-share view | Pragmatic | cut | | copyshare.py:95 |
| Review view | Pragmatic | simplify | Fewer measures. | review.py:340 |
| Attribution view | Pragmatic | cut | | |
| Drawings | Pragmatic | simplify | Layered only; mark_narratives with nine colour/line combos is beyond need (analysis.md:"Drawings"). | draw.py |
| analysis.ipynb | Pragmatic | simplify | Needs a terminal and Jupyter (analysis.md:4, 34); chat-path users cannot use it. Replace by a generated Markdown page. | tpl-pin3/analysis.ipynb |
| Index Bases (5) | Pragmatic | keep | Obsidian-native, always current. The best thing in the vault for a non-programmer. | tpl-pin3/index/ |

### 2e. Ontology (`ontology/scat.ttl`)

| Item | S/Sem/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| owl:Ontology header, versionInfo | Syntax | keep | | scat.ttl:62 |
| scat:Group | Sem | keep | The stakeholder-group layer, capped. | scat.ttl:71 |
| scat:Concern | Sem | keep | The central pattern type: an interest several groups share. | scat.ttl:82 |
| scat:Affordance | Sem | keep | | scat.ttl:93 |
| scat:Technology | Sem | keep | | scat.ttl:105 |
| scat:EdgeType | Syntax | simplify | A class so tools need no copy of the three edge types (scat.ttl:121-126). If the type column goes, so does most of its reason. | scat.ttl:122 |
| scat:Heldby / Addresses / ProvidedBy | Sem | keep | The three bipartite relations. | scat.ttl:128, 140, 151 |
| scat:Narrative | Sem | keep | | scat.ttl:166 |
| scat:Contributor | Sem | cut | See top five. | scat.ttl:178 |
| scat:Index | Syntax | simplify | A page type for a generated file with no content. | scat.ttl:187 |
| scat:TableColumn and four column instances | Syntax | cut | Data that says which of four columns is which; the format is four columns in the docs. | scat.ttl:200-231 |
| scat:Field | Syntax | simplify | Machinery for generating models. | scat.ttl:238 |
| field-type, field-status, field-title | Syntax | keep | | scat.ttl:244-264 |
| field-description | Sem | keep for nodes | The node's label. | scat.ttl:265 |
| field-timeframe | Sem | cut (from the `done` gate) | Required to reach `done` yet read into the graph only (graph.py:673) and shown in the narrative index; no view filters on it. Make it an optional tag. | scat.ttl:272; graph.py:399, 673; tpl-pin3/index/narrative.base:14 |
| field-kind | Sem | simplify | Optional; changes only which columns a fingerprint draws. | scat.ttl:279 |
| field-attributed_to | Sem | cut | See top five. | scat.ttl:286 |
| scat:status, StatusValues, stub, draft, done | Sem | simplify | Three statuses: keep `stub`/`done`; `draft` is "not a step to pass through" in the project's own norms (norms.md:90-95). | scat.ttl:297-330 |
| Annotation vocabulary: carriesStatus, key, pageDescription, requiredField, optionalField, discouragedField, endpointOrder, verb, slug, tableHeading, tableColumns, cellHolds, mapsTo, targetType, requiredFrom, valueSet | Syntax | simplify | About 16 properties to describe a lint, one of them (`discouragedField`) "used by no type" (scat.ttl:358-361). Provenance triples (`source`, `authored`, `verification`) sit on every term and triple the file. | scat.ttl:333-410; 413-426 |

### 2f. Other significant features

| Item | S/Sem/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| Lifecycle stages (plan/capture/code/analyse/report), `lifecycle.toml`, stage-gated tools | Pragmatic | cut | See top five. | contracts/lifecycle.md:1-120; stage.py |
| Attribution modes (required/optional/disallowed) | Sem | simplify | See top five. | rule-catalogue.md:394-465; coding.md:644+ |
| Stakeholder group cap | Sem | keep | See rule above. | planning.md:16-24 |
| SCATLAB app, Colima, Tailscale Funnel, session key, container | Pragmatic | simplify | See top five. | chat-path.md:178-206, 128; deploy/scatlab.sh (713 lines) |
| Machine-interface contract and JSON schema (765 lines) with "fix as data" | Syntax | simplify | Built so assistants can apply a fix automatically; but the chat assistant quotes fixes as text (assistant.md:A14). The organiser never sees it. Costs builders, not the coder. | contracts/machine-interface.schema.json; rule-catalogue.md:5-8 |
| Assistant rules A1-A20 | Pragmatic | simplify | Twenty numbered rules, several saying "the coder does this by hand" (A8, A17, A19); the organiser sees them as friction (no paste-free drafting, no merge). Keep A7, A10, A11 only. | contracts/assistant.md |
| Four coding paths and walkthroughs (REPL, chat, IDE, local LLM) | Pragmatic | simplify | The persona uses one. Five other docs pages (ide, local-llm, leave-no-trace, path-pros-and-cons, coding-paths) are noise to her. | docs/*.md |
| Merge operation (598 lines) | Pragmatic | keep | The pattern-forming act. | ops/merge.py |
| The `done` check refusal and "Done is the coder's" | Pragmatic | keep | The sign-off is the coder's accountability. | MISSION.md |

---

## 3. Top five cuts or simplifications

**1. Infer the edge type; drop the `type` column.** The type of a row is fixed by the layers of its two ends (`scat.ttl:9-10`; `page-contracts.md:259`), so the person writes a word the tool can already compute. Today it earns a column, TABLE-TYPE, a retype option in TABLE-LAYERS, a swap option for direction, and a header check (`rule-catalogue.md:579-635`). Make a row `| [[from]] | [[to]] | note |` and let the tool sort the two ends by layer. This frees the coder from knowing three verbs and their slugs, from direction errors, and removes about six rule ids and two stub options from the vocabulary. The only layer rule left is "not neighbouring layers" (a group and an affordance).

**2. Cut the lifecycle stages.** `which_stage`/`set_stage`, `lifecycle.toml`, five per-stage tool lists and guides (`lifecycle.md:45-120`). With no stage recorded, every call is refused until the coder names one (`chat-path.md:450`; `lifecycle.md:22`). This is the sharpest case of "unnecessary and undesirable rules and machinery" in the tool: a first-timer's first "run a check" is refused. It gates tools by stage but the project's own text says "A predicate is advice: no predicate moves the stage" (`lifecycle.md:14`). It frees the organiser from five new words and from a refusal that is not about her data.

**3. Collapse the check catalogue to about a dozen conditions.** Today about 50 ids (`rule-catalogue.md:137-190`): seven frontmatter rules, three config rules, nine DRAFT/DONE pairs, four attribution rules. A reader of this table does not need to know which. Keep: unreadable page, missing required field, bad value, bad name, link to nothing, uncoded narrative, wrong layers, group cap, `done` refused. Drop the DRAFT/DONE doubling by making severity a function of status, cut TABLE-SECOND, TABLE-DUPLICATE, SUGGEST-CONFIG and MENTION, and take `timeframe` and the narrative `description` out of the `done` gate (`rule-catalogue.md:364`; `graph.py:673`: nothing downstream uses timeframe). This frees the coder from deciding "past, future or mixed" on every account just to reach `done`, a decision that changes no view.

**4. Make attribution one setting, not a page type.** Three modes create the `contributor` page type, the `attributed_to` link field, the mode rule, four ATTR rules, a mode-config rule, an `attribution` CLI command, an MCP tool, a stage entry and 70 lines of `coding.md` (`scat.ttl:178-190, 286-296`; `rule-catalogue.md:394-465`; `coding.md:644-717`). What the organiser needs is a promise she can keep: "no names" (enforced by SCAT-ATTR-DISALLOWED, which I would keep) or "names allowed" (plain text in the narrative). It frees the coder from contributor pages and a field that her event's consent policy may never need, and from `required` mode's blocked `done`.

**5. Take the set-up person out of the loop.** The chat path needs Colima (via Homebrew in Terminal), Tailscale, an HTTPS and Funnel switch, a built SCATLAB.app "the person who set this up builds" (`chat-path.md:178-179`, `195-206`), and a connector removed and re-added with a new key every chat run (`chat-path.md:128`). The mission says the organiser "must not be required to open a terminal" (MISSION.md, "Users and how they work"); installation requires one, the notebook requires one (`analysis.md:4`), and merge requires one (`chat-path.md:413`). I am unsure what is achievable (a local-only connector may not be possible with every chat), but the first release should either ship a prebuilt installer or say plainly that the organiser cannot do this alone. Freed: the organiser's day-one wall.

---

## 4. What is missing for the point of the exercise

1. **Any help with abstraction itself.** A grep of `docs/coding.md`, `docs/narratives.md` and `docs/analysis.md` finds no use of "abstract", "pattern" or "synthesis". The docs teach how to link and format; nothing says that a concern is "tools must come back in good order" and not "Dana's drill was late", or that a node should be reached by several accounts. The one signal that a node is a pattern, how many narratives tell it, appears only inside the layered view's "told by" lists; the view even says it "does not weigh a node by how many lines meet it" (`docs/analysis.md:` "Layered view"). Add one short guidance page and a plain recurrence table: node, layer, number of narratives and groups reaching it.
2. **Applying a merge from the chat path.** Merging concrete nodes into an abstract one is how patterns form, and the chat server refuses to apply it, so a no-terminal organiser is stuck at the exact moment of synthesis (`server.py:138-155`; `chat-path.md:413`).
3. **The views readable in Obsidian with no terminal.** Layered and trace come as chat data or a Jupyter notebook started from a terminal (`analysis.md:4`, `34`). A generated Markdown page of the layered view, rewritten by `export_edges`, would give a reader the whole picture where she already works.
