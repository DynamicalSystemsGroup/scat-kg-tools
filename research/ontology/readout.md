# WP1 readout: composition recommendation

WP1 recommends; WP4 decides. Evidence: `survey.md`, `trade-study.md`.

## One ontology

One SKOS spine, in the pattern `concept-definition-stage` uses. Every class gets one authored IRI in one SCAT namespace. Its `skos:definition` is the cited authority's wording, and `skos:closeMatch` anchors it to the source (`exactMatch` only where the source defines the identical term). Nothing is imported whole. Concern, Stakeholder group, Affordance and Technology are the four classes. Heldby, Addresses and Attributes are three authored properties between them. Scenario and architecture records are two authored classes that link only through those properties. A coded record points to its raw record with `prov:wasDerivedFrom`. Status is one adopted property with authored values. No source publishes a usable IRI for any of the four classes, so the classes are authored IRIs with adopted definitions. Adopted IRIs appear only where a source serves one.

## Term-trace

| Element | Term (IRI, or authored) | Source, or reason | Recommendation | Runner-up | Deciding criterion |
|---|---|---|---|---|---|
| Stakeholder group | Authored IRI; `skos:closeMatch` to SEBoK Stakeholder (15288 says "individual or organization"; "group" is our usage) | ISO/IEC/IEEE 15288:2015 text via SEBoK; "group" is our usage | Adopt the definition, one class | Authored `StakeholderGroup` | Recognisability |
| Concern | Authored IRI, subclass of `skos:Concept` (`http://www.w3.org/2004/02/skos/core#Concept`) | 42010 wording, "any interest in the system", from the community site only | Adopt the definition | Authored wording | Recognisability |
| Affordance | Authored | No standard fits: WoT `td:InteractionAffordance` describes a Thing for machines, and SEBoK Capability is outcome-centred. Gibson's definition, cited via Toyoshima; `skos:closeMatch` to SEBoK Capability; WoT only as `rdfs:seeAlso` | Author the class, quote Gibson | SEBoK Capability | Fit |
| Technology | Authored IRI; `skos:closeMatch` to SEBoK System Element | ISO/IEC/IEEE 15288:2015 via SEBoK; SEBoK has no Technology entry, so the label is ours | Adopt the definition | SysML v2 PartDefinition | Maintenance (no OWL from OMG), then fit |
| Heldby | Authored property | 42010 gives the sentence, not an IRI. `prov:wasAttributedTo` means authorship, not holding | Author; stakeholder group to concern | `prov:wasAttributedTo` | Fit |
| Addresses | Authored property | `cds:addresses` is bound to `cds:Term` and is in one repository only | Author; concern to affordance | `cds:addresses` | Simplicity, independence |
| Attributes | Authored property | Nothing found for affordance to technology | Author; affordance to technology | RO `has disposition`, live only if Affordance is defined as a disposition, which we do not recommend | Simplicity |
| Scenario record | Authored class | Events stay in the page body; an event node would be a new element beyond G1 | Author | SEM `sem:Event` | Simplicity under R4 |
| Architecture record | Authored class, worded after 42010 Architecture Description; optionally `dcterms:hasPart` (`http://purl.org/dc/terms/hasPart`) | 42010 has no IRI; DCMI Recommendation term for parts and wholes | Author the class; `hasPart` only if WP4 wants a part-whole link | `ssn:hasSubSystem` | Simplicity, recognisability |
| Page status | Adopted `https://schema.org/creativeWorkStatus`; three authored values `stub`, `draft`, `done` | schema.org v30.1; typed for CreativeWork; in schema.org's pending area, so it may change | Adopt | Authored `status` | Adopt over mint at equal term count |
| Provenance | Adopted `http://www.w3.org/ns/prov#wasDerivedFrom` | PROV-O Recommendation; coded page to raw page; git holds authorship and time | Adopt | `dcterms:source` | Recognisability, fit |

## Disagreement options

Each costs terms; none ranks views.

| Option | Cost | Shows |
|---|---|---|
| D0, many-to-many Heldby (already G1) | none | the same concern held by several groups |
| D1, authored symmetric `conflictsWith` between concerns | 1 property | which concerns oppose; with D0, groups that share a concern while their other concerns oppose |
| D3, D1 plus a warning-severity shape | 1 shape; a SPARQL-based constraint costs WP2 engine support | a record that touches both ends of a conflict, flagged and never an error |
| D4, a named tension page | 1 class, 2 to 3 properties, 1 page type | n-ary, described tension |
| D6, signed Addresses | 1 property or value | an affordance that serves one concern and harms another |

Recommended: D0, D1 and D3. Deferred: D4, D6 and per-source named graphs. OWL `DisjointClasses` is rejected, because it turns a tension into an inconsistency. The disjointness idea is kept as the warning in D3.

## Not verified

- 42010:2022 text was unreachable (ISO returned HTTP 403). Concern and Stakeholder wording comes from the community site's conceptual-model page, which still carries first-edition phrasing. WP4 or the ACE must check the standard before copying a definition. If it differs, authored wording replaces it.
- Gibson's book is an image-only scan, so the quotation is read via Toyoshima 2017. Toyoshima 2022 and Maier and Fadel were not read.
- CDS IRIs under `w3id.org` were not dereferenced.
- Event Ontology, LODE, CIDOC CRM, AIF and ArchiMate were unreachable and are not assessed.
- Ratings are judgment, not measurement.
