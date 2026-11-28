---
type: narrative
status: draft
title: "F4 prose, all linked"
---

On Saturday the [[volunteer-staff|volunteers]] on the desk wrote every loan in the book. [[borrowers]] queued for a long time and one walked off, wanting [[quick-checkout]]. A volunteer called a man back to give him the [[safety-briefing]], because [[safe-handling-of-tools|nobody should get hurt]]. People asked for a [[self-checkout]] stand, which would need the [[booking-app]] and a [[barcode-scanner]].

## Edges told

| from | type | to | note |
|---|---|---|---|
| [[borrowers]] | holds | [[quick-checkout]] | Left after ten minutes in line. |
| [[volunteer-staff]] | holds | [[safe-handling-of-tools]] | Saw the saw incident. |
| [[quick-checkout]] | is addressed by | [[self-checkout]] | Asked for. |
| [[safe-handling-of-tools]] | is addressed by | [[safety-briefing]] | Given at the desk. |
| [[self-checkout]] | is provided by | [[booking-app]] | Keeps the loan record. |
| [[self-checkout]] | is provided by | [[barcode-scanner]] | Reads the label. |
