---
type: narrative
kind: scenario
status: draft
title: "Member organisations and the renewal"
description: "The community members who sign off the yearly renewal are staff of the member organisations, not the site's posters."
timeframe: past
---

Each year the [[community-members|community members]] who matter for the renewal are the staff of the beneficiary organisations. They do not post at the site. They hold the budget, and they read the yearly report to decide whether the platform is worth its share.

Their worry is [[vendor-lock-in|vendor lock-in]]: they want a reason to stay that is not only that leaving is hard. The other is [[renewal-cost-visibility|seeing what their share pays for]], which the [[shared-cost-report|shared cost report]] is meant to answer, built on the [[scheduler|scheduler]] that runs it each January.

## Edges told

| from | type | to | note |
|---|---|---|---|
| [[community-members]] | holds | [[vendor-lock-in]] | A reason to stay that is not only that leaving is hard. |
| [[community-members]] | holds | [[renewal-cost-visibility]] | What their share pays for. |
| [[renewal-cost-visibility]] | is addressed by | [[shared-cost-report]] |  |
| [[shared-cost-report]] | is provided by | [[scheduler]] | Runs each January. |
