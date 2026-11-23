# SCAT rule catalogue (WP4-D3)

What a check looks at, at what severity, and what each message tells the user to do. It serves goal WP4-G3 and
requirements R-1 to R-4 and R-8 of the mission. The TBox (`ontology/scat.ttl`) says what a conformant page is; this
file says how a departure is graded and worded. The page contracts (`contracts/page-contracts.md`) say how pages
are named, written and linked. This file uses their conventions and does not restate them.

Every rule has an id, a severity (`error` blocks, `warning` does not), a trigger a test can produce, and a message
that names the file, the field or link, and the rule id, and gives a fix. A fix is **exact** (a command, or an
exact field and value) or the rule records why it cannot be.

## 1. Conventions every rule shares

**Page terms.** A page is `<page-name>.md`. `<type-key>` is the value of a page's `type` field (`scat:key` of its
page type). A *link field* is a field with a `scat:targetType`. A *body link* is a wikilink in the page after the
frontmatter. A link's *target* is the page name inside the brackets. A page's *status* is `stub`, `draft` or `done`.
A page type with `scat:carriesStatus false` (the class page) is treated as `done` by every status rule below.

**Scopes.** A check runs at page, neighborhood or vault scope (G4). A rule reports on one file, and a page-scope
check of that file runs every rule that reports on it, reading other pages when the rule needs them. The same page
gives the same messages at every scope. The vault-level rules (SCAT-CAP, SCAT-CAP-CONFIG) run at vault scope, and
at the other two scopes when a stakeholder-group page is in the checked set. Checks never write (R-4).

**Cascade guard.** A page that fails SCAT-FM-PARSE is checked by no other rule as a source. A page whose `type` is
missing or invalid is checked by no rule that needs its type. A link whose target page has a missing or invalid
`type` is not endpoint-checked (the target already has its own error). A page whose `status` is missing or invalid
is checked by no rule marked "needs status"; the status error is reported once, on the page.

**Empty.** A field is *missing* when the key is absent or its value is null, an empty or blank string, or an empty
list. A link field that is present and empty is not an error by itself, except where a rule says the field is required.

**Status behaviour (R-3), in one table.**

| Kind of rule | stub | draft | done |
|---|---|---|---|
| Required from `stub` (`type`, `status`, `title`, `indexes`) | error | error | error |
| Required from `done` (`description`, required link fields) | silent | warning | error |
| Link shape, unlisted link, endpoint, dangling link (frontmatter and body) | error | error | error |
| Discouraged field, discouraged body link, conflict, mention, backlink, index | warning | warning | warning |
| SCAT-RAW-UNCODED | silent | silent | warning |
| Cap | error | error | error |

An unfinished page is never an error for being unfinished: nothing in the `done` row is an error before `done`.

**Order and format.** Messages sort by file name (byte order), then line, then rule id. The format:

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
`<severity>` is `error` or `warning`. `<file>` is `<page-name>.md`. `<line>` is the 1-based line of the link item or
the field key; it is given for link rules and omitted for field-level rules. `<where>` is ``field `<name>` ``,
``link [[<target>]]`` or `frontmatter`. Angle-bracket words are filled in by the tool, except a slot marked
*(author)*, which stays in the message literally because only the author can fill it. An *edit* fix says exactly
which lines to write, replace or delete. An *operation* fix names a command and its REPL twin on one line, as in
``run `scat set-status <page-name> draft` (REPL: `scat_kg.set_status("<page-name>", "draft")`)``. The same text is
printed on both paths (R-8).

**Operations the fixes name.** WP5 implements them. Their forms below are the contract of the message text only.

| Operation | CLI form | REPL form | What the messages rely on |
|---|---|---|---|
| stub | `scat stub <page-name> --type <type-key>` | `scat_kg.stub("<page-name>", type="<type-key>")` | Creates `<page-name>.md` with `status: stub` and every field required from `stub` filled, so the new page has no error. Refuses an existing page. Accepts the eight non-class type keys. |
| set-status | `scat set-status <page-name> <status>` | `scat_kg.set_status("<page-name>", "<status>")` | Sets `status`, adding the key if absent. |
| index | `scat index` | `scat_kg.index()` | Writes every class page's generated index, creating a missing class page. |

**Near match.** For a text `a` and a list of names, the near match is the name `b` with the highest
`difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()`, if that ratio is at least 0.8; ties go to the name
first in byte order. No near match means none.

**Suggestions (never required, never written).** Where a message offers pages to link, they come from links the
page already has, are sorted by page name in byte order, leave out pages already listed in the field, show at most
8 (then `(+<n> more)`), and are labelled as suggestions the author confirms. A suggestion never changes a rule's
trigger or severity. `S(<field>)` for a page P is:

