# WP40 readout: SCAT audited against the point of the exercise

Four peer reviewers audited the repository on their own, each through one persona, before the ACE wrote anything. This
readout compares and contrasts their reports, and marks each claim it relies on as verified or refuted against the code
at `wp40/audit` (from `dev` d1c519c). Pointers name the report and section:

- **[Q]** [qual-researcher](reviews/qual-researcher.md): method fit, from someone who codes field notes;
- **[O]** [first-organiser](reviews/first-organiser.md): usability, from a first-time organiser on the chat path;
- **[M]** [minimalist-maintainer](reviews/minimalist-maintainer.md): the machinery that could go;
- **[K]** [kg-modeller](reviews/kg-modeller.md): the meta-model;
- **[S]** [systems-engineer](reviews/systems-engineer.md): structure, the lifecycle and the contracts. Added after decision 1
  (D-218), when the chief engineer noted the first four were "thinking like coders and user. none like systems engineers".

The test throughout is the chief engineer's (D-217): "the coders job is to identify patterns, label those patterns and
organize the data according to them. we provide a meta-model, tools, and guidance for that. ... we're not trying to add
detail we're moving the other way". Two heuristics: make the right way the easy way, and as simple as possible but no
simpler.

## 1. The verdict in one paragraph

All four reviewers find **the core sound and the fences around it too many**. The core covers:

- the four layers and three edge types;
- a narrative whose prose links are the coding act;
- `evidence` (code and retrieve);
- `merge` (folding two codes into one);
- relations held, never ranked;
- `done` as the coder's own word.

All four cut the lifecycle stage machine, and all four cut or shrink attribution. All four collapse the rule catalogue's
warning and error twins into one rule each, with severity set by status. Three of the four say what is *missing* is
help with the abstraction itself: a count of how many narratives reach a node, and guidance that says what a pattern is.

In short, we built a lot of conformance and coordination, and very little that helps a coder see or name a pattern.

## 2. What SCAT is: syntax, semantics, pragmatics

This is synthesized from [Q §1], [O §1], [M §1] and [K §1]. Where they differ, the difference is noted.

**Syntax (what a well-formed vault is).**
- **Pages.** Six page types: four kinds of node, the narrative and the contributor. A seventh, the index, is a generated
  Base file. Each page has YAML frontmatter with `type`, `status` and `title`.
  - Nodes need `description` at `done`.
  - Narratives need `timeframe` at `done` and may carry `kind`.
- **Names.** File names are unique ASCII slugs.
- **Links.** A link must land on an existing page.
- **The table.** A narrative holds one `Edges told` table with from, type, to and note. Each row's ends are links to
  node pages in adjacent layers.
- **Configuration.** `scat.toml` holds the group cap, the attribution mode and the suggestion switch.
- **Checks.** 40 live rule ids enforce all of this ([contracts/rule-catalogue.md:192-233], verified). 22 of them are
  11 warning/error twins.

**Semantics (what the parts mean).**
- **Four codes in layers:**
  - stakeholder (a collective with a stake, never a person; today the type key and folder are `group`);
  - concern (an interest);
  - affordance (what a technology offers);
  - technology (a part of the system).
- **Three edge types:** group holds concern, concern is addressed by affordance, affordance is provided by technology.
  An edge is the coder's claim. It is never inferred from two nodes being mentioned together ([rule-catalogue.md:713-721];
  [Q 2a], [K 2a]).
- **What the graph holds.** Each edge keeps every narrative that told it. A narrative's fingerprint is what it links and
  tells, and the layered view is the union of fingerprints.
- **The two marks.** Scenario/architecture and past/future mark narratives only.
- **`done`.** The coder attests that the narrative fits the notes. The tool checks structure only.
- **The ontology.** `ontology/scat.ttl` holds this meaning. It also holds a large annotation vocabulary that drives code
  generation, plus a source/authored/verification triple on every term ([K 2e]).

**Pragmatics (how a person gets from concrete accounts to abstract patterns).**
- **The loop:** write the account, link what it names, record the edges, check, set `done`, read the views, then
  consolidate codes and go back to the notes.
- **The operations that serve abstraction directly:**
  - `evidence`: every passage behind one code. All four reviewers keep it, and [Q] calls it "the best feature in the
    repo".
  - `merge`: folds two concrete codes into one.
  - `layered`: the cross-narrative picture.
  - `edges`: co-occurrence.
