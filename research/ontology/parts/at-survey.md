# WP1-U2 survey: Affordance and Technology

Partial file for `survey.md` (WP1-D1). Scope: the elements **Affordance** and **Technology**, as `MISSION.md` G1
defines them. Fetch date for every source: 2026-11-23. "Fetched" means the text was retrieved and read this session;
quotes were checked against the retrieved text. Quotes are verbatim.

## What the mission means by the two elements

- **Affordance** (Scenarios and architectures): technologies "stay relatively fixed and out of view, and what is
  legible is their **affordances**". Architectures assemble parts "into tools that provide affordances which address
  concerns". The relation Addresses is concern × affordance; Attributes is affordance × technology.
- **Technology** (same section): architectures "formulate assemblages: parts and wholes". Technologies are part of
  the action situation but not its focus.

## Source register (WP1-R5: link and version for each source)

| # | Source | Link | Version / date | Status |
|---|---|---|---|---|
| S1 | Gibson, *The Ecological Approach to Visual Perception* (1979); the scan titled "The Theory of Affordances" | <https://monoskop.org/images/c/c6/Gibson_James_J_1977_1979_The_Theory_of_Affordances.pdf> | Houghton Mifflin 1979; Routledge Classic Edition 2014 | Scan fetched, but image-only: no text layer, no OCR available. **Substitute:** S2's verbatim quotation of the book, p. 119. |
| S2 | Toyoshima, "Modeling Affordances with Dispositions" | <https://ceur-ws.org/Vol-2205/paper20_caos3.pdf> | CEUR-WS Vol-2205 (CAOS workshop, JOWO 2017 proceedings), 6 pp. | Fetched, text read |
| S3 | Toyoshima, Barton, Ethier, "Affordances and their ontological core", *Applied Ontology* 17(2) | <https://doi.org/10.3233/AO-220267> | 2022-05-02, DOI 10.3233/AO-220267 | Publisher page returned HTTP 403. **Substitute:** Crossref record <https://api.crossref.org/works/10.3233/AO-220267> (fetched; abstract read). Body text not read. |
| S4 | Norman, "Affordances and Design", jnd.org | <https://jnd.org/affordances-and-design/> | 2008-11-17 | Fetched |
| S5 | Maier and Fadel, "Affordance based design: a relational theory for design", *Research in Engineering Design* 20(1) | <https://doi.org/10.1007/s00163-008-0060-3> | 2008-12-12 online; DOI as shown | Springer page redirects to a login handshake. **Substitute:** Crossref record <https://api.crossref.org/works/10.1007/s00163-008-0060-3> (title, authors, venue only; no abstract). Content not read. |
| S6 | Maier and Fadel, "Affordance-based design methods for innovative design, redesign and reverse engineering", *Res. Eng. Design* 20(4) | <https://doi.org/10.1007/s00163-009-0064-7> | 2009-03-12 | Same as S5; Crossref record only. Content not read. |
| S7 | Gaver, "Technology affordances", CHI '91 | <https://doi.org/10.1145/108844.108856> | 1991 | Bibliographic record only (Crossref). Content not read; not scored. |
| S8 | Hartson, "Cognitive, physical, sensory, and functional affordances in interaction design", *Behaviour & IT* 22 | <https://doi.org/10.1080/01449290310001592587> | 2003-09 | Bibliographic record only (Crossref). Content not read; not scored. |
| S9 | Moralez, "Affordance Ontology: Towards a Unified Description of Affordances as Events", *Int. J. Undergraduate Research and Creative Activities* | <https://doi.org/10.7710/2155-4838.1145> | 2016-06-24 | Crossref record only. ResearchGate copy returned HTTP 403. A web-search summary says it has a DOLCE-based OWL TBox; **not verified**, so not scored. |
| S10 | W3C, Web of Things (WoT) Thing Description 1.1 | <https://www.w3.org/TR/2023/REC-wot-thing-description11-20231205/> | W3C Recommendation, 2023-12-05; vocabulary `https://www.w3.org/2019/wot/td#` | Fetched, text read |
| S11 | W3C, WoT Architecture 1.1 | <https://www.w3.org/TR/2023/REC-wot-architecture11-20231205/> | W3C Recommendation, 2023-12-05 | Fetched, text read |
| S12 | SEBoK glossary: System Element | <https://sebokwiki.org/wiki/System_Element_(glossary)> | SEBoK v2.14, released 18 May 2026; text from ISO/IEC/IEEE 15288:2015 | Fetched, text read |
| S13 | SEBoK glossary: Capability | <https://sebokwiki.org/wiki/Capability_(glossary)> | SEBoK v2.14 | Fetched, text read |
| S14 | SEBoK glossary: Function; Product | <https://sebokwiki.org/wiki/Function_(glossary)>, <https://sebokwiki.org/wiki/Product_(glossary)> | SEBoK v2.14 | Fetched (read via the fetch tool; not used for a scored claim) |
| S15 | `concept-definition-stage` (cds), `src/cds/ontology/cds-core.ttl` and `concept-definition.ttl` | <https://github.com/Open-MBEE/concept-definition-stage> | `main` at commit `99cecd1d36c7ffd4af540773b0907b59a122c65d` (2026-07-25); `owl:versionInfo "0.1.0"`; no tags or releases | Both Turtle files downloaded and read in full |
| S16 | OMG SysML v2, Part 1: Language Specification (by reference only) | <https://www.omg.org/spec/SysML/2.0/> (PDF <https://www.omg.org/spec/SysML/2.0/Language/PDF>) | SysML 2.0, formal/2026-03-02, March 2026 | PDF downloaded, text extracted and read for the cited clauses |
| S17 | W3C, SSN/SOSA | <https://www.w3.org/TR/vocab-ssn/> | W3C Recommendation, 2017-10-19 (OGC 16-079); `http://www.w3.org/ns/sosa/`, `http://www.w3.org/ns/ssn/` | Fetched, text read |
| S18 | ETSI SAREF core | <https://saref.etsi.org/core/v4.1.1/> | v4.1.1 (ETSI TS 103 264 V4.1.1, 2025-03 per search result, not opened) | Fetched, text read |
| S19 | BFO 2020 (ISO/IEC 21838-2), `bfo-core.owl` | <https://raw.githubusercontent.com/BFO-ontology/BFO-2020/master/21838-2/owl/bfo-core.owl>; version IRI `http://purl.obolibrary.org/obo/bfo/2020/bfo-core.owl` | BFO 2020 | Downloaded, read for cited classes |
| S20 | W3C, SKOS Reference | <https://www.w3.org/TR/skos-reference/> | W3C Recommendation, 2009-08-18; `http://www.w3.org/2004/02/skos/core#` | Fetched, text read |
| S21 | QUDT | <https://www.qudt.org/> | Page shows "Release 2.1" labelled old; no current number on the page | Fetched |
| S22 | The Open Group, ArchiMate 3 Technology Layer | <https://pubs.opengroup.org/architecture/archimate3-doc/ch-Technology-Layer.html> | not obtained | **Unreachable:** redirects to a login. No substitute fetched; not scored. |
| S23 | SEBoK glossary: Technology | <https://sebokwiki.org/wiki/Technology_(glossary)> | n/a | HTTP 404. The glossary index (<https://sebokwiki.org/wiki/Glossary_of_Terms>) has no "technology" or "affordance" entry. |

