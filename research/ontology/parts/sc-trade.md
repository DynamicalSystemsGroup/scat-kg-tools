# WP1-U1 trade part: Stakeholder group and Concern

Partial file for `trade-study.md` (WP1-D2). Sources are keyed to `sc-survey.md`, which holds the links, versions and
verbatim quotes. Scope is the two elements and the endpoints of Heldby (stakeholder group on one side, concern on the
other). The Heldby relation's own name and shape belong to later packages.

## Criteria (WP1-G2)

- **Fit:** match to the meaning in `MISSION.md`. A stakeholder group is a class of people who hold concerns, abstracted
  from any one architecture (Scenarios and architectures). A concern is something a group cares about, which several
  groups can share and which can oppose another concern (Facilitation stance; G1; G10).
- **Terms:** how many terms the TBox would carry, counting classes and properties we would actually use.
- **Recog:** recognisability to systems engineers.
- **Maint:** maintenance, meaning what we must keep up as the source changes, or definitions we must write ourselves.
- **Cost:** cost to the software and the UX, meaning extra frontmatter, validation or reading burden for note-takers.

Ratings are High, Med or Low, with the reason in the cell. "Author our own" is the baseline in every table.

## Element 1: Stakeholder group

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

## Element 2: Concern

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

## Heldby endpoints (domain and range only)

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

## Summary (WP1-R8)

| Element | One-line recommendation | Runner-up | Deciding criterion |
|---|---|---|---|
| Stakeholder group | Adopt the SEBoK/15288:2015 Stakeholder definition (`skos:exactMatch`), "group" as usage | S2, author `StakeholderGroup` | Recognisability |
| Concern | Adopt 42010 Concern on `skos:Concept`; verify the 2022 wording first | C2, author `Concern` | Recognisability |
| Heldby endpoints | Domain Stakeholder, range Concern | H2, author local typing | Fit |
