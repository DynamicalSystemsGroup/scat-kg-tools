---
type: narrative
kind: architecture
status: done
title: "Sensor first pitch"
description: "A pitch to instrument the network and react fast."
---

[[smart-meter-network|Sensors on the mains]] and [[reservoir-level-gauges|at the river]] feed [[sensor-telemetry-platform|one platform]]. [[leak-alert-notifications|Alerts]] go out by [[sms-gateway|text]]. Crews work from an [[emergency-repair-roster|on-call list]].

## Linked beyond the text

- [[quick-leak-response]]
- [[minimal-service-interruptions]]
- [[drought-supply-security]]
- [[environmental-flow-protection]]
- [[river-flow-display]]

## Edges told

| type | from | to | note |
|---|---|---|---|
| is addressed by | [[environmental-flow-protection]] | [[river-flow-display]] | A partial answer so far. |
| is addressed by | [[minimal-service-interruptions]] | [[emergency-repair-roster]] | Helps in most cases. |
| is addressed by | [[minimal-service-interruptions]] | [[leak-alert-notifications]] | Works when used as intended. |
| is addressed by | [[quick-leak-response]] | [[emergency-repair-roster]] | Covers part of the concern. |
| is addressed by | [[quick-leak-response]] | [[leak-alert-notifications]] | Works when used as intended. |
| is provided by | [[emergency-repair-roster]] | [[sensor-telemetry-platform]] | Relies on it for the core function. |
| is provided by | [[emergency-repair-roster]] | [[sms-gateway]] | Provided by this part today. |
| is provided by | [[leak-alert-notifications]] | [[sensor-telemetry-platform]] | Relies on it for the core function. |
| is provided by | [[leak-alert-notifications]] | [[smart-meter-network]] | Provided by this part today. |
| is provided by | [[leak-alert-notifications]] | [[sms-gateway]] | Relies on it for the core function. |
| is provided by | [[river-flow-display]] | [[reservoir-level-gauges]] | One of the parts that deliver it. |
| is provided by | [[river-flow-display]] | [[sensor-telemetry-platform]] | Relies on it for the core function. |
