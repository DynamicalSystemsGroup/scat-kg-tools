# Variant A: edges as pages

**Rule.** Every node, narrative, edge and relationship annotation is a page, in a folder named for its type. An edge page has `type` (holds, is-addressed-by, is-provided-by), `from`, `to`, `told_by` (its narratives), `status`, `notes`. Each type has an index (a Base) in `index/`, plus `edge.base`, an edge table with one view per edge type. Edge status is draft where a draft narrative names the edge. Needs Obsidian 1.9 or later.

**Recording an edge.** Create one edge page for the pair, or add the narrative to `told_by` on the existing page. The narrative and nodes are untouched.

**Reviewing.** Each narrative embeds `fingerprint.base`, listing the edge pages that link it. Its nodes are its outgoing links.

**Mismatches expected.**
- `night-main-break` (depth first): edge treatment-operators holds quick-leak-response names it, but it links no treatment-operators. The edge treatment-operators holds low-operating-cost names it, but it links neither end.
- `night-main-break` links both ends of two minimal-service-interruptions edges (to emergency-repair-roster and to leak-alert-notifications) without naming them.
- `dry-july-allocation-talk` (breadth first) links both ends of environmental-flow-protection to river-flow-display without naming it.
- `sensor-first-pitch`: none.

A mismatch shows only by comparing the embedded table with the outgoing links.
