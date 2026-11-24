# Page contracts

What each kind of page looks like on disk in an SCAT vault, so that a person can write one by hand in Obsidian and the
tools can read, check and generate it. The TBox (`ontology/scat.ttl`) is authoritative for fields, link targets and
status values; this document adds what the TBox leaves out: file names, how links are written, what a link entails,
the index table and the vault configuration. It does not say how serious a breach is, or what message a tool gives:
that is the rule catalogue (`contracts/rule-catalogue.md`), and "the catalogue" below means it.

## 1. Pages

**A page** is a Markdown file ending `.md`, anywhere in the vault outside folders whose name starts with a dot, whose
frontmatter has a `type` key. Other Markdown files (a README, say) are not pages and are ignored. The vault's Obsidian
page-template folder (10) is not read, nor is `.obsidian/`.

**Layout.** The tools put each page they create in the folder named for its type, at the vault root:
`stakeholder-group/`, `concern/`, `affordance/`, `technology/`, `heldby/`, `addresses/`, `attributes/`, `scenario-raw/`, `scenario-coded/`,
`architecture-raw/`, `architecture-coded/`, and `class/`. A page by hand may go in any folder: the folder is never
checked, and the `type` key alone says what the page is.

**Shape of a file.**

```
---
type: concern
status: draft
title: "Safe handling of tools"
description: "Borrowers want to be sure a tool is safe to use."
conflicts:
  - "[[quick-checkout]]"
---

Free text in Markdown. Nothing in it is required.
```

- UTF-8, and the tools write LF line endings (they read CRLF too).
- The frontmatter is a YAML block between two lines of exactly `---`, at the very top of the file.
- Keys are written exactly as in the field tables below. The order does not matter; the tables' order is the one the
  tools write.
- `title`, `description` and `notes` are on one line. The tools always write them in double quotes; by hand the quotes
  are required only when the text contains `:` or `#`, starts with a quote, or has other characters YAML treats
  specially (a bare colon or `#` in an unquoted value breaks the YAML). Unquoted plain text is accepted. Inside
  quotes, `"` is written `\"` and `\` is written `\\`. `type` and `status` are written bare.
- Keys that the TBox does not list for the page type, are ignored, whatever they hold (you may add your
  own note keys). A key that is a link field of some other page type is not ignored: see 3.

**Status.** Every page except a class page has `status`: `stub`, `draft` or `done`, in that order.
- `stub`: the page exists because something links to it, or has just been started. Only the fields the tables mark "stub" are
  required: `type`, `status` and `title`, and on a relation page its two endpoint links.
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
- not one of the reserved names: `con`, `prn`, `aux`, `nul`, `com0` to `com9`, `lpt0` to `lpt9` (Windows device names),
  and the seven class page names `stakeholder-groups`, `concerns`, `affordances`, `technologies`, `heldby-pairs`,
  `addresses-pairs`, `attributes-pairs` (see 8).

This one rule covers the platforms. Lower case only means two names can never differ by case, so a case-insensitive
file system (macOS, Windows) and a case-sensitive one (Linux) see the same set of names. ASCII only means no accent can
be stored in two forms. No spaces, slashes, colons, quotes, question marks, asterisks, angle brackets, pipes, trailing
dots or trailing spaces can occur, which are the characters unsafe on one platform or another. The extension is
exactly `.md`, lower case.

**The title is the name as a person reads it.** It is free text, any language, and is what an index table shows. The
name is made from the title like this, and the tools use it whenever they propose a name:
1. decompose the title with Unicode NFKD, remove the combining marks (Unicode category M), then lower-case it (so
   `É` becomes `e`).
   Letters that do not decompose (`ß`, `ø`, `æ`, any non-Latin script) are not in `a-z0-9` and are treated as the
   characters in step 2: they become hyphens, they are never transliterated;
2. replace every run of characters outside `a-z0-9` with one `-`, and trim `-` from both ends;
3. cut to 64 characters and trim a trailing `-`: this is the stem;
4. the stem is the name unless it is taken: the name of any existing `.md` file (a Markdown file without `type` is not a page but still blocks the name), or a reserved name (including the seven
   class page names and `con`), counts as taken; names are compared without regard to case. Then try `<stem>-2`, `<stem>-3`, and so on, cutting the stem first so
   the whole name stays within 64 characters (trim a trailing `-` from the cut stem before adding the suffix), until
   the name is free.

A derived name is therefore always a legal name. "Safe handling of tools" gives `safe-handling-of-tools`. If step 3 leaves nothing (a title with no Latin letters or
digits), choose a name by hand. After a page exists, its title and its name are independent: editing the title does not
rename the file, and nothing checks that they agree. Rename a file in Obsidian, which rewrites the links to it.

**A link resolves only on the exact name.** `[[Safety-Briefing]]` does not reach `safety-briefing.md`, though Obsidian
would follow it. A link that differs from an existing name only by case, or is not a slug at all (`[[Safety
briefing]]`), is a bad link: the fix is to write the exact slug name. The stub operation never creates a page for it
(see 5).

## 3. How links are written

**In frontmatter**, a link is the quoted wikilink `"[[page-name]]"`: the name only, with no `.md`, no folder, no
`#heading` and no `|alias`. A link field is either a list or a single link, as the field tables say.

