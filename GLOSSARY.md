# Glossary

The words an organiser meets, each in one sense. The mission, the scopes of work, the contracts, the code and the docs use the plain term in the first column. The last column maps it, once, to the formal concept it stands for and where that concept comes from; formal terms appear elsewhere only where a document is precise on purpose. Three vocabularies meet in this project: graph theory, the semantic web, and Obsidian. The same idea wears different words in each, and the same word can mean different things. This glossary keeps them apart. The words are in a core, the words met across the work, and one section for each stage of the work, the words first met there.

## Across the work

The words met in every stage.

| Term | Definition | Example use | Formal concept and source |
|---|---|---|---|
| **SCAT** | The method this tool supports: it codes each narrative into four node types, groups, concerns, affordances and technologies. The name also nods to scat singing in improvised jazz. | "SCAT codes each narrative into its four node types." | Authored in SCAT |
| **node** | One group, concern, affordance or technology; its page is a node page. In Obsidian's graph view every page is drawn as a node, so that one is always spelled out as "a node in Obsidian's graph view", which is a page. | "`watershed-stewards` is a group node." | Vertex (graph theory); a 0-simplex (knowledge complex) |
| **group** | A set of people who share a stake in the work, the first layer. Groups are few and broad, so that none points to one person; the cap limits how many a vault holds. | "Farm irrigators are a group." |  |
| **concern** | What a group cares about, in the group's own words: a need, a worry or a goal. A group holds concerns, and an affordance addresses them. | "Guaranteed irrigation allocation is a concern." |  |
| **affordance** | What a technology offers that addresses a concern. An affordance is something a person can do, not a tool. | "Getting an alert when a pipe leaks is an affordance." |  |
| **technology** | A tool, device or service that provides an affordance. | "A soil sensor is a technology." |  |
| **edge** | A typed connection between two nodes in neighbouring layers: `holds`, `is addressed by` or `is provided by`. The three types read as "holds" (group to concern), "is addressed by" (concern to affordance) and "is provided by" (affordance to technology). There is at most one edge per pair. | "Farm irrigators *hold* guaranteed irrigation allocation." | Edge (graph theory); a 1-simplex (knowledge complex); in the TBox, Heldby, Addresses and ProvidedBy |
| **layer** | All the nodes of one type, in the order `group`, `concern`, `affordance`, `technology`. "Up" is toward groups. | "Tracing a concern goes one layer up to groups." | Partition of a layered (k-partite) graph (graph theory) |
| **narrative** | One story drawn from the field notes, on one `narrative` page. It is usually a scenario or an architecture. Each edge it tells is a row of its `Edges told` table. A narrative that links no node page is left out of the views and reported until it links one. | "The dry-July narrative is a scenario." | Authored in SCAT, from the coding practice of `ant-rdf` |
| **vault** | The folder of Markdown files Obsidian opens; one git repository. | "Open the vault in Obsidian." | Obsidian |
| **page** | One Markdown file with a `type` in its frontmatter. | "The narrative page holds the account." | Obsidian note |
| **field** | One key in a page's frontmatter, such as `status` or `kind`. Obsidian shows fields as "Properties". | "The `status` field reads `draft`." | YAML frontmatter (Obsidian) |
| **type** | A defined category of page, named in the page's `type` field. The node types are group, concern, affordance and technology; a narrative has a kind, scenario or architecture. | "`technology` is a node type." | Class (OWL, RDFS) |
| **status** | How far a page has got: `stub` (a name), `draft` (content, incomplete) or `done` (complete and signed off by the coder). | "The narrative is `done`: linked and signed off." | Authored in SCAT |
| **stage** | Where a project is in its lifecycle: plan, capture, code, analyse or report. A person decides it; the tool offers the tools that stage's work needs and refuses the rest. Not a status: a page changes status many times within one stage. | "The vault is in the code stage." | State of the lifecycle machine (authored; `contracts/lifecycle.md`) |
| **transition** | A move from one stage to another, forward or backward, made on a person's word. The tool may say a move is open. | "Reading the views sent the project back to code: a backward transition." | Transition of the lifecycle machine (authored) |
| **organiser** | The person who runs the elicitation: decides its scope and policies, plans it and invites contributors, facilitates the events, gathers the field notes, codes them or asks a coder to, analyses, and reports the findings. | "The organiser sets the cap before the first session." | Authored in SCAT |
| **coder** | The person who owns interpretation: reads the field notes, writes and links the narratives, and signs off `done`. The organiser, who runs the elicitation, may also be the coder. | "The coder sees that the farmers never mention price." | Authored in SCAT |
| **assistant** | An LLM, where allowed, that helps the coder and holds no authority. It proposes and the coder decides; the server refuses it the act of setting `done`. | "The assistant drafts; the coder writes the final wording." | Authored in SCAT |
| **tool** | The program that owns conformance: it checks the vault and records only what the coder accepts. It is the Python package scat-tools with its command line, also called "the tools"; the MCP server is a front end to it, not part of it. | "The tool checks that the graph matches the pages." | Authored in SCAT |
| **check** | The command that tests a vault against the rules and reports problems; a clean check has no errors. Warnings may remain on a clean check. The same word names the gate a page passes before the coder sets `done`. | "The check is clean: no errors." | Conformance checking (authored rule catalogue, against the TBox) |
| **problem** | What a check reports: an error blocks, a warning is a to-do. Each comes with a fix. | "The check reports one error and two warnings." |  |
| **refused** | Said of an operation the tool will not do: it writes nothing and says why. A refusal is not an error in the vault. | "Setting `done` is refused; the coder sets it in Obsidian." |  |

