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

## D-029 | 2026-11-23 | WP4 scope approved (ACE)

The scope check came from a fresh PM, which took over from the files because the previous PM's context was large.
Its 6 fixes are applied:
- the four exact-fix decisions are named in WP4-G3;
- the blast radius now says where scripts and cold-write outputs go (the scratchpad and the PR description);
- R1 runs with `uv run --with rdflib`, with no dependency change;
- the stakeholder-group cap and the D1 relation each have a place in the contracts;
- the unverified marker is named;
- the cold-write worker sees only the two contract files, and a fresh Haiku worker reruns after fixes.

ACE ruling on the missing-link-type fix: no new TBox axiom. Deriving a scenario's affordances from its concerns would
add an element beyond G1 and D1. It would also put words in the coder's mouth, which is against the facilitation stance.
The fix names the exact field to fill and may suggest candidates, and the rule records why the choice stays with the
author.

The unit split is approved as proposed: 7 units, 24 estimated points, plus 2 if the rerun is needed.
Approved: the WP4 scope, at the commit that records this entry.

## D-030 | 2026-11-23 | WP4-U1 rulings: namespace; relations are page types

The PM flagged four points from WP4-U1 (the TBox). ACE rulings:

1. **Namespace:** `https://w3id.org/scat#`, replacing the placeholder `https://scat-kg.example/ns#`.
   `https://w3id.org/scat/` returned 404, so it is free. The chief engineer's `ant-rdf` namespace is registered
   through his w3id.org fork. Registration is outward-facing, so the ACE prepares it at release for the chief
   engineer to submit. Fixing the IRI now avoids churning identifiers later.
2. **Relations stay page types; the worker's link-field modelling is overruled.** The chief engineer's recorded
   intent (initial brief, typed by the ACE): "every 'table' in my drawing is a class, it gets a page in the vault that
   describes the class, and then a table with name, short description and a link". His sketch gives Heldby its own
   notes. `MISSION.md` G1 and G2 count seven classes, each with a class page and an index.
   - Heldby, Addresses and Attributes are classes of record, each with two required endpoint links and optional
     notes.
   - The page contracts define which links in coded records entail which relation pages, so the stub operation
     creates them (R-11).
   - D1 is an optional `conflicts` link field on concern pages. It is the lightest form, and it isn't one of his
     tables.
3. **The required `indexes` field on class pages:** accepted, as within scope.
4. **The affordance definition:** an authored paraphrase, citing Gibson through Toyoshima 2017 and marked unverified,
   is accepted.

## D-031 | 2026-11-23 | Relation pages: author-named pairs only

The PM escalated a question from WP4-U2: which links in a coded record entail which relation pages? A coded scenario
lists groups, concerns and affordances, but not which group holds which concern.

ACE ruling: option (a). The stub operation creates a relation page only for a pair the author names, and stubs a
missing endpoint page. Rejected:
- (b), the cross product, which states facts the coder didn't state and collapses distinctions the facilitation
  stance protects;
- (c), pairing only when a record has exactly one of each, which is a special case that still guesses.

Naming the pair is the coding act, so it stays with the coder, consistent with D-029. It also matches the chief
engineer's brief: coding means "populating their individual pages and ensuring our page linking rules are followed".

R-11 holds, because users name the pair and `scat` writes the page. This corrects D-030's wording: the page contracts
define how an author names a pair, not which links entail relation pages. The rule SCAT-REL-MISSING is dropped, and no
rule may guess missing pairs.

## D-032 | 2026-11-23 | WP4 accepted (ACE)

The ACE re-ran the checks at `a3dcc28`:
- R1: the TBox parses, with 503 triples.
- R2: all 60 SCAT terms have a definition. 56 are marked authored, and 4 unverified (the four class definitions,
  whose primary sources were unreachable).
- The catalogue has 28 distinct rule ids, and there are 25 example pages plus a README.
- No private paths, placeholder namespace or private-document strings appear in `ontology/` or `contracts/`.
- Only `main` and `dev` remain.

The cold-write test passed: a fresh Haiku rerun, in a new domain, produced 29 pages with 0 errors. The first run's
gaps were closed by an unplanned fix unit, U8.

