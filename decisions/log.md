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
- **Defaults:** dropped an unverified claim that bike-share differs from every DSG domain (an earlier private
  bike-domain repository exists; its name redacted under D-082).
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
<local>/concept-definition-stage as another reference repo. it may help fill in details i left out
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

## D-050 | 2026-11-24 | Candidate verified; final dispositions; local paths redacted

**The ACE's verification of the candidate:**
- tools `dev` at `cbd2101` (candidate commit `126a6be`): 520 tests pass, ruff and the strict docs build are clean, and
  CI and Pages are green;
- Pages serves the D-049 wording;
- a fresh clone of the template's default branch (`dev`, at `9e9bad8`) runs `uv sync` and `scat check`, giving 0 errors
  and the single SCAT-CONFLICT-BOTH warning;
- `scat index` produces no diff, and the template pins `126a6be`.

**Dispositions:**
1. **R-15** is met as D-049 records, with T2 and T3 known-weak.
2. **Round-3 persona findings.** The 16 findings from round 3's Haiku REPL tester, all non-blocking, are accepted for
   the reasons D-046 gives (environment artefacts, coding judgement calls, framing epigraphs). Those that later rounds
   addressed are closed by U14b to U14d. They are listed as weakness (i) in the reviewer's guide.
3. **Gaps left for UA-M:** opening Obsidian, the push at J7, and whether a repository created from the template
   starts with fresh history. They stay in the guide's known weaknesses.

**Redaction.** The U19 sweep missed local paths that embed the user's machine username:
- session scratch paths in 11 UA-A report files and in `pm-handover.md`;
- one local path in a verbatim quote in this log (the D-010 entry).

The repository is public, so they are replaced with `<scratch>` and `<local>`. Only paths change, never any
substance. Earlier commits still hold them in git history; removing them from history would need a force-push, which
is not done without the chief engineer's say-so. This is on his morning list.

