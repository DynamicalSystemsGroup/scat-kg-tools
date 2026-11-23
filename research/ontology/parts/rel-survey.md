# WP1-U3 survey part: relations, records, status, provenance, disagreement

Feeds `survey.md` (WP1-D1). Covers: Heldby, Addresses, Attributes, the scenario record, the architecture record, page
status, provenance, and options for holding disagreement. All sources fetched on 2026-11-23 from the URL shown.
Quotes are verbatim (line breaks joined). "Unreachable" entries are listed at the end, with what was used instead.

## Sources

| ID | Source | Link (fetched) | Version / date | Covers |
|---|---|---|---|---|
| S1 | ISO/IEC/IEEE 42010 conceptual model, as published by the standard's community site | <http://www.iso-architecture.org/42010/cm/> | 2nd edition (2022) and 1st edition (2011) models on one page | Heldby, architecture record |
| S2 | PROV-O | <https://www.w3.org/TR/prov-o/> | W3C Recommendation, 30 Apr 2013 | provenance, scenario (influence), disagreement |
| S3 | SKOS Reference | <https://www.w3.org/TR/skos-reference/> | W3C Recommendation, 18 Aug 2009 | disagreement (integrity conditions) |
| S4 | DCMI Metadata Terms | <https://www.dublincore.org/specifications/dublin-core/dcmi-terms/> | issued 2020-01-20 (DCMI Recommendation) | architecture parts, provenance |
| S5 | OWL 2 Structural Specification | <https://www.w3.org/TR/owl2-syntax/> | W3C Recommendation, 11 Dec 2012 | disagreement (disjointness) |
| S6 | OWL 2 Primer | <https://www.w3.org/TR/owl2-primer/> | W3C Recommendation (2012 edition) | disagreement (punning) |
| S7 | SHACL | <https://www.w3.org/TR/shacl/> | W3C Recommendation, 20 Jul 2017 | disagreement (severity, sh:disjoint) |
| S8 | SOSA/SSN | <https://www.w3.org/TR/vocab-ssn/> | W3C Recommendation, 19 Oct 2017 | architecture parts |
| S9 | Time Ontology in OWL | <https://www.w3.org/TR/owl-time/> | W3C Candidate Recommendation Draft, 15 Nov 2022 | scenario (ordering) |
| S10 | RDF 1.1 Concepts | <https://www.w3.org/TR/rdf11-concepts/> | W3C Recommendation, 25 Feb 2014 | disagreement (named graphs) |
| S11 | Simple Event Model (SEM) | <https://semanticweb.cs.vu.nl/2009/11/sem/> | 2009-11 (VU Semantic Web group) | scenario, disagreement |
| S12 | Relations Ontology (RO) | <http://purl.obolibrary.org/obo/ro.owl> (served from `oborel/obo-relations`) | owl:versionInfo 2026-09-04 | Attributes, scenario (causal), architecture |
| S13 | iStar 2.0 Language Guide (Dalpiaz, Franch, Horkoff) | <https://arxiv.org/pdf/1605.07767> | arXiv v3, 16 Jun 2016 | Heldby, Addresses, disagreement |
| S14 | OSLC Requirements Management 2.1, Part 2: Vocabulary | <https://docs.oasis-open-projects.org/oslc-op/rm/v2.1/os/requirements-management-vocab.html> | OASIS Standard, 21 Jun 2021 | Addresses |
| S15 | Vocabulary status note (`vs:term_status`) | <https://www.w3.org/2003/06/sw-vocab-status/note> | Editor's draft of a potential W3C IG Note, 31 Dec 2009 | status |
| S16 | schema.org `creativeWorkStatus`, `Event` | <https://schema.org/creativeWorkStatus>, <https://schema.org/Event> | schema.org v30.1 (release 2026-09-16 per the page footer; pages show the development version) | status, scenario |
| S17 | ADMS | <https://www.w3.org/TR/vocab-adms/> | W3C Working Group Note, 1 Aug 2013 (retired Aug 2023; now maintained by SEMIC) | status |
| S18 | PAV | <https://pav-ontology.github.io/pav/> | 2.3.1 | provenance |
| S19 | Nanopublication Guidelines | <https://nanopub.net/guidelines/working_draft/> | working draft (undated on page) | disagreement |
| S20 | `ant-rdf` (`ONTOLOGICAL_COMMITMENTS.md`, `FUTURE_WORK.md`, `ontology/material-semiotics-core.ttl`) | <https://github.com/mzargham/ant-rdf> | commit `a2ec48edc8f44e386eaeada922c4a90349581df3`; ontology owl:versionInfo 0.1.0-draft | disagreement, status/severity |
| S21 | `concept-definition-stage` (`src/cds/core/model/notes.py`, `src/cds/core/verify.py`, `src/cds/ontology/cds-core.ttl`, `docs/user-guide.md`) | <https://github.com/Open-MBEE/concept-definition-stage> | commit `99cecd1d36c7ffd4af540773b0907b59a122c65d` (2026-07-25); package 0.1.0 | Addresses, disagreement |
| S22 | SysML v2 release (by reference only) | <https://github.com/Systems-Modeling/SysML-v2-Release> | release `2026-09.1` (2026-10-30); the spec PDFs were not read | architecture record |

