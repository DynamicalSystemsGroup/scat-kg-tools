# WP1-U2 survey: PROPERTY and TECHNOLOGY

Unit WP1-U2, branch `wp1/u2-properties-technologies`. Cluster: **Property** (concern x property via Addresses; property x
technology via Attributes) and **Technology**. Definitions are verbatim from the fetched page, with the fetch route
noted. "Fetched" means this unit retrieved the link on 2026-11-23 and the text matched. Anything not fetched is marked
**UNVERIFIED**.

Intended meaning (from `MISSION.md` Purpose and G1): a Property is a named quality a concern is about and a technology
can be said to have or lack (for example "auditability", "anonymity"); a Technology is a named thing that is pitched in an
architecture and that gives or lacks properties. Neither is presumed to be numeric, and neither is presumed to be software.

## Candidates

### S1. SEBoK glossary: System Property, Design Property, Emergent Property, Non-Functional Requirements
- Link: https://sebokwiki.org/wiki/System_Property_(glossary) ; https://sebokwiki.org/wiki/Design_Property_(glossary) ;
  https://sebokwiki.org/wiki/Emergent_Property_(glossary) ; https://sebokwiki.org/wiki/Non-Functional_Requirements_(glossary)
- Version: SEBoK v2.14, released 18 May 2026 (per https://sebokwiki.org/wiki/Stakeholder_Needs_and_Requirements). The
  Glossary category page does not itself state a version (revision oldid=77916).
- Covers: Property (strong). Technology: no glossary entry (the Glossary of Terms listing, https://sebokwiki.org/wiki/Glossary_of_Terms,
  has no "Technology", "Enabling technology" or "Quality attribute" title).
- System Property: "Any named, measurable or observable attribute, quality or characteristic of a system or system element."
  Cited there to Object Management Group 2003, "Property", SE Conceptual Model Semantic Dictionary (Draft 12_03-27-03).
- Design Property: "A characteristic obtained during design through allocation of requirements, or estimate, analysis, study, calculation, simulation, etc."
  Cited: "This definition was developed for the SEBoK."
- Emergent Property: "Property of a system that is meaningful only at higher levels of the organization of a system" (adapted from Checkland 1999, p. 78).
- Non-Functional Requirements: "Quality attributes or characteristics that are desired in a system, that define how a system is supposed to be."
  Cited: "This definition was developed for the SEBoK."
- Note: this is the canon `concept-definition-stage` commits; its pattern is `skos:exactMatch <sebokwiki glossary URL>`
  (`/Users/z/Documents/GitHub/concept-definition-stage/ontology/concept-definition.ttl`, term "Traceability"). The pages
  have no RDF IRI of their own; the wiki URL is the anchor.

### S2. SOSA/SSN (W3C)
- Link: https://www.w3.org/TR/vocab-ssn/
- Version: W3C Recommendation 19 October 2017 (link errors corrected 08 December 2017).
- Covers: Property (strong); Technology: only `ssn:System`, a sensing-oriented notion, not a fit.
- `ssn:Property` (http://www.w3.org/ns/ssn/Property): "A quality of an entity. An aspect of an entity that is intrinsic to and cannot exist without the entity."
- `sosa:ObservableProperty` (http://www.w3.org/ns/sosa/ObservableProperty): "An observable quality (property, characteristic) of a FeatureOfInterest."
- `ssn:hasProperty` (http://www.w3.org/ns/ssn/hasProperty): "Relation between an entity and a Property of that entity."
- `ssn:System` (http://www.w3.org/ns/ssn/System): "System is a unit of abstraction for pieces of infrastructure that implement Procedures."
- Note: `ssn:Property` is the generic class; `sosa:ObservableProperty` adds the observation (measurement) context we do not model.

### S3. QUDT
- Link: https://qudt.org/doc/DOC_SCHEMA-QUDT.html (class list) ; definitions from the schema Turtle at https://qudt.org/3.5.4/schema/qudt
- Version: QUDT Schema 3.5.4.
- Covers: Property only as a numeric quantity kind.
- `qudt:QuantityKind` (http://qudt.org/schema/qudt/QuantityKind), `dcterms:description`: "A Quantity Kind is any observable property that can be measured and quantified numerically."
- Note: our properties are mostly qualitative ("anonymity"). QUDT would apply only where a property is measured.

### S4. SysML v2 (by reference)
- Link: https://www.omg.org/spec/SysML/2.0/
- Version: 2.0, formal, September 2025 (per that page). Fetched page did not mention `AttributeUsage`/`AttributeDefinition`
  or `PartDefinition`; the spec body (PDF at https://github.com/Systems-Modeling/SysML-v2-Release/tree/master/doc) was **not read**, so any
  mapping of Property to an attribute construct and of Technology to `PartDefinition` is **UNVERIFIED** here.
- Covers: Technology only indirectly (a part definition is a structural element, not a technology). `concept-definition-stage`
  anchors with `owl:equivalentClass` between `https://www.omg.org/spec/SysML/20240801/SysML#PartDefinition` and
  `https://www.omg.org/spec/SysML/2.0/PartDefinition` (same file as S1 note). That date-versioned IRI is the repo's choice; this unit did not verify it resolves.

### S5. ISO/IEC/IEEE 15288 (system element) via SEBoK
- Link: https://sebokwiki.org/wiki/System_Element_(glossary) (ISO/IEC/IEEE 15288:2015 as cited there)
- Version: 15288:2015 as quoted by SEBoK; the ISO page itself was not fetchable (403) and is paywalled.
- Covers: Technology (loosely).
- "A system element is a discrete part of a system that can be implemented to fulfill specified requirements." and "A system element can be hardware, software, data, humans, processes (e.g., processes for providing service to users), procedures (e.g., operator instructions), facilities, materials, and naturally occurring entities (e.g., water, organisms, minerals), or any combination."
- Note: broader than technology (it includes humans and materials); useful as the parent notion, not as a synonym.

### S6. ISO/IEC 25010 (product quality) and ISO/IEC/IEEE 24765
- Link: https://iso25000.com/index.php/en/iso-25000-standards/iso-25010 (secondary site; ISO's own page returned 403). 24765 is cited for "Quality" at https://sebokwiki.org/wiki/Quality_(glossary).
- Version: edition not stated on the secondary page (it lists nine characteristics, including "Interaction Capability", which matches the 2023 edition; that match is this unit's inference).
- Covers: Property (a taxonomy of software quality characteristics, as a candidate controlled list, not a class).
- Quoted: "The quality of a system is the degree to which the system satisfies the stated and implied needs." (iso25000.com, as paraphrase of the standard, secondary). SEBoK Quality: "Ability of a product, service, system, component, or process to meet customer or user needs, expectations, or requirements." (cited ISO/IEC/IEEE 24765:2010).
- Note: a vocabulary of values, software-centric; no stable IRIs found.

### S7. i* / iStar and KAOS (goal models)
- Link: https://www.cs.toronto.edu/km/istar/ ; iStar 2.0 Language Guide https://arxiv.org/abs/1605.07767 (v3, 16 June 2016, Dalpiaz, Franch, Horkoff).
- Version: iStar 2.0 (2016). KAOS: not fetched, **UNVERIFIED**; no link cited.
- Covers: Property as "quality" / softgoal. The Toronto page says only: "the softgoal concept in i* draws on techniques for dealing with non-functional requirements in software engineering". The arXiv abstract page did not expose the element definitions (full text not read). Quality-element definition is therefore **UNVERIFIED** here.
- Note: no published OWL/IRI namespace found by this unit. Concern-side, not needed for the cluster.

### S8. SKOS
- Link: https://www.w3.org/TR/skos-reference/
- Version: W3C Recommendation 18 August 2009.
- Covers: either element as a labelled concept in a scheme (generic, not specific).
- `skos:Concept`: "The class skos:Concept is the class of SKOS concepts." `skos:ConceptScheme`: "A SKOS concept scheme can be viewed as an aggregation of one or more SKOS concepts." `skos:related`: "The property skos:related is used to assert an associative link between two SKOS concepts."
- Note: `concept-definition-stage` models every term as a SKOS concept. SKOS mapping properties (`skos:exactMatch`, `closeMatch`) are the lightweight anchor mechanism.

### S9. PROV-O and Dublin Core Terms
- Link: https://www.w3.org/TR/prov-o/ (Recommendation 30 April 2013) ; https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ (issued 2020-01-20).
- Covers: neither element directly. `prov:Entity`: "An entity is a physical, digital, conceptual, or other kind of thing with some fixed aspects". `dcterms:subject`: "A topic of the resource." `dcterms:requires`: "A related resource that is required by the described resource to support its function, delivery, or coherence."
- Verdict: provenance and metadata; relevant to the records unit, not to Property or Technology. Listed for completeness (R6).

### S10. DOAP
- Link: http://usefulinc.com/ns/doap# (human fetch failed on a certificate error; schema read from https://raw.githubusercontent.com/ewilderj/doap/master/schema/doap.rdf)
- Version: no version statement found in the schema file; repo https://github.com/ewilderj/doap.
- Covers: Technology only for software projects. `doap:Project`: comment "A project." (subclass of `foaf:Project`). Properties such as `doap:programming-language` exist.
- Note: describes a software project, not a technology that may be hardware, protocol or method.

### S11. schema.org SoftwareApplication
- Link: https://schema.org/SoftwareApplication
- Version: page showed "V30.1 | 2026-09-16" and marks itself the development version; no stable release label read.
- Covers: Technology only for software. Description: "A software application." Hierarchy Thing > CreativeWork > SoftwareApplication. Carries `applicationCategory`, `featureList`, `softwareVersion`, `operatingSystem`, and 20 more fields we would not use.

### S12. Technology readiness level (NASA)
- Link: https://www.nasa.gov/directorates/somd/space-communications-navigation-program/technology-readiness-levels/ (published 2023-09-27, updated 2026-06-25)
- Covers: Technology (usage only). "Technology Readiness Levels (TRL) are a type of measurement system used to assess the maturity level of a particular technology." The page never defines "technology"; it does not offer a class.

### S13. concept-definition-stage (local, read-only)
- Path: `/Users/z/Documents/GitHub/concept-definition-stage`, `ontology/cds-core.ttl` (`owl:versionInfo "0.1.0"`), last commit 4d1e52e, 2026-06-28.
- Covers: neither Property nor Technology as a class. Its README says the solution is "never presumed to be a technology". The relevant patterns: SEBoK terms as `skos:Concept` with `skos:exactMatch` to the glossary URL; SysML anchoring by `owl:equivalentClass`. `cds:addresses` (domain and range `cds:Term`, comment "A concept addresses the problem / threat / opportunity it is defined for (GtWR).") exists but is typed over cds terms, so not reusable for Concern x Property (belongs to the relations unit).

## Gaps
- 42010 text (paywalled; ISO and iso-architecture.org fetches failed) not read; it is the Concern unit's source, and does not define "property".
- SysML v2 spec body, KAOS, iStar 2.0 element definitions, ISO 25010 primary text: not read (above).
- No source found that defines "technology" as a class. SEBoK has no entry; NASA uses the word without defining it.
