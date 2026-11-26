# CLI reference

!!! tip "Your next step"
    Open a terminal in your vault folder and type `uv run scat --help`.

## Before you start

- A vault folder with a `scat.toml` file in it, for example a copy of the template. [Getting started](../getting-started.md) makes one.
- You type every command in that folder, starting with `uv run`, as in `uv run scat check`. The `--help` blocks below show `scat` alone, which is what the program calls itself.
- Every command has a twin you call from Python: `import scat_kg` in `uv run python`. The twins are in the [Python API reference](api.md), and they give the same messages.

The blocks below hold the exact output of `--help`. If your window is narrower or wider than 80 columns, your own `--help` wraps the lines differently.

The MCP server offers the same operations to a chat: see the [MCP server reference](mcp.md).

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
    check         Check the vault against the rules. PAGE is a page name or
                  its path from the vault folder; without it, the whole vault.
                  Writes nothing.
    status        Show each page's status and the counts. PAGE is a page name
                  or its path from the vault folder; without it, the whole
                  vault.
    set-status    Set a page's status to stub, draft or done.
    index         Write the index page `index/<type>.base` of each type that
                  has none. Never rewrites one.
    stub          Create a stub page: a node (group, concern, affordance or
                  technology), a narrative, or, where the vault's attribution
                  mode is required or optional, a contributor page.
    stub-links    Create the node pages that the ends of rows link and the
                  vault lacks. PAGE limits it to one page.
    record-edge   Record an edge: add its row to each narrative named by
                  --told-by that has none, stubbing a missing node or
                  narrative. Leaves the links as they are. Refuses a narrative
                  that is done.
    remove-edge   Remove an edge: delete its rows, from the narratives named
                  by --told-by or, without it, from every narrative that tells
                  it. Leaves the links. Refuses a narrative that is done.
    fingerprint   Show a narrative's fingerprint: its nodes by layer and the
                  edges its rows tell; with --candidates, also the links that
                  have no row. NARRATIVE is a name; without it, every
                  narrative. Writes nothing.
    edges         Show every edge of one type, with the narratives that tell
                  it and its status. Writes nothing.
    layered       Show the layered view: the union of the fingerprints of the
                  narratives named by --narrative, or, without it, of every
                  narrative. Writes nothing.
    trace         Follow edges from a node: up toward the groups, down toward
                  the technologies, or both. The node itself is left out.
                  Writes nothing.
    evidence      Show everything the vault says of one node page: the
                  narratives that link it, each with the paragraph around
                  every link and the linking sentence between >> and <<; its
                  edges with the narratives that tell them; and its adjacent
                  nodes by layer. Writes nothing.
    attribution   Show the narratives by contributor: each contributor page
                  with the narratives that name it, and the narratives that
                  name none. Refuses where the vault's attribution mode is
                  disallowed. Writes nothing.
    export-edges  Write each edge table to DIR as `<type>.csv` and
                  `<type>.md`. Overwrites a file only when its content
                  differs; makes DIR if it is not there. Refuses where `scat
                  edges` would, and then writes nothing.
    draw          Draw a view as an image (needs the extra `draw`): `.png` or
                  `.svg`.

options:
  -h, --help      show this help message and exit

Run `scat <command> --help` for a command.
```

`scat` has sixteen commands. Each prints a message and exits with a code:

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
    scat_kg.load()                      # the knowledge graph, derived from the pages
    scat_kg.fingerprint("narrative-name")   # views: also edge_table("holds"), layered(), trace("node")
    scat_kg.evidence("node")            # one node: its narratives, paragraphs, edges and adjacent nodes
    scat_kg.attribution()               # narratives by contributor (where the vault's mode allows attribution)
    scat_kg.export_edges("tables")      # the three edge tables, as CSV and Markdown, into this folder

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
  "schema_version": 3,
  "kind": "check",
  "operation": "check",
  "ok": true,
  "mode": "disallowed",
  "problems": []
}
```

To see a problem with a fix a program can apply, change `[[cap-setting]]` to `[[cap-settin]]` in the second row of the table of `narrative/groups-under-a-cap-pitch.md` (line 22), a one-letter typo in a link. The fix has three options: a `replace-text` edit that writes the right name, a `command` that creates the missing page, and a `delete-line` edit. `scat check` exits with 1.

```text
$ uv run scat check --json
```