- **Everything else is bookkeeping or coordination:**
  - check scopes, fix objects, the table rules;
  - stages, attribution;
  - the deploy stack, the key gate.

**Architecture.**
- One Python package reaches the user four ways: a REPL, the `scat` CLI (21 commands), an MCP server (19 tools,
  6 prompts, a stage layer, a key gate) and the template's notebook.
- `deploy/` adds a menu-bar app, a container and Tailscale Funnel for the chat path.
- **Size:** src is 10,791 lines and the tests 28,307. The contracts include a 904-line rule catalogue, a 765-line JSON
  schema and a 206-line lifecycle contract (all verified by `wc`).

## 3. Where the four agree

Each claim below was checked; the evidence column is the ACE's.

| Finding | Q | O | M | K | Verified |
|---|---|---|---|---|---|
| Cut the lifecycle stages (`which_stage`, `set_stage`, `lifecycle.toml`, stage tool lists, guides tied to stages) | cut | cut | cut | cut | Yes. With no stage recorded, "every call is refused until you name one" (`docs/chat-path.md:450-451`). The contract itself says "A predicate is advice" (`contracts/lifecycle.md:20`). In today's inference.coop run, the stage gate refused a drawing the coder asked for. |
| Attribution is not a coding step: cut it, or reduce it to one setting | cut | one setting, keep DISALLOWED | yes/no | cut | Yes. Contributor class, `attributed_to`, the mode, ATTR-DISALLOWED/LINK, DONE/DRAFT-ATTR, MODE-CONFIG, `attribution` CLI and MCP tool, and coding.md §"Contributor pages" (`docs/coding.md:644`). 26 src files mention it. The shipped template sets `disallowed` (`tpl-pin3/scat.toml`). |
| One rule per condition, severity by status (no DRAFT/DONE twins) | yes | yes | yes | yes | Yes. 11 twin pairs, 22 of the 40 ids (rule-catalogue.md:202-233). |
| Cut TABLE-SECOND (a mistake `record-edge` cannot make) | cut | cut | cut | cut | Yes, by the rule's text. Whether `record-edge` can ever write a second table was not tested. |
| Cut MENTION and SUGGEST-CONFIG | keep MENTION as a flag | cut | cut | cut | Yes, the switch is off by default (`tpl-pin3/scat.toml` has no `link_suggestions`). |
| Take `timeframe` out of the `done` gate | optional | out of gate | simplify | simplify | **Partly.** [O]'s claim "nothing downstream uses timeframe" is refuted: `evidence` displays it (`evidence.py:135, 215`) and the index lists it (`ops/index.py:16`). True that no view computes on it. |
| Cut `copy-share` | cut | cut | cut | keep (unsure) | Yes. It is a style score; `evidence` shows the same passages. |
| Strip `review` to its plain signals; drop the hidden thresholds | simplify | simplify | simplify | simplify | Yes. Fixed Jaccard 0.5, cosine 0.5, hub ≥4 and >10%, re-read 0.3 (`review.py:11-23, 50`). |
| Ontology housekeeping: `Index`, `TableColumn`, `carriesStatus`, the per-term provenance out of the TTL | simplify | cut/simplify | cut | cut | Yes. `scat.ttl:1-12` itself says the index is no page of Markdown. |
| Keep: four layers, three edges, `check`, `stub`, `record-edge`, `set-status`, `merge --plan`, `evidence`, `layered`, the cap, `done` as the coder's word | keep | keep | keep | keep | n/a |

## 4. Where they differ

