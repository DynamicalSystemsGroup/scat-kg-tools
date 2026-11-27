# Page contracts

What each kind of page looks like on disk in an SCAT vault, so that a person can write one by hand in Obsidian and the
tools can read, check and generate it. The TBox (`ontology/scat.ttl`) is authoritative for fields, status values, the
edge types and how a narrative's table is read; this document adds what the TBox leaves out: file names, how links are
written, what a link entails, the form of the table, the index pages and the vault configuration. It does not say how
serious a breach is, or what message a tool gives: that is the rule catalogue (`contracts/rule-catalogue.md`), and
"the catalogue" below means it.

The shape of the model, in one paragraph. The four node types are pages: `group`, `concern`, `affordance` and
`technology`. A `narrative` is one page: the account, with links where names appear, an optional list of what it
refers to beyond the text, and a table under the heading `Edges told` with one row for each edge the account tells.
An edge is no page and no field: it is a row. The tool builds the knowledge graph from the pages on every call; it
holds one edge per (type, from, to) and names every narrative with a row for it. An index is a generated Obsidian
Base file, not a page. Where the vault's attribution mode allows it (10), a fifth kind of page, the `contributor`,
names a person a narrative is attributed to: it is in the knowledge graph, so a narrative's `attributed_to` links
resolve to it, and it is outside the four layers, never a node, an edge, a fingerprint or part of the cap.

## 1. Pages

**A page** is a Markdown file ending `.md`, anywhere in the vault outside folders whose name starts with a dot, whose
frontmatter has a `type` key. Other Markdown files (a README, say) are not pages and are ignored. The vault's Obsidian
page-template folder (10) is not read, nor is `.obsidian/`. An index (9) is a `.base` file and is not a Markdown page: it has no frontmatter and no `type` field, though `index`
is one of the TBox's types.

**Layout.** The tools put each page they create in the folder named for its type, at the vault root: `group/`,
`concern/`, `affordance/`, `technology/` and `narrative/` (a contributor page, where the mode allows it, goes in
`contributor/`); the generated index files go in `index/`. A page by hand may
go in any folder: the folder is never checked, and the `type` key alone says what the page is.

**Shape of a file.**

```
---
type: concern
status: draft
title: "Safe handling of tools"
description: "Borrowers want to be sure a tool is safe to use."
---

Free text in Markdown. Nothing in it is required.
```

- UTF-8, and the tools write LF line endings (they read CRLF too).
- The frontmatter is a YAML block between two lines of exactly `---`, at the very top of the file.
- Keys are written exactly as in the field tables below. The order does not matter; the tables' order is the one the
  tools write.
