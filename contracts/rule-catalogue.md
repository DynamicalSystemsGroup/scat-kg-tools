# SCAT rule catalogue (WP4-D3)

What a check looks at, at what severity, and what each message tells the user to do. It serves goal WP4-G3 and
requirements R-1 to R-4 and R-8 of the mission. The TBox (`ontology/scat.ttl`) says what a conformant page is; this
file says how a departure is graded and worded. The page contracts (`contracts/page-contracts.md`) say how pages
are named, written and linked, and which pages a link entails. This file uses their conventions and does not
restate them; where it needs one it names the contract section.

Every rule has an id, a severity (`error` blocks, `warning` does not), a trigger a test can produce, and a message
that names the file, the field or link, and the rule id, and gives a fix. A fix is **exact** (a command, or an
exact field and value) or the rule records why it cannot be.

## 1. Conventions every rule shares

**Page terms.** A page is a Markdown file, anywhere in the vault outside folders whose name starts with a dot (`.obsidian`,
`.trash`), whose frontmatter has a `type` key (contract section 1); any other Markdown file is not a page and is ignored. `<file>` is the vault-relative path of the page, with `/` separators,
for example `concern/safe-handling-of-tools.md`. `<page-name>` is the file name without `.md`, unique across the
vault (contract section 2). `<type-key>` is the value of a page's `type` field (`scat:key` of its page type). A
*link field* is a field with a `scat:targetType`: a list of wikilinks, or exactly one wikilink when `scat:single` is
true (a relation page's endpoint fields `group`, `concern`, `affordance`, `technology`). An *item line* is
`- "[[<target>]]"` in a list field and `<field>: "[[<target>]]"` in a single field. `<item>` in a message is the item line as written in the file, and `<item with X>` the same line with the target replaced by `X`. A *relation page* is a page of
type `heldby`, `addresses` or `attributes`. A *body link* is a wikilink in the page after the frontmatter, read as the contract's section 3 says: `|alias`, `#heading` and `^block` are stripped and what remains is the page name, so `[[page^block]]` is a link to the page `page`
and must exist; an embed counts; text in matched code spans and fenced code blocks is never a link; and a target containing a dot or a `/`, and a link whose name is empty after the stripping (`[[#Heading]]`, `[[^id]]`), are not page links and are not checked; the dot, `/` and empty-name tests apply after stripping `|`, `#` and `^` (a Markdown-style `[text](target)` is not a wikilink). A link's *target* is
the name inside the brackets. A page's *status* is `stub`, `draft` or `done`. A page type with
`scat:carriesStatus false` (the class page) is treated as `done` by every status rule below.

**Legal name and derived name.** A name is *legal* when it satisfies the contract's slug rule (section 2: `a-z`,
`0-9` and single hyphens, starting and ending with a letter or digit, at most 64 characters, not a reserved
name, `con`, `prn`, `aux`, `nul`, `com0` to `com9`, `lpt0` to `lpt9` and the seven class page names). The *stem* of a text is steps 1 to 3 of the contract's name-from-title rule applied to it (empty when step 3 leaves
nothing), and its *free derived name* is the name step 4 gives (a numeric suffix until the name is free, a reserved name
counting as taken, as is the name of any existing `.md` file, a page or not); a derived name is always legal. Where a rule says "derived name" without "free", it means the stem,
or the free derived name when the stem is reserved.

**Scopes.** A check runs at page, neighborhood or vault scope (G4). A rule reports on one file, and a page-scope
check of that file runs every rule that reports on it, reading other pages when the rule needs them. The same page
gives the same messages at every scope. The vault-level rules (SCAT-CAP, SCAT-CAP-CONFIG) run at vault scope, and
at the other two scopes when a stakeholder-group page is in the checked set. Checks never write (R-4).

**Cascade guard.** A file that starts with a `---` line but fails SCAT-FM-PARSE is checked by no other rule as a
source. A page whose `type` is invalid is checked by no rule that needs its type. A link whose target page has an
invalid `type` is not endpoint-checked (the target already has its own error). A page whose `status` is missing or
invalid is checked by no rule marked "needs status"; the status error is reported once, on the page.

**Empty.** A field is *missing* when the key is absent or its value is null, an empty or blank string, or an empty
list. A link field that is present and empty is not an error by itself, except where a rule says the field is
required. "Present and non-empty" is the one reading used for every rule that says "carries" or "present" about a
link field.

**Add or replace.** A fix that writes a line for a field says "add the line `X`" when the key is absent, and "replace the
line `<field>: <current>` with `X`" when the key is present but empty (`<current>` is the text after the colon as
written, or nothing). Messages below show the "add" wording and carry this rule; where the "replace" wording differs
it is shown.

**Status behaviour (R-3), in one table.**

