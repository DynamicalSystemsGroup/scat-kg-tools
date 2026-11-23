# WP1-U3 trade study: relations, records, status, provenance, axioms

Source entries are in `u3-survey.md` (section numbers below, e.g. S1.2). Scores are 1 to 5, 5 best, on the WP1-G2
criteria: **Fit** (to the meaning in MISSION Purpose/G1 and D-003, D-010, D-013), **Simple** (fewer terms carried scores
higher), **Recog** (recognisability to systems engineers), **Maint** (low maintenance burden, stable upstream), **UX/SW**
(low cost to software and UX). Totals are unweighted; the deciding criterion is named separately because the core
heuristics break ties: users "make the right way the easy way", builders "as simple as possible but no simpler"
(MISSION, Core heuristics).

Shared design fact. Relations are pages (MISSION R-11), each with a status (G3). So each of Heldby, Addresses and
Attributes is carried as a **relation class with two ends** that the stub command can create. A plain binary property
cannot be a page, hence is not an option alone. Adoption below therefore means: anchor the relation's name or its ends to an
external term, not replace the page. The cost of that shape is the same for every option and is not scored.

## 1. Heldby (stakeholder group x concern)

| Option | Fit | Simple | Recog | Maint | UX/SW | Total | Note |
|---|---|---|---|---|---|---|---|
| A. Author own `Heldby` relation class | 5 | 4 | 3 | 5 | 5 | 22 | Name is the one in G1; 1 class + 2 end properties |
| B. PROV `prov:wasAttributedTo` (S1.2) | 1 | 4 | 3 | 5 | 2 | 15 | Means "ascribing of an entity to an agent"; would import attribution, the thing D-010 excludes |
| C. iStar actor-owns-element (S1.8) | 3 | 2 | 4 | 3 | 2 | 14 | No named link in the 2.0 guide to adopt; no importable IRI |
| D. 42010 stakeholder-concern relation (S1.9) | 3 | 3 | 5 | 4 | 3 | 18 | Text paywalled; I cannot quote it, so cannot confirm the fit or the term |

- Recommendation: **A, author**, with a human-readable pointer in the class description to the 42010 concern relation.
- Runner-up: D (42010 relation), as a documented anchor only.
- Deciding criterion: fit with the no-attribution decision (D-010); the only vocabulary with an IRI that says "agent plus
  thing" is PROV attribution, which is the wrong claim. Re-open D if the stakeholders-and-concerns unit adopts 42010 terms
  for the two ends, since the relation name should then follow them.

## 2. Addresses (concern x property)

| Option | Fit | Simple | Recog | Maint | UX/SW | Total | Note |
|---|---|---|---|---|---|---|---|
| A. Author own `Addresses` relation class | 5 | 4 | 4 | 5 | 5 | 23 | Name in G1; reads naturally for SE users |
| B. `cds:addresses` (S1.11) | 2 | 3 | 3 | 3 | 3 | 14 | Right word; domain/range `cds:Term` (concept definitions), would pull cds in |
| C. iStar contribution Make/Help/Hurt/Break (S1.8) | 3 | 1 | 4 | 3 | 2 | 13 | Graded and directional to a quality; adds four levels the users did not ask for |
| D. OSLC RM `oslc_rm:satisfies` (S1.7) | 3 | 3 | 4 | 4 | 3 | 17 | Generic "entities"; says satisfied, a stronger claim than addresses; domain/range unverified |
| E. `skos:related` (S1.1) | 1 | 4 | 3 | 5 | 4 | 17 | Untyped; also does not carry direction |

- Recommendation: **A, author**; record in the class description that the term is the same word as `cds:addresses` and
  informally aligned, with no import.
- Runner-up: D (`oslc_rm:satisfies`), as an optional `skos:closeMatch`-style note, not an equivalence.
- Deciding criterion: fit (the relation is "addresses", which is weaker than "satisfies", and ungraded in v0.1); simplicity
  rules out iStar's four levels.

## 3. Attributes (property x technology)

| Option | Fit | Simple | Recog | Maint | UX/SW | Total | Note |
|---|---|---|---|---|---|---|---|
| A. Author own `Attributes` relation class | 5 | 4 | 3 | 5 | 5 | 22 | Name in G1. "Attributes" is not common SE usage, but the user's glossary can say it |
| B. `sosa:isObservedBy` (S1.6) | 1 | 3 | 2 | 5 | 2 | 13 | Observation of a quality by a sensor, not provision |
| C. OSLC `oslc_rm:satisfiedBy` (S1.7) | 3 | 3 | 4 | 4 | 3 | 17 | Direction fits (property satisfied by technology); semantics stronger ("satisfied") than "attributed"; domain/range unverified |
| D. iStar contribution (S1.8) | 3 | 1 | 4 | 3 | 2 | 13 | As for Addresses |

