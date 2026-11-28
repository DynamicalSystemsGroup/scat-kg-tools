# Audit of SCAT tooling: the minimalist maintainer

> **Background, not direction.** This page records reviewers' and the ACE's proposals before the chief engineer
> decided. Most proposed cuts were **not** adopted. The direction is in [final-report.md](../final-report.md) and decisions/log.md
> (D-216 to D-238).

Persona: the person who has to support this after release. I judge machinery: what could go with no loss to a coder who is
drawing abstract patterns from concrete accounts. Read-only; I ran `scat --help`, `scat check`, `scat status`,
`scat fingerprint`, `scat review` and `scat guide` against `tpl-pin3` and changed nothing. Paths are relative to
`/Users/z/Documents/GitHub/scat-wt/wp40-audit` unless they start `tpl-pin3/`. Things I could not verify are marked *(unsure)*.

Size first, because maintenance cost is the point. `src/scat_tools` is about 10,800 lines of Python. `tests/` is 145 files and
about 28,000 lines. `contracts/` is about 2,900 lines (the rule catalogue alone is 904, `contracts/rule-catalogue.md`),
`docs/` about 4,600, `decisions/log.md` 3,440, and `deploy/` about 1,100 lines of shell and AppleScript. The template vault, by
contrast, is 4 narratives and 10 node pages (`tpl-pin3/narrative`, `tpl-pin3/group`, ...), and `scat check` on it prints
"no problems". The coder's actual task is small and the apparatus around it is not.

## 1. Explanation

### The ontology in plain terms

A SCAT vault is a folder of Markdown pages. There are four **node types**, stacked as layers: stakeholder group, concern,
affordance, technology (`ontology/scat.ttl:71-114`). There are three **edge types**, each joining two neighbouring layers:
group *holds* concern, concern *is addressed by* affordance, affordance *is provided by* technology (`scat.ttl:128-160`). An edge
is not a page. It is one row in a **narrative's** table under the heading `Edges told` (`scat.ttl:166-177`,
`contracts/page-contracts.md:147-165`). A narrative is one account from the field notes, with links in its text wherever a
name appears. Narratives move through **stub, draft, done** (`scat.ttl:304-330`); `done` is the coder's attestation. A narrative
may be marked `kind` scenario or architecture and `timeframe` past, future or mixed (`scat.ttl:272-285`). Optionally, a
**contributor** page and an `attributed_to` list record who a narrative is attributed to (`scat.ttl:178-186`, `286-293`),
under a per-vault three-way mode (`contracts/page-contracts.md:525-545`). The knowledge graph is derived from the pages on every call and never stored
(`contracts/page-contracts.md:9-13`).

### SYNTAX: what makes a vault well-formed

- Page shape: frontmatter with `type`, `status`, `title`, plus `description` (and `timeframe` on narratives) once `done`
  (`contracts/page-contracts.md:68-74`). Legal slug file names. Links must resolve.
- The edge table: four columns in a fixed order, one link per end, a type cell that is the verb or the slug, ends in the right
  layers, no duplicate rows, no second table (`contracts/page-contracts.md:161-243`).
- Vault config in `scat.toml`: `attribution` (3 values), `stakeholder_group_cap`, `link_suggestions`, `templates_folder`
  (`contracts/page-contracts.md:525-556`).
- Enforcement: 31 distinct rule ids in code (my count of `SCAT-` strings under `src/scat_tools/checks`), which become 41 in the
  catalogue index because 9 table and end rules come in DRAFT (warning) and DONE (error) twins
  (`contracts/rule-catalogue.md:137-190`, `:206-262`). Each carries a structured fix with a "kind" (exact, slot, options,
  advisory, manual) and edit actions (`contracts/rule-catalogue.md:230-262`, `contracts/machine-interface.md:50-72`).
- A page may be set `done` only if it would pass at `done` (`contracts/rule-catalogue.md:723-754`).

### SEMANTICS: what the parts mean

- A node is an abstraction; the four types give it a role. Definitions are adopted from SEBoK, ISO 42010 and Gibson, each tagged
  with source and a verified/unverified flag (`scat.ttl:71-114`).
- A row means "this narrative tells this edge". An edge in the graph is one per (type, from, to) and names every narrative that
  tells it; its status is the least advanced of those narratives (`contracts/page-contracts.md:244-253`).
