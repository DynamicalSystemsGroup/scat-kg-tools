# Plan: the stages on screen in Claude and inference.coop (WP30-R6)

**This is a plan, not a record. Do not contact claude.ai or inference.coop now.** The check is held for a sitting. The
ACE runs it as the coder, with the chief engineer's accounts, after the stage tools (`which_stage`, `set_stage`), the
guide resources and `lifecycle.toml` are built into the server SCAT Chat runs. No key, password or account detail goes
in this file or in its record. No MCP elicitation is used anywhere (the elicitation trials, RS7, are held).

What the check shows: that a person in a chat can find out the project's stage, name it, be refused outside it, and
move it, in both clients, with the stage kept in the vault. The model it follows is `contracts/lifecycle.md`; the
tools and files named here are the ones in `docs/reference/mcp.md` ("Stages").

## Before the sitting

- SCAT Chat rebuilt from tools `dev` with the stage layer, serving a lab vault (a copy of `contracts/examples`), as in
  `drawings-run.md`. The vault is a git folder, so `git status` and `git diff` show every change.
- The vault has no `lifecycle.toml`. Note the vault's `scat.toml` (`stakeholder_group_cap`) before step 6.
- Each client has the SCAT connector added the way `docs/chat-path.md` says (Claude: custom connector with
  `x-api-key`; inference.coop: API Key). Check the client's own tool list: it should show 21 tools, including
  `which_stage` and `set_stage`. The skill is loaded in both.
- A terminal in the vault folder, to read `lifecycle.toml`, `git status` and `git diff` after steps.

## Steps

Run each step in Claude, then in inference.coop, in a fresh chat each time unless the step says otherwise. Type the
prompt as written. After each step, read `lifecycle.toml` and `git status` in the vault, and fill the table at the end.

### 1. No stage recorded

- Prompt: `Run the check on the vault.`
- Look for: the assistant's call is refused with a normal result (not an error); the refusal says no stage is recorded
  and names the five stages, one line each; the assistant relays it and asks which stage the project is in; it does not
  pick one. No `lifecycle.toml` exists afterward. Try also a second prompt, `Show me the status of every page.`: the
  same refusal.

### 2. The coder names a stage

- Prompt: `We are coding.`
- Look for: the assistant calls `set_stage` with `to` as `code` and `by` as the coder's name (the name the ACE gives it
  in the chat; ask it to use `ACE`), and says what it did. `lifecycle.toml` holds `stage = "code"`, `set_by` and
  `set_at`. Then type `What stage are we in?`: the assistant calls `which_stage`, and the answer shows the stage,
  `set_by`, `set_at`, the stage's work, its tools and its exits. Then `Run the check on the vault.` now runs.

### 3. A request outside the stage

- Setup: move to analyse first (`We are analysing.`; from code this is move L5, which advises that every narrative be
  `done`; the move is made and the advisory is relayed).
- Prompt: `Add this edge: mutual-aid-group holds food-spoilage, told by lab-note-community-fridge.`
- Look for: the refusal says `record_edge` is not offered in the analyse stage, names the stage that offers it (code),
  and says a move is the coder's say-so. The assistant relays it in full, does not work around it (no hand-written
  row, no other tool) and offers to move to code only if the coder says so. Nothing is written: `git status` is clean
  apart from `lifecycle.toml`.

### 4. A stage that is not one of the five

- Prompt: `We are in the ideation stage.`
- Look for: the assistant either asks which of the five it means or calls `set_stage` with `to` as `ideation`, which is
  refused and names the five stages. Either way no move: `lifecycle.toml` is unchanged. Then type `We are in the code
  stage.` while already in code: refused (already there), no write.
- Also try a name the five do not hold but sounds like one: `Move to the review stage.` Same result.

### 5. A move with no name

- Setup: in code.
- Prompt: `Move to capture.` (no name given).
- Look for: the assistant does not invent a name. Either it asks who is saying so, or it calls `set_stage` with no
  `by`; the result says nothing moved and a request is pending (a `[pending]` table in `lifecycle.toml`, stage
  unchanged). Then `It is ACE. Move to capture.`: the move is made, `[pending]` is gone, `set_by` is the name given.
  Record which of the two the model did, and whether `which_stage` shows the pending request in between.

### 6. A move back

- Analyse to code (L6): in analyse, `We need to revisit the coding of lab-note-community-fridge. Back to code.` The
  move is made; `set_by` is the name given.
- Code to plan when the group cap is met (L7): set `stakeholder_group_cap` in `scat.toml` to the number of group pages
  the vault holds (the file is the setup person's; the ACE edits it for this check and restores it afterward). In
  code, type `Make a new stakeholder group page called night-shift-neighbours.` Look for: `stub` refuses because the
  cap is met; `which_stage` now shows L7 as holding (a detect predicate, advice only), and says the setup person
  decides. Type `Move to plan.`: the move is made with `by` as the name given (the server does not check the role; say
  so in the notes). Then the stub is allowed in plan only after the setup person raises the cap; type `Make that group
  page.` before and after raising the cap to see both.
- Look for: in every move, who decides is named as a reminder, and the assistant never proposes a move as already
  decided.

### 7. A restart and a new chat

- Setup: in a stage other than the first one tried (for example capture).
- Stop SCAT Chat and start it again (or restart the server container), then open a new chat in each client. Type `What
  stage are we in?`
- Look for: the same stage, `set_by` and `set_at` as before, with no one having named it in the new chat. Then a tool
  the stage offers works, and one it does not is refused. `git log` or `git diff` of `lifecycle.toml` shows each move.

### 8. inference.coop, where it differs

- Run steps 1 to 7 there. Note two behaviours the earlier trials found:
  - inference.coop runs one server session for all chats, so a stage kept in the session would leak between chats;
    here the stage is in the vault, so two chats open at once must show the same stage. Move the stage in one chat and
    ask `What stage are we in?` in the other.
  - The model's account of its own tools may be stale (an RS5 trial finding). If the model says a tool is missing or
    names one that does not exist, check the client's own tool list, not the model's words, and record both.
- Look for: refusals relayed in full, and whether `isError`-style failures are shown differently (the server sends
  normal results, so none should appear).

### 9. What to record

Fill this table, one row per step, and write the findings below it. Keep what each client did, not what it should have
done. No key, address or account detail goes in.

| Step | Claude | inference.coop | Notes |
|---|---|---|---|
| 1. No stage recorded | | | |
| 2. Name a stage; `which_stage` | | | |
| 3. A request outside the stage | | | |
| 4. A stage that is not one of the five | | | |
| 5. A move with no name | | | |
| 6. A move back (L6, L7) | | | |
| 7. Restart and a new chat | | | |
| 8. inference.coop: two chats, stale tool account | n/a | | |

Findings to write: whether each client relayed every refusal in full; whether any assistant moved the stage without the
coder saying so (a failure); what name it gave as `by`; whether the new chat found the stage with no help; any call
the tool list showed that the model denied; what the pending request looked like to the coder; and anything in
`docs/chat-path.md` ("Stages") that did not match what the coder saw.
