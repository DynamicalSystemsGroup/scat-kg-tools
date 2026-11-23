# Mission — Scope of work: scat-kg v0.1

| | |
|---|---|
| **Status** | Approved by the chief engineer's merge of PR #1. Each amendment is approved by the merge of its own PR; Amendment 1 is PR #2. |
| **Chief engineer (accountable)** | `mzargham` — final design authority; approves this mission and its amendments; accepts the v0.1 delivery |
| **Assistant to the chief engineer (ACE)** | The main Claude session — manages the team, writes and approves work-package scopes inside this mission, accepts work packages, escalates only intent gaps |
| **Repositories** | `scat-kg-tools` (conformance tools, TBox, docs site; this document lives here) and `scat-kg-template` (the vault to clone) |
| **Approval record** | The chief engineer's merge of this document's PR into `main` of `DynamicalSystemsGroup/scat-kg-tools` (public) |
| **Acceptance record** | The chief engineer's merge of the release PR from `dev` into `main` in each repository. The ACE opens these PRs, and no one else does, once the candidate is ready. The chief engineer's walkthrough (UA-M) runs against them, and merging them is the acceptance. The release then tags `v0.1.0` and deploys the site (see Governance). |

## Purpose

DSG needs, for an upcoming project, a first usable release of a toolkit for turning facilitated discussions into a
conformant knowledge graph. Actors (users, sponsors, other stakeholders) tell stories, which become scenarios.
Technologists (researchers, developers, operators) pitch architectures. Their raw notes are coded into pages of an
Obsidian vault in git. Coding decompiles each scenario and architecture into four concepts — **s**takeholders,
**c**oncerns, **a**ffordances and **t**echnologies (SCAT, named for scat singing in jazz) — and relates them through
explicit relationships, layered as bipartite graphs: stakeholders–concerns, concerns–affordances,
affordances–technologies. The result is a navigable, interpretable dataset. It is scaled to a human note-taker:
just enough structure to make the data interpretable, but mostly a formal structure for arranging Obsidian notes.
That dataset is the data product, and its conformance to a fixed ontology is what makes it analysable. The git repository is the data of record; the graph is derived from it.

The point of departure is the toolchain and the Obsidian reading/review experience described in *Formalizing
Document Assurance* (INCOSE IS 2026) and the earlier repos `assurances-audits-accountability`, `knowledgecomplex`,
`ant-rdf` and `concept-definition-stage`. The last of these is also a reference for the ontology: its SKOS+PROV
spine, its authority-traced definitions, and its practice of anchoring to an external ontology through equivalence
axioms instead of importing all of it. The structure here is simpler than any of them: no faces, no assurance triangles.

## Core heuristics

- **For the users: "make the right way the easy way".**
- **For the builders: "as simple as possible but no simpler".**

When a choice isn't settled elsewhere, these decide it.

## Scenarios and architectures

The two record types look at the same graph from opposite sides. This distinction is a core heuristic for
facilitating, capturing and coding.

- **Scenarios are behavioural.** They tell the story of people within an action situation doing things, through which
  outcomes and consequences are wrought. They are temporal. Technologies are part of the action situation but are not
  the focus: they stay relatively fixed and out of view, and what is legible is their **affordances**. A coded
  scenario links stakeholder groups, concerns and affordances.
- **Architectures are structural.** They formulate assemblages: parts and wholes, and how parts are assembled into
  tools that provide affordances which address concerns. Stakeholders are largely abstracted away. What is addressed
  is the concerns, and the same concern can arise from different stakeholders; an architecture can't presume which
  stakeholders will adopt it. A coded architecture links concerns, affordances and technologies.

The split between actors (who tell scenarios) and technologists (who pitch architectures) is a facilitation device,
not a division of people. Many people are both.

## Facilitation stance: improvisational jazz

SCAT takes its name, and its manner, from scat singing in improvised jazz. Facilitation works by "yes, and" and "from
this perspective". Each contribution is taken up and built on, and each is located in the perspective it comes from.

The model **holds disagreement rather than collapsing it.** As in `ant-rdf`, it exposes frictions, gaps and dissenting
views, and it can represent margins of potential conflict: for example, groups that share a concern while their
other concerns are directly opposed. So nobody has to argue anyone into agreement. We capture people's stories and
people's proposed architectures. We do not debate which architecture is correct, or which stories should be the
focal point of a design.

## Users and how they work