- A link without a row is a "candidate": the account names both ends but has not said they are related. No rule fires on it
  (`contracts/rule-catalogue.md:713-721`).
- `kind` is a label: the tool does not check a narrative's rows against it (`contracts/page-contracts.md:238-240`).
- Disagreement is held, not resolved: two narratives can tell different edges and both stand (`MISSION.md`, facilitation stance).
- A narrative that links no node page is "uncoded" and is excluded from every view (`contracts/page-contracts.md:174-186`).

### PRAGMATICS: how a person goes from concrete accounts to abstract patterns

The loop is: read field notes, write the account, link names, record rows, check, set `done` (`docs/coding.md:116-132`). The
abstraction step proper is deciding that "the borrower worried about a broken drill" and "someone was nervous about a
saw" are the same concern page. The tools around that step:

- Making things: `stub`, `stub-links`, `record-edge`, `remove-edge`, `set-status`, `index` (`src/scat_tools/cli.py:80-135`).
- Looking at the concrete behind a node: `evidence` (paragraphs around each link, across narratives, `src/scat_tools/evidence.py:1-17`).
- Looking at the abstract structure: `fingerprint`, `layered`, `trace`, `edges`, plus drawings and CSV export.
- Tidying the abstraction: `review` (possible duplicates, pages to re-read), `copy-share`, `merge`, `split-plan`.
- Three ways to drive it: REPL, CLI, or an assistant over MCP, which also carries a project "stage" machine, a launcher app
  and a tunnel (`contracts/lifecycle.md`, `deploy/README.md`).

Where the weight sits, honestly: the machinery is overwhelmingly on **syntax** (rules, fixes, the table, config, lifecycle),
and very little is on the thing the exercise is for. Merging two nodes (`ops/merge.py`, 598 lines) and `evidence` are the only
tools that directly support "these concrete accounts are one abstract pattern".

## 2. Verdict table

Legend: S = syntax, M = semantics (the meaning of the parts), P = pragmatics. For twin rules (DRAFT/DONE) I give one row.
Line cites for rules are in `contracts/rule-catalogue.md` unless stated.

### 2a. Rules (`contracts/rule-catalogue.md`)

