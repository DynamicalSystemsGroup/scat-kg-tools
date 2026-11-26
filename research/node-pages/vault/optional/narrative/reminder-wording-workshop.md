---
type: narrative
kind: scenario
status: draft
title: "Reminder wording workshop"
description: "The working group spent an afternoon on the wording of the reminder for members who had not answered."
timeframe: past
---

The [[ethnographers]] spent an afternoon on the wording of the [[direct-message-reminder|reminder]]. They had two names for the trouble it addressed, [[members-not-replying|members not replying]] and [[unanswered-direct-messages|unanswered direct messages]], and agreed the reminder should not scold either way. The [[forum-bot|forum bot]] would send whatever text they settled on.

## Edges told

| from | type | to | note |
|---|---|---|---|
| [[ethnographers]] | holds | [[members-not-replying]] |  |
| [[ethnographers]] | holds | [[unanswered-direct-messages]] |  |
| [[members-not-replying]] | is addressed by | [[direct-message-reminder]] |  |
| [[unanswered-direct-messages]] | is addressed by | [[direct-message-reminder]] |  |
| [[direct-message-reminder]] | is provided by | [[forum-bot]] | Sends whatever text they settle on. |
