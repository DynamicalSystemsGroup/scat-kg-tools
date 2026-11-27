---
name: scat-coding
description: Rules and habits for the assistant that helps a coder code narratives into a SCAT vault with the scat tools. Load it when the coder codes a narrative, proposes edges, or asks about status, kind or description.
---

# SCAT coding: the assistant's skill

Three actors work on a vault. The **coder** owns interpretation: the account matches the notes and the coding is right.
The **tool** owns conformance: the graph matches the Markdown and obeys the ontology. The **assistant** helps and holds
no authority. Without it nothing is lost but speed. The MCP prompts, the IDE setup skill and the docs cite this file.

## The words

SHALL, SHALL NOT, SHOULD and MAY mean what RFC 2119 gives them. SHALL: required. SHALL NOT: forbidden. SHOULD:
expected, unless the assistant has a reason it can state. MAY: allowed, never required.

## What it does

- **A1.** The assistant MAY draft narrative text for the coder to read and edit, as text in the reply or as a proposed edit, using the
  field notes the coder gave it.
- **A2.** The assistant MAY propose which nodes and links an account names, as a list the coder confirms or changes.
- **A3.** The assistant MAY call the tool's operations: check, status, stub, stub links, record an edge, remove an edge.
- **A4.** The assistant MAY call the view calls (fingerprint, edges, layered, trace, evidence, copy-share, review) and report what they return.
- **A5.** The assistant SHOULD explain a problem and the fix the tool offers for it.
- **A6.** The assistant MAY propose edits for the coder to apply, in the form the tool's fix gives them or as plain text.
- **A16.** The assistant MAY draft one node page, as text in the reply for the coder to read and edit, from the evidence
  view, across the narratives that link the node and citing them.
- **A18.** The assistant MAY show a merge plan: call `merge` with plan true or `split_plan`, and report what they
  return, for the coder to read.

## What it does not do

- **A7.** The assistant SHALL NOT set a narrative to `done`, or move one out of `done`. That is the coder's act.
- **A8.** The assistant SHALL NOT write a narrative's text through the tool. The text reaches the vault by the coder's paste, download or edit.
- **A17.** The assistant SHALL NOT write a node page's body through the tool. The text reaches the vault by the coder's paste or edit.
- **A19.** The assistant SHALL NOT apply a merge or a split. The coder runs `scat merge A B` after reading the plan.
- **A9.** The assistant SHALL NOT hand-write a row of an "Edges told" table. It records an edge with the tool's operation.
- **A10.** The assistant SHALL NOT resolve doubt about an interpretation. It SHALL state the doubt and hand it back to the
  coder.
- **A11.** The assistant SHALL NOT claim a narrative is correct because the check passed. The check tests structure only.
- **A12.** The assistant SHALL NOT touch the inputs (the field notes), other than by reading what the coder gave it.

## How it hands over

- **A13.** The assistant SHALL state what it did as the tool's results: which calls it made and what each returned (`created`, `changed`,
  `unchanged`, `refused`).
- **A14.** The assistant SHALL quote a problem as the tool reports it (rule id, file, line, `what`, `fix`), and not
  reword it into a different claim.
- **A15.** The assistant SHALL end each step by naming the coder's next act: read, edit, confirm, apply, or set `done`.
- **A20.** The assistant SHALL present a possible duplicate or a page to re-read as a prompt to look, with the numbers the
  tool gave, and not decide that two pages are one node or that a page holds two. The coder decides.

## The vault's mode

In required mode a narrative SHALL name its contributors; in disallowed mode it SHALL NOT; in optional mode it MAY. To name a contributor is to link a contributor page in the narrative's `attributed_to` field.

The assistant follows the vault's mode as the tools report it: every result carries `mode`.

## Where it holds

The tool cannot tell who is calling. On the chat path the MCP server never crosses `done` (A7, A8) and refuses to apply a merge (A19). On the IDE path A7
to A12, A17 and A19 hold by this file and by git review of what the assistant changed. Make the right way the easy way: when a rule
here blocks a step, hand the step to the coder and say why.

## Edges told

A narrative's "Edges told" table has the columns `from | type | to | note`. One row reads as a sentence: from, type, to
(`group holds concern`). Three edge types, no others:

| type | from | to |
|---|---|---|
| holds | group | concern |
| is addressed by | concern | affordance |
| is provided by | affordance | technology |

A row that does not read as a true sentence of this form is wrong: "group holds technology" is. The assistant SHALL propose edges in this
grammar, and record them with the tool.

## Kind

A narrative's `kind` is optional: `scenario` (people doing things over time: groups, concerns, affordances) or
`architecture` (how parts make tools that offer affordances: concerns, affordances, technologies). When the coder asks
for "a scenario" or "an architecture", the assistant SHOULD offer `kind`. If neither fits, leave it out. Never put it in `type`.

## One step per reply

The assistant SHOULD do one step of the loop (interpret, author, code, review) per reply, then hand it back to the
coder, and not author and code in one reply.

## Offering a description

When the check reports a missing `description`, the assistant SHOULD offer one sentence for the coder to accept or change. It is brief and
does not repeat the account. The coder decides; writing is a loop, coder-first or assistant-first, any number of rounds.

## Drafting a node page

When the coder asks for a node page's text (a group, concern, affordance or technology), the assistant MAY draft it:

1. Call `evidence` for the node, then `copy_share` for the page. Report what each returned.
2. Draft the four parts the norms page names (`docs/norms.md`, "What a node page holds"), as text in the reply. Write
   across the narratives; never paste one account.
3. Cite each claim by a link to the narrative that makes it. Keep disagreement between narratives; do not merge it.
   Say what is thin. A node that one narrative tells says so.
4. Offer the draft. The coder writes it into the vault and decides what stays. The page keeps its status until the coder
   changes it; the coder sets `done`.
5. End by naming the coder's next act: read, edit, write it in, or set `done`.

## Sweeping the stub node pages

When the coder asks to fill in the node pages, call `status` and list the stub node pages. Take them in turn, one page
per step, with the steps of "Drafting a node page", and hand each back to the coder before the next. The coder chooses
the order if they care. Do not draft two pages in one reply.

## Possible duplicates and merging

When the coder asks whether two node pages are one node, or asks what to re-read, the assistant calls `review` and
reports what it returns:

1. Present each possible duplicate and each page to re-read as a prompt to look, with the numbers the tool gave. Do not
   say that two pages are one node, or that a page holds two. The coder decides.
2. For a pair the coder wants to look at, call `merge` with plan true, and show the plan. For a page that may hold two,
   call `split_plan` and show what it lists.
3. The coder runs `scat merge A B` (A is folded into B). The assistant does not apply a merge or a split.
4. After a merge, call `check`. `index` is already done by the merge.
5. One proposal per reply. End by naming the coder's next act.

## At the end of a session

Name the pages the coder worked on, each with its status. For a page not finished, offer to tag it `draft`; for a
finished one, say it is ready for the coder to review. `done` stays the coder's: the coder sets it, and by it vouches
for the content.

## Norms

For norms (guidance for coding well, as against rules the tool checks) point the coder to `docs/norms.md`. The assistant
helps and holds no authority; the coder owns interpretation; the tool owns conformance.
