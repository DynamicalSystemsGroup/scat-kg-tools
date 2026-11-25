---
type: narrative
kind: architecture
status: done
title: "Parts and deployment"
description: "KOI is a paradigm written in the doctrine and played out in many deployments, and the doctrine counts the pull toward homogenisation as its main threat to requisite variety."
timeframe: past
---

Source: research/range/koi/inputs/koi-09-parts-and-deployment.md

Architectural view. The [[koi-doctrine|KOI doctrine]] names the groups around KOI, most with a place in its appendix. Research collaborators supply the requirements and conceptual framing and are material to forming the doctrine. The implementation team turns the doctrine into running protocol code. Integration teams, here part of the [[technical-team|technical team]], adapt and deploy KOI at specific field sites. Beneficiary organisations and their members, here the [[community-members|community members]], are those KOI serves. The chief engineer, also part of the technical team, is the role accountable for the coherence of the protocol as a whole and speaks for its design integrity: [[protocol-design-integrity|the protocol's design integrity]].

The doctrine separates the paradigm from its instances. The paradigm is written in the doctrine; the instances are the deployments. The paradigm lasts because instances exist, persist and get used, and they should differ meaningfully while looking alike, so KOI is understood as a pattern language and not a single product.

The doctrine counts the main threat as the pull toward homogenisation. It values [[requisite-variety|requisite variety]], and standardisation toward single objectives threatens it, so defending variety takes steady, active advocacy. Decommissioning is not a threat: the doctrine takes a lifecycle view, in which an instance arises from a need and is later evolved or retired, and a well-timed, graceful replacement is on-program. The chief engineer pushes for the paradigm to be understood and adopted, not for any one substrate, which the architectural source calls [[heterogeneous-horizontal-scaling|heterogeneous horizontal scaling]].

This is read as the baseline, what exists: the doctrine and its deployments are there.

Thin spots: the implementation team and research collaborators are named by the input but have no group in the vault (cap 4 is full), so they are named without links. The paradigm and instances distinction and the lifecycle and decommissioning view are not coded, and [[heterogeneous-horizontal-scaling|heterogeneous horizontal scaling]] is linked but tied to adoption in the source, not to variety, so no edge is coded for it. Community members are linked and hold nothing here. The source does not say what variety is protected from, beyond standardisation, nor which substrates are meant, so no technology is coded. It does not say that the doctrine or the chief engineer's push is what answers the coherence concern, so that concern has no "is addressed by" edge. The two rows marked "Reading:" are the worker's reading (a worker standing in for the coder), not something a sentence says.

## Edges told

| type | from | to | note |
|---|---|---|---|
| holds | [[technical-team]] | [[protocol-design-integrity]] | The chief engineer is accountable for the protocol's coherence as a whole. |
| holds | [[technical-team]] | [[requisite-variety]] | Reading: the worker's reading, standing in for the coder. No sentence names who holds this; the chief engineer's push for the paradigm and not any one substrate is read as the technical team holding it. |
| is addressed by | [[requisite-variety]] | [[koi-doctrine]] | Reading: the worker's reading, standing in for the coder. The doctrine holds the value and separates paradigm from instances; the source does not say it answers the concern. |
