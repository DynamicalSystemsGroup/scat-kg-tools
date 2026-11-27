---
provider: Codex
---

# The IDE path

!!! tip "Your next step"
    Read "What this path needs", then follow the worked example with Codex.

The IDE path is the way to code with an assistant that sits in your editor, or in a terminal beside it, and works on
the files of your vault. There is no server, so no public link, no key and no launcher. For the chat path with no
terminal, see [The chat path](chat-path.md).

## What this path needs

Any setup of this path has five parts:

- **An IDE or a command-line agent** that reads a project's instructions file when it starts. Cursor, VS Code with an
  agent extension and a command-line agent all qualify.
- **The tools installed in the vault.** Run `uv sync` in the vault folder, as in [Getting started](getting-started.md),
  so `uv run scat check` works.
- **The vault opened as the project.** Open the folder that holds `scat.toml`, so the agent reads the vault's own
  instructions.
- **The instructions that tell it what it is not allowed to do.** The template carries them: `AGENTS.md` at the vault's root
  points the agent to `.claude/skills/scat-ide-setup/SKILL.md`, which holds the assistant's rules from
  `contracts/assistant.md`.
- **You keeping interpretation.** The assistant drafts and proposes; you decide; the tool checks.

There is no server here to refuse a change, so the rules hold by two things: the instructions file, and you reviewing
what the assistant changed. Run `git diff` before every commit and read it. The assistant can run
`uv run scat set-status`, because the command cannot tell who types it, so you set `done` yourself, after reading
the narrative. See [Coding](coding.md#the-three-actors).

## Worked example: Codex

Codex is OpenAI's coding agent. It runs as an extension in VS Code, Cursor and Windsurf, or as a command in a
terminal. Use either one; the steps below say which.

1. **In an editor:** Install the Codex extension in VS Code, Cursor or Windsurf. The Codex icon appears in the
   sidebar.
2. **In an editor:** Open your vault folder (the one with `scat.toml`) as the project, then select the Codex icon. If
   the icon is missing, run "Codex: Open Codex Sidebar" from the Command Palette. A chat opens on your vault.
3. **In Codex:** Sign in when it asks, the first time you use it. The chat is then ready for your vault.
4. **In Codex:** Ask: "Set yourself up for this vault." Codex reads `AGENTS.md` at the vault's root when the session
   starts, follows it to `.claude/skills/scat-ide-setup/SKILL.md`, runs `uv sync` and then `uv run scat check`, and
   reads you the tool's own result.
5. **In Codex:** Ask: "What are you not allowed to do here?" Codex answers from the skill: it does not set `done`,
   does not run `set-status`, and does not write a narrative's text through the tool.

To use a terminal instead of an editor, replace steps 1 and 2 with this:

**In a terminal:** Install the command with `curl -fsSL https://chatgpt.com/codex/install.sh | sh`, go to your vault
folder, and run `codex`. Codex starts on the vault; continue from step 3.

Codex also reads an `AGENTS.md` in any folder between the vault's root and the folder you work in, so a folder can add
its own instructions. It stops reading once the instructions pass 32 KiB in all.

Codex can also connect to a server through MCP, in its settings. The IDE path does not need it: the assistant runs
the `scat` commands in the vault itself. Cursor, VS Code with another agent, and any command-line agent that reads
`AGENTS.md` follow the same steps from step 2.

If your data policy is strict, settle first what can go to the assistant's provider: see
[Data, rights and consent](data-and-consent.md).
