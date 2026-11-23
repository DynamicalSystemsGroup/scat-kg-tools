# WP1 — Scope of work: Ontology research sprint

| | |
|---|---|
| **Status** | Approved by the ACE when the decision log records it. Runs inside `MISSION.md` (G10, deliverable D-5). |
| **Branch** | `wp1/ontology-research`, units off it, merged into `dev` |

## Purpose

Before the TBox is written, decide under "import, don't mint" what it adopts and what it authors. For each SCPT
element, either an existing ontology wins a trade study (and is adopted, thinned to what we use), or nothing beats
custom (and we author it). The result must be one coherent ontology, not a patchwork.

## Goals

- **WP1-G1.** Survey candidate ontologies and vocabularies for each **element**:
  - Stakeholder group, Concern, Property, Technology;
  - Heldby, Addresses, Attributes;
  - the scenario and architecture records;
  - page status and provenance.

  Starting points (not a closed list): ISO/IEC/IEEE 42010, the SEBoK/INCOSE canon and patterns in
  `/Users/z/Documents/GitHub/concept-definition-stage` (read only), SKOS, PROV-O, Dublin Core, SOSA/SSN, QUDT,
  iStar/KAOS goal models, OSLC RM, and SysML v2 (by reference, using the equivalence-axiom pattern of
  `concept-definition-stage`).
- **WP1-G2.** A trade study for each element: the best adopt option against authoring our own. Criteria:
  - fit to the element's intended meaning, as set out in `MISSION.md` (Purpose, Users, G1, G10) and
    `decisions/log.md` (D-003, D-010, D-013);
  - simplicity, measured as the terms we would carry;
  - recognisability to systems engineers;
  - maintenance;
  - cost to the software and the UX.
- **WP1-G3.** Assess easy-win axioms, starting with the conflict between concerns (anonymity vs attribution, which the
  chief engineer called a disjointness axiom): the form it would take, what it costs, and a recommendation.
- **WP1-G4.** A composition recommendation: per element, the adopted term (IRI and source) or "authored", with the
  reason, and how the pieces fit into one ontology.

## Non-goals

- Writing the TBox Turtle, fields or page contracts (WP3).
- Tool choices (WP2).
- Importing whole ontologies. We reference what we use.
- Inventing a term where an adopted one fits.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| WP1-D1 | `research/ontology/survey.md`: each candidate with source link, version and the elements it covers | WP1-G1 |
| WP1-D2 | `research/ontology/trade-study.md`: one table per element, plus an axioms section | WP1-G2, WP1-G3 |
| WP1-D3 | `research/ontology/readout.md`: the composition recommendation with a term-trace table | WP1-G4 |

Units write partial files under `research/ontology/parts/` and the synthesis unit assembles them, so units never
share a file.

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| WP1-R1 | Every claim about an external ontology carries a link to its primary source (spec, standard page or published IRI). Quoted definitions are verbatim, with a citation. | Reviewer fetches at least 10 links |
| WP1-R2 | Every element has a trade table with at least two options, one of which is "author our own". | Checklist of the elements against `trade-study.md` |
| WP1-R3 | Each element in the readout's term-trace table has an adopted IRI with its source, or "authored" with the reason. | Inspection |
| WP1-R4 | The recommendation adds no element beyond `MISSION.md` G1 except easy-win axioms, each with its cost stated. | Inspection against `MISSION.md` G1 and G10 |
| WP1-R5 | `trade-study.md` has an axioms section covering the concern conflict: its form, its cost and a recommendation. | Inspection |
| WP1-R6 | `survey.md` covers every starting-point source and every element, each source with a link and a version. | Checklist |
| WP1-R7 | `readout.md` is no longer than 1,000 words. | `wc -w` |

## Definition of good

A systems engineer recognises the vocabulary at once. The ontology carries only the terms we use, and nothing in it
feels bolted on.

## Definition of good enough

WP1-R1 to WP1-R7 met. Each element in the readout has a one-line recommendation, the runner-up option, and the
criterion that decided between them.

## Blast radius

`research/ontology/**` only. `work-packages/board.md` belongs to the PM.

## Agent's defaults

- Research units take one cluster each: stakeholders and concerns; properties and technologies; relations, records,
  status, provenance and axioms. A synthesis unit follows them.
- Web research uses primary sources.