- Recommendation: **A, author**, noting `oslc_rm:satisfiedBy` in the description as the nearest published term.
- Runner-up: C.
- Deciding criterion: fit and simplicity; no published term means "technology is credited with a property", and the
  strongest candidates over-claim or add grades. Flag for the synthesis unit: the three relations are consistent in being
  authored; if one adopts, adopt for all, or the ontology reads as a patchwork.

## 4. Scenario and architecture records (raw and coded)

G1 requires four page types: raw and coded scenarios, raw and coded architectures; the R-11 templates cover these four.

| Option | Fit | Simple | Recog | Maint | UX/SW | Total | Note |
|---|---|---|---|---|---|---|---|
| A. Author four classes `RawScenario`, `CodedScenario`, `RawArchitecture`, `CodedArchitecture`, all `rdfs:subClassOf prov:Entity` | 5 | 3 | 4 | 5 | 5 | 22 | One class per template; the page type is the class |
| B. Author two classes (`Scenario`, `Architecture`) plus a raw/coded flag | 4 | 4 | 4 | 5 | 3 | 20 | Fewer classes, but the rules for raw and coded differ (coded links into graph, raw links to coded), so the flag becomes a hidden class and needs conditional shapes |
| C. 42010 Architecture Description as the architecture record (S1.9) | 3 | 3 | 5 | 4 | 3 | 18 | Right for coded architectures; "raw pitch notes" are not an AD; nothing for scenarios; no IRI |
| D. SysML v2 `UseCaseDefinition` / `PartDefinition` anchors (S1.10) | 2 | 2 | 5 | 4 | 3 | 16 | Anchors as annotation per the cds pattern; a scenario is a story, not a use case definition, so equivalence would be wrong |
| E. cds `Source` boundary object (S1.11) | 2 | 3 | 3 | 3 | 3 | 14 | Models cited authority documents, not facilitated notes |

- Recommendation: **A, author four classes**, each a subclass of `prov:Entity` so provenance (section 6) attaches without
  extra terms. Optionally annotate the coded architecture with a pointer to 42010 AD in its description.
- Runner-up: B (two classes plus a flag).
- Deciding criterion: "make the right way the easy way": four templates map to four classes with no conditional rules for
  the user to learn. B saves two terms but costs conditional checks and clearer messages. Do not use SysML equivalence for
  scenarios.
- Cost note: four classes versus two is two extra terms; they are authored, so no upstream dependency.

## 5. Page status (stub, draft, done)

| Option | Fit | Simple | Recog | Maint | UX/SW | Total | Note |
|---|---|---|---|---|---|---|---|
| A. Author `status` property + 3-concept SKOS scheme (`stub`, `draft`, `done`) | 5 | 4 | 4 | 5 | 5 | 23 | Same pattern as `cds:retrievalStatus` (S1.11); one property + one scheme + three concepts |
| B. Adopt `adms:status` (S1.4) with own 3 values | 4 | 4 | 3 | 2 | 4 | 17 | Range `skos:Concept` fits; the W3C Note is retired and its values are not in it; domain is "Asset" |
| C. Adopt `schema:creativeWorkStatus` (S1.5) | 3 | 4 | 2 | 4 | 4 | 17 | Accepts text or a defined term; domain CreativeWork; web-markup flavour for an SE audience |
| D. DCTERMS / SKOS only | 1 | 5 | 4 | 5 | 1 | 16 | Neither has a status term (S1.1, S1.3), so it would carry nothing |

- Recommendation: **A, author**, `status` taking one of three SKOS concepts, with an annotation naming `adms:status` as the
  near-equivalent.
- Runner-up: B (`adms:status` for the property; still author the three values).
- Deciding criterion: maintenance; the only published property is in a retired Note, so adoption buys a name and costs a
  dependency. Terms carried are the same (one property) either way, so recognition by SE users, not by semantic-web users,
  decides.
- Check owned by WP3, not here: the order `stub -> draft -> done` is enforced by rule; a SKOS scheme gives labels, not order.

## 6. Provenance (raw record to coded pages)

Direction facts: raw records link to or embed their coded pages (MISSION G1); provenance runs the other way (coded derived
from raw). The tool derives one from the other. Cost: users write one link; the tool writes the other direction.

