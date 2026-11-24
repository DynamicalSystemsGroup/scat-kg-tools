# RS1 — Research spike: an Obsidian community plugin

| | |
|---|---|
| **Status** | Approved by the ACE (log D-052). **Outside v0.1.** It is exploration the chief engineer directed, and it lifts the "Obsidian plugin" non-goal for research only. |
| **Branch** | `spike/obsidian-plugin` off `dev`, never merged into `dev` before the v0.1 release. Pushed for review. |
| **Directory** | `research/obsidian-plugin/` |

## Purpose

Find out how SCAT's tooling can work directly inside Obsidian, as an opinionated linter that makes the vault an IDE for
the ontology, so that most users can work in Obsidian and GitHub without a CLI or REPL. The spike recommends; a later
package delivers.

## Questions

1. **Obsidian's plugin API.** What does it offer for a linter's UX: diagnostics on the active note, a side panel,
   status bar, commands, editor decorations, quick fixes (applying a rule's exact fix), and file events (check on
   save)?
2. **The community-plugin path.** What are the submission and review requirements, the policies (for example on
   shelling out, network access and bundled binaries), and what desktop-only versus mobile means?
3. **Architecture, as a trade study.** Options include:
   - (a) the plugin calls the Python tools as a subprocess, desktop-only, needing uv and Python on the machine;
   - (b) a TypeScript port of the checks, generated from or tested against `ontology/scat.ttl` and the rule
     catalogue, so R-13's single source survives;
   - (c) Python in the plugin via Pyodide or WebAssembly;
   - (d) a hybrid.

   Judge each on user setup burden, single-source integrity, mobile support, maintenance, store acceptance, and speed
   on a 500-page vault.
4. **What the tools would need.** For example, machine-readable output (`--json`), stable rule ids, and a check of an
   unsaved buffer.

## Deliverables

- `research/obsidian-plugin/readout.md`: answers to the questions, with sources, the trade study, a recommendation,
  and a sketch of a first delivery package. At most 1,500 words.
- `research/obsidian-plugin/prototype/`: a minimal plugin, from Obsidian's sample-plugin layout, implementing the
  recommended architecture's core loop: run the checks for the active note and show the messages in a panel or as
  notices. It builds with `npm`, and its logic has unit tests. Nobody can open Obsidian here, so state plainly what
  was and wasn't exercised.

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| RS1-R1 | Every claim about Obsidian's API or store policy cites the official docs or the sample plugin, with a link. | The reviewer spot-checks the links |
| RS1-R2 | The prototype builds cleanly, and its unit tests pass. | Pasted output |
| RS1-R3 | The trade study scores every option on every criterion, with a reason. | Inspection |
| RS1-R4 | The readout lists what the prototype has not shown (it was never run inside Obsidian). | Inspection |

## Constraints

- Dependencies come from the official npm registry only: the Obsidian sample plugin's own toolchain (`obsidian`,
  `typescript`, `esbuild`), plus anything else named with its reason. Nothing is published to any store, and no
  release is cut.
- No private material, as always.