| Kind of rule | stub | draft | done |
|---|---|---|---|
| Required from `stub` (`status`, `title`, `indexes`, and a relation page's endpoint fields) | error | error | error |
| Required from `done` (`description`, required link fields) | silent | warning | error |
| Name, link shape, unlisted link, endpoint, dangling link (frontmatter and body) | error | error | error |
| Discouraged field, discouraged body link, conflict, self-conflict, duplicate relation page, mention, backlink, index | warning | warning | warning |
| SCAT-RAW-UNCODED | silent | silent | warning |
| Cap | error | error | error |

An unfinished page is never an error for being unfinished: nothing in the `done` row is an error before `done`.

**Order and format.** Messages sort by file path (byte order), then line (a message with no line sorts before the messages with one), then
column (only SCAT-MENTION has one; messages without sort first), then rule id, then the field or link key in the order
the page's file lists them, then the target name (byte order), then the field name (byte order; the last resort for messages with neither a line nor a target, such as two missing fields). Messages that are identical in rule, file, line and text (the same body link twice on one line, the same item twice in a flow list) are printed once, with ` (x<n>)` appended to the first line, so no two messages compare equal and the order is total. The format:

```
<severity> [<rule-id>] <file>[:<line>] <where>: <what is wrong>
  Fix: <one exact fix>
```
or, when the fix is a choice between exact alternatives:
```
  Fix, choose one:
    1. <exact fix>
    2. <exact fix>
```
`<severity>` is `error` or `warning`. `<line>` is the 1-based line of the link item or the field key; it is given
for link rules and omitted for field-level rules. SCAT-MENTION prints `<file>:<line>:<column>`, the 1-based column, counted in characters (code points), of the first character of the text. `<where>` is ``field `<name>` ``, ``link [[<target>]]`` or
`frontmatter`. Angle-bracket words are filled in by the tool, except a slot marked *(author)*, which stays in the
message literally because only the author can fill it. An *edit* fix says exactly which lines to write, replace or
delete. An *operation* fix names a command and its REPL twin on one line, as in ``run `scat set-status <page-name>
draft` (REPL: `scat_kg.set_status("<page-name>", "draft")`)``. The same text is printed on both paths (R-8).

**Operations the fixes name.** WP5 implements them. Their forms below are the contract of the message text only.

| Operation | CLI form | REPL form | What the messages rely on |
|---|---|---|---|
| stub | `scat stub <page-name> --type <type-key>` | `scat_kg.stub("<page-name>", type="<type-key>")` | Creates the page as the contract's section 5 says: `status: stub`, title from the name. Accepts only the four class keys and the record keys `scenario-raw`, `scenario-coded`, `architecture-raw`, `architecture-coded`, and refuses an illegal name and any name that is already an existing `.md` file (a page or not). It derives the opposite raw/coded link itself, on the new page only: creating a raw page writes `coded` on the new page, listing every coded page that names it in `raw`; creating a coded page writes `raw` on the new page, listing every raw page that names it in `coded`. Existing pages are never written, and the caller names no entailing page. |
| set-status | `scat set-status <page-name> <status>` | `scat_kg.set_status("<page-name>", "<status>")` | Sets `status`, adding the key if absent. |
| stub-pair | `scat stub-pair <relation> <endpoint-a> <endpoint-b>` | `scat_kg.stub_pair("<relation>", "<endpoint-a>", "<endpoint-b>")` | Creates a relation page for a named pair as the contract's section 5 says (and stubs a missing endpoint); `<relation>` is `heldby`, `addresses` or `attributes`, the endpoints are in the order of the relation (group, concern; concern, affordance; affordance, technology). Creates nothing, and reports the existing page, when a page of that relation already has that pair. |
| index | `scat index` | `scat_kg.index()` | Rewrites the generated region of every class page, creating a missing class page (contract section 8). |

A relation page is created from a pair the author names (contract section 5, log D-031), with the stub-pair operation
above. No message in this catalogue names it.

**Near match.** For a text `a` and a list of names, the near match is the name `b` with the highest
`difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()`, if that ratio is at least 0.8; ties go to the name
first in byte order. No near match means none.

**Suggestions (never required, never written).** Where a message offers pages to link, they come from relation
pages the vault already has, are sorted by page name in byte order, leave out pages already listed in the field,
show at most 8 (a ninth and later page is replaced by one final line `(+<n> more)` after the list), and are labelled as suggestions the author confirms. A suggestion never
changes a rule's trigger or severity. `S(<field>)` for a page P is:

| Field | Suggested pages |
|---|---|
| `groups` | the `group` of each `heldby` page whose `concern` is listed in P's `concerns` |
| `concerns` | the `concern` of each `heldby` page whose `group` is listed in P's `groups` |
| `affordances` | the `affordance` of each `addresses` page whose `concern` is listed in P's `concerns` |
| `technologies` | the `technology` of each `attributes` page whose `affordance` is listed in P's `affordances` |
| `raw` | raw pages of the field's target type whose `coded` lists P |
| from P's discouraged `technologies` | the `affordance` of each `attributes` page whose `technology` is listed there |
| from P's discouraged `groups` | the `concern` of each `heldby` page whose `group` is listed there |

## 2. The four decisions

Each was open in `research/toolchain/measurements.md` ("What it takes to make each fix exact").

**(1) Missing field: the fix is an author slot plus an exact way out.** The prose of `description` is the
author's, so no fix can be exact for it, and the tools do not write it: seeding it from a title or a first
sentence would put words in the coder's mouth, against the facilitation stance. The message gives two alternatives
and picks neither: write the line (the sentence is a marked slot), or run `set-status <page-name> draft` (exact,
and honest: the page is not finished). Options (a) and (c) of the measurements are the second alternative; (b)
(seeding) is rejected. A missing `title` is the one exact case: the contract gives the title a stub gets (the name
with each `-` replaced by a space and the first letter upper case), so the message gives that. Class pages have no
status, so only the first alternative is offered there.

**(2) Wrong endpoint: numbered replacements in a fixed order.** Let `W` be the wrong target, `T` the field's
target type and `P` the page. The options, in this order, are:
1. *Move* (list fields): if `P`'s page type lists, as required or optional, a list field whose target type is `W`'s
   type and `W` is not already in it, move the line there. *Swap* (a relation page): if both endpoint fields hold
   a page of the other's type, one message for the pair prints the two resulting lines literally, and there is no
   other option. (The common slip is the right page in the wrong field.)
2. *Replace* with a page of type `T` not already in the field, in tiers: first pages of type `T` that link to or
   from `W` (frontmatter or body) or that share a relation page with `W` (the other endpoint of a relation page
   that has `W` as an endpoint), then pages of type `T` that `P`'s body links; within a tier, page name in byte
   order; at most 5 shown, then one final option line `(+<n> more not shown)`, which is not an option. No other pages are offered.
3. *Delete* the item line (always last), except in a field required from `stub`, where deleting would only trade
   this error for SCAT-FM-REQUIRED-LINK.

**(3) Stub type for a dangling link.** The stub is offered only when the target is a legal name; the contract's
stub operation entails nothing for any other link. For a legal frontmatter link the type is the field's target
type (the contract's section 5 table), so the fix is exact: `stub <target> --type <type-key>`, offered after the
near match if there is one (a name that is one letter away from an existing page is more likely a typo than a new
concept, and a stub for a typo would create a duplicate). A stub for a `stakeholder-group` target is not offered
when the vault is at its cap, and the message says so, because the stub would trigger SCAT-CAP. For a target that
is not a legal name, the message offers instead: the near match, then the derived name of the target with the link
rewritten to it (and, if no such page exists, the stub of that name), and, when the derived name is empty, says to
choose a legal name by hand. For a body link the target's type is not stated, and the contract's stub creates a body
link's page only when given the type, so the type is inferred, in order: (a) if some frontmatter link field in the
vault names the same target, that field's target type (all of them, if several, sorted by type key); (b) otherwise
the four class keys in the order `stakeholder-group`, `concern`, `affordance`, `technology`, each a separate
numbered exact command. A type the page type discourages for body links is left out of the numbered stubs (it
would only trade an error for SCAT-LINK-DISCOURAGED-BODY) and the message says it was left out. Raw, coded and
relation pages are not offered for a body link: people write the first two, and a relation page is made from a
named pair.

**(4) Missing link type: the exact field and the skeleton, suggestions only, the choice stays with the author.**
Per log D-029 there is no TBox axiom that derives a record's affordances from its concerns. The message names the
exact field, gives the exact YAML to paste, and fills it with `S(<field>)`, labelled as suggestions. The choice
stays with the author for two reasons: the TBox does not say the derived set is the right set, and choosing which
affordance a scenario shows is the coder's reading, which the tools do not speak for. With no suggestions the
skeleton carries one slot *(author)*. The alternative `set-status draft` is always offered.

## 3. Rules

| Id | Severity | Fires at | Trigger (short) | Fix kind |
|---|---|---|---|---|
| SCAT-FM-PARSE | error | every status | file starts with `---` but its frontmatter is not a readable mapping | manual |
| SCAT-FM-REQUIRED | error | every status | a text field required from `stub` is missing | options |
| SCAT-FM-TYPE | error | every status | `type` is not one of the twelve keys | options |
| SCAT-FM-REQUIRED-LINK | error | every status | a relation page's required endpoint field is missing or empty | slot |
| SCAT-FM-STATUS | error | every status | `status` is not `stub`, `draft` or `done` | options |
| SCAT-FM-INDEXES | error | every status | class page `indexes` is outside its value set | options |
| SCAT-FM-SHAPE | error | every status | a text field is not a single non-empty string | exact |
| SCAT-NAME | error | every status | a page's file name is not a legal name, or is not unique, or is a class page with the wrong name | exact |
| SCAT-DONE-FIELD | error | done (class pages: always) | required text field missing | slot |
| SCAT-DONE-LINK | error | done | required link field missing or empty | slot |
| SCAT-DRAFT-FIELD | warning | draft | required text field missing | slot |
| SCAT-DRAFT-LINK | warning | draft | required link field missing or empty | slot |
| SCAT-LINK-SHAPE | error | every status | link field is not a list of `"[[<page-name>]]"` (a single field: not exactly one) | exact |
| SCAT-LINK-UNLISTED | error | every status | non-empty link field the page type does not list | exact |
| SCAT-LINK-ENDPOINT | error | every status | link target exists but has the wrong type | options |
| SCAT-LINK-DANGLING | error | every status | frontmatter link target page does not exist | options |
| SCAT-LINK-DANGLING-BODY | error | every status | body link target page does not exist | options |
| SCAT-LINK-DISCOURAGED | warning | every status | non-empty discouraged field | options |
| SCAT-LINK-DISCOURAGED-BODY | warning | every status | body link to a class the page type discourages | options |
| SCAT-CAP | error | vault | more stakeholder-group pages than the cap | options |
| SCAT-CAP-CONFIG | error | vault | `scat.toml` or its cap missing, malformed or not a whole number of at least 1 | slot |
| SCAT-CONFLICT-BOTH | warning | every status | a coded record lists both ends of a conflict | advisory |
| SCAT-CONFLICT-SELF | warning | every status | a concern lists itself under `conflicts` | exact |
| SCAT-REL-DUPLICATE | warning | every status | two relation pages state the same pair | exact |
| SCAT-MENTION | warning | every status | body names an existing page in plain text | exact |
| SCAT-RAW-BACKLINK | warning | every status | a coded page lists this raw page, which does not list it back | exact |
| SCAT-RAW-UNCODED | warning | done | a done raw page has no coded page | slot |
| SCAT-INDEX-STALE | warning | every status | a class page is missing or differs from what `index` writes | exact |

Fix kinds: **exact** (one exact edit or command); **options** (numbered alternatives, each exact; the choice is the
author's); **slot** (exact except one *(author)* slot, why recorded); **advisory** (no change is required; why
recorded); **manual** (no exact fix is possible; why recorded). Per-rule notes follow. "Test" says what a
seeded-defect test needs: every test starts from a clean fixture vault with zero messages, injects exactly one
defect, and expects exactly one message of the rule, equal to the golden text, and no other message.

### SCAT-FM-PARSE
- **Severity:** error. **Fires:** every status.
- **Trigger:** the file starts with a `---` line (so it means to be a page) and either has no closing `---` line, or the frontmatter is not valid YAML (for example `title: a: b`, or a value that starts with a quote and continues after it), or is not a mapping. Quotes around `title`, `description` and `notes` are not required (contract section 1),  so most unquoted text is valid YAML and gets no message here. An unquoted ` #` silently cuts the rest of the line as a YAML comment and is not reported, which is why the contract advises quoting. A Markdown file with no frontmatter, or with frontmatter and no `type` key, is not a page and gets no message; a link to it is a dangling link and says so (SCAT-LINK-DANGLING).
- **Message:**
```
error [SCAT-FM-PARSE] <file>[:<line>] frontmatter: <parser's reason, or "the closing --- line is missing">
  Fix: make the frontmatter a block of `key: value` lines between two lines containing only `---`, at the very top of the file; start from the first line the parser rejected
```
- **Fix kind:** manual. Why not exact: the tools cannot repair text they could not read, and the page's type is the author's to state.
- **Test:** a copy with the closing `---` deleted, and one with a tab-indented key. Two messages, one each. Also: a CRLF copy of a clean page gives none, and a README with no frontmatter gives none.

### SCAT-FM-REQUIRED
- **Severity:** error. **Fires:** every status.
- **Trigger:** a text field the page type requires from `stub` is missing: `status` and `title` on a content page; `title` and `indexes` on a class page. (`type` is present by definition of a page; a file without it is not a page. A relation page's endpoint fields are required from `stub` too; their link kind has its own rule, SCAT-FM-REQUIRED-LINK.) One message per field.
- **Messages:**
```
error [SCAT-FM-REQUIRED] <file> field `status`: missing
  Fix: run `scat set-status <page-name> draft` (REPL: `scat_kg.set_status("<page-name>", "draft")`); use `stub` or `done` instead of `draft` if that is the truth
error [SCAT-FM-REQUIRED] <file> field `title`: missing
  Fix: add the line `title: "<Title>"` (when `title:` is present but empty, replace that line), where <Title> is, on a class page whose name is in the contract's section 8 table, that table's default title (`heldby-pairs` gives `Heldby`), on a relation page whose two endpoints resolve, the contract's stub form (`<group title> holds <concern title>`, `<affordance title> addresses <concern title>`, `<affordance title> attributed to <technology title>`, using the endpoints' titles), and otherwise the page name with each - replaced by a space and the first letter upper case (reword it if you like)
error [SCAT-FM-REQUIRED] <file> field `indexes`: missing
  Fix: add the line `indexes: <key>`      (when `indexes:` is present but empty, replace that line; when the page name is in the contract's class-page table: that table's value; otherwise choose one:)
    one numbered line `indexes: <key>` for each of stakeholder-group, concern, affordance, technology, heldby, addresses, attributes
```
The contract's table (section 8) maps `stakeholder-groups` to `stakeholder-group`, `concerns` to `concern`, `affordances` to `affordance`, `technologies` to `technology`, `heldby-pairs` to `heldby`, `addresses-pairs` to `addresses` and `attributes-pairs` to `attributes`.
- **Fix kind:** options. `status`: the author knows whether it is finished; `draft` is the one that never overstates. `title` is exact (the contract's own stub title, or its default class title). `indexes` is exact when the name is in the table.
- **Test:** `status`, `title` and `indexes` removed in turn (`indexes` once on a page named `concerns`, once on a page with another name), each at status draft; `title` and `indexes` also at stub, to show no status excuses them.

### SCAT-FM-TYPE
- **Severity:** error. **Fires:** every status.
- **Trigger:** `type` is present, is a string, and is not one of the twelve page-type keys.
- **Message:**
```
error [SCAT-FM-TYPE] <file> field `type`: `<value>` is not a page type
  Fix: change it to `type: <near match>`            (when a near match among the twelve keys exists)
  Fix, choose the one that describes this page: `type: <key>` ...    (otherwise, one numbered line per key of the twelve, each with its `scat:pageDescription`, in alphabetical order)
```
- **Fix kind:** options (exact when the near match exists).
- **Test:** `type: Concern` (near match `concern`, exact) and `type: gadget` (list). Links to this page from other pages give no endpoint error (cascade guard). A file with no `type` at all is not a page (see SCAT-FM-PARSE and SCAT-LINK-DANGLING).

### SCAT-FM-REQUIRED-LINK
- **Severity:** error. **Fires:** every status.
- **Trigger:** a link field required from `stub` is missing or empty: on a `heldby` page `group` and `concern`; on an `addresses` page `concern` and `affordance`; on an `attributes` page `affordance` and `technology`. One message per field.
- **Message:**
```
error [SCAT-FM-REQUIRED-LINK] <file> field `<field>`: missing; a <type-key> page names exactly one <expected-key> page here, at every status
  Fix: <add the line | replace the line `<field>: <current>` with> `<field>: "[[<one <expected-key> page you choose>]]"` (author)
```
- **Fix kind:** slot. Why not exact: the TBox derives neither endpoint from the other and the page's name is not read as data, so which pair the page records is the author's reading. Tool-created relation pages (the stub operation) have both endpoints filled, so this error comes from a hand edit.
- **Test:** each of the six endpoint fields removed in turn, at `stub`, `draft` and `done` (same message at each); `group: ` with no value.

### SCAT-FM-STATUS
- **Severity:** error. **Fires:** every status. Not evaluated on class pages.
- **Trigger:** `status` is present, is a string, and is not `stub`, `draft` or `done`.
- **Message:**
```
error [SCAT-FM-STATUS] <file> field `status`: `<value>` is not a status
  Fix: change it to `status: <near match>`                       (when a near match among stub, draft, done exists)
  Fix, choose one: `status: stub` (just started), `status: draft` (being written), `status: done` (finished)    (otherwise)
```
- **Fix kind:** options. Which status is true is the author's.
- **Test:** `status: Done` (exact) and `status: finished` (list). The page gets no "needs status" message.

### SCAT-FM-INDEXES
- **Severity:** error. **Fires:** every status. Class pages only.
- **Trigger:** `indexes` is present and is not one of `stakeholder-group`, `concern`, `affordance`, `technology`, `heldby`, `addresses`, `attributes`.
- **Message:**
```
error [SCAT-FM-INDEXES] <file> field `indexes`: `<value>` is not a class
  Fix: change it to `indexes: <near match>`                                   (when a near match among the seven keys exists)
  Fix, choose one: the seven keys, each as `indexes: <key>`      (otherwise)
```
- **Fix kind:** options.
- **Test:** `indexes: concerns` on a class page (near match `concern`).

### SCAT-FM-SHAPE
- **Severity:** error. **Fires:** every status.
- **Trigger:** `type`, `status`, `title`, `description`, `indexes` or `notes` is present and not empty, and is not a single string (a list, a mapping, a number, or a boolean such as an unquoted `yes` or `true`). An unquoted `null` or `~` is missing, by the Empty rule above.
- **Message:**
```
error [SCAT-FM-SHAPE] <file> field `<field>`: expected one line of text, found <a list | a mapping | a number | a boolean>
  Fix: replace the field with the line `<field>: "<text>"`          (a one-item list of text: the item; a boolean or number: the value as written, quoted)
  Fix: replace the field with one line of text you write            (otherwise; no exact value exists)
```
- **Fix kind:** exact for a one-item list of text, a boolean and a number (quote the value); otherwise manual, because the intended text is unknowable.
- **Test:** `title:` as a one-item list (exact), as a mapping (manual), and `title: yes` (exact: `title: "yes"`).

### SCAT-NAME
- **Severity:** error. **Fires:** every status.
- **Trigger:** one of, for a page: (a) its name is not legal (a character outside `a-z`, `0-9`, `-`; a leading, trailing or doubled hyphen; more than 64 characters; or a reserved name that the page is not entitled to: a page is entitled to a class page name when it has `type: class` and its name is in the contract section 8 table, whatever its `indexes` value), which includes names that differ from another only by case; (b) another page elsewhere in the vault has the same name (reported on the page whose `<file>` sorts later); (c) a `class` page whose name is not the one the contract's class-page table gives for its `indexes`. One message per page.
- **Message:**
```
error [SCAT-NAME] <file> frontmatter: the page name `<page-name>` <is not legal (<reason>) | is also the name of <other-file> | is not the name of the <indexes> class page>
  Fix: change the file name to `<new-name>.md`, then change the links that meant this page from `[[<page-name>]]` to `[[<new-name>]]`
```
`<new-name>` is the free derived name of the page's `title` for (a) and (b), and the table's name for (c). For (a) and (c) every link that names `<page-name>` is changed. For (b) two pages share the name, so only the links meant for the renamed page are changed, and the author tells them apart by context: a link in a frontmatter field means the page type that field names; a body link means the page the sentence around it is about; the links meant for the other page keep `[[<page-name>]]`. When the title is missing or its derived name is empty, the fix is "choose a legal name by hand (contract section 2)".
- **Fix kind:** exact. The derivation is the contract's, so the name is not a guess; a hand choice is needed only when the title gives nothing.
- **Test:** `Safe Tool.md`; a 65-character name; `con.md`; `a--b.md`; `safety.md` and `Safety.md` (case only; both fail (a) or one does); `x.md` in two folders (one message, on the later path); a `class` page with `indexes: concern` named `foo`; a page with title "Café menu" (derived name `cafe-menu`); one with a non-Latin title (hand choice).

### SCAT-DONE-FIELD
- **Severity:** error. **Fires:** status `done`; class pages always. **Needs status** (not on class pages).
- **Trigger:** a text field required from `done` (`description`) is missing.
- **Message:**
```
error [SCAT-DONE-FIELD] <file> field `description`: missing on a page with status: done
  Fix, choose one:
    1. <add the line | replace the line `description: <current>` with> `description: "<one sentence you write>"` (author)
    2. run `scat set-status <page-name> draft` (REPL: `scat_kg.set_status("<page-name>", "draft")`) if the page is not finished
```
On a class page the first line reads `... missing` and only option 1 is printed.
- **Fix kind:** slot. Why not exact: the sentence is the author's reading (decision 1).
- **Test:** `description` removed at `done` (two options), on a relation page at `done`, and on a class page (one option); at `stub` and `draft` the same page gives no SCAT-DONE-FIELD.

### SCAT-DONE-LINK
- **Severity:** error. **Fires:** status `done`. **Needs status.**
- **Trigger:** a list link field required from `done` (`raw`, `groups`, `concerns`, `affordances`, `technologies` of the coded records) is missing or empty. One message per field.
- **Message:**
```
error [SCAT-DONE-LINK] <file> field `<field>`: required link field is missing or empty on a page with status: done
  Fix, choose one:
    1. <add this to the frontmatter | replace the line `<field>: <current>` with this>, keeping the lines that fit (suggestions found from relation pages; you decide):
         <field>:
           - "[[<suggestion>]]"
    2. run `scat set-status <page-name> draft` (REPL: `scat_kg.set_status("<page-name>", "draft")`) if the page is not finished
```
Option 1 says "add this to the frontmatter" when the key is absent, and "replace the line `<field>: <current>` with this" when the key is present and empty (`<current>` is the text after the colon as written, for example `[]`, or nothing). With no suggestions it shows the single line `- "[[<one <type-key> page you choose>]]"` (author) and says "no suggestions found".
- **Fix kind:** slot. Why not exact: decision 4 and log D-029. The field and the format are exact; which page links is the coder's reading.
- **Test:** each required link field removed in turn at `done`, once with suggestions and once without; one with the key present as `affordances: []` (the "replace" wording); the same page at `draft` gives SCAT-DRAFT-LINK, at `stub` nothing.

### SCAT-DRAFT-FIELD and SCAT-DRAFT-LINK
- **Severity:** warning. **Fires:** status `draft`. **Needs status.**
- **Trigger:** as SCAT-DONE-FIELD and SCAT-DONE-LINK, at status `draft`.
- **Message:** the same problem and suggestions as the `done` rules, no `set-status` option, because nothing is blocked:
```
warning [SCAT-DRAFT-FIELD] <file> field `description`: missing (required once the page is done)
  Fix: <add the line | replace the line `description: <current>` with> `description: "<one sentence you write>"` (author) before you set status: done
warning [SCAT-DRAFT-LINK] <file> field `<field>`: required link field is missing or empty (required once the page is done)
  Fix: <add this to the frontmatter | replace the line `<field>: <current>` with this>, keeping the lines that fit (suggestions found from relation pages; you decide):
         <field>:
           - "[[<suggestion>]]"
```
- **Fix kind:** slot. Why not exact: the same reasons as SCAT-DONE-FIELD and SCAT-DONE-LINK.
- **Test:** the seeds of SCAT-DONE-FIELD and SCAT-DONE-LINK at `draft`: warnings only, exit status of the check unchanged by them.

### SCAT-LINK-SHAPE
- **Severity:** error. **Fires:** every status.
- **Trigger:** a link field the page type lists is present and non-empty, and its value is not a list whose items are all strings of exactly the form `[[<page-name>]]` (no `|alias`, no `#heading`); for a single field (`scat:single`), not exactly one such string and no list. An unquoted `[[x]]` in YAML is a nested list and so triggers it. A one-item list in a single field triggers it too.
- **Message:**
```
error [SCAT-LINK-SHAPE] <file>:<line> field `<field>`: <value is one line, not a list | an item is not a quoted [[page-name]] link | ...>
  Fix: replace the whole field with
         <field>:
           - "[[<page-name>]]"
```
For a single field the fix is the one line `<field>: "[[<page-name>]]"`; when the value is a list of several items the choices are one numbered line per item (keep that one), and the message adds "a relation page holds one pair; to relate more pairs, create more relation pages". The block is rebuilt from the value: a bare string or a nested list gives its text; `[[a|b]]`, `[[a#b]]` and `[[a^b]]` give `[[a]]`; an item that is not text is replaced by the line `- "[[<one page you choose>]]"` (author), and the message says that item could not be read.
- **Fix kind:** exact, except an unreadable item (manual: nothing in it names a page), and a several-item list in a single field (options: which item to keep is the author's).
- **Test:** four seeds: a scalar, an unquoted `[[x]]`, an alias item, a number item; and on a relation page, `group` as a one-item list (exact) and as a two-item list (two options).

### SCAT-LINK-UNLISTED
- **Severity:** error (`scat:unlistedLinkLevel`). **Fires:** every status.
- **Trigger:** the page has a non-empty value under a key that is a link field of some page type but that its own page type lists in none of required, optional and discouraged. (A key that is no link field of any type is ignored; an empty value is ignored.)
- **Message:**
```
error [SCAT-LINK-UNLISTED] <file>:<line> field `<field>`: a <type-key> page does not take `<field>` (its link fields are: <list, alphabetical>)
  Fix: delete `<field>:` and its list items
```
- **Fix kind:** exact. No move is offered: the field names carry different relations, so the tools do not guess that the author meant another field.
- **Test:** `groups` on a concern page; `concern` on a coded scenario; an empty `groups: []` on a concern page gives none. A first-member key from the old design (`heldby:` on a group page) is no link field of any type now and is ignored; see section 5.

### SCAT-LINK-ENDPOINT
- **Severity:** error (`scat:wrongTargetLevel`). **Fires:** every status.
- **Trigger:** a link field the page type lists has an item `[[<target>]]` whose page exists, has a valid `type`, and is not of the field's target type. Class pages count as pages of type `class`.
- **Message:**
```
error [SCAT-LINK-ENDPOINT] <file>:<line> field `<field>`: [[<target>]] is a <actual-key> page, but `<field>` must link <expected-key> pages
  Fix, choose one:
    1. move the item line `<item>` from `<field>` to `<other-field>`        (list fields only): delete it from `<field>` (in a flow list `["[[a]]", "[[b]]"]` delete that one entry and its comma, leaving `[]` if it was the only one), and in `<other-field>` <add under it the line `- "[[<target>]]"` | add `<other-field>:` and under it that line | replace the line `<other-field>: <current>` with `<other-field>:` and under it every page already listed, then `- "[[<target>]]"`> (first for a block list, second when the key is absent, third for `[]`, empty or a flow list)
    2. replace `<item>` with `<item with candidate>`        (one numbered option per candidate)
    n. delete the item line `<item>` under `<field>`        (not in a field required from `stub`)
```
Options follow the order of decision 2. With no replacement available the message says "no existing <expected-key> page was found"; in a field required from `stub` it then has no option at all, and says the pair must be changed by hand (manual).

The swap case is one message, not two. When a relation page's two endpoint fields each hold a page of the other's type (a `heldby` page with a concern under `group` and a group under `concern`), the one message names both fields, is reported at the line of the first, and prints the result literally. `<field-a>` is the endpoint field that appears first in the file and `<field-b>` the other; `<w1>` is the value under `<field-a>`:
```
error [SCAT-LINK-ENDPOINT] <file>:<line> fields `<field-a>` and `<field-b>`: [[<w1>]] is a <key-1> page and [[<w2>]] is a <key-2> page, but `<field-a>` must link <expected-a> pages and `<field-b>` <expected-b> pages
  Fix: replace the two lines
         <field-a>: "[[<w1>]]"
         <field-b>: "[[<w2>]]"
       with
         <field-a>: "[[<w2>]]"
         <field-b>: "[[<w1>]]"
```
- **Fix kind:** options (the swap message: exact). Every option is exact; which one is meant is the author's intent, so the rule never picks.
- **Test:** an affordance under `concerns` of a coded scenario (move option 1 present); a relation page whose `affordance` holds a technology (replacements, tier 1 through the sharing `attributes` page, no delete); the swapped `heldby` page (exactly one message); a case with no candidates; a case with tier-1 and tier-2 candidates, to fix the order. At each status the same message appears.

### SCAT-LINK-DANGLING
- **Severity:** error. **Fires:** every status.
- **Trigger:** a link field the page type lists has an item whose target is not the name of any page. Three variants share the id, told apart in the message: (a) a legal name and no such file; (b) a legal or illegal name for which a Markdown file exists that has no `type` (so it is not a page); (c) a name that is not legal (contract section 2), including one that differs from an existing name only by case.
- **Message:**
```
error [SCAT-LINK-DANGLING] <file>:<line> field `<field>`: [[<target>]] does not reach a page (<no page is named <target> | <other-file> exists but has no `type`, so it is not a page | <target> is not a legal page name: <reason>>)
  Fix, choose one:
    1. replace `<item>` with `<item with near match>` (the closest existing <expected-key> page)
    2. run `scat stub <target> --type <expected-key>` (REPL: `scat_kg.stub("<target>", type="<expected-key>")`) to create it as a stub
```
Cap rule for every variant: any option that would create a `stakeholder-group` page (the stub of (a); the lines of (b) that turn a typeless file into a group page; the replace-then-stub and typeless-file options of (c)) is withheld when the vault is at its cap, and the message says "the vault is at its cap of <cap> stakeholder groups, so a new group page would break SCAT-CAP; choose an existing group".
Variant (a): options 1 (only if a near match exists among pages of the field's target type) and 2.
Variant (b): the target is a legal name and a Markdown file of that name exists without a `type`. Option 2 is replaced by "add these lines to the frontmatter of <other-file>: `type: <expected-key>`, `status: stub`, `title: "<Title>"`", because the stub operation refuses an existing file. If the file already has frontmatter, only the keys among `type`, `status` and `title` that it lacks are listed, and a key that is present but empty is replaced; if it has none, the three lines go in a block between two `---` lines at the very top. For an illegal target the file is not what the link meant (a link cannot reach it): variant (c) applies, and the message adds "<other-file> exists but is not a page".
Variant (c): no stub of `<target>` is offered, because the stub operation refuses an illegal name. Names are compared without regard to case, as the contract does. The replacement names are collected in this order and then deduplicated, so no two options print the same replacement: the near match `N` among pages of the field's target type; the derived name `d` of the target when it is not empty. For each name that survives: if a page of that name and the expected type exists, "replace `<item>` with `<item with name>`"; if no `.md` file of that name exists (only possible for `d`), "replace `<item>` with `<item with d>`, then run `scat stub <d> --type <expected-key>`"; if a `.md` file of that name exists without a `type`, "replace `<item>` with `<item with d>`, then add to the frontmatter of that file the lines of variant (b)"; when `d` is reserved or otherwise taken by a file that is neither of these, the free derived name is used in its place; if a page of that name exists with another type, no option is printed for it and the message adds "(`<name>` is a <key> page, so replacing the link with it would only trade this error for SCAT-LINK-ENDPOINT)". When the derived name is empty and there is no near match the message says "choose a legal page name by hand (contract section 2), then write the link with it".
- **Fix kind:** options. Exact because the type comes from the field (decision 3). On a relation page the stub option is the same command for the endpoint's own type (`group` gives `stakeholder-group`). The tools cannot tell a typo from a page the author means to create, so both are offered.
- **Test:** the measurement defect (`safety-briefings`, near match `safety-briefing`); a target with no near match (one option); `[[Safety-Briefing]]` against an existing `safety-briefing` (variant c, ratio 1); `[[Safety briefing]]` with no such page (derived name `safety-briefing`, replace then stub); `[[Safety-Briefing]]` where the near match and the derived name are the same page (one option, not two); a derived name that is an existing page of another type (withheld, with the note); a target made only of non-Latin text (hand choice); a link to a file with no `type` (variant b); a group target at the cap.

### SCAT-LINK-DANGLING-BODY
- **Severity:** error. **Fires:** every status.
- **Trigger:** a body link whose target is not the name of any page, in the same three variants as SCAT-LINK-DANGLING. Targets that are not page links (contract section 3) are never dangling.
- **Message:**
```
error [SCAT-LINK-DANGLING-BODY] <file>:<line> link [[<target>]]: does not reach a page (<reason as in SCAT-LINK-DANGLING>)
  Fix, choose one:
    1. on line <line> replace `[[<target>]]` with `[[<near match>]]`                    (only if a near match exists among all pages)
    2. run `scat stub <target> --type <key>` (REPL: `scat_kg.stub("<target>", type="<key>")`) to create a <key> page      (one numbered option per inferred type, decision 3)
    n. on line <line> replace `[[<target>]]` with `<target>` to keep the words and drop the link
```
Types the page type discourages for body links are left out of the stubs, and the message adds "(<key> left out: a <page-type> page should not link to it)". The cap rule of SCAT-LINK-DANGLING applies to every stakeholder-group option here too (a stub, the typeless-file lines, replace-then-stub), with the same note. A name that is not legal, or a file with no `type`, takes the variant wording of SCAT-LINK-DANGLING (variant (b) is offered as there, with the inferred type in place of the expected one). For an illegal name there is no stub of it; the replacement names are the near match (among all pages) and the derived name, deduplicated in that order, a name that is an existing page is a plain replacement, one that names no page is a replacement followed by the stub on the derived name (one option per inferred type), and a derived name for which a `.md` file already exists is not offered a stub (the stub condition is that no `.md` file of that name exists, compared without regard to case), and a typeless file of that name gets the variant (b) lines.
- **Fix kind:** options. The type is not written down at a body link, so the stub options are alternatives, not a guess (decision 3). The contract's other route, naming the page in the right link field of the same page, is also true and is stated in the message as a last note.
- **Test:** a body link in a coded scenario to a name that a frontmatter field elsewhere also names (one inferred type); to a name nothing else names (four options, minus `technology` on a scenario); a near match; a non-legal name; a body link inside a code fence, `[[photo.png]]`, `[[v1.2-notes]]`, `[[#Heading]]` (no message); `[[ghost^abc123]]` with no page `ghost` (a message naming target `ghost`).

### SCAT-LINK-DISCOURAGED
- **Severity:** warning. **Fires:** every status.
- **Trigger:** a field the page type lists as discouraged is present and non-empty (`technologies` on a coded scenario; `groups` on a coded architecture). One message per page and field. Endpoint and dangling checks still apply to its items.
- **Message:**
```
warning [SCAT-LINK-DISCOURAGED] <file>:<line> field `<field>`: a <type-key> record is about <what the type relates>, so linking <class> pages here is discouraged: [[<t1>]], [[<t2>]]
  Fix, choose one:
    1. delete `<field>:` and its list items
    2. keep the point by linking what they offer, in `<affordances|concerns>` (suggestions you confirm): <add under it the line `- "[[<s1>]]"` | add `<field-2>:` and under it the lines | replace the line `<field-2>: <current>` with `<field-2>:` and under it every page already listed and then the suggestions>      (first for a block list, second when the key is absent, third for `[]`, empty or a flow list)
```
`<field-2>` is `affordances` when the discouraged field is `technologies`, and `concerns` when it is `groups`. For a coded scenario the reason reads "a scenario relates groups, concerns and affordances; technologies stay in the background"; for a coded architecture, "an architecture relates concerns, affordances and technologies; stakeholders are abstracted away". The suggestions are the two "from P's discouraged ..." rows of `S`: the affordances of `attributes` pages for the field's technologies, or the concerns of `heldby` pages for the field's groups. Option 2 is left out when there are none.
- **Fix kind:** options. The warning is advice, so it does not block, and the author may keep the field.
- **Test:** `technologies` on a coded scenario, `groups` on a coded architecture, each with and without suggestions; `technologies` on a coded architecture and `groups` on a coded scenario give none.

### SCAT-LINK-DISCOURAGED-BODY
- **Severity:** warning. **Fires:** every status.
- **Trigger:** a body link on a page whose type lists `scat:discouragedBodyLink` for the class of an existing target (raw and coded scenarios: technology; raw and coded architectures: stakeholder group).
- **Message:**
```
warning [SCAT-LINK-DISCOURAGED-BODY] <file>:<line> link [[<target>]]: the body of a <type-key> page should not link to a <class> page
  Fix, choose one:
    1. on line <line> replace `[[<target>]]` with `<target>` to keep the words and drop the link
    2. on line <line> replace `[[<target>]]` with `[[<s>]]`        (one numbered option per suggestion: the affordances the technology offers, or the concerns the group holds)
```
- **Fix kind:** options.
- **Test:** a technology link in a raw scenario body and in a coded scenario body; a group link in each architecture body; the same links on a concern page give none. After fix 1, SCAT-MENTION does not fire for the same words (see that rule).

### SCAT-CAP
- **Severity:** error. **Fires:** every status; vault level.
- **Trigger:** the vault holds more pages of type `stakeholder-group`, at any status, than the integer `stakeholder_group_cap` in `scat.toml` at the vault root (contract section 10).
- **Message:**
```
error [SCAT-CAP] scat.toml field `stakeholder_group_cap`: the vault holds <n> stakeholder-group pages, over the cap of <cap>: <name>, <name>, ...
  Fix, choose one:
    1. write `stakeholder_group_cap = <n>` in scat.toml (the cap protects against identifying individuals; raise it only if the plan allows)
    2. fold <n minus cap> group(s) into the others (move their standpoints into another group's `description`) and delete those pages
```
- **Fix kind:** options. Option 2 is not exact: which groups merge is the facilitator's judgement, and the tools do not choose.
- **Test:** a fixture with cap 3 and 4 groups (one message, naming all four); with 3 groups (none); the fourth group as a stub still triggers.

### SCAT-CAP-CONFIG
- **Severity:** error. **Fires:** vault level.
- **Trigger:** `scat.toml` at the vault root is absent, or is not valid TOML, or lacks `stakeholder_group_cap` at the top level, or its value is not a TOML integer of at least 1 (a string, a float such as `3.0`, and `0` all trigger it).
- **Message:**
```
error [SCAT-CAP-CONFIG] scat.toml field `stakeholder_group_cap`: <the file is missing | the file is not valid TOML: <parser's reason> | the key is missing | the value `<value>` is not a TOML integer of 1 or more>
  Fix: <add the line | replace the line `stakeholder_group_cap = <current>` with> `stakeholder_group_cap = <number you choose>` (author) in scat.toml; choose a whole number of 1 or more (the vault has <n> stakeholder-group pages now, so choose at least <n> if <n> is 1 or more)
```
- **Fix kind:** slot. Why not exact: the cap is a planning decision.
- **Test:** the file removed; the file with a broken line; the key removed; `stakeholder_group_cap = "three"`; `stakeholder_group_cap = 0`; `stakeholder_group_cap = 2.5`; `stakeholder_group_cap = 3.0`.

### SCAT-CONFLICT-BOTH
- **Severity:** warning (D3). **Fires:** every status.
- **Trigger:** a coded record (`scenario-coded` or `architecture-coded`) lists in `concerns` two existing concern pages A and B such that {A, B} is in the conflict relation. The relation is the symmetric closure of the declarations: {A, B} is in it when A's `conflicts` lists B, or B's `conflicts` lists A, or both. A one-sided declaration is complete: no message asks for the other side. A concern listing itself is ignored. One message per record and per pair; within a pair A is the page whose name sorts first and B the other, and the pairs are sorted by (A, B). The message is reported at the line of the `concerns:` key of the coded page.
- **Message:**
```
warning [SCAT-CONFLICT-BOTH] <file>:<line> field `concerns`: this record holds both [[<A>]] and [[<B>]], which conflict (declared on <declaring pages>)
  Fix: none needed if both belong in this record. Holding both sides is allowed and is what the warning marks, a place where two concerns pull apart. If one was coded here by mistake, delete its line `- "[[<A or B>]]"` under `concerns`.
```
`<declaring pages>` is the names of the concern pages whose `conflicts` lists the other, as `[[name]]`, sorted by name and separated by `, `.
- **Fix kind:** advisory. Why: the graph holds disagreement and does not resolve it (log D-028), so the rule must not ask for the difference to be removed.
- **Test:** record lists both with a declaration on A only, on B only, and on both (one message each case, same text apart from "declared on"); lists one only (none); lists both with no declaration (none); a draft and a done record (same message).

### SCAT-CONFLICT-SELF
- **Severity:** warning. **Fires:** every status. Concern pages.
- **Trigger:** a concern page lists itself under `conflicts`. (The self pair is also ignored by SCAT-CONFLICT-BOTH.)
- **Message:**
```
warning [SCAT-CONFLICT-SELF] <file>:<line> field `conflicts`: [[<page-name>]] is this page; a concern cannot conflict with itself
  Fix: delete the line `- "[[<page-name>]]"` under `conflicts`
```
- **Fix kind:** exact. Two aspects of one concern in tension are two concerns; the message does not say which, and the tools do not split a concern for the author.
- **Test:** a concern listing itself (one message); listing itself and another (one message, the other pair still counts for SCAT-CONFLICT-BOTH).

### SCAT-REL-DUPLICATE
- **Severity:** warning. **Fires:** every status. Relation pages.
- **Trigger:** two or more pages of the same relation type have the same two endpoint targets (both endpoint fields are single, well-formed links). The page whose name sorts first in byte order is the one to keep; every other page of the pair is reported. A page whose endpoints are missing, malformed or dangling is the business of the endpoint rules, not this one.
- **Message:**
```
warning [SCAT-REL-DUPLICATE] <file> frontmatter: this <type-key> page states the same pair as [[<kept-page>]] (`<field-a>` [[<a>]], `<field-b>` [[<b>]]); a pair has one page
  Fix, two steps:
       1. in <kept-file>: if <file> has a non-empty `notes` line, put its text into the `notes` line of <kept-file> (add `notes: "<text>"` when it has none, or replace the line `notes: <current>` (bare `notes:`, `notes: ''` or `notes: ""`) with it when it is present but empty; in the written text `"` is `\"` and `\` is `\\`, as the contract says; join the two sentences in one line when both have text; skip this when <file> has no text in `notes`), and copy any part of the body of <file> you want to keep
       2. delete <file>, then run `scat index` (REPL: `scat_kg.index()`) and change every link that named `<page-name>` to `[[<kept-page>]]` (each shows as SCAT-LINK-DANGLING-BODY on the next check)
```
`<field-a>` and `<field-b>` are the relation's two endpoint fields in the order the kept page's file lists them, `<a>` and `<b>` their targets (the same in the duplicate), and `<kept-file>` is the vault-relative path of the kept page.
- **Fix kind:** exact, as two steps. The steps are exact; what is worth keeping from the body is the author's reading, and the message says so rather than merging prose.
- **Test:** two `heldby` pages for the same (group, concern) with different names and folders (one message, on the later name); the same concern with two different groups (none); `heldby` and `addresses` pages that share an endpoint (none); a duplicate of a duplicate (two messages).

### SCAT-MENTION
- **Severity:** warning (basic). **Fires:** every status. Not on raw or class pages.
- **Trigger:** the body of a page contains, as plain text, the `title` or the page name of an existing page of type `stakeholder-group`, `concern`, `affordance` or `technology`, matched case-insensitively at word boundaries, for a title or name of at least 4 characters, outside code, outside any wikilink, and when the body has no link to that page. Not the page itself. Not a page of a class that the page type discourages for body links. Reported once per page and target, at the first occurrence. No stemming, no plurals.
- **Message:**
```
warning [SCAT-MENTION] <file>:<line>:<column> text `<as written>`: names the <type-key> page [[<page-name>]] but does not link it
  Fix: on line <line> replace `<as written>` with `[[<page-name>|<as written>]]`          (`[[<page-name>]]` when the text is the page name)
```
- **Fix kind:** exact. Raw pages are exempt because they keep the story as told (facilitation capability 10); linking happens in the coded page.
- **Test:** a coded page mentioning a concern's title once in plain text (one message), once plain and once linked (none), inside a code span (none), and a technology on a scenario (none).

### SCAT-RAW-BACKLINK
- **Severity:** warning. **Fires:** every status. Raw pages.
- **Trigger:** coded page C lists raw page R in `raw`, C's type is the target type of R's `coded` field, and R's `coded` does not list C. One message per C. (Reported on R, so the fix is in the file named.)
- **Message:**
```
warning [SCAT-RAW-BACKLINK] <file> field `coded`: [[<C>]] lists this page in `raw`, but this page does not list it
  Fix: <add under `coded:` in <file> the line `- "[[<C>]]"` | in <file> add `coded:` and under it the line `- "[[<C>]]"` | replace the line `coded: <current>` with `coded:` and under it one line `- "[[<x>]]"` for each page already listed, then `- "[[<C>]]"`>
       (first when `coded` is a block list, second when the key is absent, third when it is `[]`, empty or a flow list such as `["[[a]]"]`)
```
- **Fix kind:** exact. This is the raw-to-coded warning; the link is advice, never an error (mission non-goal).
- **Test:** coded page with `raw` naming R and R with no `coded`; with `coded` naming another page; with `coded` naming C (none).

### SCAT-RAW-UNCODED
- **Severity:** warning. **Fires:** status `done`. Raw pages. **Needs status.**
- **Trigger:** raw page R has status `done`, its `coded` is empty, and no page lists R in `raw`.
- **Message:**
```
warning [SCAT-RAW-UNCODED] <file> field `coded`: status is done but no coded page derives from this page
  Fix, two steps, in this order:
       1. in <file>: <add | replace the line `coded: <current>` with> `coded:` and under it the line `- "[[<coded-page-name>]]"` (author: choose the name)
       2. run `scat stub <coded-page-name> --type <coded-key>` (REPL: `scat_kg.stub("<coded-page-name>", type="<coded-key>")`); the operation writes `raw` on the new page itself, listing this page (until it runs, the new `coded` link shows as SCAT-LINK-DANGLING)
```
`<coded-key>` is `scenario-coded` for a raw scenario and `architecture-coded` for a raw architecture.
- **Fix kind:** slot. Why not exact: the coded page's name is the author's.
- **Test:** done raw page with nothing coded (message); the same at draft (none); after step 1 alone (SCAT-LINK-DANGLING on the new `coded` link, and SCAT-RAW-UNCODED gone because `coded` is non-empty); after both steps (none: the stub wrote `raw` on the new page, and `coded` already names it); after step 2 alone (SCAT-RAW-UNCODED stays: no raw page names the new page, so the stub writes no `raw` and nothing lists the raw page).

### SCAT-INDEX-STALE
- **Severity:** warning. **Fires:** every status. Class pages and the vault.
- **Trigger:** a class page is missing for one of the seven classes, or has no well-formed start-then-end marker pair (the first such pair is the region; extra marker lines after it are not stale), or the text between the markers differs from what `index` would write from the instance pages (contract section 8: rows, columns, order). The check compares and never writes.
- **Message:**
```
warning [SCAT-INDEX-STALE] <file> index table: <the page is missing | no well-formed marker pair | the table differs from the <type-key> pages>
  Fix: run `scat index` (REPL: `scat_kg.index()`)
```
For a missing page `<file>` is the path the index operation would create (`class/<name>.md`).
- **Fix kind:** exact.
- **Test:** add an instance page without running `index` (one message on its class page); delete a class page (one message); delete a marker (one message); add a stray extra marker line after a good pair (none); run `index` and re-check (none).

## 4. Coverage

| Requirement | Rules |
|---|---|
| R-1 required fields and types | SCAT-FM-PARSE, SCAT-FM-REQUIRED, SCAT-FM-REQUIRED-LINK, SCAT-FM-TYPE, SCAT-FM-INDEXES, SCAT-FM-SHAPE, SCAT-DONE-FIELD, SCAT-DONE-LINK, SCAT-LINK-SHAPE |
| R-1 page names (contract section 2) | SCAT-NAME |
| R-1 relation endpoints | SCAT-LINK-ENDPOINT |
| R-1 linking rules, error level | SCAT-LINK-UNLISTED |
| R-1 linking rules, warning level (scenario to technology, architecture to stakeholder group; frontmatter and body) | SCAT-LINK-DISCOURAGED, SCAT-LINK-DISCOURAGED-BODY |
| R-1 stakeholder-group cap | SCAT-CAP, SCAT-CAP-CONFIG |
| R-1 valid status | SCAT-FM-STATUS |
| R-1 links to pages that do not exist | SCAT-LINK-DANGLING, SCAT-LINK-DANGLING-BODY |
| R-3 unfinished is never an error | SCAT-DRAFT-FIELD, SCAT-DRAFT-LINK (warnings at draft); nothing fires for `done` fields at stub |
| R-3 full contract at `done`; required-from-status | SCAT-DONE-FIELD, SCAT-DONE-LINK, SCAT-FM-REQUIRED |
| R-3 links and endpoints at every status | SCAT-LINK-SHAPE, SCAT-LINK-UNLISTED, SCAT-LINK-ENDPOINT, SCAT-LINK-DANGLING, SCAT-LINK-DANGLING-BODY |
| D3 conflict warning | SCAT-CONFLICT-BOTH, SCAT-CONFLICT-SELF |
| Unlinked-mention warning (basic) | SCAT-MENTION |
| Raw-to-coded warning | SCAT-RAW-BACKLINK, SCAT-RAW-UNCODED |
| Duplicate relation page (contract section 5) | SCAT-REL-DUPLICATE |
| Generated index (G2, R-11) | SCAT-INDEX-STALE |

TBox coverage map. One line per field or link rule of the TBox: `<kind> <type-key>.<field-or-class-key> -> <rule ids>`.
It is checked against `ontology/scat.ttl` by a script. Every required field, discouraged field and discouraged body
link of the TBox must appear.

```
required addresses.affordance -> SCAT-FM-REQUIRED-LINK, SCAT-LINK-SHAPE
required addresses.concern -> SCAT-FM-REQUIRED-LINK, SCAT-LINK-SHAPE
required addresses.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required addresses.status -> SCAT-FM-REQUIRED
required addresses.title -> SCAT-FM-REQUIRED
required addresses.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING
optional addresses.notes -> SCAT-FM-SHAPE
required affordance.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required affordance.status -> SCAT-FM-REQUIRED
required affordance.title -> SCAT-FM-REQUIRED
required affordance.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING
required architecture-coded.affordances -> SCAT-DONE-LINK, SCAT-DRAFT-LINK
required architecture-coded.concerns -> SCAT-DONE-LINK, SCAT-DRAFT-LINK
required architecture-coded.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required architecture-coded.raw -> SCAT-DONE-LINK, SCAT-DRAFT-LINK
required architecture-coded.status -> SCAT-FM-REQUIRED
required architecture-coded.technologies -> SCAT-DONE-LINK, SCAT-DRAFT-LINK
required architecture-coded.title -> SCAT-FM-REQUIRED
required architecture-coded.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING
discouraged-field architecture-coded.groups -> SCAT-LINK-DISCOURAGED
discouraged-body-link architecture-coded.stakeholder-group -> SCAT-LINK-DISCOURAGED-BODY
required architecture-raw.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required architecture-raw.status -> SCAT-FM-REQUIRED
required architecture-raw.title -> SCAT-FM-REQUIRED
required architecture-raw.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING
discouraged-body-link architecture-raw.stakeholder-group -> SCAT-LINK-DISCOURAGED-BODY
optional architecture-raw.coded -> SCAT-RAW-BACKLINK, SCAT-RAW-UNCODED
required attributes.affordance -> SCAT-FM-REQUIRED-LINK, SCAT-LINK-SHAPE
required attributes.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required attributes.status -> SCAT-FM-REQUIRED
required attributes.technology -> SCAT-FM-REQUIRED-LINK, SCAT-LINK-SHAPE
required attributes.title -> SCAT-FM-REQUIRED
required attributes.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING
optional attributes.notes -> SCAT-FM-SHAPE
required class.description -> SCAT-DONE-FIELD
required class.indexes -> SCAT-FM-REQUIRED
required class.title -> SCAT-FM-REQUIRED
required class.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING
required concern.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required concern.status -> SCAT-FM-REQUIRED
required concern.title -> SCAT-FM-REQUIRED
required concern.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING
optional concern.conflicts -> SCAT-CONFLICT-BOTH, SCAT-CONFLICT-SELF
required heldby.concern -> SCAT-FM-REQUIRED-LINK, SCAT-LINK-SHAPE
required heldby.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required heldby.group -> SCAT-FM-REQUIRED-LINK, SCAT-LINK-SHAPE
required heldby.status -> SCAT-FM-REQUIRED
required heldby.title -> SCAT-FM-REQUIRED
required heldby.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING
optional heldby.notes -> SCAT-FM-SHAPE
required scenario-coded.affordances -> SCAT-DONE-LINK, SCAT-DRAFT-LINK
required scenario-coded.concerns -> SCAT-DONE-LINK, SCAT-DRAFT-LINK
required scenario-coded.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required scenario-coded.groups -> SCAT-DONE-LINK, SCAT-DRAFT-LINK
required scenario-coded.raw -> SCAT-DONE-LINK, SCAT-DRAFT-LINK
required scenario-coded.status -> SCAT-FM-REQUIRED
required scenario-coded.title -> SCAT-FM-REQUIRED
required scenario-coded.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING
discouraged-field scenario-coded.technologies -> SCAT-LINK-DISCOURAGED
discouraged-body-link scenario-coded.technology -> SCAT-LINK-DISCOURAGED-BODY
required scenario-raw.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required scenario-raw.status -> SCAT-FM-REQUIRED
required scenario-raw.title -> SCAT-FM-REQUIRED
required scenario-raw.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING
discouraged-body-link scenario-raw.technology -> SCAT-LINK-DISCOURAGED-BODY
optional scenario-raw.coded -> SCAT-RAW-BACKLINK, SCAT-RAW-UNCODED
required stakeholder-group.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required stakeholder-group.status -> SCAT-FM-REQUIRED
required stakeholder-group.title -> SCAT-FM-REQUIRED
required stakeholder-group.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING
required technology.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required technology.status -> SCAT-FM-REQUIRED
required technology.title -> SCAT-FM-REQUIRED
required technology.type -> SCAT-FM-TYPE, SCAT-LINK-DANGLING
```

## 5. Needs from the TBox

Nothing blocks. Two points for the PM:
- `scat:unlistedLinkLevel` still says a page "carries" a link field, while `scat:discouragedField` says "present and non-empty". The catalogue reads both as present and non-empty. One sentence in the TBox would make it the single reading.
- The first-member fields (`heldby`, `addresses`, `attributes` on group, concern and affordance pages) are gone, so a stale `heldby:` key on a group page is no link field of any type and is ignored, not flagged. That follows the TBox comment ("keys that are not link fields and not listed are ignored").

The catalogue reads the status order from `scat:StatusValues`, "required from" from `scat:requiredFrom`, single-link fields from `scat:single`, and the class page's seven values from the `indexes` value set; all are stated. It hard-codes that raw and class pages are exempt from SCAT-MENTION and that SCAT-RAW-UNCODED fires at `done`; these are rules, not schema.

Relation pages are created only for a pair the author names (log D-031), so the catalogue has no rule for a relation page that a coded record might be thought to need, and none that guesses pairs.

## 6. Needs from the page contracts (WP4-U2)

The contract now supplies the link syntax (including what is not a body link), the legal-name rule, the name-from-title derivation, `scat.toml` and its key, the markers and rows of the generated index, the stub's content and the stub's types. What remains:
- That a Markdown file with no `type` is ignored (contract section 1) makes a missing `type` unreportable as a field error; the catalogue reports the consequence on the link that fails to reach it (SCAT-LINK-DANGLING variant b). If the contract ever wants a missing `type` graded on the file itself, it must say how a file is recognised as meant to be a page.
