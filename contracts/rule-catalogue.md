# SCAT rule catalogue (WP16, for the layout of D-088)

What a check looks at, at what severity, and what each message tells the user to do. It serves goal WP4-G3 and
requirements R-1 to R-4, R-8 and R-23 of the mission. The ontology (`ontology/scat.ttl`) says what a conformant page is;
this file says how a departure is graded and worded. The page contracts (`contracts/page-contracts.md`) say how pages
are named, written and linked, how a narrative's table is read, and which pages a link entails. This file uses their
conventions and does not restate them; where it needs one it names the contract section.

Every rule has an id, a severity (`error` blocks, `warning` does not), the status at which it fires, the scopes it
runs at, a trigger a test can produce, a message that names the file, the place and the rule id, and a fix. A fix is
**data** (machine interface, `contracts/machine-interface.md`): a kind, and the commands and edits that carry it out.

Checks concern structure only (R-1): tensions, matches and gaps are for analysis. A narrative that links both ends of
a pair and has no row for it is not a defect, and the tool says nothing about it (section 4).

## 1. Conventions every rule shares

**Page terms.** A page is a Markdown file as page contracts section 1 says; `<file>` is its vault-relative path with
`/` separators (`concern/safe-handling-of-tools.md`), `<page-name>` the file name without `.md`, `<type-key>` the value
of its `type` field. A *node page* is a page of type `group`, `concern`, `affordance` or `technology`. A *link* is as
page contracts section 3 says (aliases, headings and block references stripped; code is never a link; targets that
are not page names, containing a dot or a `/`, are not page links). A link's *target* is the name inside the brackets.
A *row end* is the `from` or `to` cell of a row of a narrative's table; a *row* is numbered `<n>` from 1 in the order
written, the separator excluded; the *layer* of an end is the node type its edge type fixes for it (page contracts
section 4: `holds` joins a `group` to a `concern`, `is addressed by` a `concern` to an `affordance`, `is provided by`
an `affordance` to a `technology`). An end *resolves* when it is one link whose target is the name of a page whose
`type` is valid. A page's *status* is `stub`, `draft` or `done`.

**Legal name and derived name.** A name is *legal* when it meets page contracts section 2 (slug characters, at most 64,
not reserved). The *stem* of a text is steps 1 to 3 of the name-from-title rule applied to it (empty when step 3
leaves nothing); its *free derived name* is what step 4 gives. A derived name is always legal. "Derived name" without
"free" means the stem, or the free derived name when the stem is reserved or taken by a file that is not a page.

**Scopes.** A check runs at *page*, *one link away* or *vault* scope (G4): the page; the page and every page it links
or that links it; every page. A rule reports on one file, and a check of that file runs every rule that reports on it,
reading other pages when the rule needs them. The one exception is SCAT-CAP, which reports on `scat.toml` though it is anchored on a page check (it runs when a `group` page is in the set). The same page gives the same messages at every scope. Rules that are not
about one page (SCAT-CAP, SCAT-CAP-CONFIG) run at vault scope, and at the other two when a `group` page is in the
checked set. For a narrative, the nodes at its row ends are one link away, so a check one link away reads them and
reports on each page it reaches by that page's own rules. Checks never write (R-4). Each rule below says which pages it
reads besides its own.

**Cascade guard.** A file that starts with a `---` line but fails SCAT-FM-PARSE is checked by no other rule as a
source. A page whose `type` is invalid is checked by no rule that needs its type, and a link whose target page has an
invalid `type` is not judged for its page type (the target has its own error), except at a row end, where a page that is not a valid node is judged by SCAT-*-END-NOTNODE. A page whose `status` is
missing or invalid is checked by no rule marked "needs status"; the status error is reported once, on the page. A
table is read only on a page of type `narrative`. A table whose header or separator row is malformed (the
SCAT-DRAFT-TABLE-HEADER and SCAT-DONE-TABLE-HEADER condition) is reported once and its rows are checked by no row rule:
which cell is which is not known until the header is right, and it tells no edge until then (a table of a header row alone is such a table). A second table or heading is not read at all (SCAT-*-TABLE-SECOND).

**Well-formed.** A *table* is well-formed when its header row has the four column names, in order, and a separator row
follows. A *row* is well-formed when it has four cells and ends with an unescaped `|` (page contracts 4, Cells). A row
that is not well-formed tells no edge: SCAT-*-TABLE-ROW judges it, first and alone; the type, layers, duplicate and end
rules do not (R-23 is not engaged until the row is right), so a link in its `from` or `to` cell is graded by nothing
until then. A link in any other cell of it is an ordinary body link. In a table whose header is malformed, in a second
table, and outside the table altogether, every link is an ordinary body link, graded by SCAT-LINK-DANGLING-BODY.

**Empty.** A field is *missing* when the key is absent or its value is null, an empty or blank string, or an empty
list. A cell is *empty* when it holds nothing but whitespace.

**Add or replace.** A fix that writes a line for a field says "add the line `X`" when the key is absent and "replace
the line `<field>: <current>` with `X`" when the key is present but empty (`<current>` is the text after the colon as
written, or nothing). Messages below show the "add" wording and carry this rule.

**Status behaviour (R-3), in one table.** "Pair" is a condition with two ids: the `SCAT-DRAFT-` id is a warning and
fires on a `stub` or `draft` narrative; the `SCAT-DONE-` id is the same condition as an error on a `done` narrative.

| Kind of rule | stub | draft | done |
|---|---|---|---|
| Required from `stub` (`status`, `title`) | error | error | error |
| Required from `done`, text (`description`) | silent | warning | error |
| Required from `done`, a value set (`timeframe`) | warning | warning | error |
| Name, frontmatter shape and values, dangling body link, cap | error | error | error |
| Pairs: table and row problems, mismatches (narratives only) | warning | warning | error |
| Mention | warning | warning | warning |

An unfinished page is never an error for being unfinished: nothing in the `done` column is an error before `done`.
Setting `done` is judged as the page would stand at `done` (section 5).

**Order and format.** Messages sort by file path (byte order), then line (a message with no line sorts first), then
column (messages with no column sort first), then rule id, then the position in the file of the field key, link or
cell, then the target name (byte order), then the field name (byte order). Messages identical in rule, file, line and
text are printed once, with ` (x<n>)` appended to the first line. The format:

```
<severity> [<rule-id>] <file>[:<line>[:<column>]] <where>: <what is wrong>
  Fix: <one exact fix>
```
or, when the fix is a choice between alternatives, or steps:
```
  Fix, choose one:
    1. <fix>
    2. <fix>
```
`<severity>` is `error` or `warning`, and `refused` in the refusal of section 5. `<line>` is the 1-based line of the link, field key, header or row; `<column>`
(characters, 1-based) is given for a table cell (its first character), a row (its first `|`), the header (its first
`|`) and a mention (the first character of the text). `<where>` is ``field `<name>` `` (a frontmatter field, or a key of `scat.toml`, whose file is then `scat.toml`), ``link [[<target>]]``,
`frontmatter`, `table header`, ``row <n>`` or ``row <n> cell `<type|from|to>` ``. Angle-bracket words are filled in by
the tool, except a slot marked *(author)*, which stays in the message literally because only the author can fill it.
A fix says exactly which line to write, replace or delete. A command fix names the command and its REPL twin on one
line, as in ``run `scat set-status <page-name> draft` (REPL: `scat_kg.set_status("<page-name>", "draft")`)``. The same
text is printed on both paths (R-8).

