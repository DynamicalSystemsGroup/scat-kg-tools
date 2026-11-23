# WP1-U3 survey: relations, records, status, provenance, axioms

Unit WP1-U3, cluster 3. Covers Heldby, Addresses, Attributes; scenario and architecture records (raw and coded); page
status; provenance (raw record to coded pages); and the sources needed for the axioms section. Fetched 2026-11-23; revised same day for the Affordance rename and the behaviour/structure framing.

Conventions. **[F]** = I fetched the page this session and the quote is from that fetch. **[NF]** = not fetched or
paywalled; nothing is quoted from it, and any claim resting on it is flagged. Quotes are verbatim and short.
Definitions that were not retrievable are left out rather than recalled (the `concept-definition-stage` rule: no
fabricated canon).

Facts about our own project that shape the survey (from `MISSION.md` and `decisions/log.md`):
- Relations are pages. "Every SCPT and relation page comes from `scpt`" (MISSION R-11, wording before the rename to SCAT/Affordance), and G3 gives every instance page a
  status, so a Heldby, Addresses or Attributes link is a page with two ends, not only a bare property.
- Raw records link to or embed their coded pages; coded records link into the graph (MISSION G1; decision log line 111).
- No attribution to individuals; Chatham House rule (D-010). So agent-centred provenance terms are out of scope.

## 1. Candidate sources

### 1.1 SKOS
- Link: <https://www.w3.org/TR/skos-reference/> [F]. Version: W3C Recommendation, 18 August 2009.
- Covers: concept schemes and labels (status values as concepts), associative links. No status property.
- "The property `skos:related` is used to assert an associative link between two SKOS concepts." (s8.1)
- "A triple `<A> skos:broader <B>` asserts that `<B>`, the object of the triple, is a broader concept than `<A>`." (s8.1)
- "`skos:related` is disjoint with the property `skos:broaderTransitive`." (S27)
- "In the SKOS data model, `skos:Concept` and `skos:Collection` are disjoint classes." (s9.6.4)
- Status: I read the first ~100k of 145k characters and found no status or lifecycle property. The unread tail was not searched.
- Axiom precedent: SKOS itself ships disjointness axioms (above), both class-level and property-level.

### 1.2 PROV-O
- Link: <https://www.w3.org/TR/prov-o/> [F]. Version: W3C Recommendation, 30 April 2013.
- Covers: provenance, derivation of one record from another; the spine `concept-definition-stage` already uses.
- `prov:Entity` (starting point): "An entity is a physical, digital, conceptual, or other kind of thing with some fixed aspects"
- `prov:wasDerivedFrom` (starting point): "A derivation is a transformation of an entity into another, an update of an entity resulting in a new one"
- `prov:hadPrimarySource` (expanded, `http://www.w3.org/ns/prov#hadPrimarySource`): "A primary source for a topic refers to something produced by some agent with direct experience and knowledge about the topic"
- `prov:Activity` (starting point, `http://www.w3.org/ns/prov#Activity`): "An activity is something that occurs over a period of time and acts upon or with entities"
- `prov:wasInformedBy` (starting point): "An activity a2 is dependent on or informed by another activity a1"
- `prov:wasInfluencedBy` (expanded): "relates any influenced Entity, Activity, or Agent to any other influencing Entity, Activity, or Agent" (s3.2 description)
- `prov:wasAttributedTo` (starting point): "Attribution is the ascribing of an entity to an agent."
- `prov:wasRevisionOf`: "A revision is a derivation for which the resulting entity is a revised version of some original."
- Inverse: "Modelers wishing to use inverses of the properties defined by PROV-O should use those reserved by this document." (Appendix B); the inverse of `prov:wasDerivedFrom` is `prov:hadDerivation`, `http://www.w3.org/ns/prov#hadDerivation`.

### 1.3 Dublin Core Terms (DCTERMS)
- Link: <https://www.dublincore.org/specifications/dublin-core/dcmi-terms/> [F]. Version: DCMI Recommendation, issued 2020-01-20 (`.../dcmi-terms/2020-01-20/`).
- Covers: provenance-lite (`source`), inclusion (`isPartOf`), versions. **No status term** (my own observation from the term index of the fetched page, not a quotation; the last ~16k characters were not read).
- `dcterms:source` (`http://purl.org/dc/terms/source`): "A related resource from which the described resource is derived."
- `dcterms:references`: "A related resource that is referenced, cited, or otherwise pointed to by the described resource."
- `dcterms:isPartOf`: "A related resource in which the described resource is physically or logically included."
- `dcterms:relation`: "A related resource."