| Field | Suggested pages |
|---|---|
| `groups` | groups that hold (`heldby`) a concern listed in P's `concerns` |
| `concerns` | concerns held by a group listed in P's `groups`, plus concerns whose `addresses` lists an affordance in P's `affordances` |
| `affordances` | affordances in `addresses` of a concern listed in P's `concerns`, plus affordances whose `attributes` lists a technology in P's `technologies` |
| `technologies` | technologies in `attributes` of an affordance listed in P's `affordances` |
| `raw` | raw pages of the field's target type whose `coded` lists P |

## 2. The four decisions

Each was open in `research/toolchain/measurements.md` ("What it takes to make each fix exact").

**(1) Missing field: the fix is an author slot plus an exact way out.** The prose of `description` is the
author's, so no fix can be exact for it, and the tools do not write it: seeding it from a title or a first
sentence would put words in the coder's mouth, against the facilitation stance. The message gives two alternatives
and picks neither: write the line (the sentence is a marked slot), or run `set-status <page-name> draft` (exact,
and honest: the page is not finished). Options (a) and (c) of the measurements are the second alternative; (b)
(seeding) is rejected. A missing `title` is the one exact case: the page name is a valid title, so the message
gives it. Class pages have no status, so only the first alternative is offered there.

**(2) Wrong endpoint: numbered replacements in a fixed order.** Let `W` be the wrong target, `T` the field's
target type and `P` the page. The options, in this order, are:
1. *Move*, if `P`'s page type lists, as required or optional, a field whose target type is `W`'s type and `W` is not
   already in it: move the line there. (The common slip is the right page in the wrong field.)
2. *Replace* with a page of type `T` not already in the field, in tiers: first pages of type `T` that link to or
   from `W` (frontmatter or body), then pages of type `T` that `P`'s body links; within a tier, page name in byte
   order; at most 5 shown (`(+<n> more)`). No other pages are offered.
3. *Delete* the line (always last).

**(3) Stub type for a dangling link.** For a frontmatter link the type is the field's target type, so the fix is
exact: `stub <target> --type <type-key>`, offered after the near match if there is one (a name that is one letter
away from an existing page is more likely a typo than a new concept, and a stub for a typo would create a
duplicate). A stub for a `stakeholder-group` target is not offered when the vault is at its cap, and the message
says so, because the stub would trigger SCAT-CAP. For a body link the target's type is not stated, so the type is
inferred, in order: (a) if some frontmatter link field in the vault names the same target, that field's target
type (all of them, if several, sorted by type key); (b) otherwise the four class keys in the order
`stakeholder-group`, `concern`, `affordance`, `technology`, each a separate numbered exact command. A type the
page type discourages for body links is left out of the numbered stubs (it would only trade an error for
SCAT-LINK-DISCOURAGED-BODY) and the message says it was left out. Raw and coded record pages are written by people,
so a body link to a missing record page gets no stub option.

**(4) Missing link type: the exact field and the skeleton, suggestions only, the choice stays with the author.**
Per log D-029 there is no TBox axiom that derives a record's affordances from its concerns. The message names the
exact field, gives the exact YAML to paste, and fills it with `S(<field>)`, labelled as suggestions. The choice
stays with the author for two reasons: the TBox does not say the derived set is the right set, and choosing which
affordance a scenario shows is the coder's reading, which the tools do not speak for. With no suggestions the
skeleton carries one slot *(author)*. The alternative `set-status draft` is always offered.

## 3. Rules

