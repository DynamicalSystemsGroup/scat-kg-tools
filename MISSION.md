# Mission — Scope of work: scpt-kg v0.1

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing is executed before then. |
| **Chief engineer (accountable)** | `mzargham` — final design authority; approves this mission and its amendments; accepts the v0.1 delivery |
| **Assistant to the chief engineer (ACE)** | The main Claude session — manages the team, writes and approves work-package scopes inside this mission, accepts work packages, escalates only what this mission cannot settle |
| **Repositories** | `scpt-kg-tools` (conformance tools, TBox, docs site; this document lives here) and `scpt-kg-template` (the vault to clone) |
| **Approval record** | The chief engineer's merge of this document's PR into `main` of `DynamicalSystemsGroup/scpt-kg-tools` (public) |
| **Acceptance record** | The chief engineer's merge of the release PR from `dev` into `main` in each repository. The ACE opens these PRs when the candidate is ready, and no one else does. The merge tags `v0.1.0` and deploys the site. |

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
Document Assurance* (INCOSE IS 2026) and the earlier repos `assurances-audits-accountability`, `knowledgecomplex` and
`ant-rdf`. The structure is simpler than those: no faces, no assurance triangles.

## Goals

- **G1. Fixed TBox.** Turtle files define seven ontology classes — Stakeholder group, Concern, Property, Technology,
  Heldby (stakeholder group × concern), Addresses (concern × property), Attributes (property × technology) — each
  record's required and optional fields, the page types that link into them (raw and coded scenarios, raw and coded
  architectures, class pages), and the linking rules.
- **G2. Vault ↔ graph.** Markdown pages with YAML frontmatter parse into an ABox that is checked against the TBox.
  Every class has a class page: a description plus an index table (name, short description, link) of its instances.
- **G3. Page lifecycle.** Every content page carries a status: `stub → draft → done`. A page that the ontology
  entails but that does not exist is created as a `stub`, so the graph is never incomplete, only unfinished.
- **G4. CLI** usable by a technically savvy non-developer in an interactive session:
  - `check <page>`, `check <page> --neighborhood`, `check --all` — conformance, with actionable messages;
  - `status` at the same three scopes, and a command to set a page's status;
  - `index` — regenerates class index tables from the instance pages;
  - a command that creates entailed missing pages as stubs.
  Local and neighborhood checks act as a fast linter during working sessions.
- **G5. Two repositories.** `scpt-kg-tools`: a slim, separately maintained package holding the TBox, the parser, the
  checks, the CLI and the documentation site. `scpt-kg-template`: the vault to clone, which installs a pinned
  version of the tools. Both builds are reproducible with uv.
- **G6. Worked example** in the template: minimal (users overwrite it) but with 2–3 records in every registry,
  plus two scenarios and two architectures, each raw and coded. It doubles as the test fixture and the documentation
  example.
- **G7. Documentation on GitHub Pages** (from `scpt-kg-tools`), following the user journey: plan a facilitation event;
  facilitate and capture raw notes (one guide for scenarios with actors, one for architectures with technologists);
  code the notes afterward; run the checks; plus a CLI reference.
- **G8. Toolchain decided by evidence.** Oxigraph, Open Knowledge Format (OKF), pydantic and the choice of rule
  language are tried on a small vault before the implementation is locked in. Each choice is recorded with its evidence.

## Non-goals

- Gen-AI aided authoring; an Obsidian plugin (the CLI is designed so one can wrap it later).
- Triangles or any faces, including ones inferred from scenarios and architectures.
- Changing the TBox, or letting instance repos extend it.
- Enforcing raw → coded links or embeds beyond a warning.
- Checking that named entities are linked beyond a basic regex warning.
- The verification / validation / human-signature assurance framework of the paper.
- Analysis tooling over the graph.
- Publishing to PyPI *(default: the template pins the tools by git tag)*.
- UX for non-technical users beyond the CLI and Obsidian.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | TBox in Turtle, in `scpt-kg-tools` | G1 |
| D-2 | Parser, checks, status, index and stub commands, CLI, test suite with seeded-defect fixtures, in `scpt-kg-tools` | G2, G3, G4 |
| D-3 | Template repository: vault skeleton (class pages, folders for raw and coded records), instance configuration (stakeholder-group cardinality cap), pinned tools, worked example | G5, G6 |
| D-4 | Documentation site, staged locally during the work and deployed to GitHub Pages by the release merge | G7 |
| D-5 | Decision records for the toolchain spike, with measurements | G8 |
| D-6 | Reviewer's guide for the chief engineer, in the release PR. It is sized for a person and split into sittings by output (tools and checks; template and worked example; docs site; the ACE's calls). Each sitting has a short checklist and its own local entry point. It lists every call the ACE made, with its evidence, and what is known to be weak. | all |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Errors block; warnings do not. Errors: required fields and types, relation endpoints of the right classes, coded scenarios and architectures linking into the graph correctly, stakeholder groups within the cap, valid status. Warnings: unlinked mention of a graph entity; raw record not linking or embedding its coded pages. | Seeded-defect tests, one or more per rule |
| R-2 | Every message names the file, the field or link, the rule broken (by id), and what to do to fix it. | Golden-output tests on seeded defects |
| R-3 | How strict a check is follows the page status: a stub needs only identity, type and status; draft and done are checked in full *(default: missing required fields warn on draft, error on done)*. | Tests per status |
| R-4 | `index` is the only command that rewrites class pages; the stub command is the only one that creates pages; checks never write. | Tests; inspection |
| R-5 | Speed on a laptop with a 500-page vault: local check < 1 s, neighborhood < 2 s, full < 5 s *(default thresholds)*. | Benchmark script |
| R-6 | Fresh clone of the template → one documented setup command → `check --all` passes on the worked example. | Clean-clone trial |
| R-7 | Both repositories commit `uv.lock`; CI runs tests and checks on every push. | CI runs |