| Item | S/M/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| SCAT-FM-PARSE | S | keep | Unreadable frontmatter means nothing else can be judged. Needed. | :265 |
| SCAT-FM-REQUIRED | S | simplify | `status` and `title` missing. Fold with TYPE, STATUS, TIMEFRAME, KIND, SHAPE into one "frontmatter value" rule. Six ids for one idea; each has its own message, fix variants and golden tests. | :276 |
| SCAT-FM-TYPE | S | simplify | As above. | :289 |
| SCAT-FM-STATUS | S | simplify | As above. The 3-value set is the lifecycle; keep the check, lose the id. | :302 |
| SCAT-FM-TIMEFRAME | S | simplify | As above. `timeframe` is a facilitation tag, not part of synthesis; the check can be a value-set test shared with `kind`. | :314 |
| SCAT-FM-KIND | S | simplify | A label nobody checks against anything (`page-contracts.md:238`). Value test only; fold. | :326 |
| SCAT-FM-SHAPE | S | cut | "Field is not a single non-empty string" and list shape: YAML's own error plus the REQUIRED rule cover it. Exists mainly for `attributed_to`. | :340 |
| SCAT-NAME | S | keep | Links resolve by name, so names must be legal and unique. Right way easy: stub derives the name. | :352 |
| SCAT-DONE-FIELD | S | keep | `description` at `done` is the one real completeness requirement; it is what an index shows. | :364 |
| SCAT-DRAFT-FIELD | S | cut | Warns, before `done`, that a field required at `done` is absent. Every draft trips it; "unfinished is never an error" (R-3) argues for silence. `set-status done` already lists it. | :378 |
| Mode rule (3 modes) | S | simplify | Required/optional/disallowed is a 3-way switch driving 4 rules, 1 page type, 1 view. Boolean (contributors on/off) would do. Chief engineer decision, as the mission asks for modes. | :394; `page-contracts.md:525-534` |
| SCAT-ATTR-DISALLOWED | S | simplify | Keep only if attribution stays; becomes "contributor pages exist but mode is off". | :415 |
| SCAT-ATTR-LINK | S | simplify | Entry must link a contributor page. Same fate as above; at most one attribution rule. | :428 |
| SCAT-DONE-ATTR / SCAT-DRAFT-ATTR | S | cut | "Required" mode with a warn-then-error pair. Making attribution mandatory has no bearing on pattern-drawing; cut the `required` mode. | :443, :456 |
| SCAT-LINK-DANGLING-BODY | S | keep | A link to nothing is the commonest slip and Obsidian shows it as a ghost. Cheap, clear. | :467 |
| SCAT-CAP | S/M | keep | The cap forces participants to cluster into groups, which is abstraction forced by design. Mission-mandated and short. | :484 |
| SCAT-CAP-CONFIG | S | simplify | One of three config rules; fold into a single SCAT-CONFIG. | :511 |
| SCAT-MODE-CONFIG | S | simplify | Same fold (and goes if attribution is boolean). | :497 |
| SCAT-SUGGEST-CONFIG | S | cut | Validates a config key that exists only for SCAT-MENTION. | :522 |
| SCAT-MENTION | S/P | cut | Off by default; plain-text name matching with hyphen/space variants and kind-based exclusions (`checks/mention.py:1-110`). It nags coders to link words, which pushes toward more links, i.e. detail, not synthesis. Opt-in, so it is also a config key, a rule, a schema entry and docs. | :535 |
| SCAT-NOEDGES | M | simplify | A `done` narrative with no rows. Useful nudge, but merge with UNCODED into one warning "this narrative adds nothing to the graph". | :547 |
| SCAT-UNCODED | M | keep | Without it a narrative silently vanishes from every view (`page-contracts.md:174-186`). Merge with NOEDGES. | :560 |
| SCAT-*-TABLE-HEADER (x2) | S | simplify | Header order and separator row. A lenient reader that finds the four columns by name would remove it, and the "advisory" fix kind. | :579 |
| SCAT-*-TABLE-ROW (x2) | S | keep | A row that cannot be read tells no edge; the coder must hear that. Keep one of the table-syntax ids. | :594 |
| SCAT-*-TABLE-TYPE (x2) | S | keep | Unknown edge type: needed. Verb or slug both accepted already. | :606 |
| SCAT-*-TABLE-LAYERS (x2) | S/M | keep | This is the grammar of the ontology (group holds concern...). It is the one table rule that carries meaning. | :621 |
| SCAT-*-TABLE-SECOND (x2) | S | cut | A second table or heading. Read every table under the heading and the rule has no reason to exist. | :636 |
| SCAT-*-TABLE-DUPLICATE (x2) | S | cut | The graph already keeps one edge per triple and names each telling (`page-contracts.md:244-246`); a repeated row is harmless. | :649 |
| SCAT-*-END-NOLINK (x2) | S | simplify | An end that is not exactly one link. Fold into TABLE-ROW. | :669 |
| SCAT-*-END-NOPAGE (x2) | S | simplify | Duplicates SCAT-LINK-DANGLING-BODY by its own admission (variants a, b, c of it, `:687`). One rule for every dangling link. | :686 |
| SCAT-*-END-NOTNODE (x2) | S | simplify | End is a narrative or contributor page. Fold into TABLE-LAYERS ("wrong kind of page"). | :700 |
| DRAFT/DONE twin ids (the doubling itself) | S | cut | 9 rules become 18 ids and every test seed runs three times (`:262-263`). One id with severity set by status achieves the same. | :137-190 |
| SCAT-DONE-REFUSED | S/P | keep | `set-status done` refuses with the list of errors. This is the right way made easy: you cannot call something done that does not hold together. | :723-754 |
| Structured fixes (kinds exact/slot/options/advisory/manual, 6 edit actions) | S/P | cut | A fix as data lets a program apply it (`machine-interface.md:50-72`). A coder reads one sentence and edits. `checks/fixes.py` 135 + `fix.py` 138 + schema 765 lines + golden tests. | :230-262; `src/scat_tools/fix.py:1-30` |
| Retired-ids list (14 rows) | S | cut | History in a contract. Keep in git. | :178-188 |

### 2b. CLI commands (`src/scat_tools/cli.py`)