| Id | Severity | Fires at | Trigger (short) | Fix kind |
|---|---|---|---|---|
| SCAT-FM-PARSE | error | every status | file has no readable frontmatter mapping | manual |
| SCAT-FM-REQUIRED | error | every status | a field required from `stub` is missing | options |
| SCAT-FM-TYPE | error | every status | `type` is not one of the nine keys | options |
| SCAT-FM-STATUS | error | every status | `status` is not `stub`, `draft` or `done` | options |
| SCAT-FM-INDEXES | error | every status | class page `indexes` is outside its value set | options |
| SCAT-FM-SHAPE | error | every status | a text field is not a single non-empty string | exact |
| SCAT-DONE-FIELD | error | done (class pages: always) | required text field missing | slot |
| SCAT-DONE-LINK | error | done | required link field missing or empty | slot |
| SCAT-DRAFT-FIELD | warning | draft | required text field missing | slot |
| SCAT-DRAFT-LINK | warning | draft | required link field missing or empty | slot |
| SCAT-LINK-SHAPE | error | every status | link field is not a list of `"[[<page-name>]]"` | exact |
| SCAT-LINK-UNLISTED | error | every status | non-empty link field the page type does not list | exact |
| SCAT-LINK-ENDPOINT | error | every status | link target exists but has the wrong type | options |
| SCAT-LINK-DANGLING | error | every status | frontmatter link target page does not exist | options |
| SCAT-LINK-DANGLING-BODY | error | every status | body link target page does not exist | options |
| SCAT-LINK-DISCOURAGED | warning | every status | non-empty discouraged field | options |
| SCAT-LINK-DISCOURAGED-BODY | warning | every status | body link to a class the page type discourages | options |
| SCAT-CAP | error | vault | more stakeholder-group pages than the cap | options |
| SCAT-CAP-CONFIG | error | vault | cap missing or not a whole number of at least 1 | slot |
| SCAT-CONFLICT-BOTH | warning | every status | a coded record lists both ends of a conflict | advisory |
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
- **Trigger:** the file does not start with a `---` line and contain a closing `---` line, or the text between them is not valid YAML, or is not a mapping.
- **Message:**
```
error [SCAT-FM-PARSE] <file>[:<line>] frontmatter: <parser's reason, or "the file does not start with a --- line">
  Fix: make the frontmatter a block of `key: value` lines between two lines containing only `---`, at the very top of the file; start from the first line the parser rejected
```
- **Fix kind:** manual. Why not exact: the tools cannot repair text they could not read, and the page's type is the author's to state.
- **Test:** a copy with the opening `---` deleted, and one with a tab-indented key. Two messages, one each. Also: a CRLF copy of a clean page gives none.

### SCAT-FM-REQUIRED
- **Severity:** error. **Fires:** every status.
- **Trigger:** a field the page type requires from `stub` is missing: `type`, `status` and `title` on a content page; `type`, `title` and `indexes` on a class page. One message per field.
- **Messages:**
```
error [SCAT-FM-REQUIRED] <file> field `type`: missing
  Fix, choose the one that describes this page: add the line `type: <key>`, where <key> is
    <key>: <scat:pageDescription>     (one line per page type: the nine keys, in alphabetical order)
error [SCAT-FM-REQUIRED] <file> field `status`: missing
  Fix: run `scat set-status <page-name> draft` (REPL: `scat_kg.set_status("<page-name>", "draft")`); use `stub` or `done` instead of `draft` if that is the truth
error [SCAT-FM-REQUIRED] <file> field `title`: missing
  Fix: add the line `title: "<page-name>"` (the page name is a valid title; reword it if you like)
error [SCAT-FM-REQUIRED] <file> field `indexes`: missing
  Fix: add the line `indexes: <key>`      (if the page name equals one of stakeholder-group, concern, affordance, technology, that key; otherwise choose one:)
    1. `indexes: stakeholder-group`  2. `indexes: concern`  3. `indexes: affordance`  4. `indexes: technology`
```
- **Fix kind:** options. `type`: the page's intended type is the author's, so the nine descriptions are the exact alternatives. `status`: the author knows whether it is finished; `draft` is the one that never overstates. `title` and `indexes` are exact when the name gives the answer.
- **Test:** four seeds (one per field), each at status draft (the `title`, `type` and `indexes` seeds also at stub, to show no status excuses them). A page whose `type` is missing gets no type-dependent message.

### SCAT-FM-TYPE
- **Severity:** error. **Fires:** every status.
- **Trigger:** `type` is present, is a string, and is not one of the nine page-type keys.
- **Message:**
```
error [SCAT-FM-TYPE] <file> field `type`: `<value>` is not a page type
  Fix: change it to `type: <near match>`            (when a near match among the nine keys exists)
  Fix, choose the one that describes this page: `type: <key>` ...    (otherwise, the nine keys as in SCAT-FM-REQUIRED)
```
- **Fix kind:** options (exact when the near match exists).
- **Test:** `type: Concern` (near match `concern`, exact) and `type: gadget` (list). Links to this page from other pages give no endpoint error (cascade guard).

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
- **Trigger:** `indexes` is present and is not one of `stakeholder-group`, `concern`, `affordance`, `technology`.
- **Message:**
```
error [SCAT-FM-INDEXES] <file> field `indexes`: `<value>` is not a class
  Fix: change it to `indexes: <near match>`                                   (when a near match among the four keys exists)
  Fix, choose one: `indexes: stakeholder-group`, `indexes: concern`, `indexes: affordance`, `indexes: technology`      (otherwise)
```
- **Fix kind:** options.
- **Test:** `indexes: concerns` on a class page (near match `concern`).

### SCAT-FM-SHAPE
- **Severity:** error. **Fires:** every status.
- **Trigger:** `type`, `status`, `title`, `description` or `indexes` is present and not empty, and is not a single string (a list, a mapping, a number).
- **Message:**
```
error [SCAT-FM-SHAPE] <file> field `<field>`: expected one line of text, found <a list | a mapping | a number>
  Fix: replace the field with the line `<field>: "<text>"`          (a one-item list of text: the item)
  Fix: replace the field with one line of text you write            (otherwise; no exact value exists)
```
- **Fix kind:** exact for a one-item list of text; otherwise manual, because the intended text is unknowable.
- **Test:** `title:` as a one-item list (exact) and as a mapping (manual).

