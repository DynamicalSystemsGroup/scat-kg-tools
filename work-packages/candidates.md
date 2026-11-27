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
| C7 | **(Done by WP21-U8, D-115.)** **The session key shows in the process list** while the app runs (passed as a dialog argument). | `deploy/` launcher | F15 |

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

## From the leave-no-trace sitting, 26 November

| ID | Candidate | What it touches | Source |
|---|---|---|---|
| C10 | **(Taken by WP22, D-125.)** **SCAT Chat as a small, clear local app that runs the MCP server.** Installed to Applications; a window that can be minimised; Copy key and Copy address buttons; says plainly it is the MCP server, with a status light; shows which vault is mounted and lets the coder change it without a terminal; no flicker when the key is copied. | `deploy/`, `docs/chat-path.md` | The run record, `~/scat-lab/evidence-lnt` (findings at steps 2, 10, and the restart); the chief engineer's words below |
| C11 | **(Taken by WP23, D-133.)** **The assistant's rules in stronger deontic words.** `contracts/assistant.md` (and the skill, which follows it) says "May" and "May not"; a pass decides SHALL, SHALL NOT or SHOULD for each of A1 to A15. | `contracts/assistant.md`, `skills/scat-coding/SKILL.md`, its drift test | The chief engineer, below |
| C12 | **(Taken by WP24, D-136.)** **Help to fill in the node pages, as synthesis across narratives.** Today the tools stub node pages and record edges; nothing helps write a node page's content. The aim is a meaningful synthesis of each group, concern, affordance and technology as it appears across many narratives, not text copied from one. Naive term matching must be avoided: different words can name one concept, and one word can name different concepts. Likely skills or agentic workflows, with views that gather, for one node, what every narrative says of it. | Skills and MCP prompts, views (a per-node evidence view beyond `trace`), norms, the node-page contracts; links to the accepted gap on renaming and merging node pages (W11, D-100) | The chief engineer, below |

The chief engineer's words, 26 November (quoted as typed; recorded by the ACE):

> C10: "SCAT Chat needs to be something i can minimize now that its open its in front of my work and i keep moving it
> out of the way" / "the Copy key button is good. i also want a button to copy the address to for the mcp server since
> i also need to paste that." / "it should be clear that this is the MCP server and provide basic status info for the
> mcp server maybe just a colored light. the server should be a very thin local service, easy to use but also
> transparent about what it is and what status it is in" / "there is an odd visual effect when the key is copied. the
> scat chat screen disappears and reappears quickly" / "we can just add the steps to get into applications in the pass
> with the other fixes to the scat chat. basically its just a small local app that runs an mcp server. let's package
> it up that way so its clear and easy to use."

> C11: "skimming the skill. i noticed you used MAY and MAY NOT. that's a pretty soft deontic. i think we'll want to
> make another pass to see if we should be using SHALL or SHOULD for some or all of these."

> C12: "i opened it and marked it done just as a test but then i downgraded it to draft. this file is coded but it
> references a bunch of stubbed content. i mean technically this page is done but all these other pages are stubbed
> out. i want to make sure our assistant is able to help us fill in the related pages. the key is that all this
> content is not unrelated. if this were the human only flow (no assistant) it would actually feel a bit repetitive.
> that's not necessarily bad because it forces you to think about what you are doing. and its particularly important
> to revisit the content to make sure the coded S, C, A, T are more than just copied text from the narrative but
> rather a meaningful synthesis of the named concepts as they appear across many narratives. we need to avoid naive
> term matching because sometimes different words are used for the same concept and sometimes the same term is used
> for a different concept. i suspect much of the work to facilitate populating the pages will come from skills or
> agentic workflows. do we have those extra tools, prompts and workflows available yet to test out?"

## From the chief engineer, 26 November (later)

| ID | Candidate | What it touches | Source |
|---|---|---|---|
| C13 | **(Taken by WP23, D-129.)** **Attributing narratives to contributors, as an organiser's choice at set-up.** Some groups prefer attribution to privacy. Attribution is off in Chatham House mode; the organiser chooses it when setting up and setting expectations. "Attributed to" is the natural word for it (the diagram's stale "attributed to" for affordance to technology is fixed: "provided by"). | The ontology (an attribution property, distinct from holding; `prov:wasAttributedTo` was weighed in the ontology research), page contracts, `scat.toml` (a mode), the planning guide and consent page, views | The chief engineer's words below |

> C13: "this is a bit of an awkward catch but hopefully not a huge disruption. i think people would be more likely to
> say "affordances are provided by technologies" than "attributed to" that also releases the "attributed to" concept
> for future use to attribute narratives to contributors. the option to attribute narratives to contributors is off
> when running in chatham house mode but i do think its something the tool should support. some groups will prefer
> attribution over privacy. this choice is part of the set up and expectation setting stage for the organizer."

## From the chief engineer, 26 November (docs)

