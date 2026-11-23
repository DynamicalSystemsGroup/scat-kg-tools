# WP1-D2: Trade study

One trade table per element, each with at least two options, one of which is authoring our own (WP1-R2). A final
section covers options for holding disagreement (WP1-G3, WP1-R7). Assembled 2026-11-23 from three part files (kept under
`parts/`). Source keys (S1, C1 ...) are defined in `survey.md`, in the part that matches. WP1 recommends; WP4 decides.

## 1. Element checklist (WP1-R2, R8)

| Element | Table in | Options (incl. author our own) | Recommendation | Runner-up | Deciding criterion |
|---|---|---|---|---|---|
| Stakeholder group | Part A, Element 1 | S1 to S8 (S2 author) | Adopt SEBoK/15288:2015 Stakeholder definition; "group" is usage | S2, author `StakeholderGroup` | Recognisability |
| Concern | Part A, Element 2 | C1 to C8 (C2 author) | Adopt 42010 Concern wording on `skos:Concept` | C2, author | Recognisability |
| Affordance | Part B, Affordance | A1 to A7 (A1 author) | Author, Gibson's wording, map to WoT and Capability | A3, SEBoK Capability | Fit |
| Technology | Part B, Technology | T1 to T6 (T6 author) | Adopt SEBoK System Element definition | T2, SysML v2 PartDefinition | Maintenance, with fit |
| Heldby | Part C, section 1 (and Part A, Heldby endpoints) | A to D (A author) | Author `heldBy`; domain Stakeholder group, range Concern | B, `prov:wasAttributedTo` | Fit |
| Addresses | Part C, section 2 | A to E (A author) | Author | B, `cds:addresses` | Simplicity, independence |
| Attributes | Part C, section 3 | A to D (A author) | Author | B, RO `has disposition` (conditional, see 2) | Simplicity |
| Scenario record | Part C, section 4 | A to E (A author) | Author; events stay in the body | B, SEM | Simplicity under R4 |
| Architecture record | Part C, section 5 | A to E (A, E author) | Author class; `dcterms:hasPart` only if WP4 wants a part-whole link | C, `ssn:hasSubSystem` | Simplicity, recognisability |
| Page status | Part C, section 6 | A to E (B author) | Adopt `schema:creativeWorkStatus`, authored values | B, authored `status` | Adopt over mint at equal terms |
| Provenance | Part C, section 7 | A to E (E author) | Adopt `prov:wasDerivedFrom` | B, `dcterms:source` | Recognisability, fit |
| Disagreement | Part C, section 8 | D0 to D6 | D0 plus D1 plus D3 | D4 | Simplicity and UX cost |

## 2. Reconciliation across parts (WP1-U4)

- **Scales differ.** Part A rates High/Med/Low with a reason; Part B rates High/Med/Low; Part C uses + / 0 / -. All
  rate the same five criteria (fit, terms, recognisability, maintenance, cost) as judgment, not measurement.
- **Attributes runner-up depends on Affordance.** Part C's runner-up for Attributes is RO `has disposition`
  (RO_0000091, relation between a bearer and a disposition). That fits only if Affordance is defined as a disposition.
  Part B defines Affordance by Gibson's relational wording (what the environment "offers the animal") and rejects the
  disposition formalisation (A4, BFO-based) on cost to the note-taker. So under the joint recommendation
  Attributes has no live adoptable runner-up: authored `attributes` wins by default, and RO is the runner-up only in
  the case where WP4 reverses A4. The same holds if Part B's runner-up (A3, SEBoK Capability) is chosen: Capability is
  an outcome, not a disposition.
- **Technology and architecture overlap.** Technology is defined as a "discrete part of a system" (System Element).
  Parts and wholes between technologies would be `dcterms:hasPart` (Part C section 5). G1 lists no part-whole relation, so
  this is optional and WP4's call. It is not an added element.
- **Stakeholder and Concern come from two sources.** Stakeholder is the 15288:2015 text via SEBoK; Concern is the
  42010 community-site text. Both are definitions for authored-IRI classes. The Concern gap is the weaker one (single
  secondary source; 2022 text unverified). If it cannot be closed, Part A names the fallback: authored wording.