Correction to D-050 (the ACE's own error). The first redaction command failed silently: zsh doesn't word-split an
unquoted variable, so `sed` received one long filename and changed nothing. The D-050 entry was committed in
`b459458` claiming a redaction that hadn't happened. The redaction was then applied file by file. 9 files changed,
16 lines each way, and a re-grep for `/Users/`, `/private/tmp` and `claude-501` across the public records returns 0.

## D-051 | 2026-11-24 | Release PRs opened

The ACE opened the release PRs, as Governance assigns:
- DynamicalSystemsGroup/scat-kg-tools#3 (`dev` → `main`, with the reviewer's guide);
- DynamicalSystemsGroup/scat-kg-template#1.

CI is green on both heads. The chief engineer's walkthrough (UA-M) runs against them, and his merges are the
acceptance. After the merge, the ACE carries out the release steps.

Held for him: WP8-U1 (a test-assertion edit), the D-040 uv departure, the optional history rewrite for the redacted
paths, and submitting the w3id registration after the merge.

Points for v0.1, from the board: about 300 estimated and about 340 realized, a ratio of about 1.13, across 8
iterations. The largest unplanned cost was the R-15 cold-read chain (rounds 2 to 5), which a stop rule set from the
start would have cut.

## D-052 | 2026-11-24 | Checkpoint rc1; the chief engineer's feedback; WP9 cleanup and two research spikes

**Checkpoint.** `checkpoint/v0.1-rc1` is tagged on tools `169061b` and template `9e9bad8`, as the chief engineer
asked, in case a revert is needed.

The chief engineer's feedback (chat, typed by the ACE):
- "the jazz references are a little heavy handed, the could be toned down a bit further. using music not logo and brief
  aside about improvisation is good. but i think there still few place we could err toward clarity over jazz
  references. you were already exploring that margin so this is just nudge, not a major refactor"
- And: "music note logo is good. sorry if that's unclear".
- "i think you were blending conformance checks with content checks. we should not be getting warnings about
  conflicting concerns. the knowledge graph mode does not and should not try to block conflicting concerns we simply
  note that stakeholders can and do hold concerns that can be in opposition to each other. its natural and desired to
  capture that as long as its explicit. this is not a warning because its related to the content not the structure.
  we have not build any analysis tools yet. given a correctly constructed model (with conformance checks passing) and
  a human "facilitator/coder" reviewing the data and signing off that the content is done, validating it reflects the
  discussioms and interviews with technologists and actors. THEN analysis can be performed to see where the tensions
  are sharpest or where there are matches or gaps. this becomes a network science problem of sorts and it can borrow
  concepts from requirements traceability but that its own research spike."
- "another research spike, would be toward building a community plugin for obsidian that we can install in obsidian
  so the tooling we build works directly with obsidian, which would allow most users to work within obsidian proper
  and github rather than use a cli or REPL. this would make our tool something like an opinionated linter for
  obsidian vault as an IDE for organizing notes according to this ontology."
- "id tag what you gave me tonight a first checkpoint ... you can take that feedback and work ahead. focus on cleaning
  up what we have and getting it ready for me to play test in the morning (ideally able to approve the 0.1 release in
  the morning and if the research spikes go well, you also have done work on the obsidian plugin and the the analysis
  tools. assume the analysis tools are used by a data scientist or network scientist working in a jupyter notebook,
  its focused graph analysis to identify and interpret patterns in the data that help us understand the "big
  picture"."

ACE outcomes:
1. **Principle: conformance checks structure, never content.** D-028's D3 (the SCAT-CONFLICT-BOTH warning) was the
   ACE's error. It blended a content observation into conformance. Reverted: the `conflicts` relation stays as an
   explicit, structurally checked link, and the warning is removed everywhere. Every remaining rule is audited for any
   other content judgement. Seeing tensions, matches and gaps is analysis, done after conformance passes and the
   coder signs off the content.
2. **Jazz, toned down.** Keep the music-note logo and one brief aside on improvisation (the "yes, and" stance). Remove
   the remaining page epigraphs and jazz framing in favour of plain words. R-15's cold-read bar gives way to the chief
   engineer's own judgement, and the reviewer's guide says so.
3. **WP9 (v0.1 cleanup)** carries 1 and 2 and refreshes the candidate, so that he can play-test and approve in the
   morning. It is release scope, on `dev`.
4. **Two research spikes, outside v0.1:**
   - RS1: an Obsidian community plugin, an opinionated linter that makes the vault an IDE for the ontology;
   - RS2: graph analysis for a data or network scientist in Jupyter.

   Both run on side branches (`spike/obsidian-plugin` and `spike/analysis`). They are not merged into `dev` before the
   release. They lift the mission's non-goals only as exploration the chief engineer directed. Any delivery is a later
   package under a mission amendment.

WP8-U1 stays held. His feedback did not address it.

## D-053 | 2026-11-24 | WP9-G2: rule audit rulings

The WP9 audit covered all 28 rule ids. 22 are unambiguously structural. SCAT-CONFLICT-BOTH is content, and is removed
(D-052). The ACE ruled on the four borderline rules:
- **B1** (LINK-DISCOURAGED and LINK-DISCOURAGED-BODY): kept. A type-pair check from the TBox is structure.
- **B2** (CONFLICT-SELF): kept. Its message is trimmed to the structural fact (a concern can't list itself under
  `conflicts`), with no interpretive sentence.
- **B3** (MENTION): kept, as link hygiene (`MISSION.md` names it). Its message says only that the text names an
  existing page without linking it, and how to link it.
- **B4** (RAW-UNCODED): kept. It is the same presence pattern as DONE-LINK.

Nothing else is removed. The audit table and these rulings go into the reviewer's guide.

## D-054 | 2026-11-24 | The spikes may continue into feature development on their branches

Directed by the chief engineer (chat, typed by the ACE): "you can feel free to keep the analysis feature branch and the
obsidian plugin feature branch out of the release but we have a pretty clean separation of concerns with core data
model pinned. you can work through design, development and some testing on the those feature branches. i don't want
to block the first release on them but i wouldn't be upset if they were also ready for me to test out".

Outcome:
- **Scope.** After their readouts, RS1 and RS2 continue on `spike/obsidian-plugin` and `spike/analysis` into design,
  development and testing.
- **Boundary.** They consume `scat_kg` and the TBox as pinned. A change they need in core goes to the ACE as a
  finding, and is not made on the branch.
- **Never blocking.** They are never merged into `dev` before v0.1, and WP9 keeps priority.
- **Aim, for each feature branch:** something the chief engineer can try in the morning.
  - **The plugin:** a built plugin he can drop into a vault's `.obsidian/plugins/`, with install steps.
  - **The analysis:** a notebook and an importable module he can run with one documented `uv` command.

  Each has its own tests, and a README stating what was and wasn't exercised.

## D-055 | 2026-11-24 | WP9 accepted; feature branches tried; Mission Amendment 2 drafted

**WP9 is accepted.** The ACE verified it at `45be728` (candidate `e1701ab`):
- 522 tests pass, ruff and the strict docs build are clean, and CI and Pages are green;
- `git grep` finds no SCAT-CONFLICT-BOTH outside the historical records;
- the docs keep only the logo and one improvisation aside (`docs/index.md`);
- a fresh template clone (`2562949`) checks with "no problems", with no index diff.

The rule audit and its rulings are in D-053.

**Feature branches, tried by the ACE from clean checkouts:**
- **`spike/analysis`:** 22 tests pass, and the executed notebook has 11 code cells, 0 errors and 7 plots.
- **`spike/obsidian-plugin`:**
  - It builds with Node v26.13.1 and passes 31 of 31 tests, including 5 end-to-end tests. Those install the built
    plugin into a scratch vault and run real uv and `scat_kg`: the case study comes back clean, and the seeded defects
    are reported as errors.
  - The PM reported 31 passing without saying that the end-to-end tests skip unless the plugin is built and a
    template clone is present.

  Both features are ready for the chief engineer to try, and neither is merged into `dev`.

**Findings for later packages, not v0.1:**
- `scat check --json` and `--stdin` would remove the plugin's Python shim.
- A public vault loader would replace the analysis package's import of the internal `scat_kg.vault.read_vault`.

**Mission Amendment 2** is drafted as PR #4 on `amendment/2-structure-and-style`:
- R-1 states structure-only conformance;
- R-15 and G7 become "a light musical reference, clarity first";
- the non-goals note that the plugin and analysis are explored on feature branches.

This reconciles the mission's text with D-052. Approval is by the chief engineer's merge of PR #4. The log is not
edited on that branch, so `main` and `dev` won't conflict at release.

**Small items, left as they are:**
- the `advisory` fix kind in the catalogue is now unused;
- the logo shows only in the drawer below about 1,220 px (Material's behaviour, which predates WP9);
- the RS unit estimates were recorded after the fact.

## D-056 | 2026-11-24 | Dependency factoring: each layer brings only what it needs

**Asked by:** the chief engineer, after merging Amendment 2: confirm that analysis dependencies are separate from the
conformance tools', and keep dependency tracking and factoring careful so a user installs only what they need.

**Confirmed (checked, not assumed):**
- The `scat-kg` wheel built from `dev` declares only `pydantic`, `PyYAML` and `rdflib`. Installed alone into a fresh
  venv it brings 9 packages, none of networkx, pandas, matplotlib or Jupyter. `dev`'s `uv.lock` names none of them.
- The analysis spike is its own uv project (`research/analysis/pyproject.toml`, own lock) and depends on `scat-kg`; it
  adds nothing to it. The plugin prototype's npm dependencies are all dev-time (bundled into `main.js`); on the
  Python side it needs only the `scat` CLI.

**Ruling (ACE):** dependencies are layered by use, and a direct import is a declared dependency of the layer that
makes it. Applied on `spike/analysis` (`448a012`):
- core `scat-analysis`: `scat-kg`, `networkx`, `pandas` (load a vault, run the analyses, DataFrames out);
- extra `plot`: `matplotlib`, `numpy` (`scat_analysis.plots`; importing it without the extra raises an error that
  says how to add it);
- dependency group `notebook`: Jupyter, nbconvert, ipykernel, never a runtime dependency; installed by default in a
  checkout so the one-command notebook run is unchanged.

Each layer was installed on its own and exercised: core runs the analyses with no matplotlib present; core + `plot`
imports the plots; the default environment passes 22 tests and executes the notebook headless.

**For the delivery packages:** the analysis package still reaches into `scat_kg.vault.read_vault` (internal), and the
plugin uses a Python shim for JSON output. Both point to the same small public surface in `scat-kg` (a vault loader,
`scat check --json`), which adds no dependencies to it.

## D-057 | 2026-11-24 | A second axis, grounding, goes into v0.1; the play test is paused

**Raised by:** the chief engineer, during play-test sitting 1 (stage 1 issued, not yet reported). In summary: SCAT should
record whether a story is historical or demonstrative, and whether an architecture is as-is or to-be (other terms are
acceptable). With behavioural vs structural, this gives a 2×2 lens: grounded in observation of what exists, or
imagining or projecting what could be. The narrator's normative posture (good, bad, a mix) stays out of the schema and
in the story's own text; problematization belongs to a richer ontology such as ANT, applied afterwards. SCAT is
pragmatic and thin, and does not compete with ANT-RDF; the same case can be coded in both with different tools.

**Question (typed by the ACE):** "Should the grounding axis (historical/demonstrative, as-is/to-be) go into the v0.1
release, or come after it?"
**Answer (the chief engineer's choice, typed by the ACE):** "Into v0.1".

**Consequence.** The play test is paused at stage 1 against candidate `e1701ab`. The change is a mission amendment
(Amendment 3: the TBox is fixed per release), then a package, then a refreshed candidate, then the play test restarts.
Tag `divergence/D-057` marks `dev` before this direction. Open questions for the amendment are being put to the chief
engineer one at a time and recorded here.

**Question (typed by the ACE):** "Must every scenario and architecture state its grounding (observed or projected),
so a missing value fails the check?"
**Answer (the chief engineer's words, typed by the ACE):** "these additions don't go into the coded ontology so impact
should be minimal its only for scenarios and architectures. required but allow "mixed" as an option."

**Outcome.** Grounding is required on scenario and architecture pages, with three values (observed, projected, mixed);
the four SCAT classes and three relations are unchanged. Placement, names and severity on unfinished pages are the
ACE's defaults in Amendment 3, approved with it.

**Clarification (the chief engineer's words, typed by the ACE):** "by doesn't go into the coded ontology i mean the
stakeholders, concerns, affordances and technologies are not marked with this axis."
**Outcome.** Amendment 3 now says so in plain words: grounding marks scenario and architecture records only.

**Direction (the chief engineer's words, typed by the ACE):** "to avoid complexity i want this to be essentially a past
future axis. present is nebulous and thing real that can be narrated is past. any thing being done with intention in
the present but not yet realized is future."

**Question (typed by the ACE):** "With grounding as a past/future axis, does "mixed" stay as a third value (past,
future, mixed), or is it now just past or future?"
**Answer (the chief engineer's words, typed by the ACE):** "(past, future) for the 2 x2 grid in the documentation.
however past our future applies to the scenario or architecture narrated and most people mix them together freely.
ideally facilitation would guide the participants to focus on past and future at seperate times in the workshop so that
its easier to sort. allowing mixed is just being honest that sometimes the accounts people give blur the two together
and its an honest ability to record that"

**Outcome.** The axis is past/future, with values `past`, `future`, `mixed`; the docs' 2×2 shows past and future; the
facilitation guides separate past and future in time. The import-don't-mint naming check is dropped: the chief engineer
set the values. Working field name `timeframe` (ACE default, in Amendment 3).

**Direction (the chief engineer's words, typed by the ACE):** "i called them past and future to avoid the reaction but
to be clear in the explanation about how to use these fields. counterfactual stories about "what would happen if" is
future, and historical descriptions "when someone would do x then y happens" is past. i think our facilitation guide
should have a list of examples of phrases (including non obvious ones) to guide the user. this stuff stays strictly in
the facilitation documentation as it just tags the captured narratives. don't bloat, this is meant to improve the
structure of the facilitation and data capture so that we can allow both types of narration but reduce the mixing to
make it a bit more interpretable after the fact. this should be address by a full work cycle rather than edited adhoc
in place since that risks destabilizing the repo. think of it as a blast radius targeted work package focused on
tightening the facilitation -> recorded raw narratives so we get a cleaner data set"

**Outcome.** Amendment 3 states the counterfactual and habitual cases and that the guidance lives in the facilitation
guides alone. The build is WP10, a scoped package with a named blast radius (`work-packages/WP10.md`), approved by the
ACE once Amendment 3 is merged; nothing is edited in place before then.

## D-058 | 2026-11-24 | Amendment 3 merged; WP10 approved; test edits authorised

**Approval.** The chief engineer merged Mission Amendment 3 (PR #5, merge `023c5f4`) and wrote "Merged, go". `main` is
merged into `dev`. The ACE approves WP10 (`work-packages/WP10.md`). Revert point: `divergence/D-057`.

**Question (typed by the ACE):** "WP10 makes `timeframe` required on raw pages, so existing test fixtures and the
assertions on them must gain the field (additions only, no weakened checks). The test-edit guard only accepts that on
your direct word. Do you authorise WP10 units to edit existing tests for this?"
**Answer (the chief engineer's choice, typed by the ACE):** "Yes, authorise".

**Direction for WP10 (the chief engineer's words, typed by the ACE):** "let me note that for architectures past can be
baseline (as is) and target (to be). TOGAF is a fine source to borrow from but don't force cite it. just explain in
plain language. the architectures also have mixed as stories often involve a lot of things that exist and things that
could exist so its still fits. we will need similar examples of things people might say and how to label them for the
architectures"
**Outcome.** WP10-R3 now asks for the phrase list in two parts, scenarios and architectures, with architecture past =
baseline (as-is), future = target (to-be), mixed allowed, in plain language. The 900-word cap (R4) stands. The PM is
told mid-package.

## D-059 | 2026-11-24 | The code play test runs on the template mid-WP10, by the chief engineer's choice

**Context.** The chief engineer began testing the code (reviewer's guide, sitting 3, then hands-on) while WP10 runs.
His bench is `~/scat-playtest`: tools at `e1701ab` (green block: 522 passed, lock, ruff and the strict build clean;
benchmark 245, 249 and 286 ms), and a fresh template clone that came out at `cdc0707` (WP10-U3, raw case-study pages
tagged `timeframe`), not the candidate `2562949`. Its pin is still `e1701ab`, whose tools ignore the unlisted key
(contract section 2, by design), so `scat check` gives `no problems`. The ACE offered to pin the clone back to
`2562949`.

**Decision (the chief engineer's words, typed by the ACE):** "i am okay with testing on the new one with the extra
field added. lets just make sure we track that choice"

**Consequence.** Findings from this sitting are against template `cdc0707` with tools `e1701ab`. The field's own
checks are not exercised here, because the pinned tools don't know it yet; they are covered by WP10's tests and the
refreshed candidate. Also noted for a later package: Material for MkDocs reaches end of life on 5 May 2027 (its build
notice names Zensical as the successor); no effect on v0.1.

## D-060 | 2026-11-24 | A stable machine interface before the first release (Amendment 4)

**Raised by:** the chief engineer, in play-test sitting 3, step 4, on the messages (finding F-4): "seems fine. can be a
bit hard to read but honestly that's mostly the REPL, not something we can change. the reason for building the
obsidian plugin is so we can capture that information payload and use it. so the only thing i'd look out for is how
ammenable the output is to use to develop the plugins features later. we want clean interfaces with stable interface
contracts"

**Direction (the chief engineer's words, typed by the ACE):** "i want you to make the output stable for plugin before
first release since i am leaning towards potentially pushing toward obsidian plugin pretty directly"

**Outcome.** Mission Amendment 4 (PR #6) adds R-16, a stable machine interface: versioned machine-readable data for
every result, on both paths, with its schema in the contracts and fixes as applicable data. The build is WP11, drafted
when the amendment is merged, and sequenced after WP10's code unit (both touch `src/` and `tests/`).

**Process note (ACE).** While the amendment was drafted, the ACE switched the shared main checkout to the amendment
branch, and a PM board/metrics commit (`5e9365a`, with an untracked `site/` build folder swept in) landed there. It was
never pushed. The ACE undid it locally, removed the build folder, and checked that the PM's records are on `dev`
(they are). From now on the ACE drafts in its own worktree and never switches the shared checkout's branch.

## D-061 | 2026-11-24 | The estimation data is an operational requirement, checked in CI

**Raised by the chief engineer (his words, typed by the ACE):** "also i want to make sure we're keeping to our work
estimation practice. i find this data very helpful to review work:
https://github.com/DynamicalSystemsGroup/scat-kg-tools/blob/dev/work-packages/metrics.jsonl", then "i want to make this
an operational requirement since it impacts my ability to assess delivered code".

**Outcome.** `ORG.md`, "Status reports", now states the operational requirement. `work-packages/check_metrics.py`
(standard library only) enforces it on every record after line 251, the log's length when WP10 was approved. Earlier
records are history: they predate the check, and several WP8 records would fail it (no `actor`, first recorded as done,
one estimate of 12 points). CI runs the check on every push, once WP10's records pass. The ACE accepts a package only
when `--accept WPn` passes.

**First run (ACE).** The practice was kept in substance for WP10: units were planned with estimates at 09:13, two minutes
after approval and before work landed; realized points carry a basis; and a mid-package scope change is named in
U2's basis. It found one gap: the four `done` records (U1 to U4) lack `iteration`, which the schema requires. The PM
appends corrected records. Also noted: U4 was split, with U4 at 5 estimated and 2 realized, and U4b planned at 3 when
it started. The split is now ruled: the original unit keeps its estimate, and the new unit is planned before it starts.

## D-062 | 2026-11-24 | Amendment 4 merged; WP11 approved and queued behind WP10

**Approval.** The chief engineer merged Mission Amendment 4 (PR #6, merge `519ff5a`) and wrote "merged". `main` is
merged into `dev` (`f014572`). The ACE approves WP11 (`work-packages/WP11.md`): JSON contract and versioning rule,
fixes as data, `--json` on every command with a Python equivalent, no new runtime dependency, references, refresh.

**Sequencing.** WP11 starts when WP10 is accepted, because both touch `src/`, `tests/` and the reference docs.
`divergence/D-060` is tagged on `dev` then.

**Held for the chief engineer, if it arises.** His D-058 authorisation covered WP10's test edits only. WP11 aims to
keep every golden message identical. If an existing test must change, the unit is held and the question comes to him.

## D-063 | 2026-11-24 | WP10 accepted

**Evidence, run by the ACE.**
- `python3 work-packages/check_metrics.py --accept WP10`: `metrics ok: 269 records (18 under the practice); WP10 is
  ready for acceptance`.
- Iteration 10: 23 points estimated and 23 realized, 0.72 h.
- 560 tests passed on `dev`.
- CI and Pages are green on `9a9b58e`. The red CI on `7a0c61f` was the ACE's metrics check failing ruff; it was fixed,
  and the check now runs in CI.
- The ACE read the phrase list against the chief engineer's words (D-057), and every mark follows them: the
  counterfactual is future, the habit with "would" is past, under way but not realized is future, past is baseline and
  future is target. The PM's report gives the evidence for R1 to R6.

**Rulings on the PM's flags.**
1. Red CI: fixed (above).
2. The stray commit: resolved (D-060).
3. `SCAT-DRAFT-FIELD` warns on a raw stub without `timeframe`. Accepted: it is Amendment 3's default, a warning
   before `done`.
4. Case-study tags. Accepted as they are. Both pitches are `future`: when told, each proposed what was not yet
   realized, which is the rule's test. The Chatham House scenario is `mixed`: it blends how sessions run with the
   design being set up.
5. The stale `scat:valueSet` annotation: play-test finding F-5, for the fix package.
6. The docs test doesn't run the transcripts: a known weakness since D-043. The PM checked them by hand.
7. Nobody has seen the rendered tables: F-6, which falls to the chief engineer's docs sitting.
8 and 9. Wording nits: accepted as they are.

**Lessons recorded.** A unit that changes tool output plans the transcript reruns of the units that show it. A pin
that another unit's test depends on is its own unit, planned up front.

## D-064 | 2026-11-24 | The trial example names its intended outcome

**Direction (the chief engineer's words, typed by the ACE):** on the phrase "We are trialling weekly checks" (future,
under way but not yet realized): "this needs an "in order to clause" to make it clear that the outcome that the
intended behavior is produced by the intervention is still hypothetical"

**Outcome.** One table row in `docs/facilitate-scenarios.md` now reads "We are trialling weekly checks in order to stop
drills going missing." Its reason: the checks are under way, but that they stop the losses is still a hypothesis. The
ACE made the edit directly: one row, outside WP11's blast radius, with the strict build clean.

## D-065 | 2026-11-24 | The template pin edit authorised for WP11

**Direction (the chief engineer's words, typed by the ACE):** "yes, authorise the pin edit and accept WP11."

**Outcome.** WP11-U11's one edit to an existing test file, the `TEMPLATE_COMMIT` line in `tests/docs/conftest.py`
(and its comment), from `6ebd305` to `5a7290f`, is authorised. The ACE checked that it is the only pre-WP11 test line
WP11 changed: `git diff a3edae4 origin/dev -- tests/` shows one deletion in total, that line. Every other test change
is a new file, or a file WP11 itself added.

## D-066 | 2026-11-24 | WP11 accepted

**Direction:** the chief engineer's words in D-065.

**The ACE's own verification, on `dev` at `30ddc6f`.**
- `python3 work-packages/check_metrics.py --accept WP11`: `metrics ok: 311 records (60 under the practice); WP11 is
  ready for acceptance`. Iteration 11: 52 points estimated, 51 realized, 2.14 h.
- `uv run pytest -q`: 982 passed. Ruff, the format check and `uv lock --check` are clean. CI and Pages are green on
  `30ddc6f`.
- R3: the wheel built from `30ddc6f` lists `Requires-Dist: pydantic`, `pyyaml`, `rdflib` and nothing else.
- On a fresh clone of the template at `5a7290f`, with a one-letter link typo seeded: `scat check --json` exits 1 and
  prints one document (`schema_version` 1, `SCAT-LINK-DANGLING` with file, line and field, and a fix of two exact
  options, one an edit and one a command). `scat_kg.check().to_dict()` equals it. The `con` refusal with `--json` gives
  one `operation` document with `ok` false and exit 1.
- The ACE read `contracts/machine-interface.md` as a plugin developer would, without opening `src/`: the versioning
  rule, the rule-id policy, the streams and exit codes, the stable fields and the edit actions are each stated once and
  are enough to build on.
- The template checkout the chief engineer will show was pulled to `5a7290f`; `scat check` prints `no problems`.

**Rulings on the PM's flags.**
1. The pin edit: authorised (D-065).
2. The relation-type refusal stays `manual`: accepted for v0.1. A multi-placeholder command rule is a later-package
   candidate.
3. "Every": restored by the ACE ("Every `scat` command takes `--json`"). The page is now at its 600-word cap, and the
   machine and docs tests pass.
4. The edit-vocabulary limits (`rename-file` doesn't rewrite links, an add-only exact option, whole-list `set-field`):
   accepted. The contract states each one.
5. Harness gaps: accepted. The golden tests cover what the guards don't. Later-package candidate.
6. The JSON blocks were seen by DOM measurement only: joined to F-6, for the chief engineer's docs sitting.
7. The reviewer's guide: the ACE fixed the wording nit and added D-064 to D-066 to the table of the ACE's calls.
8. U11's own run of the nine CLI examples (9 of 9 equal) stands. The ACE's fresh-clone run above confirms the first.
9. U5b merged before its review: a process slip, recorded. The later review passed. The rule stands: review, then
   merge.
10. Estimation lessons: as on the board.

**New finding.** F-7: the reserved-name refusal offers a concrete name, but its fix is typed `manual`. It goes to the
fix package with F-1, F-3 and F-5.

## D-067 | 2026-11-24 | A terms reference page for the coordinating project manager (Amendment 5)

**Direction (the chief engineer's words, typed by the ACE):** "i am going to need to have page in the documentation
thats just a reference schema". Asked which schema, he answered: "the vault schema. and to be clear this needs to be
pretty simple. its almost like a glossary. it should only cover load bearing terms and in the coding. Elicitation,
Scenario, Architecture, Stakeholder, Concern, Affordance, Technology. Plus connective tissue between them, its a bit
more than the ontology for coding but not much more. it needs to be a reference for the project manager who is
coordinating an event, supervising field note capture, and will be responsible for ensuring the data gets coded, and
analyzed satisfactorily"

**Outcome.** G7 lists the docs pages, and this one is new, for a reader the mission didn't name. So it goes in as
Mission Amendment 5 (PR #7): one sentence in G7 and one Agent's default. The ACE wrote WP12 to build it. WP12 is
approved when PR #7 merges.

## D-068 | 2026-11-24 | The terms reference is a fix for a field finding, not a mission change (supersedes D-067)

**Direction (the chief engineer's words, typed by the ACE):** "is it a mission change? i guess it impacts the
deliverables but i am not sure its actually a new requirement rather than an implementation detail. this feedback
comes from showing the documentation to a real user in a real field site. the PM in question expressed confusion and a
need for a place to check the "schema" so she can more clearly see how this relates to her facilitation plan, the
field note taking, the coding, and analysis work that follows. so i am giving you her feedback vis-a-vis the current
mission"

**Ruling.** The ACE agrees. The mission already serves this reader. J4 to J7 describe the user who plans the event,
captures the notes, codes them and finishes the vault. G7 and D-4 already make the docs site serve that journey. A
real user who can't see how the pieces relate is a user-acceptance finding against the current mission (F-8). Fixing it
with a reference page is an implementation detail inside D-4, so it's the ACE's call. Amendment 5 (PR #7) is withdrawn,
and D-067's outcome is superseded. WP12 is approved now. Its scope gains one thing from her words: each term says where
it enters the work (plan, capture, code, analyse).

## D-069 | 2026-11-24 | Two more pages for F-8: the end-to-end flow, and data, rights and consent (WP13)

**Direction (the chief engineer's words, typed by the ACE):** "yes close it. let's also keep in mind that her feedback
amounted to not seeing how to use this. my concern is that our current documentation also lacks a summary of the flow.
my gut is we need 2 additional pages. one which summarizes the end to end flow (essentially a user journey like flow
that is intuitive and is really just a simple lifecycle model from identifying a fieldsite and participants (getting
and documenting their consents to participate and being clear about what their contributions will and will not be
used for). then we have facilitation planning and which may involve structured, semi-structured and unstructured
interactions (which may or may not be recorded, stored, published, etc - see explicit data rights/consents). this is
an important dimension that is often neglected. we do not need to go into the level of detail covering how we studied
these topics [...]. my feeling is that we need need to have a page covering making data storage, data rights and
consents explicit so that people who choose to use scat are at least adequately informed about these operational
details but we shouldn't go into great length nor should we make normative judgements about what data rights and data
use commitments etc should or should not be offerred. our documentation should continue with the pattern of naming the
activity as a dependency and offerring "for example" to help the user understand what we mean."

(The elision drops the names of the research projects and people he mentioned as background. He said the docs need
not cover them.)

**Outcome.** PR #7 is closed, with its branch kept as the tag `archive/amendment-5-glossary`. Following D-068, the two
pages are fixes for F-8 inside G7 and D-4, not a mission change. The ACE approved WP13 (`work-packages/WP13.md`). It is
queued behind WP12, because both touch the nav and the home page. Its bar: no page prescribes a policy, every activity
is named as a dependency with a "for example", and a cold project-manager reader can find her way.

## D-070 | 2026-11-24 | Chatham House and personal attribution are example policies, not the rule

**Direction (the chief engineer's words, typed by the ACE):** "we can use the chatham house rule vs personal
attribution as examples of a policies, rather than asserting it should always be chatham house"

**Outcome.** WP13 gains G4 and R3b:
- The consent page shows the Chatham House rule and personal attribution as two example policies.
- The home page, the planning guide and both facilitation guides stop saying every session must run under Chatham
  House. They refer to "the participation terms agreed for the event", with Chatham House as the example the case
  study uses.

What the tools record stays stated as fact: coded pages name groups, never individuals, and attributing statements
to individuals remains a v0.1 non-goal (MISSION.md). The mission is unchanged. Its line "How raw notes are taken is
the facilitator's call" already leaves the policy open. `divergence/D-070` is tagged on the commit before this ruling.
WP12's terms page is held to the same stance.

## D-071 | 2026-11-24 | WP13 widened: AI use, publication split, and a pre-start checklist

The chief engineer's direction (chat, typed by the ACE):
"LLM use allow or disallow, and if allowed which tools and which data they are allowed to touch is also part of the
explicit user choice dimension but it needs to be matched up with expectations set at the time consents are secured,
and the consents should be demonstrably informed consent to the extent possible. people participating in exercises
from which the data for these coded scenarios and architectures need to know this what their inputs are being used
for, the attribution vs chatham house is a good example because it really could go either way but all participants
have to work within the same paradigm so the organizers need to decide and communicate clearly up front. whether the
resulting analysis can be published is also a different quest than whether the field notes can be published. i think
a really good addition to this would a be a short bang list of questions that need to be answer and documented before
starting a scat project."

ACE outcome: WP13 stays a docs package inside G7 and D-4, and is not yet started, so its scope is widened in place:
- G2 gains AI use (allowed or not, which tools, which data), matched to the consents; the publication item splits the
  analysis from the field notes; consent is described as informed, decided up front, one set of terms for everyone.
- New G5: a "Before you start" checklist of questions, one per G2 item, answered and documented by the organisers.
  The page still makes no choice for them.
- R2 now covers six items and the checklist, with the cap raised from 600 to 750 words.

Mission Amendment 5 (PR #8, decision 3) aligns the mission with log D-070, so WP13's note "the mission is unchanged"
is superseded once it merges. Amendment 5's ordering default folds WP13 into the schema-change package; this
widening travels with it.

## D-072 | 2026-11-24 | WP13: release levels, licence, follow-through, and two readers

The chief engineer's direction (chat, typed by the ACE):
"'Publishing the analysis and publishing the field notes are now two separate questions.' there is also a level that
makes things non public release but release to contributors. and published itself is nebulous, under what license, eg
creative commons? or what. i don't want you to litigate all possible answers instead we want pose the questions as
open ended with 2 to 3 reasonable answers each to show these are genuine choice without overloading cognitively. we
also need to thoughtful about how this documentation is written since its a different user who just wants to play
with the modeling approach on their own work and data from one who is actually organizing a facilitated session with
contributors. we're building this for analysis of data from a contributor group use case so we have these extra
questions as sign posts for organizers to 'make the right way the easy way' where the 'right way' here includes
clear expectations setting, consents and following through on the commitments made to the people who choose to
participate in the facilitated elicitation."

ACE outcome (WP13 not yet started; widened in place):
- G2's release item names levels between private and public (for example, contributors only), keeps analysis and
  field notes separate, and asks under what licence anything is published. A seventh item: how commitments to
  participants are followed through.
- G5: each checklist question is open-ended and shows 2 or 3 reasonable answers; none is argued or chosen.
- New G6: two readers, the solo modeller and the organiser of a facilitated elicitation. SCAT is built for the
  organiser; the flow page signposts both, and makes the organiser's commitments the easy path.
- R2: seven items, the checklist's answer format, the two-reader signpost; cap 800 words.

## D-073 | 2026-11-24 | WP13: the consent page is organised by three classes of material

The chief engineer's direction (chat, typed by the ACE): "3 separate classes need to be have different rules: * the
'inputs': field notes * the 'model': the git repo (coded notes + full knowledge graph) * the 'analysis': derivative
reports (jupyter notebooks and/or documents written using excerpts, data or figures)". On where raw narratives sit:
"that is the inputs. the inputs are the supplied materials [...] i do no want the details of my pilot project in the
open soure repo so you need to keep the options we are chosing for that project as examples in the choice set but
they are one of 2 to 3 reasonable alternatives and our alternatives are not presented as exhaustive just demonstrative
of the fact the choice matters". The cut [...] holds project-specific details, removed at his instruction.

ACE outcome: Mission Amendment 5 (PR #8) names the three classes. WP13's consent page is organised by them, asks each
item per class where the answer can differ, and shows no project's choices as such.

## D-074 | 2026-11-24 | WP12-U5 corrections made by the ACE; stale release PRs closed

The chief engineer's instruction (chat, typed by the ACE): "you are clear to make the described as well as clear to
close PRs without merging if they are no longer on the path to delivery. i will squash merge the PR 8 as the signal
that you are clear to enter autonomous mode when i am ready".

ACE outcome:
- WP12-U5's branch (`wp12/u5`, b1fce7f) is merged into `dev`, with the corrections its review asked for, which a
  guard had refused when the instruction reached a worker as an agent message: the acceptance README's persona counts
  now separate the three journey personas from p4's page cold read; the reviewer's guide covers items (a) to (p); and
  item (p) no longer claims every question was answered correctly in every round, but says what the PM fixed and
  points to the reports. 990 tests pass.
- The release PRs `scat-kg-tools#3` and `scat-kg-template#1` are closed without merging. They carry the candidate from
  before Mission Amendment 5, which the next candidate replaces; new release PRs are opened at the candidate stage.
- WP12's acceptance (metrics, the PM's closing record) waits for the autonomous run, which starts when the chief
  engineer squash-merges PR #8.

## D-076 | 2026-11-24 | Mission Amendment 5 merged; `dev` synced; revert point

The chief engineer merged PR #8 (merge commit 0e74f19 on `main`), which rewrote `MISSION.md` as a self-standing
document and added `GLOSSARY.md`. The decision records are in the PR #8 thread. His words: "i merged it". The merge
is the signal to enter autonomous mode (his earlier words: "i will squash merge the PR 8 as the signal that you are
clear to enter autonomous mode when i am ready").

ACE outcome:
- `main` is merged into `dev` (c0cb9c4), so `dev` carries the mission and the glossary.
- Revert point: tag `divergence/D-076` on 778e070, the `dev` commit before the merge.
- The PR branch is deleted. The merge was a merge commit, not a squash, so an early commit on that branch with a
  line the chief engineer asked to keep out of the public repo is in `main`'s history; removing it needs a
  force-push to `main`, which is his call. It is on the morning list.

## D-077 | 2026-11-24 | WP12 accepted

Evidence: `python3 work-packages/check_metrics.py --accept WP12` passes (338 records); CI and Pages green on c0cb9c4,
whose content differs from the head (d8f87b7) only in the metrics log and the board; 990 tests passed at 778e070; the
terms page and its drift test are on `dev`; the four cold-reader rounds and the U5 corrections (D-074).

Rulings on the PM's flags:
- The Elicitation entry's "Vault: none" against its clean-check line, and the page's other entries, are superseded:
  Amendment 5 changes the narrative model (one page per narrative, nodes and edges, fingerprints), so the terms page
  is rewritten in the ontology-and-layout package against `GLOSSARY.md` (R-18). No fix now.
- Status placed at "capture", and guide-derived claims outside the drift test: accepted for v0.1's current page;
  the rewrite revisits both.
- The page at its 600-word cap, and the U4 filing without a separate reviewer: accepted.

## D-078 | 2026-11-24 | The team set up for Mission Amendment 5; Pages deploys trimmed

ACE outcome:
- `ORG.md`: two new roles (the change consultant, the architecture reviewers); the loop adds the impact map before
  approval and the re-sweep before acceptance; the scope rules add `GLOSSARY.md`'s words, an impact map for any change
  to a term, contract, rule or the mission, and, after WP15, the architecture's modules and contracts; glossary
  changes are a swept, logged ACE call.
- Role files `.claude/agents/change-consultant.md` and `.claude/agents/architecture-reviewer.md`; the PM's role puts
  the glossary and the three actors in every brief.
- `work-packages/plan.md` rewritten for the mission as merged: WP14 prior art, WP15 architecture, RS3 chat-path
  spike, WP16 ontology and layout (absorbing WP13), WP17 views, WP18 chat path, WP19 range vault, WP20 candidate.
- Pages: the chief engineer asked to save runner minutes ("try not to run quite so many deployments. you will eat up
  all our runner minutes", with a screenshot of 161 deployments). The Pages workflow now runs only when what the site
  is built from changes (`docs/`, `mkdocs.yml`, `src/`, `pyproject.toml`, `uv.lock`, the workflow), and a newer
  deploy cancels an older one. CI still runs on every push (R-7); the team batches pushes, so records-only commits
  ride along with real work.

## D-079 | 2026-11-24 | WP14 (prior-art readout) approved

Scope `work-packages/WP14.md`: a readout of at most 1,800 words in `research/prior-art/`, answering five questions for
WP15 and WP16, with public sources cited and private ones read for principles only. Mission item 6 (prior-art readout
as input) and Governance ("the prior-art readout comes before the architecture document"). No impact map: it changes
no term, contract, rule or mission text.

## D-080 | 2026-11-24 | RS3 (chat-path spike) approved

Scope `work-packages/RS3-chat-path.md`: five questions on the inference.coop chat, how it reaches the tool, the
workflow, working with no terminal, and the views; offline first, then light live use with lab material after the
chief engineer signs in. `MISSION.md` G14 and the Agent's defaults ("The chat-path spike"). Runs beside WP15; the
ACE drives the live part.

## D-081 | 2026-11-24 | WP14 scope corrected; WP15's path; the ACE's calls on the WP16 impact map

**WP14.** The PM's scope check failed WP14 (no units started). Its findings were right and are fixed: the scope named
private repositories in this public repository (the ACE's error; the names now go only in the PM's brief, and the
earlier commits are in history, which the chief engineer may choose to rewrite); "typed connections" is now "edges";
an undefined acronym is replaced by plain words; the word cap excludes the source table; the source table has one
"earlier private work" row; a definition of good is added. WP15's draft gets a definition of good, and its document
moves to `contracts/architecture.md`, outside WP16's `docs/` edits, as the change consultant's overlap table advised.

**WP16 impact map** (`work-packages/impact/WP16.md`, section 8). The ACE's calls:
1. WP16 may run spike work (layout experiments, on a spike branch, checked in Obsidian) before WP15 is approved; its
   decide and build stages wait for WP15 (R-22).
2. Edge, relationship annotation and index page as page or field: decided in WP16's layout stage, in Obsidian (G15).
3. Type slugs and the ontology's edge names: decided in WP16's design, against WP15's contracts. Renaming or removing a
   field of the machine interface bumps `schema_version` (R-16's rule).
4. What a user sees follows `GLOSSARY.md`: "index page" in messages, docs, the folder and the `type` value. The
   ontology's own identifiers may keep formal names, labelled with the plain word.
5. Migration: a one-off in the template unit and the test fixtures; no migration operation ships, since no vault has
   been handed over on the old shape.
6 and 7. Where an edge records its narratives, how the one-link-away scope treats edges, and the names of the
   record-edge and remove-edge operations (R-8): WP16's design, against WP15. `stub_pair` is removed if superseded;
   there is no released interface to keep.
8. The terms page's drift test checks both: the page's words against `GLOSSARY.md`, and the vault names it shows
   against the ontology.
9. The two pins: the PM schedules them in the WP8 and WP11 pattern.
10. `spike/analysis` and `spike/obsidian-plugin` stay as they are.
11. WP16 runs one cold-reader round on the flow and consent pages (carried from WP13-R4).

## D-082 | 2026-11-24 | WP14 accepted; a private name redacted from an old entry

**WP14 accepted.** Evidence, re-run by the ACE: the readout's body is 1,735 words (cap 1,800, source table excluded);
a grep of the whole repository for each private repository's name, outside `decisions/`, finds nothing; the reviewer's
second round passed R1 to R3; `check_metrics.py --accept WP14` passes (358 records); 990 tests passed on the PM's
tier-1 run. The five recommendations go to WP15 (WP15-R2 takes each up or sets it aside with a reason).

**Redaction.** The PM flagged that an early entry of this log named a private repository. The chief engineer's rule
keeps private names out of the public repositories, so that entry now reads "an earlier private bike-domain repository
exists; its name redacted under D-082". This is the one edit to a past record, made by this decision. The name stays
in git history; the morning list carries it with the other history items.

## D-083 | 2026-11-24 | WP15 (architecture document and review) approved

`work-packages/WP15.md`, as drafted and corrected in D-081: `contracts/architecture.md` with model, views and control,
the three actors and two authorities, modules with contracts, links and edges, the coding loop and the journey traced
across modules, and what is left open; three architecture reviewers (two Sonnet, one Opus for the cross-cutting
contracts and links and edges). WP14 is accepted, so the ordering in `MISSION.md` (Governance, "The plan") holds.
RS3 runs beside it; its live part waits for the chief engineer's sign-ins.

## D-084 | 2026-11-24 | The chat route: the coder's own machine now, governed compute after v0.1

RS3's live check (the ACE in the browser pane, signed in by the chief engineer; no message sent, nothing created):
members of the inference.coop chat (LibreChat) can add their own MCP server at a public `https://` address, over
Streamable HTTPS or SSE, with no authentication, an API key or OAuth; Agent Builder offers a model, instructions,
tools, skills and file context. A server on the coder's own machine is not reachable without a public tunnel. Notes on
`spike/chat-path` (`research/chat-path/notes-live.md`).

The chief engineer's decision (chat, typed by the ACE; names of colleagues cut, marked [...]): "own machine now.
governed compute later. deferred because i need [...] to set that up. we do prefer that mcp via governed computer
later just put it after v0.1".

ACE outcome: for v0.1 the MCP server runs on the coder's machine behind a tunnel; MCP on governed compute is the
preferred long-term route, after v0.1, and is listed for after the release. RS3 continues: which tunnel, set up with
no terminal (the chat-path user must not be required to open one), and terminal-free git. Installing any tunnel
software on the chief engineer's machine for the lab run needs his explicit permission first.

## D-085 | 2026-11-24 | WP15 accepted; the architecture document approved (R-22); three calls

Evidence: `check_metrics.py --accept WP15` passes (369 records); the document is 2,499 words (cap 2,500); three fresh
reviewers (two Sonnet, one Opus for the cross-cutting contracts and links and edges) each said "not ready" on the first
pass with five blocking findings in all, which one revision fixed, with about 28 further findings answered in
`research/architecture/review.md`; tier 1: 990 passed. The ACE read sections 2 to 6.

The calls the document left to the ACE:
- (a) Rule 4: a narrative that links both ends of an edge without naming it gets no message; the fingerprint view lists
  such edges as candidates. The chief engineer's words decide it: an edge in a narrative is "about the relationship
  being in the narrative not just the vertices on the ends (thats why its okay to not have edges)", and R-1 keeps
  content out of conformance.
- (b) On the IDE path an agent can run `set-status`; authority there holds by the assistant's file and git review, and
  the docs say so. Accepted as a residual risk; the chat path holds it by construction.
- (c) The prior-art readout's guidance-versus-example gap becomes a WP16 test case.
- The PM's note: WP16's impact map adds `docs/coding.md`, `tests/ops/test_ops_status.py` and the fix-harness tests,
  because the `done` refusal and the edge operations change today's unchecked `set-status`.

The architecture document is approved (R-22): WP16's decide and build stages may start.

## D-086 | 2026-11-24 | WP16 (ontology and layout) approved

Scope `work-packages/WP16.md`, built on the approved architecture (D-085) and the impact map (WP16-U0, with D-081's
calls and D-085's additions). Staged: a layout spike on `spike/layout` (two or three candidate layouts of one lab vault,
reviewed by the ACE in Obsidian with screenshots), then the decide stage (logged), then build, quality control,
integrate (both pins) and the cascade review (the change consultant's re-sweep). Absorbs WP13. The chief engineer is
away overnight: anything that needs him goes on the morning list and does not stop the package.

## D-087 | 2026-11-24 | WP16 scope fixed for the PM's check; RS3's tunnel findings

The PM's scope check failed WP16 on two items, both right: no deliverables list at stated paths traced to goals, and
the goals did not name the architecture modules they build on (R-22). Both are added; nothing else in the scope
changes.

RS3-U3 (research only; nothing installed): the tunnel pick for v0.1 is Tailscale Funnel (free, a fixed URL, TLS ends on
the coder's machine); no tunnel is documented as set up without a terminal, so the chat path needs a shipped launcher,
and whether the Tailscale Mac app alone can switch Funnel on is unverified. Terminal-free git: GitHub Desktop, plus the
GitHub web interface for the template and Releases. A real test of Funnel on the chief engineer's Mac needs his
permission to install it: on the morning list. Whether a launcher counts as "not required to open a terminal" is
answered by the launcher's design in WP18 (a double-click app, no typed commands).

## D-088 | 2026-11-24 | WP16 decide stage: the layout

Evidence: `research/layout/review.md`, the ACE's walk of the three spike variants in Obsidian, with screenshots.
Variant B is rejected: its edges are text strings in fields, which Obsidian shows as dead text. Variant A works but
leaves one frontmatter-only page per edge. Variant C keeps coding and reviewing on one page and removes a class of
mismatch.

The decision (G15 lets WP16 decide which entries are pages and which are fields; it does not change what the graph
means):
- **A narrative is one page** holding its account, with names linked where they appear, an optional list of what it
  refers to beyond the text, and an **"Edges told" table**: one row per edge the account tells (type, from, to, note),
  each end a link.
- **An edge in the knowledge graph is one per pair, built by the tool** from every row that tells it, and it names
  those narratives (G1). Two narratives telling a pair are two tellings, each with its own note; nothing is duplicated.
- **An edge's status is derived:** it is `done` when every narrative that tells it is `done`. The coder signs off
  edges by signing off narratives; there is no separate edge sign-off (G3, read with G15).
- **Recording and removing an edge** (G4) are adding and removing a row, as operations the tool offers and as hand
  edits it checks.
- **Nodes are pages; index pages are Bases** that the tool generates once, so they never go stale.
- **A relationship annotation** is a line on one of its two entries, with a link to the other.
- **Rule 4 (D-085) still holds:** a narrative that links both ends of a pair without a row gets no message; the
  fingerprint view lists the pair as a candidate.
- **The tool reads tables whitespace-tolerantly**, since Obsidian's table editor re-pads them, and the docs say so.
- Obsidian 1.9 or later is required, for Bases.

WP16's build stage proceeds on this. The architecture's open WP16 slots (edge as page or field; where an edge records
its narratives; how the one-link-away scope treats edges) are answered by it; the PM's build units record the answers
in `contracts/architecture.md` within its word cap.

## D-089 | 2026-11-24 | WP16 build: the PM's defaults confirmed; rulings on its flags; a glossary entry added

The PM (WP16 U3 to U5 done on `wp16/build`; U6 to U14 queued; it stopped because its context grew large) recorded its
build-stage defaults in `work-packages/WP16.md` on that branch. The ACE confirms them as written: page types and the
`kind` field, edges as rows with one edge per (type, from, to), whitespace-tolerant table reading, links and
fingerprints, derived edge status, `record_edge` and `remove_edge` (refusing to change a `done` narrative until the
coder sets it to `draft`: done is not frozen, but changing it is the coder's step), the `done` refusal, relationship
annotations as body lines, Bases index pages, `schema_version` 2, and integration on `pm-work` with one push to `dev`
when green.

Rulings on the PM's flags:
1. The machine-interface page exceeds its 600-word cap (1,558 words). The page is cut back to 600 words, with the
   detail moved into the JSON Schema's descriptions and the rule catalogue; the cap test is restored, not skipped. A
   skipped test weakens a requirement, which `ORG.md` forbids.
2. `stakeholder_group_cap` is a user-visible key with no glossary word. The glossary gains **cap** (an addition, not a
   change of any sense; the sweep for "cap" finds it used only in that sense). The key keeps its name.
3. The Bases leave out pages under the template folder; the ACE opens every generated `.base` in Obsidian during
   WP16's acceptance walk.
4. Rule 4 candidates count every pair the narrative links whose edge another narrative tells: that is D-085's intent.
   Accepted.
5. Narratives need `timeframe` before `done`: correct per the ontology; the spike pages are not migrated.
6. U4's fixes after its failed review get a second, independent review before WP16 is accepted.

## D-090 | 2026-11-25 | RS3 lab run: the chat path works end to end; the MCP server runs in a container

The chief engineer's permissions and direction (chat, typed by the ACE): "you have my permission to install tailscale";
for switching on Funnel, "Yes, for this run"; for the tailnet's HTTPS and Funnel policy, "Yes, enable both"; before
enabling HTTPS published the machine's name, "Rename, then enable"; and "i also want the mcp server to be running in a
container if possible. you should have colima."

What was done (notes on `spike/chat-path`, `research/chat-path/notes-lab-run.md`): the spike MCP server, gated by an
API key and run in a read-only Docker container under Colima with the lab vault mounted read-only, was published
through Tailscale Funnel under a neutral machine name and added to the inference.coop chat (the key pasted by the chief
engineer). The co-op's model called the tool through MCP; its answer matched the tool's own output. Two messages, lab
material only. Afterwards Funnel was switched off, the container removed and the MCP entry deleted.

ACE outcome: the container is part of the v0.1 chat route (WP18 ships the image and a launcher), alongside D-084's
tunnel. WP18 takes the findings: Colima cannot read `~/Documents` under macOS privacy rules; Funnel needs the tailnet's
HTTPS and Funnel policy set once, and the machine renamed before HTTPS; the coder pastes the key; the only terminal
step was installing Tailscale. RS3's readout remains to be written (RS3-R1), from its four notes.

## D-091 | 2026-11-25 | WP16 (ontology and layout) accepted; RS3 accepted; the glossary gains "SCAT"

Evidence, checked by the ACE:
- CI and Pages green on tools `dev` 41d1efb; template `dev` 3cdbe60 CI green; the PM's full run 1,770 passed, 0
  skipped; `check_metrics.py --accept WP16` passes (435 records); RS3 likewise.
- The acceptance walk in Obsidian on a fresh template clone (`research/layout/review.md`, "Acceptance walk"):
  narrative pages, all five Bases index pages, and an incremental coding session with the tool, including the `done`
  refusal and the refusal to change a `done` narrative.
- The cold reader's five disagreements between the flow and consent pages are fixed (WP16-U15, reviewer PASS); the
  flow page renders at 375 px.
- The re-sweep's 22 remaining hits are named keeps in the impact map (tests that keep retired words retired, ontology
  identifiers, a decision title).

RS3's readout (`research/chat-path/readout.md`) and its lab run (D-090) meet RS3-R1 to R4.

Carried to the next package, none blocking: the flow page's "Two readers" heading should follow the mission's one
persona ("trying it first"); step 7's dependency should name step 4; a stray `conflicts` comment in
`ontology/scat.ttl`; the reviewer's guide's pin header (WP20 rewrites it).

The glossary gains **SCAT** (an addition: the docs expand it, and the glossary did not).

## D-092 | 2026-11-25 | WP17 (the views) approved

Scope `work-packages/WP17.md`: the view generator in the tool (fingerprint with rule-4 candidates, edge tables,
layered view, traces), CSV and document exports, drawings, the template notebook running in CI (R-17), an analysis
guide, and the three items carried from WP16. Dependency call (the ACE's, `ORG.md`): drawing and notebook libraries go
in an optional extra of `scat-kg` or in the template; the core runtime dependencies stay as they are. No impact map:
it adds, and changes no term, contract field or rule (the change consultant checks the file map). Revert point
`divergence/D-091`.

## D-093 | 2026-11-25 | WP17 held on a guard refusal; future-stamped metrics corrected; two check gaps

**Held: WP17-U3b.** The permission guard refused, twice, a one-line edit to `contracts/machine-interface.schema.json`
that would let `scat draw --out` report a path outside the vault (today only `export-edges` may). The team does not
work around a guard refusal. WP17 is otherwise on `dev` (tools 500b73f, template e8c23d0, CI green, 1,943 tests
passed) and is not accepted until this is settled. It goes to the chief engineer's morning list with two options: he
allows the schema edit, or the ACE rules that `draw` writes only inside the vault (where D-090 already keeps views on
the chat path) and the code changes instead.

**Metrics timestamps.** 45 records (lines 431 to 475) carry times in the future: the PM of WP16-U15 stamped an
invented 09:30, and the WP17 PM then stamped its own records 7 h 52 min ahead to keep the log in time order. Both are
wrong; the log is observations. A correction unit appends, for each, a record with the real time taken from the
unit's commits and a `corrects` field holding the wrong one (`metrics.md`), and `check_metrics.py` gains a rule that
refuses a timestamp more than five minutes ahead of the clock. Elapsed hours inside WP17 are unaffected (the shift was
uniform).

**Check gaps** (the WP17 PM's flags): a narrative's broken row is reported only when that narrative is checked, so a
view drawing other pages silently leaves it out; and a duplicate node name behind a row end silently drops that edge.
Both are defects against R-1 and R-23: the correction unit's PM fixes them, with tests, in the tool.

## D-094 | 2026-11-25 | WP18 (the chat path) and WP19 (the range vault) approved

Scopes `work-packages/WP18.md` and `work-packages/WP19.md`. WP18 builds the MCP server as an optional extra, the
assistant's file, the container and a no-terminal launcher that always ends torn down with the key rotated, the
chat-path guide and the IDE note; its live run needs the chief engineer to paste a key. WP19 rebuilds the public KOI
case from `mzargham/ant-rdf` as a SCAT range vault, coded by hand through the tool. They share no files and run side
by side, under one PM, after the WP17 correction unit (D-093) lands, since that unit also touches `src/` and the
metrics log. Neither touches `contracts/machine-interface.*`, where WP17-U3b is held. Revert point
`divergence/D-093`.

## D-095 | 2026-11-25 | WP17 follow-ups landed: metrics corrected, two check gaps closed

`dev` ed08bdc, CI green; `check_metrics.py` passes on the whole log (536 records), and now refuses a timestamp more than
five minutes ahead. The 45 future-stamped records are corrected by appended records carrying `corrects` (lines 476 to
520); iteration 23 is restated at 1.04 h. The two check gaps are closed: a view refuses, naming the row, rather than
omit a broken row; a duplicate node name behind a row end is named with both files. Two existing tests that asserted
the old silent omission changed with that behaviour, as D-093 decided; both are listed in the unit report. Left for
WP20's cleanup: a narrative with unparsable frontmatter is still left out of whole-vault views silently, and two
sentences in the architecture document need the new refusals. WP17 stays unaccepted only on WP17-U3b.

## D-096 | 2026-11-25 | WP18 and WP19 mid-way: rulings on the PM's defaults and flags

State: on `origin/wp18/build` (e2dfb98), not yet on `dev`: WP18-U1 (the assistant's file), U2 (the MCP server: 13
tools, 3 prompts, core dependencies unchanged, never sets `done`), U3 (image and launcher: read-only root, all
capabilities dropped, loopback only, 401 without the key, key rotated on stop, nothing left running), and WP19-U1 (the
range inputs). Remaining: WP18-U4 (docs) and U5 (the template's IDE skill), WP19-U2 to U4 (the coding), their reviews
and open wording fixes (`work-packages/pm-handover.md`).

The ACE's rulings:
- The PM's defaults stand: the vault is mounted read-write and written only through the tool's operations (the tool
  in the container must write); a WP19 review sample of at least a third of the narratives; WP19's workers set `done`
  standing in for the coder, which the note says plainly.
- `mzargham/ant-rdf` stays cited in WP19 (WP19-R1 requires the citation; it is public).
- The assistant's file drops "where they differ from it, this file rules": precedence belongs to `MISSION.md`.
- **The container runtime for the chat path is Docker Desktop**, which has a graphical installer; Colima, which has
  none, is documented as the alternative for coders comfortable with a terminal. Docker Desktop is untested here and
  installing it needs the chief engineer's permission: on the morning list. Its licence terms are named in the docs as
  a fact, without advice.
- The docs show how to put Tailscale's command line in place from the app's own menu, and how to open the unsigned
  launcher the first time (right-click, Open).
- The launcher never changes tailnet settings itself (HTTPS, the Funnel policy, the machine name); it tells the coder
  which click does it and why. Confirmed.

## D-097 | 2026-11-25 | WP19 accepted; WP18 built, waiting on its live run; WP20 approved

**WP19 accepted.** `check_metrics.py --accept WP19` passes (600 records). The range vault (`research/range/koi/`)
rebuilds the public KOI case as nine narratives and 27 edges, groups only, cited to `mzargham/ant-rdf`; it checks with
0 errors and one warning, `SCAT-NOEDGES` on the narrative that tells no edge, as G1 asks. The ACE read a narrative
against its source: it keeps both readings of a disputed event without choosing, and names where the source is thin.

**WP18 built.** On `dev`, CI green (3686a14): the MCP server (13 tools, 3 prompts, never sets `done`), the assistant's
file, the image and launcher (Docker Desktop's folder searched too), the chat-path guide and IDE note, and the
template's IDE setup skill. The zero-edge warning G1 asks for was missing and is added (`SCAT-NOEDGES`). A new launcher
test assumed a runner without `docker` and turned `dev` red; a guard refused deleting it, and the test was made
independent of the runner instead, with its assertions unchanged. WP18 waits only on WP18-R4, the live run, which
needs the chief engineer to paste a key.

**WP20 approved** (`work-packages/WP20.md`): the candidate, UA-A on the manual path now, UA-A on the chat path in the
chief engineer's sittings, the walkthrough scripts and the reviewer's guide. Revert point `divergence/D-096`.

## D-098 | 2026-11-25 | WP20 mid-way: rulings on the PM's questions

State: WP20-U1 on `dev` (92b64d7: whole-vault views refuse a page whose frontmatter cannot be read, naming the file;
the architecture's sentences added; 2,264 tests passed). U3 to U6 wait on fixes and fresh re-reviews; U2 (the pin)
and U7 (tester provisioning) wait; UA-A round 1 has not run.

The ACE's rulings:
1. The template branch may be pushed by URL to `DynamicalSystemsGroup/scat-kg-template` `dev`, as the candidate
   stage needs.
2. The stray commit "Remove the example" on the template work branch is not published: the pin commit is rebased onto
   the template's `dev` first, and the reviewer checks the pushed tree.
3. The five docs gaps the reviewers found are defects against stated requirements (R-9, R-10, R-11, G9): the
   fingerprint view's command contradiction between the coding guide and the analysis guide; no command to run the
   notebook; the solo trial (J2) without a section of its own; no way shown to see which commit a tag pins; and no
   no-terminal route on the chat path for clone, commit, push and removing the example (GitHub Desktop, D-087). A docs
   unit fixes them before the pin is redone and UA-A runs.
4. The chat path's UA-A has three testers, two on Haiku and one on Sonnet ("most on Haiku"). Their sessions are run by
   the ACE, light and spaced, in the chief engineer's sittings.

## D-099 | 2026-11-25 | WP20: a stop rule for kit reviews; answers to the PM

State: template `dev` pinned to the candidate (d6fa2af, CI green; the stray commit is not in its history). WP20-U2 to U6
and U8 (the docs unit for D-098's five defects, reviewed PASS) are on backup branches, not yet on tools `dev`; small
open defects remain in U3 to U6. UA-A round 1 has not run.

Rulings:
- **The bar for the test kits, scripts and guide** is no checkable defect against a stated requirement (the mission's
  UA-A, the docs as they stand, the glossary), not "no defects". Each re-review checks only the defects the previous
  review listed, so the loop converges; a unit gets at most two review rounds, and anything still open after the second
  comes to the ACE. This is the stop rule the ACE's memory records for test loops, applied to reviews.
- **The uv gap** (a pre-installed uv on PATH): it stays declared in the kit's README and in each report until the
  chief engineer rules (D-040, D-041; on the morning list).
- **Chat-path testers:** three (D-098) meets the mission's "at least two"; no text changes.

## D-100 | 2026-11-25 | UA-A round 1 (manual path): dispositions

Round 1 (reports `acceptance/reports/wp20-r1-p1.md` to `-p3.md`, findings `wp20-r1-findings.md`): three testers (two
Haiku, one Sonnet control) each reached J10 with a clean check, a locked version, the pinned commit and the recipient;
no blocking finding; no report void. The candidate on `dev` is green in both repositories, and R-6 holds on a fresh
template clone (uv pre-installed, declared).

The ACE's dispositions:
- **Fix (docs, then a re-pin): W1 to W7**, as the PM proposed.
- **W9, fingerprint candidates are noisy (three of three testers):** a defect against R-11 and G17's guidance. The
  fingerprint view shows the fingerprint; candidates appear only when asked for (an option in the view, its CLI and
  REPL twins, and the notebook shows how). D-085's intent holds; only the default changes.
- **W10a, `SCAT-MENTION` on an architecture page asks for a group link** that the linking rules discourage there:
  a defect (contradictory guidance). The mention rule does not suggest a link of a type the page type discourages.
- **W10b, a hyphenated group title not offered:** investigated; fixed if the mention matching misses a title it
  should match.
- **W15, work-package commits and `divergence/` tags in a clone's history:** accepted. The documented path makes a
  repository with GitHub's "Use this template", which starts with fresh history; the testers cloned directly.
- **W11** (no documented rename or delete of a node page): accepted for v0.1, listed in the reviewer's guide as known
  weak. **W8, W12 to W14, W16:** accepted as the PM proposed.

Then a re-pin and round 2 with fresh testers on the manual path.

## D-101 | 2026-11-25 | UA-A round 2 (manual path) passes; last docs fixes without a round 3

Round 1's fixes landed (tools `dev` 7d17534, template `dev` 826bc99, CI green, R-6 on a fresh clone): W1 to W7 in the
docs; fingerprint candidates off by default, with an option everywhere; the mention rule no longer suggests a
discouraged link; hyphen and space match in titles. Round 2 (`acceptance/reports/wp20-r2-*.md`, findings
`wp20-r2-findings.md`): four fresh testers (three Haiku, two of them in the Python session through J10, one Sonnet
control) all reached J10 with a clean check and a locked version; no blocking finding; none void. **The manual path
meets UA-A's pass bar.**

Dispositions: X1 (`git add .` sweeps drawings and plan files into a commit) and X5 (the tag name is the organiser's
own) are docs sentences, fixed. X3: a narrative that quotes the field notes carries that text into the model, whose
rules then apply to it; the consent page says so in one sentence, as fact. The rest are accepted as the PM proposed.
Under `MISSION.md` Governance ("the ACE decides, and logs, whether UA-A reruns"), UA-A does not rerun for three docs
sentences after a passing round; the pin moves and CI, R-6 and R-9 rerun.

## D-102 | 2026-11-25 | Release scope: the chat-path run's candidates C1 to C8

The chief engineer's answer, asked as one question about C1 to C8 (`work-packages/candidates.md`), quoted as typed and
recorded by the ACE:

> "C1 is 0.1, C2 needs to be split, having at least one node is conformance requirement but we accomplish it be
> excluding narratives with no coding programatically. and mark them as excluded. they can only become included if
> they are coded. guidance on descriptions is normative (same guidance regardless of whether the author/review is
> human or LLM). probably need to split the rules from the norms into separate concerns here. all that is 0.1
> C3, C4 and C5 all normative guidance probably gets implemented as documentation and skill files that complement cli
> tools already built.
> C6 is really the higher level approach to addressing the above.
> C7 can you use secret management for this. not sure what the right tools are, you can spike. but we want to follow
> better security practices and we want our spin up to tear lifecycle walkthough documentation to describe good
> security practices. Keep in mind we are not telling people they MUST do a build up to tear down loop, we're telling
> them they MAY, and showing them how with the walk through. In the process we're also testing / proving to ourselves
> that we can do just that.
> C8 this is one of the policy options not a recommendation that you should adopt this policy; however its an area of
> concern for our stakeholders so we're going through the effort to ensure the option is actionable."

Outcome as recorded:
- **C1** in v0.1.
- **C2** split, in v0.1. (a) A rule: a narrative with no coded node is excluded from the graph by the tool and marked
  excluded, and becomes included only once coded. (b) Norms: guidance on descriptions (and the like) is the same
  whether the author or reviewer is a person or an LLM. Rules and norms become separate concerns.
- **C3, C4, C5**: normative guidance, implemented as documentation and skill files that complement the CLI tools.
- **C6**: the higher-level approach for the norms above (skill and agent).
- **C7**: a spike on secret management for the session key; the life-cycle walkthrough describes good security
  practice.
- **C8**: one policy option, not a recommendation, made actionable. The walkthrough shows the full set-up-to-teardown
  loop as a MAY and runs it, testing that it is supported.

Release timing for C3 to C8 is put to the chief engineer as one follow-up (D-103).

## D-103 | 2026-11-25 | C3 to C8 are in v0.1

Asked as one follow-up to D-102 (are C3 to C8 also in v0.1?). The chief engineer chose "Yes, all in v0.1". All of
C1 to C8 are built before the release PRs.

## D-104 | 2026-11-25 | WP17-U3b: the schema edit is allowed

Asked whether `scat draw --out` may save outside the vault (the one-line machine-interface schema edit, guard-refused
and held, D-093) or drawings stay inside the vault. The chief engineer chose "Allow the schema edit". The schema gains
`draw` beside `export-edges`; the code is unchanged.

## D-105 | 2026-11-25 | Colima is the chat path's default runtime; the container in the open-source repo

Asked whether to install and test Docker Desktop, leave it untested, or lead with Colima. The chief engineer's answer,
quoted as typed and recorded by the ACE:

> "let's make colima the default since this version we said mac only 0.1. also i think it merits providing the docker
> container or the mcp server as part of the open source repo for the tools. this will make the spin up to tear down
> cycle much clear and more reproducible."

Outcome: Colima becomes the default runtime in the chat-path guide (v0.1 is Mac only); Docker Desktop becomes the
untested alternative, and D-096's install request is withdrawn. On the container: the Dockerfile is already in the
tools repo (`deploy/`); what "providing the container" covers is put as one follow-up (D-106).

## D-106 | 2026-11-25 | Publish the MCP server's image

Asked whether "providing the container" means publishing a built image, documenting the local build, or both. The
chief engineer chose "Publish a built image": CI builds the MCP server image and publishes it at each release, and the
launcher pulls it instead of building. In v0.1, with C7 and C8 (the life cycle).

## D-107 | 2026-11-25 | "Leave no trace" uses the temporary chat; it is an option, not a recommendation

The chief engineer, quoted as typed and recorded by the ACE, with a screenshot of inference.coop's "Temporary Chat"
control (Cmd-Shift-Y; "This chat won't appear in your history and will be deleted automatically"):

> "the leave no trace lifecycle needs to include using the temporary chat setting in session. again this is an option
> we're walk through to show how to handle one of the more extreme policy options not a recommendation that one needs
> to follow that process. for projects that prefer lower friction and less security it does not make sense to jump
> through the extra hoops to "leave no trace""

Outcome: C8 is named the "leave no trace" life cycle. Its walkthrough runs the coding session in a temporary chat, and
it is presented as the way to meet one of the stricter policy options. It is not a recommendation: the guide says
projects that prefer lower friction need not follow it.

## D-108 | 2026-11-25 | The uv gap: test the installer once

Asked whether to accept the uv gap (D-040, D-041) or test uv's official installer once. The chief engineer chose
"Test the installer once". One fresh tester runs uv's official install script before release. Agent's default: the
clean environment is a throwaway home folder on this Mac with uv removed from `PATH` (v0.1 is Mac only; a separate
macOS user account would need the chief engineer's admin password); the installer is uv's own script from its
official site, run once.

## D-109 | 2026-11-25 | Rewrite both histories

Asked whether to rewrite `main` (c58113b, the pilot line), `dev` (20ff07a, private repository names), both, or
neither. The chief engineer chose "Rewrite both": the ACE rewrites those commits, force-pushes `main` and `dev`,
verifies that the text is gone from every reachable commit, and records the old and new heads. This is the chief
engineer's authorisation for those two force-pushes only.

## D-110 | 2026-11-25 | WP8-U1: the two held assertion changes are allowed

First asked with a wrong description (the ACE said the edit touched only the test's setup); the chief engineer chose
"Allow the edit" on that description. The ACE then found, from D-042, that the edit changes two assertions, and asked
again on the right facts: in `tests/ops/test_ops_stub.py`, (1) `not r.ok` becomes `r.ok and r.unchanged ==
("concern/a.md",)` (stub on an existing page of the same type is a no-op, D-039), and (2) the same-type refusal row
becomes a different-type row (`affordance`), still refused. The chief engineer chose "Allow both changes". The ACE
applies exactly these two changes (fixes on `wp8/u1`, `3ed3163`, `9e6ca44`) and nothing else in the test.

## D-111 | 2026-11-25 | WP17 accepted

WP17-U3b applied after D-104 (tools `dev` b739347; full suite 2289 passed; ruff clean). Every WP17 unit is done and
reviewed; `check_metrics.py --accept WP17` passes. The ACE accepts WP17. Iteration 32 (WP17-U3b, WP18-R4): 6 est,
9 realized, 2.6 h, 3.46 pts/h raw; WP18-R4 ran over (setting up the chat's skill and agent, the browser pane's
file-dialog limit, a stall on the paste step).

## D-112 | 2026-11-25 | The uv gap is closed (D-108)

One fresh Haiku tester followed "Getting started" steps 1 to 3 in a throwaway home folder with no uv anywhere on its
path, running uv's official installer. The installer added itself to `~/.zshrc` and `~/.profile`; `uv sync` and
`uv run scat check` gave "no problems". The tester reported FAIL at "open a new Terminal window", but both causes were
the test harness, not the docs: its shells were non-interactive (they skip `~/.zshrc`, so `uv` was not found) and
started outside the home folder. The ACE checked that an interactive login shell in the same home finds `uv`. The
docs' steps hold; no change. D-040/D-041's gap is closed.

## D-113 | 2026-11-25 | History rewrites (D-109) held: the problem is bigger than asked

Before force-pushing, the ACE sized D-109. Commit c58113b is in `dev` as well as `main`, so removing it re-hashes
about 754 commits on `dev` and 59 on `main`; 20ff07a alone re-hashes 248 on `dev`. That orphans the template's pinned
tools commit (pyproject `rev`), the 23 `divergence/` revert tags, and the commit hashes cited throughout the decision
log, board and metrics; and GitHub keeps the old commits reachable through PR #8's head ref regardless. The question
put to the chief engineer did not state these costs, so D-109 is not acted on and the question goes back to him (morning
list).

## D-114 | 2026-11-25 | WP21 approved

WP21 (`work-packages/WP21.md`: rules and norms, the chat path's life cycle, the published image) takes C1 to C8
(D-102, D-103) with D-104 to D-107 and D-110. The PM's scope check ran two rounds (nine fixes, then six, all applied);
under D-099 there is no third round. The change consultant's impact map is `work-packages/impact/WP21.md`, with its
template and branch facts corrected by the ACE (WP18 and WP20 are merged into `dev`; the template's `dev` is 31667fc).
The image push at release waits on the chief engineer's mission amendment (morning list); without it the launcher
keeps building locally. Revert point `divergence/D-114` on `dev`. The ACE approves WP21.

## D-115 | 2026-11-25 | The session key: keychain, never in arguments, deleted at Stop (WP21-U7 decided)

The spike (`research/chat-path/secrets.md`) found the cause of F15/C7: the launcher's dialog passes its text, key
included, to `osascript` as an argument. It recommends keeping the key in the macOS login keychain, written on stdin
(never `-w VALUE`), read with `find-generic-password -w`, passed to the container with `--env-file /dev/stdin`, on the
clipboard only from a "Copy key" button, and deleted at Stop; the `security` calls isolated behind four functions with
a test stand-in. The ACE decides:
- **Keychain, as recommended.** The chief engineer asked for secret management and better security practice (D-102);
  the 0600 file would meet R5's letter, but the keychain keeps the key off disk in plain text, which is the practice
  the life-cycle guide should show. The macOS-specific part is isolated as the note proposes (MISSION, Platforms).
- **The dialog shows the address and a "Copy key" button, never the key.** Needed with either store.
- **Deleting the item at Stop is enough.** A key exists for one session only and the next Start makes a new one, so
  there is nothing left to rotate; the Stop message and the guide say "the key was deleted".
- Not verified, for U8 and the reviewer's guide: a keychain prompt from the built app or a locked keychain, iCloud
  Keychain sync of the item, Docker Desktop.
- The mission's Platforms list should name `security` among the isolated macOS tools: a mission edit, proposed to the
  chief engineer with D-106's, not made.
U8 is unblocked.

## D-116 | 2026-11-25 | Mission edits made; history stays; chat clean-up; template scratch edits discarded; w3id after release

The chief engineer, quoted as typed and recorded by the ACE:

> "i approve the small mission edits. i don't think you need to do history rewrites but you are welcome to make a
> case. i am not worried about deleting conversations on inference.coop since what we're doing now is not sensitive
> we're doing testing to make sure we have processes developed and tested that can be used on sensitive cases in the
> future. you can discard my obsidian edits we were doing scratch work as part of testing. if i had wanted to keep
> those edits i would have needed to commit them via git. we may want to make that a more explicit trigger for
> telling the system to read our written content and update the data in the knowledge graph accordingly. i'll defer
> the w3id PR to after the release so i can point back to the release to justify the PR"

Outcomes:
- **Mission edits made on `dev`:** Release step 3 also publishes the MCP server's container image from the tools tag
  (D-106; the repository variable `SCAT_PUBLISH_IMAGE` is set at release); Platforms names the chat path's launcher as
  macOS-only by design, with its macOS tools (among them `security`) behind its own functions (D-115).
- **History rewrites dropped.** D-109 is withdrawn; the ACE makes no case for them (D-113's costs outweigh the gain,
  and GitHub keeps the old commits reachable regardless).
- **No further clean-up in inference.coop is needed.** The remaining lab conversation stays: this is testing of
  processes for later sensitive cases, not sensitive material.
- **The chief engineer's template checkout:** its uncommitted `.obsidian/` edits are discarded by the ACE, on his
  instruction. The checkout has no `origin` remote and sits at 5a7290f; a fresh clone is simpler than a pull.
- **Commit as the trigger** for reading written content into the knowledge graph: a candidate (C9), not scoped.
- **The w3id namespace registration PR** is deferred until after the release, so it can cite the release.

## D-117 | 2026-11-25 | WP21-G9: the glossary's new terms, and their open points

The change consultant's sweep and the draft (`work-packages/impact/WP21-glossary-draft.md`, from WP21-U3g) are
accepted with these calls by the ACE:
- **Edges told vs edge table: option A.** "Edges told" names a narrative's own table (columns `from | type | to |
  note`); "edge table" keeps its sense (the view: all edges of one type), with the clause "Not a narrative's Edges told
  table." No existing use changes.
- **The assistant's rules.** `contracts/assistant.md` keeps its name, "the assistant's rules", and the MCP resource
  `scat://assistant-rules` is unchanged. The glossary's **rule, norm** row says that the assistant's rules are norms
  for the assistant, which the server enforces only where it refuses an act (it cannot set `done`).
- **skill** covers a package of instructions an assistant loads in the chat or the IDE (one entry).
- **coded, uncoded** as drafted: coded is at least one node link. `MISSION.md:74` uses "coded" for a narrative that is
  done ("every node the account refers to is identified and linked ..."). The ACE proposes to the chief engineer that
  it read "fully coded" (a mission edit; morning list). Until then, the glossary row notes that "done" requires a fully
  coded narrative.
- **The terms page's word cap** (600, WP12) is raised to fit the eleven new terms; the test changes in that one line.
- **Uses brought in line:** "session key" in `deploy/README.md`; "saved agent" in the chat-path guide (WP21-U10).
The application (glossary rows, `docs/reference/terms.md` bullets, the cap) is one unit, WP21-U3h, so the glossary
and its test land together.

## D-118 | 2026-11-25 | MISSION.md:74 stays; done means adequately coded, as the coder judges

Asked whether `MISSION.md:74` should say a narrative is done "when it is fully coded". The chief engineer, quoted as
typed and recorded by the ACE:

> "no not "fully", "adequately" coded as judged by the coder. it can continue to be iterated (or even reverted to
> draft) if need be. i think you can leave it."

Outcome: the mission line is unchanged. The glossary's **coded, uncoded** row (WP21-U3h) says that `done` means the
narrative is adequately coded as the coder judges, not fully coded, and that a done narrative can still be iterated or
moved back to `draft`. It does not say "fully coded". D-117's proposal is withdrawn.

## D-119 | 2026-11-25 | WP21-R7 reworded; U10 finishes in one round

U10 (the life-cycle guide and the leave-no-trace walkthrough) passed every check and two cold readers, who found both
pages followable, which is what the chief engineer asked of teardown ("documented well enough that i could do it from
the docs or you could do it for me"). Three fresh reviews failed it on R7's wording "each step names one action",
each finding new compound steps. A requirement that three rounds read differently is the defect, so under D-099 the
ACE rewords R7, not the pages: **each step names where it is done and one outcome, and refers to no step on another
page by number or range.** The second half is a real defect the last review found (`leave-no-trace.md` steps 12 to 14
and 18 point to step ranges of the chat-path guide); U10 inlines them. In the same round: the launcher's
missing-runtime message stops naming only Docker Desktop (Colima is the default, D-105), and the `test_terms.py`
docstring's "600" follows the new cap. One fresh review against the reworded R7, then merge.

Also decided: SCAT-UNCODED keeps warning at every status, `stub` included (the PM's default). It is the to-do a coder
needs early, in the spirit of C3: a narrative stays out of the knowledge graph until it links a node.

## D-120 | 2026-11-25 | Iteration 36's record corrected, on the chief engineer's yes

The PM's iteration 36 record said 10 estimated points; its units add up to 9. The PM's correction was refused by the
permission guard, and the ACE did not make it in its place; it asked the chief engineer whether the record may be
corrected to 9 estimated points. He chose "Yes, correct it". A correcting record (`corrects` the original's `ts`) is
appended and the board's row reads 9 est, 13 realized, ratio 1.44. `check_metrics.py --accept WP21` passes.
Also: template `dev` is 271c3e9, pinning tools 7f0ed05 (check: no problems); the docs tests pin it (66 passed).

## D-121 | 2026-11-25 | WP21 accepted

A fresh acceptance reviewer checked R1, R2, R2b and R3 to R10 against tools `dev` 34d5213 and template `dev` 271c3e9
and found no checkable defect: R1, R2, R2b, R3, R9, R10 met; R4 to R8 met with notes. Its evidence: 2401 tests pass,
ruff clean, the strict docs build clean, the template's check "no problems", the old table header absent except one
deliberate seed line in the catalogue. The notes are the parts reserved for the chief engineer's sitting and the
release (R4 loading the skill; R5 the keychain's behaviour from the built app, a locked keychain, iCloud sync, and a
`ps` check during a dry run; R6 the first image push; R7 the leave-no-trace run) and one fact for the reviewer's guide:
R8's test-file diff is larger than the two assertions D-110 allowed because R1's column order rewrote that file's
tables. CI went red after WP21 merged (the iteration-36 metrics slip, then the ACE's own over-long pin line, unformatted)
and is green again at 834490f. `check_metrics.py --accept WP21` passes. The ACE accepts WP21. Candidates C1 to C8 are
done in v0.1; C9 stays a candidate.

## D-122 | 2026-11-25 | WP18 accepted

WP18-R4, the live run, ran on 25 November (`acceptance/chat-path/live-run-wp18-r4.md`). Its security finding F15/C7
(the session key visible in the process list) is fixed by WP21-U8 (D-115): the key lives in the login keychain, never
in a process's arguments, and is deleted at Stop. R2's "key rotated" now reads "key deleted" (D-115; one key per
session). R1, R3, R5 hold on `dev` 834490f with CI green; `check_metrics.py --accept WP18` passes. The ACE accepts WP18.
The chat-path user tests (WP20-UC1) remain for the chief engineer's sitting.

## D-123 | 2026-11-26 | Node-page help (C12): a spike first

During the leave-no-trace sitting the chief engineer asked whether tools, prompts and workflows exist to help fill in
node pages as a synthesis across narratives (C12, quoted in `work-packages/candidates.md`). The ACE answered: not yet
(the server stubs pages and records edges; `trace` follows edges; no skill, prompt or view helps write a node page, and
renaming or merging node pages is an accepted gap, W11, D-100). Asked where the work goes, he chose "A spike first": a
short research spike on synthesis across narratives and on synonym and homonym handling, then a decision. The spike
(RS4) is scoped by the ACE; C10 and C11's timing is asked separately.

## D-124 | 2026-11-26 | The launcher (C10) is fixed before the release

After the leave-no-trace run (`acceptance/chat-path/leave-no-trace-run.md`), asked whether the launcher fixes (C10,
with the silent reuse of a remembered vault, L1) come before or after the release PRs. The chief engineer chose "Yes,
before release". The ACE scopes WP22: SCAT Chat as a small, clear local Mac app that runs the MCP server, with the
walkthrough fixes the run found (L2 to L5, L8, L10).

## D-125 | 2026-11-26 | WP22 approved

WP22 (`work-packages/WP22.md`: SCAT Chat as a small clear local app that runs the MCP server, and the walkthrough fixes
L2 to L5, L8, L10) takes C10 (D-124). The PM's scope check found nine fixes, all applied: Applications is written only
in the chief engineer's sitting, tests and builds use a temporary folder (ORG, Limits); the blast radius names every
file; the skill's comment lines are the drift test's markers and change with it; each visual requirement has a
reviewer's dry run; candidates and glossary words set right; the spike's logged decision gates the launcher unit.
Impact map `work-packages/impact/WP22.md` (change consultant's work, via the PM). Revert point `divergence/D-125`.
The ACE approves WP22.

## D-126 | 2026-11-26 | Attribution of narratives (C13): in v0.1, pending two problem-level points

Asked whether C13 (attributing narratives to contributors, off in Chatham House mode, chosen by the organiser at
set-up) is in v0.1 or after, the chief engineer chose "In v0.1". The ACE found two problem-level points it raises
(raised by D-126), put to him before scoping: (1) `MISSION.md` Non-goals holds "Attributing statements to individuals in
the ontology. The data records groups; an event's participation terms are its own policy, which the docs name without
choosing one."; (2) the TBox's formal identifier for the affordance-to-technology edge is `scat:Attributes`, the
source of the diagram's stale label, so freeing "attributed to" means renaming that identifier.

## D-127 | 2026-11-26 | Three disjoint attribution modes; scat:Attributes renamed

The two points raised by D-126, asked as two questions. The chief engineer's answers, quoted as typed and recorded by
the ACE:

> On the mission's non-goal: "change it to assert that we can have an non-attribution mode and an attribution mode and
> they are disjoint. cannot let them bleed together in use. system needs to know which mode its. Attribution Req,
> Attribution optional, Attribution disallowed. Chatham house is attribution disallowed. the disallowed mode is what i
> plan to use in my pilot but i want the other 2 modes in the software."

> On the TBox name `scat:Attributes`: "Rename it".

Outcomes:
- **Mission edited on `dev`** (on his instruction): the non-goal "Attributing statements to individuals in the
  ontology" is replaced by a non-goal against mixing modes, stating the three disjoint attribution modes (required,
  optional, disallowed; Chatham House is disallowed), set by the organiser at set-up and known to the tools; edges and
  nodes always record groups. The pilot uses the disallowed mode.
- **`scat:Attributes` is renamed** (to a name for "is provided by"), freeing "attribution" for C13.
The ACE scopes both in one package, WP23.
