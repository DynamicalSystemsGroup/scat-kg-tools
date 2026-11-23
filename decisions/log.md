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

## D-017 | 2026-11-23 | Mission Amendment 1: SCAT; scenarios are behavioural, architectures structural; roll back and restart

(D-015 and D-016 were recorded on `dev` and are rolled back with it; see below. This entry is numbered after them so
no record number is reused.)

New intent from the chief engineer. He shared a stakeholder conversation as intent information; the participants are
not named in this public record. He also wrote (chat, typed by the ACE): "one thing i noticed is that affordances may
be better than propeties here. that said, it makes our acronym scat. i think we might as well roll with it. the jazz
singing should be the reference of record to avoid the feces association."

From the stakeholder conversation, in his words: the work is "scaled to human note taker and focusing on obsidian for
'coding' data from conversations with the workshop participants. the distinction between actors and technologists is
somewhat artificial since many people will be both"; "scenarios stories center on behavior ~ chains of events,
outcomes, consequences, etc"; "architecture stories center on structure ~ arrangements of technologies into tools
with specific properties (affordances)"; "its just enough structure to make the data interpretable but mostly its a
formal structure for arranging obsidian notes".

Decided by the chief engineer (pop-up, typed by the ACE): "rename everything. i hope i caught you earlier enough. if
you are worried about drift you could revert to an earlier commit, make the change in the mission before it
propogates, and start again. i would also like to add that the clarification about how scenarios are behavioral and
architectures are structural is an important heuristic.
- scenarios tell the story of persons within an action situation doing things where outcomes and consequences are
wraught, its temporal, and technologies are part of the action situation but are not themselves the focus.
- architectures formulate assemblages they provide structures, they are about parts and wholes, and how parts are
assembled to provide affordances which address concerns.
in scenarios that technologies are relatively fix and out of view, the affordances are what are legible
in architectures the stakeholders are pretty abstracted away and the concerns are what are being addressed. the same
concerns can arise from different stakeholders and the architectures themselves provide affordances that address
concerns but cannot presume which stakeholders will adopt their architectures."
And (chat): "my intuition is we do a roll back and mission revision then kick off again".

Outcome:
- **Property becomes Affordance.** Addresses is now concern × affordance, and Attributes is now affordance × technology.
  The acronym is SCAT; scat singing is the reference of record.
- **Renames:** the repositories become `scat-kg-tools` and `scat-kg-template`, the CLI `scat`, and the Python package
  `scat_kg`.
- **New mission section, "Scenarios and architectures",** as a core heuristic. The ACE reading: a coded scenario links
  stakeholder groups, concerns and affordances, and a coded architecture links concerns, affordances and technologies.
  This matches the original sketch's Scenarios (s,c,p) and Architectures (c,p,t).
- **Purpose** adds the human-note-taker scale and "just enough structure".
- **Rollback:** the WP1/WP2 work in flight was stopped before anything merged. `dev` is reverted to the approved
  mission (history kept, no force-push), and WP1 and WP2 are re-scoped from this amendment and restarted.

Approval of this amendment: the chief engineer's merge of its PR into `main`.

## D-018 | 2026-11-23 | Amendment 1, continued: improvisational jazz stance; holding disagreement; facilitation research

Directed by the chief engineer (chat, typed by the ACE; one participant's name is replaced with [a stakeholder] in this
public record): "i want to add a note, mostly for aesthetics/language choice that we're using improvizational jazz
(scat). we want our facilitation style to involve a lot of \"yes and\"+\"from this perspective\", our model allows us
(like in ant-rdf) to expose and explore disagreements and frictions, gaps, and dissenting opinions. this means we do
not need to litigate to agreement in. i want you to include a pass back through the ANT-RDF work and potentially
ellie's recent grant proposal docs that shes shared with me, and/or the koi and the unicorn blog she and i wrote. that
research spike feeds the facilitation strategy stuff and importantly an affordance of our approach is that it can hold
rather than collapse disagreement, and can represent margins of potential conflict. in my discussion with
[a stakeholder] i noted that secrete police in an authoritarian regime AND an oppressed population in that same
scenario can share a concern for privacy, anonymity while also being directly in opposition to each others political
will. one to be free from the others control, and the other to exert it. that's a bit loaded so i'd avoid it as our
worked example but my point is that we want to capture people stories, and capture peoples proposed architectures. we
do not want to get into debates about which architecture us correct, or which stories should be the focal point of
designs."