| Item | S/M/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| `scat check` (page, `--neighborhood`) | S/P | keep | The core loop. Drop `--neighborhood`; page vs vault is enough. | cli.py:46-56 |
| `scat status` | P | keep | A worklist of what is stub/draft/done. Tiny and useful. Drop `--neighborhood`. | cli.py:57-67 |
| `scat set-status` | S/P | keep | Gate to `done`. | cli.py:68-74 |
| `scat index` | P | simplify | Writes 5 static Base files once. The template already ships them (`tpl-pin3/index/*.base`). Move to template; remove command, `ops/index.py`, an `index` stage output and a "report" step. | cli.py:75-79; ops/index.py:1-95 |
| `scat stub` | P | keep | Creates a page with correct frontmatter. Right way easy. | cli.py:80-92 |
| `scat stub-links` | P | simplify | `record-edge` already stubs missing ends. Fold into `stub` ("stub what my links need"). | cli.py:93-98 |
| `scat record-edge` | S/P | keep | Writes a valid row; hand-typing a four-cell table is where most syntax errors come from. | cli.py:99-120 |
| `scat remove-edge` | P | cut | Deleting a table line in Obsidian is easier and safer than a CLI call. Exists chiefly so an assistant need not edit text (A9). | cli.py:121-134 |
| `scat merge` (`--plan`) | P | keep | The synthesis operation: two concrete-ish nodes become one abstract one, links rewritten. Check-before-write design is sound. 598 lines is heavy; *(unsure)* whether the temp-copy proof is needed. | cli.py:135-149; ops/merge.py:1-17 |
| `scat split-plan` | P | simplify | Writes nothing; only lists links to re-point by hand. A `grep` for the node name does that. Fold into `evidence`. | cli.py:150-157; ops/split.py |
| `scat fingerprint` | P | simplify | Identical to `layered --narrative X`; the views doc defines layered as "the union of fingerprints" (`views.py:1-30`). One command. | cli.py:158-169 |
| `scat edges` | P | keep | One table of who tells what. Fold CSV export in as `--csv`. | cli.py:170-180 |
| `scat layered` | P | keep | The "big picture" of the abstract structure. | cli.py:181-198 |
| `scat trace` | P | simplify | A filter on layered (`--from NODE`). Own command, own drawing, own MCP tool. | cli.py:199-213 |
| `scat evidence` | P | keep | The best tool here for the brief: all the concrete passages behind one abstraction, with edges and neighbours. | cli.py:214-223; evidence.py:1-17 |
| `scat copy-share` | P | cut | Five-word-run overlap between a node page and narratives. A crude plagiarism check on whether a node page was pasted from one narrative. The norm (write across narratives) belongs in guidance, not a metric. | cli.py:224-237; copyshare.py:1-30 |
| `scat review` | P | simplify | Candidate duplicates by Jaccard on neighbours, cosine on descriptions, twin rows, hub detection, plus "pages to re-read" with 7 tunable thresholds (`review.py:41-50`). On the template it found one pair on a twin-row signal alone. Keep one signal (twin rows or shared neighbours); drop cosine, hubs, re-read. | cli.py:238-245; review.py:1-60 |
| `scat attribution` | P | cut | A listing of narratives per contributor; goes with contributors. | cli.py:246-252 |
| `scat export-edges` | P | simplify | Writes CSV and Markdown per type. Make it `edges --csv`; drop the Markdown twin. | cli.py:253-262; export.py:1-30 |
| `scat guide` | P | cut | Prints the stage list and 12 transitions. Part of the lifecycle machine. | cli.py:263-269; guides/__init__.py |
| `scat draw fingerprint / layered / trace` | P | simplify | One drawing is useful (layered, since the picture is the pattern). 647 lines of crossing minimisation, bands and narrative-mark colours (`draw.py:1-40`); needs matplotlib extra. Keep layered only, simple column layout. *(unsure how much the layout work pays off)* | cli.py:270-331; draw.py:1-40 |
| Global flags `--root`, `--json` | S | simplify | `--json` binds every command to a 765-line schema (`machine-interface.schema.json`). Keep for MCP use if any; otherwise cut. | cli.py:35-45; machine-interface.md:1-12 |

### 2c. MCP tools, prompts, resource (`src/scat_tools/mcp_server/`)

