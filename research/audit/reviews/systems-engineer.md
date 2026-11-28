# Audit: systems engineer (MBSE, 42010, state machines, interface contracts)

Reviewer persona: structure and lifecycle. Read-only. Repos: `wp40-audit` (tools) and `tpl-pin3` (template). I did not read work-packages, decisions or other audits. Where I am unsure I say so. "Row" in the table means one rule id or, for DRAFT/DONE pairs, one condition naming both ids (the pair is one condition at two severities, rule-catalogue.md:64, `Status behaviour` table).

Yardstick: the coder's job is synthesis, that is, finding patterns in concrete accounts, labelling them, and filing the data under them. Every feature is asked: does it help the coder label a pattern or see one, or does it only guard structure that nobody needed guarded? The two heuristics are "right way = easy way" and "as simple as possible but no simpler".

---

## 1. Explanation

### 1.1 In one paragraph

A SCAT vault is a git folder of Markdown pages. Concrete accounts are written as **narrative** pages. Inside a narrative, names of things are linked to **node** pages of four kinds (a layered chain: group, concern, affordance, technology). A table at the foot of the narrative, `Edges told`, says which neighbouring-layer pairs the account asserts. The tool derives a knowledge graph from those pages on every call and never stores it (architecture.md:33-38). Abstraction happens in two places: a node page is the label for a pattern that several accounts share, and `merge` folds two labels into one. Everything else is checking, viewing, and moving the project through stages.

### 1.2 Ontology (what exists)

- Four node classes, `Group`, `Concern`, `Affordance`, `Technology`, each a SKOS concept with one page per instance (ontology/scat.ttl:71-114).
- Three edge types as properties, `holds` (group to concern), `is addressed by` (concern to affordance), `is provided by` (affordance to technology). Each fixes the types of its two ends (ttl:128-160). An edge is not a page: it is a row, and the graph holds one edge per (type, from, to) naming every narrative that tells it (ttl:116-121; page-contracts.md:244-253).
- Three non-node page types: `Narrative`, `Contributor`, `Index` (ttl:166-195). The index is not a Markdown page, it is a generated Obsidian Base file (ttl:4-5, 187-195).
- A table-reading vocabulary (`TableColumn` with four columns, `tableHeading`, `tableColumns`, `cellHolds`; ttl:200-232) so the loader reads the table from the ontology alone.
- Seven fields: `type`, `status`, `title`, `description`, `timeframe`, `kind`, `attributed_to` (ttl:244-290).
- A page status ordered `stub`, `draft`, `done` (ttl:297-330).
- Vault configuration outside the ontology: `scat.toml` with `attribution` (required, optional, disallowed), `stakeholder_group_cap`, `link_suggestions` (page-contracts.md:525-557).

### 1.3 Architecture

Eleven modules M0 to M10 (architecture.md:51-82): ontology reader, loader, result and fix data, checks, mismatch, operations (the only writer), view generator, Python API and CLI, MCP server, notebook, template. MVC framing: model is ontology plus vault in git, views are built from a conformant model, control is Obsidian, git, CLI, MCP and IDE agents (architecture.md:24-36). Three actors: the coder owns interpretation, the tool owns conformance, the assistant holds no authority (architecture.md:40-49; assistant.md:3-6). Every tool result is data first, then text (architecture.md:53).

Tool surface (what I counted, not what the docs say): 21 CLI commands (`cli.py:47-264`, plus a `draw` group with three sub-drawings at `cli.py:270-330`); 19 MCP tools plus the two stage tools `which_stage` and `set_stage` (`mcp_server/server.py:50-320`, `mcp_server/stage.py:393-407`); 6 prompts and one `assistant-rules` resource (`server.py:343-391`); five guide resources, one per stage (`stage.py:410-423`); a menu-bar launcher app and Docker image for the chat path (`deploy/`, 1,130 lines). Checks are about 2,750 lines of Python (`src/scat_tools/checks/`).

### 1.4 The lifecycle and how it relates to the ontology and tools

