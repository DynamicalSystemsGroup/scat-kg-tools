# Metrics log

`metrics.jsonl` is an append-only JSON Lines log of the planning data: one JSON object per line, never edited or
reordered. The PM is its only writer, and appends a record at every unit state change and at every iteration close.
It is read for the chief engineer's own analysis, for example:

```python
import pandas as pd
m = pd.read_json("work-packages/metrics.jsonl", lines=True)
units = m[m.kind == "unit"]
iterations = m[m.kind == "iteration"]
```

## Record kinds

Every record has `ts` (ISO 8601 with timezone) and `kind`.

**`unit`**: a unit was planned, or changed state.

| Field | Type | Meaning |
|---|---|---|
| `wp` | str | Work package, e.g. `"WP1"` |
| `unit` | str | Unit id, e.g. `"WP1-U2"` |
| `actor` | str | Worker identity, e.g. `"ontology research engineer"` |
| `model` | str | `"sonnet"`, `"haiku"` or `"opus"` |
| `state` | str | `queued`, `in flight`, `in review`, `done` or `blocked` |
| `est_pts` | int | Estimated points, set at planning and never changed |
| `realized_pts` | int or null | Set only on the record where `state` is `done` |
| `basis` | str or null | One line on how the realized points were scored |
| `waiting_on` | str or null | For `queued` or `blocked` units: what they wait on |
| `iteration` | int or null | The iteration the unit landed in (set when `done`) |

**`iteration`**: an iteration closed.

| Field | Type | Meaning |
|---|---|---|
| `iteration` | int | 1, 2, 3, … |
| `units` | list[str] | Units that landed in it |
| `est_pts` | int | Estimated points of those units |
| `realized_pts` | int | Realized points of those units |
| `elapsed_h` | float | Wall-clock hours from the iteration's start to its close |
| `velocity` | float | `realized_pts / elapsed_h` |

The smoothed velocity and the forecast are derived from these records, not stored, so the log holds only
observations. The method is in `board.md`, under "Velocity and forecast".
