# RS2 readout: graph analysis of a SCAT vault

Spike RS2, units U2 and U3 (package `src/scat_analysis`, described in `README.md`). Everything below is backed by `notebook/scat-graph-analysis.ipynb` (executed copy: `notebook/executed.ipynb`), run on the template's case study (3 groups, 3 concerns) and the synthetic water-cooperative vault (7 groups, 18 concerns, 13 affordances, 10 technologies, 5 conflicts, 7 coded records).

## 1. The graph model

A directed, typed `networkx.DiGraph`: nodes carry `layer` (stakeholder group, concern, affordance, technology); edges run group to concern (`heldby`), concern to affordance (`addresses`), affordance to technology (`attributes`), each tagged with the relation page that wrote it. Three companions:

- **Conflicts** as a separate undirected graph over concerns. The vault declares each on one concern page only; the loader takes the symmetric closure and records `declared_by`. In the synthetic vault all 5 pairs are one-sided, so without the closure the answer to "which groups sit opposite?" would depend on which end is asked.
- **Provenance** as a table, one row per coded scenario or architecture record, listing the nodes it names. These are hyperedges (one record, many nodes); projecting them into graph edges would invent pairwise links nobody wrote.
- **Status** as a node attribute, so any analysis can be restricted to signed-off pages (`load_graph(root, status="done")`).

A layered (4-partite) graph was enough. A full multilayer model adds nothing until there is a fifth kind of thing to relate.

## 2. Meaningful analyses and how to read them

Each has a "Reads as" and a "Does not mean" block in the notebook. All are counts and structure; none orders stories, groups or architectures.

| Analysis | Finding on the data | Must not be read as |
|---|---|---|
| Traceability chains | Synthetic: 15 of 18 concerns reach a technology; 3 reach nothing; school-liaisons hold only unaddressed concerns; 3 affordances have no technology. Case study: `attribution` is held by no group and addressed by nothing; `workshop-participants` hold no concern. | A verdict on neglect. A gap is in what has been coded. |
| Bipartite projections | Synthetic: 6 of 7 groups are linked by shared concerns (13 edges); school-liaisons share none. Case study: no shared links at all. | Agreement. Shared concerns can be wanted for opposite ends. |
| Tension | Synthetic: 4 cases of a group holding both sides (board-volunteers on 3 pairs), 14 opposite-side group pairs, e.g. farm-irrigators against watershed-stewards and households. Case study: `anonymity` vs `attribution`; no group holds both, but one coded scenario names both. | Disagreement that has occurred, or a flaw. |
| Centrality and brokerage | Synthetic: `usage-dashboard` carries 8 concerns from 6 groups (the most of any affordance); `member-portal` carries 13 (the most of any technology). Case study: every node carries 1. | Importance, risk or quality. |
| Community structure | Synthetic: 7 clusters (greedy modularity) vs 6 (Louvain), agreeing on only 0.31 of same-cluster pairs. | Teams or architectures. Low agreement means weak clustering. |
| Provenance footprint | Which concerns each coded record names; which records name both sides of a conflict. | Fullness of an account. |

**Recommended set**: all six, in this order. Traceability and tension answer the spike's purpose directly (gaps, where tensions are sharpest). Centrality is useful paired with the gap list. Community structure is the most fragile: two standard algorithms disagree, so the notebook reports both and their agreement rather than one partition. Treat it as optional until vaults are larger than a few dozen nodes.

Two cautions from building it. The case study is too small to show any pattern (three disjoint chains, every count 1), so the synthetic vault is needed to see the analyses work. And the synthetic vault has its patterns built in (`synth/README.md` lists them), so each analysis finds what was placed there: the spike shows the analyses run and read sensibly, not that they surface anything unexpected on real, signed-off content.

## 3. What the tools would need to provide

What the notebook had to reach for: `scat_kg.vault.read_vault` (internal; `scat_kg.ops.common.open_vault` wraps it with a refusal path and was not needed), then `Page.type`, `.name`, `.status`, `.fields["title"]` and `.fm_links`. Nothing parses frontmatter. Class (index) pages come back as pages with no status and are skipped by type.

Gaps this exposed, in order of cost:

1. **No public loader.** From `import scat_kg` a user gets a report of problems, never the vault as data. The notebook depends on an internal module whose shape may change.
2. **Relations are pages.** Group to concern is a three-node pattern (group, relation page, concern); every consumer re-flattens it. The tools should offer the flattened edge list.
3. **Conflicts are one-sided.** Every consumer must take the symmetric closure and keep who declared it.
4. **`status()` carries no links.** A status filter has to be joined to link data by hand.
5. **Scenario and architecture records are hyperedges** with no standard flattened form (record, node, role).
6. **Identifiers are file names.** They hold while pages are not renamed, but a rename silently breaks any saved analysis; an explicit id, or a rename-aware alias, would help.
7. **No status filter at load time.** Analysis usually wants signed-off pages only; the notebook implements it as a loader argument.

## 4. Library choice

**networkx**, with pandas for tables and matplotlib for figures.
- Everything needed is built in: ancestors, betweenness, connected components, greedy modularity, Louvain. Only the one-mode projection is hand-written (about ten lines).
- Pure Python, no compiled extension, so it installs wherever `scat_kg` does. Vaults are hundreds of nodes, not millions; speed is not a constraint.
- Readable for a data scientist: nodes and edges are dictionaries, and `nx.to_pandas_edgelist` exports a table.

Lighter alternatives, rejected: plain pandas merges cover traceability and coverage but not betweenness or communities; `scipy.sparse.csgraph` covers components and paths but not communities; `igraph` and `graph-tool` are faster with richer community algorithms but add compiled dependencies for a problem this size. Revisit `igraph` only if vaults reach tens of thousands of nodes. `rdflib` (already a `scat_kg` dependency) could answer traceability by SPARQL; it is the natural bridge if the vault is exported as RDF, but the structural analyses (projections, communities) need a graph library anyway.

## 5. Sketch: analysis module and delivery package

```
scat_kg.load(root, statuses=None) -> Vault            # public loader, wraps read_vault
vault.edges()     -> DataFrame[src, rel, dst, page, status]   # flattened relations
vault.conflicts() -> DataFrame[a, b, declared_by]             # symmetric, one row per pair
vault.records()   -> DataFrame[record, kind, role, node]      # hyperedges as rows
scat_kg.graph.to_networkx(vault) -> (DiGraph, Graph, DataFrame)
scat_kg.graph.traceability / tension / carriage / projection / communities   # the notebook's functions
```

**Delivery.** Split at the dependency line. The loader and flattened tables belong in `scat_kg` itself (plain dataclasses or lists; no heavy dependency). The graph functions need networkx (and pandas for tables) and should ship as an optional extra (`scat-kg[analysis]`) or a sibling package, so `scat check` stays light. The notebook ships as a template beside that package, with a path variable and the case study copied in so it runs offline. A later package should first make the loader public, then move the `scat_analysis` package over with its tests, and keep the "Reads as / Does not mean" blocks as part of the product, not as decoration.
