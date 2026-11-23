# WP1 — Scope of work: Ontology research sprint

| | |
|---|---|
| **Status** | Approved by the ACE when the decision log records it. Runs inside `MISSION.md`: G10, part of G1, and deliverable D-5. |
| **Branch** | Each unit works on `wp1/u<k>`, branched off `dev` and merged back into `dev` (ORG.md). |

## Purpose

Before the TBox is designed, find out under "import, don't mint" what it should adopt and what it should author. For
each SCAT element, either an existing ontology wins a trade study (and is adopted, thinned to what we use), or nothing
beats custom (and we author it). The aim is one coherent ontology, not a patchwork. WP1 recommends; the TBox design
(WP4) decides.

## Goals

- **WP1-G1.** Survey candidate ontologies and vocabularies for each **element**:
  - Stakeholder group, Concern, Affordance, Technology;
  - Heldby (stakeholder group × concern), Addresses (concern × affordance), Attributes (affordance × technology);
  - the scenario record, which is behavioural (events, outcomes, consequences, over time);
  - the architecture record, which is structural (parts, wholes, assemblages);
  - page status and provenance.

  Starting points, not a closed list:
  - ISO/IEC/IEEE 42010;
  - the SEBoK/INCOSE canon and patterns in `concept-definition-stage`
    (<https://github.com/Open-MBEE/concept-definition-stage>);
  - SKOS, PROV-O, Dublin Core, SOSA/SSN, QUDT;
  - iStar and KAOS goal models, OSLC RM;
  - SysML v2, by reference only;
  - affordance sources (Gibson's ecological concept, affordances in HCI and design, any published affordance
    ontology);
  - event and causal-chain vocabularies, for scenarios.
- **WP1-G2.** Run a trade study for each element: the best option to adopt, against authoring our own. The criteria:
  - fit to the element's intended meaning in `MISSION.md` (Purpose; Scenarios and architectures; Facilitation stance;
    G1; G10);
  - simplicity, counted as the terms we would carry;
  - recognisability to systems engineers;
  - maintenance;
  - cost to the software and the UX.
- **WP1-G3.** Assess the light options for holding disagreement and margins of potential conflict. This starts with a
  conflict between concerns (anonymity versus attribution), which the chief engineer called a disjointness axiom. For
  each option, give its form, its cost, and what it would let the graph show.
- **WP1-G4.** Recommend a composition: for each element, the adopted term (IRI and source) or "authored", with the
  reason, and how the pieces fit into one ontology.

## Non-goals

- Writing the TBox, fields or page contracts (WP4).
- Choosing tools (WP2).
- Facilitation practice (WP3).
- Importing whole ontologies.
- Inventing a term where an adopted one fits.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| WP1-D1 | `research/ontology/survey.md`: every candidate, with its source link, version and the elements it covers | WP1-G1 |
| WP1-D2 | `research/ontology/trade-study.md`: one table per element, plus a section on disagreement | WP1-G2, WP1-G3 |
| WP1-D3 | `research/ontology/readout.md`: the composition recommendation, with a term-trace table | WP1-G4 |

Units write partial files under `research/ontology/parts/`, and the synthesis unit assembles them.

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| WP1-R1 | Every claim about an external ontology carries a link to its primary source. Quoted definitions are verbatim, with a citation. Where a primary source can't be reached, the readout says so, along with what was used instead. | The reviewer fetches at least 10 links |
| WP1-R2 | Every element has a trade table with at least two options, one of which is "author our own". | A checklist of the elements |
| WP1-R3 | Every element in the readout's term-trace table has either an adopted IRI with its source, or "authored" with the reason. | Inspection |
| WP1-R4 | The recommendation adds no element beyond `MISSION.md` G1, except options for holding disagreement, each with its cost. | Inspection against G1 and G10 |
| WP1-R5 | `survey.md` covers every starting point and every element, with a link and a version for each source. | A checklist |
| WP1-R6 | `readout.md` is no longer than 1,000 words. | `wc -w` |
| WP1-R7 | Each disagreement option in `trade-study.md` states its form, its cost, and what it would let the graph show. | A checklist per option |
| WP1-R8 | Each element in the term-trace table has a one-line recommendation, the runner-up, and the criterion that decided between them. | A checklist over the table |

## Definition of good

A systems engineer recognises the vocabulary at once. The ontology carries only the terms we use, and nothing in it
feels bolted on.

## Definition of good enough

WP1-R1 to WP1-R8 are met.

## Blast radius

`research/ontology/**` only.

## Agent's defaults

- Units by cluster:
  - stakeholder groups and concerns;
  - affordances and technologies;
  - relations, records, status, provenance and disagreement;

  followed by a synthesis unit.
- Web research uses primary sources wherever they can be reached.
