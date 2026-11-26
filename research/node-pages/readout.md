# RS4 readout: node-page synthesis

Scripts and drafts are in `research/node-pages/notes/`. Everything was run on the range vault (9 narratives, 27 nodes, 27 edges) unless said otherwise; the template example and lab vaults are too small to say more. No assistant was run: the drafts are by hand.

## Recommendation

Build help in two packages. Package A: a per-node **evidence view**, a **norm** for what a node page holds, and an **MCP prompt and skill** that drafts a page for the coder to accept. Package B, after A has been used: a **review view** that proposes synonym/homonym candidates, and one tool operation, **merge**, with a dry-run plan (split is a plan only). The coder decides whether two pages are one concept.

## Q1. Evidence for one node

`evidence.py` builds the view from what the vault already holds: `scat_kg.load` gives the node, its edges with every telling (narrative and note) and its neighbours; the account's text is read from the narrative files. It returns, for one node: each narrative that links it (status, kind, timeframe), the passages that link it, the link text the coder wrote, the edges with narrative and note, neighbours by layer, and which narratives link the node but tell no edge for it.

On `community-members` it showed five narratives, four edges, and three narratives saying the page is a cluster. Two things the view must handle:
- A link marks where a name first appears, not every mention. For `shared-data-set-integrity` the sentences that matter ("a club good") do not carry the link. Return the whole paragraph with the linking sentence marked, not the sentence alone.
- The range vault is sparse across narratives: only 7 of 27 nodes appear in two or more narratives; 12 of 13 concerns appear in one. Synthesis across narratives is real for groups and a few others; for the rest the page synthesises one narrative's passages and edges, and says so.

## Q2. Synthesis, not copying

I drafted `community-members` (group), `shared-data-set-integrity` (concern), `forget-signal` (affordance) and `telescope` (technology) from the evidence. Dropped into a copy of the vault they pass `scat check` (0 errors) and leave the knowledge graph unchanged (same edges, tellings and fingerprints), because a node page's links to narratives are not read as edges.

