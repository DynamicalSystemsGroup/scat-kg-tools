# SCAT tooling audit: the qualitative researcher

Reviewer persona: years of coding field notes (grounded theory, thematic analysis, codebooks). Read-only. I read MISSION.md, ontology/scat.ttl, the rule catalogue, page contracts, the CLI and MCP surfaces, the skill, the lifecycle contract, deploy/README, one docs page (coding.md, partly) and the template vault. I ran `scat --help`, `scat check`, `scat review` and `scat guide code` against the template. I did not read the tests, the notebook, or most of the docs site, so claims about those are absent, not negative. Where I am unsure I say so.

Paths are relative to `/Users/z/Documents/GitHub/scat-wt/wp40-audit` unless marked `tpl:` (the template, `/Users/z/Documents/GitHub/scat-wt/tpl-pin3`).

---

## 1. Explanation

### What this is, in one paragraph

A person has field notes from workshops. They write each account up as one Markdown page (a *narrative*) and, inside the prose, link the things it names. Each linked thing is one of four fixed kinds: stakeholder **group**, **concern**, **affordance**, **technology** (MISSION.md:15-19, ontology/scat.ttl:71-118). They also list, in a small table at the bottom of the page, which pairs of neighbouring kinds the story connects: group holds concern, concern is addressed by affordance, affordance is provided by technology (tpl:narrative/groups-under-a-cap-pitch.md; ontology/scat.ttl:128-160). A Python tool reads the vault, builds a graph, checks it and draws views. Optional AI assistants help, but the coder keeps authority (MISSION.md:128-135, skills/scat-coding/SKILL.md:1-10).

In my terms: the four node types are a **fixed, four-level codebook**; a node page is a **code with a definition**; a narrative is a **coded document**; a link in the prose is a **coded segment**; a table row is an **explicit relation memo between two codes**. The graph is the code-by-document matrix plus a fixed relational structure.

### SYNTAX: what makes a vault well-formed

- **Page types and fields.** Six page types: four nodes, narrative, contributor (ontology/scat.ttl:71-198, page-contracts.md:1-30). Every page has `type`, `status`, `title`; `description` is required once `done`; narratives also need `timeframe` (past/future/mixed) once `done`; `kind` (scenario/architecture) is optional (ontology/scat.ttl:244-290, rule-catalogue.md:202-203).
- **Names.** Page file names are ASCII lower-case slugs, at most 64 characters, unique across the vault (page-contracts.md:70-80; SCAT-NAME at rule-catalogue.md:201).
- **Links.** A link must hit an exact slug; `[[Safety briefing]]` is a bad link even though Obsidian would follow it (page-contracts.md:100-103; SCAT-LINK-DANGLING-BODY, rule-catalogue.md:208).
- **The Edges-told table.** Heading `Edges told`, columns from/type/to/note, one row per edge, each end exactly one link to a node page of the layer the edge type demands, no duplicate rows, only one table (rule-catalogue.md:216-233, page-contracts.md section 4). Each of the table checks exists twice, once as a warning for `stub`/`draft` and once as an error for `done`.
- **Status.** stub, draft, done. Setting `done` is refused while the page would have any error (rule-catalogue.md:723-753).
- **Vault configuration.** `scat.toml` holds a cap on the number of group pages, an attribution mode (required/optional/disallowed), and a switch for link suggestions (tpl:scat.toml; rule-catalogue.md:209-212).
- **Links vs rows.** A link records only "this narrative mentions that node"; a row is the claim that the story tells an edge. Mismatches between the two are warnings while drafting and errors at `done` (MISSION.md:329-340, R-23).

### SEMANTICS: what the parts mean

