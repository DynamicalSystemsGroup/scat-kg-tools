# U1 survey: Stakeholder group and Concern

Unit WP1-U1. Cluster: STAKEHOLDER GROUP and CONCERN. Fetch date for every link: 2026-11-23.
Quotes are verbatim from the page named. "Primary" means the spec or standard text itself; "secondary" means a page quoting it.

Intended meaning (from `MISSION.md` Purpose, G1, G10; `decisions/log.md` D-003, D-010, D-013): a **Stakeholder group** is a
class of people with a shared stake, recorded as a group so no individual is identifiable (Chatham House). A **Concern** is
something such a group cares about, which a **Property** can address. Heldby is group x concern.

## Access limits (read first)

- ISO/IEC/IEEE 42010 (2011 and 2022) is paywalled. `https://www.iso.org/standard/50508.html` and `.../74393.html` return HTTP 403,
  and `iso-architecture.org` (the 42010 community site) refused connection from this host. **No 42010 definition below is
  verified verbatim from the standard.** Where 42010 wording is given, it is labelled secondary and unverified.
- The SEBoK has no glossary page for "Concern" (`https://sebokwiki.org/wiki/Concern_(glossary)` returned HTTP 404).
- KAOS: no primary source reached; entry is secondary only.

## A. Candidates for STAKEHOLDER GROUP

### A1. SEBoK v2.14 glossary, "Stakeholder" (already in concept-definition-stage)
- Link: https://sebokwiki.org/wiki/Stakeholder_(glossary) . Version: SEBoK v2.14 (the version `cdsterm:stakeholder` cites).
- Covers: the notion of stakeholder, with four sourced definitions. Does not define a group class.
- Verbatim, ISO/IEC/IEEE 15288:2015: "Individual or organization having a right, share, claim, or interest in a system or in its possession of characteristics that meet their needs and expectations".
- Verbatim, ISO/IEC 26702:2007: "An individual, team, or organization (or classes thereof) with interests in, or concerns relative to, a system."
- Verbatim, Freeman (1984): "A stakeholder in an organisation is (by definition) any group or individual who can affect or is affected by the achievement of the organisation's objectives."
- Note: the 26702 and Freeman wordings already admit groups ("team", "classes thereof", "any group"). 15288 names individual or organization only.
- Companion: https://sebokwiki.org/wiki/Stakeholder_Needs_and_Requirements (v2.14, 18 May 2026): "classes of stakeholders across the life cycle"; no phrase "stakeholder group".

### A2. concept-definition-stage `cdsterm:stakeholder` (local pattern, read-only)
- Path: `/Users/z/Documents/GitHub/concept-definition-stage/ontology/concept-definition.ttl`, term `cdsterm:stakeholder` (no release tag; repo HEAD read 2026-11-23).
- Pattern: `a cds:Term, skos:Concept ; cds:cites <https://w3id.org/cds/src/sebok-v2-14> ; cds:definitionSource "ISO/IEC/IEEE 2015" ; skos:definition "<verbatim>" ; skos:exactMatch <https://sebokwiki.org/wiki/Stakeholder_(glossary)> ; skos:inScheme ... ; skos:prefLabel "Stakeholder"`.
- Covers: Stakeholder as a SKOS concept anchored to SEBoK by `skos:exactMatch`. It is a vocabulary entry, not an OWL class of people. The file also uses `skos:closeMatch`, `skos:relatedMatch` and `skos:broadMatch` where the fit is weaker.

### A3. ISO/IEC/IEEE 42010 (stakeholder) -- UNVERIFIED, standard not reachable
- Link: https://www.iso.org/standard/74393.html (2022 edition, 403 from this host). Editions per https://en.wikipedia.org/wiki/ISO/IEC_42010 : 2022 current, 2011 deprecated, 2007 identical to IEEE 1471:2000.
- Covers: Stakeholder as an architecture-description element; no OWL or RDF vocabulary is published by ISO that I could find.
- Verbatim (secondary), IEEE 1471-2000 via https://en.wikipedia.org/wiki/IEEE_1471 , citing IEEE Std 610.12-1990: "An individual, team, or organization (or classes thereof) with interests in, or concerns relative to, a system."
- Paraphrase only (web-search summary, not verbatim, not verified): 2011 edition "individual, team, organization, or classes thereof having an interest in a system"; 2022 adds "right, share, or claim".