| Option | Fit | Simple | Recog | Maint | UX/SW | Total | Note |
|---|---|---|---|---|---|---|---|
| A. Adopt `prov:wasDerivedFrom` (S1.2), coded -> raw | 5 | 5 | 4 | 5 | 4 | 23 | Defined as a transformation of one entity into another; PROV is the cds spine; inverse `prov:hadDerivation` is reserved |
| B. Adopt `dcterms:source` (S1.3) | 4 | 5 | 4 | 5 | 4 | 22 | "A related resource from which the described resource is derived."; lighter, but a second vocabulary alongside PROV |
| C. `prov:hadPrimarySource` (S1.2) | 3 | 4 | 3 | 4 | 4 | 18 | Expanded term; its wording presumes an agent with direct experience; weaker fit, closer to attribution |
| D. Author own `codedFrom` | 4 | 3 | 2 | 5 | 4 | 18 | One extra term for the same meaning |

- Recommendation: **A, adopt `prov:wasDerivedFrom`** (`http://www.w3.org/ns/prov#wasDerivedFrom`), from coded record (and its
  SCPT and relation pages, if wanted) to the raw record. Use the same property for any later page-to-page derivation.
- Runner-up: B (`dcterms:source`).
- Deciding criterion: coherence; one ontology, one provenance vocabulary, already the spine of `concept-definition-stage`.
- Do not adopt `prov:wasAttributedTo` or `prov:Agent` in v0.1: raw notes are Chatham House (D-010), so no agent is named.
- If the raw-links-to-coded direction cannot be derived automatically, the cost shifts to the user (one link each way);
  flag to WP3.

## 7. Axioms

### 7.1 The concern conflict (anonymity vs attribution)

D-010: "those can be related by a disjointness axiom." The intent (keep the conflict in the data and let the tools use it)
is sound. The form needs care, because **OWL disjointness is defined on classes and properties, not on instances**.

Our concerns, anonymity and attribution, are **instances** (pages): one page per concern. Facts:
- `owl:disjointWith` / `DisjointClasses` (OWL 2 s9.1.3): "no individual can be at the same time an instance of both CEi and
  CEj". This says an individual cannot be in both classes. It says nothing about two individuals that are different concerns.
- `DisjointObjectProperties` (s9.2.3): "no individual x can be connected to an individual y by both OPEi and OPEj". Also not it.
- `DifferentIndividuals` (s9.6.2) only says "all of the individuals ai ... are different from each other", i.e. not identical,
  which is trivially true of two pages.
- The only way to apply class disjointness to concerns is to turn each concern into a class (the "Anonymity" page would have to be
  a class). Metamodeling is allowed (s5.9: one IRI can refer to more than one type of entity), but then the
  disjointness holds for the class view and still means "nothing is both an Anonymity thing and an Attribution thing". It
  does not mean "a stakeholder group should not hold both", and it adds a class per concern, so the user has to model concerns
  as classes. That breaks the page model (a concern is a page) and the SCPT class count, and is not an easy win.

So, taken literally, **a disjointness axiom does not express the conflict**; the honest consequence is that either it is
vacuous (no individual is typed as both), or it forces concerns into classes. What the chief engineer wants is a typed
pairwise relation between concerns.

| Option | Fit | Simple | Recog | Maint | UX/SW | Total | Form and cost |
|---|---|---|---|---|---|---|---|
| A. `owl:disjointWith` between concern classes (needs a class per concern) | 1 | 1 | 3 | 3 | 1 | 9 | Concerns become classes; user must create a class and an instance; most terms; vacuous on instance pages |
| B. Authored symmetric, irreflexive object property `conflictsWith` (Concern x Concern), asserted on instances | 5 | 4 | 4 | 5 | 4 | 22 | 1 property; the user adds one link on a concern page; one SHACL shape |
| C. `skos:related` plus a note (S1.1) | 1 | 5 | 3 | 5 | 4 | 18 | Untyped; "related" is the opposite of the intent |
| D. iStar `Hurt`/`Break` contribution (S1.8) | 2 | 1 | 4 | 3 | 2 | 12 | Directional and graded, from element to quality; not a symmetric pairwise conflict |
| E. A reified `Conflict` relation page between two concerns | 4 | 2 | 3 | 5 | 2 | 16 | Consistent with relation pages, but a page per conflict adds work to the facilitator for a rarely used link |

