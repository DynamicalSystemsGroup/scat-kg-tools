# Later-package candidates

Work the chief engineer or a run has surfaced that is **not yet scoped**. Nothing here is approved or decided. Whoever
scopes a package starts here, reads the source each item points to (the chief engineer's words are quoted there in
full, as typed), and turns the items into goals, requirements and non-goals at the approval gate. Words follow
`GLOSSARY.md`. Add items as they come up; strike an item through when a scope takes it, naming the package.

## From the chat-path live run, 25 November (`acceptance/chat-path/live-run-wp18-r4.md`)

| ID | Candidate | What it touches | Source |
|---|---|---|---|
| C1 | **The "Edges told" table reads as subject, predicate, object.** Order the columns `from \| type \| to \| note` so a row reads "parents holds bike-safe-for-children"; check every edge name reads in that direction; state a skimmability requirement. The edge names already run that way, so most of it is the column order. | Layout contract (D-088), the tool's table writer and reader, the template and range vaults, docs, the skill | "For later revisions", first quote |
| C2 | **Normative levels for coding a narrative.** Coded = at least one declared node; the expected shape is a coherent story plus a set of nodes and edges, not necessarily connected (worth comes from recurrence across narratives, assembled in the layered view); the table is the "shall"; links in the account text at most a "may". Give a lone node (no edge) one conformant place to be declared. | Page contracts, rule catalogue (SCAT-MENTION is a warning today, stronger than "may"), glossary ("link"), coding guide | "For later revisions", second to fourth quotes |
| C3 | **Show what `done` needs while a page is still a stub.** `description` is silent at `stub` and warns only at `draft`, so a coder who finishes a stub in one sitting meets it only as the error at `done`. Nothing forces `draft`; the fix is the catalogue row, not the status rules. | Rule catalogue (Status behaviour table), checks, tests | On F14 |
| C4 | **Status is set when the coder leaves a page.** `done` if finished, `draft` if not; `draft` marks unfinished work, not a step to pass through. | Coding guide, walkthroughs, the skill (end of session: name the pages to tag, offer `draft`; `done` stays the coder's) | "His model of status" |
| C5 | **Descriptions are brief and do not repeat the account.** The `done` error for a missing `description` is intended, like a required commit message; on the chat path the assistant may offer one. Writing the account and the description is a mixed loop, coder-first or assistant-first, any number of rounds; the coder's move to `done` validates the content. | Coding guide, chat-path guide, the skill | "On the `description` error", and the chief engineer's choice after it |
| C6 | **Ship the assistant's rules as a chat skill and set up a saved agent.** The chat (LibreChat) has Skills and an Agent Builder; the guide uses neither. The skill also needs the edge grammar (F8), `kind` (F12), one step per reply (F9) and an offered `description` (C5). Agents start from the Agent Builder's Select on this instance. | WP18 deliverables (`contracts/assistant.md` as a SKILL.md), `docs/chat-path.md` | F5, F6, F8, F9, F12 |
| C7 | **The session key shows in the process list** while the app runs (passed as a dialog argument). | `deploy/` launcher | F15 |

Process lesson from the same run, kept in the ACE's own notes and here for workers: steps that need no judgement, sign-in
or key (copying between apps, pasting an accepted draft, opening a vault) are done by whoever drives the run, not
handed to the chief engineer.
