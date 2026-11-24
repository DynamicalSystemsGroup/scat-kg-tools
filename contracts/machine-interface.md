# Machine interface (schema version 1)

Every `scat` command takes `--json` and prints one document, shaped by
[`machine-interface.schema.json`](machine-interface.schema.json) (JSON Schema 2020-12).

## Rules of the interface

- **Versioning.** Every document has an integer `schema_version`, now 1. Adding a field keeps the version.
  Removing, renaming or changing the meaning of a field bumps it. Ignore unknown fields. The closed lists
  (severities, fix kinds, option kinds, edit actions) are part of the meaning: a new value bumps the version.
- **Rule ids** are stable: never renamed, only retired. New ids may appear without a version bump, so match the
  pattern `^SCAT-[A-Z0-9]+(-[A-Z0-9]+)*$`, not a list.
- **Streams and exit code.** Stdout holds exactly one JSON document. Text for humans goes to stderr. The exit code is
  unchanged: 0 when `ok`, 1 otherwise, 2 for a command line that cannot be read.
- **Python twin.** Every result has `to_dict()`, which returns exactly the data the CLI prints.
- **Paths** are vault-relative, with `/`, no leading `/`, no `..`.

## Three kinds of document

`kind` is `check`, `status` or `operation`. When any command refuses, `check` and `status` included, it gives kind `operation` with `ok` false. `ok` is false when there is an error or a
refusal; warnings alone keep it true.

## Fields you may rely on

Anything not in this table is not promised.

| Object | Fields |
|---|---|
| every document | `schema_version`, `kind`, `operation`, `ok` |
| check | `problems` |
| problem | `rule`, `severity` (`error` or `warning`), `file`, `line`, `column`, `field` (null when the problem is about a link, a name or the whole front matter), `where`, `what`, `repeat` (how many identical messages this one stands for), `fix`, `text` (the message as `scat check` prints it) |
| status | `scope` (`page`; `neighborhood`, a page and its linked pages; `vault`), `rows`, `counts` (per status, with `other`, `none`), `notes` |
| status row | `path`, `name`, `type`, `status` (as written, or null) |
| operation | `created`, `changed`, `unchanged` (already right, nothing written), `refused`, `notes` (sentences for a person) |
| refusal | `subject`, `why`, `fix` |
| fix | `kind`, `head`, `sequence`, `options`, `notes` |
| option | `kind`, `text`, `command`, `edits` |
| command | `argv` (arguments after `scat`), `repl`, `author_slot` |
| edit | `action`, `file`, `field`, `value`, `author_slot`, `line`, `column`, `find`, `replace`, `to` |

`line` and `column` are integers from 1, or null. `line` counts the file's own lines, front matter included;
`column` counts characters.

## Fixes are data

A fix's `kind` is the rule's kind in the catalogue (exact, options, slot, advisory, manual); each option carries
its own kind (not `options`) and the `text` shown to a person. The `options` are alternatives, unless `sequence` is
true: then they are steps, applied in order, one option per step. An option's own order is its `edits`, then its
`command`.

- `exact` carries a `command`, `edits`, or both.
- `slot` has an `author_slot` on an edit or on its `command`: the placeholder text the author must replace, never
  written as is. In an array `value` it is the text inside one string element.
- `advisory` and `manual` carry neither.

An edit has one `action`:

| `action` | Fields used |
|---|---|
| `set-field` | `file`, `field`, `value` (the whole new value; you choose the YAML or TOML spelling; a file with no front matter gets a block between two `---` lines; a key of `scat.toml` too) |
| `delete-field` | `file`, `field` |
| `replace-text` | `file`, `line`, `find`, `replace`, optional `column` |
| `rename-file` | `file`, `to` |
| `delete-file` | `file` |
