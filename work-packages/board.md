# Board

Kept current by the PM. Units: one tight scope and one set of files each. Points use the scale 1, 2, 3, 5, 8.

## Packages

| WP | Title | State | Scope |
|---|---|---|---|
| WP1 | Ontology research sprint | approved | `WP1.md` |
| WP2 | Toolchain spike | approved | `WP2.md` |
| WP3 | Facilitation research spike | approved | `WP3.md` |
| WP4 | Ontology and page contracts | not yet scoped | — |
| WP5 | Conformance tools | not yet scoped | — |
| WP6 | Template and case study | not yet scoped | — |
| WP7 | Docs and Pages | not yet scoped | — |
| WP8 | Candidate and user acceptance | not yet scoped | — |

## Units

States: `queued` · `in flight` · `in review` · `done` · `blocked`. A queued or blocked unit says what it is waiting on.

Estimated points are set when a unit is planned and never revised. Realized points are scored on the same scale when
the unit lands, from what it actually took. The two are expected to differ, and the gap is how we learn to estimate.

| Unit | Actor (worker identity, model) | Est. pts | Realized pts | Branch | State | Waiting on | Done at | Basis for realized |
|---|---|---|---|---|---|---|---|---|
| WP1-U1 | ontology research engineer, sonnet | 3 | 5 | `wp1/u1` | done |  | 2026-11-23T15:43:09-05:00 | 1 push-back for a provenance mislabel; 2 reviews; about 5 min worker plus rework |
| WP1-U2 | ontology research engineer, sonnet | 3 | 3 | `wp1/u2` | done |  | 2026-11-23T15:26:15-05:00 | about 10 min worker, 60 tool calls, review passed first time with 4 minor nits; matches estimate |
| WP1-U3 | ontology designer, sonnet | 5 | 5 | `wp1/u3` | done |  | 2026-11-23T15:43:09-05:00 | 1 push-back (one defect disputed by worker, upheld as not a defect); about 10 min worker; heavy tool use |
| WP1-U4 | ontology designer, sonnet | 3 |  | `wp1/u4` | in flight |  |  |  |
| WP1-U5 | link-check reviewer, haiku | 1 |  | `wp1/u5` | queued | WP1-U4 merged |  |  |
| WP2-U1 | Python developer, sonnet | 5 | 3 | `wp2/u1` | done |  | 2026-11-23T15:26:15-05:00 | about 2.5 min worker, 14 tool calls, reviewer PASS first time; easier than estimated |
| WP2-U2 | Python developer, sonnet | 3 | 2 | `wp2/u2` | done |  | 2026-11-23T15:43:09-05:00 | about 2 min worker, first-time PASS, small scope |
| WP2-U3 | Python developer, sonnet | 3 | 3 | `wp2/u3` | done |  | 2026-11-23T15:43:09-05:00 | about 10 min worker, first-time PASS; mapping layer and sparql variant added work |
| WP2-U4 | Python developer, sonnet | 3 | 3 | `wp2/u4` | done |  | 2026-11-23T15:43:09-05:00 | about 3 min worker, first-time PASS; two parts (stack and R-13) |
| WP2-U5 | test engineer, sonnet | 2 | 2 | `wp2/u5` | done |  | 2026-11-23T15:43:09-05:00 | about 2 min worker, first-time PASS; lint nit left on dev, fix forward |
| WP2-U6 | test engineer and technical writer, sonnet | 3 |  | `wp2/u6` | in flight |  |  |  |
| WP3-U1 | research engineer, sonnet | 3 |  | `wp3/u1` | in review | reviewer |  |  |
| WP3-U2 | research engineer, sonnet | 3 | 3 | `wp3/u2` | done |  | 2026-11-23T15:43:09-05:00 | 1 push-back for citation errors (summariser-read sources); about 1 min plus rework |
| WP3-U3 | research engineer, sonnet | 2 |  | `wp3/u3` | in review | reviewer |  |  |
| WP3-U4 | technical writer, sonnet | 5 |  | `wp3/u4` | queued | WP3-U1 to U3 merged |  |  |

## Iterations and velocity

| Iteration | Units landed | Est. pts landed | Realized pts | Realized ÷ est. | Elapsed (wall clock) | Velocity (realized pts / hour) |
|---|---|---|---|---|---|---|

## Velocity and forecast

- **Raw counts first:** estimated points proposed (all planned units), estimated points of the completed units, and
  realized points of the completed units.
- **Raw velocity** for each iteration: realized points ÷ elapsed hours.
- **Smoothed velocity**, once there are at least 3 iterations *(default)*: an exponentially weighted moving average
  that weights recent iterations most, v̂ₙ = α·vₙ + (1 − α)·v̂ₙ₋₁, with α = 0.5 *(default)* and v̂₁ = v₁.
- **A forecast** to the candidate only once the smoothed velocity exists: (remaining estimated points × the running
  realized-to-estimated ratio) ÷ v̂. Before then, the board says so instead of forcing a number.

Current: 47 est. pts proposed; 30 est. pts completed; 29 realized pts completed; no iteration has closed yet.
