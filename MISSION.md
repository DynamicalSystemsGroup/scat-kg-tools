# Mission — Scope of work: scat-kg v0.1

| | |
|---|---|
| **Status** | Approved by the chief engineer's merge of PR #1 into `main` of `DynamicalSystemsGroup/scat-kg-tools`. Each amendment is approved by the merge of its own PR; Amendment 1 is PR #2, Amendment 2 is PR #4, Amendment 3 is PR #5, Amendment 4 is PR #6 and Amendment 5 is PR #8. |
| **Chief engineer (accountable)** | `mzargham`: final design authority. Approves this mission and its amendments, and accepts the v0.1 delivery. |
| **Assistant to the chief engineer (ACE)** | The main Claude session. Manages the team, writes and approves work-package scopes inside this mission, accepts work packages, and escalates only intent gaps (see Governance). |
| **Repositories** | `scat-kg-tools` (the tools, the TBox, the docs site; this document) and `scat-kg-template` (the vault to clone). |
| **Acceptance record** | The chief engineer's merge of the release PRs, as set out under Governance, "Release". |

## Purpose

DSG needs, for an upcoming project, a first usable release of a toolkit for turning facilitated discussions into a
conformant knowledge graph. Participants tell stories (scenarios) and propose architectures. Their raw notes are coded
into pages of an Obsidian vault in git. Coding decompiles each scenario and architecture into four concepts:
**s**takeholders, **c**oncerns, **a**ffordances and **t**echnologies. The acronym is SCAT, named for scat singing in
jazz. Coding relates the four concepts through explicit relationships, layered as bipartite graphs:
stakeholders–concerns, concerns–affordances, and affordances–technologies.

The result is a navigable, interpretable dataset, and that dataset is the data product. Its conformance to a fixed
ontology is what makes it analysable. It is scaled to a human note-taker: just enough structure to make the data
interpretable, but mostly a formal structure for arranging Obsidian notes. The git repository is the data of record,
and the graph is derived from it.

