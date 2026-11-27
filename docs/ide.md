---
provider: Copilot
---

# The IDE path

!!! tip "Your next step"
    Read "What this path needs", then follow the worked example with Copilot in VS Code.

The IDE path is the way to code with an assistant that sits in your editor, or in a terminal beside it, and works on
the files of your vault. There is no server, so no public link, no key and no launcher. For the chat path with no
terminal, see [The chat path](chat-path.md).

## What this path needs

Any setup of this path has five parts:

- **An IDE or a command-line agent** that reads a project's instructions file when it starts. Cursor, VS Code with an
  agent extension and a command-line agent all qualify.
- **The tools installed in the vault.** You need `uv` on your computer, as in [Getting started](getting-started.md). The
  assistant runs `uv sync` in the vault folder at set-up; you read what it reports. You can run it yourself instead.
  Either way, `uv run scat` commands are typed in the vault folder. [`scat check`](reference/cli.md#scat-check)
  is the tool's test of whether the vault is well formed.
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

## The stage on this path

A project is in one stage at a time: plan, capture, code, analyse or report. The stage is not a
page's status. On this path the stage is advisory, because no server refuses a call outside it. The assistant reads
the guides with the tool's own command, and you say which stage the project is in:

```bash
uv run scat guide
uv run scat guide code
```

The first prints the five stages and the moves between them. The second prints one stage's guide: what the work is,
what it needs and makes, which tools it offers, and where it can go next. The assistant offers only the work and the
tools of the stage you name, and a move to another stage is yours to say. If your vault has a `lifecycle.toml` at its
root, the assistant reads the stage from it. The file needs only one line, `stage = "code"`; `set_by` and `set_at` are optional.

## Worked example: Copilot in VS Code

GitHub Copilot in VS Code is the example here; another IDE agent that reads project instructions, such as Codex or
Cursor's agent, works the same way, from step 3.

Copilot is GitHub's coding assistant. Recent versions of VS Code have its chat built in; you sign in to GitHub to use
it, and GitHub's own pages list its plans.

1. **In an editor:** Open VS Code, choose **File** > **Open Folder**, and open your vault folder (the one with
   `scat.toml`). The vault's files are listed in the sidebar.
2. **In an editor:** Open the chat: click the chat icon in the title bar, or press Ctrl-Cmd-I. If VS Code asks you to
   sign in to GitHub for Copilot, do so. The chat shows a box, "Chat with Copilot".
3. **In Copilot:** Under the box, set the mode to **Agent**. Agent mode can run commands in the vault; it asks you
   before each one, and you approve it.
4. **In Copilot:** Ask: "Set yourself up for this vault." Copilot reads `AGENTS.md` at the vault's root, follows it to
   `.claude/skills/scat-ide-setup/SKILL.md`, asks to run `uv sync` and then `uv run scat check`, and reads you the
   tool's own result, such as "attribution mode: disallowed; no problems".
5. **In Copilot:** Ask: "What are you not allowed to do here?" Copilot answers from the skill: it does not set `done`
   or run `set-status`, does not write a narrative's text through the tool, does not hand-write rows of an
   "Edges told" table, and does not commit or push.

To end a session, close the chat. Then run `git diff` in the vault folder and read what changed before you commit.

Copilot in VS Code can also connect to a server through MCP. The IDE path does not need it: the assistant runs the
`scat` commands in the vault itself.

If your data policy is strict, settle first what can go to the assistant's provider: see
[Data, rights and consent](data-and-consent.md).
