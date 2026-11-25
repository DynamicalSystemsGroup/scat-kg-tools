# RS3 — Scope of work: chat-path spike

| | |
|---|---|
| **Status** | Approved by the ACE (log D-080). Runs beside WP15. Its live part waits for the chief engineer's sign-ins. |
| **Branch** | `spike/chat-path` off `dev`; never merged into `dev`. The readout is merged into `dev` on its own. |
| **Revert point** | `divergence/D-076` |

## Purpose

Find a workable route for the chat path (`MISSION.md` G14): a coder, with no terminal, using the inference.coop
browser chat with an MCP server built on `scat-kg`, drafting and coding narratives from uploaded field notes, keeping
the work in a private git repository, editing it in Obsidian, generating the views, and locking a version. Pick the
route to build now (WP18), and document another as the preferred long-term route if they differ. Words follow
`GLOSSARY.md`.

## Questions

1. **The chat itself.** What does the inference.coop chat offer a coder: uploading files as a collection, custom
   models or system prompts, MCP servers or other tool servers (and how each is connected), downloading files the chat
   makes? Is it built on Open WebUI, and if so which of its features are switched on?
2. **Reaching the tool.** Where does the MCP server run, and how does the chat reach it: a server the co-op's side
   calls, a server the coder's browser calls on their own machine, or another route? What data passes through it, and
   does that fit the rules for the inputs and the model?
3. **The workflow.** A short, simple loop from uploaded field notes to a narrative page in the private repository and
   back, with as little copying and pasting as the route allows, and with the coder confirming in Obsidian.
4. **No terminal.** How the coder sets up, commits, checks and locks a version (a GitHub Release or GitHub Desktop)
   with no terminal.
5. **Views.** How the MCP server returns the fingerprint view, edge tables, layered view and traces, and where they
   are kept (the private repository).

## Method

- **Offline first:** the public documentation of inference.coop and of the chat software it uses; a throwaway MCP
  server on `spike/chat-path` with one or two `scat-kg` operations, tested locally against the lab vault.
- **Live second, light:** after the chief engineer signs in to inference.coop and GitHub in the browser pane, the ACE
  drives the chat at a human pace, one session at a time, with lab (synthetic) material only, and screenshots each
  step. No load tests, no loops, no parallel sessions.

## Non-goals

- Building the production MCP server or any change to `src/` on `dev` (WP18).
- Any real field material.
- Testing other providers.

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| RS3-R1 | `research/chat-path/readout.md` answers the five questions, each from evidence (documentation cited, commands and screenshots for what was tried), and names the route to build now and, if different, the preferred long-term route, with reasons. At most 1,500 words. | Inspection |
| RS3-R2 | The route works with no terminal for the coder, keeps authority with the coder and the tool (the assistant holds none), and works with no LLM as well (R-19). | The ACE's review against `MISSION.md` |
| RS3-R3 | Only lab material went to inference.coop; use was light and sequential. | The readout's run log |
| RS3-R4 | `python3 work-packages/check_metrics.py --accept RS3` passes. | The check's output |

## Definition of good enough

RS3-R1 to R4 met, and the route is concrete enough for WP18's scope to name its modules from the architecture
document.

## Blast radius

`spike/chat-path` (anything on that branch); on `dev`: `research/chat-path/`, `work-packages/board.md`,
`work-packages/metrics.jsonl`.