| Question | The positions | Note |
|---|---|---|
| **Is each edge recorded twice?** | [Q §3.1]: yes. Prose links and table rows are two records of one claim, and every R-23 rule exists to keep them in step; keep one. [M], [K] and [O] keep the table, with [K] and [O] slimming it. | MISSION G17 (`MISSION.md:329-335`) asks for the two to "stay in step" and calls it "a known pitfall". WP39, landing now, tightens that step: every row end must be linked in the account. [Q]'s point is the chief engineer's to settle. |
| **Drop the `type` column?** | [O §3.1], [K §3.1]: yes. A row's type is fixed by its ends' layers, so a row is two links and a note. [M] keeps TABLE-TYPE; [Q] calls it table bookkeeping. | Verified: `scat.ttl:10` says "A row's type is fixed by the layers of its ends." [K] is unsure whether the column helps a reader in Obsidian. |
| **Fixes as data (fix kinds, edit objects, the JSON schema)** | [M §3.2]: cut, the largest source of lock-step change. [K]: keep, narrower. [O]: simplify. [Q]: keep, because "a fix that is a command is easy". | The assistant and the server rely on the JSON. Cutting it changes the machine interface. |
| **`stub-links`, `split-plan`, `fingerprint`, `trace`** | [M] and [K] fold them into `layered` and `evidence`. [Q] keeps `stub-links` ("incremental coding done right"). | Verdicts by command are in §6. |
| **The group cap as a blocking error** | [Q]: downgrade it to a count. [O], [M], [K]: keep. | A privacy device, not an analytic one (MISSION.md:178-181). |
| **SCAT-NAME's ASCII slugs** | [Q]: they lose in vivo and non-Latin labels. [O] and [M] keep them; [K] simplifies. | `title` keeps the label either way. |
| **The chat-path install** | [O §3.5]: a terminal, Colima, Tailscale and a new key every run contradict "must not be required to open a terminal". The others don't judge it. | Verified: the connector must be removed and re-added with a new key every run (`docs/chat-path.md:127-128`), and the notebook starts from a terminal (`docs/analysis.md:4`). This session hit the stale key today. |

## 4a. The systems engineer's view [S]

[S] also puts the stage machine first among its cuts ([S §3.1]). D-218 keeps it. [S]'s reasons are different from the
other four, though: they are failures of the structure to be applied the same way everywhere, which is exactly what
D-218 says the structure is for. Its structural findings ([S §5]), each checked:

| # | Finding | Verified |
|---|---|---|
| S1 | The stage is enforced at three strengths: the MCP server refuses, the IDE path is advisory, the CLI has none; the template ships no `lifecycle.toml`, so a new vault's first MCP call is refused as unknown | Yes for the template: `tpl-pin3/lifecycle.toml` does not exist. |
| S2 | Two actor models: the architecture has coder, tool and assistant; the lifecycle adds organiser and setup person, and the organiser, who decides most moves, is in no authority table | Yes: "organiser" appears 0 times in `contracts/assistant.md`, once in `contracts/architecture.md`. |
| S3 | `analyse` offers `review` and `evidence` but not `merge`, `split_plan` or `look-for-duplicates`, so synthesis needs a move back to `code` | Yes (`contracts/lifecycle.md:96-108`). |
| S4 | Whether the assistant may set status has three answers: A3 omits it, the template's AGENTS.md forbids it, the server exposes it and `code` offers it | Yes (`contracts/assistant.md:17`; `tpl-pin3/AGENTS.md:12`; `mcp_server/server.py:67`). |
| S5 | `kind` has meaning in code that no contract states: drawings drop a layer by kind, and the mention rule discourages a layer by kind | Yes (`draw.py:63-66`, `checks/mention.py:12-14`). |
| S6 | Contributor stub: the page contract and the catalogue say `stub` refuses a contributor; the CLI help says it makes one where the mode allows | Yes (`contracts/page-contracts.md:278-280`; `cli.py:83`). |
| S7 | Rules restate what the ontology already fixes (TABLE-TYPE, TABLE-LAYERS and the value rules vs `endpointOrder`, `verb`/`slug`, `valueSet`); `mapsTo` and `discouragedField` are read by no code | Yes for the second half: `mapsTo` and `discouragedField` have no reader in `src/`. |
| S8 | Duplicated text and overloaded words: `contracts/architecture.md` is identical to `docs/architecture.md`; the assistant rules are copied into the skill and the prompts; `kind` has four meanings | Yes: the two `architecture.md` are identical (`diff -q`). |

[S]'s other cuts agree with the rest: one id per rule with severity by status, folding the row rules into "the row does
not fit its edge type" ([S §3.2]); stop validating `kind` and `timeframe` and cut MENTION ([S §3.3]); strip the TTL to
what the code reads ([S §3.4]); state the assistant's authority once ([S §3.5]). Its missing items add a way to read
tensions in `analyse` to the recurrence view and the link to field notes.

## 5. What is missing for the point of the exercise

