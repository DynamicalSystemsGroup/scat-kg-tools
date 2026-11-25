# The IDE path

!!! tip "Your next step"
    Open your vault folder in Cursor, or in VS Code with an agent, and ask the assistant to set itself up.

The IDE path is the other way to code with an assistant: in an IDE (Cursor, or VS Code with an agent) with a
terminal inside it. There is no server, so no public link, no key and no launcher. For the chat path with no
terminal, see [The chat path](chat-path.md).

## Set it up

1. Open your vault folder in the IDE. The folder is the one with `scat.toml`.
2. Ask the assistant to set itself up from the setup skill in the template, at
   `.claude/skills/scat-ide-setup/SKILL.md`. The skill points the assistant at the rules in `contracts/assistant.md`
   and at the tool's commands. (That skill is written separately in the template; this page does not check its
   wording.)

## What holds the rules

On the chat path the server cannot set `done`, so the assistant cannot. Here there is no server. The assistant can
run `uv run scat set-status`, because the command cannot tell who types it. So the rules A7 to A12 in
`contracts/assistant.md` hold by two things:

- that file, which the setup skill gives the assistant; and
- you reviewing what the assistant changed: run `git diff` before every commit, and read it.

You still set `done` yourself, after reading the narrative. That is a residual risk, accepted: see
[Coding](coding.md#the-three-actors).

## What stays the same

The [coding loop](coding.md#the-coding-loop) is the same. The assistant drafts and proposes; you decide; the tool
checks. Field notes may go to the assistant's provider, so settle that first: see
[Data, rights and consent](data-and-consent.md).