A **list field** is always a YAML list, even for one item, and an empty list `[]` or an absent key both mean no
links:

```
concerns:
  - "[[safe-handling-of-tools]]"
  - "[[opening-hours]]"
```

A **single-link field** (`group`, `concern`, `affordance`, `technology`) holds exactly one link, written as a plain
quoted scalar and not as a list: `concern: "[[safe-handling-of-tools]]"`. A list there, even of one, is wrong.

The quotes are required: without them YAML reads `[[x]]` as a nested list. The flow form `["[[a]]", "[[b]]"]` is the
same list; the tools write the block form above.

**Typed edges.** A frontmatter link field is a typed edge: the key says what the link means (an end of a relation, the
conflict relation, the coded-to-raw derivation, or a record-to-class link), and the TBox says which page type its
target must be. Only these eleven keys are link fields: `group`, `concern`, `affordance`, `technology` (single
links, on relation pages), `conflicts`, `groups`, `concerns`, `affordances`, `technologies` (lists), and `raw` and
`coded` (lists). `raw` and `coded` each have a different target on
scenario and architecture pages; section 7 gives the target of each.

**In the body**, a link is `[[page-name]]`, optionally `[[page-name|text to show]]` or `[[page-name#Heading]]`; the
tools strip `|...`, `#...` and `^...` (a block reference) and read the page name, which must exist. What is and is
not a body link:
- Text inside matched code spans and fenced code blocks is never a link. An indented code block is not code here, and
  an unmatched backtick starts nothing.
- An embed `![[page-name]]` of a page name is a body link.
- Markdown-style links `[text](target)` are not wikilinks and are ignored.
- The tests below apply to the target after stripping `|alias`, `#heading` and `^block`. A target left empty by the
  stripping (`[[^blk]]`, `[[|a]]`) is not a page link.
- A target that is not a page is not a page link, and is never checked or stubbed: anything containing a dot
  (`[[photo.png]]`, `[[v1.2-notes]]`; page names never contain a dot, see 2), anything with a `/`, and a same-page link
  `[[#Heading]]`.

A body link is untyped: it says "see also" and nothing more, so it is never
read into the graph as a relation. Two checks still look at it:
- it must reach a page that exists;
- a scenario page's body should not link a `technology` page, and an architecture page's body should not link a
  `stakeholder-group` page (warning-level, as the TBox says).

Links elsewhere in frontmatter (a key that is not a link field) are ignored.

## 4. The three relations and the conflict relation

**The three relations are page types, with an instance page for each pair.** A relation page states one fact and is
the one place that fact is written: there is no field for it on the group, concern or affordance page.

| Relation | `type` | The page states | Endpoint fields (each exactly one link) |
|---|---|---|---|
| Heldby | `heldby` | this group holds this concern | `group` (a `stakeholder-group`), `concern` (a `concern`) |
| Addresses | `addresses` | this affordance addresses this concern | `concern` (a `concern`), `affordance` (an `affordance`) |
| Attributes | `attributes` | this affordance is attributed to this technology | `affordance` (an `affordance`), `technology` (a `technology`) |

