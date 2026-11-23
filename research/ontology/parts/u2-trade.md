# WP1-U2 trade study: PROPERTY and TECHNOLOGY

Candidates and quotations: see `u2-survey.md` (S-numbers). Scores 1 (poor) to 5 (good). Criteria: **Fit** to intended meaning
(`MISSION.md` Purpose, G1, G10; D-003 "decompiling into those 4 concepts"); **Simple** (fewer terms carried scores higher);
**Recog** (recognisability to systems engineers); **Maint** (low upkeep scores higher); **Cost** (low software/UX cost scores higher).
Tie-breaker: D-013, "make the right way the easy way" (users) and "as simple as possible but no simpler" (builders).
Scores are this unit's judgement, not measurements.

## PROPERTY

Intended meaning: a named quality, usually qualitative ("anonymity", "auditability"), that a concern is about (Addresses) and that
technologies give or lack (Attributes). Not necessarily measured, not tied to software.

| Option | Fit | Simple | Recog | Maint | Cost | Notes |
|---|---|---|---|---|---|---|
| P1. Author `scpt:Property`, anchored by `skos:exactMatch` to SEBoK "System Property" (S1), `skos:closeMatch` to `ssn:Property` (S2) | 5 | 5 | 5 | 4 | 5 | One class carried. SEBoK definition ("Any named, measurable or observable attribute, quality or characteristic of a system or system element.") matches our meaning, including "named". Anchoring is the `concept-definition-stage` pattern. The SEBoK URL is an anchor, not an RDF class, so there is no class to inherit. |
| P2. Adopt `ssn:Property` directly (S2) | 4 | 4 | 3 | 5 | 4 | Stable W3C Recommendation IRI. "intrinsic to and cannot exist without the entity" is stricter than a desired quality a technology might lack. Reads as sensor vocabulary to a systems engineer. Brings `ssn:hasProperty`, whose domain is any entity, so it does not give us Attributes (property x technology) with our direction. |
| P3. `qudt:QuantityKind` (S3) | 2 | 3 | 3 | 4 | 3 | Numeric ("quantified numerically"). Fails for qualitative properties; would force a unit story we do not need in v0.1. Possible later extension for measured properties. |
| P4. SysML v2 attribute construct, by reference (S4) | 3 | 3 | 4 | 4 | 3 | Mapping unverified (spec body not read). Right level for a model-based design, but a Property in SCPT is a stakeholder-facing named quality, not a typed model feature. |
| P5. iStar/KAOS quality or softgoal (S7) | 3 | 3 | 3 | 2 | 2 | Close in spirit (non-functional quality). No verified IRI or maintained OWL; element definitions unread; pulls in goal-model semantics (contribution links) we do not use. |
| P6. Plain `skos:Concept` per property, with a ConceptScheme (S8) | 3 | 5 | 3 | 5 | 5 | Cheapest, but loses the class: a Property then cannot be told from a Concern in the graph without extra typing. |

**Recommendation: P1, author the one class and anchor it to SEBoK System Property (exact) and `ssn:Property` (close). Runner-up: P2 (adopt `ssn:Property` directly). Deciding criterion: fit, because SEBoK's definition is the only one that says "named" and does not require the quality to be intrinsic, and it is the canon `concept-definition-stage` already commits.**
The authored term is justified because no candidate offers a class IRI that is both stable and unconstrained in meaning; SEBoK has the right definition but no IRI, SSN has the IRI but a narrower definition. P3 and P4 remain optional anchors for measured or model-linked properties and cost nothing to add later.

## TECHNOLOGY

Intended meaning: a named thing pitched in an architecture (software, hardware, protocol, service, method) that has or lacks properties. No candidate defines "technology" as a class (survey, Gaps).

| Option | Fit | Simple | Recog | Maint | Cost | Notes |
|---|---|---|---|---|---|---|
| T1. Author `scpt:Technology`, anchored by `skos:closeMatch` or `skos:broadMatch` to ISO/IEC/IEEE 15288 system element (via S5) and, if verified, SysML v2 part definition (S4) | 5 | 5 | 4 | 4 | 5 | One class. 15288's element list ("hardware, software, data, humans, processes ... procedures ... facilities") is broad enough to cover non-software technologies. A technology is not identical to a system element (it excludes humans, materials), so the anchor must be broader/close, not exact. SysML anchor depends on reading the spec (unverified). |
| T2. `schema:SoftwareApplication` (S11) | 2 | 2 | 3 | 3 | 3 | "A software application." Excludes hardware, protocols, methods. Over 20 fields we would not use; dev-version page. |
| T3. `doap:Project` (S10) | 2 | 3 | 2 | 2 | 3 | "A project." Software-project vocabulary; no version statement found; human page failed on a certificate error. Recognised in the open-source world, not among systems engineers. |
| T4. Adopt SysML v2 `PartDefinition` as the class (S4) | 3 | 3 | 4 | 4 | 2 | Familiar to SysML users, but it implies a structural model element, and the facilitator-analyst would meet "part definition" in an architecture pitch about, say, a consent protocol. Mapping unverified. |
| T5. `skos:Concept` only (S8) | 3 | 5 | 3 | 5 | 5 | As P6: cheapest, no class distinction. |
| T6. `prov:Entity` (S9) | 2 | 4 | 2 | 5 | 3 | Too generic ("a physical, digital, conceptual, or other kind of thing"); would also type every page and record. |

**Recommendation: T1, author `scpt:Technology` with a broad/close match to the 15288 system element. Runner-up: T5 (plain `skos:Concept`). Deciding criterion: fit, since the software-specific candidates (T2, T3) mis-type non-software technologies and the generic ones (T5, T6) cannot tell a Technology from the other three classes.**
Honest note: this is "author", not "adopt". The research found no existing term that truly means technology, and the 15288 element is a parent notion, not a synonym.

## Flags for the readout unit
- SysML mappings (P4, T1, T4) need the spec body read before any equivalence axiom is written; use the closer-to-weaker `skos` match until then.
- SEBoK anchors are wiki URLs, which can change; `concept-definition-stage` accepts this. Version-pin as SEBoK v2.14.