### 1.4 ADMS (Asset Description Metadata Schema)
- Link: <https://www.w3.org/TR/vocab-adms/> [F]. Version: W3C Working Group Note, 1 August 2013, **retired August 2023**; maintained by SEMIC at <https://uri.semic.eu/w3c/ns/adms>.
- Covers: status of an asset in a workflow.
- `adms:status` (s5.3.34): "The status of the Asset in the context of a particular workflow process." Range `skos:Concept`.
- The Note does not list the status values; it says they are in the original ADMS 1.0 spec (example IRI seen: `http://purl.org/adms/status/Completed`).

### 1.5 schema.org `creativeWorkStatus`
- Link: <https://schema.org/creativeWorkStatus> [F]. Version: schema.org V30.1 (2026-09-16, shown as the development version).
- "The status of a creative work in terms of its stage in a lifecycle." Example terms: "Incomplete, Draft, Published, Obsolete." Expected types: DefinedTerm, Text.
- Domain is CreativeWork. Our pages are not typed as that, so adoption brings a web-markup vocabulary into an SE ontology.

### 1.6 SOSA/SSN
- Link: <https://www.w3.org/TR/vocab-ssn/> [F]. Version: W3C Recommendation, 19 October 2017.
- Covers: a property-to-device relation, the nearest to Attributes (affordance x technology), but for observation.
- `sosa:ObservableProperty`: "An observable quality (property, characteristic) of a FeatureOfInterest."
- `sosa:isObservedBy` (`http://www.w3.org/ns/sosa/isObservedBy`): "Relation between an ObservableProperty and the Sensor able to observe it."
- `ssn:Property`: "A quality of an entity. An aspect of an entity that is intrinsic to and cannot exist without the entity."
- Fit: the relation is about measuring, not providing; a Technology is not a Sensor. Terms listed for completeness.

### 1.7 OSLC Requirements Management 2.1
- Links: <https://docs.oasis-open-projects.org/oslc-op/rm/v2.1/os/requirements-management-spec.html> and <https://docs.oasis-open-projects.org/oslc-op/rm/v2.1/os/requirements-management-vocab.html> [F]. Version: OASIS Standard, 21 June 2021. Namespace `http://open-services.net/ns/rm#`.
- `oslc_rm:Requirement`: "Statement of need."
- `oslc_rm:satisfiedBy` (`http://open-services.net/ns/rm#satisfiedBy`): "The subject is satisfied by the object. For example, a user requirement is satisfied by a system requirement."
- `oslc_rm:satisfies`: "Expresses a relationship between entities, where the subject entity satisfies the object entity."
- `oslc_rm:affectedBy`: "Expresses an affects relationship between entities, where the object entity in some way affects the subject entity."
- Covers: the nearest SE-recognised verb for Attributes (technology satisfies affordance) and for Addresses.
  Phrased over "entities", but I did not verify its formal domain and range.

### 1.8 iStar 2.0 (and KAOS)
- Link: <https://arxiv.org/abs/1605.07767> (PDF <https://arxiv.org/pdf/1605.07767>) [F]. Version: iStar 2.0 Language Guide, Dalpiaz, Franch, Horkoff, v3 16 June 2016.
- Covers: actors with intentional elements, graded contribution links. s6.3 (read from the PDF text):
  - "Contribution links represent the effects of intentional elements on qualities"
  - Types: Make ("sufficient positive evidence for the satisfaction of the target"), Help ("weak positive evidence"), Hurt ("weak evidence against the satisfaction"), Break ("sufficient evidence against the satisfaction").
- iStar 2.0 has no concern-to-concern conflict link and no "holds" link. Contribution runs from an element to a quality, and is directional and graded.
- KAOS: **[NF]**. Its conflict links come from van Lamsweerde's textbook (Wiley, 2009), which I did not retrieve. I make no KAOS claim beyond "to be checked".
- Neither publishes an OWL vocabulary that I found, so nothing here is importable as an IRI.

