# Board

Kept current by the PM. Units: one tight scope and one set of files each. Points use the scale 1, 2, 3, 5, 8.

## Packages

| WP | Title | State | Scope |
|---|---|---|---|
| WP1 | Ontology research sprint | accepted | `WP1.md` |
| WP2 | Toolchain spike | accepted | `WP2.md` |
| WP3 | Facilitation research spike | accepted | `WP3.md` |
| WP4 | Ontology and page contracts | accepted | `WP4.md` |
| WP5 | Conformance tools | accepted | `WP5.md` |
| WP6 | Template and case study | accepted | `WP6.md` |
| WP7 | Docs and Pages | accepted | `WP7.md` |
| WP8 | Candidate and user acceptance | approved | `WP8.md` |

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
| WP4-U7 | cold-write rerun tester, haiku | 2 | 2 | `wp4/u7` | done |  | 2026-11-23T17:09:44-05:00 | fresh Haiku, new domain: 29 pages, 0 errors; no branch (scratch output) |
| WP4-U8 | contract fixer, sonnet | 3 | 3 | `wp4/u8` | done |  | 2026-11-23T17:09:44-05:00 | unplanned fix unit for the 9 review defects; 1 push-back, 2 reviews; added by PM |
| WP5-U1 | Python developer (packaging, CI, TBox loader), sonnet | 5 | 5 | `wp5/u1` | done |  | 2026-11-23T17:22:50-05:00 | first-time review PASS; about 3 min worker plus 1 min review; matches estimate |
| WP5-U2 | Python developer (vault reader), sonnet | 5 | 5 | `wp5/u2` | done |  | 2026-11-23T17:53:23-05:00 | 1 push-back (non-string type crashed the reader), 2 reviews; about 8 min worker plus rework; matches estimate |
| WP5-U3 | Python developer (checks), sonnet | 8 | 8 | `wp5/u3` | done |  | 2026-11-23T17:53:23-05:00 | 27 rules, 244 tests, first-time review PASS; about 18 min worker; matches estimate |
| WP5-U4 | Python developer (operations), sonnet | 8 | 8 | `wp5/u4` | done |  | 2026-11-23T17:53:23-05:00 | 90 tests, first-time review PASS; about 7 min worker; 12 contract gaps flagged; matches estimate |
| WP5-U5 | Python developer (CLI and API), sonnet | 3 | 8 | `wp5/u5` | done |  | 2026-11-23T20:10:59-05:00 | blocked by the permission guard, then D-035 authorisation and D-036 scope change; fixture edits to 10 assertions, 2 reviews; absorbed the INDEX-STALE rule and an integration fix (U10); ran over |
| WP5-U6 | test engineer, sonnet | 3 | 3 | `wp5/u6` | done |  | 2026-11-23T20:10:59-05:00 | first-time review PASS; reviewer caught 5 of 5 mutations; matches estimate |
| WP5-U7 | clean-install tester, haiku | 2 | 2 | none (scratch) | done |  | 2026-11-23T20:10:59-05:00 | two Haiku runs (before and after fixes); first run found 2 findings fed to U8; second run clean with no fix steps; matches estimate |
| WP5-U10 | Python developer (integration fix), sonnet | 1 | 1 | `wp5/u10` | done |  | 2026-11-23T20:10:59-05:00 | unplanned: one test assertion adjusted after SCAT-INDEX-STALE landed; PM re-ran the suite (no separate review for a three-line change) |
| WP5-U9 | Python developer (reader exclusion, D-034), sonnet | 1 | 1 | `wp5/u9` | done |  | 2026-11-23T17:53:23-05:00 | unplanned unit added by PM after ruling D-034; first-time PASS; small |
| WP5-U8 | fixer, sonnet | 3 | 5 | `wp5/u8` | done |  | 2026-11-23T20:10:59-05:00 | planned fix unit; scope grew by D-035 items 1 to 3 (TBox labels, marker wording, empty type) plus help text; first-time review PASS; replanned estimate 5 |
| WP6-U1 | template designer, sonnet | 5 | 5 | `wp6/u1` | done |  | 2026-11-23T17:53:23-05:00 | 1 amendment for D-034 (templates_folder key); first-time review PASS; about 3 min worker; matches estimate |
| WP6-U2 | case-study writer, sonnet | 8 | 8 | `wp6/u2` | done |  | 2026-11-23T20:10:59-05:00 | 28 pages, 12 quotes traced verbatim, first-time review PASS; 5 items flagged for the ACE; matches estimate |
| WP6-U3 | technical writer, sonnet | 2 | 3 | `wp6/u3` | done |  | 2026-11-23T20:10:59-05:00 | 1 push-back (7 README items), 2 reviews; ran over by one |
| WP6-U4 | Python developer (pin and CI), sonnet | 3 | 2 | `wp6/u4` | done |  | 2026-11-23T20:10:59-05:00 | first-time review PASS; small config; under estimate |
| WP6-U5 | mechanical checker, haiku | 2 | 2 | none (scratch) | done |  | 2026-11-23T20:10:59-05:00 | first-time review PASS; matches estimate |
| WP6-U6 | fixer, sonnet | 3 | 2 | `wp6/u6` | done |  | 2026-11-23T20:10:59-05:00 | planned fix unit; the re-pin needed no page fixes; verified by the clean-environment unit; under estimate |
| WP6-U7 | clean-environment tester, haiku | 2 | 2 | none (scratch) | done |  | 2026-11-23T20:10:59-05:00 | README path ran as written from 'uv installed' on; install, gh and web paths not exercised (no download permission); matches estimate |
| WP6-U8 | case-study editor, sonnet | 3 | | `wp6/u8` | done | | 2026-11-23T20:21:00-05:00 | fix unit for D-037; 2 push-backs (near-verbatim echoes, then clause-structure echoes), 3 fresh reviews; merged to template `dev` at f446a02; about 7 min |
| WP7-U1 | Python developer (mkdocs skeleton, docs group, CI), sonnet | 3 | 3 | `wp7/u1` | done |  | 2026-11-23T20:26:03-05:00 | first-time review PASS (build, tests, browser at desktop and 375 px); the brief said 9 pages, the nav has 8; matches estimate |
| WP7-U2 | technical writer (home and getting started), sonnet | 5 | 5 | `wp7/u2` | done |  | 2026-11-23T20:56:20-05:00 | 1 push-back (6 literal-reader gaps), 2 fresh reviews, browser checked at desktop and 375 px; matches estimate |
| WP7-U3 | technical writer (planning and facilitation guides), sonnet | 8 | 8 | `wp7/u3` | done |  | 2026-11-23T20:56:20-05:00 | 1 push-back (6 items: a turned-away story, who writes, real outputs, links), 2 reviews; long spec-heavy pages; matches estimate |
| WP7-U4 | technical writer (coding guide), sonnet | 5 | 8 | `wp7/u4` | done |  | 2026-11-23T21:10:17-05:00 | 3 push-backs and 4 fresh reviews: shown outputs were not real for the stub-made raw page, then the messages shared state; settled by a PM ruling (each message starts from a fresh copy and states its start); 32 runnable steps; ran over by 3 |
| WP7-U5 | technical writer (API and CLI reference), sonnet | 5 | 5 | `wp7/u5` | done |  | 2026-11-23T20:56:20-05:00 | 1 push-back (tab outputs not true in page order, reserved-name row), 2 reviews, help diff byte-exact; matches estimate |
| WP7-U6 | test engineer (docs test), sonnet | 5 | 5 | `wp7/u6` | done |  | 2026-11-23T20:56:20-05:00 | 1 push-back (3 pinning tests accepted from review), mutation-checked by two reviewers, red on the placeholder reference until U5 merged by design; matches estimate |
| WP7-U7 | technical writer (jazz style and visual assets), sonnet | 3 | 3 | `wp7/u7` | done |  | 2026-11-23T21:24:28-05:00 | 1 push-back (illegible bandstand at 375 px, opaque musical terms, 'score' near a no-scoring disclaimer, jazz cue), 2 reviews; byte-exact proof that no code block, heading or tip changed; ran at estimate |
| WP7-U8 | fixer (planned fix unit), sonnet | 5 | 8 | `wp7/u8` | done |  | 2026-11-23T21:44:56-05:00 | planned fix unit for the two Haiku reads; 3 rounds (round 1 from the reads, round 2 from the reruns incl. a real defect: <group> swallowed as an HTML tag, round 3 residuals), 2 fresh reviews; ran over by 3 |
| WP7-R6 | clarity-read tester, haiku, haiku | 2 | 3 | none (scratch) | done |  | 2026-11-23T21:44:56-05:00 | 2 reads (first plus a fresh rerun on the fixed pages): both reached a clean whole-vault check with no blocking finding; first run 6 non-blocking guesses (fixed or accepted), second run 6 (mostly test-setup artefacts: the scratch pin change staged by 'git add .', and having only two of the pages); install, gh and website paths and Obsidian not exercised |
| WP7-R5 | cold-read tester, haiku, haiku | 2 | 5 | none (scratch) | done |  | 2026-11-23T21:44:56-05:00 | 4 reads in all (first read plus 3 fresh reruns): every read named jazz or improvisation unprompted (the text carries the word jazz in one plain sentence per guide); each read still listed 5 to 7 minor places where a phrase left an instruction less than plain, fewer each time (7, 7, 5); no blocking item; ACE to judge whether R5's 'no place' is met |
| WP8-U1 | Python developer (operations fixes), sonnet | 5 |  | `wp8/u1` | in flight |  |  |  |
| WP8-U2 | Python developer (message fixes), sonnet | 5 |  | `wp8/u2` | in flight |  |  |  |
| WP8-U3 | technical writer (docs sync), sonnet | 3 |  | `wp8/u3` | queued | U1 and U2 |  |  |
| WP8-U4 | technical writer (template README), sonnet | 2 |  | `wp8/u4` | in flight |  |  |  |
| WP8-U5 | Python developer (Pages workflow and banner), sonnet | 3 |  | `wp8/u5` | in flight |  |  |  |
| WP8-U6 | test engineer and technical writer (UA-A kit), sonnet | 8 |  | `wp8/u6` | in flight |  |  |  |
| WP8-U7 | technical writer (walkthrough script), sonnet | 5 |  | `wp8/u7` | in flight |  |  |  |
| WP8-U8 | Python developer (candidate pins), sonnet | 3 |  | `wp8/u8` | queued | U1 to U5 merged |  |  |
| WP8-U9 | mechanical checker (clean clone), haiku | 2 |  | `wp8/u9` | queued | U8 and the ACE's settings |  |  |
| WP8-U10 | UA-A round 1 testers, haiku | 12 |  | `wp8/u10` | queued | U6, U9 |  |  |
| WP8-U11 | fixer (planned, after round 1), sonnet | 8 |  | `wp8/u11` | queued | U10 |  |  |
| WP8-U12 | re-pin and rerun, sonnet | 2 |  | `wp8/u12` | queued | U11 |  |  |
| WP8-U13 | UA-A round 2 testers, haiku | 12 |  | `wp8/u13` | queued | U12 |  |  |
| WP8-U14 | fixer (planned, after round 2), sonnet | 5 |  | `wp8/u14` | queued | U13 |  |  |
| WP8-U15 | re-pin and rerun, sonnet | 2 |  | `wp8/u15` | queued | U14 |  |  |
| WP8-U16 | UA-A round 3 (conditional), haiku | 12 |  | `wp8/u16` | queued | U15 and a blocking finding in round 2 |  |  |
| WP8-U17 | technical writer (reviewer's guide), sonnet | 8 |  | `wp8/u17` | queued | U16 or a clean round 2 |  |  |
| WP8-U18 | technical writer (w3id registration file), sonnet | 2 |  | `wp8/u18` | queued | U10 |  |  |
| WP8-U19 | sweep checker, haiku | 1 |  | `wp8/u19` | queued | U17 |  |  |

## Iterations and velocity

| Iteration | Units landed | Est. pts landed | Realized pts | Realized ÷ est. | Elapsed (wall clock) | Velocity (realized pts / hour) |
|---|---|---|---|---|---|---|
| 1 | WP1-U1, WP1-U2, WP1-U3, WP2-U1, WP3-U1, WP3-U2, WP3-U3 | 24 | 27 | 1.12 | 0.66 h | 40.9 |
| 2 | WP2-U2, WP2-U3, WP2-U4, WP2-U5 | 11 | 10 | 0.91 | 0.41 h | 24.4 |
| 3 | WP1-U4, WP1-U5, WP2-U6, WP3-U4 | 12 | 15 | 1.25 | 0.16 h | 93.8 |
| 4 | WP4-U1 to WP4-U8 | 29 | 38 | 1.31 | 1.09 h | 34.9 |
| 5 | WP5-U1 to WP5-U10 (U9, U10 unplanned), WP6-U1 to WP6-U7 | 64 | 70 | 1.09 | 2.94 h | 23.8 |
| 6 | WP6-U8 | 3 | 5 | 1.67 | 0.11 h | 45.5 |
| 7 | WP7-U1 to WP7-U8, WP7-R5, WP7-R6 | 43 | 53 | 1.23 | 1.38 h | 38.4 |

## Velocity and forecast

- **Raw counts first:** estimated points proposed (all planned units), estimated points of the completed units, and
  realized points of the completed units.
- **Raw velocity** for each iteration: realized points ÷ elapsed hours.
- **Smoothed velocity**, once there are at least 3 iterations *(default)*: an exponentially weighted moving average
  that weights recent iterations most, v̂ₙ = α·vₙ + (1 − α)·v̂ₙ₋₁, with α = 0.5 *(default)* and v̂₁ = v₁.
- **A forecast** to the candidate only once the smoothed velocity exists: (remaining estimated points × the running
  realized-to-estimated ratio) ÷ v̂. Before then, the board says so instead of forcing a number.

Current: WP8 approved (D-041): 19 units, 100 est. pts planned (U16 conditional); wave 1 (U1, U2, U4, U5, U6, U7) in flight, iteration 8 open. Before WP8: 186 est. pts proposed (WP1 to WP7, including the unplanned WP5-U9, WP5-U10 and WP6-U8, and the two WP7 reads; WP8 not yet scoped); 186 est. pts completed; 218 realized pts completed. 7 iterations closed; running realized/estimated ratio 1.17; raw velocities [40.9, 24.4, 93.8, 34.9, 23.8, 45.5, 38.4]; smoothed velocity v-hat 39.7 realized pts/hour. Forecast: still not stated as a number, because the remaining estimated points do not exist yet (WP8 has no scope). WP7 landed at 43 estimated and 53 realized (ratio 1.23). Iteration 7 is five units in parallel, so its 1.38 h of wall clock counts overlapping workers once and its velocity is noisy.

Over and under, WP7: on estimate: the skeleton (3), home and getting started (5), planning and facilitation guides (8), the reference (5), the docs test (5) and the style pass (3). Over: the coding guide, 8 against 5, because a guide that shows provoked messages must give each one a stated start state (three push-backs, four reviews; a PM ruling settled it); and the planned fix unit, 8 against 5, because the reruns found a real defect (a placeholder swallowed as an HTML tag) and each read still turned up minor phrases. Lessons: a guide that shows real tool output should be planned with a start state per example; plan Haiku reads with their reruns (3 each, not 2); a style pass should state in its brief where a metaphor may not stand in for an instruction.

Over and under, WP6-U8: ran at 5 against 3. A privacy rewrite has no mechanical check for 'close paraphrase', so review rounds, not the edit, were the cost; plan a paraphrase unit with the review standard stated up front (no 3-word runs and no clause-order echo).

Over and under, WP5 and WP6: WP5-U5 ran at 8 against an estimate of 3 (a new rule changed the shared test fixture, a permission guard blocked the edit, and an ACE ruling changed its scope); WP5-U8, the planned fix unit, ran at 5 against 3 (D-035 added three items; its replanned estimate was 5, logged in metrics, original unchanged); WP6-U3 (README) ran at 3 against 2 after a push-back. Under: WP6-U4 and WP6-U6 (pin work, 2 against 3). At estimate: the checks and operations units (8 and 8), the case study (8), the reader (5) and the verification tests (3). Lesson: a unit that adds a rule or changes a shared fixture should be planned for the tests it disturbs, and any unit that edits existing tests needs the guard's authorisation arranged before it starts.

Over and under, WP4: the three specification units (TBox, page contracts, rule catalogue) ran at 8 against an estimate of 5 each, because two ACE rulings arrived mid-flight and each unit took three or four review rounds. The examples, cold-write, cross-check and rerun units landed at their estimates. Spec-heavy units that other units must align with should be estimated at 8, and an unplanned fix unit should be planned for after any cold-write test.
