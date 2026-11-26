# Machine interface (schema version 2)

Every `scat` command takes `--json` and prints one document shaped by
[`machine-interface.schema.json`](machine-interface.schema.json) (JSON Schema 2020-12). The schema's `description`
fields detail each object; the rule catalogue (section 8) gives the edge operations, table problems and
changes from version 1.

- **Versioning.** `schema_version` is an integer, 2. Adding a field keeps the version. Removing, renaming or
  changing a field's meaning bumps it, as does a new value in a closed list (severities, fix kinds, option kinds, edit
  actions, edge types). Ignore unknown fields.
- **Rule ids** are never renamed, only retired. New ids need no bump: match `^SCAT-[A-Z0-9]+(-[A-Z0-9]+)*$`, not a list.
- **Streams.** Stdout holds exactly one JSON document; text for humans goes to stderr. Exit 0 when `ok`, 1 otherwise,
  2 for a command line that cannot be read.
- **Python.** A result's `to_dict()` returns the CLI's data.
- **Paths** are vault-relative (`/`, no leading `/`, no `..`), except in `export-edges` and `draw` results: outside the vault, as given. `line` and `column` count from 1, or are null.

`kind` is `check`, `status`, `operation` or `view` (`fingerprint`, `edges`, `layered`, `trace`). A refusal, even by `check` or `status`, gives kind `operation` with `ok` false.

## Fields you may rely on

Nothing else is promised.

| Object | Fields |
|---|---|
| every document | `schema_version`, `kind`, `operation`, `ok`, `mode` |
| check | `problems` |
| problem | `rule`, `severity` (`error` or `warning`), `file`, `line`, `column`, `field`, `where`, `what`, `repeat`, `fix`, `text` (the message as `scat check` prints it) |
| status | `scope` (`page`; `neighborhood`, a page and its linked pages; `vault`), `rows`, `counts`, `notes` |
| status row | `path`, `name`, `type`, `status` |
| operation | `created`, `changed`, `unchanged` (already right, nothing written), `refused`, `notes` (sentences for a person), `problems` |
| record-edge, remove-edge result | an operation, and when `ok`: `edge`, `rows_added`, `rows_removed` |
| edge | `type` (`holds`, `addressed-by` or `provided-by`), `from`, `to`, `narratives` |
| row | `narrative`, `file`, `line`, `note` |
| refusal | `subject`, `why`, `fix`, `rule`, `problems` |
| fix | `kind`, `head`, `sequence`, `options`, `notes` |
| option | `kind`, `text`, `command`, `edits` |
| command | `argv`, `repl`, `author_slot` |
| edit | `action`, `file`, `field`, `value`, `author_slot`, `line`, `column`, `find`, `replace`, `to` |

## View fields

| Object | Fields |
|---|---|
| view | `narratives` (`candidates` on request), `edge_type`, `from_layer`, `to_layer`, `rows`, `nodes`, `edges`, `node`, `direction`, `up`, `down`, `excluded` |
| node | `name`, `type`, `status` |
| view edge | the edge fields and `status` |

## Fixes

A fix's `kind` is the catalogue rule's kind (exact, options, slot, advisory, manual); each option has its own kind
and a `text`. `options` are alternatives unless `sequence` is true: steps in order. An option applies `edits`, then `command`.

- `exact` carries a `command`, `edits` or both; `advisory` and `manual` carry neither.
- `slot` has an `author_slot` on an edit or on its `command`: the placeholder to replace, never written. Or it
  chooses among exact values (no `author_slot`), e.g. the missing `timeframe` of a page (SCAT-DONE-FIELD). An option
  may only add (a suggestion you confirm) without clearing the problem on its own; read its `text`.

Edits are computed from the file as checked. A `set-field` carries the whole new value, so two fixes for one field do
not compose: apply one, then re-check. An edit has one `action`: `set-field`, `delete-field`, `replace-text`,
`delete-line`, `rename-file` or `delete-file`. For `replace-text`, `find` is the literal text as written in the file at
that line. Without `column`, `find` is replaced everywhere on `line`; with it, only the occurrence at that column.
