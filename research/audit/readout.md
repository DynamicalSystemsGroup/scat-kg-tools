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
  - group (a collective with a stake, never a person);
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

**Columns.** S/Se/P is syntax, semantics or pragmatics. Q/O/M/K are each reviewer's verdict: k = keep, s = simplify,
c = cut, ? = unsure, – = not judged. Proposed is the ACE's synthesis after verification. It is a proposal for the
decision list, not a decision. Each verdict's reason, in terms of drawing patterns from accounts, is in that reviewer's own table under
the same item; this table carries no reason column of its own.

### 6a. Rules (contracts/rule-catalogue.md)

| Item | S/Se/P | Q | O | M | K | Proposed |
|---|---|---|---|---|---|---|
| SCAT-FM-PARSE | S | k | s | k | k | keep |
| SCAT-FM-REQUIRED | S | k | k | s | s | fold into one field rule |
| SCAT-FM-TYPE | S | k | s | s | s | fold into one field rule |
| SCAT-FM-STATUS | S | k | s | s | s | fold into one field rule |
| SCAT-FM-TIMEFRAME | S | s | s | s | s | fold; out of the `done` gate |
| SCAT-FM-KIND | S | k | s | s | s | fold into one field rule |
| SCAT-FM-SHAPE | S | k | s | c | s | fold into one field rule |
| SCAT-NAME | S | s | k | k | s | keep (decision list 10) |
| SCAT-DONE-FIELD / SCAT-DRAFT-FIELD | S | s | s | k/c | s | one rule; node `description` only |
| SCAT-ATTR-DISALLOWED | S | c | k | s | c | per attribution decision |
| SCAT-ATTR-LINK | S | c | c | s | c | cut |
| SCAT-DONE-ATTR / SCAT-DRAFT-ATTR | S | c | c | c | c | cut |
| SCAT-LINK-DANGLING-BODY | S | k | k | k | k | keep; absorbs END-NOPAGE |
| SCAT-CAP | Se | s | k | k | k | keep |
| SCAT-MODE-CONFIG | S | c | s | s | c | per attribution decision |
| SCAT-CAP-CONFIG | S | s | s | s | s | one config rule |
| SCAT-SUGGEST-CONFIG | S | c | c | c | c | cut |
| SCAT-MENTION | P | k | c | c | c | cut |
| SCAT-NOEDGES | P | k | s | s | k | keep |
| SCAT-UNCODED | P | k | k | k | s | keep |
| SCAT-DRAFT-TABLE-HEADER / SCAT-DONE-TABLE-HEADER | S | s | s | s | s | one lenient table-read rule |
| SCAT-DRAFT-TABLE-ROW / SCAT-DONE-TABLE-ROW | S | s | s | k | s | one lenient table-read rule |
| SCAT-DRAFT-TABLE-TYPE / SCAT-DONE-TABLE-TYPE | S | s | c | k | c | cut if the type column goes (decision 4) |
| SCAT-DRAFT-TABLE-LAYERS / SCAT-DONE-TABLE-LAYERS | Se | k | s | k | s | keep, one id |
| SCAT-DRAFT-TABLE-SECOND / SCAT-DONE-TABLE-SECOND | S | c | c | c | c | cut |
| SCAT-DRAFT-TABLE-DUPLICATE / SCAT-DONE-TABLE-DUPLICATE | S | s | c | c | c | cut (the graph keeps one edge) |
| SCAT-DRAFT-END-NOLINK / SCAT-DONE-END-NOLINK | S | s | s | s | s | one rule: a row end must reach a node page |
| SCAT-DRAFT-END-NOPAGE / SCAT-DONE-END-NOPAGE | S | s | s | s | s | into the rule above |
| SCAT-DRAFT-END-NOTNODE / SCAT-DONE-END-NOTNODE | Se | k | s | s | s | into the rule above |
| SCAT-DONE-REFUSED | P | s | k | k | k | keep |
| Retired-ids list (rule-catalogue.md:177-188) | – | c | c | c | – | move to the log |
| Structured fixes (fix kinds, edit actions) | P | k | s | c | k | decision 8 |

### 6b. CLI commands (and the MCP tool of the same name)

