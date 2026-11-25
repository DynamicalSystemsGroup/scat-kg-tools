# WP18-R4: the live run (25 November)

The chat path run once end to end in inference.coop's chat, with lab material only (a synthetic bike-library note),
the vault in `~/scat-lab/`, the server in its container behind Funnel, and the chief engineer's sign-in and key.
Words follow `GLOSSARY.md`. The run is complete and torn down; the ACE's call on WP18 is made separately.

## What ran

1. A first attempt pasted the note into the chat instead of attaching it, with the template's example still in the
   vault. It is discarded as a deviation from the guide (findings F1 to F4 below).
2. The vault was reset and the example removed, as the guide says.
3. In the chat's own tools: a skill `scat-coding`, built from the server's `code-a-narrative` text unchanged, and an
   agent "SCAT coder (lab)" (tinfoil/gpt-oss-120b, the scat-lab MCP tools, the chat's Ask User, the skill only).
4. In Chrome (the built-in browser pane cannot reach a file dialog): a chat with the agent, the note attached as a
   file, one short request. The agent asked four questions, drafted the account as text, proposed nodes and edges,
   took the coder's corrections, made 11 pages and recorded 8 edges by the tool (20 tool calls), ran the check and
   handed back the next act. The vault matched what the coder confirmed; the check reported only `timeframe`.
5. The ACE, as the coder's hands, pasted the account and set `timeframe: mixed` in Obsidian. Check: no problems.
6. The chief engineer set `done` in Obsidian. The check failed on SCAT-DONE-FIELD (no `description`); the chat
   assistant, asked to re-check, quoted the error and offered a sentence. The chief engineer chose the ACE's shorter
   one; the ACE added it. Check of the whole vault: no problems, with the narrative `done`.
7. Teardown at 13:04 by quitting SCAT Chat (its Stop). Verified: no SCAT Chat process, no `scat-chat` container,
   Funnel reports no serve config, the public address does not answer, the clipboard holds no key, and the stored key
   (mode 600) differs from the session's key. The chief engineer then deleted the "Scat Lab" MCP entry in the chat by hand. Left in the chat
   account: the uploaded note and the two conversations (C8), and the `scat-coding` skill and the agent, kept for the
   chat-path user tests.

## Findings

| ID | Finding | Kind |
|---|---|---|
| F1 | The ACE pasted the note instead of attaching it; the guide says attach. | Protocol (ACE) |
| F2 | With the example in the vault the cap of 3 groups was full, so no edge could be recorded. | Docs: removing the example matters on the chat path |
| F3 | The assistant proposed `type: scenario` frontmatter. | Assistant error |
| F4 | Bare MCP entry: ten tool calls in one turn; the server's prompts were not loaded by the chat. | Assistant behaviour |
| F5 | The chat has Skills; the assistant's rules belong there as a SKILL.md. | Deliverable gap (WP18) |
| F6 | The chat has an Agent Builder; a saved agent replaces the per-chat setup line. Agents are started from the Agent Builder's Select; not from the model menu or `@` on this instance. | Docs gap |
| F7 | The model first called the skill-file reader on the attachment (failed); the note's text reached it anyway. | Assistant behaviour |
| F8 | The proposed edges ignored the edge grammar (e.g. "group holds technology"); the coder corrected them. The skill does not state the grammar. | Deliverable gap (skill text) |
| F9 | Authoring and coding came in one reply, not one step at a time. | Assistant behaviour |
| F10 | Chrome's upload tool reads only the session's folders; the note was copied to the scratchpad. | Harness |
| F11 | Opening the vault in Obsidian writes `.obsidian/` settings into it. | Known (template) |
| F12 | The coder asked for "a scenario"; the narrative was made with no `kind`, and nothing prompted it. | Assistant behaviour; skill text |
| F14 | Set to `done` straight from `stub`, the narrative failed SCAT-DONE-FIELD (no `description`). A `draft` page is warned about `description`; a `stub` page is not, and the assistant never moved the page to `draft`, so nothing flagged it before `done`. | Rule staging; skill text |
| F15 | While a session runs, its key is in plain text in the process list: the app shows it in a dialog launched with the key as a command-line argument, so any local process can read it with `ps`. The key ends with the session (rotated at Stop). | Security defect (WP18 launcher) |
| F16 | The guide's Stop named the chat-entry delete only in its failure branch, with no steps. Fixed on `dev` (8d620fe): Stop is now stop, check, delete the entry. | Docs gap, fixed |
| F13 | The account has no links to the nodes it names, and SCAT-MENTION stayed silent (see below). | Rule condition; skill text |

## For later revisions

The chief engineer's UX observation on the "Edges told" table, 25 November (quoted as typed; recorded by the ACE):

> "(1) the edges should all be oriented semantically so they can be read "from" "edge" "to" ~ "parents hold concern
> bike safe for children" should be skimmable from the table
> (2) requires reordering the tables, checking (and possibly changing edge semantics) and making skimmability
> requirements. i don't necessarily want to bloat the table but given the natural subject predicate object structure
> of the underlying data this should honestly be pretty easy."

A second observation, same day (quoted as typed; recorded by the ACE):

> "another optional but potentially desirable change would be adding wikilinks in the text itself."

The ACE's note on it: the layout (D-088) and the glossary already expect the account to link the nodes it names, and
rule SCAT-MENTION (warning, every status) exists to suggest those links. It did not fire here: the account names
`parents` and other node pages as plain text, and the check reported no problems. The likely cause is the rule's
condition "when the body has no link to that page": the "Edges told" table's `from` and `to` cells already link every
node, so the account is never prompted. The assistant drafted the account without links, and the skill does not ask
for them. Related: the narrative has no `kind`, though the coder said "a scenario"; nothing prompted it (F12).

The chief engineer's weighting of the two, same day (quoted as typed; recorded by the ACE):

> "i would say that the table formatting is pretty nice and possibly better ux than in narrative linking from a
> skimming standpoint so i would probably downgrade in text linking to "may" not even "should", the "shall" deontic
> (meaning required for conformance) is the table."

So: the "Edges told" table is the "shall" (required for conformance); links in the account text are at most a "may".
For whoever scopes it: SCAT-MENTION is a warning today, which reads stronger than "may", and the layout (D-088) and
glossary wording should be checked against the same weighting. F13 is reweighted accordingly: the silent rule is not a
defect to fix by making it louder.

His follow-up, same day (quoted as typed; recorded by the ACE):

> "good point. i think the should for the table of links is fine BUT then we have no source of links at all unless we
> link up the text. you can see there is some fuzziness here that we want to tighten up. i am okay with normative
> guidance. strictly speaking the narrative is uncoded (cannot be tied to the graph) unless it has at least one node
> (stakeholder, concern, affordance or technology) declared. in practice we want a collection of nodes and edges, (not
> necessarily a connected graph) but a narrative coherent story and identification of a collection of nodes and edges.
> our approach is to identify nodes and edges that reappear across many narratives to build a map (the layer graph) so
> we see how those stories fit together."

The fuzziness, as the ACE reads it, to be tightened by normative guidance in the later package (not decided here):

- **What makes a narrative coded.** At least one node declared. Today a node can only be declared by a link: in the
  table (which needs an edge, so two nodes) or in the text. A narrative that names one node and no edge has no
  conformant place to declare it unless the text links it.
- **Where links come from.** If the table is "should" and text links "may", a narrative may have neither, and then it
  is not tied to the graph at all.
- **What a finished narrative aims at.** A coherent story plus a collection of nodes and edges, not necessarily
  connected; its worth is in nodes and edges that recur across narratives, which the layered view assembles.
- So the levels to state are: the minimum to count as coded (one declared node), the expected shape (nodes and edges,
  the table), and the optional (links in the text), with one place a lone node can be declared.

On F14, the chief engineer, same day (quoted as typed; recorded by the ACE):

> "it seems to me that forcing the intermediate state is bad UX. i think its fine to have the cli force two steps but
> that's the machine write path. the machine read path should allow me to set the status to the status i am attesting
> even if it skips a step. in practice lets say i opened up a stub, filled in the draft and coded it up to my
> satisfaction in one sitting then i need to be able to attest to that status change. the intermediate state existed
> (while i was working) but it feels wrong to make me stop and tag it"

What the contracts say today, checked by the ACE: nothing forces `draft`. A page may go from `stub` to `done`; setting
`done` through the tool is refused only while the page would fail at `done` (`contracts/page-contracts.md`, Status),
and a `done` set by hand in Obsidian is accepted and judged. What bit here is one row of the catalogue's status table
(`contracts/rule-catalogue.md`, Status behaviour): "Required from `done`, text (`description`)" is **silent** at
`stub` and a warning only at `draft`, while `timeframe` warns at both. So the coder who works a stub to completion in
one sitting is not shown the to-do list until the error at `done`. The candidate fix, for whoever scopes it: show the
fields `done` needs at `stub` too (at least once the page has an account), so a one-sitting attestation is possible
without an intermediate tag. Not decided.

His model of status, same day (quoted as typed; recorded by the ACE):

> "i think the tag is a terminal state for a session. if i move on from a page to another one then i should tag the
> one i am moving away from with its status (draft) if i am not done coding it"

As the ACE reads it: status is set when the coder leaves a page, not while working on it. `done` if finished, `draft`
if not; `draft` marks work left unfinished, not a step to pass through. For whoever scopes it, this touches the coding
guide and the walkthroughs (say when to set status), the assistant's skill (at the end of a session, name the pages to
tag and offer `draft` for unfinished ones; `done` stays the coder's), and the catalogue row above.

On the `description` error itself, the chief engineer, same day (quoted as typed; recorded by the ACE):

> "creating a description flagging as nonconformant for missing direction is the system working as intent. for a human
> this is a prompt from the python software to write a short description (a bit like github requiring a commit
> message) but in an ai assisted setting have the ai assistant offer a description is acceptable"

So the SCAT-DONE-FIELD error is intended, like a required commit message. On the chat path the assistant may offer the
sentence for the coder to accept. For the skill: when the check reports a missing `description`, offer one.

The assistant offered "Volunteers use a checklist, spreadsheet, and QR code to ensure bike safety for children." The
ACE offered "Volunteers and parents want broken bikes caught at return; a paper checklist and a repair log do that
now, and a QR code on each frame is proposed." The chief engineer chose the ACE's (quoted as typed; recorded by the
ACE):

