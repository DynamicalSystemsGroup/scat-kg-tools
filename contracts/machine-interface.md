# Machine interface (schema version 2)

Every `scat` command takes `--json` and print one document shaped by
[`machine-interface.schema.json`](machine-interface.schema.json) (JSON Schema 2020-12).

- **Versioning.** `schema_version` is an integer, now 2 (what changed from 1 is under CHANGES, below). Adding a field keeps the version.
  Removing, renaming or changing a field's meaning bumps it, as does a new value in a closed list (severities,
  fix kinds, option kinds, edit actions). Ignore unknown fields.
- **Rule ids** are stable: never renamed, only retired. New ids need no bump: match
  `^SCAT-[A-Z0-9]+(-[A-Z0-9]+)*$`, not a list.
- **Streams.** Stdout holds exactly one JSON document; text for humans goes to stderr. Exit 0 when `ok`, 1 otherwise,
  2 for a command line that cannot be read.
- **Python.** A result's `to_dict()` returns exactly the CLI's data.
- **Paths** are vault-relative: `/`, no leading `/`, no `..`.

`kind` is `check`, `status` or `operation`. A refusal, even by `check` or `status`, gives kind `operation` with `ok` false. `ok` is false on an error or refusal; warnings keep it true.

## Fields you may rely on

Nothing outside it is promised.

| Object | Fields |
|---|---|
| every document | `schema_version`, `kind`, `operation`, `ok` |
| check | `problems` |
| problem | `rule`, `severity` (`error` or `warning`), `file`, `line`, `column`, `field` (null for a link, name or all front matter), `where`, `what`, `repeat` (identical messages it stands for), `fix`, `text` (the message as `scat check` prints it) |
| status | `scope` (`page`; `neighborhood`, a page and its linked pages; `vault`), `rows`, `counts` (per status, and `other`), `notes` |
| status row | `path`, `name`, `type`, `status` (as written, or null) |
| operation | `created`, `changed`, `unchanged` (already right, nothing written), `refused`, `notes` (sentences for a person); optional `problems` (what the write leaves, one link away) |
| record-edge, remove-edge result | an operation, and when `ok`: `edge`, `rows_added`, `rows_removed` |
| edge | `type` (`holds`, `addressed-by` or `provided-by`), `from`, `to` (page names), `narratives` (the page names of every narrative with a row for the edge once the operation is done) |
| row | `narrative`, `file`, `line`, `note` |
| refusal | `subject`, `why`, `fix`; optional `rule`, `problems` (the problems that make the refusal, each with its fix) |
| fix | `kind`, `head`, `sequence`, `options`, `notes` |
| option | `kind`, `text`, `command`, `edits` |
| command | `argv` (arguments after `scat`), `repl`, `author_slot` |
| edit | `action`, `file`, `field`, `value`, `author_slot`, `line`, `column`, `find`, `replace`, `to` |

`line` and `column` are integers from 1, or null. `line` counts the file's lines, front matter included; `column`, characters.

## Fixes

A fix's `kind` is the catalogue rule's kind (exact, options, slot, advisory, manual); each option has its
own kind (not `options`) and a `text`. `options` are alternatives unless `sequence` is
true: then steps in order, one per option. An option applies its `edits`, then its `command`.

- `exact` carries a `command`, `edits` or both.
- `slot` has an `author_slot` on an edit or on its `command`: the placeholder to replace, never written. In an array `value` it is the text in one string element. Or it chooses among exact values (no
  `author_slot`), e.g. the missing `timeframe` of a page (SCAT-DONE-FIELD). An option may only add (a suggestion you confirm) without clearing the problem on its own; read its `text`.
- `advisory` and `manual` carry neither.

Edits are computed from the file as checked. A `set-field` carries the whole new value, so two fixes for one field do not compose: apply one, then re-check.

An edit has one `action`:

| `action` | Fields used |
|---|---|
| `set-field` | `file`, `field`, `value` (you choose the YAML or TOML spelling; no front matter: add a block between two `---` lines; a key of `scat.toml` too) |
| `delete-field` | `file`, `field` |
| `replace-text` | `file`, `line`, `find` (the literal text as written in the file at that line), `replace`, optional `column`, optional `author_slot`. Without `column`, `find` is replaced everywhere on `line`; with it, only the occurrence at that column. `replace` may hold a line break, which adds a line (the separator row of a table is added this way) |
| `delete-line` | `file`, `line`, `find` (the whole line as written, a guard: nothing is deleted when the line is not exactly this). Removes a table row |
| `rename-file` | `file`, `to` |
| `delete-file` | `file` |

