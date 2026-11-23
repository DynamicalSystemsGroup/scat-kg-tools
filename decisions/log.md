# Decision log

Rulings and approvals by the ACE, and the chief engineer's decisions (quoted verbatim, typed by the ACE).
Numbered D-nnn, newest last.

## D-001 | 2026-11-23 | Mission OD1: repositories and approval record

Decided by the chief engineer (pop-up answer, typed by the ACE): "DSG, public, PR merge".
Outcome: both repositories are created now in `DynamicalSystemsGroup` as public. The mission is approved by the
chief engineer merging its PR into `main` of `scpt-kg-tools`.

## D-002 | 2026-11-23 | Mission OD2: Agent's defaults

Asked as one item. The chief engineer didn't choose an option. His standing instruction, given in the same turn
(typed by the ACE): "the only explicit sign off i demand is the mission scope and the acceptance of mission
delivery. any other signoffs go to the ACE (assistant chief engineer) and only get escalated to me if their is an
intent gap".
Ruling (ACE): the defaults are details, not intent, so they are the ACE's sign-off. They stand as listed in
`MISSION.md`, and he can still change any of them when he reviews the mission PR.

## D-003 | 2026-11-23 | Repository names and framing

Decided by the chief engineer (chat, typed by the ACE): "`scpt-kg-tools` and `scpt-kg-template` for the 2 repos.
stakeholders, concerns, properties and technologies. we're using scenarios and architectures and we're decompiling
into those 4 concepts and interrelating them through explicitly relationships (layered using bipartite graphs). the
result is a navigable, interpretable dataset."
Outcome: the repositories are renamed throughout, and `MISSION.md` Purpose carries this framing. ACE default: the CLI
command is `scpt`.

## D-004 | 2026-11-23 | Spot check against tradespace

Asked by the chief engineer (chat, typed by the ACE): "tradespace, rather than toaster was the example i was thinking
of. can you spot check against that one before i review the PR. revise if needed" and "you may need to look at its git
history".
ACE revisions after reading tradespace's `AGENTS.md`, `GOVERNANCE.md`, `work-packages/PM-BRIEF.md` and, from its
history, the WP0 setup (`42813502`, `727af775`), the autonomous phase (`e8bb13cf`) and the 0.1 mandate (`85574ded`):
- Branches: `dev` integrates and `main` holds releases only. Acceptance is the chief engineer's merge of the release PR
  `dev` → `main`, which the ACE opens. Before this revision the ACE merged packages into `main`, which would have left
  the acceptance merge with nothing to accept.
- The chain is chief engineer → ACE → one persistent PM → fresh workers, with no level skipped. The PM spawns its own
  workers and is swapped for a fresh one through a file-based handover.
- Who answers what, the escalation rule (quoted from tradespace), and the ACE's calls recorded with evidence for review
  at acceptance.
- Verification in tiers, reviews that run the thing (browser and Obsidian), parallel units with disjoint files, commit
  and push to `dev` as soon as a unit is done, worktree hygiene, negative edits, state in files.
- Models by role: workers on Sonnet or Haiku, Opus only on the ACE's word. Dropped the toaster rule that author and
  reviewer must run on different models; tradespace requires a fresh context instead.
- Nothing is deployed, tagged or published before the release merge. The docs site is staged locally, and the
  simulated-user test reads the staged site.
- D-6 is a reviewer's guide in sittings by output, listing every ACE call (as in tradespace's 0.1 hand-off).
- Defaults: MIT, copyright DSG (the tradespace precedent); `.python-version` 3.12, ruff and `uv lock --check` in CI;
  CI fails on attribution lines.

## D-005 | 2026-11-23 | User acceptance criteria; licence

Raised by the chief engineer (chat, typed by the ACE): "i think we may be missing clear user accept criteria. this
means the documentation is clear and navigable, the user journey is clear. we need all the requirements for the AI
user tests as well as my own user tests using terminal/repl, the github pages, also the github web where repo is
crated from template to start a new one from template and then do an interactive session."
Outcome in `MISSION.md`: G9; R-8 to R-10; a User acceptance section with the journey (J1 to J7), the AI user tests
(UA-A) with their pass bar, and the chief engineer's walkthrough (UA-M); D-7, the acceptance kit; the reviewer's guide
now opens with the walkthrough; WP6 is now the candidate and user acceptance.
ACE readings (his to reverse):
- "terminal/repl" is read as: every CLI operation is also callable from a Python REPL with the same messages (R-8).
- His walkthrough needs a live Pages site and a usable GitHub template before acceptance. So the mission now defines
  a candidate stage: Pages deploys from `dev` with a pre-release banner; the template is marked as a GitHub template
  with `dev` as its default branch until release; tools are pinned to the exact candidate commit.

