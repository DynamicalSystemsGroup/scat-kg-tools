# Essays: what two published works say on the WP3-G1 topics

Unit WP3-U2. Input to WP3-D1 and WP3-G3. Research notes in our own words; no strategy, no ontology terms, no ranking, voting or consensus methods.

## Sources and how they were read

- **[KOI]** "KOI & The Unicorn", Block Science blog, <https://blog.block.science/koi-and-the-unicorn/> (23 October 2025). Sections: an untitled opening, The Mirror, Diffraction, Terraforming, Conclusion. There is no section called Summary or Introduction; the opening is cited as "opening (untitled)".
- **[Loop]** "Building the Loop: The Role of Ethnography in Artificial Organisational Intelligence", EPIC Proceedings 2025, DOI 10.1111/epic.70009, <https://doi.org/10.1111/epic.70009>. The DOI redirects to the publisher page <https://proceedings.epicpeople.org/article/154018-building-the-loop-the-role-of-ethnography-in-artificial-organisational-intelligence>, which was reachable. Sections: Abstract, Introduction, Methods, Theories and Practices of the Firm, Knowledge Organisation Infrastructure (KOI), Telescope, Ethnography as Building the Loop (with Observation, Interpretation, Inscription), Conclusion, and three end notes (n1 firms/organisations, n2 ontologisation, n3 model caveat).
- **Reading.** Revised after review: the full text of both pages was fetched as raw HTML and read directly, not through a summarising tool. Every claim below was checked against that text. Quotes are avoided; all wording is ours.

"Silent" means the source, as read, does not address the topic in that section or at all (WP3-R6). Where a line is our reading rather than the source's claim, it says "our inference".

---

## 1. KOI & The Unicorn [KOI]

### (a) Eliciting stories and proposed designs

- **Silent as a method.** The post does not describe gathering stories or proposed designs from people (all sections).
- **Terraforming:** closest. Participants shape the system's ground rules together, set against rules that change on them without their knowing. This is participatory rule-setting, not story or design elicitation.
- **Diffraction:** says what the infrastructure shows is the material traces of contributions, knowledge and practices. It does not say how those are collected from people.

### (b) Keeping multiple perspectives

- The most developed theme, carried mostly by theory (Barad) rather than by the views of people involved.
- **Diffraction:** differences emerge through relation, not separation; observer and observed are entangled; the approach helps a group notice patterns it is already making together.
- **The Mirror:** a mirror gives a bounded subject its own image; the post notes feminist critiques and Barad's "separateness" and moves away from it. Little on plural views.
- **Opening (untitled):** a model and the world it mirrors cannot align, so people outside the model must recalibrate it. Implicit at most.
- **Terraforming, Conclusion:** implicit (collective rule-setting; relation over representation). No account of differing views within a group.

### (c) Exposing controversy, friction, gaps and dissent

- **Largely silent** on disagreement among the people KOI serves (all sections).
- **Opening (untitled):** names a gap between model and world that widens with each iteration, and cites a warning that digital twins are "useful enough to be dangerous". This is a critique of digital twins, not of group dissent.
- **The Mirror:** admits the mirror metaphor has problems.
- **Diffraction:** interference patterns are used only as a metaphor; no conflicts, dissent or gaps are named.
- **Terraforming, Conclusion:** silent.

### (d) Risks of collapsing disagreement

- **Silent** on flattening disagreement inside a group (all sections).
- **Opening (untitled):** warns that treating a model as the thing it represents risks acting inside the simulation. A different risk (confusing model and world).
- **The Mirror:** flags reinforcing a bounded, self-regulating subject. Not about disagreement.
- **Diffraction, Terraforming, Conclusion:** silent. Our inference, not the source's claim: stressing connection and co-presence could smooth over disagreement; the post does not consider it.

---

## 2. Building the Loop [Loop]

### (a) Eliciting stories and proposed designs

- **Methods:** a design-oriented, participatory ethnography; tools co-developed with collaborators and field participants; three phases (consent automation and collection of approved posts; a plug-in to pull posts into local vaults with notes, tags and links; sending annotated notes back so participants see additions and changes, including deletions). Decisions on consent, visibility and "who participates in interpretation" are built into the architecture.
- **Telescope:** participants flag messages with an emoji; a bot asks the author for consent; approved content is shown in a dedicated channel. Early deployments showed that flagged messages needed added context and links to be interpretable (the reason for the move to KOI).
- **Ethnography as Building the Loop / Interpretation:** research participants can tag data to signal importance to a topic.
- **Theories and Practices of the Firm:** cites Orr's work on storytelling among technicians, as background. The paper does not itself describe interviews or narrative elicitation.
- **Silent** on eliciting *proposed designs* from participants (all sections). Participation is documented for tool design, flagging and consent, not for gathering people's accounts.

### (b) Keeping multiple perspectives

