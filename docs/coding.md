---
provider: none
---

# Coding

!!! tip "Your next step"
    In your vault folder, run `uv run scat check` and read what it says.

Coding means linking the nodes a narrative names and recording the edges it tells, on the narrative's own page.

A **narrative** is one story drawn from your field notes, kept on one page. Coding is the step where that story becomes part of the graph. You write the account, link each group, concern, affordance or technology where the account names it, and add one row to the page's `Edges told` table for each edge the account tells. The tool checks the result and tells you in plain words what still disagrees. Nothing is copied to a second page: you code in the same page you wrote the account in. The [home page](index.md) defines the four node types, and the [terms](reference/terms.md) page defines every other word used here.

## What this path needs

Coding by hand needs only these, in any setup:

- A vault folder from the template, set up as in [Getting started](getting-started.md), with `uv sync` already run. For a trial, a plain clone of the template needs no sign-in.
- A Markdown editor that opens the vault folder and shows `[[links]]` and page properties. Any editor that does this works; Obsidian is the worked example below, and the index pages are Obsidian Bases, so they show only there.
- A terminal in the vault folder, to run the check.
- A narrative: your narrative of one session, on a page in `narrative/`.

There is no account, key, server or assistant. You write every word, and the tool checks the result.

## Worked example: Obsidian