| Item | S/M/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| `check`, `status`, `stub`, `stub_links`, `record_edge`, `merge`, `evidence`, `layered`, `edge_table` | P | keep (or as per CLI) | A thin wrapper over the same operations; keep exactly those that survive on the CLI. | server.py:44-66, 91-155, 240-285 |
| `set_status` | S/P | keep | Wrapper refuses `done` (server-side guard for the assistant). | server.py:61-90 |
| `remove_edge`, `split_plan`, `index`, `trace`, `fingerprint`, `copy_share`, `review`, `attribution`, `export_edges` | P | cut / simplify | Each follows its CLI verdict. Each is a tool description the assistant must read and choose among; fewer tools is a better assistant. | server.py:101-320 |
| `which_stage`, `set_stage` | P | cut | A project-level state machine (5 stages, 12 transitions, `lifecycle.toml`), enforced by refusal (`stage.py:1-10`). An unset vault answers every call with a "tell me the stage" refusal (`lifecycle.md:22`). That makes the wrong thing (nothing works) the default and the right thing (name a stage) a chore. The assistant gets nothing from it that the coder's chat message does not give. | stage.py:1-60; lifecycle.md:12-165 |
| Stage tool allow-lists (plan: 4 tools, capture: 2, ...) | P | cut | Limits what the assistant may call per stage; the coder cannot see why `fingerprint` is "not offered in the plan stage". | lifecycle.md:61-125; stage.py:166-176 |
| 6 prompts (`code-a-narrative`, `explain-a-problem`, `review-before-done`, `draft-a-node-page`, `fill-in-node-pages`, `look-for-duplicates`) | P | simplify | Each repeats RULES text (`prompts.py:7-27`) and a numbered loop. Keep `code-a-narrative`; the others are the same loop with a different noun. | server.py:343-382; prompts.py:1-104 |
| Resource `assistant-rules` | P | cut | The same rules appear a third time (`contracts/assistant.md`, `skills/scat-coding/SKILL.md`, `prompts.RULES`). One copy. | server.py:385-391 |
| HTTP transport and key gate | S | simplify | `gated()` ASGI wrapper, header parsing, loopback refusal rules (`gate.py:1-53`). Needed only for the tunnelled chat path; stdio needs none of it. *(unsure)* whether the chat path can be reached another way. | gate.py:1-53; __main__.py:30-61 |

### 2d. Views

| Item | S/M/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| Fingerprint view (per narrative) | M/P | simplify | Same data as layered for one narrative. One view, not two. | views.py:1-30 |
| Edge table view | M/P | keep | | views.py |
| Layered view | M/P | keep | | views.py |
| Trace view | M/P | simplify | A node-rooted filter of layered. | views.py |
| Evidence view | M/P | keep | The core support for abstraction. | evidence.py:1-17 |
| Copy-share view | P | cut | See above. | copyshare.py:1-30 |
| Review view | P | simplify | See above. | review.py:1-60 |
| Attribution view | P | cut | See above. | views.py:21-24 |
| Candidates (`--candidates`, links with no row) | M/P | keep | The one place the tool says "you named both ends but did not code the edge". It directly serves the coding step. | page-contracts.md:166-172; rule-catalogue.md:713-721 |
| Excluded-narrative notice on every view | P | keep | Without it a narrative disappears silently. | views.py:1-30 |
| Drawings | P | simplify | See `draw`. | draw.py |

### 2e. Ontology classes and properties (`ontology/scat.ttl`)

