---
type: narrative
kind: architecture
status: done
title: "What KOI is and the RID"
description: "KOI is a protocol for organising knowledge where authority is scoped, and the RID is the stable handle that keeps a resource referable across subnets without a single source of truth."
timeframe: past
---

Source: research/range/koi/inputs/koi-07-what-koi-is-and-the-rid.md

Architectural view. KOI stands for Knowledge Organization Infrastructure: a protocol for organising knowledge where authority is scoped, running across subnets and coordinator nodes. The [[koi-doctrine|KOI doctrine]] frames the assembly in terms of "ASoT" and "MOSA" (the source uses the abbreviations without spelling them out) and sets it against two things, a single source of truth and a walled garden. It is explicitly neither. The infrastructure performs six functions of identification, which the source names as a set but does not list.

It works over Resource Identifiers. The [[resource-identifier|RID]] is the stable handle the infrastructure assigns so that a resource can be referenced, related, updated and forgotten across subnets without a single source of truth: the concern is that [[resources-referable-across-subnets|resources stay referable across subnets]]. Alongside the handle the infrastructure carries three FUN signals: new, update and [[forget-signal|forget]]. The forget signal is the one that figures in the forget incident.

The doctrine also names per-relationship discipline; the source gives no more of it.

This is read as the baseline, what exists: the account is in the present tense of a thing that is there.

Thin spots: the source lists neither the six functions nor the detail of per-relationship discipline, and says nothing of ASoT and MOSA beyond the abbreviations. It names subnets and coordinator nodes as where KOI runs but does not say that they, or anything else, provide the RID, so no technology is coded. It names no group, and the doctrine is linked here but no edge is coded for it, since the source says it frames the assembly and not that it addresses a concern. The FUN signals (new, update, forget) are listed beside the RID, not tied to it: the forget signal is linked but no edge is coded for it, and the new and update signals have no node of their own.

## Edges told

| type | from | to | note |
|---|---|---|---|
| is addressed by | [[resources-referable-across-subnets]] | [[resource-identifier]] | The RID is the stable handle so a resource can be referenced, related, updated and forgotten without a single source of truth. |
