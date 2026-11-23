# Sources: what each says on the four topics (WP3-D1)

Input to `strategy.md`. Citation keys: **[ant-rdf]** is <https://github.com/mzargham/ant-rdf> at commit
`a2ec48edc8f44e386eaeada922c4a90349581df3`; **[KOI]** is "KOI & The Unicorn", Block Science blog,
<https://blog.block.science/koi-and-the-unicorn/>; **[Loop]** is "Building the Loop", EPIC Proceedings 2025,
DOI 10.1111/epic.70009. Full reading notes, with section-level citations, are in `parts/`. Where a line is our
reading and not the source's claim, it says so. "Silent" means the source does not address the topic.

The four topics (WP3-G1): **(a)** eliciting stories and proposed designs; **(b)** keeping multiple perspectives;
**(c)** exposing controversy, friction, gaps and dissent; **(d)** the risks of collapsing disagreement.

## Source by topic

| Source | (a) Eliciting | (b) Perspectives | (c) Controversy, gaps, dissent | (d) Risks of collapse |
|---|---|---|---|---|
| [ant-rdf] | One question at a time, never pre-sorting; many entry routes; raw capture kept apart from later reading. Silent on live rooms and on eliciting a proposed design. | Strong: every statement sits under the perspective it was authored in; one thing can be read two ways without conflict. Cross-perspective handling is stated as unfinished. | Comparison shows where readings flip; each reading's silence is stated; failure and gaps are first-class; acknowledged gaps carry a reason. Silent on surfacing friction live. | Strong, as design stance: merging frames is a loss; agreement is a finding, not truth. Silent on social harm to a group. |
| [KOI] | Silent as a method; participatory rule-setting only. | Developed, theoretical: differences arise through relation. | Largely silent on disagreement among people. | Silent on flattening disagreement; warns instead against mistaking the model for the world. |
| [Loop] | Flagging, consent and co-built tools; tagging by participants. Silent on narrative or design elicitation. | Developed for access, authorship and legibility; no single ontology. Silent on holding conflicting views. | Contest is possible in principle; a withdrawn-consent episode left an auditable trace. Silent on dissent and its handling. | Adjacent only: ordering the world makes it more singular than it is. |
| The supplied drafts | Draw on what people already do; others' notes stay open to the owner's correction. Silent on designs. | Each party's account kept apart, with origin and time. | Put differences and unexamined arrangements to people as questions. | Boiling accounts down to one can mislead a group about its own spread of views. |

## [ant-rdf]

Contributes the most to this strategy. It is a toolkit for an ethnographer, not a facilitation method, and it has no
section on dissent as such; its stance is in its vocabulary and authoring rules.

- **(a) Eliciting.** The human gives the plain-language account and the tool only translates; the questions come
  one at a time, not batched; the person is not asked to pre-sort what comes up (for example, thing or person); the
  last question asks what is contested or coming apart. (`CLAUDE.md`, "The golden path", "Authoring flow";
  `.claude/skills/ant-mgmt.md`, "Catechism"; `ONTOLOGICAL_COMMITMENTS.md` C2; a2ec48e.) Raw material may be
  registered first and characterised later, and machine-extracted content lands only as candidates the human
  confirms. (`ONTOLOGICAL_COMMITMENTS.md` C7, C8; a2ec48e.) A rendering is shown back for revision in the person's own
  words. (`CLAUDE.md`, "Authoring flow", step 5; a2ec48e.) Silent on groups in a room and on eliciting a proposed
  design; the nearest item is a program and its opposing anti-program. (`ontology/material-semiotics-core.ttl`; a2ec48e.)
- **(b) Perspectives.** Different readings of one site may all be valid even when they contradict. Each statement
  carries the perspective it was authored under, and the same thing can be given different roles under different
  practices with no inconsistency. (`ONTOLOGICAL_COMMITMENTS.md` C6; `adr/0000-foundational-decisions.md` R3, R8;
  a2ec48e.) Readings are provenance, not fact. (`AGENTS.md`, pitfalls 1 and 2; a2ec48e.) Limit: handling of
  overlapping or contradictory perspectives is deferred. (`adr/0000-foundational-decisions.md` R9a; `FUTURE_WORK.md`;
  a2ec48e.)
