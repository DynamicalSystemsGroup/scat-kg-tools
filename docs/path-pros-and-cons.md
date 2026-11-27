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

## By hand

- **Pros:** nothing leaves your computer and no AI provider is involved; every file is written by you or by the tool's
  commands; no setup beyond [Getting started](getting-started.md).
- **Cons:** all the drafting, linking and edge recording is yours, which takes longer across many narratives; you type
  the tool's commands in a terminal.

## An AI chatbot

- **Pros:** you code in a chat window, with no terminal (setting up, in [Install once](chat-path.md#install-once),
  uses one); the assistant drafts, proposes links and records edges for you; the server holds the rules, as above.
- **Cons:** what you share in the chat, such as field notes and narrative text, goes to the chat's provider, so your
  data policy has to allow it; the most setup of any path (SCAT Chat, a container runtime, Tailscale); the server's
  address is public while a session runs, and only the session key lets a request through; each session has a new
  key to paste into the chat.

## An AI chatbot, leave no trace

- **Pros:** everything the chatbot path gives, and nothing stays on the platform afterwards: a temporary chat, the
  field notes as one collection, and the server entry, agent and skill removed at the end.
- **Cons:** the content still passes through the platform during the session; the clean-up is yours, every session,
  so there are more steps.

## An AI IDE

- **Pros:** little to set up: an editor with an agent, and no server, public address or key; the agent runs the
  tool's commands in the vault and reads the vault's rules from `AGENTS.md`.
- **Cons:** nothing enforces the rules, as above, so you review every change; the files the agent reads go to its
  provider, so your data policy has to allow it.

## A local LLM

- **Pros:** nothing leaves your computer; the server holds the rules, as above.
- **Cons:** you supply the model and the hardware: several GB of memory, slow turns on an older Mac, and no GPU in
  Docker on a Mac; a small model may answer from its own guesses instead of calling the tool; setting up uses a
  terminal and Docker.
