# U1 trade study: Stakeholder group and Concern

Unit WP1-U1. Candidate entries and links are in `u1-survey.md` (section numbers A1-A10, B1-B8 refer to it).
Criteria, from `WP1.md` WP1-G2: **Fit** to intended meaning, **Simple** (terms we would carry), **Recog** (recognisable to systems engineers),
**Maint** (maintenance), **Cost** (to software and UX). Scores 1 (poor) to 5 (good). Scores are my judgement, not measurements.
Heuristics applied: "make the right way the easy way" (users), "as simple as possible but no simpler" (builders).

Adoption pattern assumed throughout (from `concept-definition-stage`): we author a local class and anchor it to external terms with
`skos:exactMatch` / `skos:closeMatch` plus `cds:definitionSource`-style citation. No whole-ontology import.
"Adopt" below therefore means "use the external IRI as the class itself", the stronger commitment.

Caveat: ISO/IEC/IEEE 42010 text could not be fetched (paywalled; see survey, "Access limits"). Scores that lean on 42010 rest on the
verbatim 26702/1471 stakeholder wording (A1, A3) and on unverified summaries for Concern (B1).

## 1. Stakeholder group

Intended meaning: a class of people sharing a stake, never an individual (Chatham House, `MISSION.md` Users; G6; D-010).

| Option | Fit | Simple | Recog | Maint | Cost | Notes |
|---|---|---|---|---|---|---|
| **S1. Author own class "Stakeholder group"**, anchored with `skos:closeMatch` to SEBoK Stakeholder (A1) and the 26702 wording quoted as source | 5 | 4 | 5 | 4 | 4 | Name matches what facilitators and SEs say. Definition can say "group, never an individual" in one sentence. One term carried; anchors add no classes. Nothing to track upstream except SEBoK page URLs, which `concept-definition-stage` already tracks. |
| S2. Adopt `dcterms:AgentClass` (A6) as the class | 3 | 5 | 2 | 5 | 3 | Definition "A group of agents." is literally right on grouping and the IRI is stable (DCMI Recommendation 2020-01-20). But it says nothing about stake or interest, and "AgentClass" is unfamiliar to SEs and to the facilitator-analyst; the UI would have to relabel it, so we carry a label mapping. |
| S3. Adopt SEBoK/15288 "Stakeholder" as the class, group-ness by convention (cap field, naming rule) | 3 | 5 | 5 | 4 | 3 | Recognised instantly. But 15288 wording is "Individual or organization" (A1); the individual-never rule then lives only in a checker and docs, not in the class meaning, which weakens the Chatham House guarantee. 26702 admits "classes thereof", so the fit is arguable, not clean. |
| S4. `prov:Agent`/`prov:Organization` (A4) or `org:Organization` (A5) | 2 | 3 | 2 | 5 | 2 | `prov:Person` is individuals and `prov:Organization` is an institution; a stakeholder group is neither. ORG brings membership and posts, which invite identifying people. Wrong direction for G10 and Chatham House. |
| S5. iStar Role / Agent (A8) | 2 | 3 | 2 | 3 | 2 | Role is an abstract kind of actor, close in spirit, but pulls in the actor/intentional-element model and is unfamiliar outside requirements-modelling circles. |

**Recommendation:** S1, author own class "Stakeholder group", anchored to SEBoK Stakeholder by `skos:closeMatch` (not `exactMatch`, because ours is narrower: groups only). Runner-up: S2, adopting `dcterms:AgentClass` (we could additionally declare `rdfs:subClassOf dcterms:AgentClass` at no UX cost if WP3 wants a stable upper anchor; I do not recommend it by default). Deciding criterion: fit plus recognisability, since no published term says "a group of people sharing a stake" and the only adoptable group term (AgentClass) is unrecognisable to SEs.

Plain statement: nothing existing truly fits "stakeholder group". Pieces exist (stakeholder in SEBoK; group in DCMI), so the authored class is a one-term composition of them, not an invention.

## 2. Concern

Intended meaning: something a stakeholder group cares about, which properties address; concerns may conflict (anonymity vs attribution, D-010).

| Option | Fit | Simple | Recog | Maint | Cost | Notes |
|---|---|---|---|---|---|---|
| **C1. Author own class "Concern"**, definition adapted from 42010 and cited, optional `skos:closeMatch` to SysML v2 `ConcernDefinition` (B3) | 5 | 5 | 5 | 4 | 5 | The word and the meaning come from 42010 (B1), which SEs know. No published IRI exists for the 42010 concern, so there is nothing to import. One term carried. Definition wording must be checked against the paid standard before it is quoted (not verified here). |
| C2. Adopt SysML v2 `ConcernDefinition` (B3) as the class | 3 | 2 | 4 | 3 | 2 | Published (OSLC SysML 2.0 vocabulary, Draft 01, 25 April 2024) and SE-recognisable. But it is a `RequirementDefinition` subtype: a concern would become a kind of requirement, and the stakeholders come as owned parameters, duplicating our Heldby relation. Tracks a draft vocabulary of a large language. |
| C3. `skos:Concept` in a concern scheme (B4) | 2 | 5 | 3 | 5 | 4 | Cheapest, and matches the `concept-definition-stage` spine. But a concern is then only a named idea; classes and constraints on "something a group holds" are lost, and conflict axioms would have to be stated on concepts. Fine as the *anchor* for definitions, not as the class. |
| C4. iStar Goal / Quality or KAOS goal (B6, B7) | 1 | 3 | 2 | 3 | 2 | Goals have achievement criteria; concerns do not. Quality is nearer our Property. Mismatch of meaning. |
| C5. SEBoK "concern" as used in Problem (B2) | 1 | n/a | 3 | n/a | n/a | Risk-management sense (probability, consequence). Conflicts with our meaning. Recorded to avoid accidental reuse. |

**Recommendation:** C1, author own class "Concern", definition adapted from 42010 with citation, with `skos:closeMatch` to SysML v2 ConcernDefinition as an optional anchor. Runner-up: C2, adopting SysML `ConcernDefinition`. Deciding criterion: fit and simplicity, because the only published concern term is a requirement subtype that imports machinery we do not use and duplicates Heldby.

Plain statement: for Concern, nothing published beats authoring; the adopted element is the 42010 *word and definition*, not an IRI.

## Cross-cutting notes for the synthesis unit

- Both recommendations are "author, anchored", consistent with the `concept-definition-stage` equivalence-axiom pattern (A2, Section C of the survey); that is what makes them one coherent ontology rather than a patchwork.
- If the synthesis unit adopts the match-strength convention, record S1 as `closeMatch` and C1's SysML anchor as `closeMatch` (both narrower or differently scoped).
- Open item for the supervisor, not decided here: confirm the 42010 definition text from the standard before it is quoted in the TBox (the standard is paywalled; I could not).
- Conflict between concerns (axiom form) is outside this unit; see the relations/axioms unit.
