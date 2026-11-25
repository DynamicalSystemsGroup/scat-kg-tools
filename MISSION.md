# Mission — Scope of work: scat-kg v0.1

| | |
|---|---|
| **Status** | Approved by the chief engineer's merges into `main` of `DynamicalSystemsGroup/scat-kg-tools`. This document is self-standing and always current; its history is the git history of `main`, and the reasoning behind each call is in `decisions/log.md` and the PR threads. |
| **Chief engineer (accountable)** | `mzargham`: final design authority. Approves this mission and its changes, and accepts the v0.1 delivery. |
| **Assistant to the chief engineer (ACE)** | The main Claude session. Manages the team, writes and approves work-package scopes inside this mission, accepts work packages, and escalates only intent gaps (see Governance). |
| **Repositories** | `scat-kg-tools` (the tools, the TBox, the docs site; this document) and `scat-kg-template` (the vault to clone). |
| **Acceptance record** | The chief engineer's merge of the release PRs, as set out under Governance, "Release". |

## Purpose

DSG needs, for an upcoming project, a first usable release of a toolkit for turning facilitated discussions into a
conformant knowledge graph. Participants tell stories (scenarios) and propose architectures. Their field notes are drafted
into narratives, which are coded in pages of an Obsidian vault in git. Coding decompiles each narrative into four concepts:
**s**takeholders, **c**oncerns, **a**ffordances and **t**echnologies. The acronym is SCAT, named for scat singing in
jazz. Coding relates the four concepts through explicit, typed edges, layered as bipartite graphs:
stakeholders–concerns, concerns–affordances, and affordances–technologies.

The result is a navigable, interpretable dataset, and that dataset is the data product. Its conformance to a fixed
ontology is what makes it analysable. It is scaled to a human note-taker: just enough structure to make the data
interpretable, but mostly a formal structure for arranging Obsidian notes. The git repository is the data of record,
and the graph is derived from it.