Outcome in `MISSION.md`:
- New section, "Facilitation stance: improvisational jazz": "yes, and" and "from this perspective"; the model holds
  disagreement rather than collapsing it, and represents margins of potential conflict; no litigating to agreement.
- New non-goal: adjudicating between stories or architectures.
- G10: WP1 assesses the lightest way for the graph to hold disagreement.
- New WP3, a facilitation research spike, running in parallel with WP1 and WP2. Its sources, located by the ACE:
  `ant-rdf`; "KOI & The Unicorn" (blog.block.science); "Building the Loop" (EPIC 2025); and recent unpublished
  grant drafts from the same collaboration. The later packages are renumbered WP4 to WP8.
- D-5 and good enough now include the facilitation readout.
- New default: private sources are read for principles only. The repositories are public, so readouts cite only
  published work.

The authoritarian-regime illustration is kept out of the worked example, as directed.

## D-019 | 2026-11-23 | Consistency pass on Amendment 1; jazz as the stylistic reference

Asked by the chief engineer (chat, typed by the ACE): "can you do a cruft, drift and consistency pass for me." Then,
during the pass: "you also seem to be not capturing my requirement that the scat package takes its stylistic
references from jazz music. that is something we can cold read test for with the docs. even if its handled through
visual metaphor".

New: R-15. Jazz is the stylistic reference, in language and through visual metaphor, and never at the cost of
clarity. It is checked by a cold read: the reader names jazz unprompted and finds no instruction obscured. G7 and the
UA-A reports carry it.

Consistency pass (a cold reader and the ACE). Fixed:
- **Privacy:** an unpublished grant draft was named with its author and location in WP3 and in this log's D-018
  outcome; both now read "unpublished grant-proposal drafts".
- **Holding disagreement:** the facilitation stance promised it, but no goal required it. G1 now requires the TBox to
  hold it, in the form WP1 decides, at minimum the same concern held by different groups.
- **Link rules per record type:**
  - G1 now states them;
  - R-1 makes a missing required link type an error;
  - a scenario linking a technology, or an architecture linking a stakeholder group, is a warning that points to the
    affordance or the concern *(ACE default)*.
- **Non-adjudication:** it was unchecked. New R-14 requires the guides to carry the stance with no ranking or
  adjudication step. G6 now excludes politically loaded illustrations.
- **G7 vs the journey table:** G7's "one page per stage" contradicted the table, which shares some pages between
  stages. G7 now names the five guide pages.
- **Traceability:** the facilitation research traced to no goal. New G11 (facilitation strategy) now carries D-4 and
  D-5.
- **Duplicates and leftovers:**
  - the actor/technologist point appeared twice and J4 treated them as separate people; the duplicate is removed and
    J4 is reworded around sessions;
  - each UA-A tester now codes at least one scenario and one architecture.
- **Bookkeeping:**
  - the Open decisions counts were stale and are recounted;
  - "log" now prefixes log ids where they sit next to deliverable ids;
  - the header status is updated;
  - a broken table row in R-8 is mended;
  - the README no longer says "once it is merged".

## D-020 | 2026-11-23 | Final pass on the constitutive document; requirements separated from design

Asked by the chief engineer (chat, typed by the ACE): "one last consistency, clarity, cruft, drift pass. this is the
constitutive doc for the project so weaknesses here could ripple into major issues later". During the pass: "be
careful not to specify design details. you can provide guidance, but overspecification is also failure mode." And:
"we rolled back because we had a false start but fortunately our toolchain has affordances that allowed us to catch
ourselves, refine our mission and then when its approved start again clean".

