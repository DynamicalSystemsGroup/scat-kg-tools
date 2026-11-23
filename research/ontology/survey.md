# WP1-D1: Ontology survey

Every candidate vocabulary and source for the SCAT elements, with link, version and the elements it covers. Assembled
2026-11-23 from three part files (kept under `parts/`) and checked as set out in the link log below. Quotes are verbatim
from the fetched text. Where a primary source could not be reached, the entry says so and says what was used instead
(WP1-R1).

Elements (MISSION G1): Stakeholder group, Concern, Affordance, Technology; Heldby, Addresses, Attributes; the scenario
record; the architecture record; page status and provenance. Disagreement options (WP1-G3) are surveyed with the
relations.

## 1. Coverage of the WP1-G1 starting points

| Starting point | Primary link | Version as fetched | Elements it covers | Reached? | Detail in |
|---|---|---|---|---|---|
| ISO/IEC/IEEE 42010 | <https://www.iso.org/standard/74393.html>; community site <http://www.iso-architecture.org/42010/cm/> and <http://www.iso-architecture.org/ieee-1471/cm/> | 42010:2022 (2nd ed.); the community pages mix 1st-edition wording with 2nd-edition notes | Stakeholder group, Concern, Heldby, architecture record | Standard: no, HTTP 403 (re-tried in WP1-U4, 403). Community site: yes | A.1, C |
| SEBoK / INCOSE canon | <https://sebokwiki.org/wiki/Stakeholder_(glossary)>, <https://sebokwiki.org/wiki/System_Element_(glossary)>, <https://sebokwiki.org/wiki/Capability_(glossary)> | SEBoK v2.14 (18 May 2026); text from ISO/IEC/IEEE 15288:2015. No Concern entry (HTTP 404) and no Technology entry (HTTP 404) | Stakeholder group, Technology, Affordance (Capability) | Yes | A.1, B |
| `concept-definition-stage` patterns | <https://github.com/Open-MBEE/concept-definition-stage> | commit `99cecd1d36c7ffd4af540773b0907b59a122c65d` (2026-07-25); package 0.1.0; no tags | Stakeholder group; Addresses; Tension (disagreement); SKOS+PROV spine | Yes | A.1, B, C |
| SKOS | <https://www.w3.org/TR/skos-reference/> | W3C Rec 2009-08-18 | carrier for Concern and all definitions; mapping properties | Yes | A.1 |
| PROV-O | <https://www.w3.org/TR/prov-o/> | W3C Rec 2013-04-30 | provenance; scenario (influence); Heldby (rejected) | Yes | A.1, C |
| Dublin Core | <https://www.dublincore.org/specifications/dublin-core/dcmi-terms/> | DCMI Metadata Terms, issued 2020-01-20 | architecture parts (`hasPart`), provenance (`source`), AgentClass | Yes | A.1, C |
| SOSA/SSN | <https://www.w3.org/TR/vocab-ssn/> | W3C Rec 2017-10-19 | Technology (Platform, System); Attributes and architecture (rejected) | Yes | B, C |
| QUDT | <https://www.qudt.org/> | page shows "Release 2.1", labelled old; no current number | none: no element carries a quantity in G1 | Yes | B |
| iStar | <https://arxiv.org/abs/1605.07767> | iStar 2.0 Language Guide, arXiv v3, 2016-06-16 | Stakeholder group (actor, role), Concern (goal), Addresses (contribution), disagreement | Yes | A.1, C |
| KAOS | <https://webperso.info.ucl.ac.be/~avl/files/RE01.pdf> | van Lamsweerde, RE'01 (2001), author's copy | Concern (goal), disagreement (conflict link) | Yes (WP1-U1; re-fetched in WP1-U4) | A.1, C |
| OSLC RM | <https://docs.oasis-open-projects.org/oslc-op/rm/v2.1/os/requirements-management-vocab.html> | OASIS Standard 2.1, 2021-06-21 | none for Stakeholder or Concern (no such term); Addresses (`rm:satisfies`, rejected) | Yes | A.1, C |
| SysML v2 (by reference only) | <https://github.com/Systems-Modeling/SysML-v2-Release>; <https://www.omg.org/spec/SysML/2.0/> | Two versions were read: tag `2026-09.1` (published 2026-10-30, document stamp "Version 2.1 Beta 2") in Part A, and formal/2026-03-02 (SysML 2.0) in Part B. The clauses cited are the same constructs; neither is a published ontology (no OWL) | Concern, Stakeholder (parameters), Technology (PartDefinition), architecture record | Yes | A.1, B, C |
| Affordance sources | Gibson 1979 (via Toyoshima, <https://ceur-ws.org/Vol-2205/paper20_caos3.pdf>); Norman <https://jnd.org/affordances-and-design/>; Maier and Fadel <https://doi.org/10.1007/s00163-008-0060-3>; Toyoshima et al. <https://doi.org/10.3233/AO-220267> | Gibson 1979 (Houghton Mifflin; Routledge 2014); Toyoshima 2017 CEUR Vol-2205; Norman 2008-11-17; Toyoshima 2022 | Affordance | Gibson: scan image-only, so read through Toyoshima's verbatim quotation, re-verified in WP1-U4. Toyoshima 2022 and Maier and Fadel: bibliographic records only | B |
| Event and causal-chain vocabularies | SEM <https://semanticweb.cs.vu.nl/2009/11/sem/>; RO <http://purl.obolibrary.org/obo/ro.owl>; OWL-Time <https://www.w3.org/TR/owl-time/>; `schema:Event` <https://schema.org/Event> | SEM 2009-11; RO 2026-09-04; OWL-Time Candidate Rec draft 2022-11-15; schema.org v30.1 | scenario record | SEM, RO, OWL-Time, schema.org: yes. Event Ontology (HTTP 403), LODE (404, re-tried 404), CIDOC CRM (404), AIF (unreachable): no, and not assessed | C |

Added by the units, beyond the starting points: FOAF, ORG, W3C WoT Thing Description, SAREF, BFO 2020, OWL 2, SHACL,
RDF 1.1, PAV, ADMS, `vs:term_status`, schema.org `creativeWorkStatus`, nanopublications, and `ant-rdf`. All are in the
parts below with link and version.

## 2. Where the parts overlapped or disagreed (WP1-U4 reconciliation)

- **KAOS.** Part C lists KAOS as "not fetched"; Part A fetched it from the author's open copy. Part A stands, and Part C's
  row is corrected. The conflict-link sentence was re-read in WP1-U4: "a conflict link between two goals is introduced
  when the satisfaction of one of them may prevent the other from being satisfied".
- **Concern wording.** It comes only from the 42010 community site. The 2022 standard is unreachable (HTTP 403, tried
  again). The community page was re-read in WP1-U4: its Stakeholder and Concern text ("Stakeholders are individuals,
  groups or organizations holding Concerns for the System of Interest."; "A Concern is any interest in the system.") sits
  beside a note that the 2nd edition (2022) introduces Stakeholder Perspectives, so it is first-edition wording that the
  page still carries. Whether the 2022 text is the same was **not** verified. SEBoK has no Concern entry.
- **Two different standards stand behind Stakeholder and Concern.** The Stakeholder definition adopted is the
  ISO/IEC/IEEE 15288:2015 text (via SEBoK). It names "individual or organization", not groups. The 42010 community
  site names groups. The class label "Stakeholder group" is our usage.
- **Affordance and Attributes.** Part B defines Affordance by Gibson's relational wording and rejects the disposition
  formalisations on cost. Part C's runner-up for Attributes (RO `has disposition`) fits only if Affordance is a
  disposition. The trade study resolves this (section on Attributes).
- **SysML v2 versions.** See the table row above; both read, neither published as OWL.
- **Source keys** (S1, S2 ...) are local to each part. Parts A and C use their own keys; Part B uses S1 to S23.
- **Small defects fixed in the parts:** FOAF quote spacing; schema.org release date (2026-09-16 per the page footer);
  KAOS row; `creativeWorkStatus` is typed for CreativeWork.

## 3. Link log (WP1-R1), WP1-U4 re-fetch on 2026-11-23

| # | Link | Result |
|---|---|---|
| 1 | <http://www.iso-architecture.org/42010/cm/> | 200. Stakeholder and Concern text confirmed verbatim; 2nd-edition note present |
| 2 | <http://www.iso-architecture.org/ieee-1471/cm/> | 200. Same two sentences |
| 3 | <https://www.iso.org/standard/74393.html> | 403, not reachable |
| 4 | <https://schema.org/creativeWorkStatus> | OK. "Used on" CreativeWork; expected DefinedTerm and Text; footer "V30.1 \| 2026-09-16" |
| 5 | <http://xmlns.com/foaf/spec/> | OK. Phrase "(and may itself play the role of a Agent, ie. something that can perform actions)" confirmed |
| 6 | <https://sebokwiki.org/wiki/Stakeholder_(glossary)> | OK. Four definitions, entry 1 from ISO/IEC/IEEE 15288:2015, entry 3 from ISO/IEC 26702:2007 confirmed |
| 7 | <https://sebokwiki.org/wiki/System_Element_(glossary)> | OK. "A system element is a discrete part of a system that can be implemented to fulfill specified requirements." confirmed |
| 8 | <https://sebokwiki.org/wiki/Concern_(glossary)> | 404, confirmed no entry |
| 9 | <https://webperso.info.ucl.ac.be/~avl/files/RE01.pdf> | OK (PDF, read with pdftotext). "A goal is an objective the system under consideration should" and the conflict-link sentence confirmed |
| 10 | <https://www.w3.org/TR/prov-o/> | OK. `http://www.w3.org/ns/prov#wasDerivedFrom`; "A derivation is a transformation of an entity into another" confirmed |
| 11 | <https://www.dublincore.org/specifications/dublin-core/dcmi-terms/> | OK. `http://purl.org/dc/terms/hasPart` and definition confirmed |
| 12 | <https://www.w3.org/TR/2023/REC-wot-thing-description11-20231205/> | OK. InteractionAffordance definition confirmed |
| 13 | <https://ceur-ws.org/Vol-2205/paper20_caos3.pdf> | OK (PDF). Gibson quotation "[1, p. 119]" confirmed |
| 14 | <https://semanticweb.cs.vu.nl/2009/11/sem/> | OK. "Events are things that happen."; View and accordingTo sentences confirmed |
| 15 | <https://jnd.org/affordances-and-design/> | 200. "To Gibson, affordances are a relationship." confirmed |
| 16 | <https://raw.githubusercontent.com/Open-MBEE/concept-definition-stage/99cecd1d36c7ffd4af540773b0907b59a122c65d/src/cds/ontology/cds-core.ttl> | 200. `cds:addresses` with comment and `rdfs:domain cds:Term` confirmed |
| 17 | <https://www.w3.org/TR/skos-reference/>, <https://docs.oasis-open-projects.org/oslc-op/rm/v2.1/os/requirements-management-vocab.html>, <https://www.qudt.org/>, <https://github.com/Open-MBEE/concept-definition-stage>, <https://www.w3.org/TR/vocab-ssn/> | 200 each (reachability only) |
| 18 | <http://linkedevents.org/ontology/> | 404 again |

Not re-fetched in WP1-U4 (stand on the unit's own fetch): RO, OWL-Time, BFO, SAREF, PAV, ADMS, nanopublications,
`ant-rdf`, OWL 2, SHACL, iStar, SysML v2, ORG, DCMI audience.

# Part A: Stakeholder group and Concern (WP1-U1)

### Sources

| Key | Source (primary link) | Version / date as fetched | Fetched | Covers |
|---|---|---|---|---|
| ISO42010-site | ISO/IEC/IEEE 42010 community site, conceptual model page: <http://www.iso-architecture.org/ieee-1471/cm/>; home <http://www.iso-architecture.org/42010/> | The home page announces the second edition, ISO/IEC/IEEE 42010:2022. The conceptual-model page carries no edition stamp. | Yes | Stakeholder, Concern, Heldby endpoints |
| ISO42010 | The standard itself: <https://www.iso.org/standard/74393.html> | 42010:2022 (second edition) | **No: HTTP 403** (also the ISO browsing platform, 403) | Stakeholder, Concern |
| SEBoK-SH | SEBoK glossary, Stakeholder: <https://sebokwiki.org/wiki/Stakeholder_(glossary)> | Page last edited 18 September 2025 | Yes | Stakeholder |
| SEBoK-CO | SEBoK glossary, Concern: <https://sebokwiki.org/wiki/Concern_(glossary)> | n/a | **No such page: HTTP 404.** Architecture, Architecture Framework (<https://sebokwiki.org/wiki/Architecture_Framework_(glossary)>) and other glossary pages were fetched and give no definition of Concern | Concern (negative finding) |
| CDS | `concept-definition-stage`, <https://github.com/Open-MBEE/concept-definition-stage>, files `src/cds/ontology/concept-definition.ttl`, `cds-core.ttl`, `waivers.ttl` | Commit `99cecd1d36c7ffd4af540773b0907b59a122c65d` (2026-07-25); `pyproject.toml` version 0.1.0; vocabulary `owl:versionInfo "0.1.0"` | Yes (shallow clone) | Stakeholder; the SKOS+PROV spine |
| SKOS | SKOS Reference: <https://www.w3.org/TR/skos-reference/> | W3C Recommendation 18 August 2009 | Yes | Concern (scaffolding), both (anchoring properties) |
| PROV-O | PROV-O: <https://www.w3.org/TR/prov-o/> | W3C Recommendation 30 April 2013 | Yes | Stakeholder group (as agent) |
| DCMI | DCMI Metadata Terms: <https://www.dublincore.org/specifications/dublin-core/dcmi-terms/> | Page states Date Issued 2020-01-20 | Yes | Stakeholder group (AgentClass) |
| FOAF | FOAF Vocabulary Specification: <http://xmlns.com/foaf/spec/> | 0.99, 14 January 2014 (Paddington Edition) | Yes | Stakeholder group (Group) |
| ORG | The Organization Ontology: <https://www.w3.org/TR/vocab-org/> | W3C Recommendation 16 January 2014 | Yes | Stakeholder group (Organization) |
| iStar | iStar 2.0 Language Guide, Dalpiaz, Franch, Horkoff: <https://arxiv.org/abs/1605.07767> (PDF <https://arxiv.org/pdf/1605.07767>). The i* community landing page <https://www.cs.toronto.edu/km/istar/> was also fetched; it points to the literature and has no definitions | arXiv v3, 16 Jun 2016 | Yes | Stakeholder group (actor, role), Concern (goal, quality) |
| KAOS | van Lamsweerde, "Goal-Oriented Requirements Engineering: A Guided Tour", RE'01, Toronto, August 2001: <https://webperso.info.ucl.ac.be/~avl/files/RE01.pdf> (author's copy) | RE'01 paper, 10 pp. | Yes | Concern (goal), Stakeholder group (agent) |
| OSLC-RM | OSLC Requirements Management 2.1: spec <https://docs.oasis-open-projects.org/oslc-op/rm/v2.1/os/requirements-management-spec.html>, vocabulary <https://docs.oasis-open-projects.org/oslc-op/rm/v2.1/os/requirements-management-vocab.html>, machine-readable <https://docs.oasis-open-projects.org/oslc-op/rm/v2.1/os/requirements-management-vocab.ttl> | OASIS Standard, 21 June 2021 | Yes | Neither (negative finding) |
| SysML2 | OMG Systems Modeling Language v2, from the release repository <https://github.com/Systems-Modeling/SysML-v2-Release>, file `doc/2a-OMG_Systems_Modeling_Language.pdf` at tag `2026-09.1` (published 2026-10-30) | Document stamp "Version 2.1 Beta 2", August 2026. **By reference only** (WP1-G1) | Yes | Concern, Stakeholder |

### What each source says

#### ISO/IEC/IEEE 42010 (stakeholders and concerns)

The standard is paywalled and unreachable (ISO42010 above). What was used instead is the standard's community site,
which is a secondary description and not the standard text. It describes the conceptual model in these words
(ISO42010-site):

> "Stakeholders are individuals, groups or organizations holding Concerns for the System of Interest."

> "A Concern is any interest in the system."

The site's text is written in the first-edition vocabulary ("System of Interest"), though its page also introduces the
second edition. The wording of the 2022 edition's own definitions was **not** verified. WP4 or the ACE should check
them against the standard before any definition is copied (D-012 requires adopted definitions to be used directly).

SEBoK's glossary entry for **Stakeholder** (SEBoK-SH, entry 1) cites ISO/IEC/IEEE 15288:2015 (*System Life Cycle Processes*), not 42010. SEBoK's source list names 15288:2015 for entry 1, ISO/IEC CD 29148 (June 2010) for entry 2, ISO/IEC 26702:2007 for entry 3, and Freeman (1984) for entry 4. Entry 1 reads:

> "Individual or organization having a right, share, claim, or interest in a system or in its possession of characteristics that meet their needs and expectations"

and entry 3 (citing ISO/IEC 26702:2007):

> "An individual, team, or organization (or classes thereof) with interests in, or concerns relative to, a system."

SEBoK has **no glossary entry for Concern** (SEBoK-CO, 404).

#### concept-definition-stage

CDS already anchors the same definition as SEBoK entry 1, that is the 15288:2015 text (CDS, `cdsterm:stakeholder`): `cds:definitionSource "ISO/IEC/IEEE 2015"` (the year only; CDS does not name the standard number, and SEBoK's source list shows it is 15288),
`skos:definition` identical to the SEBoK entry 1 text above, and `skos:exactMatch
<https://sebokwiki.org/wiki/Stakeholder_(glossary)>`. This is the equivalence-axiom anchoring practice named in
`MISSION.md`. CDS has **no concern term**. Its only use of the word is inside the definition of `problem`: "A concern
that has a probability of occurrence equal to one, a consequence of occurrence greater than zero, and a time-frame that
is current." That is the risk-management sense and is not the 42010 sense. The CDS IRIs under `https://w3id.org/cds/`
were not dereferenced in this unit; whether they resolve is unverified.

#### SKOS

SKOS (SKOS) defines `skos:Concept` (section 3): "A SKOS concept can be viewed as an idea or notion; a unit of thought."
It supplies `skos:related` ("used to assert an associative link between two SKOS concepts") and the mapping properties
`skos:exactMatch` ("used to link two concepts, indicating a high degree of confidence that the concepts can be used
interchangeably across a wide range of information retrieval applications") and `skos:closeMatch` ("used to link two
concepts that are sufficiently similar that they can be used interchangeably in some information retrieval
applications"). It also states that "skos:Collection is disjoint with each of skos:Concept and skos:ConceptScheme".

#### PROV-O, Dublin Core, FOAF, ORG (agents and groups)

- PROV-O (PROV-O): "An agent is something that bears some form of responsibility for an activity taking place, for the
  existence of an entity, or for another agent's activity." Also `prov:Organization`: "An organization is a social or
  legal institution such as a company, society, etc." and `prov:Person`: "Person agents are people." The notion is
  responsibility for an activity, not having a stake.
- DCMI (DCMI): `dcterms:Agent`, "A resource that acts or has the power to act."; `dcterms:AgentClass`, "A group of
  agents."; and `dcterms:audience`, "A class of agents for whom the resource is intended or useful."
- FOAF (FOAF): `foaf:Group`, "The Group class represents a collection of individual agents (and may itself play the
  role of a Agent, ie. something that can perform actions). This concept is intentionally quite broad, covering
  informal and ad-hoc groups, long-lived communities, organizational groups within a workplace, etc." Also
  `foaf:interest` has range `Document` ("A page about a topic of interest to this person"), so it cannot link a group
  to a concern as a class instance.
- ORG (ORG): `org:Organization`, "Represents a collection of people organized together into a community or other social,
  commercial or political structure. The group has some common purpose or reason for existence which goes beyond the
  set of people belonging to it and can act as an Agent."

#### iStar 2.0 (goal models)

From iStar (section 2): "Actors are active, autonomous entities that aim at achieving their goals by exercising their
know-how, in collaboration with other actors." Two types: "Role: an abstract characterization of the behavior of a
social actor within some specialized context or domain of endeavor." and "Agent: an actor with concrete, physical
manifestations, such as a human individual, an organization, or a department." From section 4: "Intentional elements
are the things actors want." with "Goal : a state of affairs that the actor wants to achieve and that has clear-cut
criteria of achievement." and "Quality: an attribute for which an actor desires some level of achievement."

#### KAOS (goal models)

From KAOS (section 2, "What are goals?"): "A goal is an objective the system under consideration should achieve." The
paper's goal model has goal, agent, responsibility and conflict links ("a conflict link between two goals is
introduced when the satisfaction of one of them may prevent the other from being satisfied"). KAOS goals belong to the
system, not to a stakeholder, and the paper has no Concern class. The conflict link is relevant to WP1-G3 and is left
to the unit that covers disagreement.

#### OSLC RM

The OSLC RM 2.1 specification describes requirements as "the basis for defining what the system stakeholders (users,
customers, suppliers and so on) need from a system" (OSLC-RM, section 1.1). The machine-readable vocabulary
(`requirements-management-vocab.ttl`) contains **zero** occurrences of "stakeholder" or "concern" (checked by
`grep -i -c`). OSLC RM offers no class for either element.

#### SysML v2 (by reference only)

SysML2, requirements clause: "A stakeholder parameter represents a role played by an entity (usually a person,
organization or other group) having concerns related to the containing requirement." "A concern definition is a kind
of requirement definition that represents a stakeholder concern." "The stakeholder parameters of a concern definition
or usage then delineate the stakeholders that have a certain concern." SysML v2 therefore models Concern as a kind of
requirement and holding as a stakeholder parameter, which is heavier than the SCAT meaning.

### Coverage

| Source | Stakeholder group | Concern | Heldby endpoints |
|---|---|---|---|
| ISO42010 / ISO42010-site | Yes (community site only) | Yes (community site only) | Yes ("holding Concerns") |
| SEBoK | Yes (15288 text) | **No entry** | No |
| CDS | Yes | No (risk sense only) | No |
| SKOS | Scaffolding | Scaffolding | `skos:related` (untyped) |
| PROV-O | Agent only | No | No |
| DCMI | AgentClass, Agent | No | `dcterms:audience` (resource to agent class: wrong shape) |
| FOAF / ORG | Group, Organization | No | `foaf:interest` (range Document: wrong shape) |
| iStar 2.0 | Actor, Role, Agent | Goal, Quality | Actor boundary (containment) |
| KAOS | Agent | Goal | Responsibility link (goal to agent: different meaning) |
| OSLC RM | No | No | No |
| SysML v2 | Stakeholder parameter | ConcernDefinition | Stakeholder parameter of a concern |

# Part B: Affordance and Technology (WP1-U2)

### What the mission means by the two elements

- **Affordance** (Scenarios and architectures): technologies "stay relatively fixed and out of view, and what is
  legible is their **affordances**". Architectures assemble parts "into tools that provide affordances which address
  concerns". The relation Addresses is concern × affordance; Attributes is affordance × technology.
- **Technology** (same section): architectures "formulate assemblages: parts and wholes". Technologies are part of
  the action situation but not its focus.

### Source register (WP1-R5: link and version for each source)

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

### Findings by source

#### Affordance

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

#### Technology

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

### Coverage of the starting points, for these two elements

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

# Part C: Relations, records, status, provenance and disagreement (WP1-U3)

### Sources

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

### Findings per element (the evidence the trade tables use)

#### Heldby (stakeholder group x concern)
- S1: "Stakeholders are individuals, groups or organizations holding Concerns for the System of Interest." and "A Concern
  is any interest in the system." Concept only; no IRI is published.
- S13: "Goal: a state of affairs that the actor wants to achieve and that has clear-cut criteria of achievement." (an
  intentional element sits inside an actor's boundary). No IRI published in the guide.
- S2: `prov:wasAttributedTo`: "Attribution is the ascribing of an entity to an agent."
- S21: `cds:forStakeholder` links a need to a stakeholder (used in `verify.py`, `compile.py`); it is a link from a need,
  not from a concern, and `cds` publishes it only as a code-level link in the version fetched.

#### Addresses (concern x affordance)
- S21: `cds:addresses`, domain and range `cds:Term`: "A concept addresses the problem / threat / opportunity it is
  defined for (GtWR)."
- S14: `rm:satisfies`: "Expresses a relationship between entities, where the subject entity satisfies the object
  entity. For example, a system requirement satisfies a user requirement."
- S13: contribution links: "Help: The source provides weak positive evidence for the satisfaction of the target." and
  "Hurt: The source provides weak evidence against the satisfaction (or for the denial) of the target." Source: an
  intentional element; target: a quality.
- S1 (2nd edition note): "This 2nd edition introduces Stakeholder Perspectives as a means to group Concerns and
  therefore to organize Viewpoints framing those Concerns." Viewpoints frame concerns; they are not affordances.

#### Attributes (affordance x technology)
- S12: `RO_0000091` has disposition: "a relation between an independent continuant (the bearer) and a disposition, in
  which the disposition specifically depends on the bearer for its existence".
- S8: `ssn:System`: "System is a unit of abstraction for pieces of infrastructure that implement Procedures." The
  specification opens: "The Semantic Sensor Network (SSN) ontology is an ontology for describing sensors and their
  observations, the involved procedures, the studied features of interest, the samples used to do so, and the observed
  properties, as well as actuators."
- Affordance sources (Gibson and later) belong to the Affordance class unit; they were not fetched here.

#### Scenario record (behavioural)
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

#### Architecture record (structural)
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

#### Page status
- S16: `schema:creativeWorkStatus`: "The status of a creative work in terms of its stage in a lifecycle. Example terms
  include Incomplete, Draft, Published, Obsolete. Some organizations define a set of terms for the stages of their
  publication lifecycle." Values: DefinedTerm or Text.
- S15: `vs:term_status` values 'unstable', 'testing', 'stable', 'archaic'; "the value space for the property is
  open-ended". It labels vocabulary terms, not pages.
- S17: `adms:status`: "The status of the Asset in the context of a particular workflow process." Note retired Aug 2023.
- S18: PAV defines authorship and versioning (`pav:authoredBy`, `pav:previousVersion`), no status property was found.

#### Provenance
- S2: `prov:wasDerivedFrom`: "A derivation is a transformation of one entity into another." `prov:generatedAtTime`
  bounds an Entity's existence. `prov:wasAttributedTo` as above.
- S4: `dcterms:source`: "A related resource from which the described resource is derived." `dcterms:provenance`: "A
  statement of any changes in ownership and custody of the resource since its creation that are significant for its
  authenticity, integrity, and interpretation."
- S18: `pav:authoredBy`: "The author of the content of a resource may be different from the creator of the resource
  representation (although they are often the same)."

#### Disagreement and margins of conflict
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

### Unreachable or unread, and what was used instead

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
