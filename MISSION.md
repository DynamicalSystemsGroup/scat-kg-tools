# Mission — Scope of work: scpt-kg v0.1

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing is executed before then. |
| **Chief engineer (accountable)** | `mzargham` — final design authority; approves this mission and its amendments; accepts the v0.1 delivery |
| **Assistant to the chief engineer (ACE)** | The main Claude session — manages the team, writes and approves work-package scopes inside this mission, accepts work packages, escalates only intent gaps |
| **Repositories** | `scpt-kg-tools` (conformance tools, TBox, docs site; this document lives here) and `scpt-kg-template` (the vault to clone) |
| **Approval record** | The chief engineer's merge of this document's PR into `main` of `DynamicalSystemsGroup/scpt-kg-tools` (public) |
| **Acceptance record** | The chief engineer's merge of the release PR from `dev` into `main` in each repository. The ACE opens these PRs when the candidate is ready, and no one else does. The release then tags `v0.1.0` and deploys the site (see Governance). |

## Purpose

DSG needs, for an upcoming project, a first usable release of a toolkit for turning facilitated discussions into a
conformant knowledge graph. Actors (users, sponsors, other stakeholders) tell stories, which become scenarios.
Technologists (researchers, developers, operators) pitch architectures. Their raw notes are coded into pages of an
Obsidian vault in git. Coding decompiles each scenario and architecture into four concepts — **s**takeholders,
**c**oncerns, **p**roperties and **t**echnologies (SCPT) — and relates them through explicit relationships, layered
as bipartite graphs: stakeholders–concerns, concerns–properties, properties–technologies. The result is a navigable,
interpretable dataset. That dataset is the data product, and its conformance to a fixed ontology is what makes it
analysable. The git repository is the data of record; the graph is derived from it.

The point of departure is the toolchain and the Obsidian reading/review experience described in *Formalizing
Document Assurance* (INCOSE IS 2026) and the earlier repos `assurances-audits-accountability`, `knowledgecomplex`,
`ant-rdf` and `concept-definition-stage`. The last of these is also a reference for the ontology: its SKOS+PROV
spine, its authority-traced definitions, and its practice of anchoring to an external ontology through equivalence
axioms instead of importing all of it. The structure here is simpler than any of them: no faces, no assurance triangles.

## Users and how they work

The v0.1 user is a facilitator-analyst: technically savvy, but not a software developer. They:
- navigate GitHub's web interface, including creating a repository from a template;
- read, write and follow links in an Obsidian vault;
- work in an **interactive session**, with the `scpt` CLI in a terminal and a Python REPL (`import scpt_kg`) open
  alongside it. Both are equal paths to the same operations and the same messages. The CLI suits one-off commands; the
  REPL suits looping over pages while coding.
- follow documentation literally, step by step. Testers on a small model stand in for this user, so the right way
  has to be the easy way.

One person may be both an actor and a technologist; these are roles in elicitation, not classes in the data model. The
people in the data are stakeholder **groups**, under the Chatham House rule, so no individual is identifiable.

## Goals

- **G1. Fixed TBox.** Designed under G10, then fixed for v0.1. Turtle files define seven ontology classes — Stakeholder
  group, Concern, Property, Technology, Heldby (stakeholder group × concern), Addresses (concern × property),
  Attributes (property × technology), with names that may follow an adopted ontology — plus any easy-win relations
  G10 adds, together with each
  record's required and optional fields, the other page types (class pages; raw and coded scenarios; raw and coded
  architectures), and the linking rules: coded scenarios and architectures link into the graph, and raw ones link to
  or embed their coded pages.
- **G2. Vault ↔ graph.** Markdown pages with YAML frontmatter parse into an ABox that is checked against the TBox.
  Every class has a class page: a description plus an index table (name, short description, link) of its instances.
- **G3. Page lifecycle.** Every instance page and every scenario or architecture page carries a status:
  `stub → draft → done`. (Class pages are generated, so they carry none.) `scpt` creates a page that the ontology
  entails but that doesn't exist yet as a `stub`, so the graph is never incomplete, only unfinished.
