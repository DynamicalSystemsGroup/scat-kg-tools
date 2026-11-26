# Norms for coding a narrative

A **rule** is what the tool checks. A breach is reported by `scat check` with a rule id (`SCAT-...`) and either blocks
(an error) or does not (a warning); the rule catalogue (`contracts/rule-catalogue.md`) holds every rule, and a "must"
on this page always names one. A **norm** is guidance for coding well. It is the same for a person as for an LLM
assistant, and the tool does not enforce it, so this page says "should" and "may" for norms. Each section below opens
by saying which it is.

## A coded narrative

*A rule and a norm.* The rule: a narrative is **coded** when it links at least one node page anywhere in its body; an
**uncoded** narrative is **excluded** from the knowledge graph and every view, and `scat check` reports it as a
warning (SCAT-UNCODED). The warning never blocks, and the narrative is included as soon as it links a node page.

The norm is the shape to aim for: a coherent account of what was told, plus the set of nodes and edges the account
names. That set need not be connected. A single narrative is a small sample. Its worth shows in recurrence across
narratives, which you read in the layered view.

## Links in the account

*A norm, resting on one rule.* You may link a node wherever the account names it, and you should when the name
matters to the story. A link adds no edge; only a row of the `Edges told` table does. A link in the account is also
the conformant place to declare a lone node, one the account names with no edge: that link codes the narrative and
puts the node in its fingerprint (SCAT-UNCODED; a `done` narrative with no row only gets a warning, SCAT-NOEDGES).

When the account names a node page in plain text, the tool can suggest the link (SCAT-MENTION). That is a warning, and
it shows only when `scat.toml` sets `link_suggestions = true`. Taking a suggestion is your choice.

## Descriptions

*A rule and a norm.* The rule: `description` is silent at `stub`, a warning at `draft` and an error at `done`
(SCAT-DRAFT-FIELD, SCAT-DONE-FIELD). The error is intended, like a required commit message: it makes you say what the
page is in a sentence before you sign it off.

The norm: keep the description brief, and do not repeat the account. It says what the page is for, not what happened
in it. An assistant may offer one, as text for you to read. You decide what stays.

## What a node page holds

*A norm.* A node page (a group, concern, affordance or technology) holds four parts, written across the narratives
that link it. Never paste one account into it.

- **What it is**, in the node's own terms: what the group, concern, affordance or technology is, as the people in the
  narratives mean it.
- **How the narratives tell it.** Cite each claim by a link to the narrative that makes it, and say when several
  narratives agree. A node that appears in one narrative only says so.
- **Where accounts differ.** Keep the differences and do not merge them. A group page that spans several senses (a cap
  forces broad groups) says so and names the senses.
- **What is thin**: what no narrative says.

To look, run `scat evidence <node>`: it shows every narrative that links the node, with the paragraph around each
link. `scat copy-share` shows how much of each page repeats a narrative word for word. A high share is a prompt to
look at the page, not a fault. The assistant may draft a page as text; you write it into the vault and decide what
stays.

## Writing together

*A norm.* Writing the account and the description is a mixed loop. You may go first, or the assistant may, and you
may go any number of rounds. Whoever drafts, your move to `done` is the validation of what the page says.

You own interpretation: that the account matches the field notes and the coding is right. The tool owns conformance:
it checks structure only, so a passing check does not say a narrative is correct. The assistant helps and holds no
authority; it may not set `done` (`contracts/assistant.md`, A7).

Whether a narrative names its contributors is set by the vault's attribution mode (`attribution` in `scat.toml`). In
required mode a narrative names its contributors: it links a contributor page in its `attributed_to` field, which is a
warning to lack before `done` (SCAT-DRAFT-ATTR) and an error at `done` (SCAT-DONE-ATTR). In disallowed mode no
narrative names a contributor and the vault holds no contributor page (SCAT-ATTR-DISALLOWED). In optional mode a
narrative may name its contributors or not, and nothing is required.

## Status when you leave a page

*A norm.* When you stop working on a page, set its status to say where it stands: `done` if it is finished, `draft`
if not. `draft` marks unfinished work. It is not a step to pass through, and nothing forces you to use it: you may go
from `stub` to `done` in one sitting. An unfinished page is never an error for being unfinished: nothing in the `done`
column of the status table is an error before `done`.

## What `done` needs

*A rule.* `scat set-status <page-name> done` judges the page as it would stand at `done`, and refuses while any error
would stand (SCAT-DONE-REFUSED); it writes nothing then. Warnings do not block. These are the errors to clear:

- Every page: `status` and `title` present (SCAT-FM-REQUIRED), and a `description` (SCAT-DONE-FIELD). A legal, unique
  file name (SCAT-NAME), single-string text fields (SCAT-FM-SHAPE) and no link to a page that does not exist
  (SCAT-LINK-DANGLING-BODY) are errors at every status, so they must also be right.
- A narrative: `timeframe` set to `past`, `future` or `mixed` (SCAT-DONE-FIELD, SCAT-FM-TIMEFRAME). `kind`, if
  present, must be in its value set (SCAT-FM-KIND).
- A narrative's `Edges told` table, if it has one: each problem the table has at `draft` as a warning is an error at
  `done` (SCAT-DONE-TABLE-HEADER, SCAT-DONE-TABLE-ROW, SCAT-DONE-TABLE-TYPE, SCAT-DONE-TABLE-LAYERS,
  SCAT-DONE-TABLE-SECOND, SCAT-DONE-TABLE-DUPLICATE). Each end of a row must be exactly one link to a node page that
  exists (SCAT-DONE-END-NOLINK, SCAT-DONE-END-NOPAGE, SCAT-DONE-END-NOTNODE).

Not needed at `done`: a link, an edge, a row, or a clean mention check. These give warnings only (SCAT-UNCODED,
SCAT-NOEDGES, SCAT-MENTION).
