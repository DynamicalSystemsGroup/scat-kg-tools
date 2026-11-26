# The "leave no trace" walkthrough, run once (26 November)

The first end-to-end run of `docs/leave-no-trace.md` (WP21-R7), which also covered loading the skill package (R4)
and the session key's handling (R5). Lab material only: a synthetic community-fridge note. The chief engineer did the
app, the key, the trust consent and `done`; the ACE was the hands in Chrome and the coder's voice. The full run record,
with times, is kept outside the repository (it names the chat's address). Words follow `GLOSSARY.md`.

Candidate: tools `dev` 23244b7 (`src/` and `docs/` as c89411e), template `dev` 271c3e9; SCAT Chat built from 23244b7.
Assistant model: tinfoil/gpt-oss-120b. Messages to the assistant: 5.

As the chief engineer said during the run, this option is supported, tested and documented, and is not a routine:
ordinary sessions stop and restart SCAT Chat and keep the chat's entry, skill and agent.

## What the run showed

- **R4, the skill loads.** The published `skills/scat-coding/SKILL.md` (byte-identical to `dev`) was pasted into the
  chat's "Write skill instructions"; the chat parsed its frontmatter and loaded it in the session ("Skill").
- **R5, the key.** While a session ran, the key was in the login keychain and in no process's arguments (`ps`); at
  each Stop the keychain item was deleted, Funnel was off, the container gone and the address dead. A keychain prompt
  at start was not reported.
- **The assistant, with the skill and a saved agent**, did one loop step per reply, offered a brief description, kept
  every proposed edge in the grammar, handed back at each step, and kept its tool through a key change. Compare the
  first live run (`live-run-wp18-r4.md`), where most edges were mis-typed and steps ran together.
- **Temporary chat with a saved agent works**: an agent chosen with the Agent Builder's Select runs inside a temporary
  chat, which then does not appear in history.
- **Everything set up in the platform was removed** (server entry, agent, skill, the uploaded note), and the local
  notes and vault stayed.

## Findings

| ID | Finding | Kind |
|---|---|---|
| L1 | **Blocking, fixed by restarting:** SCAT Chat reused the vault it remembered from 25 November without asking; the window does not say which vault is mounted, and the only way to choose again is the command `change-vault`, which a coder with no terminal cannot run. Found only because the tool refused a fourth group and listed the old vault's groups. | Launcher defect (C10) |
| L2 | The walkthrough's step 2 says "open the app" but not what SCAT Chat is or where it is; the built app is in the repository's `deploy/build`, not in Applications. | Docs, packaging (C10) |
| L3 | The launcher window cannot be minimised; it has Copy key but no Copy address; it does not say it is the MCP server or show its status; it flickers when the key is copied. | Launcher (C10) |
| L4 | The chat's server form has a required "I trust this application" consent and a header-format choice; the walkthrough mentions neither. The new entry stays unconnected until Connect is clicked; the walkthrough has no Connect step or check. | Docs |
| L5 | The chat's skill form requires a Description; the walkthrough does not say so. The skill file's HTML comments show as visible text in the chat. | Docs; skill file |
| L6 | "Upload a skill" opens the Mac's file picker; the paste route was used, as the page allows. | Note |
| L7 | No collections: the file library is a flat list. The page's fallback (attach to the temporary chat) worked. | Docs (answers an open question) |
| L8 | The note attached in the temporary chat stayed in the file library after the temporary chat was deleted; step 43 is needed. | Docs: keep the step, say why |
| L9 | The assistant labelled its steps with the rule ids ("Step A1"); used non-breaking hyphens in names it wrote in text (the files it made had plain ones); did not offer `kind` though asked for "a scenario"; did not quote the check's own result when asked to check. | Skill text (C6, C11) |
| L10 | An agent's tool binding does not survive deleting its server entry (seen on the old agent). | Docs |
| L11 | Deviations by the ACE: steps 27 and 28 written into the page file (full-screen control for Obsidian's folder dialog timed out); step 32 committed with git, not GitHub Desktop (the lab vault is not in Desktop). | Run notes |

The chief engineer's observations in the run are candidates C10 (the launcher as a small, clear local app), C11
(stronger deontic words for the assistant's rules) and C12 (help to fill in node pages as a synthesis across
narratives; a spike first, D-123), quoted in full in `work-packages/candidates.md`.