### SCAT-DONE-FIELD
- **Severity:** error. **Fires:** status `done`; class pages always. **Needs status** (not on class pages).
- **Trigger:** a text field required from `done` (`description`) is missing.
- **Message:**
```
error [SCAT-DONE-FIELD] <file> field `description`: missing on a page with status: done
  Fix, choose one:
    1. add the line `description: "<one sentence you write>"` (author)
    2. run `scat set-status <page-name> draft` (REPL: `scat_kg.set_status("<page-name>", "draft")`) if the page is not finished
```
On a class page the first line reads `... missing` and only option 1 is printed.
- **Fix kind:** slot. Why not exact: the sentence is the author's reading (decision 1).
- **Test:** `description` removed at `done` (two options) and on a class page (one option); at `stub` and `draft` the same page gives no SCAT-DONE-FIELD.

### SCAT-DONE-LINK
- **Severity:** error. **Fires:** status `done`. **Needs status.**
- **Trigger:** a link field required from `done` is missing or empty. One message per field.
- **Message:**
```
error [SCAT-DONE-LINK] <file> field `<field>`: required link field is missing or empty on a page with status: done
  Fix, choose one:
    1. write this in the frontmatter, keeping the lines that fit (suggestions found from links this page already has; you decide):
         <field>:
           - "[[<suggestion>]]"
    2. run `scat set-status <page-name> draft` (REPL: `scat_kg.set_status("<page-name>", "draft")`) if the page is not finished
```
With no suggestions, option 1 shows the single line `- "[[<one <type-key> page you choose>]]"` (author) and says "no suggestions found".
- **Fix kind:** slot. Why not exact: decision 4 and log D-029. The field and the format are exact; which page links is the coder's reading.
- **Test:** each required link field removed in turn at `done` (`raw`, `groups`, `concerns`, `affordances` on a coded scenario; `raw`, `concerns`, `affordances`, `technologies` on a coded architecture), once with suggestions and once without; the same page at `draft` gives SCAT-DRAFT-LINK, at `stub` nothing.

### SCAT-DRAFT-FIELD and SCAT-DRAFT-LINK
- **Severity:** warning. **Fires:** status `draft`. **Needs status.**
- **Trigger:** as SCAT-DONE-FIELD and SCAT-DONE-LINK, at status `draft`.
- **Message:** the same problem and suggestions as the `done` rules, no `set-status` option, because nothing is blocked:
```
warning [SCAT-DRAFT-FIELD] <file> field `description`: missing (required once the page is done)
  Fix: add the line `description: "<one sentence you write>"` (author) before you set status: done
warning [SCAT-DRAFT-LINK] <file> field `<field>`: required link field is missing or empty (required once the page is done)
  Fix: write this in the frontmatter, keeping the lines that fit (suggestions found from links this page already has; you decide):
         <field>:
           - "[[<suggestion>]]"
```
- **Fix kind:** slot. Why not exact: the same reasons as SCAT-DONE-FIELD and SCAT-DONE-LINK.
- **Test:** the seeds of SCAT-DONE-FIELD and SCAT-DONE-LINK at `draft`: warnings only, exit status of the check unchanged by them.

### SCAT-LINK-SHAPE
- **Severity:** error. **Fires:** every status.
- **Trigger:** a link field the page type lists is present and its value is not a list whose items are all strings of exactly the form `[[<page-name>]]` (no `|alias`, no `#heading`). An unquoted `[[x]]` in YAML is a nested list and so triggers it.
- **Message:**
```
error [SCAT-LINK-SHAPE] <file>:<line> field `<field>`: <value is one line, not a list | an item is not a quoted [[page-name]] link | ...>
  Fix: replace the whole field with
         <field>:
           - "[[<page-name>]]"
```
The block is rebuilt from the value: a bare string or a nested list gives its text; `[[a|b]]` and `[[a#b]]` give `[[a]]`; an item that is not text is replaced by the line `- "[[<one page you choose>]]"` (author), and the message says that item could not be read.
- **Fix kind:** exact, except an unreadable item (manual: nothing in it names a page).
- **Test:** four seeds: a scalar, an unquoted `[[x]]`, an alias item, a number item.

