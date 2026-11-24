# Machine interface (schema version 1)

Every `scat` command takes `--json` and prints one document shaped by
[`machine-interface.schema.json`](machine-interface.schema.json) (JSON Schema 2020-12).

## Rules

- **Versioning.** `schema_version` is an integer, now 1. Adding a field keeps the version.
  Removing, renaming or changing the meaning of a field bumps it, as does a new value in a closed list (severities,
  fix kinds, option kinds, edit actions). Ignore unknown fields.
- **Rule ids** are stable: never renamed, only retired. New ids need no bump: match
  `^SCAT-[A-Z0-9]+(-[A-Z0-9]+)*$`, not a list.
- **Streams and exit code.** Stdout holds one JSON document; text for humans goes to stderr. Exit 0 when `ok`, 1 otherwise,
  2 for a command line that cannot be read.
- **Python twin.** Every result's `to_dict()` returns exactly the data the CLI prints.
- **Paths** are vault-relative, with `/`, no leading `/`, no `..`.

## Kinds

`kind` is `check`, `status` or `operation`. A refusal, even by `check` or `status`, gives kind `operation` with `ok` false. `ok` is false on an error or refusal; warnings keep it true.

## Fields you may rely on

Nothing outside it is promised.

| Object | Fields |
|---|---|
| every document | `schema_version`, `kind`, `operation`, `ok` |
| check | `problems` |
| problem | `rule`, `severity` (`error` or `warning`), `file`, `line`, `column`, `field` (null for a link, a name or all front matter), `where`, `what`, `repeat` (identical messages it stands for), `fix`, `text` (the message as printed) |
| status | `scope` (`page`, `neighborhood`, `vault`), `rows`, `counts` (per status, `other`, `none`), `notes` |
| status row | `path`, `name`, `type`, `status` (as written, or null) |
| operation | `created`, `changed`, `unchanged` (already right), `refused`, `notes` |
| refusal | `subject`, `why`, `fix` |
| fix | `kind`, `head`, `sequence`, `options`, `notes` |
| option | `kind`, `text`, `command`, `edits` |
| command | `argv` (arguments after `scat`), `repl`, `author_slot` |
| edit | `action`, `file`, `field`, `value`, `author_slot`, `line`, `column`, `find`, `replace`, `to` |

`line` and `column` are integers from 1, or null. `line` counts the file's lines, front matter included; `column`, characters.

## Fixes are data

A fix's `kind` is the catalogue rule's kind (exact, options, slot, advisory, manual); each option has its
own kind (not `options`) and a `text` for a person. The `options` are alternatives, unless `sequence` is
true: then they are steps in order, one per option. An option applies its `edits`, then its `command`.

- `exact` carries a `command`, `edits` or both.
- `slot` has an `author_slot` on an edit or on its `command`: the placeholder to replace, never
  written. In an array `value` it is the text in one string element. It may instead choose among exact values (no
  `author_slot`), e.g. a `timeframe`. An option may add something without clearing the problem alone (an additive
  suggestion): its `text` says so.
- `advisory` and `manual` carry neither.

Edits are computed from the file as checked. A `set-field` carries the whole new value, so two fixes for one field do not compose: apply one, then re-check.

An edit has one `action`:

| `action` | Fields used |
|---|---|
| `set-field` | `file`, `field`, `value` (you choose the YAML or TOML spelling; no front matter: add a block between two `---` lines; a key of `scat.toml` too) |
| `delete-field` | `file`, `field` |
| `replace-text` | `file`, `line`, `find` (the literal text as written in the file at that line), `replace`, optional `column`. Without `column`, `find` is replaced everywhere on `line`; with it, only the occurrence at that column |
| `rename-file` | `file`, `to` |
| `delete-file` | `file` |