The point of departure is the toolchain, and the Obsidian reading and review experience, described in *Formalizing
Document Assurance* (INCOSE IS 2026; the chief engineer has a copy), together with earlier repositories:
- `ant-rdf` (<https://github.com/mzargham/ant-rdf>);
- `knowledgecomplex` (<https://github.com/DynamicalSystemsGroup/knowledgecomplex>);
- `assurances-audits-accountability` (<https://github.com/DynamicalSystemsGroup/assurances-audits-accountability>);
- `concept-definition-stage` (<https://github.com/Open-MBEE/concept-definition-stage>). This one is also a reference
  for the ontology: its SKOS+PROV spine, its definitions traced to their authorities, and its practice of anchoring to
  an external ontology through equivalence axioms instead of importing all of it.

The structure here is simpler than any of them.

## Core heuristics

- **For the users: "make the right way the easy way".**
- **For the builders: "as simple as possible but no simpler".**

When a choice isn't settled elsewhere, these decide it. Over-specifying is a failure too. This mission states intent
and outcomes; how to achieve them is decided in the work packages, by evidence. Design guidance at the end of this
document is advice, not requirement.

## Scenarios and architectures

The two record types look at the same graph from opposite sides. This is an important heuristic for facilitating,
capturing and coding.

- **Scenarios are behavioural.** They tell the story of people within an action situation doing things, through which
  outcomes and consequences are wrought. They are temporal. Technologies are part of the action situation but not
  the focus: they stay relatively fixed and out of view, and what is legible is their **affordances**. A coded
  scenario relates stakeholder groups, concerns and affordances.
- **Architectures are structural.** They formulate assemblages: parts and wholes, and how parts are assembled into
  tools that provide affordances which address concerns. Stakeholders are largely abstracted away. What is addressed
  is concerns, and the same concern can arise from different stakeholders; an architecture can't presume which
  stakeholders will adopt it. A coded architecture relates concerns, affordances and technologies.

A second lens cuts across the first: **past or future**. A story may tell what happened or what could happen. An
architecture may describe a system that exists or one that is proposed. The rule is simple, because the present is
nebulous: anything real that can be narrated is past, and anything being done with intention but not yet realized is
future. Behavioural or structural, past or future: the docs show this as a 2×2 for unbundling narratives. Every
scenario and architecture records which it is (log D-057). Only these records are marked: stakeholder groups,
concerns, affordances and technologies are not, and the three relations don't change.

People mix past and future freely when they talk. The facilitation guides lead participants to the past and the
future at separate times in a workshop, and explain the mark with example phrases, including ones that mislead: a
counterfactual "what would happen if" is future, and a habitual "when someone would do x, y happens" is past. A
record may be marked **mixed**, the honest record of an account that blurs the two. The mark only tags the captured
narratives, and the guidance on it lives in the facilitation guides alone.

Whether the narrator sees what is told as good, bad or a mix is not recorded in the schema. For anything real a mix is
expected, and it stays in the story's own words. SCAT is pragmatic and thin. It doesn't compete with richer ontologies
such as `ant-rdf`, which cost more and do more analytically: problematization belongs there, and nothing stops the same
case from being coded in both, with different tools.

Calling participants "actors" (users, sponsors and other stakeholders, who tell scenarios) or "technologists"
(researchers, developers and operators, who pitch architectures) is a facilitation device, not a division of people.
Many people are both.

## Facilitation stance: improvisational jazz

SCAT takes its name, and its manner, from scat singing in improvised jazz. Facilitation works by "yes, and" and "from
this perspective": each contribution is taken up and built on, and each is placed in the perspective it comes from.

The model **holds disagreement rather than collapsing it.** As in `ant-rdf`, it exposes frictions, gaps and dissenting
views, and it can represent margins of potential conflict. One example is groups that share a concern while their other
concerns are directly opposed. So nobody has to argue anyone into agreement. We capture people's stories and their
proposed architectures. We do not debate which architecture is correct, or which stories should be the focal point
of a design.

## Users and how they work

The v0.1 user is a facilitator-analyst: technically savvy, but not a software developer, working on macOS for v0.1 (see Governance).
They:
- navigate GitHub's web interface, including creating a repository from a template;
- read, write and follow links in an Obsidian vault;
- work in an **interactive session** in the Python REPL (`import scat_kg`), with the `scat` CLI as an equal path to
  the same operations and messages. The docs lead with the REPL, because CLI commands get long when run through uv;
- follow documentation literally, step by step.

The people in the data are stakeholder **groups**, under the Chatham House rule, so no individual is identifiable.
Each vault sets a cap on how many stakeholder groups it holds, and participants are clustered into groups that fit
under it (the chief engineer's initial brief).

## Goals

- **G1. Fixed TBox.** Designed through G10's research, then fixed for v0.1. Turtle files define:
  - the four SCAT classes (Stakeholder group, Concern, Affordance, Technology) and the three relations between
    them: Heldby (stakeholder group × concern), Addresses (concern × affordance) and Attributes (affordance ×
    technology). Names may follow an adopted ontology;
  - each record's required and optional fields;
  - the other page types: class pages, raw and coded narratives, with raw and coded scenarios and architectures as
    their subclasses (Amendment 5);
  - two base classes, from the knowledge-complex pattern at its lowest dimensions (Amendment 5): **vertices** (the
    four SCAT classes, 0-simplices) and **edges** (the three typed relations, 1-simplices). Narrative is a base class
    of its own, outside that pattern. Each edge between a given pair appears once, and names the narratives that
    refer to it. A narrative is coded by identifying its vertices and edges; its **support** is the subgraph of every
    vertex and edge it mentions;
  - the past, future or mixed mark every scenario and architecture records (see "Scenarios and architectures");
  - the linking rules, reflecting how scenarios and architectures differ;
  - how the graph holds disagreement and margins of potential conflict. At minimum, the same concern can be held by
    different stakeholder groups;
  - one generic **relationship** between two records of the same class: a note with a place in the graph, whose only
    rule is that both ends share a class. It is optional, the tools give it no meaning, and analysis views leave it
    out. It replaces the typed `conflicts` link between concerns (Amendment 5).
- **G2. Vault ↔ graph.** Markdown pages with YAML frontmatter parse into an ABox that is checked against the TBox.
  Every class has a class page: a description, plus an index table of its instances (name, short description, link)
  that the tools generate from the instance pages.
- **G3. Page lifecycle.** Every content page carries a status, `stub → draft → done`. Class pages are generated, so
  they carry none. The tools create any page the ontology entails that doesn't exist yet, as a `stub`, so the graph is
  never incomplete, only unfinished.
- **G4. Operations**, in the Python API and the `scat` CLI, usable in an interactive session:
  - check conformance at three scopes: one page, its neighborhood (the page plus everything one link away, in either
    direction), and the whole vault;
  - read status at the same three scopes, and set a page's status;
  - regenerate the class indexes;
  - create entailed missing pages as stubs.

  The local and neighborhood checks act as a fast linter during working sessions.
- **G5. Two repositories.** `scat-kg-tools` is a slim, separately maintained package with the TBox, the tools and the
  docs site. `scat-kg-template` is the vault to clone, which installs a pinned version of the tools. Both builds are
  reproducible with uv.
- **G6. The worked example is this project, as its own case study.** The template's example content is the
  elicitation of scat-kg itself, drawn from the chief engineer's recorded statements and the decision log. It is small,
  because users overwrite it, but every class has 2–3 instances, and there are two scenarios and two architectures,
  each raw and coded. Its stakeholder groups follow the Chatham House rule like any others: no group stands for one
  identifiable person. It avoids politically loaded illustrations. It doubles as the test fixture and the
  documentation example.
- **G7. Documentation on GitHub Pages**, from `scat-kg-tools`, with a light musical reference (R-15). It has a page for each
  stage of the journey: getting started, a planning guide, a scenario facilitation guide, an architecture facilitation
  guide and a coding guide. It also has a reference for the Python API and the CLI.
- **G8. Toolchain decided by evidence.** The candidates are tried on a small vault and measured before the
  implementation is locked in:
  - oxigraph;
  - Open Knowledge Format (OKF, <https://github.com/open-knowledge-format/open-knowledge-format>);
  - pydantic;
  - the choice of rule language.

  Each choice is recorded with its evidence.
- **G9. Clear user journey.** A technically savvy user who isn't a developer can get from the docs site to a new
  repository made from the template, through an interactive working session, to a clean, navigable graph, using only
  the documentation.
- **G10. Ontology by evidence: import, don't mint.** A research sprint surveys existing ontologies for each SCAT class
  and relation. Examples: ISO/IEC/IEEE 42010 for stakeholders and concerns, the SEBoK and INCOSE canon that
  `concept-definition-stage` commits, SKOS and PROV.
  - **Trade study:** for each class, adopt an existing ontology (thinned to what we use, and anchored rather than
    imported whole) or author our own, but only where nothing beats custom.
  - **Coherence:** the result is one coherent ontology, not a patchwork. Every term traces to its source, or is
    recorded as authored, with the reason.
  - **Easy wins:** we take easy wins in expressiveness where they don't complicate the software or the UX. The first
    candidate was a conflict between concerns, such as anonymity versus attribution, which the chief engineer called a
    disjointness axiom. Amendment 5 withdraws it: typed links between records of the same class are not yet stable
    enough to fix, so v0.1 offers only the generic relationship (G1).
  - **Disagreement:** how the graph holds disagreement is decided when the TBox is designed, from both this research
    and G11's.
- **G11. Facilitation strategy grounded in research.** The planning and facilitation guides are written from a
  facilitation strategy derived from prior work: `ant-rdf` (its handling of controversy, dissent and multiple
  perspectives), "KOI & The Unicorn" (<https://blog.block.science/koi-and-the-unicorn/>), "Building the Loop" (EPIC
  2025, DOI 10.1111/epic.70009), and recent unpublished grant-proposal drafts from the same collaboration, which the
  chief engineer supplies and which are read for principles only. The strategy covers the improvisational stance,
  eliciting scenarios and architectures, and holding disagreement without adjudicating it.
- **G12. A template analysis notebook (Amendment 5).** The template carries a notebook that loads a vault bound to the
  schema and gives a few named views. The first is the **narrative view**: one coded narrative's support (G1), the
  vertices and edges it mentions, drawn as four columns in class order (group, concern, affordance, technology) with
  the edges between neighbouring columns. The second is the **composed view**: the same drawing of the graph
  that emerges from composing the supports of a set of narratives, up to the whole vault. A
  narrative is a page type of its own (G1): the parent of scenario and architecture, so a field note may be neither.
  The past/future mark is a property of the narrative.
  Relationships (G1) stay out of the views.
- **G13. Ripple-aware change (Amendment 5).** A change to a term, a contract, a rule or the mission reaches every
  artifact that depends on it, in one package, and no two packages edit the same file in turn (see Governance).

## Non-goals

- Gen-AI aided authoring or coding in v0.1. Two spikes explore it (Amendment 5): the feasibility of AI-aided coding,
  with a tooling choice (tool calls, skills, or an MCP server that depends on `scat-kg`); and compatibility with
  inference.coop, the only AI approved to touch the pilot's field notes. Their readouts feed later amendments.
- The Obsidian plugin (Amendment 5). It stays on its feature branch (log D-054); v0.1 provides the stable interface it
  builds on (R-16).
- Typed links between records of the same class, such as incompatible concerns, adversarial groups, complementary
  affordances or compatible technologies. They are parked on the feature branch `feature/same-type-edges`
  (Amendment 5), and nothing in the release refers to them.
- Faces or triangles of any kind, including ones inferred from scenarios and architectures.
- Letting instance repositories extend the TBox, and evolving the TBox after v0.1.
- Enforcing links from raw records to their coded pages beyond a warning.
- Checking that named entities are linked, beyond a basic warning.
- The verification, validation and human-signature assurance framework of the INCOSE paper.
- Attributing statements to individuals. v0.1 is built for Chatham House settings, and attribution is a possible
  extension. How raw notes are taken is the facilitator's call, and the guides explain the rule.
- Recording the narrator's normative posture (good, bad or mixed) in the schema. It stays in the story's text;
  problematization is for a richer ontology such as `ant-rdf`, applied afterwards (log D-057).
- Adjudicating between stories or architectures. Neither the tools nor the guides judge which architecture is correct
  or which stories should be focal.
- Analysis tooling beyond the template notebook's views (G12). RS2 stays on its feature branch (log D-054).
- Publishing to PyPI.
- A path for users who don't use a terminal or REPL.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The TBox in Turtle, in `scat-kg-tools` | G1, G10 |
| D-2 | The tools (parser, checks, the operations, the Python API and CLI, and their machine-readable output with its schema) with their test suite, in `scat-kg-tools` | G2, G3, G4 |
| D-3 | The template repository: vault skeleton, class pages, instance configuration (the stakeholder-group cap), the pinned tools, the case study, and the analysis notebook | G5, G6, G9, G12 |
| D-4 | The documentation site on GitHub Pages: a candidate preview during user acceptance, then the release | G7, G9, G11 |
| D-5 | Research readouts and decision records: the ontology survey and trade study, the toolchain spike, the facilitation research, and the two AI spikes (Amendment 5) | G8, G10, G11 |
| D-6 | The reviewer's guide for the chief engineer, in the `scat-kg-tools` release PR. It is sized for a person and split into sittings: (1) the end-to-end walkthrough (UA-M); (2) the docs site; (3) the tools and checks; (4) the ACE's calls. Each sitting has a short checklist and its own entry point. It lists every call the ACE made, with its evidence, and what is known to be weak. | all |
| D-7 | The user-acceptance kit, in `scat-kg-tools/acceptance/`: the AI tester personas and briefs, the report template, every AI test report with its dispositions, and the walkthrough script | G9 |

## Requirements

Requirements state outcomes. How each is met is decided in the work packages.

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Conformance checks structure, never content: types, fields, links, names, status, the cap and index freshness. What the content says (tensions, matches, gaps) is for analysis, after conformance passes and the coder signs off the content (log D-052). Conformance problems are graded: errors block and warnings don't. Errors cover the ontology's constraints (required fields and types, relation endpoints, the linking rules), the stakeholder-group cap, valid status, and links to pages that don't exist. The rule catalogue gives every rule an id and a severity. | Seeded-defect tests, at least one per rule |
| R-2 | Every message names the file, the field or link, and the rule broken (by id). It gives the fix as something a literal reader can apply: an exact command to run, or an exact field and value to write. | Golden-output tests on the seeded defects |
| R-3 | An unfinished page is never an error just for being unfinished. The full contract applies when a page is `done`. Links and relation endpoints are checked at every status. | Tests per status |
| R-4 | Checks never write to the vault. Every write is an explicit operation (index, stub, set status). | Tests that snapshot the vault before and after each operation |
| R-5 | The checks are fast enough to work as a linter. On a laptop, with a 500-page vault: one page under 1 s, a neighborhood under 2 s, the whole vault under 5 s *(ACE's thresholds)*. | Benchmark over a generated 500-page vault |
| R-6 | Starting from a clean user environment with only the documented prerequisites: a fresh clone of the template, then one documented setup command, after which `check` on the whole vault passes on the worked example. | Clean-environment trial |
| R-7 | Both repositories commit `uv.lock`, and CI runs the tests and checks on every push. | CI runs |
| R-8 | The Python REPL and the `scat` CLI are equal paths: every operation is available on both, with the same messages. The docs lead with the REPL and show the CLI equivalent alongside it. | Tests on both paths; the docs test runs both |
| R-9 | Every snippet and command shown in the docs runs as shown, and the CLI reference matches `--help`. | A docs test that extracts and runs them; a reference diff |
| R-10 | The docs site has no dead ends or broken links. Every journey page says what you need before you start and where to go next. | Strict build and link check; the ACE's browser pass over every page, at desktop and phone width |
| R-11 | **Make the right way the easy way.** There is one obvious way to create each kind of page, and users never hand-write structure the tools can generate. Each journey page leads with the one action to take next. | The Haiku testers' reports; the ACE's review |
| R-12 | Repositories made from the template are private by default, and the docs and the template's README recommend private repositories. | A probe of the documented creation path on the candidate; UA-M |
| R-13 | The schema has one source. The TBox is authoritative; any other form the tools use is generated from it or held equal to it by a test. | The generator or the equality test, in CI |
| R-14 | The planning and facilitation guides carry the improvisational stance ("yes, and"; "from this perspective"). They contain no step that ranks, votes on or adjudicates between stories or architectures. | The ACE's review of the guides; UA-M |
| R-15 | **A light musical reference, clarity first.** The package and its docs carry the music-note logo and one brief aside on improvisation, where the "yes, and" stance is introduced. Everywhere else, plain words win over any musical reference. | The chief engineer's judgement in UA-M (log D-052) |
| R-16 | **A stable machine interface.** Every result the operations return is also available as versioned, machine-readable data, from the Python API and the CLI alike. Its schema lives with the contracts, and changing it follows a stated versioning rule. A fix is data a tool can apply (what kind of fix it is, the exact command, or the field to write), not only a sentence. This is the interface the Obsidian plugin and any later tool build on (log D-060). | Every operation's output validated against the schema in tests; a test that the text messages and the data agree |
| R-17 | **The notebook runs.** The template's analysis notebook runs top to bottom on the template's vault, and its narrative view gives, for each coded narrative, exactly its support, with no relationship. | The notebook executed in the template's CI, with a test on the view |
| R-18 | **Ripple-complete changes.** Before a package that changes a term, contract, rule or the mission is approved, its impact map lists every artifact that refers to what changes, each marked change, keep (with why) or historical. At acceptance, the same sweep finds no reference that is unmarked or still says the old thing. | The impact map in the scope; the sweep's output in the acceptance record |

## User acceptance

Acceptance is judged by people using the product, not only by tests. The journey under test:

| Stage | The user | Docs page |
|---|---|---|
| J1 Find | lands on the docs site and understands what it is for and how to start | home |
| J2 Create | on GitHub's web interface, makes a new **private** repository from `scat-kg-template`, then clones it | getting started |
| J3 Set up | installs the prerequisites from exact commands, runs one setup command, gets a working `scat_kg`, and opens the folder as an Obsidian vault | getting started |
| J4 Plan | plans a facilitation event: which sessions elicit scenarios and which elicit architectures, who takes part in each, the Chatham House framing, and stakeholder groups within the cap | planning guide |
| J5 Capture | during the event, records raw scenarios and raw architectures | the two facilitation guides |
| J6 Code | afterwards, in an interactive session (the Python REPL or the `scat` CLI), decompiles the raw notes into SCAT pages and relations, moving pages from stub through draft to done and fixing each problem from its message | coding guide; API and CLI reference |
| J7 Finish | reaches a clean whole-vault check, commits and pushes, and navigates the resulting graph in Obsidian | coding guide |

**UA-A, the AI user tests**, run by the team on the candidate before the chief engineer's walkthrough:

- **Personas.** At least three, each written in the user's own words and never the tool's vocabulary. **Most run on
  Haiku**, so the test doesn't depend on much reasoning: if the right way needs reasoning to find, it isn't yet the
  easy way.
  - a facilitator-analyst who is comfortable with a terminal, GitHub and Obsidian but is not a developer (Haiku);
  - a newcomer to Obsidian and the command line, careful and literal (Haiku);
  - the same facilitator-analyst on Sonnet, as a control: a step that Sonnet passes and Haiku fails points to the
    docs or the tools, not the user.

  At least one Haiku tester works in the Python REPL, and at least one uses the CLI.
- **Setup.** Each tester starts in a clean user environment (a fresh home directory, uv not installed), from the
  Pages preview URL, and follows only what the docs say.
  - J2 is simulated with an isolated clone of the template that has its remote removed.
  - The Obsidian steps (J3, J7) are checked through the files. Obsidian itself is covered by UA-M.
  - Each tester codes a small elicitation in a domain of its own, different from the worked example: at least one
    scenario and one architecture, each raw and coded.
- **Reporting.** Testers may not read `src/` or `tests/`, and every claim comes with pasted output. A report first
  answers what style or reference the docs evoke. Then, stage by stage, it says where the tester got stuck,
  what it had to guess, and where the docs left it with nowhere to go.
- **Pass bar.** Every tester, the Haiku testers included, reaches J7 with a clean check. Every guess (any action the
  docs did not literally state) counts as a finding. A finding is **blocking** if it stopped the tester short of J7,
  or if a docs command doesn't work as shown. Every finding is dispositioned: either fixed and re-tested by a fresh
  tester, or accepted with a reason and listed in the reviewer's guide. The final round leaves no blocking finding.
- **Void reports.** A report that reuses names from the worked example, or that makes claims without pasted output,
  is void and is run again. A report with no findings is checked by the ACE for plausibility.

**UA-M, the chief engineer's walkthrough** (the first sitting of the reviewer's guide, and the core of acceptance):

- He runs J1 to J7 himself on the candidate. He starts from the Pages preview, makes a real repository through the
  documented creation path, clones it, sets up, and works through an interactive session with the REPL and the CLI,
  coding a small elicitation of his own choosing.
- The walkthrough script gives each stage's entry point and what "done" looks like, so the session can be split and
  resumed.
- **Pass:** he completes the journey from the documentation without help, and judges the documentation clear and
  navigable and the journey clear.
- Anything he flags is fixed on `dev`, and the candidate is refreshed (see Governance, "Release"). The walkthrough
  then resumes from the affected stage.

## Definition of good

- Make the right way the easy way: following the docs literally, and using the provided templates and operations, is
  the shortest path, and it produces a conformant vault.
- The ontology is lean and recognisable: adopted where an existing ontology wins, authored where it doesn't, never a
  patchwork.
- A first-time user fixes every conformance problem from the message alone, without reading the source.
- The worked example reads well in Obsidian, as judged by the chief engineer in UA-M.

## Definition of good enough

- R-1 to R-15 met, with evidence.
- UA-A passes on the candidate.
- The candidate is staged for UA-M, with the reviewer's guide ready.
- The ontology, toolchain and facilitation research readouts exist. Every TBox term traces to an adopted ontology or
  is recorded as authored, with the trade study's reason.

## Definition of done

Good enough is met, and no open item remains. Open items are open decisions, unresolved gaps and blocking findings.
The chief engineer has accepted by merging the release PRs.

## Governance

- **Sign-offs.** The chief engineer signs off on exactly two things: this mission (and its amendments) and the
  acceptance of the delivery. Every other sign-off belongs to the ACE. The ACE approves each work-package scope inside
  this mission, accepts each package against its scope, and logs every ruling in `decisions/log.md`.
- **Intent gaps.** The ACE escalates only an **intent gap**: a question that this mission and the chief engineer's
  recorded statements don't settle, and that changes what is built or whether it serves its purpose. Escalations come
  one at a time, with a recommendation, while other work continues. This is the one definition; `ORG.md` points here.
- **Evidence.** The ACE runs a spike wherever the evidence for a call is missing. Every call is recorded with its
  evidence for the chief engineer's review at acceptance, and reversing any of them is his prerogative.
- **The plan.** The ordered work packages are kept in `work-packages/plan.md`, which the ACE owns and revises at
  each package acceptance. It must respect these orderings:
  - the ontology research comes before the TBox and page contracts;
  - the TBox and page contracts come before implementation;
  - the toolchain is chosen by its spike before implementation;
  - the facilitation research comes before the facilitation guides;
  - the user tests come last.
- **TBox changes before release.** Once the TBox and page contracts are accepted, a change to them during v0.1 is the
  ACE's logged call if it serves the mission as written. It is an intent gap if it would change what the graph means.
- **Constraints set by the chief engineer:**
  - Apache-2.0 licence, copyright Dynamical Systems Group, for code, docs and ontology (log D-005);
  - adopted ontologies, standards and their definitions are used directly and cited, per engineering practice (log
    D-012);
  - private sources are read for principles only, and since the repositories are public, readouts cite only published
    work;
  - no AI attribution on commits, PRs or documents.
  - **Platforms:** macOS is the supported user platform for v0.1, and CI runs on Linux. Nothing may be built in a
    way known to put later Linux or Windows support at risk: no platform-specific paths, shells, line endings or
    tools in the package, and anything unavoidably platform-specific is isolated and recorded (log D-021).
- **Until the release,** nothing is merged to `main`, tagged or published, with two exceptions:
  - this mission's approval and amendments;
  - the **candidate stage** that UA-M needs:
    - the docs site deploys from `dev` to Pages, marked pre-release;
    - `scat-kg-template` is marked as a GitHub template, with `dev` as its default branch;
    - the template pins the tools to the candidate commit.

  Every fix during user acceptance moves the pin, reruns CI, R-6 and R-9, and the ACE decides, and logs, whether
  UA-A reruns.
- **Release.**
  1. The ACE opens one release PR from `dev` to `main` in each repository, and no one else does.
  2. The chief engineer's walkthrough runs against them, and his merges, as merge commits, are the acceptance.
  3. The ACE then tags `v0.1.0` on the merge commit in each repository, redeploys the site from `main` without the
     pre-release mark, and restores `main` as the template's default branch. The template's pin stays on the
     accepted candidate commit, whose content the tag marks.
- **Ripple-aware change (Amendment 5).** A change-management consultant, an agent that supports the PM, builds each
  impact map (R-18) before the ACE approves a scope and re-runs the sweep before acceptance. It also keeps the file
  map of the packages in flight: packages whose blast radii overlap are merged or put in order, never run so that
  one undoes another.
- **How the team runs** is set out in `ORG.md`.

## Timeline

No date is set. A date is deferred until velocity has been established (log D-011). The estimates are lightweight and
agile in style: a heuristic for driving convergence and forecasting, not a schedule fixed in advance, and they are
expected to be noisy at first.
- **Ownership.** The PM owns the timeline. Every unit gets story points when it is planned *(default scale 1, 2, 3,
  5, 8; anything bigger is split)*. An **iteration** is one batch of units that the PM dispatches and lands *(default)*.
- **Velocity.** The board records each iteration's points done and its elapsed wall-clock time, so velocity converts
  to a date. The forecast to the candidate is updated from the measured velocity.
- **What it forecasts.** The forecast runs to **a candidate ready for the chief engineer's review**, including
  testing, the UA-A rounds and the revisions they cause. Time to address his review feedback is estimated later, when
  that feedback exists.

## Design guidance (not binding)

Starting points for the work packages, from what has been learnt so far. A package may depart from any of these by
recording why.
- **Page creation.** Obsidian page templates suit the four record types, which people write in Obsidian. Entity and
  relation pages are better created by the tools from links in coded records, so users never write their structure.
- **Linking severity.** A scenario that links a technology, or an architecture that links a stakeholder group, is
  probably a warning that points to the affordance or the concern, rather than an error.
- **Status strictness.** On a `draft` page, missing required fields are probably warnings.
- **CLI and API.** The CLI is best kept as a thin layer over the Python API.
- **Private repositories.** A creation link that pre-selects private visibility, or `gh repo create --template …
  --private`, would make private the default.
- **Ambiguous names.** If two pages share a filename, addressing a page by name is ambiguous. The page contracts
  should settle this.
- **Prior spike findings** (the halted first run, archived as tags `archive/pre-amendment-1/*`): all three stacks
  were far inside R-5; exact fixes in error messages are the hard part of R-2; OKF did not yet fit. Verify these
  again; don't inherit them.

## Agent's defaults

- Names: `scat-kg-tools`, `scat-kg-template`, the CLI `scat`, the Python package `scat_kg`.
- Python 3.12 or later. The template installs the tools through uv, as a git dependency pinned to a commit.
- Facilitation and coding guides are written once, on the Pages site, and the template links to them.
- Documentation built with MkDocs Material.
- `.python-version` and `uv.lock` are committed. CI runs `uv sync --locked`, `uv lock --check`, ruff (check and
  format) and pytest, and fails on attribution lines.
- Branches: `main` holds approved missions and releases only, `dev` is the integration branch, and work happens on
  short-lived unit branches off `dev`.
- The worked example sets the stakeholder-group cap to 3.
- The machine interface (Amendment 4): JSON, from `--json` on every `scat` command and an equivalent method on every
  result in Python. Its schema is a JSON Schema file in `contracts/`, with an integer `schema_version`. Adding a field
  keeps the version, and removing or changing one bumps it. Schema validation runs in the test suite only, so it adds
  no runtime dependency to `scat-kg` (log D-056). Not included: checking an unsaved editor buffer, and a public vault
  loader for analysis. Both are left for the packages that need them.
- The past/future mark (Amendment 3) is a field on the raw scenario and raw architecture pages, the record of what was
  told; a coded page is a reading of its raw page and inherits it. Working field name `timeframe`, with the chief
  engineer's values `past`, `future` and `mixed`. Like every required field (R-3), a missing value is an error on a
  `done` page and a warning before.
- Amendment 5 *(default)*:
  - **Relationship's form.** A relation page per pair, like the three links: type `relationship`, two ends of the same
    class, and the note in its body. Its only rule is the same-class check; it is never entailed, never required and
    never in an index's required links. The `conflicts` field, its rule `SCAT-CONFLICT-SELF` and every mention of
    them leave the release; existing `conflicts` values migrate to relationship pages.
  - **The parked branch.** `feature/same-type-edges` holds the withdrawn `conflicts` material and the chief engineer's
    notes on the four typed links. It is a parked design, not work to build.
  - **The notebook** reads the vault through the tools' public data (R-16) where it can, which needs the public vault
    loader that Amendment 4 left for "the packages that need them".
  - **The consultant** runs on Sonnet as a role in `.claude/agents/`. Its sweep is a written list of search terms per
    change, run with `git grep` over both repositories and the live branches, so the same sweep runs at scoping and
    at acceptance.
  - **The spikes** run on side branches with readouts in `research/`. In spike B the chief engineer signs in; the
    agent never enters credentials, and only synthetic data goes to inference.coop.
  - **Order.** WP12 is accepted, then the relationship change, which absorbs WP13's pages so the shared docs are
    edited once, then the notebook. The spikes run alongside, since they touch no release file.

## Open decisions (for the chief engineer)

Amendment 5 (open, asked one at a time):
1. **Narrative in the schema.** Decided: a page type of its own (PR #8 thread).
2. **Which links "appear within" a field note.** Decided: each edge appears once per pair and names the narratives
   it came from; the view shows a narrative's support (PR #8 thread). The vertex and edge base classes come from the
   same answer.
3. **Chatham House in this mission** *(raised by the ripple sweep)*. The mission asserts the rule in four places
   (Scenarios and architectures, G6, J4, and the non-goal on attribution), while log D-070 makes it one example
   policy in the docs. Bring the mission in line, or keep it?
4. **The Agent's defaults** for Amendment 5, as one item.
5. **The Obsidian projection** *(raised by the chief engineer's play test, 24 Nov)*. The vault as Obsidian shows it
   is hard to use: raw and coded pages duplicate each other, and the layout makes little use of what Obsidian offers.
   Is reshaping the projection in v0.1's scope? The division of labour it serves, in his words: the human coder does
   the interpretive act and validates that meaning is preserved, in Obsidian; the machine does mechanical
   transcription and conformance checking.
6. **A prior-art readout** *(raised with 5)*. Revisit the INCOSE paper's split between AI assistant and human operator,
   the AICC loops and MVC architecture in `ant-rdf` and the eBike prototypes, and the Obsidian-and-git vaults
   delivered to clients, before the projection is redesigned?

Earlier amendments: none open. Every item was resolved through the decision loop and is recorded in
`decisions/log.md`:
- 15 decided by the chief engineer: log D-001, D-003, D-005 to D-008, D-010 to D-014, D-017 to D-019, D-021;
- 1 assigned to the ACE: log D-002;
- 1 deferred by him: the target date, until velocity is known (log D-011, which also decided the timeline method);
- Amendment 4: 1 decided by the chief engineer, log D-060 (a stable machine interface before the first release);
- Amendment 3: 3 decided by the chief engineer, log D-057 (into v0.1; required, with "mixed"; a past/future axis).

Log D-004, D-009, D-012, D-019 and D-020 also record consistency passes. Log D-015 and D-016 were rolled back with
`dev`.
