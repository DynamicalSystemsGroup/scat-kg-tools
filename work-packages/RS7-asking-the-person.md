# RS7 — Scope of work: research spike on how a tool asks the person

| | |
|---|---|
| **Status** | DRAFT. Approval is recorded in `decisions/log.md`, quoting the chief engineer. Feeds WP29 (how the server asks the coder for a stage or a decision) and WP31 (the assistant's habits). |
| **Branch** | `spike/asking` off `dev`; never merged into `dev`. The readout is merged into `dev` on its own. |
| **Revert point** | `divergence/D-163` (shared) |

## Purpose

RS5's client trials tried MCP elicitation once: the SDK's `elicit_form`, one form, sent mid-call. It hung in Claude
and was absent in inference.coop. The chief engineer (typed by the agent): "seems like we must be missing something.
this is a common pattern in LLM based work. we may need a spike to understand standards and best practices". A spike
answers questions; it builds nothing that ships.

## Goals

- **RS7-G1. The standards.** What the MCP specification (each version in use) defines for a server to ask the person:
  elicitation (form and any other modes), its capability declaration, timing and transport requirements, and any
  related mechanisms, such as sampling, tool annotations and confirmation hints.
- **RS7-G2. The practice.** The established patterns in LLM tools for pausing to ask the person: the assistant asking in
  its reply, client-side approval of tool calls, confirm-then-write (a two-step tool), and protocol elicitation. For each:
  who sees the question, who answers, what is recorded, and where it is used today.
- **RS7-G3. What went wrong in our trial.** Whether Claude's hang came from the client or from our server (transport,
  timing, schema, session), shown by reproducing it and by trying corrected variants.
- **RS7-G4. Options for WP29 and WP31.** How the server asks the coder for a stage or a decision, per client (Claude,
  inference.coop), each option with its evidence and cost. No choice: WP29 chooses.

## Non-goals

- Building the server's stage handling (WP30).
- Stronger proof of whose call a change was (C17, deferred in D-179).
- Copilot (passed in D-180).

## Open decisions

None. Every item was resolved through the decision loop: O1 (client trials) decided, included (D-182); the Agent's
defaults approved (D-184). Counts: decided 2, deferred 0, raised 0.

## Deliverables

| Deliverable | Path | Goal |
|---|---|---|
| The readout: standards, practice, our trial's cause, options | `research/asking/readout.md` (merged to `dev`) | G1 to G4 |
| Variant servers and their notes | `spike/asking` branch | G3 |
| Client trials in Claude and inference.coop, human-paced, with the ACE as coder | the readout's evidence section; screenshots outside the repository | G2, G3 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| RS7-R1 | Every claim about a standard cites the specification page and version it comes from. | The readout |
| RS7-R2 | Each pattern in G2 names a real product or document that uses it. | The readout |
| RS7-R3 | G3 ends in a stated cause with its evidence, or says what is still unknown and why. | The readout |
| RS7-R4 | The readout ends with WP29's options, each with its cost and the clients it works in. | The readout |
| RS7-R5 | No file on `dev` changes except the readout. | git |
| RS7-R6 | Each pattern tried in a client is recorded with what the person saw and what the server received. | The trial record |

## Definition of good enough

RS7-R1 to R6 met, with the client trials recorded.

## Definition of good

WP29 can choose how the server asks the coder, knowing what each client will actually show the person.

## Agent's defaults

- *(default)* The readout is at most about 2,000 words, with sources and variant results in appendices.
- *(default)* Local experiments use the RS5 spike server and the SDK client, on 127.0.0.1.
- *(default)* Any client trial reuses RS5's setup (key gate, short-lived Funnel, torn down afterward), with the ACE as coder.

## Blast radius

`research/asking/` on `dev` (the readout only); everything else on `spike/asking`. `decisions/log.md`, the board and
metrics.