Two independent state machines:
- **Status** (page level): `stub`, `draft`, `done`. Many changes per stage. Only the coder sets `done` (assistant.md:21; lifecycle.md:7-10).
- **Stage** (project level): `plan`, `capture`, `code`, `analyse`, `report`, plus `unknown` (lifecycle.md:30-37). Twelve transitions L1 to L12, each with a trigger, a predicate (detect or person) and a deciding role (lifecycle.md:126-142). Only one predicate is a detect (L5, "every narrative is done and the whole-vault check has no errors", lifecycle.md:134), and detects only advise (lifecycle.md:20).

Stage is stored in `lifecycle.toml` and read on every MCP call. The tool list is stable; an out-of-stage call is refused with a normal result (lifecycle.md:172-185; `stage.py:185-205`). Each stage lists allowed outputs, tools, prompts, skill sections (lifecycle.md:47-124). Relation to the ontology: the ontology has no stage class or property (the only "stage" strings in the TTL are "build-stage defaults" in provenance notes, ttl:282,375,380,385). Stage is a layer wrapped around the tools, not a property of the model. Stage reads status only through one counting predicate (L5).

### 1.5 Syntax, semantics, pragmatics

**SYNTAX (what makes a vault well-formed)**
- Page shape: UTF-8 Markdown, frontmatter with `type`, `status`, `title` (+ `description`, `timeframe` from `done`), unknown keys ignored (page-contracts.md:19-80).
- Names: ASCII slug, at most 64 characters, no reserved names, one name per vault, a 4-step derivation from the title (page-contracts.md:82-121; SCAT-NAME, rule-catalogue.md:352).
- Links: `[[exact-name]]` only; case differences are bad links (page-contracts.md:117-121; SCAT-LINK-DANGLING-BODY).
- The table: heading `Edges told`, four columns in order, one link per `from`/`to`, no duplicate rows, one table per narrative (page-contracts.md:147-243; rule-catalogue.md:573-712).
- Layer fit: each row's ends must be the node types its edge type fixes (SCAT-*-TABLE-LAYERS).
- Vault: group cap, attribution mode, optional link suggestions (rule-catalogue.md:484-534).
- Status grading: warnings before `done`, errors at `done` (rule-catalogue.md:64, "Status behaviour").
- Machine interface: schema version 3 JSON for every command (machine-interface.md:1-72, schema 765 lines).

**SEMANTICS (what the parts mean)**
- A node is a pattern label held in a layer; an edge is a pattern relation (page-contracts.md:244-253).
- An edge's status is derived: done when every narrative that tells it is done (page-contracts.md:249).
- A narrative is "coded" if it links at least one node page; uncoded narratives are excluded from every view (page-contracts.md:177-190; SCAT-UNCODED).
- `kind` (scenario or architecture) marks which layers a narrative mostly tells; `timeframe` marks past, future, mixed (ttl:272-285; page-contracts.md:236-243).
- A contributor is a person a narrative is attributed to, outside the four layers (ttl:178-186).
- A link without a row is a *candidate*, not an error (page-contracts.md:198-200).
- A relationship annotation (for example "pulls against") is body text that has no meaning to the tool (page-contracts.md:294-305).

**PRAGMATICS (how a person gets from concrete to abstract)**
1. Interpret the field notes (outside the graph; lifecycle.md:67-70).
2. Author the account in a narrative page, linking names.
3. `stub`/`stub-links` create missing node pages; `record-edge` adds a table row.
4. `check`, `fingerprint` (what this one account told) to review.
5. Move up a level: `evidence` (what every account says of one node), `copy-share` (is the node page just a pasted account?), `review` (pages that may be one node; pages whose accounts disagree), then `merge A B` to fold labels (cli.py:136; review.py:1-30; copyshare.py:1-25).
6. `layered`, `trace`, `edges`, `export-edges`, `draw` to read the whole graph (analyse and report).
7. `set-status done` is judged by the full rule set first (rule-catalogue.md:723-754), but only the coder, in Obsidian, may use it (server.py:67-90).

Pragmatics also include 20 docs pages, a skill, 6 prompts, a notebook, Docker and a menu-bar app.

---

## 2. Verdict table