- `title` and `description` are on one line. The tools always write them in double quotes; by hand the quotes are
  required only when the text contains `:` or `#`, starts with a quote, or has other characters YAML treats
  specially (a bare colon or `#` in an unquoted value breaks the YAML). Unquoted plain text is accepted. Inside
  quotes, `"` is written `\"` and `\` is written `\\`. `type`, `status`, `kind` and `timeframe` are written bare.
- Keys that the TBox does not list for the type are ignored, whatever they hold (you may add your own note
  keys). One field is a link field, a narrative's `attributed_to` (8); a link in any other frontmatter field is
  never read (3).

**Status.** Every page has `status`: `stub`, `draft` or `done`, in that order.
- `stub`: the page exists because something links to it, or has just been started. Only `type`, `status` and `title`
  are required.
- `draft`: being written. The required fields are the same as for `stub`; the fields that `done` requires are the
  author's to-do list, and how a tool grades their absence on a draft is the catalogue's call.
- `done`: the author judges the page complete. Every required field in the type's table must be present and
  non-empty, and the page is judged as it would stand at `done`: setting `done` is refused while it would fail.
- At every status, every link is checked: it must reach a page that exists, except that the link at a row's end (4)
  is graded as a mismatch (a warning until the narrative is `done`). Being unfinished is never a fault in itself.

**What each type needs at each status.** "Needs" means required and graded as the catalogue says.

| Type | `stub` | `draft` | `done` |
|---|---|---|---|
| `group`, `concern`, `affordance`, `technology` | `type`, `status`, `title` | the same | and `description` |
| `narrative` | `type`, `status`, `title` | the same | and `description`, `timeframe`; every row of its table conformant (4) |
| `contributor` | `type`, `status`, `title` | the same | the same: nothing else is required |
| `index` | not a page: no fields | | |

`kind` is optional on a narrative at every status. A narrative's table is optional at every status: a narrative with
no table tells no edge. A mismatch or other problem of the table (4) involving a narrative is a warning until the narrative is `done`, and an
error at `done`.

**The field tables** below give each key's "Required from": `stub` (present at every status), `done` (required once the
page is `done`) or `optional` (may be present).

## 2. Names and addresses

**The page name is the file name without `.md`.** It is the only address: a link writes the name and nothing else, so
the name is unique across the whole vault, whatever the type or folder.

**The name is a slug.** It must match all of:
- only the characters `a` to `z`, `0` to `9` and the hyphen `-`;
- starts and ends with a letter or digit, and never has two hyphens in a row;
- at most 64 characters;
- not one of the reserved names: `con`, `prn`, `aux`, `nul`, `com0` to `com9`, `lpt0` to `lpt9` (Windows device names).

This one rule covers the platforms. Lower case only means two names can never differ by case, so a case-insensitive
file system (macOS, Windows) and a case-sensitive one (Linux) see the same set of names. ASCII only means no accent can
be stored in two forms. No spaces, slashes, colons, quotes, question marks, asterisks, angle brackets, pipes, trailing
dots or trailing spaces can occur, which are the characters unsafe on one platform or another. The extension is
exactly `.md`, lower case.

**The title is the name as a person reads it.** It is free text, any language, and is what an index shows. The name is
made from the title like this, and the tools use it whenever they propose a name:
1. decompose the title with Unicode NFKD, remove the combining marks (Unicode category M), then lower-case it (so
   `É` becomes `e`).
   Letters that do not decompose (`ß`, `ø`, `æ`, any non-Latin script) are not in `a-z0-9` and are treated as the
   characters in step 2: they become hyphens, they are never transliterated;
2. replace every run of characters outside `a-z0-9` with one `-`, and trim `-` from both ends;
3. cut to 64 characters and trim a trailing `-`: this is the stem;
4. the stem is the name unless it is taken: the name of any existing `.md` file (a Markdown file without `type` is not
   a page but still blocks the name), or a reserved name, counts as taken; names are compared without regard to case.
   Then try `<stem>-2`, `<stem>-3`, and so on, cutting the stem first so the whole name stays within 64 characters
   (trim a trailing `-` from the cut stem before adding the suffix), until the name is free.

A derived name is therefore always a legal name. "Safe handling of tools" gives `safe-handling-of-tools`. If step 3
leaves nothing (a title with no Latin letters or digits), choose a name by hand. After a page exists, its title and its
name are independent: editing the title does not rename the file, and nothing checks that they agree. Rename a file in
Obsidian, which rewrites the links to it.

**A link resolves only on the exact name.** `[[Safety-Briefing]]` does not reach `safety-briefing.md`, though Obsidian
would follow it. A link that differs from an existing name only by case, or is not a slug at all (`[[Safety
briefing]]`), is a bad link: the fix is to write the exact slug name. The stub operation never creates a page for it
(6).

## 3. How links are written

**A link is `[[page-name]]`**, optionally `[[page-name|text to show]]` or `[[page-name#Heading]]`; the tools strip
`|...`, `#...` and `^...` (a block reference) and read the page name, which must exist. In the frontmatter, links are
never read, with one exception: the entries of a narrative's `attributed_to` (8), a list of text each written as a
link, `"[[ada-quill]]"` (quoted, as YAML needs). They are read as text and are no link of the page: in no backlink,
no fingerprint and no edge, and a link to a contributor page anywhere in the body is a link like any other, to a page
that is not a node, so it never codes a narrative. A link in any other frontmatter field is ignored. In the body, which is what is meant by a link
below, what is and is not a link:
- Text inside matched code spans and fenced code blocks is never a link. An indented code block is not code here, and
  an unmatched backtick starts nothing.
- An embed `![[page-name]]` of a page name is a link.
- Markdown-style links `[text](target)` are not wikilinks and are ignored.
- The tests below apply to the target after stripping `|alias`, `#heading` and `^block`. A target left empty by the
  stripping (`[[^blk]]`, `[[|a]]`) is not a page link.
- A target that is not a page is not a page link, and is never checked or stubbed: anything containing a dot
  (`[[photo.png]]`, `[[v1.2-notes]]`; page names never contain a dot, see 2), anything with a `/`, and a same-page link
  `[[#Heading]]`.

**A link says "see also" and nothing more**, except in a narrative's table (4), where a link at a row's end names one
end of an edge. A link is never an edge by itself. One check looks at every link: it must reach a page that exists (a link at a row's end is graded as a mismatch, 4).

**In a table cell**, a bar inside a link is written `\|` (`[[page-name\|text to show]]`), as Obsidian writes it; the
tools read that and the unescaped form alike (4).

## 4. The narrative page

A narrative is one page, `type: narrative`, in this order (the order is the convention; only the heading of the table
is fixed):

1. **The account**: free text in the body, with a link wherever a name appears (a group, concern, affordance or
   technology; another page it should point to). Write the link where the name appears, and use `[[name|text]]` to
   keep the sentence natural.
2. **Linked beyond the text** (optional): a list of links to nodes the narrative refers to that the account does not
   name in words. Its heading is not read; it is any other part of the page, so its links count as links of the
   narrative like every other.
3. **`## Edges told`**: the table.

```
## Edges told

| from | type | to | note |
|---|---|---|---|
| [[borrowers]] | holds | [[quick-checkout]] | Said twice in the first hour. |
| [[quick-checkout]] | is addressed by | [[self-checkout]] | Covers part of the concern. |
```

**What a narrative's links are.** Every link on the page: the account, the list, the table's ends and its notes. Its
**fingerprint** is the nodes it links and the edges its rows tell. A link at one end of a pair and a link at the other
without a row for the pair is a *candidate*: the narrative has not said whether it tells the edge, and no message is
given (the fingerprint view lists the candidate pair).

**Coded and uncoded.** A narrative is *coded* when it links at least one node page anywhere in its body (a row end of
its table, or a link in its account or its list); it is *uncoded* when it links none. An uncoded narrative is
*excluded*: the knowledge graph and every view (fingerprints, edge tables, the layered view, traces, exports, drawings)
leave it out, and `scat check` (SCAT-UNCODED) and each view that draws every narrative report it by name, with how to
include it: link one node page. It is included as soon as it is coded. A link in the account to a node page is the
place for a node the narrative names with no edge (a lone node): it codes the narrative and the node is in its
fingerprint. A link to a contributor page is not a node link: a narrative that links only contributor pages, in its
body or in `attributed_to`, is still uncoded. A row can tell an edge only through links to node pages, so an uncoded narrative tells no edge and no edge
waits on one.

**Reading the table.** The rules, all of which a person can follow by hand:
- *Where.* The table is the first table under a heading named `Edges told` at any heading level (`#` to `######`),
  the name compared without regard to case and ignoring spaces at its ends. "Under" means after the heading and
  before the next heading of the same or a higher level. No such heading, or no table under it, means the narrative
  tells no edge. A second table, or a second such heading, is not read: its rows tell no edge, and the catalogue grades it. A heading spelled otherwise, and a table on a page that is not a narrative, are not read and nothing is reported.
- *Columns.* The header row has the four column names of the TBox, in its order: `from`, `type`, `to`, `note`, each
  compared without regard to case. The next line is the separator row (`|---|`, with or without alignment colons).
  The table is the contiguous lines whose first non-space character is `|`, from the header row to the first line that
  is not such a line; each line after the separator row is a row. A heading or a table inside a fenced code block is not
  read. A row has four cells, one for
  each column, and a leading and a trailing `|`.
- *Cells.* A cell is the text between two unescaped `|`. In every cell, whitespace (any Unicode space, a tab or a
  no-break space) at the ends is dropped and a run of it inside is read as one; the same holds inside `[[ name ]]`,
  where the name is read trimmed. So Obsidian's table editor may re-pad the columns (it does, and a hand-aligned table
  is as good as a compact one). `\|` inside a cell is a bar in the text, not the end of the cell. A bar inside
  `[[ ]]` is never the end of a cell, written escaped or not. A `\|` inside a code span in a cell is read as one bar
  in the cell text. A row with a missing trailing cell has the wrong number of cells.
- *The `type` cell* is the verb or the slug of one of the three edge types, compared without regard to case:

  | Edge type | Slug | Verb | `from` is a | `to` is a |
  |---|---|---|---|---|
  | holds | `holds` | `holds` | `group` | `concern` |
  | is addressed by | `addressed-by` | `is addressed by` | `concern` | `affordance` |
  | is provided by | `provided-by` | `is provided by` | `affordance` | `technology` |

  The tools write the verb. Both spellings in one table are fine.
- *The `from` and `to` cells* each hold exactly one link and nothing else, as in 3 (an alias link `[[name\|text]]`
  is one link; the name is read; an embed `![[name]]` is accepted as an end).
- *The `note` cell* is free text on one line, and it may be empty. A `|` in it is written `\|`. It has no meaning to
  the tool; a link in it is a link of the narrative like any other.

**Skimmable.** A row reads as a sentence, subject, predicate, object: `from`, `type`, `to` ("borrowers holds quick-checkout"), with the `note` after it, so each edge name (the verb of its type) reads from the `from` node to the `to` node. A table in any other order is refused (SCAT-*-TABLE-HEADER).

**One row, one edge told.** The row is the narrative's telling of the pair (type, from, to). If a second narrative
tells the same pair it has its own row with its own note; nothing is copied between them.

**Mismatches.** A mismatch is a link and an edge that should agree and do not (glossary). In a narrative that happens
at a row's end, and the contract names two cases; the catalogue grades them and gives a fix for each:
- an end that is not a link;
- an end that is a link that reaches no page, or reaches a page that is not a node.

The other disagreement, a link at both ends of a pair with no row for it, is the *candidate* above and gets no message.

**Other problems of the table.** These are not mismatches; the catalogue grades them too:
- an end whose node is of the wrong layer for the type (a `concern` at the `from` end of `holds`), including the pair
  written in the wrong direction and a pair between layers that are not neighbours (a group and an affordance);
- an unknown type in the `type` cell;
- two rows of one narrative with the same type, `from` and `to`;
- a table whose header is not the four columns, or a header with no separator row after it (a table of a header row alone is such a table); the rows under a malformed header are not read, and the table tells no edge;
- a row whose number of cells is not four, or that does not end with a `|`;
- a second `Edges told` table, or a second such heading, on one narrative.

**`kind`.** `scenario` is a narrative about people doing things over time: it tells groups, concerns and affordances.
`architecture` is a narrative about how parts are put together into tools that offer affordances: it tells concerns,
affordances and technologies. A narrative that is neither leaves `kind` out. The tool does not check the layers of its
rows against `kind`.

**`timeframe`** says whether the narrative tells what happened (`past`), what would or will happen (`future`), or both
(`mixed`). It is required at `done`.

## 5. The edge, and its status

An edge is no page. The knowledge graph has **one edge for each (type, from, to)**, built from every row anywhere in the
vault that tells it. It **names the narratives** that have a row for it, each with its note. Nothing about an edge is
written outside those rows, so there is no edge to open and nothing to keep in step.

**An edge's status is derived**: it is `done` when every narrative that tells it is `done`; otherwise it has the least
advanced status of the narratives that tell it. The coder signs off edges by signing off narratives. To record an edge
is to add a row to a narrative, and to remove it is to delete the row; the links stay, since they are the account's.

## 6. What a link entails: the stub operation

Every link must reach an existing page. The stub operation creates the pages that links entail and are missing. It
writes only new files, never an existing page, and it is an explicit operation: checks never run it.

**A link at an end of a table row entails a node of the layer its type fixes**: the `from` end of a `holds` row is a
`group`, its `to` end a `concern`, and so on by the table in 4. The new page has exactly:

```
---
type: <the node type's slug>
status: stub
title: "<the name with each - replaced by a space, first letter upper case>"
---
```

and an empty body. For example, the row `| [[safety-briefing]] | is provided by | [[booking-app]] | |` creates
`affordance/safety-briefing.md` with type `affordance` and title "Safety briefing", and `technology/booking-app.md`.
The author edits the title after. A row whose type cell is unknown entails nothing, and neither does an end that
already reaches a page of another type: that is a problem of the table (4) and the author decides whether the row or the page's
`type` is wrong.

**Any other link entails a page, but not its type.** The account does not say what the page is, and guessing would put
words in the coder's mouth. So the stub operation creates a page for such a link only when it is given the type slug
explicitly, and then it creates it exactly as above. The slugs it accepts are the four node types (`group`, `concern`,
`affordance`, `technology`) and `narrative`; it refuses any other slug (a contributor page is made by hand, or by the
later operation the attribution mode gates). It also refuses a name that is illegal (2) or
already taken (any existing `.md` file name counts), when the name is given directly and not derived: it creates
nothing and says why. With no type, it creates nothing and reports the link. The usual way to give such a link a type
is to add the row that tells the edge, which entails the stub with that type and makes the link resolve. A stub of a
`narrative` has the line `timeframe:` after `title`, with no value, for the author to fill.

**Other cases.**
- A link that is not an exact slug name (2) entails nothing: it is corrected in the link.
- A stub that would be a `group` page, if creating it would take the vault over its cap (10), is not created: the
  operation refuses, prints the cap problem, and creates nothing from that call. The cap is lifted by raising it in
  `scat.toml`, or by linking an existing group.
- A row entails no other row. A narrative that links a group and a concern does not thereby tell that the group holds
  the concern; only a row does (4).

## 7. The relationship annotation

A relationship annotation is **a line in the body of one of its two entries, with a link to the other**. It records a
remark between two entries of the same type, such as two concerns that pull against each other:

```
Pulls against [[quick-checkout]]: a loan written down takes time.
```

It is ordinary body text. It has no field, no type and no meaning to the tool: it is a link like any other, so the
link must resolve, and it stays out of every view and of the knowledge graph. Write it on whichever of the two entries
is read first; it is not repeated on the other.

## 8. Types: fields

The folder the tools create a page in is the type's slug. Every type here that is a page has `type`, `status`, `title` and
`description`. Every field table below is the TBox's, field for field (11).

### `group`

One page per group: who the group is, in the group's own terms. A group, never a named person. The number of these
pages is capped for the vault (10). The concerns it holds are told by narratives.

| Key | Value | Required from |
|---|---|---|
| `type` | `group` | stub |
| `status` | `stub`, `draft` or `done` | stub |
| `title` | text | stub |
| `description` | short text | done |

```
---
type: group
status: done
title: "Volunteer staff"
description: "The people who run the lending desk on open days."
---
```

### `concern`

One page per concern: what the interest is. Who holds it and what addresses it are told by narratives.

| Key | Value | Required from |
|---|---|---|
| `type` | `concern` | stub |
| `status` | `stub`, `draft` or `done` | stub |
| `title` | text | stub |
| `description` | short text | done |

```
---
type: concern
status: done
title: "Safe handling of tools"
description: "Borrowers want to be sure a tool is safe to use."
---
```

### `affordance`

One page per affordance: what is offered. The technologies that provide it are told by narratives.

| Key | Value | Required from |
|---|---|---|
| `type` | `affordance` | stub |
| `status` | `stub`, `draft` or `done` | stub |
| `title` | text | stub |
| `description` | short text | done |

```
---
type: affordance
status: draft
title: "Safety briefing"
---
```

### `technology`

One page per technology: what the part is.

| Key | Value | Required from |
|---|---|---|
| `type` | `technology` | stub |
| `status` | `stub`, `draft` or `done` | stub |
| `title` | text | stub |
| `description` | short text | done |

```
---
type: technology
status: stub
title: "Booking app"
---
```

### What a node page's body holds

A group, concern, affordance or technology page has a body as well as a description. The tool reads it as text and
checks nothing in it; its links are links like any other. The norm for it (not a rule, and no rule id): the body holds
four parts, written across the narratives that link the node and never pasted from one.

1. What the node is, in its own terms.
2. How the narratives tell it: each claim cited by a link to the narrative, recurrence named, and a node that one
   narrative alone links says so. A group page that spans several senses (a cap forces broad groups) says so.
3. Where accounts differ: kept, not merged.
4. What is thin: what no narrative says.

What "what the node is" holds depends on the type (a norm the tool does not check):

- **A group:** who they are as the narratives tell them, and what they hold.
- **A concern:** what is at stake and who holds it, and what addresses it.
- **An affordance:** what it offers, and which technologies provide it.
- **A technology:** what it is as the narratives tell it, and which affordances rest on it.

`scat evidence <node>` shows what the narratives say of the node. `scat copy-share` reports how much of a page repeats a
narrative word for word: a prompt to look, not a check. The coder writes the page; the assistant may offer a draft as
text.

### `narrative`

One account on one page: the account, an optional list of links, and the table of edges it tells (4).

| Key | Value | Required from |
|---|---|---|
| `type` | `narrative` | stub |
| `status` | `stub`, `draft` or `done` | stub |
| `title` | text | stub |
| `description` | short text | done |
| `timeframe` | `past`, `future` or `mixed` | done |
| `kind` | `scenario` or `architecture` | optional |
| `attributed_to` | a list of links to contributor pages, each written `"[[name]]"` | optional |

`attributed_to` names the people the narrative is attributed to (GLOSSARY: attribution): each entry is a link to a
contributor page, for example `attributed_to: ["[[ada-quill]]", "[[bo-marsh]]"]`. It is a link field and not an
edge: it tells no edge, names no node, and is no part of the narrative's fingerprint, and a link in it never codes
the narrative (4). The TBox says only that it is optional and that its links reach pages of type `contributor`; the
attribution mode decides the rest, in one rule (the mode rule, the catalogue's section 3): in `required` mode a
narrative names a contributor (a warning before `done`, an error at `done`, SCAT-DRAFT-ATTR, SCAT-DONE-ATTR); in
`disallowed` mode the field is an error at every status (SCAT-ATTR-DISALLOWED); in `optional` mode it is free. In
the two modes that allow it, an entry that is not a link, that reaches no page or that reaches a page that is not a
contributor page is an error (SCAT-ATTR-LINK). A value that is not a list of text is SCAT-FM-SHAPE's. Only a
narrative has the field; on another page it is an unlisted key, which the tools ignore.

The page's heading of the table is `Edges told`; its columns are `from`, `type`, `to`, `note`.

```
---
type: narrative
kind: scenario
status: done
title: "Saturday at the lending desk"
description: "Notes from the volunteer session on a busy open day."
timeframe: past
---

The queue was out of the door by ten. A [[borrowers|borrower]] wanted [[quick-checkout|a quick checkout]].

## Edges told

| from | type | to | note |
|---|---|---|---|
| [[borrowers]] | holds | [[quick-checkout]] | Said twice in the first hour. |
```

### `contributor`

One page per person narratives are attributed to, outside the four layers: the name or handle as the organiser
records it, as the `title`. Present only where the vault's attribution mode is `required` or `optional`; in a
`disallowed` vault a contributor page is an error at every status (SCAT-ATTR-DISALLOWED). It takes no part in any
edge, the group cap, a fingerprint or a layered view: the layered graph holds the four layers only, and a
contributor page is in the knowledge graph as a page a narrative's `attributed_to` link resolves to. Nothing about
a person beyond the name is a field here, and the tools keep no contact details or consent record.

| Key | Value | Required from |
|---|---|---|
| `type` | `contributor` | stub |
| `status` | `stub`, `draft` or `done` | stub |
| `title` | text | stub |

```
---
type: contributor
status: done
title: "Ada Quill"
---
```

A narrative names her with `attributed_to: ["[[ada-quill]]"]`.

### `index`

Not a page and no fields: the Obsidian Base file the tool generates for a type (9).

## 9. Index pages

An index lists the pages of one type. It is **one Obsidian Base per type**, `index/<type>.base`, a view of the pages
whose `type` matches. It needs Obsidian 1.9 or later. It is generated once by `scat index` and never kept up to date by
a tool, because a Base reads the vault itself, so it cannot go stale. The loader ignores it. A Base leaves out the pages under the
template folder (10).

`scat index` writes the five files `index/group.base`, `index/concern.base`, `index/affordance.base`,
`index/technology.base` and `index/narrative.base`. It writes only a file that does not exist and never rewrites one
(an author may add columns). The file is UTF-8 with LF line endings and ends with one newline. It is written in the
form Obsidian itself saves a Base, so opening the index in Obsidian leaves it unchanged. A person can write the same
file by hand. The content, for the type `concern`:

```
filters:
  and:
    - note.type == "concern"
    - '!file.inFolder("templates")'
views:
  - type: table
    name: Concerns
    order:
      - file.name
      - title
      - status
      - description
    sort:
      - property: file.name
        direction: ASC
```

For another type, replace `concern` in the first filter and the view's name with the type and its plural title: `group`
and "Groups", `affordance` and "Affordances", `technology` and "Technologies". The narrative's file has two more columns
after `description`: `kind` and `timeframe`. The second filter names the vault's
`templates_folder` (10), here the default `templates`.

## 10. Vault configuration: the attribution mode and the group cap

Neither is in the TBox. Both are set per vault in a file named **`scat.toml` at the vault root**, in TOML. The file of the example vault in `contracts/examples` reads, with that vault's own cap of 3:

```
attribution = "disallowed"
stakeholder_group_cap = 3
```

- `attribution` is the vault's **attribution mode**: a TOML string, one of `required`, `optional` or `disallowed`
  (GLOSSARY: attribution mode). It says whether a narrative may name the people it is attributed to; the per-mode
  rules for the narrative's field are the catalogue's. There is no default: a vault with no `attribution` key, or
  a value that is not one of the three, is a configuration problem for the catalogue to report
  (SCAT-MODE-CONFIG), with a fix that names the three choices. The tools read the mode before any other key, and
  report it: `check` prints it, and every document of the machine interface carries it as `mode` (a string; null
  when the vault declares none, or an unknown one). A vault that changes its mode is checked as a whole against the
  new one: no narrative or page keeps what the old mode allowed, so a switch to `disallowed` flags every narrative
  that still has `attributed_to` and every contributor page. The rule that differs by mode is one sentence, in the
  catalogue (the mode rule); nothing else differs.

- The value is a TOML integer of 1 or more (a float such as `3.0` is a configuration problem). The tools read this key
  and ignore any other key in the file, except `link_suggestions` (below) and `templates_folder`: the vault-relative folder of the Obsidian page
  templates, which the tools do not read as pages (1). It is a string; if the key is absent, empty or not a string, the
  folder is `templates`.
- `link_suggestions` turns the link suggestions on (SCAT-MENTION, in the catalogue): a TOML boolean, `true` or
  `false`. If the key is absent the suggestions are off, as `false`; a value that is not a boolean is a configuration
  problem for the catalogue to report (SCAT-SUGGEST-CONFIG).
- The count is the number of pages with `type: group`, at every status, stubs included.
- The cap is checked over the whole vault. A vault above the cap is not conformant.
- The keys are at the top level of the file. The cap has no default: if the file is missing or not valid TOML, or the key
  is missing, not at the top level, or not such a number, that is itself a configuration problem for the catalogue to
  report.

## 11. Agreement with the TBox

Every key in the field tables is a `scat:key` of a field of that type in the TBox, and every field the TBox lists
for a type is in its table, with the TBox's level (`requiredField` with its `requiredFrom`, `optionalField`).
The types are the TBox's seven `scat:key` values: `group`, `concern`, `affordance`, `technology`, `narrative`,
`contributor` and `index`. A field with `scat:targetType` is a link field (`attributed_to`, whose links reach
`contributor` pages); no other field is. The statuses are the TBox's `StatusValues`: `stub`, `draft`, `done`. `timeframe` takes `past`, `future`,
`mixed` and `kind` takes `scenario`, `architecture`, as the TBox's value sets. The edge types, with their slugs, verbs
and the node types of their two ends, are the table in 4, and the TBox's three `scat:EdgeType` properties
(`scat:Heldby`, `scat:Addresses`, `scat:ProvidedBy`). The heading `Edges told` and the columns `from`, `type`, `to`,
`note`, in that order, with the cell each holds, are the TBox's `scat:tableHeading`, `scat:tableColumns` and
`scat:cellHolds`. Things in this document that the TBox does not state (names, folders, how the table's cells are read,
the form of the Base files, the cap file, what a link entails, how an edge's status is derived) are the contract's own.

## 12. Needs from the TBox and the catalogue

**Needs from the TBox.** Nothing blocks this contract. One point for the PM: the TBox keeps `scat:targetType` and
`scat:discouragedField` as declared vocabulary that no type uses now; the reader may drop them.

**Needs from the rule catalogue.** The contract names these conditions; the catalogue grades them:
- Name validity: a name that is not a slug (2); a name over 64 characters; a reserved name; two pages with the same
  name in different folders; two names that differ only by case.
- A link that reaches no page (3, 6); at a row's end it is a mismatch, graded by status.
- The mismatches and other problems of 4, and a narrative that is `done` while one is left; setting `done` is judged as the page would stand
  at `done`.
- The attribution mode rule (8, `contributor`, 10): `attributed_to` and contributor pages per mode, and an entry that
  is no link to a contributor page.
- A missing or invalid `scat.toml`, a missing or unknown attribution mode (10); a group stub that would exceed the cap (6, 10), for which the stub option is
  withdrawn.