## Edge operations

`record-edge` and `remove-edge` (the catalogue's operations table gives their forms) return an operation document. An
edge is no page: it is the rows of narratives, so the result says which rows the call wrote.

- `edge` is the edge as the call leaves it: `type` (the slug; for `remove-edge`, the type its ends' layers fix),
  `from`, `to`, and `narratives`, every narrative that has a row for it afterwards, in byte order. After a
  `remove-edge` that took the last row, `narratives` is empty: the edge is gone from the graph.
- `rows_added` and `rows_removed` list the rows written and deleted, each with its `narrative`, `file`, `line` and
  `note`. The line of an added row is its line in the file as written; the line of a removed row is its line before the
  write. Both are empty when the call found nothing to do: `ok` is true and the narratives are in `unchanged`.
- Stubs the call created (a missing end node or narrative) are in `created`; narrative pages it wrote a row into are in
  `changed`. Links are never added or removed by either call.
- A refusal (a narrative it would change is `done`; an unknown type; ends in the wrong layers) has `ok` false, nothing
  written, and `edge`, `rows_added` and `rows_removed` may be absent.

Example, `scat record-edge holds borrowers quick-checkout --told-by saturday-at-the-desk --json` (abridged):

```json
{"schema_version": 2, "kind": "operation", "operation": "record-edge", "ok": true,
 "created": [], "changed": ["narrative/saturday-at-the-desk.md"], "unchanged": [], "refused": [], "notes": [],
 "edge": {"type": "holds", "from": "borrowers", "to": "quick-checkout", "narratives": ["saturday-at-the-desk"]},
 "rows_added": [{"narrative": "saturday-at-the-desk", "file": "narrative/saturday-at-the-desk.md", "line": 14, "note": ""}],
 "rows_removed": []}
```

## Table problems and the refusal to set `done`

A problem about a table or a row of it has `field` null, `line` the line of the row (of the header row, for the header),
`column` the first character of the cell it is about (of the first `|`, for a whole row), and a `where` such as
``row 2 cell `to` ``. A row is removed by a `delete-line` edit; a cell is corrected by a `replace-text` edit with a `column`.

A refusal to set a page to `done` (`set-status`) has `rule` `SCAT-DONE-REFUSED` and `problems`: the errors the page would
have at status `done`, each with its own fix. Its own `fix` is two advisory options.

## CHANGES

From version 1 to version 2. The version bumps because a closed list gains a value and a field goes (the rule at the
top of this file); the rest is additive. The reason for all of it is D-088: an edge is a row of a narrative's table,
not a page, and there are no raw and coded pairs, relation pages or class pages.

| Change | Kind | Why |
|---|---|---|
| New edit action `delete-line` | closed list gains a value: bumps | A table row is a whole line; `replace-text` cannot remove one without leaving an empty line, which ends the table. Row insertion needs no action: `replace-text` with a line break in `replace` (and, for a new table, an anchor on the last line of the file) covers it, and no catalogue fix inserts a row |
| `counts` of a status result no longer has `none` | field removed: bumps | It counted class pages, which carried no status. Every page type has one now (an index is a generated file and no page), so the count is always 0 |
| `StatusRow.type` takes the five page types `group`, `concern`, `affordance`, `technology`, `narrative` (version 1: the twelve) | meaning of values changes: bumps | The ontology's page types changed |
| Edge types: slugs `holds`, `addressed-by`, `provided-by` in `edge.type` | new closed list | The CLI and API spelling of the three edge types (`scat:slug`) |
| `record-edge` and `remove-edge` results: `edge`, `rows_added`, `rows_removed` | added | The new operations of M5; they replace `stub-pair`, which is gone |
| `Refusal.rule` and `Refusal.problems` | added | The refusal to set `done` lists what blocks it, with fixes |
| `OperationResult.problems` | added, optional | M5 reports the problems a write leaves, one link away |
| `ReplaceText.author_slot` | added | A table cell that is empty has a slot to fill (an author's choice of node); the other edit that carried a slot was `set-field` |
| `replace-text` `replace` may hold a line break | meaning widened | Adds the separator row of a table |
| `stub-pair` leaves the operation names | none: the names are a pattern | The command is removed |

A reader of version 1 documents finds the same objects and fields, except the ones above. A reader that ignores
unknown fields and edit actions it does not know reads version 2 documents to the extent that it does not apply
`delete-line` edits.