| Item | S/M/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| `scat:Group`, `Concern`, `Affordance`, `Technology` | M | keep | The four layers; the heart of the meta-model. Trim the long source annotations (see below). | scat.ttl:71, 82, 93, 105 |
| `scat:EdgeType` | S | simplify | A class whose only members are the three properties; used so no tool keeps a copy of the three types. A comment would do. | scat.ttl:122 |
| `scat:Heldby`, `Addresses`, `ProvidedBy` | M | keep | The three edge types. Odd name `Heldby`, but the plain labels cover it. | scat.ttl:128, 140, 151 |
| `scat:Narrative` | M | keep | | scat.ttl:166 |
| `scat:Contributor` | M | simplify | Tied to the attribution mode; keep only if attribution stays, as plain names not pages. | scat.ttl:178 |
| `scat:Index` | S | cut | Not a page, no fields; a class that exists to say it has no fields (`carriesStatus false`). | scat.ttl:187 |
| `scat:TableColumn` and `column-type/from/to/note` | S | cut | Four instances, plus `tableColumns`, `cellHolds`, to tell a reader the columns are from, type, to, note. The contract says it too (`page-contracts.md:174-200`). | scat.ttl:200-231, 383, 388 |
| `scat:Field` and `field-type`, `status`, `title`, `description` | S | keep | The frontmatter. | scat.ttl:238-270 |
| `scat:field-timeframe` | M | simplify | Required at `done`. A facilitation tag; make optional. | scat.ttl:272 |
| `scat:field-kind` | M | keep | Optional label. | scat.ttl:279 |
| `scat:field-attributed_to` | M | simplify | With contributors. | scat.ttl:286 |
| `scat:status`, `StatusValues`, `stub`, `draft`, `done` | M | keep / simplify | The lifecycle is good. The `skos:OrderedCollection` and `memberList` ceremony could be three plain values. | scat.ttl:297-330 |
| `scat:carriesStatus`, `discouragedField` | S | cut | `carriesStatus` is for the Index only; `discouragedField` is "used by no type" (`scat.ttl:358`). | scat.ttl:333, 358 |
| `scat:mapsTo` | S | cut | No code in `src/` reads it (grep: no hits). | scat.ttl:393 |
| `scat:key`, `pageDescription`, `requiredField`, `optionalField`, `requiredFrom`, `valueSet`, `targetType`, `endpointOrder`, `verb`, `slug`, `tableHeading` | S | simplify | Needed if the TBox is the single source of schema (R-13); but each is a bespoke annotation property to say what a Python dict could say. *(unsure)* what the TBox's external readers (analysts using rdflib) need. | scat.ttl:338-408 |
| `scat:source`, `authored`, `verification` | M | cut (from the TTL) | Provenance of every term, including "unverified" flags. Useful to the ontologist; zero value to the coder; the maintainer must keep three annotations on every term in step. Move to a docs page. | scat.ttl:413-426 |

### 2f. Other significant features

| Item | S/M/P | Verdict | Reason | Evidence |
|---|---|---|---|---|
| Lifecycle stages (5 stages, 12 transitions, `lifecycle.toml`, `guides/*.md`) | P | cut | See `which_stage`. The loop is already the coder's own knowledge. Also ships `contracts/lifecycle.md` into the wheel (`pyproject.toml:38`). | contracts/lifecycle.md:12-165 |
| Machine-interface schema (v3) and `--json` documents | S | cut | 765-line schema for outputs that only a program reads. | contracts/machine-interface.schema.json; machine-interface.md |
| SCATLAB (menu-bar app, Docker, Tailscale Funnel, keychain, 713-line launcher, 250-line AppleScript, `retire-old.sh`) | P | simplify *(unsure)* | The mission requires a chat path with no terminal (`MISSION.md`, paths 1-4). This is the single largest support burden: macOS only, three third-party runtimes, tests with stubbed docker/tailscale/security. I cannot see a cheaper route to a terminal-free chat path; if one exists, take it. | deploy/README.md:1-29; deploy/scatlab.sh:1-40 |
| Relationship annotation (a free line "Pulls against [[x]]") | M | keep | Costs nothing: no rule, no view, "no meaning to the tool". Models disagreement in prose. | page-contracts.md:294-305 |
| `analysis.ipynb` in the template | P | simplify | Needs a `notebook` dependency group (jupyterlab, nbconvert, nbclient, ipykernel) just to show what `scat layered` prints. | tpl-pin3/pyproject.toml; docs/analysis.md |
| `skills/scat-coding/SKILL.md` and `contracts/assistant.md` | P | simplify | 20 numbered SHALL/MAY rules (A1-A20) say, in ~200 lines, "the coder decides". Third copy in `prompts.RULES`. One copy of one paragraph would serve. | skills/scat-coding/SKILL.md:1-163; contracts/assistant.md:1-58 |
| `decisions/log.md` (D-nnn references everywhere) | P | cut (from the shipped repo) | 3,440 lines of rationale that source files and TTL cite by number (`scat.ttl:1-60`). A reader must open the log to read a comment. | decisions/log.md |

## 3. Top five cuts, most valuable first

1. **Delete the lifecycle/stage machine** (`which_stage`, `set_stage`, `lifecycle.toml`, the 5 guides, `scat guide`, per-stage tool
   refusals, 12 transitions, `contracts/lifecycle.md`, its tests). Frees the coder from a vault that refuses to work until
   someone has "named the stage", and from learning the word "stage" alongside "status". Frees the maintainer from one more
   consistency test between a YAML block in a Markdown file and the code (`lifecycle.md:39-43`). Nothing the coder does in
   synthesis depends on it.