- **KAOS.** Part A fetched KAOS; Part C did not. The KAOS conflict link ("a conflict link between two goals is introduced
  when the satisfaction of one of them may prevent the other from being satisfied", van Lamsweerde, RE'01) is the
  nearest published form of option D1 in section 8. It relates goals, not concerns, and we cannot adopt it.
- **Heldby.** Part A types the endpoints (domain Stakeholder group, range Concern); Part C chooses the property
  (authored). The two are consistent. Both name H1/A as the recommendation.
- **No element beyond G1.** Every row above is a G1 element or a disagreement option with its cost.

# Part A: Stakeholder group and Concern (WP1-U1)

### Criteria (WP1-G2)

- **Fit:** match to the meaning in `MISSION.md`. A stakeholder group is a class of people who hold concerns, abstracted
  from any one architecture (Scenarios and architectures). A concern is something a group cares about, which several
  groups can share and which can oppose another concern (Facilitation stance; G1; G10).
- **Terms:** how many terms the TBox would carry, counting classes and properties we would actually use.
- **Recog:** recognisability to systems engineers.
- **Maint:** maintenance, meaning what we must keep up as the source changes, or definitions we must write ourselves.
- **Cost:** cost to the software and the UX, meaning extra frontmatter, validation or reading burden for note-takers.

Ratings are High, Med or Low, with the reason in the cell. "Author our own" is the baseline in every table.

### Element 1: Stakeholder group

| # | Option | Fit | Terms | Recog | Maint | Cost |
|---|---|---|---|---|---|---|
| S1 | **Adopt the SEBoK Stakeholder definition (ISO/IEC/IEEE 15288:2015, normative text)**, anchored by `skos:exactMatch` to the SEBoK glossary entry (the CDS practice). The 42010 community site's "individuals, groups or organizations holding Concerns" is secondary support, from a different source than the Concern text in C1. The class is labelled "Stakeholder group" and the vault uses it for groups only. | Med to High. The 15288 text says "Individual or organization" and does not mention groups. Groups are covered by SEBoK-SH entry 3 (ISO/IEC 26702:2007, "(or classes thereof)") and by the community site's "groups". "Group" is our usage convention. | 1 class | High. The term every SE already knows, and SEBoK is the canon named in G10. | Low. Definition is cited, not ours. The 15288:2015 text itself was reached only through SEBoK, not the standard. | Low. One class, one class page. |
| S2 | **Author our own** `StakeholderGroup`, defined by us, with `skos:closeMatch` to the SEBoK entry. | High. Exactly "a class of people with a stake". | 1 class | Med. The label is recognisable, the definition is new to them. | Med. We write and defend a definition (against D-012). | Low. |
| S3 | **iStar 2.0 Role** (with Actor and Agent). | Med. Role is "an abstract characterization of the behavior of a social actor" (iStar), close to a class of people. It brings the actor boundary, where intentional elements live inside the actor. | 2 to 3 classes (Actor, Role, Agent) | Med. Known to requirements engineers, less to systems engineers. | Med. Tracking an academic language guide. | Med. Invites goal-model structure the vault does not use. |
| S4 | **`dcterms:AgentClass`** ("A group of agents."). | Med. Right shape, a class of agents. Defined for audiences of resources. | 1 class | Low. Known to metadata people. | Low. Stable DCMI term. | Low. |
| S5 | **`foaf:Group`** or **`org:Organization`**. | Low. These enumerate named members, or model a formal organization with a purpose. SCAT groups are open categories ("note-takers"). | 1 class (plus member property if used) | Med. | Low. | Low to Med. Pulls toward listing members. |
| S6 | **`prov:Agent`** (with Organization, Person). | Low. Defined as bearing "responsibility for an activity". That says who did something, not who has a stake. | 1 to 3 classes | Med. | Low. | Low. |
| S7 | **SysML v2 stakeholder parameter** (by reference only). | Low. A role in a requirement, not a free-standing class. | n/a | High | n/a | Not usable. |
| S8 | **CDS `cdsterm:stakeholder`** (the same 15288:2015 text as S1, already published as SKOS). | High, same as S1. | 1 class | Med. | Med. Depends on a young 0.1.0 vocabulary whose IRIs were not dereferenced here. | Low. |

**Recommendation (S1):** Adopt the SEBoK Stakeholder definition (ISO/IEC/IEEE 15288:2015 text, which is the normative
source here; the 42010 community site is supporting only), anchored to the SEBoK entry by `skos:exactMatch`, and carry "group" as our usage, not as a new class.

**Runner-up:** S2, author our own `StakeholderGroup`.

**Deciding criterion:** recognisability, with maintenance behind it. Fit is close to level: the 15288 text omits groups,
but SEBoK entry 3 and the 42010 community site admit them, so authoring buys little meaning and costs a definition we would have to defend. S8
is the same text through a younger intermediary; S1 cites the SEBoK source directly (as CDS itself does).

**Flag:** the class name ("Stakeholder group") and the IRI minted for it are WP4's call. If WP4 prefers a distinct
class name, S2 with `skos:closeMatch` costs one extra class and no extra property.

### Element 2: Concern

| # | Option | Fit | Terms | Recog | Maint | Cost |
|---|---|---|---|---|---|---|
| C1 | **Adopt 42010 Concern**: term and definition "A Concern is any interest in the system." (ISO42010-site only; this is a different source from the Stakeholder text in S1, so the two definitions are not from one standard), modelled as a `skos:Concept` subclass so labels, definitions, `skos:related` and match properties come from SKOS. | High. "Any interest" is broad enough for anonymity, attribution, cost, and a concern can be shared by several groups. | 1 class (SKOS properties are reused, not new) | High. The 42010 term; SysML v2 uses it as well. | Low to Med. Source text is a secondary site, the 2022 standard text is unverified, and SEBoK has no entry to cite. WP4 must check the standard before copying a definition. | Low. |
| C2 | **Author our own** `Concern`, our definition, `skos:closeMatch` to 42010 if wished. | High. | 1 class | Med to High. The word is the same, the definition is ours. | Med. We own the definition, and we have no primary definition to cite. | Low. |
| C3 | **iStar Goal and Quality.** | Med. "Intentional elements are the things actors want." A concern need not be a wanted state ("cost" or "anonymity" is an interest, not an achievement). Goals have "clear-cut criteria of achievement". | 2 classes (Goal, Quality) plus the actor containment | Med. | Med. | Med. Pushes notes toward success criteria. |
| C4 | **KAOS Goal.** | Low. "An objective the system under consideration should achieve" is system-owned and optative. The paper has no stakeholder concern class. | 1 class (plus link types if used) | Low to Med. | Med. | Med. |
| C5 | **SysML v2 ConcernDefinition** (by reference only). | Low. "A kind of requirement definition", so evaluated true or false. Too heavy for a note-taker's interest. | n/a | High | n/a | Not usable. |
| C6 | **`skos:Concept` alone, no Concern class**, with concerns as untyped concepts in a scheme. | Low. Cannot say what is a concern, so no class page, no Heldby range. | 0 | High | Low | Low, but loses the SCAT structure. |
| C7 | **OSLC RM** (Requirement). | Low. No concern or stakeholder term in the vocabulary (zero occurrences). | n/a | High | n/a | Not usable. |
| C8 | **CDS.** | None. CDS has no concern term (its only use is the risk sense inside `problem`). | n/a | n/a | n/a | Not usable. |

**Recommendation (C1):** Adopt the 42010 Concern as the class, defined by the 42010 wording, built on `skos:Concept`
for labels, definitions and mappings.

**Runner-up:** C2, author our own `Concern` with the same label and our own definition.

**Deciding criterion:** recognisability, since the whole SCAT vocabulary is meant to read as systems engineering at
once, and the term and the sense ("interest in a system, held by stakeholders") are the 42010 ones. Fit is level
with C2. The cost of C1 over C2 is an unresolved primary-source gap: the standard was unreachable and SEBoK has no
glossary entry. If WP4 cannot verify the 2022 definition against the standard, C2 becomes the right choice, worded in
42010's terms, with the gap recorded.

**Honest note:** for Concern the evidence for "adopt" is weaker than for Stakeholder. Only one adoptable definition
was seen, and it came from a secondary page.

### Heldby endpoints (domain and range only)

| # | Option | Fit | Terms | Recog | Maint | Cost |
|---|---|---|---|---|---|---|
| H1 | **Domain Stakeholder group (S1), range Concern (C1)**, as the 42010 sentence has it ("Stakeholders ... holding Concerns"). | High. | 0 beyond S1 and C1 | High. | Low. | Low. |
| H2 | **Author our own endpoint typing**, with disjoint or unrelated local classes. | High. | 0 beyond S2 and C2 | Med. | Med. | Low. |
| H3 | **`foaf:interest` or `dcterms:audience` as the property.** | Low. Both have the wrong range or domain (a Document, a resource). | 1 property | Med. | Low. | Low, but wrong. |
| H4 | **`skos:related` between the two.** | Low. Associative but untyped, so Heldby could not be told from Addresses. | 0 | High. | Low. | Low. |

**Recommendation (H1):** Type the endpoints with the adopted Stakeholder (domain) and Concern (range), and leave the
property's name and form to the unit and package that own the relation.

**Runner-up:** H2.

**Deciding criterion:** fit. H3 and H4 fail on it, and H1 and H2 differ only in recognisability.

**Flag for WP1-G3 and the synthesis unit:** both a shared concern (one concern, several groups) and a concern conflict
need Concern to be a class of individually named things, not a literal. C1 satisfies that. The KAOS conflict link
(KAOS) and SKOS `skos:Collection`/`skos:Concept` disjointness (SKOS) are relevant material for the disagreement
unit.

### Summary (WP1-R8)

| Element | One-line recommendation | Runner-up | Deciding criterion |
|---|---|---|---|
| Stakeholder group | Adopt the SEBoK/15288:2015 Stakeholder definition (`skos:exactMatch`), "group" as usage | S2, author `StakeholderGroup` | Recognisability |
| Concern | Adopt 42010 Concern on `skos:Concept`; verify the 2022 wording first | C2, author `Concern` | Recognisability |
| Heldby endpoints | Domain Stakeholder, range Concern | H2, author local typing | Fit |

# Part B: Affordance and Technology (WP1-U2)

### Affordance

Intended meaning: what a technology makes possible, legible to stakeholder groups in a scenario's action situation
and offered by a tool in an architecture; the class sits between Concern and Technology.

| Option | Source | Fit | Simplicity (terms carried) | Recognition | Maintenance | Cost | Note |
|---|---|---|---|---|---|---|---|
| A1. Author our own `Affordance`; definition taken verbatim from Gibson with citation; anchor by mapping, not by import | S2 (Gibson p.119), S4, S20 | High: the name and sense are the mission's | High: 1 term (+ the SKOS carrier fields we already use) | Med: engineers know "capability" better; HCI folk know "affordance" | High: nothing external to track beyond the mappings | Low | Gibson's text is the adopted part; the class IRI is ours. |
| A2. Adopt `td:InteractionAffordance` (WoT TD 1.1) | S10, S11 | Low-Med: it is "Metadata of a Thing that shows the possible choices to Consumers", i.e. a description for machine consumers, attached to a `td:Thing` | Med: the class plus its three subclasses come as a family; we would use 1 | Med: an IoT and web standard, not a systems-engineering one | High: W3C Recommendation 2023 | Med: Thing, Consumer and form semantics leak into pages | Best name match among standards; wrong subject (a document about a Thing, not the possibility). |
| A3. Adopt SEBoK `Capability` (def. 4, "An outcome or effect which can be achieved through use of features of a system of interest ...") | S13, S15 | Med: fits the architecture side (tool features yield outcomes); weak on the scenario side (action situation, perceived options) | High: cds already carries `cdsterm:capability` | High: INCOSE/SEBoK canon | Med: the entry holds four differing definitions; cds picked the DoD wording | Low-Med: renames the user-facing class from the mission's "Affordance" | Strongest on recognition and coherence with cds. |
| A4. Adopt a formal disposition-based affordance (Toyoshima 2017/2022 on BFO-style dispositions) | S2, S3, S19 | Med: faithful to Gibson and Turvey; needs an agent's effectivity and a realization event | Low: affordance, effectivity, realization, bearer, trigger, background condition | Low | Low-Med: no released OWL found for S2; S3 body not reached; BFO import is out of scope | High: modelling burden on a note-taker | Right for an upper ontology, too heavy for "just enough structure". |
| A5. Adopt BFO `function` or `disposition` (`BFO_0000034`, `BFO_0000016`) | S19 | Low: function is tied to design or evolution of the bearer; an affordance need not be designed | Med: 1 class, but its axioms come with it | Low-Med | High: ISO/IEC 21838-2 | Med: upper-ontology constraints in a human-scale graph | Rejected on fit. |
| A6. Adopt `saref:Function` | S18 | Low: "Logical groups of commands that devices support" | High | Low | Med | Med | Rejected on fit. |
| A7. Maier and Fadel affordance-based design | S5, S6 | Med (theory) | n/a | Med | n/a | n/a | No vocabulary reached (content unread); source of method, not of terms. |

**Recommendation (one line):** Author the `Affordance` class (our IRI), take its definition verbatim from Gibson as
cited via Toyoshima (S2), and record mappings to `td:InteractionAffordance` and SEBoK Capability as anchors only; adopt
no class.

**Runner-up:** A3, SEBoK Capability adopted as the class (relabelled or with "affordance" as an alternate label).

**Deciding criterion:** Fit. SEBoK's Capability is outcome-centred and has four competing definitions, while the
scenario record needs the possibility on offer, before any outcome; and the mission fixes the class name "Affordance".
If the TBox work prefers recognition over fit, A3 wins on Recognition and coherence with cds.

Honest note: nothing adoptable beat custom on fit. The "adopt over mint" test is met by adopting Gibson's wording and
mapping to two published terms, not by importing a class.

### Technology

Intended meaning: the parts and wholes of an architecture, assembled into tools that provide affordances; part of the
action situation in a scenario but out of view.

| Option | Source | Fit | Simplicity (terms carried) | Recognition | Maintenance | Cost | Note |
|---|---|---|---|---|---|---|---|
| T1. Adopt the definition of SEBoK / ISO 15288 **System Element** ("A system element is a discrete part of a system that can be implemented to fulfill specified requirements."); class carried under our label `Technology`, anchored by `skos:exactMatch`-style mapping to the SEBoK entry, as cds does | S12, S15, S20 | High: parts and wholes; may be hardware, software, data, humans, processes ... so it covers whole assemblages | High: 1 term | High: the SE canon, and `concept-definition-stage` uses the same pattern | High: stable glossary URL, ISO source, v2.14 | Low | "Technology" is the mission's word; SEBoK has no Technology entry (S23), so the label is ours and the meaning adopted. |
| T2. SysML v2 `PartDefinition`, by reference | S16, S15 | Med-High: "an ItemDefinition of a Class of systems or parts of systems"; structural | High | High among MBSE users | Low-Med: OMG ships XMI/KPAR/JSON, **no OWL**; cds uses two different namespaces for it | Med: equivalence to a language metaclass invites SysML semantics | Mission says SysML by reference only; equivalence axioms exceed that. |
| T3. SOSA/SSN `Platform` / `ssn:System` | S17 | Low-Med: hosts sensors and actuators; System "implement[s] Procedures" | Med: brings Procedure and Deployment | Med in sensing, low elsewhere | High: W3C Rec 2017 | Med | Domain too narrow. |
| T4. SAREF `Device` | S18 | Low: "A tangible object designed to accomplish a particular task" excludes software and people | High | Low | Med | Med | Rejected on fit. |
| T5. ArchiMate Technology Layer | S22 | not assessed | not assessed | High | n/a | n/a | Unreachable (login redirect); stated, not scored. |
| T6. Author our own `Technology` with no external anchor | n/a | High: matches mission wording | High: 1 term | Low-Med: reads as invented to an SE | High | Low | Valid fallback; fails G10's "traces to its source". |

**Recommendation (one line):** Carry `Technology` as our class label with the SEBoK / ISO/IEC/IEEE 15288 System Element
definition adopted verbatim and mapped to the SEBoK entry; mention SysML `PartDefinition` as a reference mapping only.

**Runner-up:** T2, SysML v2 `PartDefinition` as an equivalent class (the `concept-definition-stage` precedent for its
System-of-Interest).

**Deciding criterion:** Maintenance, with Fit. OMG publishes no OWL for SysML v2 (S16) and cds already needs two
namespaces for one construct (S15), while the SEBoK entry has a stable URL and ISO provenance; and the mission says
SysML is by reference only.

### Cross-element note for the readout (not a TBox decision)

Both recommendations use one pattern: an authored class IRI, a definition taken verbatim from a cited authority, and a
mapping to published terms by SKOS mapping properties (as in S15). Attributes (affordance × technology) and
Addresses (concern × affordance) are owned by other units.

# Part C: Relations, records, status, provenance and disagreement (WP1-U3)

### 1. Heldby (stakeholder group x concern)

| Option | Fit | Simplicity | Recog. | Maint. | Cost | Note |
|---|---|---|---|---|---|---|
| A. Author `heldBy`, defined from 42010's "Stakeholders ... holding Concerns" (S1) | + | + (1 property) | + (42010 wording) | 0 (ours) | + | many-to-many, so "the same concern held by different groups" (G1) is native |
| B. `prov:wasAttributedTo` (S2) | - | + (0 new) | 0 | + (W3C Rec) | 0 | "ascribing of an entity to an agent" says who a claim comes from, not who holds a concern; the two meanings must stay apart for disagreement (section 8) |
| C. iStar actor boundary around a goal (S13) | 0 | - (needs actor, goal, boundary) | 0 | 0 (2016, no IRIs) | - | models what an actor wants; a concern is "any interest", not a goal with achievement criteria |
| D. `cds:forStakeholder` (S21) | - | 0 | 0 | 0 | 0 | links a need to a stakeholder; direction and subject differ; not a published standalone term |

- **Recommendation:** author `heldBy`, defined by reference to 42010's wording; no IRI exists to adopt.
- **Runner-up:** B (`prov:wasAttributedTo`).
- **Deciding criterion:** fit. Holding a concern is not attribution of authorship, and WP1-G3 needs both.

### 2. Addresses (concern x affordance)

| Option | Fit | Simplicity | Recog. | Maint. | Cost | Note |
|---|---|---|---|---|---|---|
| A. Author `addresses` | + | + (1 property) | + (verb used in 42010 and `cds`) | 0 | + | direction: affordance addresses concern |
| B. `cds:addresses` (S21), domain and range `cds:Term` | 0 | + (0 new) | 0 | 0 (0.1.0, one team) | 0 | meaning "solution addresses problem" matches; its domain/range tie us to `cds` classes; we would borrow the name, not the constraints |
| C. `rm:satisfies` (S14) | - | + | + (OSLC users) | + (OASIS Standard) | 0 | "a system requirement satisfies a user requirement": requirement-to-requirement, claims satisfaction; an affordance does not satisfy a concern in that sense |
| D. iStar contribution Make/Help/Hurt/Break (S13) | 0 | - (4 values) | + (RE community) | 0 | - | signed degree of effect; adds polarity (see D6 in section 8) but source/target are intentional element and quality |
| E. 42010 "viewpoint frames concerns" (S1) | - | n/a | + | n/a | n/a | a viewpoint frames concerns; it is not an affordance |

- **Recommendation:** author `addresses`, with a skos:closeMatch-style note to `cds:addresses`.
- **Runner-up:** B (`cds:addresses`).
- **Deciding criterion:** simplicity and independence: adopting B would carry `cds:Term` domain/range, and the term is
  unpublished beyond one repository's Turtle. If WP4 wants a shared DSG namespace, B becomes a rename.

### 3. Attributes (affordance x technology)

| Option | Fit | Simplicity | Recog. | Maint. | Cost | Note |
|---|---|---|---|---|---|---|
| A. Author `attributes` (technology offers affordance) | + | + (1 property) | + | 0 | + | |
| B. RO `has disposition` (RO_0000091, S12) | 0 | - (needs BFO class commitments: bearer, disposition) | - (biomedical) | + (2026-09-04 release) | - | "the disposition specifically depends on the bearer for its existence"; fits only if Affordance is defined as a disposition |
| C. `ssn:hasProperty`-style / SSN System (S8) | - | 0 | 0 | + | 0 | scope is sensors, observation and actuation |
| D. `dcterms:hasPart`-like reuse of architecture parts (S4) | - | + | + | + | 0 | an affordance is not a part of a technology |

- **Recommendation:** author `attributes`.
- **Runner-up:** B (RO has disposition).
- **Deciding criterion:** simplicity. B only fits if the Affordance unit defines affordance as a disposition; flag to
  the synthesis unit (not decided here: Gibson was not fetched in this unit).

### 4. Scenario record (behavioural)

What is needed (MISSION: events, outcomes, consequences over time, relating stakeholder groups, concerns,
affordances). G1 lists the scenario only as a page type, so inner event structure is a design question for WP4.

| Option | Fit | Simplicity | Recog. | Maint. | Cost | Note |
|---|---|---|---|---|---|---|
| A. Author a scenario record class; narrative stays in the page body; links are the three relations | + | + (1 class) | + | 0 | + | no event nodes, so nothing beyond G1 (R4) |
| B. SEM (S11): `sem:Event`, `sem:Actor`, `sem:hasSubEvent`, timestamps | + | 0 (4 core classes plus types) | 0 | 0 (2009, stable doc) | 0 | gives events as nodes; `hasSubEvent` "does not mean ... any causal relationship"; no causal property |
| C. PROV-O Activity chains, `prov:wasInformedBy`, `prov:wasInfluencedBy` (S2) | 0 | 0 | + | + | 0 | built for provenance of data; using it for story content mixes content and provenance (section 7) |
| D. RO `causally upstream of` + OWL-Time `time:before` (S12, S9) | 0 | - (two imports) | - | 0 (S9 is a Candidate Recommendation Draft, 2022) | - | the only explicit causal chain terms found; heavy for a note-taker |
| E. `schema:Event` (S16) | 0 | + | + | + | 0 | a class only, "at a certain time and location"; no relations |

- **Recommendation:** author the scenario record class and keep events in the narrative. If WP4 makes events nodes,
  adopt SEM `sem:Event` and `sem:hasSubEvent`, and add RO causal terms only if a causal chain must be queried.
- **Runner-up:** B (SEM).
- **Deciding criterion:** simplicity under R4 (an event node is a new element beyond G1).
- Not assessed: Event Ontology, LODE, CIDOC CRM (unreachable, see survey).

### 5. Architecture record (structural)

| Option | Fit | Simplicity | Recog. | Maint. | Cost | Note |
|---|---|---|---|---|---|---|
| A. Author an architecture record class named after 42010's Architecture Description (S1); parts and wholes via `dcterms:hasPart` (S4) | + | + (1 class, 0 new properties) | + | + (DCMI) | + | 42010 publishes no IRI, so the class is authored by reference; `hasPart` is a plain non-literal part-whole link |
| B. SysML v2 part usage (S22), by reference only | 0 | n/a | + | + | - (modelling language, not RDF) | cited in docs as the engineer's route to a full model; never imported |
| C. `ssn:hasSubSystem` (S8) | 0 | + | 0 | + | 0 | "component parts" of a System; sensor-domain system class |
| D. BFO `part of` (S12) | 0 | - | - | + | - | strict mereology, needs BFO classes |
| E. Author `hasPart` | 0 | 0 | 0 | 0 | 0 | duplicates A for no gain |

- **Recommendation:** author the record class (42010-worded); adopt `dcterms:hasPart` (<http://purl.org/dc/terms/hasPart>)
  for assemblage; cite SysML v2 by reference.
- **Runner-up:** C (`ssn:hasSubSystem`).
- **Deciding criterion:** simplicity plus recognisability: no domain class to import, and `hasPart` is a DCMI Recommendation term. Whether `hasPart` is needed at all in v0.1 is a WP4 decision, since G1 lists
  no part-whole relation.

### 6. Page status (`stub -> draft -> done`)

| Option | Fit | Simplicity | Recog. | Maint. | Cost | Note |
|---|---|---|---|---|---|---|
| A. Adopt `schema:creativeWorkStatus` (S16) with our three values | + | + (0 new properties; 3 values authored) | 0 | + | + | "stage in a lifecycle ... Draft"; values DefinedTerm or Text, so our values are allowed. The property is typed for CreativeWork (schema.org lists CreativeWork under "used on"), so a page would also be typed `schema:CreativeWork`, or the domain is left unenforced |
| B. Author `status` plus a three-value scheme | + | 0 (1 property + 3 values) | + | 0 | + | |
| C. `vs:term_status` (S15) | - | + | 0 | - (unfinished note, 2009) | 0 | for vocabulary terms, values unstable/testing/stable/archaic |
| D. `adms:status` (S17) | 0 | 0 | 0 | - (note retired 2023) | 0 | "status of the Asset in the context of a particular workflow process" |
| E. PAV versioning (S18) | - | 0 | 0 | + | 0 | versions, authors; no status |

- **Recommendation:** adopt `schema:creativeWorkStatus`; author the three values.
- **Runner-up:** B (authored `status`).
- **Deciding criterion:** "adopt over mint" at equal term count (the values are authored either way). Flip to B if WP4
  finds that a `schema:` namespace in the vault confuses the UX or the shape language.

### 7. Provenance

MISSION: the git repository is the data of record. Authorship and time live in git; the graph needs mainly the link
from a coded page to the raw page it came from. Chatham House (G6): no group stands for one identifiable person, so
attribution to named people is out of scope for the graph.

| Option | Fit | Simplicity | Recog. | Maint. | Cost | Note |
|---|---|---|---|---|---|---|
| A. `prov:wasDerivedFrom` for coded-from-raw (S2); everything else left to git | + | + (1 term) | + | + (W3C Rec) | + | "a transformation of one entity into another" |
| B. `dcterms:source` (S4) | + | + (1 term) | + | + | + | "A related resource from which the described resource is derived." Looser, no PROV chain |
| C. Add `prov:wasAttributedTo`, `prov:generatedAtTime` | 0 | - | + | + | - | duplicates git; attribution raises the Chatham House issue |
| D. PAV `authoredBy`, `previousVersion` (S18) | 0 | - | 0 | + | 0 | duplicates git |
| E. Author our own `derivedFrom` | 0 | 0 | - | 0 | 0 | |

- **Recommendation:** adopt `prov:wasDerivedFrom` (<http://www.w3.org/ns/prov#wasDerivedFrom>) coded page to raw page.
- **Runner-up:** B (`dcterms:source`).
- **Deciding criterion:** recognisability and fit: derivation is exactly PROV's meaning, and it leaves the door open
  to PROV for disagreement (D5) without a second vocabulary. B is equal on cost; either is defensible.

### 8. Options for holding disagreement and margins of conflict (WP1-G3)

Scope: the groups, concerns and relations in G1. Each option states form, cost and what the graph could show (WP1-R7).
"Cost" counts terms added (R4 allows these) and the effect on software and UX. No option here ranks or settles
between views (R-14).

The disjointness note first. The chief engineer's "disjointness axiom" idea is sound as an *integrity condition* (SKOS
itself calls disjointness one: S3), but in OWL it applies to classes or to relations, not to two concerns that are
individuals: `DisjointClasses` says "no individual can be at the same time an instance of both" (S5), and
`DisjointObjectProperties` says no pair of individuals is connected by both. Only if concerns are classes and records are typed by them does the axiom bite: a record typed as an instance of both
concern classes is then inconsistent. A record that merely links to two concerns is not inconsistent, so the axiom would
not even flag that case, and where it does apply it turns real tension into an error. So the disjointness idea is
best realised as a SHACL warning over an authored conflict link (D3), not as an OWL axiom (D2).

**Margins of potential conflict** (two groups share a concern, while their other concerns are opposed) are a derived
view: a query over `heldBy` joined with whichever conflict link below exists. No option needs a reasoner.

| ID | Option | Form | Cost | What the graph could show |
|---|---|---|---|---|
| D0 | Baseline (G1 minimum): many-to-many `heldBy` | the same concern linked from several groups | 0 terms | shared concerns across groups, concerns held by only one group; no opposition |
| D1 | Authored symmetric property between concerns, e.g. `conflictsWith` (S13 Hurt/Break and S3 `skos:related` are the nearest published ideas; neither is adoptable) | one edge between two concern pages | 1 property; 1 line in a concern page; low UX cost | which concerns are opposed; with D0, the margins: groups sharing a concern whose other concerns are linked by D1. Cannot say who asserted it or why |
| D2 | OWL `DisjointClasses` between concerns made classes (S5, S6 punning) | axiom per pair; concerns become classes as well as individuals | 0 properties but concern pages become classes; needs an OWL reasoner; works only if records are typed by concern classes; a record typed by both is inconsistent (a record that only links to both is not) | only inconsistency. Cannot show tension without blocking the data; works against "holds disagreement" |
| D3 | D1 plus a SHACL shape at `sh:Warning` severity (S7: `sh:disjoint` compares two property value sets on one focus node, so it cannot relate two concerns by itself; the rule needs `sh:sparql` or a property path over the conflict link, and a SPARQL-based constraint adds engine cost for WP2; S20 Tier-2 pattern with waiver) | shape per rule, not per pair; severity warning, never violation | D1's property plus 1 shape; no new class; `ant-rdf` adds a waiver class if justification is wanted (extra) | a coded record that touches both ends of a conflict is flagged, as an advisory the facilitator sees and may dismiss; matches the "warning, not error" guidance in MISSION design notes. It points at a tension, it does not rule |
| D4 | Named tension record (S21 `Tension`: label, description, `between`, status) | a page per tension, linking 2 or more concerns (or records) | 1 class, 2-3 properties, 1 page type; generated pages and index | n-ary conflict with a name and a description, who surfaced it (through the page's links), and its open/resolved state. Drop `resolved`: it implies someone adjudicated (R-14); keep `open` only or a free note |
| D5 | Per-source perspective: each relation asserted per coded record; "according to" the record (S11 `sem:View`/`sem:accordingTo`/`sem:Authority`; S20 `ant:Perspective`, `ant:Characterization`; S10 named graphs; S19 nanopublication) | light form: edge keeps the page it was coded in, derived from the vault (and `prov:wasDerivedFrom`); heavy form: one named graph per record, or SEM View nodes | light: 0 terms if the derived graph keeps the source page; heavy: named-graph store and per-graph SHACL, which `ant-rdf` itself deferred as "technically deep" (cost small only after the data shape is kept) | "from this perspective": the same concern held or addressed differently per source, with both coexisting without inconsistency (C6 of `ant-rdf`). Heavy form shows full contrastive views; light form shows only the page each edge came from |
| D6 | Signed `addresses` (S13 Help/Hurt idea): an affordance addresses one concern and harms another | a polarity on Addresses or two properties (`addresses`, `harms`) | 1 property or 1 value; low UX cost | an affordance that helps one concern while hurting another, i.e. conflict arising from architecture; complements D1 (concern-concern) rather than replacing it. Polarity here is a source's claim, not a verdict |
| - | Argumentation vocabularies (AIF, IBIS) | issue/position/argument nodes | several classes | not assessed: AIF primary source unreachable; node types that structure argument lean toward adjudication, which MISSION excludes |

How `ant-rdf` handles controversy (source S20, checked at the commit in the survey): it does not forbid contradiction.
Assertions carry the perspective they were authored under (C6), the reified Characterization lets one actant hold two
roles "without OWL inconsistency", structural problems are Tier-1 violations while analytical ones are Tier-2 warnings
that "may be waived with a justification" (C7), and every association is "in principle contestable" (C5). Named graphs
per perspective are deferred to v2 for cost reasons (`FUTURE_WORK.md` 1.2). `concept-definition-stage` takes the same
stance more simply: a Tension is a named, linkable record, and its conflict checks "flag rather than block" (S21).

- **Recommendation (for WP4 to decide):** D0 (already in G1), plus D1 and D3 together as the cheapest pair that makes
  the chief engineer's conflict example visible: 1 property and 1 warning-level shape. Defer D4 (a page type) and the
  heavy form of D5 (a store) until a worked example needs them. D5's light form comes free if the derived graph keeps
  each edge's source page.
- **Runner-up:** D4, which shows more (named, n-ary, described) at the price of one page type.
- **Deciding criterion:** simplicity of the terms carried and cost to the UX; fit to "holds disagreement" rules out D2.
- Caveat: D3's warning wording must not rank views. The facilitator-facing message should say two linked concerns are
  in tension, not that either side is wrong.