| Gap | Raised by | Verified |
|---|---|---|
| **Recurrence**: per node, how many narratives (and groups) reach it. A pattern is what recurs. | [O §4.1], [M §4.1], [K §4.3] | Yes, absent. No count in `views.py`, and `docs/analysis.md:19` says the layered view "does not weigh a node by how many lines meet it". |
| **Guidance on abstraction itself**: what a pattern is, and naming a concern at the right level. | [O §4.1], [Q §4.1] | Yes. "abstract", "pattern" and "synthesis" appear 0 times in `docs/coding.md`, `docs/narratives.md` and `docs/analysis.md`. |
| **A step above a node** (a theme, or `skos:broader`) without destroying the concrete node | [Q §4.2], [K §4.1] | Yes. The only move is `merge`, which deletes A and carries its body into B (`ops/merge.py:4, 271`), the carry-over D-216 rejected. |
| **Rename a node** (the simplest abstraction move: "broken drill" becomes "unsafe equipment") | [M §4.3] | Yes, there is no rename operation in `ops/` (only a `rename_file` fix edit, `checks/fixes.py:69`). |
| **A narrative's link back to its field notes** | [Q §4.3], [K §4.2] | Yes, absent by design (inputs are outside the ontology). |
| **Row notes visible in the views** | [M §4.2], unsure | Partly. The note reaches `evidence` (`evidence.py:183`) but not the edge tables or the layered view (`views.py` has no `note`). |
| **Applying a merge from the chat path** | [O §4.2] | Yes, refused by design: "this server never applies a merge: that is the coder's act" (`mcp_server/server.py:150`). |

**Bearing on C22 (D-216).** No reviewer asked for more pages. [K]'s answer to abstraction is a relation between nodes
(`skos:broader`), not a page. C22's reified link page is still the chief engineer's decision, but it should be weighed
against this.

## 6. Verdict table

**Columns:**
- **S/Se/P:** syntax, semantics or pragmatics.
- **Q/O/M/K:** each of the first four reviewers' verdicts: k = keep, s = simplify, c = cut, ? = unsure, – = not judged.
  The systems engineer's verdicts are in [its own table](reviews/systems-engineer.md).
- **Outcome:** what the chief engineer decided (D-218 to D-236). Where no decision touched an item, it stays as built.
- **Reason:** why the item earns its place, or why it changes. It is stated in terms of the purpose (D-230): the people
  at the events supply the detail, and coding organizes it into common, interrelated patterns. Most rows also test one
  of the two heuristics, the right way being the easy way and as simple as possible but no simpler.

### 6a. Rules (contracts/rule-catalogue.md)

