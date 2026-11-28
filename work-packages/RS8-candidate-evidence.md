# RS8 — Scope of work: UX spike on telling a coder when candidate links carry no evidence

| | |
|---|---|
| **Status** | DRAFT. Approval is recorded in `decisions/log.md`, quoting the chief engineer. Rests on D-191. |
| **Branch** | `spike/candidates` off `dev`; never merged into `dev`. The readout is merged into `dev` on its own. |
| **Revert point** | `divergence/D-174` (shared with WP32 to WP35) |

## Purpose

WP34 added candidate links to the layered view and a no-account flag. A candidate is a pair of linked nodes in adjacent
layers that no `Edges told` row joins. The flag fires when a narrative has no text outside its table, because then the
only links are the rows' own ends and every candidate is just an adjacent pair. WP34's PM noted that a narrative whose
prose links no node is in the same state and is not flagged. The chief engineer (typed by the agent, D-191): "ux spike
and consider alternatives. please respect our "mak the right way the easy way and as simple as possible but now simpler
heurisics"". A spike answers questions; it changes nothing that ships.

## Goals

- **RS8-G1. The cases.** On the contract examples, the lab vault and small fixtures, which narratives produce candidates
  that carry evidence (the account links both nodes) and which produce only adjacent pairs, by cause: no account, prose
  with no links, prose linking only some nodes.
- **RS8-G2. The alternatives.** At least these, each shown on the same narratives as a drawing and a table: (a) the flag
  as built (no account text); (b) the flag when the account links no node; (c) no flag, and a candidate is drawn only
  when the account links both of its nodes; (d) a per-candidate mark of whether the account links both nodes; and any
  simpler one the cases suggest.
- **RS8-G3. What the coder does next.** For each alternative, what a coder reading the figure would do, and whether the
  easy reading is the right one (the coder adds a link or a row from the account, and does not add a row because a
  figure suggested it). Read by the ACE as coder, and by the assistant in Claude and in inference.coop.
- **RS8-G4. A recommendation** for the chief engineer, with the cost of each alternative in code, docs and tests.

## Non-goals

- Changing WP34's flag or candidates (a follow-up package does, after the chief engineer chooses).
- New views; the stage model; the glossary words (WP38).

## Open decisions

None. Every item was resolved through the decision loop: the Agent's defaults approved (D-193). Counts: decided 1,
deferred 0, raised 0.

## Deliverables

| Deliverable | Path | Goal |
|---|---|---|
| The readout: cases, alternatives with their figures, the coder's next step, a recommendation | `research/candidates/readout.md` (merged to `dev`) | G1 to G4 |
| Prototype renderings and fixtures | `spike/candidates` branch | G1, G2 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| RS8-R1 | Every case in G1 names the narrative, its cause and its counts (candidates, of which with evidence). | The readout |
| RS8-R2 | Each alternative is shown on the same narratives, as a drawing and a table. | The readout |
| RS8-R3 | Each alternative states what the coder does next and whether that is the right step, from a recorded reading. | The readout |
| RS8-R4 | The recommendation is the simplest alternative that makes the right step the easy one, or says why a simpler one fails. | The readout |
| RS8-R5 | No file on `dev` changes except the readout, the board and metrics. | git |

## Definition of good enough

RS8-R1 to R5 met.

## Definition of good

The chief engineer can choose the flag's meaning, or replace the flag, from the readout alone.

## Agent's defaults

- *(default)* The readout is at most about 1,500 words, with the figures and counts in appendices.
- *(default)* The assistant readings in G3 reuse RS5's trial setup (key gate, short-lived Funnel, torn down after),
  human-paced, at most 10 messages per client, with the ACE as coder, at a sitting the chief engineer chooses; the
  desk parts run first, without it.

## Blast radius

`research/candidates/` on `dev` (the readout only); everything else on `spike/candidates`. `decisions/log.md`, the board
and metrics.
