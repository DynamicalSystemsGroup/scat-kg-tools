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
| [`scat_kg.merge`](#scat_kgmerge) | [`scat merge`](cli.md#scat-merge) | Fold node page A into node page B of the same type; `plan=True` shows it and writes nothing. |
| [`scat_kg.split_plan`](#scat_kgsplit_plan) | [`scat split-plan`](cli.md#scat-split-plan) | Show what must be re-linked to split a node page. Writes nothing. |
| [`scat_kg.stub_links`](#scat_kgstub_links) | [`scat stub-links`](cli.md#scat-stub-links) | Create the node pages that the ends of rows link and the vault lacks. |
| [`scat_kg.set_status`](#scat_kgset_status) | [`scat set-status`](cli.md#scat-set-status) | Set a page's status. |
| [`scat_kg.load`](#scat_kgload) | none | Read the vault into its knowledge graph. Writes nothing. |
| [`scat_kg.fingerprint`](#scat_kgfingerprint) | [`scat fingerprint`](cli.md#scat-fingerprint) | View: a narrative's nodes and edges (candidates when asked). |
| [`scat_kg.edge_table`](#scat_kgedge_table) | [`scat edges`](cli.md#scat-edges) | View: every edge of one type. |
| [`scat_kg.layered`](#scat_kglayered) | [`scat layered`](cli.md#scat-layered) | View: the union of fingerprints, in four layers. |
| [`scat_kg.trace`](#scat_kgtrace) | [`scat trace`](cli.md#scat-trace) | View: what a node reaches, up or down the layers. |
| [`scat_kg.evidence`](#scat_kgevidence) | [`scat evidence`](cli.md#scat-evidence) | View: one node's narratives with the paragraph around each link, its edges and its adjacent nodes. |
| [`scat_kg.copy_share`](#scat_kgcopy_share) | [`scat copy-share`](cli.md#scat-copy-share) | View: for each node page, the share of its text that repeats a narrative word for word. |
| [`scat_kg.review`](#scat_kgreview) | [`scat review`](cli.md#scat-review) | View: pairs of node pages that may be one node, and pages whose accounts tell them to different other ends. |
| [`scat_kg.attribution`](#scat_kgattribution) | [`scat attribution`](cli.md#scat-attribution) | View: the narratives by contributor (where the vault's attribution mode allows it). |
| [`scat_kg.export_edges`](#scat_kgexport_edges) | [`scat export-edges`](cli.md#scat-export-edges) | Write the edge tables as CSV and Markdown. |
| [`scat_kg.guide`](#scat_kgguide) | [`scat guide`](cli.md#scat-guide) | Show the guide of a lifecycle stage, or the index of the stages. Needs no vault. |
| [`scat_kg.draw.render`](#scat_kgdrawrender), [`scat_kg.draw.fingerprint`](#scat_kgdrawfingerprint), [`scat_kg.draw.layered`](#scat_kgdrawlayered), [`scat_kg.draw.trace`](#scat_kgdrawtrace) | [`scat draw`](cli.md#scat-draw) | Draw a view, or a view's result, as an image (needs the extra `draw`). |

## Machine-readable output

`result.to_dict()` returns the data of the result as plain Python: the same document that the matching `scat` command prints with `--json` (see the [CLI reference](cli.md#machine-readable-output)). `--json` prints exactly one JSON document and nothing else, and the exit code does not change. Print it with `json.dumps(result.to_dict(), indent=2)`. The fields, and the rule for when `schema_version` changes (it is 3), are in the [machine interface contract](https://github.com/DynamicalSystemsGroup/scat-kg-tools/blob/dev/contracts/machine-interface.md).

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

It prints one block per problem, then a count line: `<n> errors, <n> warnings`. It starts with the vault's attribution mode (`attribution mode: disallowed`). With no problems it then prints `no problems`. Errors block, warnings do not. A rule id such as `SCAT-DONE-END-NOPAGE` names the rule; the `Fix:` line says what to do. Asking for `neighborhood=True` without a page, or for a page that is not there, returns a refusal.

The whole vault, and a page and every page one link away:

=== "Python"

    ```python
    import scat_kg

    scat_kg.check()
    scat_kg.check("anonymity", neighborhood=True)
    ```

    ```text
    attribution mode: disallowed
    no problems
    attribution mode: disallowed
    no problems
    ```

=== "CLI"

    ```bash
    uv run scat check
    uv run scat check anonymity --neighborhood
    ```

    ```text
    attribution mode: disallowed
    no problems
    attribution mode: disallowed
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
    attribution mode: disallowed
    no problems
    attribution mode: disallowed
    no problems
    ```

=== "CLI"

    ```bash
    uv run scat check anonymity
    uv run scat check concern/anonymity.md
    ```

    ```text
    attribution mode: disallowed
    no problems
    attribution mode: disallowed
    no problems
    ```

As data, on the unchanged template (`import json` first):

```text
>>> print(json.dumps(scat_kg.check().to_dict(), indent=2))
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

To see a problem with a fix a program can apply, change `[[cap-setting]]` to `[[cap-settin]]` in the second row of the table of `narrative/groups-under-a-cap-pitch.md` (line 22), a one-letter typo in a link. The fix has three options: a `replace-text` edit that writes the right name, a `command` that creates the missing page, and a `delete-line` edit.

```text
>>> print(json.dumps(scat_kg.check().to_dict(), indent=2))
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
                "find": "| [[groups-clustered-under-a-cap]] | is provided by | [[cap-settin]] | The cap setting is what fixes the number of groups. The cap is a per-instance parameter; the example vault sets it to 6. |"
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
  "schema_version": 3,
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
  "schema_version": 3,
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
  "schema_version": 3,
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

As data:

```text
>>> print(json.dumps(scat_kg.record_edge("addressed-by", "reading-group", "reading-shelf", ["desk-notes-one"]).to_dict(), indent=2))
```

```json
{
  "schema_version": 3,
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
    "added `| [[reading-group]] | is addressed by | [[reading-shelf]] | |` to narrative/desk-notes-one.md at line 13"
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
  "schema_version": 3,
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

## scat_kg.merge

```text
merge(a, b, *, plan=False, root=".")
```

Folds node page `a` into node page `b`, two pages of one type: every link to `a` in the narratives and node pages becomes a link to `b`, `a`'s body is added to `b` under `## From a`, `a`'s description is dropped (`b` keeps its own, with its status and other fields), and `a`'s page is removed. `a` is folded into `b`, never the other way round. CLI twin: [`scat merge`](cli.md#scat-merge).

| Parameter | Meaning |
|---|---|
| `a` | The name of the node page that is folded in, and removed. |
| `b` | The name of the node page that stays. |
| `plan` | `True` shows what the merge would do and writes nothing. The default applies it. |
| `root` | The vault folder. |

The whole result is built in a temporary copy of the vault first, and written only when the copy passes the check with no new error, holds no link to `a`, and gives the graph the vault had, with `a` renamed `b`. A narrative that is `done` stays `done`; `done_narratives` lists each one whose text changed. It refuses, and writes nothing, for a pair of different types, a page that is not a node page, a contributor page whose body links `a` (a merge never writes a contributor page), an error in a page it reads, and a narrative that would end with two rows for one edge (both rows are listed). The [CLI reference](cli.md#scat-merge) says how each kind of link is rewritten.

=== "Python"

    ```python
    scat_kg.merge("project-leads", "workshop-participants", plan=True)
    ```

    ```text
    merge plan: `project-leads` is folded into `workshop-participants`; nothing is written
      3 links to `project-leads` would be rewritten
    would change narrative/false-start-and-clean-restart.md (2 links)
    would change narrative/two-branches-and-tags-pitch.md (1 link)
    would remove group/project-leads.md
    would change 2 `done` narratives (they stay `done`): false-start-and-clean-restart, two-branches-and-tags-pitch
    note: `project-leads` has no body, so nothing is appended to `workshop-participants`
    note: the description of `project-leads` is dropped; `workshop-participants` keeps its own, and its status (`done`) and other fields are unchanged
    note: a `done` narrative whose text changes stays `done`: read it again before you rely on it
    ```

=== "CLI"

    ```bash
    uv run scat merge --plan project-leads workshop-participants
    ```

    The same text.

`result.to_dict()` is the document the command prints with `--json`; its `plan`, `removed`, `done_narratives` and `links_rewritten` fields are in the [CLI reference](cli.md#scat-merge). A refusal prints what to do next, and nothing is written:

```python
scat_kg.merge("project-leads", "gated-approval", plan=True)
```

```text
refused project-leads and gated-approval: `project-leads` is a group and `gated-approval` is an affordance: a merge needs two pages of one type
  Fix: name two node pages of one type (group, concern, affordance, technology): `scat merge A B` folds A into B
```

## scat_kg.split_plan

```text
split_plan(a, *, root=".")
```

Shows what must be re-linked to split node page `a` in two. It writes nothing. For each narrative (or node page) that links `a` it lists every link and every `Edges told` row that names `a`; you assign each narrative to `a` or to a new page and edit by hand. A contributor page is never listed. CLI twin: [`scat split-plan`](cli.md#scat-split-plan).

| Parameter | Meaning |
|---|---|
| `a` | The name of the node page to split. |
| `root` | The vault folder. |

The returned plan has `node`, `node_type` and `pages` (each with `file`, `name`, `type`, `status`, `links` and `rows`). It refuses a name that is no page, a page that is not a node page, and an error in a page it reads.

=== "Python"

    ```python
    scat_kg.split_plan("project-leads")
    ```

    ```text
    split plan for `project-leads` (group): 2 pages, 3 links, 1 row to re-link; nothing is written
      narrative/false-start-and-clean-restart.md (narrative, done): links at line 13, 28
        row 1, line 28: | [[project-leads]] | holds | [[intent-without-drift]] | The project leads hold these as the concerns of the false-start story. |
      narrative/two-branches-and-tags-pitch.md (narrative, done): links at line 13
    note: you assign each narrative to `project-leads` or to a new page: make the new page with `scat stub <name> --type group`, then edit each link and row by hand
    note: narratives that are `done` are yours to reopen before you edit them: false-start-and-clean-restart, two-branches-and-tags-pitch
    note: the vault allows 6 groups and has 3; a new group page makes 4
    ```

=== "CLI"

    ```bash
    uv run scat split-plan project-leads
    ```

    The same text.

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
  "schema_version": 3,
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
      1. replace the line `timeframe:` with `timeframe: past` (author)
      2. replace the line `timeframe:` with `timeframe: future` (author)
      3. replace the line `timeframe:` with `timeframe: mixed` (author)
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
  "schema_version": 3,
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
  "schema_version": 3,
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

## scat_kg.load

```text
load(root=".")
```

Reads the vault into its knowledge graph and returns a `Graph`. It writes nothing and does not check: the views and the other calls check for themselves.

| Parameter | Meaning |
|---|---|
| `root` | The vault folder. |

A `Graph` holds `nodes` (by layer, in layer order), `edges`, `narratives` (the coded ones), `excluded` (the uncoded ones, left out), `candidates` and `links`. `graph.summary()` counts them. A vault folder that is not there does not raise: `graph.ok` is `False` and `graph.refusal` says what to do. It has no CLI twin: every `scat` command reads the same graph.

```python
scat_kg.load().summary()
```

```text
{'nodes': {'group': 3, 'concern': 5, 'affordance': 3, 'technology': 3}, 'narratives': 6, 'excluded': 0, 'edges': 8, 'edge_status': {'stub': 0, 'draft': 0, 'done': 8}, 'candidates': 7, 'links': 43}
```

## Views

A view is a purposeful picture or table made from a conformant vault, and the calls below make the views. Each returns a `View`, or a refusal. Each takes `root=`, writes nothing, and gives the same output for the same vault.

- `str(view)` is a short text, one line per node or edge. At the REPL the view prints as that text.
- `view.ok` is `True`. `view.to_dict()` is the document.
- A view refuses, with the problems and their fixes, on a name that is not there or is ambiguous, an edge type or direction that does not exist, a vault folder that is missing, any error in the pages it draws, and a row of a narrative it draws that tells no edge (the file and the row are named; the edge table and the trace draw every narrative). Warnings do not refuse. A narrative that links no node page is excluded: left out of every view, listed under `excluded` (name, file and how to include it) by each view that draws every narrative, and refused when you name it. Relationship annotations appear in no view.

The document has `kind` `view` and an `operation` of `fingerprint`, `edges`, `layered`, `trace`, `evidence`, `copy-share`, `review` or `attribution`. This is an excerpt of `scat_kg.edge_table("holds").to_dict()`; the full documents are in the [CLI reference](cli.md#scat-fingerprint) and the [machine interface contract](https://github.com/DynamicalSystemsGroup/scat-kg-tools/blob/dev/contracts/machine-interface.md):

```text
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
      "narratives": ["notes-at-a-chatham-house-session"],
      "status": "done"
    }
  ],
  "excluded": []
}
```

## scat_kg.fingerprint

```text
fingerprint(narrative=None, *, candidates=False, root=".")
```

Shows the fingerprint of a narrative: the nodes it links, the edges its rows tell, and, with `candidates=True`, its candidates (links between two nodes that an edge type fits and that have no row; without the option the view shows none). CLI twin: [`scat fingerprint`](cli.md#scat-fingerprint).

| Parameter | Meaning |
|---|---|
| `narrative` | A narrative name. Without it, every narrative, in path order. |
| `candidates` | `True` to add the candidates. Default `False`. CLI: `--candidates`. |
| `root` | The vault folder. |

It refuses when the name is not a narrative, when two pages share it, and on an error in a page it draws. With `candidates=True`, a narrative whose account text is empty (its body outside its `Edges told` section, headings aside) carries `no_account: true`: its only links are its rows, so every adjacent pair is a candidate and the candidates say nothing about any text. The text form says so on a line.

=== "Python"

    ```python
    scat_kg.fingerprint("groups-under-a-cap-pitch")
    ```

    ```text
    fingerprint groups-under-a-cap-pitch (architecture, done)
      concern
        anonymity [done]
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

    The same text.

## scat_kg.edge_table

```text
edge_table(type, *, root=".")
```

Shows every edge of one type, in graph order, with the narratives that tell it and its status. CLI twin: [`scat edges`](cli.md#scat-edges).

| Parameter | Meaning |
|---|---|
| `type` | `holds`, `addressed-by` or `provided-by`. |
| `root` | The vault folder. |

It refuses on any other type, and on an error in a page it draws.

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

    The same text.

## scat_kg.layered

```text
layered(narratives=None, *, candidates=False, root=".")
```

Shows the layered view: the union of the fingerprints of the narratives you name, as four layers. Without `narratives`, every narrative. CLI twin: [`scat layered`](cli.md#scat-layered), with one `--narrative` for each name.

| Parameter | Meaning |
|---|---|
| `narratives` | A list of narrative names. |
| `candidates` | `True` to add the candidates. Default `False`. CLI: `--candidates`. |
| `root` | The vault folder. |

The result also carries `orphans` when there are any: each node page that is an end of no edge anywhere in the vault (the whole vault, whichever narratives you name), with its name, type and status. With `candidates=True` it carries `candidates`, each `{type, from, to, narrative}` for the chosen narratives, and `no_account`, the names of the chosen narratives whose account text is empty (their body outside the `Edges told` section, headings aside). A narrative with no account has only its rows as links, so every adjacent pair of its nodes is a candidate and its candidates say nothing about any text. The text form lists the candidates, the narratives with no account and the orphans.

It refuses on a name that is not a narrative, on a value that is not a list of names, on a `candidates` that is not `True` or `False`, and on an error in a page it draws.

=== "Python"

    ```python
    scat_kg.layered(["groups-under-a-cap-pitch"])
    ```

    ```text
    layered view of groups-under-a-cap-pitch
      concern
        anonymity [done]
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

    The same text.

## scat_kg.trace

```text
trace(node, direction="both", *, root=".")
```

Follows edges from a node: `up` toward the groups, `down` toward the technologies, or `both`. The node itself is left out. CLI twin: [`scat trace`](cli.md#scat-trace), with `--direction`.

| Parameter | Meaning |
|---|---|
| `node` | The name of a group, concern, affordance or technology. |
| `direction` | `up`, `down` or `both`. |
| `root` | The vault folder. |

It refuses when the name is not a node, when the direction is not one of the three, and on an error in a page it draws.

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

    The same text.

A refusal prints what to do next, and nothing is written:

```python
scat_kg.trace("anonymity", "sideways")
```

```text
refused sideways: this is not a direction
  Fix: use one of: up, down, both
```

## scat_kg.evidence

```text
evidence(node, *, root=".")
```

Returns everything the vault says of one node page: the narratives that link it, each with the whole paragraph around every link and the sentence that holds the link marked (`start` and `end` are offsets in the paragraph); the narratives that link it and tell no edge for it, flagged (`tells_edge` is `False`); its edges, each with the narratives that tell it and the row's note; and its adjacent nodes by layer. CLI twin: [`scat evidence`](cli.md#scat-evidence).

| Parameter | Meaning |
|---|---|
| `node` | The name of a group, concern, affordance or technology. |
| `root` | The vault folder. |

`str(view)` begins with the vault's attribution mode and puts the marked sentence between `>>` and `<<`. A link inside the `Edges told` table is not a paragraph: it shows through the edges. The view reads no `attributed_to` field and lists no contributor page. It refuses when the name is not a node page (a narrative, a contributor page, or no page), when two pages carry the name, and on an error in a page it draws.

=== "Python"

    ```python
    scat_kg.evidence("anonymity")
    ```

    ```text
    attribution mode: disallowed
    evidence anonymity (concern, done): 2 narratives, 2 edges
      narratives (the sentence with the link is between >> and <<)
        groups-under-a-cap-pitch [done, architecture, future]
          line 12
            - [[groups-clustered-under-a-cap|The vault holds groups]], and [[cap-setting|an instance setting]] caps their number.
            - The cap is set for each vault, in the vault's own configuration. The example vault sets it to 6.
            - A group is named by its role. No group stands for one identifiable person.
            - >>Reason given: the people in the data are groups under the Chatham House rule, so [[anonymity|no individual is identifiable]].<<
        notes-at-a-chatham-house-session [done, scenario, mixed]
          line 12
            - [[workshop-participants|Workshop participants]] tell stories in conversations. The work is sized for manual note-taking in Obsidian.
            - [[facilitator-analysts|Facilitators]] take the field notes. >>The setting is Chatham House rule: the people in the data are groups, so [[anonymity|no individual is identifiable]].<<
            - The vault holds groups, and [[groups-clustered-under-a-cap|an instance setting caps their number]].
            - This vault runs in the disallowed attribution mode: the notes name groups, never individuals, and no note links to a person. A project that needs names chooses another mode when it sets up.
            - >>[[attribution|Attribution]] and [[anonymity]] conflict as concerns, and the vault records that as a remark on one of them.<<
      edges
        holds: facilitator-analysts -> anonymity [done; told by notes-at-a-chatham-house-session]
            notes-at-a-chatham-house-session: They take the field notes under the Chatham House rule, so no individual is identifiable.
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

`view.to_dict()` is the document, the one `scat evidence anonymity --json` prints; see the [CLI reference](cli.md#scat-evidence) for all of it. A refusal prints what to do next, and nothing is written:

```python
scat_kg.evidence("nobody")
```

```text
refused nobody: no node has this name
  Fix: give the name of a page (the file name without `.md`) that is a group, concern, affordance or technology
```

## scat_kg.copy_share

```text
copy_share(node=None, *, root=".")
```

Returns, for each node page (or the one named), the share of its five-word runs that appear word for word in a narrative, from 0 to 1, and the narratives those runs come from, the one with most runs first. The narratives named are those whose text the page repeats, whether or not they link the node. The pages come most repeated first. A page of fewer than five words, such as a stub, has a share of `None`. A high share is a prompt to look at the page (see [`scat_kg.evidence`](#scat_kgevidence)), not a fault. CLI twin: [`scat copy-share`](cli.md#scat-copy-share).

| Parameter | Meaning |
|---|---|
| `node` | The name of a group, concern, affordance or technology; without it, every node page. |
| `root` | The vault folder. |

The page's text is its `description` and its body, without an `Edges told` section; a narrative's text is its body. Case, punctuation and line breaks count for nothing, and a link counts as the text it shows. A narrative that links no node page is excluded: its text is not compared, and it is listed under `excluded`. `str(view)` begins with the vault's attribution mode. The view reads no `attributed_to` field and lists no contributor page. It refuses when the name is not a node page (a narrative, a contributor page, or no page), when two pages carry the name, and on an error in a page it draws.

=== "Python"

    ```python
    scat_kg.copy_share("gated-approval")
    ```

    ```text
    attribution mode: disallowed
    copy-share: 1 node page
        gated-approval (affordance, done): 15 words, share 0.18; from two-branches-and-tags-pitch
    excluded (no node page linked; link one node page to include it)
        desk-notes-one (narrative/desk-notes-one.md)
        desk-notes-two (narrative/desk-notes-two.md)
    ```

=== "CLI"

    ```bash
    uv run scat copy-share gated-approval
    ```

    The same text.

`view.to_dict()` is the document, the one `scat copy-share gated-approval --json` prints; see the [CLI reference](cli.md#scat-copy-share) for all of it. A refusal prints what to do next, and nothing is written:

```python
scat_kg.copy_share("nobody")
```

```text
refused nobody: no node has this name
  Fix: give the name of a page (the file name without `.md`) that is a group, concern, affordance or technology
```

## scat_kg.review

```text
review(*, root=".")
```

Returns two lists to read from, never findings. `proposals` holds pairs of node pages of one type that may be one node: their adjacent nodes overlap by at least half (two or more each), or their descriptions share at least half of their words, or a narrative tells the same row for both and at least half of their narratives are shared. Each pair carries the three overlaps, the twin rows with the line of each, the shared adjacent nodes with the hubs marked, a one-line `reason`, and the link texts coders gave each page; names are never compared and link text is never scored. `reread` holds pages whose edges are told by four or more narratives that mostly tell them to different other ends, with the narratives grouped. CLI twin: [`scat review`](cli.md#scat-review), which describes both lists.

| Parameter | Meaning |
|---|---|
| `root` | The vault folder. |

A narrative that links no node page is excluded: it is listed under `excluded` and not used. `str(view)` begins with the vault's attribution mode. The view reads no `attributed_to` field and lists no contributor page. It refuses on an error in a page it draws, on a row that tells no edge, and when the vault folder is missing.

=== "Python"

    ```python
    scat_kg.review()
    ```

    ```text
    attribution mode: disallowed
    review: 1 page pair that may be one node
        gated-approval ~ revert-with-history-kept (affordance; done, done): may be one node: a narrative tells the same row for both (2x)
            narratives 1.00, adjacent nodes 0.33, descriptions 0.00
            twin row: false-start-and-clean-restart (narrative/false-start-and-clean-restart.md lines 29 and 30) tells addressed-by with intent-without-drift
            twin row: two-branches-and-tags-pitch (narrative/two-branches-and-tags-pitch.md lines 26 and 27) tells addressed-by with intent-without-drift
            shared adjacent nodes: intent-without-drift
            link texts for gated-approval: "Approval is a merge into main", "a gated mission"
            link texts for revert-with-history-kept: "dev is reverted to the approved state. History is kept", "reverting without losing history"
    pages to re-read: 0
        none
    ```

=== "CLI"

    ```bash
    uv run scat review
    ```

    The same text.

`view.to_dict()` is the document, the one `scat review --json` prints; see the [CLI reference](cli.md#scat-review) for all of it.

## scat_kg.attribution

```text
attribution(*, root=".")
```

Shows each contributor page with the narratives whose `attributed_to` field names it, then the narratives that name none. A contributor page is in the knowledge graph but in no layered view, so no other view shows one. CLI twin: [`scat attribution`](cli.md#scat-attribution).

| Parameter | Meaning |
|---|---|
| `root` | The vault folder. |

It refuses in a vault whose attribution mode is `disallowed`, where no narrative names a contributor and there is no contributor page to list. It refuses too on an error in a page it draws. The template's mode is `disallowed`, so on a fresh copy it refuses:

=== "Python"

    ```python
    scat_kg.attribution()
    ```

    ```text
    refused scat.toml field `attribution`: this vault's attribution mode is `disallowed`, so it allows no attribution: no narrative names a contributor and there is no contributor page to list
      Fix: the coder who wants contributors named changes `attribution` in scat.toml for the whole vault
    ```

=== "CLI"

    ```text
    $ uv run scat attribution
    refused scat.toml field `attribution`: this vault's attribution mode is `disallowed`, so it allows no attribution: no narrative names a contributor and there is no contributor page to list
      Fix: the coder who wants contributors named changes `attribution` in scat.toml for the whole vault
    ```

    The command exits with 1, as every refusal does.

Take a copy of the template with `attribution = "optional"` in `scat.toml`, and the coding guide's `saturday-at-the-tool-library` narrative with `attributed_to: ["[[ada-quill]]"]`, and `ada-quill` made with `scat stub ada-quill --type contributor`. The view prints, with the template's four narratives naming no one:

```text
attribution: narratives by contributor
  ada-quill [stub]
    saturday-at-the-tool-library
  narratives that name no contributor
    false-start-and-clean-restart
    groups-under-a-cap-pitch
    notes-at-a-chatham-house-session
    two-branches-and-tags-pitch
```

## scat_kg.export_edges

```text
export_edges(out, *, root=".")
```

Writes each edge table to `<out>/<type>.csv` and `<out>/<type>.md`, and returns a `Result`. `out` is required. CLI twin: [`scat export-edges --out`](cli.md#scat-export-edges).

| Parameter | Meaning |
|---|---|
| `out` | The folder to write in; made if it is not there. |
| `root` | The vault folder. |

The CSV has the columns `from`, `to`, `narratives` (joined by `;`) and `status`. A file that is there is rewritten only when its content differs, so a second call prints `unchanged`. It refuses where `edge_table` would, and when `out` is a file; it then writes nothing.

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

    The same lines, with `edge-tables/` in place of `tables/`.

## scat_kg.guide

```text
guide(stage=None)
```

Returns the guide of one stage of the project's lifecycle (`"plan"`, `"capture"`, `"code"`, `"analyse"` or `"report"`). With no `stage`, or `"index"`, it returns the index: the five stages and the moves between them. It needs no vault and has no `root`. A stage is where the project is; it is not a page's status. CLI twin: [`scat guide`](cli.md#scat-guide).

| Parameter | Meaning |
|---|---|
| `stage` | The stage's name, or `"index"`. Without it, the index. |

`str(result)` is the text `scat guide` prints, and the result prints as that text. Besides `ok` (always `True` for a stage or the index), it holds `stage`, `text`, `docs` (the stage's docs page, or `None` for the index), `tools` (the stage's tools) and `exits` (the ids of its moves). A name that is not a stage returns a `Result` that is a refusal naming the five stages, with `ok` set to `False`.

=== "Python"

    ```python
    scat_kg.guide("analyse")
    scat_kg.guide("analyse").tools
    scat_kg.guide("ideation").ok
    ```

=== "CLI"

    ```bash
    uv run scat guide analyse
    ```

    The first line prints the guide. The other two lines give the stage's tools, and `False`.

## Drawings

A drawing shows a view as columns, one for each layer, in layer order, with the edges as lines between them. The columns are labelled stakeholder, concern, affordance and technology; the first holds the nodes of the `group` layer. SVG and PNG are the same drawing in two formats. It needs the extra `draw`: `pip install "scat-kg[draw]"`. Without it, the call returns a refusal that says so. In the vault template it is already installed. Import the module with `from scat_kg import draw`. Where a view refuses, the drawing refuses with the same refusal.

A view's query returns a result: its document is the table of nodes and edges. A drawing and a table are two renderings of one result, and drawing never runs the query again. [`draw.render`](#scat_kgdrawrender) draws a result you already hold; `draw.fingerprint`, `draw.layered` and `draw.trace` run the query once and render it. To have the picture and the table from one query, run the view once and pass its result to `draw.render`. A drawing's `.nodes()` and `.edges()` always equal the table of the result it was drawn from, except that a fingerprint of an architecture or a scenario leaves out one column, as the note under the drawing says, and that a trace's drawing includes the starting node, which the trace's table names (`node`) but lists in neither `up` nor `down`.

### scat_kg.draw.render

```text
draw.render(result)
```

Draws a query result you already hold, without running any query: a fingerprint of one narrative, a layered view or a trace, as returned by [`scat_kg.fingerprint`](#scat_kgfingerprint), [`scat_kg.layered`](#scat_kglayered) or [`scat_kg.trace`](#scat_kgtrace). Returns a `Drawing`. A refusal passed in comes back unchanged. Any other result (an edge table, for example), or a fingerprint of more than one narrative, is refused with what to pass instead.

### scat_kg.draw.fingerprint

```text
draw.fingerprint(narrative, *, candidates=False, root=".")
```

Draws a narrative's fingerprint. The drawing follows the narrative's kind: an architecture has three columns (concern, affordance, technology), a scenario three (stakeholder, concern, affordance), and a narrative with no kind all four. A note under the drawing says which column is not drawn, why, and how many nodes of that layer the narrative links that it leaves out. The view's data, [`scat_kg.fingerprint`](#scat_kgfingerprint), keeps every node. With `candidates=True` its candidates are added as dashed lines. Returns a `Drawing`. `narrative` is required: one name. `candidates` is `False` unless you pass `True` (CLI: `--candidates`). CLI twin: [`scat draw fingerprint`](cli.md#scat-draw-fingerprint).

### scat_kg.draw.layered

```text
draw.layered(narratives=None, *, candidates=False, root=".")
```

Draws the layered view of the named narratives, or of every narrative. It keeps all four columns, because it mixes narratives. With `candidates=True` the candidates are added as dashed lines, and the footer names the narratives that have no account text. The footer also names the node pages no row tells, at most ten, then "and N more". Returns a `Drawing`. `candidates` is `False` unless you pass `True` (CLI: `--candidates`). CLI twin: [`scat draw layered`](cli.md#scat-draw-layered).

### scat_kg.draw.trace

```text
draw.trace(node, direction="both", *, root=".")
```

Draws what [`scat_kg.trace`](#scat_kgtrace) follows from a node: up toward the groups, down toward the technologies, or both. The node itself is drawn too, in its own layer's column, and the title names it, its type and the direction (`trace of concern water, up and down`). It keeps all four columns. Returns a `Drawing`. `node` is required: the name of a group, concern, affordance or technology. `direction` is `up`, `down` or `both` (the default; CLI: `--direction`). CLI twin: [`scat draw trace`](cli.md#scat-draw-trace).

### Drawing

| Member | What it does |
|---|---|
| `.png()` | The image, as bytes. |
| `.svg()` | The image, as text. |
| `.nodes()` | The nodes drawn, as `(name, layer)` pairs, column by column. |
| `.edges()` | The edges drawn, as `(from, to, dashed)`, the lines whose two ends are both drawn. |
| `.save(path)` | Writes the image to `path` and returns a `Result`. It is the only call here that writes a drawing. |

In Jupyter, a drawing shows itself. `.save` makes the folder if needed, rewrites a file only when its content differs, and refuses a name that does not end in `.png` or `.svg`, or that is a folder. The same view gives the same bytes.

=== "Python"

    ```python
    from scat_kg import draw

    draw.layered(["groups-under-a-cap-pitch"]).save("layered.png")
    draw.fingerprint("groups-under-a-cap-pitch").save("fingerprint.svg")
    draw.layered().save("layered.gif")
    ```

    ```text
    created layered.png
    created fingerprint.svg
    refused layered.gif: `.gif` is not an image type this draws
      Fix: end the file name with .png or .svg, for example `layered.png`
    ```

=== "CLI"

    ```bash
    uv run scat draw layered --narrative groups-under-a-cap-pitch --out drawn.png
    ```

    ```text
    created drawn.png
    ```

## Results

Each call returns one of these kinds of result. All print as their message.

| Kind | Returned by | Holds |
|---|---|---|
| `CheckResult` | `check`, when it ran | `problems`, `errors`, `warnings` (tuples of problems), `ok`. A problem has `rule`, `severity` (`"error"` or `"warning"`), `file`, `where`, `what`, `fix` and `line`. |
| `StatusReport` | `status`, when it ran | `scope` (`"page"`, `"neighborhood"` or `"vault"`), `rows` (each with `path`, `name`, `type`, `status`), `counts` (pages per status; `other` is a missing or invalid status), `ok`. |
| `Result` | `stub`, `stub_links`, `set_status`, `index`, and any refusal | `created`, `changed`, `unchanged`, `notes` (tuples of text), `refused` (each with `subject`, `why`, `fix`), `ok`. |
| `EdgeResult` | `record_edge`, `remove_edge` | everything a `Result` holds, and `edge`, `rows_added`, `rows_removed`. |
| `Guide` | `guide` | `stage`, `text`, `docs`, `tools`, `exits`, `ok` (always `True`). |
| `MergeResult`, `SplitPlan` | `merge`, `split_plan`, when they ran | everything a `Result` holds, and `plan`, `removed`, `done_narratives`, `links_rewritten` (merge); `node`, `node_type`, `pages` (split plan). |

The views return a `View` (see [Views](#views)) and the drawings a `Drawing` (see [Drawings](#drawings)).

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
- [Analysis guide](../analysis.md): the views, and how to read them.
- [Home](../index.md)
