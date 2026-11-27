# RS6 — Scope of work: research spike on the glossary

| | |
|---|---|
| **Status** | Approved by the chief engineer (log D-168). Feeds the glossary cleanup package, scoped after WP29 locks the stages. |
| **Branch** | `spike/glossary` off `dev`; never merged into `dev`. The readout is merged into `dev` on its own. |
| **Revert point** | `divergence/D-163` (shared) |

## Purpose

The chief engineer, reviewing the glossary's pending changes (typed by the agent): "should we do a spike and design a
cleanup pass to make sure our glossary is consistent and aligned with our app and workflows. we've made some revisions
and while it seems mostly aligned it feels a little be inconsistent in scope, i don't want the glossay to be huge and
there are terms from a few different levels of abstraction in there, this glossary is for the user of the app (which is
the organizer deciding scope and policies, planning and soliciting contributors, facilitating during events, gathering
field notes after the event, coding those notes, analyzing, and eventually reporting out findings." A spike answers
questions; it changes no term.

## Goals

- **RS6-G1. Inventory.** Every term in `GLOSSARY.md` and `docs/reference/terms.md`, and every term the docs, the tool's
  messages and the MCP server use that the glossary lacks, each with where the organiser meets it.
- **RS6-G2. Classify.** Each term as organiser-facing (the organiser meets it in deciding scope and policies, planning
  and soliciting contributors, facilitating, gathering field notes, coding, analysing or reporting), assistant- or
  builder-facing (it belongs in the contracts, the assistant's rules or the architecture, not the user's glossary), or
  redundant; and its level of abstraction.
- **RS6-G3. Inconsistencies.** Terms used in more than one sense, definitions of uneven scope or depth, and docs or
  messages that use a term against its entry.
- **RS6-G4. Options for the cleanup.** How a small organiser glossary could be organised (for example by the organiser's
  journey, which RS5 and WP29 make the stages), where the other terms would live, and what the terms page and its tests
  would need; each option with its cost. No choice: the cleanup package chooses after WP29.

## Non-goals

- Changing any term, entry or page (the cleanup package does, after WP29).
- The stage words themselves (WP29 defines **stage** and **transition**).
- The ontology's identifiers.

## Deliverables

| Deliverable | Path | Goal |
|---|---|---|
| The readout: inventory, classification, inconsistencies, options | `research/glossary/readout.md` (merged to `dev`) | G1 to G4 |
| The full inventory as data | `spike/glossary` branch | G1, G2 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| RS6-R1 | Every glossary term is classified with its evidence (where it is used); every user-facing term the app uses but the glossary lacks is listed. | The readout; the inventory data |
| RS6-R2 | Each inconsistency names the places that disagree. | The readout |
| RS6-R3 | The readout ends with the options for the cleanup package, each with its cost. | The readout |
| RS6-R4 | No file on `dev` changes except the readout. | git |

## Definition of good enough

RS6-R1 to R4 met.

## Definition of good

The cleanup package can draft the organiser's glossary from the readout alone.

## Agent's defaults

- *(default)* The organiser's journey in the chief engineer's words is the classification's frame until WP29's stages
  replace it.
- *(default)* The readout is at most about 2,000 words, with the inventory as data on the spike branch.

## Blast radius

`research/glossary/` on `dev` (the readout only); everything else on `spike/glossary`. `decisions/log.md`, the board
and metrics.