- **Abstract; Theories and Practices of the Firm; KOI:** KOI connects disparate systems and practices without homogenisation, without forcing organisations into a unified database, centralised ontology (n2 defines the term) or loss of control of their data. KOI standardises communication between nodes, not what nodes do inside.
- **Telescope:** the same record can be available to some people or machines and not others; an ethnographer can set a note as available to a colleague, the community or an LLM.
- **Interpretation:** sense-making is spread across ethnographers, LLMs and agents; data is deliberately oversampled so a diverse set of human and machine actors can interpret it later; boundaries and rules stay visible and co-created.
- **Inscription:** inscription becomes multi-authored, not a single fixed narrative; cites Anderson et al. that narrating from a human perspective alone is not enough.
- **Conclusion:** cites Law that the world is more than one but less than many, and that social science often makes it more singular than it is; says the approach is "more than one", with interpretation co-produced with moderators, stewards and AI agents.
- **Limit:** the plurality described is mostly of access, authorship and legibility. The paper does not show how conflicting interpretations among people are held side by side.

### (c) Exposing controversy, friction, gaps and dissent

- **Inscription:** the closest statement. Inscribed traces form a queryable mesh that humans and algorithmic agents can traverse, contest and augment, instead of one fixed narrative. This allows contest in principle; no instance of contested interpretation is reported.
- **Telescope (withdrawal episode):** a contributor revoked consent soon after approving a post. The post was deleted, but its identifier stayed, and the history of the deletion (not its content) stayed queryable as an auditable record that a boundary had been renegotiated. The authors call the consent layer a live governance surface.
- **Telescope (early deployments):** the gap between a flagged message and what is needed to interpret it was a limitation found in practice.
- **Conclusion:** the field is described as enacted through boundary-setting and permissions, not discovered.
- **Silent** on dissent within communities, on disagreement over annotations or interpretations, and on how any such disagreement was handled (whole paper). The work is described as "initial explorations" (Introduction) with "ongoing experiments" (end of Inscription); there is no findings or limitations section.

### (d) Risks of collapsing disagreement

- **Not addressed directly.**
- **Conclusion:** the Law passage is the nearest statement: ordering and representing the world tends to make it more singular than it is. The authors apply it to their approach as a reason to be "more than one". It concerns social-science representation, not group disagreement as such (our reading).
- **Abstract; KOI:** argues against homogenisation of systems and against a unified ontology. Again about systems, not about disagreement among people.
- **Observation; Interpretation; Conclusion:** the ethnographer configures what counts as meaning, acts as a "context-librarian", and holds authority through configuring and maintaining intelligibility. Our inference: this concentrates interpretive authority; the paper does not state it as a risk.
- **Note 3:** a model connected through retrieval to a KOI node still produces answers influenced by its vendor's training and rules. The note's point is that any model can be used, including organisation-made ones. It says nothing about flattening disagreement.
- **KOI section (Goldenfein):** discusses human-in-the-loop oversight as a shortcut that hides how responsibility is distributed. It is about accountability for automated decisions, not about disagreement, so it is not placed under (c) or (d).

---

## 3. Capabilities the graph would need to show (feeds WP3-G3)

Capabilities, not terms. Each is a need that follows from a source's statement or gap; the basis shows which. All are inferences for WP4 to confirm, none is a design.

1. **Hold more than one account of the same thing side by side without merging them.** Basis: [KOI] Diffraction; [Loop] KOI section (no unified ontology), Inscription (multi-authored, not one fixed narrative), Conclusion (Law). Neither source shows conflicting accounts coexisting, so the graph must supply that.
2. **Show who or which group holds each account.** Basis: [Loop] Inscription (multi-authored; trace of who did what); [KOI] Diffraction (perspective as relation). Source silent on attribution of conflicting views.
3. **Show where accounts differ, overlap or are in tension, as something visible.** Basis: [Loop] Inscription (traces can be contested); [KOI] Diffraction (interference, metaphor only). Neither source says how.
4. **Show gaps: what has not been said, and where a model and its world part.** Basis: [KOI] opening (model/world gap); [Loop] Telescope (flagged items lacking context).
5. **Keep each claim traceable to its source and to whoever recorded, annotated or interpreted it,** so the interpreter's role can be inspected. Basis: [Loop] Observation and Interpretation (ethnographer configures meaning), Inscription (trace of ethnographic labour).
6. **Show limits on who may see a record, and keep a trace when a record is withdrawn.** Basis: [Loop] Telescope (visible to some and not others; deletion history queryable; identifier persists). The paper is silent on analyses already published when consent is withdrawn, which is an open question for WP4.
7. **Show change over time in an account or boundary.** Basis: [Loop] Telescope (boundary renegotiated), Conclusion (temporality); [KOI] Terraforming (rules shaped collectively).
8. **Keep a proposed design distinct from the stories that motivate it.** Basis: both sources silent on eliciting designs; inferred from that gap.

## 4. Where the sources are silent (WP3-R6 summary)

| Topic | KOI | Loop |
|---|---|---|
| (a) eliciting | silent as method; participatory rule-setting only (Terraforming) | flagging, consent, co-built tools, tagging; silent on narrative or design elicitation |
| (b) perspectives | developed, theoretical | developed: no unified ontology, multi-authored inscription, Law; silent on holding conflicting views |
| (c) controversy and dissent | essentially silent | contest named as possible (Inscription); consent-withdrawal episode; silent on dissent and handling it |
| (d) collapse risk | silent | not directly addressed; Law passage and interpretive-authority point are adjacent |

Consequence: neither source supplies a method for holding disagreement. That has to come from `ant-rdf` and the other WP3 sources.
