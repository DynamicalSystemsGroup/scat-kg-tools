# Mission — Scope of work: scat-tools v0.1

| | |
|---|---|
| **Status** | Approved by the chief engineer's merges into `main` of `DynamicalSystemsGroup/scat-tools`. This document is self-standing and always current; its history is the git history of `main`, and the reasoning behind each call is in `decisions/log.md` and the PR threads. |
| **Chief engineer (accountable)** | `mzargham`: final design authority. Approves this mission and its changes, and accepts the v0.1 delivery. |
| **Assistant to the chief engineer (ACE)** | The main Claude session. Manages the team, writes and approves work-package scopes inside this mission, accepts work packages, and escalates only intent gaps (see Governance). |
| **Repositories** | `scat-tools` (the tools, the ontology, the docs site; this document) and `scat-template` (the vault to clone). |
| **Acceptance record** | The chief engineer's merge of the release PRs, as set out under Governance, "Release". |

## Purpose

DSG needs, for an upcoming project, a first usable release of a toolkit for turning facilitated discussions into a
conformant knowledge graph. Participants tell stories (scenarios) and propose architectures. Their field notes are drafted
into narratives, which are coded in pages of an Obsidian vault in git. Coding decompiles each narrative into four types of node:
**s**takeholders, **c**oncerns, **a**ffordances and **t**echnologies. The acronym is SCAT, named for scat singing in
jazz. Coding relates the nodes through explicit, typed edges, read as three edge tables:
stakeholders–concerns, concerns–affordances, and affordances–technologies.

**What coding is for.** The people at the events provide the details, in their own accounts of their own
experiences. Those details are captured as field notes and organized into narratives, which are then coded. Coding
identifies and interrelates the elements the accounts have in common, organizing many detailed things into an
expression of common patterns: the result is a synthesis. That is why it takes human judgement. Synthesis is
interpretive: recognizing that two things that look different are structurally the same, or that two things that
sound the same are structurally different, takes human intuition. The ontology provides the language for describing
structure, so the person coding can draw out those patterns. The tools never push toward more detail.

The result is a navigable, interpretable dataset, and that dataset is the data product. Its conformance to a fixed
ontology is what makes it analysable. It is scaled to a human note-taker: just enough structure to make the data
interpretable, but mostly a formal structure for arranging Obsidian notes. The git repository is the authoritative copy of the data,
and the knowledge graph is derived from it.

