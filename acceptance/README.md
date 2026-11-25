# User acceptance kit (UA-A, D-7)

This kit runs the AI user tests defined in `MISSION.md` (User acceptance, UA-A) and `ORG.md` (User tests). The PM
provisions the testers and runs the rounds. The ACE reads every report and dispositions the findings. Nothing here is
run by the tools or by CI. The kit is not in the docs site's navigation.

## What is in the kit

| File | What it is |
|---|---|
| `personas/` | Personas in the user's own words. All three are the organiser at the solo-trial stage (GLOSSARY: organiser), varying only in comfort with the tools: p1 comfortable with a terminal, GitHub and Obsidian, Python session, Haiku (`p1-organiser-comfortable-repl-haiku.md`); p2 new to the command line, careful and literal, command line, Haiku (`p2-organiser-newcomer-cli-haiku.md`); p3 p1's persona on Sonnet, as control (`p3-organiser-comfortable-repl-sonnet-control.md`). p4 is a page cold read (row below). |
| `briefs/` | One self-contained brief per persona, which is all a tester is given, and `cold-read-part1.md` and `cold-read-part2.md`, the two halves of the R-15 cold read. The cold-read briefs are retained for reference only: the cold read is not part of this release's acceptance (D-052). |
| `report-template.md` | What a tester returns: the cold-read answer first (retained for reference), then J1 to J10, findings, severity, the end state with the hand-over (tag, commit, recipient), dispositions, void rules. |
| `personas/p4-…`, `briefs/p4-…` | Persona 4 and its brief (`personas/p4-event-coordinator-haiku.md`, `briefs/p4-event-coordinator-haiku.md`) are the project-manager cold read of one docs page, the Terms page, for WP12-R3. The tester gets the brief plus the page text only and uses no tools, so the clean-environment setup below does not apply. The reports are `reports/wp12-r3-round1.md` to `wp12-r3-round4.md`. |

Each journey persona (p1 to p3) has a coding domain of its own, none of them the worked example: p1 flood readiness in a river town, p2
stall allocation at a farmers' market, p3 parts ordering at a bicycle-repair co-operative. Each brief carries its
domain's own notes: a short solo-trial note (J2: one narrative, set `done`) and the event notes (J5 onward): three groups, one story
session and one design session, within the template's cap. A tester codes at least one story and one design proposal,
each as a narrative with its "Edges told" table. Each brief also carries a hand-over case for J10 with an invented
recipient: p1 a contract delivery to a client body, p2 a class project hand-in to an instructor, p3 a paper submission
to a venue. The tester decides the model is finished (the coder decides, not the tool or an assistant), locks a version
with `git tag` on a clean-checked commit, and names the tag, the commit it pins and the recipient in the report.

## How a round is run

1. Pick the candidate: the commit the Pages preview and the template pin. Record the hash.
2. Run each persona in a fresh agent on the model its brief names. Give it its brief and the report template, and
   nothing else (no persona file, no README, no repository). The PM sets up its environment first (below).
3. *(Not part of this release's acceptance, D-052: the chief engineer's own judgement replaced the R-15 cold-read bar. The briefs are kept for reference. Skip this step.)* Run the cold read in a further fresh agent, with the home page left out, in two messages. First send `briefs/cold-read-part1.md` alone (question 1). Wait for the reader's answer to question 1. Only then send `briefs/cold-read-part2.md` as a second message (question 2). The reader never sees question 2 before answering question 1. The reader gets no report template. The PM assembles the two answers into the cold-read section of `report-template.md` afterwards, and records in the report that the two messages were sent in that order.
4. Collect the reports unedited. Testers write in their own scratch folder and hand the report back as text; they never write into this repository. The PM saves each finished report as `acceptance/reports/<round>-<persona>.md` (for example `r1-p1.md`) and the cold read as `acceptance/reports/<round>-cold-read.md`. Check each against the void rules in `report-template.md` and the grep below. Rerun a
   void report with a fresh tester.
5. The ACE reads each report, merges the findings, and dispositions each: fixed and re-tested by a fresh tester, or
   accepted with a reason and listed in the reviewer's guide. Rerun after fixes with fresh testers. The final round
   leaves no blocking finding.

