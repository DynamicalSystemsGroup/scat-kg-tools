# Variant B: edges as fields on node pages

**Rule.** Nodes and narratives are pages; edges and the relationship annotation are fields. Each edge is stored once: `held_by` and `addressed_by` on the concern, `provided_by` on the affordance. A list item reads the other end, `told by`, the narratives, `note:`. An annotation is a `pulls_against` item on one of its two entries. Index pages are generated tables in `index/`. An edge has no status of its own.

**Recording an edge.** Add a list item on the concern (or affordance), naming the narratives; if the pair is there, add the narrative to its item. The narrative is not edited.

**Reviewing.** Each narrative embeds a core Search query showing the lines that name it. Its nodes are its outgoing links.

**Mismatches expected.**
- `night-main-break` (depth first): the item for treatment-operators on quick-leak-response names it, but it links no treatment-operators. The item on low-operating-cost names it, but it links neither end.
- `night-main-break` links both ends of two minimal-service-interruptions edges without naming them.
- `dry-july-allocation-talk` (breadth first) links both ends of environmental-flow-protection to river-flow-display without naming it.
- `sensor-first-pitch`: none.

They show by comparing the query result with outgoing links.