- **One page per pair.** The relation is many-to-many by many pages. A concern held by three groups has three `heldby`
  pages, one per group, so each group's account stays its own. The endpoints are required at every status, even on a
  stub: a relation page without both says nothing.
- **Where an account lives.** The optional `notes` field on a relation page holds a one-line account of that pair
  (for a `heldby` page, how that group holds that concern), quoted as `title` is (1). A longer account goes in the
  page body, which is free text.
- **Users need not write a relation page's structure.** The stub operation creates it with `type`, `status`, `title`
  and both endpoint links filled, from the pair the author names (5), and the author then writes only `description`,
  `notes` and the body. To write one by hand, copy the skeleton in 5. The endpoint order is the one in the table above.
- To see which groups hold a concern, use the index of `heldby` pages (`heldby-pairs`) or Obsidian's backlinks on the
  concern page. The concern page does not repeat them.
- A relation key written on the wrong page type (`group` on a concern page, say) is an unlisted link field (1), and is
  not permitted.

**The conflict relation (D1) is the optional link field `conflicts` on concern pages**, a list of concern wikilinks.
There is no conflict page. It shows a tension between two concerns and never ranks or resolves it. Checks concern structure only: tensions, matches and gaps are for analysis, after conformance passes and a coder signs off the content.
- It is symmetric. A concern `a` listing `b` states the conflict for both: you do not also write it on `b`. A
  one-sided declaration is complete, and the tools read the pair `{a, b}` as the union of what `a` and `b` each list.
- The tools never add the other side for you. Writing it on both is allowed and means the same thing.
- A concern does not list itself.
- Groups that share a concern and differ on others need nothing more: two `heldby` pages name the same concern, one
  for each group, and the concerns they differ on are linked by `conflicts`.

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
| `concern`, `conflicts`, `concerns` | `concern` |
| `affordance`, `affordances` | `affordance` |
| `technology`, `technologies` | `technology` |
| `group`, `groups` | `stakeholder-group` |
| `raw` on a `scenario-coded` page | `scenario-raw` |
| `raw` on an `architecture-coded` page | `architecture-raw` |
| `coded` on a `scenario-raw` page | `scenario-coded` |
| `coded` on an `architecture-raw` page | `architecture-coded` |

For the two pairs raw and coded only, the operation derives the opposite link itself, with no extra argument. When it
creates a raw page that coded pages name in `raw`, it writes `coded` on the new page, listing every coded page of the
matching kind that names it; when it creates a coded page that raw pages name in `coded`, it writes `raw` listing every
raw page that names it. So a stub made to fix a dangling `raw` or `coded` link starts with the link back already
there. Nothing else is pre-filled.

**A coded record entails no relation page by itself** (ACE ruling, log D-031: the contracts define how an author names a
pair, not which links entail relation pages). A coded scenario lists groups, concerns and affordances, but it
does not say which group holds which concern, or which affordance addresses which concern. Pairing every group with
every concern would state facts the coder never stated, so no list of links in a coded record entails a `heldby`,
`addresses` or `attributes` page, whatever it lists. A relation page is created only for a pair the author names, and
then it is entailed, not hand-written:
- the operation is `scat stub-pair <relation> <endpoint-a> <endpoint-b>` on the command line, and
  `scat_kg.stub_pair("<relation>", "<endpoint-a>", "<endpoint-b>")` in the REPL: the relation (`heldby`, `addresses` or
  `attributes`) and the two endpoint names, in the order of the table in 4 (group then concern; concern then
  affordance; affordance then technology);
- it creates the page below, and also stubs either endpoint that does not exist, by the table above;
- if a page of that relation with exactly those two endpoints already exists, under any name, it creates nothing and
  reports that page: one page per pair;
- the page is:

```
---
type: heldby
status: stub
title: "Volunteer staff holds Safe handling of tools"
group: "[[volunteer-staff]]"
concern: "[[safe-handling-of-tools]]"
---
```