> "i prefer the ACEs since its more brief and i think long description approach being repetitive with the content
> itself which can be pretty short. i will note though that the ACE doing it is more consistent with testing the human
> authored (not AI assisted) flow since the ACE is emulating me (the user). Or the other extreme workflow where we're
> using an IDE and the ACE is playing the part of the in IDE assistant (which is what it actually is); in the case
> where the MCP server is use, we'd generally expect the MCP server (chat assistant to do it). keep in mind that for
> both the discription and the body of the narrative we're anticipating a mixed flow: sometimes the user will choose to
> write first and have the chatbot refine, sometimes the chatbot will draft copy and the user will refine. the
> composition and number of iterations of that loop doesn't matter as long as the users decision to shift to done
> denotes their validation of the content."

As the ACE reads it, for the guide and the skill: a `description` is brief and does not repeat the account. Writing
the account and the description is a mixed loop, coder-first or assistant-first, any number of rounds. What counts is
that the coder's move to `done` validates the content. This run's description came by the ACE as the coder's hands,
which tests the human-authored flow, not the chat assistant's; the assistant's offer is recorded above.

What both observations touch, for whoever scopes them: the column order of the "Edges told" table (today `type | from | to | note`),
the edge names and their direction in the ontology, the layout contract (D-088), the tool's writer and reader of the
table, the template's pages and the range vault, a stated skimmability requirement, SCAT-MENTION's condition, and the
`scat-coding` skill's text. Not decided; candidates for a later package.