## Plan

Setting the terms of the elicitation, setting up the vault, planning the sessions.

| Term | Definition | Example use | Formal concept and source |
|---|---|---|---|
| **session** | A facilitated event at which participants tell the organiser what they know. Only that event is called a session here; a run of the chat is called a chat run. | "The second session heard from the crew leads." |  |
| **participant** | Anyone who takes part in the elicitation. A participant is a contributor only where a narrative is attributed to them. | "Three participants came to the first session." |  |
| **consent** | The agreement of participants to what is recorded, kept and shared, settled before the first session. | "Participants gave consent to the notes being kept." |  |
| **attribution mode** | The vault's setting for naming people: attribution required, optional or disallowed. Disallowed is the Chatham House rule. The organiser chooses it before the first session and the person who set up the tools writes it in `scat.toml`. | "The vault runs in attribution-disallowed mode, so no narrative names who said it." | Authored in SCAT; the Chatham House rule |
| **cap** | The most groups one vault may hold, set in `scat.toml` (key `stakeholder_group_cap`). The organiser chooses it, so that few, broad groups cannot point to one person. | "The cap is 3, so a fourth group is refused." | Authored in SCAT |
| **coding path** | A way of coding the field notes: by hand, in an AI IDE, in a chat, or with a local LLM. The organiser picks one when setting up. | "The coding path for this project is chat." |  |
| **MCP server** | The program that lets a chat or an IDE assistant call the tool. It is a front end to the tool; "connector" is a chat platform's name for it. | "The chat reaches the tool through the MCP server." | Model Context Protocol server |

## Capture

Facilitating the sessions and gathering field notes.

| Term | Definition | Example use | Formal concept and source |
|---|---|---|---|
| **facilitating** | Running a session: drawing out what participants know while another person takes the notes. | "Facilitating a scenario session means asking what people do over time." |  |
| **field notes** | The supplied material, in whatever form it arrives. They are gathered in a session and read by the coder. | "Draft two narratives from the workshop's field notes." | The inputs (authored) |
| **timeframe** | Whether a narrative tells what happened (`past`), what will happen (`future`) or both (`mixed`). It is the narrative's `timeframe` field, required at `done`, and the author's reading of the text. | "A narrative about a proposed tool has timeframe `future`." | Authored in SCAT (page contracts) |
| **scenario** | A narrative with `kind` `scenario`: people doing things over time. It tells groups, concerns and affordances. | "A scenario rarely names a technology." | Authored in SCAT |
| **architecture** | A narrative with `kind` `architecture`: parts put together into tools. It tells concerns, affordances and technologies. | "An architecture rarely names a group." | Authored in SCAT |

## Code

Turning field notes into narratives, nodes and edges.