- **G4. CLI** usable by a technically savvy non-developer in an interactive session:
  - `check <page>`, `check <page> --neighborhood`, `check --all` — conformance, with actionable messages;
  - `status` at the same three scopes, and a command to set a page's status;
  - `index` — regenerates class index tables from the instance pages;
  - a command that creates entailed missing pages as stubs.
  Local and neighborhood checks act as a fast linter during working sessions.
- **G5. Two repositories.** `scpt-kg-tools`: a slim, separately maintained package holding the TBox, the parser, the
  checks, the CLI and the documentation site. `scpt-kg-template`: the vault to clone, which installs a pinned
  version of the tools. Both builds are reproducible with uv.
- **G6. Worked example: this project as its own case study.** The template's example content is the elicitation of
  scpt-kg itself: its stakeholder groups, concerns (for example, anonymity versus attribution), properties and
  technologies, drawn from the chief engineer's recorded statements and the decision log. Its stakeholder groups
  follow the Chatham House rule like any other: no group stands for one identifiable person. It is minimal (users
  overwrite it), but has 2–3 records in every registry, plus two scenarios and two architectures, each raw and coded.
  It doubles as the test fixture and the documentation example.
- **G7. Documentation on GitHub Pages** (from `scpt-kg-tools`), organised by the user journey J1–J7 (see User
  acceptance): getting started, a planning guide, two facilitation guides (scenarios with actors, architectures with
  technologists), a coding guide, and a reference for both the CLI and the Python API.
- **G8. Toolchain decided by evidence.** Oxigraph, Open Knowledge Format (OKF), pydantic and the choice of rule
  language are tried on a small vault before the implementation is locked in. Each choice is recorded with its evidence.
- **G9. Clear user journey.** A technically savvy user who is not a developer can go from the docs site to a new
  repository made from the template, through an interactive working session, to a clean, navigable graph, using only the
  documentation. The documentation is clear and navigable at every step.
- **G10. Ontology by evidence: import, don't mint.** A research sprint surveys existing ontologies for each SCPT
  class and relation (for example ISO/IEC/IEEE 42010 for stakeholders and concerns, the SEBoK and INCOSE canon that
  `concept-definition-stage` commits, SKOS and PROV). A trade study then decides, class by class, whether to adopt
  (thinned to what we use, anchored by equivalence axioms rather than importing everything) or to author our own,
  authoring only where nothing beats custom. The result is one coherent ontology, not a patchwork of imports. Every
  term traces to the ontology it was adopted from, or is recorded as authored, with the reason. Easy wins in
  expressiveness are taken where they don't complicate the software or the UX. An example is a conflict relation
  between concerns, such as anonymity versus attribution.

## Non-goals

- Gen-AI aided authoring; an Obsidian plugin (the CLI is designed so one can wrap it later).
- Triangles or any faces, including ones inferred from scenarios and architectures.
- Changing the TBox once WP3 has fixed it, or letting instance repos extend it.
- Enforcing raw → coded links or embeds beyond a warning.
- Checking that named entities are linked beyond a basic regex warning.
- The verification / validation / human-signature assurance framework of the paper.
- Attributing statements to individuals. v0.1 is built for Chatham House settings, and attribution is a possible
  extension. How raw notes are taken is the facilitator's call; the guides explain the rule.
