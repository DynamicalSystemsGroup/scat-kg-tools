# WP1-U1 survey part: Stakeholder group and Concern

Partial file for `survey.md` (WP1-D1). It covers only the elements **Stakeholder group** and **Concern**, and the two
endpoints of **Heldby**. All sources were fetched on 2026-11-23. A quoted definition is verbatim from the fetched text
and is followed by its citation key. Other elements, and the starting points that serve only them (SOSA/SSN, QUDT,
event vocabularies, affordance sources), are for other units.

## Sources

| Key | Source (primary link) | Version / date as fetched | Fetched | Covers |
|---|---|---|---|---|
| ISO42010-site | ISO/IEC/IEEE 42010 community site, conceptual model page: <http://www.iso-architecture.org/ieee-1471/cm/>; home <http://www.iso-architecture.org/42010/> | The home page announces the second edition, ISO/IEC/IEEE 42010:2022. The conceptual-model page carries no edition stamp. | Yes | Stakeholder, Concern, Heldby endpoints |
| ISO42010 | The standard itself: <https://www.iso.org/standard/74393.html> | 42010:2022 (second edition) | **No: HTTP 403** (also the ISO browsing platform, 403) | Stakeholder, Concern |
| SEBoK-SH | SEBoK glossary, Stakeholder: <https://sebokwiki.org/wiki/Stakeholder_(glossary)> | Page last edited 18 September 2025 | Yes | Stakeholder |
| SEBoK-CO | SEBoK glossary, Concern: <https://sebokwiki.org/wiki/Concern_(glossary)> | n/a | **No such page: HTTP 404.** Architecture, Architecture Framework (<https://sebokwiki.org/wiki/Architecture_Framework_(glossary)>) and other glossary pages were fetched and give no definition of Concern | Concern (negative finding) |
| SEBoK-SNR | SEBoK, Stakeholder Needs and Requirements: <https://sebokwiki.org/wiki/Stakeholder_Needs_and_Requirements> | Page last edited as shown by the live page | Yes | Stakeholder |
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

## What each source says

### ISO/IEC/IEEE 42010 (stakeholders and concerns)

The standard is paywalled and unreachable (ISO42010 above). What was used instead is the standard's community site,
which is a secondary description and not the standard text. It describes the conceptual model in these words
(ISO42010-site):

> "Stakeholders are individuals, groups or organizations holding Concerns for the System of Interest."

> "A Concern is any interest in the system."

The site's text is written in the first-edition vocabulary ("System of Interest"), though its page also introduces the
second edition. The wording of the 2022 edition's own definitions was **not** verified. WP4 or the ACE should check
them against the standard before any definition is copied (D-012 requires adopted definitions to be used directly).

SEBoK carries the 42010 definition of **Stakeholder** (SEBoK-SH, entry 1, citing ISO/IEC/IEEE 2015):

> "Individual or organization having a right, share, claim, or interest in a system or in its possession of characteristics that meet their needs and expectations"

and a further entry (SEBoK-SH, entry 3, citing ISO/IEC 2007):

> "An individual, team, or organization (or classes thereof) with interests in, or concerns relative to, a system."

SEBoK has **no glossary entry for Concern** (SEBoK-CO, 404).

### concept-definition-stage

CDS already anchors the same definition (CDS, `cdsterm:stakeholder`): `cds:definitionSource "ISO/IEC/IEEE 2015"`,
`skos:definition` identical to the SEBoK entry 1 text above, and `skos:exactMatch
<https://sebokwiki.org/wiki/Stakeholder_(glossary)>`. This is the equivalence-axiom anchoring practice named in
`MISSION.md`. CDS has **no concern term**. Its only use of the word is inside the definition of `problem`: "A concern
that has a probability of occurrence equal to one, a consequence of occurrence greater than zero, and a time-frame that
is current." That is the risk-management sense and is not the 42010 sense. The CDS IRIs under `https://w3id.org/cds/`
were not dereferenced in this unit; whether they resolve is unverified.

### SKOS

