# Essays: what two published works say on the WP3-G1 topics

Unit WP3-U2. Input to WP3-D1 and WP3-G3. Research notes in our own words; no strategy, no ontology terms, no ranking, voting or consensus methods.

## Sources and how they were read

- **[KOI]** "KOI & The Unicorn", Block Science blog, <https://blog.block.science/koi-and-the-unicorn/>. Sections cited: Introduction, The Mirror, Diffraction, Terraforming, Conclusion.
- **[Loop]** "Building the Loop: The Role of Ethnography in Artificial Organisational Intelligence", EPIC 2025, DOI 10.1111/epic.70009, <https://doi.org/10.1111/epic.70009>. The DOI redirects to the publisher page <https://proceedings.epicpeople.org/article/154018-building-the-loop-the-role-of-ethnography-in-artificial-organisational-intelligence>, which was reachable and is what was read. Sections cited: Abstract, Introduction, Methods, Theories and Practices of the Firm, Knowledge Organisation Infrastructure, Telescope, Ethnography as Building the Loop (Observation, Interpretation, Inscription), Conclusion, Notes.
- **Reading caveat.** Both pages were read through an automated fetch-and-summarise tool, not by a person reading the full text. Section attributions follow the headings the tool reported. A human check of the cited sections is advised before the claims are relied on. Quotes are kept to a minimum.

"Silent" below means the source, as read, does not address the topic in that section or at all (WP3-R6).

---

## 1. KOI & The Unicorn [KOI]

### (a) Eliciting stories and proposed designs

- **Largely silent.** The post does not describe a method for gathering people's stories or proposed designs (Summary across sections; Introduction, The Mirror, Conclusion silent).
- **Diffraction:** says traces of contributions, knowledge and practices become visible, but not how they are collected from people.
- **Terraforming:** closest. Participants shape a system's ground rules together, set against rules imposed without their knowledge. This is participatory rule-setting, not story or design elicitation.

### (b) Keeping multiple perspectives

- The most developed theme, though carried by theory more than by the views of people involved (across sections).
- **Diffraction:** differences arise through overlapping relations, and the approach helps a group notice patterns it already makes together. Strongest passage on this topic.
- **The Mirror:** a mirror gives one viewer their own image; the post draws on feminist critiques and Barad's work on separateness to question it. Limited on plurality of views.
- **Introduction:** contrasts a model with the world it mirrors; humans outside the model must recalibrate it. Implicit.
- **Terraforming, Conclusion:** implicit only (collective change; relation over representation).

### (c) Exposing controversy, friction, gaps and dissent

- **Mostly silent** about internal disagreement among the people or organisations KOI serves (Summary).
- **Introduction:** names a gap between model and world and cites a warning that digital twins are useful enough to be dangerous. That is a critique of twins, not of group dissent.
- **The Mirror:** admits problems with its own metaphor.
- **Diffraction:** interference patterns suggest friction only as a metaphor; no conflicts, dissent or gaps are named.
- **Terraforming, Conclusion:** silent.

### (d) Risks of collapsing disagreement

- **Silent** on flattening disagreement in a group (Summary).
- **Introduction:** warns against treating a model as the thing it represents. This is a different risk (confusing map and territory).
- **The Mirror:** flags the risk of reinforcing a bounded, self-regulating subject. Not about disagreement.
- **Diffraction, Terraforming, Conclusion:** silent. Reader's note: the emphasis on connection could smooth over disagreement, and the post does not consider this; that is our inference, not the source's claim.

---

## 2. Building the Loop [Loop]

### (a) Eliciting stories and proposed designs

- **Methods:** a participatory, design-oriented ethnography in three phases, from consented capture, to annotation, to syncing back into organisations. Tools are co-developed with participants.
- **Telescope:** capture is triggered by participants flagging messages with an emoji, with a consent flow; a plugin for Obsidian syncs notes. A worked example covers a consent withdrawal.
- **Theories and Practices of the Firm:** cites Orr's work on storytelling, but the paper does not itself use interviews or narrative elicitation.
- **Assessment:** participation is strongest in tool design and consent, weaker in eliciting people's own accounts. Elicitation of *proposed designs* as such: silent.