Each draft has four parts, which I suggest as the norm: **what it is** in the group's or concept's own terms; **how the narratives tell it** (a citation by link for each claim, recurrence named); **where accounts differ** (kept, not merged: ant-rdf's rule that no view presents the union of viewpoints as the single truth); **thin** (what no narrative says).

A cheap measure of copying: the share of a page's five-word runs found verbatim in any narrative (`copycheck.py`). The drafts score 0 to 14%. The existing descriptions in the range vault score a mean of 25%, and `resources-referable-across-subnets` and `it-that-just-works` score 100%, which is the chief engineer's observation measured. As a norm this is a prompt to look, not a rule.

Assistant fit: drafting is A1 and A2 (text for the coder), the evidence view is A4, the coder pastes or edits, the draft names what it cites (A13), and the page stays `draft` until the coder sets `done` (A7). Drafting needs no new rule; merge does (below).

## Q3. Synonyms and homonyms

Methods tried on the range vault, none by matching names:

1. **Structural role** (neighbour sets over edges). Two pairs score 1.00: `requisite-variety` / `vendor-lock-in` (both held by the technical team, both addressed by the KOI doctrine) and `how-members-figure-in-koi` / `what-integration-does-to-the-protocol` (both held by two groups). Read by hand, the first pair is related but distinct; the second is one concern read two ways by two groups, recorded on purpose. A candidate list is a review prompt, not a merge list.
2. **Context split** (nodes co-linked in each narrative, overlap across narratives). Low for every multi-narrative node (about 0.1), because narratives differ in topic; alone it flags everything.
3. **Link-text profile** (the words the coder put in `[[node|text]]`). With the coder's own cues ("here clustered") it finds homonym by design: the cap forces broad groups, so a group page is deliberately several things.
4. **Description reuse** across all pages. Finds `resources-referable-across-subnets` (concern) and `resource-identifier` (affordance) with 82% overlap: one text on two layers, which is a conflation to review, not a synonym.
5. **Passage tf-idf similarity** over the paragraphs that link each node. Found nothing: pairs scored high only because they shared a paragraph; among same-layer pairs sharing no narrative the top score was 0.22. On a vault this sparse it does not work; it needs many narratives per node.


**Smallest safe operation: `merge A into B`**, same type only. `merge.py` does it on a copy: rewrite every body link `[[A…]]` to `[[B…]]`, keeping the shown text (a bare link in prose becomes `[[B|A]]`; one in a table end stays bare); append A's body to B under a heading; delete A; then run the check and compare the graph with the old graph under A→B. Tried on five pairs (two concerns, two affordances, two groups, one collision, one cross-type): the graph matched the old one under A→B each time, the cross-type pair was refused, and the collision was caught by the existing check (SCAT-DONE-TABLE-DUPLICATE).

Conformance argument: every link is rewritten, so none dangles; names stay unique slugs (a page is only removed); same type keeps every row's layers valid; the cap only falls for groups; one edge per (type, from, to) is kept by the graph, which unites the tellings; and a narrative that ends with two identical rows is refused, listing both rows, with nothing written. Rename is Obsidian's job already (contract 2); merge into a name that does not exist adds nothing. Split cannot be automated: the tool prints, per narrative, the links and rows naming A, the coder assigns each narrative to A or to a new stub A2, and apply rewrites those links; a narrative that uses both senses is edited by hand. A group split is refused over the cap.

Decision for the coder: the merge changes `done` narratives' links. Leave their status and list them, or move them to `draft`. The assistant may call the dry-run plan; the apply is the coder's act, like `done`.

## Q4. The shape of the help

| Part | Kind |
|---|---|
| Evidence for one node; review view (candidates A, 3, 4 above, copy share, clusters); merge/split plan; merge apply | view / tool operation |
| Draft a node page from the evidence; propose merge/split candidates with reasons | MCP prompt and skill |
| Sweep: list stubs and drafts, worst first (most narratives, fewest words), draft one at a time, the coder accepts each | workflow (a loop of the above, no new tool) |
| The four parts of a page; cite, don't paste; keep disagreement; clustered groups say so; a candidate is not a merge | norm (docs/norms.md, coding.md) |

Both paths run on the same view calls: the coder runs `scat evidence` and writes, or the assistant runs it and drafts. The human-only pass stays repetitive, as the chief engineer says; the view speeds it, not skips it.

## Q5. Prior art

- Codebooks with definitions and inclusion and exclusion rules, kept by a team (MacQueen, McLellan, Kay and Milstein 1998, *Cultural Anthropology Methods* 10(2): <https://journals.sagepub.com/doi/10.1177/1525822X980100020301>) correspond to node pages with a description and "where it differs".
- Axial coding relates categories to their subcategories (Strauss and Corbin, *Basics of Qualitative Research*; constant comparison from Glaser and Strauss 1967), and is contested as over-prescriptive (Glaser 1992) and optional (Charmaz 2006): <https://methods.sagepub.com/ency/edvol/embed/sage-encyc-qualitative-research-methods/chpt/axial-coding>. SCAT's typed edges already are the axial step, so only the consolidation of codes is missing.
- SKOS separates `exactMatch`, `closeMatch` and `related`, which `research/ontology/readout.md` already uses. The same grading fits candidates: same, close, related (a relationship annotation).

Cited from search results, not full texts.

## Proposed package: node-page help

Goals: a coder can see everything the vault says of a node in one view; can get a draft synthesis to accept; can find and act on likely duplicates or overloads. Points are rough, one point being about half a day of agent work.

| Unit | Points |
|---|---|
| A1 `scat evidence <node>`, API and MCP view call, paragraph-with-link marked | 3 |
| A2 Norm: the four parts and node-page contract text; copy-share check as a view | 3 |
| A3 MCP prompt and skill: draft one node page; sweep workflow | 3 |
| A4 Tried by cold users on a larger vault | 2 |
| B1 Review view: structural candidates, clusters, description reuse | 3 |
| B2 `merge` with plan, refusal and conformance test; split plan | 5 |
| B3 Assistant rule for merge; docs | 1 |

A is 11 points, B 9.

## Open

- A real assistant draft (the lab assistant was not run).
- Whether merge leaves `done` narratives `done`.
- Method results need a vault with many narratives per node.
