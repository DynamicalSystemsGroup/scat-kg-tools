# WP1-U2 trade study: AFFORDANCE and TECHNOLOGY

Candidates and quotations: see `u2-survey.md` (A-numbers, T-S-numbers). Scores 1 (poor) to 5 (good). Criteria: **Fit** to intended
meaning; **Simple** (fewer terms carried scores higher); **Recog** (recognisability to systems engineers); **Maint** (low upkeep
scores higher); **Cost** (low software/UX cost scores higher). Tie-breaker: D-013, "make the right way the easy way" (users) and
"as simple as possible but no simpler" (builders). Scores are this unit's judgement, not measurements.

## AFFORDANCE

Fit now means: an affordance of a technology or tool, read as a perceived-possible action by a human user (Norman, A2), named by a
note-taker, not computed or measured. Addresses links a concern to it; Attributes links it to a technology. The ontology is
"just enough structure ... mostly a formal structure for arranging obsidian notes": one class, a definition, a few anchors.

| Option | Fit | Simple | Recog | Maint | Cost | Notes |
|---|---|---|---|---|---|---|
| F1. Author `scpt:Affordance` (one class, plain-language definition built on Gibson/Norman), anchored by `skos:closeMatch` to `td:InteractionAffordance` (A5) and `skos:relatedMatch` to `ease:Affordance` (A4) | 5 | 5 | 4 | 4 | 5 | One term carried. Definition can state both halves (what the technology offers; perceived by a human user). The anchors say who else uses the word; neither is imported. No IRI exists for Gibson or Norman, so the definition text cites them. |
| F2. Adopt `td:InteractionAffordance` (A5) | 3 | 4 | 2 | 4 | 3 | Right shape (Thing offers affordance), stable W3C. Defined for machine Consumers and protocol interactions; drags in Property/Action/Event subtypes and a Thing/Forms metadata model. A systems engineer meeting "PropertyAffordance" will misread it. |
| F3. Adopt `ease:Affordance` (A4) | 2 | 1 | 2 | 2 | 1 | The only formal OWL affordance class with a quoted definition, but DOLCE-based (Relation, Disposition, Role, Task); robot agent and physics validation. A franken-ontology risk (G10). |
| F4. Keep a quality class: `ssn:Property` or SEBoK System Property (A7) | 2 | 4 | 5 | 5 | 4 | Familiar and stable, but names what a system is like, not what a user can do. Wrong direction for the new framing, retained only to show why it lost. |
| F5. schema.org `potentialAction` (A6) | 2 | 3 | 2 | 3 | 2 | A property linking a thing to an Action instance; no class for the named possibility, and Action's description was unread. |
| F6. Plain `skos:Concept` per affordance (A8) | 3 | 5 | 3 | 5 | 5 | Cheapest; cannot be told apart from the other three classes without extra typing. |

**Recommendation: F1, author `scpt:Affordance` with close/related anchors to WoT `td:InteractionAffordance` and EASE `Affordance`. Runner-up: F2 (adopt `td:InteractionAffordance`). Deciding criterion: fit, because only an authored definition can say "perceived-possible action by a human user" for a note-taker, while the nearest published class is defined for machines.**
This is authoring, not adopting; the justification is that no existing class both has a stable IRI and means a human-perceived action possibility. If the chief engineer later wants machine-consumable technologies, F2 becomes cheap to add as a subclass link.

## TECHNOLOGY

Intended meaning: a named thing pitched in an architecture (software, hardware, protocol, service, method) that offers affordances. Arrangements of technologies into tools are expressed through notes and links, not a new class (G1 has four classes). No candidate defines "technology" as a class (survey Gaps).

| Option | Fit | Simple | Recog | Maint | Cost | Notes |
|---|---|---|---|---|---|---|
| T1. Author `scpt:Technology`, anchored by `skos:closeMatch`/`skos:broadMatch` to the 15288 system element (T-S1) and, once verified, SysML v2 PartDefinition (T-S5) | 5 | 5 | 4 | 4 | 5 | One class. 15288's element list covers hardware, software, procedures, so non-software technologies fit. Not an exact match (excludes humans, materials), so the anchor is broad/close. |
| T2. `schema:SoftwareApplication` (T-S3) | 2 | 2 | 3 | 3 | 3 | "A software application." Excludes hardware, protocols, methods; 20+ unused fields; development-version page. |
| T3. `doap:Project` (T-S4) | 2 | 3 | 2 | 2 | 3 | "A project." Software-project vocabulary; no version found. |
| T4. SysML v2 `PartDefinition` as the class (T-S5) | 3 | 3 | 4 | 4 | 2 | Familiar to SysML users but implies a structural model element; mapping unverified. |
| T5. `skos:Concept` only (A8) | 3 | 5 | 3 | 5 | 5 | Cheapest; no class distinction. |
| T6. `td:Thing` (WoT; A5) | 2 | 3 | 2 | 3 | 3 | Pairs naturally with F2 (Thing offers InteractionAffordance), but is defined for networked devices; **UNVERIFIED** definition text (not quoted in the survey). Listed only to show the coupling. |
| T7. `prov:Entity` (T-S6) | 2 | 4 | 2 | 5 | 3 | "a physical, digital, conceptual, or other kind of thing"; too generic, would also type every page and record. |

**Recommendation: T1, author `scpt:Technology` with a broad/close match to the 15288 system element. Runner-up: T5 (plain `skos:Concept`). Deciding criterion: fit, since the software-specific candidates (T2, T3) mis-type non-software technologies and the generic ones (T5, T7) cannot tell a Technology from the other three classes.**
Honest note: authoring, not adopting; the 15288 element is a parent notion, not a synonym.

## Flags for the readout unit
- SysML mappings (T1, T4) need the spec body read before any equivalence axiom is written; use `skos` matches until then.
- SEBoK anchors are wiki URLs, which can change; concept-definition-stage accepts this. Pin SEBoK v2.14.
- Gibson/Norman/Turvey/Stoffregen/Chemero were not read in full (survey Gaps); the definition text for `scpt:Affordance` should cite only what is quoted in A1, A2 and A4.