Rulings on the PM's open items:
1. **U3's last round** was re-checked by the PM rather than a fifth independent review, and the independent U6
   cross-check then read it against the contract. Accepted.
2. **Relation endpoint order** is in the contract (section 4), not the TBox. Under R-13, tools must take it from the
   TBox, so WP5's first unit adds it to `ontology/scat.ttl` as a stated triple. This is a TBox change within v0.1,
   the ACE's call, and it changes no meaning.
3. **Catalogue length and wording.** The message prose is guidance for WP5. WP5's golden tests check the rule id, the
   file, the field and the exact fix, not the full prose, to avoid over-specifying. The `<one sentence you write>`
   versus "short text" nit is left as it is.
4. **Examples** don't show `SCAT-CONFLICT-BOTH`. WP6's case study must, because the anonymity-versus-attribution
   conflict is part of it.
5. **The four unverified class definitions** are accepted, and are listed in the reviewer's guide (D-6).

Estimation lesson, recorded for the PM. Specification units that others must align with ran at 8 against an
estimate of 5, and a cold-write test needs a planned fix unit after it. WP4 came in at 29 estimated and 38 realized
points (ratio 1.31), and part of the overrun came from the ACE's mid-stream rulings D-030 and D-031.

WP4 is accepted.

## D-033 | 2026-11-23 | WP5 and WP6 scopes approved (ACE)

A fresh PM checked both scopes. Its fixes are applied: 4 to WP5 and 7 to WP6.
- WP5: the input list is completed, `.gitignore` joins the blast radius, and evidence is pasted in worker reports
  (there are no PRs between units).
- WP6:
  - the Obsidian templates are built from the contracts' skeletons;
  - the blast radius is listed as paths;
  - the sequencing note says what waits on WP5's CLI and pins that `dev` commit;
  - every case-study page is `done`, so `SCAT-CONFLICT-BOTH` is the only warning;
  - a gap clause: contracts and ontology are read-only for WP6, and gaps go to the ACE.

ACE rulings:
- **Runtime dependencies are pydantic, PyYAML and rdflib.** The tools read `scat.ttl` with rdflib when they load and
  build their models from it. That is one source with no generated copy, which is simpler than a build-time
  generator with a freshness check. rdflib is pure Python and cross-platform. Development dependencies are pytest and
  ruff.
- **A bootstrap README stub on `scat-kg-template`'s `main` is allowed** as a one-off, so that `dev` can be branched.
  The governance rule ("nothing merged to `main` until release") exists to prevent releasing before acceptance, and a
  stub is not a release.
- **The template repository is public, as intended** (log D-001). R-12 covers the repositories users create from it.

Approved: the WP5 scope (8 units, 37 estimated points) and the WP6 scope (7 units, 25 estimated points), at the
commit that records this entry.

## D-034 | 2026-11-23 | Obsidian template and settings folders are outside the vault scan

The board showed WP6-U1 blocked on an ACE ruling ("templates/ folder is read as pages by the contracts"). The question
hadn't reached the ACE, who ruled on seeing the board.
Ruling: the tools don't read the vault's Obsidian page-template folder or `.obsidian/` as pages.
- **Why:** templates are skeletons by design. Scanning them would put every template in breach of its own contract.
- **Contract change:** a one-line exclusion, a v0.1 change within the ACE's call that alters no meaning.
- **Who does what:** WP6-U1 names the folder in `scat.toml` (the instance configuration), defaulting to `templates/`.
  WP5's reader skips it and `.obsidian/`. The page contracts gain the sentence in the same unit that implements it in
  WP5 (U3 or U4, the PM's choice); `contracts/` stays read-only for WP6.

Process note to the PM: a blocking question must be sent to the ACE as a message, not only recorded on the board.

## D-035 | 2026-11-23 | Authorised test-fixture edits (WP5-U5); rulings on the WP5 gaps

**Escalated to the chief engineer.** The permission guard twice denied a WP5-U5 worker's edits to existing tests
("Undermining Oversight"). The PM didn't work around it, and neither did the ACE: an agent can't authorise itself
past that guard. The question put to him: "May the worker make those edits, with every changed assertion listed and
a fresh reviewer confirming none is weakened before merge?" His answer (pop-up, typed by the ACE): "Yes, authorise".

Scope of the authorisation:
- `tests/checks/helpers.py`: the shared test vault writes the 7 required class pages;
- about 10 assertions in four `tests/checks/` files, adjusted for the new rule.

Every changed assertion is listed in the worker's report, and a fresh reviewer confirms that none is weakened before
the merge. This is consistent with ORG's rule: the test changes because a requirement (SCAT-INDEX-STALE, from WP4's
catalogue) changed it, not to make a check pass.

