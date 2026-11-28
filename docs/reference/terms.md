# Terms

Each word in one sense, as the glossary fixes it. See [Coding](../coding.md).

## Across the work

- **SCAT**: The method this tool supports: it codes each narrative into four node types, groups, concerns, affordances and technologies.
- **node**: One group, concern, affordance or technology; its page is a node page.
- **group**: A set of people who share a stake in the work, the first layer.
- **concern**: What a group cares about, in the group's own words: a need, a worry or a goal.
- **affordance**: What a technology offers that addresses a concern.
- **technology**: A tool, device or service that provides an affordance.
- **edge**: A typed connection between two nodes in neighbouring layers: `holds`, `is addressed by` or `is provided by`.
- **layer**: All the nodes of one type, in the order `group`, `concern`, `affordance`, `technology`.
- **narrative**: One story drawn from the field notes, on one `narrative` page.
- **vault**: The folder of Markdown files Obsidian opens; one git repository.
- **page**: One Markdown file with a `type` in its frontmatter.
- **field**: One key in a page's frontmatter, such as `status` or `kind`.
- **type**: A defined category of page, named in the page's `type` field.
- **status**: How far a page has got: `stub` (a name), `draft` (content, incomplete) or `done` (complete and signed off by the coder).
- **stage**: Where a project is in its lifecycle: plan, capture, code, analyse or report.
- **transition**: A move from one stage to another, forward or backward, made on a person's word.
- **organiser**: The person who runs the elicitation: decides its scope and policies, plans it and invites contributors, facilitates the events, gathers the field notes, codes them or asks a coder to, analyses, and reports the findings.
- **coder**: The person who owns interpretation: reads the field notes, writes and links the narratives, and signs off `done`.
- **assistant**: An LLM, where allowed, that helps the coder and holds no authority.
- **tool**: The program that owns conformance: it checks the vault and records only what the coder accepts.
- **check**: The command that tests a vault against the rules and reports problems; a clean check has no errors.
- **problem**: What a check reports: an error blocks, a warning is a to-do.
- **refused**: Said of an operation the tool will not do: it writes nothing and says why.

## Plan

- **session**: A facilitated event at which participants tell the organiser what they know.
- **participant**: Anyone who takes part in the elicitation.
- **consent**: The agreement of participants to what is recorded, kept and shared, settled before the first session.
- **attribution mode**: The vault's setting for naming people: attribution required, optional or disallowed.
- **cap**: The most groups one vault may hold, set in `scat.toml` (key `stakeholder_group_cap`).
- **coding path**: A way of coding the field notes: by hand, in an AI IDE, in a chat, or with a local LLM.
- **MCP server**: The program that lets a chat or an IDE assistant call the tool.

## Capture

- **facilitating**: Running a session: drawing out what participants know while another person takes the notes.
- **field notes**: The supplied material, in whatever form it arrives.
- **timeframe**: Whether a narrative tells what happened (`past`), what will happen (`future`) or both (`mixed`).
- **scenario**: A narrative with `kind` `scenario`: people doing things over time.
- **architecture**: A narrative with `kind` `architecture`: parts put together into tools.

## Code

- **coding**: Identifying and linking the nodes a narrative tells, and recording the edges it tells.
- **reviewing**: The coder's check that a narrative matches the field notes and that its coding is a correct use of SCAT.
- **rule**: What the check tests; a breach is reported as a problem.
- **account**: The prose of a narrative: its text outside the `Edges told` table.
- **link**: An Obsidian `[[...]]` reference from one page to another; never an edge by itself.
- **Edges told**: The table headed `Edges told` on a `narrative` page, one row for each edge the account tells.
- **candidate**: A pair of nodes that the account links, in adjacent layers, and that no row of the `Edges told` table joins.
- **mismatch**: A link and an edge that disagree about the same relationship, reported with a fix.
- **attribution**: The people a narrative is attributed to, held as its `attributed_to` links to `contributor` pages.
- **contributor**: A participant whose name a narrative is attributed to.
- **contributor page**: A page of type `contributor`, outside the four layers, naming one contributor.
- **REPL**: Python's interactive prompt, where each command of the tool has a twin function.

## Analyse

- **view**: A picture or table drawn from a vault whose check passes.
- **fingerprint**: The nodes a narrative links and the edges that name it.
- **edge table**: All edges of one type, between two neighbouring layers, as a table.
- **layered view**: The fingerprints of chosen narratives together, up to the whole vault, drawn as the four layers.
- **trace**: Following edges from one node up or down the layers.
- **evidence**: The view of one node page: the narratives that link it, with the paragraph around each link.

## Report

- **index page**: The page the tool generates for each type (`index`), listing that type's pages.
