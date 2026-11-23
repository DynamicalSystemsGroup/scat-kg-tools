# Plan

The ordered work packages. Owned by the ACE, and revised at each package acceptance within the orderings that
`MISSION.md` (Governance, "The plan") sets. The chief engineer does not approve this file; changes are logged in
`decisions/log.md`.

1. **WP1 Ontology research sprint.** Survey existing ontologies for each SCAT class and relation, including the
   patterns in `concept-definition-stage`. Run the trade study (adopt and thin, or author), and assess easy-win axioms
   and options for holding disagreement. Produces: the ontology part of D-5.
2. **WP2 Toolchain spike.** In parallel with WP1. Try OKF, oxigraph, pydantic and the rule-language options on a
   throwaway mini-vault, and measure them. Produces: the toolchain decision, and the toolchain part of D-5.
3. **WP3 Facilitation research spike.** In parallel with WP1. Work through the sources `MISSION.md` G11 names.
   Produces: the facilitation strategy, input to WP4 on holding disagreement, and the facilitation part of D-5.
4. **WP4 Ontology and page contracts.** From WP1 to WP3: the TBox in Turtle, the fields, page types, linking rules,
   status rules, how disagreement is held, and the rule catalogue with ids, severities and message wording.
   Produces: D-1 and the vault conventions.
5. **WP5 Conformance tools.** Sets up the `scat-kg-tools` package and its CI. Builds the tools on WP2's toolchain and
   WP4's contracts. Produces: D-2.
6. **WP6 Template and case study.** Starts once WP4 is accepted, in parallel with WP5, and is accepted after WP5.
   Sets up `scat-kg-template` and its CI. Produces: D-3.
7. **WP7 Docs and Pages.** Written journey-first (J1–J7), with the facilitation guides built on WP3. Accepted after
   WP5 and WP6. Produces: D-4.
8. **WP8 Candidate and user acceptance.** Integration, the candidate stage, UA-A rounds to the pass bar, the
   reviewer's guide and the walkthrough script. Produces: D-6 and D-7.
