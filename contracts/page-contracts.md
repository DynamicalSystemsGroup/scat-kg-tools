# Page contracts

What each kind of page looks like on disk in an SCAT vault, so that a person can write one by hand in Obsidian and the
tools can read, check and generate it. The TBox (`ontology/scat.ttl`) is authoritative for fields, link targets and
status values; this document adds what the TBox leaves out: file names, how links are written, what a link entails,
the index table and the vault configuration. It does not say how serious a breach is, or what message a tool gives:
that is the rule catalogue (`contracts/rule-catalogue.md`), and "the catalogue" below means it.

## 1. Pages

**A page** is a Markdown file ending `.md`, anywhere in the vault outside folders whose name starts with a dot, whose
frontmatter has a `type` key. Other Markdown files (a README, say) are not pages and are ignored.

**Layout.** The tools put each page they create in the folder named for its type, at the vault root:
`stakeholder-group/`, `concern/`, `affordance/`, `technology/`, `scenario-raw/`, `scenario-coded/`,
`architecture-raw/`, `architecture-coded/`, and `class/`. A page by hand may go in any folder: the folder is never
checked, and the `type` key alone says what the page is.

**Shape of a file.**

```
---
type: concern
status: draft
title: "Safe handling of tools"
description: "Borrowers want to be sure a tool is safe to use."
addresses:
  - "[[safety-briefing]]"
---

Free text in Markdown. Nothing in it is required.
```

- UTF-8, and the tools write LF line endings (they read CRLF too).
- The frontmatter is a YAML block between two lines of exactly `---`, at the very top of the file.
- Keys are written exactly as in the field tables below. The order does not matter; the tables' order is the one the
  tools write.
- `title` and `description` are always written in double quotes, on one line (a `"` inside is written `\"`). `type` and
  `status` are written bare.
- Keys that the TBox does not list for the page type, and that hold no wikilink, are ignored (you may add your
  own note keys). A key that is a link field of some other page type is not ignored: see 3.

**Status.** Every page except a class page has `status`: `stub`, `draft` or `done`, in that order.
- `stub`: the page exists because something links to it, or has just been started. Only `type`, `status` and `title`
  are required.
- `draft`: being written. The required fields are the same as for `stub`; the fields that `done` requires are the
  author's to-do list, and how a tool grades their absence on a draft is the catalogue's call.
- `done`: the author judges the page complete. Every required field in the page type's table must be present, and
  every required link field non-empty.
- At every status, every link is checked: it must reach a page that exists, and that page must be of the type the
  field names. Being unfinished is never a fault in itself.

**The field tables** below give each key's "Required from": `stub` (present at every status), `done` (required once the
page is `done`), `always` (class pages, which carry no status), `optional` (may be present), or `discouraged` (allowed,
but graded as a warning when present and non-empty). A link field is a list of wikilinks. A link field that a page
type's table does not list is not permitted on that page type.

## 2. Names and addresses

**The page name is the file name without `.md`.** It is the only address: a link writes the name and nothing else, so
the name is unique across the whole vault, whatever the type or folder.

**The name is a slug.** It must match all of:
- only the characters `a` to `z`, `0` to `9` and the hyphen `-`;
- starts and ends with a letter or digit, and never has two hyphens in a row;
- at most 64 characters;
- not one of the reserved names: `con`, `prn`, `aux`, `nul`, `com1` to `com9`, `lpt1` to `lpt9` (Windows device names),
  and `stakeholder-groups`, `concerns`, `affordances`, `technologies` (the class pages, see 8).

This one rule covers the platforms. Lower case only means two names can never differ by case, so a case-insensitive
file system (macOS, Windows) and a case-sensitive one (Linux) see the same set of names. ASCII only means no accent can
be stored in two forms. No spaces, slashes, colons, quotes, question marks, asterisks, angle brackets, pipes, trailing
dots or trailing spaces can occur, which are the characters unsafe on one platform or another. The extension is
exactly `.md`, lower case.

**The title is the name as a person reads it.** It is free text, any language, and is what an index table shows. The
name is made from the title like this, and the tools use it whenever they propose a name:
1. lower-case the title and drop accents (decompose, then remove the combining marks);
2. replace every run of characters outside `a-z0-9` with one `-`, and trim `-` from both ends;
3. cut to 64 characters and trim a trailing `-`;
4. if that name is taken, add `-2`, then `-3`, and so on, until it is free.

