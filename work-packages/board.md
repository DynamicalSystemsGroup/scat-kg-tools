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
| WP1-U1 | ontology research engineer, sonnet | 3 | | `wp1/u1` | in review | reviewer | | |
| WP1-U2 | ontology research engineer, sonnet | 3 | | `wp1/u2` | in review | reviewer | | |
| WP1-U3 | ontology designer, sonnet | 5 | | `wp1/u3` | in review | reviewer | | |
| WP1-U4 | ontology designer, sonnet | 3 | | `wp1/u4` | queued | WP1-U1, U2, U3 merged | | |
| WP1-U5 | link-check reviewer, haiku | 1 | | `wp1/u5` | queued | WP1-U4 merged | | |
| WP2-U1 | Python developer, sonnet | 5 | | `wp2/u1` | in review | reviewer | | |
| WP2-U2 | Python developer, sonnet | 3 | | `wp2/u2` | queued | WP2-U1 merged | | |
| WP2-U3 | Python developer, sonnet | 3 | | `wp2/u3` | queued | WP2-U1 merged | | |
| WP2-U4 | Python developer, sonnet | 3 | | `wp2/u4` | queued | WP2-U1 merged | | |
| WP2-U5 | test engineer, sonnet | 2 | | `wp2/u5` | queued | WP2-U1 merged | | |
| WP2-U6 | test engineer and writer, sonnet | 3 | | `wp2/u6` | queued | WP2-U2 to U5 merged | | |
| WP3-U1 | research engineer, sonnet | 3 | | `wp3/u1` | in review | reviewer | | |
| WP3-U2 | research engineer, sonnet | 3 | | `wp3/u2` | in review | reviewer | | |
| WP3-U3 | research engineer, sonnet | 2 | | `wp3/u3` | in review | reviewer | | |
| WP3-U4 | technical writer, sonnet | 5 | | `wp3/u4` | queued | WP3-U1, U2, U3 merged | | |

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

Current: no iterations have landed yet.