### (b) Keeping multiple perspectives

- **Abstract, KOI section:** KOI links systems without homogenising them; there is no single unified ontology; organisations keep control of their data; participants can make material visible to some people or models and not others.
- **Theories and Practices of the Firm / KOI:** draws on John Law's idea of a world that is more than one.
- **Ethnography as Building the Loop (Interpretation, Inscription):** interpretation becomes recursive and multi-agent; inscription becomes a queryable, multi-authored mesh.
- **Limit:** the multiplicity is mostly about access and legibility. The paper does not show how conflicting interpretations among people are held or reconciled.

### (c) Exposing controversy, friction, gaps and dissent

- **Thin.** Friction appears in the consent-withdrawal episode (Telescope), which the authors treat as a renegotiated boundary, and in the use of Goldenfein's critique of human oversight (KOI section).
- Gaps are treated as things to make legible, not as sites of disagreement (across sections).
- **Silent** on dissent within communities and on how contested interpretations or annotations were handled (whole paper).
- The paper reports "initial explorations" and "ongoing experiments" (Conclusion/Methods): no findings, no limitations section.

### (d) Risks of collapsing disagreement

- **Not addressed directly.**
- It argues against homogenisation (Abstract, KOI section).
- **Related risk, partly implied:** the ethnographer "configures" what counts as meaning and acts as a context-librarian (Ethnography as Building the Loop), which concentrates interpretive authority. Whether that collapses disagreement is our reading, not stated.
- **Notes:** a caveat that model behaviour still reflects its training; LLM querying over annotated notes could flatten nuance. The paper touches this only in passing.
- Silent on how LLM outputs are checked or corrected by participants.

---

## 3. Capabilities the graph would need to show (feeds WP3-G3)

Capabilities, not terms. Each is a need implied by a source's gap or stated concern, so each is marked as inferred. None is a design.

1. **Hold more than one account of the same thing side by side without merging them.** Basis: [KOI] Diffraction; [Loop] KOI section (no unified ontology; world "more than one"). Both sources value plurality but neither shows how conflicting accounts coexist, so the graph must supply that.
2. **Show who or which group holds each account.** Basis: [KOI] Mirror and Diffraction (perspective as relation); [Loop] Interpretation and Inscription (multi-authored). Source silent on attribution of conflicting views.
3. **Show where accounts differ, overlap or are in tension, as a visible thing.** Basis: [KOI] Diffraction (interference as metaphor only); [Loop] silent on handling contested interpretation. Inferred.
4. **Show gaps: where nobody has said anything, or where a model and the world part.** Basis: [KOI] Introduction (model/world gap); [Loop] gaps treated as legibility problems.
5. **Keep the trace from a claim back to its source and to whoever recorded or interpreted it,** so an interpreter's role is inspectable. Basis: [Loop] Ethnography as Building the Loop (ethnographer configures meaning); Telescope (consent flow, provenance).
6. **Show visibility and consent limits on a record,** and a record's change when consent is withdrawn. Basis: [Loop] KOI and Telescope (visible to some, not others; withdrawal example). Loop is silent on already-published analyses, so the graph should at least not hide that question.
7. **Show change over time in an account,** including renegotiated boundaries. Basis: [Loop] Telescope (withdrawal as renegotiation); [KOI] Terraforming (collectively shaped rules).
8. **Keep a proposed design distinct from the stories that motivate it.** Basis: both sources silent on eliciting designs ([KOI] (a), [Loop] (a)). Inferred from the gap, flagged for WP4 to confirm.

## 4. Where both sources are silent (WP3-R6 summary)

| Topic | KOI | Loop |
|---|---|---|
| (a) eliciting | silent, except participatory rule-setting (Terraforming) | participant-flagged capture and co-built tools; silent on narrative or design elicitation |
| (b) perspectives | developed, theoretical | developed, structural (access, no single ontology) |
| (c) controversy and dissent | essentially silent | thin; no handling of contested interpretation |
| (d) collapse risk | silent | not addressed directly; related concern about interpretive authority |

Consequence: neither source supplies a method for holding disagreement. The strategy has to draw that from `ant-rdf` and the other WP3 sources, not from these two.
