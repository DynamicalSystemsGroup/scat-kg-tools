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

## D-010 | 2026-11-23 | Privacy, attribution, case study, ontology research; second cleanup pass

Decided by the chief engineer (pop-ups, typed by the ACE):
- Repositories: "docs recommend private repos but i think its best if we can make the default private when the
  template is used. the template is public. we're just suggesting people using these tools use them to make private
  repos."
- Raw notes: "facilitators call; its not currently built for attribution because we're using it chatham house rule
  settings, but extensions could support projects where attribution is desired property. to keep this tight. let's
  make this repo its own case study. so the example content in the template repo should be this package. we just had
  our first case of a concern conflict (\"attribution\") vs (\"anonymity\"); those can be related by a disjointness
  axiom. we should keep an eye out for easy wins in the ontology as long as they don't overcomplicate the software
  implementation or UX."

Directed by the chief engineer (chat, typed by the ACE): "actually i think you may need this
/Users/z/Documents/GitHub/concept-definition-stage as another reference repo. it may help fill in details i left out
in the ontology. I also want you to include research sprint on existing ontologies. if we have existing ontologies we
can adopt (even if we have to thin it out) i've applied a doctrine of import don't mint for ontologies like we do with
python packages. that also doesn't mean build a franken ontology. we can author ontologies instead of import them if
there isn't one that beats custom in a trade study. the ontology design work here preceeds implementation and will
require research spikes. lets make sure the advice above is followed then re-run the cruft, drift consistency pass on
the mission docs."

Outcome in `MISSION.md`:
- R-12: private by default, through the docs' create link with private pre-selected, falling back to `gh repo create
  --private`. J2 and UA-M updated to match.
- New non-goal: attribution to individuals. How raw notes are taken is the facilitator's call.
- G6: the worked example is this project's own case study. Its stakeholder groups follow the Chatham House rule, so
  no group stands for one identifiable person; this last point is an ACE reading.
- New G10, ontology by evidence: a survey, then a trade study per class (adopt and thin, anchored by equivalence
  axioms in the `concept-definition-stage` pattern, or author where nothing beats custom). It must not become a patchwork,
  every term is traced, and easy-win axioms are taken (the concern conflict is the first). G1 is now designed under G10.
- The breakdown now opens with WP1, the ontology research sprint, and WP2, the toolchain spike, in parallel, then WP3,
  ontology and page contracts, before any implementation. It now has seven work packages.
- `concept-definition-stage` is added as a reference. Its licence practice for adopted definitions is now a default:
  cite and link restricted text (SEBoK is CC BY-NC-SA).

Second cleanup pass (ACE):
- G10's spacing fixed.
- G1 now admits the easy-win relations.
- The non-goal "changing the TBox" is now bounded to after WP3.
- D-1 now also serves G10.
- The void rule for test reports uses the case study's record names, since the tool's own name is now in the
  example.
- "demo" becomes "worked example" in the defaults.
- ORG hygiene now keeps D-5's readouts in the tree.

## D-011 | 2026-11-23 | Timeline: deferred; velocity-based forecasting

Decided by the chief engineer (pop-up, typed by the ACE): "defer date until velocity is established. you can use
story points, and velocity estimate agile style. keep it lightweight its just a heuristic that allows you to drive
convergence and estimate timelines without pre ordaining them. i am assuming my timeline estimates to be noisy at
first. also do no forget to account for testing and feedback and revisions. this is timeline to having a candidate
for me to review. we can estimate timelines to address my feedback later when we get to that. PM role owns times. in
agile terms, that PM is basically scrum-master, i am the product owner, you are the product manager, and the task
agents are our team".
Outcome: a new Timeline section in `MISSION.md`, and the agile role mapping added under Governance. In ORG.md and
pm.md, the PM gives units story points, records velocity on the board, and reports the forecast to the candidate
(including testing, UA-A rounds and revisions).

## D-012 | 2026-11-23 | No licence handling for standards; third cleanup pass

Decided by the chief engineer (chat, typed by the ACE): "i don't want complex licences. these are engineering
standards. just use them and cite them per engineering practice. we're not selling anything here".
Outcome: the default that cited restricted text instead of reproducing it is replaced. Adopted ontologies,
standards and definitions are used directly and cited.

Third cleanup pass (ACE). It ran after D-011, because the second pass came before the timeline was added. It also
used a cold reader, so it isn't anchored on the ACE's own wording. Fixed:
- G5's stale "pinned version" now says pinned to a commit.
- The acceptance record states the sequence once: the ACE opens the PRs, UA-M runs against them, and the merge is
  the acceptance.
- The concern conflict in G10 has one term, and WP1 and WP3 own its form and its check.
- R-3: status relaxes only missing fields; links and relation endpoints are checked at every status.
- Checks that can now be run: R-4 (vault snapshots), R-5 (a generated synthetic 500-page vault), R-11 (a
  template-per-page-type test).
- UA-A now defines "guess" and "blocking".
- The definition of good drops a duplicate of R-5 and a criterion that couldn't be checked; the worked example's
  reading is now judged in UA-M.
- WP1 and WP2 now fix deliverable D-5, and WP4 builds on WP2's toolchain.
- Timeline: the point scale, "iteration", and elapsed time (so velocity converts to a date). The ACE creates
  `work-packages/` at WP1.
- Open decisions now carry their counts.
- Not changed: findings about the log's historical wording. The log records what was true when each entry was
  written.

## D-013 | 2026-11-23 | Core heuristics

Stated by the chief engineer (chat, typed by the ACE): "our core heuristics * for the users: \"make the right way the
easy way\" * for the builders: \"as simple as possible but no simpler\"".
Outcome: a Core heuristics section near the top of `MISSION.md`, as the tie-breaker for any choice not settled
elsewhere. ORG.md states both, and the PM puts them in every worker's brief.

## D-014 | 2026-11-23 | Review against the core heuristics

Asked by the chief engineer (chat, typed by the ACE): "review the document against those two heuristics". The ACE
proposed seven changes. The chief engineer answered (chat, typed by the ACE): "2 lead with REPL because otherwise
commands get long due to uv". The ACE took this as approval of all seven, with item 2 reversed.
Applied:
1. One way to create each kind of page (R-11). Obsidian templates cover the four record types only; SCPT and relation
   pages come from linking and the stub command; class pages come from `index`.
2. The docs lead with the Python REPL and show the CLI in a tab (users section, R-8, J6). R-9 now also runs the REPL
   snippets. G4 is renamed "Operations".
3. Pages are named the way Obsidian shows them, or by path (G4).
4. Setup prerequisites: J3 covers uv and a one-time GitHub sign-in. R-6 runs from a machine with only those, and AI
   testers start without uv.
5. New R-13: the schema has one source. The TBox is authoritative; other forms are generated from it or tested equal
   to it.
6. ORG.md drops `INDEX.md` and the rule that records leave the tree; records stay in `work-packages/` for v0.1.
7. G1 is split into short lines. G7 points to the journey table instead of repeating it. The agile role mapping now
   appears only in ORG.md.
Not changed, because each is as simple as it can be: the candidate stage, the three statuses, and the three tester
personas.
Note: `MISSION.md` grew slightly (from about 4,000 to about 4,100 words). R-13, the prerequisites and the
one-way-per-page rule added more than the trims removed.

## D-015 | 2026-11-23 | Mission approved; dev created; WP1 and WP2 drafted

Mission approval verified: PR #1 was merged by `mzargham` at 2026-11-23T19:00:31Z, as merge commit `3437230`. The
ACE created `dev` from it, along with `work-packages/board.md` and drafts of WP1 (ontology research sprint) and WP2
(toolchain spike). The two run in parallel, and their blast radii (`research/ontology/**` and
`research/toolchain/**`) don't overlap.

## D-016 | 2026-11-23 | WP1 and WP2 scopes approved (ACE)

The PM's scope check returned 7 fixes for WP1 and 8 for WP2. All were applied:
- unit-prefixed IDs;
- blast radii limited to `research/ontology/**` and `research/toolchain/**`, with the board owned by the PM;
- requirements for every goal (WP1-R5 to WP1-R7, WP2-R3, WP2-R6 and WP2-R7), including word limits on the readouts;
- "neighborhood" defined as one hop in each direction;
- stacks A, B and C named;
- a placeholder TBox path for the spike.

ACE calls:
- The spike's PyPI dependencies are pre-approved: pyoxigraph, rdflib, pyshacl, pydantic, pyyaml, python-frontmatter
  and pytest.
- OKF may be installed only from the chief engineer's named repository, pinned to a recorded commit, cloned into its
  own empty directory, read before running, and run with paths passed as arguments.

The PM's proposed units are approved as given: WP1 at 20 points and WP2 at 19, run in parallel.
Approved: WP1 and WP2 scopes, at the commit that records this entry.