"Safe handling of tools" gives `safe-handling-of-tools`. If step 3 leaves nothing (a title with no Latin letters or
digits), choose a name by hand. After a page exists, its title and its name are independent: editing the title does not
rename the file, and nothing checks that they agree. Rename a file in Obsidian, which rewrites the links to it.

**A link resolves only on the exact name.** `[[Safety-Briefing]]` does not reach `safety-briefing.md`, though Obsidian
would follow it. A link that differs from an existing name only by case, or is not a slug at all (`[[Safety
briefing]]`), is a bad link: the fix is to write the exact slug name. The stub operation never creates a page for it
(see 5).

## 3. How links are written

**In frontmatter**, a link is the quoted wikilink `"[[page-name]]"`: the name only, with no `.md`, no folder, no
`#heading` and no `|alias`. A link field is always a YAML list, even for one item, and an empty list `[]` or an absent
key both mean no links:

```
heldby:
  - "[[safe-handling-of-tools]]"
  - "[[opening-hours]]"
```

The quotes are required: without them YAML reads `[[x]]` as a nested list. The flow form `["[[a]]", "[[b]]"]` is the
same list; the tools write the block form above.

**Typed edges.** A frontmatter link field is a typed edge: the key says what the link means (the three relations, the
conflict relation, the coded-to-raw derivation and the record-to-class links), and the TBox says which page type its
target must be. Only these ten keys are link fields: `heldby`, `addresses`, `attributes`, `conflicts`, `groups`,
`concerns`, `affordances`, `technologies`, `raw` and `coded`. `raw` and `coded` each have a different target on
scenario and architecture pages; section 7 gives the target of each.

**In the body**, a link is `[[page-name]]`, optionally `[[page-name|text to show]]` or `[[page-name#Heading]]`; the
tools read the part before `|` and `#`. A body link is untyped: it says "see also" and nothing more, so it is never
read into the graph as a relation. Two checks still look at it:
- it must reach a page that exists;
- a scenario page's body should not link a `technology` page, and an architecture page's body should not link a
  `stakeholder-group` page (warning-level, as the TBox says).

An embed `![[page-name]]` is read as a body link. Links elsewhere in frontmatter (a key that is not a link field) are
ignored.

## 4. The three relations and the conflict relation

The three relations are not page types and have no pages. Each is a link field on the page of the first member of the
pair, so you write a relation by editing one page:

| Relation | Written on | Key | Reads as |
|---|---|---|---|
| Heldby | `stakeholder-group` page | `heldby` | (group, concern): the concerns this group holds |
| Addresses | `concern` page | `addresses` | (concern, affordance): the affordances that address this concern |
| Attributes | `affordance` page | `attributes` | (affordance, technology): the technologies this affordance is attributed to |

Each is many-to-many: one concern may be listed by several groups, one group may list several concerns. To see which
groups hold a concern, use Obsidian's backlinks on the concern page; the concern page does not repeat them. Writing a
relation on the wrong page is the unlisted-link-field case (1): `heldby` on a concern page is not permitted.

**The conflict relation (D1) is the optional link field `conflicts` on concern pages**, a list of concern wikilinks.
There is no conflict page. It shows a tension between two concerns and never ranks or resolves it.
- It is symmetric. A concern `a` listing `b` states the conflict for both: you do not also write it on `b`. A
  one-sided declaration is complete, and the tools read the pair `{a, b}` as the union of what `a` and `b` each list.
- The tools never add the other side for you. Writing it on both is allowed and means the same thing.
- A concern does not list itself.
- Groups that share a concern and differ on others need nothing more: two group pages list the same concern in
  `heldby`, and other concerns of theirs are linked by `conflicts`.

## 5. What a link entails: the stub operation

Every wikilink must reach an existing page. The stub operation creates the pages that links entail and are missing. It
writes only new files, never an existing page, and it is an explicit operation: checks never run it.

**A link in a link field entails a page of the field's target type.** The new page has exactly:

```
---
type: <the target type's slug>
status: stub
title: "<the name with each - replaced by a space, first letter upper case>"
---
```

