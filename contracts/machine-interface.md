# Machine interface (schema version 1)

Every `scat` command takes `--json` and prints one document. Its shape is
[`machine-interface.schema.json`](machine-interface.schema.json) (JSON Schema 2020-12). A plugin needs this page and
that file, not the source.

## Rules of the interface

- **Versioning.** Every document has an integer `schema_version`, now 1. Adding a field keeps the version.
  Removing, renaming or changing the meaning of a field bumps it. Ignore fields you do not know. The closed lists
  (severities, fix kinds, option kinds, edit actions) are part of the meaning: a new value bumps the version.
- **Rule ids** are stable. A rule is never renamed, only retired. New ids may appear without a version bump, so match
  the pattern `SCAT-[A-Z0-9-]+`, not a list.
- **Streams and exit code.** Stdout holds exactly one JSON document. Text for humans goes to stderr. The exit code is
  unchanged: 0 when `ok`, 1 otherwise, 2 for a command line that cannot be read (then there is no document).
- **Python twin.** Every result has `to_dict()`, which returns exactly the data the CLI prints.
- **Paths** are vault-relative, with `/`.

## Three kinds of document

`kind` says which. `check` and `status` give their own kind when they run. When any command refuses (not a vault, page
not found, ...), including `check` and `status`, it gives kind `operation` with `ok` false. `ok` is false when there
is an error or a refusal; warnings alone keep it true.

## Fields you may rely on

Anything not in this table is not promised.

| Object | Fields |
|---|---|
| every document | `schema_version`, `kind`, `operation` (the command name), `ok` |
| check | `problems` |
| problem | `rule`, `severity` (`error` or `warning`), `file`, `line`, `column` (integer from 1, or null), `field` (null when the problem is about a link, a name or the whole front matter), `where`, `what`, `repeat`, `fix`, `text` (the message exactly as `scat check` prints it) |
| status | `scope`, `rows`, `counts` (per status, with `other` and `none`), `notes` |
| status row | `path`, `name`, `type`, `status` (as written, or null) |
| operation | `created`, `changed`, `unchanged`, `refused`, `notes` |
| refusal | `subject`, `why`, `fix` |
| fix | `kind`, `head`, `sequence`, `options`, `notes` |
| option | `kind`, `text`, `command`, `edits` |
| command | `argv` (arguments after `scat`), `repl` |
| edit | `action`, `file`, `field`, `value`, `author_slot`, `line`, `column`, `find`, `replace`, `to` |

## Fixes are data

A fix has a `kind` (exact, options, slot, advisory or manual, as in the rule catalogue), an optional `head`, and
`options`. The `options` are alternatives to choose from, unless `sequence` is true: then do all, in order. An option
has its own `kind` and the `text` shown to a person.

- `exact` carries a `command`, `edits`, or both (apply the edits, then run the command).
- `slot` carries `edits`, one of which has `author_slot`: the placeholder text in `value` that the author must
  replace. Never write it as is.
- `advisory` and `manual` carry neither.

An edit is one of five `action` values:

| `action` | Fields used |
|---|---|
| `set-field` | `file`, `field`, `value` (the whole new value; adds the field or replaces it; a key of `scat.toml` too) |
| `delete-field` | `file`, `field` |
| `replace-text` | `file`, `line`, `find`, `replace`, optional `column` |
| `rename-file` | `file`, `to` |
| `delete-file` | `file` |
