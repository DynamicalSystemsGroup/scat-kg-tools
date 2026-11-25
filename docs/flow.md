# The flow

The path from a first conversation to a vault (a folder Obsidian opens) that a coder codes, as an organiser sees it.

## Two readers

SCAT (Stakeholder groups, Concerns, Affordances and Technologies) is built for an **organiser** who runs a facilitated elicitation with contributors. For that reader, setting
expectations, securing consent and following through on the commitments made to participants are steps of the flow
(4 and 6 to 10). A reader trying the approach alone, on their own notes, can skip the consent steps: set up (step 5), try (step 2), then code the notes (step 8).

## The steps

| Step and guide | What happens | Depends on |
|---|---|---|
| **1 Discover**<br>[Home](index.md) | The organiser finds out what SCAT turns a discussion into: a vault of **narratives**, **nodes** and **edges**. | Nothing. |
| **2 Try**<br>[Getting started](getting-started.md) | Alone, on their own notes: one narrative is coded, its **fingerprint** (the nodes it links and the edges it tells) is looked at in Obsidian, and it is set to `done`. | Setup, as in step 5. |
| **3 Decide**<br>This page | The organiser chooses to run a facilitated elicitation. | The trial. |
| **4 Set terms**<br>[Data, rights and consent](data-and-consent.md) | The organiser answers and documents the up-front questions: participation terms, AI use, how each kind of material is kept and released, and the commitments made to participants. | Step 3. |
| **5 Set up**<br>[Getting started](getting-started.md) | A private repository is made from the template, cloned, set up with one command and opened in Obsidian as a vault. | Step 4's answer on where the material is kept. |
| **6 Plan**<br>[Planning](planning.md) | Sessions: which tell scenarios and which architectures, who takes part, the participation terms and the groups, held to the cap in `scat.toml`. | Steps 4 and 5. |
| **7 Capture**<br>[Scenarios](facilitate-scenarios.md), [Architectures](facilitate-architectures.md) | At each event, field notes are taken. They stay outside the tool, in the form step 4 allowed. | Step 6, and what participants were told. |
| **8 Code**<br>[Coding](coding.md), [CLI](reference/cli.md) | Each narrative goes round the coding loop (interpreting, authoring, coding, reviewing): a narrative page, node pages, and one `Edges told` row per edge. The tool checks conformance; the coder owns interpretation. | Steps 5 and 7. |
| **9 Analyse**<br>[Terms](reference/terms.md) | Views of the knowledge graph (a fingerprint, an edge table, the layered view, a trace) are read. Reading can send the coder back to step 8. | A conformant vault. |
| **10 Hand over**<br>[Coding](coding.md) | A clean whole-vault check, `scat index`, a commit and a push; the coder states the model is finished and tags the version. That hand-over is a release, at the level step 4 set. | Steps 8 and 9, and the release answers of step 4. |

Following through on commitments to participants, such as sharing findings back, comes after step 10 and depends on step 4.

A **narrative** is one page: the account, a link wherever it names a node, and a table of the edges it tells. A
**node** is a group, concern, affordance or technology page. An **edge** is a row in that table, not a page.