and an empty body. For example, `affordances: ["[[safety-briefing]]"]` on a coded scenario creates
`affordance/safety-briefing.md` with type `affordance` and title "Safety briefing". The author edits the title after.

| Link field | Page it entails (`type`) |
|---|---|
| `heldby`, `conflicts`, `concerns` | `concern` |
| `addresses`, `affordances` | `affordance` |
| `attributes`, `technologies` | `technology` |
| `groups` | `stakeholder-group` |
| `raw` on a `scenario-coded` page | `scenario-raw` |
| `raw` on an `architecture-coded` page | `architecture-raw` |
| `coded` on a `scenario-raw` page | `scenario-coded` |
| `coded` on an `architecture-raw` page | `architecture-coded` |

For the two pairs raw and coded only, the new stub also gets the opposite link back to the page that entailed it
(`raw: ["[[the-raw-page]]"]` on a new coded stub; `coded: ["[[the-coded-page]]"]` on a new raw stub), because that link
is certain and the coded page requires it at `done`. Nothing else is pre-filled.

**A link in the body entails a page, but not its type.** The body does not say what the page is, and guessing would put
words in the coder's mouth. So the stub operation creates a page for a body link only when it is given the type slug
explicitly (the same slug that appears in `type`), and then it creates it exactly as above. With no type, it creates
nothing and reports the link. The usual way to give a body link a type is to name the page in the right link field of
the same page, which entails the stub with that type and makes the body link resolve.

**Other cases.**
- A link whose target exists but has the wrong type entails nothing: it is a wrong-endpoint problem, and the author
  decides whether the link or the page's `type` is wrong.
- A link that is not an exact slug name (2) entails nothing: it is corrected in the link.
- The four class pages are entailed by the TBox itself. If one is missing, the stub operation (and the index operation)
  creates it as in 8. They are not created from links.

## 6. Page types: summary

| `type` | A page of this type is | Folder |
|---|---|---|
| `stakeholder-group` | one stakeholder group | `stakeholder-group/` |
| `concern` | one concern | `concern/` |
| `affordance` | one affordance | `affordance/` |
| `technology` | one technology | `technology/` |
| `scenario-raw` | a scenario as told | `scenario-raw/` |
| `scenario-coded` | a reading of a raw scenario | `scenario-coded/` |
| `architecture-raw` | an architecture pitch as given | `architecture-raw/` |
| `architecture-coded` | a reading of a raw architecture | `architecture-coded/` |
| `class` | the page of one of the four classes | `class/` |

Every page type has the keys `type`, `status`, `title` and `description` (a class page has no `status`). The rest are in
the tables. The value of `type` is the slug in the first column.

## 7. Page types: fields

### `stakeholder-group`

One page per stakeholder group: who the group is, in the group's own terms, and the concerns it holds. A group, never
a named person. The number of these pages is capped for the vault (section 10).

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `stakeholder-group` | | stub |
| `status` | `stub`, `draft` or `done` | | stub |
| `title` | text | | stub |
| `description` | text, one sentence | | done |
| `heldby` | list of wikilinks | `concern` | optional |

```
---
type: stakeholder-group
status: done
title: "Volunteer staff"
description: "The people who run the lending desk on open days."
heldby:
  - "[[safe-handling-of-tools]]"
---
```

### `concern`

One page per concern: what the interest is, the affordances that address it, and any concerns it conflicts with.

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `concern` | | stub |
| `status` | `stub`, `draft` or `done` | | stub |
| `title` | text | | stub |
| `description` | text, one sentence | | done |
| `addresses` | list of wikilinks | `affordance` | optional |
| `conflicts` | list of wikilinks | `concern` | optional |

```
---
type: concern
status: done
title: "Safe handling of tools"
description: "Borrowers want to be sure a tool is safe to use."
addresses:
  - "[[safety-briefing]]"
conflicts:
  - "[[quick-checkout]]"
---
```

### `affordance`

One page per affordance: what is offered, and the technologies it is attributed to.

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `affordance` | | stub |
| `status` | `stub`, `draft` or `done` | | stub |
| `title` | text | | stub |
| `description` | text, one sentence | | done |
| `attributes` | list of wikilinks | `technology` | optional |

