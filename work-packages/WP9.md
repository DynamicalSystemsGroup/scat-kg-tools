# WP9 — Scope of work: v0.1 cleanup after the chief engineer's skim

| | |
|---|---|
| **Status** | Approved by the ACE (log D-052). Release scope. |
| **Branch** | Units on `wp9/u<k>` off `dev`, merged into `dev`, in whichever repository they touch. |
| **Revert point** | `checkpoint/v0.1-rc1` on both repositories |

## Purpose

Apply the chief engineer's two corrections, so he can play-test and approve v0.1 in the morning:
1. Conformance checks structure, never content.
2. Tone the jazz down further, toward clarity.

## Goals

- **WP9-G1. Remove SCAT-CONFLICT-BOTH everywhere:** the rule catalogue, the contracts, the tools, tests, examples,
  docs, the template's expected output, the kit and the reviewer's guide.
  - The `conflicts` link stays as an explicit, structurally checked relation (endpoint type, target exists).
  - The page contracts and rule catalogue state the principle in one sentence: checks concern structure only.
    Tensions, matches and gaps are for analysis, after conformance passes and a coder signs off the content.
- **WP9-G2. Audit every remaining rule for content judgement.** For each rule, the audit says whether it checks
  structure (types, fields, links, names, status, cap, index freshness) or the meaning of what is recorded. Content
  rules are removed under G1's principle. The audit is a table in the worker's report, and the ACE rules on
  borderline cases.
- **WP9-G3. Jazz nudge.**
  - **Keep:** the music-note logo, and one brief aside on improvisation where the "yes, and" stance is introduced.
  - **Remove:** page epigraphs and taglines, the remaining "borrows from jazz" framing sentences, and musical
    metaphors in prose.
  - **Plain words throughout.** It is a nudge, not a rewrite. Facilitation content and instructions are unchanged
    except where a jazz term stood in for plain meaning.
- **WP9-G4. Refresh the candidate.**
  - Re-pin both repositories.
  - A fresh clone of the template checks with **0 errors and 0 warnings**.
  - The docs test, the walkthrough, the kit and the reviewer's guide match.
  - Pages redeploys from `dev`.

## Non-goals

- WP8-U1 (still held for the chief engineer).
- New rules or features.
- Another UA-A or cold-read round. The chief engineer's play test replaces it.
- Anything in the research spikes.

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| WP9-R1 | No trace of SCAT-CONFLICT-BOTH remains in either repository's tracked files, outside `decisions/` and `acceptance/reports/` (historical records). | `git grep` |
| WP9-R2 | `conflicts` links are still checked structurally: wrong endpoint type and dangling target are errors, tested. | Tests |
| WP9-R3 | The audit table covers every rule id in the catalogue. | Checklist against the catalogue |
| WP9-R4 | The docs keep the logo and exactly one improvisation aside. No page carries an epigraph or a jazz framing sentence. | `grep -i -E 'jazz|improvis|tune|riff|chorus|chart|gig|score|tuning'` over `docs/`, each hit justified, with a browser pass |
| WP9-R5 | Template fresh clone: 0 errors, 0 warnings, no index diff. Tests, ruff, the strict docs build, CI and Pages are green. | A clean-clone trial; CI |
| WP9-R6 | The reviewer's guide, walkthrough and kit no longer expect any warning. The guide records D-052 and the revert point, and says that R-15's cold-read bar gave way to the chief engineer's judgement. | Inspection |

## Definition of good enough

WP9-R1 to WP9-R6 are met.

## Blast radius

- **`scat-kg-tools`:** `contracts/`, `ontology/` (only if the conflict rule's severity is stated there), `src/`,
  `tests/`, `docs/`, `acceptance/` (except `reports/`), `mkdocs.yml`, and the board and metrics.
- **`scat-kg-template`:** the case-study pages (if any text refers to the warning), `README.md`, and the pin files.
- **Test edits** that remove the conflict warning's assertions are directed by the chief engineer's own words, quoted
  in log D-052. Briefs quote them. If a guard still refuses, hold the unit and message the ACE.