### 1.9 ISO/IEC/IEEE 42010
- Links: <https://standards.ieee.org/ieee/42010/6846/> [F] (metadata only); <https://www.iso.org/standard/74393.html> [NF] (HTTP 403); <https://www.iso-architecture.org/> [NF] (connection refused).
- Version: IEEE/ISO/IEC 42010-2022 *Software, systems and enterprise: Architecture description*, approved 2022-09-21, published 2022-11-07, supersedes 42010-2011.
- Scope (page text): "specifies requirements for the structure and expression of an architecture description" (AD); covers "frameworks, languages, viewpoints, and model kinds".
- **Verbatim definitions of stakeholder, concern, AD, viewpoint are not quoted**: the standard is paywalled and no open copy was retrievable. The `stakeholders and concerns` unit owns those. For this cluster the standard supplies the AD record idea (architecture description) and the vocabulary "concern", with no relation IRIs (it publishes no OWL).

### 1.10 SysML v2 (by reference)
- Link: <https://www.omg.org/spec/SysML/2.0> [F]. Version: SysML 2.0, formal, September 2025. Machine-readable files under `https://www.omg.org/spec/SysML/20250201/` (the Beta4 page, Beta4 date July 2025).
- "SysML is a general-purpose modeling language for modeling systems"
- Pattern in `concept-definition-stage` (`ontology/concept-definition.ttl`, read-only): `sysml:UseCaseDefinition owl:equivalentClass omg-sysml:UseCaseDefinition`, with `cds:sysmlConstruct` on concepts. The concept is anchored by an annotation, not by import.
- Parts: `concept-definition-stage` also anchors `sysml:PartDefinition` to `omg-sysml:PartDefinition` by `owl:equivalentClass` (read, `ontology/concept-definition.ttl`). The SysML page fetched does not quote part semantics, so none is claimed here.
- Fit for this cluster: a scenario is a story told by actors, not a use case definition; any SysML link would be an annotation at most.

### 1.11 `concept-definition-stage` (local, read-only)
- Path: `/Users/z/Documents/GitHub/concept-definition-stage` [F], at commit `4d1e52e` (2026-06-28); `cds` core ontology `owl:versionInfo "0.1.0"`.
- `cds:addresses`: "A concept addresses the problem / threat / opportunity it is defined for (GtWR)." Domain and range `cds:Term` (SEBoK/INCOSE concept definitions). A same-named term exists, with a different domain; reuse would pull in `cds:Term`.
- Status pattern: `cds:RetrievalStatus` is a `skos:ConceptScheme` with concepts `pending`, `provided`, `verified`; `cds:retrievalStatus` is an object property to a `skos:Concept`. The ordered lifecycle is encoded as SKOS concepts plus one property, with SHACL enforcing the order.
- Provenance pattern: `cds:Source rdfs:subClassOf prov:Entity` ("A boundary object: a specific artifact held by an authority."), and `prov:wasDerivedFrom` from the vocabulary to sources.

