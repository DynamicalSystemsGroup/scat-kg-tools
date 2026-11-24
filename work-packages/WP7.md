# WP7 — Scope of work: Docs and Pages

| | |
|---|---|
| **Status** | Approved by the ACE when the decision log records it. Runs inside `MISSION.md`: G7, G9, G11, R-8, R-9, R-10, R-11, R-14, R-15, and deliverable D-4. |
| **Branch** | Each unit works on `wp7/u<k>`, branched off `dev` and merged back into `dev` (ORG.md). |
| **Inputs** | `research/facilitation/strategy.md` and `readout.md` (WP3), `contracts/`, the tools (WP5), the template (WP6), the WP5 caveats in log D-037, and `MISSION.md` (the journey J1–J7, Scenarios and architectures, Facilitation stance) |

## Purpose

Write the documentation site that takes a facilitator-analyst from not knowing what SCAT is to a clean, navigable
graph, following the docs literally. The site carries the improvisational stance, and jazz is its style reference.

## Goals

- **WP7-G1. The journey pages:**
  - home (J1);
  - getting started (J2, J3);
  - a planning guide (J4);
  - a scenario facilitation guide and an architecture facilitation guide (J5);
  - a coding guide (J6, J7).

  Each page leads with the one action to take next, says what you need before you start, and where to go next.
- **WP7-G2. Reference:** the Python API and the CLI. The REPL leads, and the CLI equivalent sits in a tab alongside.
- **WP7-G3. The facilitation guides,** written from WP3's strategy:
  - the stance ("yes, and"; "from this perspective") made concrete at each stage;
  - scenarios as behavioural, architectures as structural;
  - disagreement held, never adjudicated.
- **WP7-G4. Style:** jazz is the reference, in language and through light visual metaphor, never at the cost of
  clarity. Visual assets are made for the site, and none are downloaded.
- **WP7-G5. Build:** a strict MkDocs Material build, and a docs test that runs every snippet and command shown
  (R-9). The site is built and checked locally. Deploying it is WP8's candidate stage.

## Non-goals

- Deploying to Pages, and editing the template repository (WP8).
- Changing tool behaviour, the contracts or the TBox. Gaps the docs expose go to the ACE.
- Adjudication, ranking or consensus methods in any guide.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| WP7-D1 | `docs/`: the journey pages and the reference | WP7-G1 to WP7-G4 |
| WP7-D2 | `mkdocs.yml`, and a `docs` dependency group in `pyproject.toml` with its lock | WP7-G5 |
| WP7-D3 | The docs test, in `tests/docs/` | WP7-G5 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| WP7-R1 | `mkdocs build --strict` passes, and no internal link is broken. | The build and a link check, with output in the worker's report |
| WP7-R2 | Every REPL snippet and command shown runs as shown against the template vault, and the CLI reference matches `--help` (R-9). | The docs test, in CI |
| WP7-R3 | Every journey page leads with the next action, says what you need first and where to go next, and has no dead end (R-10, R-11). | A checklist per page |
| WP7-R4 | The planning and facilitation guides carry the stance concretely at each stage, with no ranking, voting or adjudication step (R-14). | A checklist, and a grep for "vote", "rank", "best" and "consensus", with each hit justified |
| WP7-R5 | **Cold read.** A fresh Haiku reader, given only the built site except any page that explains the name, is asked openly what style it evokes and names jazz unprompted. It reports no place where the metaphor obscured an instruction (R-15). | The reader's report; if it fails, a planned fix unit and a fresh rerun |
| WP7-R6 | **Clarity read.** A fresh Haiku reader follows getting started and the coding guide literally, against a scratch copy of the template, and reaches a clean check. Each guess is a finding. | The reader's report, with pasted output; findings fixed in the planned fix unit |
| WP7-R7 | Every reviewer looks at the rendered site in a browser, at desktop and 375 px, with screenshots or notes in the report. | The review records |

## Definition of good

A newcomer reads the home page and wants to run a session. A facilitator can run one from the guide in hand. Every
page feels like it was played, not lectured, and never makes the reader guess.

## Definition of good enough

WP7-R1 to WP7-R7 are met.

## Blast radius

`docs/**`, `mkdocs.yml`, `tests/docs/**`, `.github/workflows/` (the docs test and build only), and the `docs`
dependency group in `pyproject.toml` and `uv.lock`.

## Pre-approved by the ACE

- The docs dependency group: `mkdocs-material`, plus at most two small mkdocs plugins if needed, each named in the
  worker's report. Nothing is added to the package's runtime dependencies.