## Clean-environment setup (per tester)

Do this in a shell the tester will use. Nothing from the PM's own account carries across.

```text
export HOME="$(mktemp -d "<PM scratch dir>/home.XXXXXX")"   # fresh home directory, under the PM's scratch dir
export PATH="<dir holding the existing uv>:/usr/bin:/bin:/usr/sbin:/sbin"
unset GH_TOKEN GITHUB_TOKEN                      # no credentials
git config --global user.name  "Test Person"     # git asks for these; set test values only
git config --global user.email "test@example.invalid"
cd "$HOME"
git clone <template url or local path> my-trial  # the solo trial (J1 to J2)
git clone <template url or local path> my-vault  # the facilitated event (J5 onward)
for d in my-trial my-vault; do git -C "$d" remote remove origin; done   # simulates GitHub's "Use this template"; nothing can push
```

- **uv.** The existing `uv` binary is put on `PATH`. This stands in for "after installing uv". **The uv installer is
  not run**, by anyone, in any round. **Every report must say plainly that uv was preinstalled.** This departs from
  UA-A's "uv not installed". It is a known gap, held for the chief engineer's walkthrough (log D-040, D-041), and
  the reviewer's guide lists it as known-weak.
- **Two clones (default).** `my-trial` is for the solo trial (J1 to J2) and `my-vault` is for the facilitated event (J5 onward). The
  getting-started page is followed twice, once for each: the flow page names it at step 2 (the trial, "Setup, as in
  step 5") and at step 5, and the trial's page should not travel into the event's folder. The brief says so. If the
  docs ever make the trial run in the same repository, drop to one clone and edit the briefs' "Where you start" and J2.
- **J2 and J5.** Each remote-less clone stands in for creating a repository on GitHub from the template on its web
  interface. The brief tells the tester that step is done for it, at J2 and again at J5, and that it could not check
  the repository was private. The template's default branch is `dev`; a tester told by the docs to switch branch does
  so as the page says. J10's push (of the branch and of the tag) fails because there is no remote; the tester pastes the
  failure and goes on.
- **J10.** The tester locks a version with `git tag` (the clone has no remote, so no push of the tag), on a commit made
  when the whole-folder check was clean, and names the tag, the commit it pins and the recipient in the report.
- **Scratch folders.** Each tester gets its own scratch folder, separate from the clones, for its report and for the J4
  file (the consent choices stay outside the tool).
- **Obsidian.** The Obsidian steps (J2, J5, J8 and J10) are checked through files. Obsidian itself is UA-M's.
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

Run the same grep against each brief (`grep ... briefs/p1-*.md`) before a round: a hit in a brief is a defect in the brief, and the output must be empty.

A hit in the pasted output of the untouched example is expected. A hit in a name the tester chose, or in output after the
example was removed, makes the report void.

## UA-A rules and the kit file that enforces each

| UA-A rule in MISSION.md | Kit file and section |
|---|---|
| At least three personas, in the user's own words, never the tool's vocabulary | `personas/` (p1 to p3; p4 is a page cold read), "About me" and "How I work" |
| An organiser comfortable with a terminal, GitHub and Obsidian, not a developer (Haiku) | `personas/p1-organiser-comfortable-repl-haiku.md` |
| An organiser new to the command line, careful and literal (Haiku) | `personas/p2-organiser-newcomer-cli-haiku.md` |
| The first organiser on Sonnet, as control | `personas/p3-organiser-comfortable-repl-sonnet-control.md`, `briefs/p3-...` |
| Every tester is the organiser at the solo-trial stage, varying only in comfort with the tools; each runs the whole journey from J1 | `personas/` (one persona, three comforts); each brief, "What to do, stage by stage", J1 to J10 |
| Most on Haiku | two of the three journey personas; the model is named in each brief |
| At least one Haiku tester in the REPL, at least one on the CLI | p1 (Python session, J2 to J10), p2 (command line, J2 to J10) |
| Clean user environment: fresh home directory, uv not installed | this README, "Clean-environment setup". The uv half is replaced by "preinstalled", stated in each report (D-040, D-041) |
| Starts from the Pages preview URL and follows only what the docs say | each brief, "Where you start" and "Follow only the pages"; this README, "Docs source" |
| J5's repository simulated by an isolated clone with the remote removed (and J2's, by a second clone) | this README, "Clean-environment setup", "Two clones" and "J2 and J5"; each brief, "Where you start" |
| Obsidian steps (J2, J5, J8, J10) checked through files | each brief, "Follow only the pages", J2, J5, J8; this README |
| Codes a small elicitation in a domain of its own, at least one scenario and one architecture, each a narrative with an "Edges told" table | each brief, "Your solo-trial note", "Your event notes" and J2, J7, J8; the domains in `personas/` |
| No reading of `src/` or `tests/` | each brief, "Follow only the pages"; `report-template.md`, void rule 3 |
| Every claim has pasted output | each brief; `report-template.md`, section 1 and void rule 2 |
| The report first answers what style the docs evoke (R-15) | `report-template.md`, section 0 |
| Then stage by stage: stuck, guessed, nowhere to go | `report-template.md`, section 1 |
| *(Retained for reference only, D-052; not part of this release's acceptance.)* R-15 cold read: a fresh reader, home page excluded, asked openly; reports whether the metaphor obscured an instruction | `briefs/cold-read-part1.md` and `briefs/cold-read-part2.md`; `report-template.md`, section 0 |
| Pass bar: everyone reaches the end with a clean check, as a hand-over: a stated case, the decision that the model is finished, a locked version, the tag, the commit it pins and the recipient named | each brief, J10 and "Your hand-over case"; `report-template.md`, section 3 |
| Every guess is a finding | each brief; `report-template.md`, section 2 |
| Blocking: stopped short of the end (J10), or a docs command fails as shown | `report-template.md`, severity |
| Every finding dispositioned: fixed and re-tested by a fresh tester, or accepted with a reason in the reviewer's guide | `report-template.md`, section 4; this README, "How a round is run" step 5 and "Disposition table" |
| The final round leaves no blocking finding | this README, step 5 |
| Void reports: reused names or claims with no pasted output; a report with no findings checked by the ACE for plausibility | `report-template.md`, "Void reports" and section 4; this README, "Checking a report mechanically" |

## Disposition table

Each round's findings go in one table, `reports/rN-findings.md` (for example `reports/r3-findings.md`), written by the
PM from that round's reports for the ACE to disposition. It carries the candidate (commit hashes and the Pages
preview), the reports it digests, the void check, the pass bar with the result for each line, the findings (one row each, with
page and words, what the testers said, and origin), and the PM's recommendation. The ACE's disposition of each finding (fixed and
re-tested, or accepted with a reason that goes in the reviewer's guide) is recorded in that table, and in each report's own section 4.

## Cold-read answers in persona reports do not count

The whole cold read is retained for reference only (D-052). What follows is how it was run.

Each persona report opens with a cold-read answer, but those testers read the home page, which explains the name. That
answer does **not** count toward R-15. Only the cold read (`briefs/cold-read-part1.md` and `briefs/cold-read-part2.md`) counts, and the ACE judges it on the words the reader
noticed, since the guide text carries the word jazz in one plain sentence.

## Known gaps

- uv is preinstalled, not installed from the docs' command. The docs' install step is exercised only by the chief
  engineer (UA-M). Log D-040 and D-041.
- The isolated clones have no remote, so J10's push cannot work (nor the push of the tag), and the tester's environment may also refuse `git push` (or `git commit`). This is a known limit of the isolation. For agents, J10 is a clean whole-vault check plus a local `git commit` and a local `git tag` that pins it (D-044). The briefs tell the tester to paste what happened to the push and move on: a failed or refused push is not a finding and is not blocking.
- The testers have no interactive terminal. The REPL testers (p1, p3) type their lines by piping them into `uv run python -i`; the brief gives the pattern. p1 and p3 must use the Python session for every tool step from J2 to J10, and p2 the command line.
- The test git identity is pre-set in the environment (the docs' own `git` identity prompt is not exercised).
- A local build of the docs is weaker than the Pages deploy and is recorded as such.
- The persona text is a model's reading of a person. It tests the docs, not real users, which UA-M covers.
