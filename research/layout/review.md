# WP16 layout review (the ACE, in Obsidian)

24 November, late. The three variants on `spike/layout` (e1b2ddb) were each opened as a vault in Obsidian 1.12.7, with
full-screen control, and walked from the depth-first draft narrative `night-main-break`. Screenshots are in `img/`.
Lab material only. Words follow `GLOSSARY.md`.

## What each looked like

**Variant A, edges as pages** (`img/variant-a-narrative.jpg`). The narrative page holds the account with its links in
place, a short "Linked beyond the text" list, and an embedded Base, "Edges that name this narrative", which renders as
a live table (type, from, to, told by). The Base works in Obsidian. But every edge is its own page with only
frontmatter, so recording an edge means making a page, and the vault has 16 pages a coder would rarely want to open.

**Variant B, edges as fields on node pages** (`img/variant-b-narrative.jpg`, `img/variant-b-concern.jpg`). Each edge is
a text string in a list field on the concern or affordance, for example `[[treatment-operators]]; told by
[[night-main-break]]; note: ...`. Obsidian shows these strings as plain text in the Properties panel: the links are
not clickable and are not in backlinks or the graph view. The narrative's embedded search shows raw strings. Writing
these by hand invites errors. Rejected.

**Variant C, edges as a table on the narrative** (`img/variant-c-narrative.jpg`). The narrative page holds the account,
the "Linked beyond the text" list, and an "Edges told" table: one row per edge the account tells (type, from, to,
note), every end a clickable link. One page to open per narrative; coding and reviewing happen in one place. A pair
told by two narratives has two rows, each with its own note: two tellings, not a duplicate. Because each row's ends
are links, a whole class of mismatch (an edge naming a narrative that doesn't link its ends) cannot occur.

**One finding about Obsidian.** Placing the cursor in a table makes Obsidian's table editor re-pad every column. The
content is unchanged, but the file changes and git shows a diff. The tool must read tables whitespace-tolerantly, and
the docs should say this reformatting is harmless. (The change was reverted.)

## Against R-21 and G17

| | A | B | C |
|---|---|---|---|
| Code and review in Obsidian alone | yes | no (dead links) | yes |
| Nothing duplicated | yes | yes | yes (rows are tellings) |
| No content-free pages to open | no (16 edge pages) | yes | yes |
| Mismatch classes to detect (G17) | all | all | fewer: row ends are links |
| Recording an edge by hand | a new page | a structured string | a table row |

## Recommendation

Variant C, with variant A's Bases for the index pages. The decision and what it means for the model are in log D-088.

## Acceptance walk (WP16), 25 November

A fresh clone of the template's `dev` (3cdbe60, pinning tools 29438f4) opened in Obsidian 1.12.7:
- `scat check` on the clone: "no problems".
- The narrative pages show their properties (`kind`, `status`, `timeframe`), the account with names linked in place,
  and the "Edges told" table (`img/acceptance-narrative.jpg`).
- All five generated index pages render as live Bases: concern 3, affordance 3, group 3, narrative 4 (with kind and
  timeframe), technology 3 (`img/acceptance-concern-index.jpg`).
- An incremental session with the tool: `stub --type narrative`, the account written, the status set to `draft`, two
  edges recorded with `record-edge` (rows added, links left alone), `set-status done` refused with exact fixes while
  `description` and `timeframe` were missing and accepted once they were filled, `record-edge` on the `done` narrative
  refused with the coder's step named, and the vault checking clean. The page reads correctly in Obsidian
  (`img/acceptance-coded-in-session.jpg`).
- Small finding: `scat stub narrative NAME` is refused; the form is `scat stub --type narrative NAME`. The message
  says so; the coding guide should show the form.
