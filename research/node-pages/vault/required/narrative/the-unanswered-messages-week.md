---
type: narrative
kind: scenario
status: draft
title: "The unanswered messages week"
description: "One week in which the opening messages of a round went unanswered and the reminder was tried for the first time."
timeframe: past
attributed_to: ["[[lab-member-c]]"]
---

In the week the round opened, the [[ethnographers]] counted the [[unanswered-direct-messages|messages that went unanswered]] and stopped counting at thirty. They had expected a few. Because the [[closing-the-loop|loop]] depends on members answering first, a silent inbox meant the whole round could not begin.

On the Thursday they switched on the [[direct-message-reminder|reminder]], which the [[forum-bot|forum bot]] sent to everyone who had not replied. By Sunday about half of the thirty had answered. The ethnographers read this as the reminder working, and wrote it into [[telescope|Telescope]] so that the next round would start from it.

## Edges told

| from | type | to | note |
|---|---|---|---|
| [[ethnographers]] | holds | [[closing-the-loop]] | The loop depends on members answering first. |
| [[closing-the-loop]] | is addressed by | [[durable-shared-records]] | Written up for the next round. |
| [[durable-shared-records]] | is provided by | [[telescope]] |  |
| [[ethnographers]] | holds | [[unanswered-direct-messages]] | Counted to thirty and stopped. |
| [[unanswered-direct-messages]] | is addressed by | [[direct-message-reminder]] | About half answered by Sunday. |
| [[direct-message-reminder]] | is provided by | [[forum-bot]] |  |
