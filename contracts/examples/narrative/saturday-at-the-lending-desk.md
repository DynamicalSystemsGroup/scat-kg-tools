---
type: narrative
kind: scenario
status: done
title: "Saturday at the lending desk"
description: "Notes from the volunteer session on a busy open day."
timeframe: past
---

The queue was out of the door by ten. The [[volunteer-staff|volunteers]] on the desk wrote every loan in the book, because losing a tool is what they dread ([[careful-record-keeping]]). One [[borrowers|borrower]] took a saw without asking how the guard works, so a volunteer called him back and gave him the [[safety-briefing]]; everyone agreed [[safe-handling-of-tools|nobody should get hurt]]. Another walked off after ten minutes in line. The borrowers wanted [[quick-checkout]], and the [[self-checkout]] stand was the thing they asked for.

## Linked beyond the text

- [[funders]]

## Edges told

| type            | from                    | to                           | note                                       |
|-----------------|-------------------------|------------------------------|--------------------------------------------|
| holds           | [[volunteer-staff]]     | [[safe-handling-of-tools]]   | They saw the saw incident first-hand.      |
| holds           | [[borrowers]]           | [[safe-handling-of-tools]]   | Said in passing, after being called back.  |
| holds           | [[borrowers]]           | [[quick-checkout]]           | One left after ten minutes in the queue.   |
| holds           | [[volunteer-staff]]     | [[careful-record-keeping]]   | Every loan written in the book.            |
| is addressed by | [[quick-checkout]]      | [[self-checkout]]            | Asked for, not yet there.                  |
