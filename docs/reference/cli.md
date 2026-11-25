# CLI reference

!!! tip "Your next step"
    Open a terminal in your vault folder and type `uv run scat --help`.

## Before you start

- A vault folder with a `scat.toml` file in it, for example a copy of the template. [Getting started](../getting-started.md) makes one.
- You type every command in that folder, starting with `uv run`, as in `uv run scat check`. The `--help` blocks below show `scat` alone, which is what the program calls itself.
- Every command has a twin you call from Python: `import scat_kg` in `uv run python`. The twins are in the [Python API reference](api.md), and they give the same messages.

The blocks below hold the exact output of `--help`. If your window is narrower or wider than 80 columns, your own `--help` wraps the lines differently.

## Machine-readable output

Every command takes `--json`. It prints exactly one JSON document on stdout and nothing else, and the exit code is the same as without it. A program such as a plugin reads that document instead of the message. The Python twins return the same data from `to_dict()` (see the [Python API reference](api.md#machine-readable-output)). The fields, and the rule for when `schema_version` changes, are in the [machine interface contract](https://github.com/DynamicalSystemsGroup/scat-kg-tools/blob/dev/contracts/machine-interface.md).

The examples below show `--json` once for each command, with the output a fresh copy of the template gives at that point in the page. These JSON blocks are for reading: they are not run by the docs test.

## scat

```text
usage: scat [-h] <command> ...

Check and work on a SCAT knowledge-graph vault. Every command has a REPL twin
(`import scat_kg`) that gives the same messages.

positional arguments:
  <command>
    check        Check the vault against the rules. PAGE is a page name or its
                 path from the vault folder; without it, the whole vault.
                 Writes nothing.
    status       Show each page's status and the counts. PAGE is a page name
                 or its path from the vault folder; without it, the whole
                 vault.
    set-status   Set a page's status to stub, draft or done.
    index        Write the index page `index/<type>.base` of each type that
                 has none. Never rewrites one.
    stub         Create a stub page: a node (group, concern, affordance or
                 technology) or a narrative.
    stub-links   Create the node pages that the ends of rows link and the
                 vault lacks. PAGE limits it to one page.
    record-edge  Record an edge: add its row to each narrative named by
                 --told-by that has none, stubbing a missing node or
                 narrative. Leaves the links as they are. Refuses a narrative
                 that is done.
    remove-edge  Remove an edge: delete its rows, from the narratives named by
                 --told-by or, without it, from every narrative that tells it.
                 Leaves the links. Refuses a narrative that is done.

options:
  -h, --help     show this help message and exit

Run `scat <command> --help` for a command.
```

`scat` has eight commands. Each prints a message and exits with a code:

| Exit code | Meaning |
|---|---|
| 0 | No error and no refusal. Warnings alone give 0. |
| 1 | An error was found, or the command refused: it says why and gives a `Fix:` line. |
| 2 | The command line cannot be read (a missing argument, an unknown command). Nothing is run. |

Every command takes `--root ROOT`, the vault folder (default: the current folder). A command that refuses writes nothing.

=== "Python"

    ```python
    import scat_kg

    print(scat_kg.__doc__)
    ```

    ```text
    scat_kg: check and work on a SCAT knowledge-graph vault from the Python REPL.

        import scat_kg

        scat_kg.check()                     # the whole vault in the current directory
        scat_kg.check("concern/x.md")       # one page (a name or a path)
        scat_kg.check("x", neighborhood=True)
        scat_kg.status()                    # the same three scopes, for status
        scat_kg.set_status("x", "draft")
        scat_kg.index()
        scat_kg.stub("x", type="concern")
        scat_kg.stub_links()                # or stub_links("x")
        scat_kg.record_edge("holds", "a", "b", ["narrative-name"], note="")
        scat_kg.remove_edge("a", "b")       # or remove_edge("a", "b", ["narrative-name"])

    Each call takes `root=` (the vault folder; default: the current directory) and returns an object whose
    `str()` is the message the `scat` command prints, and which prints as that message. `.ok` is False when
    there is an error or a refusal (warnings alone leave it True): it is what the command's exit code is.
    ```

=== "CLI"

    ```bash
    uv run scat --help
    ```

    The output is the block above.

## scat check

```text
usage: scat check [-h] [--root ROOT] [--json] [--neighborhood] [PAGE]

Check the vault against the rules. PAGE is a page name or its path from the vault folder; without it, the whole vault. Writes nothing.

positional arguments:
  PAGE            check this page only

options:
  -h, --help      show this help message and exit
  --root ROOT     the vault folder, the one with scat.toml (default: here)
  --json          print the result as one JSON document (machine-interface
                  contract), nothing else
  --neighborhood  check PAGE and every page one link away, in either direction

REPL: `scat_kg.check()`, `scat_kg.check("<page>")`, `scat_kg.check("<page>", neighborhood=True)`
```

Checks the whole vault, one page, or one page and every page one link away. It writes nothing. It prints each problem with its rule id and a `Fix:` line, then a count line, or `no problems`.

Exit codes: 0 when there are no errors (warnings are fine), 1 when there is an error or a refusal (a page that is not there, a vault folder that is not there, `--neighborhood` without `PAGE`).

=== "Python"

    ```python
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

With `--json`, on the unchanged template:

```text
$ uv run scat check --json
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

To see a problem with a fix a program can apply, change `[[cap-setting]]` to `[[cap-settin]]` in the second row of the table of `narrative/groups-under-a-cap-pitch.md` (line 22), a one-letter typo in a link. The fix has three options: a `replace-text` edit that writes the right name, a `command` that creates the missing page, and a `delete-line` edit. `scat check` exits with 1.

```text
$ uv run scat check --json
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

## scat status

```text
usage: scat status [-h] [--root ROOT] [--json] [--neighborhood] [PAGE]

Show each page's status and the counts. PAGE is a page name or its path from the vault folder; without it, the whole vault.

positional arguments:
  PAGE            show this page only

options:
  -h, --help      show this help message and exit
  --root ROOT     the vault folder, the one with scat.toml (default: here)
  --json          print the result as one JSON document (machine-interface
                  contract), nothing else
  --neighborhood  show PAGE and every page one link away, in either direction

REPL: `scat_kg.status()`, `scat_kg.status("<page>")`, `scat_kg.status("<page>", neighborhood=True)`
```

Shows the status of each page, then the counts. It writes nothing. The status is `stub`, `draft` or `done`.

Exit codes: 0, or 1 for a refusal (a page that is not there, a vault folder that is not there, `--neighborhood` without `PAGE`).

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

With `--json`:

```text
$ uv run scat status anonymity --json
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

## scat set-status

```text
usage: scat set-status [-h] [--root ROOT] [--json] PAGE STATUS

Set a page's status to stub, draft or done.

positional arguments:
  PAGE         the page's name or path
  STATUS       stub, draft or done

options:
  -h, --help   show this help message and exit
  --root ROOT  the vault folder, the one with scat.toml (default: here)
  --json       print the result as one JSON document (machine-interface
               contract), nothing else

REPL: `scat_kg.set_status("<page-name>", "<status>")`
```

Changes the `status:` line of one page and nothing else in the file. `PAGE` is a name or a path. Setting a narrative or a node to `done` is judged as the page would stand at `done`, and refused while it would fail: the refusal lists each error with its fix and writes nothing (see [Coding](../coding.md#6-set-it-to-done)).

Exit codes: 0 when the status was changed or already was that value, 1 for a refusal (not a status, no such page, a page that would fail at `done`).

=== "Python"

    ```python
    scat_kg.set_status("anonymity", "draft")
    ```

    ```text
    changed concern/anonymity.md
    note: `status` set to draft (was done)
    ```

=== "CLI"

    ```bash
    uv run scat set-status attribution draft
    ```

    ```text
    changed concern/attribution.md
    note: `status` set to draft (was done)
    ```

The CLI example uses a different page from the Python one, so both can run in one vault. Running either again prints `unchanged` and a note that the status is already `draft`, and still exits with 0.

With `--json`:

```text
$ uv run scat set-status attribution draft --json
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
    "concern/attribution.md"
  ],
  "refused": [],
  "notes": [
    "status is already draft"
  ]
}
```

A refusal has the same shape, with `ok` false and the reason in `refused`; the exit code is 1:

```text
$ uv run scat set-status attribution finished --json
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

## scat index

```text
usage: scat index [-h] [--root ROOT] [--json]

Write the index page `index/<type>.base` of each type that has none. Never rewrites one.

options:
  -h, --help   show this help message and exit
  --root ROOT  the vault folder, the one with scat.toml (default: here)
  --json       print the result as one JSON document (machine-interface
               contract), nothing else

REPL: `scat_kg.index()`
```

Writes `index/<type>.base`, the index page of each type, for each one that is missing, and never rewrites one. It prints one line per file: `created`, `changed` or `unchanged`. The template ships all five, so on it every line says `unchanged`.

Exit codes: 0, or 1 for a refusal (another file holds an index page's name).

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

With `--json`:

```text
$ uv run scat index --json
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

## scat stub

```text
usage: scat stub [-h] [--root ROOT] [--json] --type TYPE NAME

Create a stub page: a node (group, concern, affordance or technology) or a narrative.

positional arguments:
  NAME         the new page's name: a-z, 0-9 and hyphens

options:
  -h, --help   show this help message and exit
  --root ROOT  the vault folder, the one with scat.toml (default: here)
  --json       print the result as one JSON document (machine-interface
               contract), nothing else
  --type TYPE  the page's type, one of: group, concern, affordance,
               technology, narrative

REPL: `scat_kg.stub("<page-name>", type="<type>")`
```

Creates one page with `status: stub`. The `--type` option is required. A node (`group`, `concern`, `affordance`, `technology`) or a `narrative`; a narrative stub also carries an empty `timeframe:` line for you to fill.

Exit codes: 0 when the page was created, 1 for a refusal (not a legal name, a file already has the name, not a stubbable type, or the group cap). A missing `--type` is a command line that cannot be read: exit code 2.

The CLI example uses different names from the Python one, so both can run in one vault.

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

With `--json`:

```text
$ uv run scat stub study-circle-two --type concern --json
```

```json
{
  "schema_version": 2,
  "kind": "operation",
  "operation": "stub",
  "ok": true,
  "created": [
    "concern/study-circle-two.md"
  ],
  "changed": [],
  "unchanged": [],
  "refused": [],
  "notes": []
}
```

## scat stub-links

```text
usage: scat stub-links [-h] [--root ROOT] [--json] [PAGE]

Create the node pages that the ends of rows link and the vault lacks. PAGE limits it to one page.

positional arguments:
  PAGE         look at this page's links only

options:
  -h, --help   show this help message and exit
  --root ROOT  the vault folder, the one with scat.toml (default: here)
  --json       print the result as one JSON document (machine-interface
               contract), nothing else

REPL: `scat_kg.stub_links()`, `scat_kg.stub_links("<page>")`
```

Creates the node pages that the ends of rows link and the vault lacks, each of the type its layer fixes, from one page or the whole vault. A link elsewhere in a narrative names no layer, so it is reported as a note and made with `scat stub`. When there is nothing to create it prints `stub-links: nothing to do`.

Exit codes: 0 when it created pages or had nothing to do, 1 for a refusal (the group cap, a page that is not there).

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

With `--json`:

```text
$ uv run scat stub-links --json
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

## scat record-edge

```text
usage: scat record-edge [-h] [--root ROOT] [--json] --told-by NARRATIVE
                        [--note TEXT]
                        TYPE FROM TO

Record an edge: add its row to each narrative named by --told-by that has none, stubbing a missing node or narrative. Leaves the links as they are. Refuses a narrative that is done.

positional arguments:
  TYPE                 one of: holds (group then concern), addressed-by
                       (concern then affordance), provided-by (affordance then
                       technology)
  FROM                 the name of the node at the first end
  TO                   the name of the node at the second end

options:
  -h, --help           show this help message and exit
  --root ROOT          the vault folder, the one with scat.toml (default:
                       here)
  --json               print the result as one JSON document (machine-
                       interface contract), nothing else
  --told-by NARRATIVE  the narrative that tells the edge; repeat it for each
                       narrative
  --note TEXT          the row's note (default: none)

REPL: `scat_kg.record_edge("<type>", "<from>", "<to>", ["<narrative>"], note="<text>")`
```

Records an edge: adds its row to each narrative named by `--told-by` that has none, makes a missing node or narrative as a stub, and leaves every link alone. `TYPE` is `holds`, `addressed-by` or `provided-by` (the verb, such as `"is addressed by"`, is accepted too). If a narrative already has the row it prints `unchanged` and writes nothing. `--note` is the row's note.

Exit codes: 0 when it changed or found the row there, 1 for a refusal (a narrative that is `done`, an unknown type, ends in the wrong layers, the same name at both ends).

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

With `--json`, which adds the edge and the rows added:

```text
$ uv run scat record-edge addressed-by study-circle reading-shelf --told-by desk-notes-two --json
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
    "narrative/desk-notes-two.md"
  ],
  "unchanged": [],
  "refused": [],
  "notes": [
    "added `| is addressed by | [[study-circle]] | [[reading-shelf]] | |` to narrative/desk-notes-two.md at line 13"
  ],
  "edge": {
    "type": "addressed-by",
    "from": "study-circle",
    "to": "reading-shelf",
    "narratives": [
      "desk-notes-two"
    ]
  },
  "rows_added": [
    {
      "narrative": "desk-notes-two",
      "file": "narrative/desk-notes-two.md",
      "line": 13,
      "note": ""
    }
  ],
  "rows_removed": []
}
```

## scat remove-edge

```text
usage: scat remove-edge [-h] [--root ROOT] [--json] [--told-by NARRATIVE]
                        FROM TO

Remove an edge: delete its rows, from the narratives named by --told-by or, without it, from every narrative that tells it. Leaves the links. Refuses a narrative that is done.

positional arguments:
  FROM                 the name of the node at the first end
  TO                   the name of the node at the second end

options:
  -h, --help           show this help message and exit
  --root ROOT          the vault folder, the one with scat.toml (default:
                       here)
  --json               print the result as one JSON document (machine-
                       interface contract), nothing else
  --told-by NARRATIVE  remove the rows of this narrative only; repeat it for
                       each narrative

REPL: `scat_kg.remove_edge("<from>", "<to>")`, `scat_kg.remove_edge("<from>", "<to>", ["<narrative>"])`
```

Removes an edge: deletes its rows, from the narratives named by `--told-by` or, without it, from every narrative that tells it. The links stay. It refuses a narrative that is `done`: set it to `draft` first. When no narrative tells the edge it prints `remove-edge: nothing to do`.

Exit codes: 0, or 1 for a refusal (a narrative that is `done`).

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

With `--json`:

```text
$ uv run scat remove-edge study-circle reading-shelf --json
```

```json
{
  "schema_version": 2,
  "kind": "operation",
  "operation": "remove-edge",
  "ok": true,
  "created": [],
  "changed": [
    "narrative/desk-notes-two.md"
  ],
  "unchanged": [],
  "refused": [],
  "notes": [
    "removed the row at line 12 of narrative/desk-notes-two.md",
    "the links stay in the narratives; remove one by hand if the account no longer names it"
  ],
  "edge": {
    "type": "addressed-by",
    "from": "study-circle",
    "to": "reading-shelf",
    "narratives": []
  },
  "rows_added": [],
  "rows_removed": [
    {
      "narrative": "desk-notes-two",
      "file": "narrative/desk-notes-two.md",
      "line": 12,
      "note": ""
    }
  ]
}
```

## Where next

Keep the reference close:

- [Python API reference](api.md): every operation, with its parameters and what it returns.
- [Coding guide](../coding.md): how to use these commands while you code your notes.
- [Home](../index.md)