### A4. PROV-O (W3C Recommendation, 30 April 2013)
- Link: https://www.w3.org/TR/prov-o/ . IRIs `http://www.w3.org/ns/prov#Agent`, `#Organization`, `#Person`, `#Collection`, `#hadMember`.
- Verbatim: "An agent is something that bears some form of responsibility for an activity taking place" (continues in the spec).
- Verbatim: "An organization is a social or legal institution such as a company, society, etc."
- Verbatim: "Person agents are people."
- Verbatim: "A collection is an entity that provides a structure to some constituents, which are themselves entities."
- Covers: agents of provenance. There is no group-of-persons agent class. `prov:Person` is individuals, which we must not model; `prov:Organization` is an institution, narrower than "a class of people with a shared stake".

### A5. W3C Organization Ontology, ORG (W3C Recommendation, 16 January 2014)
- Link: https://www.w3.org/TR/vocab-org/ . IRIs under `http://www.w3.org/ns/org#`.
- Verbatim: "Represents a collection of people organized together into a community or other social, commercial or political structure." (`org:Organization`; the same entry adds "The group has some common purpose or reason for existence".)
- Verbatim: "An Organization such as a department or support unit which is part of some larger Organization." (`org:OrganizationalUnit`)
- Verbatim: "Denotes a role that a Person or other Agent can take in an organization." (`org:Role`)
- Covers: organisations, units, posts, membership. Built around identifiable members and posts; a stakeholder group is not necessarily organised.

### A6. Dublin Core Terms (DCMI Recommendation, 2020-01-20)
- Link: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ . IRIs `http://purl.org/dc/terms/AgentClass`, `#Agent`, `#audience`.
- Verbatim: "A group of agents." (`dcterms:AgentClass`)
- Verbatim: "A resource that acts or has the power to act." (`dcterms:Agent`)
- Verbatim: "A class of agents for whom the resource is intended or useful." (`dcterms:audience`)
- Covers: the only published, stable IRI I found whose definition is literally a group of agents. It carries no notion of stake or interest.

### A7. SKOS (W3C Recommendation, 18 August 2009)
- Link: https://www.w3.org/TR/skos-reference/ . IRIs under `http://www.w3.org/2004/02/skos/core#`.
- Verbatim: "SKOS concept collections are labeled and/or ordered groups of SKOS concepts." (`skos:Collection`)
- Verbatim: "...indicating a high degree of confidence that the concepts can be used interchangeably..." (`skos:exactMatch`, section 10.1, partial quote of the sentence)
- Covers: grouping of *concepts*, not people. Relevant only as the spine and the match properties, not as the class.

### A8. iStar 2.0 (language guide, arXiv:1605.07767v3, 16 Jun 2016)
- Link: https://arxiv.org/pdf/1605.07767v3 (section 2, read from the PDF text).
- Verbatim: "Actors are active, autonomous entities that aim at achieving their goals by exercising their know-how, in collaboration with other actors."
- Verbatim: "Role: an abstract characterization of the behavior of a social actor within some specialized context or domain of endeavor."
- Verbatim: "Agent: an actor with concrete, physical manifestations, such as a human individual, an organization, or a department."
- Covers: actors with intentions; Role is the abstract kind. It has no "Stakeholder" element.

### A9. SysML v2 (by reference), via the OSLC SysML 2.0 vocabulary
- Link: https://docs.oasis-open-projects.org/oslc-op/sysml/v2.0/sysml-vocab.html . Version: OSLC SysML 2.0 Part 2 Vocabulary, Project Specification Draft 01, 25 April 2024 (the OMG spec itself, https://www.omg.org/spec/SysML/2.0/Language/PDF, was not read).
- Verbatim: "A StakeholderMembership is a ParameterMembership that identifies a PartUsage as a stakeholderParameter" (continues: it "specifies a role played by an entity with concerns framed by the owningType").
- Covers: stakeholder as a role-bearing part in a concern or requirement model element. A modelling-language construct, not a class of real-world groups.

### A10. OSLC RM 2.1 (OASIS Standard, 21 June 2021)
- Link: https://docs.oasis-open-projects.org/oslc-op/rm/v2.1/os/requirements-management-spec.html
- Defines no Stakeholder or Concern resource. Only prose: "Requirements are the basis for defining what the system stakeholders (users, customers, suppliers and so on) need". Not a candidate; recorded for coverage.

## B. Candidates for CONCERN

