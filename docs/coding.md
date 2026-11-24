# Coding

!!! tip "Your next step"
    In your vault folder, run `uv run scat check` and read what it says.

Coding means reading a raw page, then restating its meaning in plain words.

Coding is the step where your raw notes become part of the graph. You read each raw scenario or raw architecture and write each raw page again as a **coded page**. Restate each raw page in your own plain words. Keep its meaning, and add no judgement of your own. A coded page names the stakeholder groups, concerns, affordances and technologies the notes talk about. A **concern** is something a group cares about. An **affordance** is something a tool or arrangement lets someone do. A **technology** is the thing that provides it. The [home page](index.md) defines all four. You do not summarise or judge. You name what is there, keeping the meaning of the raw wording. The raw page stays exactly as it was written; the coded page is a separate page that reads it.

You say which things the notes name. The tools create the pages and links that follow, and the checker tells you in plain words what is still wrong. Two links you write by hand: the `raw:` link on the coded page, which says which raw page it reads, and the `coded:` link on the raw page. The check names the `coded:` link when it is missing (`SCAT-RAW-BACKLINK`), and you add it. This page shows the whole loop, from start to finish: a raw page, a pushed commit and a look at the graph.

## Before you start

- A vault set up as in [Getting started](getting-started.md): the folder holds `scat.toml`, you are inside it in Terminal, and `uv sync` has run. While SCAT is a preview being tried before its first release, a fresh clone may need `git checkout dev` first.
- Remove the worked example from your vault before you add any page of your own: see [Start your own content](getting-started.md#5-start-your-own-content). If you already added pages, the same step still works, and the check lists draft warnings for them and no errors.
- Raw notes saved as raw pages, from [Facilitating scenarios](facilitate-scenarios.md) or [Facilitating architectures](facilitate-architectures.md). In hand, you need a few plain sentences of raw notes, written as they were told.
- Your stakeholder groups, planned in the [planning guide](planning.md) and named by role. In hand, you need a short list of the groups, one name per group.

Every operation below has two spellings that give the same messages. Each step shows the Python REPL way first and the command-line way beside it. To open the REPL, type `uv run python`, then `import scat_kg` once. The commands on this page can all be typed in a copy of the template vault, so you can follow along and lose nothing. The worked example is a small community tool library.

## What the pages are

There are four kinds of thing in a vault (SCAT), three kinds of relation page, raw and coded pages, and class pages.

| Page type | Folder | What it holds | Who writes it |
|---|---|---|---|
| `stakeholder-group` | `stakeholder-group/` | a group, named by role | you, or `scat stub` |
| `concern` | `concern/` | an interest someone holds | you, or `scat stub` |
| `affordance` | `affordance/` | something that can be done | you, or `scat stub` |
| `technology` | `technology/` | a thing that provides an affordance | you, or `scat stub` |
| `heldby` | `heldby/` | this group holds this concern | the tools, from a pair you name |
| `addresses` | `addresses/` | this affordance addresses this concern | the tools, from a pair you name |
| `attributes` | `attributes/` | this affordance is attributed to this technology | the tools, from a pair you name |
| `scenario-raw`, `architecture-raw` | `scenario-raw/`, `architecture-raw/` | the notes as told | you |
| `scenario-coded`, `architecture-coded` | `scenario-coded/`, `architecture-coded/` | your reading of one raw page | you |
| `class` | `class/` | a generated table of every page of one kind | `scat index` |

A **relation page** says one fact: a group holds a concern, an affordance addresses a concern, an affordance is attributed to a technology. You do not write its structure. You name the pair, and the tools write the page with both ends filled in. You then add a description, and a note on how this group holds this concern if you have one. The order of the pair matters:

| Relation | Name the pair as |
|---|---|
| `heldby` | group, then concern |
| `addresses` | concern, then affordance |
| `attributes` | affordance, then technology |

Choose each pair from the notes. For `heldby`, take a group and one concern that group voiced in its own words. For `addresses`, take that concern and an affordance the notes show answering it. For `attributes`, take that affordance and the technology the notes name as providing it. The description of a relation page is one sentence saying that fact in plain words, for example `description: "Participants want borrowed tools returned in the state they left."` If the notes name no group for a concern, use the group assigned to that note in your session plan. If that is not known, create no pair and leave the gap recorded.

### The linking rules

A coded page links to the pages it relates, and what it relates depends on what it is.

- A **scenario** relates **groups, concerns and affordances**. It tells what people did and cared about.
- An **architecture** relates **concerns, affordances and technologies**. It tells what a design offers and what provides it.

Both link back to the raw page they were read from, in `raw`. Here is the coded scenario of some tool-library notes. It is page content, which you type in Obsidian, so it is a `text` block and not a command:

```text
---
type: scenario-coded
status: draft
title: "Saturday at the tool library, coded"
description: "Loans go unrecorded when the sheet runs out."
raw:
  - "[[saturday-at-the-tool-library]]"
groups:
  - "[[workshop-participants]]"
concerns:
  - "[[tools-come-back-in-good-order]]"
affordances:
  - "[[sign-out-sheet]]"
---

Read from [[saturday-at-the-tool-library]].
```

A coded architecture has the same shape, with `technologies` where a scenario has `groups`:

```text
---
type: architecture-coded
status: draft
title: "Shared sheet pitch, coded"
description: "A shared spreadsheet provides the sign-out sheet."
raw:
  - "[[shared-sheet-pitch]]"
concerns:
  - "[[tools-come-back-in-good-order]]"
affordances:
  - "[[sign-out-sheet]]"
technologies:
  - "[[shared-spreadsheet]]"
---

Read from [[shared-sheet-pitch]].
```

The raw page lists its coded pages in `coded`, so a reader can walk both ways. The tools check this and tell you if one side is missing.

## Where raw and coded pages come from

A raw page is the notes as told. Its body holds the plain-sentence notes, written as they were told, with no links. The [facilitation guides](facilitate-scenarios.md) teach how to write one, so this page does not repeat it. `scat stub` is the one way to create a raw or a coded page. Run `scat stub <name> --type scenario-raw` (or `scenario-coded`, `architecture-raw`, `architecture-coded`). Name a coded page after its raw page with `-coded` on the end.

A stub starts at `status: stub`, with only `type`, `status` and `title`: no `description` and no `coded` or `raw` line. A raw page's stub also has an empty `timeframe:` line, which you fill from the [facilitation guides](facilitate-scenarios.md)' phrase list.

For example, the stub of a raw page and of its coded page, as the tool makes them:

```text
$ uv run scat stub saturday-at-the-tool-library --type scenario-raw
created scenario-raw/saturday-at-the-tool-library.md
$ uv run scat stub saturday-at-the-tool-library-coded --type scenario-coded
created scenario-coded/saturday-at-the-tool-library-coded.md
```

```text
---
type: scenario-raw
status: stub
title: "Saturday at the tool library"
timeframe: # past | future | mixed
---
```

```text
---
type: scenario-coded
status: stub
title: "Saturday at the tool library coded"
---
```

You then write the notes into the raw page and the links into the coded page, as in the example above.

## Status: stub, draft, done

Every page of your own carries a `status`. It usually moves forward as you work, and you can set it back:

| Status | Meaning |
|---|---|
| `stub` | the page exists because something links to it. It has the minimum. |
| `draft` | you are writing it. |
| `done` | you finished it. The full contract applies. |

**An unfinished page is never an error for being unfinished.** A stub or a draft that lacks a description gets no error, and at most a warning that the page is not finished. Links and relation ends are checked at every status, because a link to a page that does not exist is wrong whatever the status. Class pages are generated and carry no status.

## The operations, in the order you meet them

### Check, at three scopes

`check` reads the vault and writes nothing. Run it often. It has three scopes:

- **One page**: the page you just touched. The quickest.
- **Neighbourhood**: the page and every page one link away, in either direction. Use it after you add links.
- **Whole vault**: every page. Use it before you commit.

A page is named by its name (`gated-approval`) or by its path from the vault folder (`affordance/gated-approval.md`).

=== "Python (REPL)"

    ```python
    import scat_kg
    scat_kg.check()
    ```

=== "CLI"

    ```bash
    uv run scat check
    ```

```text
no problems
```

The template's own example is clean. Warnings, when there are any, do not block. A command exits with 0 unless there is an error, so "0 errors" is a pass. Now one page, then its neighbourhood:

=== "Python (REPL)"

    ```python
    scat_kg.check("gated-approval")
    scat_kg.check("gated-approval", neighborhood=True)
    ```

=== "CLI"

    ```bash
    uv run scat check gated-approval
    uv run scat check gated-approval --neighborhood
    ```

```text
no problems
no problems
```

### Stub: create pages, never write structure

The tools create the page, as a `stub`, for anything a link needs. Three commands:

- `stub` makes one page of a kind you name: `concern`, `affordance`, `technology`, `stakeholder-group`, or a raw or coded page (`scenario-raw`, `scenario-coded`, `architecture-raw`, `architecture-coded`). It refuses a name that is already taken.
- `stub-pair` makes the relation page for a pair, and stubs an end that does not exist. Run it once for each pair you find in the notes. Naming the same pair again changes nothing.
- `stub-links` makes the pages that link fields name and the vault lacks. Use it after you write a coded page, to create everything the page points at.

`stub` refuses a name that is already taken, so the two spellings below make two different concerns. Type one spelling, or both.

=== "Python (REPL)"

    ```python
    scat_kg.stub("lending-desk-opens-on-time", type="concern")
    ```

=== "CLI"

    ```bash
    uv run scat stub volunteers-are-easy-to-find --type concern
    ```

```text
created concern/lending-desk-opens-on-time.md
```

The CLI line prints `created concern/volunteers-are-easy-to-find.md`. Each is a stub, so neither is an error. A stub stays a stub until you write it.

Now the three pairs. The group already exists in the template. The tools create the concern, the affordance and the technology that the pairs name:

=== "Python (REPL)"

    ```python
    scat_kg.stub_pair("heldby", "workshop-participants", "tools-come-back-in-good-order")
    scat_kg.stub_pair("addresses", "tools-come-back-in-good-order", "sign-out-sheet")
    scat_kg.stub_pair("attributes", "sign-out-sheet", "shared-spreadsheet")
    ```

=== "CLI"

    ```bash
    uv run scat stub-pair heldby workshop-participants tools-come-back-in-good-order
    uv run scat stub-pair addresses tools-come-back-in-good-order sign-out-sheet
    uv run scat stub-pair attributes sign-out-sheet shared-spreadsheet
    ```

```text
created concern/tools-come-back-in-good-order.md
created heldby/workshop-participants-holds-tools-come-back-in-good-order.md
note: write `description`, `notes` and the body in heldby/workshop-participants-holds-tools-come-back-in-good-order.md; the endpoints are filled
created affordance/sign-out-sheet.md
created addresses/tools-come-back-in-good-order-addresses-sign-out-sheet.md
note: write `description`, `notes` and the body in addresses/tools-come-back-in-good-order-addresses-sign-out-sheet.md; the endpoints are filled
created technology/shared-spreadsheet.md
created attributes/sign-out-sheet-attributed-to-shared-spreadsheet.md
note: write `description`, `notes` and the body in attributes/sign-out-sheet-attributed-to-shared-spreadsheet.md; the endpoints are filled
```

A relation page's file name is made from its title, joined by the relation's verb, and cut at 64 characters, not counting `.md`. If a pair's names are long, the file name is shorter than the two names together and may end partway through a word, and a clash with an existing name adds `-2`, `-3` and so on. The full title stays in the page's `title:` line, and you need not rename the file.

That is the output of the first spelling you type. The second spelling prints `unchanged <file>` and a note that the page already states the pair, for each of the three. Nothing is written twice.

Open one of the new pages. The tools wrote everything except what only you know:

```text
---
type: heldby
status: stub
title: "Workshop participants holds Tools come back in good order"
group: "[[workshop-participants]]"
concern: "[[tools-come-back-in-good-order]]"
---
```

Nothing in the body is required. You add a `description` and, if you have one, an optional one-line `notes` on how this group holds this concern. In Obsidian the page then reads:

```text
---
type: heldby
status: draft
title: "Workshop participants holds Tools come back in good order"
description: "Participants want borrowed tools returned in the state they left."
group: "[[workshop-participants]]"
concern: "[[tools-come-back-in-good-order]]"
notes: "Held most strongly about the ladder."
---
```

Now `stub-links`. Run it on the whole vault, or name one page. Nothing is missing here, so it says so:

=== "Python (REPL)"

    ```python
    scat_kg.stub_links()
    ```

=== "CLI"

    ```bash
    uv run scat stub-links
    ```

```text
stub-links: nothing to do
```

When you have written a coded page that links to pages that do not exist yet, `scat stub-links <page>` creates them. That is the fastest way to code: write the links, then run it. The first message under "How to read a message" shows it at work.

New stubs are never errors. Check the neighbourhood of the concern to see:

=== "Python (REPL)"

    ```python
    scat_kg.check("tools-come-back-in-good-order", neighborhood=True)
    ```

=== "CLI"

    ```bash
    uv run scat check tools-come-back-in-good-order --neighborhood
    ```

```text
no problems
```

### Status, and set-status

`status` lists each page's status and the counts, at the same three scopes as `check`.

=== "Python (REPL)"

    ```python
    scat_kg.status("sign-out-sheet")
    scat_kg.status("tools-come-back-in-good-order", neighborhood=True)
    ```

=== "CLI"

    ```bash
    uv run scat status sign-out-sheet
    uv run scat status tools-come-back-in-good-order --neighborhood
    ```

```text
stub         affordance/sign-out-sheet.md
1 stub
stub         concern/tools-come-back-in-good-order.md
stub         addresses/tools-come-back-in-good-order-addresses-sign-out-sheet.md
stub         heldby/workshop-participants-holds-tools-come-back-in-good-order.md
3 stub
```

The whole vault lists every page and ends with the counts:

=== "Python (REPL)"

    ```python
    scat_kg.status()
    ```

=== "CLI"

    ```bash
    uv run scat status
    ```

The last lines of the output. It lists every page first, and shows class pages as `(no status: class page)`:

```text
done         technology/main-and-dev-branches.md
stub         technology/shared-spreadsheet.md
7 stub, 28 done, 7 none
```

That is the count after one spelling of the steps above. If you typed both the REPL and the CLI `stub` line, you made one more concern, and the count reads `8 stub, 28 done, 7 none`.

`set-status` moves a page along: `stub`, `draft` or `done`. A stub becomes a draft when you start filling it in: set it with `scat set-status <page> draft` (REPL: `scat_kg.set_status("<page>", "draft")`), or edit the `status` line by hand. When the page is finished, set `done`, then run `check` on that page. Setting the status a page already has changes nothing, so you can repeat it.

=== "Python (REPL)"

    ```python
    scat_kg.set_status("sign-out-sheet", "draft")
    ```

=== "CLI"

    ```bash
    uv run scat set-status sign-out-sheet draft
    ```

```text
changed affordance/sign-out-sheet.md
note: `status` set to draft (was stub)
```

The second spelling prints `unchanged affordance/sign-out-sheet.md` and `note: status is already draft`.

`set-status` writes the status and nothing else. It does not check that the page is ready. Run `check` on the page after you set `done`. Message 7 below shows why.

### Index: keep the class pages current

A class page lists every page of its kind in a table, with a name, a short description and a link. The tools write the table, between two marker lines, so never edit it by hand. After you add pages, the tables are out of date, and the whole-vault check says so as a warning:

=== "Python (REPL)"

    ```python
    scat_kg.check()
    ```

=== "CLI"

    ```bash
    uv run scat check
    ```

```text
warning [SCAT-DRAFT-FIELD] affordance/sign-out-sheet.md field `description`: missing (required once the page is done)
  Fix: add the line `description: "<one sentence you write>"` (author) before you set status: done
warning [SCAT-INDEX-STALE] class/addresses-pairs.md index table: the table differs from the addresses pages
  Fix: run `scat index` (REPL: `scat_kg.index()`)
warning [SCAT-INDEX-STALE] class/affordances.md index table: the table differs from the affordance pages
  Fix: run `scat index` (REPL: `scat_kg.index()`)
warning [SCAT-INDEX-STALE] class/attributes-pairs.md index table: the table differs from the attributes pages
  Fix: run `scat index` (REPL: `scat_kg.index()`)
warning [SCAT-INDEX-STALE] class/concerns.md index table: the table differs from the concern pages
  Fix: run `scat index` (REPL: `scat_kg.index()`)
warning [SCAT-INDEX-STALE] class/heldby-pairs.md index table: the table differs from the heldby pages
  Fix: run `scat index` (REPL: `scat_kg.index()`)
warning [SCAT-INDEX-STALE] class/technologies.md index table: the table differs from the technology pages
  Fix: run `scat index` (REPL: `scat_kg.index()`)
0 errors, 7 warnings
```

The `Fix:` line is the exact command. Run it:

=== "Python (REPL)"

    ```python
    scat_kg.index()
    ```

=== "CLI"

    ```bash
    uv run scat index
    ```

```text
changed class/addresses-pairs.md
changed class/affordances.md
changed class/attributes-pairs.md
changed class/concerns.md
changed class/heldby-pairs.md
changed class/technologies.md
unchanged class/stakeholder-groups.md
```

`unchanged` means that page did not need a rewrite. That is good news, not a fault. Run `index` a second time, for example the other spelling, and every line says `unchanged`. Run the whole-vault check again:

=== "Python (REPL)"

    ```python
    scat_kg.check()
    ```

=== "CLI"

    ```bash
    uv run scat check
    ```

```text
warning [SCAT-DRAFT-FIELD] affordance/sign-out-sheet.md field `description`: missing (required once the page is done)
  Fix: add the line `description: "<one sentence you write>"` (author) before you set status: done
0 errors, 1 warning
```

Zero errors. The draft warning says the affordance still needs a description before it can be `done`. That is a to-do, not a fault.

## How to read a message

Every message has the same parts:

```text
error [SCAT-LINK-DANGLING] scenario-coded/saturday-at-the-tool-library-coded.md:11 field `concerns`: [[tools-come-back-in-good-order]] does not reach a page (no page is named tools-come-back-in-good-order)
  Fix: run `scat stub tools-come-back-in-good-order --type concern` (REPL: `scat_kg.stub("tools-come-back-in-good-order", type="concern")`) to create it as a stub
```

1. **Severity.** `error` blocks. `warning` does not. `refused` means a command did not run, and nothing was written.
2. **The rule id**, in square brackets. It names the rule, and it is the word to search for in the reference.
3. **The file**, and the line number after it when there is one.
4. **The field or the link**: the frontmatter field (`concerns`) or the `[[link]]`.
5. **What is wrong**, in one sentence.
6. **The fix.** An exact command, or an exact line to write or delete. A fix marked `(author)` is a line only you can word.

Do what the fix says, then check again. Each message below starts from a fresh copy of the template, and its first line says which pages it needs and what status they have, so you can follow any one on its own. All were provoked and fixed in a scratch copy. Each shows page content as `text`, because you edit it in Obsidian. A line that starts with `$` is a command you type, without the `$`.

### 1. A link to a page that does not exist (`SCAT-LINK-DANGLING`)

Start: a fresh copy of the template, a raw page `saturday-at-the-tool-library` made with `scat stub`, and the coded page above, still a draft, with nothing else made yet. Checking the coded page:

```text
$ uv run scat check saturday-at-the-tool-library-coded
error [SCAT-LINK-DANGLING] scenario-coded/saturday-at-the-tool-library-coded.md:11 field `concerns`: [[tools-come-back-in-good-order]] does not reach a page (no page is named tools-come-back-in-good-order)
  Fix: run `scat stub tools-come-back-in-good-order --type concern` (REPL: `scat_kg.stub("tools-come-back-in-good-order", type="concern")`) to create it as a stub
error [SCAT-LINK-DANGLING] scenario-coded/saturday-at-the-tool-library-coded.md:13 field `affordances`: [[sign-out-sheet]] does not reach a page (no page is named sign-out-sheet)
  Fix: run `scat stub sign-out-sheet --type affordance` (REPL: `scat_kg.stub("sign-out-sheet", type="affordance")`) to create it as a stub
2 errors, 0 warnings
```

Two fixes, two commands. One command does both, because `stub-links` creates every page the page links to:

```text
$ uv run scat stub-links saturday-at-the-tool-library-coded
created affordance/sign-out-sheet.md
created concern/tools-come-back-in-good-order.md
$ uv run scat check saturday-at-the-tool-library-coded
no problems
```

### 2. The raw page does not point back (`SCAT-RAW-BACKLINK`)

Start: a fresh copy of the template, the raw page (made with `scat stub`, so `status: stub` with only `type`, `status` and `title`) and the coded page above, and the concern and affordance stub pages they link to (the result of message 1). The neighbourhood check of the coded page:

```text
$ uv run scat check saturday-at-the-tool-library-coded --neighborhood
warning [SCAT-RAW-BACKLINK] scenario-raw/saturday-at-the-tool-library.md field `coded`: [[saturday-at-the-tool-library-coded]] lists this page in `raw`, but this page does not list it
  Fix: in scenario-raw/saturday-at-the-tool-library.md add `coded:` and under it the line `- "[[saturday-at-the-tool-library-coded]]"`
0 errors, 1 warning
```

Its fix is a hand edit, in the raw page. Add the two lines to the frontmatter, for example straight after `title`:

```text
coded:
  - "[[saturday-at-the-tool-library-coded]]"
```

Check the raw page again. The warning is gone:

```text
$ uv run scat check saturday-at-the-tool-library
no problems
```

A stub gets no description warning, because an unfinished page is never faulted for being unfinished. The warning comes when you set the page to `draft`:

```text
$ uv run scat set-status saturday-at-the-tool-library draft
changed scenario-raw/saturday-at-the-tool-library.md
note: `status` set to draft (was stub)
$ uv run scat check saturday-at-the-tool-library
warning [SCAT-DRAFT-FIELD] scenario-raw/saturday-at-the-tool-library.md field `description`: missing (required once the page is done)
  Fix: add the line `description: "<one sentence you write>"` (author) before you set status: done
0 errors, 1 warning
```

The warning is a to-do: the raw page is a draft and still wants its sentence.

### 3. A status the tools do not know (`SCAT-FM-STATUS`)

Start: a fresh copy of the template and the raw page made with `scat stub`, with a typo in its status line, `status: dun`:

```text
$ uv run scat check saturday-at-the-tool-library
error [SCAT-FM-STATUS] scenario-raw/saturday-at-the-tool-library.md field `status`: `dun` is not a status
  Fix, choose one: `status: stub` (just started), `status: draft` (being written), `status: done` (finished)
1 error, 0 warnings
```

Write `status: draft` in its place. The error is gone, and the check shows the to-do for the empty description:

```text
$ uv run scat check saturday-at-the-tool-library
warning [SCAT-DRAFT-FIELD] scenario-raw/saturday-at-the-tool-library.md field `description`: missing (required once the page is done)
  Fix: add the line `description: "<one sentence you write>"` (author) before you set status: done
0 errors, 1 warning
```

### 4. A link to the wrong kind of page (`SCAT-LINK-ENDPOINT`)

Start: a fresh copy of the template, the raw page, the stub pages `tools-come-back-in-good-order` (concern), `sign-out-sheet` (affordance) and `shared-spreadsheet` (technology, made with `scat stub shared-spreadsheet --type technology`), and the coded page set to `done`, with the technology under `affordances` by mistake:

```text
affordances:
  - "[[shared-spreadsheet]]"
```

```text
$ uv run scat check saturday-at-the-tool-library-coded
error [SCAT-LINK-ENDPOINT] scenario-coded/saturday-at-the-tool-library-coded.md:13 field `affordances`: [[shared-spreadsheet]] is a technology page, but `affordances` must link affordance pages
  Fix: `affordances` is required on a page with status: done and this is its only good item, and no existing affordance page was found to replace it with: run `scat set-status saturday-at-the-tool-library-coded draft` (REPL: `scat_kg.set_status("saturday-at-the-tool-library-coded", "draft")`) first, then change the item by hand
1 error, 0 warnings
```

The page is `done` and this is its only item, so deleting it alone would only trade this error for a missing-link error. The fix says to set the page back to `draft` first, then change the item by hand:

```text
$ uv run scat set-status saturday-at-the-tool-library-coded draft
changed scenario-coded/saturday-at-the-tool-library-coded.md
note: `status` set to draft (was done)
```

The check now offers the plain fix:

```text
$ uv run scat check saturday-at-the-tool-library-coded
error [SCAT-LINK-ENDPOINT] scenario-coded/saturday-at-the-tool-library-coded.md:13 field `affordances`: [[shared-spreadsheet]] is a technology page, but `affordances` must link affordance pages
  Fix: delete the item line `- "[[shared-spreadsheet]]"` under `affordances`
  (no existing affordance page was found to replace it with)
1 error, 0 warnings
```

The notes name the sign-out sheet, so write that item in its place, then set the page to `done` again. The next message is what the check says if you delete the item and leave `affordances:` empty.

### 5. A finished page that is missing a link (`SCAT-DONE-LINK`)

Start: a fresh copy of the template, the raw page, the stub pages `tools-come-back-in-good-order` (concern) and `sign-out-sheet` (affordance), and the coded page set to `done` with `affordances:` empty (the page of message 4 with its wrong item deleted).

```text
$ uv run scat check saturday-at-the-tool-library-coded
error [SCAT-DONE-LINK] scenario-coded/saturday-at-the-tool-library-coded.md field `affordances`: required link field is missing or empty on a page with status: done
  Fix, choose one:
    1. replace the line `affordances:` with this, keeping the lines that fit (no suggestions found; you decide):
         affordances:
           - "[[<one affordance page you choose>]]" (author)
    2. run `scat set-status saturday-at-the-tool-library-coded draft` (REPL: `scat_kg.set_status("saturday-at-the-tool-library-coded", "draft")`) if the page is not finished
1 error, 0 warnings
```

Two ways out, and the message gives you both. The sign-out sheet is the affordance the notes name, so choose fix 1:

```text
affordances:
  - "[[sign-out-sheet]]"
```

```text
$ uv run scat check saturday-at-the-tool-library-coded
no problems
```

### 6. A technology on a scenario (`SCAT-LINK-DISCOURAGED`)

Start: a fresh copy of the template, the raw page, the three stub pages from message 4, and the coded page set to `done` with `sign-out-sheet` under `affordances`. A scenario relates groups, concerns and affordances. Now add `technologies:` and its item straight after the `affordances` block:

```text
affordances:
  - "[[sign-out-sheet]]"
technologies:
  - "[[shared-spreadsheet]]"
```

```text
$ uv run scat check saturday-at-the-tool-library-coded
warning [SCAT-LINK-DISCOURAGED] scenario-coded/saturday-at-the-tool-library-coded.md:14 field `technologies`: a scenario relates groups, concerns and affordances; technologies stay in the background, so linking technology pages here is discouraged: [[shared-spreadsheet]]
  Fix: delete `technologies:` and its list items
0 errors, 1 warning
```

The line number depends on where you put the line. The technology belongs in an architecture, as in the example above. Delete the two lines, and the check reads:

```text
$ uv run scat check saturday-at-the-tool-library-coded
no problems
```

### 7. A finished page that is missing a field (`SCAT-DONE-FIELD`)

Start: a fresh copy of the template and one stub page, made with `scat stub sign-out-sheet --type affordance`. `set-status` accepts `done` for it. The check does not:

```text
$ uv run scat set-status sign-out-sheet done
changed affordance/sign-out-sheet.md
note: `status` set to done (was stub)
$ uv run scat check sign-out-sheet
error [SCAT-DONE-FIELD] affordance/sign-out-sheet.md field `description`: missing on a page with status: done
  Fix, choose one:
    1. add the line `description: "<one sentence you write>"` (author)
    2. run `scat set-status sign-out-sheet draft` (REPL: `scat_kg.set_status("sign-out-sheet", "draft")`) if the page is not finished
1 error, 0 warnings
```

If the page is finished, write the sentence (fix 1):

```text
---
type: affordance
status: done
title: "Sign out sheet"
description: "A paper sheet where each loan is written down."
---
```

```text
$ uv run scat check sign-out-sheet
no problems
```

If you do not have the sentence yet, fix 2 sets the page back to `draft`, and the error becomes the warning you saw earlier (`SCAT-DRAFT-FIELD`). An unfinished page is not an error. (If the page was a `draft` first, the `set-status` note reads `(was draft)`.)

### 8. A new group over the cap (`SCAT-CAP`)

Start: a fresh copy of the template and nothing else. The vault allows three stakeholder groups, set by `stakeholder_group_cap` in `scat.toml`. The cap protects anonymity: few, broad groups cannot point to one person. Naming a fourth group in a pair is refused, and nothing is written:

```text
$ uv run scat stub-pair heldby volunteer-stewards tools-come-back-in-good-order
refused scat.toml field `stakeholder_group_cap`: the vault is at its cap of 3 stakeholder groups, so a new group page (volunteer-stewards) would break SCAT-CAP; choose an existing group
  Fix: either link an existing group, or write `stakeholder_group_cap = 4` in scat.toml (the cap protects against identifying individuals; raise it only if the plan allows)
```

The template's three example groups already fill the cap. Your own vault replaces them with the groups you planned: see [Start your own content](getting-started.md#5-start-your-own-content) in the getting-started guide. Then name an existing group, which is usually the right fix. The other way out is the second fix: write `stakeholder_group_cap = 4` in `scat.toml`. With it set to 4, the new group page is created. Raise the cap only if your plan allows it, because the cap protects anonymity.

Naming an existing group works at once:

```text
$ uv run scat stub-pair heldby workshop-participants tools-come-back-in-good-order
created concern/tools-come-back-in-good-order.md
created heldby/workshop-participants-holds-tools-come-back-in-good-order.md
note: write `description`, `notes` and the body in heldby/workshop-participants-holds-tools-come-back-in-good-order.md; the endpoints are filled
```

### Two messages you have already met

`SCAT-INDEX-STALE` (a warning) means a class page's table is out of date. Run `scat index`. `SCAT-DRAFT-FIELD` (a warning) means a draft page lacks a field it needs by `done`.

## What the check does not judge

The check looks at structure: that a page has the fields its type needs, that every link points at a page that
exists, that names and counts follow the rules. It does not judge what your notes say. Concerns that pull against
each other are normal, and recording them is the point of SCAT. A concern can say so, in its `conflicts` field:

```text
conflicts:
  - "[[attribution]]"
```

`conflicts` is an explicit link between concerns. The check makes sure the link has the right type and points at a
page that exists, and that a concern does not list itself. That is all. A coded record may hold two concerns that
pull apart, and the check says nothing about it. Seeing where tensions are sharpest, or where concerns match or leave
a gap, is analysis. It comes after the check passes and a coder has signed off the content.

## Reaching a clean whole-vault check

"Clean" means **zero errors**. A check with nothing to report prints `no problems`. Work in this order:

1. Run `uv run scat check`. Read the errors first.
2. Fix an error the way its `Fix:` line says. Check the page, then its neighbourhood, then the whole vault.
3. Run `uv run scat index` so the class pages match.
4. Run `uv run scat check` again. When it ends `0 errors`, you are clean.

Aim to bring every page you made to `done`: the raw pages, the coded pages, the relation pages, and the stubs the tools made for you. A page left at `stub` or `draft` does not stop a clean check, because the bar is 0 errors; a `draft` that lacks a field `done` needs gets a warning. To finish a page, write its description and links, run `set-status <page> done`, then run `check`.

Then look at the warnings. Each is a to-do (a draft that still needs a sentence) or a rule you can satisfy with a command.

## Commit and push

Your vault is a git repository, and your repository is private. Save the work as a commit, then push it. These are not tool commands, so they are `text`:

```text
git status
git add .
git commit -m "Code the notes from my first session"
git push
```

Run `git status` first and read the list: it shows what the commit will hold. `git add .` stages every change in the folder, so if the list holds a change you did not mean to make, stop and sort that out before you go on. `git commit` saves it with a message you write. `git push` sends it to GitHub. If git asks who you are the first time, it prints the two lines to type. Commit when the whole-vault check ends with zero errors.

## Look at it in Obsidian

Open the vault folder in Obsidian (**Open folder as vault**). The same pages, now as a graph:

- **Links.** Every `[[name]]` is a link. Click it to go to that page.
- **Backlinks.** Open a concern page and look at the Backlinks panel in the right sidebar. It lists every page that points at the concern: each Heldby page (who holds it), each Addresses page (what addresses it) and each coded page that names it. This is how you ask "who holds this concern?" without a second list.
- **Graph view.** Open the graph view from the left ribbon or the command palette. Each page is a dot and each link a line. A Heldby page sits between a group and a concern, so a concern held by several groups shows several lines. Where two groups hold the same concern, you see it. The local graph shows one page and its neighbours.
- **Class pages.** The pages in the `class` folder (Concerns, Affordances and so on) are the tables `scat index` writes. Open `class/concerns.md` to see every concern at a glance, with its description and a link. Run `uv run scat index` first if you added pages.

Obsidian shows the graph. Only the tools check it, so run `uv run scat check` before you commit.

## Where next

Keep the reference close:

- [Python API reference](reference/api.md): every REPL call, with all its options.
- [CLI reference](reference/cli.md): every command and its full help text.
- [Facilitating scenarios](facilitate-scenarios.md) and [Facilitating architectures](facilitate-architectures.md): collect the next round of raw notes.
- [Planning](planning.md): revisit your groups before the next workshop.
- [Home](index.md)