- **(c) Controversy and gaps.** A comparison of two readings lists where they converge, where they diverge and what
  only one holds; each reading states what it is silent on. (`briefs/koi-comparison.md`; a2ec48e.) Every association
  is in principle contestable; failure and incompleteness are allowed, and an acknowledged gap needs a stated reason
  and an author. (`ONTOLOGICAL_COMMITMENTS.md` C5 for contestability; C7 for the waiver justification;
  `ontology/shapes/ant-shapes-warnings.ttl`; `adr/0000-foundational-decisions.md` R9b for who waived; a2ec48e.) A subversive use recorded as a documented exception is a worked
  dissent case. (`briefs/koi-ethnographic-network.md`; a2ec48e.) Silent on noticing friction before anyone voices it.
- **(d) Collapse.** A single global typing would smuggle one observer's frame into the model, so it is withheld;
  union of two frames is rejected in favour of partial connection; convergence is a finding, not objectivity;
  losses are documented, not absorbed. (`adr/0000-foundational-decisions.md` R2; `FUTURE_WORK.md`;
  `briefs/koi-comparison.md`; a2ec48e.) Silent on harm to a group; it frames the risk as analytical distortion.

## [KOI]

- **(a)** Silent as a method. Closest is the Terraforming section: participants shape ground rules together,
  against rules that change on them unseen. This is rule-setting, not eliciting stories or designs.
- **(b)** Developed through theory (Diffraction; The Mirror): differences emerge through relation, and observer and
  observed are entangled. Little on differing views inside a group.
- **(c)** Largely silent on disagreement among people. The opening names a widening gap between a model and the
  world, which is a critique of digital twins, not of group dissent.
- **(d)** Silent on flattening disagreement. The opening warns of treating the model as the thing it represents.
  Our inference: stressing connection could smooth over disagreement; the post does not say so.

## [Loop]

- **(a)** Participants flag messages, authors consent, approved content is shown, and tools were co-developed;
  participants can tag data as important (Methods; Telescope; Interpretation). Silent on eliciting narratives or
  proposed designs.
- **(b)** KOI links systems without homogenising them or imposing a central ontology; inscription is multi-authored;
  the Conclusion takes the world to be more than one, but less than many (Abstract; KOI; Inscription; Conclusion).
  The plurality described is of access and authorship; it does not show conflicting interpretations held side by side.
- **(c)** Traces can in principle be contested by people and agents (Inscription). A contributor withdrew consent;
  the content went, but the history of the withdrawal stayed queryable (Telescope). Silent on dissent and its handling.
- **(d)** Not addressed directly. The Conclusion says ordering the world tends to make it more singular than it is.
  Our inference: the ethnographer's interpretive authority concentrates control; the paper does not name it a risk
  (Interpretation; Conclusion).

## The supplied drafts (principles only)

Unpublished drafts from the same collaboration were read for principles. They concern a different setting from
facilitation sessions, so they bear on the topics indirectly. They are an unnamed group; nothing here is quoted,
linked or attributed.

- **(a)** Accounts are best drawn from what people already do, not from extra work asked of them. Whatever someone
  other than the owner writes down stays open to the owner's correction or withdrawal. Silent on proposed designs.
- **(b)** A party's account stays its own, and the party decides what travels beyond it. Contributions keep a note of
  where and when they came from.
- **(c)** Differences between accounts, and arrangements nobody has looked at lately, are put to people as questions
  to consider.
- **(d)** Boiling many accounts down to one can leave a group misled about its own spread of views.

## Where the sources are silent

Taken together, none of the sources supplies a live-room method for holding disagreement: [ant-rdf] holds it
analytically, [KOI] and [Loop] say little on it, and the drafts bear on it indirectly. [ant-rdf] and the drafts
both leave open how to notice a margin of potential conflict before anyone voices it, and none of the sources shows
the same concern held by different groups. These gaps are ours to fill in `strategy.md` and are marked there as our
design, not as findings from the sources.