The v0.1 user is a facilitator-analyst: technically savvy, but not a software developer. They:
- navigate GitHub's web interface, including creating a repository from a template;
- read, write and follow links in an Obsidian vault;
- work in an **interactive session** in the Python REPL (`import scat_kg`), with the `scat` CLI as an equal path to
  the same operations and messages. The docs lead with the REPL, because CLI commands get long when run through uv.
- follow documentation literally, step by step. Testers on a small model stand in for this user, so the right way
  has to be the easy way.

The people in the data are stakeholder **groups**, under the Chatham House rule, so no individual is identifiable.

## Goals

- **G1. Fixed TBox**, designed under G10 and then fixed for v0.1. Turtle files define:
  - the seven SCAT classes: Stakeholder group, Concern, Affordance, Technology, and the relations Heldby (stakeholder
    group × concern), Addresses (concern × affordance) and Attributes (affordance × technology). Names may follow an
    adopted ontology;
  - any easy-win relations G10 adds;
  - each record's required and optional fields;
  - the other page types: class pages, raw and coded scenarios, raw and coded architectures;
  - the linking rules: a coded scenario links stakeholder groups, concerns and affordances; a coded architecture
    links concerns, affordances and technologies; raw records link to or embed their coded pages;
  - how the graph holds disagreement and margins of potential conflict, in the form WP1 decides (at minimum, the same
    concern held by different stakeholder groups, plus any conflict relation WP1 adopts).
- **G2. Vault ↔ graph.** Markdown pages with YAML frontmatter parse into an ABox that is checked against the TBox.
  Every class has a class page: a description plus an index table (name, short description, link) of its instances.
- **G3. Page lifecycle.** Every instance page and every scenario or architecture page carries a status:
  `stub → draft → done`. (Class pages are generated, so they carry none.) `scat` creates a page that the ontology
  entails but that doesn't exist yet as a `stub`, so the graph is never incomplete, only unfinished.
- **G4. Operations**, in the Python API and the `scat` CLI, usable by a technically savvy non-developer in an
  interactive session:
  - `check <page>`, `check <page> --neighborhood`, `check --all` — conformance, with actionable messages;
  - `status` at the same three scopes, and a command to set a page's status;
  - `index` — regenerates class index tables from the instance pages;
  - a command that creates entailed missing pages as stubs.
  Local and neighborhood checks act as a fast linter during working sessions. Every operation takes a page by the
  name Obsidian shows (its filename, with or without `.md`) or by its path.
- **G5. Two repositories.** `scat-kg-tools`: a slim, separately maintained package holding the TBox, the parser, the
  checks, the CLI and the documentation site. `scat-kg-template`: the vault to clone, which installs the tools
  pinned to a commit. Both builds are reproducible with uv.
- **G6. Worked example: this project as its own case study.** The template's example content is the elicitation of
  scat-kg itself: its stakeholder groups, concerns (for example, anonymity versus attribution), affordances and
  technologies, drawn from the chief engineer's recorded statements and the decision log. Its stakeholder groups
  follow the Chatham House rule like any other: no group stands for one identifiable person. It avoids politically loaded illustrations. It is minimal
  (users overwrite it), but has 2–3 records in every registry, plus two scenarios and two architectures, each raw and coded.
  It doubles as the test fixture and the documentation example.
- **G7. Documentation on GitHub Pages** (from `scat-kg-tools`), styled after jazz (R-15), with the pages the journey table names (see User
  acceptance): getting started, a planning guide, a scenario facilitation guide, an architecture facilitation guide,
  and a coding guide, plus a reference for the Python API and the CLI.
- **G8. Toolchain decided by evidence.** Oxigraph, Open Knowledge Format (OKF), pydantic and the choice of rule
  language are tried on a small vault before the implementation is locked in. Each choice is recorded with its evidence.
- **G9. Clear user journey.** A technically savvy user who is not a developer can go from the docs site to a new
  repository made from the template, through an interactive working session, to a clean, navigable graph, using only the
  documentation. The documentation is clear and navigable at every step.
