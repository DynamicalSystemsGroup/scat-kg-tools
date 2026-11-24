# User acceptance kit (UA-A, D-7)

This kit runs the AI user tests defined in `MISSION.md` (User acceptance, UA-A) and `ORG.md` (User tests). The PM
provisions the testers and runs the rounds. The ACE reads every report and dispositions the findings. Nothing here is
run by the tools or by CI. The kit is not in the docs site's navigation.

## What is in the kit

| File | What it is |
|---|---|
| `personas/` | Three personas in the user's own words: p1 facilitator-analyst, Python session, Haiku; p2 newcomer, command line, Haiku; p3 facilitator-analyst, Python session, Sonnet, as control. |
| `briefs/` | One self-contained brief per persona, which is all a tester is given, and `cold-read-part1.md` and `cold-read-part2.md`, the two halves of the R-15 check. |
| `report-template.md` | What a tester returns: the cold-read answer first, then J1 to J7, findings, severity, dispositions, void rules. |

Each persona has a coding domain of its own, none of them the worked example: p1 flood readiness in a river town, p2
stall allocation at a farmers' market, p3 parts ordering at a bicycle-repair co-operative. Each brief carries its
domain's event notes: three groups, one story session and one design session, within the template's cap. A tester
codes at least one story and one design proposal, each raw and coded.

## How a round is run

1. Pick the candidate: the commit the Pages preview and the template pin. Record the hash.
2. Run each persona in a fresh agent on the model its brief names. Give it its brief and the report template, and
   nothing else (no persona file, no README, no repository). The PM sets up its environment first (below).
3. Run the cold read in a further fresh agent, with the home page left out, in two messages. First send `briefs/cold-read-part1.md` alone (question 1). Wait for the reader's answer to question 1. Only then send `briefs/cold-read-part2.md` as a second message (question 2). The reader never sees question 2 before answering question 1. The reader gets no report template. The PM assembles the two answers into the cold-read section of `report-template.md` afterwards, and records in the report that the two messages were sent in that order.
4. Collect the reports unedited. Testers write in their own scratch folder and hand the report back as text; they never write into this repository. The PM saves each finished report as `acceptance/reports/<round>-<persona>.md` (for example `r1-p1.md`) and the cold read as `acceptance/reports/<round>-cold-read.md`. Check each against the void rules in `report-template.md` and the grep below. Rerun a
   void report with a fresh tester.
5. The ACE reads each report, merges the findings, and dispositions each: fixed and re-tested by a fresh tester, or
   accepted with a reason and listed in the reviewer's guide. Rerun after fixes with fresh testers. The final round
   leaves no blocking finding.

## Clean-environment setup (per tester)

Do this in a shell the tester will use. Nothing from the PM's own account carries across.

```text
export HOME="$(mktemp -d)"                       # fresh home directory
export PATH="<dir holding the existing uv>:/usr/bin:/bin:/usr/sbin:/sbin"
unset GH_TOKEN GITHUB_TOKEN                      # no credentials
git config --global user.name  "Test Person"     # git asks for these; set test values only
git config --global user.email "test@example.invalid"
cd "$HOME"
git clone <template url or local path> my-vault
cd my-vault && git remote remove origin          # simulates J2; nothing can push
```

- **uv.** The existing `uv` binary is put on `PATH`. This stands in for "after installing uv". **The uv installer is
  not run**, by anyone, in any round. **Every report must say plainly that uv was preinstalled.** This departs from
  UA-A's "uv not installed". It is a known gap, held for the chief engineer's walkthrough (log D-040, D-041), and
  the reviewer's guide lists it as known-weak.
- **J2.** The remote-less clone stands in for creating a repository on GitHub. The brief tells the tester that step is
  done for it. The template's default branch is `dev`; a tester told by the docs to switch branch does so as the page
  says. J7's push fails because there is no remote; the tester pastes the failure and goes on.
- **Obsidian.** J3 and J7 are checked through files. Obsidian itself is UA-M's.
- **Docs source.** Start from the Pages URL <https://dynamicalsystemsgroup.github.io/scat-kg-tools/> if the tester
  can fetch it. If not, serve a local build of the same commit (`uv run --group docs mkdocs build`) and **record the report as
  known-weak**, since it skips what the Pages deploy does.

## Tester isolation

- Each tester is a fresh agent with no memory of an earlier round.
- It works in its own clone, not in this repository. It does not read `src/` or `tests/`, or the decision log.
- Every claim has pasted output. A guess (any action the docs did not literally state) counts as a finding.
- The brief and the persona never use the tool's vocabulary. If a tester ever needs a word the persona does not
  have, that is a docs finding, not a brief edit.

## Checking a report mechanically

For the void rule on reused names, grep a report for the worked example's names and the docs' own example names.
**Keep this list from testers.** It was built from the page folders of the template's example (`scat-kg-template`) and the `[[...]]` names in `docs/`. Refresh it whenever either changes.

