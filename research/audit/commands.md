# WP40 item 9: every command, by what the coder does with it

> **Background, not direction.** This page records reviewers' and the ACE's proposals before the chief engineer
> decided. Most proposed cuts were **not** adopted. The direction is in [final-report.md](final-report.md) and decisions/log.md
> (D-216 to D-238).

Asked for by the chief engineer: "list them out and map them to what activity the coder uses them for. what are they
interpreting or reviewing". There are 22 CLI commands (`scat --help`, plus `draw`) and 21 MCP tools (19 that mirror a
command, plus `which_stage` and `set_stage`). "Stages" lists where the MCP server offers the tool (`contracts/lifecycle.md:45-122`).

## Setting up the vault

| Command (MCP tool) | What it does | What the person interprets or reviews | Stages |
|---|---|---|---|
| `index` (index) | Writes one Obsidian Base page per type (`index/<type>.base`), once; never rewrites | Nothing to interpret: it gives Obsidian a table of the pages of each type | code, report |
| `stub` (stub) | Creates a page with `status: stub`: a node, a narrative, or a contributor where attribution is on | Which concept or account deserves a page | plan, code |
| — (which_stage, set_stage) | Reads and moves the project's stage, signed by the person | Where the project is, and whether its exit holds | all |
| `guide` | Prints a stage's guide | What the work of this stage is | CLI only |

## Coding one narrative

| Command (MCP tool) | What it does | What the person interprets or reviews | Stages |
|---|---|---|---|
| `record-edge` (record_edge) | Adds an edge's row to the narratives that tell it, stubbing a missing node | The coder's claim: this account tells that this group holds that concern (and so on) | code |
| `remove-edge` (remove_edge) | Deletes an edge's rows | A claim the coder withdraws | code |
| `stub-links` (stub_links) | Creates the node pages that row ends link but the vault lacks | Nothing new: it fills in pages for codes already named | code |
| `check` (check) | Runs the rules; each problem comes with its fix | Conformance only: what is malformed and how to fix it; never whether the coding is right | every stage |
| `fingerprint` (fingerprint) | One narrative's nodes by layer and the edges its rows tell; `--candidates` adds linked pairs with no row | Did I code this account the way I read it? What did I link but not claim? | code, analyse, report |
| `status` (status) | Each page's status and the counts | Progress: what is still stub or draft | every stage |
| `set-status` (set_status) | Sets stub, draft or done; `done` is refused while errors stand | The coder's attestation that the account fits the notes | code |

## Consolidating codes

| Command (MCP tool) | What it does | What the person interprets or reviews | Stages |
|---|---|---|---|
| `review` (review) | Proposes possible duplicate pages and pages whose accounts diverge (plain signals after D-225) | Are these two codes one concept? Is this code doing two jobs? | code, analyse |
| `merge` (merge, plan only) | Folds page A into B: every link to A becomes a link to B (C22 changes how the body is handled) | The decision that two concrete codes are one more abstract one | code (CLI applies, MCP plans) |
| `split-plan` (split_plan) | Lists every narrative, link and row naming a page, so the coder can split it by hand | Which accounts use the code in which sense | code |

## Reading across narratives

| Command (MCP tool) | What it does | What the person interprets or reviews | Stages |
|---|---|---|---|
| `layered` (layered) | The union of the fingerprints of all, or chosen, narratives in the four layers; `--candidates` too | The big picture: what is shared across accounts, what stands alone | code, analyse, report |
| `edges` (edge_table) | Every edge of one type, with the narratives that tell it | Which claims recur across accounts, and which rest on one | code, analyse, report |
| `trace` (trace) | Follows edges from one node up to the groups, down to the technologies | For one concern: who holds it, and what is offered to address it | code, analyse, report |
| `evidence` (evidence) | Everything the vault says of one node: each linking paragraph, its edges and the narratives behind them, its neighbours | What a code rests on in the accounts: the basis for writing or revising its definition | code, analyse |
| `attribution` (attribution) | Narratives by contributor, where attribution is on | Whose accounts the patterns rest on | plan, code, analyse, report |

## Handing over and reporting

| Command (MCP tool) | What it does | What the person interprets or reviews | Stages |
|---|---|---|---|
| `export-edges` (export_edges) | Writes the edge tables as CSV | Nothing in the tool: it is for analysis elsewhere | analyse, report |
| `draw` | PNG or SVG of a fingerprint, the layered view or a trace | The same as the view it draws, as a picture for a report | CLI and notebook |

## Already decided

- `copy-share` (copy_share) is cut (D-225). It scored how much of a node page was copied verbatim from narratives.

## The ones most likely unfamiliar

`index`, `stub-links`, `split-plan`, `trace`, `guide` and `export-edges`. Each is in the tables above.
