# Python API reference

!!! tip "Your next step"
    In a terminal in your vault folder, type `uv run python`.

## Before you start

- A vault folder with a `scat.toml` file in it, for example a copy of the template. [Getting started](../getting-started.md) makes one.
- A Python session started in that folder with `uv run python`, and `import scat_kg` typed in it. Every call below looks in the current folder unless you pass `root=`.
- The same operations as commands are in the [CLI reference](cli.md). The two paths give the same messages.

## How every call behaves

- Every call returns a result. At the REPL, the result prints as the message the matching `scat` command prints, so you do not need `print`.
- `str(result)` is that message. `result.ok` is `False` when the message holds an error or a refusal, and `True` otherwise. Warnings leave it `True`. On the CLI, `ok` is the exit code: `True` is 0, `False` is 1.
- A call that cannot do what you asked does not raise. It returns a result that starts with `refused` and says what to do next. Nothing is written when a call refuses.
- Every call takes the keyword `root=`, the vault folder (default: the current folder). On the CLI it is `--root`.
- The outputs on this page are what a fresh copy of the template prints. The Python tab and the CLI tab use different new page names (`reading-group` and `study-circle`, `reading-list` and `reading-shelf`), so you can run both tabs in one vault, in page order, and each prints what is shown.

| Python | CLI | What it does |
|---|---|---|
| [`scat_kg.check`](#scat_kgcheck) | [`scat check`](cli.md#scat-check) | Check the vault, a page, or a page and its neighbours. Writes nothing. |
| [`scat_kg.status`](#scat_kgstatus) | [`scat status`](cli.md#scat-status) | Show each page's status and the counts. Writes nothing. |
| [`scat_kg.index`](#scat_kgindex) | [`scat index`](cli.md#scat-index) | Rewrite the generated table of every class page. |
| [`scat_kg.stub`](#scat_kgstub) | [`scat stub`](cli.md#scat-stub) | Create one stub page. |
| [`scat_kg.stub_pair`](#scat_kgstub_pair) | [`scat stub-pair`](cli.md#scat-stub-pair) | Create the relation page for a pair. |
| [`scat_kg.stub_links`](#scat_kgstub_links) | [`scat stub-links`](cli.md#scat-stub-links) | Create the pages that links name and the vault lacks. |
| [`scat_kg.set_status`](#scat_kgset_status) | [`scat set-status`](cli.md#scat-set-status) | Set a page's status. |

## scat_kg.check

```text
check(page=None, *, neighborhood=False, root=".")
```

Checks the vault against the rules and returns a `CheckResult` (see [Results](#results)). Writes nothing.

| Parameter | Meaning |
|---|---|
| `page` | A page name (`anonymity`) or its path from the vault folder (`concern/anonymity.md`). Without it, the whole vault. |
| `neighborhood` | `True` checks `page` and every page one link away, in either direction. It needs `page`. |
| `root` | The vault folder. |

It prints one block per problem, then a count line: `<n> errors, <n> warnings`. With no problems it prints `no problems`. Errors block, warnings do not. A rule id such as `SCAT-CONFLICT-BOTH` names the rule; the `Fix:` line says what to do. Asking for `neighborhood=True` without a page, or for a page that is not there, returns a refusal.

The whole vault:

=== "Python"

    ```python
    import scat_kg

    scat_kg.check()
    ```

    ```text
    warning [SCAT-CONFLICT-BOTH] scenario-coded/notes-at-a-chatham-house-session-coded.md:11 field `concerns`: this record holds both [[anonymity]] and [[attribution]], which conflict (declared on [[anonymity]])
      Fix: none needed if both belong in this record. Holding both sides is allowed and is what the warning marks, a place where two concerns pull apart. If one was coded here by mistake, delete its line `- "[[anonymity]]"` or `- "[[attribution]]"` under `concerns`.
    0 errors, 1 warning
    ```

=== "CLI"

    ```bash
    uv run scat check
    ```

    ```text
    warning [SCAT-CONFLICT-BOTH] scenario-coded/notes-at-a-chatham-house-session-coded.md:11 field `concerns`: this record holds both [[anonymity]] and [[attribution]], which conflict (declared on [[anonymity]])
      Fix: none needed if both belong in this record. Holding both sides is allowed and is what the warning marks, a place where two concerns pull apart. If one was coded here by mistake, delete its line `- "[[anonymity]]"` or `- "[[attribution]]"` under `concerns`.
    0 errors, 1 warning
    ```

`SCAT-CONFLICT-BOTH` is a warning. It marks a place where two concerns pull apart, and it may stay.

One page, by name or by path:

=== "Python"

    ```python
    scat_kg.check("anonymity")
    scat_kg.check("concern/anonymity.md")
    ```

    ```text
    no problems
    no problems
    ```

=== "CLI"

    ```bash
    uv run scat check anonymity
    uv run scat check concern/anonymity.md
    ```

    ```text
    no problems
    no problems
    ```

A page and every page one link away:

=== "Python"

    ```python
    scat_kg.check("anonymity", neighborhood=True)
    ```

    ```text
    warning [SCAT-CONFLICT-BOTH] scenario-coded/notes-at-a-chatham-house-session-coded.md:11 field `concerns`: this record holds both [[anonymity]] and [[attribution]], which conflict (declared on [[anonymity]])
      Fix: none needed if both belong in this record. Holding both sides is allowed and is what the warning marks, a place where two concerns pull apart. If one was coded here by mistake, delete its line `- "[[anonymity]]"` or `- "[[attribution]]"` under `concerns`.
    0 errors, 1 warning
    ```

=== "CLI"

    ```bash
    uv run scat check anonymity --neighborhood
    ```

    ```text
    warning [SCAT-CONFLICT-BOTH] scenario-coded/notes-at-a-chatham-house-session-coded.md:11 field `concerns`: this record holds both [[anonymity]] and [[attribution]], which conflict (declared on [[anonymity]])
      Fix: none needed if both belong in this record. Holding both sides is allowed and is what the warning marks, a place where two concerns pull apart. If one was coded here by mistake, delete its line `- "[[anonymity]]"` or `- "[[attribution]]"` under `concerns`.
    0 errors, 1 warning
    ```

## scat_kg.status

```text
status(page=None, *, neighborhood=False, root=".")
```

Reads the status of each page and returns a `StatusReport` (see [Results](#results)). Writes nothing.

| Parameter | Meaning |
|---|---|
| `page` | A page name or path. Without it, the whole vault. |
| `neighborhood` | `True` shows `page` and every page one link away, in either direction. It needs `page`. |
| `root` | The vault folder. |

It prints one line per page: the status (`stub`, `draft`, `done`, `(missing)` or something invalid as written), then the path. A class page shows `(no status: class page)`. The last line counts the pages by status. For a neighborhood, the page comes first and the others follow in path order. A missing page, or `neighborhood=True` without a page, returns a refusal.

=== "Python"

    ```python
    scat_kg.status("anonymity")
    scat_kg.status("anonymity", neighborhood=True)
    ```

    ```text
    done         concern/anonymity.md
    1 done
    done         concern/anonymity.md
    done         addresses/groups-clustered-under-a-cap-addresses-anonymity.md
    done         architecture-coded/groups-under-a-cap-pitch-coded.md
    (no status: class page) class/concerns.md
    done         concern/attribution.md
    done         heldby/facilitator-analysts-holds-anonymity.md
    done         scenario-coded/notes-at-a-chatham-house-session-coded.md
    6 done, 1 none
    ```

=== "CLI"

    ```bash
    uv run scat status anonymity
    uv run scat status anonymity --neighborhood
    ```

    ```text
    done         concern/anonymity.md
    1 done
    done         concern/anonymity.md
    done         addresses/groups-clustered-under-a-cap-addresses-anonymity.md
    done         architecture-coded/groups-under-a-cap-pitch-coded.md
    (no status: class page) class/concerns.md
    done         concern/attribution.md
    done         heldby/facilitator-analysts-holds-anonymity.md
    done         scenario-coded/notes-at-a-chatham-house-session-coded.md
    6 done, 1 none
    ```

`scat_kg.status()` and `scat status` list every page in the vault, then the counts.

## scat_kg.index

```text
index(*, root=".")
```

Rewrites the generated table in each of the seven class pages, so each lists the pages of its type. It creates a class page that is missing. Everything outside the table markers stays as it was.

| Parameter | Meaning |
|---|---|
| `root` | The vault folder. |

It prints one line per class page: `created`, `changed` or `unchanged`. After new pages are made, `check` warns with `SCAT-INDEX-STALE` until you run it. A table that is already right prints `unchanged`. It refuses for a class-page name that another file already holds, or when a page has no readable table markers.

Each tab below first makes a new page (a different type in each, so the two tabs do not undo each other), then runs `index`:

=== "Python"

    ```python
    scat_kg.stub("reading-list", type="technology")
    scat_kg.index()
    ```

    ```text
    created technology/reading-list.md
    changed class/technologies.md
    unchanged class/addresses-pairs.md
    unchanged class/affordances.md
    unchanged class/attributes-pairs.md
    unchanged class/concerns.md
    unchanged class/heldby-pairs.md
    unchanged class/stakeholder-groups.md
    ```

=== "CLI"

    ```bash
    uv run scat stub reading-shelf --type affordance
    uv run scat index
    ```

    ```text
    created affordance/reading-shelf.md
    changed class/affordances.md
    unchanged class/addresses-pairs.md
    unchanged class/attributes-pairs.md
    unchanged class/concerns.md
    unchanged class/heldby-pairs.md
    unchanged class/stakeholder-groups.md
    unchanged class/technologies.md
    ```

## scat_kg.stub

```text
stub(name, type, *, root=".")
```

Creates one stub page: its type, `status: stub`, and a title made from the name. It never changes an existing file.

| Parameter | Meaning |
|---|---|
| `name` | The new page's name: `a-z`, `0-9` and single hyphens, starting and ending with a letter or digit, at most 64 characters. These names are reserved and refuse: `con`, `prn`, `aux`, `nul`, `com0` to `com9`, `lpt0` to `lpt9`, and the seven class-page names (`concerns`, `affordances`, `technologies`, `stakeholder-groups`, `addresses-pairs`, `attributes-pairs`, `heldby-pairs`). |
| `type` | The page type key: `affordance`, `architecture-coded`, `architecture-raw`, `concern`, `scenario-coded`, `scenario-raw`, `stakeholder-group` or `technology`. |
| `root` | The vault folder. |

It prints `created <path>`. It refuses when the name is not legal (a reserved name prints ``refused name `con`: `con` is a reserved name``; a 65-character name prints `a name is at most 64 characters (this one has 65)`; both end with a `Fix:` line that offers a name that works), when a Markdown file already has the name (in any letter case), when the type is a relation or class type, and when a new `stakeholder-group` page would take the vault over its cap.

=== "Python"

    ```python
    scat_kg.stub("reading-group", type="concern")
    ```

    ```text
    created concern/reading-group.md
    ```

=== "CLI"

    ```bash
    uv run scat stub study-circle --type concern
    ```

    ```text
    created concern/study-circle.md
    ```

Running it again for the same name refuses, and the CLI exits with 1:

```text
refused name `reading-group`: a Markdown file already has this name (concern/reading-group.md); names are compared without regard to case
  Fix: link to the existing page, or choose another name
```

## scat_kg.stub_pair

```text
stub_pair(relation, endpoint_a, endpoint_b, *, root=".")
```

Creates the relation page for one pair of pages. An endpoint page that does not exist is created as a stub too.

| Parameter | Meaning |
|---|---|
| `relation` | `addresses` (concern, then affordance), `attributes` (affordance, then technology) or `heldby` (group, then concern). |
| `endpoint_a`, `endpoint_b` | The two page names, in the order the relation lists. |
| `root` | The vault folder. |

It prints `created <path>` for each page it made, then a note naming the relation page whose `description`, `notes` and body you write. If a page of that relation already states exactly this pair, it prints `unchanged <path>` and creates nothing. It refuses when the two names are equal, when an endpoint exists with the wrong type, or when a new name is not legal.

=== "Python"

    ```python
    scat_kg.stub_pair("heldby", "project-leads", "reading-group")
    ```

    ```text
    created heldby/project-leads-holds-reading-group.md
    note: write `description`, `notes` and the body in heldby/project-leads-holds-reading-group.md; the endpoints are filled
    ```

=== "CLI"

    ```bash
    uv run scat stub-pair heldby project-leads study-circle
    ```

    ```text
    created heldby/project-leads-holds-study-circle.md
    note: write `description`, `notes` and the body in heldby/project-leads-holds-study-circle.md; the endpoints are filled
    ```

## scat_kg.stub_links

```text
stub_links(ref=None, *, root=".")
```

Creates the pages that link fields name and the vault lacks. Each new page has the type its link field expects. It creates nothing for a link to an existing page.

| Parameter | Meaning |
|---|---|
| `ref` | A page name or path: look at that page's links only. Without it, every page. (The CLI calls this `PAGE`.) |
| `root` | The vault folder. |

It prints `created <path>` for each page made, or `stub-links: nothing to do`. Links it cannot act on appear as `note:` lines. It refuses when links name one page as two different types, or when a new group would pass the cap.

=== "Python"

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

When a page links to a page the vault lacks, `check` reports it and `stub_links` makes the page. Here is a vault where one page links to `[[travel-time]]`, a concern that is not there. `check` says so (exit code 1 on the CLI), and the Fix line names the call:

```text
error [SCAT-LINK-DANGLING] scenario-coded/false-start-and-clean-restart-coded.md:11 field `concerns`: [[travel-time]] does not reach a page (no page is named travel-time)
  Fix: run `scat stub travel-time --type concern` (REPL: `scat_kg.stub("travel-time", type="concern")`) to create it as a stub
warning [SCAT-CONFLICT-BOTH] scenario-coded/notes-at-a-chatham-house-session-coded.md:11 field `concerns`: this record holds both [[anonymity]] and [[attribution]], which conflict (declared on [[anonymity]])
  Fix: none needed if both belong in this record. Holding both sides is allowed and is what the warning marks, a place where two concerns pull apart. If one was coded here by mistake, delete its line `- "[[anonymity]]"` or `- "[[attribution]]"` under `concerns`.
1 error, 1 warning
```

`scat_kg.stub_links()` and `scat stub-links` then both print:

```text
created concern/travel-time.md
```

## scat_kg.set_status

```text
set_status(name, status, *, root=".")
```

Sets the `status:` line in a page's frontmatter and changes nothing else in the file. The lifecycle is `stub`, then `draft`, then `done`.

| Parameter | Meaning |
|---|---|
| `name` | A page name or path. (The CLI calls this `PAGE`.) |
| `status` | `stub`, `draft` or `done`. |
| `root` | The vault folder. |

It prints `changed <path>` and a note with the old status. When the page already has that status, it prints `unchanged <path>` and writes nothing. It refuses when `status` is not one of the three, when the page is not there, when the page is a class page (those carry no status), and when the frontmatter cannot be read.

=== "Python"

    ```python
    scat_kg.set_status("reading-group", "draft")
    ```

    ```text
    changed concern/reading-group.md
    note: `status` set to draft (was stub)
    ```

=== "CLI"

    ```bash
    uv run scat set-status study-circle draft
    ```

    ```text
    changed concern/study-circle.md
    note: `status` set to draft (was stub)
    ```

A status that does not exist refuses, and the CLI exits with 1:

```text
refused status `finished`: this is not a status
  Fix: use one of: stub, draft, done (stub: just started, draft: being written, done: finished)
```

## Results

Each call returns one of three kinds of result. All print as their message.

| Kind | Returned by | Holds |
|---|---|---|
| `CheckResult` | `check`, when it ran | `problems`, `errors`, `warnings` (tuples of problems), `ok`. A problem has `rule`, `severity` (`"error"` or `"warning"`), `file`, `where`, `what`, `fix` and `line`. |
| `StatusReport` | `status`, when it ran | `scope` (`"page"`, `"neighborhood"` or `"vault"`), `rows` (each with `path`, `name`, `type`, `status`), `counts` (pages per status; `other` is a missing or invalid status, `none` a class page), `ok`. |
| `Result` | `stub`, `stub_pair`, `stub_links`, `set_status`, `index`, and any refusal | `created`, `changed`, `unchanged`, `notes` (tuples of text), `refused` (each with `subject`, `why`, `fix`), `ok`. |

A `Result` prints its lines in this order: `created`, `changed`, `unchanged`, `refused`, then `note:` lines. When it holds nothing, it prints `<operation>: nothing to do`.

=== "Python"

    ```python
    result = scat_kg.check("anonymity", neighborhood=True)
    result.ok
    len(result.warnings)
    result.problems[0].rule
    scat_kg.status("anonymity").counts
    ```

    ```text
    True
    1
    'SCAT-CONFLICT-BOTH'
    {'stub': 0, 'draft': 0, 'done': 1, 'other': 0, 'none': 0}
    ```

=== "CLI"

    ```bash
    uv run scat check anonymity --neighborhood
    ```

    The command prints the message that `str(result)` holds. Its exit code is `result.ok` as 0 or 1: here 0, because warnings alone are not errors.

## Where next

Keep the reference close:

- [CLI reference](cli.md): the same operations as `scat` commands, with their `--help` text.
- [Coding guide](../coding.md): how to use them while you code your notes.
- [Home](../index.md)