### 1.12 OWL 2 (axioms)
- Link: <https://www.w3.org/TR/owl2-syntax/> [F]. Version: W3C Recommendation, 11 December 2012.
- "_Classes_ can be understood as sets of individuals." (s5.1)
- DisjointClasses (s9.1.3): "no individual can be at the same time an instance of both CEi and CEj for i != j." (Here "!=" transliterates the spec's inequality sign; the rest is verbatim.) Note the section is 9.1.3; 9.1.4 is DisjointUnion.
- DisjointObjectProperties (s9.2.3): "no individual x can be connected to an individual y by both OPEi and OPEj for i != j." ("!=" transliterates the inequality sign.)
- Different individuals (s9.6.2): "all of the individuals ai, 1 <= i <= n, are different from each other" ("<=" transliterates the spec's symbol.)
- Metamodeling (s5.9): "An IRI I can be used in an OWL 2 ontology to refer to more than one type of entity." (the spec calls it metamodeling; the term "punning" did not appear in the text I read.)
- OWL gives no axiom saying "these two individuals are in conflict"; disjointness constrains classes and properties, and different-individuals only says they are not identical.

### 1.13 SHACL
- Link: <https://www.w3.org/TR/shacl/> [F]. Version: W3C Recommendation, 20 July 2017.
- `sh:class` (s4.1.1): constraint component `sh:ClassConstraintComponent`.
- `sh:disjoint` (s4.5.2): constraint component `sh:DisjointConstraintComponent`; "For each value node that also exists as a value of the property $disjoint at the focus node" (a violation arises).
- `sh:not` (s4.6.1): "Otherwise, if v conforms to the shape $not, there is validation result with v as sh:value."
- SHACL-SPARQL (s5): constraint component `sh:SPARQLConstraintComponent`; "SHACL-SPARQL supports a constraint component that can be used to express restrictions based on a SPARQL SELECT query."
- Severity levels (Violation, Warning, Info) are in SHACL core; `concept-definition-stage` maps its tiers T1/T2/T3 to them (AGENTS.md, read). Not re-quoted from the spec by me.

### 1.14 Event Ontology (events)
- Link: <https://motools.sourceforge.net/event/event.html> [F]. Version: 1.0, 25 October 2007; namespace `http://purl.org/NET/c4dm/event.owl#`.
- `event:Event`: "An arbitrary classification of a space/time region, by a cognitive agent."
- `event:factor`: "Relates an event to a passive factor (a tool, an instrument, an abstract cause...)"
- `event:sub_event`: "This property provides a way to split a complex event" (into simpler events).
- No causal property is defined; the only causal wording is "an abstract cause" in `event:factor`.

### 1.15 LODE (linking open descriptions of events)
- Links tried: <https://linkedevents.org/ontology/> and <http://linkedevents.org/ontology/> [NF]: both HTTP 404. No claim made.

### 1.16 SEM (Simple Event Model)
- Link: <http://semanticweb.cs.vu.nl/2009/11/sem/> [F]. Version: no explicit date; 2009 per the IRI path.
- `sem:Event`: "Events are things that happen."
- `sem:hasActor`: "Has actor is used to state which Actors or Objects participate in an Event."
- `sem:hasSubEvent`: connects an Event to Events that belong to it; the document says it "does not mean... that there is any causal relationship."
- No causal or sequence property is defined.

### 1.17 CIDOC-CRM
- Link: <https://cidoc-crm.org/html/cidoc_crm_v7.1.3.html> [F]. Version: 7.1.3, released February 2024.
- `E5 Event`: "This class comprises distinct, delimited and coherent processes and interactions of a material nature"
- `P15 was influenced by` (range E1 CRM Entity) and `P17 was motivated by` (range E1) are the generic influence links. Definitions not quoted.
- Scale: a large cultural-heritage model; named for completeness.

### 1.18 OWL-Time
- Link: <https://www.w3.org/TR/owl-time/> [F]. Version: W3C Candidate Recommendation Draft, 15 November 2022.
- `time:TemporalEntity`: "A temporal interval or instant."
- `time:before`: "The subject is a temporal entity that occurs before the object."
- No event class; events and activities attach to time through `time:hasTime`.

### 1.19 Causal-chain and consequence vocabularies
- None found among the sources above. The Event Ontology, SEM and OWL-Time define no causal property; PROV and CIDOC-CRM have generic influence links only. I searched only these sources, so "none found" is not "none exist".

## 2. Coverage matrix (what each candidate offers per element)

| Element | SKOS | PROV-O | DCTERMS | ADMS | schema.org | SOSA/SSN | OSLC RM | iStar | 42010 | SysML v2 | cds |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Heldby | none | `wasAttributedTo` (wrong: agent credit) | none | none | none | none | none | actor owns elements (no named link) | stakeholder-concern relation, text NF | none | none |
| Addresses | `related` (untyped) | none | none | none | none | none | `satisfies` (nearest, partial) | contribution links (graded, to quality) | NF | none | `cds:addresses` (Term x Term) |
| Attributes | `related` (untyped) | none | none | none | none | `isObservedBy` (observation) | `satisfiedBy` (nearest) | contribution (to quality) | none | none | none |
| Scenario / architecture records | Concept (wrong) | `Entity` | `BibliographicResource` NF | `Asset` NF | CreativeWork NF | none | `Requirement` (wrong) | none | AD record | UseCaseDefinition, PartDefinition (anchor only) | `Source` (boundary object) |
| Status | scheme of concepts | none | none | `status` | `creativeWorkStatus` | none | none | none | none | none | `retrievalStatus` pattern |
| Provenance | none | `wasDerivedFrom` and others | `source` | none | none | none | none | none | none | none | uses PROV |

### Added coverage: behaviour and structure

| Element | Candidates | Best fit found |
|---|---|---|
| Events in a scenario | PROV `Activity`; Event Ontology `Event`; SEM `Event`; CIDOC `E5`; (LODE NF) | PROV `Activity` (already the provenance spine); none needed if prose carries it |
| Causal chain, consequence | PROV `wasInformedBy`, `wasInfluencedBy`; CIDOC `P15`; Event Ontology `event:factor` (text only) | PROV `wasInformedBy` for activity chains; none has a causal-consequence term |
| Sequence / time | OWL-Time `before` | not needed; order of the list in the note |
| Structure, composition | `dcterms:hasPart`; SysML v2 part by reference; 42010 AD | `dcterms:hasPart` if a link is wanted |
