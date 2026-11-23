# WP1-U2 trade study: Affordance and Technology

Partial file for `trade-study.md` (WP1-D2). Source IDs (S1 ...) refer to the register in `at-survey.md`.

Criteria (WP1-G2), scored High / Med / Low, where High is better for us:

- **Fit**: matches the meaning in `MISSION.md` (Purpose; Scenarios and architectures; Facilitation stance; G1; G10).
- **Simplicity**: few terms to carry. The count is the terms we would add to our TBox for this element.
- **Recognition**: a systems engineer knows the vocabulary at once.
- **Maintenance**: a stable, served, versioned source we can anchor to.
- **Cost**: to the software and the UX (what the facilitator-analyst sees; what the tools must handle).

Scores are the unit's judgment from the sources cited, not measurements.

## Affordance

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
cited via Toyoshima (S2), and record a `skos:closeMatch` to SEBoK Capability, with WoT `td:InteractionAffordance` kept only as a loose `rdfs:seeAlso` (it describes a Thing to machine consumers); adopt
no class.

**Runner-up:** A3, SEBoK Capability adopted as the class (relabelled or with "affordance" as an alternate label).

**Deciding criterion:** Fit. SEBoK's Capability is outcome-centred and has four competing definitions, while the
scenario record needs the possibility on offer, before any outcome; and the mission fixes the class name "Affordance".
If the TBox work prefers recognition over fit, A3 wins on Recognition and coherence with cds.

Honest note: nothing adoptable beat custom on fit. The "adopt over mint" test is met by adopting Gibson's wording and
mapping to one published term (Capability), not by importing a class.

## Technology

Intended meaning: the parts and wholes of an architecture, assembled into tools that provide affordances; part of the
action situation in a scenario but out of view.

| Option | Source | Fit | Simplicity (terms carried) | Recognition | Maintenance | Cost | Note |
|---|---|---|---|---|---|---|---|
| T1. Adopt the definition of SEBoK / ISO 15288 **System Element** ("A system element is a discrete part of a system that can be implemented to fulfill specified requirements."); class carried under our label `Technology`, anchored by `skos:closeMatch` to the SEBoK entry (not exact: SEBoK has no Technology entry and the label is ours; cds uses `exactMatch` for terms SEBoK does define) | S12, S15, S20 | High: parts and wholes; may be hardware, software, data, humans, processes ... so it covers whole assemblages | High: 1 term | High: the SE canon, and `concept-definition-stage` uses the same pattern | High: stable glossary URL, ISO source, v2.14 | Low | "Technology" is the mission's word; SEBoK has no Technology entry (S23), so the label is ours and the meaning adopted. |
| T2. SysML v2 `PartDefinition`, by reference | S16, S15 | Med-High: "an ItemDefinition of a Class of systems or parts of systems"; structural | High | High among MBSE users | Low-Med: OMG ships XMI/KPAR/JSON, **no OWL**; cds uses two different namespaces for it | Med: equivalence to a language metaclass invites SysML semantics | Mission says SysML by reference only; equivalence axioms exceed that. |
| T3. SOSA/SSN `Platform` / `ssn:System` | S17 | Low-Med: hosts sensors and actuators; System "implement[s] Procedures" | Med: brings Procedure and Deployment | Med in sensing, low elsewhere | High: W3C Rec 2017 | Med | Domain too narrow. |
| T4. SAREF `Device` | S18 | Low: "A tangible object designed to accomplish a particular task" excludes software and people | High | Low | Med | Med | Rejected on fit. |
| T5. ArchiMate Technology Layer | S22 | not assessed | not assessed | High | n/a | n/a | Unreachable (login redirect); stated, not scored. |
| T6. Author our own `Technology` with no external anchor | n/a | High: matches mission wording | High: 1 term | Low-Med: reads as invented to an SE | High | Low | Valid fallback; fails G10's "traces to its source". |

**Recommendation (one line):** Carry `Technology` as our class label with the SEBoK / ISO/IEC/IEEE 15288 System Element
definition adopted verbatim and mapped to the SEBoK entry by `skos:closeMatch`; mention SysML `PartDefinition` as a reference mapping only.

**Runner-up:** T2, SysML v2 `PartDefinition` as an equivalent class (the `concept-definition-stage` precedent for its
System-of-Interest).

**Deciding criterion:** Maintenance, with Fit. OMG publishes no OWL for SysML v2 (S16) and cds already needs two
namespaces for one construct (S15), while the SEBoK entry has a stable URL and ISO provenance; and the mission says
SysML is by reference only.

## Cross-element note for the readout (not a TBox decision)

Both recommendations use one pattern: an authored class IRI, a definition taken verbatim from a cited authority, and a
mapping to published terms by SKOS mapping properties (as in S15). Attributes (affordance × technology) and
Addresses (concern × affordance) are owned by other units.