- **Group** = a collective with a stake (SEBoK paraphrase), never an individual (ontology/scat.ttl:71-80). **Concern** = "any interest in a system" (82-91). **Affordance** = what a technology offers to people in an action situation (93-103). **Technology** = a discrete part of a system (105-114).
- **Edges** are directed, many-to-many, "at most one edge per pair", and each edge remembers every narrative that told it (ontology/scat.ttl:128-160; MISSION.md:196-201).
- **Fingerprint** = the nodes a narrative links plus the edges it tells; the **layered view** is the union of fingerprints (MISSION.md:203-207, 281-295).
- **Scenario vs architecture** (behavioural vs structural) and **past vs future** are marks on narratives only (MISSION.md:100-125).
- **Disagreement is held, not resolved.** Two groups can hold opposed concerns without the tool adjudicating (MISSION.md:127-140). One free-text "relationship annotation" between same-type pages is allowed and gets no meaning from the tool (MISSION.md:216-219; page-contracts.md:294-300; example at tpl:concern/anonymity.md "Pulls against [[attribution]]").
- **`done`** means the coder attests that the narrative interprets the notes appropriately; the tool checks only structure (MISSION.md:72-79).

### PRAGMATICS: how a coder gets from concrete to abstract

The designed loop is: interpret field notes, write the account, link names, record edges, check, review, set `done`, then look at views and return to the notes (MISSION.md:79-87, docs/coding.md:116-130).

The operations that serve it:

- **Make pages:** `stub`, `stub-links`, `index` (cli.py:81-99).
- **Record structure:** `record-edge`, `remove-edge`, `set-status` (cli.py:69, 100-135).
- **Consolidate codes:** `merge` (with a plan), `split-plan` (cli.py:136-158).
- **Read back what was coded:** `fingerprint`, `edges`, `layered`, `trace`, `evidence`, `export-edges`, `draw` (cli.py:159-214, 254-313).
- **Prompts to look:** `review` (possible duplicate nodes, pages whose accounts diverge), `copy-share` (node pages that repeat narrative text) (cli.py:225-253; review.py:1-25; copyshare.py:1-25).
- **Policy and orientation:** `attribution`, `guide` (cli.py:264).

What the coder actually does with it, once the vault is set up, is the following. They write prose with `[[links]]`. For each edge, they ask the tool to record a row, because they are told never to hand-write one (MISSION.md:150, skill A9). They run `check` and fix each message. Then they look at the views, and the node's `evidence` view shows every paragraph that links it. That evidence view is the best thing in the toolkit (more below).

### ARCHITECTURE and surfaces (plain terms)

- A Python package reads the vault into a graph, runs checks, produces typed results (a versioned JSON schema, contracts/machine-interface.schema.json), and exposes them three ways: REPL, `scat` CLI, MCP server (MISSION.md:128-135, R-8, R-16).
- The MCP server has 19 tools, 7 prompts-and-resources, a "stage" layer with `lifecycle.toml`, and a key-gated HTTP transport (server.py:44-330 and 335-395; stage.py:1-30; gate.py:1-30).
- `deploy/` carries a Dockerfile, a launcher script, and a menu-bar macOS app ("SCATLAB") that starts the server, uses Tailscale Funnel, stores a session key in the keychain and keeps the Mac awake (deploy/README.md:1-30).
- `skills/scat-coding/SKILL.md` and `src/scat_tools/guides/*.md` are the assistant's rules and stage guides.
- The template vault supplies the folders, a worked example, `analysis.ipynb`, and `scat.toml` (tpl: listing).

---

## 2. Verdict table

Verdicts are judged on one question: does this help a coder move from concrete accounts to abstract patterns, or does it pull them into bookkeeping? S/Se/P = syntax/semantics/pragmatics. "Pair" rules are DRAFT (warning) and DONE (error) twins and are judged together; the duplication itself is one finding (see section 3).

### 2a. Rules (contracts/rule-catalogue.md)