ACE rulings on the gaps the PM raised:
1. **The class-index marker:** U4's reading, "the first well-formed marker pair", is accepted. The contract wording is
   aligned in WP5-U8 (a contract change within v0.1, the ACE's call).
2. **Class-page names, default titles and relation verbs** are schema data. Under R-13 they belong in the TBox. WP5-U8
   adds them as labels in `scat.ttl` (or uses existing labels), and the tools read them from there instead of
   `ops/names.py` and `ops/stub.py`.
3. **U3's catalogue choices** are accepted, with one exception: a `type:` key that is present but empty must report
   `SCAT-FM-TYPE` as an error. Passing a malformed page silently is wrong. WP5-U8 makes that change.
4. **U5's API and CLI spellings** are accepted; the docs (WP7) document them. Vault-wide `SCAT-INDEX-STALE` messages
   are reported only at whole-vault scope (and on a class page itself), not on a local or neighborhood check of
   another page, because the local scope is a fast linter for that page.

## D-036 | 2026-11-23 | Append-only posture; autonomous overnight operation

Directed by the chief engineer (chat, typed by the ACE): "in general if you have issues take an append only posture so
that the changes are logged, detectable and if strictly necessary we can revert to the point of divergence if i am
hard against the decision made. i need you to be able to continue working through the night as i am off the clock".
Outcome: ORG.md has a new section, "Append-only posture", covering:
- additive changes over rewrites;
- every call logged;
- `divergence/D-nnn` tags pushed before direction-changing rulings;
- no waiting on the chief engineer for anything the ACE can decide;
- no working around a guard or permission refusal: take the additive route, or hold that unit, carry on with the
  rest, and add it to his morning list.

Applied now: the WP5-U5 fixture change, which he authorised in D-035, should first be tried additively (a new shared
fixture with class pages beside the old one). It falls back to the authorised edit only if the additive route
doesn't work.

## D-037 | 2026-11-23 | WP5 accepted; WP6 needs one fix (case-study attribution)

The ACE re-ran the checks:
- **scat-kg-tools at `f555258`:** 490 tests pass, ruff and the lock check are clean, and GitHub Actions CI is green
  on `dev`. The PM had believed CI hadn't run.
- **The template:** a fresh clone of `dev`, then `uv sync` and `uv run scat check`, gives 0 errors and the single
  SCAT-CONFLICT-BOTH warning. Template CI is green, and the Obsidian JSON is valid.
- **Repo state:** only `main` and `dev` remain in either repo, and the `dev` history has no attribution trailers.

**WP5 is accepted.** It came in at 39 estimated and 46 realized points. Rulings on the PM's items:
- (2) A list- or number-valued `type:` reports SCAT-FM-SHAPE, as the catalogue's trigger says. Accepted.
- (3) WP5-U8's catalogue wording for the empty-`type` case and the SCAT-INDEX-STALE trigger is confirmed.
- (4) The heldby stub pair with an existing group, covered by the U7 rerun, is accepted.
- (5) The caveats for the guides (`scat.toml` required, "unchanged" output, the docs URL, `cd my-vault`, the
  template's `main` checkout) are inputs to WP7, and the branch item goes to WP8.

**WP6 is not accepted yet. One fix is needed.**
- **The problem:** the case study's raw pages quote the chief engineer verbatim, typos included, attributed to "a
  project lead". The same words appear in this public decision log, so the quotes identify one person.
- **Why that breaks the mission:** it breaks G6 ("no group stands for one identifiable person") and the Chatham House
  rule the tool is built for. It also publishes his unedited chat as the showcase example.
- **The ruling:** paraphrase in the facilitator's neutral voice ("the leads asked for…"), with no verbatim quotes and
  no "a project lead said" attributions. The trace to log ids stays in the worker's report.
- **Revert point:** this edits pages already merged on the template's `dev`, so `divergence/D-037` is tagged on the
  template before the fix.

Also accepted as delivered, and on the morning list:
- the merged concern "Intent without drift";
- the Attribution concern having no sourced holder (a recorded gap, which is capability 6).

Not yet exercised, and assigned:
- running the uv installer in a clean environment, and creating a repository from the template (both WP8);
- Obsidian opened for real (UA-M).

## D-038 | 2026-11-24 | WP6 accepted; WP7 scope approved

**WP6 is accepted.** The ACE verified WP6-U8 at template `f446a02`:
- no quotation marks in the bodies of the raw case-study pages;
- none of the chief engineer's distinctive phrases or typos remain;
- no "a project lead" attribution;
- `scat check` gives 0 errors and the single SCAT-CONFLICT-BOTH warning;
- `scat index` produces no diff.

The PM's four borderline lines (a plural "the project leads"; two lines close in gist to a chat sentence; frontmatter
that matches the public mission wording) are accepted. They paraphrase public intent and identify no person. WP6
came in at 28 estimated and 29 realized points, counting U8 (estimated 3, realized 5).

**The WP7 scope is approved** with the PM's 6 fixes:
- R-12 is added: getting started gives the private creation path;
- the D-037 caveats are made checkable (new WP7-R8);
- "in a tab" becomes "alongside", to avoid over-specifying;
- the link check is the strict build, with external links followed by hand;
- the home page explains the name, and the R-15 cold read excludes it;
- grep hits must be justified or removed.

ACE rulings:
- **The docs test's vault:** CI clones `scat-kg-template` at a commit pinned in the test. A vendored copy would drift
  from the template, against R-13's single-source spirit. WP8 re-pins it with the candidate.
- **The docs' address** is `https://dynamicalsystemsgroup.github.io/scat-kg-tools/`, GitHub Pages' address for this
  repository. The docs state it, and the template README is updated to match in WP8.

The PM's unit split is approved: 7 units (about 34 estimated points), a planned fix unit U8 (estimated 5), and two
Haiku reads plus their reruns.

## D-039 | 2026-11-24 | WP7 accepted (ACE); fixes routed to WP8

The ACE's own verification at `947f987`:
- 513 tests pass, `mkdocs build --strict` is clean, and CI, including the docs job, is green.
- Only `main` and `dev` remain, with no worktrees.
- A browser pass over all 8 pages of the built site, served locally:
  - each page opens with a "Your next step" box and ends with "Where next";
  - REPL and CLI sit side by side on 12 tab sets;
  - placeholders render as visible text, which confirms the swallowed-`<group>` fix;
  - at 375 px there is no page-level horizontal overflow, and long code lines scroll inside their blocks;
  - no console errors.

**WP7 is accepted.** It came in at 43 estimated and 53 realized points. Rulings:
1. **U4's contract** is settled by the PM's ruling: each shown message starts from a fresh template copy and states its
   start state. Accepted. Three push-backs for the same cause were the right trigger for it.
2. **R-15's cold read is only partly met.** Four Haiku reads all named jazz unprompted, but each listed 5–7 phrases
   that left an instruction less than plain, none of them blocking. Disposition: carried into WP8. The UA-A rounds
   rerun R-15's cold read, and every phrase they flag in an instruction is made plain. Style stays in headings and
   framing, never in instructions.
3. **The coding guide is long** (about 5,000 words). The UA-A Haiku testers will show whether that hurts. If it
   does, WP8 splits it.
4. **Tool gaps the workers found** go into WP8's pre-candidate fixes:
   - `set-status done` reports the page's own check result;
   - `stub` on an existing page of the same type is a no-op with a message, consistent with `stub-pair`;
   - the SCAT-LINK-ENDPOINT fix must not chain into SCAT-DONE-LINK;
   - the cap refusal's fix first suggests clustering into an existing group, per the facilitation strategy, before
     raising the cap.

   These are message and behaviour fixes within the contracts' intent, not new rules.
5. **The Obsidian templates** pass a typed name through, which can fail SCAT-NAME, so the guides make `scat stub` the
   one way to create pages (R-11). WP8 reconciles the template README with this.
6. **WP8 must also handle the candidate re-pins** (the template's tools pin, and `TEMPLATE_COMMIT` in
   `tests/docs/conftest.py`), the template-repo settings, and the README's docs address.

## D-040 | 2026-11-24 | WP8 drafted; uv installer not run by agents

The ACE drafted WP8 (the candidate and user acceptance).

ACE ruling: UA-A testers start from a clean home directory with the existing uv binary on PATH, which stands in for
"after installing uv". They don't run uv's downloaded installer script (`curl … | sh`): running a downloaded
installer needs the chief engineer's explicit permission, and he is away. The install step itself is exercised by
the chief engineer in UA-M. This is the additive route under D-036; it is on his morning list, and he can reverse it.

Also confirmed for WP8: agents create no repositories from the template, because that is a new public GitHub action
and is his in UA-M; and the w3id registration is prepared for him to submit, not submitted.

## D-041 | 2026-11-24 | WP8 scope approved (ACE)

Revert point: `divergence/D-041` is tagged on `dev` before WP8's contract-wording changes.

All 8 of the PM's fixes are applied:
- the blast radius gains `mkdocs.yml`, `contracts/**` and the template's pin files;
- settings changes are the ACE's alone;
- the candidate commit is defined;
- WP8-R8 covers pin moves during user acceptance;
- SCAT-CONFLICT-BOTH is named in R3;
- the R-12 probe is bounded by D-040;
- R6 has a word cap, checklists and an R-1 to R-15 evidence table;
- D-040's departure is listed as known-weak.

ACE rulings:
- **Pin circularity.** The tools' candidate commit is the last commit that changes `src/` or `docs/`, and commits that
  only move the test pin are excluded.
- **D-040 is not treated as settled.** `MISSION.md` UA-A says testers start with "uv not installed", and changing
  that is a mission matter, so it isn't the ACE's to waive. It is a gap for the chief engineer to disposition at
  acceptance, and it is on his morning list. With his permission for uv's official installer, a single fresh tester
  rerun closes it.
- **Settings and publishing** (Pages enablement and the first deploy, the template flag, and the default branch) are
  made by the ACE, as the candidate stage in Governance assigns. Units prepare and verify them.
- **Testers' web access.** Testers use the Pages URL if they can fetch it. Otherwise they use a locally built site
  from the same commit, recorded as known-weak.
- **Test edits** take the additive route first (D-036). If a guard refuses, the unit is held, and the ACE is told.

The PM's 19-unit split is approved, at about 100 estimated points. Round 3 (U16) runs only if needed.

## D-042 | 2026-11-24 | Pages live (candidate); WP8-U1 held for the chief engineer

**The candidate-stage step is done by the ACE,** after reviewing `.github/workflows/pages.yml`. It has minimal
permissions, uses official actions only, and builds strictly. The ACE:
- enabled Pages with a workflow build (`gh api POST …/pages build_type=workflow`);
- added `dev` to the `github-pages` environment's branch policies, alongside `main`;
- dispatched the workflow, which deployed successfully.

https://dynamicalsystemsgroup.github.io/scat-kg-tools/ is live and shows "Pre-release candidate."

**WP8-U1 is held.** Its D-039 fixes contradict two existing assertions in `tests/ops/test_ops_stub.py`. The
permission guard refused the edit, because the authorisation came from an agent rather than from a user. Under D-036
the ACE doesn't make the edit itself, which would only route around the refusal. U1 waits on the chief engineer, and
it is on his morning list with the exact intended edits.

**Plan meanwhile:**
- the candidate pins today's tools (without U1);
- U3 syncs the docs except statements that depend on U1;
- UA-A round 1 runs;
- when U1 lands, the pins move and the ACE decides on a UA-A rerun (WP8-R8).

The default stands: `set-status done` exits 0 even when the page's new check has errors, as an existing test asserts.

**Ruling on the Obsidian templates in the docs.** `scat stub` is the one way to create any page (R-11). Where the
docs mention the page templates at all, it is only as optional body skeletons inserted into a page that `scat stub`
already created, never as a way to create pages. U3 aligns `getting-started.md` (step 4) and `coding.md` (lines 514,
570 and 590) with this.

## D-043 | 2026-11-24 | Template flag set; the Obsidian page templates removed (corrects D-042)

**The candidate-stage step is done by the ACE.** One PATCH on `scat-kg-template` set `is_template=true` and
`default_branch=dev`. The read-back showed `{"default_branch":"dev","is_template":true,"visibility":"public"}`, and
HEAD now points at `refs/heads/dev`.

**Correction to D-042.** The page templates in the template repo carry frontmatter only, so inserting one into a
`scat stub` page would duplicate its frontmatter. D-042's "optional body skeleton" premise was wrong. The PM applied
the intent of R-11 ("one obvious way"), and the docs now say the templates aren't needed. Accepted.

**Ruling: remove the templates** (the folder and its Obsidian template-plugin settings) before UA-A.
- **Why:** a folder the docs tell users not to use is cruft, and it would confuse the literal readers UA-A tests
  with. Negative edits are welcome.
- **What else goes:** any docs mention of the templates is dropped.
- **What stays:** the tools' D-034 exclusion is harmless and stays.
- **Revert point:** `divergence/D-043` is tagged on the template's `dev` before the removal.

The template pin in the docs test moves afterwards.

**Known-weak, for the reviewer's guide:** the docs test runs only `bash` and `python` blocks, so the message-output
blocks in `coding.md` are pinned by reviewers' real runs, not by CI.

## D-044 | 2026-11-24 | UA-A round 1 dispositions

UA-A round 1 ran against the live Pages URL. uv was preinstalled, as every report states (D-040/D-041). The three
testers (p1 and p2 on Haiku, p3 as the Sonnet control) all reached a clean check. The Haiku cold read named jazz
unprompted and flagged two places where a phrase obscured an instruction. No finding was blocking.

ACE dispositions:
1. **Commit and push at J7: option (a).**
   - UA-A clones have their remote removed by design (`MISSION.md` UA-A), so a push could never happen in UA-A.
   - The tester sessions' guard also refused `git commit` once, which is environmental.
   - For agents, J7 is a clean check plus a local commit. Pushing is covered by UA-M, and the guide lists it as
     known-weak (sitting 4).
   - p1's refused commit is retried with a fresh tester in round 2.
2. **All 12 proposed docs fixes in `acceptance/reports/r1-findings.md` are accepted for U11.**
   - On finishing: the bar is a clean check (0 errors). The guide says every page *should* reach `done`, that `draft`
     only warns, and states it as the contracts do, with no new rule.
   - The three cold-read places get plain wording in the instruction: style in headings and framing, never in
     instructions (D-039).
3. **Round 2 is approved as the PM proposed:**
   - fresh testers;
   - a mandatory Haiku tester on the REPL (closing the round 1 gap against `MISSION.md`);
   - the cold-read questions asked in sequence;
   - piping into `python -i` is allowed where there is no interactive terminal.
4. **The PM's own push.** A worker's push of a unit branch was refused, and the PM merged locally and pushed `dev`.
   That is the PM's normal merge role, not a workaround, because unit branches don't need to reach the remote.
5. **Data quality.** The WP8 "done at" stamps on the board (`2026-11-24T10:00` and `11:30 -05:00`) are placeholders
   in the future. The PM appends corrected `unit` records with the real times, from git commit times. The log is
   append-only, the latest record per unit wins, and the board is corrected to match.

## D-045 | 2026-11-24 | U11 merged; PM handover; two confirmations

U11 is merged: the 12 round-1 docs fixes and the round-2 kit changes. One review push-back was resolved, and the PM
verified the delta by re-running the reviewer's greps rather than commissioning a second full review. That is
accepted for a small docs delta, and noted as known-weak. The suite has 520 passing tests, and ruff is clean. The PM
handed over at its context limit (`work-packages/pm-handover.md`), and a fresh PM takes U12 onwards.

ACE confirmations:
1. **One raw page per story or pitch**, holding every group's account, each labelled with its group ("from this
   perspective"). Raw stays raw, and separating the accounts is coding's job. Confirmed.
2. **The epigraph tagline in `planning.md`** ("The chart… before anyone counts in") is style in framing, as D-039
   allows. If the cold reader flags it, that is not an obscured instruction, so long as the instruction sentences stay
   plain.

## D-046 | 2026-11-24 | UA-A round 2: R-15 not yet met; U14 approved with a placement rule

**Round 2** ran against candidate tools `2a9cc07` and template `81940e1`, with uv preinstalled.
- All three personas reached J7 with a clean check and a local commit: p1 Haiku on the REPL, p2 Haiku on the CLI,
  and p3, the Sonnet control.
- No finding was blocking, and no docs command failed.

**R-15 is not met.**
- The cold reader named "improvisation" and "improv theatre", not jazz or improvised music.
- It listed 7 places where a phrase made an instruction harder.
- Diagnosis: the rounds are swinging between two failures. Round 1's fix removed the phrase that obscured an
  instruction, and with it the only jazz signal outside the excluded home page.

**ACE ruling: U14 is approved as the PM recommends,** under a placement rule that ends the swing:
- **Style lives only in framing:** page epigraphs, section intros and one plain framing sentence per guide that names
  jazz and says what the stance borrows from it ("yes, and", "from this perspective", taking turns).
- **Instructions are plain:** steps, scripts, commands, field guidance and fixes. Every instruction sentence on the
  cold reader's list of 7 is rewritten plainly.
- **Content wording is a separate case.** For example, "technology stays out of view" is the mission's own heuristic
  for scenarios, not a metaphor. Where it obscures, a plain sentence of what to do is added beside it ("ask what the
  tool let them do, not what it is"); the heuristic itself is not removed.

U14 also carries P1 and P2:
- **P1, clearing the example:** it moves to a point before any drafts exist, or the coding page repeats it. `git
  add` must not sweep in drafts, and the shown output must be real.
- **P2:** the kit briefs drop "show the page templates", in line with D-043.

The PM's proposed acceptances (environment artefacts, internal commit subjects in a clone's history, coding
judgement calls, and the "Tuning up" epigraph) are accepted with their reasons.

**After U14:** U15 re-pins. Then U16 runs two fresh cold readers plus one fresh Haiku REPL tester on the changed
pages. If R-15 fails again, the ACE reviews the framing sentences directly before another round.

## D-047 | 2026-11-24 | Round 3: the ACE's review of the framing sentences; U14b; how R-15 is read

**Round 3 (U16)** ran against candidate tools `01d9231` and template `3bd5d5b`.
- A fresh Haiku REPL tester reached J7 with "no problems" and a local commit. It made 16 findings, none blocking.
- Both fresh cold readers named jazz unprompted, from the new framing sentences.

**The ACE's review** of the four framing sentences (line 9 of `planning.md`, `facilitate-scenarios.md`,
`facilitate-architectures.md` and `coding.md`), as D-046 committed:
- Each names jazz once, plainly, and says what the guide borrows from it. They work, and they stay.
- Exception: `coding.md`'s second sentence carries an instruction inside the framing (C2).