The title is, by relation, "`<group title>` holds `<concern title>`", "`<affordance title>` addresses `<concern
title>`" or "`<affordance title>` attributed to `<technology title>`", using each endpoint's `title`. The page name is
made from that title by the rule in 2 (here `volunteer-staff-holds-safe-handling-of-tools`), so it is a slug and unique
like any other. The body is empty. A tool may print the pairs a coded record's links would allow, to choose from, but
creates none of them.

**A link in the body entails a page, but not its type.** The body does not say what the page is, and guessing would put
words in the coder's mouth. So the stub operation creates a page for a body link only when it is given the type slug
explicitly, and then it creates it exactly as above. The slugs it accepts are the four class keys
(`stakeholder-group`, `concern`, `affordance`, `technology`) and the four record keys (`scenario-raw`,
`scenario-coded`, `architecture-raw`, `architecture-coded`). It refuses any other slug: a relation page is made only by
naming a pair, and a class page only by the index operation. It also refuses a name that is illegal (2) or already
taken (any existing `.md` file name counts), when the name is given directly and not derived: it creates nothing and says why. With no type, it creates
nothing and reports the link. The usual way to give a body link a type is to name the page in the right link field of
the same page, which entails the stub with that type and makes the body link resolve.

**Other cases.**
- A link whose target exists but has the wrong type entails nothing: it is a wrong-endpoint problem, and the author
  decides whether the link or the page's `type` is wrong.
- A link that is not an exact slug name (2) entails nothing: it is corrected in the link.
- A stub that would be a `stakeholder-group` page, if creating it would take the vault over its cap (section 10), is not
  created: the operation refuses, prints the cap problem, and creates nothing from that call. The cap is lifted by
  raising it in `scat.toml`, or by linking an existing group.
- The seven class pages are entailed by the TBox itself. If one is missing, the stub operation (and the index operation)
  creates it as in 8. They are not created from links.

## 6. Page types: folders

Section 7 gives each page type's fields. The folder the tools create its pages in is the slug, for every page type (`class` pages go in `class/`). The `type` value
is the slug. Every page type has `type`, `title` and
`description`, and every type except `class` has `status`.

## 7. Page types: fields

### `stakeholder-group`

One page per stakeholder group: who the group is, in the group's own terms. The concerns it holds are stated on
`heldby` pages. A group, never a named person. The number of these pages is capped for the vault (section 10).

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `stakeholder-group` | | stub |
| `status` | `stub`, `draft` or `done` | | stub |
| `title` | text | | stub |
| `description` | short text | | done |

```
---
type: stakeholder-group
status: done
title: "Volunteer staff"
description: "The people who run the lending desk on open days."
---
```

### `concern`

One page per concern: what the interest is, and any concerns it conflicts with. Who holds it and what addresses it
are stated on `heldby` and `addresses` pages.

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `concern` | | stub |
| `status` | `stub`, `draft` or `done` | | stub |
| `title` | text | | stub |
| `description` | short text | | done |
| `conflicts` | list of wikilinks | `concern` | optional |

```
---
type: concern
status: done
title: "Safe handling of tools"
description: "Borrowers want to be sure a tool is safe to use."
conflicts:
  - "[[quick-checkout]]"