| Item | S/Se/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| SCAT-FM-PARSE | S | keep | A broken YAML block must be flagged or the page silently vanishes from the graph; no coding judgement involved. | rule-catalogue.md:194 |
| SCAT-FM-REQUIRED | S | keep | `status` and `title` only. Minimal. | rule-catalogue.md:195 |
| SCAT-FM-TYPE | S | keep | The page type is the whole dispatch mechanism; wrong type means wrong layer. | rule-catalogue.md:196 |
| SCAT-FM-STATUS | S | keep | Three values, cheap. | rule-catalogue.md:197 |
| SCAT-FM-TIMEFRAME | S/Se | simplify | Fine as a value check, but the field it guards is mandatory at `done` (below). Past/future is tagging for facilitation, not a step toward patterns. | rule-catalogue.md:198 |
| SCAT-FM-KIND | S/Se | keep | Optional field, value check only. Scenario vs architecture is a real analytic cut. | rule-catalogue.md:199 |
| SCAT-FM-SHAPE | S | keep | Cheap type check; no analytic cost. | rule-catalogue.md:200 |
| SCAT-NAME | S | simplify | ASCII-lower-case-slug names stop a coder naming a page in their own language or script; non-Latin titles must be given a hand-chosen name. The good in vivo label ("Walk-in customers") must be re-spelled. Keep uniqueness; drop the character restrictions to what Obsidian itself needs. Unsure whether Windows/Linux portability forced this; the contract says it does (page-contracts.md:70-80). | rule-catalogue.md:201 |
| SCAT-DONE-FIELD | S/P | simplify | Requires `description` on every node at `done`. A description is the codebook definition, which is real analytic work, but forcing it before `done` pushes the coder to write the definition at the moment they want to move on. Also requires `timeframe` on narratives. Keep the node `description`; make `timeframe` optional. | rule-catalogue.md:202; ontology/scat.ttl:265-278 |
| SCAT-DRAFT-FIELD | S | simplify | Warning twin of the above; a draft nags about fields it cannot have yet. A stub node should not be nagged for `timeframe` either (rule-catalogue.md:203 says it is). | rule-catalogue.md:203 |
| SCAT-ATTR-DISALLOWED | S/Se | cut | Attribution policy encoded as a rule, a page type, and a view. This is a consent decision about the project, not a step in coding. See section 3. | rule-catalogue.md:204 |
| SCAT-ATTR-LINK | S | cut | Same family. | rule-catalogue.md:205 |
| SCAT-DONE-ATTR | S | cut | Forces a coder in `required` mode to link a contributor page before they can mark a narrative done. | rule-catalogue.md:206 |
| SCAT-DRAFT-ATTR | S | cut | Warning twin. | rule-catalogue.md:207 |
| SCAT-LINK-DANGLING-BODY | S | keep | A link to nowhere breaks the code-and-retrieve loop. The fix offers `scat stub`, which is the right easy path. | rule-catalogue.md:208 |
| SCAT-CAP | S/Se | simplify | A cap on the number of groups (tpl:scat.toml sets 6) is a design choice to prevent identifiable individuals, stated by the chief engineer. As a coder I would rather see "group count" as a number in `status` than have an error block me while clustering. The rule is a privacy device, not an analytic one. Keep only if the project insists on the anonymity guarantee; downgrade to warning. | rule-catalogue.md:209; MISSION.md:178-181 |
| SCAT-MODE-CONFIG | S | cut | Goes with the attribution family. | rule-catalogue.md:210 |
| SCAT-CAP-CONFIG | S | simplify | Needed only if SCAT-CAP stays. | rule-catalogue.md:211 |
| SCAT-SUGGEST-CONFIG | S | cut | A config key, and a rule to validate it, for a feature (SCAT-MENTION) that is off by default. Make the suggestion a flag on `check`, as the fingerprint's `--candidates` already is, and drop this rule. | rule-catalogue.md:212 |
| SCAT-MENTION | S/P | keep | Suggests turning a plain-text mention of an existing code into a link. That is the nearest thing to auto-suggesting codes in text, which a coder wants in the middle of coding. Its type-aware silences (architecture does not get offered groups) are over-engineering, but the rule is useful. Off by default is wrong for the central coding act; sensible as a flag. | rule-catalogue.md:213, 535-545 |
| SCAT-NOEDGES | P | keep | Warning only, and genuinely useful: a narrative marked done with no relations is likely a skipped step. | rule-catalogue.md:214, 547-558 |
| SCAT-UNCODED | P | keep | Tells the coder a narrative is excluded from every view because it links nothing. Silent exclusion would be a worse failure. | rule-catalogue.md:215, 560-571 |
| SCAT-DRAFT/DONE-TABLE-HEADER | S | simplify | The header row of a hand-formatted table is checked for names, order, separator. This is table bookkeeping; `record-edge` writes the table anyway. If the tool writes the table, the check is only for hand edits. | rule-catalogue.md:216-217 |
| SCAT-DRAFT/DONE-TABLE-ROW | S | simplify | Four cells, closing `|`. Same. | rule-catalogue.md:218-219 |
| SCAT-DRAFT/DONE-TABLE-TYPE | S | simplify | The type cell must be a verb or slug of an edge type. Same. | rule-catalogue.md:220-221 |
| SCAT-DRAFT/DONE-TABLE-LAYERS | Se | keep | Group-holds-technology is a category error and should be caught. This is the one table rule that carries meaning. | rule-catalogue.md:222-223 |
| SCAT-DRAFT/DONE-TABLE-SECOND | S | cut | Forbids a second `Edges told` table or heading. A rule about a mistake the tool's own `record-edge` never makes. | rule-catalogue.md:224-225 |
| SCAT-DRAFT/DONE-TABLE-DUPLICATE | S | simplify | Duplicate rows in one narrative. Harmless to the graph, which keeps one edge per pair; could be silently merged. | rule-catalogue.md:226-227 |
| SCAT-DRAFT/DONE-END-NOLINK | S/P | simplify | A row end must be exactly one link. The R-23 mismatch idea is right, but see section 3: the root problem is that every edge is written twice. | rule-catalogue.md:228-229 |
| SCAT-DRAFT/DONE-END-NOPAGE | S | simplify | A row end links a name that is no page; the fix is `stub`, which is good, but the rule is the same as dangling link. Merge with LINK-DANGLING-BODY. | rule-catalogue.md:230-231 |
| SCAT-DRAFT/DONE-END-NOTNODE | Se | keep | A row end that links a narrative or contributor is a category error. Cheap and meaningful. | rule-catalogue.md:232-233 |
| SCAT-DONE-REFUSED | P | simplify | The refusal to set `done` while errors stand makes `done` a structural gate, which fits "tool owns conformance". But the coder's attestation (that the narrative fits the notes) is a different thing, and a refusal list of up to a dozen formatting errors blurs the two. Keep the refusal; keep the list short. | rule-catalogue.md:723-753 |
| Rule 4 has no rule (a narrative linking both ends with no row) | Se | keep | The decision not to infer an edge from co-mention is exactly right: the coder's row is the claim. Good. | rule-catalogue.md:713-721 |
| Retired rules (SCAT-FM-REQUIRED-LINK, ...-INDEXES, ...-CONFLICT-SELF and the rest) | S | n/a | Already removed; the catalogue still lists 14 as history, which makes the document longer than the live rule set. Move to the decision log. | rule-catalogue.md:177-188 |