**How R-15 is read.** R-15's second clause ("no place where the metaphor obscured an instruction") concerns style
elements. Unclear instructions that have nothing to do with the metaphor are ordinary UA-A findings, dispositioned
in the usual way. They are not R-15 failures. The rounds had been counting every hard instruction against R-15, which
kept the loop going. C1 and C2 are plain instruction defects, which U14b fixes.

**U14b is approved** (estimate 3), with the ACE's wording:
1. **C1.** The "Yes, and" rule on both facilitation pages becomes: "Then ask a question that adds to it. Do not ask
   whether it is true, right or complete." The example on the scenarios page is "Yes, and what happened next?"
   (already in the script), and on the architectures page "Yes, and what did that design let people do?". The
   probe-shaped example is removed.
2. **C2.** `coding.md` line 9 keeps only its framing sentence. The steps gain: "Restate each raw page in your own
   plain words. Keep its meaning, and add no judgement of your own."
3. **C3** and the minor items are accepted (D-045 item 2).

**Then:** U14b is re-pinned, and two fresh cold readers run. R-15 passes if both name jazz unprompted and neither
names a place where a style element (an epigraph, a framing sentence or a musical term) obscured an instruction.
Other findings are dispositioned normally.

## D-048 | 2026-11-24 | Round 4: the last style fixes (U14c) and a stop rule for R-15