### SCAT-LINK-UNLISTED
- **Severity:** error (`scat:unlistedLinkLevel`). **Fires:** every status.
- **Trigger:** the page has a non-empty value under a key that is a link field of some page type but that its own page type lists in none of required, optional and discouraged. (A key that is no link field of any type is ignored; an empty list is ignored.)
- **Message:**
```
error [SCAT-LINK-UNLISTED] <file>:<line> field `<field>`: a <type-key> page does not take `<field>` (its link fields are: <list, alphabetical>)
  Fix: delete `<field>:` and its list items
```
- **Fix kind:** exact. No move is offered: the field names carry different relations (`heldby` and `concerns` both take concerns, with different meanings), so the tools do not guess that the author meant another field.
- **Test:** `groups` on a concern page; `heldby` on a coded scenario; an empty `groups: []` on a concern page gives none.

### SCAT-LINK-ENDPOINT
- **Severity:** error (`scat:wrongTargetLevel`). **Fires:** every status.
- **Trigger:** a link field the page type lists has an item `[[<target>]]` whose page exists, has a valid `type`, and is not of the field's target type. Class pages count as pages of type `class`.
- **Message:**
```
error [SCAT-LINK-ENDPOINT] <file>:<line> field `<field>`: [[<target>]] is a <actual-key> page, but `<field>` must link <expected-key> pages
  Fix, choose one:
    1. move the line `- "[[<target>]]"` from `<field>` to `<other-field>`
    2. replace `- "[[<target>]]"` with `- "[[<candidate>]]"`        (one numbered option per candidate)
    n. delete the line `- "[[<target>]]"` under `<field>`
```
Options follow the order of decision 2. With none of options 1 and 2 available the message says "no existing <expected-key> page was found" and prints only the delete.
- **Fix kind:** options. Every option is exact; which one is meant is the author's intent, so the rule never picks.
- **Test:** the measurement defect (a technology under `addresses`); a coded scenario with an affordance under `concerns` (move option 1 present); a case with no candidates; a case with tier-1 and tier-2 candidates, to fix the order. At each status the same message appears.

### SCAT-LINK-DANGLING
- **Severity:** error. **Fires:** every status.
- **Trigger:** a link field the page type lists has an item whose target has no page `<target>.md`.
- **Message:**
```
error [SCAT-LINK-DANGLING] <file>:<line> field `<field>`: [[<target>]] does not exist (no file <target>.md)
  Fix, choose one:
    1. replace `- "[[<target>]]"` with `- "[[<near match>]]"` (the closest existing <expected-key> page)       (only if a near match exists among pages of the field's target type)
    2. run `scat stub <target> --type <expected-key>` (REPL: `scat_kg.stub("<target>", type="<expected-key>")`) to create it as a stub
```
When the target is a `stakeholder-group` and the vault is at its cap, option 2 is replaced by "the vault is at its cap of <cap> stakeholder groups, so a new group page would break SCAT-CAP; choose an existing group".
- **Fix kind:** options. Exact because the type comes from the field (decision 3). The tools cannot tell a typo from a page the author means to create, so both are offered.
- **Test:** the measurement defect (`safety-briefings`, near match `safety-briefing`); a target with no near match (one option); a target differing from an existing page only in case (near match, ratio 1); a group target at the cap.

### SCAT-LINK-DANGLING-BODY
- **Severity:** error. **Fires:** every status.
- **Trigger:** a body link whose target has no page `<target>.md`. Links inside code spans and fenced code blocks are not body links.
- **Message:**
```
error [SCAT-LINK-DANGLING-BODY] <file>:<line> link [[<target>]]: does not exist (no file <target>.md)
  Fix, choose one:
    1. on line <line> replace `[[<target>]]` with `[[<near match>]]`                    (only if a near match exists among all pages)
    2. run `scat stub <target> --type <key>` (REPL: `scat_kg.stub("<target>", type="<key>")`) to create a <key> page      (one numbered option per inferred type, decision 3)
    n. on line <line> replace `[[<target>]]` with `<target>` to keep the words and drop the link
```
Types the page type discourages for body links are left out of the stubs, and the message adds "(<key> left out: a <page-type> page should not link to it)".
- **Fix kind:** options. The type is not written down at a body link, so the stub options are alternatives, not a guess (decision 3).
- **Test:** a body link in a coded scenario to a name that a frontmatter field elsewhere also names (one inferred type); to a name nothing else names (four options, minus `technology` on a scenario); a near match; a body link inside a code fence (no message).