### 2b. CLI commands (cli.py; `uv run scat --help`)

| Item | S/Se/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| `check` | S/P | keep | The linter. Three scopes (page, neighbourhood, vault) are one scope too many; page and vault suffice. | cli.py:47; MISSION.md:150-155 |
| `status` | P | keep | Counts of stub/draft/done: a progress view a coder wants. | cli.py:58 |
| `set-status` | P | keep | Needed. | cli.py:69 |
| `index` | P | simplify | Writes Obsidian Base files once. Could be done at vault creation, not a daily command. | cli.py:81 |
| `stub` | P | keep | Makes a node or narrative page. The right easy path. | cli.py:81-92 |
| `stub-links` | P | keep | Creates the node pages named by links: lets the coder write prose with links and let the pages follow. This is incremental coding done right. | cli.py:93-99 |
| `record-edge` | P | simplify | The only way a coder can add a row. "Never hand-write a row" is a rule that makes a one-line table edit into a command with four arguments. The coder already typed the two links in the same paragraph. See section 3. | cli.py:100-121; MISSION.md:150; skill A9 |
| `remove-edge` | P | simplify | Same. | cli.py:122-135 |
| `merge` | P | keep | Folding two codes into one is core coding practice (consolidation). The plan-first behaviour is good. | cli.py:136-150 |
| `split-plan` | P | simplify | Prints every narrative and row naming a page so the coder can split it by hand. It is a view, not a split; fold it into `evidence`. | cli.py:151-158 |
| `fingerprint` | P | keep | One narrative's codes and relations in four columns. Helps the coder check what they coded. | cli.py:159-170 |
| `edges` | P | keep | An edge table with its narratives: the code co-occurrence list a coder wants. | cli.py:171-181 |
| `layered` | P | keep | Union of fingerprints: the cross-narrative pattern. The main synthesis output. | cli.py:182-199 |
| `trace` | P | keep | Follow a code up to groups and down to technologies. A fair retrieval. | cli.py:200-214 |
| `evidence` | P | keep | Everything the vault says of one node: each linking paragraph, the sentence marked, edges, neighbours. This is code-and-retrieve, the heart of qualitative analysis. Best feature in the repo. | cli.py:215-224 |
| `copy-share` | P/Se | cut | Measures what share of a node page's five-word runs appear verbatim in a narrative. Presumably to push node pages away from copy-paste towards synthesis. It is a diagnostic about writing style, and it needs the coder to read a number before they read the pages. `evidence` already shows the passages. | cli.py:225-253; copyshare.py:1-25 |
| `review` | P/Se | simplify | Proposes duplicate nodes and pages whose narratives disagree. Duplicate detection is real work in coding (constant comparison). But the thresholds (0.5 Jaccard, "hub" = at least 4 neighbours and more than a tenth of all nodes, 0.3 pair divergence) are hidden machinery the coder cannot adjust, and I could not tell from the output when they bite. In the template it flagged two affordances because "a narrative tells the same row for both" (2x). That is a good prompt. Keep only the twin-row and shared-neighbour signals. Unsure how it behaves on a large vault. | cli.py:225-253; review.py:1-25; run on tpl-pin3 |
| `attribution` | P | cut | Views narratives by contributor. See attribution family. | cli.py (command list); MISSION.md:349-358 |
| `export-edges` | P | keep | CSV for analysis outside the tool. | cli.py:254-263 |
| `guide` | P | simplify | Prints a lifecycle-stage guide. Keep as plain help text; tie it to nothing else. | cli.py:264; guides/*.md |
| `draw` | P | keep | PNG/SVG of fingerprint, layered, trace (optional extra). | cli.py:270-313 |

### 2c. MCP tools, prompts, resources (mcp_server/server.py)

| Item | S/Se/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| tools `check`, `status`, `set_status`, `stub`, `stub_links`, `record_edge`, `remove_edge`, `merge`, `split_plan`, `index`, `fingerprint`, `edge_table`, `layered`, `trace`, `evidence`, `export_edges` | P | as the CLI | Same verdicts as the CLI twins. | server.py:44-330 |
| tool `copy_share` | P | cut | Same as the CLI. | server.py:292 |
| tool `review` | P | simplify | Same. | server.py:302 |
| tool `attribution` | P | cut | Same. | server.py:311 |
| tools `which_stage`, `set_stage` + `lifecycle.toml` + detects | P | cut | A five-stage lifecycle (plan, capture, code, analyse, report) enforced as refusals by the server, with a stage file kept in the vault. A coder knows what stage they are in. The cost is a new file, refusals that block tool calls, and a coder who must learn "stages". The design record says it was built to survive chat clients' memory limits, which is a chat-path problem, not a method need. | stage.py:1-30; lifecycle.md:1-60, 167-206; detects.py:1-30 |
| prompts `code-a-narrative`, `review-before-done`, `draft-a-node-page`, `explain-a-problem` | P | keep | Wrappers around the loop. They suit an assistant, not method. Fine. | server.py:343-372 |
| prompt `fill-in-node-pages` | P | keep | Walks stubs one by one. Matches how a coder fills definitions. | server.py:372 |
| prompt `look-for-duplicates` | P | simplify | Same as `review`. | server.py:379 |
| resource `scat://assistant-rules` | P | keep | Short rule set for the assistant. | server.py:387-395; SKILL.md |
| HTTP key gate | S | out of scope | Security of the transport. Not a method question. | gate.py:1-30 |
| deploy menu-bar app, Docker, Tailscale Funnel | P | out of scope | I cannot judge method fit; it exists for the chat path, so the coder's concern is "does it hide a terminal", which the README suggests. I note only that a coder would need Docker Desktop or Colima and a Tailscale account to code a narrative. | deploy/README.md:1-30 |

### 2d. Views

| Item | S/Se/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| Fingerprint view | P | keep | One document, its codes and relations. | MISSION.md:281-295 |
| Edge tables (3) | P | keep | Co-occurrence of codes across documents; exports to CSV. | MISSION.md:281-295 |
| Layered view | P | keep | Cross-document pattern. | MISSION.md:281-295 |
| Traces | P | keep | Follow a code across layers. | MISSION.md:281-295 |
| Candidates (`--candidates`: links with no row) | P | keep | Shows links the coder has not turned into a claim. Good: the tool does not decide for them. | cli.py:159-199; rule-catalogue.md:713-721 |
| Evidence | P | keep | See `evidence`. | cli.py:215 |
| Obsidian Base index per type | P | keep | Table of pages per type, auto-generated. | tpl: index/*.base; ontology/scat.ttl:187-198 |
| Notebook (`analysis.ipynb`) | P | unsure | Not read. It is a Python notebook; whether a qualitative coder will run Jupyter I cannot say. | tpl: listing; MISSION.md:281 |

### 2e. Ontology (ontology/scat.ttl)

| Item | S/Se/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| `scat:Group`, `Concern`, `Affordance`, `Technology` | Se | keep, with a caveat | Four fixed layers is a very opinionated codebook. It is the project's intent; it makes comparison easy and gives the pattern-finding its shape. But it also means a coder who sees a theme that is none of these has nowhere to put it (section 4). | ontology/scat.ttl:71-114 |
| `scat:EdgeType` | Se | keep | Holds the three edge types as data so no tool copies them. | ontology/scat.ttl:122-126 |
| `scat:Heldby` ("holds") | Se | keep | group holds concern. | ontology/scat.ttl:128-138 |
| `scat:Addresses` ("is addressed by") | Se | keep | concern is addressed by affordance. | ontology/scat.ttl:140-149 |
| `scat:ProvidedBy` ("is provided by") | Se | keep | affordance is provided by technology. Note the class is `Heldby` but the verb is "holds" (direction reversed against the name): a small trap for anyone reading the Turtle. | ontology/scat.ttl:128-160 |
| `scat:Narrative` | Se | keep | The one coded-document page. | ontology/scat.ttl:166-176 |
| `scat:Contributor` | Se | cut | A page type for a person, outside the graph, existing only in two of three attribution modes. | ontology/scat.ttl:178-186 |
| `scat:Index` | S | simplify | A class for a generated file with no frontmatter, so no vault page is of this type; `carriesStatus false` exists to say it has no status. Declare it in the contracts, not in the ontology. | ontology/scat.ttl:187-198 |
| `scat:TableColumn` + `column-type/from/to/note` | S | keep | Declares the four table columns as data; the `note` column is where a coder writes why an edge holds, which is real analytic value. | ontology/scat.ttl:200-236 |
| `scat:Field` + `field-type/status/title/description/timeframe/kind/attributed_to` | S/Se | simplify | Seven fields as classes. `attributed_to` goes with attribution (cut); `timeframe` becomes optional; the rest stay. | ontology/scat.ttl:238-293 |
| `scat:status`, `scat:StatusValues`, `scat:stub/draft/done` | Se | keep | Three-step status. | ontology/scat.ttl:297-330 |
| Annotation properties: `key`, `pageDescription`, `requiredField`, `optionalField`, `discouragedField`, `endpointOrder`, `verb`, `slug`, `tableHeading`, `tableColumns`, `cellHolds`, `mapsTo`, `targetType`, `requiredFrom`, `valueSet`, `carriesStatus` | S | keep, invisible | Machinery that lets tools be generated from one file (R-13). The coder never sees it. As long as it stays out of the coder's sight, no cost to them. | ontology/scat.ttl:333-420 |
| Provenance properties: `source`, `authored`, `verification` | Se | keep, invisible | Each term traces to a source or says it was authored. Most definitions are marked `unverified` (e.g. scat.ttl:78, 90, 101, 113): the standards were not read. That is honest but means "traced to authority" is thinner than MISSION.md:262-270 suggests. | ontology/scat.ttl:411-426 |
| Relationship annotation (not in ontology as a class; a line in the page body) | Se/P | keep | The one place where "pulls against" lives. No syntax, no rule, no view. Cheapest feature in the repo and the only place the model holds a tension. | page-contracts.md:294-300; tpl:concern/anonymity.md |

### 2f. Other significant features

| Item | S/Se/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| Three attribution modes + contributor pages + `attribution` view | S/Se/P | cut | See section 3. | MISSION.md:349-358; rule-catalogue.md:394-414 |
| Stakeholder-group cap | S/Se | simplify | See SCAT-CAP. | MISSION.md:178-181 |
| Three check scopes (page, one link away, vault) | S/P | simplify | Page and vault are enough; the middle scope is a performance device for a linter. | MISSION.md:150-155; rule-catalogue.md:42-50 |
| Machine-readable JSON for every result + schema | S | out of scope | Needed by the assistant and the server; invisible to the coder. | contracts/machine-interface.schema.json |
| Fix as data: every message offers "exact", "options", "slot", "advisory" or "manual" fixes | P | keep | A coder follows documentation literally. A fix that is a command is easy. | rule-catalogue.md:236-262 |
| Merge refusals (different types, contributor links, would give a narrative two rows) | P | keep | Safe consolidation. | cli.py:136-150 |
| "Edges told" table as a second record of what the prose already says | S/Se/P | simplify | See section 3. | page-contracts.md:10-14; MISSION.md:329-340 |
| Assistant skill rules A1-A20 | P | simplify | Twenty numbered SHALL/SHOULD/MAY rules. A1-A19 mostly say "the coder decides". Most of them reduce to three sentences. | skills/scat-coding/SKILL.md:20-60 |
| Done is the coder's attestation (not the tool's) | P | keep | The right split: a coder says "this reads right", the tool says "this is well-formed". | MISSION.md:72-79 |
| Facilitation guides and "past/future/mixed" marking | P | unsure | Not read; the mission says they live in docs only. | MISSION.md:112-125 |

---

## 3. Top five cuts or simplifications

**1. Collapse the prose-plus-table duplication (cut the second record of each edge).**
Right now a coder links `[[anonymity]]` and `[[groups-clustered-under-a-cap]]` in the prose, *and* an edge is a separate table row that the coder is told not to hand-write (tpl:narrative/groups-under-a-cap-pitch.md; MISSION.md:150; skill A9). Every R-23 rule (END-NOLINK/NOPAGE/NOTNODE pairs, TABLE-* rules, NOEDGES, `record-edge`, `remove-edge`, `stub-links`, the candidates list) exists to keep two records of the same claim in step. The mission itself calls this "a known pitfall" (MISSION.md:329-340). What I would do: let a coder state a relation where they say it, in the sentence, as one line such as `[[anonymity]] is addressed by [[groups-clustered-under-a-cap]]`, or let the table be the only edge record and treat prose links as plain mentions. One record, no reconciliation. This would free the coder from running a command each time they say "this group holds that concern", from fixing every mismatch before `done`, and from learning that a link is not an edge. I am unsure what the Obsidian experience costs here; the mission says it was reviewed in Obsidian, and I did not see the screenshots. The simplest honest option may be to keep the table as the only claim and let the tool validate it, and to make "link with no row" a harmless mention (as it is today for the candidates list).

**2. Drop the attribution machinery.**
Three modes, a sixth page type, five rules, a config key, a view and a CLI command (MISSION.md:349-358; rule-catalogue.md:204-211, 394-414; cli.py `attribution`). This is a consent policy, and the mission itself says the organiser decides what participants are told "up front" and that it is "the event's own agreed policy" (MISSION.md:171-176). A coder does not move from accounts to patterns by naming contributors; they move by comparing accounts. If a project needs contributor names, a free-text `attributed_to` line in the page is enough, and if it forbids them it forbids them in the project plan. This frees the coder from a config choice at set-up, a page type they will never open, and a rule family that blocks `done`.

**3. Remove the twin DRAFT/DONE rules; grade by a single rule and a single status test.**
Of the 24 table and end rules at rule-catalogue.md:216-233, each exists twice, once as a warning and once as an error (12 pairs). Both are documented, tested and worded. The only difference is severity at `done`. Make each rule fire once with an "error at done" flag. Then drop the rules that guard against a mistake `record-edge` cannot make: TABLE-SECOND, TABLE-HEADER, TABLE-ROW. This frees the coder from reading a catalogue 900 lines long to find out why a table line fails, and halves the surface the tests and docs must hold.

**4. Cut the lifecycle/stage layer from the server.**
`which_stage`, `set_stage`, `lifecycle.toml`, the detect predicates and refusal-by-stage (stage.py:1-30; lifecycle.md:1-60; detects.py:1-30). A coder knows they are capturing, coding or analysing. The server refusing tool calls because a file says the wrong stage is a way to let an assistant forget which stage it is in; it is not a method need. This frees the coder from a state file, a stage-setting step on first call, and a refusal they could meet mid-session.

**5. Make `timeframe` optional, drop `copy-share`, and shrink `review`.**
`timeframe` (past/future/mixed) is required at `done` on every narrative (ontology/scat.ttl:272-277; rule-catalogue.md:202). It is a tag for facilitation and not a step towards a pattern, and it adds a field to fill and a rule to satisfy on every narrative. `copy-share` is a style diagnostic whose useful output (which narratives a page repeats) is already in `evidence` (copyshare.py:1-25). `review` should keep the twin-row and shared-neighbour signals and drop the Jaccard/cosine/hub thresholds the coder cannot tune (review.py:1-25). This frees the coder from three things to read and one field to fill before they can look at their own data.

Honourable mentions: the `SCAT-NAME` slug rule (loses non-Latin and in vivo labels; rule-catalogue.md:201), the group cap as a blocking error, and the chat-path deployment app, which I have not judged.

---

## 4. What is missing for the point of the exercise (three items)

1. **A way to say why a pattern is a pattern: a memo.** The coder's job is to "identify patterns, label them, and organize the data according to them". The tool gives them fixed labels (four types) and a place to define each (the node `description`). It has no place for an analytic memo that says "I think these three concerns are one theme because...", and the only free text is a relationship annotation between two same-type pages. The node page body could be that place (it exists, and `evidence` shows what it cites), but nothing in the docs or the tool treats it as a memo. At least the guide should say so, and `review` should open from it.

2. **A grouping above the four types, or an honest statement that it is out of scope.** If a coder sees that "anonymity", "attribution" and "intent without drift" are one theme, there is nowhere to put a theme. The ontology is fixed for v0.1 and "evolving the ontology" is a non-goal (MISSION.md:345-347), which I understand, but the pattern-finding that matters (concerns clustering into larger concerns, affordances into capability families) happens above the nodes. A single optional "theme" field or list on a node, shown in the index and the layered view, would cover most of it. I am unsure whether the chief engineer would call this "adding detail" (it is the opposite: it is an abstraction step), so I record it as a gap and not a recommendation.

3. **A link from each narrative back to its field notes.** A narrative is "one account drawn from the field notes" (MISSION.md:60-62) and the coder confirms it matches (MISSION.md:79-87). The `evidence` view shows the narrative paragraph around a link, but the tool does not hold where in the notes the paragraph came from. The inputs are "outside the ontology" by design (MISSION.md:183-190). For a coder defending an abstract pattern, "which notes does this rest on" matters more than any check. An optional `source` field on a narrative, free text or a file link, with `evidence` showing it, would cost almost nothing.

---

## What I would keep without hesitation

The strengths are real and should not be traded away in the cuts. A narrative is one page and the coding happens in its own prose. Links are the coding act. Nothing is duplicated onto a second page (MISSION.md:329). `evidence` gives me code-and-retrieve. `merge` supports consolidation. Relations are held and never ranked, and an edge is the coder's claim and not an inference from co-mention (rule-catalogue.md:713-721). Disagreement is allowed to sit in the data. `done` is the coder's own word (MISSION.md:72-79). The tool never writes during a check (R-4). The tool offers the fix as a command. These are what a qualitative researcher would recognise as sound practice, and everything I cut above is the material that sits around them.