2. **Make fixes plain text, not data.** Drop the fix kinds, edit actions, `Command`/`Edit` objects and `--json` schema
   (`fix.py`, `checks/fixes.py`, the 765-line schema, golden tests for every message variant). A coder reads "replace X with Y".
   Frees the coder from nothing visible, but frees the maintainer from the largest single source of lock-step changes: every
   new rule needs a fix kind, options, edits and a schema entry. If a program must drive the tool, give it `check`'s text.
3. **Collapse the table rules.** Nine rules in DRAFT/DONE twins (18 ids) plus DANGLING-BODY plus the FM-* family plus three
   CONFIG rules become roughly: file unreadable, value not allowed, row unreadable, wrong layers, link goes nowhere, config bad.
   One id each, severity set by status (errors at `done`, warnings before). Read the table leniently (all tables under the
   heading, any column order by header name, duplicates harmless). Frees the coder from learning a dozen ways a table can be
   wrong; they learn "a row says: from, verb, to".
4. **Cut the attribution apparatus to a yes/no.** Contributor pages, `attributed_to`, a 3-way mode with required/optional
   pairs, 4 rules, the `attribution` view, CLI command and MCP tool. If the vault wants names, a plain `contributors:` list in
   frontmatter does it; if not, nothing. Frees the coder from a decision (and a config key) that has no bearing on drawing patterns,
   and the maintainer from a second page type threaded through every view ("contributor pages are in no other view",
   `views.py:21-24`).
5. **Prune the analysis tools to what serves abstraction:** keep `evidence`, `layered` (absorbing fingerprint, trace and the
   one drawing), `edges` (absorbing CSV), `merge`; cut `copy-share`, cosine/hub/re-read parts of `review`, `split-plan`, `export-edges`
   as a command and the separate drawing commands. Frees the coder from a menu of 8 view commands with overlapping meaning and
   from numbers (a "share of 0.43", a Jaccard of 0.5) that they must be told not to trust ("a prompt to look, not a fault",
   `copyshare.py:1-30`).

Honourable mentions: remove SCAT-MENTION and `link_suggestions`; drop the SCAT-DRAFT-FIELD warning; move `scat index` to the
template; strip the three provenance annotations from the TTL; keep one copy of the assistant rules.

## 4. Missing, if the point of the exercise needs it (no more than three)

1. **Recurrence per node.** The point is to find patterns, and a pattern is something that recurs. The tools show per-edge
   tellings (`edges`) and per-node evidence, but I found no plain listing "node, number of narratives that link it, number that
   tell an edge to it, in order". `status` counts pages (`cli.py:57-67`), `review` re-read needs 4 or more narratives
   (`review.py:48`). A one-column count on `layered` or `status` would let the coder see at a glance which nodes are
   thin (one narrative: still concrete) and which are load-bearing. *(unsure)* I did not read `views.py` end to end; it may exist
   inside the layered footer, which `docs/analysis.md` says "does not weigh a node by how many lines meet it".
2. **A way to see the concrete under a row.** `evidence` shows narrative paragraphs around links, but a row's `note` is a
   free-text cell with "no meaning to the tool" (`scat.ttl:227-231`). If abstraction is the aim, the row note is where the
   coder keeps the concrete quote or pointer to field notes; the views should show it next to the edge (the edge table does
   carry `narratives`; whether it prints `note` I did not confirm).
3. **A rename/promote operation.** Merge folds A into B, but I found no `rename` of a node page (grep: no hit in `ops/`). In
   abstraction, a node's name changes as accounts accumulate ("broken drill" becomes "unsafe equipment"); today that is
   hand-editing every link, with `merge` as the nearest tool and it needs two existing pages. A rename that rewrites links
   would be the abstraction move in its simplest form.

## What I would not touch

The four layers, the three edge types, the one-row-one-edge table, `check`, `stub`, `record-edge`, `set-status` with its refusal,
the `done` gate, `merge --plan`, `evidence`, the cap, and the template vault. They are small, legible, and carry the meaning.
The trouble is not the core; it is how many fences have been built around it.