## Findings by source

### Affordance

**Gibson (S1 via S2).** S2 quotes the book: "The affordances of the environment are what it offers the animal, what it
provides or furnishes, either for good or ill" (Gibson 1979, p. 119, as cited in S2). The sense is relational and
animal-environment. Gibson is a theory, not a vocabulary: no classes, no IRIs.

**Norman (S4).** "To Gibson, affordances are a relationship." and "Part of the blame lies with me: I should have used
the term “perceived affordance,” for in design, we care much more about what the user perceives than what is actually
true." So the HCI sense differs: what the user *perceives*. For SCAT, scenario participants tell what they can do, which
is closer to the perceived sense; architecture pitches state what a tool offers, closer to the actual sense.

**Maier and Fadel (S5, S6).** Design-engineering theory ("affordance based design"; an affordance structure matrix
relating artifact and user affordances). Only bibliographic records were reached, so no claim about their content is
made beyond the titles. Not a vocabulary as far as reached. Candidate for the readout's bibliography, not for adoption.

**Published affordance ontologies.**
- S2 (Toyoshima 2017): "a preliminary first-order formalization of the dispositional conception of affordance along
  Turvey's line of argument." An affordance is a disposition inhering in a non-agentive object; an *effectivity* is
  its reciprocal disposition inhering in an agent; realization is an action. Uses Röhl and Jansen's disposition
  relations (bearer, trigger, realization, background condition). No OWL file or IRI is released in the paper.