## Definition of good

- A first-time user fixes every conformance error from the message alone, without reading the source.
- The checks feel instant in an interactive session.
- The tools are small enough that one person can maintain them.
- The demo vault reads in Obsidian as well as the paper's reader/reviewer screenshots suggest.

## Definition of good enough

- R-1 to R-7 met, with evidence.
- A simulated-user test passes: a cold agent with a technically savvy persona and an isolated clone of the template,
  following only the staged docs site, codes a small elicitation in a different domain from the worked example and
  reaches a clean `check --all`. Its report is pasted; what it had to guess is counted as defects and fixed or
  dispositioned.
- The documentation site builds strictly, covers the whole journey, and has had the ACE's browser pass on every page
  (desktop and phone width), with findings fixed or listed. It deploys on the release merge.
- The spike's decision records exist.

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
- Until the release PR, nothing is merged to `main`, tagged, deployed or published. The only exception is this
  mission's own approval and its amendments.
- Amendments to this mission are approved by the same act as the mission.
- How the team runs is in `ORG.md`.

## Initial breakdown (a plan, not a contract; the ACE revises it at each work-package acceptance)

1. **WP1 Toolchain spike.** OKF, oxigraph, pydantic and the rule language, tried on a throwaway mini-vault and
   measured. Fixes: the toolchain.
2. **WP2 Ontology and page contracts.** Fields per class, page types, link rules, status rules, the rule catalogue
   with ids and message wording. Fixes: the TBox and the vault conventions.
3. **WP3 Conformance tools.** Parser, checks, CLI, seeded-defect tests, benchmark. Fixes: D-1, D-2.
4. **WP4 Template and worked example.** Can run in parallel with WP3 once WP2 is accepted. Fixes: D-3.
5. **WP5 Docs and Pages.** Fixes: D-4.
6. **WP6 Integration and simulated-user test; release candidate and review.** Fixes: D-6.

## Agent's defaults

- Names: `scpt-kg-tools`, `scpt-kg-template`, CLI command `scpt`.
- The mission, org and decision records live in `scpt-kg-tools`.
- Python ≥ 3.12; the template installs the tools from a git tag through uv; no PyPI.
- Facilitation and coding guides are written once, on the Pages site; the template links to them rather than copying them.
- Status strictness (R-3) and speed thresholds (R-5) as stated above.
- Documentation built with MkDocs Material (as in `assurances-audits-accountability` and `knowledgecomplex`).
- CI on GitHub Actions, ubuntu-latest; development on macOS. `.python-version` (3.12) and `uv.lock` are committed; CI runs
  `uv sync --locked`, `uv lock --check`, ruff check and format, and pytest.
- Branches: `main` holds approved missions and releases only; `dev` is the integration branch; work happens on
  short-lived unit branches off `dev`.
- Licence: MIT, copyright Dynamical Systems Group, for code, docs and ontology. This follows the tradespace precedent (`WP8-decisions.md` there).
- Worked example domain: a city bike-share scheme. It's familiar, has clear stakeholder groups (riders, city transport
  office, operator), and gives obvious stories of things going wrong and right. It differs from any DSG project domain.
- The stakeholder-group cap is set in the template's configuration file, with the demo set to 3.
- No AI attribution on commits, PRs or documents; CI fails on attribution lines, as in tradespace.

## Open decisions (for the chief engineer)

None. Every item was resolved through the decision loop: 1 decided by the chief engineer (OD1: public repositories
in `DynamicalSystemsGroup`, approval by PR merge), 1 assigned to the ACE (OD2: the Agent's defaults are the ACE's
sign-off under the governance rule), 0 deferred, 0 raised. See `decisions/log.md` D-001 and D-002.