The review used a cold reader on Opus (the ACE's named reason: this is the constitutive document) and the ACE's own
read. `MISSION.md` was rewritten in full. Its IDs are kept, because the log refers to them.

**Over-specification removed:**
- Requirements now state outcomes:
  - R-1 now names the classes of error and leaves severities to the rule catalogue;
  - R-3 is "never an error just for being unfinished";
  - R-4 is "checks never write";
  - R-11 is "one obvious way to create each kind of page";
  - R-12 is "private by default".
- G4 describes operations, not command syntax.
- D-2 and D-3 no longer list mechanisms.
- The specific mechanisms moved to a new, non-binding "Design guidance" section that work packages may depart from,
  with a reason.

**Structural:**
- The breakdown left the mission for `work-packages/plan.md`, owned by the ACE. The mission keeps only the
  orderings, so goals no longer cite work-package numbers, and revising the plan no longer needs an amendment.
- "Intent gap" now has one definition, in the mission, and ORG points to it.

**Gaps closed:**
- Release steps after the merge are now defined and authorised (tagging, redeploying, restoring the default branch),
  and the pin rule is simplified.
- A fix made during user acceptance now moves the pin and reruns CI, R-6 and R-9; the ACE decides whether UA-A
  reruns.
- TBox changes during v0.1 have a path: the ACE's call, or an intent gap if the graph's meaning changes.
- How disagreement is held is now decided at TBox design, so the facilitation research can feed it.
- The stakeholder-group cap is defined, citing the chief engineer's initial brief, which wasn't previously logged:
  "stakeholders in the data model are stakeholder groups, essentially clustered down to fit in a cardinality parameter
  (set per instance)".
- A link to a missing page is now an error class.
- The test environment is now buildable: a clean user environment, Obsidian steps checked through the files and
  covered by UA-M, and macOS as the supported platform *(ACE default)*.
- The void rule no longer voids clean reports; it voids reports without pasted output.
- Source locations are given: all four reference repositories are public.
- R-15's cold read excludes any page that explains the name.
- "Neighborhood", "open item" and the G6 counts are defined, and OKF is linked.
- `plan.md` fixes the sequencing: WP5 and WP6 set up their repositories and CI, WP6 is accepted after WP5, and WP7
  after WP5 and WP6.

**Cruft:**
- Duplicates removed: the release sequence, "no faces", the defaults list repeating inline defaults, and a
  maintainability criterion that couldn't be judged.
- The chief engineer's own constraints (licence, citation, private sources, attribution) moved from the Agent's
  defaults to Governance.
- "Core heuristic" became "important heuristic", his word.

**Scenario candidate for the worked example (G6):** the false start, then halt, roll back, refine the mission and
restart clean. Concerns: staying faithful to intent, and avoiding drift. Affordances: a gated mission, halting before
anything merges, reverting without losing history, and tags that keep findings available without seeding the
restart. The stakeholder group is named by role, such as "project leads", under the Chatham House rule.

## D-021 | 2026-11-23 | Platforms

Decided by the chief engineer (chat, typed by the ACE), on the ACE's macOS default: "i am willing to accept this. but
will need to be clear that does not mean we should do anything we know introduces risks being able to support it on
linux and windows."
Outcome: macOS is the supported user platform for v0.1, and CI runs on Linux. The platform rule moves from the Agent's
defaults to the chief engineer's constraints in Governance: nothing may be built in a way known to put later Linux or
Windows support at risk. That means no platform-specific paths, shells, line endings or tools in the package, and
anything unavoidably platform-specific is isolated and recorded.

## D-022 | 2026-11-23 | Amendment 1 approved; branch hygiene

Amendment 1 approval verified: PR #2 was merged by `mzargham` at 2026-11-23T20:07:01Z, as merge commit `3c3a5ef`.
`dev` is now brought up to date with `main`.

Guideline from the chief engineer (chat, typed by the ACE): "this is more of a guideline than a mission mandate but i
do want you to make sure the branches get cleaned up periodically".
Outcome:
- ORG.md Hygiene now says unit branches are deleted once merged and package branches once accepted. The ACE checks at
  each package acceptance, and abandoned work is tagged under `archive/` first.
- pm.md's merge steps now include deleting the unit branch.
- Applied now: `mission/v0.1` and `amendment/1-scat` are deleted (both merged), and the amendment worktree is removed.
  Only `main` and `dev` remain, and the 8 `archive/pre-amendment-1/*` tags are kept.

## D-023 | 2026-11-23 | WP1, WP2 and WP3 scopes approved (ACE)

A fresh PM checked the scopes. Its 12 fixes are applied:
- **Branches:** units branch off `dev` as `wpN/uK`.
- **WP1:** requirements for the disagreement options (WP1-R7) and for each element's recommendation, runner-up and
  deciding criterion (WP1-R8).
- **WP2:**
  - OKF is cloned outside the repository;
  - the fixes for each defect are made exact (WP2-R8);
  - the readout lists anything platform-specific (WP2-R9).
- **WP3:**
  - topic coverage (WP3-R6);
  - the stance made concrete in J4, J5 and J6 (WP3-R7);
  - a concrete definition of good enough for what WP4 and WP7 receive.

WP3's mention of the private draft was removed before this, so the PM withdrew that fix.

ACE calls:
- The PM's unit split is approved: WP1 at 15 points, WP2 at 19, WP3 at 13.
- Models are pinned by alias (sonnet, haiku), because the agent tool accepts only aliases.
- WP3-U3 may open the private drafts through the Drive connector. The chief engineer asked for them to be read. Their
  identity goes only in the spawn prompts of that unit and its reviewer.

Approved: the WP1, WP2 and WP3 scopes, at the commit that records this entry.

## D-024 | 2026-11-23 | Periodic status report

Requested by the chief engineer (chat, typed by the ACE): "i want a periodic report on recently completed work, whats
in flight & what actor is working on it, then what's queued, and what the queued items are waiting on."
Outcome:
- The board's Units table now records, for each unit, the actor, its state, what it is waiting on, and when it was
  done.
- ORG.md has a "Status reports" section, which makes the PM responsible for keeping that table true.
- The ACE runs an hourly report from the board and the git history of `dev` *(ACE default cadence)*, without
  interrupting the PM.

## D-025 | 2026-11-23 | Estimated and realized points in the hourly report

Requested by the chief engineer (chat, typed by the ACE): "please include story points and velocity estimates in the
hourly update. i want estimate points for the proposed work and realized points for completed work. i expect them to
diverge. we have to allow them to deviate in order to learn the patterns and improve our future estimates".
Outcome:
- **The board** now records, for each unit, estimated points (set at planning and never revised) and realized points
  (scored when the unit lands, with a one-line basis). Each iteration row shows the estimated and realized points,
  their ratio, the elapsed time, and the velocity in realized points per hour.
- **The forecast** is the remaining estimate, corrected by the running ratio, divided by the velocity.
- **ORG.md** asks the PM to note at each package acceptance which kinds of unit ran over or under.
- **The hourly report** now carries all of this.

## D-026 | 2026-11-23 | Velocity: raw first, smoothed later

Directed by the chief engineer (chat, typed by the ACE): "velocity estimates only really become useful once we have a
few data points so don't need force it. i think raw counts of story points estimate and completed, then velocities,
and once we have a bit more data i'd like an exponetionally smoothed weighted average with the recent velocities
carrying the weight".
Outcome:
- Reports give the raw point counts (estimated proposed, estimated completed, realized completed), then the raw
  velocity for each iteration.
- From 3 iterations onwards *(ACE default)*, they add an exponentially weighted moving average,
  v̂ₙ = α·vₙ + (1 − α)·v̂ₙ₋₁, with α = 0.5 *(ACE default)*, so recent iterations carry the weight.
- A forecast appears only once the smoothed velocity exists.

## D-027 | 2026-11-23 | A JSON log of the planning data

Requested by the chief engineer (chat, typed by the ACE): "keep a json log of this data so i can review it myself in
a python notebook without disrupting your flow".
Outcome:
- `work-packages/metrics.jsonl` is an append-only JSON Lines log with two record kinds: a `unit` record for every unit
  state change, with estimated and realized points, and an `iteration` record for every iteration close, with raw
  velocity.
- `work-packages/metrics.md` documents the schema and a one-line pandas read.
- The PM is the only writer, which keeps appends conflict-free. Derived figures (the smoothed velocity and the
  forecast) are not stored, so the log holds only observations *(ACE default)*.

## D-028 | 2026-11-23 | WP1, WP2 and WP3 accepted (ACE); rulings on the research

The ACE's own verification:
- all units are merged on `dev`, and only `main` and `dev` remain;
- the spike's 5 R-13 tests pass on rerun;
- the readouts are 841, 961 and 927 words, against a limit of 1,000;
- the private-document grep is clean across the tree and across `origin/dev`'s history (0 hits);
- `metrics.jsonl` has 37 records.

**Metrics log.** Two units have an early `done` record without realized points, followed by a complete one. The log
is append-only, so the fix is the documented rule that the latest record per unit is authoritative (`metrics.md`).
Iterations overlapped in wall-clock time, so the early velocities overstate throughput, and that is now noted.

**WP2 ruling: the toolchain is stack C** (pydantic models plus plain Python), on the readout's evidence. All stacks
are well inside R-5, the messages don't separate them, and C needs no graph store and no second rule language for a
contributor to learn.
- OKF is rejected as the format between vault and graph. It treats wikilinks as non-links, found 0 edges, caught 0
  of 4 defects, and its status vocabulary clashes with ours.
- The question is left open for WP5: R-13 for C is currently a hand-written model held equal to the TBox by a test
  that can't see slugs, descriptions or status values. WP4's TBox must state these, and WP5 should prefer generating
  the models from the TBox if that proves simple.
- Exact fixes for three of the four defect kinds need project decisions. These go into WP4's rule catalogue.

**WP1 ruling: the composition recommendation is accepted as WP4's starting point.**
- One SKOS spine, with authored SCAT IRIs, adopted definitions and `skos:closeMatch` anchors.
- Authored relations and record classes; `prov:wasDerivedFrom` from coded to raw; adopted
  `schema:creativeWorkStatus` with authored values. Because it sits in schema.org's pending area, WP4 may author
  `status` instead if it judges the instability a risk.
- Unverified sources (the ISO 42010:2022 text was unreachable, and Gibson was read via a secondary source): WP4 uses
  authored wording that cites the source it could reach, and marks it as unverified. This is not an intent gap.
- Disagreement: D0 (many-to-many Heldby), D1 (an authored, symmetric conflict relation between concerns) and D3 (a
  warning when a record touches both ends of a conflict) are accepted. OWL disjointness is rejected, because it would
  turn a tension into an inconsistency, against the mission's "holds rather than collapses". **Extension flag for the
  chief engineer:** he called the concern conflict "a disjointness axiom". The ruling keeps his intent, a conflict
  between concerns that the graph shows, but implements it as a relation plus a warning, not as an OWL disjointness
  axiom.

**WP3 ruling: the strategy is accepted, and its 15 capabilities are triaged for WP4 under "as simple as possible".**
- Capabilities 1–3 (shared concerns, concerns in tension, margins of conflict) are required. They are met by D0, D1
  and D3.
- Capabilities met by structure that is already planned need nothing new: raw kept apart from its reading (10),
  status and unfinished work (11 in part, and 15), provenance (11 in part), and several designs per concern and
  concerns per design (8).
- The rest (4–7, 9, 12–14) are met through page content and the facilitation guides, or deferred. WP4 adds no
  element beyond `MISSION.md` G1 and D1 without a written trade-off.

WP1, WP2 and WP3 are accepted.