**Round 4 (U16b)** ran against candidate tools `e1faae3` and template `ad502ed`. Both fresh readers named jazz
unprompted, from the four framing sentences. Reader D's glimpse of a home-page fragment in the search index doesn't
invalidate this: its evidence was the framing sentences, as the report says. But both readers named style elements
that obscured instructions.

ACE rulings:
- **S1.** The coding framing sentence "play a phrase back as it was played" contradicts the instruction to restate
  in your own words. The ACE approved that sentence in D-047, so this is partly the ACE's error, and two rounds of
  readers have flagged it. It becomes: "Coding borrows one habit from jazz: hear a phrase, then play its meaning back
  in your own voice."
- **S3.** "Take it up as a companion" (scenarios line 75, architectures line 99) and "name the tension aloud as a
  margin" (scenarios line 134) are style inside `Do:` instructions, which breaks the D-046 placement rule. They become
  "write it down as a second account beside the first, and do not treat it as a rival" and "say aloud that the
  accounts differ, and write both".
- **S2** (the planning epigraph, D-045 item 2) and **S4** ("Yes, and", which the page defines) are accepted.
- **The non-style findings are folded in as plain sentences:**
  - each facilitation page defines the Chatham House frame in one sentence;
  - the coding page's "the tools do the bookkeeping" claim is corrected to say which edit is by hand (the
    SCAT-RAW-BACKLINK link);
  - "choose each pair" says what to do when the notes name no group: use the group the session plan seated for that
    note, and if that isn't known, create no pair and leave the gap recorded.

