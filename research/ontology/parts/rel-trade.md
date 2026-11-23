# WP1-U3 trade part: relations, records, status, provenance, disagreement

Feeds `trade-study.md` (WP1-D2). Source IDs (S1..S22) are defined in `rel-survey.md`, which holds the links, versions
and verbatim quotes. Criteria (WP1-G2): **Fit** to the element's meaning in `MISSION.md`; **Simplicity** (terms we
would carry); **Recog.** (recognisability to systems engineers); **Maint.** (maintenance); **Cost** (to software and
UX). Ratings: + good, 0 neutral, - poor. They are judgments from the cited evidence, not measurements. This part
recommends; WP4 decides.

## 1. Heldby (stakeholder group x concern)

| Option | Fit | Simplicity | Recog. | Maint. | Cost | Note |
|---|---|---|---|---|---|---|
| A. Author `heldBy`, defined from 42010's "Stakeholders ... holding Concerns" (S1) | + | + (1 property) | + (42010 wording) | 0 (ours) | + | many-to-many, so "the same concern held by different groups" (G1) is native |
| B. `prov:wasAttributedTo` (S2) | - | + (0 new) | 0 | + (W3C Rec) | 0 | "ascribing of an entity to an agent" says who a claim comes from, not who holds a concern; the two meanings must stay apart for disagreement (section 8) |
| C. iStar actor boundary around a goal (S13) | 0 | - (needs actor, goal, boundary) | 0 | 0 (2016, no IRIs) | - | models what an actor wants; a concern is "any interest", not a goal with achievement criteria |
| D. `cds:forStakeholder` (S21) | - | 0 | 0 | 0 | 0 | links a need to a stakeholder; direction and subject differ; not a published standalone term |

- **Recommendation:** author `heldBy`, defined by reference to 42010's wording; no IRI exists to adopt.
- **Runner-up:** B (`prov:wasAttributedTo`).
- **Deciding criterion:** fit. Holding a concern is not attribution of authorship, and WP1-G3 needs both.

## 2. Addresses (concern x affordance)

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

## 3. Attributes (affordance x technology)

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

## 4. Scenario record (behavioural)

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

## 5. Architecture record (structural)

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

## 6. Page status (`stub -> draft -> done`)

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

## 7. Provenance

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

## 8. Options for holding disagreement and margins of conflict (WP1-G3)

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