| Item | S/Se/P | Q | O | M | K | Outcome | Reason |
|---|---|---|---|---|---|---|---|
| SCAT-FM-PARSE | S | k | s | k | k | keep | A page that cannot be read drops out of the graph silently, and a pattern can't rest on a page the graph never saw. |
| SCAT-FM-REQUIRED | S | k | k | s | s | keep | `type`, `status` and `title` are what place a page in the model. Without them a page has no layer and no state. |
| SCAT-FM-TYPE | S | k | s | s | s | keep | The type puts a code in its layer. A wrong type puts a concern where a group belongs and breaks every pattern drawn across layers. |
| SCAT-FM-STATUS | S | k | s | s | s | keep | Three values keep the coder's state of work legible; it costs nothing. |
| SCAT-FM-TIMEFRAME | S | s | s | s | s | becomes the value check of the actual / hypothetical / unclassified filter (D-224) | A filter must hold known values to separate conjecture from what could be verified. It no longer gates `done`. |
| SCAT-FM-KIND | S | k | s | s | s | keep, as a filter's value check (D-224) | Scenario and architecture are a filter on the accounts. They no longer change any output silently. |
| SCAT-FM-SHAPE | S | k | s | c | s | keep | A field of the wrong shape (a list for a string) is misread by every view. The check is cheap. |
| SCAT-NAME | S | s | k | k | s | keep (D-228) | Slugs keep names portable and unique. The `title` keeps the label as people said it. |
| SCAT-DONE-FIELD / SCAT-DRAFT-FIELD | S | s | s | k/c | s | one id, severity by status (D-223); `timeframe` out of the gate (D-224) | A node's `description` is its definition, the abstraction the coder commits to. Asking for it at `done` is asking for the synthesis. |
| SCAT-ATTR-DISALLOWED | S | c | k | s | c | keep (D-219) | Keeps the promise to activists that no account is tied to a named person. |
| SCAT-ATTR-LINK | S | c | c | s | c | keep (D-219) | Keeps attribution pointing at real contributor pages where the community wants contributions tracked. |
| SCAT-DONE-ATTR / SCAT-DRAFT-ATTR | S | c | c | c | c | keep (D-219), one id, severity by status (D-223) | In the required mode a done narrative must say whose account it is. That is the promise the organiser made. |
| SCAT-LINK-DANGLING-BODY | S | k | k | k | k | keep | A link to nowhere breaks the path from a code back to its accounts. |
| SCAT-CAP | Se | s | k | k | k | keep | The cap forces groups to be clusters, not individuals: an abstraction step, and a privacy guarantee. |
| SCAT-MODE-CONFIG | S | c | s | s | c | keep (D-219) | Without a declared mode the vault can't tell which attribution promise it keeps. |
| SCAT-CAP-CONFIG | S | s | s | s | s | keep | The cap must be readable to be enforced. |
| SCAT-SUGGEST-CONFIG | S | c | c | c | c | cut (D-223) | It validated a switch for a rule nobody turned on. |
| SCAT-MENTION | P | k | c | c | c | cut (D-223) | It suggested more links. Under D-220 prose links are optional, and coding is the table, not more linking. |
| SCAT-NOEDGES | P | k | s | s | k | keep | A done narrative with no rows has contributed nothing to any pattern, and is likely a skipped step. |
| SCAT-UNCODED | P | k | k | k | s | keep | An account that links nothing is excluded from every view. Silent exclusion would bias the synthesis. |
| SCAT-DRAFT-TABLE-HEADER / SCAT-DONE-TABLE-HEADER | S | s | s | s | s | one id, severity by status (D-223) | The table is the coding of record (D-220), so it must be readable. One rule is enough. |
| SCAT-DRAFT-TABLE-ROW / SCAT-DONE-TABLE-ROW | S | s | s | k | s | one id, severity by status (D-223) | A row that can't be read is a claim lost. |
| SCAT-DRAFT-TABLE-TYPE / SCAT-DONE-TABLE-TYPE | S | s | c | k | c | keep the column (D-222), one id (D-223) | The type names what the pair means ("holds", "is addressed by"). It is the structure the coder reads. |
| SCAT-DRAFT-TABLE-LAYERS / SCAT-DONE-TABLE-LAYERS | Se | k | s | k | s | one id, severity by status (D-223) | A group holding a technology is a category error. The ontology's layers are what make patterns comparable. |
| SCAT-DRAFT-TABLE-SECOND / SCAT-DONE-TABLE-SECOND | S | c | c | c | c | cut (D-223) | It guarded a mistake the tool's own `record-edge` never makes. |
| SCAT-DRAFT-TABLE-DUPLICATE / SCAT-DONE-TABLE-DUPLICATE | S | s | c | c | c | cut (D-223) | The graph already keeps one edge per pair. A duplicate row changes no pattern. |
| SCAT-DRAFT-END-NOLINK / SCAT-DONE-END-NOLINK | S | s | s | s | s | one id, severity by status (D-223) | Each end of a claim must name a code, or the claim joins nothing. |
| SCAT-DRAFT-END-NOPAGE / SCAT-DONE-END-NOPAGE | S | s | s | s | s | one id, severity by status (D-223) | A claim about a code with no page has no definition behind it. The fix (`stub`) is the easy way. |
| SCAT-DRAFT-END-NOTNODE / SCAT-DONE-END-NOTNODE | Se | k | s | s | s | one id, severity by status (D-223) | Only the four node types are codes. A row ending at a narrative is a category error. |
| Prose link not in the table (WP39 amendment 1) | Se | – | – | – | – | new, one id, warning in draft, error at done (D-220, D-221) | The table is the coding of record. A linked word the table doesn't hold would read as coding when it is not. |
| SCAT-DONE-REFUSED | P | s | k | k | k | keep | `done` is the coder's attestation. Refusing it while errors stand keeps conformance and judgement apart. |
| Retired-ids list (rule-catalogue.md:177-188) | – | c | c | c | – | move to the log (D-236) | History, not a rule. It lengthens the catalogue the coder reads. |
| Structured fixes (fix kinds, edit actions) | P | k | s | c | k | keep; item-by-item review (D-226) | Every guard comes with a remediation, which makes the right way the easy way for the coder and the assistant. |

### 6b. CLI commands (and the MCP tool of the same name)

