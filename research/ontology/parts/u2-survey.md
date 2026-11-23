# WP1-U2 survey: AFFORDANCE and TECHNOLOGY

Unit WP1-U2, branch `wp1/u2-properties-technologies` (name kept on purpose). Cluster: **Affordance** (renamed from Property; the
acronym is now SCAT: Stakeholders, Concerns, Affordances, Technologies) and **Technology**. Relations in this cluster:
Addresses (concern x affordance) and Attributes (affordance x technology). Definitions are verbatim from the page named,
with the fetch route noted. "Fetched" means this unit retrieved the link on 2026-11-23 and the text matched. Anything not
fetched, or read only through a secondary source, is marked **UNVERIFIED** or **secondary**.

Intended meaning (chief engineer, via the ACE): architecture stories centre on structure, that is, arrangements of
technologies into tools with specific affordances; the structure is "just enough ... to make the data interpretable but mostly
... a formal structure for arranging obsidian notes", scaled to a human note-taker. So an **Affordance** is a named action
possibility that a technology or tool offers, as a human user would perceive it (for example "export without a name",
"review a change before it lands"). A **Technology** is a named thing pitched in an architecture. No class for "tool" is added
(`MISSION.md` G1 has four classes).

## Affordance: candidates

### A1. Gibson, The Ecological Approach to Visual Perception (1979)
- Link: https://en.wikipedia.org/wiki/Affordance (secondary; quotes the book, p. 127 per that article). The book itself was not fetched (no open full text found).
  The same quotation is reproduced in a primary-literature paper: https://ai.uni-bremen.de/papers/bessler20affordances.pdf (fetched; cites it as Gibson [10]).
- Version: Boston: Houghton Mifflin, 1979 (as cited on the Wikipedia page; **UNVERIFIED** against the book).
- Covers: the origin of the concept; the environment-relative notion.
- Verbatim (as quoted in both sources): "The affordances of the environment are what it offers the animal, what it provides or furnishes, either for good or ill."
  Further quoted in Beßler et al.: "...an affordance is neither an objective property nor a subjective property; or it is both if you like."
- Note: the noun is relational (environment-for-animal), not an observer's judgement. It carries no IRI. Wikipedia's text calls the "action possibilities" gloss later than Gibson; do not attribute that wording to him.

### A2. Norman, perceived affordances and signifiers
- Link: https://jnd.org/affordances-and-design/ (Norman, 17 November 2008); https://www.jnd.org/the-design-of-everyday-things-revised-and-expanded-edition/ (book page, 2013 edition; no date on page, footer 2023).
- Version: The Design of Everyday Things, revised and expanded edition, Basic Books, 2013 (as cited on both pages and by Wikipedia).
- Covers: affordance as design/HCI term, the user's side. The 2008 page: "there can be both real and perceived affordances, and the two need not be the same" and "we care much more about what the user perceives than what is actually true."
- Signifiers: the 2008 page does not mention them. The book page's synopsis says the science is unchanged "except for the addition of "signifiers,"". Wikipedia quotes the 2013 book: "Affordances determine what actions are possible. Signifiers communicate where the action should take place." (secondary; Norman's own definition text **UNVERIFIED**).
- Note: this is the meaning the chief engineer's phrase "perceived-possible action by a human user" points at. No IRI.