SKOS (SKOS) defines `skos:Concept` (section 3): "A SKOS concept can be viewed as an idea or notion; a unit of thought."
It supplies `skos:related` ("used to assert an associative link between two SKOS concepts") and the mapping properties
`skos:exactMatch` ("used to link two concepts, indicating a high degree of confidence that the concepts can be used
interchangeably across a wide range of information retrieval applications") and `skos:closeMatch` ("used to link two
concepts that are sufficiently similar that they can be used interchangeably in some information retrieval
applications"). It also states that "skos:Collection is disjoint with each of skos:Concept and skos:ConceptScheme".

### PROV-O, Dublin Core, FOAF, ORG (agents and groups)

- PROV-O (PROV-O): "An agent is something that bears some form of responsibility for an activity taking place, for the
  existence of an entity, or for another agent's activity." Also `prov:Organization`: "An organization is a social or
  legal institution such as a company, society, etc." and `prov:Person`: "Person agents are people." The notion is
  responsibility for an activity, not having a stake.
- DCMI (DCMI): `dcterms:Agent`, "A resource that acts or has the power to act."; `dcterms:AgentClass`, "A group of
  agents."; and `dcterms:audience`, "A class of agents for whom the resource is intended or useful."
- FOAF (FOAF): `foaf:Group`, "The Group class represents a collection of individual agents (and may itself play the
  role of a Agent , ie. something that can perform actions). This concept is intentionally quite broad, covering
  informal and ad-hoc groups, long-lived communities, organizational groups within a workplace, etc." Also
  `foaf:interest` has range `Document` ("A page about a topic of interest to this person"), so it cannot link a group
  to a concern as a class instance.
- ORG (ORG): `org:Organization`, "Represents a collection of people organized together into a community or other social,
  commercial or political structure. The group has some common purpose or reason for existence which goes beyond the
  set of people belonging to it and can act as an Agent."

### iStar 2.0 (goal models)

From iStar (section 2): "Actors are active, autonomous entities that aim at achieving their goals by exercising their
know-how, in collaboration with other actors." Two types: "Role: an abstract characterization of the behavior of a
social actor within some specialized context or domain of endeavor." and "Agent: an actor with concrete, physical
manifestations, such as a human individual, an organization, or a department." From section 4: "Intentional elements
are the things actors want." with "Goal : a state of affairs that the actor wants to achieve and that has clear-cut
criteria of achievement." and "Quality: an attribute for which an actor desires some level of achievement."

### KAOS (goal models)

From KAOS (section 2, "What are goals?"): "A goal is an objective the system under consideration should achieve." The
paper's goal model has goal, agent, responsibility and conflict links ("a conflict link between two goals is
introduced when the satisfaction of one of them may prevent the other from being satisfied"). KAOS goals belong to the
system, not to a stakeholder, and the paper has no Concern class. The conflict link is relevant to WP1-G3 and is left
to the unit that covers disagreement.

### OSLC RM

The OSLC RM 2.1 specification describes requirements as "the basis for defining what the system stakeholders (users,
customers, suppliers and so on) need from a system" (OSLC-RM, section 1.1). The machine-readable vocabulary
(`requirements-management-vocab.ttl`) contains **zero** occurrences of "stakeholder" or "concern" (checked by
`grep -i -c`). OSLC RM offers no class for either element.

### SysML v2 (by reference only)

SysML2, requirements clause: "A stakeholder parameter represents a role played by an entity (usually a person,
organization or other group) having concerns related to the containing requirement." "A concern definition is a kind
of requirement definition that represents a stakeholder concern." "The stakeholder parameters of a concern definition
or usage then delineate the stakeholders that have a certain concern." SysML v2 therefore models Concern as a kind of
requirement and holding as a stakeholder parameter, which is heavier than the SCAT meaning.

## Coverage

| Source | Stakeholder group | Concern | Heldby endpoints |
|---|---|---|---|
| ISO42010 / ISO42010-site | Yes | Yes | Yes ("holding Concerns") |
| SEBoK | Yes (SH, SNR) | **No entry** | No |
| CDS | Yes | No (risk sense only) | No |
| SKOS | Scaffolding | Scaffolding | `skos:related` (untyped) |
| PROV-O | Agent only | No | No |
| DCMI | AgentClass, Agent | No | `dcterms:audience` (resource to agent class: wrong shape) |
| FOAF / ORG | Group, Organization | No | `foaf:interest` (range Document: wrong shape) |
| iStar 2.0 | Actor, Role, Agent | Goal, Quality | Actor boundary (containment) |
| KAOS | Agent | Goal | Responsibility link (goal to agent: different meaning) |
| OSLC RM | No | No | No |
| SysML v2 | Stakeholder parameter | ConcernDefinition | Stakeholder parameter of a concern |