The example codes one narrative in the template vault, `groups-under-a-cap-pitch`: it adds one link and one row to the `Edges told` table, then runs the check until the tool says there is no problem. The same four steps of the [coding loop](#the-coding-loop) apply on every narrative.

1. **In Obsidian:** open the vault folder as a vault (Manage vaults, then Open next to Open folder as vault), and see the folders `affordance`, `concern`, `group`, `index`, `narrative` and `technology` in the left pane.

2. **In Obsidian:** open `narrative/groups-under-a-cap-pitch` and read it, so that you have the account and the two rows of its `Edges told` table in front of you.

3. **In Obsidian:** change the `status` property from `done` to `draft`, so that you can edit a `done` narrative; the check runs on it again when you set `done` at the end.

4. **In Obsidian:** link a node where the account names it. In the last bullet of the account, the one that begins "Reason given", turn the words "the people in the data" into a link to the group `workshop-participants`:

    ```text
    - Reason given: [[workshop-participants|the people in the data]] are groups under the Chatham House rule, so [[anonymity|no individual is identifiable]].
    ```

    The account now links a group where it names one.

5. **In Obsidian:** add one row at the foot of the `Edges told` table, so that the account tells that this group holds a concern:

    ```text
    | [[workshop-participants]] | holds | [[anonymity]] | They appear only as groups, so no individual is identifiable. |
    ```

6. **In a terminal:** in the vault folder, run `uv run scat check groups-under-a-cap-pitch` and read what it says. A misspelt link is named with the line to change. A link written `[[workshop-participnts]]` produces this output:

    ```text
    attribution mode: disallowed
    warning [SCAT-DRAFT-END-NOPAGE] narrative/groups-under-a-cap-pitch.md:23:3 row 3 cell `from`: [[workshop-participnts]] does not reach a page (no page is named workshop-participnts)
      Fix, choose one:
        1. replace `[[workshop-participnts]]` with `[[workshop-participants]]`
        2. run `scat stub workshop-participnts --type group` (REPL: `scat_kg.stub("workshop-participnts", type="group")`) to create a group page
        3. delete the row
    0 errors, 1 warning
    ```

    Correct the link in Obsidian and run the check again until it reads `no problems`.

7. **In a terminal:** start `uv run python`, then type the lines below, and see the same text the command printed:

    ```python
    import scat_kg
    print(scat_kg.check("groups-under-a-cap-pitch"))
    ```

    ```text
    attribution mode: disallowed
    no problems
    ```

8. **In Obsidian:** confirm that the account still matches your notes and that the row is a correct use of SCAT, then change `status` back to `done`.

9. **In a terminal:** run `uv run scat check` for the whole vault, and see a conformant result:

    ```text
    attribution mode: disallowed
    no problems
    ```

The rest of this page is the reference for every step above: what the pages are, the loop, and each operation.

## Before you start

- A vault set up as in [Getting started](getting-started.md): the folder holds `scat.toml`, and `uv sync` has run. For a trial, a plain clone of the template works with no sign-in: `git clone https://github.com/DynamicalSystemsGroup/scat-kg-template`. In Terminal, go into the vault folder with `cd` and its name (for a clone, `cd scat-kg-template`) before any `uv` command.
- Obsidian 1.9 or later, with the vault open. The index pages are Obsidian Bases, which older versions do not show.
- Field notes from a session, as in [Facilitating scenarios](facilitate-scenarios.md) or [Facilitating architectures](facilitate-architectures.md). In hand, you need a few plain sentences of notes, written as they were told.
- Your groups, planned in the [planning guide](planning.md) and named by role. A group is a role, never a person: the vault holds at most the cap of groups set in `scat.toml`.
- To follow along, type the commands in a copy of the template vault, so you lose nothing. The worked example is a small community tool library.

## What the pages are

| Page type | Folder | What it holds | Who writes it |
|---|---|---|---|
| `group` | `group/` | a group, named by role | you, or `scat stub` |
| `concern` | `concern/` | what a group cares about | you, or `scat stub` |
| `affordance` | `affordance/` | what a tool or arrangement lets someone do | you, or `scat stub` |
| `technology` | `technology/` | the thing that provides an affordance | you, or `scat stub` |
| `narrative` | `narrative/` | one account, with the table of edges it tells | you, or `scat stub --type narrative NAME` |
| `contributor` | `contributor/` | a person a narrative is attributed to; only where the vault's attribution mode is `required` or `optional` | you, or `scat stub --type contributor NAME` |
| index pages | `index/` | a list of the pages of one type | `scat index`, once |

An **edge** is no page. It is one row of a narrative's `Edges told` table, and there are three types, fixed by the layers they join:

| Edge type | Name it as | The `from` node is a | The `to` node is a |
|---|---|---|---|
| `holds` | `holds` | `group` | `concern` |
| `is addressed by` | `addressed-by` | `concern` | `affordance` |
| `is provided by` | `provided-by` | `affordance` | `technology` |

The tool builds the graph of nodes and edges from the pages on every call and never holds it. It has one edge for each (type, from, to), and the edge names every narrative that has a row for it. An edge is `done` when every narrative that tells it is `done`, so you sign off edges by signing off narratives. A **link** is only "this page refers to that one". A link never makes an edge; only a row does. A contributor page is no node either: it sits outside the four layers, and a narrative's link to one says who the account is attributed to, not what it tells.

## The coding loop

You work each narrative round the same four steps, as often as it takes:

1. **Interpreting.** Read the field notes, and later the views, and decide what they say. This is yours alone.
2. **Authoring.** Write or revise the account on the narrative page. An assistant may draft it; the wording you keep is yours.
3. **Coding.** Link each node where the account names it, and record each edge it tells.
4. **Reviewing.** Run the check, then fix what it reports. You confirm two things yourself: the account matches the field notes, and the coding is a correct use of SCAT. The tool cannot judge either.

The [norms](norms.md) say what the tool requires and what is only guidance, and what `done` needs.

A node page is written across the narratives that link it, not from one of them. The norms section [What a node page holds](norms.md#what-a-node-page-holds) says what it holds, and `scat evidence <node>` shows every narrative that links the node, with the paragraph around each link.

**Two pages for one node.** `scat review` shows node pages of one type that may be one node, and pages to re-read. To see what a merge does, run `scat merge A B --plan`; then `scat merge A B` does it, and A is folded into B. `scat split-plan A` lists what to re-link if you split A in two.

When the check passes and you confirm both, set the narrative to `done`. Done is not frozen: to change a `done` narrative you set it back to `draft`, edit, then set `done` again, and the tool checks it again then.

### The three actors

- **You, the coder,** own interpretation. You alone move a narrative into or out of `done`.
- **The tool** owns conformance. It checks that the graph matches the pages and that it obeys the rules. No part of the tool can tell who is calling it.
- **An assistant,** where your participation terms allow one, helps and holds no authority. It may draft and may run the commands. Which data an assistant may touch is settled before the first session: see [Data, rights and consent](data-and-consent.md).

On the chat path, the server never moves a page into or out of `done`, so the assistant cannot, by construction. On the IDE path an assistant can run `scat set-status`, because the command cannot tell who types it. There, authority rests on the rules written for the assistant and on your review of what it changed in git (`git diff` before every commit), not on the tool.

## Where narratives and their edges come from

Everything starts in the field notes, and only you read them. You turn what a session told into one narrative page, with `scat stub` making the empty page and you writing the account. The narrative is where each edge comes from: a row of its `Edges told` table says "this account tells that a group holds that concern". There is no other place an edge is written, and no page to open for one.

A narrative that links at least one node page, in a row of its table or in its account, is read into the graph and the views. Until it does, the graph and every view leave it out, and `scat check` and the views name it (their messages say "excluded") and say how to include it: link one node page. A link in the account is also the place for a node the narrative names with no edge. A new stub is left out until you link a node.

Two narratives can tell the same edge. Each has its own row and its own note, and the graph has one edge naming both. A narrative that mentions two nodes without a row for the pair has not told an edge, even if the notes would support one: the row is your statement that the account tells it.

## A narrative, start to finish

This is one narrative coded the way most people begin, writing first and recording edges as they come. The vault is a copy of the template, whose attribution mode is `disallowed`, so every check prints that mode first. Each `$` line is a command you type, without the `$`; the lines under it are exactly what the tool prints. Page content is what you type in Obsidian.

### 1. Make the page

```text
$ uv run scat stub saturday-at-the-tool-library --type narrative
created narrative/saturday-at-the-tool-library.md
```

The page starts as a stub, with only what every page needs:

```text
---
type: narrative
status: stub
title: "Saturday at the tool library"
timeframe:
---
```

The check does not fault an unfinished page. It notes, as a warning, what `done` will need:

```text
$ uv run scat check saturday-at-the-tool-library
attribution mode: disallowed
warning [SCAT-DRAFT-FIELD] narrative/saturday-at-the-tool-library.md field `timeframe`: missing (required once the page is done)
  Fix, choose one before you set status: done:
    1. replace the line `timeframe:` with `timeframe: past` (author)
    2. replace the line `timeframe:` with `timeframe: future` (author)
    3. replace the line `timeframe:` with `timeframe: mixed` (author)
warning [SCAT-UNCODED] narrative/saturday-at-the-tool-library.md body: the narrative links no node page, so it is excluded from the knowledge graph and every view
  Fix, choose one:
    1. link a node page where the account names one, as `[[<node-name>]]` (or list it under a heading such as `Linked beyond the text`); a node the account names with no edge needs only this link
    2. or tell an edge: a row of the table whose ends are links to node pages; if the node has no page, `scat stub <name> --type <type>` makes one
0 errors, 2 warnings
```

### 2. Write the account

Open the page in Obsidian and write the account under the front matter, as it was told. Set `kind` to `scenario` (a story of people doing things over time) or `architecture` (how parts fit into tools), set `timeframe` to `past`, `future` or `mixed` (see [past or future](facilitate-timeframe.md)), and change `status` to `draft`. The `description` can wait. The links come next.

```text
---
type: narrative
kind: scenario
status: draft
title: "Saturday at the tool library"
timeframe: past
---

From the point of view of Workshop participants (about 10:20)

- Saturday, desk opens at 9. Three people ask for the same drill.
- Concern: "tools must come back in good order."
- The sign-out sheet lets us see who has what. It stops us seeing tools that are late.
```

The check shows the to-do for the `description`, and says the page is still left out (it links no node page):

```text
$ uv run scat check saturday-at-the-tool-library
attribution mode: disallowed
warning [SCAT-DRAFT-FIELD] narrative/saturday-at-the-tool-library.md field `description`: missing (required once the page is done)
  Fix: add the line `description: "<one sentence you write>"` (author) before you set status: done
warning [SCAT-UNCODED] narrative/saturday-at-the-tool-library.md body: the narrative links no node page, so it is excluded from the knowledge graph and every view
  Fix, choose one:
    1. link a node page where the account names one, as `[[<node-name>]]` (or list it under a heading such as `Linked beyond the text`); a node the account names with no edge needs only this link
    2. or tell an edge: a row of the table whose ends are links to node pages; if the node has no page, `scat stub <name> --type <type>` makes one
0 errors, 2 warnings
```

The check does not suggest links by default. To have it say where the account names a node the vault already has and
does not link it (`SCAT-MENTION`), add the line `link_suggestions = true` to `scat.toml`. Each suggestion names the
text and the link to write there:

```text
warning [SCAT-MENTION] narrative/saturday-at-the-tool-library.md:9:27 text `Workshop participants`: names the group page [[workshop-participants]] but does not link it
  Fix: on line 9 replace `Workshop participants` with `[[workshop-participants|Workshop participants]]`
```

### 3. Record the edges

Each edge the account tells is a row. `record-edge` writes the row for you, and creates the node pages the row names if the vault lacks them, as stubs of the right type: the layer fixes the type. `--told-by` names the narrative:

```text
$ uv run scat record-edge holds workshop-participants tools-come-back-in-good-order --told-by saturday-at-the-tool-library --note "Said twice in the first hour."
created concern/tools-come-back-in-good-order.md
changed narrative/saturday-at-the-tool-library.md
note: added `| [[workshop-participants]] | holds | [[tools-come-back-in-good-order]] | Said twice in the first hour. |` to narrative/saturday-at-the-tool-library.md at line 19
$ uv run scat record-edge addressed-by tools-come-back-in-good-order sign-out-sheet --told-by saturday-at-the-tool-library
created affordance/sign-out-sheet.md
changed narrative/saturday-at-the-tool-library.md
note: added `| [[tools-come-back-in-good-order]] | is addressed by | [[sign-out-sheet]] | |` to narrative/saturday-at-the-tool-library.md at line 20
```

The new concern and affordance are stubs, so you write their descriptions later. The rows are in the page, which you can also edit by hand:

```text
---
type: narrative
kind: scenario
status: draft
title: "Saturday at the tool library"
timeframe: past
---

From the point of view of Workshop participants (about 10:20)

- Saturday, desk opens at 9. Three people ask for the same drill.
- Concern: "tools must come back in good order."
- The sign-out sheet lets us see who has what. It stops us seeing tools that are late.

## Edges told

| from | type | to | note |
|---|---|---|---|
| [[workshop-participants]] | holds | [[tools-come-back-in-good-order]] | Said twice in the first hour. |
| [[tools-come-back-in-good-order]] | is addressed by | [[sign-out-sheet]] | |
```

Recording an edge the narrative already tells changes nothing, so you can repeat a command safely:

```text
$ uv run scat record-edge holds workshop-participants tools-come-back-in-good-order --told-by saturday-at-the-tool-library
unchanged narrative/saturday-at-the-tool-library.md
note: narrative/saturday-at-the-tool-library.md already has this row, so nothing was written
```

### 4. Link the names

In Obsidian, link each node where the account names it, with `[[name|words as written]]`. A row's own ends are links already. Here are the three links added to the account:

```text
---
type: narrative
kind: scenario
status: draft
title: "Saturday at the tool library"
timeframe: past
---

From the point of view of [[workshop-participants|Workshop participants]] (about 10:20)

- Saturday, desk opens at 9. Three people ask for the same drill.
- Concern: "[[tools-come-back-in-good-order|tools must come back in good order]]."
- [[sign-out-sheet|The sign-out sheet]] lets us see who has what. It stops us seeing tools that are late.

## Edges told

| from | type | to | note |
|---|---|---|---|
| [[workshop-participants]] | holds | [[tools-come-back-in-good-order]] | Said twice in the first hour. |
| [[tools-come-back-in-good-order]] | is addressed by | [[sign-out-sheet]] | |
```

```text
$ uv run scat check saturday-at-the-tool-library --neighborhood
attribution mode: disallowed
warning [SCAT-DRAFT-FIELD] narrative/saturday-at-the-tool-library.md field `description`: missing (required once the page is done)
  Fix: add the line `description: "<one sentence you write>"` (author) before you set status: done
0 errors, 1 warning
```

Check one page, or a page and every page one link away, as here, as you go.

### 5. A link without a row

You may link a node that the account only mentions. Here the first bullet gains a link to a second group, the project leads:

```text
- Saturday, desk opens at 9. Three people ask for the same drill, and the [[project-leads|project leads]] hear of it.
```

The check says:

```text
$ uv run scat check saturday-at-the-tool-library --neighborhood
attribution mode: disallowed
warning [SCAT-DRAFT-FIELD] narrative/saturday-at-the-tool-library.md field `description`: missing (required once the page is done)
  Fix: add the line `description: "<one sentence you write>"` (author) before you set status: done
0 errors, 1 warning
```

No message. A narrative that links both nodes of a pair but has no row for it is a **candidate**: the tool does not know whether the account tells that edge, and that is your judgement of the field notes, not a defect. The fingerprint view shows the fingerprint (the nodes the page links and the edges it tells) and leaves such pairs out; ask for them with `--candidates` (in the REPL, `candidates=True`), so that you can decide for each whether to add a row. Run it for the narrative:

```text
$ uv run scat fingerprint saturday-at-the-tool-library --candidates
fingerprint saturday-at-the-tool-library (scenario, draft)
  group
    project-leads [stub]
    workshop-participants [stub]
  concern
    tools-come-back-in-good-order [stub]
  affordance
    sign-out-sheet [stub]
  edges
    holds: workshop-participants -> tools-come-back-in-good-order [draft; told by saturday-at-the-tool-library]
    addressed-by: tools-come-back-in-good-order -> sign-out-sheet [draft; told by saturday-at-the-tool-library]
  candidates (linked, no row)
    holds: project-leads -> tools-come-back-in-good-order
```

The last block is the candidate: the page links `project-leads` and the concern but tells no row for the pair. Add a row if the account tells the edge, and leave it if it does not. Without `--candidates` the view shows the nodes and edges only. Without a narrative name, `uv run scat fingerprint` shows every narrative. In Obsidian, the Outgoing links panel for the page shows the nodes it links, and its table shows the edges it tells. Together they are the narrative's **fingerprint**; [Analysis](analysis.md) shows the same view as a drawing.

### 6. Set it to done

Setting `done` is judged as the page would stand at `done`. It is refused while it would fail, and nothing is written:

```text
$ uv run scat set-status saturday-at-the-tool-library done
refused [SCAT-DONE-REFUSED] narrative/saturday-at-the-tool-library.md: 1 error(s) would stand at status done; status unchanged
  error [SCAT-DONE-FIELD] narrative/saturday-at-the-tool-library.md field `description`: missing on a page with status: done
    Fix, choose one:
      1. add the line `description: "<one sentence you write>"` (author)
      2. run `scat set-status saturday-at-the-tool-library draft` (REPL: `scat_kg.set_status("saturday-at-the-tool-library", "draft")`) if the page is not finished
  Fix, choose one:
    1. fix the problems above, then run `scat set-status saturday-at-the-tool-library done` again
    2. leave the page at `draft`: run `scat set-status saturday-at-the-tool-library draft` (REPL: `scat_kg.set_status("saturday-at-the-tool-library", "draft")`)
```

Fix what it lists (here, add the line `description: "Loans go unrecorded when the sheet runs out."` to the front matter), then set it again:

```text
$ uv run scat set-status saturday-at-the-tool-library done
changed narrative/saturday-at-the-tool-library.md
note: `status` set to done (was draft)
check of narrative/saturday-at-the-tool-library.md: no problems
$ uv run scat status saturday-at-the-tool-library --neighborhood
done         narrative/saturday-at-the-tool-library.md
stub         affordance/sign-out-sheet.md
stub         concern/tools-come-back-in-good-order.md
done         group/project-leads.md
done         group/workshop-participants.md
2 stub, 3 done
```

`done` is your word that the account matches the field notes and the coding is right. The tool has checked only the structure.

### 7. Change a done narrative

A `done` narrative is not frozen, but changing it is your step. `record-edge` and `remove-edge` refuse to touch one:

```text
$ uv run scat record-edge provided-by sign-out-sheet shared-spreadsheet --told-by saturday-at-the-tool-library
refused narrative/saturday-at-the-tool-library.md: the narrative is `done` and this row would change it; changing a `done` narrative is your step
  Fix: set the narrative to `draft` with `scat set-status saturday-at-the-tool-library draft` (REPL: `scat_kg.set_status("saturday-at-the-tool-library", "draft")`), run this again, then set it to `done` again; the page is checked then
```

Set it to `draft`, make the change, then set it to `done` again. Here the edge is removed. The links stay, since they belong to the account:

```text
$ uv run scat set-status saturday-at-the-tool-library draft
changed narrative/saturday-at-the-tool-library.md
note: `status` set to draft (was done)
$ uv run scat remove-edge workshop-participants tools-come-back-in-good-order
changed narrative/saturday-at-the-tool-library.md
note: removed the row at line 20 of narrative/saturday-at-the-tool-library.md
note: the links stay in the narratives; remove one by hand if the account no longer names it
```

The row is gone and the links are where they were:

```text
---
type: narrative
kind: scenario
status: draft
title: "Saturday at the tool library"
description: "Loans go unrecorded when the sheet runs out."
timeframe: past
---

From the point of view of [[workshop-participants|Workshop participants]] (about 10:20)

- Saturday, desk opens at 9. Three people ask for the same drill, and the [[project-leads|project leads]] hear of it.
- Concern: "[[tools-come-back-in-good-order|tools must come back in good order]]."
- [[sign-out-sheet|The sign-out sheet]] lets us see who has what. It stops us seeing tools that are late.

## Edges told

| from | type | to | note |
|---|---|---|---|
| [[tools-come-back-in-good-order]] | is addressed by | [[sign-out-sheet]] | |
```

```text
$ uv run scat check saturday-at-the-tool-library
attribution mode: disallowed
no problems
```

## Coding in increments

Coding is rarely done in one go. You stub something, fill it in, stub more, and fill in again, and the tool tells you what disagrees after every step. Two orders are common, and neither hides a mismatch.

**Depth first** codes one narrative at a time, as above: write the account, record its edges (which creates the nodes), link the names. **Breadth first** makes the nodes first, then links, then records the edges. Here the three nodes of a Sunday narrative are made with `scat stub`, named in the account, and checked:

```text
$ uv run scat stub sunday-at-the-desk --type narrative
created narrative/sunday-at-the-desk.md
$ uv run scat stub late-returns --type concern
created concern/late-returns.md
$ uv run scat stub reminder-text --type affordance
created affordance/reminder-text.md
```

```text
---
type: narrative
kind: scenario
status: draft
title: "Sunday at the desk"
description: "Late returns, and a text that might help."
timeframe: future
---

From the point of view of [[workshop-participants|Workshop participants]]: [[late-returns|late returns]] spoil the week. A [[reminder-text|reminder text]] on Friday would help.
```

```text
$ uv run scat check sunday-at-the-desk --neighborhood
attribution mode: disallowed
no problems
```

Linking two nodes of a pair says nothing yet, so there is no message, and each step is cheap. Then the edges, one row each:

```text
$ uv run scat record-edge holds workshop-participants late-returns --told-by sunday-at-the-desk --note "Said as the main worry."
changed narrative/sunday-at-the-desk.md
note: added `| [[workshop-participants]] | holds | [[late-returns]] | Said as the main worry. |` to narrative/sunday-at-the-desk.md at line 16
$ uv run scat record-edge addressed-by late-returns reminder-text --told-by sunday-at-the-desk
changed narrative/sunday-at-the-desk.md
note: added `| [[late-returns]] | is addressed by | [[reminder-text]] | |` to narrative/sunday-at-the-desk.md at line 17
```

```text
---
type: narrative
kind: scenario
status: draft
title: "Sunday at the desk"
description: "Late returns, and a text that might help."
timeframe: future
---

From the point of view of [[workshop-participants|Workshop participants]]: [[late-returns|late returns]] spoil the week. A [[reminder-text|reminder text]] on Friday would help.

## Edges told

| from | type | to | note |
|---|---|---|---|
| [[workshop-participants]] | holds | [[late-returns]] | Said as the main worry. |
| [[late-returns]] | is addressed by | [[reminder-text]] | |
```

```text
$ uv run scat check sunday-at-the-desk --neighborhood
attribution mode: disallowed
no problems
```

Linking a name before its page exists is the one thing that is an error at every status, because a link must reach a page. The message offers `scat stub NAME --type ...` for each type, and a row's end offers the one type the layer fixes.

## When a link and an edge disagree

A **mismatch** is a link and an edge that disagree. It happens at a row's end: the end is not a link, or links a name that is no page, or links a page that is not a node. The table has other faults too: a row in the wrong direction or between layers that are not neighbours, a row repeated within one narrative, a type the ontology does not know, or a row that is not four cells. The tool grades them all alike.

While the narrative is a `stub` or `draft`, each is a warning. Once it is `done`, each is an error, and `set-status ... done` refuses. This hand-written table has three of them:

```text
---
type: narrative
kind: scenario
status: draft
title: "Monday at the desk"
description: "A hand-written table."
timeframe: past
---

From the point of view of [[workshop-participants|Workshop participants]]: [[late-returns|late returns]] again.

## Edges told

| from | type | to | note |
|---|---|---|---|
| [[workshop-participants]] | holds | late-returns | |
| [[late-returns]] | holds | [[workshop-participants]] | |
| [[workshop-participants]] | holds | [[late-return]] | |
```

```text
$ uv run scat check monday-at-the-desk
attribution mode: disallowed
warning [SCAT-DRAFT-END-NOLINK] narrative/monday-at-the-desk.md:16:39 row 1 cell `to`: `late-returns` is not a link; each end of a row is one link, `[[page-name]]`
  Fix, choose one:
    1. replace `late-returns` with `[[late-returns]]`
    2. delete the row
warning [SCAT-DRAFT-TABLE-LAYERS] narrative/monday-at-the-desk.md:17:1 row 2: `holds` joins a group to a concern, but [[late-returns]] is a concern page, and [[workshop-participants]] is a group page
  Fix, choose one:
    1. swap the two ends: replace `[[late-returns]] | [[workshop-participants]]` with `[[workshop-participants]] | [[late-returns]]`
    2. delete the row
warning [SCAT-DRAFT-END-NOPAGE] narrative/monday-at-the-desk.md:18:39 row 3 cell `to`: [[late-return]] does not reach a page (no page is named late-return)
  Fix, choose one:
    1. replace `[[late-return]]` with `[[late-returns]]`
    2. run `scat stub late-return --type concern` (REPL: `scat_kg.stub("late-return", type="concern")`) to create a concern page
    3. delete the row
0 errors, 3 warnings
```

Each message names the row and cell, says what is wrong and gives its fixes. Setting `done` now is judged as the page would stand at `done`:

```text
$ uv run scat set-status monday-at-the-desk done
refused [SCAT-DONE-REFUSED] narrative/monday-at-the-desk.md: 3 error(s) would stand at status done; status unchanged
  error [SCAT-DONE-END-NOLINK] narrative/monday-at-the-desk.md:16:39 row 1 cell `to`: `late-returns` is not a link; each end of a row is one link, `[[page-name]]`
    Fix, choose one:
      1. replace `late-returns` with `[[late-returns]]`
      2. delete the row
  error [SCAT-DONE-TABLE-LAYERS] narrative/monday-at-the-desk.md:17:1 row 2: `holds` joins a group to a concern, but [[late-returns]] is a concern page, and [[workshop-participants]] is a group page
    Fix, choose one:
      1. swap the two ends: replace `[[late-returns]] | [[workshop-participants]]` with `[[workshop-participants]] | [[late-returns]]`
      2. delete the row
  error [SCAT-DONE-END-NOPAGE] narrative/monday-at-the-desk.md:18:39 row 3 cell `to`: [[late-return]] does not reach a page (no page is named late-return)
    Fix, choose one:
      1. replace `[[late-return]]` with `[[late-returns]]`
      2. run `scat stub late-return --type concern` (REPL: `scat_kg.stub("late-return", type="concern")`) to create a concern page
      3. delete the row
  Fix, choose one:
    1. fix the problems above, then run `scat set-status monday-at-the-desk done` again
    2. leave the page at `draft`: run `scat set-status monday-at-the-desk draft` (REPL: `scat_kg.set_status("monday-at-the-desk", "draft")`)
```

Apply the first fix to each: link the name, swap the two ends, and link the existing concern in place of the misspelt one. Rows 2 and 3 now say what row 1 says, so the check reports each as a repeat:

```text
$ uv run scat check monday-at-the-desk
attribution mode: disallowed
warning [SCAT-DRAFT-TABLE-DUPLICATE] narrative/monday-at-the-desk.md:17:1 row 2: tells the same edge as row 1 (`holds`, [[workshop-participants]], [[late-returns]]); a narrative tells an edge once
  Fix: delete the row `| [[workshop-participants]] | holds | [[late-returns]] | |`
warning [SCAT-DRAFT-TABLE-DUPLICATE] narrative/monday-at-the-desk.md:18:1 row 3: tells the same edge as row 1 (`holds`, [[workshop-participants]], [[late-returns]]); a narrative tells an edge once
  Fix: delete the row `| [[workshop-participants]] | holds | [[late-returns]] | |`
0 errors, 2 warnings
```

Delete rows 2 and 3, which leaves row 1 as the one row. The narrative passes and can be set to `done`:

```text
$ uv run scat check monday-at-the-desk
attribution mode: disallowed
no problems
$ uv run scat set-status monday-at-the-desk done
changed narrative/monday-at-the-desk.md
note: `status` set to done (was draft)
check of narrative/monday-at-the-desk.md: no problems
```

### The table in Obsidian

Obsidian's table editor re-pads the columns when you click into a table. That is harmless: the tool reads a table whatever its spacing, so a hand-aligned table passes as a compact one does.

```text
| from  | type                      | to                | note                 |
| ----- | ------------------------- | ----------------- | -------------------- |
| [[workshop-participants]] | holds | [[late-returns]]  | Said as the main worry. |
```

```text
$ uv run scat check monday-at-the-desk
attribution mode: disallowed
no problems
```

### Relationship annotations

Two pages of one type can pull against each other, such as two concerns. SCAT records that as a **relationship annotation**: a line in the body of one of the two pages, with a link to the other. It has no meaning to the tool, is not an edge and stays out of every view. The link must still reach a page, like any link:

```text
---
type: concern
status: stub
title: "Late returns"
---

Pulls against [[anonymity]]: chasing a borrower for a late tool means knowing who they are.
```

```text
$ uv run scat check late-returns --neighborhood
attribution mode: disallowed
no problems
```

## Contributor pages and `attributed_to`

Where the vault's attribution mode is `required` or `optional`, a narrative can name the people it is attributed to. Each person has a **contributor page** in `contributor/`, outside the four layers, and the narrative names them in its `attributed_to` field: a list of quoted links to those pages.

```text
attributed_to: ["[[ada-quill]]"]
```

A contributor page is no node and a link to one is no edge. The page holds a name or a handle, as the organiser records it, in its `title`. What each mode asks of a narrative:

| Mode | What the check says |
|---|---|
| `required` | A narrative names its contributors. Without `attributed_to`, a draft gets a warning (`SCAT-DRAFT-ATTR`) and `done` is an error (`SCAT-DONE-ATTR`). |
| `optional` | A narrative names its contributors or names none. The check asks for nothing. |
| `disallowed` | No narrative names a contributor and the vault holds no contributor page. Either is an error at every status (`SCAT-ATTR-DISALLOWED`), and `scat stub --type contributor` refuses. |

The [norms](norms.md#writing-together) state the same three cases. Every check prints the mode first, so you see which applies.

The examples start from a copy of the template with `attribution = "required"` in `scat.toml`, and a draft narrative `saturday-at-the-tool-library` that links a node page and has its `description` and `timeframe`, as in step 6 above, but names nobody. The check warns, and setting `done` is refused:

```text
$ uv run scat check saturday-at-the-tool-library
attribution mode: required
warning [SCAT-DRAFT-ATTR] narrative/saturday-at-the-tool-library.md field `attributed_to`: missing (required once the page is done: the vault's attribution mode is `required`)
  Fix: add the line `attributed_to: ["[[<a contributor page you link>]]"]` (author) before you set status: done
0 errors, 1 warning
$ uv run scat set-status saturday-at-the-tool-library done
refused [SCAT-DONE-REFUSED] narrative/saturday-at-the-tool-library.md: 1 error(s) would stand at status done; status unchanged
  error [SCAT-DONE-ATTR] narrative/saturday-at-the-tool-library.md field `attributed_to`: missing on a page with status: done (the vault's attribution mode is `required`)
    Fix, choose one:
      1. add the line `attributed_to: ["[[<a contributor page you link>]]"]` (author)
      2. run `scat set-status saturday-at-the-tool-library draft` (REPL: `scat_kg.set_status("saturday-at-the-tool-library", "draft")`) if the page is not finished
  Fix, choose one:
    1. fix the problems above, then run `scat set-status saturday-at-the-tool-library done` again
    2. leave the page at `draft`: run `scat set-status saturday-at-the-tool-library draft` (REPL: `scat_kg.set_status("saturday-at-the-tool-library", "draft")`)
```

Make the contributor page with `scat stub`, then link it in the narrative's front matter:

```text
$ uv run scat stub ada-quill --type contributor
created contributor/ada-quill.md
```

```text
---
type: contributor
status: stub
title: "Ada quill"
---
```

Write the name as the organiser records it in the `title` (here, "Ada Quill"), and add `attributed_to: ["[[ada-quill]]"]` to the narrative. A link reaches a page, or the check reports it:

```text
$ uv run scat check saturday-at-the-tool-library
attribution mode: required
no problems
```

In a `disallowed` vault the same field is refused. Here `scat.toml` says `attribution = "disallowed"`, and the narrative carries the field above:

```text
$ uv run scat check saturday-at-the-tool-library
attribution mode: disallowed
error [SCAT-ATTR-DISALLOWED] narrative/saturday-at-the-tool-library.md field `attributed_to`: present, and the vault's attribution mode is `disallowed`
  Fix: delete the field `attributed_to` (all its lines): this vault's attribution mode is `disallowed`; the coder who wants contributors named changes `attribution` in scat.toml for the whole vault
1 error, 0 warnings
```

The mode belongs to the whole vault and the organiser sets it before the first session. The tool never changes it. If you change it, the next whole-vault check reads every page against the new mode.

`scat attribution` lists each contributor page with the narratives that name it, and the narratives that name none. It refuses in a `disallowed` vault. Its reference is in the [CLI reference](reference/cli.md), and its Python form is in the [Python API reference](reference/api.md#scat_kgattribution).

## The operations

Every operation has two spellings that give the same messages: the Python REPL (`uv run python`, then `import scat_kg` once) and the command line. Each step shows both. The names differ between the two spellings, so you can type both in one vault. All of them write only new files or the lines they name, and none of them writes a narrative's account.

### Check, at three scopes

`check` reads the vault and writes nothing. It has three scopes: **one page**, the quickest; **a page and every page one link away**, in either direction, which you use after adding links; and **the whole vault**, which you use before you commit. A page is named by its name (`anonymity`) or its path from the vault folder (`concern/anonymity.md`).

=== "Python (REPL)"

    ```python
    import scat_kg
    scat_kg.check()
    scat_kg.check("anonymity")
    scat_kg.check("anonymity", neighborhood=True)
    ```

    ```text
    attribution mode: disallowed
    no problems

    attribution mode: disallowed
    no problems

    attribution mode: disallowed
    no problems
    ```

=== "CLI"

    ```bash
    uv run scat check
    uv run scat check anonymity
    uv run scat check anonymity --neighborhood
    ```

    ```text
    attribution mode: disallowed
    no problems

    attribution mode: disallowed
    no problems

    attribution mode: disallowed
    no problems
    ```

Every check prints the vault's attribution mode first. The template's own example is clean, and its mode is `disallowed`. Warnings do not block: a command exits with 0 unless there is an error.

### Stub: make a page

`stub` makes one page of the type you name (`group`, `concern`, `affordance`, `technology` or `narrative`, and `contributor` where the vault's attribution mode is `required` or `optional`) with `status: stub`. It refuses a name that is taken, a name that is not legal (lower-case letters, digits and single hyphens), a new group that would go over the cap, and a contributor page in a `disallowed` vault.

=== "Python (REPL)"

    ```python
    scat_kg.stub("lending-desk-opens-on-time", type="concern")
    scat_kg.stub("desk-notes-one", type="narrative")
    ```

    ```text
    created concern/lending-desk-opens-on-time.md

    created narrative/desk-notes-one.md
    ```

=== "CLI"

    ```bash
    uv run scat stub volunteers-are-easy-to-find --type concern
    uv run scat stub desk-notes-two --type narrative
    ```

    ```text
    created concern/volunteers-are-easy-to-find.md

    created narrative/desk-notes-two.md
    ```

### Record an edge, and remove one

`record-edge` takes the type, the two nodes and the narrative that tells it. It adds a row to that narrative, makes a missing node or narrative as a stub, and leaves every link alone. `remove-edge` deletes the rows that tell a pair, from the narratives you name with `--told-by` or, without it, from every narrative that tells it. Both refuse a narrative that is `done`.

=== "Python (REPL)"

    ```python
    scat_kg.record_edge("holds", "workshop-participants", "lending-desk-opens-on-time", ["desk-notes-one"], note="Said twice.")
    scat_kg.remove_edge("workshop-participants", "lending-desk-opens-on-time")
    ```

    ```text
    changed narrative/desk-notes-one.md

    note: added `| [[workshop-participants]] | holds | [[lending-desk-opens-on-time]] | Said twice. |` to narrative/desk-notes-one.md at line 12

    changed narrative/desk-notes-one.md

    note: removed the row at line 12 of narrative/desk-notes-one.md

    note: the links stay in the narratives; remove one by hand if the account no longer names it
    ```

=== "CLI"

    ```bash
    uv run scat record-edge holds workshop-participants volunteers-are-easy-to-find --told-by desk-notes-two --note "Said twice."
    uv run scat remove-edge workshop-participants volunteers-are-easy-to-find
    ```

    ```text
    changed narrative/desk-notes-two.md

    note: added `| [[workshop-participants]] | holds | [[volunteers-are-easy-to-find]] | Said twice. |` to narrative/desk-notes-two.md at line 12

    changed narrative/desk-notes-two.md

    note: removed the row at line 12 of narrative/desk-notes-two.md

    note: the links stay in the narratives; remove one by hand if the account no longer names it
    ```

### Stub links

`stub-links` makes the node pages that the ends of rows link and the vault lacks, as the type the layer fixes. A link in the account has no layer, so it needs `scat stub NAME --type ...`. With nothing to make, it says so:

=== "Python (REPL)"

    ```python
    scat_kg.stub_links()
    ```

    ```text
    stub-links: nothing to do
    ```

=== "CLI"

    ```bash
    uv run scat stub-links
    ```

    ```text
    stub-links: nothing to do
    ```

### Status, and set-status

`status` lists each page's status and the counts, at the same three scopes as `check`. `set-status` moves a page between `stub`, `draft` and `done`; setting the status a page already has changes nothing. Setting `done` is checked, as in step 6.

=== "Python (REPL)"

    ```python
    scat_kg.status("desk-notes-one")
    scat_kg.set_status("desk-notes-one", "draft")
    ```

    ```text
    stub         narrative/desk-notes-one.md

    1 stub

    changed narrative/desk-notes-one.md

    note: `status` set to draft (was stub)
    ```

=== "CLI"

    ```bash
    uv run scat status desk-notes-two
    uv run scat set-status desk-notes-two draft
    ```

    ```text
    stub         narrative/desk-notes-two.md

    1 stub

    changed narrative/desk-notes-two.md

    note: `status` set to draft (was stub)
    ```

### Index: the index pages

An index page lists the pages of one type. It is an Obsidian Base, `index/<type>.base`, which reads the vault itself, so it cannot go stale. `index` writes the ones that are missing and never rewrites one, so you can add a column to a Base by hand. The template ships all five, so on a fresh copy every line says `unchanged`:

=== "Python (REPL)"

    ```python
    scat_kg.index()
    ```

    ```text
    unchanged index/group.base

    unchanged index/concern.base

    unchanged index/affordance.base

    unchanged index/technology.base

    unchanged index/narrative.base
    ```

=== "CLI"

    ```bash
    uv run scat index
    ```

    ```text
    unchanged index/group.base

    unchanged index/concern.base

    unchanged index/affordance.base

    unchanged index/technology.base

    unchanged index/narrative.base
    ```

Open `index/concern.base` in Obsidian (1.9 or later) to see every concern at a glance, with its status and description.

## How to read a message

Every message has the same parts, as in this one from step 6 above:

```text
error [SCAT-DONE-FIELD] narrative/saturday-at-the-tool-library.md field `description`: missing on a page with status: done
  Fix, choose one:
    1. add the line `description: "<one sentence you write>"` (author)
    2. run `scat set-status saturday-at-the-tool-library draft` (REPL: `scat_kg.set_status("saturday-at-the-tool-library", "draft")`) if the page is not finished
```

1. **Severity.** `error` blocks. `warning` does not. `refused` means a command did not run, and nothing was written.
2. **The rule id**, in square brackets. It names the rule. Rule ids with `DRAFT` are the warnings a `stub` or `draft` gets; the same rule with `DONE` is the error at `done`.
3. **The file**, the line and column, and the row and cell when it is a table.
4. **What is wrong**, in one sentence.
5. **The fix.** An exact command, or an exact line to write or delete. A fix marked `(author)` is a line only you can word.

Do what the fix says, then check again.

## What the check does not judge

The check looks at structure: that a page has the fields its type needs, that every link reaches a page, that every row is well formed and joins the right layers. It does not judge what your notes say. A forgotten edge is graded by no rule: only you know the account tells it. Tensions, matches and gaps are for analysis, which comes after the check passes and you have signed off the content.

## Reaching a clean whole-vault check

"Clean" means **zero errors**. A check with nothing to report prints `no problems`. Work in this order:

1. Run `uv run scat check`. Read the errors first.
2. Fix each the way its `Fix:` line says. Check the page, then its neighbourhood, then the whole vault.
3. Run `uv run scat check` again. When it ends `0 errors` or prints `no problems`, you are clean.

Aim to bring every narrative you made to `done`. A page left at `stub` or `draft` does not stop a clean check, because an unfinished page is never faulted for being unfinished. Then look at the warnings: each is a to-do.

## Commit and push

Your vault is a git repository, and your repository is private. Save the work as a commit, then push it. These are not tool commands, so they are `text`:

```text
git status
git add .
git commit -m "Code the notes from my first session"
git push
```

Run `git status` first and read the list: it shows what the commit will hold. `git add .` stages every change in the folder that git does not ignore, so it also stages a drawing such as `fingerprint.png` and a plan file such as `plan.txt`, not only the model. To leave such a file out, name the files you want instead (`git add narrative group concern affordance technology`) or list the file in `.gitignore`; to keep it, do nothing and it goes into the commit with the rest. If the list holds any other change you did not mean to make, sort that out before you go on. Commit when the whole-vault check ends with zero errors. If `git status` says there is nothing to commit, your work is already saved: go on to `git push`, or to the lock below.

## Lock a version

To state that the vault is finished, lock the version: a git tag on the commit you pushed, then push the tag. Like the commands above, these are not tool commands:

```text
git tag v1
git push origin v1
```

The tag name is yours to choose: `v1` is only an example, and any name that is not already a tag will do. The tag names that commit for good; later commits do not move it. Locking is your statement that the vault is finished, and `git tag` does not run the tool. Stub pages do not stop you: the tool never faults a page for being unfinished. Run the whole-vault check first, so the version you lock is clean.

### See which commit a tag pins

To read off the commit a tag names, ask git. `git rev-parse` prints the full commit hash, and `git show --stat` shows that commit's message and the files it changed:

```text
$ git rev-parse v1^{commit}
31da04dc8bf6416a2328384572727a044a58fbf1
$ git show --stat v1
commit 31da04dc8bf6416a2328384572727a044a58fbf1
Author: t <t@example.com>
Date:   Wed Nov 25 05:25:20 2026 -0500

    Code the notes from my first session

 affordance/sign-out-sheet.md              |   5 +++++
 concern/tools-come-back-in-good-order.md  |   5 +++++
 fingerprint.png                           | Bin 0 -> 22130 bytes
 group/workshop-participants.md            |   5 +++++
 narrative/saturday-at-the-tool-library.md |  21 +++++++++++++++++++++
 5 files changed, 36 insertions(+)
```

Your hash, author, date and files will differ. To see the commit you have, `git log --oneline --decorate -3` marks the tag beside it. To see that the tag reached GitHub and names the same commit, ask the remote:

```text
$ git ls-remote --tags origin v1
31da04dc8bf6416a2328384572727a044a58fbf1	refs/tags/v1
```

The two hashes match when the tag you pushed is the tag you locked.

## Look at it in Obsidian

Open the vault folder in Obsidian (**Open folder as vault**, version 1.9 or later):

- **Links.** Every `[[name]]` is a link. Click it to go to that page.
- **Backlinks.** Open a concern and look at the Backlinks panel. It lists every narrative that names the concern, which is how you ask "who tells this?" without a second list.
- **Outgoing links.** Open a narrative and look at the Outgoing links panel: the nodes it links, which with its table are its fingerprint.
- **Graph view.** Each page is a dot and each link a line. Obsidian draws every page as a node here, narratives included.
- **Index pages.** The Bases in `index/` list every page of one type.

Obsidian shows the vault. Only the tool checks it, so run `uv run scat check` before you commit.

## Where next

Keep the reference close:

- [Python API reference](reference/api.md): every REPL call, with all its options.
- [CLI reference](reference/cli.md): every command and its full help text.
- [The flow](flow.md): where coding sits between capture and analysis.
- [Coding paths](coding-paths.md): coding with an assistant, in [an AI chatbot](chat-path.md) (with its [leave no trace](leave-no-trace.md) variant), [an AI IDE](ide.md) or [a local LLM](local-llm.md).
- [Facilitating scenarios](facilitate-scenarios.md) and [Facilitating architectures](facilitate-architectures.md): collect the next round of notes.
- [Planning](planning.md): revisit your groups before the next workshop.
- [Home](index.md)