| ID | Candidate | What it touches | Source |
|---|---|---|---|
| C14 | **Coding approaches, as a drill-down with a walkthrough each.** The sidebar's top level is "coding approaches", with: coding by hand (no AI); coding with an AI IDE (example: Codex); coding with an AI chatbot (example: Claude); coding with a local LLM (example: Ollama running in Docker; or a better local model); and leave no trace (example: inference.coop). Different providers for the IDE, chat and leave-no-trace flows, so no tool is favoured. Each walkthrough has screenshots and makes set-up as easy as possible: fewer steps where possible, but no step removed if that would confuse; automation may remove steps, never points where a person must choose. | `mkdocs.yml` navigation, `docs/coding.md`, `docs/chat-path.md`, `docs/ide.md`, `docs/leave-no-trace.md`, new pages (local LLM, chatbot), screenshots under `docs/assets/`, the launcher or set-up scripts where automation helps | The chief engineer's words below |
| C15 | **Facilitating and planning, rethought together.** The Facilitating section opens with **Narratives**, then Scenarios and Architectures (introduced as heuristics for organising and interpreting narratives), and may give what is versus what could be its own content; mode-aware content on attributing participants; all of it aimed at capturing field notes. Coupled with revisiting the planning content: high-level guidance on organising the event to set the stage for facilitation and field-note collection, by event kind (a one-off online discussion, a recurring discussion, an in-person meetup, a multi-day workshop), including who takes field notes and, with several note takers, how notes are collected and compiled as input to the coding workflow. Kept light, not bloated. | `mkdocs.yml` navigation, `docs/facilitate-*.md`, a new narratives page, `docs/planning.md`, `docs/data-and-consent.md`, WP23's attribution modes | The chief engineer's words below |
| C16 | **A terminal-free Install once on the chat path.** v0.1 tolerates one-time Terminal use at setup, done by the setup person (D-164); the aim is an install an organiser can do without Terminal (for example an installer, or SCAT Chat setting up Colima and Tailscale itself). | `deploy/` (SCAT Chat, the launcher), `docs/chat-path.md` Install once | The chief engineer, D-164 |
| C17 | **Robust tracking of on whose call a change was made.** v0.1 writes who made a stage move in a signature-like field the assistant fills (D-179); a later package could make that field something the assistant cannot fake. | WP29's model, WP30's server, the record of moves | The chief engineer, D-179 |
| C18 | **The IDE and local LLM paths documented at our side of the handshake.** Two separate approaches, as now; neither gets an end-to-end walkthrough. Each page states the API standards and interface contracts our tool uses, with enough instruction to use our tools; the user configures their IDE, or their local LLM with Open WebUI, themselves. The chat paths keep full walkthroughs. | `docs/ide.md`, `docs/local-llm.md`, `docs/coding-paths.md`, `docs/path-pros-and-cons.md`, `contracts/` (as the referenced standard) | The chief engineer, D-183 |
| C19 | **Follow-ups from WP32 to WP35.** Regenerate `docs/assets/layered-case-study.png` (it still shows the old "group" column and unordered nodes); offer `mark_narratives` from the CLI and the server (Python only today); small `api.md` nits (the no-account footer line explained only under `draw.layered`; text-form line order differs between fingerprint and layered). Glossary words the reviewers noted (orphan, plot, query result, candidate, account text) go to WP38. | `docs/assets/`, `src/scat_kg/cli.py`, `src/scat_kg/mcp_server/server.py`, `docs/reference/api.md`, `GLOSSARY.md` (WP38) | The WP32 to WP35 PM's hand-off, D-190 |

> C14: "the sidebar with the "coding" in chat should be a drill down. the top level is coding approaches and it should
> have several options: coding by hand (which is the no ai option), coding with an AI IDE (like codex or claude code or
> cursor), coding with an AI chatbot, coding with a local LLM (eg i have ollama locally), leave no trace. we can talk
> this out a bit more if you need more guidance but the idea is to give the reader some clarity about options and
> provide some walk throughs for each. i prefer to provide some screen shots in the walk throughs to make them
> intuitive. our local LLM example is ollama running in docker, our chat example can be claude, leave no trace examples
> are inference.coop and our ide example can be codex. we don't really want to bias the tools so having the IDE, the
> chat and the leave-no-trace flows use different service providers is a good practice. we can also look at whether
> there is a better local LLM to use. i don't usually use local LLMs on this machine because its old and they are slow
> but that should not stop us from providing a clear path for others to use local first LLM."
>
> "walk throughs need screen shots and we should make sure the materials we provide are aimed at making the set up as
> easy as possible. fewer steps where we can but not eliminating steps if it will result in confusion. automation can
> help remove steps but should not remove points where humans need to make choices"

> C15: "this should also have a narratives section. that should come first. then scenarios and architectures.
> scenarios and architectures are introduced to provide heuristics for organizing and interpreting narratives.
> similarly our distinction between observations about what is versus what could be may merit their own content. (all
> under the facilitating heading). there probably needs to be mode aware content on attribution of participants. all
> this content is specifically there to help capture field notes. and i think the design of this documentation should
> be coupled with revisiting the planning content which involves setting setting up for the facilitated events. will be
> very different if you are hosting a one off online discussion, a reocurring discussion, an in person meetup or a
> multiday workshop. i don't want this too get too bloated so the idea is that we should provide high level guidance
> for how to organize the event to set the stage for facilitation and field note collection, including identifying who
> is going to be responisble for taking field notes. and when there are multiple field note takers how are they to be
> collected and compiled to serve as an input to our coding workflow"