### SCAT-LINK-DISCOURAGED
- **Severity:** warning. **Fires:** every status.
- **Trigger:** a field the page type lists as discouraged is present and non-empty (`technologies` on a coded scenario; `groups` on a coded architecture). One message per page and field. Endpoint and dangling checks still apply to its items.
- **Message:**
```
warning [SCAT-LINK-DISCOURAGED] <file>:<line> field `<field>`: a <type-key> record is about <what the type relates>, so linking <class> pages here is discouraged: [[<t1>]], [[<t2>]]
  Fix, choose one:
    1. delete `<field>:` and its list items
    2. keep the point by linking what they offer: add to `<affordances|concerns>` (suggestions you confirm) - "[[<s1>]]"
```
For a coded scenario the reason reads "a scenario relates groups, concerns and affordances; technologies stay in the background"; for a coded architecture, "an architecture relates concerns, affordances and technologies; stakeholders are abstracted away". The suggestions are `S(affordances)` computed from the field's technologies, or `S(concerns)` computed from the field's groups. Option 2 is left out when there are none.
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
- **Trigger:** the vault holds more pages of type `stakeholder-group`, at any status, than the cap in `<config-file>` (page-contracts names the file and key).
- **Message:**
```
error [SCAT-CAP] <config-file> field `<cap-key>`: the vault holds <n> stakeholder-group pages, over the cap of <cap>: <name>, <name>, ...
  Fix, choose one:
    1. write `<cap-key>: <n>` in <config-file> (the cap protects against identifying individuals; raise it only if the plan allows)
    2. fold <n minus cap> group(s) into the others (move their standpoints into another group's `description`) and delete those pages
```
- **Fix kind:** options. Option 2 is not exact: which groups merge is the facilitator's judgement, and the tools do not choose.
- **Test:** a fixture with cap 3 and 4 groups (one message, naming all four); with 3 groups (none); the fourth group as a stub still triggers.

### SCAT-CAP-CONFIG
- **Severity:** error. **Fires:** vault level.
- **Trigger:** `<config-file>` is absent, or lacks `<cap-key>`, or its value is not a whole number of at least 1.
- **Message:**
```
error [SCAT-CAP-CONFIG] <config-file> field `<cap-key>`: <the file is missing | the key is missing | the value `<value>` is not a whole number of at least 1>
  Fix: write `<cap-key>: <number you choose>` (author) in <config-file>; the vault has <n> stakeholder-group pages now, so choose <n> or more
```
- **Fix kind:** slot. Why not exact: the cap is a planning decision.
- **Test:** the file removed; the key removed; `<cap-key>: three`; `<cap-key>: 0`.

### SCAT-CONFLICT-BOTH
- **Severity:** warning (D3). **Fires:** every status.
- **Trigger:** a coded record (`scenario-coded` or `architecture-coded`) lists in `concerns` two existing concern pages A and B such that {A, B} is in the conflict relation. The relation is the symmetric closure of the declarations: {A, B} is in it when A's `conflicts` lists B, or B's `conflicts` lists A, or both. A one-sided declaration is complete: no message asks for the other side. A concern listing itself is ignored. One message per record and per pair, pairs sorted by name.
- **Message:**
```
warning [SCAT-CONFLICT-BOTH] <file>:<line> field `concerns`: this record holds both [[<A>]] and [[<B>]], which conflict (declared on <declaring page(s)>)
  Fix: none needed if both belong in this record. Holding both sides is allowed and is what the warning marks, a place where two concerns pull apart. If one was coded here by mistake, delete its line `- "[[<A or B>]]"` under `concerns`.
```
- **Fix kind:** advisory. Why: the graph holds disagreement and does not resolve it (log D-028), so the rule must not ask for the difference to be removed.
- **Test:** record lists both with a declaration on A only, on B only, and on both (one message each case, same text apart from "declared on"); lists one only (none); lists both with no declaration (none); a draft and a done record (same message).

### SCAT-MENTION
- **Severity:** warning (basic). **Fires:** every status. Not on raw or class pages.
- **Trigger:** the body of a page contains, as plain text, the `title` or the page name of an existing page of type `stakeholder-group`, `concern`, `affordance` or `technology`, matched case-insensitively at word boundaries, for a title or name of at least 4 characters, outside code, outside any wikilink, and when the body has no link to that page. Not the page itself. Not a page of a class that the page type discourages for body links. Reported once per page and target, at the first occurrence. No stemming, no plurals.
- **Message:**
```
warning [SCAT-MENTION] <file>:<line> text `<as written>`: names the <type-key> page [[<page-name>]] but does not link it
  Fix: on line <line> replace `<as written>` with `[[<page-name>|<as written>]]`          (`[[<page-name>]]` when the text is the page name)
```
- **Fix kind:** exact. Raw pages are exempt because they keep the story as told (facilitation capability 10); linking happens in the coded page.
- **Test:** a coded page mentioning a concern's title once in plain text (one message), once plain and once linked (none), inside a code span (none), and a technology on a scenario (none).