```json
{
  "schema_version": 3,
  "kind": "check",
  "operation": "check",
  "ok": false,
  "mode": "disallowed",
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
                "find": "| [[groups-clustered-under-a-cap]] | is provided by | [[cap-settin]] | The cap setting is what fixes the number of groups. The cap is a per-instance parameter (D-020); the example vault sets it to 3. |"
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
  "schema_version": 3,
  "kind": "status",
  "operation": "status",
  "ok": true,
  "mode": "disallowed",
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
  "schema_version": 3,
  "kind": "operation",
  "operation": "set-status",
  "ok": true,
  "mode": "disallowed",
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
  "schema_version": 3,
  "kind": "operation",
  "operation": "set-status",
  "ok": false,
  "mode": "disallowed",
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
  "schema_version": 3,
  "kind": "operation",
  "operation": "index",
  "ok": true,
  "mode": "disallowed",
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

Create a stub page: a node (group, concern, affordance or technology), a narrative, or, where the vault's attribution mode is required or optional, a contributor page.

positional arguments:
  NAME         the new page's name: a-z, 0-9 and hyphens

options:
  -h, --help   show this help message and exit
  --root ROOT  the vault folder, the one with scat.toml (default: here)
  --json       print the result as one JSON document (machine-interface
               contract), nothing else
  --type TYPE  the page's type, one of: group, concern, affordance,
               technology, narrative, contributor

REPL: `scat_kg.stub("<page-name>", type="<type>")`
```

Creates one page with `status: stub`. The `--type` option is required. A node (`group`, `concern`, `affordance`, `technology`), a `narrative`, or a `contributor` page. A narrative stub also carries an empty `timeframe:` line for you to fill. A contributor page is made only where the vault's attribution mode (in `scat.toml`) is `required` or `optional`; in `disallowed` mode the command refuses and says that the vault holds no contributor page.

