# JSON contract: `scat check --json`

`scat check --json` does not exist. This is the shape the plugin expects. It is derived from `Problem` in
`src/scat_kg/checks/problem.py`. Since D-054 the plugin does not call `scat`: it runs the shim `scat_json.py`
(public `scat_kg.check` only) with `uv run --project VAULT python scat_json.py NOTE.md [--neighborhood]`, and the shim
prints this JSON. The shim's extra fields are in the section at the end.

```json
{
  "schema_version": 1,
  "ok": false,
  "problems": [
    {
      "rule": "SCAT-NAME",
      "severity": "error",
      "file": "people/ada.md",
      "where": "field `name`",
      "what": "the name does not match the file name",
      "fix": "Fix: rename the field to `ada`",
      "line": 3,
      "column": 1,
      "repeat": 1
    }
  ]
}
```

| Field | Type | Required | Source in `Problem` | Plugin behavior when absent |
|---|---|---|---|---|
| `schema_version` | integer | no | new | assumed 1; a value above 1 is refused |
| `ok` | boolean | no | `Report` | derived: true when there is no `error` |
| `problems` | array | **yes** | `Report.problems` | whole payload rejected |
| `rule` | string | **yes** | `rule` | entry dropped |
| `file` | string, vault-relative, `/` | **yes** | `file` | entry dropped |
| `severity` | `"error"` or `"warning"` | no | `severity` | treated as `error` |
| `where` | string | no | `where` | empty |
| `what` | string | no | `what` | empty |
| `fix` | string, the whole fix block | no | `fix` | empty |
| `line`, `column` | integer >= 1 or `null` | no | `line`, `column` | `null` (no jump target) |
| `repeat` | integer >= 1 | no | `repeat` | 1 |

Rules for the tool side:

- Stdout holds only the JSON object. Messages for humans go to stderr.
- Exit code stays as today (1 when there are errors); the plugin reads stdout whatever the exit code.
- `order` is internal and is not emitted. Problems arrive in the catalogue's sort order and the plugin keeps it.
- Unknown extra fields are ignored. Removing or retyping a field bumps `schema_version`.
- Not in this version: structured edits for quick fixes, an unsaved-buffer overlay (see the readout, section 4).

## Fields the shim adds (`scat_json.py`)

| Field | Meaning |
|---|---|
| `status` | `ok` (checked), `not-a-vault` (no `scat.toml` in the note's folder or above), `not-a-page` (no `type:` in the frontmatter), `refused` (scat_kg declined; `message` has its words), `no-scat-kg` (this Python cannot import it), `error`. Absent means `ok`. |
| `message` | Words for a human when `status` is not `ok`; empty otherwise. |
| `root` | Absolute path of the SCAT vault (the folder with `scat.toml`). `file` of each problem is relative to it, so the plugin joins the two to find the note. |
| `page` | The checked note, relative to `root`. |

Differences from the list above: the shim's exit code is 0 whenever it printed JSON (errors in the note do not change it), and it takes an absolute note path instead of `--root`.