---
```

### `affordance`

One page per affordance: what is offered. The technologies it is attributed to are stated on `attributes` pages.

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `affordance` | | stub |
| `status` | `stub`, `draft` or `done` | | stub |
| `title` | text | | stub |
| `description` | short text | | done |

```
---
type: affordance
status: draft
title: "Safety briefing"
---
```

### `technology`

One page per technology: what the part is. It has no link field.

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `technology` | | stub |
| `status` | `stub`, `draft` or `done` | | stub |
| `title` | text | | stub |
| `description` | short text | | done |

```
---
type: technology
status: stub
title: "Booking app"
---
```

### `heldby`

One page per (group, concern) pair: this group holds this concern, with notes on that pair. A concern held by several
groups has several of these, one per group.

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `heldby` | | stub |
| `status` | `stub`, `draft` or `done` | | stub |
| `title` | text | | stub |
| `description` | short text | | done |
| `group` | one wikilink | `stakeholder-group` | stub |
| `concern` | one wikilink | `concern` | stub |
| `notes` | text | | optional |

```
---
type: heldby
status: done
title: "Volunteer staff holds Safe handling of tools"
description: "The volunteer staff hold this concern."
group: "[[volunteer-staff]]"
concern: "[[safe-handling-of-tools]]"
notes: "They see it as the thing that stops a borrower being hurt."
---
```

### `addresses`

One page per (concern, affordance) pair: this affordance addresses this concern, with notes on that pair.

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `addresses` | | stub |
| `status` | `stub`, `draft` or `done` | | stub |
| `title` | text | | stub |
| `description` | short text | | done |
| `concern` | one wikilink | `concern` | stub |
| `affordance` | one wikilink | `affordance` | stub |
| `notes` | text | | optional |

```
---
type: addresses
status: draft
title: "Safety briefing addresses Safe handling of tools"
concern: "[[safe-handling-of-tools]]"
affordance: "[[safety-briefing]]"
---
```

### `attributes`

One page per (affordance, technology) pair: this affordance is attributed to this technology, with notes on that pair.

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `attributes` | | stub |
| `status` | `stub`, `draft` or `done` | | stub |
| `title` | text | | stub |
| `description` | short text | | done |
| `affordance` | one wikilink | `affordance` | stub |
| `technology` | one wikilink | `technology` | stub |
| `notes` | text | | optional |

```
---
type: attributes
status: stub
title: "Safety briefing attributed to Booking app"
affordance: "[[safety-briefing]]"
technology: "[[booking-app]]"
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
| `description` | short text | | done |
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
| `description` | short text | | done |
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
| `description` | short text | | done |
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
| `description` | short text | | done |
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

The page of one of the seven classes (the four classes and the three relations): its description (the default is in 8)
and the index table of its instances. It carries no status, so every field here is required at all times.

| Key | Value | Target type | Required from |
|---|---|---|---|
| `type` | `class` | | always |
| `title` | text | | always |
| `description` | short text | | always |
| `indexes` | `stakeholder-group`, `concern`, `affordance`, `technology`, `heldby`, `addresses` or `attributes` | | always |

```
---
type: class
title: "Concerns"
description: "One page per concern: what the interest is, and any concerns it conflicts with. Who holds it and what addresses it are stated on Heldby and Addresses pages."
indexes: concern
---
```

## 8. Class pages and their index tables

There are seven class pages, one per class, with these names (they are reserved, see 2) and `indexes` values:

| Page name | `indexes` | Default title | Default description |
|---|---|---|---|
| `stakeholder-groups` | `stakeholder-group` | "Stakeholder groups" | "One page per stakeholder group: who the group is, in the group's own terms. The concerns it holds are stated on Heldby pages." |
| `concerns` | `concern` | "Concerns" | "One page per concern: what the interest is, and any concerns it conflicts with. Who holds it and what addresses it are stated on Heldby and Addresses pages." |
| `affordances` | `affordance` | "Affordances" | "One page per affordance: what is offered. The technologies it is attributed to are stated on Attributes pages." |
| `technologies` | `technology` | "Technologies" | "One page per technology: what the part is." |
| `heldby-pairs` | `heldby` | "Heldby" | "A Heldby page: which group holds which concern, with notes on that pair." |
| `addresses-pairs` | `addresses` | "Addresses" | "An Addresses page: which concern an affordance addresses, with notes on that pair." |
| `attributes-pairs` | `attributes` | "Attributes" | "An Attributes page: which technology an affordance is attributed to, with notes on that pair." |

A class page is the frontmatter in 7, then a body that is free text and optional, then the generated region:

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
- **Row template.** Each row is `| <title> | <description> | [[<page-name>]] |`: a pipe, one space, the cell text, one
  space, a pipe, and so on. A page with no description has an empty description cell, written `| name |  | [[name]] |`
  (two spaces between the pipes). The header row is `| Name | Description | Link |` and the separator row is
  `|---|---|---|`. The line just before the end marker is the last row, or the separator row when there are no rows.
- **Padding.** The generated region is compared with padding and trailing spaces ignored: spaces around a cell's
  text, and spaces at the end of a line, make no difference. A table that is aligned with extra spaces is not stale.
