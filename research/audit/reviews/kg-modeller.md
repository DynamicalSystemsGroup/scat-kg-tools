# Audit: the SCAT meta-model, read as a knowledge-graph / ontology modeller

Reviewer persona: RDF/OWL/SKOS modeller, reification-minded. Read-only. Repos: `scat-wt/wp40-audit` (tools) and `scat-wt/tpl-pin3` (template). I ran `scat check`, `scat layered` and `scat review` in `tpl-pin3` (read-only; it printed "no problems", a 4-layer view with 8 edges, and one duplicate proposal). Paths below are relative to `wp40-audit` unless noted. "ttl:N" is `ontology/scat.ttl`, "RC:N" is `contracts/rule-catalogue.md`, "PC:N" is `contracts/page-contracts.md`.

Short verdict. The conceptual core is small and good: four node types, three edge types between neighbouring layers, one page type for accounts (the narrative), and an edge that remembers which narratives tell it. That core is about 10 terms. Around it sits a lot that does not help a coder get from concrete accounts to abstract patterns. There is a ~40-id rule catalogue, most of it policing a hand-typed table whose `type` column repeats what the node layers already say. There is an attribution subsystem (a page type, three modes, six rules, a view, a CLI command, an MCP tool) that the shipped template turns off. There is a five-stage lifecycle state machine gating the MCP tools. And the TBox is half meta-vocabulary describing itself (13 annotation properties, `Field`, `TableColumn`, `Index`). Separately, the most important structure for pattern-finding, "this edge is told by these narratives", is nowhere in the ontology file.

---

## 1. Explanation

### SYNTAX: what makes a vault well-formed

- A vault is a git folder of Markdown pages with YAML frontmatter. One folder per page type: `group`, `concern`, `affordance`, `technology`, `narrative`, plus `contributor` where attribution is on, plus generated `index/*.base` Obsidian Bases (template: `tpl-pin3/{group,concern,...}`, `tpl-pin3/index/concern.base`).
- Every page has `type`, `status` (stub, draft, done), `title` from the first status. At `done`, `description` is also required, and on a narrative `timeframe` (ttl:244-295). `kind` (scenario or architecture) and `attributed_to` are optional on a narrative (ttl:166-176).
- File names are slugs: `a-z`, `0-9`, hyphen, at most 64 characters, no reserved names (RC:352-362). Links are Obsidian wikilinks.
- Edges live only as rows in a table under the heading `Edges told` in a narrative, with columns `from | type | to | note` (ttl:166-176; example `tpl-pin3/narrative/groups-under-a-cap-pitch.md`). Each end is exactly one link. The type is one of three edge types, written as a verb or a slug. The ends must be in the layers the type fixes (RC:606-648).
- The vault has `scat.toml` with `attribution` (required, optional or disallowed) and `stakeholder_group_cap` (`tpl-pin3/scat.toml`). A second config key, `link_suggestions`, exists (RC:522).
- A `done` narrative must pass every error rule. `set-status done` re-checks the page as if `done` and refuses on any error (RC:723-755). Before `done`, the same table problems are warnings, not errors (RC:210-262).
- The check never writes. Each problem carries a machine-readable fix (exact, slot, options, advisory or manual).

### SEMANTICS: what the parts mean

- The four node types are `skos:Concept` subclasses (ttl:71-120). Group is a stakeholder group (never a person), concern is "any interest in a system" (42010), affordance is a possibility of action a technology offers (Gibson), technology is a discrete system element (SEBoK). Definitions are cited, with a `scat:verification` flag marking which citations were really checked (almost all "unverified": ttl:80, 91, 103, 115).
- The three edge types are `owl:ObjectProperty` with `rdfs:domain` and `rdfs:range`, and also instances of `scat:EdgeType` (ttl:128-164): Group holds Concern; Concern is addressed by Affordance; Affordance is provided by Technology. The graph is layered and bipartite between neighbours. A group cannot hold an affordance directly: the coder must say which concern sits between.
- A narrative is one account. It is not a node. It contains links and a table of the edges it tells. Two narratives telling the same (type, from, to) make one graph edge with two tellings, each with its own note (ttl:111-115 comments; `graph.py` `Telling`/`Edge`, graph.py:357-392). Edge status is derived: `done` only if every telling is `done`, else the least advanced (graph.py:524-527).
- `kind` (scenario = behavioural, architecture = structural) and `timeframe` (past, future, mixed) are tags on narratives only (ttl:272-285; MISSION.md "Narratives"). Good, bad, mix is deliberately not modelled (MISSION.md, same section).
- Disagreement is held, not resolved. Different narratives may attach different edges to a shared node; nothing adjudicates. A "relationship annotation" (a body sentence such as "Pulls against [[x]]") is explicitly outside the graph (PC:294-304).
- Attribution: a `contributor` page and `attributed_to` links, with the `prov:wasAttributedTo` sense, outside the four layers (ttl:178-186, 286-295).
- Candidates: if a narrative links two nodes with no row for them, there is no rule; only the fingerprint view lists it as a candidate (RC:713-721).

