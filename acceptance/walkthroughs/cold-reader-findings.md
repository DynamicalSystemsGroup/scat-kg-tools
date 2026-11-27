# WP25-U11: cold readers (WP25-R7), round 1

Three Haiku testers, isolated from the code: each had only a copy of `docs/` and `mkdocs.yml`, no `src/`, `tests/` or
other worktrees, no accounts, and no sign-ins. Guesses count as findings. These are the PM's condensed records of the
testers' returned reports, not the originals (weaker evidence, as in WP24's D-150 ruling 5).

| Tester | Task | Reached |
|---|---|---|
| T1 | choose a path from `coding-paths.md`; follow the by-hand walkthrough on a scratch clone of the template | Chose by hand. Reached the page's end state (whole-vault check, no problems; the misspelt-link output matched the page). Obsidian steps not driven (a script edited the files). |
| T2 | choose a path for a strict local data policy; read `local-llm.md` as if about to follow it (nothing started or pulled) | Chose a local LLM. Understood the example is one way. Could follow all but steps 5, 7, 8, 10 from the page alone. |
| T3 | for three situations (Claude chat, strict policy, IDE with Codex) say from the pages what they would need and do | Chose correctly in each; listed needs and steps; stopped where the pages said to. |

## Findings and what was done (fix round, branches wp25/fix3 to fix6)

| # | Finding | Disposition |
|---|---|---|
| 1 | local-llm: a new session makes a new key but Open WebUI keeps the old one (401); "key lives only in this terminal" conflicts | fix (fix4) |
| 2 | local-llm: `uv run scat check` run from the vault folder is not in the scat project | fix (fix4) |
| 3 | local-llm: Function Name Filter List `check, status` vs tool shown as `scat_check` | fix (fix4) |
| 4 | local-llm: clone and compose folder not named; Docker memory setting not located; first-start download and time; "nothing leaves" vs the helper-model download | fix (fix4) |
| 5 | by-hand: step 4's example line says something the narrative does not support; where to put it; GitHub sign-in assumed; "you are inside it" ambiguous | fix (fix3) |
| 6 | coding-paths: no-AI question last; "data policy" unglossed | fix (fix3) |
| 7 | ide: needs says the coder runs `uv sync`, the example has Codex run it; piped remote install script; no stop; `scat check` undefined | fix (fix6) |
| 8 | chat-path Claude steps (remove and re-add a connector) vs the generic section (keep the entry); mixed plan wording; undefined terms | fix (fix5) for the new sections; the generic section is WP26's |
| 9 | chat-path and leave-no-trace are long (570 lines, 57 steps); "untested" status notes; the public Tailscale record not mentioned in leave no trace; step 46 vs step 54 on attached notes; jargon (narrative, node, edge) undefined on these pages; Obsidian-only claims | WP26 (the sweep and the clarity rounds): the status notes are D-146's; the rest is outside this package's pages' scope |
| 10 | by-hand: `coding.md` is 1,053 lines; "Edges told" headings repeat | WP26 |
