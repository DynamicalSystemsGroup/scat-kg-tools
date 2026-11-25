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
- The outputs on this page are what a fresh copy of the template prints. The Python tab and the CLI tab use different new page names (`reading-group` and `study-circle`, `desk-notes-one` and `desk-notes-two`), so you can run both tabs in one vault, in page order, and each prints what is shown.

| Python | CLI | What it does |
|---|---|---|
| [`scat_kg.check`](#scat_kgcheck) | [`scat check`](cli.md#scat-check) | Check the vault, a page, or a page and its neighbours. Writes nothing. |
| [`scat_kg.status`](#scat_kgstatus) | [`scat status`](cli.md#scat-status) | Show each page's status and the counts. Writes nothing. |
| [`scat_kg.index`](#scat_kgindex) | [`scat index`](cli.md#scat-index) | Write the index page of each type that has none. |
| [`scat_kg.stub`](#scat_kgstub) | [`scat stub`](cli.md#scat-stub) | Create one stub page. |
| [`scat_kg.record_edge`](#scat_kgrecord_edge) | [`scat record-edge`](cli.md#scat-record-edge) | Record an edge: add its row to the narratives that tell it. |
| [`scat_kg.remove_edge`](#scat_kgremove_edge) | [`scat remove-edge`](cli.md#scat-remove-edge) | Remove an edge: delete its rows. |
| [`scat_kg.stub_links`](#scat_kgstub_links) | [`scat stub-links`](cli.md#scat-stub-links) | Create the node pages that the ends of rows link and the vault lacks. |
| [`scat_kg.set_status`](#scat_kgset_status) | [`scat set-status`](cli.md#scat-set-status) | Set a page's status. |

## Machine-readable output

`result.to_dict()` returns the data of the result as plain Python: the same document that the matching `scat` command prints with `--json` (see the [CLI reference](cli.md#machine-readable-output)). `--json` prints exactly one JSON document and nothing else, and the exit code does not change. Print it with `json.dumps(result.to_dict(), indent=2)`. The fields, and the rule for when `schema_version` changes (it is 2), are in the [machine interface contract](https://github.com/DynamicalSystemsGroup/scat-kg-tools/blob/dev/contracts/machine-interface.md).

The examples below show `to_dict()` once for each call, with the output a fresh copy of the template gives at that point in the page. These JSON blocks are for reading: they are not run by the docs test.

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

It prints one block per problem, then a count line: `<n> errors, <n> warnings`. With no problems it prints `no problems`. Errors block, warnings do not. A rule id such as `SCAT-DONE-END-NOPAGE` names the rule; the `Fix:` line says what to do. Asking for `neighborhood=True` without a page, or for a page that is not there, returns a refusal.

The whole vault, and a page and every page one link away:

=== "Python"

    ```python
    import scat_kg

    scat_kg.check()
    scat_kg.check("anonymity", neighborhood=True)
    ```

    ```text
    no problems
    no problems
    ```

=== "CLI"

    ```bash
    uv run scat check
    uv run scat check anonymity --neighborhood
    ```

    ```text
    no problems
    no problems
    ```

The check looks at structure only. It does not judge what the notes say: a forgotten edge is graded by no rule, and tensions, matches and gaps are for analysis, after the check passes and a coder has signed off the content.

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

As data, on the unchanged template (`import json` first):

```text
>>> print(json.dumps(scat_kg.check().to_dict(), indent=2))
```

```json
{
  "schema_version": 2,
  "kind": "check",
  "operation": "check",
  "ok": true,
  "problems": []
}
```

To see a problem with a fix a program can apply, change `[[cap-setting]]` to `[[cap-settin]]` in the second row of the table of `narrative/groups-under-a-cap-pitch.md` (line 22), a one-letter typo in a link. The fix has three options: a `replace-text` edit that writes the right name, a `command` that creates the missing page, and a `delete-line` edit.

```text
>>> print(json.dumps(scat_kg.check().to_dict(), indent=2))
```

```json
{
  "schema_version": 2,
  "kind": "check",
  "operation": "check",
  "ok": false,
  "problems": [
    {
      "rule": "SCAT-DONE-END-NOPAGE",
      "severity": "error",
      "file": "narrative/groups-under-a-cap-pitch.md",
      "line": 22,
      "column": 55,
      "field": null,
      "where": "row 2 cell `to`",
      "what": "[[cap-settin]] does not reach a page (no page is named cap-settin)",
      "repeat": 1,
      "fix": {
        "kind": "options",
        "options": [
          {
            "kind": "exact",
            "text": "replace `[[cap-settin]]` with `[[cap-setting]]`",
            "edits": [
              {
                "action": "replace-text",
                "file": "narrative/groups-under-a-cap-pitch.md",
                "line": 22,
                "column": 55,
                "find": "[[cap-settin]]",
                "replace": "[[cap-setting]]"
              }
            ]
          },
          {
            "kind": "exact",
            "text": "run `scat stub cap-settin --type technology` (REPL: `scat_kg.stub(\"cap-settin\", type=\"technology\")`) to create a technology page",
            "command": {
              "argv": [
                "stub",
                "cap-settin",
                "--type",
                "technology"
              ],
              "repl": "scat_kg.stub(\"cap-settin\", type=\"technology\")"
            }
          },
          {
            "kind": "exact",
            "text": "delete the row",
            "edits": [
              {
                "action": "delete-line",
                "file": "narrative/groups-under-a-cap-pitch.md",
                "line": 22,
                "find": "| is provided by | [[groups-clustered-under-a-cap]] | [[cap-settin]] | The cap setting is what fixes the number of groups. The cap is a per-instance parameter (D-020); the example vault sets it to 3. |"
              }
            ]
          }
        ],
        "notes": []
      },
      "text": "error [SCAT-DONE-END-NOPAGE] narrative/groups-under-a-cap-pitch.md:22:55 row 2 cell `to`: [[cap-settin]] does not reach a page (no page is named cap-settin)\n  Fix, choose one:\n    1. replace `[[cap-settin]]` with `[[cap-setting]]`\n    2. run `scat stub cap-settin --type technology` (REPL: `scat_kg.stub(\"cap-settin\", type=\"technology\")`) to create a technology page\n    3. delete the row"
    }
  ]
}
```

Change the typo back (`[[cap-settin]]` to `[[cap-setting]]`) before you type the next commands, which assume the narrative as the template has it.

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

It prints one line per page: the status (`stub`, `draft`, `done`, `(missing)` or something invalid as written), then the path. The last line counts the pages by status. For a neighborhood, the page comes first and the others follow in path order. A missing page, or `neighborhood=True` without a page, returns a refusal.

=== "Python"

    ```python
    scat_kg.status("anonymity")
    scat_kg.status("anonymity", neighborhood=True)
    ```

    ```text
    done         concern/anonymity.md
    1 done
    done         concern/anonymity.md
    done         concern/attribution.md
    done         narrative/groups-under-a-cap-pitch.md
    done         narrative/notes-at-a-chatham-house-session.md
    4 done
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
    done         concern/attribution.md
    done         narrative/groups-under-a-cap-pitch.md
    done         narrative/notes-at-a-chatham-house-session.md
    4 done
    ```

`scat_kg.status()` and `scat status` list every page in the vault, then the counts.

As data:

```text
>>> print(json.dumps(scat_kg.status("anonymity").to_dict(), indent=2))
```

```json
{
  "schema_version": 2,
  "kind": "status",
  "operation": "status",
  "ok": true,
  "scope": "page",
  "rows": [
    {
      "path": "concern/anonymity.md",
      "name": "anonymity",
      "type": "concern",
      "status": "done"
    }
  ],
  "counts": {
    "stub": 0,
    "draft": 0,
    "done": 1,
    "other": 0
  },
  "notes": []
}
```

## scat_kg.index

```text
index(*, root=".")
```

Writes the index page of each type that has none: `index/<type>.base`, an Obsidian Base that reads the vault itself and so cannot go stale. It never rewrites an existing file, so a column you add by hand stays.

| Parameter | Meaning |
|---|---|
| `root` | The vault folder. |

It prints one line per index page: `created`, or `unchanged` for one that exists. The template ships all five, so on it every line says `unchanged`. It refuses for an index page's name that another file already holds.

=== "Python"

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

As data:

```text
>>> print(json.dumps(scat_kg.index().to_dict(), indent=2))
```

```json
{
  "schema_version": 2,
  "kind": "operation",
  "operation": "index",
  "ok": true,
  "created": [],
  "changed": [],
  "unchanged": [
    "index/group.base",
    "index/concern.base",
    "index/affordance.base",
    "index/technology.base",
    "index/narrative.base"
  ],
  "refused": [],
  "notes": []
}
```

## scat_kg.stub

```text
stub(name, type, *, root=".")
```

Creates one stub page: its type, `status: stub`, and a title made from the name. A `narrative` stub also has an empty `timeframe:` line for you to fill. It never changes an existing file.

| Parameter | Meaning |
|---|---|
| `name` | The new page's name: `a-z`, `0-9` and single hyphens, starting and ending with a letter or digit, at most 64 characters. These names are reserved and refuse: `con`, `prn`, `aux`, `nul`, `com0` to `com9`, `lpt0` to `lpt9`. |
| `type` | The page type key: `group`, `concern`, `affordance`, `technology` or `narrative`. |
| `root` | The vault folder. |

It prints `created <path>`. It refuses when the name is not legal (a reserved name, or one over 64 characters; each ends with a `Fix:` line that offers a name that works), when a Markdown file already has the name (in any letter case), when the type is not one of the five, and when a new `group` page would take the vault over its cap.

=== "Python"

    ```python
    scat_kg.stub("reading-group", type="concern")
    scat_kg.stub("desk-notes-one", type="narrative")
    ```

    ```text
    created concern/reading-group.md
    created narrative/desk-notes-one.md
    ```

=== "CLI"

    ```bash
    uv run scat stub study-circle --type concern
    uv run scat stub desk-notes-two --type narrative
    ```

    ```text
    created concern/study-circle.md
    created narrative/desk-notes-two.md
    ```

Running it again for the same name refuses, and the CLI exits with 1:

```text
refused name `reading-group`: a Markdown file already has this name (concern/reading-group.md); names are compared without regard to case
  Fix: link to the existing page, or choose another name
```

As data:

```text
>>> print(json.dumps(scat_kg.stub("reading-list", type="technology").to_dict(), indent=2))
```

```json
{
  "schema_version": 2,
  "kind": "operation",
  "operation": "stub",
  "ok": true,
  "created": [
    "technology/reading-list.md"
  ],
  "changed": [],
  "unchanged": [],
  "refused": [],
  "notes": []
}
```

## scat_kg.record_edge

```text
record_edge(type, from_, to, told_by, note="", *, root=".")
```

Records an edge: adds its row to each narrative in `told_by` that has none. A node or a narrative that does not exist is made as a stub, the node of the type its layer fixes. It leaves every link as it is.

| Parameter | Meaning |
|---|---|
| `type` | `holds` (group, then concern), `addressed-by` (concern, then affordance) or `provided-by` (affordance, then technology). The verb, such as `"is addressed by"`, is accepted too. |
| `from_`, `to` | The names of the two nodes, in the order the type lists. |
| `told_by` | The name of a narrative, or a list of names. |
| `note` | The row's note (default: none). |
| `root` | The vault folder. |

It prints `created <path>` for each page it made, `changed <path>` for each narrative it added a row to, and a note naming the row and its line. A narrative that already has the row prints `unchanged <path>`, so repeating a call writes nothing. It refuses, and writes nothing, when a narrative it would change is `done` (set it to `draft` first), when the type is unknown, when the two names are the same, or when a node exists with the wrong type for its layer. The result has `edge` (the type, the two names and every narrative that now tells it), `rows_added` and `rows_removed`.

=== "Python"

    ```python
    scat_kg.record_edge("holds", "project-leads", "reading-group", ["desk-notes-one"], note="Said twice.")
    ```

    ```text
    changed narrative/desk-notes-one.md
    note: added `| holds | [[project-leads]] | [[reading-group]] | Said twice. |` to narrative/desk-notes-one.md at line 12
    ```

=== "CLI"

    ```bash
    uv run scat record-edge holds project-leads study-circle --told-by desk-notes-two --note "Said twice."
    ```

    ```text
    changed narrative/desk-notes-two.md
    note: added `| holds | [[project-leads]] | [[study-circle]] | Said twice. |` to narrative/desk-notes-two.md at line 12
    ```

As data:

```text
>>> print(json.dumps(scat_kg.record_edge("addressed-by", "reading-group", "reading-shelf", ["desk-notes-one"]).to_dict(), indent=2))
```

```json
{
  "schema_version": 2,
  "kind": "operation",
  "operation": "record-edge",
  "ok": true,
  "created": [
    "affordance/reading-shelf.md"
  ],
  "changed": [
    "narrative/desk-notes-one.md"
  ],
  "unchanged": [],
  "refused": [],
  "notes": [
    "added `| is addressed by | [[reading-group]] | [[reading-shelf]] | |` to narrative/desk-notes-one.md at line 13"
  ],
  "edge": {
    "type": "addressed-by",
    "from": "reading-group",
    "to": "reading-shelf",
    "narratives": [
      "desk-notes-one"
    ]
  },
  "rows_added": [
    {
      "narrative": "desk-notes-one",
      "file": "narrative/desk-notes-one.md",
      "line": 13,
      "note": ""
    }
  ],
  "rows_removed": []
}
```

## scat_kg.remove_edge

```text
remove_edge(from_, to, told_by=None, *, root=".")
```

Removes an edge: deletes its rows, from the narratives named in `told_by` or, without it, from every narrative that tells it. The links stay.

| Parameter | Meaning |
|---|---|
| `from_`, `to` | The names of the two nodes. The type follows from their layers. |
| `told_by` | A narrative name, or a list of names; without it, every narrative that tells the edge. |
| `root` | The vault folder. |

It prints `changed <path>` for each narrative it deleted a row from, and a note that the links stay. When no narrative tells the edge it prints `remove-edge: nothing to do`. It refuses, and writes nothing, when a narrative it would change is `done`.

=== "Python"

    ```python
    scat_kg.remove_edge("project-leads", "reading-group")
    ```

    ```text
    changed narrative/desk-notes-one.md
    note: removed the row at line 12 of narrative/desk-notes-one.md
    note: the links stay in the narratives; remove one by hand if the account no longer names it
    ```

=== "CLI"

    ```bash
    uv run scat remove-edge project-leads study-circle
    ```

    ```text
    changed narrative/desk-notes-two.md
    note: removed the row at line 12 of narrative/desk-notes-two.md
    note: the links stay in the narratives; remove one by hand if the account no longer names it
    ```

As data:

```text
>>> print(json.dumps(scat_kg.remove_edge("reading-group", "reading-shelf", ["desk-notes-one"]).to_dict(), indent=2))
```

```json
{
  "schema_version": 2,
  "kind": "operation",
  "operation": "remove-edge",
  "ok": true,
  "created": [],
  "changed": [
    "narrative/desk-notes-one.md"
  ],
  "unchanged": [],
  "refused": [],
  "notes": [
    "removed the row at line 12 of narrative/desk-notes-one.md",
    "the links stay in the narratives; remove one by hand if the account no longer names it"
  ],
  "edge": {
    "type": "addressed-by",
    "from": "reading-group",
    "to": "reading-shelf",
    "narratives": []
  },
  "rows_added": [],
  "rows_removed": [
    {
      "narrative": "desk-notes-one",
      "file": "narrative/desk-notes-one.md",
      "line": 12,
      "note": ""
    }
  ]
}
```

## scat_kg.stub_links

```text
stub_links(ref=None, *, root=".")
```

Creates the node pages that the ends of rows link and the vault lacks. Each new page has the type its layer fixes. It creates nothing for a link to an existing page, and nothing for a link outside a row, which has no layer: that is reported as a note, and you make the page with `stub`.

| Parameter | Meaning |
|---|---|
| `ref` | A page name or path: look at that page's rows only. Without it, every page. (The CLI calls this `PAGE`.) |
| `root` | The vault folder. |

It prints `created <path>` for each page made, or `stub-links: nothing to do`. It refuses when a new group would pass the cap.

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

As data:

```text
>>> print(json.dumps(scat_kg.stub_links().to_dict(), indent=2))
```

```json
{
  "schema_version": 2,
  "kind": "operation",
  "operation": "stub-links",
  "ok": true,
  "created": [],
  "changed": [],
  "unchanged": [],
  "refused": [],
  "notes": []
}
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

It prints `changed <path>` and a note with the old status. When the page already has that status, it prints `unchanged <path>` and writes nothing. It refuses when `status` is not one of the three, when the page is not there, and when the frontmatter cannot be read. Setting `done` is judged as the page would stand at `done`, and refused while it would have an error (see below).

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
  Fix: use one of: stub, draft, done (stub: a name, perhaps some metadata; draft: content, not yet complete; done: complete, conformant and signed off by the coder)
```

Setting `done` on a page that would fail refuses with the rule `SCAT-DONE-REFUSED`. The page is not written, and the refusal lists each error with its fix, as `check` prints it at `done`. Here the narrative has neither a `description` nor a `timeframe`:

```text
refused [SCAT-DONE-REFUSED] narrative/desk-notes-one.md: 2 error(s) would stand at status done; status unchanged
  error [SCAT-DONE-FIELD] narrative/desk-notes-one.md field `description`: missing on a page with status: done
    Fix, choose one:
      1. add the line `description: "<one sentence you write>"` (author)
      2. run `scat set-status desk-notes-one draft` (REPL: `scat_kg.set_status("desk-notes-one", "draft")`) if the page is not finished
  error [SCAT-DONE-FIELD] narrative/desk-notes-one.md field `timeframe`: missing on a page with status: done
    Fix, choose one:
      1. replace the line `timeframe: # past | future | mixed` with `timeframe: past` (author)
      2. replace the line `timeframe: # past | future | mixed` with `timeframe: future` (author)
      3. replace the line `timeframe: # past | future | mixed` with `timeframe: mixed` (author)
      4. run `scat set-status desk-notes-one draft` (REPL: `scat_kg.set_status("desk-notes-one", "draft")`) if the page is not finished
  Fix, choose one:
    1. fix the problems above, then run `scat set-status desk-notes-one done` again
    2. leave the page at `draft`: run `scat set-status desk-notes-one draft` (REPL: `scat_kg.set_status("desk-notes-one", "draft")`)
```

As data:

```text
>>> print(json.dumps(scat_kg.set_status("reading-group", "draft").to_dict(), indent=2))
```

```json
{
  "schema_version": 2,
  "kind": "operation",
  "operation": "set-status",
  "ok": true,
  "created": [],
  "changed": [],
  "unchanged": [
    "concern/reading-group.md"
  ],
  "refused": [],
  "notes": [
    "status is already draft"
  ]
}
```

A refusal has the same shape, with `ok` false and the reason in `refused` (the CLI exits with 1):

```text
>>> print(json.dumps(scat_kg.set_status("reading-group", "finished").to_dict(), indent=2))
```

```json
{
  "schema_version": 2,
  "kind": "operation",
  "operation": "set-status",
  "ok": false,
  "created": [],
  "changed": [],
  "unchanged": [],
  "refused": [
    {
      "subject": "status `finished`",
      "why": "this is not a status",
      "fix": {
        "kind": "manual",
        "options": [
          {
            "kind": "manual",
            "text": "use one of: stub, draft, done (stub: a name, perhaps some metadata; draft: content, not yet complete; done: complete, conformant and signed off by the coder)"
          }
        ],
        "notes": []
      }
    }
  ],
  "notes": []
}
```

## Results

Each call returns one of three kinds of result. All print as their message.

| Kind | Returned by | Holds |
|---|---|---|
| `CheckResult` | `check`, when it ran | `problems`, `errors`, `warnings` (tuples of problems), `ok`. A problem has `rule`, `severity` (`"error"` or `"warning"`), `file`, `where`, `what`, `fix` and `line`. |
| `StatusReport` | `status`, when it ran | `scope` (`"page"`, `"neighborhood"` or `"vault"`), `rows` (each with `path`, `name`, `type`, `status`), `counts` (pages per status; `other` is a missing or invalid status), `ok`. |
| `Result` | `stub`, `stub_links`, `set_status`, `index`, and any refusal | `created`, `changed`, `unchanged`, `notes` (tuples of text), `refused` (each with `subject`, `why`, `fix`), `ok`. |
| `EdgeResult` | `record_edge`, `remove_edge` | everything a `Result` holds, and `edge`, `rows_added`, `rows_removed`. |

A `Result` prints its lines in this order: `created`, `changed`, `unchanged`, `refused`, then `note:` lines. When it holds nothing, it prints `<operation>: nothing to do`.

=== "Python"

    ```python
    result = scat_kg.check("anonymity", neighborhood=True)
    result.ok
    len(result.warnings)
    result.problems
    scat_kg.status("anonymity").counts
    ```

    ```text
    True
    0
    ()
    {'stub': 0, 'draft': 0, 'done': 1, 'other': 0}
    ```

=== "CLI"

    ```bash
    uv run scat check anonymity --neighborhood
    ```

    The command prints the message that `str(result)` holds. Its exit code is `result.ok` as 0 or 1: here 0, because there are no errors.

## Where next

Keep the reference close:

- [CLI reference](cli.md): the same operations as `scat` commands, with their `--help` text.
- [Coding guide](../coding.md): how to use them while you code your notes.
- [Home](../index.md)
