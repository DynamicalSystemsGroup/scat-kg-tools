---
type: narrative
kind: architecture
status: done
title: "Self-service kiosk pitch"
description: "A pitch for a kiosk where a borrower scans a tool and records the loan alone."
timeframe: future
---

A kiosk at the door gives [[quick-checkout]]: the borrower scans the tool with a [[barcode-scanner]] and the [[booking-app]] records the loan, which is the [[self-checkout]]. The kiosk shows a [[safety-briefing]] before it releases a tool, so a borrower still hears how it works, which is what [[safe-handling-of-tools]] asks.

## Edges told

| type | from | to | note |
|---|---|---|---|
| addressed-by | [[quick-checkout]] | [[self-checkout\|the kiosk]] | Would cut the queue to a scan. |
| addressed-by | [[safe-handling-of-tools]] | [[safety-briefing]] | The kiosk shows it on screen first. |
| provided-by | [[self-checkout]] | [[booking-app]] | The app keeps the loan record. |
| provided-by | [[self-checkout]] | [[barcode-scanner]] | Identifies the tool by its label. |
