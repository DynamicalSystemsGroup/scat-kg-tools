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
| 1 | WP1-U1, WP1-U2, WP1-U3, WP2-U1, WP3-U1, WP3-U2, WP3-U3 | 24 | 27 | 1.12 | 0.66 h | 40.9 |
| 2 | WP2-U2, WP2-U3, WP2-U4, WP2-U5 | 11 | 10 | 0.91 | 0.41 h | 24.4 |

## Velocity and forecast

- **Raw counts first:** estimated points proposed (all planned units), estimated points of the completed units, and
  realized points of the completed units.
- **Raw velocity** for each iteration: realized points ÷ elapsed hours.
- **Smoothed velocity**, once there are at least 3 iterations *(default)*: an exponentially weighted moving average
  that weights recent iterations most, v̂ₙ = α·vₙ + (1 − α)·v̂ₙ₋₁, with α = 0.5 *(default)* and v̂₁ = v₁.
- **A forecast** to the candidate only once the smoothed velocity exists: (remaining estimated points × the running
  realized-to-estimated ratio) ÷ v̂. Before then, the board says so instead of forcing a number.

Current: 47 est. pts proposed; 35 est. pts completed; 37 realized pts completed; 2 iterations closed, so no smoothed velocity and no forecast yet. Iterations overlap in wall-clock time (units were dispatched while earlier ones were in review), so the raw velocities are noisy.