## Findings per element (the evidence the trade tables use)

### Heldby (stakeholder group x concern)
- S1: "Stakeholders are individuals, groups or organizations holding Concerns for the System of Interest." and "A Concern
  is any interest in the system." Concept only; no IRI is published.
- S13: "Goal: a state of affairs that the actor wants to achieve and that has clear-cut criteria of achievement." (an
  intentional element sits inside an actor's boundary). No IRI published in the guide.
- S2: `prov:wasAttributedTo`: "Attribution is the ascribing of an entity to an agent."
- S21: `cds:forStakeholder` links a need to a stakeholder (used in `verify.py`, `compile.py`); it is a link from a need,
  not from a concern, and `cds` publishes it only as a code-level link in the version fetched.

### Addresses (concern x affordance)
- S21: `cds:addresses`, domain and range `cds:Term`: "A concept addresses the problem / threat / opportunity it is
  defined for (GtWR)."
- S14: `rm:satisfies`: "Expresses a relationship between entities, where the subject entity satisfies the object
  entity. For example, a system requirement satisfies a user requirement."
- S13: contribution links: "Help: The source provides weak positive evidence for the satisfaction of the target." and
  "Hurt: The source provides weak evidence against the satisfaction (or for the denial) of the target." Source: an
  intentional element; target: a quality.
- S1 (2nd edition note): "This 2nd edition introduces Stakeholder Perspectives as a means to group Concerns and
  therefore to organize Viewpoints framing those Concerns." Viewpoints frame concerns; they are not affordances.

### Attributes (affordance x technology)
- S12: `RO_0000091` has disposition: "a relation between an independent continuant (the bearer) and a disposition, in
  which the disposition specifically depends on the bearer for its existence".
- S8: `ssn:System`: "System is a unit of abstraction for pieces of infrastructure that implement Procedures." The
  specification opens: "The Semantic Sensor Network (SSN) ontology is an ontology for describing sensors and their
  observations, the involved procedures, the studied features of interest, the samples used to do so, and the observed
  properties, as well as actuators."
- Affordance sources (Gibson and later) belong to the Affordance class unit; they were not fetched here.

### Scenario record (behavioural)
- S11: "Events are things that happen." Core classes: `sem:Event`, `sem:Actor`, `sem:Place`, `sem:Time`.
  `sem:hasSubEvent`: "This is a very generic property that does not mean the subevents fully define the superconcept or
  that there is any causal relationship." SEM defines no causal property.
- S12: `RO_0002411` causally upstream of: "p is causally upstream of q iff p is causally related to q, the end of p
  precedes the end of q, and p is not an occurrent part of q."
- S9: `time:before`: "The subject is a temporal entity that occurs before the object." Status: Candidate
  Recommendation Draft.
- S2: `prov:wasInfluencedBy` "is a superproperty that relates any influenced Entity, Activity, or Agent to any other
  influencing Entity, Activity, or Agent that had an effect on its characteristics."
- S16: `schema:Event`: "An event happening at a certain time and location, such as a concert, lecture, or festival."
- Event Ontology, LODE and CIDOC CRM: unreachable (below). SEM's own page maps `sem:Event` to them (`skos:broadMatch
  eo:Event, lode:Event`; `skos:closeMatch cidoc:E5.Event, dctype:Event`), which is secondary evidence only.

### Architecture record (structural)
- S1: "An Architecture Description (AD) is an artifact that expresses an Architecture." and "the architecture of a system
  is defined as: 'fundamental concepts or properties of a system in its environment embodied in its elements,
  relationships, and in the principles of its design and evolution'."
- S4: `dcterms:hasPart`: "A related resource that is included either physically or logically in the described
  resource." Comment: "This property is intended to be used with non-literal values."
- S8: `ssn:hasSubSystem`: "Relation between a System and its component parts."
- S12: `BFO_0000050` part of: "a core relation that holds between a part and its whole".
- S22: SysML v2 is cited by reference only (the release repository states OMG adoption of SysML v2 on 30 June 2025).
- S21: the sibling repository's SKOS+PROV spine and its anchoring by equivalence axioms are the mission's stated
  pattern for adoption; no part-whole property was found in its ontology
  Turtle files (grep for part, hasPart, hasSubSystem).

### Page status
- S16: `schema:creativeWorkStatus`: "The status of a creative work in terms of its stage in a lifecycle. Example terms
  include Incomplete, Draft, Published, Obsolete. Some organizations define a set of terms for the stages of their
  publication lifecycle." Values: DefinedTerm or Text.
- S15: `vs:term_status` values 'unstable', 'testing', 'stable', 'archaic'; "the value space for the property is
  open-ended". It labels vocabulary terms, not pages.
- S17: `adms:status`: "The status of the Asset in the context of a particular workflow process." Note retired Aug 2023.
- S18: PAV defines authorship and versioning (`pav:authoredBy`, `pav:previousVersion`), no status property was found.

### Provenance
- S2: `prov:wasDerivedFrom`: "A derivation is a transformation of an entity into another, an update of an entity resulting in a new one, or the construction of a new entity based on a pre-existing entity." `prov:generatedAtTime`
  bounds an Entity's existence. `prov:wasAttributedTo` as above.
- S4: `dcterms:source`: "A related resource from which the described resource is derived." `dcterms:provenance`: "A
  statement of any changes in ownership and custody of the resource since its creation that are significant for its
  authenticity, integrity, and interpretation."
- S18: `pav:authoredBy`: "The author of the content of a resource may be different from the creator of the resource
  representation (although they are often the same)."

### Disagreement and margins of conflict
- S3 (SKOS): "skos:related is disjoint with the property skos:broaderTransitive." and "the statement that <Dog> and
  <Cat> are disjoint classes can be viewed as an integrity condition on a data model."
- S5: "A disjoint classes axiom DisjointClasses( CE 1 ... CE n ) states that all of the class expressions CE i, 1 <= i <=
  n, are pairwise disjoint; that is, no individual can be at the same time an instance of both CE i and CE j for i != j."
  and "A disjoint object properties axiom ... that is, no individual x can be connected to an individual y by both OPE i
  and OPE j for i != j."
- S6: "an IRI may denote different entity-types (e.g. both an individual and a class) at the same time. This possibility,
  called 'punning,' has been introduced to allow for a certain amount of metamodeling".
- S7 (SHACL): "sh:disjoint specifies the condition that the set of value nodes is disjoint with the set of objects of
  the triples that have the focus node as subject and the value of sh:disjoint as predicate." Severity: "For every shape,
  sh:Violation is the default if sh:severity is unspecified." and "The specific values of sh:severity have no impact on
  the validation".
- S10: "An RDF dataset is a collection of RDF graphs. All but one of these graphs have an associated IRI or blank node.
  They are called named graphs".
- S11 (SEM): the worked example "contains conflicting views on the role of the actor: were the Dutch liberators or
  occupiers?". "To represent opinions sem:accordingTo relates a sem:View to a sem:Authority." and "Views are properties
  that only hold according to a certain Authority."
- S19: a nanopublication "consists of an assertion, the provenance of the assertion ..., and the provenance of the whole
  nanopublication"; each part "is represented as an RDF graph".
- S13 (iStar): Make, Help, Hurt, Break contribution types (quoted above).
- S20 (`ant-rdf`), verbatim from `ONTOLOGICAL_COMMITMENTS.md`:
  - C5: "The vocabulary makes this visible - every association is in principle contestable."
  - C6: "Different perspectives / analysis scopes on the same fieldsite may be **simultaneously valid even when otherwise
    contradictory**".
  - C6: "reified `ant:Characterization` (§4.1.1) lets the same actant carry incompatible role-assignments (e.g., Mediator
    under one practice, Intermediary under another) without OWL inconsistency".
  - C7: "Between these sit **Tier-2 Warnings** - analytical hygiene that should not be violated silently but may be waived
    with a justification".
  - `FUTURE_WORK.md` 1.2: v1 "stores all assertions in a single default graph"; named graphs per perspective are
    deferred ("Mol's multiplicity ... is technically deep"), and "The lift cost is small (one `publicID` argument plus
    per-graph SHACL)".
  - `ant:Perspective`: "A named analysis scope on a fieldsite. ... In v1 a first-class RDF subject; in v2 the same IRI
    becomes the URI of a named graph (no migration)."
  - `ant:ConstraintWaiver`: "An append-only acknowledgement of a Tier-2 SHACL warning, with required justification".
- S21 (`concept-definition-stage`): `Tension` is "A named conflict between records (surfaced, not hidden) - e.g. two
  needs that pull apart." with fields slug, label, description, `between` (IRIs of the records in tension) and status
  `open` or `resolved`; its conflict checks "are surfaced (T2/T3), not gate-failing; they flag rather than block, per the
  elicitation ethos."

## Unreachable or unread, and what was used instead

| Source | Result | Used instead |
|---|---|---|
| ISO/IEC/IEEE 42010 standard text, <https://www.iso.org/standard/74393.html> | HTTP 403 | S1 (community site's conceptual model); definitions are quoted from S1 only |
| LODE, <http://linkedevents.org/ontology/> | HTTP 404 | none; not assessed beyond SEM's mapping |
| Event Ontology, <http://motools.sourceforge.net/event/event.html> and <http://purl.org/NET/c4dm/event.owl> | HTTP 403 | none; not assessed beyond SEM's mapping |
| CIDOC CRM entity pages (version 7.1.3) | HTTP 404 for E5 and P9; version page carries no definitions | none; not assessed |
| Argument Interchange Format (arg.dundee.ac.uk, arg-tech.org) | connection failure / 404 | none; AIF is therefore not assessed |
| OMG SysML 2.0 spec page | bot challenge page | S22 (repository), by reference only |
| KAOS (van Lamsweerde) | not fetched in this unit; fetched by WP1-U1 from the author's open copy (see `sc-survey.md`) | `sc-survey.md` KAOS entry; its conflict link is used in section 8 |
| Gibson on affordances | not fetched here (Affordance class unit) | none |