### PRAGMATICS: how a person gets from concrete accounts to abstract patterns

1. Draft the narrative as free text in Obsidian (stub, then draft). Link names where nodes appear. `scat stub` makes node pages.
2. Add rows to the edge table (by hand, or `record-edge`, which the assistant must use instead of hand-writing: `contracts/assistant.md` A9). Run `scat check`; it explains each problem and offers fixes.
3. Set `done` (the coder's attestation; the tool only gates structure).
4. Read the views: `layered` (union of narratives' nodes/edges, orphans listed), `edges <type>` (each edge with its tellings), `trace` (follow edges up or down), `evidence <node>` (every paragraph that links the node), `fingerprint` (one narrative's slice), `draw` (images), `export-edges` (CSV to a notebook).
5. Do the abstraction. The one act the tools actually support is changing nodes: `review` proposes pages that may be one node or pages told to unrelated other ends; `copy-share` flags node descriptions copied word for word from narratives (i.e. not yet abstracted); `merge A B` folds A into B; `split-plan` lists what to re-link to split a node. The group cap forces clustering of people into at most N groups.
6. Everything else is process: the five-stage lifecycle (plan, capture, code, analyse, report) with a `lifecycle.toml`, `which_stage`/`set_stage` on the MCP server, guides, seven MCP prompts, and an assistant contract of 20 SHALL/MAY clauses.

The real abstraction mechanism is thus: concrete = narrative text; abstract = shared node pages; pattern = a node or edge that several narratives tell, with the layered graph showing structure. That is a sound design, and small.

---

## 2. Verdict table

Notes on reading it. "S/Se/P" = syntax, semantics, pragmatics. A pair rule row covers both its `DRAFT` and `DONE` ids. I count 41 live rule ids: 22 single ids, 9 pairs (18 ids), and `SCAT-DONE-REFUSED` (RC:137-188). Where I am unsure I say so.

### 2a. Rules (rule-catalogue)

| Item | S/Se/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| SCAT-FM-PARSE | S | keep | Unreadable frontmatter makes a page invisible to the graph. Needed. | RC:265 |
| SCAT-FM-REQUIRED | S | simplify | `status` and `title` missing. One frontmatter-completeness rule, driven by the TBox, would replace this, DONE-FIELD, DRAFT-FIELD, TYPE, STATUS, TIMEFRAME, KIND and SHAPE. | RC:276 |
| SCAT-FM-TYPE | S | simplify | Value must be one of six types. Same generic "value in set" rule as below. | RC:289 |
| SCAT-FM-STATUS | S | simplify | Same: generic value-set rule. | RC:302 |
| SCAT-FM-TIMEFRAME | S | simplify | Same. The field itself is questioned in 2d. | RC:314 |
| SCAT-FM-KIND | S | simplify | Same. | RC:326 |
| SCAT-FM-SHAPE | S | simplify | "A text field is a single non-empty string." Half of it exists only for `attributed_to` lists. Falls away if attribution is cut. | RC:340 |
| SCAT-NAME | S | simplify | Slug names make wikilinks reliable (keep that). But 64-character cap, reserved names and case-only collisions are extra, and non-Latin titles get "hand choice, no fix" (RC:362), a real cost for a field exercise. Obsidian already enforces uniqueness of names. | RC:352-362 |
| SCAT-DONE-FIELD / SCAT-DRAFT-FIELD | S | simplify | One rule with severity chosen by status, not two ids. Required `description` at `done` on node pages is reasonable (it is the label the abstraction carries). | RC:364-392 |
| SCAT-ATTR-DISALLOWED | S/Se | cut | Attribution is provenance of who said it, not a pattern. Template ships it off. Errors on any `contributor` page or `attributed_to` key, even empty, in a disallowed vault. | RC:415 |
| SCAT-ATTR-LINK | S | cut | Link checking for a field the template does not use. | RC:428 |
| SCAT-DONE-ATTR / SCAT-DRAFT-ATTR | S | cut | Same. A rule that fires only in `required` mode. | RC:443-465 |
| SCAT-MODE-CONFIG | S | cut | Config for the cut feature. | RC:497; `tpl-pin3/scat.toml` |
| SCAT-LINK-DANGLING-BODY | S | keep | A link to a page that does not exist is how a node is born (stub). Cheap, direct, and the fix (`stub`) is the right way made easy. Obsidian marks it too, but the tool must know for the graph. | RC:467 |
| SCAT-CAP | Se/P | keep | The one rule that forces abstraction: people must be clustered into at most N groups. This is genuinely the point of the exercise. | RC:484; `tpl-pin3/scat.toml` |
| SCAT-CAP-CONFIG | S | simplify | A missing or malformed number. Fold into one config rule if config is kept at all. | RC:511 |
| SCAT-SUGGEST-CONFIG | S | cut | Config for a lint that is off by default. | RC:522 |
| SCAT-MENTION | P | cut | Warns where a node's name appears as plain text. Off unless configured; Obsidian already shows unlinked mentions. | RC:535 |
| SCAT-NOEDGES | Se/P | keep | A `done` narrative that tells no edge contributes nothing to a pattern. Warning only. Could share an id with UNCODED. | RC:547 |
| SCAT-UNCODED | Se/P | simplify | A narrative that links no node is excluded from views. Tell the user once; same message family as NOEDGES. | RC:560; views.py:140 |
| SCAT-*-TABLE-HEADER | S | simplify | Exists because the table has a fixed four-column layout that a human might misorder. A narrower table (see top cut 1) needs only "has a table". | RC:579 |
| SCAT-*-TABLE-ROW | S | simplify | Wrong cell count. Falls out of any simpler row. | RC:594 |
| SCAT-*-TABLE-TYPE | S/Se | cut | Checks the typed word in the `type` column. That word is fully determined by the layers of the two ends (ttl:8-9 says so: "A row's type is fixed by the layers of its ends"). Remove the column, remove the rule. | RC:606; ttl:8-9 |
| SCAT-*-TABLE-LAYERS | Se | simplify | Keep one check: the ends are in neighbouring layers. The "swap the ends" and "retype" fixes vanish when the type and the order are inferred. | RC:621 |
| SCAT-*-TABLE-SECOND | S | cut | A second `Edges told` table is silently unread. Read every table under it, or just tell the author. A rule for a rare typo. | RC:636 |
| SCAT-*-TABLE-DUPLICATE | S | cut | A repeated row says the same edge twice; the graph keys edges by (type, from, to) and already merges. Collapse silently. | RC:649; graph.py:357 |
| SCAT-*-END-NOLINK | S | simplify | One of three variants of "a row end is not a link to a node page". | RC:669 |
| SCAT-*-END-NOPAGE | S | simplify | Same: merge with LINK-DANGLING-BODY. The row end is just a body link. | RC:686 |
| SCAT-*-END-NOTNODE | S/Se | simplify | Same: one rule "a row end must be a link to a node page". | RC:700 |
| SCAT-DONE-REFUSED | S/P | keep | `set-status done` re-runs the check and refuses with the list. This is the one gate where conformance is actually enforced. The doc is long but the idea is minimal. | RC:723-755 |
| (rule 4: no rule for candidates) | Se | keep | Restraint: "a link says see also; an edge is about the relationship" is correct modelling. | RC:713-721 |

### 2b. CLI commands (`uv run scat --help`; subparsers at `cli.py:28,270`)

| Item | S/Se/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| `check` | S/P | keep | Core. | cli help; mcp `check` server.py:50 |
| `status` | P | simplify | Counts of pages by status. `check` plus Obsidian Bases already show status. Could be a flag of `check`. | server.py:58 |
| `set-status` | P | keep | Needed for the done gate. | server.py:67; RC:723 |
| `index` | P | simplify | Generates 5 `.base` files "once, never rewritten". Fine, but then a one-time template concern, not a command. Put the files in the template. | ttl:187-197; `tpl-pin3/index/` |
| `stub` | P | keep | Makes node pages; the easy way to add a node. | server.py:98 |
| `stub-links` | P | cut | Bulk `stub` for dangling row ends. The check fix already says "run `scat stub X`". | server.py:106 |
| `record-edge` | S/P | keep | Writes a row without the human typing a table. This is "right way = easy way"; it is the only thing standing between the coder and 18 table rules. But if the table loses its `type` column it becomes trivial. | server.py:115; contracts/assistant.md A9 |
| `remove-edge` | P | keep | Counterpart. Could be hand-deleting a row once rows are simple. | server.py:126 |
| `merge` | Se/P | keep | The abstraction act: fold A into B. Keep. Note it destroys A's description and appends body under a heading, so a loss of provenance of the abstraction step (not recorded in the graph). | server.py:138; cli help |
| `split-plan` | P | cut | A read-only list of links and rows naming A. `evidence A` already shows every paragraph and every row. | server.py:162 |
| `fingerprint` | Se/P | simplify | One narrative's nodes and edges = `layered --narrative X`. Same data, one name too many. | views.py:262; views.py:343 |
| `edges <type>` | Se/P | keep | The per-edge list with tellings is the pattern table: which edges several narratives agree on. | views.py:311 |
| `layered` | Se/P | keep | The whole graph in layers, with orphans. | views.py:343 |
| `trace` | Se/P | simplify | Reachability up or down from a node. Useful but is a filter of `layered`; could be `layered --from NODE`. Unsure it earns its own command. | views.py:408 |
| `evidence <node>` | Se/P | keep | Takes the abstract back to the concrete: each paragraph around each link. This is the pattern-to-evidence path, the most valuable single view. | evidence.py:152 |
| `copy-share` | Se/P | keep (unsure) | A node description copied verbatim from narratives has not been abstracted. It is the only direct measure of "moving the other way". Five-word-run test is crude; threshold unspecified. | copyshare.py:95 |
| `review` | Se/P | simplify | Proposes duplicate nodes (three overlap measures, hubs, thresholds) and nodes "told to different ends". Duplicate detection is on point. Six tuned constants (`ADJACENT_JACCARD`... ) and a pages-to-re-read heuristic are tuning for unknown benefit. Keep only "twin rows". | review.py:36-47 |
| `attribution` | Se | cut | Attribution view. | views.py:480 |
| `export-edges` | P | keep | CSV exit to the analyst's own tools. Cheap, no new concept. | export.py:66 |
| `guide` | P | keep | Stage guides without a vault. Content, not machinery. | cli help; `src/scat_tools/guides/` |
| `draw` | P | simplify | PNG/SVG of fingerprint, layered, trace. Keep one picture (layered); a 300-line renderer with crossing minimisation (draw.py:237-322) is heavy. | draw.py:553-660 |

### 2c. MCP tools and prompts (`mcp_server/server.py`, `stage.py`)

The server exposes the CLI/API operations 1:1 (check, status, set_status, stub, stub_links, record_edge, remove_edge, merge, split_plan, index, fingerprint, edge_table, layered, trace, evidence, copy_share, review, attribution, export_edges: server.py:50-320), plus `which_stage` and `set_stage` (stage.py:384-410), seven prompts and a guide resource (server.py:344-391).

| Item | S/Se/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| MCP tools that mirror a kept CLI command | P | keep | The assistant path is the same operations. Same verdicts as 2b. | server.py:50-320 |
| MCP `stub_links`, `split_plan`, `attribution` | P | cut | As the CLI. | server.py:106, 162, 311 |
| MCP `which_stage`, `set_stage` | P | cut | A state machine (5 stages, transitions, "who decides", detect and person predicates, `lifecycle.toml`) that gates which tools an assistant sees. It tells the assistant what the coder is doing; it does not produce a pattern. High cost, low yield for a note-taker. The guides alone do the "where am I" job. | stage.py:384-410; contracts/lifecycle.md:15-60 |
| MCP prompts (7: code-a-narrative, explain-a-problem, review-before-done, draft-a-node-page, fill-in-node-pages, look-for-duplicates, assistant-rules) | P | simplify | `look-for-duplicates` and `draft-a-node-page` are the abstraction acts. Others restate the check and the guide. | server.py:344-391 |
| Assistant contract (A1-A20) | P | simplify | Twenty clauses, in RFC 2119 words, for a role described as "the one non-critical role". Four clauses carry it: never set `done`, never hand-write a row, state doubts, report tool results as given. | contracts/assistant.md |

### 2d. Ontology classes and properties (`ontology/scat.ttl`)

| Item | S/Se/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| `scat:Group`, `Concern`, `Affordance`, `Technology` | Se | keep | The minimal four-layer vocabulary. Definitions cited to 42010, Gibson, SEBoK is good practice. But I would drop the `unverified` provenance triple per term from the TBox (see `source`, `authored`, `verification`). | ttl:71-120 |
| `scat:Heldby` / `Addresses` / `ProvidedBy` | Se | keep | The three typed layer-adjacent edges are the heart. Naming is odd (`Heldby` reads inversely to its pair order, ttl:131 admits it). | ttl:128-164 |
| `scat:EdgeType` (class, punned with the properties) | Se | simplify | Making an `ObjectProperty` also an instance of a class is punning, legal in OWL 2 but unusual. Its only job is to let Python find the three properties. Use `rdfs:subPropertyOf scat:edge` or a SKOS collection. | ttl:122-126 |
| `rdfs:domain` / `rdfs:range` on the edge properties | Se | simplify | In OWL, domain/range infers types; it does not reject a wrong-layer row. The real constraint is checked in Python (`TABLE-LAYERS`) from `scat:endpointOrder`. The same constraint is therefore stated twice, and the OWL one cannot enforce it. State once (SHACL, or the endpointOrder alone). | ttl:128-164 (domain/range and endpointOrder both) |
| `scat:Narrative` | Se | keep | One account is the evidence unit. | ttl:166-176 |
| `scat:Contributor`, `field-attributed_to` | Se | cut | See attribution rows above. Provenance of who spoke is not a pattern; the template runs with it off. | ttl:178-186, 286-295 |
| `scat:Index` | S | cut | Not a page type, not in the graph, no fields; the TBox says "the loader ignores it". It is documentation. | ttl:187-197 |
| `scat:Field` and 7 field instances | S | simplify | A frontmatter key per field as a typed `Field` object, so tools need no second file. Reasonable engineering, but it is meta-vocabulary the coder never meets. | ttl:238-295 |
| `scat:field-type`, `field-status`, `field-title`, `field-description` | S | keep | The common frontmatter. | ttl:244-270 |
| `scat:field-timeframe` | Se | simplify (unsure) | Past / future / mixed on narratives. Required at `done`. Useful as a facet when slicing patterns ("do the same concerns recur in what happened and in what is proposed?"), and the chief engineer asked for it. But "mixed" admits the tag can't be applied, and it is required, so it costs a coder a decision for every narrative. Make it optional, as `kind` is. | ttl:272-277 |
| `scat:field-kind` | Se | keep | Optional scenario or architecture tag. Same facet logic; optional is the right strength. | ttl:279-284 |
| `scat:TableColumn` and 4 column instances; `scat:tableHeading`, `tableColumns`, `cellHolds` | S | cut (follows top cut 1) | Five terms and a class to say "the table has columns from, type, to, note, in that order, under 'Edges told'". That is the Markdown contract being carried as RDF. With a two-link row, it is a sentence in the contract. | ttl:200-235, 378-391 |
| `scat:status`, `StatusValues`, `stub`, `draft`, `done` | Se | keep for narratives; simplify for nodes | Status on narratives is a real lifecycle. On node pages it adds a field, a warning pair, and the claim "an edge is draft because one narrative that tells it is draft" (graph.py:524). I see no pattern-finding use of node or edge status. Unsure: the template shows `status: done` on every node. | ttl:297-330; graph.py:519-527 |
| `skos:OrderedCollection` + `skos:memberList` for 3 values | Se | simplify | Heavy for an ordered triple. `scat:valueSet` does the same for timeframe and kind with a bare RDF list (ttl:408); two ways to say "enumerated values". | ttl:304-309, 408-411 |
| `scat:carriesStatus` | S | cut | Used only so that `Index` can opt out. Goes with `Index`. | ttl:333-336, 187 |
| `scat:key`, `pageDescription`, `requiredField`, `optionalField`, `requiredFrom`, `mapsTo`, `targetType`, `endpointOrder`, `verb`, `slug`, `valueSet` | S | simplify | Eleven annotation properties by which the TBox describes how to parse pages. `discouragedField` is declared and "used by no type" (ttl:358-361, 40). `targetType` is used by one field (attribution). `slug` and `verb` both spell the edge name (see top cut 2). Keep `key`, `requiredField`, `endpointOrder`, `valueSet`; fold the rest. | ttl:333-411 |
| `scat:source`, `authored`, `verification` (on every term) | Se | simplify | Provenance of the definitions. Valuable once, as a changelog or a note in `docs/`. On every term it triples the size of the file (almost every term has three extra triples). A coder reading the TBox sees more provenance than ontology. | ttl:413-426 |
| `skos:closeMatch` to SEBoK and 42010 | Se | keep | The right way to anchor without importing. | ttl:75, 86, 97, 109 |
| `rdfs:seeAlso` WoT `InteractionAffordance` | Se | keep | Fine. | ttl:98 |
| Missing: `skos:prefLabel`, `skos:altLabel`, `skos:broader`, `skos:inScheme` | Se | (see section 4) | Nodes are `skos:Concept` but use `dcterms:title`, not `prefLabel`. | ttl:258-263 |

### 2e. Other significant features

| Item | S/Se/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| The edge table in the narrative (rather than any other carrier) | S/Se | simplify | A hand-typed Markdown table is the most fragile carrier available; it is the origin of 9 pair rules, a table reader (`graph.py:62-345`, ~280 lines), and a row-editing module. A list item `- [[a]] ↔ [[b]] note` or a two-link line would give the same graph. | graph.py:62-345; RC:573-711 |
| The `type` column | S/Se | cut | Determined by the layers of its ends. It is a second statement of what the node pages' types already say; the checker has to reconcile them. It also duplicates three spellings (verb, slug, ttl label). | ttl:8-9; PC:201-209; ttl:373-377 |
| Graph load derived on every call | S/P | keep | Git is the source; the graph is derived. Good, no stale state, no store to manage. | views.py docstring, views.py:1-24; MISSION.md "Purpose" |
| Derived edge status | Se | cut | `done` only if every telling is `done`. What a coder wants about an edge is how many narratives tell it, not whether a status is aligned. | graph.py:519-527 |
| Group cap | Se/P | keep | See SCAT-CAP. | RC:484 |
| Relationship annotation (body sentence, outside the graph) | Se | keep | Holds disagreement without adding a fifth edge type. But it is invisible to every view. It is the right restraint. | PC:294-304 |
| Lifecycle stages and `lifecycle.toml` | P | cut | See MCP `set_stage`. | contracts/lifecycle.md |
| Fix kinds (exact, slot, options, advisory, manual) and the "message with a fix" convention | S/P | keep, narrower | "Right way easy": a message with a fix is good. Five fix kinds and a JSON schema of 765 lines (`machine-interface.schema.json`) are heavy. | RC:137-188; contracts/machine-interface.schema.json |
| Obsidian Base index per type | P | keep | Navigation, no concepts. | `tpl-pin3/index/*.base` |
| `analysis.ipynb` in the template | P | keep | Read-only notebook that loads the graph and draws views. Good bridge to pattern-reading. | `tpl-pin3/analysis.ipynb` |

---

## 3. Top five cuts or simplifications (most valuable first)

1. **Drop the `type` column and the from/to order: a row is two links and a note.** The edge type is a function of the layers of the two node pages (ttl:8-9 says so itself), and direction is the layer order. So the tool can infer both. This removes the whole type-and-direction rule family (TABLE-TYPE, the "swap" and "retype" branches of TABLE-LAYERS, TABLE-HEADER's column-order variant, the near-match among six spellings of PC:201-209) and the TBox's `TableColumn`, `cellHolds`, `tableColumns`, `column-*` terms. It frees the coder from learning three verbs and two spellings of each and from getting a pair "the wrong way round". It costs one thing: the human reading of "holds" in the note, which the docs can print. This is the biggest saving per unit of concept removed. Unsure: Obsidian rendering of the table may still want a header; that is cosmetic.
2. **Cut attribution end to end** (Contributor class, `attributed_to`, mode config, 6 rules, `attribution` view, CLI command and MCP tool, `ATTR-*` messages). It is provenance of who said what; it is not a pattern of the account; and the shipped template sets it to disallowed (`tpl-pin3/scat.toml`). If a project needs it, a plain `attributed_to: [text]` frontmatter field with no link check is the whole feature. It frees the coder from the mode decision in planning and from three contributor-page rules, and frees every vault from carrying the one rule that fails on an empty key (RC:415).
3. **Collapse the rule catalogue from 41 ids to roughly 10 conditions.** Make severity a function of status, not a separate id (9 pairs become 9 rules, 18 ids become 9). Fold FM-TYPE/STATUS/TIMEFRAME/KIND/SHAPE/REQUIRED and DONE/DRAFT-FIELD into one TBox-driven "field value or presence" rule. Fold DANGLING-BODY and the three END-* into "a link must reach a node page". Cut SECOND, DUPLICATE, MENTION, SUGGEST-CONFIG, MODE-CONFIG. What is left: PARSE, FIELD, NAME, LINK, LAYERS (row ends in neighbouring layers), CAP, CONFIG, NOEDGES/UNCODED, and DONE-REFUSED. This frees the coder from reading 41 message formats and the maintainers from golden tests for each (RC:253-262 describe one-defect-one-message tests per rule).
4. **Cut the stage machine and the matching MCP tools.** `which_stage`, `set_stage`, `lifecycle.toml`, stage-filtered tool lists, who-decides roles and detect predicates (contracts/lifecycle.md:15-60) coordinate an assistant with a plan that the guides already state. It frees the coder from being told which "stage" the tool thinks they are in. Keep the guides. Also fold `stub-links`, `split-plan`, `fingerprint`, and perhaps `trace` into `layered`/`evidence`/`stub`.
5. **Shrink the TBox to the ontology and move the rest to documentation.** Remove `Index`, `carriesStatus`, `discouragedField`, `TableColumn` stuff, and the `source`/`authored`/`verification` triple on every term (put the provenance in a table in the docs). State the layer constraint once, not as domain/range plus `endpointOrder`. This does not change what a coder does; it makes the 426-line TBox legible to the one person likely to read it, an ontologist reviewing it. It frees the reviewer from reading provenance noise to find eight classes and three properties.

Honourable mention: `status` on node pages and derived edge status (graph.py:519-527). I see no pattern-finding use, but unsure; the chief engineer may use stubs as a to-do list.

---

## 4. Missing, if the point of the exercise is synthesis (at most three)

1. **A way to say "this node is an instance or a kind of that node" without destroying the concrete one.** The only abstraction step is `merge`, which removes A and appends its body to B (cli help for `merge`; server.py:138). A merge is final and drops A's description. A coder who sees three concerns as aspects of one pattern ("trust", "no surprise", "predictability") can only collapse them or leave them unrelated. The nodes are already `skos:Concept`, so `skos:broader` (or `skos:related` for a soft "pulls against") is the idiomatic answer and costs one optional section of a node page. Today this is the unstructured body-text "relationship annotation" which every view ignores (PC:294-304). Unsure whether the chief engineer wants a second level on purpose; the mission says the model is thin on purpose.
2. **A link from a narrative to its source, and a label list on nodes.** The node pages hold `title` mapped to `dcterms:title` (ttl:258) and not `skos:prefLabel`; the link texts coders actually used for a node (`[[node|text]]`) are surfaced only as an aside in `review` (review.py:36-47 docstring, link texts) and never modelled as `skos:altLabel`. They are exactly the vocabulary of the field notes that a pattern name abstracts away from. And the narrative has no property tying it to the field notes it summarises (inputs are "outside the ontology", MISSION.md), so a pattern traces down to a narrative but not on to the notes. Smallest fix: `prov:wasDerivedFrom` (optional text on narrative) and altLabels computed from link texts.
3. **A support count the coder can sort by.** The graph knows how many narratives tell each edge (`edges` shows the list; graph.py:376-392) but there is no node-by-narrative or edge-by-narrative count table in the CLI, only the CSV export and the notebook. "Which concerns do four different groups' accounts converge on?" is the first question a synthesis asks. I did not find it as one command; unsure whether the notebook answers it (I read cell titles only). A `--count` column on `edges` and `layered` would do.

---

## Things I am unsure about

- Whether the table's `type` column also serves human readers in Obsidian enough to keep. My claim is that the tool can infer it; the docs and sample narratives may rely on it for readability.
- Whether the chief engineer wants `timeframe` required (MISSION.md frames it as a mark on every narrative).
- I read the machine-interface schema, lifecycle and assistant contract only at headline level, and did not read docs/ or the test suite beyond names. Verdicts on the guide texts and prompts are therefore soft.
- The `review` thresholds (review.py:36-47) may have been tuned on a real vault I cannot see.