**Fix data.** Under each rule, "Edits" is the fix as data, in the machine interface's vocabulary: `set-field{field,
value}`, `replace-text{line, column, find, replace}`, `delete-line{line, find}` (removes one whole row), and
`command{argv}`. A fix that edits a table cell uses `replace-text` with the cell's `column`, and `find` is the cell's
content as written, trimmed. An *empty* cell has no content to find: its fix takes the whole row line as `find` and
writes the row line again with the cell filled. A fix that removes a row is a `delete-line` whose `find` is the row as
written. Fix kinds: **exact** (one exact edit or command); **options** (alternatives, each exact or advisory; the
choice is the author's); **slot** (exact except one *(author)* slot); **advisory** (no change is required); **manual**
(no exact fix is possible; why recorded). A rule whose kind differs by variant says so.

**Operations the fixes name.**

| Operation | CLI form | REPL form | What the messages rely on |
|---|---|---|---|
| stub | `scat stub <page-name> --type <type-key>` | `scat_kg.stub("<page-name>", type="<type-key>")` | Creates the page as page contracts section 6 says (`status: stub`, title from the name). Accepts the four node types and `narrative`; refuses an illegal name, a name that is already an existing `.md` file, and a `group` page that would take the vault over its cap. Writes nothing else. |
| set-status | `scat set-status <page-name> <status>` | `scat_kg.set_status("<page-name>", "<status>")` | Sets `status`, adding the key if absent. Setting `done` is judged first (section 5). |

`record-edge` and `remove-edge` are operations of the tool too (`scat record-edge TYPE FROM TO --told-by NARRATIVE
[--told-by NARRATIVE ...] [--note TEXT]`, `scat remove-edge FROM TO [--told-by NARRATIVE ...]`; `--told-by` may be repeated,
and `remove-edge` without it removes the rows of every narrative that tells the pair), with results in the machine interface. No message
names them: recording an edge is writing a row, which the author does in Obsidian or by that command, and no rule says
a row is missing (section 4).

**Near match.** For a text `a` and a list of names, the near match is the name `b` with the highest
`difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()`, if that ratio is at least 0.8; ties go to the name
first in byte order. No near match means none.

**Candidates for a row end** of layer `T`: the near match of the end's text among the pages of type `T`, then the other
pages of type `T` that the narrative links elsewhere (body or other rows), in byte order; each only once; at most 5
shown, then one final line `(+<n> more not shown)`, which is not an option.

## 2. Rule index

Every id in the catalogue, with its status in this version. *Kept*: same condition, same id. *Adapted*: same id, the
condition or message follows the new model. *New*. *Retired*: the id is never reused or renamed; the rule is gone
because the model it checked is gone (D-088).

| Id | Status | Note |
|---|---|---|
| SCAT-FM-PARSE | kept | |
| SCAT-FM-REQUIRED | adapted | `status` and `title` only; `indexes` is gone |
| SCAT-FM-TYPE | adapted | five page types |
| SCAT-FM-STATUS | kept | |
| SCAT-FM-TIMEFRAME | adapted | on a narrative |
| SCAT-FM-KIND | new | `kind` outside its value set |
| SCAT-FM-SHAPE | adapted | the fields of the new types |
| SCAT-NAME | adapted | no class page names |
| SCAT-DONE-FIELD | adapted | `description`; `timeframe` on a narrative |
| SCAT-DRAFT-FIELD | adapted | |
| SCAT-LINK-DANGLING-BODY | adapted | every link outside a table end |
| SCAT-CAP | adapted | counts `group` pages |
| SCAT-CAP-CONFIG | kept | |
| SCAT-MENTION | adapted | on every page, narratives included |
| SCAT-DRAFT-TABLE-HEADER, SCAT-DONE-TABLE-HEADER | new | pair |
| SCAT-DRAFT-TABLE-ROW, SCAT-DONE-TABLE-ROW | new | pair |
| SCAT-DRAFT-TABLE-TYPE, SCAT-DONE-TABLE-TYPE | new | pair |
| SCAT-DRAFT-TABLE-LAYERS, SCAT-DONE-TABLE-LAYERS | new | pair |
| SCAT-DRAFT-TABLE-SECOND, SCAT-DONE-TABLE-SECOND | new | pair |
| SCAT-DRAFT-TABLE-DUPLICATE, SCAT-DONE-TABLE-DUPLICATE | new | pair |
| SCAT-DRAFT-END-NOLINK, SCAT-DONE-END-NOLINK | new | pair; a mismatch (R-23) |
| SCAT-DRAFT-END-NOPAGE, SCAT-DONE-END-NOPAGE | new | pair; a mismatch |
| SCAT-DRAFT-END-NOTNODE, SCAT-DONE-END-NOTNODE | new | pair; a mismatch |
| SCAT-DONE-REFUSED | new | the refusal to set `done` (an operation, not a check) |
| SCAT-FM-REQUIRED-LINK | retired | no link fields; no relation pages |
| SCAT-FM-INDEXES | retired | no class pages |
| SCAT-DONE-LINK, SCAT-DRAFT-LINK | retired | no required link fields |
| SCAT-LINK-SHAPE | retired | no link fields |
| SCAT-LINK-UNLISTED | retired | no link fields |
| SCAT-LINK-ENDPOINT | retired | no link fields; the layers of a row's ends are SCAT-*-TABLE-LAYERS |
| SCAT-LINK-DANGLING | retired | it checked frontmatter links, which are never read now (page contracts 3) |
| SCAT-LINK-DISCOURAGED, SCAT-LINK-DISCOURAGED-BODY | retired | no discouraged field or body link in the ontology |
| SCAT-CONFLICT-SELF | retired | the `conflicts` field is gone; a relationship annotation has no meaning to the tool |
| SCAT-REL-DUPLICATE | retired | no relation pages; duplicates in a narrative are SCAT-*-TABLE-DUPLICATE |
| SCAT-RAW-BACKLINK, SCAT-RAW-UNCODED | retired | no raw and coded pairs |
| SCAT-INDEX-STALE | retired | an index is a generated Base and cannot go stale |

## 3. Rules

| Id | Severity | Fires at | Runs at | Trigger (short) | Fix kind |
|---|---|---|---|---|---|
| SCAT-FM-PARSE | error | every status | all | file starts with `---` but its frontmatter is not a readable mapping | manual |
| SCAT-FM-REQUIRED | error | every status | all | `status` or `title` is missing | options |
| SCAT-FM-TYPE | error | every status | all | `type` is not one of the five page types | options |
| SCAT-FM-STATUS | error | every status | all | `status` is not `stub`, `draft` or `done` | options |
| SCAT-FM-TIMEFRAME | error | every status | all | `timeframe` on a narrative is outside its value set | options |
| SCAT-FM-KIND | error | every status | all | `kind` on a narrative is outside its value set | options |
| SCAT-FM-SHAPE | error | every status | all | a text field is not a single non-empty string | manual |
| SCAT-NAME | error | every status | all | a page's file name is not a legal name, or is not unique | manual |
| SCAT-DONE-FIELD | error | done | all | a field required from `done` is missing | slot |
| SCAT-DRAFT-FIELD | warning | draft; stub for `timeframe` | all | a field required from `done` is missing | slot |
| SCAT-LINK-DANGLING-BODY | error | every status | all | a link outside a table end reaches no page | options |
| SCAT-CAP | error | vault | vault; all when a `group` page is in the set | more `group` pages than the cap | options |
| SCAT-CAP-CONFIG | error | vault | vault; all when a `group` page is in the set | `scat.toml` or its cap missing, malformed or not a whole number of at least 1 | slot |
| SCAT-MENTION | warning | every status | all | body names an existing node page in plain text | exact |
| SCAT-DRAFT-TABLE-HEADER | warning | stub, draft | all | the table's header or separator row is malformed | advisory |
| SCAT-DONE-TABLE-HEADER | error | done | all | the table's header or separator row is malformed | advisory |
| SCAT-DRAFT-TABLE-ROW | warning | stub, draft | all | a row does not have four cells and its closing `\|` | options |
| SCAT-DONE-TABLE-ROW | error | done | all | a row does not have four cells and its closing `\|` | options |
| SCAT-DRAFT-TABLE-TYPE | warning | stub, draft | all | a `type` cell is not the verb or slug of an edge type | options |
| SCAT-DONE-TABLE-TYPE | error | done | all | a `type` cell is not the verb or slug of an edge type | options |
| SCAT-DRAFT-TABLE-LAYERS | warning | stub, draft | all | a row end is a node of a layer the type does not allow there | options |
| SCAT-DONE-TABLE-LAYERS | error | done | all | a row end is a node of a layer the type does not allow there | options |
| SCAT-DRAFT-TABLE-SECOND | warning | stub, draft | all | a second `Edges told` table or heading on a narrative | options |
| SCAT-DONE-TABLE-SECOND | error | done | all | a second `Edges told` table or heading on a narrative | options |
| SCAT-DRAFT-TABLE-DUPLICATE | warning | stub, draft | all | a row repeats the type, `from` and `to` of an earlier row of the same narrative | exact |
| SCAT-DONE-TABLE-DUPLICATE | error | done | all | a row repeats the type, `from` and `to` of an earlier row of the same narrative | exact |
| SCAT-DRAFT-END-NOLINK | warning | stub, draft | all | a row end is not exactly one link | options |
| SCAT-DONE-END-NOLINK | error | done | all | a row end is not exactly one link | options |
| SCAT-DRAFT-END-NOPAGE | warning | stub, draft | all | a row end links a name that is no page | options |
| SCAT-DONE-END-NOPAGE | error | done | all | a row end links a name that is no page | options |
| SCAT-DRAFT-END-NOTNODE | warning | stub, draft | all | a row end links a page that is not a node | options |
| SCAT-DONE-END-NOTNODE | error | done | all | a row end links a page that is not a node | options |

The Fix kind column is the least exact kind any variant of the rule has, in the order exact, slot, options, advisory,
manual. The variants, where they differ:

| Rule | Variants and their kinds |
|---|---|
| SCAT-FM-REQUIRED | `status`: options; `title`: exact |
| SCAT-FM-TYPE, SCAT-FM-TIMEFRAME | with a near match: exact; without: options |
| SCAT-FM-SHAPE | one-item list, boolean, number: exact; otherwise manual |
| SCAT-DONE-FIELD, SCAT-DRAFT-FIELD | `description`: slot; `timeframe`: slot (a choice among exact values) |
| SCAT-NAME | exact; a hand choice (no title to derive from): manual |
| SCAT-LINK-DANGLING-BODY | options in every variant |
| SCAT-*-TABLE-HEADER | name wrong or separator missing: exact; the four names in another order: advisory |
| SCAT-*-TABLE-ROW | (a), (b), (c): exact; (d), (e): options |
| SCAT-*-TABLE-TYPE, -LAYERS, -NOLINK, -NOPAGE, -NOTNODE, -SECOND | options in every variant |
| SCAT-CAP | options; SCAT-CAP-CONFIG: slot |

SCAT-FM-STATUS is options in every variant: which status is true is a claim about the page, so even a near match is the
author's to confirm; the near matches of SCAT-FM-TYPE and SCAT-FM-TIMEFRAME are exact, as a spelling mends a spelling.
The schema wants two or more options for kind `options`, so a fix left with one option takes that option's kind. The
built tool does this in these named cases, where the column above names the kind of the choice: SCAT-FM-REQUIRED
`status` (one command: exact); the near match of SCAT-FM-STATUS (one edit: exact); SCAT-LINK-DANGLING-BODY when only
the replace-by-text option remains (exact); and, in SCAT-CAP, option 1 is kind `manual`, not `advisory`.

"all" is page, one link away and vault. The pair rules are *needs status*: a narrative whose `status` is missing or
invalid gets the status error and none of them. They report only on narratives. Tests: every test starts from a clean
fixture vault with zero messages, injects exactly one defect, and expects exactly one message of the rule, equal to
the golden text, and no other message. A pair has one seed set run three times: at `stub` and `draft` (the DRAFT id,
warning, same message) and at `done` (the DONE id, error, same message but for the id and severity). Every fix is data.

### SCAT-FM-PARSE
- **Severity:** error. **Fires:** every status. **Runs at:** all; reads only its page.
- **Trigger:** the file starts with a `---` line (so it means to be a page) and either has no closing `---` line, or the frontmatter is not valid YAML (for example `title: a: b`), or is not a mapping. An unquoted ` #` silently cuts the rest of the line as a YAML comment and is not reported, which is why the contract advises quoting. A Markdown file with no frontmatter, or with frontmatter and no `type` key, is not a page and gets no message; a link to it is a dangling link (SCAT-LINK-DANGLING-BODY variant b).
- **Message:**
```
error [SCAT-FM-PARSE] <file>[:<line>] frontmatter: <parser's reason, or "the closing --- line is missing">
  Fix: make the frontmatter a block of `key: value` lines between two lines containing only `---`, at the very top of the file; start from the first line the parser rejected
```
- **Fix kind:** manual. The tools cannot repair text they could not read, and the page's type is the author's to state. Edits: none.
- **Seed:** a node page with the closing `---` deleted; one with a tab-indented key. A CRLF copy of a clean page gives none; a README with no frontmatter gives none.

