# Plan

The ordered work packages. Owned by the ACE, and revised at each package acceptance within the orderings that
`MISSION.md` (Governance, "The plan") sets. The chief engineer does not approve this file; changes are logged in
`decisions/log.md`. Words follow `GLOSSARY.md`.

Unscoped work surfaced by the chief engineer or by runs is kept in `candidates.md`; read it before scoping a package.

## Done

WP1 to WP11 built and accepted the first candidate (ontology research, toolchain, facilitation research, ontology and
page contracts, conformance tools, template and case study, docs and Pages, candidate and user acceptance, cleanup,
the stable machine interface). WP12 added the terms page (accepted, log D-077). The release PRs for that candidate
were closed unmerged (log D-074): the mission has since changed, and the next candidate replaces it.

## Next, in order (from `MISSION.md` as merged at 0e74f19)

1. **WP14 Prior-art readout.** The INCOSE paper's split between AI assistant and human operator; the AICC loops and
   model–view–control in `ant-rdf`; the knowledge-complex repositories; and the Obsidian-and-git vaults delivered to
   clients. Read as a way of thinking, not parts to carry over; private sources for principles only; the readout
   cites only published work. Produces: the prior-art part of D-5, and input to WP15.
2. **WP15 Architecture document and review** (G16, R-22). Model (the ontology plus a conformant vault), views (the
   Obsidian layout, the fingerprint view, the edge tables, the layered view, traces) and control plane (Obsidian, git
   and GitHub, the CLI and REPL, the MCP server, IDE agents): modules, interface contracts, responsibilities. Reviewed
   by architecture reviewers, one on Opus for the cross-cutting contracts and links and edges (G17). Produces: the
   architecture document (D-2). Gate: no further package starts detailed design before it is approved.
3. **RS3 Chat-path spike** (G14), side by side with WP15. Designs and tries the chat workflow with lab material: how
   the inference.coop chat reaches the tool (MCP), where that service runs, how a coder locks a version with no
   terminal, and what the views look like there. Live use waits for the chief engineer to sign in, and stays light.
   Produces: the chat-path readout (D-5) and the route to build.
4. **WP16 Ontology and layout** (G1, G15, G17, R-21, R-23), staged: spike, decide, build, quality control, integrate,
   cascade review. One page per narrative with status as its coding state; nodes and edges as base types; edges that
   name their narratives; fingerprints; relationship annotations replacing `conflicts`; mismatch detection with
   fixes; recording and removing an edge (G4); the Obsidian layout redesigned and checked in Obsidian. Absorbs WP13
   (the flow page and the data, rights and consent page) and rewrites the terms page against `GLOSSARY.md`, so the
   shared docs are edited once. Needs its impact map first (R-18).
5. **WP17 Views** (G12, R-17). One view generator in the tool, shared by the notebook and the MCP server; the public
   vault loader; the template notebook with the fingerprint view, edge tables, layered view and traces.
6. **WP18 Chat path** (G14, R-20). The MCP server with its tools, prompts and skills, on the route RS3 chose; views
   through the shared generator; the chat-path guide and the IDE note with its setup skill.
7. **WP19 Range vault** (R-20). The public KOI case in `mzargham/ant-rdf`, rebuilt as a SCAT model with groups, not
   named people; the lab and range runs.
8. **WP22 SCAT Chat as a small clear local app (D-124).** The launcher packaged and transparent; the walkthrough fixes
   from the leave-no-trace run. Before WP20's chat-path UA-A.
9. **WP23 Three disjoint attribution modes (D-127).** The mode in `scat.toml`, the `attributed_to` field, no bleeding
   into the knowledge graph; `scat:Attributes` renamed. Alongside WP22.
10. **WP24 Node-page help and merge (D-136).** The evidence view, the node-page norm, a drafted page; then review
    candidates and `merge`. After WP23.
11. **WP25 Docs: coding approaches and facilitating (D-137).** C14 and C15: the coding approaches drill-down with a
    screenshot walkthrough each; facilitating with narratives first; planning by event kind and field-note taking.
    After WP23 and WP24.
12. **WP26 Prompt-residue sweep and user-test loops (D-139).** Clean wording that echoes prompts; AI user-test
    rounds on both paths for clarity, concision and docs-code alignment, fixed between rounds. Before the chief
    engineer's walkthrough.
13. **WP20 Candidate and user acceptance.** The whole journey, J1 to J10, on both paths: UA-A rounds to the pass bar,
   the walkthrough scripts, the reviewer's guide, the candidate stage and new release PRs.

The order of WP17 and WP18 may change with the architecture document. Open play-test findings (F-1, F-3, F-5, F-7)
go into whichever package touches their files.
