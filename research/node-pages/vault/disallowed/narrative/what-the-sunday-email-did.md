---
type: narrative
kind: scenario
status: draft
title: "What the Sunday email did"
description: "The emailed digest reached members who never opened the forum, with mixed results."
timeframe: past
---

The [[digest-email|digest email]] reached some members who never opened the forum. It went out through the [[mail-relay|mail relay]], and a few weeks in the relay marked a batch as junk. The working group did not find out until a member mentioned it. For [[members-lose-the-thread|members who lose the thread]], the email was the only summary they saw, since the posted [[weekly-digest|weekly digest]] never reached their inbox.

## Edges told

| from | type | to | note |
|---|---|---|---|
| [[members-lose-the-thread]] | is addressed by | [[digest-email]] | Only summary some members saw. |
| [[digest-email]] | is provided by | [[mail-relay]] | A batch was marked as junk. |
