# Coding

!!! tip "Your next step"
    In your vault folder, run `uv run scat check` and read what it says.

Coding means linking the nodes a narrative names and recording the edges it tells, on the narrative's own page.

A **narrative** is one account drawn from your field notes, kept on one page. Coding is the step where that account becomes part of the knowledge graph. You write the account, link each group, concern, affordance or technology where the account names it, and add one row to the page's `Edges told` table for each edge the account tells. The tool checks the result and tells you in plain words what still disagrees. Nothing is copied to a second page: you code in the same page you wrote the account in. The [home page](index.md) defines the four kinds of node, and the [terms](reference/terms.md) page defines every other word used here.

## Before you start

- A vault set up as in [Getting started](getting-started.md): the folder holds `scat.toml`, you are inside it in Terminal, and `uv sync` has run.
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
| `narrative` | `narrative/` | one account, with the table of edges it tells | you |
| index pages | `index/` | a list of the pages of one type | `scat index`, once |

An **edge** is no page. It is one row of a narrative's `Edges told` table, and there are three types, fixed by the layers they join:

| Edge type | Name it as | The `from` node is a | The `to` node is a |
|---|---|---|---|
| `holds` | `holds` | `group` | `concern` |
| `is addressed by` | `addressed-by` | `concern` | `affordance` |
| `is provided by` | `provided-by` | `affordance` | `technology` |

The tool builds the knowledge graph from the pages on every call and never holds it. It has one edge for each (type, from, to), and the edge names every narrative that has a row for it. An edge is `done` when every narrative that tells it is `done`, so you sign off edges by signing off narratives. A **link** is only "this page refers to that one". A link never makes an edge; only a row does.

## The coding loop

You work each narrative round the same four steps, as often as it takes:

1. **Interpreting.** Read the field notes, and later the views, and decide what they say. This is yours alone.
2. **Authoring.** Write or revise the account on the narrative page. An assistant may draft it; the wording you keep is yours.
3. **Coding.** Link each node where the account names it, and record each edge it tells.
4. **Reviewing.** Run the check, then fix what it reports. You confirm two things yourself: the account matches the field notes, and the coding is a correct use of SCAT. The tool cannot judge either.

When the check passes and you confirm both, set the narrative to `done`. Done is not frozen: to change a `done` narrative you set it back to `draft`, edit, then set `done` again, and the tool checks it again then.

### The three actors

- **You, the coder,** own interpretation. You alone move a narrative into or out of `done`.
- **The tool** owns conformance. It checks that the knowledge graph matches the pages and that it obeys the ontology. No part of the tool can tell who is calling it.
- **An assistant,** where your participation terms allow one, helps and holds no authority. It may draft and may run the commands. Which data an assistant may touch is settled before the first session: see [Data, rights and consent](data-and-consent.md).

On the chat path, the server never moves a page into or out of `done`, so the assistant cannot, by construction. On the IDE path an assistant can run `scat set-status`, because the command cannot tell who types it. That is a residual risk, accepted: there, authority holds by the rules written for the assistant and by your review of what it changed in git (`git diff` before every commit), not by the tool.

## Where narratives and their edges come from

Everything starts in the field notes, and only you read them. You turn what a session told into one narrative page, with `scat stub` making the empty page and you writing the account. The narrative is where each edge comes from: a row of its `Edges told` table says "this account tells that a group holds that concern". There is no other place an edge is written, and no page to open for one.

Two narratives can tell the same edge. Each has its own row and its own note, and the knowledge graph has one edge naming both. A narrative that mentions two nodes without a row for the pair has not told an edge, even if the notes would support one: the row is your statement that the account tells it.

## A narrative, start to finish

This is one narrative coded the way most people begin, writing first and recording edges as they come. Each `$` line is a command you type, without the `$`; the lines under it are exactly what the tool prints. Page content is what you type in Obsidian.

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
timeframe: # past | future | mixed
---
```

The check does not fault an unfinished page. It notes, as a warning, what `done` will need:

```text
$ uv run scat check saturday-at-the-tool-library
warning [SCAT-DRAFT-FIELD] narrative/saturday-at-the-tool-library.md field `timeframe`: missing (required once the page is done)
  Fix, choose one before you set status: done:
    1. replace the line `timeframe: # past | future | mixed` with `timeframe: past` (author)
    2. replace the line `timeframe: # past | future | mixed` with `timeframe: future` (author)
    3. replace the line `timeframe: # past | future | mixed` with `timeframe: mixed` (author)