```
---
type: affordance
status: draft
title: "Safety briefing"
attributes:
  - "[[booking-app]]"
---
```

### `technology`

One page per technology: what the part is. It has no link field.

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `technology` | | stub |
| `status` | `stub`, `draft` or `done` | | stub |
| `title` | text | | stub |
| `description` | text, one sentence | | done |

```
---
type: technology
status: stub
title: "Booking app"
---
```

### `scenario-raw`

A raw scenario: the told story in the page body, kept as told, linked to the coded scenarios derived from it. Events
stay in the body. The body should not link a `technology` page.

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `scenario-raw` | | stub |
| `status` | `stub`, `draft` or `done` | | stub |
| `title` | text | | stub |
| `description` | text, one sentence | | done |
| `coded` | list of wikilinks | `scenario-coded` | optional |

```
---
type: scenario-raw
status: done
title: "Saturday at the lending desk"
description: "Notes from the volunteer session on a busy open day."
coded:
  - "[[saturday-desk-coded]]"
---

(the notes as taken, unedited)
```

### `scenario-coded`

A coded scenario: links to its raw scenario, and to the groups, concerns and affordances found in it. It should not
link technologies, and its body should not link a `technology` page.

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `scenario-coded` | | stub |
| `status` | `stub`, `draft` or `done` | | stub |
| `title` | text | | stub |
| `description` | text, one sentence | | done |
| `raw` | list of wikilinks | `scenario-raw` | done |
| `groups` | list of wikilinks | `stakeholder-group` | done |
| `concerns` | list of wikilinks | `concern` | done |
| `affordances` | list of wikilinks | `affordance` | done |
| `technologies` | list of wikilinks | `technology` | discouraged |

```
---
type: scenario-coded
status: done
title: "Saturday at the lending desk, coded"
description: "A reading of the busy-open-day scenario."
raw:
  - "[[saturday-at-the-lending-desk]]"
groups:
  - "[[volunteer-staff]]"
concerns:
  - "[[safe-handling-of-tools]]"
affordances:
  - "[[safety-briefing]]"
---
```

### `architecture-raw`

A raw architecture: the pitch in the page body, kept as given, linked to the coded architectures derived from it. The
body should not link a `stakeholder-group` page.

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `architecture-raw` | | stub |
| `status` | `stub`, `draft` or `done` | | stub |
| `title` | text | | stub |
| `description` | text, one sentence | | done |
| `coded` | list of wikilinks | `architecture-coded` | optional |

```
---
type: architecture-raw
status: draft
title: "Self-service kiosk pitch"
coded:
  - "[[kiosk-pitch-coded]]"
---
```

### `architecture-coded`

A coded architecture: links to its raw architecture, and to the concerns, affordances and technologies found in it. It
should not link stakeholder groups, and its body should not link a `stakeholder-group` page.

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `architecture-coded` | | stub |
| `status` | `stub`, `draft` or `done` | | stub |
| `title` | text | | stub |
| `description` | text, one sentence | | done |
| `raw` | list of wikilinks | `architecture-raw` | done |
| `concerns` | list of wikilinks | `concern` | done |
| `affordances` | list of wikilinks | `affordance` | done |
| `technologies` | list of wikilinks | `technology` | done |
| `groups` | list of wikilinks | `stakeholder-group` | discouraged |

```
---
type: architecture-coded
status: done
title: "Self-service kiosk, coded"
description: "A reading of the kiosk pitch."
raw:
  - "[[self-service-kiosk-pitch]]"
concerns:
  - "[[quick-checkout]]"
affordances:
  - "[[self-checkout]]"
technologies:
  - "[[booking-app]]"
---
```

### `class`

The page of one of the four classes: a description of the class, and the index table of its instances (8). It carries
no status, so every field here is required at all times.

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `class` | | always |
| `title` | text | | always |
| `description` | text, one sentence | | always |
| `indexes` | `stakeholder-group`, `concern`, `affordance` or `technology` | | always |

```
---
type: class
title: "Concerns"
description: "Every concern in the vault, with the affordances that address it."
indexes: concern
---
```

## 8. Class pages and their index tables

