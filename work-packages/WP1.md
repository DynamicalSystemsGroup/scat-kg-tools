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

- G1. Survey candidate ontologies and vocabularies for each element:
  - Stakeholder group, Concern, Property, Technology;
  - Heldby, Addresses, Attributes;
  - the scenario and architecture records;
  - page status and provenance.

  Starting points (not a closed list): ISO/IEC/IEEE 42010, the SEBoK/INCOSE canon and patterns in
  `/Users/z/Documents/GitHub/concept-definition-stage`, SKOS, PROV-O, Dublin Core, SOSA/SSN, QUDT, iStar/KAOS goal
  models, OSLC RM, SysML v2 (by reference, using the equivalence-axiom pattern of `concept-definition-stage`).
- G2. A trade study for each element: the best adopt option against authoring our own. Criteria:
  - fit to the meaning the chief engineer gave the element;
  - simplicity, measured as the terms we would carry;
  - recognisability to systems engineers;
  - maintenance;
  - cost to the software and the UX.
- G3. Assess easy-win axioms, starting with the conflict between concerns (anonymity vs attribution, which the chief
  engineer called a disjointness axiom): the form it would take, what it costs, and a recommendation.
- G4. A composition recommendation: per element, the adopted term (IRI and source) or "authored", with the reason, and
  how the pieces fit into one ontology.

## Non-goals

- Writing the TBox Turtle, fields or page contracts (WP3).
- Tool choices (WP2).
- Importing whole ontologies. We reference what we use.
- Inventing a term where an adopted one fits.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| WP1-D1 | `research/ontology/survey.md`: each candidate with source link, version and what it covers | G1 |
| WP1-D2 | `research/ontology/trade-study.md`: one table per element | G2, G3 |
| WP1-D3 | `research/ontology/readout.md`: the composition recommendation (at most two pages) with a term-trace table | G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R1 | Every claim about an external ontology carries a link to its primary source (spec, standard page or published IRI), and quoted definitions are verbatim with a citation. | Reviewer spot-checks at least 10 links by fetching them |
| R2 | Every element has at least two options in its trade table, one of which is "author our own". | Inspection of `trade-study.md` |
| R3 | Every element in the readout's term-trace table has either an adopted IRI with its source, or "authored" with the reason. | Inspection |
| R4 | The recommendation adds no element outside G1's list except easy-win axioms, each with its cost stated. | Inspection against `MISSION.md` G1 and G10 |

## Definition of good

A systems engineer recognises the vocabulary at once. The ontology carries only the terms we use, and nothing in it
feels bolted on.

## Definition of good enough

R1 to R4 met, and the readout is clear enough for the ACE to rule on each element.

## Blast radius

`research/ontology/**` and this file's board rows. Nothing else.

## Agent's defaults

- Research workers each take a cluster of elements (stakeholders and concerns; properties and technologies;
  relations, records, status and provenance), plus one synthesis unit.
- Web research uses primary sources.