- Analysis tooling over the graph.
- Publishing to PyPI.
- UX for non-technical users beyond the CLI and Obsidian.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | TBox in Turtle, in `scpt-kg-tools` | G1, G10 |
| D-2 | Parser, checks, status, index and stub commands, CLI, test suite with seeded-defect fixtures, in `scpt-kg-tools` | G2, G3, G4 |
| D-3 | Template repository: vault skeleton (class pages, folders for raw and coded records), an Obsidian page template for every page type, instance configuration (stakeholder-group cardinality cap), pinned tools, the case study (G6) | G5, G6, G9 |
| D-4 | Documentation site on GitHub Pages: a candidate preview during user acceptance, then the release | G7, G9 |
| D-5 | Research readouts and decision records: the ontology survey and trade study, and the toolchain spike, with evidence and measurements | G8, G10 |
| D-6 | Reviewer's guide for the chief engineer, in the release PR. It is sized for a person and split into sittings by output: (1) the end-to-end walkthrough (UA-M below); (2) the docs site; (3) the tools and checks; (4) the ACE's calls. Each sitting has a short checklist and its own entry point. It lists every call the ACE made, with its evidence, and what is known to be weak. | all |
| D-7 | User-acceptance kit, in `scpt-kg-tools/acceptance/`: the AI tester personas and briefs, the report template, every AI test report with its dispositions, and the chief engineer's walkthrough script | G9 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Errors block; warnings do not. Errors: required fields and types, relation endpoints of the right classes, coded scenarios and architectures linking into the graph correctly, stakeholder groups within the cap, valid status. Warnings: unlinked mention of a graph entity; raw record not linking or embedding its coded pages. | Seeded-defect tests, one or more per rule |
| R-2 | Every message names the file, the field or link, and the rule broken (by id). It gives the fix as something a literal reader can apply: the exact command to run, or the exact field and value to write. | Golden-output tests on seeded defects |
| R-3 | How strict a check is follows the page status: a stub needs only identity, type and status; draft and done are checked in full *(default: missing required fields warn on draft, error on done)*. | Tests per status |
| R-4 | `index` is the only command that rewrites class pages; the stub command is the only one that creates pages; checks never write. | Tests; inspection |
| R-5 | Speed on a laptop with a 500-page vault: local check < 1 s, neighborhood < 2 s, full < 5 s *(default thresholds)*. | Benchmark script |
| R-6 | Fresh clone of the template → one documented setup command → `check --all` passes on the worked example. | Clean-clone trial |
| R-7 | Both repositories commit `uv.lock`; CI runs tests and checks on every push. | CI runs |
| R-8 | The interactive session has two equal paths: the `scpt` CLI in a terminal, and the Python REPL (`import scpt_kg`). Every operation is available on both, with the same messages, and the docs show both side by side. The CLI is a thin layer over the Python API. | Tests calling both paths; docs test runs both |
| R-9 | Every command shown in the docs runs as shown, and the CLI reference matches `--help`. | Docs test that extracts and runs the commands; reference diff |
| R-10 | The docs site has no dead ends or broken links. Every journey page says what you need before you start and where to go next. | Strict build plus link check; the ACE's browser pass over every page, at desktop and phone width |
| R-11 | **Make the right way the easy way.** The template ships an Obsidian page template for every page type. `scpt` creates entailed pages and regenerates indexes, so users never write that structure by hand. Each journey stage's docs page leads with the one command or action to take next. | Inspection; the Haiku testers' reports |
| R-12 | New repositories are private by default. The docs and the template's README recommend private repositories. Their "create your project" link opens GitHub's new-repository page from the template with private visibility pre-selected; if GitHub can't pre-select it, the docs give the `gh repo create --template … --private` command as the first path. | Probe of the link on the candidate; UA-M |

## User acceptance

Acceptance is judged by people using the product, not only by tests. The journey under test is:

| Stage | The user | Docs page |
|---|---|---|
| J1 Find | lands on the docs site and understands what this is for and how to start | home |
| J2 Create | on GitHub's web interface, makes a new **private** repository from `scpt-kg-template`, then clones it | getting started |
| J3 Set up | runs one documented command, gets a working `scpt`, and opens the folder as an Obsidian vault | getting started |
| J4 Plan | plans a facilitation event: who comes as actors and who as technologists, the Chatham House framing, stakeholder groups within the cap | planning guide |
| J5 Capture | during the event, records raw scenarios and raw architectures | the two facilitation guides |
| J6 Code | afterwards, in an interactive session (the `scpt` CLI in a terminal, or the Python REPL), decompiles the raw notes into SCPT pages and relations: creates stubs, moves pages to draft and done, regenerates the indexes, and fixes each error from its message using local and neighborhood checks | coding guide, CLI reference |
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
- Each tester starts from the Pages preview URL and follows only what the docs site says. J2 is simulated with
  `git clone --no-hardlinks` of the template with its remote removed; all other stages run as written. Each tester
  codes a small elicitation in a domain of its own, different from the worked example.
- Testers may not read `src/` or `tests/`. Every claim comes with pasted command output. Each tester reports, per
  stage: where it got stuck, what it had to guess, and where the docs left it with nowhere to go.