| Item | S/Se/P | Q | O | M | K | Outcome | Reason |
|---|---|---|---|---|---|---|---|
| `check` / check | S, P | k | k | k | k | keep | Conformance only, so the coder's attention goes to interpretation. |
| `status` / status | P | k | k | k | s | keep | Shows what is still stub or draft: where the synthesis isn't finished. |
| `set-status` / set_status | P | k | s | k | k | keep | The coder's attestation, recorded. Who may call it is settled in the consistency package (D-236). |
| `index` / index | P | s | c | s | s | keep (D-227) | Gives Obsidian one table per code type, a quick look across all codes of a layer. |
| `stub` / stub | P | k | k | k | k | keep | One easy way to name a new code. |
| `stub-links` / stub_links | P | k | s | s | c | keep (D-227) | Lets the coder name codes in rows first and fill pages after: incremental coding. |
| `record-edge` / record_edge | P | s | k | k | k | keep | Records the coder's claim in the table of record without hand-writing structure. |
| `remove-edge` / remove_edge | P | s | k | c | k | keep | Withdrawing a claim is part of revising a synthesis. |
| `merge` / merge | P | k | k | k | k | keep; no carried body, optional link pages (C22, D-233); in `synthesise` (D-235) | Folding two concrete codes into one is the core abstraction move. |
| `split-plan` / split_plan | P | s | s | s | c | renamed `where-used` (D-227); in `synthesise` (D-235) | Shows every place a code is used, so the coder can see when one name covers two structures. |
| `rename` (new) | P | – | – | k | – | add (D-230) | Renaming a code ("broken drill" to "unsafe equipment") is the simplest abstraction move. |
| `fingerprint` / fingerprint | P | k | k | s | s | keep (D-227) | One account's codes: did I code this account the way I read it? |
| `edges` / edge_table | P | k | s | k | k | keep | Which claims recur across accounts and which rest on one. |
| `layered` / layered | P | k | k | k | k | keep | The cross-account picture: the synthesis seen whole. |
| `trace` / trace | P | k | k | s | s | keep (D-227) | For one concern: who holds it, and what addresses it. |
| `evidence` / evidence | P | k | k | k | k | keep | Code and retrieve: what a code rests on, the basis for its definition. |
| recurrence view (new) | P | – | k | k | k | add (D-229) | A pattern is what recurs. It counts the narratives and groups that reach each code and marks the singletons. |
| `copy-share` / copy_share | P | c | c | c | k? | cut (D-225) | It scored writing style. `evidence` already shows the passages. |
| `review` / review | P | s | s | s | s | plain signals only (D-225) | Prompts the coder to compare codes that may be one, without scores the coder can't see. |
| `attribution` / attribution | P | c | c | c | c | keep (D-219) | Shows whose accounts a pattern rests on, where the community wants that. |
| `export-edges` / export_edges | P | k | k | s | k | keep | Hands the coded structure to other analysis. |
| `guide` | P | s | c | c | k | keep (D-218) | States each stage's work, part of the scaffolding. |
| `draw` | P | k | s | s | s | keep; no layer dropped by `kind` (D-224) | Pictures of the views for a report. |
| MCP which_stage, set_stage | P | c | c | c | c | keep (D-218); same strength on every path (D-234) | The stage machine stabilises what the assistant offers at each point of the work. |
| MCP prompts (code-a-narrative, explain-a-problem, review-before-done, draft-a-node-page, fill-in-node-pages, look-for-duplicates) | P | k | s | s | s | keep; guidance on the note slots added (D-233) | Each starts one step of the loop the stage offers. |
| MCP resource assistant-rules; SKILL A1-A20 | P | s | s | c | s | one copy (D-236) | One statement of the assistant's limits, so the copies can't disagree. |
| HTTP key gate | S | – | – | s | – | keep | Security of the chat path. Not a coding question. |

### 6c. Views

| Item | S/Se/P | Q | O | M | K | Outcome | Reason |
|---|---|---|---|---|---|---|---|
| Fingerprint | P | k | k | s | s | keep | One account, coded. |
| Edge tables | P | k | s | k | k | keep | Recurring claims. |
| Layered (with candidates) | P | k | k | k | k | keep; filters by the marks (D-224) | The whole synthesis. Candidates show linked pairs not yet claimed. |
| Trace | P | k | k | s | s | keep | One code's chain across layers. |
| Evidence | P | k | k | k | k | keep | What a code rests on. |
| Recurrence (new) | P | – | k | k | k | add (D-229) | How widely a pattern recurs. |
| Copy-share | P | c | c | c | k? | cut (D-225) | A style score, not a pattern. |
| Review | P | s | s | s | s | plain signals (D-225) | Where two codes may be one. |
| Attribution | P | c | c | c | c | keep (D-219) | Whose accounts, where promised. |
| Index Bases | P | k | k | – | k | keep | All codes of a layer at a glance in Obsidian. |
| Notebook | P | ? | s | s | k | keep; a helper sets up the terminal (D-232) | The views at a desk. |