The practices it supports, eliciting, capturing and coding narratives and holding disagreement without adjudicating
it, were co-developed with Ellie Rennie in the actor-network coding work of `ant-rdf`
(<https://github.com/mzargham/ant-rdf>) as part of the broader AOI
(<https://anthrosource.onlinelibrary.wiley.com/doi/full/10.1111/epic.70009>) research agenda.

The point of departure is the toolchain, and the Obsidian reading and review experience, described in *Formalizing
Document Assurance* (INCOSE IS 2026; the chief engineer has a copy), together with earlier repositories:
- `ant-rdf` (<https://github.com/mzargham/ant-rdf>);
- `knowledgecomplex` (<https://github.com/DynamicalSystemsGroup/knowledgecomplex>);
- `assurances-audits-accountability` (<https://github.com/DynamicalSystemsGroup/assurances-audits-accountability>);
- `concept-definition-stage` (<https://github.com/Open-MBEE/concept-definition-stage>). This one is also a reference
  for the ontology: its SKOS+PROV spine, its definitions traced to their authorities, and its practice of anchoring to
  an external ontology through equivalence axioms instead of importing all of it.

The structure here is simpler than any of them.

v0.1 is aimed at a first field deployment. It is built so that a person can do all of it by hand, and so that an LLM,
where the project's data rights allow one, can take the mechanical work through standard interfaces.

## Core heuristics

- **For the users: "make the right way the easy way".** The right way includes setting clear expectations with
  participants, securing their informed consent, and keeping the commitments made to them.
- **For the builders: "as simple as possible but no simpler".** Hard fought simplicity comes from fit for purpose
  modular architecture, well defined interface contracts, and purposeful components.

When a choice isn't settled elsewhere, these decide it. Over-specifying is a failure too. This mission states intent
and outcomes; how to achieve them is decided in the work packages, by evidence. Design guidance at the end of this
document is advice, not requirement.

**Syntax, semantics and pragmatics.** The ontology's conformance rules are the syntax: they fix which structures can
be expressed. The semantics attach those structures to meaning. The pragmatics are the software, the documentation
and the user guidance. Syntax and semantics decide whether this is a system of representation in which correctly
built models say meaningful things; pragmatics and semantics decide whether meaningful things get said in a real
project. The syntax is packaged away: it is what lets the views (G12) be defined in advance, and users get that
benefit without seeing the full ontology. They just need it to work; the documentation is there if they want more.
They work directly with the two kinds of narrative and the four kinds of vertex, and less directly with the three
kinds of edge.

## Narratives: scenarios and architectures

A **narrative** is one account drawn from the field notes, kept on one page that moves through the status states (G3):
a **stub** has a name and perhaps some metadata; a **draft** holds the account, possibly as plain text with no coding
yet; and it is **done** when it is coded: every concept it names is identified and linked, so it has a valid support,
the coding is conformant, and the coder has judged that it interprets the field notes appropriately. Done is not
frozen: the repository is git, and a narrative can keep evolving. Most
narratives are one of two kinds, which look at the same graph from opposite sides. This is an important heuristic
for facilitating, capturing and coding, though a narrative may be neither.

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
narrative records which it is. Only narratives are marked: stakeholder groups, concerns, affordances and technologies
are not, and the three kinds of edge don't change.

People mix past and future freely when they talk. The facilitation guides lead participants to the past and the
future at separate times in a workshop, and explain the mark with example phrases, including ones that mislead: a
counterfactual "what would happen if" is future, and a habitual "when someone would do x, y happens" is past. A
narrative may be marked **mixed**, the honest record of an account that blurs the two. The mark only tags the
captured narratives, and the guidance on it lives in the facilitation guides alone.

Whether the narrator sees what is told as good, bad or a mix is not recorded in the schema. For anything real a mix is
expected, and it stays in the story's own words. SCAT is pragmatic and thin. It doesn't compete with richer ontologies
such as `ant-rdf`, which cost more and do more analytically: problematization belongs there, and nothing stops the same
case from being coded in both, with different tools.

Calling participants "actors" (users, sponsors and other stakeholders, who tell scenarios) or "technologists"
(researchers, developers and operators, who pitch architectures) is a facilitation device, not a division of people.
Many people are both.

## Facilitation stance: improvisational jazz

SCAT takes its name, and its manner, from scat singing in improvised jazz. Participants can layer in their own
perspectives, even disagreeing ones; we're not litigating truths. Facilitation works by "yes, and" and "from this
perspective": each contribution is taken up and built on, and SCAT is constructed to support semantically disagreeing
perspectives to coexist within data while remaining syntactically correct.

The model **holds disagreement rather than collapsing it.** As in `ant-rdf`, it exposes frictions, gaps and dissenting
views, and it can represent margins of potential conflict. One example is groups that share a concern while their other
concerns are directly opposed. So nobody has to argue anyone into agreement. We capture people's stories and their
proposed architectures. We do not debate which architecture is correct, or which stories should be the focal point
of a design.

## Users and how they work

The v0.1 user codes the data and is accountable for its interpretation. There are two kinds of reader: someone trying
the modelling approach on their own work and data, and an organiser running a facilitated elicitation with
contributors. SCAT is built for the organiser.

The user, a facilitator-analyst, is technically savvy but not a software developer, and works on macOS for v0.1 (see
Governance). They navigate GitHub's web interface, including creating a repository from a template; read, write and
follow links in Obsidian; and follow documentation literally, step by step. They code by one of three paths (G14), and
each has its own user experience:
1. **By hand in Obsidian**, with the tools in an **interactive session**: the Python REPL (`import scat_kg`), with the
   `scat` CLI as an equal path to the same operations and messages. The docs lead with the REPL, because CLI commands
   get long when run through uv. Its future state is an Obsidian community plugin, which is out of scope for v0.1
   (see Non-goals).
2. **Through a chat with an MCP server**, editing in Obsidian. This user must not be required to open a terminal. The docs explain how to
   configure inference.coop, as an example of an OpenAI-API-compatible interface, to use the MCP server.
3. **Through an IDE with agents**, such as Cursor, or VS Code with an agent. The docs point to the skills that help the
   AI coding assistant set itself up.

Whatever the path, the machine does mechanical work only, such as transcription and conformance checking. The interpretive
act, and the check that meaning is preserved, stay with the human coder, in Obsidian.

**The people in the data** are stakeholder **groups**, never individuals. Each vault sets a cap on how many
stakeholder groups it holds, and participants are clustered into groups that fit under it. What participants are told
about how their contributions are used is the event's own agreed policy, decided by the organisers up front and the
same for everyone: for example, the Chatham House rule or personal attribution.

**Three classes of material.** A SCAT project holds three classes of material, each with its own rules for who and
what may touch it, where it is kept, and how far it is released:
- **the inputs:** the supplied materials: the field notes, in whatever form they arrive, which need not follow the
  ontology;
- **the model:** the git repository, holding the narratives at every stage and the full knowledge graph;
- **the analysis:** derivative reports, such as notebooks and documents written with excerpts, data or figures.

The docs present each class's rules as choices, each shown with 2 or 3 reasonable answers that demonstrate the choice
matters without claiming to be exhaustive. No particular project's choices appear as such.

## Goals

- **G1. Fixed TBox.** Designed through G10's research, then fixed for v0.1. Turtle files define:
  - two base classes, from the knowledge-complex pattern at its lowest dimensions: **vertices** (0-simplices) and
    **edges** (1-simplices);
  - the four SCAT vertex classes (Stakeholder group, Concern, Affordance, Technology) and the three edge classes
    between them: Heldby (stakeholder group × concern), Addresses (concern × affordance) and Attributes (affordance ×
    technology). Names may follow an adopted ontology. Each edge between a given pair appears once, and names the
    narratives that refer to it;
  - **narrative**, a base class of its own, outside the vertex and edge pattern, and a page type of its own, one page
    per narrative whose status is its coding state, with scenario and architecture as its subclasses. A narrative's **support** is the subgraph of every vertex and edge it mentions;
  - each record's required and optional fields, including the past, future or mixed mark on every narrative (see
    "Narratives");
  - the other page type: class pages;
  - the linking rules, reflecting how scenarios and architectures differ; a narrative that is neither carries only the
    narrative's own rules;
  - how the graph holds disagreement and margins of potential conflict. At minimum, the same concern can be held by
    different stakeholder groups;
  - one generic **relationship** between two records of the same class: a note with a place in the graph, whose only
    rule is that both ends share a class. It is optional, the tools give it no meaning, and analysis views leave it
    out. No typed links between records of the same class are defined (see Non-goals).
- **G2. Vault ↔ graph.** Markdown pages with YAML frontmatter parse into an ABox that is checked against the TBox.
  Every class has a class page: a description, plus an index table of its instances (name, short description, link)
  that the tools generate from the instance pages.
- **G3. Page lifecycle.** Every content page carries a status, `stub → draft → done`. Class pages are generated, so
  they carry none. For a narrative, `done` means coded (see "Narratives"). The tools create any page the ontology entails that doesn't exist yet, as a `stub`, so the graph is
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
  each coded. Like any others, its stakeholder groups are groups: none stands for one identifiable person. It
  avoids politically loaded illustrations. It doubles as the test fixture and the documentation example.
- **G7. Documentation on GitHub Pages**, from `scat-kg-tools`, with a light musical reference (R-15). It has a page for
  each stage of the journey: getting started, a planning guide, a scenario facilitation guide, an architecture
  facilitation guide and a coding guide, a guide for the chat path, and a short note on the IDE path. It summarises the end-to-end flow on one
  page, makes data storage, rights and consent explicit, and gives a reference for the terms, the Python API and the
  CLI. Each operational choice (participation terms, AI use, where each class of material is kept, who it is released
  to and under what licence, and how commitments to participants are kept) is named as a dependency, with "for
  example" answers and no judgement about which to choose. A short checklist of questions an organiser answers and
  documents before a project starts closes the consent page.
- **G8. Toolchain decided by evidence.** The candidates are tried on a small vault and measured before the
  implementation is locked in:
  - oxigraph;
  - Open Knowledge Format (OKF, <https://github.com/open-knowledge-format/open-knowledge-format>);
  - pydantic;
  - the choice of rule language.

  Each choice is recorded with its evidence.
- **G9. Clear user journeys.** A technically savvy user who isn't a developer can get from the docs site to a new
  repository made from the template, through a working session, to a clean, navigable graph, using only the
  documentation, by the manual path and by the chat path.
- **G10. Ontology by evidence: import, don't mint.** A research sprint surveys existing ontologies for each SCAT class
  and edge. Examples: ISO/IEC/IEEE 42010 for stakeholders and concerns, the SEBoK and INCOSE canon that
  `concept-definition-stage` commits, SKOS and PROV.
  - **Trade study:** for each class, adopt an existing ontology (thinned to what we use, and anchored rather than
    imported whole) or author our own, but only where nothing beats custom.
  - **Coherence:** the result is one coherent ontology, not a patchwork. Every term traces to its source, or is
    recorded as authored, with the reason.
  - **Easy wins:** we take easy wins in expressiveness where they don't complicate the software or the UX.
  - **Disagreement:** how the graph holds disagreement is decided when the TBox is designed, from both this research
    and G11's.
- **G11. Facilitation strategy grounded in research.** The planning and facilitation guides are written from a
  facilitation strategy derived from prior work: `ant-rdf` (its handling of controversy, dissent and multiple
  perspectives), "KOI & The Unicorn" (<https://blog.block.science/koi-and-the-unicorn/>), "Building the Loop" (EPIC
  2025, DOI 10.1111/epic.70009), and recent unpublished grant-proposal drafts from the same collaboration, which the
  chief engineer supplies and which are read for principles only. The strategy covers the improvisational stance,
  eliciting scenarios and architectures, and holding disagreement without adjudicating it.
- **G12. A template analysis notebook.** The template carries a notebook that loads a vault bound to the schema and
  gives the network analysis the project needs, as named views:
  - the **narrative view**: one coded narrative's support (G1), its fingerprint: the vertices and edges it mentions,
    drawn as four columns in class order (group, concern, affordance, technology) with the edges between neighbouring
    columns;
  - the **table views**: each of the three kinds of edge is a bipartite subgraph and so a table, exported as CSV and
    used to generate documents, which is how people navigating the data already think of it;
  - the **composed view**: the four-layer graph that emerges from composing the supports of a set of narratives, up
    to the whole vault, for reasoning about the big picture;
  - **traces**: forward and backward traceability from any vertex through the layers. Tracing a concern goes one
    layer up to the groups that hold it, one down to the affordances that address it, and two down to the
    technologies that provide those affordances. A group traces three layers down to technologies, and a technology
    three layers up to groups.

  Relationships (G1) stay out of the views.
- **G13. Ripple-aware change.** A change to a term, a contract, a rule or this mission reaches every artifact that
  depends on it, in one package, and no two packages edit the same file in turn (see Governance).
- **G14. Three coding paths.** The tools support the three paths in "Users and how they work". None is forced to look
  like another.
  - **By hand in Obsidian** is the base: LLM use is never assumed (R-19).
  - **The chat path** is the priority for design and testing in v0.1. The first field deployment may use one private
    LLM service, inference.coop, through its browser chat, which reaches outside tools only through MCP servers. The
    open-source service is built for it: an MCP server with its tools, prompts and skills, depending on `scat-kg`. A
    workable chat workflow is a UX design problem in its own right: the input material is uploaded to the chat as a
    collection, files are created and downloaded, kept in a private git repository and edited in Obsidian, with
    copying and pasting where it can't be avoided. It is kept simple, and its setup, git and checks work without a
    terminal. A spike designs and tries it with lab material before it is built. Within this path the spike picks the
    technical route to build now (how the chat reaches the tools, and where that service runs), and may document
    another route as the preferred long-term one; R-20 holds either way. inference.coop is the interoperability test
    case: it follows the OpenAI-compatible API standard, so working through it is expected to carry over to other
    providers that follow the same standard, though v0.1 tests no other. Testing with Claude would be cheating, since
    Claude is the development team.
  - **The IDE path** is supported, not the priority.
- **G15. A usable Obsidian projection.** The vault as Obsidian shows it is where the human coder codes and checks that
  meaning is preserved. Each narrative is one page, nothing is duplicated, and the layout uses what Obsidian offers rather
  than folders of near-empty pages. The design may decide which other records are pages and which are fields, and so
  how G2's class pages and G3's stubs are realised, but not what the graph means; narratives stay pages. It is checked in Obsidian itself, not
  reasoned about from the files.
- **G16. A shared architecture.** The system is model, view and control. The **model** is the knowledge graph: the
  TBox and a conformant vault. The **views** are purposeful views built from a conformant model: the Obsidian
  projection, the notebook views and the table views. The **control plane** is how people and LLMs act on the model:
  Obsidian, git and GitHub, the CLI and REPL, the MCP server and the agents in an IDE. One architecture document gives
  this common picture, with the modules, their interface contracts and who is responsible for what. It is planned
  from a prior-art readout and reviewed before detailed design starts.

## Non-goals

- Typed links between records of the same class, such as incompatible concerns, adversarial groups, complementary
  affordances or compatible technologies. They are parked on the feature branch `feature/same-type-edges` as a design,
  not work to build, and nothing in the release refers to them.
- The Obsidian plugin. It stays on its feature branch, `spike/obsidian-plugin`; v0.1 provides the stable interface it builds on (R-16).
- Testing AI assistance against any provider other than inference.coop in v0.1. Broader testing comes later.
- Faces or triangles of any kind, including ones inferred from scenarios and architectures.
- Letting instance repositories extend the TBox, and evolving the TBox after v0.1.
- Checking that named entities are linked, beyond a basic warning.
- The verification, validation and human-signature assurance framework of the INCOSE paper.
- Attributing statements to individuals in the schema. The data records groups; an event's participation terms are
  its own policy, which the docs name without choosing one. How field notes are taken is the facilitator's call.
- Recording the narrator's normative posture (good, bad or mixed) in the schema. It stays in the story's text;
  problematization is for a richer ontology such as `ant-rdf`, applied afterwards.
- Adjudicating between stories or architectures. Neither the tools nor the guides judge which architecture is correct
  or which stories should be focal.
- Analysis tooling beyond the template notebook's views (G12). The earlier analysis spike stays on its branch, `spike/analysis`.
- Legal advice, consent-form templates, or recommended data-use policies.
- Publishing to PyPI.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The TBox in Turtle, in `scat-kg-tools` | G1, G10 |
| D-2 | The tools (parser, checks, the operations, the Python API and CLI, their machine-readable output with its schema, the table views, a public vault loader, and the MCP server with its prompts and skills) with their test suite, and the architecture document, in `scat-kg-tools` | G2, G3, G4, G12, G14, G16 |
| D-3 | The template repository: vault skeleton, class pages, instance configuration (the stakeholder-group cap), the pinned tools, the case study, and the analysis notebook | G5, G6, G9, G12, G15 |
| D-4 | The documentation site on GitHub Pages: a candidate preview during user acceptance, then the release | G7, G9, G11, G14 |
| D-5 | Research readouts and decision records: the ontology survey and trade study, the toolchain spike, the facilitation research, the prior-art readout and the chat-path spike | G8, G10, G11, G14, G16 |
| D-6 | The reviewer's guide for the chief engineer, in the `scat-kg-tools` release PR. It is sized for a person and split into sittings: (1) the end-to-end walkthroughs (UA-M); (2) the docs site; (3) the tools and checks; (4) the ACE's calls. Each sitting has a short checklist and its own entry point. It lists every call the ACE made, with its evidence, and what is known to be weak. | all |
| D-7 | The user-acceptance kit, in `scat-kg-tools/acceptance/`: the AI tester personas and briefs, the report template, every AI test report with its dispositions, and the walkthrough scripts | G9 |

## Requirements

Requirements state outcomes. How each is met is decided in the work packages.

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Conformance checks structure, never content: types, fields, links, names, status, the cap and index freshness. What the content says (tensions, matches, gaps) is for analysis, after conformance passes and the coder signs off the content. Conformance problems are graded: errors block and warnings don't. Errors cover the ontology's constraints (required fields and types, edge endpoints, the linking rules), the stakeholder-group cap, valid status, and links to pages that don't exist. The rule catalogue gives every rule an id and a severity. | Seeded-defect tests, at least one per rule |
| R-2 | Every message names the file, the field or link, and the rule broken (by id). It gives the fix as something a literal reader can apply: an exact command to run, or an exact field and value to write. | Golden-output tests on the seeded defects |
| R-3 | An unfinished page is never an error just for being unfinished. The full contract applies when a page is `done`. Links and edge endpoints are checked at every status. | Tests per status |
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
| R-15 | **A light musical reference, clarity first.** The package and its docs carry the music-note logo and one brief aside on improvisation, where the "yes, and" stance is introduced. Everywhere else, plain words win over any musical reference. | The chief engineer's judgement in UA-M |
| R-16 | **A stable machine interface.** Every result the operations return is also available as versioned, machine-readable data, from the Python API and the CLI alike. Its schema lives with the contracts, and changing it follows a stated versioning rule. A fix is data a tool can apply (what kind of fix it is, the exact command, or the field to write), not only a sentence. This is the interface the MCP server, the Obsidian plugin and any later tool build on. | Every operation's output validated against the schema in tests; a test that the text messages and the data agree |
| R-17 | **The notebook runs.** The template's analysis notebook runs top to bottom on the template's vault. Its narrative view gives, for each coded narrative, exactly its support, with no relationship; its table views export the three edge tables; and a trace from a vertex of each class returns exactly the vertices reachable up and down the layers. | The notebook executed in the template's CI, with tests on the views and the traces |
| R-18 | **Ripple-complete changes.** Before a package that changes a term, contract, rule or this mission is approved, its impact map lists every artifact that refers to what changes, each marked change, keep (with why) or historical. At acceptance, the same sweep finds no reference that is unmarked or still says the old thing. | The impact map in the scope; the sweep's output in the acceptance record |
| R-19 | **Manual first.** Every step, from field notes to coded vault to analysis, can be done by a person by hand, in Obsidian and the CLI, with no LLM. The process stays consistent with ethnographic coding practice, so a project whose data rights rule out AI loses nothing but speed. Any AI assistance is optional, provider-agnostic, and does mechanical work only; the interpretive act stays with the human coder. | The UA-M walkthrough and the docs test, run with no LLM; the ACE's review of each spike readout against it |
| R-20 | **The chat path works, at two test levels.** The MCP server's tools pass automated tests, and the chat path (G14) is run end to end in the inference.coop browser chat at two levels. **Lab:** synthetic material. **Range:** real but predigested material: the public KOI case in `mzargham/ant-rdf`, coded there with the ANT ontology, rebuilt as a SCAT model from its public contents. The field test comes after v0.1 and is not part of this repository. Other providers are not tested in v0.1. | The automated tests in CI; each end-to-end run recorded step by step with screenshots in the acceptance record |
| R-21 | **Coding happens in Obsidian.** A coder can code a narrative and review its support in Obsidian alone, without the same content held on two pages, and without opening pages that carry no content of their own. | A review in Obsidian with screenshots in the record; UA-M |
| R-22 | **Architecture before detailed design.** The architecture document names the model, the views and the control plane, each module's interface contract and responsibilities, and is reviewed by architecture reviewers before any further package starts detailed design. | The review record; the ACE's approval, logged |

## User acceptance

Acceptance is judged by people using the product, not only by tests. It covers two paths: the manual path and the chat
path. The IDE path is tested by the team only.

**The manual journey:**

| Stage | The user | Docs page |
|---|---|---|
| J1 Find | lands on the docs site and understands what it is for and how to start | home |
| J2 Create | on GitHub's web interface, makes a new **private** repository from `scat-kg-template`, then clones it | getting started |
| J3 Set up | installs the prerequisites from exact commands, runs one setup command, gets a working `scat_kg`, and opens the folder as an Obsidian vault | getting started |
| J4 Plan | plans a facilitation event: which sessions elicit scenarios and which elicit architectures, who takes part in each, the participation terms agreed for the event, and stakeholder groups within the cap | planning guide |
| J5 Capture | during the event, records field notes | the two facilitation guides |
| J6 Code | afterwards, in an interactive session (the Python REPL or the `scat` CLI), drafts narratives from the field notes and codes them into SCAT pages and edges, moving pages from stub through draft to done and fixing each problem from its message | coding guide; API and CLI reference |
| J7 Finish | reaches a clean whole-vault check, commits and pushes, and navigates the resulting graph in Obsidian | coding guide |

**The chat journey** is written with the chat path (G14): from the input material uploaded to the chat, through coding
in the chat and in Obsidian, to a clean check of a private repository, with no terminal.

**UA-A, the AI user tests**, run by the team on the candidate before the chief engineer's walkthrough:

- **Personas.** At least three for the manual journey, each written in the user's own words and never the tool's
  vocabulary. **Most run on Haiku**, so the test doesn't depend on much reasoning: if the right way needs reasoning to
  find, it isn't yet the easy way.
  - a facilitator-analyst who is comfortable with a terminal, GitHub and Obsidian but is not a developer (Haiku);
  - a newcomer to Obsidian and the command line, careful and literal (Haiku);
  - the same facilitator-analyst on Sonnet, as a control: a step that Sonnet passes and Haiku fails points to the
    docs or the tools, not the user.

  At least one Haiku tester works in the Python REPL, and at least one uses the CLI. The chat journey has its own
  personas *(default: at least two, most on Haiku)*, who drive the inference.coop browser chat after the chief
  engineer signs in, with lab material only.
- **Setup.** Each manual tester starts in a clean user environment (a fresh home directory, uv not installed), from
  the Pages preview URL, and follows only what the docs say.
  - J2 is simulated with an isolated clone of the template that has its remote removed.
  - The Obsidian steps (J3, J7) are checked through the files. Obsidian itself is covered by UA-M and R-21.
  - Chat testers start from the Pages preview and a private repository made from the template, with no terminal.
  - Each tester codes a small elicitation in a domain of its own, different from the worked example: at least one
    scenario and one architecture, each coded.
- **Reporting.** Testers may not read `src/` or `tests/`, and every claim comes with pasted output or a screenshot. A
  report first answers what style or reference the docs evoke. Then, stage by stage, it says where the tester got
  stuck, what it had to guess, and where the docs left it with nowhere to go.
- **Pass bar.** Every tester, the Haiku testers included, reaches the end of its journey with a clean check. Every
  guess (any action the docs did not literally state) counts as a finding. A finding is **blocking** if it stopped the
  tester short of the end, or if a docs command doesn't work as shown. Every finding is dispositioned: either fixed and
  re-tested by a fresh tester, or accepted with a reason and listed in the reviewer's guide. The final round leaves no
  blocking finding.
- **Void reports.** A report that reuses names from the worked example, or that makes claims without pasted output or a
  screenshot, is void and is run again. A report with no findings is checked by the ACE for plausibility.

**UA-M, the chief engineer's walkthroughs** (the first sitting of the reviewer's guide, and the core of acceptance):

- He runs the manual journey, J1 to J7, himself on the candidate. He starts from the Pages preview, makes a real
  repository through the documented creation path, clones it, sets up, and works through an interactive session with
  the REPL and the CLI, coding a small elicitation of his own choosing. He also runs the chat journey as he would use
  it.
- The walkthrough scripts give each stage's entry point and what "done" looks like, so a session can be split and
  resumed.
- **Pass:** he completes both journeys from the documentation without help, and judges the documentation clear and
  navigable and the journeys clear.
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

- R-1 to R-22 met, with evidence.
- UA-A passes on the candidate, for both journeys.
- The candidate is staged for UA-M, with the reviewer's guide ready.
- The ontology, toolchain, facilitation, prior-art and chat-path readouts exist, and the architecture document is
  reviewed (R-22). Every TBox term traces to an adopted ontology or is recorded as authored, with the trade study's
  reason.

## Definition of done

Good enough is met, and no open item remains. Open items are open decisions, unresolved gaps and blocking findings.
The chief engineer has accepted by merging the release PRs.

## Governance

- **Sign-offs.** The chief engineer signs off on exactly two things: this mission (and every change to it) and the
  acceptance of the delivery. Every other sign-off belongs to the ACE. The ACE approves each work-package scope inside
  this mission, accepts each package against its scope, and logs every ruling in `decisions/log.md`.
- **Changing this mission.** A change is a PR into `main` that edits this document in place, so it always reads as a
  whole; the chief engineer's merge approves it. The PR thread holds the decision records, and the git history is the
  change log.
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
  - the prior-art readout comes before the architecture document, and the reviewed architecture document comes before
    detailed design of any further package (R-22);
  - the user tests come last.
- **TBox changes before release.** Once the TBox and page contracts are accepted, a change to them during v0.1 is the
  ACE's logged call if it serves the mission as written. It is an intent gap if it would change what the graph means.
- **Ripple-aware change.** A change-management consultant, an agent that supports the PM, builds each impact map
  (R-18) before the ACE approves a scope and re-runs the sweep before acceptance. It also keeps the file map of the
  packages in flight: packages whose blast radii overlap are merged or put in order, never run so that one undoes
  another.
- **Constraints set by the chief engineer:**
  - Apache-2.0 licence, copyright Dynamical Systems Group, for code, docs and ontology;
  - adopted ontologies, standards and their definitions are used directly and cited, per engineering practice;
  - private sources are read for principles only, and since the repositories are public, readouts cite only published
    work;
  - no particular project's details, and no personal names beyond published authorship, in the public repositories;
  - no AI attribution on commits, PRs or documents;
  - **Platforms:** macOS is the supported user platform for v0.1, and CI runs on Linux. Nothing may be built in a
    way known to put later Linux or Windows support at risk: no platform-specific paths, shells, line endings or
    tools in the package, and anything unavoidably platform-specific is isolated and recorded.
- **Until the release,** nothing is merged to `main`, tagged or published, with two exceptions:
  - changes to this mission;
  - the **candidate stage** that UA-M needs:
    - the docs site deploys from `dev` to Pages, marked pre-release;
    - `scat-kg-template` is marked as a GitHub template, with `dev` as its default branch;
    - the template pins the tools to the candidate commit.

  Every fix during user acceptance moves the pin, reruns CI, R-6 and R-9, and the ACE decides, and logs, whether
  UA-A reruns.
- **Release.**
  1. The ACE opens one release PR from `dev` to `main` in each repository, and no one else does.
  2. The chief engineer's walkthroughs run against them, and his merges, as merge commits, are the acceptance.
  3. The ACE then tags `v0.1.0` on the merge commit in each repository, redeploys the site from `main` without the
     pre-release mark, and restores `main` as the template's default branch. The template's pin stays on the
     accepted candidate commit, whose content the tag marks.
- **How the team runs** is set out in `ORG.md`.

## Timeline

No date is set; a date waits until velocity has been established. The estimates are lightweight and agile in style:
a heuristic for driving convergence and forecasting, not a schedule fixed in advance, and they are expected to be
noisy at first.
- **Ownership.** The PM owns the timeline. Every unit gets story points when it is planned *(default scale 1, 2, 3, 5,
  8; anything bigger is split)*. An **iteration** is one batch of units that the PM dispatches and lands *(default)*.
- **Velocity.** The board records each iteration's points done and its elapsed wall-clock time, so velocity converts
  to a date. The forecast to the candidate is updated from the measured velocity.
- **What it forecasts.** The forecast runs to **a candidate ready for the chief engineer's review**, including
  testing, the UA-A rounds and the revisions they cause. Time to address his review feedback is estimated later, when
  that feedback exists.

## Design guidance (not binding)

Starting points for the work packages. A package may depart from any of these by recording why.
- **Page creation.** Obsidian page templates suit the narratives, which people write in Obsidian. Vertex and edge
  records are better created by the tools from links in coded narratives, so users never write their structure.
- **Linking severity.** A scenario that links a technology, or an architecture that links a stakeholder group, is
  probably a warning that points to the affordance or the concern, rather than an error.
- **Status strictness.** On a `draft` page, missing required fields are probably warnings.
- **CLI and API.** The CLI is best kept as a thin layer over the Python API, and the MCP server likewise.
- **Private repositories.** A creation link that pre-selects private visibility, or `gh repo create --template …
  --private`, would make private the default.
- **Ambiguous names.** If two pages share a filename, addressing a page by name is ambiguous. The page contracts
  should settle this.
- **Prior art.** Read the earlier work as a way of thinking, not as parts to carry over: a typed formal model kept
  minimal; machine verification and human validation; one model with many views and a control plane per use-context;
  composition with provenance.

## Agent's defaults

Details the ACE settled and the chief engineer approved as a set. The ACE may revise one by a logged call where it
serves this mission as written; a change that would alter the mission goes to the chief engineer.
- Names: `scat-kg-tools`, `scat-kg-template`, the CLI `scat`, the Python package `scat_kg`.
- Python 3.12 or later. The template installs the tools through uv, as a git dependency pinned to a commit.
- Facilitation and coding guides are written once, on the Pages site, and the template links to them.
- Documentation built with MkDocs Material.
- `.python-version` and `uv.lock` are committed. CI runs `uv sync --locked`, `uv lock --check`, ruff (check and
  format) and pytest, and fails on attribution lines.
- Branches: `main` holds approved missions and releases only, `dev` is the integration branch, and work happens on
  short-lived unit branches off `dev`.
- The worked example sets the stakeholder-group cap to 3.
- **The machine interface:** JSON, from `--json` on every `scat` command and an equivalent method on every result in
  Python. Its schema is a JSON Schema file in `contracts/`, with an integer `schema_version`. Adding a field keeps the
  version, and removing or changing one bumps it. Schema validation runs in the test suite only, so it adds no runtime
  dependency to `scat-kg`. Not included: checking an unsaved editor buffer.
- **The past/future mark** is a field on the narrative page.
  Working field name `timeframe`, with the values `past`, `future` and `mixed`. Like every required field (R-3), a missing
  value is an error on a `done` page and a warning before.
- **Links are not edges.** An Obsidian link is a reference in a Markdown file; an edge is a typed fact in the model.
  The tools read the links and decide what they mean, and nothing else does:
  - a link from a narrative to a vertex says the narrative mentions it (coding in place: names are linked where they
    appear, so the account keeps its words);
  - an edge is its own record, naming its two vertices and the narratives that refer to it; a link from a narrative to
    a vertex never creates an edge;
  - the checks hold the two in step: every edge's endpoints have the right classes (R-1), and an edge that names a
    narrative has both its vertices mentioned by that narrative, so a support is always a closed subgraph. A narrative
    that breaks this cannot be `done`.

  The schema-and-projection package settles how edges are written and shown, checked in Obsidian (G15).
- **The relationship** has only the same-class rule; it is never entailed, never required and never in an index's
  required links. Whether it is a page or a field is decided by the projection design (G15). The earlier typed
  `conflicts` link between concerns, and its rule `SCAT-CONFLICT-SELF`, leave the release; existing values migrate to
  relationships.
- **Test edits.** Tests that encode `conflicts`, the old page types or the old layout may change, each change listed
  in the review record.
- **The notebook** reads the vault through the tools' public data (R-16) where it can, through a public vault loader.
- **New dependencies** (the MCP server's, the notebook's) go in optional extras or the template, so `scat-kg`'s core
  runtime dependencies stay as they are.
- **The change consultant** runs on Sonnet as a role in `.claude/agents/`. Its sweep is a written list of search terms
  per change, run with `git grep` over both repositories and the live branches, so the same sweep runs at scoping and
  at acceptance.
- **The chat-path spike** runs on a side branch with its readout in `research/`. The ACE drives the inference.coop
  browser chat after the chief engineer signs in; the agent never enters credentials, and only lab and range material
  (R-20) goes to it. The R-20 end-to-end runs are made on demand, not on every push.
- **Architecture reviewers** are fresh agents, on Sonnet with one on Opus for a named reason (the cross-cutting
  contracts), that review the architecture document before detailed design (R-22).
- **The range vault** rebuilds the KOI case with groups, not named people.
- **Order of work.** WP12 (the terms page) is accepted first. Then the prior-art readout; then the architecture
  document and the chat-path spike, side by side. Then one schema-and-projection package (G1, G15), which absorbs WP13
  (the flow and consent pages) so the shared docs are edited once. Then the views (G12) and the chat path (G14), in the order the
  architecture sets.

## Open decisions (for the chief engineer)

None. Every item was resolved through the decision loop. The decisions are recorded in `decisions/log.md` and in the
threads of the PRs that changed this document.
