# Pros and cons of each path

!!! tip "Your next step"
    Read the row for each path that fits your data policy, then open its walkthrough from [Coding paths](coding-paths.md).

Every path gives the same result: the same nodes, edges and checks, and you own the interpretation. The paths differ
in what leaves your computer, how much there is to set up, and what stops an assistant from writing what only the
tool or you should write.

## How each path holds the rules

The tool writes some things itself: the rows of an "Edges told" table (`record-edge`), stub pages and index files. You
write others: a narrative's text, a node page's body, and `status: done`. An assistant should do neither by hand.

| Path | What stops an assistant writing what it should not |
| --- | --- |
| [By hand](coding.md) | There is no assistant. |
| [An AI chatbot](chat-path.md) | The assistant reaches your vault only through the SCAT server's tools. It cannot write a file the tools do not write, and the server refuses to set a page to `done` or move one out of it. |
| [Leave no trace](leave-no-trace.md) | The same as the chatbot: it uses the same server. |
| [An AI IDE](ide.md) | Only its instructions and your review. The agent has your vault's files and a terminal, so it can hand-write a table row or a page, or run `set-status`. Read `git diff` before every commit. |
| [A local LLM](local-llm.md) | The same as the chatbot: the model reaches your vault through the same server. |

## What the model sees in a drawing

A drawing is made for you to look at. Whether the assistant's model can look at it too depends on the path. Each
path's list below has a **Drawings** line. Where a line says what a model receives, it names the run record it rests
on, in `acceptance/walkthroughs/`; the IDE and local LLM lines say what the tool returns, since the client decides what
its model does with it. Whatever the path, a model that cannot see the picture can read the same drawing as a table or
as SVG text: ask for `output` `table` or `both`, or for `format` svg. See [Analysis](analysis.md#drawings).

## By hand

- **Pros:** nothing leaves your computer and no AI provider is involved; every file is written by you or by the tool's
  commands; no setup beyond [Getting started](getting-started.md).
- **Cons:** all the drafting, linking and edge recording is yours, which takes longer across many narratives; you type
  the tool's commands in a terminal.
- **Drawings:** you look at the picture yourself, from the notebook or `uv run scat draw`; there is no model.

## An AI chatbot

- **Pros:** you code in a chat window, with no terminal (setting up, in [Install once](chat-path.md#install-once),
  uses one); the assistant drafts, proposes links and records edges for you; the server holds the rules, as above.
- **Cons:** what you share in the chat, such as field notes and narrative text, goes to the chat's provider, so your
  data policy has to allow it; the most setup of any path (SCAT Chat, a container runtime, Tailscale); the server's
  address is public during a chat run, and only the session key lets a request through; each chat run has a new
  key to paste into the chat.
- **Drawings:** the chat shows you the picture the tool returns. In claude.ai, the model received the image and
  described it in the recorded run (`acceptance/walkthroughs/mvc-loop-claude.md`). In inference.coop's chat, the chat's
  default model (`tinfoil/deepseek-v4-1-flash`) received nothing from a PNG, so it could not look at the drawing,
  though it read an SVG as text; ask it for the table or for `format` svg
  (`acceptance/walkthroughs/analysis-session-inference-coop.md`).

## An AI chatbot, leave no trace

- **Pros:** everything the chatbot path gives, and nothing stays on the platform afterwards: a temporary chat, the
  field notes attached to it and then deleted, and the server entry, agent and skill removed at the end.
- **Cons:** the content still passes through the platform during the chat run; the clean-up is yours, every chat run,
  so there are more steps.
- **Drawings:** this is the chatbot path with the same server, and its walkthrough uses inference.coop's chat, so the
  inference.coop line above applies; there is no separate run of this path
  (`acceptance/walkthroughs/analysis-session-inference-coop.md`).

## An AI IDE

- **Pros:** little to set up: an editor with an agent, and no server, public address or key; the agent runs the
  tool's commands in the vault and reads the vault's rules from `AGENTS.md`.
- **Cons:** nothing enforces the rules, as above, so you review every change; the files the agent reads go to its
  provider, so your data policy has to allow it.
- **Drawings:** `uv run scat draw` writes a PNG or an SVG file you name, and the view commands print the table. An
  SVG file and the table are text; whether an agent can see a PNG is the IDE's. For a model that cannot, ask for the
  table or an SVG file. Through `scat-mcp --stdio`, the tools return as in the [MCP server
  reference](reference/mcp.md#drawings): a PNG as image content, an SVG as text, the table as JSON text.

## A local LLM

- **Pros:** nothing leaves your computer; the server holds the rules, as above.
- **Cons:** you supply the model and the hardware: several GB of memory, slow turns on an older Mac, and no GPU in
  Docker on a Mac; a small model may answer from its own guesses instead of calling the tool; setting up uses a
  terminal and Docker.
- **Drawings:** the server returns a plot as MCP image content (`png`) or as text (`svg`), and the table as JSON text.
  Whether the model sees a PNG is up to its client and the model. If it cannot, ask for `output` `table` or `both`,
  or for `format` svg.
