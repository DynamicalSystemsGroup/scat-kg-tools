# Board

Kept current by the PM. Units: one tight scope and one set of files each. Points use the scale 1, 2, 3, 5, 8.

## Packages

| WP | Title | State | Scope |
|---|---|---|---|
| WP1 | Ontology research sprint | accepted | `WP1.md` |
| WP2 | Toolchain spike | accepted | `WP2.md` |
| WP3 | Facilitation research spike | accepted | `WP3.md` |
| WP4 | Ontology and page contracts | approved | `WP4.md` |
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
| WP1-U4 | ontology designer, sonnet | 3 | 5 | `wp1/u4` | done |  | 2026-11-23T16:00:21-05:00 | 1 push-back plus a fix-forward from the link check; 3 review passes; about 12 min worker total |
| WP1-U5 | link-check reviewer, haiku | 1 | 2 | `wp1/u5` | done |  | 2026-11-23T16:00:21-05:00 | review-only unit (no merge); Haiku link checker found 4 real disclosure and quote items; ~2 min |
| WP2-U1 | Python developer, sonnet | 5 | 3 | `wp2/u1` | done |  | 2026-11-23T15:26:15-05:00 | about 2.5 min worker, 14 tool calls, reviewer PASS first time; easier than estimated |
| WP2-U2 | Python developer, sonnet | 3 | 2 | `wp2/u2` | done |  | 2026-11-23T15:43:09-05:00 | about 2 min worker, first-time PASS, small scope |
| WP2-U3 | Python developer, sonnet | 3 | 3 | `wp2/u3` | done |  | 2026-11-23T15:43:09-05:00 | about 10 min worker, first-time PASS; mapping layer and sparql variant added work |
| WP2-U4 | Python developer, sonnet | 3 | 3 | `wp2/u4` | done |  | 2026-11-23T15:43:09-05:00 | about 3 min worker, first-time PASS; two parts (stack and R-13) |
| WP2-U5 | test engineer, sonnet | 2 | 2 | `wp2/u5` | done |  | 2026-11-23T15:43:09-05:00 | about 2 min worker, first-time PASS; lint nit left on dev, fix forward |
| WP2-U6 | test engineer and technical writer, sonnet | 3 | 3 | `wp2/u6` | done |  | 2026-11-23T16:00:21-05:00 | first-time PASS; reran all benches and messages; about 10 min worker |
| WP3-U1 | research engineer, sonnet | 3 | 3 | `wp3/u1` | done |  | 2026-11-23T15:50:36-05:00 | 2 push-backs (name hardening; typo and history squash); small reading unit |
| WP3-U2 | research engineer, sonnet | 3 | 3 | `wp3/u2` | done |  | 2026-11-23T15:43:09-05:00 | 1 push-back for citation errors (summariser-read sources); about 1 min plus rework |
| WP3-U3 | research engineer, sonnet | 2 | 5 | `wp3/u3` | done |  | 2026-11-23T15:50:36-05:00 | 3 rounds: two near-verbatim review failures and rewrites, squash; Drive connector worked first time |
| WP3-U4 | technical writer, sonnet | 5 | 5 | `wp3/u4` | done |  | 2026-11-23T16:00:21-05:00 | 1 push-back (one wrong citation, privacy hardening) plus a re-review with the private brief |
| WP4-U1 | ontology designer, sonnet | 5 | 8 | `wp4/u1` | done |  | 2026-11-23T16:25:01-05:00 | rework after D-030 (relations as page types, namespace); 2 push-backs, 3 review passes; about 25 min worker |
| WP4-U2 | page-contract designer, sonnet | 5 | 8 | `wp4/u2` | done |  | 2026-11-23T16:48:41-05:00 | reworked for D-030 and D-031; 3 push-backs, 3 reviews; spec-heavy |
| WP4-U3 | rule-catalogue author, sonnet | 5 | 8 | `wp4/u3` | done |  | 2026-11-23T16:53:33-05:00 | reworked for D-030 and D-031; 4 push-backs, 4 reviews; last round checked by PM re-run, cross-read left to U6 |
| WP4-U4 | technical writer, sonnet | 3 | 3 | `wp4/u4` | done |  | 2026-11-23T17:03:08-05:00 | first-time pass; independent checker 0 errors; matches estimate |
| WP4-U5 | cold-write tester, haiku | 3 | 3 | `wp4/u5` | done |  | 2026-11-23T17:03:08-05:00 | 29 conformant pages from the two contracts alone; defects fed to U8; no branch (scratch output) |
| WP4-U6 | cross-check reviewer, sonnet | 3 | 3 | `wp4/u6` | done |  | 2026-11-23T17:03:08-05:00 | R3, R5, R7, R8 pass; 9 defects found; no branch (read-only) |
| WP4-U7 | cold-write rerun tester, haiku | 2 |  | `wp4/u7` | queued | WP4-U8 merged |  |  |
| WP4-U8 | contract fixer (TBox, contracts, catalogue), sonnet | 3 |  | `wp4/u8` | in flight |  |  | unplanned: fixes the 9 defects from U6 and U5; added by PM |

## Iterations and velocity

| Iteration | Units landed | Est. pts landed | Realized pts | Realized ÷ est. | Elapsed (wall clock) | Velocity (realized pts / hour) |
|---|---|---|---|---|---|---|
| 1 | WP1-U1, WP1-U2, WP1-U3, WP2-U1, WP3-U1, WP3-U2, WP3-U3 | 24 | 27 | 1.12 | 0.66 h | 40.9 |
| 2 | WP2-U2, WP2-U3, WP2-U4, WP2-U5 | 11 | 10 | 0.91 | 0.41 h | 24.4 |
| 3 | WP1-U4, WP1-U5, WP2-U6, WP3-U4 | 12 | 15 | 1.25 | 0.16 h | 93.8 |

## Velocity and forecast

- **Raw counts first:** estimated points proposed (all planned units), estimated points of the completed units, and
  realized points of the completed units.
- **Raw velocity** for each iteration: realized points ÷ elapsed hours.
- **Smoothed velocity**, once there are at least 3 iterations *(default)*: an exponentially weighted moving average
  that weights recent iterations most, v̂ₙ = α·vₙ + (1 − α)·v̂ₙ₋₁, with α = 0.5 *(default)* and v̂₁ = v₁.
- **A forecast** to the candidate only once the smoothed velocity exists: (remaining estimated points × the running
  realized-to-estimated ratio) ÷ v̂. Before then, the board says so instead of forcing a number.

Current: 47 est. pts proposed (WP1 to WP3 only; WP4 to WP8 are not scoped, so not estimated); 47 est. pts completed; 52 realized pts completed. 3 iterations closed; running realized/estimated ratio 1.11; raw velocities [40.9, 24.4, 93.8]; smoothed velocity v-hat 63.2 realized pts/hour. Forecast: not stated as a number, because the remaining estimated points do not exist yet (WP4 to WP8 have no scopes); see the report to the ACE for the formula applied to an assumed size. Iterations overlap in wall-clock time and the workers are fast, so the velocity is noisy and likely far above what a gated pace will sustain.
