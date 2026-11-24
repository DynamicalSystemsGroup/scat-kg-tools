# WP8 — Scope of work: Candidate and user acceptance

| | |
|---|---|
| **Status** | Approved by the ACE when the decision log records it. Runs inside `MISSION.md`: User acceptance (UA-A, and preparation for UA-M), the candidate stage and the release steps (Governance), R-6, R-12, R-15, and deliverables D-6 and D-7. |
| **Branch** | Each unit works on `wp8/u<k>`, off `dev`, in whichever repository it touches. |
| **Inputs** | Log D-037 to D-039 (pre-candidate fixes, R-15 residue, re-pins, the Obsidian template reconciliation), `MISSION.md` (User acceptance; Governance), and `research/facilitation/strategy.md` |

## Purpose

Turn the accepted packages into a candidate the chief engineer can walk through and accept:
- fix what the docs work exposed;
- stand up the candidate stage;
- run the AI user tests to their pass bar;
- prepare his walkthrough and reviewer's guide;
- open the release PRs.

The package ends with the PRs open and the morning list current. His walkthrough and merges are his.

## Goals

- **WP8-G1. Pre-candidate fixes,** from D-039 item 4: `set-status done` reports the page's own check result; `stub`
  on an existing page of the same type is a no-op with a message; the SCAT-LINK-ENDPOINT fix doesn't chain into
  SCAT-DONE-LINK; the cap refusal suggests clustering into an existing group before raising the cap. Plus the
  template README reconciliation (D-039 item 5) and the docs address.
- **WP8-G2. The candidate stage,** as `MISSION.md` Governance defines it:
  - the docs site deploys from `dev` to GitHub Pages, marked pre-release;
  - `scat-kg-template` is marked as a GitHub template, with `dev` as its default branch;
  - the template pins the tools' candidate commit, and the docs test pins the template's candidate commit. The
    tools' **candidate commit** is the last tools commit that changes `src/` or `docs/`; commits that only move the
    test pin are excluded, which breaks the circularity (log D-041).
- **WP8-G3. The acceptance kit (D-7):** personas, briefs, the report template, and the chief engineer's walkthrough
  script. The script splits J1–J7 into resumable stages, each with its entry point and what "done" looks like.
- **WP8-G4. UA-A rounds** to the pass bar in `MISSION.md`:
  - at least three personas, most of them on Haiku, with a Sonnet control;
  - at least one Haiku tester in the REPL and one on the CLI;
  - each tester codes one scenario and one architecture in a domain of its own;
  - the R-15 cold read first.

  Every finding is dispositioned. Phrases in instructions that the cold read flags are made plain (D-039 item 2).
- **WP8-G5. The reviewer's guide (D-6),** in sittings:
  - (1) the walkthrough;
  - (2) the docs site;
  - (3) the tools and checks;
  - (4) the ACE's calls, with their evidence and `divergence/` tags, and what is known to be weak.
- **WP8-G6. The release PRs** (`dev` → `main`), opened by the ACE in both repositories, with the reviewer's guide in
  the `scat-kg-tools` PR. The w3id namespace registration is prepared for the chief engineer to submit from his
  fork. The ACE doesn't submit it.

## Non-goals

- Merging to `main`, tagging `v0.1.0`, the release redeploy, and restoring the template's default branch. These
  follow the chief engineer's merge (Governance, "Release").
- Creating any GitHub repository from the template. That is the chief engineer's, in UA-M.
- Running a downloaded installer script (log D-040).
- New features, rules or ontology changes beyond the fixes in G1.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| WP8-D1 | The tool and message fixes, with tests; the template README reconciled | WP8-G1 |
| WP8-D2 | A Pages workflow deploying from `dev` with a pre-release mark; the template's settings; both pins | WP8-G2 |
| WP8-D3 | `acceptance/`: personas, briefs, the report template, every UA-A report with its dispositions, and the walkthrough script | WP8-G3, WP8-G4 |
| WP8-D4 | `acceptance/reviewers-guide.md` | WP8-G5 |
| WP8-D5 | The two release PRs, and a prepared w3id registration (a file in `acceptance/` with the exact content for the chief engineer's PR) | WP8-G6 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| WP8-R1 | Each G1 fix has a test, and the suite and CI stay green. | CI |
| WP8-R2 | The Pages site is live at `https://dynamicalsystemsgroup.github.io/scat-kg-tools/`, marked pre-release, and matches `dev`. | The ACE fetches it in a browser |
| WP8-R3 | The template is a GitHub template with `dev` as its default branch, and pins the candidate tools commit. A fresh clone of the default branch, set up and checked, gives 0 errors and only SCAT-CONFLICT-BOTH. R-12 is checked here as far as D-040 allows: the template flag (by `gh api`), and the docs and README text recommending private repositories. The real creation path is left to UA-M. | `gh api` output; a clean-clone trial; a grep of the docs and README |
| WP8-R4 | UA-A meets the `MISSION.md` pass bar. Every report is in `acceptance/` with its dispositions, and the final round has no blocking finding. | The reports |
| WP8-R5 | R-15: the final cold read names jazz unprompted and reports no instruction obscured by a metaphor. | The final cold-read report |
| WP8-R6 | Each sitting in the reviewer's guide and each stage of the walkthrough is no more than about 800 words, with a checklist and an entry point. The guide lists every ACE call with its log id and divergence tag. Sitting 3 has a table of R-1 to R-15, each with its evidence. Sitting 4 lists the known weaknesses, including D-040's departure from UA-A (uv preinstalled) as a gap for the chief engineer to disposition. Nothing private appears. | `wc -w` per section; checklists; a grep for private strings |
| WP8-R8 | Every fix during user acceptance moves the pins and reruns CI, R-6 and R-9. The ACE logs whether UA-A reruns (Governance). | CI runs and log entries |
| WP8-R7 | The release PRs are open, CI is green on both heads, and the PR bodies follow the attribution rules. | `gh pr view` |

## Definition of good

The chief engineer sits down with one guide, follows the walkthrough without help, and finds nothing surprising.
Every call made on his behalf is visible, evidenced and revertible.

## Definition of good enough

WP8-R1 to WP8-R7 are met.

## Blast radius

- **`scat-kg-tools`:** `src/**` and `tests/**` (the G1 fixes and pins), `docs/**` (plain-language fixes),
  `.github/workflows/` (the Pages deploy), `acceptance/**`, and the board and metrics (the PM's).
- **`scat-kg-template`:** `README.md` and the pin files.
- `mkdocs.yml` (the banner) and `contracts/**` (the G1 message and catalogue wording; `divergence/D-041` is tagged
  before any change).
- **`scat-kg-template`:** additionally `pyproject.toml` and `uv.lock`, as pin files.
- **Repository settings** (Pages enablement and deploy, the template flag, the default branch) are changed by the
  ACE only. Units prepare and verify them.

## Agent's defaults

- **UA-A clean environment:** a fresh home directory with the existing uv binary on PATH, which stands in for "after
  installing uv". The install step itself is exercised in UA-M (log D-040).
- **The pre-release mark:** a site-wide banner from the build configuration, not committed page text.
