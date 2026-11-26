# Glossary

The words this project uses, each in one sense. The mission, every scope of work, the contracts, the code and the docs
use the plain term in the first column. The last column maps it, once, to the formal concept it stands for and where
that concept comes from; formal terms appear elsewhere only where a document is precise on purpose (the ontology
readout, the architecture document, the TBox itself).

Three vocabularies meet in this project: graph theory, the semantic web, and Obsidian. The same idea wears different
words in each, and the same word can mean different things. This glossary keeps them apart.

**Changing this glossary.** The bar is high, but changes are allowed: an overlooked distinction is better fixed here
than worked around. The ACE makes a change on `dev` as a logged call: the change consultant's sweep (R-18) finds every
use of the changed term first, the change and its reason go in `decisions/log.md`, and every use is brought in line in
the same package. Each change is listed for the chief engineer's review at acceptance.

## The graph and its views

| Term | Definition | Example use | Formal concept and source |
|---|---|---|---|
| **SCAT** | The four node types, stakeholder groups, concerns, affordances and technologies; the name also nods to scat singing in improvised jazz. | "SCAT codes each narrative into its four node types." | Authored in SCAT |
| **node** | One group, concern, affordance or technology in the layered graph. One exception, always spelled out: Obsidian's graph view draws every page as a node; there, say "a node in Obsidian's graph view", which is a page. | "`watershed-stewards` is a group node." | Vertex (graph theory); a 0-simplex (knowledge complex) |
| **edge** | A typed connection between two nodes in neighbouring layers. There are three types, read as "holds" (group → concern), "is addressed by" (concern → affordance) and "is provided by" (affordance → technology). At most one per pair. | "Farm irrigators *hold* guaranteed irrigation allocation." | Edge (graph theory); a 1-simplex (knowledge complex); in the TBox, Heldby, Addresses and ProvidedBy |
| **element** | Any node or edge. | "Coding identifies every element the account tells." | Simplex (knowledge complex) |
| **layer** | All the nodes of one type. The four layers, in order: group, concern, affordance, technology. "Up" is toward groups. | "Tracing a concern goes one layer up to groups." | Partition of a layered (k-partite) graph (graph theory) |
| **layered graph** | The nodes and edges only, in their four layers: the knowledge graph without narratives and relationship annotations. | "A trace walks the layered graph." | Layered (k-partite) graph (graph theory) |
| **knowledge graph** | The nodes, edges and narratives the tool builds from a vault and checks against the ontology, and the contributor pages where the vault's attribution mode allows them. The contributor pages are in the knowledge graph but not in the layered graph. | "The tool checks that the knowledge graph matches the pages." | An ABox under a TBox (description logic) |
| **narrative** | One account drawn from the field notes, on one page. Usually a scenario or an architecture, sometimes neither. In analysis it can be drawn as a node of its own, joined to what it tells. | "The dry-July narrative is a scenario." | Authored in SCAT, from the coding practice of `ant-rdf` |
| **coded, uncoded** | Said of a narrative. Coded: it links at least one node page anywhere in its body, in a row end of its Edges told table or in a link in its account. Uncoded: it links none. A coded narrative is in the knowledge graph; an uncoded one is excluded. Being coded is not being done: `done` means the narrative is adequately coded, as the coder judges, and a `done` narrative can still be iterated or moved back to `draft`. | "The new narrative is uncoded until it links its first node." | Authored in SCAT; the conformance requirement of WP21-G2 |
| **excluded** | Said of an uncoded narrative: left out of the knowledge graph and every view, and reported as excluded by the check and the views. It is included as soon as it is coded. | "The check reports the draft narrative as excluded: it links no node." | Authored in SCAT; exclusion by the tool, not an error (WP21-G2) |
| **scenario** | A narrative about people doing things over time; it tells groups, concerns and affordances. | "A scenario rarely names a technology." | Authored in SCAT |
| **architecture** | A narrative about how parts are put together into tools that offer affordances; it tells concerns, affordances and technologies. | "An architecture rarely names a group." | Authored in SCAT |
| **fingerprint** | The elements a narrative tells: the nodes it links and the edges that name it. Drawn joined to the narrative, it is everything the narrative touches. It may have no edges and may be disconnected. | "The sensor-first pitch's fingerprint has seven nodes and two edges." | Support (mathematics: where a function is non-zero, here the narrative's indicator over the elements); neighbourhood (graph theory) |
| **edge table** | All edges of one type, between two neighbouring layers, read as a table. Not a narrative's Edges told table. | "Export the *holds* table as CSV." | Bipartite graph (graph theory) |
| **layered view** | The union of the fingerprints of a chosen set of narratives, up to the whole vault, drawn as the four layers. | "In the layered view, three groups share one concern." | Layered graph drawing (graph theory) |
| **trace** | Following edges from one node up or down the layers. | "Trace this concern down to the technologies behind it." | Reachability (graph theory); traceability (requirements engineering) |
| **view** | A purposeful picture or table made from a conformant knowledge graph: a fingerprint, an edge table, the layered view, a trace. | "The views are generated after the check passes." | View in model–view–controller (software architecture) |
| **relationship annotation** | A free-text remark between two entries of the same type, such as two concerns that pull against each other. Not an edge; it stays out of every view. | "A relationship annotation records that anonymity and attribution pull apart." | Authored in SCAT |

## The ontology underneath

| Term | Definition | Example use | Formal concept and source |
|---|---|---|---|
| **type** | One of the defined categories: the four node types, the three edge types, narrative (with scenario and architecture), and relationship annotation. A page names its type in its `type` field. | "`technology` is a node type." | Class (OWL, RDFS) |
| **the ontology** | This project's fixed definitions of the types and their rules, which the tool checks against. ("An ontology", unqualified, is any other one, such as those surveyed for adoption.) | "The ontology says a holds edge joins a group to a concern." | TBox (description logic; OWL, in Turtle) |
| **entry** | One node, edge, narrative or relationship annotation as stored in the vault: a page, or a field on a page. | "Each node is an entry with its own page." | Record; an individual in the ABox (description logic) |
| **model** | The ontology plus a conformant vault (in the architecture); as a kind of material, the git repository that holds them. | "The model is a good representation of the field notes." | Model in model–view–controller (software architecture) |
| **conformant** | Passing the tool's two checks: the knowledge graph matches the pages, and it obeys the ontology. | "The vault is conformant: no errors." | Conformance checking (authored rule catalogue, against the TBox) |

## The vault, as Obsidian shows it

| Term | Definition | Example use | Formal concept and source |
|---|---|---|---|
| **vault** | The folder of Markdown files Obsidian opens; one git repository. | "Open the vault in Obsidian." | Obsidian |
| **page** | One Markdown file with a `type` in its frontmatter. | "The narrative page holds the account." | Obsidian note |
| **field** | One key in a page's frontmatter; Obsidian shows fields as "Properties". | "The `status` field reads `draft`." | YAML frontmatter (Obsidian) |
| **Edges told** | The table on a narrative page under the heading `Edges told`: one row for each edge the account tells, with the columns `from \| type \| to \| note`, each row read as a sentence. Not an edge table. | "Add a row to the Edges told table: parents *hold* bike-safe-for-children." | Authored in SCAT (page contracts); a table of subject, predicate, object |
| **link** | An Obsidian `[[…]]` reference from one page to another. Never an edge by itself. | "Link `quick-leak-response` where the account names it." | Wikilink (Obsidian) |
| **cap** | The most stakeholder groups one vault may hold, set by the organiser in the vault's `scat.toml` (key `stakeholder_group_cap`), so few, broad groups can't point to one person. | "The cap is 3, so a fourth group is refused." | Authored in SCAT |
| **attribution mode** | The setting a vault runs in, exactly one of: attribution required, optional or disallowed. Disallowed is the Chatham House rule. The organiser sets it at set-up in `scat.toml`, and the tools know it. | "The vault runs in attribution-disallowed mode, so no narrative names who said it." | Authored in SCAT (ACE call D-129); the Chatham House rule |
| **attribution** | The people a narrative is attributed to, named in its `attributed_to` field, where the mode allows or requires it. Never a node, never a link. Not the participants in general, whom the mission calls contributors. | "The narrative's attribution names the two engineers who told it." | Authored in SCAT (ACE call D-129); attribution (provenance) |
| **contributor page** | A page of type `contributor`, outside the four layers, naming a person a narrative is attributed to; it exists only where the vault's attribution mode (required or optional) allows it. A narrative's `attributed_to` field links to these pages, and those links are its attribution. Not a node. "Contributor" alone keeps its sense of a participant in the elicitation, as in the mission and the organiser's example. | "The narrative's `attributed_to` links to the contributor page for the engineer who told it." | Authored in SCAT (ACE call D-138) |
| **index page** | The page the tool generates for a type, listing its entries. | "The concern index page lists 18 concerns." | Class page (authored) |
| **status** | How far an entry has got: `stub` (a name, perhaps some metadata), `draft` (content, not yet complete) or `done` (complete, conformant and signed off by the coder). | "The narrative is `done`: coded and signed off." | Authored in SCAT |
| **mismatch** | A link and an edge that should agree but don't. The tool reports each with a fix. | "The tool reports a mismatch between the page and the graph." | Divergence (authored; R-23) |

## The work

| Term | Definition | Example use | Formal concept and source |
|---|---|---|---|
| **organiser** | The one persona: the person who runs a facilitated elicitation and codes its data. They first try the tools alone, on their own notes. | "An organiser tries SCAT solo before using it with contributors." | Authored in SCAT |
| **coder, assistant, tool** | The three actors. The coder (the organiser, in that role) owns interpretation; the tool (the Python package `scat-kg` with its CLI, also called "the tools"; the MCP server is a front end to it, not part of it) owns conformance; the assistant (an LLM, where allowed) helps and holds no authority. | "The tool checks that the knowledge graph matches the pages." | Authored in SCAT |
| **inputs, model, analysis** | The three kinds of material: the field notes; the git repository with the narratives and the knowledge graph; and the reports derived from it. Each has its own rules for who and what may touch it. | "Only the approved service may touch the inputs." | Authored in SCAT |
| **field notes** | The supplied material, in whatever form it arrives. | "Draft two narratives from the workshop's field notes." | The inputs (authored) |
| **interpreting** | Reading the field notes and reasoning about what they do and don't actually say; also reading the views. Always the coder's act, even when an assistant helps. | "Interpreting the notes, the coder sees the farmers never mention price." | Interpretation in qualitative research (ethnographic practice) |
| **authoring** | Writing or revising a narrative from the coder's interpretation of the field notes. | "The assistant drafts; the coder authors the final wording." | Authored in SCAT |
| **coding** | Identifying and linking the nodes a narrative tells, and recording the edges it tells. | "Coding links `quick-leak-response` where the account names it." | Qualitative coding (ethnographic practice) |
| **reviewing** | The coder checks that the narrative is aligned with the field notes, and that the coding is a correct use of SCAT, both in the coder's interpretation; the tool checks conformance alongside. | "Reviewing found the narrative overstated the crew's concern." | Authored in SCAT |
| **the coding loop** | Interpreting → authoring → coding → reviewing, repeated until, with the tool's check passing, the coder confirms both checks in reviewing; that sets the narrative to `done`. | "Two more turns of the coding loop, then it's done." | Authored in SCAT |
| **analysing** | The output step: acting on the knowledge graph's structure to generate views. The coder interprets the views, which can send them back to the field notes and round the loop again. | "Analysing showed a concern no technology reaches." | Network analysis; data visualisation |
| **a finished model** | Finished for the whole exercise: the knowledge graph is conformant, the vault is navigable, the views are generated, and the coder who interpreted the field notes states that the model is a good representation of what those notes contain. The statement is made outside the tool, by locking a version (tagging a commit) and handing it over. | "The coder tagged the commit and handed the finished model over." | Authored in SCAT |
| **rule, norm** | A rule is what conformance requires and the tool enforces: the catalogue's rules, whose breach the check reports. A norm is guidance to coders and assistants, the same for a person as for an LLM, carried in the docs and in skill files; the tool does not enforce it. The assistant's rules are norms for the assistant: the server enforces them only where it refuses an act (it cannot set `done`). | "A narrative with no node link is excluded by a rule; a brief description is a norm." | Rule and norm (authored in SCAT); rule: conformance checking (rule catalogue); norm: guidance of practice (deontic, not enforced) |
| **skill** | A package of instructions that an assistant loads, in the chat or in the IDE, and follows. The assistant is still the actor and holds no authority. | "Load the SCAT skill before the first reply." | Skill (a feature of the chat and the IDE; Claude's Agent Skills) |
| **saved agent** | The chat's feature that keeps an assistant set up for a purpose (its instructions, skills and tools) so a new chat starts from it. The assistant is still the actor and holds no authority. | "Start the session from the saved agent for SCAT." | Saved agent (a feature of the chat platform) |
| **session key** | The key the coder pastes into the chat for one session, so the chat reaches the tool. It is kept in the login keychain and deleted at Stop. | "The session key was deleted at Stop." | Bearer token for one session (access control); macOS login keychain |
| **leave no trace** | The strict data-policy option of the chat path's life cycle: a temporary chat, the field notes uploaded as a collection, and the server entry, agents, prompts and skills set up for the session removed from the platform at the end, local copies kept. One option among policies, not a recommendation. | "A project under a non-retention policy may choose the leave no trace life cycle." | Authored in SCAT (WP21-G7); data minimisation (privacy practice) |
| **range vault** | A vault that rebuilds a published case with groups, not named people, to test the tools; it is not field data. | "The KOI range vault passes the check." | Authored in SCAT (test fixture; MISSION) |