- **G10. Ontology by evidence: import, don't mint.** A research sprint surveys existing ontologies for each SCAT
  class and relation (for example ISO/IEC/IEEE 42010 for stakeholders and concerns, the SEBoK and INCOSE canon that
  `concept-definition-stage` commits, SKOS and PROV). A trade study then decides, class by class, whether to adopt
  (thinned to what we use, anchored by equivalence axioms rather than importing everything) or to author our own,
  authoring only where nothing beats custom. The result is one coherent ontology, not a patchwork of imports. Every
  term traces to the ontology it was adopted from, or is recorded as authored, with the reason. Easy wins in
  expressiveness are taken where they don't complicate the software or the UX. The first candidate is a conflict
  between concerns, such as anonymity versus attribution (the chief engineer called it a disjointness axiom). More
  generally, WP1 assesses the lightest way for the graph to hold disagreement and margins of potential conflict
  (see Facilitation stance). WP1 decides the form, and WP4's rule catalogue says how it is checked.

- **G11. Facilitation strategy grounded in research.** The planning and facilitation guides are written from a
  facilitation strategy that WP3 derives from prior work: the improvisational stance, eliciting scenarios and
  architectures, and holding disagreement without adjudicating it.
## Non-goals

- Gen-AI aided authoring; an Obsidian plugin (the CLI is designed so one can wrap it later).
- Triangles or any faces, including ones inferred from scenarios and architectures.
- Changing the TBox once WP4 has fixed it, or letting instance repos extend it.
- Enforcing raw → coded links or embeds beyond a warning.
- Checking that named entities are linked beyond a basic regex warning.
- The verification / validation / human-signature assurance framework of the paper.
- Attributing statements to individuals. v0.1 is built for Chatham House settings, and attribution is a possible
  extension. How raw notes are taken is the facilitator's call; the guides explain the rule.
- Adjudicating between stories or architectures: neither the tools nor the facilitation guides judge which
  architecture is correct or which stories should be focal.
- Analysis tooling over the graph.
- Publishing to PyPI.
- UX for non-technical users beyond the CLI and Obsidian.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | TBox in Turtle, in `scat-kg-tools` | G1, G10 |
| D-2 | Parser, checks, status, index and stub commands, CLI, test suite with seeded-defect fixtures, in `scat-kg-tools` | G2, G3, G4 |
| D-3 | Template repository: vault skeleton (class pages, folders for raw and coded records), Obsidian page templates for the four record types, instance configuration (stakeholder-group cardinality cap), pinned tools, the case study (G6) | G5, G6, G9 |
| D-4 | Documentation site on GitHub Pages: a candidate preview during user acceptance, then the release | G7, G9, G11 |
| D-5 | Research readouts and decision records: the ontology survey and trade study, the toolchain spike, and the facilitation research, with evidence and measurements | G8, G10, G11 |
| D-6 | Reviewer's guide for the chief engineer, in the release PR. It is sized for a person and split into sittings by output: (1) the end-to-end walkthrough (UA-M below); (2) the docs site; (3) the tools and checks; (4) the ACE's calls. Each sitting has a short checklist and its own entry point. It lists every call the ACE made, with its evidence, and what is known to be weak. | all |
| D-7 | User-acceptance kit, in `scat-kg-tools/acceptance/`: the AI tester personas and briefs, the report template, every AI test report with its dispositions, and the chief engineer's walkthrough script | G9 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Errors block; warnings do not. Errors: required fields and types, relation endpoints of the right classes, coded scenarios and architectures missing a required link type (a scenario with no stakeholder group, concern or affordance; an architecture with no concern, affordance or technology), stakeholder groups within the cap, valid status. Warnings: unlinked mention of a graph entity; raw record not linking or embedding its coded pages; a scenario linking a technology (link its affordance instead) or an architecture linking a stakeholder group (link the concern instead) *(default)*. | Seeded-defect tests, one or more per rule |
| R-2 | Every message names the file, the field or link, and the rule broken (by id). It gives the fix as something a literal reader can apply: the exact command to run, or the exact field and value to write. | Golden-output tests on seeded defects |
| R-3 | How strict a check is follows the page status, but only for missing fields: a stub needs only identity, type and status, and missing required fields warn on draft and are errors on done *(default)*. Links and relation endpoints are checked at every status. | Tests per status |
| R-4 | `index` is the only command that rewrites class pages; the stub command is the only one that creates pages; checks never write. | Tests that snapshot the vault before and after each command |
| R-5 | Speed on a laptop with a 500-page vault: local check < 1 s, neighborhood < 2 s, full < 5 s *(default thresholds)*. | Benchmark script over a synthetic 500-page vault that it generates |
| R-6 | From a machine with only the documented prerequisites: fresh clone of the template → one documented setup command → `check --all` passes on the worked example. | Clean-clone trial |
| R-7 | Both repositories commit `uv.lock`; CI runs tests and checks on every push. | CI runs |
| R-8 | The interactive session has two equal paths: the Python REPL (`import scat_kg`) and the `scat` CLI in a terminal. Every operation is available on both, with the same messages. The docs lead with the REPL and show the CLI equivalent in a tab. The CLI is a thin layer over the Python API. | Tests calling both paths; docs test runs both |
| R-9 | Every REPL snippet and command shown in the docs runs as shown, and the CLI reference matches `--help`. | Docs test that extracts and runs the snippets and commands; reference diff |
| R-10 | The docs site has no dead ends or broken links. Every journey page says what you need before you start and where to go next. | Strict build plus link check; the ACE's browser pass over every page, at desktop and phone width |
| R-11 | **Make the right way the easy way: one way to create each kind of page.** Raw and coded scenarios and architectures, which people write in Obsidian, come from Obsidian page templates. Every SCAT and relation page comes from `scat`: link it from a coded record, then run the stub command, which creates it with the right type. Class pages come from `index`. Users never write that structure by hand. Each journey stage's docs page leads with the one action to take next. | A test that each of the four record types has a template; tests of the stub command; the Haiku testers' reports |
| R-12 | New repositories are private by default. The docs and the template's README recommend private repositories. Their "create your project" link opens GitHub's new-repository page from the template with private visibility pre-selected; if GitHub can't pre-select it, the docs give the `gh repo create --template … --private` command as the first path. | Probe of the link on the candidate; UA-M |
| R-13 | The schema has one source. The TBox is authoritative; any other form the checks use (for example pydantic models) is either generated from it or held equal to it by a test. WP2 picks the mechanism. | The generator, or the equality test, in CI |
| R-14 | The planning and facilitation guides carry the improvisational stance ("yes, and"; "from this perspective") and contain no step that ranks, votes on or adjudicates between stories or architectures. | The ACE's review of the guides; UA-M |
| R-15 | **Jazz is the stylistic reference.** The package and its docs take their style from jazz music, in language and through visual metaphor, as a light touch that never costs clarity: names, headings, examples and images may draw on improvisation, ensembles, charts, riffs and call and response. | Cold-read test: a fresh reader of the docs site, asked open-endedly what style or reference it evokes, names jazz or improvised music unprompted; the same reader reports no place where the metaphor obscured an instruction |