- **Pass bar:** every tester, the Haiku testers included, reaches J7 with a clean `check --all`. Every guess counts
  as a finding. Every finding is dispositioned: either fixed and re-tested by a fresh tester, or accepted with a
  reason and listed in the reviewer's guide. The final round leaves no blocking finding unresolved.
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
- The checks feel instant in an interactive session.
- The tools are small enough that one person can maintain them.
- The worked example reads in Obsidian as well as the paper's reader/reviewer screenshots suggest.

## Definition of good enough

- R-1 to R-12 met, with evidence.
- The AI user tests (UA-A) pass on the candidate.
- The candidate is staged for the chief engineer's own walkthrough (UA-M), with the reviewer's guide ready.
- The ontology trade study and the toolchain decision records exist. Every TBox term traces to an adopted ontology
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
  - `scpt-kg-template` is marked as a GitHub template, with `dev` as its default branch until the release;
  - the template pins the tools to the exact candidate commit.
  At the release, `v0.1.0` tags that same commit, the site redeploys from `main`, and the template's default branch
  returns to `main`.
- Amendments to this mission are approved by the same act as the mission.
- How the team runs is in `ORG.md`.

## Initial breakdown (a plan, not a contract; the ACE revises it at each work-package acceptance)

Ontology design comes before implementation, and the design is driven by research.

1. **WP1 Ontology research sprint.** Survey existing ontologies for each SCPT class and relation, and the patterns
   in `concept-definition-stage`. Run the trade study (adopt and thin, or author) and assess easy-win axioms.
   Readout and decision records. Fixes: what the TBox imports, anchors to, or authors.
2. **WP2 Toolchain spike.** In parallel with WP1. OKF, oxigraph, pydantic and the rule language, tried on a throwaway
   mini-vault and measured. Fixes: the toolchain.
3. **WP3 Ontology and page contracts.** From WP1 and WP2: the TBox in Turtle, fields per class, page types, link
   rules, status rules, the rule catalogue with ids and message wording. Fixes: D-1 and the vault conventions.
4. **WP4 Conformance tools.** Parser, checks, the Python API and the CLI over it, seeded-defect tests, benchmark.
   Fixes: D-2.
5. **WP5 Template and case study.** In parallel with WP4 once WP3 is accepted. Fixes: D-3.
6. **WP6 Docs and Pages.** Written journey-first (J1–J7). Fixes: D-4.
7. **WP7 Candidate and user acceptance.** Integration, the candidate stage, UA-A rounds to the pass bar, the
   reviewer's guide and the walkthrough script. Fixes: D-6, D-7.

## Agent's defaults

- Names: `scpt-kg-tools`, `scpt-kg-template`, CLI command `scpt`.
- The mission, org and decision records live in `scpt-kg-tools`.
- Python ≥ 3.12. The template installs the tools through uv as a git dependency pinned to a commit; no PyPI.
- Facilitation and coding guides are written once, on the Pages site; the template links to them rather than copying them.
- Status strictness (R-3) and speed thresholds (R-5) as stated above.
- Documentation built with MkDocs Material (as in `assurances-audits-accountability` and `knowledgecomplex`).
- CI on GitHub Actions, ubuntu-latest; development on macOS. `.python-version` (3.12) and `uv.lock` are committed; CI runs
  `uv sync --locked`, `uv lock --check`, ruff check and format, and pytest.
- Branches: `main` holds approved missions and releases only; `dev` is the integration branch; work happens on
  short-lived unit branches off `dev`.
- Licence: Apache-2.0, copyright Dynamical Systems Group, for code, docs and ontology (the chief engineer's decision, D-005).
- Adopted definitions follow `concept-definition-stage`'s licence practice. Text under a restrictive licence (SEBoK is
  CC BY-NC-SA) is cited and linked, not reproduced, in anything we publish.
- The stakeholder-group cap is set in the template's configuration file, with the worked example set to 3.
- No AI attribution on commits, PRs or documents; CI fails on attribution lines, as in tradespace.

## Open decisions (for the chief engineer)

None. Every item was resolved through the decision loop and is recorded in `decisions/log.md`.