### SCAT-RAW-BACKLINK
- **Severity:** warning. **Fires:** every status. Raw pages.
- **Trigger:** coded page C lists raw page R in `raw`, C's type is the target type of R's `coded` field, and R's `coded` does not list C. One message per C. (Reported on R, so the fix is in the file named.)
- **Message:**
```
warning [SCAT-RAW-BACKLINK] <raw-file> field `coded`: [[<C>]] lists this page in `raw`, but this page does not list it
  Fix: under `coded:` in <raw-file> add the line `- "[[<C>]]"`       (when `coded` is absent, add `coded:` and then that line)
```
- **Fix kind:** exact. This is the raw-to-coded warning; the link is advice, never an error (mission non-goal).
- **Test:** coded page with `raw` naming R and R with no `coded`; with `coded` naming another page; with `coded` naming C (none).

### SCAT-RAW-UNCODED
- **Severity:** warning. **Fires:** status `done`. Raw pages. **Needs status.**
- **Trigger:** raw page R has status `done`, its `coded` is empty, and no page lists R in `raw`.
- **Message:**
```
warning [SCAT-RAW-UNCODED] <raw-file> field `coded`: status is done but no coded page derives from this page
  Fix: choose a name for the coded page, run `scat stub <coded-page-name> --type <scenario-coded|architecture-coded> ` (REPL: `scat_kg.stub("<coded-page-name>", type="<...>")`), then write `raw:` with the line `- "[[<R>]]"` in it (author: the name)
```
The type is `scenario-coded` for a raw scenario and `architecture-coded` for a raw architecture.
- **Fix kind:** slot. Why not exact: the coded page's name is the author's.
- **Test:** done raw page with nothing coded (message); the same at draft (none); after adding a coded page with `raw` (SCAT-RAW-BACKLINK instead).

### SCAT-INDEX-STALE
- **Severity:** warning. **Fires:** every status. Class pages and the vault.
- **Trigger:** a class page is missing for one of the four classes, or its generated index differs from what `index` would write from the instance pages (page-contracts defines the generated part). The check compares and never writes.
- **Message:**
```
warning [SCAT-INDEX-STALE] <class-file> index table: <the page is missing | the table differs from the <type-key> pages>
  Fix: run `scat index` (REPL: `scat_kg.index()`)
```
- **Fix kind:** exact.
- **Test:** add an instance page without running `index` (one message on its class page); delete a class page (one message); run `index` and re-check (none).

## 4. Coverage

| Requirement | Rules |
|---|---|
| R-1 required fields and types | SCAT-FM-PARSE, SCAT-FM-REQUIRED, SCAT-FM-TYPE, SCAT-FM-INDEXES, SCAT-FM-SHAPE, SCAT-DONE-FIELD, SCAT-DONE-LINK, SCAT-LINK-SHAPE |
| R-1 relation endpoints | SCAT-LINK-ENDPOINT |
| R-1 linking rules, error level | SCAT-LINK-UNLISTED |
| R-1 linking rules, warning level (scenario to technology, architecture to stakeholder group; frontmatter and body) | SCAT-LINK-DISCOURAGED, SCAT-LINK-DISCOURAGED-BODY |
| R-1 stakeholder-group cap | SCAT-CAP, SCAT-CAP-CONFIG |
| R-1 valid status | SCAT-FM-STATUS |
| R-1 links to pages that do not exist | SCAT-LINK-DANGLING, SCAT-LINK-DANGLING-BODY |
| R-3 unfinished is never an error | SCAT-DRAFT-FIELD, SCAT-DRAFT-LINK (warnings at draft); nothing fires for `done` fields at stub |
| R-3 full contract at `done`; required-from-status | SCAT-DONE-FIELD, SCAT-DONE-LINK, SCAT-FM-REQUIRED |
| R-3 links and endpoints at every status | SCAT-LINK-SHAPE, SCAT-LINK-UNLISTED, SCAT-LINK-ENDPOINT, SCAT-LINK-DANGLING, SCAT-LINK-DANGLING-BODY |
| D3 conflict warning | SCAT-CONFLICT-BOTH |
| Unlinked-mention warning (basic) | SCAT-MENTION |
| Raw-to-coded warning | SCAT-RAW-BACKLINK, SCAT-RAW-UNCODED |
| Generated index (G2, R-11) | SCAT-INDEX-STALE |

TBox coverage map. One line per field or link rule of the TBox: `<kind> <type-key>.<field-or-class-key> -> <rule ids>`.
It is checked against `ontology/scat.ttl` by a script. Every required field, discouraged field and discouraged body
link of the TBox must appear.