## User acceptance

Acceptance is judged by people using the product, not only by tests. The journey under test is:

| Stage | The user | Docs page |
|---|---|---|
| J1 Find | lands on the docs site and understands what this is for and how to start | home |
| J2 Create | on GitHub's web interface, makes a new **private** repository from `scat-kg-template`, then clones it | getting started |
| J3 Set up | installs the prerequisites from exact commands (uv, and a one-time GitHub sign-in so a private repository can be cloned), runs one setup command, gets a working `scat_kg`, and opens the folder as an Obsidian vault | getting started |
| J4 Plan | plans a facilitation event: which sessions elicit scenarios and which elicit architectures, and who takes part in each, the Chatham House framing, stakeholder groups within the cap | planning guide |
| J5 Capture | during the event, records raw scenarios and raw architectures | the two facilitation guides |
| J6 Code | afterwards, in an interactive session (the Python REPL, or the `scat` CLI), decompiles the raw notes into SCAT pages and relations: creates stubs, moves pages to draft and done, regenerates the indexes, and fixes each error from its message using local and neighborhood checks | coding guide, API and CLI reference |
| J7 Finish | reaches a clean `check --all`, commits and pushes, and navigates the resulting graph in Obsidian | coding guide |

**UA-A, the AI user tests** (run by the team on the candidate, before the chief engineer's walkthrough):

- At least three personas, each written in the user's own words, never the tool's vocabulary. **Most of them run on
  Haiku**, so the test doesn't depend on a lot of reasoning: if the right way needs reasoning to find, it isn't yet
  the easy way.
  - a facilitator-analyst who is comfortable with a terminal, GitHub and Obsidian but is not a developer (Haiku);
  - a newcomer to Obsidian and the command line who is careful and follows instructions literally (Haiku);
  - the same facilitator-analyst on Sonnet, as a control: a step that Sonnet passes and Haiku fails points to the
    docs or the tool, not the user.

  Between them, at least one Haiku tester works in the Python REPL and at least one uses the CLI.
- Each tester starts on a machine without uv, from the Pages preview URL, and follows only what the docs site says. J2 is simulated with
  `git clone --no-hardlinks` of the template with its remote removed; all other stages run as written. Each tester
  codes a small elicitation in a domain of its own, different from the worked example: at least one scenario and one
  architecture, each raw and coded.
- Testers may not read `src/` or `tests/`. Every claim comes with pasted command output. Each tester reports, per
  stage: where it got stuck, what it had to guess, and where the docs left it with nowhere to go.
- **Pass bar:** every tester, the Haiku testers included, reaches J7 with a clean `check --all`. Every guess (any
  action the docs did not literally state) counts as a finding. A finding is **blocking** if it stopped the tester
  short of J7 or if it is a docs command that doesn't work as shown. Every finding is dispositioned: either fixed and re-tested by a fresh tester, or accepted with a
  reason and listed in the reviewer's guide. The final round leaves no blocking finding unresolved.
- Each tester's report also answers, before anything else, what style or reference the docs evoke (R-15's cold read).
- A report that reuses names from the worked example's records, or that finds nothing, is void and is run again.