### 6d. Ontology (ontology/scat.ttl)

| Item | S/Se/P | Q | O | M | K | Outcome | Reason |
|---|---|---|---|---|---|---|---|
| scat:Group, scat:Concern, scat:Affordance, scat:Technology | Se | k | k | k | k | keep | The four layers are the language for structure. They make different-looking accounts comparable. |
| scat:EdgeType | Se | k | s | s | s | keep | Holds the three relation types as data, so no tool copies them. |
| scat:Heldby, scat:Addresses, scat:ProvidedBy | Se | k | k | k | k | keep | The three relations are how codes interrelate. Their names say what a row means (D-222). |
| rdfs:domain / rdfs:range on edges, scat:endpointOrder | Se | – | – | s | s | keep | Fix which layers each relation joins. That is the rule that makes a pattern well-formed. |
| scat:Narrative | Se | k | k | k | k | keep | The coded account, the concrete source of every pattern. |
| scat:Contributor, scat:field-attributed_to | Se | c | c | s | c | keep (D-219) | The attribution promise, where the community wants it. |
| scat:Index | S | s | s | c | c | out of the TTL (D-231) | A generated file, not part of the model. |
| scat:TableColumn, column-type/from/to/note, scat:tableHeading, scat:tableColumns, scat:cellHolds | S | k | c | c | c | out of the TTL (D-231) | Layout of the table, not meaning. It belongs in the contracts. |
| scat:Field, field-type, field-status, field-title, field-description, field-kind | S | k | k | k | k | keep | The fields a code or account carries. `description` is the code's definition. |
| scat:field-timeframe | S | s | c | s | s | reframed as actual / hypothetical / unclassified, a filter (D-224) | Separates conjecture from what could be verified, without gating the work. |
| scat:status, scat:StatusValues, scat:stub, scat:draft, scat:done | Se | k | s | k | k/s | keep | The state of each piece of work. Distinct from the project's stage (D-177). |
| scat:carriesStatus, scat:discouragedField, scat:mapsTo | S | k | s | c | c | out of the TTL (D-231) | Unread or implementation detail. |
| scat:key, scat:pageDescription, scat:requiredField, scat:optionalField, scat:requiredFrom, scat:valueSet, scat:targetType, scat:verb, scat:slug | S | k | s | s | s | keep | They let the tools be generated from the model, so the rules follow the ontology and are not written twice. |
| scat:source, scat:authored, scat:verification | Se | k | s | c | s | to a docs table (D-231) | Research provenance, not model. |
| skos:closeMatch (SEBoK, 42010), rdfs:seeAlso (WoT) | Se | – | – | – | k | keep | Ties the layers to established terms, so a reader recognises them. |

### 6e. Other features

| Item | S/Se/P | Q | O | M | K | Outcome | Reason |
|---|---|---|---|---|---|---|---|
| Lifecycle stages and `lifecycle.toml` | P | c | c | c | c | keep (D-218); template starts in plan; same strength everywhere; roles (D-234); `synthesise` stage (D-235) | The scaffolding that breaks the work into simple pieces and stabilises the assistant's behaviour. |
| Attribution modes | S/Se/P | c | s | s | c | keep (D-219) | Two real use cases: activists who reject named contributions, and a community that tracks them. |
| Prose links plus table rows (two records) | S/Se/P | s | – | k | s | the table is the record; prose links are a subset (D-220) | One record of the coding. The prose stays interpretive, connective tissue. |
| Narrative-to-node link page | Se | – | – | – | – | optional slot (D-216, D-233) | Room for notes on how one account uses a code, without requiring a page. |
| The relationship annotation (a free line) | Se | k | – | k | k | keep | An optional slot for a tension between two codes. |
| Machine-interface JSON schema | S | – | s | c | k | keep; item-by-item review (D-226) | Carries the guard and remediation to the assistant. |
| SCATLAB, container, Funnel, keys | P | – | s | s? | – | keep; docs say a helper sets it up (D-232) | Gets the tools to a chat without the organiser installing anything. |
| Four coding paths and walkthroughs | P | – | s | – | – | keep | Different people code in different places. |
| `decisions/log.md` in the shipped repo | – | – | – | c | – | keep; no D-nnn in user pages | The record of the chief engineer's calls. |