### A3. Turvey, Stoffregen, Chemero: what kind of thing an affordance is
- Links: Stoffregen 2003, Ecological Psychology 15(2):115-134, DOI 10.1207/S15326969ECO1502_2 (abstract seen via search results only, https://experts.umn.edu/en/publications/affordances-as-properties-of-the-animal-environment-system/, not fetched, **UNVERIFIED**); Chemero 2003 "An Outline of a Theory of Affordances", Ecological Psychology (cited on https://en.wikipedia.org/wiki/Affordance, not read); Turvey 1992 (cited in Beßler et al., link in A4, not read).
- Version: 2003 articles; no edition number.
- Covers: the dispute, as reported in A4's text: whether an affordance is a property of the animal-environment system (Stoffregen), a relation (Chemero), or a disposition (Turvey). Beßler et al. adopt the disposition-description reading (A4). This unit did not read the three papers; do not cite them for more than their existence and thesis titles.
- Note: informs a design choice (relation vs property), but ontology authors in practice take one stance; see A4.

### A4. Beßler et al., "A Formal Model of Affordances for Flexible Robotic Task Execution" (ECAI 2020) and the EASE ontology
- Link: https://ai.uni-bremen.de/papers/bessler20affordances.pdf (fetched, text extracted) ; ontology https://raw.githubusercontent.com/knowrob/ease_ontology/ecai2020/owl/EASE-OBJ.owl (fetched; repo https://github.com/knowrob/ease_ontology).
- Version: ECAI 2020 (the ontology URL is tagged branch `ecai2020`; the PDF's year is inferred from that tag and the figure path "20-ECAI-affordance", not a stated date). Ontology IRI http://www.ease-crc.org/ont/EASE-OBJ.owl, no `owl:versionInfo`.
- Covers: Affordance as a formal class. Paper: "Definition 2 An affordance is the description of a disposition." Also: "an affordance is not a property of the environment but rather describes how an agent may make use of some property of the environment by executing the task that is defined by the affordance." Abstract: "implemented as a TBox OWL ontology of affordances based on the DOLCE Ultra Light + DnS foundational ontology."
- Class: `http://www.ease-crc.org/ont/EASE-OBJ.owl#Affordance`, `rdfs:subClassOf` `DUL.owl#Relation` and restricted to describe a `Disposition`. Stance: robot agent, physics-simulated validation; heavy (DOLCE, Disposition, Role, Task, Situation).
- Note: the one published OWL affordance class this unit found with a definition; wrong weight and wrong agent (robot) for a note-taker. Other robotics affordance ontologies surfaced by search (OntOGrasp, ABO, an arXiv 2606.00117 navigation paper) were not opened and are not cited beyond this mention.

### A5. W3C Web of Things Thing Description, InteractionAffordance
- Link: https://www.w3.org/TR/wot-thing-description11/ ; vocabulary https://www.w3.org/2019/wot/td
- Version: W3C Recommendation 5 December 2023 (TD 1.1); the Turtle vocabulary file carries `owl:versionInfo "0.9.0"`.
- Covers: Affordance as metadata of a thing for software consumers. Class `https://www.w3.org/2019/wot/td#InteractionAffordance` (a `td:` namespace term): "Metadata of a Thing that shows the possible choices to Consumers, thereby suggesting how Consumers may interact with the Thing. There are many types of potential affordances, but W3C WoT defines three types of Interaction Affordances: Properties, Actions, and Events." Relation `td:hasInteractionAffordance`: "Offers an affordance to interact with the Thing".
- Note: the closest published Thing-offers-Affordance shape (technology = Thing, affordance = what it offers). Its consumers are machines and its subtypes (Property, Action, Event) are protocol interactions; a human note-taker would not use the subtypes. Namespace prefix expansion here is this unit's reading of the file, not an IRI printed in the spec text.

### A6. schema.org potentialAction
- Link: https://schema.org/potentialAction
- Version: V30.1, 2026-09-16 (development version page).
- Covers: partly. "Indicates a potential Action, which describes an idealized action in which this thing would play an 'object' role." The description of the `Action` type was not on the fetched page (**UNVERIFIED**).
- Note: an Action is an event-like instance, not a named kind of possibility; usable only as a looser anchor.

### A7. Quality-type sources, retained as comparison only
- SEBoK System Property, https://sebokwiki.org/wiki/System_Property_(glossary), SEBoK v2.14 (18 May 2026, per https://sebokwiki.org/wiki/Stakeholder_Needs_and_Requirements): "Any named, measurable or observable attribute, quality or characteristic of a system or system element." Cited there to OMG 2003, SE Conceptual Model Semantic Dictionary. Also Non-Functional Requirements, https://sebokwiki.org/wiki/Non-Functional_Requirements_(glossary): "Quality attributes or characteristics that are desired in a system, that define how a system is supposed to be."
- SOSA/SSN, https://www.w3.org/TR/vocab-ssn/ (W3C Recommendation 19 October 2017): `ssn:Property` http://www.w3.org/ns/ssn/Property, "A quality of an entity. An aspect of an entity that is intrinsic to and cannot exist without the entity."
- QUDT, https://qudt.org/doc/DOC_SCHEMA-QUDT.html, schema 3.5.4, `qudt:QuantityKind`: "A Quantity Kind is any observable property that can be measured and quantified numerically." (from https://qudt.org/3.5.4/schema/qudt).
- ISO/IEC 25010 on a secondary site, https://iso25000.com/index.php/en/iso-25000-standards/iso-25010 : the fetched page showed four of the characteristics (Functional Suitability, Performance Efficiency, Compatibility, Interaction Capability) and no edition; ISO's own page returned 403. It names qualities of software, as a value list, not as a class. No edition is claimed.
- i*/iStar (https://www.cs.toronto.edu/km/istar/; iStar 2.0 Language Guide, https://arxiv.org/abs/1605.07767, v3 16 June 2016): the softgoal, "draws on techniques for dealing with non-functional requirements in software engineering" (Toronto page). Element definitions not read, **UNVERIFIED**; KAOS not fetched, no link.
- Verdict for this element: these describe what a system *is like* (a quality), not what a user *can do with it*. They bear on the old Property element, and remain only as comparison options.

### A8. SKOS and concept-definition-stage patterns
- SKOS, https://www.w3.org/TR/skos-reference/, W3C Recommendation 18 August 2009: "The class skos:Concept is the class of SKOS concepts." `skos:related`: "The property skos:related is used to assert an associative link between two SKOS concepts." Mapping properties (`skos:exactMatch`, `skos:closeMatch`) are the lightweight anchor.
- concept-definition-stage (local, read-only), `/Users/z/Documents/GitHub/concept-definition-stage/ontology/cds-core.ttl` (`owl:versionInfo "0.1.0"`, last commit 4d1e52e, 2026-06-28) and `/Users/z/Documents/GitHub/concept-definition-stage/ontology/concept-definition.ttl`: SEBoK terms as `skos:Concept` with `skos:exactMatch` to the glossary URL; `owl:equivalentClass` between `https://www.omg.org/spec/SysML/20240801/SysML#PartDefinition` and `https://www.omg.org/spec/SysML/2.0/PartDefinition`. No affordance term; `cds:addresses` is typed over cds terms ("A concept addresses the problem / threat / opportunity it is defined for (GtWR).") and so is not reusable for Concern x Affordance (relations unit).

### A9. SysML v2, by reference
- https://www.omg.org/spec/SysML/2.0/ ; formal version 2.0, September 2025 (per that page). The fetched page does not mention AttributeUsage, AttributeDefinition or PartDefinition, and the spec body was not read. SysML has no "affordance" element that this unit found; any mapping is **UNVERIFIED**.

## Technology: candidates

### T-S1. ISO/IEC/IEEE 15288 system element, via SEBoK
- Link: https://sebokwiki.org/wiki/System_Element_(glossary) (ISO/IEC/IEEE 15288:2015 as cited there; ISO page not fetchable, 403).
- Version: 15288:2015 as quoted by SEBoK; SEBoK v2.14.
- "A system element is a discrete part of a system that can be implemented to fulfill specified requirements." and "A system element can be hardware, software, data, humans, processes (e.g., processes for providing service to users), procedures (e.g., operator instructions), facilities, materials, and naturally occurring entities (e.g., water, organisms, minerals), or any combination."
- Note: a parent notion, broader than technology (humans, materials).

### T-S2. SEBoK and NASA usage of "technology"
- SEBoK: no entry titled "Technology" in the Glossary of Terms listing (https://sebokwiki.org/wiki/Glossary_of_Terms, as the page was fetched). The glossary entry "Information Technology" exists, https://sebokwiki.org/wiki/Information_Technology_(glossary): "Resources required to acquire, process, store and disseminate information." (cited there to ISO/IEC 38500:2008, clause 1.6.7). That is narrower than ours (information only).
- NASA TRL page, https://www.nasa.gov/directorates/somd/space-communications-navigation-program/technology-readiness-levels/ (published 2023-09-27, updated 2026-06-25): "Technology Readiness Levels (TRL) are a type of measurement system used to assess the maturity level of a particular technology." It uses "technology" without defining it.

### T-S3. schema.org SoftwareApplication
- https://schema.org/SoftwareApplication ; V30.1, 2026-09-16 (development version). "A software application." Thing > CreativeWork > SoftwareApplication; 20+ fields (`applicationCategory`, `featureList`, `softwareVersion`, `operatingSystem` ...).

### T-S4. DOAP
- Vocabulary https://github.com/ewilderj/doap (the `usefulinc.com/ns/doap#` page failed on a certificate error; schema read from https://raw.githubusercontent.com/ewilderj/doap/master/schema/doap.rdf). No version in the schema file. `doap:Project`: "A project." (subclass of `foaf:Project`).

### T-S5. SysML v2 PartDefinition (by reference)
- https://www.omg.org/spec/SysML/2.0/ , 2.0 formal, Sept 2025. Used by concept-definition-stage as an equivalence anchor (A8). Mapping to Technology **UNVERIFIED** (spec body unread).

### T-S6. PROV-O and DCMI
- https://www.w3.org/TR/prov-o/ (W3C Recommendation 30 April 2013): `prov:Entity`, "An entity is a physical, digital, conceptual, or other kind of thing with some fixed aspects". https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ (issued 2020-01-20): `dcterms:requires`, "A related resource that is required by the described resource to support its function, delivery, or coherence." Provenance and metadata; relevant to the records unit.

## Gaps
- Gibson's 1979 text, Norman's definition of "signifier" in the 2013 book, and the Turvey, Stoffregen and Chemero papers were not read directly (see marks above).
- 42010 text (paywalled; ISO and iso-architecture.org fetches failed): Concern unit's source; it does not define affordance.
- SysML v2 spec body, KAOS and iStar 2.0 element definitions: not read.
- No existing source defines "technology" as a class (SEBoK has no entry titled Technology; NASA uses the word undefined). No source found for "tool" as an arrangement of technologies; not needed, since no tool class is added.
