# scat_analysis: reading a SCAT vault as a graph

A small, tested Python package and one notebook for a data or network scientist who wants the "big picture" of a SCAT vault: where the coded chain stops, where concerns pull against each other, where structure concentrates. It describes; it never ranks stories, groups or architectures as better or worse. This is research-spike code (RS2, continued under D-054); it is not part of `scat_kg` and is not merged into `dev`.

## Run it

Prerequisite: [uv](https://docs.astral.sh/uv/). Nothing else to install; `uv` builds the environment (including `scat_kg` from this checkout, two directories up) on first use.

One command, from the repo checkout:

```
cd research/analysis && uv run jupyter lab notebook/scat-graph-analysis.ipynb
```

Headless (what CI would do), and the tests:

```
cd research/analysis
uv run jupyter nbconvert --to notebook --execute --output executed.ipynb notebook/scat-graph-analysis.ipynb
uv run pytest -q
```

The notebook runs offline on two vaults committed here: `notebook/case-study/` (a copy of the template's case study) and `synth/vault/` (synthetic, see below). Point it at your own vault by editing the path variables in its second cell. `status="done"` (variable `STATUS`) keeps only signed-off pages.

## Use it in your own notebook

```python
import scat_analysis as sa
from scat_analysis import plots

sg = sa.load_graph("path/to/vault")        # status="done" to keep signed-off pages only
sa.traceability(sg)                        # one function per analysis; each returns a DataFrame or plain data
plots.draw_layered(sg)                     # plotting helpers draw onto a matplotlib Axes
```

`sg.G` is a directed `networkx` graph (group, concern, affordance, technology; edges `heldby`, `addresses`, `attributes`). `sg.conflicts` is an undirected graph over concerns. `sg.records` is the table of coded records.

## Before you trust any of it

These results are only as good as the vault:

1. `uv run scat check --root <vault>` must pass (conformance: structure).
2. The facilitator/coder must have signed off the content as reflecting the interviews and discussions (content). Filter with `status="done"`.

Conformance checks structure and never content. Conflicts, for example, are never flagged by `scat check`; they are surfaced here, after sign-off. Every gap or tension below is a statement about what was coded, not about the real system.

## What each analysis tells you

For each: the question, how to read it, what it does not mean, and what to do first. "First" always includes the two steps above.

### 1. Traceability and gaps: `traceability`, `group_coverage`, `gaps`
- **Question.** For each concern, who holds it, what addresses it, which technologies stand behind that? Where does the chain stop?
- **Read.** `chain` is `complete`, `addressed, no technology` or `unaddressed`. `gaps` lists concerns no affordance addresses, affordances with no technology, groups holding no concern, and groups whose concerns are all unaddressed.
- **Not.** A verdict of neglect or an unmet need. The vault may not yet be coded that far.
- **First.** Check with the coder that each listed gap is a real absence of coding, not a missed page.

### 2. Projections: `projections`, `projection`
- **Question.** Which groups share concerns, and which concerns share an affordance?
- **Read.** Edges join nodes of one kind that reach a common node of the next; `shared` counts them and `via` names them.
- **Not.** Agreement. Groups can share a concern for opposite ends. A hub makes a clique of its neighbours.
- **First.** Read tension (3) alongside, and note which hubs create the dense parts.

### 3. Tension: `tension`
- **Question.** Which concern pairs are declared to conflict, which groups hold both sides, and which groups hold opposite sides?
- **Read.** `pairs` (one row per pair, the symmetric closure of the declared links), `both_sides` (a group carrying a trade-off), `opposite_sides`.
- **Not.** A disagreement that happened, a flaw, or adversaries. No declared conflict does not mean harmony; two concerns may simply not have been compared.
- **First.** Confirm with the coder that the declared conflicts are the ones the interviews support.

### 4. Centrality and brokerage: `centrality`
- **Question.** Where do recorded concerns concentrate, and which nodes sit between otherwise separate parts?
- **Read.** `concerns_carried`, `groups_behind`, `degree`, `betweenness`, per affordance and technology, listed alphabetically.
- **Not.** Importance, quality or risk. The counts depend on how finely concerns were written and how many records were coded. Do not compare across vaults.
- **First.** Check that concerns were written at a similar grain; one split concern moves these counts.

### 5. Communities: `communities`, `community_agreement`
- **Question.** Does the graph fall into densely linked clusters that cut across layers?
- **Read.** Two algorithms (greedy modularity, Louvain, fixed `seed`, default 1) in one table; `community_agreement` is their overlap from 0 to 1. Low agreement means weak clustering; hold any partition loosely.
- **Not.** Teams, workstreams or architectures. The most fragile analysis: treat it as optional until vaults hold more than a few dozen nodes.
- **First.** Report both partitions and the agreement, never one alone.

### 6. Provenance: `provenance`, `provenance_matrix`, `conflict_records`
- **Question.** Which nodes does each coded scenario or architecture record name, and which records name both ends of a conflict?
- **Read.** A long table (record, kind, role, node), a record-by-concern matrix, and the records that name a conflicting pair.
- **Not.** Fullness or quality of an account; records differ in what they were written to cover.
- **First.** Confirm that records are coded against the same nodes you are analysing (same status filter).

## What the data can and cannot show

- **The case study is too small.** 3 groups, 3 concerns, three disjoint chains, one conflict: every count is 1 and there is no pattern to find. It shows that the loader works on a real vault and what the gaps look like at a glance (`attribution` is held by no group and addressed by nothing; `workshop-participants` hold no concern).
- **The synthetic vault has planted patterns.** A fictional water cooperative (7 groups, 18 concerns, 13 affordances, 10 technologies, 5 conflicts, 7 records), generated with a fixed seed. `synth/README.md` lists what was placed where (gaps, a group holding both sides, groups on opposite sides, hubs). So each analysis finds what was put there: this shows the analyses run and read sensibly, not that they surface anything unexpected on real, signed-off content.
- Vaults here are tens to hundreds of nodes; nothing is tuned for scale.

## Layout

```
src/scat_analysis/   graph.py (load_graph, ScatGraph), analyses.py, plots.py
tests/               facts on both vaults; no rank/score columns; deterministic communities
notebook/            scat-graph-analysis.ipynb, executed.ipynb (re-run output), case-study/
synth/               generate.py and the generated vault (do not edit by hand)
readout.md           the spike's findings, library choice and what core could provide
```

## What `scat_kg` lacks for this (worked around here)

`load_graph` imports `scat_kg.vault.read_vault`, which is internal: core has no public loader, no flattened edge list, no symmetric conflicts, no status filter at load time and no flattened record table. All are rebuilt in `graph.py`. See `readout.md` section 3.