Abbreviations: SYN, SEM, PRA. "Pairs" = DRAFT/DONE ids of one condition. Line refs: `rc` = contracts/rule-catalogue.md, `pc` = contracts/page-contracts.md, `ttl` = ontology/scat.ttl, `lc` = contracts/lifecycle.md, `cli` = src/scat_tools/cli.py, `srv` = src/scat_tools/mcp_server/server.py, `stg` = src/scat_tools/mcp_server/stage.py.

### 2.1 Rules (rule-catalogue.md)

| Item | S/S/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| SCAT-FM-PARSE | SYN | keep | Unreadable frontmatter blocks everything; needed for any tool. | rc:265 |
| SCAT-FM-REQUIRED | SYN | simplify | Same "required key" test as DONE-FIELD, different phase. One required-fields rule, severity from status. | rc:276, rc:364 |
| SCAT-FM-TYPE | SYN | simplify | One of four "value must be in the ontology's set" rules (TYPE, STATUS, TIMEFRAME, KIND). Derive from `valueSet` and write one rule. | rc:289, ttl:308 |
| SCAT-FM-STATUS | SYN | simplify | As above. | rc:302 |
| SCAT-FM-TIMEFRAME | SYN | cut | `timeframe` does not help draw a pattern; only evidence prints it. Drop the field's validation with the field. | rc:314; evidence.py:135,215 |
| SCAT-FM-KIND | SYN | cut | `kind` has no checked meaning; only draw and mention hard-code it (see finding 5). | rc:326; pc:236-238 |
| SCAT-FM-SHAPE | SYN | simplify | "text field must be one string" covers six fields; keep only for fields that stay. | rc:340 |
| SCAT-NAME | SYN | simplify | The name is the address and must be unique, so some rule is needed. ASCII-only 64-char slug plus a 4-step derivation is heavy for labelling patterns in any language. | rc:352; pc:82-121 |
| SCAT-DONE-FIELD / SCAT-DRAFT-FIELD (pair) | SYN | simplify | `description` required at done is useful for node pages (the pattern's label text). On narratives it is an index convenience. `timeframe` goes. | rc:364, 378 |
| Mode rule (4 ids below) | SEM | keep as one | Attribution is a consent gate that the project needs; but it is one sentence (rc:394-401) carried by four ids. | rc:394-466 |
| SCAT-ATTR-DISALLOWED | SEM | simplify | Fold into one `attribution` rule with three variants. | rc:415 |
| SCAT-ATTR-LINK | SYN | simplify | Same fold. | rc:428 |
| SCAT-DONE-ATTR / SCAT-DRAFT-ATTR (pair) | SEM | simplify | Same fold. | rc:443, 456 |
| SCAT-LINK-DANGLING-BODY | SYN | keep | A link to nothing breaks the graph; Obsidian already shows it, but the tool must agree. | rc:467 |
| SCAT-CAP | SEM | keep | The only rule that forces abstraction of the people: groups, not persons, under a cap. Closest the tool gets to a pattern constraint. | rc:484; pc:525-557 |
| SCAT-MODE-CONFIG | SYN | simplify | Three config rules (MODE, CAP, SUGGEST) check one small TOML file. One rule. | rc:497 |
| SCAT-CAP-CONFIG | SYN | simplify | As above. | rc:511 |
| SCAT-SUGGEST-CONFIG | SYN | cut | Goes with the cut below. | rc:522 |
| SCAT-MENTION | PRA | cut | Off by default, nags the coder to link plain-text mentions, and hard-codes kind-to-layer in code. Pushes detail, not abstraction. | rc:535; checks/mention.py:15 |
| SCAT-NOEDGES | SEM | simplify | A done narrative with no rows. Same signal as UNCODED for a narrative that tells nothing; merge into one "tells no edge" warning. | rc:547 |
| SCAT-UNCODED | SEM | keep | Silent exclusion from views would hide narratives; the warning is the right thing. | rc:560; pc:177-190 |
| SCAT-*-TABLE-HEADER (pair) | SYN | keep | The table is the one place the coder states edges; a malformed header makes it unreadable. | rc:579 |
| SCAT-*-TABLE-ROW (pair) | SYN | keep | Same. | rc:594 |
| SCAT-*-TABLE-TYPE (pair) | SYN | simplify | Edge-type vocabulary is in the ontology (ttl:128-160). Merge with LAYERS as one "row does not fit an edge type". | rc:606 |
| SCAT-*-TABLE-LAYERS (pair) | SYN | simplify | Restates `endpointOrder`; merge with TYPE and NOTNODE. | rc:621; ttl:128-160 |
| SCAT-*-TABLE-SECOND (pair) | SYN | simplify | A rule for a second table. Could be "only the first table is read" with no id; the tool already ignores it. | rc:636 |
| SCAT-*-TABLE-DUPLICATE (pair) | SYN | simplify | Idempotent graph (one edge per triple) already absorbs duplicates; a warning is enough, not paired ids. | rc:649 |
| SCAT-*-END-NOLINK (pair) | SYN | simplify | Merge three END rules into one "row end must be a link to a node page". | rc:669 |
| SCAT-*-END-NOPAGE (pair) | SYN | simplify | Same; overlaps DANGLING-BODY. | rc:686 |
| SCAT-*-END-NOTNODE (pair) | SYN | simplify | Same; overlaps TABLE-LAYERS. | rc:700 |
| SCAT-DONE-REFUSED (operation rule) | PRA | keep | The one point where the tool gates the coder's attestation by running the full contract. | rc:723-754 |
| Retired ids (list of 14) | n/a | cut | A tombstone list inside the catalogue; ids are "never reused" (rc:140) but this belongs in a changelog. | rc:143-190 |

### 2.2 CLI commands (all have MCP twins except `guide`, `draw`)

| Item | S/S/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| `check` | SYN | keep | Core. | cli:47 |
| `status` | PRA | keep | Counts and page list; needed to see where the coding stands. | cli:58 |
| `set-status` | PRA | keep | The `done` gate. Assistant may not use it for done; see finding 4. | cli:69; srv:67 |
| `index` | PRA | simplify | Generates Base files once; could be done by the template and never rerun. Needed only because ontology has an `Index` class. | cli:76; ttl:187 |
| `stub` | PRA | keep | Makes the right way easy. | cli:81; srv:98 |
| `stub-links` | PRA | keep | Same. | cli:94; srv:106 |
| `record-edge` | PRA | keep | The coder's actual act of coding an edge; also stubs nodes. | cli:100; srv:115 |
| `remove-edge` | PRA | keep | Undo of the above. | cli:122; srv:126 |
| `merge` | PRA | keep | The synthesis act: folding two labels into one pattern. The best-justified write in the tool. | cli:136; srv:138 |
| `split-plan` | PRA | keep (unsure) | Plan only, no apply; asymmetric with merge but splitting is judgement. | cli:151; srv:162 |
| `fingerprint` | PRA | keep | What one account told. | cli:159; srv:228 |
| `edges` (MCP `edge_table`) | PRA | keep | Edges by type with narratives, the table of patterns. | cli:171; srv:245 |
| `layered` | PRA | keep | The whole graph, the synthesis picture. | cli:182; srv:256 |
| `trace` | PRA | keep | Follow a pattern up and down layers. | cli:200; srv:271 |
| `evidence` | PRA | keep | From a pattern back to the accounts. Core of the concrete-to-abstract loop. | cli:215; srv:283; evidence.py:1-10 |
| `copy-share` | PRA | simplify | Detects node pages that merely paste a narrative, which is the failure the exercise fears. But five-word-run overlap is a narrow detector; keep as a section of `evidence`, not a command. | cli:225; copyshare.py:1-25 |
| `review` | PRA | keep | Duplicates and diverging pages: proposes where abstraction could be tightened. Thresholds hard-coded (0.5, 0.3, 4 narratives) are unverified. | cli:239; review.py:1-30 |
| `attribution` | PRA | simplify | A view of narratives by contributor; an Obsidian Base filter on `attributed_to` does the same job. | cli:247; views.py:480 |
| `export-edges` | PRA | keep | Output for reports. | cli:254; export.py:66 |
| `guide` | PRA | keep | Static per-stage guides; this is where the lifecycle should live. | cli:264; guides/ |
| `draw` (fingerprint, layered, trace) | PRA | simplify | An optional matplotlib extra, 647 lines, duplicating the data views as images; Obsidian graph/notebook may cover. | cli:270-330; draw.py |
| `--json` / schema v3 | SYN | simplify | Needed for the MCP server; 765-line schema and five edit actions is over-specified for 21 commands. | machine-interface.md; schema.json |

### 2.3 MCP tools, prompts, resources

| Item | S/S/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| 19 tools mirroring CLI | PRA | keep (as above) | Same verdicts as the CLI rows. | srv:50-320 |
| `which_stage` | PRA | cut | Only exists because stage is server state. | stg:393 |
| `set_stage` (with `by` signature) | PRA | cut | `by` is "not proof of consent" (lc:183); a signature that proves nothing is ceremony. | stg:407; lc:183 |
| Out-of-stage refusal | PRA | cut | The tool is refused rather than offered; a stable list plus a refusal makes the right way harder. | lc:181-182; stg:167-178 |
| Unknown-stage refusal | PRA | cut | A fresh vault refuses every tool until a stage is named (lc:22, 181); the template ships no `lifecycle.toml` (tpl-pin3 listing). | stg:154; lc:22 |
| `code-a-narrative` prompt | PRA | keep | The coding loop in one prompt. | srv:343 |
| `explain-a-problem` | PRA | keep | Helps with messages. | srv:350 |
| `review-before-done` | PRA | keep | Pre-done checklist. | srv:357 |
| `draft-a-node-page`, `fill-in-node-pages` | PRA | simplify | Two prompts for one act (drafting a node page); one prompt. | srv:364, 371 |
| `look-for-duplicates` | PRA | keep | Wraps `review` and `merge --plan`. | srv:378 |
| `assistant-rules` resource | PRA | simplify | Fourth copy of the authority statement; see finding 8. | srv:387; prompts.py:6 |
| Stage guide resources (5) | PRA | keep as docs | Guides are useful; resources keyed on server stage are not. | stg:410-423 |
| API key gate / loopback rule | PRA | keep | Needed if HTTP is served at all. | gate.py:1-53 |

### 2.4 Views

| Item | S/S/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| fingerprint, edges, layered, trace, evidence, review, export-edges | PRA | keep | See 2.2. | views.py:262-480 |
| copy-share view | PRA | simplify | See 2.2. | copyshare.py |
| attribution view | PRA | simplify | See 2.2. | views.py:480 |
| Candidates (links without a row) | SEM | keep | Shows what the account named but the coder has not yet related. | pc:198-200 |
| Excluded (uncoded) list in every view | SEM | simplify | A repeated block; one note suffices. | views.py:140; pc:177-190 |
| Derived edge status | SEM | keep | Gets `done` for free from the narratives, no extra state. | pc:249 |

### 2.5 Ontology classes, properties, fields, annotations

| Item | S/S/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| Group, Concern, Affordance, Technology | SEM | keep | The pattern layers; the core. | ttl:71-114 |
| EdgeType | SEM | keep | Carries the three edge types as data. | ttl:122 |
| Heldby, Addresses, ProvidedBy | SEM | keep | Three edge types, exactly the minimum chain. | ttl:128-160 |
| Narrative | SEM | keep | The concrete account. | ttl:166 |
| Contributor | SEM | simplify | A whole page type (plus `attributed_to`, mode, 4 rules) for consent-gated attribution; could be a plain-text field. | ttl:178; rc:394-466 |
| Index | SYN | cut | Not a page, has no fields, the loader ignores it (ttl:187-195); the only user of `carriesStatus`. | ttl:4-5, 187, 333 |
| TableColumn + four column individuals | SYN | simplify | Four columns carried as five ontology resources; a constant in the loader would do. | ttl:200-232 |
| Field class and seven field individuals | SYN | keep (class) | Needed to state required/optional once. | ttl:238 |
| field `type`, `status`, `title` | SYN | keep | Needed. | ttl:244-264 |
| field `description` | SEM | keep for nodes | The label text of a pattern. | ttl:265 |
| field `timeframe` | SEM | cut | Metadata about the account, not the pattern; required at `done` (ttl:272). | ttl:272 |
| field `kind` | SEM | cut | Not enforced; two hard-coded uses in code; the layers a narrative touches are visible in its table. | ttl:279; draw.py:63; mention.py:15 |
| field `attributed_to` | SEM | simplify | See Contributor. | ttl:286 |
| `scat:status` property | SEM | keep | Needed for the status machine. | ttl:297 |
| StatusValues, `stub`, `draft`, `done` | SEM | simplify (unsure) | `stub` and `draft` are graded identically except one silent/warning difference for `description` (rc:64 table). Two values (open, done) would carry the same attestation. | ttl:304-330 |
| `carriesStatus` | SYN | cut | Used only by Index. | ttl:333 |
| `key`, `pageDescription` | SYN | keep | Page-type dispatch. | ttl:338-345 |
| `requiredField`, `optionalField` | SYN | keep | Used by tbox.py. | ttl:348-355; tbox.py:213-214 |
| `discouragedField` | SYN | cut | Declared, used by no type (ttl:11 header). | ttl:358 |
| `endpointOrder`, `verb`, `slug` | SEM | keep | Edge type data. | ttl:363-375 |
| `tableHeading`, `tableColumns`, `cellHolds` | SYN | keep or simplify | Table reading as data; see TableColumn. | ttl:378-390 |
| `mapsTo` | SYN | cut | Not read by any code (grep of src). | ttl:393 |
| `targetType`, `requiredFrom`, `valueSet` | SYN | keep | Read by tbox.py. | ttl:398-410; tbox.py:129-143 |
| `source`, `authored`, `verification` (on every term) | n/a | cut from the TTL | Provenance of definitions, "unverified" on most; read by no code; research notes in the tool-facing file. | ttl:413-426 |

### 2.6 Other significant features

| Item | S/S/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| Stage machine (5 stages, 12 transitions, `lifecycle.toml`) | PRA | simplify | See cut 1. | lc:44-142 |
| Per-stage `tools`, `prompts`, `skill_sections`, `allowed_outputs`, `review` lists | PRA | cut | Triple-booked with the guides, the skill and the tool descriptions (test keeps them in step, lc:39-41). | lc:47-124 |
| Group cap in `scat.toml` | SEM | keep | See SCAT-CAP. | pc:525-557 |
| Attribution mode | SEM | keep (simplify) | Needed for consent; fewer ids. | rc:394-466 |
| `link_suggestions` key | PRA | cut | See SCAT-MENTION. | pc:547-557 |
| `templates_folder` key | SYN | simplify | One more key the tool must tolerate. | pc:545-546 |
| Relationship annotation | SEM | keep, but see missing 2 | Untyped, invisible to views by design (pc:294-305). | pc:294 |
| Notebook `analysis.ipynb` | PRA | keep | A reader of views for a desk coder. | tpl-pin3/analysis.ipynb |
| Chat-path launcher (`scatlab.sh` 713 lines, AppleScript 250, Docker) | PRA | simplify | An adapter for a different product (a Mac menu-bar server) living in the conformance tools repo; separate repo and release cadence. | deploy/README.md; wc |
| Skill `scat-coding` (163 lines) | PRA | simplify | Contains `assistant.md` verbatim plus loop; see finding 8. | skills/scat-coding/SKILL.md:12-58 |
| `docs/` (20 pages, `coding.md` 1,053, `chat-path.md` 600) | PRA | simplify (unsure) | Not read in full; sizes only. | wc |
| Template `AGENTS.md` and `scat-ide-setup` skill | PRA | keep | The IDE assistant's entry point; but see finding 4. | tpl-pin3/AGENTS.md |

---

## 3. Top five cuts or simplifications

1. **Replace the stage state machine with the guides.** Keep `scat guide <stage>` (cli:264) and the five guide texts; delete `lifecycle.toml`, `which_stage`, `set_stage` and its `by` slot, both refusals, and the per-stage tool/prompt/skill lists. This frees the coder from a fresh vault where every tool call is refused until a stage is named (lc:22, 181), from signing moves that prove nothing (lc:183), and from being told `merge` is "not offered in analyse" at the very point synthesis is done (finding 3). Keep the status machine; it is the one that carries an attestation.

2. **Halve the rule ids.** Collapse DRAFT/DONE pairs into one id whose severity follows status (the table at rc:64 already says so); fold TYPE/STATUS/TIMEFRAME/KIND into one "value not in the ontology's set"; fold TABLE-TYPE, -LAYERS, END-NOLINK, -NOPAGE, -NOTNODE into one "row does not fit its edge type"; fold the four attribution ids and three config ids. From roughly 40 ids to about 12. This frees the coder and the assistant from reading ids that restate one fact in five spellings, and frees the maintainers from the id-never-reused tombstones.

3. **Stop validating account metadata: cut `kind` and `timeframe`, and `SCAT-MENTION`/`link_suggestions`.** None helps draw a pattern. `kind` has code uses the ontology does not state (finding 5). `timeframe` is required at `done` and only printed by `evidence`. The mention rule nags the coder to add links, which is more detail not less. This frees the coder from three fields' worth of "done" blockers and a config key.

4. **Strip the ontology back to what the tools read.** Remove `scat:Index`, `carriesStatus`, `discouragedField`, `mapsTo`, and the `source`/`authored`/`verification` triples (move them to a research note). Replace the five TableColumn resources with a constant. This frees the reader of the "contract of record" from separating the model from the research notes (the TTL is 426 lines, 103 of its lines carry source, authored or verification triples), and removes seven terms that no code reads (tbox.py reads a subset: `key`, `pageDescription`, `requiredField`, `optionalField`, `valueSet`, `requiredFrom`, `targetType`, `endpointOrder`, `verb`, `slug`, `tableHeading`, `tableColumns`, `cellHolds`).

5. **State the assistant's authority once.** Today the same statement appears in `contracts/assistant.md`, `skills/scat-coding/SKILL.md:12-58` (a copy), `prompts.RULES` (prompts.py:6-29), every tool description's `_OWN` prefix (stage.py:34-37), the template `AGENTS.md`, and `scat-ide-setup`. Keep `assistant.md` as the source, generate or reference it elsewhere, and delete `contracts/architecture.md`'s twin `docs/architecture.md` (identical, `diff` reports no difference). This frees the coder from the places where the copies already disagree (finding 4) and the maintainers from keeping six in step.

(Honourable mention: the page-name slug machinery, pc:82-121. ASCII-only 64-character slugs with a four-step derivation constrain how patterns are labelled in a project whose people may not write in Latin letters. I would let the file name be the label and slug only on creation, but I am unsure what Obsidian-side constraints forced the rule.)

---

## 4. Missing (at most three)

1. **A recurrence view.** Synthesis is about what recurs. `edges` lists narratives per edge and `review` flags pages told by four or more narratives that diverge, but I found no view that ranks nodes and edges by how many narratives tell them or that lists nodes told by one narrative only (views.py exports: fingerprint, edge_table, layered, trace, attribution; evidence is per node). The guidance says a singleton "says so" (pc:403-405), but no tool shows it. Unsure: `layered` may already show counts; I did not run it on real data.
2. **A way to see tensions and matches in analysis.** The catalogue says "tensions, matches and gaps are for analysis" (rc:11), yet the one construct for tensions is an untyped body line that "stays out of every view" (pc:302-304). The analyse stage therefore has no tool to read the very thing its work is about.
3. **A link from a narrative to its field notes.** Edge to narrative is recorded, narrative to node is recorded, but notes are "outside the graph" (lc:67-70) and a narrative names its source in prose ("Source: the mission", tpl-pin3/narrative/*.md). The chain concrete note to account to pattern is broken at the first hop.

---

## 5. Structural findings

1. **Stage is enforced at three strengths.** MCP: enforced by refusal (lc:172-185; stg:185-205). IDE: advisory, "no server refuses a call" (tpl-pin3/.claude/skills/scat-ide-setup/SKILL.md:30). CLI: no mention of stage (grep of cli.py and checks: none except `guide`). The lifecycle contract claims "a stage names the work a person is doing, so the server can offer the tools that work needs" (lc:6-8), but the same vault's stage binds a chat coder and not an IDE coder. The template ships no `lifecycle.toml` (tpl-pin3 listing), so the first MCP call returns the unknown-stage refusal (lc:22).

2. **Two actor models.** The architecture has coder, tool, assistant (architecture.md:40-49; assistant.md:3-6). The lifecycle has organiser, coder and setup person (lc:21, 55-57) and transitions decided by the organiser on a predicate the coder states (L8, lc:141; L12 and L10 similarly). In the solo trial the two are one person (docs/flow.md:7). A role that decides L2, L3, L4, L7, L8, L9, L11 appears in no module's authority table.

3. **Analyse offers a tool whose result it forbids you to act on.** Analyse offers `review` (proposals that two pages may be one node) and `evidence`, but not `merge`, `split_plan` or the `look-for-duplicates` prompt (lc:96-108). Merge changes node pages, which analyse forbids (lc:97), so a coder who finds a duplicate while reading views must move to code via L6, with a detect predicate in the other direction (L5) that requires every narrative `done`. Synthesis, the point of the exercise, is the one write the stage rules push away from the reading.

4. **The assistant's `set_status` permission contradicts itself.** `assistant.md` A3 lists the permitted operations as "check, status, stub, stub links, record an edge, remove an edge" (assistant.md:17), omitting `set-status`. The template `AGENTS.md:12` says never run `uv run scat set-status`. The MCP server exposes `set_status` (srv:67), and the lifecycle lists it in code stage with "`set_status` (done is the coder's)" (lc:87-89). Four documents, three answers.

5. **`kind` has meaning in code that the ontology does not state.** The ontology gives `kind` a value set (ttl:279-285) and the page contract says "the tool does not check the layers of its rows against `kind`" (pc:238). But `draw.py:63-66` drops the group column for architectures and the technology column for scenarios, and `mention.py:15` uses the same mapping to suppress suggestions. A rule that lives in two files and in no contract is a leak.

6. **A contributor stub is both refused and created.** Page-contracts says the stub operation "refuses any other slug" than the four node types and `narrative`, and that a contributor page is "made by hand, or by the later operation the attribution mode gates" (pc:279-282); the catalogue's operation table says the same (rc:120). The CLI help and `stub.py:170` create contributor pages where the mode allows (cli:81-83). The implementation is probably the intent; the contract is stale. Related: the ontology calls `index` a page type with a `key` though it "is not a Markdown page" (ttl:4-5), so the ontology's "seven page types" and the checks' "six" (rc:147, 196) differ by definition.

7. **Rules repeat what the ontology already fixes, and the ontology states things no code reads.** TABLE-TYPE and TABLE-LAYERS restate `endpointOrder` and `verb`/`slug` (ttl:128-160; rc:606-635); four FM rules restate `valueSet`; the TABLE-HEADER rule restates `tableColumns` (ttl:166-175). Conversely `mapsTo`, `discouragedField`, and the provenance triples are declared and read by nothing (tbox.py:129-213; ttl:11, 393). The ontology is both under-used as the source for rules and over-stocked with unread terms.

8. **Same statement in many places, same word with several meanings.** Identical files: `contracts/architecture.md` and `docs/architecture.md` (diff silent). `assistant.md` body is copied into `SKILL.md:12-58`, `prompts.RULES`, and echoed in `AGENTS.md`. The lifecycle YAML is mirrored in guides and tool descriptions, held in step by a test (lc:39-41). Words: `kind` means the narrative's scenario/architecture (ttl:279), a result's kind `check`/`status`/`operation`/`view` (machine-interface.md:13), a fix's kind `exact`/`options`/... (rc:107-130), and a predicate's kind `detect`/`person` (lc:130). `mode` is the attribution mode and the assistant's "vault's mode" is the same word in the skill; `status` is a page's status, an edge's derived status, and, in a machine result, `status` the view. `stage` and `status` are kept apart by a paragraph of prose (lc:6-10), which is a sign that the vocabulary does not do the work.

---

Files read: README.md, MISSION.md (core heuristics and purpose sections), ontology/scat.ttl, contracts/{lifecycle,rule-catalogue,page-contracts,architecture,assistant,machine-interface}.md, src/scat_tools/{cli,tbox,views,review,copyshare,draw,export}.py, mcp_server/*, ops/stub.py, checks/mention.py, skills/scat-coding/SKILL.md, deploy/README.md, docs/flow.md, tpl-pin3 (AGENTS.md, README.md, scat.toml, narrative pages, ide-setup skill). Not read: work-packages, decisions, docs pages other than flow, most tests, `scatlab.sh`. I ran `uv run scat --help` only.
