# RS5 — Scope of work: research spike on the lifecycle as a state machine

| | |
|---|---|
| **Status** | Approved by the chief engineer (log D-163). Rests on D-157 and D-162. Feeds WP29. |
| **Branch** | `spike/lifecycle` off `dev`; never merged into `dev`. The readout is merged into `dev` on its own. |
| **Revert point** | `divergence/D-163` (shared) |

## Purpose

Gather what WP29 needs to design the lifecycle model the chief engineer set out (D-162): "a small finite state machine
where each state is a stage, and each stage has a narrower set of expected inputs, outputs, tools and skills that keep
the agent on track. predicates help detect or request state-transistions", "as simple as possible but no simpler",
with "a concrete instance", where stage may travel in "the header for messages to the mcp server", and where an
unknown stage gets "a result asking for clarification". A spike answers questions; it builds nothing that ships.

## Goals

- **RS5-G1. The formal model's smallest sufficient form.** How comparable non-linear processes are modelled as state
  machines (states, transitions, guards or predicates, inputs and outputs per state), from qualitative-analysis cycles,
  action and design research loops and workflow state machines, read for principles; what the smallest form is that
  still carries stage-scoped inputs, outputs, tools and skills and backward moves.
- **RS5-G2. Our own instance's raw material.** The stages, inputs, outputs, tools, prompts, skill sections and
  transitions that the flow page, the mission's journeys J1 to J10, the coding loop, the views and the 27 November runs
  already imply, laid out for WP29 to choose from, without choosing.
- **RS5-G3. How stage reaches the server.** The options for carrying stage on MCP requests (a request header, a session
  value set by a tool, an argument on each call), and for the server to answer an unknown stage with a request for
  clarification, each tried against the MCP SDK the server uses, in a throwaway server on the spike branch.
- **RS5-G4. How the server can scope what it exposes.** Whether a stage can change the listed tools, prompts and
  resources mid-session (the protocol's list-changed notifications) and whether Claude, inference.coop and VS Code's
  Copilot honour it; what to do where a client does not (refuse an out-of-stage call with a clarification result).
  Includes the chief engineer's option (typed by the agent): "if forced to, we could make it so each stage is its own
  MCP server, and that Scat-lab is actually a mini app hosting those servers together plus one additional top level
  server that handles the state machine and routes to the server for the current state. that would be a clean
  functional decomposition". The spike tries it: whether the top-level server can route (proxy) to per-stage servers
  inside one client connection, whether that avoids or only moves the need for a mid-session tool-list change, and what
  hosting several servers costs in SCAT Chat (ports, keys, one public address or several).
- **RS5-G5. Predicates.** Which transition predicates the existing tools can already evaluate (`status`, `check`, the
  views, `scat.toml`), and which need the user's word.

## Non-goals

- Choosing the model or its instance (WP29 does, at his gate).
- Any change on `dev` beyond the readout.

## Deliverables

| Deliverable | Path | Goal |
|---|---|---|
| The readout: findings per goal, options with evidence, open questions for WP29 | `research/lifecycle/readout.md` (merged to `dev`) | G1 to G5 |
| The throwaway server experiments and their notes | `spike/lifecycle` branch only | G3, G4 |
| The client trials, with screenshots kept outside the repository | the readout's evidence section | G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| RS5-R1 | Each goal has findings with sources (cited literature, code tried, or a client trial) and states what is not known. | The readout |
| RS5-R2 | Each way of carrying stage (G3) is tried in the spike server and reported as works, partly works or does not, with the SDK version. | The readout; the branch |
| RS5-R3 | For each of Claude, inference.coop and VS Code's Copilot, the readout says whether a mid-session change of tools is honoured, from a trial. | The readout |
| RS5-R3b | The per-stage-servers-with-a-router option is tried in the spike server and compared with a single stage-scoped server on the same questions (client support, routing, hosting cost). | The readout; the branch |
| RS5-R4 | The readout ends with the questions WP29 must decide, each with its options. | The readout |

## Definition of good enough

RS5-R1 to R4 met.

## Definition of good

WP29 can write the model and its instance without further research, and every choice it makes has evidence behind it.

## Agent's defaults

- *(default)* The client trials (G4) use the chief engineer's accounts and keys, with the ACE as coder, human-paced.
- *(default)* Literature is read for principles and cited; nothing is copied into the tools.
- *(default)* The readout is at most about 2,500 words, with the evidence in appendices.

## Blast radius

`research/lifecycle/` on `dev` (the readout only); everything else on `spike/lifecycle`. `decisions/log.md`, the board
and metrics.