### SCAT-FM-REQUIRED
- **Severity:** error. **Fires:** every status. **Runs at:** all; reads its page (and, for none, the vault).
- **Trigger:** `status` or `title` is missing (the fields required from `stub`; `type` is present by definition of a page). One message per field.
- **Messages:**
```
error [SCAT-FM-REQUIRED] <file> field `status`: missing
  Fix: run `scat set-status <page-name> draft` (REPL: `scat_kg.set_status("<page-name>", "draft")`); use `stub` or `done` instead of `draft` if that is the truth
error [SCAT-FM-REQUIRED] <file> field `title`: missing
  Fix: add the line `title: "<Title>"` (the page name with each - replaced by a space and the first letter upper case; reword it if you like)
```
- **Fix kind:** options for `status` (the author knows whether the page is finished; `draft` never overstates), exact for `title` (the contract's own stub title). When `title:` is present but empty the fix reads "replace the line `title:` with `title: "<Title>"`" and the same tail. Edits: `status`: `command{set-status <page-name> draft}`; `title`: `set-field{title, "<Title>"}`.
- **Seed:** `status`, then `title`, removed in turn, each at `stub` and `draft` (a `stub` status excuses neither); a narrative as well as a node page.

### SCAT-FM-TYPE
- **Severity:** error. **Fires:** every status. **Runs at:** all; reads only its page.
- **Trigger:** `type` is present and is a string that is not one of `group`, `concern`, `affordance`, `technology`, `narrative` (the ontology's page types that are Markdown pages: `index` is a type of the ontology, but an index is a generated Base and not a Markdown page, so `type: index` in a Markdown file is a wrong type); or `type` is present but empty. A value that is not a string is SCAT-FM-SHAPE's.
- **Message:**
```
error [SCAT-FM-TYPE] <file> field `type`: `<value>` is not a page type
  Fix: change it to `type: <near match>`            (when a near match among the five types exists)
  Fix, choose the one that describes this page: `type: <key>` ...    (otherwise, one numbered line per type with its `scat:pageDescription`, in alphabetical order)
```
For an empty `type`, `the value is empty, which is not a page type` replaces `` `<value>` is not a page type`` and the list is given. For `index`, the list is given and a note says an index is generated by `scat index`.
- **Fix kind:** options (exact when the near match exists). Edits: one `set-field{type, <key>}` per option.
- **Seed:** `type: Concern` (near match `concern`); `type: gadget` (list); `type:` with no value; `type: index`. A link to the page from a narrative's row gives SCAT-*-END-NOTNODE, besides this error (cascade guard). A file with no `type` is not a page.

### SCAT-FM-STATUS
- **Severity:** error. **Fires:** every status. **Runs at:** all; reads only its page.
- **Trigger:** `status` is present, is a string, and is not `stub`, `draft` or `done`.
- **Message:**
```
error [SCAT-FM-STATUS] <file> field `status`: `<value>` is not a status
  Fix: change it to `status: <near match>`                       (when a near match among stub, draft, done exists)
  Fix, choose one: `status: stub` (just started), `status: draft` (being written), `status: done` (finished)    (otherwise)
```
- **Fix kind:** options. Which status is true is the author's. Edits: one `set-field{status, <value>}` per option.
- **Seed:** `status: Done` (near match); `status: finished` (list). The page gets no "needs status" message.

### SCAT-FM-TIMEFRAME
- **Severity:** error. **Fires:** every status. **Runs at:** all; reads only its page. Narratives only.
- **Trigger:** `timeframe` is present and not empty, is a string, and is not `past`, `future` or `mixed` (the ontology's value set). An empty `timeframe:` is missing, not invalid: see SCAT-DONE-FIELD and SCAT-DRAFT-FIELD. A value that is not a string is SCAT-FM-SHAPE's.
- **Message:**
```
error [SCAT-FM-TIMEFRAME] <file> field `timeframe`: `<value>` is not a timeframe
  Fix: change it to `timeframe: <near match>`                                 (when a near match among the three values exists)
  Fix, choose one: the three values, each as `timeframe: <value>`      (otherwise)
```
- **Fix kind:** options. Edits: one `set-field{timeframe, <value>}` per option.
- **Seed:** `timeframe: Past` (near match) and `timeframe: soon` (list), at `stub`, `draft` and `done`.

### SCAT-FM-KIND
- **Severity:** error. **Fires:** every status. **Runs at:** all; reads only its page. Narratives only.
- **Trigger:** `kind` is present and not empty, is a string, and is not `scenario` or `architecture`. The field is optional: absent or empty is no defect. A value that is not a string is SCAT-FM-SHAPE's.
- **Message:**
```
error [SCAT-FM-KIND] <file> field `kind`: `<value>` is not a kind
  Fix, choose one:
    1. change it to `kind: <near match>`            (only when a near match among scenario, architecture exists)
    2. the two values, each as `kind: <value>`      (when there is no near match; with it, option 1 only)
    n. delete the line `kind: <value>`: a narrative that is neither a scenario nor an architecture leaves `kind` out
```
- **Fix kind:** options. Edits: `set-field{kind, <value>}`; the last option `delete-field{kind}`.
- **Seed:** `kind: Scenario` (near match); `kind: story` (two values and the delete option); `kind:` empty gives none.

### SCAT-FM-SHAPE
- **Severity:** error. **Fires:** every status. **Runs at:** all; reads only its page.
- **Trigger:** `type`, `status`, `title` or `description` (on any page), or `timeframe` or `kind` (on a narrative only), is present and not empty, and is not a single string (a list, a mapping, a number, or a boolean such as an unquoted `yes` or `true`). An unquoted `null` or `~` is missing, by the Empty rule.
- **Message:**
```
error [SCAT-FM-SHAPE] <file> field `<field>`: expected one line of text, found <a list | a mapping | a number | a boolean>
  Fix: replace the field with the line `<field>: "<text>"`          (a one-item list of text: the item; a boolean or number: the value as written, quoted)
  Fix: replace the field with one line of text you write            (otherwise; no exact value exists)
```
- **Fix kind:** exact for a one-item list of text, a boolean and a number; manual otherwise (the intended text is unknowable). Edits: `set-field{<field>, "<text>"}`.
- **Seed:** `title:` as a one-item list (exact), as a mapping (manual), and `title: yes` (exact: `title: "yes"`).

### SCAT-NAME
- **Severity:** error. **Fires:** every status. **Runs at:** all; reads the vault (to find another page of the same name; reported on the page whose `<file>` sorts later, so a check of the earlier one is silent).
- **Trigger:** one of, for a page: (a) its name is not legal (a character outside `a-z`, `0-9`, `-`; a leading, trailing or doubled hyphen; more than 64 characters; a reserved name), which includes names that differ from another only by case; (b) another page elsewhere in the vault has the same name. One message per page.
- **Message:**
```
error [SCAT-NAME] <file> frontmatter: the page name `<page-name>` <is not legal (<reason>) | is also the name of <other-file>>
  Fix: change the file name to `<new-name>.md`, then change the links that meant this page from `[[<page-name>]]` to `[[<new-name>]]`
```
`<new-name>` is the free derived name of the page's `title`. For (a) every link that names `<page-name>` is changed. For (b) two pages share the name, so only the links meant for the renamed page are changed, and the author tells them apart by context; the links meant for the other page keep `[[<page-name>]]`. When the title is missing or its derived name is empty, the fix is "choose a legal name by hand (page contracts section 2)".
- **Fix kind:** exact; manual when no legal name can be derived from the title (the hand choice, no edits). Edits: `rename-file{file, to}`, then one `replace-text` per link to rename (a table cell edited by its `column`).
- **Seed:** `Safe Tool.md`; a 65-character name; `con.md`; `a--b.md`; `safety.md` and `Safety.md` (case only); `x.md` in two folders (one message, on the later path); a page titled "Café menu" (derived name `cafe-menu`); one with a non-Latin title (hand choice).

### SCAT-DONE-FIELD
- **Severity:** error. **Fires:** status `done`. **Needs status.** **Runs at:** all; reads only its page.
- **Trigger:** a field required from `done` is missing: `description` on every page type, `timeframe` on a narrative.
- **Message:**
```
error [SCAT-DONE-FIELD] <file> field `description`: missing on a page with status: done
  Fix, choose one:
    1. <add the line | replace the line `description: <current>` with> `description: "<one sentence you write>"` (author)
    2. run `scat set-status <page-name> draft` (REPL: `scat_kg.set_status("<page-name>", "draft")`) if the page is not finished
```
For `timeframe` the options are one line per value, `<add the line | replace the line `timeframe: <current>` with> `timeframe: <value>``, then the `set-status` option.
- **Fix kind:** slot. The sentence is the author's reading (the tools do not seed it from a title or a first sentence: that would put words in the coder's mouth). `timeframe`: a choice among exact values. Edits: `set-field{description, "<one sentence you write>", author_slot}`; `set-field{timeframe, <value>}`; `command{set-status <page-name> draft}`.
- **Seed:** `description` removed at `done` on a node page and on a narrative; `timeframe` removed, and empty, on a narrative at `done`. At `stub` and `draft` the same pages give no SCAT-DONE-FIELD.

### SCAT-DRAFT-FIELD
- **Severity:** warning. **Fires:** status `draft`; and status `stub` for a field with a value set (`timeframe`), which `scat stub` writes empty so the author sees it. **Needs status.** **Runs at:** all; reads only its page.
- **Trigger:** as SCAT-DONE-FIELD, at those statuses.
- **Message:** the same problem and options, no `set-status` option, because nothing is blocked:
```
warning [SCAT-DRAFT-FIELD] <file> field `description`: missing (required once the page is done)
  Fix: <add the line | replace the line `description: <current>` with> `description: "<one sentence you write>"` (author) before you set status: done
warning [SCAT-DRAFT-FIELD] <file> field `timeframe`: missing (required once the page is done)
  Fix, choose one before you set status: done:
    1. <add the line | replace the line `timeframe: <current>` with> `timeframe: past` (author)
    2. the same with `future`
    3. the same with `mixed`
```
- **Fix kind:** slot. Edits as SCAT-DONE-FIELD, without the command.
- **Seed:** the seeds of SCAT-DONE-FIELD at `draft`: warnings only, the exit status of the check unchanged by them. `timeframe` empty at `stub` (a freshly stubbed narrative gives exactly this one message).

### SCAT-LINK-DANGLING-BODY
- **Severity:** error. **Fires:** every status. **Runs at:** all; reads the vault (names, near match, the cap).
- **Trigger:** a link in a page after the frontmatter whose target is not the name of any page, and that is not a row end: a link in the `from` or `to` cell of a row of a narrative's first table, when the table is well-formed (those are SCAT-*-END-NOPAGE, graded by status, or for a row that is not well-formed, graded by nothing: section 1). A link in a row's `note` cell is a link like any other and is covered here. Targets that are not page links (page contracts 3) are never dangling. Frontmatter links are never read. Three variants share the id: (a) a legal name and no such file; (b) a legal name for which a Markdown file exists that has no `type`, so it is not a page; (c) a name that is not legal, including one that differs from an existing name only by case.
- **Message:**
```
error [SCAT-LINK-DANGLING-BODY] <file>:<line> link [[<target>]]: does not reach a page (<no page is named <target> | <other-file> exists but has no `type`, so it is not a page | <target> is not a legal page name: <reason>>)
  Fix, choose one:
    1. on line <line> replace `[[<target>]]` with `[[<near match>]]`                    (only if a near match exists among all pages)
    2. run `scat stub <target> --type <key>` (REPL: `scat_kg.stub("<target>", type="<key>")`) to create a <key> page      (one numbered option per inferred type)
    n. on line <line> replace `[[<target>]]` with `<target>` to keep the words and drop the link
```
**Inferred types.** A body link does not say what its page is, and the stub operation creates one only for a given type, so the options are alternatives and not a guess: (a) if some row end in the vault names the same target, the layer type that row fixes (all of them, if several, sorted by type key); (b) otherwise the five types `group`, `concern`, `affordance`, `technology`, `narrative`, each a separate numbered exact command. The cap rule: any option that would create a `group` page is withheld when the vault is at its cap, and the message says "the vault is at its cap of <cap> groups, so a new group page would break SCAT-CAP; choose an existing group".
**Variant (b)** (a typeless file of that name): option 2 is replaced by "add these lines to the frontmatter of <other-file>: `type: <key>`, `status: stub`, `title: "<Title>"`", because the stub operation refuses an existing file; only the keys it lacks are listed, a key present but empty is replaced; a file with no frontmatter gets the three lines in a block between two `---` lines at the very top. For an illegal target the file is not what the link meant: variant (c) applies and the message adds "<other-file> exists but is not a page".
**Variant (c)** (not a legal name): no stub of `<target>` is offered, because the stub operation refuses an illegal name. Names are compared without regard to case. The replacement names are collected in this order and deduplicated: the near match among all pages; the derived name of the target when it is not empty. A name that is an existing page is a plain replacement; a name that no `.md` file has is "replace `[[<target>]]` with `[[<d>]]`, then run `scat stub <d> --type <key>`" (one option per inferred type); a typeless file of that name gets the variant (b) lines; a name that is a page of another type gets no option here, because replacing would link the wrong page. A derived name that is empty says "choose a legal name by hand".
- **Fix kind:** options. Edits: `replace-text{line, column, find "[[<target>]]", replace}`; `command{stub ...}` after the edit in a replace-then-stub option (`sequence` true); `set-field` lines for variant (b).
- **Seed:** a body link to a name that a row end elsewhere names (one inferred type); to a name nothing else names (five options); a near match (`safety-briefings` for `safety-briefing`); `[[Safety-Briefing]]` against `safety-briefing` (variant c); `[[Safety briefing]]` with no such page (derived name, replace then stub); a link to a file with no `type` (variant b); a group target at the cap (no group option). `[[photo.png]]`, `[[v1.2-notes]]`, `[[#Heading]]`, a link inside a code fence and a row end linking a missing page give none from this rule. `[[ghost^abc123]]` with no page `ghost` names target `ghost`. A link in a `note` cell to a missing page gives this rule.

### SCAT-CAP
- **Severity:** error. **Fires:** vault level. **Runs at:** vault; at page and one link away when a `group` page is in the set. Reads `scat.toml` and every page.
- **Trigger:** the vault holds more pages of type `group`, at any status, than the integer `stakeholder_group_cap` in `scat.toml` at the vault root (page contracts 10).
- **Message:**
```
error [SCAT-CAP] scat.toml field `stakeholder_group_cap`: the vault holds <n> group pages, over the cap of <cap>: <name>, <name>, ...
  Fix, choose one:
    1. cluster <n minus cap> group(s) into the others, by shared standpoint: move their standpoints into another group's `description`, change every link to them to point at that group, and delete those pages
    2. or, only if the plan allows more groups, write `stakeholder_group_cap = <n>` in scat.toml (the cap protects against identifying individuals)
```
- **Fix kind:** options. Clustering comes first because the facilitation strategy clusters standpoints before it raises a cap. Option 1 is advisory (which groups merge is the facilitator's judgement); option 2 is exact: `set-field{file scat.toml, field stakeholder_group_cap, value <n>}`.
- **Seed:** cap 3 and 4 groups (one message, naming all four); 3 groups (none); the fourth group as a stub still triggers.

### SCAT-CAP-CONFIG
- **Severity:** error. **Fires:** vault level. **Runs at:** as SCAT-CAP.
- **Trigger:** `scat.toml` at the vault root is absent, not valid TOML, lacks `stakeholder_group_cap` at the top level, or its value is not a TOML integer of at least 1 (a string, a float such as `3.0`, and `0` all trigger it).
- **Message:**
```
error [SCAT-CAP-CONFIG] scat.toml field `stakeholder_group_cap`: <the file is missing | the file is not valid TOML: <parser's reason> | the key is missing | the value `<value>` is not a TOML integer of 1 or more>
  Fix: <add the line | replace the line `stakeholder_group_cap = <current>` with> `stakeholder_group_cap = <number you choose>` (author) in scat.toml; choose a whole number of 1 or more (the vault has <n> group pages now, so choose at least <n> if <n> is 1 or more)
```
- **Fix kind:** slot. The cap is a planning decision. Edits: `set-field{file scat.toml, field stakeholder_group_cap, value "<number you choose>", author_slot}`.
- **Seed:** the file removed; a broken line; the key removed; `stakeholder_group_cap = "three"`; `= 0`; `= 2.5`; `= 3.0`.

### SCAT-MENTION
- **Severity:** warning. **Fires:** every status. **Runs at:** all; reads the vault (the titles and names of node pages).
- **Trigger:** the body of a page (narrative or node; a table's `note` cells are included, its `from` and `to` cells are not: those are row ends, judged by SCAT-*-END-NOLINK) contains, as plain text, the `title` or the page name of an existing node page, matched case-insensitively at word boundaries, for a title or name of at least 4 characters, outside code, outside any wikilink, and when the body has no link to that page. Not the page itself. Reported once per page and target, at the first occurrence. No stemming, no plurals.
- **Message:**
```
warning [SCAT-MENTION] <file>:<line>:<column> text `<as written>`: names the <type-key> page [[<page-name>]] but does not link it
  Fix: on line <line> replace `<as written>` with `[[<page-name>|<as written>]]`          (`[[<page-name>]]` when the text is the page name)
```
In a table cell the bar of an alias link is written `\|`: the replacement is `[[<page-name>\|<as written>]]` (page contracts 3).
- **Fix kind:** exact. Edits: `replace-text{line, column, find "<as written>", replace "[[<page-name>|<as written>]]"}`. Linking where a name appears is the coding the narrative needs, and a link adds no edge: only a row does.
- **Seed:** a narrative mentioning a concern's title once in plain text (one message); once plain and once linked (none); inside a code span (none); in a `note` cell (one message); plain text in a `from` cell (none from this rule); a node page mentioning another node's title (one message); the page's own title (none).

### Pairs: the table (SCAT-DRAFT-TABLE-* and SCAT-DONE-TABLE-*)

These six conditions are conformance problems of a narrative's table (page contracts 4, "Other problems of the table").
Each has a warning id and an error id (section 1, status behaviour); the message is the same but for the id and
severity. In the sections below `[SCAT-*-X]` stands for both. **Runs at:** all. **Needs status**, narratives only.

#### SCAT-*-TABLE-HEADER
- **Reads:** its page. **Trigger:** under the heading `Edges told` (page contracts 4 rules for where) the first table's header row does not have the cells `type`, `from`, `to`, `note`, in that order, compared without regard to case and ignoring spaces at their ends; or the line after the header row is not a separator row (`|---|` with or without alignment colons), including when the table is a header row alone. One message per table, even when the header and the separator are both wrong: the header message takes precedence. The rows of such a table are checked by no row rule.
- **Message:**
```
<severity> [SCAT-*-TABLE-HEADER] <file>:<line>:<column> table header: the header row is `<header as written>`, not `| type | from | to | note |`       (the names are wrong, or in another order)
<severity> [SCAT-*-TABLE-HEADER] <file>:<line>:<column> table header: the line after the header row is `<line as written>`, not a separator row       (the names are right and a line follows)
<severity> [SCAT-*-TABLE-HEADER] <file>:<line>:<column> table header: there is no separator row after the header row       (the names are right and the table is the header row alone)
  Fix: replace the line `<header as written>` with `| type | from | to | note |`
  Fix: replace the line `<line as written>` with `|---|---|---|---|`
  Fix: replace the line `<header as written>` with two lines, `<header>` then `|---|---|---|---|`           (no separator row: the second line is a row, or no line follows)
```
In the third fix `<header>` is the right header when the names are wrong, else the header as written. When the header and the separator are both wrong, the fix is one option of two edits, in line order: "replace the line `<header as written>` with `| type | from | to | note |` and the line `<line as written>` with `|---|---|---|---|`". When the header has the four names but in another order, the fix is **advisory** and has no edit: "the columns must be `type`, `from`, `to`, `note`, in this order: move the cells of the header and of every row; the tool never moves cells" (rewriting only the header would make every row misread).
- **Fix kind:** exact when a name is wrong or missing, or the separator is missing or wrong; advisory for the order. Edits: `replace-text{line, find <the line as written>, replace}`; the third form's `replace` holds a line break.
- **Seed:** header `| from | to | type | note |` (advisory); header `| kind | from | to | note |` (exact); header `| type | from | to |`; separator `| a | b |`; separator missing (the second line a row); a header row alone with nothing after it.

#### SCAT-*-TABLE-ROW
- **Reads:** its page. **Trigger:** a row of a well-formed table does not have four cells (page contracts 4, Cells), or does not end with a `|`. A cell is the text between two unescaped `|`, `\|` and a bar inside `[[ ]]` not counting. A row that is not well-formed (section 1) tells no edge, and this is the only rule that judges it.
- **Message:**
```
<severity> [SCAT-*-TABLE-ROW] <file>:<line>:<column> row <n>: the row has <k> cells, not 4 (type, from, to, note)
<severity> [SCAT-*-TABLE-ROW] <file>:<line>:<column> row <n>: the row does not end with `|`
  Fix: <exact fix of the variant>
```
The second message is for variant (b) alone; every other variant, with or without its closing `|`, gets the first. Variants and their fix sentences, as built: (a) three cells, the closing `|` present (the note is missing): "add an empty note: replace the final `|` with `| |`"; (b) four cells and no closing `|`: "write ` |` after the last cell: replace `<last cell>` with `<last cell> |`"; (c) three cells and no closing `|` (`| holds | [[a]] | [[b]]`): "write ` | |` after the last cell, which adds the empty note and the closing bar: replace `<last cell>` with `<last cell> | |`"; (d) more than four cells, choose one: "a `|` inside the note is written `\|`: replace the `|` that opens cell 5 and the ones after it with `\|`" (one edit per bar, right to left; the extra cells are read only as the note), or "delete the row"; (e) fewer than three cells, with or without the closing `|`, choose one: "delete the row", or the advisory "write the row again with four cells and a closing `|`: `| type | from | to | note |`".
- **Fix kind:** exact for (a), (b) and (c); options for (d) and (e). Edits: `replace-text{line, column, find "|", replace "| |"}`; `replace-text{... find <last cell>, replace "<last cell> |"}`; `delete-line{line, find}`.
- **Seed:** `| holds | [[a]] | [[b]] |` (a); `| holds | [[a]] | [[b]] | n` (b); `| holds | [[a]] | [[b]]` (c); `| holds | [[a]] | [[b]] | x | y |` (d); `| holds | [[a]] |` (e).

#### SCAT-*-TABLE-TYPE
- **Reads:** its page, and the pages at its ends (to fix the type from their layers). **Trigger:** the `type` cell of a well-formed row is empty, or is not the verb or the slug of one of the three edge types (`holds`, `is addressed by`, `is provided by`; `holds`, `addressed-by`, `provided-by`), compared without regard to case. The row's ends are still checked by the end rules; its layers are not judged.
- **Message:**
```
<severity> [SCAT-*-TABLE-TYPE] <file>:<line>:<column> row <n> cell `type`: `<value>` is not an edge type (holds, is addressed by, is provided by)
  Fix, choose one:
    1. replace `<value>` with `<verb>`            (when both ends resolve to node pages, in the order of one edge type's layers: that type)
    2. replace `<value>` with `<near match>`      (when a near match among the six spellings exists)
    3. replace `<value>` with `holds`; 4. ... `is addressed by`; 5. ... `is provided by`    (when neither 1 nor 2 applies)
    n. delete the row
```
For an empty cell the message reads `row <n> cell `type`: the value is empty, which is not an edge type (holds, is addressed by, is provided by)` and each option reads "replace the empty cell with `<verb>`".
- **Fix kind:** options (a single exact option 1 is still printed with the delete option). Edits: `replace-text{line, column, find <value>, replace <verb>}` (an empty cell: the whole row line as `find`); `delete-line{line, find}`.
- **Seed:** `| owns | [[g]] | [[c]] | |` with a group and a concern (option 1); `| holdz | ... |` (near match); an empty cell; a row of two unresolved ends (options 3 to 5).

#### SCAT-*-TABLE-LAYERS
- **Reads:** its page, and the pages at its ends. **Trigger:** the `type` cell is an edge type, and at least one end resolves to a node page of a layer other than the one the type fixes for that end. It covers a pair written the wrong way round and a pair between layers that are not neighbours (a group and an affordance). One message per row, naming each wrong end.
- **Message:**
```
<severity> [SCAT-*-TABLE-LAYERS] <file>:<line>:<column> row <n>: `<verb>` joins a <from-key> to a <to-key>, but [[<from>]] is a <actual> page<, and [[<to>]] is a <actual> page>
  Fix, choose one:
    1. swap the two ends: replace `[[<from>]] | [[<to>]]` with `[[<to>]] | [[<from>]]`        (only when each resolved end is of the layer the other end should have: the pair is written the wrong way round)
    2. replace `<verb>` with `<verb of the type whose layers are these>`        (only when the two layers, in this order, are those of another edge type)
    3. none of the three edge types joins a <actual> to a <actual>: tell it as two rows through a node between them (advisory)      (only when neither 1 nor 2 applies)
    n. delete the row
```
Options 1 and 2 cannot both apply. The swap's `find` is the text from the first character of the `from` cell's content to the last of the `to` cell's content, as written (the padding and the bar between them included, kept in place).
- **Fix kind:** options. Edits: `replace-text{line, column of the from cell, find, replace}`; `replace-text` on the `type` cell; `delete-line{line, find}`.
- **Seed:** `holds` with a concern and a group (swap); `holds` with a concern and an affordance (retype to `is addressed by`); `holds` with a group and an affordance (option 3); one end resolved and wrong, the other unresolved (only the wrong end named).

#### SCAT-*-TABLE-SECOND
- **Reads:** its page. **Trigger:** a narrative has a second heading named `Edges told` (any level, compared as page contracts 4 says), or a second table under the heading whose first table is read. Only the first table under the first such heading is read; the rows of any other tell no edge, which the author may not have meant. One message for each such heading or table, anchored on the heading line (a second heading) or on the header row of the table (a second table).
- **Deliberately unreported:** a heading spelled in any other way (`Edges`, `Edge told`) and a table on a page that is not a narrative are not read and nothing is reported: the tool cannot tell a misspelled heading from other text, and a table elsewhere is the author's own text.
- **Message:**
```
<severity> [SCAT-*-TABLE-SECOND] <file>:<line>:<column> table: a second <heading `Edges told` | table> on this narrative; only the first table under the first `Edges told` is read, so its rows tell no edge
  Fix, choose one:
    1. move the rows you want into the first table (line <m>), then delete this <heading and> table           (advisory)
    2. replace the heading `<heading as written>` with `<heading you choose>` (author), so it is no longer an `Edges told` heading           (a second heading only)
```
- **Fix kind:** options. Edits: option 2 `replace-text{line, find <heading as written>, replace "<heading you choose>", author_slot}`; option 1 none.
- **Seed:** a narrative with two `## Edges told` headings and a table under each (one message, on the second heading); two tables under one heading (one message, on the second header row); a heading `## Edges tolds` and a table on a concern page (none).

#### SCAT-*-TABLE-DUPLICATE
- **Reads:** its page. **Trigger:** a well-formed row has the same edge type (verb and slug compared as one), the same `from` target and the same `to` target as an earlier row of the same narrative. Each later row is reported once, against the first. Rows whose ends are not links are not compared. The same pair in two narratives is not a duplicate: it is two tellings of one edge.
- **Message:**
```
<severity> [SCAT-*-TABLE-DUPLICATE] <file>:<line>:<column> row <n>: tells the same edge as row <m> (`<verb>`, [[<from>]], [[<to>]]); a narrative tells an edge once
  Fix: delete the row `<row as written>`          (when the row has a note, the sentence goes on: (if its note `<note>` is worth keeping, put it in the note of row <m> first))
```
- **Fix kind:** exact. Edits: `delete-line{line, find <row as written>}`.
- **Seed:** two identical rows; the same pair once as `holds` and once as the slug `holds`; a third copy (two messages); the same pair in two narratives (none).

### Pairs: the mismatches (SCAT-DRAFT-END-* and SCAT-DONE-END-*)

A mismatch (R-23) is a link and an edge that should agree and do not. In the row model it happens at a row end, and
page contracts 4 names the cases: an end that is not a link, and an end that is a link reaching no page or a page that
is not a node. These are graded as pairs: a warning while the narrative is `stub` or `draft` (R-3), an error once it
is `done`. A mismatch is always anchored on the narrative, at the cell. The knowledge graph has no row for an end that
is not a node, so the narrative's fingerprint does not include it. **Runs at:** all. **Needs status**, narratives only.
A table with a malformed header, and a row with the wrong number of cells, are not checked here (cascade guard).
A duplicated row, a row in the wrong direction and a row between the wrong layers are *other problems* of the table (page contracts 4), covered under the pair E-N rules (section 6); they are not mismatches, and R-23's closed list is the three end rules.

#### SCAT-*-END-NOLINK
- **Reads:** its page, and the vault when it looks for pages of the layer. **Trigger:** a `from` or `to` cell is not exactly one link: (a) it is empty; (b) it holds text and no link; (c) it holds more than one link, or a link beside other text. An embed `![[name]]` is one link, and an alias link is one link.
- **Message:**
```
<severity> [SCAT-*-END-NOLINK] <file>:<line>:<column> row <n> cell `<from|to>`: `<cell as written>` is not a link; each end of a row is one link, `[[page-name]]`
<severity> [SCAT-*-END-NOLINK] <file>:<line>:<column> row <n> cell `<from|to>`: the cell is empty; each end of a row is one link, `[[page-name]]`       (a: the empty cell)
  Fix, choose one:
    1. replace `<text>` with `[[<name>]]`                       (b: when a page of the layer's type has that name, or the derived name of the text; one option per candidate, near match first)
    2. replace `<text>` with `[[<d>]]`, then run `scat stub <d> --type <layer key>` (REPL: `scat_kg.stub("<d>", type="<layer key>")`)       (b: when no page has the derived name <d> and the layer is known; two steps)
    3. replace the empty cell with `[[<node you choose>]]` (author)       (a)
    4. replace the cell with `<one link of it>`; any text beside it belongs in the `note` cell by hand      (c: one option per link)
    n. delete the row
```
Variant (c) uses the first message, "is not a link", though a link is there: the cell is not exactly one. When the layer is not known (the `type` cell is not an edge type, SCAT-*-TABLE-TYPE) options 2 are withheld, and 1 offers only existing pages. The cap rule of SCAT-LINK-DANGLING-BODY applies to a stub of a `group`.
- **Fix kind:** options (a: slot among the options). Edits: `replace-text{line, column, find <text>, replace "[[<name>]]"}`; `command{stub <d> --type <layer key>}` as the second step of option 2 (`sequence` true); `delete-line{line, find}`; an empty cell: the whole row line as `find`, `author_slot` the placeholder.
- **Seed:** `| holds | borrowers | [[c]] | |` where `borrowers` is an existing group's page name (option 1) and where it is not (option 2); `| holds | | [[c]] | |` (empty); `| holds | [[a]] and [[b]] | [[c]] | |` (c); the same defect on the `to` cell.

#### SCAT-*-END-NOPAGE
- **Reads:** its page and the vault. **Trigger:** a row end is one link whose target is not the name of any page: the variants (a), (b) and (c) of SCAT-LINK-DANGLING-BODY. The type is known from the row, so the stub is exact. A row end whose layer is unknown (the `type` cell is not an edge type) is covered by the variants without a stub.
- **Message:**
```
<severity> [SCAT-*-END-NOPAGE] <file>:<line>:<column> row <n> cell `<from|to>`: [[<target>]] does not reach a page (<reason as in SCAT-LINK-DANGLING-BODY>)
  Fix, choose one:
    1. replace `[[<target>]]` with `[[<near match>]]`        (only if a near match exists among the pages of the layer's type)
    2. run `scat stub <target> --type <layer key>` (REPL: `scat_kg.stub("<target>", type="<layer key>")`) to create a <layer key> page      (variant a; the layer key is the type the row fixes, as page contracts 6 says)
    n. delete the row
```
Variant (b) replaces option 2 by the lines that make the typeless file a page of the layer's type; variant (c) takes the replacement and replace-then-stub options of SCAT-LINK-DANGLING-BODY, with the layer's type as the one inferred type. The cap rule applies to a `group` layer.
- **Fix kind:** options. Edits as SCAT-LINK-DANGLING-BODY, with `column` on the `replace-text`; `delete-line{line, find}`.
- **Seed:** `| holds | [[ghost]] | [[c]] | |` (options 1 only if a near match, 2, delete); a near match (`[[borrower]]` for `borrowers`); `[[Safety briefing]]` (variant c); a link to a typeless file (variant b); a group stub at the cap (no group option).

#### SCAT-*-END-NOTNODE
- **Reads:** its page, the vault and the target's page. **Trigger:** a row end is one link whose target is a page that is not a valid node: a page of type `narrative`, or a page whose `type` is missing from the five or invalid (that page has its own SCAT-FM-TYPE error as well; this is the mismatch, at the row). A node page of the wrong layer is SCAT-*-TABLE-LAYERS.
- **Message:**
```
<severity> [SCAT-*-END-NOTNODE] <file>:<line>:<column> row <n> cell `<from|to>`: [[<target>]] is <a narrative page | a page with the invalid type `<value>` | a page with an empty `type`>, not a node; a row joins two nodes
  Fix, choose one:
    1. replace `[[<target>]]` with `[[<candidate>]]`        (one option per candidate for the end's layer; withheld when the layer is unknown)
    2. replace `[[<target>]]` with `[[<node you choose>]]` (author)        (when there is no candidate)
    n. delete the row
```
- **Fix kind:** options. Edits: `replace-text{line, column, find "[[<target>]]", replace}`; `delete-line{line, find}`.
- **Seed:** `| holds | [[a-narrative]] | [[c]] | |` with and without candidate groups the narrative links elsewhere; a link to a page with `type: gadget` (this message, and the page's own SCAT-FM-TYPE).

## 4. Rule 4 has no rule

Architecture section 4, rule 4 (the *candidate*): a narrative that links both ends of a pair and has no row for it.
**There is no rule, no id and no message for it, at any status, scope or severity** (D-085 (a), D-088). A link says
"see also"; an edge is about the relationship being in the narrative and not only its two ends, so a narrative that
has not said it tells the edge has not told it, and conformance does not judge content (R-1). Only the fingerprint
view lists such a pair as a candidate. Seed (a test for the absence): a narrative linking a group and a concern that
are not joined by any row, at every status and at every scope, gives zero messages, and a table with a row for the
pair gives zero as well. A row alone, with its ends linked, is conformant.

## 5. The done check

Setting a page to `done` is judged as the page would stand at `done`, and refused while it would fail (page contracts
1; architecture M5). `SCAT-DONE-REFUSED` is the rule that gives the refusal: an operation rule, not a check rule, so it
is not in the section 3 table and no `scat check` ever prints it.

- **Severity:** a refusal (`ok` false, nothing written). **Fires:** `set-status <page> done` only; setting `stub` or
  `draft` is never refused. **Runs at:** page, with one link away: the check is page-scope on the page as at `done`,
  and the pages one link away are read (the nodes at a narrative's row ends) but add nothing: no rule reports on one
  page by reason of another page's status, so a page's status never changes what a rule says about its neighbour.
- **What is judged:** every rule is run on the page with its status taken as `done`: the `SCAT-DONE-` ids replace the
  `SCAT-DRAFT-` ids, so the page's required fields (`description`; `timeframe` for a narrative) and each row of its
  table must be conformant. A page whose `status` is missing or invalid is judged as `done` too (the refusal lists the
  status error with the rest, and the fix of that error is the `done` the author asked for or another status).
- **What is listed:** every problem of error severity the page would have at `done`, each exactly as `scat check`
  prints it for that page at `done`, in the catalogue's order, with its fix. Warnings are not listed: they do not block.
  With no errors, `done` is set and the result is an ordinary operation result.
- **Message:**
```
refused [SCAT-DONE-REFUSED] <file>: <n> error(s) would stand at status done; status unchanged
  <the n problems, each as `scat check` would print it at done, indented>
  Fix, choose one:
    1. fix the problems above, then run `scat set-status <page-name> done` again
    2. leave the page at `draft`: run `scat set-status <page-name> draft` (REPL: `scat_kg.set_status("<page-name>", "draft")`)
```
- **Fix kind:** options: option 1 advisory (the fixes that matter are each listed problem's own), option 2 exact (`command{set-status <page-name> draft}`, with its REPL twin). Data: a `Refusal` with `subject` the file, `why`, `rule` `SCAT-DONE-REFUSED`, `problems` the list, and `fix` of those two options.
- **Vault-wide errors are not listed:** an error of SCAT-CAP or SCAT-CAP-CONFIG, though it runs at page scope when the page is a `group`, does not depend on this page's status and is not in the refusal's `problems`; a `group` page with no other error is set to `done` in a vault over its cap, and `scat check` reports the cap.
- **Seed:** a narrative at `draft` with a row end that is not a link and no `description` (set `done`: refused, listing SCAT-DONE-FIELD and SCAT-DONE-END-NOLINK, and the file unchanged); the same narrative with both fixed (set: done); a node page with no `description` (refused); a narrative with only warnings at `done` (a SCAT-MENTION, set); a page with an invalid `status` (refused, the status error listed).

`record-edge` and `remove-edge` have their own refusals (a narrative they would change is `done`; an unknown type; ends
in the wrong layers), carried as operation refusals with no rule id; they list no problems of the check.

## 6. Coverage

| Requirement | Rules |
|---|---|
| R-2 every message names the file, the place and the rule, and gives the fix | every rule: the message format and fix of section 1, checked by the golden tests of section 3 |
| R-1 required fields and types | SCAT-FM-PARSE, SCAT-FM-REQUIRED, SCAT-FM-TYPE, SCAT-FM-STATUS, SCAT-FM-TIMEFRAME, SCAT-FM-KIND, SCAT-FM-SHAPE, SCAT-DONE-FIELD |
| R-1 page names (page contracts 2) | SCAT-NAME |
| R-1 links to pages that do not exist | SCAT-LINK-DANGLING-BODY; at a table end SCAT-DRAFT-END-NOPAGE, SCAT-DONE-END-NOPAGE |
| R-1 the table of edges (page contracts 4) | SCAT-*-TABLE-HEADER, -ROW, -TYPE, -LAYERS, -DUPLICATE, -SECOND |
| R-1 the group cap | SCAT-CAP, SCAT-CAP-CONFIG |
| R-3 unfinished is never an error | SCAT-DRAFT-FIELD, and every SCAT-DRAFT- pair id, as warnings; nothing else fires for `done` fields at `stub` or `draft` |
| R-3 full contract at `done`; the `done` check | SCAT-DONE-FIELD, every SCAT-DONE- pair id, SCAT-DONE-REFUSED |
| R-4 checks never write | none: no rule writes (section 1, Scopes); the operations are `stub`, `set-status`, `record-edge`, `remove-edge` and `index` |
| R-8 fixes as data | every rule: a fix kind and its edits (the machine interface) |
| R-23 mismatches | SCAT-*-END-NOLINK, -NOPAGE, -NOTNODE (and the table above); rule 4: none, section 4 |
| Unlinked-mention warning (basic) | SCAT-MENTION |

**R-23: the six pairs of form (architecture section 4), as they fall in the row model.** The four forms: L is a
narrative's link to a node; E is an edge's entry; N is the edge's references to its two nodes; T is the edge's
references to its narratives. In this layout E, N and T are one thing, a row of a narrative's table: the row is the
edge's telling, its two end cells are N and the narrative whose page holds the row is T. There is no stored edge to
disagree with the rows, so the graph holds one edge per (type, from, to) by construction.

| Pair | What disagrees, in the row model | Rule, or why it cannot occur |
|---|---|---|
| **L-N** | An edge's end and the narrative's link to it: a row end that is not a link, or whose link reaches no page or a page that is not a valid node (a narrative, or a page with an invalid `type`) | SCAT-DRAFT-END-NOLINK / SCAT-DONE-END-NOLINK, SCAT-DRAFT-END-NOPAGE / SCAT-DONE-END-NOPAGE, SCAT-DRAFT-END-NOTNODE / SCAT-DONE-END-NOTNODE: warning until the narrative is `done`, then an error, anchored on the cell. A narrative that has a row cannot fail to link an end that is a link: the end cell is the link |
| **L-T** | An edge names a narrative that links neither end | Cannot occur in this layout, because T is the page the row sits on and the row's ends are links on that same page. Its nearest case, a row whose two ends are not links, is two messages of SCAT-*-END-NOLINK, one per cell |
| **L-E** | A narrative links both ends of an edge and has no row for it | No rule and no message (D-085, section 4). The fingerprint view lists the pair as a candidate |
| **E-N** | An end is missing, or in the wrong layer, or two entries join one pair | Missing end: SCAT-*-END-NOPAGE (no page), SCAT-*-END-NOLINK (no link), SCAT-*-END-NOTNODE (not a valid node: a narrative, or a page with an invalid `type`). Wrong layer or direction, or layers not neighbouring: SCAT-*-TABLE-LAYERS. Unknown type: SCAT-*-TABLE-TYPE. Two rows joining one pair in one narrative: SCAT-*-TABLE-DUPLICATE. Two entries joining one pair across narratives cannot occur, because the graph keeps one edge per (type, from, to) and names the narratives |
| **E-T** | An edge names no narrative, or one that is absent or not a narrative | Cannot occur in this layout, because an edge exists only as a row on a narrative's page; no row, no edge, so no edge is left naming nothing, and the narrative it names is the page it is read from. A table on a page that is not a narrative is not read |
| **N-T** | The edge is `done` but a narrative it names lacks a link | Cannot occur as a separate problem, because an edge has no file to anchor it. The problem is the narrative's mismatch (the L-N rules), an error on the narrative once it is `done`; an edge is `done` only when every narrative telling it is `done`, so each such mismatch is already an error there; and the refusal to set `done` (section 5) holds it back first |

**Ontology coverage map.** One line per field of the ontology: `<kind> <type-key>.<field> -> <rule ids>`; `*` stands for the
pair's two ids. It is checked against `ontology/scat.ttl` by a script. Every required and optional field of every page
type of the ontology must appear.

```
required group.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING-BODY
required group.status -> SCAT-FM-REQUIRED, SCAT-FM-STATUS
required group.title -> SCAT-FM-REQUIRED
required group.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required concern.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING-BODY
required concern.status -> SCAT-FM-REQUIRED, SCAT-FM-STATUS
required concern.title -> SCAT-FM-REQUIRED
required concern.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required affordance.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING-BODY
required affordance.status -> SCAT-FM-REQUIRED, SCAT-FM-STATUS
required affordance.title -> SCAT-FM-REQUIRED
required affordance.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required technology.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING-BODY
required technology.status -> SCAT-FM-REQUIRED, SCAT-FM-STATUS
required technology.title -> SCAT-FM-REQUIRED
required technology.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required narrative.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING-BODY
required narrative.status -> SCAT-FM-REQUIRED, SCAT-FM-STATUS
required narrative.title -> SCAT-FM-REQUIRED
required narrative.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required narrative.timeframe -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD, SCAT-FM-TIMEFRAME
optional narrative.kind -> SCAT-FM-KIND
table-heading narrative.Edges-told -> SCAT-*-TABLE-HEADER, SCAT-*-TABLE-SECOND
table-column narrative.type -> SCAT-*-TABLE-TYPE, SCAT-*-TABLE-LAYERS, SCAT-*-TABLE-DUPLICATE
table-column narrative.from -> SCAT-*-END-NOLINK, SCAT-*-END-NOPAGE, SCAT-*-END-NOTNODE, SCAT-*-TABLE-LAYERS, SCAT-*-TABLE-DUPLICATE
table-column narrative.to -> SCAT-*-END-NOLINK, SCAT-*-END-NOPAGE, SCAT-*-END-NOTNODE, SCAT-*-TABLE-LAYERS, SCAT-*-TABLE-DUPLICATE
table-column narrative.note -> SCAT-LINK-DANGLING-BODY, SCAT-MENTION, SCAT-*-TABLE-ROW
edge-type holds -> SCAT-*-TABLE-TYPE, SCAT-*-TABLE-LAYERS
edge-type addressed-by -> SCAT-*-TABLE-TYPE, SCAT-*-TABLE-LAYERS
edge-type provided-by -> SCAT-*-TABLE-TYPE, SCAT-*-TABLE-LAYERS
```

`index` has no fields and is no Markdown page: no rule reads it.

## 7. Needs from the ontology and the page contracts

Nothing blocks. Points for the PM, none fixed here (the contract and the ontology are other units' work):
- Page contracts 4 lists "an end that is not a link" as the mismatch, and says an end holds "exactly one link and nothing else". The catalogue reads a cell that is empty, has text only, or has several links or text beside one link as that mismatch (SCAT-*-END-NOLINK, variants a to c).
- The ontology lists `index` among the `scat:key` types. A Markdown file with `type: index` is a wrong type here (SCAT-FM-TYPE).
- Page contracts 10 and `scat.toml` still call the cap `stakeholder_group_cap`; the catalogue keeps the key and says "group" everywhere else.
- Architecture section 4, rule 2 (an edge names at least one narrative) and rule 1's "one entry per pair" are moot in this layout, because an edge is its rows; the architecture's wording of M3 and M4 will want the same change.
- Architecture M4 says severity is given by paired rule ids; this catalogue does so (SCAT-DRAFT-X and SCAT-DONE-X).

## 8. Machine interface: edge operations, table problems and the changes from version 1

Moved from `contracts/machine-interface.md`, which keeps the promises and points here. The objects are defined in
`contracts/machine-interface.schema.json`.

**Edge operations.** `record-edge` and `remove-edge` (the operations table in section 1 gives their forms) return an
operation document. An edge is no page: it is the rows of narratives, so the result says which rows the call wrote.
- `edge` is the edge as the call leaves it: `type` (the slug; for `remove-edge`, the type its ends' layers fix), `from`,
  `to`, and `narratives`, every narrative that has a row for it afterwards, in byte order. After a `remove-edge` that
  took the last row, `narratives` is empty: the edge is gone from the graph.
- `rows_added` and `rows_removed` list the rows written and deleted, each with its `narrative`, `file`, `line` and
  `note`. The line of an added row is its line in the file as written; the line of a removed row is its line before
  the write. Both are empty when the call found nothing to do: `ok` is true and the narratives are in `unchanged`.
- Stubs the call created (a missing end node or narrative) are in `created`; narratives it wrote a row into are in
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

**Table problems and the refusal to set `done`.** A problem about a table or a row of it has `field` null, `line` the
line of the row (of the header row, for the header), `column` the first character of the cell it is about (of the
first `|`, for a whole row), and a `where` such as ``row 2 cell `to` ``. A row is removed by a `delete-line` edit; a
cell is corrected by a `replace-text` edit with a `column`. A refusal to set a page to `done` (`set-status`) has
`rule` `SCAT-DONE-REFUSED` and `problems`: the errors the page would have at status `done`, each with its own fix. Its
own `fix` is two options: an advisory one, and `set-status <page> draft` as an exact command.

**Detail of the promised fields.** `field` of a problem is a frontmatter field or a key of `scat.toml`, and null for
a link, a table or row, a name or all frontmatter. `repeat` is the number of identical messages a problem stands for.
`counts` of a status result is per status, and `other`. `problems` of an operation is what the write leaves, one link
away. `problems` of a refusal is the problems that make it, each with its fix. `to_dict()` of a result returns exactly
the data the CLI prints.

**Changes from schema version 1 to version 2.** The version bumps because a closed list gains a value and a field
goes; the rest is additive. The reason for all of it is D-088: an edge is a row of a narrative's table, not a page,
and there are no raw and coded pairs, relation pages or class pages.

| Change | Kind | Why |
|---|---|---|
| New edit action `delete-line` | closed list gains a value: bumps | A table row is a whole line; `replace-text` cannot remove one without leaving an empty line, which ends the table. Row insertion needs no action: `replace-text` with a line break in `replace` (and, for a new table, an anchor on the last line of the file) covers it, and no catalogue fix inserts a row |
| `counts` of a status result no longer has `none` | field removed: bumps | It counted pages of version 1 that carried no status (class pages). Every type has a status now (an index page is generated, not authored: `index` has no fields), so the count is always 0 |
| `StatusRow.type` takes the five types `group`, `concern`, `affordance`, `technology`, `narrative` (version 1: the twelve) | meaning of values changes: bumps | The ontology's types changed |
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