Exit codes: 0 when the page was created, 1 for a refusal (not a legal name, a file already has the name, not a stubbable type, the group cap, or a contributor page where the attribution mode is `disallowed`). A missing `--type` is a command line that cannot be read: exit code 2.

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
  "schema_version": 3,
  "kind": "operation",
  "operation": "stub",
  "ok": true,
  "mode": "disallowed",
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
  "schema_version": 3,
  "kind": "operation",
  "operation": "stub-links",
  "ok": true,
  "mode": "disallowed",
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
    note: added `| [[project-leads]] | holds | [[reading-group]] | Said twice. |` to narrative/desk-notes-one.md at line 12
    ```

=== "CLI"

    ```bash
    uv run scat record-edge holds project-leads study-circle --told-by desk-notes-two --note "Said twice."
    ```

    ```text
    changed narrative/desk-notes-two.md
    note: added `| [[project-leads]] | holds | [[study-circle]] | Said twice. |` to narrative/desk-notes-two.md at line 12
    ```

With `--json`, which adds the edge and the rows added:

```text
$ uv run scat record-edge addressed-by study-circle reading-shelf --told-by desk-notes-two --json
```

```json
{
  "schema_version": 3,
  "kind": "operation",
  "operation": "record-edge",
  "ok": true,
  "mode": "disallowed",
  "created": [
    "affordance/reading-shelf.md"
  ],
  "changed": [
    "narrative/desk-notes-two.md"
  ],
  "unchanged": [],
  "refused": [],
  "notes": [
    "added `| [[study-circle]] | is addressed by | [[reading-shelf]] | |` to narrative/desk-notes-two.md at line 13"
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
  "schema_version": 3,
  "kind": "operation",
  "operation": "remove-edge",
  "ok": true,
  "mode": "disallowed",
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

## scat fingerprint

```text
usage: scat fingerprint [-h] [--root ROOT] [--json] [--candidates] [NARRATIVE]

Show a narrative's fingerprint: its nodes by layer and the edges its rows tell; with --candidates, also the links that have no row. NARRATIVE is a name; without it, every narrative. Writes nothing.

positional arguments:
  NARRATIVE     show this narrative only

options:
  -h, --help    show this help message and exit
  --root ROOT   the vault folder, the one with scat.toml (default: here)
  --json        print the result as one JSON document (machine-interface
                contract), nothing else
  --candidates  also show the candidates: links between two nodes that have no
                row

REPL: `scat_kg.fingerprint()`, `scat_kg.fingerprint("<narrative>", candidates=True)`
```

Shows what one narrative tells: its nodes by layer, the edges its rows tell (each with its status and every narrative that tells it), and, with `--candidates`, the candidates, which are links between two nodes that an edge type fits and that have no row. Without the option the fingerprint shows no candidates. Without `NARRATIVE` it shows every narrative, in path order. It writes nothing and never shows a relationship annotation.

It refuses, writing nothing, when the name is not a narrative, when two pages share the name, and when a page it draws has an error: the refusal carries those problems with their fixes.

Exit codes: 0, or 1 for a refusal.

=== "Python"

    ```python
    scat_kg.fingerprint("groups-under-a-cap-pitch")
    ```

    ```text
    fingerprint groups-under-a-cap-pitch (architecture, done)
      concern
        anonymity [draft]
      affordance
        groups-clustered-under-a-cap [done]
      technology
        cap-setting [done]
      edges
        addressed-by: anonymity -> groups-clustered-under-a-cap [done; told by groups-under-a-cap-pitch, notes-at-a-chatham-house-session]
        provided-by: groups-clustered-under-a-cap -> cap-setting [done; told by groups-under-a-cap-pitch]
    ```

=== "CLI"

    ```bash
    uv run scat fingerprint groups-under-a-cap-pitch
    ```

    ```text
    fingerprint groups-under-a-cap-pitch (architecture, done)
      concern
        anonymity [draft]
      affordance
        groups-clustered-under-a-cap [done]
      technology
        cap-setting [done]
      edges
        addressed-by: anonymity -> groups-clustered-under-a-cap [done; told by groups-under-a-cap-pitch, notes-at-a-chatham-house-session]
        provided-by: groups-clustered-under-a-cap -> cap-setting [done; told by groups-under-a-cap-pitch]
    ```

With `--json`:

```text
$ uv run scat fingerprint groups-under-a-cap-pitch --json
```

```json
{
  "schema_version": 3,
  "kind": "view",
  "operation": "fingerprint",
  "ok": true,
  "mode": "disallowed",
  "narratives": [
    {
      "name": "groups-under-a-cap-pitch",
      "kind": "architecture",
      "status": "done",
      "nodes": [
        {
          "name": "anonymity",
          "type": "concern",
          "status": "draft"
        },
        {
          "name": "groups-clustered-under-a-cap",
          "type": "affordance",
          "status": "done"
        },
        {
          "name": "cap-setting",
          "type": "technology",
          "status": "done"
        }
      ],
      "edges": [
        {
          "type": "addressed-by",
          "from": "anonymity",
          "to": "groups-clustered-under-a-cap",
          "narratives": [
            "groups-under-a-cap-pitch",
            "notes-at-a-chatham-house-session"
          ],
          "status": "done"
        },
        {
          "type": "provided-by",
          "from": "groups-clustered-under-a-cap",
          "to": "cap-setting",
          "narratives": [
            "groups-under-a-cap-pitch"
          ],
          "status": "done"
        }
      ]
    }
  ],
  "excluded": []
}
```

With `--candidates` each narrative also has a `candidates` list (here `"candidates": []`); without the option the key is absent.

## scat edges

```text
usage: scat edges [-h] [--root ROOT] [--json] TYPE

Show every edge of one type, with the narratives that tell it and its status. Writes nothing.

positional arguments:
  TYPE         one of: holds (group then concern), addressed-by (concern then
               affordance), provided-by (affordance then technology)

options:
  -h, --help   show this help message and exit
  --root ROOT  the vault folder, the one with scat.toml (default: here)
  --json       print the result as one JSON document (machine-interface
               contract), nothing else

REPL: `scat_kg.edge_table("<type>")`
```

Shows every edge of one type, in the order of the graph: the two ends, the narratives that tell it and its status. It writes nothing.

Exit codes: 0, or 1 for a refusal (a type that is not one of the three, a page it draws that has an error).

=== "Python"

    ```python
    scat_kg.edge_table("holds")
    ```

    ```text
    edges holds (group -> concern): 2
        holds: facilitator-analysts -> anonymity [done; told by notes-at-a-chatham-house-session]
        holds: project-leads -> intent-without-drift [done; told by false-start-and-clean-restart]
    ```

=== "CLI"

    ```bash
    uv run scat edges holds
    ```

    ```text
    edges holds (group -> concern): 2
        holds: facilitator-analysts -> anonymity [done; told by notes-at-a-chatham-house-session]
        holds: project-leads -> intent-without-drift [done; told by false-start-and-clean-restart]
    ```

With `--json`:

```text
$ uv run scat edges holds --json
```

```json
{
  "schema_version": 3,
  "kind": "view",
  "operation": "edges",
  "ok": true,
  "mode": "disallowed",
  "edge_type": "holds",
  "from_layer": "group",
  "to_layer": "concern",
  "rows": [
    {
      "type": "holds",
      "from": "facilitator-analysts",
      "to": "anonymity",
      "narratives": [
        "notes-at-a-chatham-house-session"
      ],
      "status": "done"
    },
    {
      "type": "holds",
      "from": "project-leads",
      "to": "intent-without-drift",
      "narratives": [
        "false-start-and-clean-restart"
      ],
      "status": "done"
    }
  ],
  "excluded": []
}
```

## scat layered

```text
usage: scat layered [-h] [--root ROOT] [--json] [--narrative NARRATIVE]

Show the layered view: the union of the fingerprints of the narratives named by --narrative, or, without it, of every narrative. Writes nothing.

options:
  -h, --help            show this help message and exit
  --root ROOT           the vault folder, the one with scat.toml (default:
                        here)
  --json                print the result as one JSON document (machine-
                        interface contract), nothing else
  --narrative NARRATIVE
                        include this narrative; repeat it for each narrative

REPL: `scat_kg.layered()`, `scat_kg.layered(["<narrative>"])`
```

Shows the layered view: the union of the fingerprints of the narratives you name, or of every narrative when you name none. The nodes are grouped by layer, in layer order, and the edges are the rows those narratives tell; there are no candidates. It writes nothing.

Exit codes: 0, or 1 for a refusal (a name that is not a narrative, a page it draws that has an error).

=== "Python"

    ```python
    scat_kg.layered(["groups-under-a-cap-pitch"])
    ```

    ```text
    layered view of groups-under-a-cap-pitch
      concern
        anonymity [draft]
      affordance
        groups-clustered-under-a-cap [done]
      technology
        cap-setting [done]
      edges
        addressed-by: anonymity -> groups-clustered-under-a-cap [done; told by groups-under-a-cap-pitch, notes-at-a-chatham-house-session]
        provided-by: groups-clustered-under-a-cap -> cap-setting [done; told by groups-under-a-cap-pitch]
    ```

=== "CLI"

    ```bash
    uv run scat layered --narrative groups-under-a-cap-pitch
    ```

    ```text
    layered view of groups-under-a-cap-pitch
      concern
        anonymity [draft]
      affordance
        groups-clustered-under-a-cap [done]
      technology
        cap-setting [done]
      edges
        addressed-by: anonymity -> groups-clustered-under-a-cap [done; told by groups-under-a-cap-pitch, notes-at-a-chatham-house-session]
        provided-by: groups-clustered-under-a-cap -> cap-setting [done; told by groups-under-a-cap-pitch]
    ```

With `--json`:

```text
$ uv run scat layered --narrative groups-under-a-cap-pitch --json
```

```json
{
  "schema_version": 3,
  "kind": "view",
  "operation": "layered",
  "ok": true,
  "mode": "disallowed",
  "narratives": [
    "groups-under-a-cap-pitch"
  ],
  "nodes": {
    "group": [],
    "concern": [
      {
        "name": "anonymity",
        "type": "concern",
        "status": "draft"
      }
    ],
    "affordance": [
      {
        "name": "groups-clustered-under-a-cap",
        "type": "affordance",
        "status": "done"
      }
    ],
    "technology": [
      {
        "name": "cap-setting",
        "type": "technology",
        "status": "done"
      }
    ]
  },
  "edges": [
    {
      "type": "addressed-by",
      "from": "anonymity",
      "to": "groups-clustered-under-a-cap",
      "narratives": [
        "groups-under-a-cap-pitch",
        "notes-at-a-chatham-house-session"
      ],
      "status": "done"
    },
    {
      "type": "provided-by",
      "from": "groups-clustered-under-a-cap",
      "to": "cap-setting",
      "narratives": [
        "groups-under-a-cap-pitch"
      ],
      "status": "done"
    }
  ],
  "excluded": []
}
```

## scat trace

```text
usage: scat trace [-h] [--root ROOT] [--json] [--direction DIRECTION] NODE

Follow edges from a node: up toward the groups, down toward the technologies, or both. The node itself is left out. Writes nothing.

positional arguments:
  NODE                  the name of a group, concern, affordance or technology

options:
  -h, --help            show this help message and exit
  --root ROOT           the vault folder, the one with scat.toml (default:
                        here)
  --json                print the result as one JSON document (machine-
                        interface contract), nothing else
  --direction DIRECTION
                        up, down or both (default: both)

REPL: `scat_kg.trace("<node>")`, `scat_kg.trace("<node>", "<direction>")`
```

Follows edges from a node, and shows the nodes it reaches in layer order and the edges it walked. `up` goes toward the groups, `down` toward the technologies, `both` (the default) does both. It writes nothing.

Exit codes: 0, or 1 for a refusal (a name that is not a node, a direction that is not one of the three, a page it draws that has an error).

=== "Python"

    ```python
    scat_kg.trace("anonymity", "up")
    ```

    ```text
    trace anonymity (up)
     up
      group
        facilitator-analysts [done]
      edges
        holds: facilitator-analysts -> anonymity [done; told by notes-at-a-chatham-house-session]
    ```

=== "CLI"

    ```bash
    uv run scat trace anonymity --direction up
    ```

    ```text
    trace anonymity (up)
     up
      group
        facilitator-analysts [done]
      edges
        holds: facilitator-analysts -> anonymity [done; told by notes-at-a-chatham-house-session]
    ```

With `--json`:

```text
$ uv run scat trace anonymity --direction up --json
```

```json
{
  "schema_version": 3,
  "kind": "view",
  "operation": "trace",
  "ok": true,
  "mode": "disallowed",
  "node": "anonymity",
  "direction": "up",
  "up": [
    {
      "name": "facilitator-analysts",
      "type": "group",
      "status": "done"
    }
  ],
  "down": [],
  "edges": [
    {
      "type": "holds",
      "from": "facilitator-analysts",
      "to": "anonymity",
      "narratives": [
        "notes-at-a-chatham-house-session"
      ],
      "status": "done"
    }
  ],
  "excluded": []
}
```

## scat evidence

```text
usage: scat evidence [-h] [--root ROOT] [--json] NODE

Show everything the vault says of one node page: the narratives that link it, each with the paragraph around every link and the linking sentence between >> and <<; its edges with the narratives that tell them; and its adjacent nodes by layer. Writes nothing.

positional arguments:
  NODE         the name of a group, concern, affordance or technology

options:
  -h, --help   show this help message and exit
  --root ROOT  the vault folder, the one with scat.toml (default: here)
  --json       print the result as one JSON document (machine-interface
               contract), nothing else

REPL: `scat_kg.evidence("<node>")`
```

Shows, for one node page, what the vault says of it, so that you can write the page from the narratives and not from one of them. It prints the vault's attribution mode first, then:

- **narratives**: every narrative that links the node, with its status, kind and timeframe. For each link in the account, the whole paragraph around it (the lines between blank lines, as written), with the sentence that holds the link between `>>` and `<<`. The sentence that matters may be the next one: the paragraph is there to show it. Several links in one paragraph make one entry. A narrative that links the node and tells no edge for it says so. A link inside the `Edges told` table is not a paragraph: it shows through the edges.
- **edges**: the node's edges, each with the narratives that tell it and each row's note.
- **adjacent nodes**: the nodes one edge away, by layer.

A paragraph is the lines between blank lines; a row of any table (a line that starts with `|`) is a paragraph of its own and is never cut into sentences. A sentence ends at a `.`, `!` or `?` followed by a space, so an abbreviation such as `e.g.` ends one early; the paragraph is always whole. A narrative that links no node page is excluded and listed at the end, as in the other views. The command reads no `attributed_to` field and lists no contributor page. It writes nothing.

Exit codes: 0, or 1 for a refusal (a name that is not a node page, such as a narrative or a contributor page, a name that two pages carry, a page it draws that has an error).

=== "Python"

    ```python
    scat_kg.evidence("anonymity")
    ```

    ```text
    attribution mode: disallowed
    evidence anonymity (concern, draft): 2 narratives, 2 edges
      narratives (the sentence with the link is between >> and <<)
        groups-under-a-cap-pitch [done, architecture, future]
          line 12
            - [[groups-clustered-under-a-cap|The vault holds groups]], and [[cap-setting|an instance setting]] caps their number.
            - The cap is set for each vault, in the vault's own configuration. The example vault sets it to 3.
            - A group is named by its role. No group stands for one identifiable person.
            - >>Reason given in the record: the people in the data are groups under the Chatham House rule, so [[anonymity|no individual is identifiable]].<<
        notes-at-a-chatham-house-session [done, scenario, mixed]
          line 12
            - [[workshop-participants|Workshop participants]] tell stories in conversations. The work is sized for manual note-taking in Obsidian.
            - [[facilitator-analysts|Facilitators]] take the field notes. >>The setting is Chatham House rule: the people in the data are groups, so [[anonymity|no individual is identifiable]].<<
            - The vault holds groups, and [[groups-clustered-under-a-cap|an instance setting caps their number]].
            - This vault runs in the disallowed attribution mode: the notes name groups, never individuals, and no note links to a person. A project that needs names chooses another mode when it sets up.
            - >>[[attribution|Attribution]] and [[anonymity]] conflict as concerns, and the vault records that as a remark on one of them.<<
      edges
        holds: facilitator-analysts -> anonymity [done; told by notes-at-a-chatham-house-session]
            notes-at-a-chatham-house-session: They take the field notes under the Chatham House rule, so no individual is identifiable (D-010).
        addressed-by: anonymity -> groups-clustered-under-a-cap [done; told by groups-under-a-cap-pitch, notes-at-a-chatham-house-session]
            groups-under-a-cap-pitch: Participants appear only as groups, so no group stands for one identifiable person.
            notes-at-a-chatham-house-session: The mission says the people in the data are groups under the Chatham House rule, so no individual is identifiable.
      adjacent nodes
        group
          facilitator-analysts [done]
        affordance
          groups-clustered-under-a-cap [done]
    excluded (no node page linked; link one node page to include it)
        desk-notes-one (narrative/desk-notes-one.md)
        desk-notes-two (narrative/desk-notes-two.md)
    ```

=== "CLI"

    ```bash
    uv run scat evidence anonymity
    ```

    The same text.

A name that is not a node page is refused, and nothing is written:

```text
$ uv run scat evidence nobody
refused nobody: no node has this name
  Fix: give the name of a page (the file name without `.md`) that is a group, concern, affordance or technology
```

With `--json`:

```text
$ uv run scat evidence anonymity --json
```

```json
{
  "schema_version": 3,
  "kind": "view",
  "operation": "evidence",
  "ok": true,
  "mode": "disallowed",
  "node": "anonymity",
  "node_type": "concern",
  "node_status": "draft",
  "narratives": [
    {
      "name": "groups-under-a-cap-pitch",
      "status": "done",
      "kind": "architecture",
      "timeframe": "future",
      "tells_edge": true,
      "paragraphs": [
        {
          "line": 12,
          "paragraph": "- [[groups-clustered-under-a-cap|The vault holds groups]], and [[cap-setting|an instance setting]] caps their number.\n- The cap is set for each vault, in the vault's own configuration. The example vault sets it to 3.\n- A group is named by its role. No group stands for one identifiable person.\n- Reason given in the record: the people in the data are groups under the Chatham House rule, so [[anonymity|no individual is identifiable]].",
          "sentences": [
            {
              "text": "Reason given in the record: the people in the data are groups under the Chatham House rule, so [[anonymity|no individual is identifiable]].",
              "start": 296,
              "end": 435
            }
          ]
        }
      ]
    },
    {
      "name": "notes-at-a-chatham-house-session",
      "status": "done",
      "kind": "scenario",
      "timeframe": "mixed",
      "tells_edge": true,
      "paragraphs": [
        {
          "line": 12,
          "paragraph": "- [[workshop-participants|Workshop participants]] tell stories in conversations. The work is sized for manual note-taking in Obsidian.\n- [[facilitator-analysts|Facilitators]] take the field notes. The setting is Chatham House rule: the people in the data are groups, so [[anonymity|no individual is identifiable]].\n- The vault holds groups, and [[groups-clustered-under-a-cap|an instance setting caps their number]].\n- This vault runs in the disallowed attribution mode: the notes name groups, never individuals, and no note links to a person. A project that needs names chooses another mode when it sets up.\n- [[attribution|Attribution]] and [[anonymity]] conflict as concerns, and the vault records that as a remark on one of them.",
          "sentences": [
            {
              "text": "The setting is Chatham House rule: the people in the data are groups, so [[anonymity|no individual is identifiable]].",
              "start": 197,
              "end": 314
            },
            {
              "text": "[[attribution|Attribution]] and [[anonymity]] conflict as concerns, and the vault records that as a remark on one of them.",
              "start": 611,
              "end": 733
            }
          ]
        }
      ]
    }
  ],
  "edges": [
    {
      "type": "holds",
      "from": "facilitator-analysts",
      "to": "anonymity",
      "narratives": [
        "notes-at-a-chatham-house-session"
      ],
      "status": "done",
      "tellings": [
        {
          "narrative": "notes-at-a-chatham-house-session",
          "note": "They take the field notes under the Chatham House rule, so no individual is identifiable (D-010)."
        }
      ]
    },
    {
      "type": "addressed-by",
      "from": "anonymity",
      "to": "groups-clustered-under-a-cap",
      "narratives": [
        "groups-under-a-cap-pitch",
        "notes-at-a-chatham-house-session"
      ],
      "status": "done",
      "tellings": [
        {
          "narrative": "groups-under-a-cap-pitch",
          "note": "Participants appear only as groups, so no group stands for one identifiable person."
        },
        {
          "narrative": "notes-at-a-chatham-house-session",
          "note": "The mission says the people in the data are groups under the Chatham House rule, so no individual is identifiable."
        }
      ]
    }
  ],
  "adjacent": {
    "group": [
      {
        "name": "facilitator-analysts",
        "type": "group",
        "status": "done"
      }
    ],
    "concern": [],
    "affordance": [
      {
        "name": "groups-clustered-under-a-cap",
        "type": "affordance",
        "status": "done"
      }
    ],
    "technology": []
  },
  "excluded": [
    {
      "name": "desk-notes-one",
      "file": "narrative/desk-notes-one.md",
      "fix": "link one node page in the narrative (a row end or its account), then run this again"
    },
    {
      "name": "desk-notes-two",
      "file": "narrative/desk-notes-two.md",
      "fix": "link one node page in the narrative (a row end or its account), then run this again"
    }
  ]
}
```

In the document, `paragraphs[].line` is the file line of the paragraph's first line, and each sentence has `start` and `end`, 0-based character offsets in `paragraph` (`end` not included), so that `paragraph[start:end]` is the sentence.

## scat attribution

```text
usage: scat attribution [-h] [--root ROOT] [--json]

Show the narratives by contributor: each contributor page with the narratives that name it, and the narratives that name none. Refuses where the vault's attribution mode is disallowed. Writes nothing.

options:
  -h, --help   show this help message and exit
  --root ROOT  the vault folder, the one with scat.toml (default: here)
  --json       print the result as one JSON document (machine-interface
               contract), nothing else

REPL: `scat_kg.attribution()`
```

Lists each contributor page with the narratives whose `attributed_to` field names it, and then the narratives that name nobody. It is a view of the knowledge graph, not of the layered graph: a contributor page has no edge and appears in no other view. It writes nothing.

Where the vault's attribution mode is `disallowed`, no narrative names anyone and no contributor page may exist, so the command refuses and says so; it does not print an empty list. It refuses too when `scat.toml` declares no usable mode, and, like the other views, when a page it draws has an error.

Exit codes: 0, or 1 for a refusal.

The examples below are for a vault whose mode is `optional`, with two contributor pages.

=== "Python"

    ```python
    scat_kg.attribution()
    ```

    ```text
    attribution: narratives by contributor
      ada-quill [done]
        funders-meeting
        saturday-at-the-lending-desk
      bo-marsh [stub]
        saturday-at-the-lending-desk
      narratives that name no contributor
        self-service-kiosk-pitch
    ```

=== "CLI"

    ```text
    $ uv run scat attribution
    ```

    ```text
    attribution: narratives by contributor
      ada-quill [done]
        funders-meeting
        saturday-at-the-lending-desk
      bo-marsh [stub]
        saturday-at-the-lending-desk
      narratives that name no contributor
        self-service-kiosk-pitch
    ```

In a vault whose mode is `disallowed`:

```text
$ uv run scat attribution
refused scat.toml field `attribution`: this vault's attribution mode is `disallowed`, so it allows no attribution: no narrative names a contributor and there is no contributor page to list
  Fix: the coder who wants contributors named changes `attribution` in scat.toml for the whole vault
```

With `--json`:

```text
$ uv run scat attribution --json
```

```json
{
  "schema_version": 3,
  "kind": "view",
  "operation": "attribution",
  "ok": true,
  "mode": "optional",
  "contributors": [
    {
      "name": "ada-quill",
      "title": "Ada Quill",
      "status": "done",
      "narratives": [
        "funders-meeting",
        "saturday-at-the-lending-desk"
      ]
    },
    {
      "name": "bo-marsh",
      "title": "Bo Marsh",
      "status": "stub",
      "narratives": [
        "saturday-at-the-lending-desk"
      ]
    }
  ],
  "unattributed": [
    "self-service-kiosk-pitch"
  ],
  "excluded": []
}
```

## scat export-edges

```text
usage: scat export-edges [-h] [--root ROOT] [--json] --out DIR

Write each edge table to DIR as `<type>.csv` and `<type>.md`. Overwrites a file only when its content differs; makes DIR if it is not there. Refuses where `scat edges` would, and then writes nothing.

options:
  -h, --help   show this help message and exit
  --root ROOT  the vault folder, the one with scat.toml (default: here)
  --json       print the result as one JSON document (machine-interface
               contract), nothing else
  --out DIR    the folder the tables go in (no default)

REPL: `scat_kg.export_edges("<dir>")`
```

Writes the three edge tables, one CSV and one Markdown file each, into `DIR`. The CSV file has the columns `from`, `to`, `narratives` (joined by `;`) and `status`. The Markdown file is a generated heading, one sentence and a table. Names are plain text, so the files add no page, link or row to a vault, even when `DIR` is inside it. Of the six commands here, it and `scat draw` are the only ones that write.

A file that is there is rewritten only when its content differs, so running it again changes nothing. It refuses, writing nothing, where `scat edges` would, and when `DIR` is a file. Paths inside the vault folder are shown from it; a folder outside it is shown as you gave it.

Exit codes: 0, or 1 for a refusal.

=== "Python"

    ```python
    scat_kg.export_edges("tables")
    ```

    ```text
    created tables/holds.csv
    created tables/holds.md
    created tables/addressed-by.csv
    created tables/addressed-by.md
    created tables/provided-by.csv
    created tables/provided-by.md
    ```

=== "CLI"

    ```bash
    uv run scat export-edges --out edge-tables
    ```

    ```text
    created edge-tables/holds.csv
    created edge-tables/holds.md
    created edge-tables/addressed-by.csv
    created edge-tables/addressed-by.md
    created edge-tables/provided-by.csv
    created edge-tables/provided-by.md
    ```

With `--json`, a second time:

```text
$ uv run scat export-edges --out edge-tables --json
```

```json
{
  "schema_version": 3,
  "kind": "operation",
  "operation": "export-edges",
  "ok": true,
  "mode": "disallowed",
  "created": [],
  "changed": [],
  "unchanged": [
    "edge-tables/holds.csv",
    "edge-tables/holds.md",
    "edge-tables/addressed-by.csv",
    "edge-tables/addressed-by.md",
    "edge-tables/provided-by.csv",
    "edge-tables/provided-by.md"
  ],
  "refused": [],
  "notes": []
}
```

## scat draw

```text
usage: scat draw [-h] <drawing> ...

Draw a view as an image, four columns in layer order. Needs the extra `draw`: `pip install "scat-kg[draw]"`. The only write is the image file you name with --out.

positional arguments:
  <drawing>
    fingerprint  Draw a narrative's fingerprint: its nodes and edges in four
                 columns; with --candidates, the links that have no row
                 dashed. Refuses where `scat fingerprint` would, and then
                 writes nothing.
    layered      Draw the layered view of the narratives named by --narrative
                 or, without it, of every narrative. Refuses where `scat
                 layered` would, and then writes nothing.

options:
  -h, --help     show this help message and exit

REPL: `from scat_kg import draw`, then `draw.fingerprint(...)` or `draw.layered(...)`
```

Draws a view as an image in four columns, one for each layer, in layer order, with the layer's name at the top. Each node is a box labelled with its name, and with its status in brackets when that is not `done`; each edge is a line between neighbouring columns. Within a column the nodes are in order of name. `scat draw fingerprint` draws one narrative's fingerprint and shows no candidates unless you add `--candidates`, which draws the links with no row as dashed lines. `scat draw layered` draws the layered view of the narratives you name with `--narrative`, or of every narrative.

Drawing needs the extra `draw`: `pip install "scat-kg[draw]"`. Without it, the command refuses and says so. The same command gives the same image, byte for byte.

`--out FILE` is required. A file ending in `.png` or `.svg` is written, and any other ending is refused. A file that is there is rewritten only when its content differs. It is the only thing `scat draw` writes. It refuses, writing nothing, where `scat fingerprint` or `scat layered` would. Paths inside the vault folder are shown from it; a file outside it is shown as you gave it.

Exit codes: 0, or 1 for a refusal.

### scat draw fingerprint

```text
usage: scat draw fingerprint [-h] [--root ROOT] [--json] [--candidates] --out
                             FILE
                             NARRATIVE

Draw a narrative's fingerprint: its nodes and edges in four columns; with --candidates, the links that have no row dashed. Refuses where `scat fingerprint` would, and then writes nothing.

positional arguments:
  NARRATIVE     the narrative's name

options:
  -h, --help    show this help message and exit
  --root ROOT   the vault folder, the one with scat.toml (default: here)
  --json        print the result as one JSON document (machine-interface
                contract), nothing else
  --candidates  also draw the candidates: links with no row, dashed
  --out FILE    the image file to write, ending in `.png` or `.svg` (no
                default)

REPL: `draw.fingerprint("<narrative>", candidates=True).save("<file>")`
```

### scat draw layered

```text
usage: scat draw layered [-h] [--root ROOT] [--json] [--narrative NARRATIVE]
                         --out FILE

Draw the layered view of the narratives named by --narrative or, without it, of every narrative. Refuses where `scat layered` would, and then writes nothing.

options:
  -h, --help            show this help message and exit
  --root ROOT           the vault folder, the one with scat.toml (default:
                        here)
  --json                print the result as one JSON document (machine-
                        interface contract), nothing else
  --narrative NARRATIVE
                        include this narrative; repeat it for each narrative
  --out FILE            the image file to write, ending in `.png` or `.svg`
                        (no default)

REPL: `draw.layered().save("<file>")`, `draw.layered(["<narrative>"]).save("<file>")`
```

=== "Python"

    ```python
    from scat_kg import draw

    draw.layered().save("layered.png")
    ```

    ```text
    created layered.png
    ```

=== "CLI"

    ```bash
    uv run scat draw layered --out layered.png
    ```

    ```text
    created layered.png
    ```

## Where next

Keep the reference close:

- [Python API reference](api.md): every operation, with its parameters and what it returns.
- [Coding guide](../coding.md): how to use these commands while you code your notes.
- [Home](../index.md)
