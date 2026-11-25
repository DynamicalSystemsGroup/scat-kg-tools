# Translating the KOI coding into SCAT: what was kept, lost and interpreted

## What this is, and is not

The source is the public KOI case in `mzargham/ant-rdf` (commit `a2ec48edc8f44e386eaeada922c4a90349581df3`), coded there with the ANT ontology. Nine short texts were written from that coding (`inputs/`) as predigested stand-ins for field notes. They are a step above the synthetic lab vault and short of a field test.

Workers coded the texts by hand through the tool (`stub`, `record-edge`, `set-status`), standing in for the coder. The coder owns interpretation. Here nobody who knows the field confirmed any reading, yet every narrative is `done`. Per ruling D-096, `done` means "a worker set it", not "a coder attested it". Read every judgement below as the workers' proposal to a coder, not as a coder's finding.

## What the vault holds

`scat check` reports no problems. Counts, from `scat status` and `scat layered`:

- 4 groups (the cap): ethnographers, technical-team, community-members, ethics-committees.
- 13 concerns, 8 affordances, 2 technologies (Obsidian, Telescope).
- 9 narratives, all `done`: six scenarios (koi-01 to koi-06) and three architectures (koi-07 to koi-09).
- 27 edges: 15 *holds*, 9 *is addressed by*, 3 *is provided by*. This is after the review.

## What translating kept

- **Two readings of one matter.** The source shows the architectural and ethnographic perspectives diverging on how members figure in KOI and on what integration does to the protocol. Each is one concern, held by two groups, with the contrast in the row notes. The disagreement stays visible: two *holds* edges meet on one concern.
- **Tools help but cannot close the loop.** Kept as the concern "closing the loop", addressed by durable shared records, provided by Obsidian and Telescope.
- **The club good.** The data set's integrity matters to every member together; one concern, held by community members.
- **One affordance, two sides.** The forget signal is coded as the answer to the right to be forgotten in the forget incident (the scenario); the architecture (koi-08) tells its routine designed use, and koi-07 links it only as one of the FUN signals, with no edge. It is one affordance on two pages.
- **The doctrine** addresses vendor lock-in (scenario) and requisite variety (architecture).

## What translating lost

- ANT's translation moments (problematization, interessement, enrolment, mobilization) and obligatory passage points. SCAT has no element for them.
- Multiple enactments of one actant, and the mediator versus intermediary distinction.
- **Outcomes.** One tool decayed and was decommissioned; another is new. Edges carry no outcome, so this survives only in row notes and prose. A view will not show it.
- The operative versus constitutive layer, and the tensions between perspectives. Prose only.
- Paradigm versus instances: the doctrine is an affordance, the deployments are not coded.
- Any edge type for turning an affordance against its own configuration.

## What needed interpreting

- **Readings coded as concerns.** The inputs speak of perspectives, not groups, and a perspective is not a want. To hold a disagreement, the workers coded each reading as a concern ("how members figure in KOI", "what integration does to the protocol") and let two groups hold it.
- **Perspectives mapped to groups, then clustered to the cap.** Architectural perspective to technical-team, ethnographic to ethnographers; integration teams went into technical-team, Metagov members into community-members. Research collaborators and the implementation team have no group (the cap is full) and appear unlinked. Ethics committees stayed a group although they are an oversight gate; that is a judgement.
- **Two tools typed as affordances.** The chatbot and Ask Metagov are affordances because the inputs name no technology beneath them.
- **Architectures carry no technologies.** The three *is provided by* edges come only from two scenarios (the ethnographic loop and consent).
- **Scenario as nearest type.** koi-04, koi-05 and koi-06 tell no sequence of events.
- **All narratives are `past`.**
- **Edges marked as the worker's reading.** Two rows in parts-and-deployment carry "Reading:": the technical team holding "requisite variety", and the doctrine addressing it. Four concerns have no *is addressed by* edge: the two readings, "protocol design integrity" (the source does not say the doctrine or the chief engineer answers it) and the club-good integrity concern.

## What review taught

A review removed edges whose only support was that two things sit next to each other in the source. An edge is a claim the account tells, not a neighbourhood. Koi-08 tells no edge, and heterogeneous horizontal scaling is a linked affordance with no edge.

## What it means for the coding guide

1. **Clustering to a cap is a coding act.** With four groups, source perspectives, roles and teams must be folded. The guide should say that a fold is recorded in the narrative's own words (a "here part of" clause), because the tool will not.
2. **Readings versus wants.** A concern is not only what a group wants. Where sources record a difference of reading, coding it as a concern held by both groups works, but the guide should state it as a pattern and warn that the concern's name must be neutral.
3. **Outcomes live in notes.** An edge says a thing addresses a concern, not whether it worked. Tell coders to put outcomes in the row note and the prose, and to expect no view to show them.
4. **Silence is a result.** A concern with no *is addressed by* edge, or an architecture with no technology, is correct when the source says nothing; say so in "Thin spots", as these narratives do.

## Finding for the chief engineer

The tool now warns on a `done` narrative with no edges, as MISSION.md G1 says: `scat check` shows `SCAT-NOEDGES` on koi-08 (`narrative/the-data-set-and-the-two-layers.md`), a warning that does not block. It was a tool gap, found here and closed in the tool, not the vault's fault.

## What a field test would add

Real notes with real contradiction, a coder who attests `done`, and groups and concerns chosen by someone who was there.
