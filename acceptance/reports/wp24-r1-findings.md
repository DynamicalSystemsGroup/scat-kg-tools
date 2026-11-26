# WP24 UA-A round 1 (node-page help): findings and proposed dispositions

Candidate: `pm-wp24` after U1 to U5 (evidence, copy-share, A16 and A17, the two prompts; the G6 vault). Testers: t1 Haiku (disallowed copy), t2 Haiku (optional copy), t3 Haiku (required copy), t4 Sonnet control (disallowed copy). Each worked on its own copy of `research/node-pages/vault/<mode>`, two stub node pages and the draft page with the highest copy-share, playing the assistant and the coder in turn, with the documentation pages and the printed MCP prompts. The reports were returned as text (the environment refused writes to the scratch folder); this file is the PM's record of them, condensed, with the numbers as the testers pasted them.

## Void check

- `src/` and `tests/`: no tester read either (each said so; the commands they ran were `scat`, `copy-share`, `evidence`, `status`, `check`, `stub`, `set-status` and printing `prompts.*`).
- Tester slips, not findings about the tool: t1 and t3 stored the command prefix in a shell variable that zsh did not split (exit 127), then wrote the commands out. t1 did not keep the assistant and coder parts apart (it wrote each draft straight into the vault), so its separate review step is missing; t2, t3 and t4 kept them apart, as one agent playing both parts.
- No report void: every claim carries pasted output.

## Pass bar (WP24-R9)

| Line | Result |
|---|---|
| Each tester drafts and accepts three node pages with the assistant's help, a clean check at the end | Met by t1 to t4 (0 errors, the one standing SCAT-NOEDGES warning on `the-data-set-and-the-two-layers`, present before) |
| Blocking findings (stopped short, or a command on a page fails as shown) | None |
| Guesses are findings | Listed below |

Copy-share of the draft page `members-not-replying`: 0.83 before; 0.05 (t4), 0.09 (t1), 0.10 (t2, t3) after the tester's rewrite. Stubs written to 0.01 to 0.14.

## Findings

| Id | Reports | Page and words | Proposed disposition |
|---|---|---|---|
| X1 | t1 F1 | `scat set-status <page> done` succeeded on the command line and so did moving the page back; the refusal of `done` is the MCP server's. The command line is the coder's own tool. | Accept: the assistant's authority is held by the server on the chat path and by the assistant's rules on the IDE path (the assistant's file, "Where it holds"); no change. |
| X2 | t1 F2, t2 F12, t3 F3, t4 F2/F5 | Copy-share names a narrative as a source that does not link the node (`ethnographic-loop` for `members-not-replying`); evidence lists only narratives that link it. Copy-share reads text, evidence follows links. | Fix (docs, one sentence in the copy-share entries, U8): sources are narratives whose text the page repeats, linked or not. |
| X3 | t1 F4, t2 F8, t3 F10, t4 F7 | A stub with a written body stays `stub`; nothing says when it becomes `draft`. The norms page ("Status when you leave a page") already says to set the status. | Accept: the norm covers it; the brief let the tester leave statuses. |
| X4 | t1 F3, t2 F11 | A description that repeats the narrative is flagged by no rule (a norm only). | Accept: by design (norms, "Descriptions"). |
| X5 | t3 F2, t4 F1 | "The top of the copy-share list" is a `done` page; the testers chose the top draft. | Accept: the list covers every node page. |
| X6 | t3 F1 | `scat check concern/renewal-cost-visibility` (path without `.md`) is refused; the fix line does not say `.md`. | Accept as before (the same wording as the earlier rounds); follow-up if wanted. |
| X7 | t2 F6 | `scat stub` on an existing page exits 0 ("unchanged"). | Accept: the contract's wording for unchanged. |
| X8 | t4 F6 | A narrative name and a misspelt name get the same "no node has this name". | Accept. |
| X9 | all | No unlinked stub in the G6 vault, so that case ran on a created probe page (t2, t4: "0 narratives, 0 edges"). | Accept. |
| X10 | t1, t2, t4 | The first Assistant draft for a one-narrative node reads as a summary of that narrative, not a synthesis; each said so and stated that only one narrative tells it, as the norm asks. | Accept: honest for one narrative. |

The synthesis question, in the testers' words: for `members-not-replying` the draft across three or four narratives read as a synthesis and kept the two names as a difference; for one-narrative nodes it reads as a careful summary that names what is thin.
