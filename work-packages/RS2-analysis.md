# RS2 — Research spike: graph analysis for the "big picture"

| | |
|---|---|
| **Status** | Approved by the ACE (log D-052). **Outside v0.1.** It is exploration the chief engineer directed, and it lifts the "analysis tooling" non-goal for research only. |
| **Branch** | `spike/analysis` off `dev`, never merged into `dev` before the v0.1 release. Pushed for review. |
| **Directory** | `research/analysis/` |

## Purpose

Explore what a data or network scientist can learn from a conformant, signed-off SCAT graph, working in a Jupyter
notebook:
- where tensions are sharpest;
- where groups match or differ;
- where there are gaps (concerns no affordance addresses, affordances no technology attributes, groups whose
  concerns go unaddressed).

The spike recommends the analyses and the shape of an analysis module. A later package delivers.

## Questions

1. **The graph model.** How should a SCAT vault be represented for analysis? For example, a typed multilayer or
   4-partite graph (stakeholder group, concern, affordance, technology), plus `conflicts` edges among concerns, plus
   the scenario and architecture records as provenance.
2. **Which analyses are meaningful, and how are they read?** Candidates include:
   - traceability chains, stakeholder group → concern → affordance → technology, borrowing from requirements
     traceability, with coverage and gaps;
   - bipartite projections, such as groups linked by shared concerns, and concerns linked by shared affordances;
   - tension analysis: conflicting concerns, and the groups that hold both sides or opposite sides;
   - centrality and brokerage: which affordances or technologies carry the most concerns;
   - community structure.

   Each comes with what it means, and what it must not be taken to mean (no adjudication: the analysis describes, it
   doesn't rank stories or architectures).
3. **What it needs from the tools.** For example, an API that returns the ABox as a graph, and stable identifiers.
4. **Libraries.** networkx versus alternatives, kept light.

## Deliverables

- `research/analysis/readout.md`: answers, a recommended set of analyses, and a sketch of a module and delivery
  package. At most 1,500 words.
- `research/analysis/notebook/`: a runnable Jupyter notebook in its own uv project. It loads a vault through
  `scat_kg`, builds the graph, and demonstrates each recommended analysis with plots and an interpretation, on:
  - (a) the template's case study;
  - (b) a richer synthetic vault the spike generates, with multiple groups, conflicts and gaps, so that patterns are
    visible.

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| RS2-R1 | The notebook runs top to bottom headless (`jupyter nbconvert --execute`), with output saved. | Pasted output |
| RS2-R2 | Every analysis has a plain interpretation, and a "does not mean" line. | Inspection |
| RS2-R3 | Analyses only describe the graph: no scoring that ranks stories, groups or architectures as better or worse. | The reviewer's inspection |
| RS2-R4 | It reads the vault through `scat_kg`, without a parallel parser. | Inspection |
| RS2-R5 | The synthetic vault passes `scat check` with 0 errors. | Pasted output |

## Constraints

- Dependencies (networkx, pandas, matplotlib, jupyter or nbconvert) come from PyPI, in the spike's own project, never
  in the package.
- No private material.