```
required affordance.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required affordance.status -> SCAT-FM-REQUIRED
required affordance.title -> SCAT-FM-REQUIRED
required affordance.type -> SCAT-FM-REQUIRED
optional affordance.attributes -> SCAT-LINK-ENDPOINT, SCAT-LINK-DANGLING
required architecture-coded.affordances -> SCAT-DONE-LINK, SCAT-DRAFT-LINK
required architecture-coded.concerns -> SCAT-DONE-LINK, SCAT-DRAFT-LINK
required architecture-coded.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required architecture-coded.raw -> SCAT-DONE-LINK, SCAT-DRAFT-LINK
required architecture-coded.status -> SCAT-FM-REQUIRED
required architecture-coded.technologies -> SCAT-DONE-LINK, SCAT-DRAFT-LINK
required architecture-coded.title -> SCAT-FM-REQUIRED
required architecture-coded.type -> SCAT-FM-REQUIRED
discouraged-field architecture-coded.groups -> SCAT-LINK-DISCOURAGED
discouraged-body-link architecture-coded.stakeholder-group -> SCAT-LINK-DISCOURAGED-BODY
required architecture-raw.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required architecture-raw.status -> SCAT-FM-REQUIRED
required architecture-raw.title -> SCAT-FM-REQUIRED
required architecture-raw.type -> SCAT-FM-REQUIRED
discouraged-body-link architecture-raw.stakeholder-group -> SCAT-LINK-DISCOURAGED-BODY
optional architecture-raw.coded -> SCAT-RAW-BACKLINK, SCAT-RAW-UNCODED
required class.description -> SCAT-DONE-FIELD
required class.indexes -> SCAT-FM-REQUIRED
required class.title -> SCAT-FM-REQUIRED
required class.type -> SCAT-FM-REQUIRED
required concern.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required concern.status -> SCAT-FM-REQUIRED
required concern.title -> SCAT-FM-REQUIRED
required concern.type -> SCAT-FM-REQUIRED
optional concern.addresses -> SCAT-LINK-ENDPOINT, SCAT-LINK-DANGLING
optional concern.conflicts -> SCAT-CONFLICT-BOTH
required scenario-coded.affordances -> SCAT-DONE-LINK, SCAT-DRAFT-LINK
required scenario-coded.concerns -> SCAT-DONE-LINK, SCAT-DRAFT-LINK
required scenario-coded.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required scenario-coded.groups -> SCAT-DONE-LINK, SCAT-DRAFT-LINK
required scenario-coded.raw -> SCAT-DONE-LINK, SCAT-DRAFT-LINK
required scenario-coded.status -> SCAT-FM-REQUIRED
required scenario-coded.title -> SCAT-FM-REQUIRED
required scenario-coded.type -> SCAT-FM-REQUIRED
discouraged-field scenario-coded.technologies -> SCAT-LINK-DISCOURAGED
discouraged-body-link scenario-coded.technology -> SCAT-LINK-DISCOURAGED-BODY
required scenario-raw.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required scenario-raw.status -> SCAT-FM-REQUIRED
required scenario-raw.title -> SCAT-FM-REQUIRED
required scenario-raw.type -> SCAT-FM-REQUIRED
discouraged-body-link scenario-raw.technology -> SCAT-LINK-DISCOURAGED-BODY
optional scenario-raw.coded -> SCAT-RAW-BACKLINK, SCAT-RAW-UNCODED
required stakeholder-group.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required stakeholder-group.status -> SCAT-FM-REQUIRED
required stakeholder-group.title -> SCAT-FM-REQUIRED
required stakeholder-group.type -> SCAT-FM-REQUIRED
optional stakeholder-group.heldby -> SCAT-LINK-ENDPOINT, SCAT-LINK-DANGLING
required technology.description -> SCAT-DONE-FIELD, SCAT-DRAFT-FIELD
required technology.status -> SCAT-FM-REQUIRED
required technology.title -> SCAT-FM-REQUIRED
required technology.type -> SCAT-FM-REQUIRED
```

## 5. Needs from the TBox

Nothing blocks. Two clarifications would remove a reading this catalogue had to choose:
- `scat:discouragedField` says "present and non-empty" but `scat:unlistedLinkLevel` says only "carries". The catalogue ignores an empty list in both cases. The TBox could say so for the unlisted rule.
- The status ranking used here (stub, then draft, then done) is read from `scat:StatusValues`, and "required from" from `scat:requiredFrom`; both are stated. The catalogue hard-codes that raw and class pages are exempt from SCAT-MENTION and that SCAT-RAW-UNCODED fires at `done`; these are rules and not schema, so they are not asked of the TBox.

## 6. Needs from the page contracts (WP4-U2)

- The link syntax for body links: aliases, headings, embeds, code spans and fences, and what counts as a legal page name (the stub operation refuses an illegal one; the message then drops its stub option and says the link name is not a legal page name).
- The configuration file and the cap key (`<config-file>`, `<cap-key>`) and its format.
- The generated part of a class page and its table (SCAT-INDEX-STALE), and whether `index` creates a missing class page (this catalogue assumes it does).
- What a stub page contains beyond the fields required from `stub` (the catalogue only requires that it have no error).