| Item | S/Se/P | Q | O | M | K | Proposed |
|---|---|---|---|---|---|---|
| `check` / check | S, P | k | k | k | k | keep; two scopes, not three |
| `status` / status | P | k | k | k | s | keep; add recurrence (decision 11) |
| `set-status` / set_status | P | k | s | k | k | keep |
| `index` / index | P | s | c | s | s | move to vault creation |
| `stub` / stub | P | k | k | k | k | keep |
| `stub-links` / stub_links | P | k | s | s | c | decision 9 |
| `record-edge` / record_edge | P | s | k | k | k | keep |
| `remove-edge` / remove_edge | P | s | k | c | k | keep |
| `merge` / merge | P | k | k | k | k | keep; no carried body (C22) |
| `split-plan` / split_plan | P | s | s | s | c | fold into `evidence` |
| `fingerprint` / fingerprint | P | k | k | s | s | decision 9 |
| `edges` / edge_table | P | k | s | k | k | keep; show row notes |
| `layered` / layered | P | k | k | k | k | keep |
| `trace` / trace | P | k | k | s | s | decision 9 |
| `evidence` / evidence | P | k | k | k | k | keep |
| `copy-share` / copy_share | P | c | c | c | k? | cut |
| `review` / review | P | s | s | s | s | simplify |
| `attribution` / attribution | P | c | c | c | c | cut |
| `export-edges` / export_edges | P | k | k | s | k | keep (fold into `edges --csv`) |
| `guide` | P | s | c | c | k | goes with the stages (decision 1) |
| `draw` | P | k | s | s | s | one drawing per view |
| MCP which_stage, set_stage | P | c | c | c | c | cut |
| MCP prompts (code-a-narrative, explain-a-problem, review-before-done, draft-a-node-page, fill-in-node-pages, look-for-duplicates) | P | k | s | s | s | keep fewer, after the cuts |
| MCP resource assistant-rules; SKILL A1-A20 | P | s | s | c | s | shrink to a few sentences |
| HTTP key gate | S | – | – | s | – | keep (security) |

### 6c. Views

| Item | S/Se/P | Q | O | M | K | Proposed |
|---|---|---|---|---|---|---|
| Fingerprint | P | k | k | s | s | decision 9 |
| Edge tables | P | k | s | k | k | keep |
| Layered (with candidates) | P | k | k | k | k | keep |
| Trace | P | k | k | s | s | decision 9 |
| Evidence | P | k | k | k | k | keep |
| Copy-share | P | c | c | c | k? | cut |
| Review | P | s | s | s | s | simplify |
| Attribution | P | c | c | c | c | cut |
| Index Bases | P | k | k | – | k | keep |
| Notebook | P | ? | s | s | k | keep; no terminal needed (decision 12) |

### 6d. Ontology (ontology/scat.ttl)

| Item | S/Se/P | Q | O | M | K | Proposed |
|---|---|---|---|---|---|---|
| scat:Group, scat:Concern, scat:Affordance, scat:Technology | Se | k | k | k | k | keep |
| scat:EdgeType | Se | k | s | s | s | simplify |
| scat:Heldby, scat:Addresses, scat:ProvidedBy | Se | k | k | k | k | keep (`Heldby` reads inversely to "holds", `scat.ttl:128-134`) |
| rdfs:domain / rdfs:range on edges, scat:endpointOrder | Se | – | – | s | s | state once |
| scat:Narrative | Se | k | k | k | k | keep |
| scat:Contributor, scat:field-attributed_to | Se | c | c | s | c | per attribution decision |
| scat:Index | S | s | s | c | c | out of the TTL |
| scat:TableColumn, column-type/from/to/note, scat:tableHeading, scat:tableColumns, scat:cellHolds | S | k | c | c | c | out of the TTL |
| scat:Field, field-type, field-status, field-title, field-description, field-kind | S | k | k | k | k | keep |
| scat:field-timeframe | S | s | c | s | s | optional |
| scat:status, scat:StatusValues, scat:stub, scat:draft, scat:done | Se | k | s | k | k/s | keep |
| scat:carriesStatus, scat:discouragedField, scat:mapsTo | S | k | s | c | c | cut |
| scat:key, scat:pageDescription, scat:requiredField, scat:optionalField, scat:requiredFrom, scat:valueSet, scat:targetType, scat:verb, scat:slug | S | k | s | s | s | keep, fewer |
| scat:source, scat:authored, scat:verification | Se | k | s | c | s | move to a docs table |
| skos:closeMatch (SEBoK, 42010), rdfs:seeAlso (WoT) | Se | – | – | – | k | keep |

### 6e. Other features

| Item | S/Se/P | Q | O | M | K | Proposed |
|---|---|---|---|---|---|---|
| Lifecycle stages and `lifecycle.toml` | P | c | c | c | c | cut (decision 1) |
| Attribution modes | S/Se/P | c | s | s | c | decision 2 |
| Prose links plus table rows (two records) | S/Se/P | s | – | k | s | decision 3 |
| The relationship annotation (a free line) | Se | k | – | k | k | keep |
| Machine-interface JSON schema | S | – | s | c | k | decision 8 |
| SCATLAB, container, Funnel, keys | P | – | s | s? | – | decision 12 |
| Four coding paths and walkthroughs | P | – | s | – | – | after the cuts |
| `decisions/log.md` in the shipped repo | – | – | – | c | – | keep; no D-nnn in user pages |

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