- S3 (Toyoshima, Barton, Ethier 2022), abstract (Crossref): "This paper lays down a foundation for an ontology of
  affordances by elaborating the idea of “core affordance”". Two kinds: specific (reciprocal with an agent's
  effectivity) and general ("does not depend on individual agents; rather, its realization involves an action by an
  instance of a determinate class of agents"). Whether an OWL artifact exists could not be determined (body text
  unreachable).
- S9: unverified, undergraduate venue.
- Negative result: web search found no standalone published OWL affordance vocabulary beyond these (search summary,
  not a fetched primary source).

**W3C WoT (S10, S11).** The only widely used *standard* vocabulary with an affordance class. Verbatim, S10 5.3.1.2:
"Metadata of a Thing that shows the possible choices to Consumers, thereby suggesting how Consumers may interact with
the Thing". Subclasses: PropertyAffordance ("An Interaction Affordance that exposes state of the Thing."),
ActionAffordance, EventAffordance. S11's glossary: "Metadata of a Thing that shows and describes the possible choices to
Consumers". Note the sense: *metadata describing* the possibilities for machine Consumers of a `td:Thing`, not the
possibilities themselves. Namespace `https://www.w3.org/2019/wot/td#`.

**SEBoK Capability (S13).** Four definitions. The one "created for the SEBoK": "An outcome or effect which can be
achieved through use of features of a system of interest and which contributes to a desired benefit or goal". Others
from DoD 2009 and MOD 2004 define capability as an "ability" ("The ability to achieve a desired effect under specified
(performance) standards and conditions ..."). cds already carries `cdsterm:capability` with the DoD wording and
`skos:exactMatch` to this SEBoK page (S15, `concept-definition.ttl` l.220-229) and tags it
`cds:sysmlConstruct sysml:UseCaseDefinition`.

**BFO (S19).** `BFO_0000016` disposition, elucidation: "A disposition b is a realizable entity such that if b ceases
to exist then its bearer is physically changed & b's realization occurs when and because this bearer is in some
special physical circumstances & this realization occurs in virtue of the bearer's physical make-up". `BFO_0000034`
function (subclass of disposition): "The function of a hammer to drive in nails" is an example; the elucidation ties
function to "evolution ... or ... intentional design (in the case of artefacts)". S2 and S3 build on this family of
disposition ontologies. BFO is an upper ontology: adopting a class would drag its axioms (e.g. disjointness of
disposition and role) into our graph.

**SAREF (S18).** `saref:Function`: "Logical groups of commands that devices support to accomplish their tasks." IoT
device commands; far narrower than the mission's sense.

**SysML v2 (S16, by reference only).** No affordance construct. Closest are Action/Use case, which are behaviours of
the system, not what a stakeholder perceives. Not scored.

**SKOS (S20).** Provides `skos:Concept` ("The class skos:Concept is the class of SKOS concepts"), `skos:ConceptScheme`
("A SKOS concept scheme can be viewed as an aggregation of one or more SKOS concepts") and mapping properties.
It defines no affordance term. Role: the carrier form for a definition-plus-anchor, as cds does (S15).

### Technology

**SEBoK / ISO 15288 System Element (S12).** Verbatim: "A system element is a discrete part of a system that can be
implemented to fulfill specified requirements." and, from the same entry, "A member of a set of elements that
constitutes a system." The entry goes on to say the element can be hardware, software, data, humans, processes,
procedures, facilities, materials, or naturally occurring entities, or a combination (summary by the fetch tool;
exact sentence not quoted). Attribution on the page: ISO/IEC/IEEE 15288:2015. cds has **no** System Element term:
its 36 `cdsterm:` entries (checked by listing) include `system-of-interest`, `engineered-system`, `capability`,
`function`, `solution`, but not `system-element` or `technology`. Its precedent is to add a term with
`skos:definition` verbatim, `cds:definitionSource` and `skos:exactMatch` to the SEBoK glossary page.

**SEBoK has no "Technology" glossary entry (S23).** HTTP 404 for the entry URL and no entry in the glossary index.
Search for "affordance" across the SEBoK found nothing relevant (web-search result; only "System Affordability").

**SysML v2 (S16), by reference only.** Part 1, 8.3.11.2: "A PartDefinition is an ItemDefinition of a Class of systems
or parts of systems." The OMG page (S16) lists normative machine-readable artefacts: MOF XMI, KerML KPAR libraries,
JSON schema. **No OWL or Turtle file is among them**, so there is no OMG-published IRI for `PartDefinition` to anchor
to. cds nevertheless declares `omg-sysml:PartDefinition` in the namespace
`https://www.omg.org/spec/SysML/20240801/SysML#` and `sysml:PartDefinition` in `https://www.omg.org/spec/SysML/2.0/`,
joined by `owl:equivalentClass`, and tags `cdsterm:system-of-interest` with `cds:sysmlConstruct sysml:PartDefinition`
(S15, l.531-541, 570-593). Two namespaces for one construct, neither an OMG-served ontology, is a maintenance warning.

**SOSA/SSN (S17).** `sosa:Platform`: "A Platform is an entity that hosts other entities, particularly Sensors,
Actuators, Samplers, and other Platforms." `ssn:System`: "System is a unit of abstraction for pieces of
infrastructure that implement Procedures." Has `ssn:hasSubSystem` (parts and wholes). Bound to sensing and actuation;
Procedure, Deployment and observation vocabulary would come with it.

**SAREF (S18).** `saref:Device`: "A tangible object designed to accomplish a particular task." ... "the device performs
one or more functions". Tangible only: excludes software, data, procedures and people, which "technology" in an
architecture pitch may include.

**ArchiMate Technology Layer (S22).** Unreachable (login redirect). It is the best-known enterprise-architecture
"technology" vocabulary, so the gap is noted rather than papered over; it is not scored.

**BFO (S19).** `BFO_0000040` material entity could host tangible parts only; same upper-ontology cost as above.
Not scored as a separate option.

**QUDT (S21).** Units and quantities. Neither element carries a quantity in `MISSION.md` G1. Not applicable; recorded
so the starting point is covered.

## Coverage of the starting points, for these two elements

| Starting point | Covers Affordance | Covers Technology | Where |
|---|---|---|---|
| Gibson / HCI / design affordance | yes (theory) | no | S1-S9 |
| Published affordance ontology | yes (S2, S3 formal; no released OWL found) | no | S2, S3 |
| SEBoK / INCOSE canon | partly (Capability) | yes (System Element) | S12, S13 |
| `concept-definition-stage` | partly (Capability term) | no entry; pattern only | S15 |
| SKOS | carrier only | carrier only | S20 |
| SOSA/SSN | no | partly (Platform, System) | S17 |
| SysML v2 (by reference) | no | partly (PartDefinition) | S16 |
| QUDT | not applicable | not applicable | S21 |
| ISO/IEC/IEEE 42010, PROV-O, Dublin Core, iStar/KAOS, OSLC RM, event vocabularies | not applicable to these elements (owned by other units) | same | n/a |
| Added: W3C WoT TD, SAREF, BFO, ArchiMate | yes (WoT, SAREF, BFO) | SAREF, BFO; ArchiMate unreachable | S10, S11, S18, S19, S22 |