## 7. Decision list

One line each, for the chief engineer to answer one at a time. Each is a cut or a simplification. Every one would
become its own small package.

1. **Stages.** Decided (D-218): the stage machine stays. [S]'s findings S1 to S3 become item 16.
2. **Attribution.** Cut it entirely, or keep one switch ("no names" enforced, or names as free text)?
3. **One record or two.** Keep both prose links and table rows (MISSION G17, WP39), or make one of them the only record
   of an edge? [Q] alone.
4. **The `type` column.** Infer the edge type from the ends' layers and drop the column? [O] and [K].
5. **The rule catalogue.** One rule per condition with severity set by status; cut SECOND, DUPLICATE, MENTION and
   SUGGEST-CONFIG; about ten conditions in all.
6. **`timeframe`.** Make it optional, out of the `done` gate.
7. **`copy-share` and `review`.** Cut `copy-share`; strip `review` to its plain signals with no hidden thresholds.
8. **Fixes as data.** Keep the fix objects and JSON schema (the assistant uses them), narrow them, or reduce them to
   plain text?
9. **Fewer views and commands.** Fold `fingerprint`, `trace`, `split-plan` and `stub-links` into `layered`, `evidence`
   and `stub`?
10. **Names.** Keep ASCII slugs, or allow any Obsidian-legal name?
11. **Add recurrence.** A count of narratives and groups per node (and per edge) in `status` or `layered`. Three
    reviewers; verified absent.
12. **Add abstraction guidance.** One short page on what a pattern is and how to name a code at the right level, plus a
    rename operation. Verified absent.
13. **The ontology file.** Move `Index`, the table-column terms, `carriesStatus` and the per-term provenance out of the
    TTL.
14. **The chat-path setup.** A first release with a prebuilt installer and no key reset each run, or a plain statement
    that setup needs a helper?
15. **C22 (D-216).** Reconsider the reified narrative-to-node page in light of §5 (no reviewer asked for more pages;
    [K] proposes `skos:broader`).
16. **The lifecycle, respected everywhere.** Ship the template with a starting stage so the first call is not refused;
    one strength of enforcement across the MCP, IDE and CLI paths; and whether `analyse` may consolidate codes (merge)
    or synthesis goes back to `code` ([S] S1 to S3).
17. **Consistency fixes, one package.** One actor model with the organiser in the authority tables; one answer on
    whether the assistant sets status; `kind`'s effects stated in the contract or removed; the contributor-stub
    contradiction; one copy of the assistant rules and of `architecture.md`; terms no code reads out of the TTL ([S] S2,
    S4 to S8). These are contradictions, not choices: the ACE would settle each by the ontology and the contracts.

## 8. Outcomes

The chief engineer answered every item on 28 November (decisions/log.md D-218 to D-236):

| Item | Outcome | Log |
|---|---|---|
| 1 Stages | Stay; the stage machine is the scaffolding that keeps the rest simple | D-218 |
| 2 Attribution | Stays as built; it serves two real use cases | D-219 |
| 3 One record or two | The table is the coding of record; prose links are a subset of its nodes (warning in draft, error at done) | D-220, D-221 |
| 4 Type column | Stays | D-222 |
| 5 Rule catalogue | One id per condition, severity by status; TABLE-SECOND, TABLE-DUPLICATE, MENTION, SUGGEST-CONFIG cut | D-223 |
| 6 Marks | `timeframe` (as actual / hypothetical / unclassified) and `kind` become analysis filters, gating nothing | D-224 |
| 7 copy-share, review | copy-share cut; review keeps plain signals | D-225 |
| 8 Fixes as data | Stay; an item-by-item review later | D-226 |
| 9 Commands | `split-plan` becomes `where-used`; the rest stay | D-227 |
| 10 Names | ASCII slugs stay | D-228 |
| 11 Recurrence | A separate view | D-229 |
| 12 Abstraction | A guide page, `rename`, a documentation pass, core glossary terms; the purpose statement | D-230, D-232 |
| 13 TTL | Stripped to the model | D-231 |
| 14 Chat setup | The docs say a helper sets it up | D-232 |
| 15 C22 | Stands; the link page is an optional slot; the assistant is guided on every slot | D-233 |
| 16 Lifecycle | Template starts in plan; same strength everywhere; roles replace authority tables; a sixth stage, `synthesise` | D-234, D-235 |
| 17 Consistency | One package, settled by the ACE | D-236 |