- **Order.** By page name, ascending, in plain character order (names are ASCII, so there is one order).
- **Markers.** The two lines `<!-- scat:index:start -->` and `<!-- scat:index:end -->` are exact, each on a line of its
  own. The index operation replaces everything between them, header included, and nothing outside them. Do not edit
  between them: the next run overwrites it. With no instances the region holds the header and separator rows only. The
  region is the first end marker that has a start marker before it, paired with the nearest start marker before it. If
  there is none (both markers missing, an end marker missing, or the markers out of order), the operation writes a
  fresh region, start and end markers included, at the end of the body, and leaves every stray marker line and all
  author text untouched. Marker lines outside that pair are likewise left alone.
- **When missing.** If a class page does not exist, the stub or index operation creates it with the default title, the
  `indexes` value, the default description from the table above, an empty body and the region.

## 9. Raw and coded pages

- A raw page holds the notes as told, in its body, unedited. It links to its coded pages with `coded`, which is
  optional: enforcing it is a non-goal, and the catalogue grades a raw page with no coded page as a warning.
- A coded page links to the raw page it was read from with `raw`, a list: a coded page may be derived from more than
  one raw page, and one raw page may have several coded pages. `raw` is required at `done`.
- The two sides are separate, so the same relation can be written on both. The tools never write one for you, except
  the link a new stub derives (5).
- A raw page is linked, not embedded: the contract has no embed. An `![[...]]` embed in a body is an ordinary body link.
- The target of `raw` and `coded` follows the page's own pair: scenarios link scenarios, architectures link
  architectures. A scenario linking an architecture is a wrong endpoint.

## 10. Vault configuration: the stakeholder-group cap

The cap is not in the TBox. It is set per vault in a file named **`scat.toml` at the vault root**, in TOML:

```
stakeholder_group_cap = 3
```

- The value is a TOML integer of 1 or more (a float such as `3.0` is a configuration problem). The tools read this key and ignore any other key in the file, except `templates_folder`: the vault-relative folder of the Obsidian page templates, which the tools do not read as pages (1). It is a string; if the key is absent, empty or not a string, the folder is `templates`.
- The count is the number of pages with `type: stakeholder-group`, at every status, stubs included.
- The cap is checked over the whole vault. A vault above the cap is not conformant.
- The key is at the top level of the file. There is no default: if the file is missing or not valid TOML, or the key
  is missing, not at the top level, or not such a number, that is itself a configuration problem for the catalogue to
  report.

## 11. Agreement with the TBox

Every key in the field tables is a `scat:key` of a field of that page type in the TBox, and every field the TBox lists
for a page type is in its table, with the TBox's level (`requiredField` with its `requiredFrom`, `optionalField`,
`discouragedField`). The seven default descriptions in 8 are compared with the TBox: each equals the `pageDescription` of
the page type in the `indexes` column. The `unlistedLinkLevel`, `wrongTargetLevel` and `discouragedBodyLink` statements are the TBox's;
this document only says where a person writes the links they govern. Things in this document that the TBox does not
state (names, folders, the markers, the sort order, the cap file, what a link entails) are the contract's own.

## 12. Needs from the TBox and the catalogue

**Needs from the TBox.** Nothing blocks this contract. Points for the PM:
- The TBox does not say a concern may not list itself in `conflicts`; section 4 says so. The catalogue may want a rule,
  or the TBox a note.
- The TBox gives no rule for which page a body link entails. Section 5 decides (no type without an explicit one) and
  needs no TBox term; the catalogue's dangling-link fix for a body link is therefore two-step.
- `scat:requiredFrom` on `description` is `done`, but a class page has no status. This contract reads that, with
  `carriesStatus false`, as "always required" (section 7, `class`). The TBox is consistent with that reading, but says
  it only in a comment.
- The TBox does not say whether two relation pages may state the same pair. This contract says one page per pair (5),
  which the stub operation honours; a hand-written duplicate is for the catalogue to grade.

**Needs from the rule catalogue.** The contract names these conditions; the catalogue grades them:
- Name validity: a name that is not a slug (2); a name over 64 characters; a reserved name; two pages with the same
  name in different folders; two names that differ only by case.
- A single-link field written as a list, or empty or missing on a relation page.
- A relation page that duplicates another's pair; a concern listing itself in `conflicts`.
- A stale or malformed index region (8); a missing or invalid `scat.toml` (10); a stakeholder-group stub that would
  exceed the cap (5, 10), for which the stub option is withdrawn.