### B1. ISO/IEC/IEEE 42010 (concern) -- UNVERIFIED, standard not reachable
- Link: https://www.iso.org/standard/74393.html (2022; 403). A hosted copy of the 2011 text (`https://cs.uns.edu.ar/~mc/disenio/downloads/Otro%20Material/iso-iec-ieee-42010-2011.pdf`) refused connection and was not read.
- Verbatim (secondary), IEEE 1471-2000 per https://en.wikipedia.org/wiki/IEEE_1471 : concerns are "those interests which pertain to the system's development, its operation" and other aspects important to one or more stakeholders (page lists performance, reliability, security, distribution, evolvability). Wikipedia's paraphrase; not the standard's own sentence.
- Paraphrase (web-search summary, unverified): 2011 "interest in a system relevant to one or more of its stakeholders"; 2022 "matter of relevance or importance regarding an entity of interest to a stakeholder".
- Covers: Concern held by Stakeholder, framed by Viewpoint, addressed in Views. Closest semantic match to our meaning; not published as an RDF IRI that I could find.

### B2. SEBoK v2.14
- No glossary entry for Concern (404 at `https://sebokwiki.org/wiki/Concern_(glossary)`). The only use in the stakeholder glossary page is inside the ISO/IEC 26702 definition quoted in A1 ("interests in, or concerns relative to, a system").
- concept-definition-stage uses "concern" only inside the *Problem* definition (Conrow 2008): "A concern that has a probability of occurrence equal to one, a consequence of occurrence greater than zero, and a time-frame that is current." (`cdsterm:problem`, `concept-definition.ttl`). That is risk-management usage; it conflicts with our meaning and should not be imported.

### B3. SysML v2 `ConcernDefinition` / `ConcernUsage` (by reference)
- Link: https://docs.oasis-open-projects.org/oslc-op/sysml/v2.0/sysml-vocab.html (OSLC SysML 2.0 Vocabulary, Draft 01, 25 April 2024).
- Verbatim: "A ConcernDefinition is a RequirementDefinition that one or more stakeholders may be interested in having addressed."
- Verbatim: "A ConcernUsage is a Usage of a ConcernDefinition."
- Covers: Concern modelled as a kind of requirement, with owned stakeholders. A published vocabulary exists, but the term is a subclass of RequirementDefinition and pulls in the KerML type machinery.

### B4. SKOS `skos:Concept` (W3C Recommendation, 2009)
- Link: https://www.w3.org/TR/skos-reference/ . Verbatim: "The class skos:Concept is the class of SKOS concepts."
- Covers: a generic idea in a scheme. Fits a concern only as "a thing named in a vocabulary"; says nothing about being held by anyone.

### B5. Dublin Core `dcterms:subject`
- Link: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ . Verbatim: "A topic of the resource."
- Covers: a topic a resource is about. A property, not a class; no notion of stake.

### B6. iStar 2.0 Goal and Quality
- Link: https://arxiv.org/pdf/1605.07767v3 (section 4). Verbatim: "Goal : a state of affairs that the actor wants to achieve and that has clear-cut criteria of achievement." and "Quality: an attribute for which an actor desires some level of achievement."
- Covers: intentions of an actor. A concern is a looser "matter of interest", often without clear-cut criteria; Quality is closer to our Property. Not a fit for Concern.

### B7. KAOS (secondary only)
- Source found: https://webperso.info.ucl.ac.be/~avl/files/avl-MontereyLNCS.pdf and a search summary. The summary says a goal is an objective the system should achieve; an agent is an "active object". Primary text not read; no verbatim quote taken. Same fit verdict as iStar: goals, not concerns.

### B8. OSLC RM 2.1
- No Concern resource (see A10). Not a candidate.

## C. concept-definition-stage patterns that carry over

Read in `/Users/z/Documents/GitHub/concept-definition-stage/ontology/`:
- SKOS+PROV spine: `skos:Concept`, `skos:inScheme`, `prov:` and `dcterms:` prefixes (`cds-core.ttl`).
- Authority trace per term: `cds:cites`, `cds:definitionSource`.
- Equivalence axiom pattern: `skos:exactMatch`, `skos:closeMatch`, `skos:broadMatch`, `skos:relatedMatch` to external pages (SEBoK glossary pages, SysML IRIs) instead of imports. Terms are recorded with the strength of the match, which is the honest way to say "partly fits".