The practices it supports, eliciting, capturing and coding narratives and holding disagreement without adjudicating
it, were co-developed with Ellie Rennie in the actor-network coding work of `ant-rdf`
(<https://github.com/mzargham/ant-rdf>) as part of the broader AOI
(<https://anthrosource.onlinelibrary.wiley.com/doi/full/10.1111/epic.70009>) research agenda.

It builds on the Obsidian reading and review experience described in *Formalizing
Document Assurance* (INCOSE IS 2026; the chief engineer has a copy), together with earlier repositories:
- `ant-rdf` (<https://github.com/mzargham/ant-rdf>);
- `knowledgecomplex` (<https://github.com/DynamicalSystemsGroup/knowledgecomplex>);
- `assurances-audits-accountability` (<https://github.com/DynamicalSystemsGroup/assurances-audits-accountability>);
- `concept-definition-stage` (<https://github.com/Open-MBEE/concept-definition-stage>). This one is also a reference
  for the ontology: its SKOS+PROV spine, its definitions traced to their authorities, and its practice of anchoring to
  an external ontology through equivalence axioms instead of importing all of it.

The structure here is simpler than any of them.

v0.1 is aimed at a first field deployment. It is built so that a person can do all of it by hand, and so that an LLM,
where the project's data rights allow one, can assist the coder through standard interfaces.

## Core heuristics

- **For the users: "make the right way the easy way".** The right way includes setting clear expectations with
  participants, securing their informed consent, and keeping the commitments made to them.
- **For the builders: "as simple as possible but no simpler".** Hard fought simplicity comes from fit for purpose
  modular architecture, well defined interface contracts, and purposeful components.

When a choice isn't settled elsewhere, these decide it. Over-specifying is a failure too. This mission states intent
and outcomes; how to achieve them is decided in the work packages, by evidence.

**Syntax, semantics and pragmatics.** The ontology's conformance rules are the syntax: they fix which structures can
be expressed. The semantics attach those structures to meaning. The pragmatics are the software, the documentation
and the user guidance. Syntax and semantics decide whether this is a system of representation in which correctly
built models say meaningful things; pragmatics and semantics decide whether meaningful things get said in a real
project. The syntax is packaged away: it is what lets the views (G12) be defined in advance, and users get that
benefit without seeing the full ontology. They just need it to work; the documentation is there if they want more.
They work directly with narratives (mostly scenarios and architectures) and the four node types, and less directly
with the three edge types.

## Words

This project uses each word in one sense, defined in [`GLOSSARY.md`](GLOSSARY.md), which also maps each plain word,
once, to the formal concept it stands for and its source. This mission, every scope of work, the contracts, the code
and the docs use the glossary's words in its senses (see Governance, "The glossary").

## Narratives: scenarios and architectures

A **narrative** is one account drawn from the field notes, kept on one page that moves through the three statuses (G3):
a **stub** has a name and perhaps some metadata; a **draft** holds the account, possibly as plain text with no coding
yet; and it is **done** when it is coded: every edge it tells is recorded in its table, the table being the coding of record, so it has a
valid fingerprint (G1), the coding is conformant, and the coder has judged that it interprets the field notes appropriately. Links in the
account's prose are optional; those it has name only nodes its table holds. Setting
`done` is the coder's attestation of that judgement; the tools check only the structure. Done is not
frozen: the repository is git, and a narrative can keep evolving.

**The coding loop.** The coder works each narrative round a loop: interpreting the field notes, authoring the
narrative, coding it, and reviewing it, until in reviewing they confirm that the narrative is aligned with the field
notes and that the coding is a correct use of SCAT, both in their interpretation. When the tool's check passes and the coder confirms both, they set the narrative to `done`. It is the coder interpreting and coding even when the work is machine-aided. **Synthesising** comes after, across
narratives: consolidating codes, so that what is structurally the same is one node and what is structurally different
is two. **Analysing** comes last: it generates the views, and the reading of the views can send the work back to
synthesis, or to a narrative and round the loop again.

**A finished model.** The exercise is finished when four things hold: the knowledge graph is conformant, the vault is
navigable in Obsidian, the views are generated, and the coder who interpreted the field notes states that the model
is a good representation of what those notes contain. That statement is made outside the tool, the way work is
handed over: the coder decides the model is finished, locks a version, and hands it over, as in a contract delivery, a
paper submission or a class project hand-in. Locking a version means tagging a commit in git: with `git tag` on the manual path,
and with GitHub's own features (a GitHub Release, or GitHub Desktop) on the chat path.
A project may have several co-authors and peer reviewers, like a paper; git records who coded what, and the
statement is made by any one of them, by the project's own rule. SCAT adds nothing of its own for this.

Most narratives are one of two types, which look at the same knowledge graph from opposite sides. This is an important heuristic
for facilitating, capturing and coding, though a narrative may be neither.

- **Scenarios are behavioural.** They tell the story of people within an action situation doing things, through which
  outcomes and consequences are wrought. They are temporal. Technologies are part of the action situation but not
  the focus: they stay relatively fixed and out of view, and what is legible is their **affordances**. A coded
  scenario relates stakeholders, concerns and affordances.
- **Architectures are structural.** They formulate assemblages: parts and wholes, and how parts are assembled into
  tools that provide affordances which address concerns. Stakeholders are largely abstracted away. What is addressed
  is concerns, and the same concern can arise from different stakeholders; an architecture can't presume which
  stakeholders will adopt it. A coded architecture relates concerns, affordances and technologies.

A second lens cuts across the first: the **claim type**. An account may tell what is actual, facts about the world
that could be independently verified, or what is hypothetical, what people are only conjecturing. Accounts can't be
forced into these buckets, so a narrative may stay **unclassified**, the default. Kind (scenario or architecture) and
claim type are marks on narratives only, used as filters in the analysis views; neither gates any status, and no tool
changes its output because of one unless a person filters by it. Stakeholders, concerns, affordances and technologies
are not marked, and the three edge types don't change. The planning and facilitation guides steer the capture along
both lenses, to get more interpretable data.

Whether the narrator sees what is told as good, bad or a mix is not recorded in the ontology. For anything real a mix is
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
views, and it can represent margins of potential conflict. One example is stakeholders that share a concern while their other
concerns are directly opposed. So nobody has to argue anyone into agreement. We capture people's stories and their
proposed architectures. We do not debate which architecture is correct, or which stories should be the focal point
of a design.

## Users and how they work

The v0.1 user codes the data and is accountable for its interpretation. There is one persona, the **organiser** of a
facilitated elicitation with contributors, and the design is aware of the adoption lifecycle: an organiser first tries
the tools alone, on their own work and data, to decide whether to use them, and someone who cannot make it work solo
will never commit to it for a facilitated project. So trying it solo is a stage of the organiser's journey, not a
separate user, and the docs make that first try easy.

The organiser is also the **coder** of the data. They are technically savvy but not a software developer, and works on macOS for v0.1 (see
Governance). They navigate GitHub's web interface, including creating a repository from a template; read, write and
follow links in Obsidian; and follow documentation literally, step by step. They code by one of four paths (G14), and
each has its own user experience and a walkthrough with screenshots:
1. **By hand in Obsidian**, with the tools in an **interactive session**: the Python REPL (`import scat_tools`), with the
   `scat` CLI as an equal path to the same operations and messages. The docs lead with the REPL, because CLI commands
   get long when run through uv. Its future state is an Obsidian community plugin, which is out of scope for v0.1
   (see Non-goals).
2. **Through an AI chatbot with an MCP server**, editing in Obsidian. A technical helper sets the path up once; from
   then on, the coder needs no terminal. The walkthrough's example is Claude. **Leave no trace** is an option of this path for a strict
   data policy; its example is inference.coop, an OpenAI-API-compatible interface.
3. **Through an AI IDE with agents**. The docs describe it briefly, by the standards the tools adopt (MCP, the skill,
   the machine interface), and point to the skill that helps the AI coding assistant set itself up.
4. **Through a local LLM**, running on the organiser's own machine. The docs describe it briefly, by the same
   standards; it suits a project that keeps its material local.

The chatbot path's walkthrough uses Claude, and its leave-no-trace option uses inference.coop, so no tool is favoured.
Full walkthroughs for the IDE and local-LLM paths are future work, tracked as issues.

**Actant types.** Borrowed from actor-network theory and mostly in the background, three types of actant decide what
can edit what, whatever the path:
- the **human user**: every person, whatever their role. A human user owns interpretation: they look at the Markdown
  in Obsidian and confirm that it represents their coding;
- the **CLI tools** (the Python package and its front ends) own conformance, with two jobs: (i) the knowledge graph
  matches the Markdown, and (ii) the knowledge graph conforms to the ontology;
- the **AI assistant** (an LLM, where the project allows one) helps produce and review the text in the Markdown,
  drafting narratives from the field notes included, and helps drive the tools' calls. It decides nothing.
The human user and the CLI tools are required; the AI assistant is not. Without it, nothing is lost but speed.

**Roles.** A second axis, for planning. People hold roles, roles are responsible for activities, and activities occur
in the stages of the project lifecycle (G18). The **organiser** is one person, accountable for the whole project: that
every activity is completed, that the report is produced, and that the promises made on data use, release, retention
and attribution are kept. The other roles may each have several people: participant liaison, setup person, event
coordinator, facilitator, note-taker, coder and analyst. A person may hold several roles, and the organiser often does.
The roles are planning guidance that helps the organiser assemble the people the lifecycle needs.

**The people in the four layers** are **stakeholders**: collectives, never individuals. Where the vault's attribution mode
enables it, contributor pages name the people a narrative is attributed to, outside the four layers. **Caps** bound the
scale: planning sets an expected upper bound on how many nodes each layer holds, and setup writes them into the vault.
A cap is an upper bound that encourages synthesis, never a target; fewer nodes is better, and going over a cap is a
warning, not an error. What participants are told
about how their contributions are used is the event's own agreed policy, decided by the organisers up front and the
same for everyone: for example, the Chatham House rule or personal attribution.

**Three kinds of material.** A SCAT project holds three kinds of material (inputs, model, analysis), each with its own rules for who and
what may touch it, where it is kept, and how far it is released:
- **the inputs:** the supplied materials: the field notes, in whatever form they arrive, which need not follow the
  ontology;
- **the model:** the git repository, holding the narratives at every stage and the full knowledge graph;
- **the analysis:** derivative reports, such as notebooks and documents written with excerpts, data or figures.

The docs present each kind's rules as choices, each shown with 2 or 3 reasonable answers that demonstrate the choice
matters without claiming to be exhaustive. No particular project's choices appear as such.

## Goals

- **G1. A fixed ontology**, fixed for v0.1. In Turtle, it defines:
  - nodes and edges as its two base types, the lowest dimensions of the knowledge-complex pattern (see the glossary);
  - the four node types (stakeholder, concern, affordance, technology) and the three edge types between
    neighbouring layers: holds (stakeholder → concern), is addressed by (concern → affordance) and is provided by
    (affordance → technology). These are plain readings; the ontology's own names may follow an adopted ontology, and
    the docs map each reading to its name. Each edge between a given pair appears once, and
    names the narratives that tell it;
  - that a link is not an edge: a narrative's table is the coding of record. A link in the account's prose is
    optional, names only a node the table holds, and never creates an edge;
  - **narrative**, a type outside the layered graph and a page type of its own, one page per narrative whose status
    records how far its coding has got, with scenario and architecture as its subtypes. A narrative's **fingerprint**
    is the nodes it links plus the edges that name it. A fingerprint is **valid** when every edge that names the
    narrative has both its nodes linked by it. A fingerprint may be disconnected; a `done` narrative whose fingerprint
    has no edges gets a warning, not an error, so the coder confirms it was intended;
  - each entry's required and optional fields, including the kind and claim-type marks on narratives (see
    "Narratives");
  - index pages, which the tool generates;
  - how the graph holds disagreement and margins of potential conflict. At minimum, the same concern can be held by
    different stakeholders;
  - one generic **relationship annotation** between two entries of the same type: a free-text remark with a place in
    the vault, whose only rule is that both ends share a type. It is optional, the tool gives it no meaning, and the
    views leave it out. No typed edges between nodes of the same type are defined (see Non-goals).
- **G2. Vault ↔ knowledge graph.** Markdown pages with YAML frontmatter are read into the knowledge graph, which is checked
  against the ontology. Every type has an index page: a description, plus a table of its entries (name, short
  description, link) that the tool generates from the entries' pages.
- **G3. Entry lifecycle.** Every entry carries a status, wherever it is stored, `stub → draft → done`. Index pages are
  generated, so they carry none. For a narrative, `done` means coded (see "Narratives"); for a node or edge, its
  required fields and links, as the ontology's linking rules set them, are complete and the coder has signed it off; for a relationship annotation, its two ends exist and share a type. The tools create any page the ontology entails that doesn't exist yet, as a `stub`, so the graph is
  never incomplete, only unfinished.
- **G4. Operations**, in the Python API and the `scat` CLI, usable in an interactive session:
  - check conformance at three scopes: one page, the page with every page one link away in either
    direction, and the whole vault;
  - read status at the same three scopes, and set a page's status;
  - regenerate the index pages;
  - create entailed missing pages as stubs;
  - record an edge, and remove one, so neither the coder nor the assistant hand-writes its structure (R-11);
  - merge two node pages of the same type into one synthesized node, with a plan shown first (git keeps the history);
    narratives already done stay done and are listed;
  - rename a node page, rewriting every link and row that names it, and show every place a node is used.

  Optional slots hold notes without adding required structure: a row's note, the relationship annotation, and an
  optional page for one narrative's use of one node.

  The one-page and one-link-away checks act as a fast linter during working sessions.
- **G5. Two repositories.** `scat-tools` is a slim, separately maintained package with the ontology, the tools and the
  docs site. `scat-template` is the vault to clone, which installs a pinned version of the tools. Both builds are
  reproducible with uv.
- **G6. The worked example is this project, as its own case study.** The template's example content is the
  elicitation of scat-tools itself, drawn from the chief engineer's recorded statements and the decision log. It is small,
  because users overwrite it, but every node type and edge type has 2–3 entries, and there are two scenarios and two architectures,
  each coded. Like any others, its stakeholders are collectives: none stands for one identifiable person. It
  avoids politically loaded illustrations. It doubles as the test fixture and the documentation example.
- **G7. Documentation on GitHub Pages**, from `scat-tools`, with a light musical reference (R-15). It has a page for
  each stage of the journey (J1–J10): getting started, a planning guide with the roles, a scenario facilitation guide,
  an architecture facilitation guide, a page on narratives and their marks, a coding guide, a synthesis guide on
  patterns and abstraction, an analysis guide, and a page on the coding paths (a walkthrough for by hand and for the AI
  chatbot with its leave-no-trace option; the AI IDE and local LLM described briefly by the standards adopted). Its
  navigation follows the lifecycle's stages, and each activity names its stage and the role that does it. A person in
  a role reads only what their activities need. It previews on localhost from a clone of the repository. It summarises the end-to-end flow on one
  page, makes data storage, rights and consent explicit, and gives a reference for the terms, the Python API and the
  CLI. Each operational choice (participation terms, AI use, where each kind of material is kept, who it is released
  to and under what licence, and how commitments to participants are kept) is named as a dependency, with "for
  example" answers and no judgement about which to choose. A short checklist of questions an organiser answers and
  documents before a project starts closes the consent page.
- **G8. The toolchain.** The tools are plain Python 3.12 or later: pydantic models generated from, or held equal to,
  the ontology's Turtle (read with rdflib), and Markdown with YAML frontmatter read with PyYAML. There is no graph store
  and no second rule language. Builds are reproducible with uv, the docs site is MkDocs Material, the drawings are an
  optional extra (matplotlib), and the MCP server is an optional extra on the MCP Python SDK.
- **G9. Clear user journeys.** A technically savvy user who isn't a developer can get from the docs site to a new
  repository made from the template, through a working session, to a clean, navigable vault, using only the
  documentation, by the manual path and by the chat path.
- **G10. An ontology that imports rather than mints.** The ontology is one SKOS spine with authored SCAT terms, each
  anchored to the established vocabulary it stands for (for example ISO/IEC/IEEE 42010 and the SEBoK for stakeholders
  and concerns) by `skos:closeMatch`, never imported whole. It is one coherent model, not a patchwork, and the docs
  give each term's source, or say it is authored and why.
- **G11. Facilitation grounded in prior work.** The planning and facilitation guides follow a strategy drawn from
  `ant-rdf` (its handling of controversy, dissent and multiple perspectives), "KOI & The Unicorn"
  (<https://blog.block.science/koi-and-the-unicorn/>) and "Building the Loop" (EPIC 2025, DOI 10.1111/epic.70009): the
  improvisational stance, eliciting scenarios and architectures, and holding disagreement without adjudicating it.
- **G12. A template analysis notebook.** The template carries a notebook that loads a conformant vault and
  gives the network analysis the project needs, as named views:
  - the **fingerprint view**: one coded narrative's fingerprint (G1), drawn as four columns in layer order (stakeholder,
    concern, affordance, technology) with the edges between neighbouring columns;
  - the **edge tables**: each of the three edge types as a table, exported as CSV and used to generate documents, which
    is how people navigating the data already think of it;
  - the **layered view**: the union of the fingerprints of a chosen set of narratives, up to the whole vault, drawn as
    the four layers,
    for reasoning about the big picture;
  - **traces**: following edges from any node up or down the layers. Tracing a concern goes one layer up to the stakeholders
    that hold it, one down to the affordances that address it, and two down to the technologies that provide those
    affordances. A stakeholder traces three layers down to technologies, and a technology three layers up to stakeholders;
  - the **recurrence view**: how many narratives, and how many stakeholders' accounts, reach each node and edge,
    singletons marked. A pattern is what recurs.

  Relationship annotations (G1) stay out of the views.
- **G13. Ripple-aware change.** A change to a term, a contract, a rule or this mission reaches every artifact that
  depends on it, in one package, and no two packages edit the same file in turn (see Governance).
- **G14. Four coding paths.** The tools support the four paths in "Users and how they work". None is forced to look
  like another.
  - **By hand in Obsidian** is the base: LLM use is never assumed (R-19).
  - **The chat path** is the priority in v0.1. **SCATLAB**, a macOS menu-bar app, runs the MCP server on the coder's own
    machine in a container (Colima), reachable by the chat through a Tailscale Funnel address, with a session key kept
    in the keychain. The server offers the tools, prompts and skill, and generates the views (G12) from the same code
    the notebook uses. Field notes go to the chat as a collection; files are created and downloaded, kept in a private
    git repository through GitHub Desktop and edited in Obsidian, so after a technical helper's one-time setup the
    coder needs no terminal. MCP on governed compute is the preferred route after v0.1. inference.coop is the
    interoperability case: it follows the OpenAI-compatible API standard, so what works there carries over to other
    providers that follow it. The chatbot walkthrough uses Claude, and the leave-no-trace option uses inference.coop.
  - **The IDE path** is supported, not the priority. The docs describe it by the standards the tools adopt; a full
    walkthrough is future work.
  - **The local-LLM path** is supported, not the priority, described the same way; a full walkthrough is future work.
- **G15. A usable Obsidian layout.** The vault as Obsidian shows it is where the coder codes and checks that meaning is
  preserved. Each narrative is one page holding its account and its `Edges told` table; each node is a page in its
  layer's folder; each type has an Obsidian Base index page the tool generates. Nothing is duplicated, and edges are
  rows, not pages.
- **G16. A shared architecture.** The system is model, view and control. The **model** is the ontology plus a
  conformant vault. The **views** are purposeful views built from a conformant model: the Obsidian layout, the
  fingerprint view, the edge tables, the layered view, traces and the recurrence view. The **control plane** is how
  people and LLMs act on the model: Obsidian, git and GitHub, the CLI and REPL, the MCP server and the agents in an IDE,
  with the CLI and the MCP server as thin layers over the Python API. The architecture document gives this picture,
  with the modules, their interface contracts and which actant type may do what.

- **G17. The table is the coding of record (a known pitfall).** Much of the coding appears in two forms: "this page
  references that page" in Obsidian, and "this node is connected to that node" in the knowledge graph. The table of
  edges a narrative tells is the coding of record; it is structural, and it is what the knowledge graph is held in step
  with. The account's prose is interpretive, connective tissue: linking it is desired but not required, and the nodes it
  links are a subset, possibly empty, of the nodes its table holds. If something is linked, it belongs in the table or
  it should not be linked. Coding is incremental: stub, fill in, stub further, fill in again, breadth first for some
  people and depth first for others. The tool makes each step's mismatches visible with a fix: a warning while a
  narrative is a draft, an error once it is `done`.
- **G18. A project lifecycle.** A SCAT project moves through six stages: plan, capture, code, synthesise, analyse and
  report. Each stage names its work, what it needs, what it may produce and who decides each move out of it; the stage
  is recorded in the vault, and every path (the CLI, the MCP server, the IDE) respects it at the same strength. A
  stage is a project's state; a page's status (stub, draft, done) is a different, smaller state machine. The lifecycle
  is the scaffolding that breaks the work into simple pieces and keeps an assistant's behaviour stable, and every
  activity in the docs is located in one stage, with the role that does it.

## Non-goals

- Typed edges between nodes of the same type, such as incompatible concerns, adversarial stakeholders, complementary
  affordances or compatible technologies. They are parked on the feature branch `feature/same-type-edges` as a design,
  not work to build, and nothing in the release refers to them.
- The Obsidian plugin. It stays on its feature branch, `spike/obsidian-plugin`; v0.1 provides the stable interface it builds on (R-16).
- Testing AI assistance in v0.1 beyond the R-20 runs and one run of each path's walkthrough with its example provider
  (D-148). Broader testing comes later.
- Faces or triangles of any sort, including ones inferred from scenarios and architectures.
- Letting a project's own repository extend the ontology, and evolving the ontology after v0.1.
- Checking that pages named in a page's text are linked, beyond a basic warning.
- The verification, validation and human-signature assurance framework of the INCOSE paper.
- Mixing attribution modes in one vault. A vault runs in exactly one **attribution mode**, set by the organiser at
  set-up and known to the tools: **attribution required** (every narrative names its contributors), **attribution
  optional**, or **attribution disallowed** (no narrative names a contributor; the Chatham House rule is this mode).
  The modes are disjoint: the tools refuse attribution in a disallowed vault and do not let modes bleed together in
  use. The four layers (stakeholders, concerns, affordances, technologies) record collectives, never individuals. Where the mode
  enables attribution, each contributor has a page outside the four layers, and a narrative's attributed-to links
  resolve to those pages. How field notes are taken is the facilitator's call.
- Recording the narrator's normative posture (good, bad or mixed) in the ontology. It stays in the story's text;
  problematization is for a richer ontology such as `ant-rdf`, applied afterwards.
- Adjudicating between stories or architectures. Neither the tools nor the guides judge which architecture is correct
  or which stories should be focal.
- Analysis tooling beyond the views of G12. The earlier analysis spike stays on its branch, `spike/analysis`.
- Legal advice, consent-form templates, or recommended data-use policies.
- A mechanism of SCAT's own for signing off a finished model, or for authorship and review across coders; git and
  GitHub provide it.
- Publishing to PyPI.
- Knowledge-graph tooling for planning: the roles, data policies, event logistics, format and agenda. The docs are
  written so that it can be added later without a refactor.
- Full walkthroughs for the AI IDE and local-LLM paths; they are tracked as issues.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The ontology in Turtle, in `scat-tools` | G1, G10 |
| D-2 | The tool (parser, checks, the operations, the Python API and CLI, their machine-readable output with its schema, a public vault loader, and the view generation the notebook and the MCP server share), and the MCP server with its prompts and skills, with their test suite, and the architecture document, in `scat-tools` | G2, G3, G4, G12, G14, G16, G17 |
| D-3 | The template repository: vault skeleton, index pages, the vault's configuration (the caps, the attribution mode), the starting stage, the pinned tools, the case study, the analysis notebook, and a setup skill for IDE agents | G5, G6, G9, G12, G14, G15 |
| D-4 | The documentation site on GitHub Pages: a candidate preview during user acceptance, then the release | G7, G9, G11, G14, G17 |
| D-5 | The decision records, and the research readouts behind the choices this mission states as settled | G8, G10, G11, G13, G14, G16 |
| D-6 | The reviewer's guide for the chief engineer, in the `scat-tools` release PR. It is sized for a person and split into sittings: (1) the end-to-end walkthroughs (UA-M); (2) the docs site; (3) the tools and checks; (4) the ACE's calls. Each sitting has a short checklist and its own entry point. It lists every call the ACE made, with its evidence, and what is known to be weak. | all |
| D-7 | The user-acceptance kit, in `scat-tools/acceptance/`: the AI tester personas and briefs, the report template, every AI test report with its dispositions, and the walkthrough scripts | G9 |

## Requirements

Requirements state outcomes. How each is met is decided in the work packages.

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Conformance checks structure, never content: types, fields, links, names, status, the cap and whether index pages are up to date. What the content says (tensions, matches, gaps) is for analysis, after conformance passes and the coder signs off the content. Conformance problems are graded: errors block and warnings don't. Errors cover the ontology's constraints (required fields and types, the ends of edges, the linking rules), valid status, and links to pages that don't exist; going over a layer's cap is a warning. Each rule has one id, and its severity follows the page's status where it depends on it. The rule catalogue gives every rule an id and a severity. | Seeded-defect tests, at least one per rule |
| R-2 | Every message names the file, the field or link, and the rule broken (by id). It gives the fix as something a literal reader can apply: an exact command to run, or an exact field and value to write. | Golden-output tests on the seeded defects |
| R-3 | An unfinished page is never an error just for being unfinished. The full contract applies when a page is `done`. Links and the ends of edges are checked at every status; R-23 sets when a mismatch between links and edges is an error. | Tests per status |
| R-4 | Checks never write to the vault. Every write is an explicit operation (index, stub, set status). | Tests that snapshot the vault before and after each operation |
| R-5 | The checks are fast enough to work as a linter. On a laptop, with a 500-page vault: one page under 1 s, a page with the pages one link away under 2 s, the whole vault under 5 s *(ACE's thresholds)*. | Benchmark over a generated 500-page vault |
| R-6 | On the manual path, starting from a clean user environment with only the documented prerequisites: a fresh clone of the template, then one documented setup command, after which `check` on the whole vault passes on the worked example. | Clean-environment trial |
| R-7 | Both repositories commit `uv.lock`, and CI runs the tests and checks on every push. | CI runs |
| R-8 | The Python REPL and the `scat` CLI are equal paths: every operation is available on both, with the same messages. The docs lead with the REPL and show the CLI equivalent alongside it. | Tests on both paths; the docs test runs both |
| R-9 | Every snippet and command shown in the docs runs as shown, and the CLI reference matches `--help`. | A docs test that extracts and runs them; a reference diff |
| R-10 | The docs site has no dead ends or broken links. Every journey page says what you need before you start and where to go next. | Strict build and link check; the ACE's browser pass over every page, at desktop and phone width |
| R-11 | **Make the right way the easy way.** There is one obvious way to create each kind of page, and users never hand-write structure the tools can generate. Each journey page leads with the one action to take next. | The Haiku testers' reports; the ACE's review |
| R-12 | Repositories made from the template are private by default, and the docs and the template's README recommend private repositories. | A probe of the documented creation path on the candidate; UA-M |
| R-13 | The ontology has one source, which is authoritative; any other form the tools use is generated from it or held equal to it by a test. | The generator or the equality test, in CI |
| R-14 | The planning and facilitation guides carry the improvisational stance ("yes, and"; "from this perspective"). They contain no step that ranks, votes on or adjudicates between stories or architectures. | The ACE's review of the guides; UA-M |
| R-15 | **A light musical reference, clarity first.** The package and its docs carry the music-note logo and one brief aside on improvisation, where the "yes, and" stance is introduced. Everywhere else, plain words win over any musical reference. | The chief engineer's judgement in UA-M |
| R-16 | **A stable machine interface.** Every result the operations return is also available as versioned, machine-readable data, from the Python API and the CLI alike. Its schema lives with the contracts, and changing it follows a stated versioning rule. A fix is data a tool can apply (what kind of fix it is, the exact command, or the field to write), not only a sentence. This is the interface the MCP server, the Obsidian plugin and any later tool build on. | Every operation's output validated against the schema in tests; a test that the text messages and the data agree |
| R-17 | **The notebook runs.** The template's analysis notebook runs top to bottom on the template's vault. Its fingerprint view gives, for each coded narrative, exactly its fingerprint, with no relationship annotation; it exports the three edge tables; and a trace from a node of each type returns exactly the nodes reachable up and down the layers. | The notebook executed in the template's CI, with tests on the views and the traces |
| R-18 | **Ripple-complete changes.** Before a package that changes a term, contract, rule or this mission is approved, its impact map lists every artifact that refers to what changes, each marked change, keep (with why) or historical. At acceptance, the same sweep finds no reference that is unmarked or still says the old thing. | The impact map in the scope; the sweep's output in the acceptance record |
| R-19 | **Manual first.** Every step, from field notes to coded vault to analysis, can be done by a person by hand, in Obsidian and the REPL or CLI, with no LLM. The process stays consistent with ethnographic coding practice, so a project whose data rights rule out AI loses nothing but speed. Any AI assistance is optional and provider-agnostic, and decides nothing: a human user owns interpretation and the CLI tools own conformance (see "Actant types"). | The UA-M walkthrough and the docs test, run with no LLM; the ACE's review of each package against it |
| R-20 | **The chat path works, at two test levels.** The MCP server's tools pass automated tests, its views equal the notebook's on the same vault, and the chat path (G14) is run end to end in the inference.coop browser chat at two levels. **Lab:** synthetic material. **Range:** real but predigested material: the public KOI case in `mzargham/ant-rdf`, coded there with the ANT ontology, rebuilt as a SCAT model from its public contents, which stand in for field notes. The field test comes after v0.1 and is not part of this repository. Beyond these runs, v0.1 runs the chatbot walkthrough with Claude and its leave-no-trace option with inference.coop. | The automated tests in CI; each end-to-end run recorded step by step with screenshots in the acceptance record |
| R-21 | **Coding happens in Obsidian.** A coder can code a narrative and review its fingerprint in Obsidian alone, without the same content held on two pages, and without opening pages that carry no content of their own. | A review in Obsidian with screenshots in the record; UA-M |
| R-22 | **The architecture document is current.** It names the model, the views and the control plane, each module's interface contract and responsibilities, and what each actant type may do, and it changes in the same package as the code it describes. | The ACE's review at each package acceptance |
| R-23 | **Links and edges reconcile.** A narrative's table is the coding of record, and the nodes its account links must be nodes its table holds; a row end need not be linked in the account. The tool detects each mismatch and gives a fix that reconciles it. A mismatch is a warning while the narrative is a draft and an error once it is `done`. Incremental coding, breadth first or depth first, never leaves a mismatch the tool can't see. The docs show both ways of working. | Tests that generate vaults with mismatches and check each mismatch is reported with a working fix; a named architecture reviewer for this area; a UX review in Obsidian of an incremental coding session, with screenshots |

## User acceptance

Acceptance is judged by people using the product, not only by tests. It follows the organiser's whole journey, from
first hearing of SCAT to handing over a finished model, on the manual path and on the chat path. The IDE path is
tested by the team only.

**The journey:**

| Stage | The organiser | Docs page |
|---|---|---|
| J1 Discover | finds the docs site or the repository, understands what SCAT is for, and gets interested | home |
| J2 Try | tries it alone, on their own work and data: sets up, codes one narrative from their own notes, sees its fingerprint in Obsidian, and sets it `done` | getting started; the solo trial |
| J3 Decide | decides to use SCAT to organise a facilitated elicitation | the flow |
| J4 Set terms | makes and documents the up-front decisions and assumptions: participation terms, AI use, how each kind of material is kept and released, and the commitments made to participants | data, rights and consent; the "Before you start" checklist |
| J5 Set up | on GitHub's web interface, makes a new **private** repository from `scat-template`, clones it, installs the prerequisites from exact commands, runs one setup command, gets a working `scat_tools`, and opens the folder as an Obsidian vault | getting started |
| J6 Plan | plans one or more facilitation events: which sessions elicit scenarios and which architectures, who takes part in each, the participation terms, the roles, and the caps on each layer | planning guide |
| J7 Capture | at each event, records field notes | the two facilitation guides |
| J8 Code | works each narrative round the coding loop (interpreting, authoring, coding, reviewing) in an interactive session (the Python REPL or the `scat` CLI) and in Obsidian, fixing each problem from its message, until it is `done` | coding guide; API and CLI reference |
| J8b Synthesise | consolidates the codes across narratives: reviews possible duplicates, merges and renames nodes, and writes each node page's definition, so that what is structurally the same is one node | synthesis guide |
| J9 Analyse | generates the views, interprets them, and goes back round the coding loop where they send it | analysis guide; the notebook |
| J10 Hand over | reaches a clean whole-vault check with the views generated and the vault navigable in Obsidian, commits and pushes, decides the model is finished, locks a version and hands it over. A hand-over is a release: work can continue after it, toward the next | coding guide |

J1 and J2 are the **solo trial**: short enough for one sitting, because an organiser who can't make the tools work
alone won't adopt them. J2 runs on the manual path *(default)*.

**The chat journey** follows the same stages, J1 to J10, with the chat path (G14) in place of the interactive session
from J5 on: the field notes uploaded to the chat as a collection, the coding loop in the chat and in Obsidian, views
generated through the MCP server, and a clean check of a private repository, then the hand-over, all with no terminal.

**UA-A, the AI user tests**, run by the team on the candidate before the chief engineer's test:

- **By role.** There is one tester per role (see "Users and how they work"). No tester tries to make sense of
  everything in the docs. What each reads, what it tries to do, and whether it is satisfied with what it finds follow
  from its role's activities in their stages. **Most run on Haiku**, so the test doesn't depend on much reasoning: if
  the right way needs reasoning to find, it isn't yet the easy way.
- **Through the user interfaces, as a person would.** Humans are visual. A tester reads the docs site in a browser,
  hosted on localhost from a fresh clone, and clicks through it; uses the tools in their user interfaces: Claude and
  inference.coop in the browser, Obsidian on the desktop, the menu-bar app and, where its role's docs say so, a
  terminal; and follows only what the docs say. Reading the code instead of using the interfaces is not user
  acceptance. The roles that code do so on the manual
  path and on the chat path, at least once each, each with material in a domain of its own, different from the
  worked example.
- **Reporting.** Testers may not read `src/` or `tests/`, and every claim comes with a screenshot of what the tester saw. A
  report says, activity by activity, where the tester got stuck, what it had to guess, and whether it was satisfied.
- **Pass bar.** Every tester completes its role's activities. A finding is **blocking** if it stopped the tester short,
  or if a docs command doesn't work as shown. A finding is fixed by simplifying or trimming the docs, not by adding
  clarification, and is re-tested by a fresh tester of that role, or accepted with a reason. The final round leaves no
  blocking finding.
- **Void reports.** A report that reuses names from the worked example, or that makes claims without pasted output or
  a screenshot, is void and is run again.

**UA-M, the chief engineer's test** (the core of acceptance):

- On a Mac, he clones both repositories, switches to `dev`, and previews the documentation site on
  localhost. Following only the docs, he installs SCATLAB, uses it from Claude and from inference.coop, and codes a
  real project of his own in one of the two chats.
- **Pass:** he is satisfied enough to give minor feedback, if any, to prepare the release.
- Anything he flags is fixed on `dev`, and the candidate is refreshed (see Governance, "Release").

## Definition of good

- Make the right way the easy way: following the docs literally, and using the provided templates and operations, is
  the shortest path, and it produces a conformant vault.
- The ontology is lean and recognisable: adopted where an existing ontology wins, authored where it doesn't, never a
  patchwork.
- A first-time user fixes every conformance problem from the message alone, without reading the source.
- The worked example reads well in Obsidian, as judged by the chief engineer in UA-M.

## Definition of good enough

- R-1 to R-23 met, with evidence.
- UA-A passes on the candidate, for every role.
- The candidate is staged for UA-M, with the reviewer's guide ready.
- The architecture document is current (R-22), and the docs give every ontology term's source, or say it is
  authored and why.

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
  each package acceptance. The user tests come last.
- **Ontology changes before release.** Once the ontology and page contracts are accepted, a change to them during v0.1 is the
  ACE's logged call if it serves the mission as written. It is an intent gap if it would change what the graph means.
- **The glossary.** `GLOSSARY.md` defines the project's words, each in one sense, and maps each to its formal
  concept and source once. Keeping to it is part of every package: each scope of work, contract, test name and docs
  page uses its words in its senses, the PM's scope check rejects a scope that doesn't, and the change consultant's
  sweep includes it. The glossary can change, at a high bar: the ACE makes the change on `dev` as a logged call, after
  the consultant's sweep finds every use, brings every use in line in the same package, and lists the change for the
  chief engineer's review at acceptance.
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
    tools in the package, and anything unavoidably platform-specific is isolated and recorded. The chat path's
    launcher is macOS-only by design; its macOS tools (among them `security`, for the session key in the keychain)
    sit behind its own functions.
- **Until the release,** nothing in `scat-tools` or `scat-template` is merged to `main`, tagged or published, with two exceptions:
  - changes to this mission;
  - the **candidate stage** that UA-M needs:
    - the docs site deploys from `dev` to Pages, marked pre-release;
    - `scat-template` is marked as a GitHub template, with `dev` as its default branch;
    - the template pins the tools to the candidate commit.

  Every fix during user acceptance moves the pin, reruns CI, R-6 and R-9, and the ACE decides, and logs, whether
  UA-A reruns.
- **Release.**
  1. The ACE opens one release PR from `dev` to `main` in each repository, and no one else does.
  2. The chief engineer's walkthroughs run against them, and his merges, as merge commits, are the acceptance.
  3. The ACE then tags `v0.1.0` on the merge commit in each repository, redeploys the site from `main` without the
     pre-release mark, publishes the MCP server's container image from the tools tag, and restores `main` as the
     template's default branch. The template's pin stays on the
     accepted candidate commit, whose content the tag marks.
- **Public-facing content is written as finished.** The code, the docs and the template describe the product as it
  is, with no development or test progress in them; progress stays in the work packages and the decision log.
  Explicitly deferred work becomes issues.
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

## Agent's defaults

Details the ACE settled and the chief engineer approved as a set. The ACE may revise one by a logged call where it
serves this mission as written; a change that would alter the mission goes to the chief engineer.
- Names: `scat-tools`, `scat-template`, the CLI `scat`, the Python package `scat_tools`.
- Python 3.12 or later. The template installs the tools through uv, as a git dependency pinned to a commit.
- Facilitation and coding guides are written once, on the Pages site, and the template links to them.
- Documentation built with MkDocs Material.
- `.python-version` and `uv.lock` are committed. CI runs `uv sync --locked`, `uv lock --check`, ruff (check and
  format) and pytest, and fails on attribution lines.
- Branches: `main` holds approved missions and releases only, `dev` is the integration branch, and work happens on
  short-lived unit branches off `dev`.
- The template sets the caps to stakeholder 6, concern 12, affordance 12 and technology 12, each the planner's to choose.
- **The machine interface:** JSON, from `--json` on every `scat` command and an equivalent method on every result in
  Python. Its schema is a JSON Schema file in `contracts/`, with an integer `schema_version`. Adding a field keeps the
  version, and removing or changing one bumps it. Schema validation runs in the test suite only, so it adds no runtime
  dependency to `scat-tools`. Not included: checking an unsaved editor buffer.
- **The claim-type mark** is a field on the narrative page, `claim_type`, with the values `actual`, `hypothetical` and
  `unclassified` (the default). It gates no status; with `kind`, it is a filter in the analysis views.
- **Links are not edges.** A link is a reference in a Markdown file; an edge is a typed fact in the knowledge graph.
  The Markdown is what the coder confirms; the tool reads it, builds the knowledge graph, and checks that the graph
  matches it (job (i)) and is conformant (job (ii)). An edge is asserted in the Markdown, written by the coder or by
  the assistant for the coder to confirm:
  - an edge is a row of a narrative's table, the coding of record, naming its two nodes; the narratives that tell an
    edge are the ones whose tables hold it;
  - a link in the account's prose is optional, names a node the table holds, and never creates an edge;
  - the checks hold the two in step: every edge's ends have the right node types (R-1), and a node the account links
    is one its table holds. A narrative that breaks this cannot be `done`.

  The ontology-and-layout package settles how edges are written and shown, checked in Obsidian (G15).
- **The IDE setup skill** in the template (D-3) is a short skill file that helps an AI coding assistant set itself up
  for the vault; the docs point to it.
- **The relationship annotation** has only the same-type rule; it is never entailed, never required and never in an index page's
  required links. It is a line in a node page's body.
- **The notebook** reads the vault through the tools' public data (R-16) where it can, through a public vault loader.
- **New dependencies** (the MCP server's, the notebook's) go in optional extras or the template, so `scat-tools`'s core
  runtime dependencies stay as they are.
- **The change consultant** runs on Sonnet as a role in `.claude/agents/`. Its sweep is a written list of search terms
  per change, run with `git grep` over both repositories and the live branches, so the same sweep runs at scoping and
  at acceptance.
- **Chat-path runs.** The ACE drives the inference.coop browser chat after the chief engineer signs in, and uses his
  GitHub account, signed in by him; the agent never enters credentials, and only lab and range material (R-20) goes to
  it. The R-20 end-to-end runs are made on demand, not on every push.
- **The range vault** rebuilds the KOI case with stakeholders, not named people.
- **Views on the chat path** are written into the project's private repository, so a finished model's views can be
  checked there.

## Open decisions (for the chief engineer)

None. Every item was resolved through the decision loop. The decisions are recorded in `decisions/log.md` and in the
threads of the PRs that changed this document.
