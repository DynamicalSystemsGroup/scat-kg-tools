# The flow

The path from a first conversation to a vault (a folder Obsidian opens) that a coder codes.

## First try

SCAT (Stakeholder groups, Concerns, Affordances and Technologies) is built for an **organiser** who runs a facilitated elicitation with contributors. An organiser trying it alone, on their own notes, takes steps 5, 2 and 8 in that order: with no participants there is no step 4 or 7.

## The steps

| Step and guide | What happens | Depends on |
|---|---|---|
| **1 Discover**<br>[Home](index.md) | The organiser finds out what SCAT makes of a discussion: a vault of narratives, nodes and edges. | Nothing. |
| **2 Try**<br>[The solo trial](getting-started.md#the-solo-trial) | Alone, on their own notes: one narrative is coded, its [fingerprint](reference/terms.md) is viewed in Obsidian, and it is set to `done`. | Setup, as in step 5. |
| **3 Decide**<br>This page | The organiser chooses to run a facilitated elicitation. | The trial. |
| **4 Set terms**<br>[Data, rights and consent](data-and-consent.md) | Before the first session, the organiser answers and documents the nine choices: collection, storage, consent, use of contributions (which fixes the attribution mode), AI, release, licence, rights holders, and commitments to participants. | Step 3. |
| **5 Set up**<br>[Getting started](getting-started.md) | A private repository is made on GitHub from the template, cloned, set up with one command and opened in Obsidian as a vault. | Alone, nothing. With contributors, step 4's storage answer. |
| **6 Plan**<br>[Planning](planning.md) | Sessions: scenarios or architectures, who takes part, the attribution mode chosen in `scat.toml` and what participants are told, and the groups, held to the cap in `scat.toml`. | Steps 4 and 5. |
| **7 Capture**<br>[Scenarios](facilitate-scenarios.md), [Architectures](facilitate-architectures.md) | At each event, field notes are taken. They stay outside the tool, with the consent records, as step 4 allowed. | Steps 4, 6, and what participants were told. |
| **8 Code**<br>[Coding](coding.md), [CLI](reference/cli.md) | Each narrative goes round the [coding loop](reference/terms.md) (interpreting, authoring, coding, reviewing): a narrative page, node pages, and one `Edges told` row per edge. The tool checks conformance. | Step 5, field notes (step 7, or your own), and with contributors step 4's AI answer. |
| **9 Analyse**<br>[Analysis](analysis.md) | [Views](reference/terms.md) of the [knowledge graph](reference/terms.md) are read. Reading can send the coder back to step 8. | A [conformant](reference/terms.md) vault, and the uses step 4 allowed. |
| **10 Hand over**<br>[Coding](coding.md) | A clean whole-vault check, `scat index`, a commit and a push; the coder states the model is finished and locks the version with a git tag (the coding guide says how). That is a release, at the level step 4 set. | Steps 8 and 9, and step 4's release, licence and rights answers. |

Following through on commitments to participants comes after step 10 and depends on step 4.

To code with an assistant, see the [coding paths](coding-paths.md): [the chat path](chat-path.md) (a chat window, no terminal), [the IDE path](ide.md) or [a local LLM](local-llm.md).

A **narrative** is one page: the account, a link wherever it names a node, and a table of the edges it tells. A
**node** is a group, concern, affordance or technology page. An **edge** is a row in that table, not a page.