```text
grep -niE 'anonymity|attribution|intent-without-drift|gated-approval|groups-clustered-under-a-cap|revert-with-history-kept|groups-under-a-cap-pitch|two-branches-and-tags-pitch|false-start-and-clean-restart|notes-at-a-chatham-house-session|facilitator-analysts|project-leads|workshop-participants|volunteer-stewards|cap-setting|archive-tags|main-and-dev-branches|tools-come-back|shared-spreadsheet|sign-out-sheet|shared-sheet-pitch|saturday-at-the-tool-library|travel-time|tool-library|lending|borrowers|volunteer-staff|funders|booking-app|kiosk|self-checkout|quick-checkout|safe-handling|careful-record-keeping|reading-group|study-circle|reading-list' report.md
```

A hit in the pasted output of the untouched example is expected. A hit in a name the tester chose, or in output after the
example was removed, makes the report void.

## UA-A rules and the kit file that enforces each

| UA-A rule in MISSION.md | Kit file and section |
|---|---|
| At least three personas, in the user's own words, never the tool's vocabulary | `personas/` (three files), "About me" and "How I work" |
| Facilitator-analyst, terminal, GitHub and Obsidian but not a developer (Haiku) | `personas/p1-facilitator-repl-haiku.md` |
| Newcomer to Obsidian and the command line, careful and literal (Haiku) | `personas/p2-newcomer-cli-haiku.md` |
| Same facilitator-analyst on Sonnet, as control | `personas/p3-facilitator-repl-sonnet-control.md`, `briefs/p3-...` |
| Most on Haiku | two of three personas; the model is named in each brief |
| At least one Haiku tester in the REPL, at least one on the CLI | p1 (Python session), p2 (command line) |
| Clean user environment: fresh home directory, uv not installed | this README, "Clean-environment setup". The uv half is replaced by "preinstalled", stated in each report (D-040, D-041) |
| Starts from the Pages preview URL and follows only what the docs say | each brief, "Where you start" and "Follow only the pages"; this README, "Docs source" |
| J2 by an isolated clone with the remote removed | this README, "Clean-environment setup" and "J2" |
| Obsidian steps (J3, J7) checked through files | each brief, J3 and J7; this README |
| Codes a small elicitation in a domain of its own, at least one scenario and one architecture, each raw and coded | each brief, "Your event notes" and J5, J6; the domains in `personas/` |
| No reading of `src/` or `tests/` | each brief, "Follow only the pages"; `report-template.md`, void rule 3 |
| Every claim has pasted output | each brief; `report-template.md`, section 1 and void rule 2 |
| The report first answers what style the docs evoke (R-15) | `report-template.md`, section 0 |
| Then stage by stage: stuck, guessed, nowhere to go | `report-template.md`, section 1 |
| R-15 cold read: a fresh reader, home page excluded, asked openly; reports whether the metaphor obscured an instruction | `briefs/cold-read-part1.md` and `briefs/cold-read-part2.md`; `report-template.md`, section 0 |
| Pass bar: everyone reaches J7 with a clean check | brief J7; `report-template.md`, section 3 |
| Every guess is a finding | each brief; `report-template.md`, section 2 |
| Blocking: stopped short of J7, or a docs command fails as shown | `report-template.md`, severity |
| Every finding dispositioned: fixed and re-tested by a fresh tester, or accepted with a reason in the reviewer's guide | `report-template.md`, section 4; this README, "How a round is run" step 5 |
| The final round leaves no blocking finding | this README, step 5 |
| Void reports: reused names or claims with no pasted output; a report with no findings checked by the ACE for plausibility | `report-template.md`, "Void reports" and section 4; this README, "Checking a report mechanically" |

## Cold-read answers in persona reports do not count

Each persona report opens with a cold-read answer, but those testers read the home page, which explains the name. That
answer does **not** count toward R-15. Only the cold read (`briefs/cold-read-part1.md` and `briefs/cold-read-part2.md`) counts, and the ACE judges it on the words the reader
noticed, since the guide text carries the word jazz in one plain sentence.

## Known gaps

- uv is preinstalled, not installed from the docs' command. The docs' install step is exercised only by the chief
  engineer (UA-M). Log D-040 and D-041.
- The isolated clone has no remote, so J7's push cannot work, and the tester's environment may also refuse `git push` (or `git commit`). This is a known limit of the isolation. For agents, J7 is a clean whole-vault check plus a local `git commit` (D-044). The briefs tell the tester to paste what happened to the push and move on: a failed or refused push is not a finding and is not blocking.
- The testers have no interactive terminal. The REPL testers (p1, p3) type their lines by piping them into `uv run python -i`; the brief gives the pattern. p1 must use the Python session for J5 to J7.
- The test git identity is pre-set in the environment (the docs' own `git` identity prompt is not exercised).
- A local build of the docs is weaker than the Pages deploy and is recorded as such.
- The persona text is a model's reading of a person. It tests the docs, not real users, which UA-M covers.