Decided by the chief engineer (chat, typed by the ACE): "i am think apache 2.0. i know i've gone back and forth on
this. but for this one i want apache".
Outcome: Apache-2.0, copyright Dynamical Systems Group, for code, docs and ontology. This replaces the MIT default in
D-004.

## D-006 | 2026-11-23 | Haiku testers; make the right way the easy way

Decided by the chief engineer (chat, typed by the ACE): "also when running user testing agents (at least some of the
personas) needs to be haiku so we don't expect a lot of reasoning. we need to \"make the right way the easy way\"".
Outcome in `MISSION.md`:
- UA-A now runs at least three personas, most of them on Haiku. A Sonnet run of the same facilitator persona acts as a
  control, and the pass bar binds the Haiku testers.
- R-2: every fix is given as an exact command, or an exact field and value.
- New R-11: Obsidian page templates for every page type, `scpt` generates the structure, and each docs page leads
  with the next action.
- "Make the right way the easy way" is now the first item of the definition of good.
- D-3 now includes the page templates.

## D-007 | 2026-11-23 | CLI and Python REPL

Decided by the chief engineer (chat, typed by the ACE): "using a cli and assume we use the python repl".
This confirms the ACE's reading of "terminal/repl" in D-005. The interactive session has two equal paths, the `scpt`
CLI and the Python REPL. R-8, J6 and UA-M now say so, the docs show both paths side by side, and UA-A covers both
(at least one Haiku tester on each).

## D-008 | 2026-11-23 | The user pattern, documented

Asked by the chief engineer (chat, typed by the ACE): "document that user pattern".
Outcome: `MISSION.md` has a new section, "Users and how they work". It describes the facilitator-analyst, who uses the
GitHub web interface, an Obsidian vault, and an interactive session with the CLI and the Python REPL as equal paths,
and who follows the docs literally. It also records the actor/technologist roles and the Chatham House stakeholder
groups. The sources are his statements in this conversation and D-005 to D-007.

## D-009 | 2026-11-23 | Consistency, drift and cruft pass on the mission

Asked by the chief engineer (chat, typed by the ACE): "do a consistency, drift and cruft pass on the mission
document since we just did some incremental iterations based on my feedback. let me know if any open questions
surface so i can resolve them now".

Fixed (ACE):
- **Contradiction:** the non-goals and the defaults said the tools are pinned "by git tag", but the candidate stage
  pins them to a commit. Everything now says pinned to the exact candidate commit, which `v0.1.0` tags at release.
- **G1:** said raw records link into the graph; they don't. Coded records link into the graph, and raw records link
  to their coded pages.
- **G3:** "content page" was undefined. Status now applies to instance pages and to scenario and architecture pages.
  Class pages are generated and carry none. Stubs are created by `scpt`, which matches R-4.
- **G7:** rewritten against J1–J7, and now names the Python API reference (R-8).
- **Users section:** "actor in one event and a technologist in another" had narrowed his words "some real people may
  be both". Reworded to match them. Dropped a line that repeated the non-goals.
- **Requirements:** R-11 moved into order. The browser pass at desktop and phone width moved into R-10's check, and
  its duplicate in good enough was dropped.
- **UA-A:** the REPL/CLI coverage rule was formatted as if it were a persona; fixed.
- **Wording:** "demo vault" becomes "worked example"; "neighbourhood" becomes "neighborhood", to match the CLI flag.
- **Header:** the ACE row now says "escalates only intent gaps".
- **Breakdown:** D-1 (the Turtle) is fixed by WP2, not WP3. WP3 now names the Python API.
- **Defaults:** dropped an unverified claim that bike-share differs from every DSG domain (`eBike-GDS-documentation`
  exists).
- **Open decisions:** the section was stale (it only cited D-001 and D-002) and now points to the log.
- **ORG.md and pm.md:** the duplicated tester rules are replaced by a pointer to UA-A; testers' models follow UA-A;
  loop step 6 now follows the candidate → UA-A → guide → PRs → walkthrough sequence.
