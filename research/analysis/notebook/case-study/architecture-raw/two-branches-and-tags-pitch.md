---
type: architecture-raw
status: done
title: "Two branches and tags pitch"
description: "The pitch that two branches and archive tags give approved work, a safe rollback and kept findings."
coded:
  - "[[two-branches-and-tags-pitch-coded]]"
---

Pitch notes, as given. Source: the decision log, D-001, D-004, D-017, D-020 and D-022.

- One branch, main, holds approved missions and releases only. A second, dev, integrates the work. Work happens on short-lived branches off dev.
- Approval is a merge into main. A mission is approved when the project leads merge it.
- When work must be undone, dev is reverted to the approved state. History is kept, no force-push.
- Abandoned work is tagged under archive/ before it goes. The tags keep the findings available without seeding the restart.
- Branch tidy-up is periodic and advisory.