**UA-M, the chief engineer's walkthrough** (the first sitting of the reviewer's guide, and the core of acceptance):

- He runs J1 to J7 himself on the candidate: starting from the Pages preview, using the docs' "create your project" link
  (GitHub's template flow, private by default) to make a real repository, cloning it, setting up, and working through an interactive session with the CLI and
  the Python REPL, coding a small elicitation of his own choosing.
- The walkthrough script gives each stage's entry point and what "done" looks like, so the session can be split up
  and resumed.
- **Pass:** he completes the journey from the documentation without help, and judges the documentation clear and
  navigable and the journey clear. Anything he flags is fixed on `dev` and the walkthrough is resumed from the
  affected stage. He accepts by merging the release PRs.

## Definition of good

- Make the right way the easy way: following the docs literally and using the provided templates and commands is
  the shortest path, and it produces a conformant vault.
- The ontology is lean and recognisable: adopted where an existing ontology wins, authored where it doesn't, never a
  patchwork.
- A first-time user fixes every conformance error from the message alone, without reading the source.
- The tools are small enough that one person can maintain them.
- The worked example reads well in Obsidian, as judged by the chief engineer in UA-M.

## Definition of good enough

- R-1 to R-15 met, with evidence.
- The AI user tests (UA-A) pass on the candidate.
- The candidate is staged for the chief engineer's own walkthrough (UA-M), with the reviewer's guide ready.
- The ontology trade study, the toolchain decision records and the facilitation readout exist. Every TBox term traces to an adopted ontology
  or is recorded as authored, with the trade study's reason.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the chief engineer has accepted by the acceptance
record above.

## Governance

- The ACE approves each work-package scope inside this mission, accepts each work package against its scope, and
  logs every ruling in `decisions/log.md`.
- The chief engineer signs off on exactly two things: this mission scope (and amendments to it) and the acceptance of
  the mission's delivery. Every other sign-off belongs to the ACE.
- The ACE escalates only an **intent gap**: a question whose answer this mission and the chief engineer's recorded
  statements don't settle, and that changes what is built or whether it serves its purpose. Escalations come one at a time,
  with a recommendation, and other work continues meanwhile.
- The ACE runs a spike wherever the evidence for a call is missing. Every call the ACE makes is recorded with its
  evidence for the chief engineer's review at acceptance; reversing any of them is his prerogative.
- Until the release PR, nothing is merged to `main`, tagged or published. The exceptions are this mission's own
  approval and amendments, and the **candidate stage** the chief engineer's walkthrough needs:
  - the docs site deploys from `dev` to Pages, with a banner marking it pre-release;
  - `scat-kg-template` is marked as a GitHub template, with `dev` as its default branch until the release;
  - the template pins the tools to the exact candidate commit.
  At the release, `v0.1.0` tags that same commit, the site redeploys from `main`, and the template's default branch
  returns to `main`.
- Amendments to this mission are approved by the same act as the mission.
- How the team runs is in `ORG.md`.

## Timeline

No date is set. A date is deferred until velocity has been established. The estimates are lightweight and agile in
style: a heuristic for driving convergence and forecasting, not a schedule fixed in advance, and they are expected
to be noisy at first.
- The PM owns the timeline. Every unit gets story points when it is planned *(default scale 1, 2, 3, 5, 8; anything
  bigger is split)*. An **iteration** is one batch of units that the PM dispatches and lands *(default)*. The board
  records each iteration's points done and its elapsed wall-clock time, so velocity converts to a date. The forecast
  to the candidate is updated from the measured velocity.
- The forecast runs to **a candidate ready for the chief engineer's review**. It includes testing, the UA-A rounds,
  and the revisions they cause. Time to address his review feedback is estimated later, when that feedback exists.

## Initial breakdown (a plan, not a contract; the ACE revises it at each work-package acceptance)

Ontology design comes before implementation, and the design is driven by research.

1. **WP1 Ontology research sprint.** Survey existing ontologies for each SCAT class and relation, and the patterns
   in `concept-definition-stage`. Run the trade study (adopt and thin, or author) and assess the easy-win axioms,
   including how disagreement is held. Readout and decision records. Fixes: what the TBox imports, anchors to, or
   authors; D-5 (ontology part).
2. **WP2 Toolchain spike.** In parallel with WP1. OKF, oxigraph, pydantic and the rule language, tried on a throwaway
   mini-vault and measured. Fixes: the toolchain; D-5 (toolchain part).
3. **WP3 Facilitation research spike.** In parallel with WP1. A pass back through `ant-rdf` (its handling of
   controversy, dissent and multiple perspectives), the post "KOI & The Unicorn"
   (<https://blog.block.science/koi-and-the-unicorn/>), "Building the Loop" (EPIC 2025), and recent unpublished grant-proposal
   drafts from the same collaboration (read for principles only). Fixes: the facilitation strategy (the "yes, and" and "from this
   perspective" stance, eliciting scenarios and architectures, and holding disagreement) that the planning and
   facilitation guides are written from; inputs to WP4 on representing disagreement; D-5 (facilitation part).
4. **WP4 Ontology and page contracts.** From WP1 to WP3: the TBox in Turtle, fields per class, page types, link rules,
   status rules, the rule catalogue with ids and message wording. Fixes: D-1 and the vault conventions.
5. **WP5 Conformance tools.** Built on the toolchain WP2 fixed: parser, checks, the Python API and the CLI over it,
   seeded-defect tests, benchmark. Fixes: D-2.
6. **WP6 Template and case study.** In parallel with WP5 once WP4 is accepted. Fixes: D-3.
7. **WP7 Docs and Pages.** Written journey-first (J1–J7), with the facilitation guides built on WP3. Fixes: D-4.
8. **WP8 Candidate and user acceptance.** Integration, the candidate stage, UA-A rounds to the pass bar, the
   reviewer's guide and the walkthrough script. Fixes: D-6, D-7.

## Agent's defaults

- Names: `scat-kg-tools`, `scat-kg-template`, CLI command `scat`.
- Python ≥ 3.12. The template installs the tools through uv as a git dependency pinned to a commit; no PyPI.
- Facilitation and coding guides are written once, on the Pages site; the template links to them rather than copying them.
- Status strictness (R-3) and speed thresholds (R-5) as stated above.
- Documentation built with MkDocs Material (as in `assurances-audits-accountability` and `knowledgecomplex`).
- CI on GitHub Actions, ubuntu-latest; development on macOS. `.python-version` (3.12) and `uv.lock` are committed; CI runs
  `uv sync --locked`, `uv lock --check`, ruff check and format, and pytest.
- Branches: `main` holds approved missions and releases only; `dev` is the integration branch; work happens on
  short-lived unit branches off `dev`.
- Licence: Apache-2.0, copyright Dynamical Systems Group, for code, docs and ontology (the chief engineer's decision, log D-005).
- Adopted ontologies, standards and their definitions are used directly and cited, per engineering practice.
- The stakeholder-group cap is set in the template's configuration file, with the worked example set to 3.
- Private sources (such as unpublished grant drafts) are read for principles only. Since the repositories are
  public, the readouts summarise them in our own words and cite only published work.
- No AI attribution on commits, PRs or documents; CI fails on attribution lines, as in tradespace.

## Open decisions (for the chief engineer)

None. Every item was resolved through the decision loop and is recorded in `decisions/log.md`:
- 13 decided by the chief engineer: log D-001, D-003, D-005 to D-008, D-010 to D-014, D-017 and D-018;
- 1 assigned to the ACE: log D-002;
- 1 deferred by him: the target date, until velocity is known (log D-011).

Log D-004, D-009 and D-012 also record the ACE's consistency passes. Log D-015 and D-016 were rolled back with `dev`.
