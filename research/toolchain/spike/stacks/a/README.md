# Stack A: pyoxigraph store, rules as SPARQL (WP2-U2, throwaway)

Parser (python-frontmatter + wikilink regex) feeds an in-memory pyoxigraph store holding the placeholder
TBox and the pages. Six rules are SPARQL SELECTs in `core.py` (`RULES`); each returns the violating pages and
the message text is built from the rows. Scopes: `page` (page plus its link targets, to learn their classes),
`neighborhood` (page plus pages one link away either way, plus their targets), `full`. Every timing is cold:
file scan, parse, load, rules.

Run from the repository root:

```
uv run --directory research/toolchain/spike python -m stacks.a.bench
uv run --directory research/toolchain/spike python -m stacks.a.messages
uv run --directory research/toolchain/spike python -m stacks.a.check vault --neighborhood access-cost
```

Rule ids: SCAT-REQ-FIELD, SCAT-DONE-DESCRIPTION, SCAT-DONE-LINK, SCAT-LINK-DANGLING, SCAT-LINK-ENDPOINT,
SCAT-LINK-DOMAIN. Not covered (spike): unknown `type`/`status` values, link fields not in the TBox.

## What it takes to make each fix exact (WP2-R8)

| Defect | Exact today? | What it takes |
|---|---|---|
| missing-field (`description`) | Only the alternative `status: draft` is exact. The value of `description` is the author's prose. | A literal reader can apply "set `status: draft`" with no placeholder. An exact `description:` line would need the text itself from a source: e.g. the page's first body sentence or `title`, offered as a candidate the author accepts. No tool can invent the intent. |
| wrong-endpoint | Candidates only. The message names pages of the right class that already link the wrong target (here `reserve-online`, `repair-queue`), so there are two. | Exact needs one answer. It needs a human choice, or a rule that breaks ties (e.g. the candidate that also appears in the page's body or a coded record). A write-ready line then reads `- "[[reserve-online]]"`. |
| dangling-link | Exact when one existing page name is close (difflib, cutoff 0.8): "write [[safety-briefing]]". | Typo case is exact. If no close name exists, the choices are create the page or drop the link; picking needs the author. Creating the page exactly needs the new page's `type`, `status`, `title`, which the link alone does not carry. |
| missing-link-type (`affordances`) | Candidates derived from the page's concerns' `addresses` (here exactly the removed values `reserve-online`, `safety-briefing`). | Exact once the derivation is accepted as the rule: write the derived list verbatim. It is a derivation, not a fact, so the author confirms. When the concerns are missing too, no candidate exists. |

Common thread: a fix is exact when the vault itself already contains the answer (typo, derivable link); it
is not when the answer is author intent (prose, a choice among equals).