0 errors, 1 warning
```

### 2. Write the account

Open the page in Obsidian and write the account under the front matter, as it was told. Set `kind` to `scenario` (a story of people doing things over time) or `architecture` (how parts fit into tools), set `timeframe` to `past`, `future` or `mixed` (see [past or future](facilitate-scenarios.md#past-or-future-one-at-a-time)), and change `status` to `draft`. The `description` can wait. The links come next.

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

The check shows the to-do for the `description`, and notices that the account names a group the vault already has and asks you to link it:

```text
$ uv run scat check saturday-at-the-tool-library
warning [SCAT-DRAFT-FIELD] narrative/saturday-at-the-tool-library.md field `description`: missing (required once the page is done)
  Fix: add the line `description: "<one sentence you write>"` (author) before you set status: done
warning [SCAT-MENTION] narrative/saturday-at-the-tool-library.md:9:27 text `Workshop participants`: names the group page [[workshop-participants]] but does not link it
  Fix: on line 9 replace `Workshop participants` with `[[workshop-participants|Workshop participants]]`
0 errors, 2 warnings
```

### 3. Record the edges

Each edge the account tells is a row. `record-edge` writes the row for you, and creates the node pages the row names if the vault lacks them, as stubs of the right type: the layer fixes the type. `--told-by` names the narrative:

```text
$ uv run scat record-edge holds workshop-participants tools-come-back-in-good-order --told-by saturday-at-the-tool-library --note "Said twice in the first hour."
created concern/tools-come-back-in-good-order.md
changed narrative/saturday-at-the-tool-library.md
note: added `| holds | [[workshop-participants]] | [[tools-come-back-in-good-order]] | Said twice in the first hour. |` to narrative/saturday-at-the-tool-library.md at line 19
$ uv run scat record-edge addressed-by tools-come-back-in-good-order sign-out-sheet --told-by saturday-at-the-tool-library
created affordance/sign-out-sheet.md
changed narrative/saturday-at-the-tool-library.md
note: added `| is addressed by | [[tools-come-back-in-good-order]] | [[sign-out-sheet]] | |` to narrative/saturday-at-the-tool-library.md at line 20
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

| type | from | to | note |
|---|---|---|---|
| holds | [[workshop-participants]] | [[tools-come-back-in-good-order]] | Said twice in the first hour. |
| is addressed by | [[tools-come-back-in-good-order]] | [[sign-out-sheet]] | |
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

| type | from | to | note |
|---|---|---|---|
| holds | [[workshop-participants]] | [[tools-come-back-in-good-order]] | Said twice in the first hour. |
| is addressed by | [[tools-come-back-in-good-order]] | [[sign-out-sheet]] | |
```

```text
$ uv run scat check saturday-at-the-tool-library --neighborhood
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
warning [SCAT-DRAFT-FIELD] narrative/saturday-at-the-tool-library.md field `description`: missing (required once the page is done)
  Fix: add the line `description: "<one sentence you write>"` (author) before you set status: done
0 errors, 1 warning
```

No message. A narrative that links both nodes of a pair but has no row for it is a **candidate**: the tool does not know whether the account tells that edge, and that is your judgement of the field notes, not a defect. The fingerprint view lists such pairs, so that you can decide for each whether to add a row. That view is not one of the `scat` commands yet. Until it arrives, Obsidian's Outgoing links panel for the page shows the nodes it links, and its table shows the edges it tells. Together they are the narrative's **fingerprint**.

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

| type | from | to | note |
|---|---|---|---|
| is addressed by | [[tools-come-back-in-good-order]] | [[sign-out-sheet]] | |
```

```text
$ uv run scat check saturday-at-the-tool-library
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
no problems
```

Linking two nodes of a pair says nothing yet, so there is no message, and each step is cheap. Then the edges, one row each:

```text
$ uv run scat record-edge holds workshop-participants late-returns --told-by sunday-at-the-desk --note "Said as the main worry."
changed narrative/sunday-at-the-desk.md
note: added `| holds | [[workshop-participants]] | [[late-returns]] | Said as the main worry. |` to narrative/sunday-at-the-desk.md at line 16
$ uv run scat record-edge addressed-by late-returns reminder-text --told-by sunday-at-the-desk
changed narrative/sunday-at-the-desk.md
note: added `| is addressed by | [[late-returns]] | [[reminder-text]] | |` to narrative/sunday-at-the-desk.md at line 17
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

| type | from | to | note |
|---|---|---|---|
| holds | [[workshop-participants]] | [[late-returns]] | Said as the main worry. |
| is addressed by | [[late-returns]] | [[reminder-text]] | |
```

```text
$ uv run scat check sunday-at-the-desk --neighborhood
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

| type | from | to | note |
|---|---|---|---|
| holds | [[workshop-participants]] | late-returns | |
| holds | [[late-returns]] | [[workshop-participants]] | |
| holds | [[workshop-participants]] | [[late-return]] | |
```

```text
$ uv run scat check monday-at-the-desk
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

Apply the first fix to each: link the name, swap the two ends, and link the existing concern in place of the misspelt one. Swapping the ends of row 2 gave it the same pair as row 1, and the check says so:

```text
$ uv run scat check monday-at-the-desk
warning [SCAT-DRAFT-TABLE-DUPLICATE] narrative/monday-at-the-desk.md:17:1 row 2: tells the same edge as row 1 (`holds`, [[workshop-participants]], [[late-returns]]); a narrative tells an edge once
  Fix: delete the row `| holds | [[workshop-participants]] | [[late-returns]] | |`
0 errors, 1 warning
```

Delete the second row, and the narrative passes and can be set to `done`:

```text
$ uv run scat check monday-at-the-desk
no problems
$ uv run scat set-status monday-at-the-desk done
changed narrative/monday-at-the-desk.md
note: `status` set to done (was draft)
```

### The table in Obsidian

Obsidian's table editor re-pads the columns when you click into a table. That is harmless: the tool reads a table whatever its spacing, so a hand-aligned table passes as a compact one does.

```text
| type  | from                      | to                | note                 |
| ----- | ------------------------- | ----------------- | -------------------- |
| holds | [[workshop-participants]] | [[late-returns]]  | Said as the main worry. |
```

```text
$ uv run scat check monday-at-the-desk
no problems
```

### Relationship annotations

Two entries of one type can pull against each other, such as two concerns. SCAT records that as a **relationship annotation**: a line in the body of one of the two pages, with a link to the other. It has no meaning to the tool, is not an edge and stays out of every view. The link must still reach a page, like any link:

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
no problems
```

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
    no problems

    no problems

    no problems
    ```

=== "CLI"

    ```bash
    uv run scat check
    uv run scat check anonymity
    uv run scat check anonymity --neighborhood
    ```

    ```text
    no problems

    no problems

    no problems
    ```

The template's own example is clean. Warnings do not block: a command exits with 0 unless there is an error.

### Stub: make a page

`stub` makes one page of the type you name (`group`, `concern`, `affordance`, `technology` or `narrative`) with `status: stub`. It refuses a name that is taken, a name that is not legal (lower-case letters, digits and single hyphens), and a new group that would go over the cap.

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

    note: added `| holds | [[workshop-participants]] | [[lending-desk-opens-on-time]] | Said twice. |` to narrative/desk-notes-one.md at line 12

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

    note: added `| holds | [[workshop-participants]] | [[volunteers-are-easy-to-find]] | Said twice. |` to narrative/desk-notes-two.md at line 12

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

Run `git status` first and read the list: it shows what the commit will hold. `git add .` stages every change in the folder, so if the list holds a change you did not mean to make, sort that out before you go on. Commit when the whole-vault check ends with zero errors.

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
- [Facilitating scenarios](facilitate-scenarios.md) and [Facilitating architectures](facilitate-architectures.md): collect the next round of notes.
- [Planning](planning.md): revisit your groups before the next workshop.
- [Home](index.md)
