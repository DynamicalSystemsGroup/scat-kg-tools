# Reading notes: ant-rdf, against the four WP3-G1 topics

Unit WP3-U1. Source: <https://github.com/mzargham/ant-rdf>, read at commit `a2ec48edc8f44e386eaeada922c4a90349581df3`
(`a2ec48e` below; every citation is to that commit). Paths are relative to the ant-rdf repo root.

**Scope note.** `ant-rdf` is a toolkit for an ethnographer analysing a field site. It is not a facilitation method,
and it has no briefs titled "controversy" or "dissent" (the briefs are `briefs/*.md`, per case: network, comparison,
catalog). What it says about our four topics is mostly implicit in its vocabulary and authoring contract. Where it
says nothing, this file says "silent". Anything in "Reading for SCAT" is my inference, labelled as such.

## (a) Eliciting stories and proposed designs

**What the source says**

- Authoring starts from the ethnographer's plain-language account, which the tool turns into records. Assertions
  about the field come from humans, and the model only translates. (`CLAUDE.md`, "The golden path" and "What Claude
  is for"; a2ec48e.)
- The elicitation script is a "catechism" of one question at a time, not batched: network, actants, the four
  translation moments, inscriptions, the practice one speaks from, where the configuration holds, and what is
  contested or unraveling. (`.claude/skills/ant-mgmt.md`, "Catechism"; `CLAUDE.md`, "Authoring flow for a new case";
  a2ec48e.)
- The moments are prompted as open questions about a story: who defined the problem, how alternatives were cut off,
  whether each party accepted its scripted role or resisted, who spoke for the network. (`.claude/skills/ant-mgmt.md`,
  step 4; a2ec48e.)
- Elicitation avoids pre-categorising what comes up. The skill says not to ask whether an actant is a person or a
  thing, because that pre-sorts it. (`.claude/skills/ant-mgmt.md`, step 3; `ONTOLOGICAL_COMMITMENTS.md`, C2; a2ec48e.)
- Several entry routes are offered at every step: talking it through, importing existing notes, or registering raw
  material first and characterising it later. Raw material is kept apart from the reading of it. (`ONTOLOGICAL_COMMITMENTS.md`,
  C8; `.claude/skills/ant-mgmt.md`, "Before you start"; a2ec48e.)
- Machine-extracted content never goes in as fact. It lands as candidates the human confirms after a dry run.
  (`ONTOLOGICAL_COMMITMENTS.md`, C7; `CLAUDE.md`, "Critical rules"; a2ec48e.)
- A reviewable rendering is shown back and the person revises it "in their words", then loops. (`CLAUDE.md`, "Authoring
  flow", step 5; a2ec48e.)

**Silent on:** eliciting from groups or a live room, eliciting a proposed design as such (it captures how an existing
assemblage holds together, not a design someone proposes), and facilitation technique generally. The one design-like
item is the program / anti-program pair, "a scripted course of action" and its opposing one. (`ontology/material-semiotics-core.ttl`,
`ant:ProgramOfAction`, `ant:AntiProgram`, `ant:opposes`; a2ec48e.) The hotel-keys brief uses it for a manager's
sign and fob against the guest's counter-script. (`briefs/hotel-keys-network.md`; a2ec48e.)

**Reading for SCAT (inference).** The one-question-at-a-time, never-pre-sort, accept-any-route manner fits "yes, and".
The split between raw inscription and later characterisation matches capturing first, coding later.

## (b) Keeping multiple perspectives

**What the source says**

- Perspectives are a commitment: different readings of one site "may be simultaneously valid even when otherwise
  contradictory". (`ONTOLOGICAL_COMMITMENTS.md`, C6; a2ec48e.)
- A perspective is the relation between a perspective-haver and what is seen. It records who holds it
  (`perspectiveHeldBy`), the practice it is grounded in, and the invariance it tracks. It lives inside a case.
  (`ontology/material-semiotics-core.ttl`, `ant:Perspective`, `ant:Practice`; `adr/0000-foundational-decisions.md`, R9a; a2ec48e.)
- Every assertion carries the perspective it was authored under. Records are stored per perspective in the repo
  (`instances/cases/<case>/perspectives/<slug>/`), and the path is intended to become a named graph. (`ONTOLOGICAL_COMMITMENTS.md`,
  C6; `adr/0000-foundational-decisions.md`, R8; a2ec48e.)
- Roles are not attributes of a thing. A "characterization" binds a target to a role within a network, a practice and
  an invariance criterion. The same actant can be Mediator under one practice and Intermediary under another with no
  inconsistency. (`ontology/material-semiotics-core.ttl`, `ant:Characterization`; `adr/0000-foundational-decisions.md`, R3; `AGENTS.md`,
  "The mental model"; a2ec48e.)
- Worked examples: the koi case has two perspectives (architectural, ethnographic) on one site, and the scallops
  case has two readings of one actant. (`briefs/koi-comparison.md`, `briefs/scallops-network.md`; a2ec48e.)
- Reading discipline: "A reading is provenance, not fact"; agreement across perspectives is "a finding, not
  objectivity". The reader should write "under <practice>, X is characterized as...", never "X is...".
  (`AGENTS.md`, pitfalls 1 and 2; a2ec48e.)
- The tool refuses to pick the frame for the author: it does not choose perspectives or invariances without explicit
  human input. (`CLAUDE.md`, "What Claude is not for"; a2ec48e.)
- The comparison brief lays perspectives side by side (my inference from the brief, not a stated principle),
  pivoting on the actant both frames share, and sorts actants into "converge", "diverge", or "single frame".
  (`briefs/koi-comparison.md`, tables; `src/ant_rdf/compilers/perspectivecomparison.py`; a2ec48e.)

**Limits the source states about itself:** cross-perspective handling is deferred. In v1 "overlapping/contradictory
perspectives" wait for named graphs, there is no per-perspective constraint checking, and a clean treatment of "the
same actant in two graphs" is still to be decided. (`adr/0000-foundational-decisions.md`, R9a; `FUTURE_WORK.md`,
section on multiplicity; a2ec48e.)

**Silent on:** perspectives held by a group in a room. In the source they are held by analysts or teams, such as
the architectural and the ethnographic perspectives (`briefs/koi-comparison.md`, a2ec48e). It is also silent on how
to invite or protect a perspective during a session.
## (c) Exposing controversy, friction, gaps and dissent

**What the source says**

- Disagreement is made visible by the comparison, not resolved by it. The "diverge" list holds the "flips": one
  actant given different roles by different practices. (`briefs/koi-comparison.md`,  "Where the frames diverge"; query `ant query flips` in `.claude/skills/ant-query.md`; a2ec48e.)
- Each frame's silence is stated in the brief itself. The architectural network is "Silent on the human governance
  acts" that the ethnographic one foregrounds, and the ethnographic frame foregrounds what "the architecture cannot
  see". (`briefs/koi-comparison.md`, "Architectural" and "Ethnographic" sections; a2ec48e.) A frame's blind spot is
  recorded as a gap, and both frames stay.
- Contest is a built-in question: the catechism ends with "What's contested or unraveling?" (`CLAUDE.md`,
  "Authoring flow", step 2; a2ec48e.) Precariousness is a commitment: every association is "in principle
  contestable", and failed translations can be modelled. (`ONTOLOGICAL_COMMITMENTS.md`, C5; a2ec48e.)
- Failure and incompleteness are first-class, not errors. A translation with fewer than four moments raises a
  warning that can be acknowledged with a stated moment of failure. (`ontology/shapes/ant-shapes-warnings.ttl`,
  translation-completeness message; `ONTOLOGICAL_COMMITMENTS.md`, C5; a2ec48e.)
- Missing grounds are shown, not hidden. A characterization without a practice or an invariance triggers a warning,
  and the query output labels it "(no practice)". (`ontology/shapes/ant-shapes-warnings.ttl`; `AGENTS.md`, pitfall 5;
  `.claude/skills/ant-query.md`, "Fidelity notes"; a2ec48e.)
- Waivers are append-only and need a justification and an author. They apply to warnings only, never to structural
  errors. (`ontology/material-semiotics-core.ttl`, `ant:ConstraintWaiver`; `adr/0000-foundational-decisions.md`, R9b;
  a2ec48e.) This is a worked pattern for "acknowledged gap, with a reason, on the record".
- Opposition is representable at the level of designed behaviour: `ant:opposes` links a program to an anti-program.
  (`ontology/material-semiotics-core.ttl`; a2ec48e.)
- A concrete dissent case: in the koi ethnographic network, a contributor's "subversive" use of a forget function is
  recorded as a documented exception within the enrolment moment, and as a single-frame reading. (`briefs/koi-ethnographic-network.md`,
  Enrolment row; `briefs/koi-comparison.md`, tables; a2ec48e.) The same brief names a friction point, the loop
  failing to close. (`briefs/koi-ethnographic-network.md`, network description; a2ec48e.)

**Not yet there (source says so):** reified relations carrying "contestation status" and a "contestedBy" link are
listed as future work, not built. (`FUTURE_WORK.md`, section on qualified relations; a2ec48e.)

**Silent on:** how a facilitator surfaces friction in the moment, and how to notice a margin of potential conflict
before anyone voices it. The comparison finds divergence only after two readings have been authored.

## (d) The risks of collapsing disagreement

**What the source says (implicitly, as design stance, not as a named risk section)**

- Merging frames is treated as a loss. A global typing would "smuggle one observer-frame into the ontology", so the
  design withholds it. (`adr/0000-foundational-decisions.md`, R2, "Why"; a2ec48e.)
- Pre-sorting is a distortion: the bare typing of an actant as Mediator or Intermediary is called "pre-perspectival"
  and flagged. (`ontology/shapes/ant-shapes-warnings.ttl`, messages on typed Actant + Mediator/Intermediary; a2ec48e.)
- Fidelity risks are listed as pitfalls: roles read as types; a reading mistaken for fact; shared IRIs that "inflate
  counts" across frames. (`AGENTS.md`, "Five interpretive pitfalls"; a2ec48e.)
- Aggregate union is explicitly not the plan for the same actant seen in two frames: the plan is "partial connection
  rendering (Strathern 1991) rather than aggregate union". (`FUTURE_WORK.md`, multiplicity section; a2ec48e.)
- Convergence is not rewarded as truth: independent frames agreeing "is itself a finding, not a redundancy".
  (`briefs/koi-comparison.md`, "Where the frames converge"; a2ec48e.)
- Facts versus judgement are kept apart: "verification is machine; validation is human". The tool does not arbitrate
  field truth. (`ONTOLOGICAL_COMMITMENTS.md`, C7; `CLAUDE.md`, "Critical rules"; a2ec48e.)
- Silent smoothing is resisted: where a brief loses something, the loss is "documented as a known limitation, not
  silently absorbed". (`FUTURE_WORK.md`, validation regime section; a2ec48e.)
- Conflating separate acts is called "analytical opacity": scope, query, analysis and committed reading stay as
  separate artefacts, and a network summary is only materialised by "explicit human commitment". (`adr/0000-foundational-decisions.md`,
  R5; a2ec48e.)

**Silent on:** consequences of collapsing for a group (loss of trust, hidden dissent, the loudest view winning). It
frames the risk as analytical distortion, not social harm. It names no process for ranking or consensus, and
`ant-rdf` has none (also out of scope for WP3).

## Capabilities the graph would need to show (feeds WP3-G3; capabilities, not terms)

Each follows from a cited behaviour in sections (a) to (d) above (all at a2ec48e); "From" names where `ant-rdf` does it.

1. **Show who holds a reading, and from where.** Every statement is placed in the viewpoint it came from, and that
   place is readable. (From: perspective, practice; (b).)
2. **Hold two readings of one thing without conflict.** The same item can be described differently by different
   groups and neither overwrites the other. (From: characterization; (b), (d).)
3. **Compare viewpoints side by side on a shared item.** For any item, list what each viewpoint says, and mark
   agreement, difference, or held by one only. (From: comparison brief, flips query; (b), (c).)
4. **Show a viewpoint's silence.** Say what a viewpoint does not address, so a gap is a recorded fact and not an
   absence. (From: "Silent on..." in briefs; (c).)
5. **Show opposition between things people want or designed to happen**, without saying which is right. (From:
   program / anti-program; (c).)
6. **Show something marked incomplete, failed or contested, with its reason**, and let it stay that way. (From:
   waivers, translation-completeness warning; (c).)
7. **Show missing grounds** (a claim with no stated source viewpoint) as visible, not silently defaulted. (From:
   Tier-2 warnings, "(no practice)"; (c).)
8. **Separate raw capture from interpretation**, so what people said survives independently of how it is later
   read. (From: inscriptions and uploads, C8; (a).)
9. **Keep convergence as a recorded observation**, not as a settled answer. (From: C6, converge list; (d).)
10. **Refuse a merged answer**: no view may present the union of viewpoints as the single truth. (From: R2,
    partial-connection note; (d).)

Gap for WP3-G3: `ant-rdf` does not itself show "the same concern held by different groups" (its comparison pivots on
the actant, shared across readers) or "groups sharing one concern but opposed on others". Those two are SCAT's
own need (MISSION.md, Facilitation stance); `ant-rdf` offers only the nearest pattern, the cross-frame comparison.