- Recommendation: **B, authored `conflictsWith`**, declared symmetric and irreflexive in the TBox; stored on one concern
  page only (Obsidian's backlinks show the other direction).
- Runner-up: E (reified), if a conflict needs its own status or notes.
- Deciding criterion: it is the only option that expresses the conflict between two instance pages without making concerns
  classes (the user-facing cost of A) or inventing grades (D).
- State this to the chief engineer plainly: **the axiom is "conflictsWith is symmetric and irreflexive", not "disjoint";**
  the word disjointness stays only for the class axiom in 7.2.

**Form (SHACL, to be written in WP3; shown as a pattern, not as TBox Turtle).**
1. TBox: `conflictsWith` is an `owl:ObjectProperty`, `owl:SymmetricProperty`, `owl:IrreflexiveProperty`, domain and range Concern.
2. SHACL: a node shape on Concern (`sh:class` check for both ends, `sh:ClassConstraintComponent`, S1.13) plus a SHACL-SPARQL
   constraint (`sh:SPARQLConstraintComponent`) for irreflexivity, if the checker does not do OWL reasoning.
3. SHACL does not do OWL inference: a link written on one page is not a link on the other unless the tool materialises the
   inverse or the query treats the property as symmetric. Choose one in WP3.

**What the user gets, and its cost.**
- Value: the graph can show tensions; a facilitator sees conflicts, and a stakeholder group holding both concerns, or a
  property that addresses both, is visible (the case-study case, G6).
- Cost, user: 1 optional link on a concern page; 0 new page types; 0 required fields.
- Cost, software: 1 property; 1 to 3 rules, all at warning or info severity, never errors, since a group may hold
  conflicting concerns; the rule to find "a group holds both" is a SHACL-SPARQL query (the one that needs a SPARQL engine).
- Cost, UX: the message needs plain words (for example "These two concerns conflict and are both held by group X"). It is
  not a defect, so it must not be worded as one.

### 7.2 Other easy-win axioms

| Axiom | Value | Cost | Recommendation |
|---|---|---|---|
| Pairwise disjointness of the four SCPT classes (S, C, P, T); `owl:AllDisjointClasses`, in the style of SKOS Concept vs Collection (S1.1) | Catches a page typed as two classes, e.g. after a bad merge | 1 axiom; 0 fields; 0 UX; a rule only fires if a page has two types, which the page templates make rare, so low value | **Adopt**; near-zero cost. Skip if it adds any rule or message the user sees |
| Domain/range of the three relations (end checks, `sh:class`) | The "relation endpoints of the right classes" error in MISSION R-1 | Already required by R-1; not an extra axiom | Not an easy win but baseline; WP3 |
| `owl:inverseOf` for each relation (for example `heldBy` / `holds`) | Backward navigation in queries | 3 more terms; the Obsidian backlinks already cover the reading case | **Do not adopt** |
| Property disjointness of `conflictsWith` and `skos:related` (S1.1 shows SKOS does a similar disjointness itself) | Stops a pair of concerns being both related and in conflict | Pulls SKOS associative links into the vocabulary just to forbid them | **Do not adopt** |
| Cardinality, e.g. every Heldby has exactly one group and one concern | Completeness of relation pages | Duplicates `sh:minCount`/`sh:maxCount` in the shapes | Leave to SHACL in WP3 |

### 7.3 Axioms summary

- Concern conflict: **B, authored symmetric and irreflexive `conflictsWith`**; runner-up E; criterion: expresses instance-level
  conflict with no class-per-concern.
- Class disjointness of S, C, P, T: adopt at zero cost, optional.
- Nothing else is recommended; each extra axiom would add terms or messages without a user-visible gain in v0.1.

## 8. Composition notes (for the synthesis unit)

| Element | Recommendation | Source or "authored" |
|---|---|---|
| Heldby | authored relation class | authored; reason: no term matches without implying attribution |
| Addresses | authored relation class | authored; same word as `cds:addresses`, not imported |
| Attributes | authored relation class | authored; nearest `oslc_rm:satisfiedBy`, not adopted |
| Scenario, architecture records | four authored classes under `prov:Entity` | `http://www.w3.org/ns/prov#Entity` (parent only), the rest authored |
| Status | authored `status` + 3-concept SKOS scheme | authored; pattern from `cds:retrievalStatus`; uses `skos:Concept`, `skos:ConceptScheme` |
| Provenance | `prov:wasDerivedFrom` | `http://www.w3.org/ns/prov#wasDerivedFrom` |
| Concern conflict | authored `conflictsWith` (symmetric, irreflexive) | authored; OWL 2 property characteristics |
| Class disjointness | `owl:AllDisjointClasses` over S, C, P, T | OWL 2, optional |

Imported terms carried by this cluster: `prov:Entity`, `prov:wasDerivedFrom`, `skos:Concept`, `skos:ConceptScheme`. All others are
authored, which fits the patchwork test only if the stakeholders-and-concerns and properties-and-technologies units also
author or adopt consistently; flagged for synthesis.

## 9. Caveats

- 42010 text is paywalled and was not retrievable; the Heldby option D and the AD record option C rest on that gap.
- KAOS conflict links were not retrieved.
- OSLC RM formal domain and range for `satisfies` and `satisfiedBy` were not checked.
- Scores are my judgement and unweighted; they show the ranking, not a measured difference.
- Limited reads: SKOS (first 100k of 145k characters), DCTERMS (first 100k of ~117k), PROV-O (about 260k read in parts); the unread tails were not searched.