| Term | Definition | Example use | Formal concept and source |
|---|---|---|---|
| **coding** | Identifying and linking the nodes a narrative tells, and recording the edges it tells. It is one step of the coding loop: interpreting the field notes, authoring the narrative, coding it and reviewing it, repeated until the coder sets it `done`. | "Coding links `quick-leak-response` where the account names it." | Qualitative coding (ethnographic practice) |
| **reviewing** | The coder's check that a narrative matches the field notes and that its coding is a correct use of SCAT. Both are the coder's judgement; the tool checks conformance alongside. | "Reviewing found the narrative overstated the crew's concern." | Authored in SCAT |
| **rule** | What the check tests; a breach is reported as a problem. The rules are in a catalogue and the tool enforces them. | "A narrative with a broken link breaks a rule." | Conformance checking (rule catalogue) |
| **account** | The prose of a narrative: its text outside the `Edges told` table. A link stands wherever the account names a node. | "The account names the leak response, so it links `quick-leak-response`." | Authored in SCAT |
| **link** | An Obsidian `[[...]]` reference from one page to another; never an edge by itself. | "Link `quick-leak-response` where the account names it." | Wikilink (Obsidian) |
| **Edges told** | The table headed `Edges told` on a `narrative` page, one row for each edge the account tells. Its columns are `from`, `type`, `to` and `note`, and each row reads as a sentence. It is not an edge table. | "Add a row to the Edges told table: parents *hold* bike-safe-for-children." | Authored in SCAT (page contracts); a table of subject, predicate, object |
| **candidate** | A pair of nodes that the account links, in adjacent layers, and that no row of the `Edges told` table joins. The tool cannot know whether the account tells that edge, so the coder decides: add a row, or leave it. | "The fingerprint view shows the candidates when asked." |  |
| **mismatch** | A link and an edge that disagree about the same relationship, reported with a fix. It is one of the problems a check reports, and the fix says which side to change. | "The tool reports a mismatch between the page and the graph." | Divergence (authored) |
| **attribution** | The people a narrative is attributed to, held as its `attributed_to` links to `contributor` pages. Where the mode disallows attribution there are none. It is never a node or an edge. | "The narrative's attribution names the two engineers who told it." | Authored in SCAT; attribution (provenance) |
| **contributor** | A participant whose name a narrative is attributed to. Only where the attribution mode allows it. | "The engineer who told it is the narrative's contributor." | Authored in SCAT |
| **contributor page** | A page of type `contributor`, outside the four layers, naming one contributor. A narrative's `attributed_to` field links to it. It is not a node. | "The narrative's `attributed_to` links to the contributor page for the engineer who told it." | Authored in SCAT |
| **REPL** | Python's interactive prompt, where each command of the tool has a twin function. | "In the REPL, `candidates=True` does what `--candidates` does on the command line." | Read-eval-print loop |

## Analyse

Reading the views of the whole graph.

| Term | Definition | Example use | Formal concept and source |
|---|---|---|---|
| **view** | A picture or table drawn from a vault whose check passes. The fingerprint, the edge table, the layered view and the trace are views. | "The views are generated after the check passes." | View in model-view-controller (software architecture) |
| **fingerprint** | The nodes a narrative links and the edges that name it. Drawn joined to the narrative, it is everything the narrative touches. It may have no edges and may be disconnected. | "The sensor-first pitch's fingerprint has seven nodes and two edges." | Support (mathematics: where a function is non-zero, here the narrative's indicator over nodes and edges); neighbourhood (graph theory) |
| **edge table** | All edges of one type, between two neighbouring layers, as a table. It is not a narrative's `Edges told` table. | "Export the *holds* table as CSV." | Bipartite graph (graph theory) |
| **layered view** | The fingerprints of chosen narratives together, up to the whole vault, drawn as the four layers. | "In the layered view, three groups share one concern." | Layered graph drawing (graph theory) |
| **trace** | Following edges from one node up or down the layers. | "Trace this concern down to the technologies behind it." | Reachability (graph theory); traceability (requirements engineering) |
| **evidence** | The view of one node page: the narratives that link it, with the paragraph around each link. | "The evidence for this concern shows three narratives." |  |

## Report

Handing the work over.

| Term | Definition | Example use | Formal concept and source |
|---|---|---|---|
| **index page** | The page the tool generates for each type (`index`), listing that type's pages. It is an Obsidian Base, 1.9 or later. | "The concern index page lists 18 concerns." | Class page (authored) |
