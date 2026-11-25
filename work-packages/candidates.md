# Later-package candidates

Work the chief engineer or a run has surfaced that is **not yet scoped**. Nothing here is approved or decided. Whoever
scopes a package starts here, reads the source each item points to (the chief engineer's words are quoted there in
full, as typed), and turns the items into goals, requirements and non-goals at the approval gate. Words follow
`GLOSSARY.md`. Add items as they come up; strike an item through when a scope takes it, naming the package.

**C1 to C8 are taken by WP21 (D-114), all in v0.1 (D-102, D-103).**

## From the chat-path live run, 25 November (`acceptance/chat-path/live-run-wp18-r4.md`)

| ID | Candidate | What it touches | Source |
|---|---|---|---|
| C1 | **The "Edges told" table reads as subject, predicate, object.** Order the columns `from \| type \| to \| note` so a row reads "parents holds bike-safe-for-children"; check every edge name reads in that direction; state a skimmability requirement. The edge names already run that way, so most of it is the column order. | Layout contract (D-088), the tool's table writer and reader, the template and range vaults, docs, the skill | "For later revisions", first quote |
| C2 | **Normative levels for coding a narrative.** Coded = at least one declared node; the expected shape is a coherent story plus a set of nodes and edges, not necessarily connected (worth comes from recurrence across narratives, assembled in the layered view); the table is the "shall"; links in the account text at most a "may". Give a lone node (no edge) one conformant place to be declared. | Page contracts, rule catalogue (SCAT-MENTION is a warning today, stronger than "may"), glossary ("link"), coding guide | "For later revisions", second to fourth quotes |
| C3 | **Show what `done` needs while a page is still a stub.** `description` is silent at `stub` and warns only at `draft`, so a coder who finishes a stub in one sitting meets it only as the error at `done`. Nothing forces `draft`; the fix is the catalogue row, not the status rules. | Rule catalogue (Status behaviour table), checks, tests | On F14 |
| C4 | **Status is set when the coder leaves a page.** `done` if finished, `draft` if not; `draft` marks unfinished work, not a step to pass through. | Coding guide, walkthroughs, the skill (end of session: name the pages to tag, offer `draft`; `done` stays the coder's) | "His model of status" |
| C5 | **Descriptions are brief and do not repeat the account.** The `done` error for a missing `description` is intended, like a required commit message; on the chat path the assistant may offer one. Writing the account and the description is a mixed loop, coder-first or assistant-first, any number of rounds; the coder's move to `done` validates the content. | Coding guide, chat-path guide, the skill | "On the `description` error", and the chief engineer's choice after it |
| C6 | **Ship the assistant's rules as a chat skill and set up a saved agent.** The chat (LibreChat) has Skills and an Agent Builder; the guide uses neither. The skill also needs the edge grammar (F8), `kind` (F12), one step per reply (F9) and an offered `description` (C5). Agents start from the Agent Builder's Select on this instance. | WP18 deliverables (`contracts/assistant.md` as a SKILL.md), `docs/chat-path.md` | F5, F6, F8, F9, F12 |
| C8 | **A session's full life cycle in the chat-path guide: start, use, stop, clean up.** Clean-up covers the server entry (done in 8d620fe), the uploaded field notes (delete them from the chat's file library), and the conversation (delete it, or use the chat's temporary mode from the start when the history should not be kept; inference.coop shows a "Temporary Chat" control, not yet tried). | `docs/chat-path.md`, the walkthroughs, `docs/data-and-consent.md` | The chief engineer, 25 November, quoted below |
| C7 | **The session key shows in the process list** while the app runs (passed as a dialog argument). | `deploy/` launcher | F15 |

Process lesson from the same run, kept in the ACE's own notes and here for workers: steps that need no judgement, sign-in
or key (copying between apps, pasting an accepted draft, opening a vault) are done by whoever drives the run, not
handed to the chief engineer.

C8, the chief engineer's words (25 November, quoted as typed; recorded by the ACE):

> "a full life cycle for this may include spinning up, using and tearing down (and cleaning up) after a session. in the
> event that we don't want to save the conversation history we may also include using the ephemeral chat mode. and if
> we are uploading field notes we may also want to delete/remove the collection from the AI tool as part of the tear
> down"

C8, refined by the chief engineer the same day (quoted as typed; recorded by the ACE):

> "you can keep them locally on my machine. deleting them is not delete them everywhere its delete them in the
> inference.coop environment. The point i am making is an information management lifecycle one. in the event that
> we're in an "approved chatbot only" policy. Plus another candidate project data policy is a retention policy which
> in our worked case i want to support an AI platform non retention policy, specifically that involves uploading a
> collection, instancing the MCP server, uploading the field notes as a collection, performing the workflows using
> any other agents, prompts, tools excetera that need to be configured. performing the coding work then tearing
> everything back down. I am not suggesting that this level of facilities scrutiny is always required but we are
> demonstrating (and testing) that it is supported"

As the ACE reads it: C8 is an information-management life cycle the release should **demonstrate and test**, not
require of every coder. Under an "AI platform non-retention" project data policy, a session sets up everything it
needs in the chat platform (the MCP server entry, the field notes uploaded as a collection, any agents, prompts,
skills or tools), does the coding, and then removes all of it from the platform. Local copies on the coder's machine
are kept. It also serves an "approved chatbot only" policy.

## From the chief engineer, 25 November (D-116)

| ID | Candidate | What it touches | Source |
|---|---|---|---|
| C9 | **A commit is the trigger to read written content into the knowledge graph.** Uncommitted edits are scratch work; committing them via git is the explicit signal that the content should be read and the knowledge graph updated. Not in v0.1 unless the chief engineer says so. | The coding guide and norms, the views (what they read: working tree or committed state), the chat-path life cycle | D-116 |