There are four class pages, one per class, with these names (they are reserved, see 2) and `indexes` values:

| Page name | `indexes` | Default title |
|---|---|---|
| `stakeholder-groups` | `stakeholder-group` | "Stakeholder groups" |
| `concerns` | `concern` | "Concerns" |
| `affordances` | `affordance` | "Affordances" |
| `technologies` | `technology` | "Technologies" |

A class page is the frontmatter above, then your description of the class in the body, then the generated region:

```
<!-- scat:index:start -->
| Name | Description | Link |
|---|---|---|
| Safe handling of tools | Borrowers want to be sure a tool is safe to use. | [[safe-handling-of-tools]] |
| Quick checkout | Borrowers want to leave with a tool in a minute. | [[quick-checkout]] |
<!-- scat:index:end -->
```

- **Rows.** One row for every page whose `type` equals the `indexes` value, at every status (a stub is a row).
- **Columns.** `Name` is the page's `title`; `Description` is its `description` (empty if it has none); `Link` is the
  wikilink `[[page-name]]`. In a cell, `|` is written `\|`, and the text is on one line.
- **Order.** By page name, ascending, in plain character order (names are ASCII, so there is one order).
- **Markers.** The two lines `<!-- scat:index:start -->` and `<!-- scat:index:end -->` are exact, each on a line of its
  own. The index operation replaces everything between them, header included, and nothing outside them. Do not edit
  between them: the next run overwrites it. With no instances the region holds the header and separator rows only. If a
  page lacks the markers, the operation appends the region at the end of the body.
- **When missing.** If a class page does not exist, the stub or index operation creates it with the default title, the
  `indexes` value, a `description` that is the page type's one-sentence description from the TBox, an empty body and the
  region.

## 9. Raw and coded pages

- A raw page holds the notes as told, in its body, unedited. It links to its coded pages with `coded`, which is
  optional: enforcing it is a non-goal, and the catalogue grades a raw page with no coded page as a warning.
- A coded page links to the raw page it was read from with `raw`, a list: a coded page may be derived from more than
  one raw page, and one raw page may have several coded pages. `raw` is required at `done`.
- The two sides are separate, so the same relation can be written on both. The tools never write one for you, except
  the pre-filled link on a new stub (5).
- A raw page is linked, not embedded: the contract has no embed. An `![[...]]` embed in a body is an ordinary body link.
- The target of `raw` and `coded` follows the page's own pair: scenarios link scenarios, architectures link
  architectures. A scenario linking an architecture is a wrong endpoint.

## 10. Vault configuration: the stakeholder-group cap

The cap is not in the TBox. It is set per vault in a file named **`scat.toml` at the vault root**, in TOML:

```
stakeholder_group_cap = 3
```

- The value is a whole number of 1 or more. The tools read this key and ignore any other key in the file.
- The count is the number of pages with `type: stakeholder-group`, at every status, stubs included.
- The cap is checked over the whole vault. A vault above the cap is not conformant.
- There is no default: if the file or the key is missing, or the value is not such a number, that is itself a
  configuration problem for the catalogue to report.

## 11. Agreement with the TBox

Every key in the field tables is a `scat:key` of a field of that page type in the TBox, and every field the TBox lists
for a page type is in its table, with the TBox's level (`requiredField` with its `requiredFrom`, `optionalField`,
`discouragedField`). The `unlistedLinkLevel`, `wrongTargetLevel` and `discouragedBodyLink` statements are the TBox's;
this document only says where a person writes the links they govern. Things in this document that the TBox does not
state (names, folders, the markers, the sort order, the cap file, what a link entails) are the contract's own.

## 12. Needs from the TBox

Nothing blocks this contract. Three points for the PM:
- The TBox does not say a concern may not list itself in `conflicts`; section 4 says so. The catalogue may want a rule,
  or the TBox a note.
- The TBox gives no rule for which page a body link entails. Section 5 decides (no type without an explicit one) and
  needs no TBox term; it is recorded here so the catalogue's dangling-link fix for a body link is two-step.
- `scat:requiredFrom` on `description` is `done`, but a class page has no status. This contract reads that, with
  `carriesStatus false`, as "always required" (section 7, `class`). The TBox is consistent with that reading, but says
  it only in a comment.
