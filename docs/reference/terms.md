# Terms

Each word in one sense, as the glossary fixes it. See [Coding](../coding.md).

## The graph and its views

- **SCAT**: the four node types.
- **node**: a group, concern, affordance or technology of the layered graph. (Obsidian's graph view also calls every page a node.)
- **edge**: a typed connection between nodes in neighbouring layers, one per pair: `holds` (group to concern), `is addressed by` (concern to affordance), `is provided by` (affordance to technology).
- **element**: a node or edge.
- **layer**: all nodes of one type: `group`, `concern`, `affordance`, `technology`, in that order.
- **layered graph**: nodes and edges, in four layers.
- **knowledge graph**: the nodes, edges and narratives built from a vault, and its contributor pages; those are not in the layered graph.
- **narrative**: one account of the field notes, on one `narrative` page. Each edge it tells is a row of its `Edges told` table.
- **coded, uncoded**: said of a narrative. Coded: it links at least one node page. Uncoded: it links none. `done` means adequately coded, as the coder judges; a `done` narrative can be iterated or moved back to `draft`.
- **excluded**: said of an uncoded narrative: left out of the knowledge graph and every view, and reported.
- **timeframe**: what a narrative tells: happened (`past`), could happen (`future`), both (`mixed`).
- **scenario**: a narrative (`kind` `scenario`) about people doing things over time; it tells groups, concerns and affordances.
- **architecture**: a narrative (`kind` `architecture`) about parts put together into tools; it tells concerns, affordances and technologies.
- **fingerprint**: the nodes a narrative links and the edges that name it.
- **edge table**: all edges of one type, as a table. Not a narrative's `Edges told` table.
- **layered view**: the union of chosen narratives' fingerprints, drawn as the four layers.
- **trace**: following edges from a node up or down the layers.
- **view**: a picture or table made from a conformant knowledge graph.
- **relationship annotation**: a remark between two entries of one type, written as a body line with a link. Not an edge; in no view.

## The ontology underneath

- **type**: a defined category, named in a page's `type` field.
- **the ontology**: the fixed types and their rules.
- **entry**: a node, edge, narrative or annotation as stored: a page, row or line.
- **model**: the ontology plus a conformant vault; also the repository holding them.
- **conformant**: said of a vault whose knowledge graph matches its pages and obeys the ontology.

## The vault, as Obsidian shows it

- **vault**: the folder of Markdown files Obsidian opens; one git repository.
- **page**: a Markdown file with a `type` in its frontmatter.
- **field**: a key in a page's frontmatter.
- **Edges told**: the table on a `narrative` page, one row for each edge the account tells; columns `from`, `type`, `to`, `note`. Not an edge table.
- **link**: an Obsidian `[[…]]` reference. Never an edge by itself.
- **cap**: the most groups a vault may hold, set in `scat.toml` (key `stakeholder_group_cap`).
- **attribution mode**: required, optional or disallowed (Chatham House rule); set in `scat.toml`.
- **attribution**: the people a narrative is attributed to, where the mode allows, held as its `attributed_to` links to contributor pages; never a node or edge of the four layers.
- **contributor page**: a page of type `contributor`, outside the four layers, naming a person a narrative is attributed to, where the mode allows; the narrative's `attributed_to` field links to it. "Contributor" alone still means a participant.
- **index page**: the page generated for a type (`index`), listing its entries; an Obsidian Base, 1.9 or later.
- **status**: how far an entry has got: `stub` (a name), `draft` (content, incomplete) or `done` (complete, conformant, signed off by the coder).
- **stage**: where a project is in its lifecycle: plan, capture, code, analyse or report; decided by a person. Not a status: a page changes status many times within one stage.
- **transition**: a move from one stage to another, forward or backward, made on a person's word.
- **mismatch**: a link and an edge that disagree about the same relationship, reported with a fix.

## The work

- **organiser**: the one persona: runs a facilitated elicitation, codes its data.
- **coder, assistant, tool**: the three actors. The coder owns interpretation; the tool owns conformance; the assistant helps and holds no authority.
- **inputs, analysis**: the field notes; reports from the model.
- **field notes**: supplied material.
- **interpreting**: reading the field notes and views; the coder's act.
- **authoring**: writing a narrative from the coder's interpretation.
- **coding**: linking the nodes a narrative tells and recording its edges.
- **reviewing**: the coder checks narrative against notes and coding against SCAT; the tool checks conformance.
- **the coding loop**: interpreting, authoring, coding, reviewing, until the coder sets it to `done`.
- **analysing**: generating views from the knowledge graph's structure.
- **a finished model**: conformant, navigable, with views, and the coder's statement that it represents the notes.
- **rule, norm**: a rule is what conformance requires and the tool enforces. A norm is guidance to coders and assistants, not enforced; the assistant's rules are norms the server enforces only where it refuses an act.
- **skill**: a package of instructions an assistant loads, in the chat or the IDE.
- **saved agent**: the chat's saved assistant setup, from which a new chat starts.
- **session key**: the key the coder pastes into the chat for one session; deleted at Stop.
- **leave no trace**: the strict data-policy choice: the chat's copies removed at the end, local copies kept.
- **range vault**: a vault that rebuilds a published case with groups, not named people, to test the tools; not field data.