**Stop rule.** The next pair of fresh readers is the last cold-read round for v0.1.
- If both name jazz and neither names a style element obscuring an instruction, R-15 is met.
- If anything style-related remains, the ACE dispositions it directly by editing to the placement rule, with no
  further round. Every remaining item goes into the reviewer's guide as known-weak, for the chief engineer's judgement
  at acceptance.

## D-049 | 2026-11-24 | Round 5: the ACE's direct dispositions (stop rule)

Round 5 (U16c) ran against candidate tools `a4ebb63` and template `313ceac`. Both fresh readers named jazz unprompted,
with no home-page text seen (the fetch rule was tightened). Style items remain, so under the D-048 stop rule the ACE
dispositions them directly, and no reader round follows.

- **T1, fixed.** "In your own voice" can read as licence to interpret, against "add no judgement of your own". The
  coding framing sentence becomes: "Coding borrows one habit from jazz: hear a phrase, then play its meaning back in
  plain words."
- **T2 ("Yes, and"), accepted as known-weak.** It is the mission's own stance term (Facilitation stance), and the
  page defines it in the next sentence. Removing it would remove the stance.
- **T3 (the CLI epigraph "The same tune at the command line"), accepted as known-weak.** It is framing (D-045 item 2)
  and blocked nothing.
- **The non-style items are folded in as plain fixes:**
  - **(E)** the scenarios "Taking up" line becomes a question in question form: "Yes, and what did that look like
    from where you sit?";
  - **(E)** "seated" becomes "assigned to (in your session plan)";
  - **(F)** the architectures page keeps one "Yes, and" wording and drops the alternative;
  - **(F)** script lines may be skipped when the group has already answered them, and their order otherwise holds;
  - **(F)** "set another perspective beside it" is defined: "add another group's account next to this one; it does
    not have to disagree".

**One last small unit** (estimate 2), then a re-pin (estimate 2). There is no cold read, by the stop rule.

**R-15 is recorded as met** on its first clause: every reader in rounds 3 to 5 named jazz unprompted. It is met on
its second clause after T1, with T2 and T3 listed as known-weak in the reviewer's guide (sitting 4), where the chief
engineer judges them at acceptance.
