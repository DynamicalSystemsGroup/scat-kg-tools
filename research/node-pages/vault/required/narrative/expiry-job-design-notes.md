---
type: narrative
kind: architecture
status: draft
title: "Expiry job design notes"
description: "Notes on how the platform removes records that pass their age limit."
timeframe: future
attributed_to: ["[[lab-member-a]]"]
---

The [[technical-team|technical team]] needs a [[data-retention-schedule|schedule]] for removing records that pass their age limit. The plan is an [[auto-expiry-job|auto-expiry job]] that runs nightly and removes what is due. It would run on the [[scheduler|scheduler]], which the team already uses for backups.

Open question: whether the job keeps a log of what it removed. The team has not settled this.

## Edges told

| from | type | to | note |
|---|---|---|---|
| [[technical-team]] | holds | [[data-retention-schedule]] |  |
| [[data-retention-schedule]] | is addressed by | [[auto-expiry-job]] | Nightly run. |
| [[auto-expiry-job]] | is provided by | [[scheduler]] | Already used for backups. |
