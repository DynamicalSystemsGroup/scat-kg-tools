# Stack C: no graph store, pydantic models plus plain Python

Parses `<stem>.md` (YAML frontmatter via PyYAML, libyaml loader when present; wikilinks by regex), validates
each page with one pydantic model per page type (`models.py`), and applies the cross-page rules in plain
Python (`checks.py`). Nothing is indexed or stored; every call starts from the files.

All commands run from the repository root.

```
# 500-page vault (needed by the bench)
uv run --directory research/toolchain/spike python -m gen --out out/vault500
# timings: page / neighborhood / whole vault, median and min of N fresh-Vault repeats, machine details
uv run --directory research/toolchain/spike python -m stacks.c.bench
# messages for the clean mini-vault and the four seeded defects (exit 1 if clean fails or a defect != 1 violation)
uv run --directory research/toolchain/spike python -m stacks.c.messages
```

API: `Vault(dir)`, `check_page(v, stem)`, `check_neighborhood(v, stem)`, `check_vault(v)`; each returns
`Violation(file, field, rule, message, fix)` items. Neighborhood needs inbound links, which means reading
every file's text once (a regex scan); that is the price of having no index.

Rule ids: `SCAT-FM-PARSE`, `-FM-TYPE`, `-FM-REQUIRED`, `-FM-STATUS`, `-FM-SHAPE`, `-DONE-DESCRIPTION`,
`-DONE-LINK`, `-LINK-SHAPE`, `-LINK-DANGLING`, `-LINK-ENDPOINT`. Unfinished pages are not errors for being
unfinished (R-3); links and endpoints are checked at every status.

The models are held equal to the placeholder TBox by `r13/` (see `../../r13/README.md`).

## What it takes to make each fix exact (WP2-R8)

An "exact fix" here is a line or file content a literal reader can paste, with no placeholders.

| Defect | Exact today? | What it would take |
|---|---|---|
| missing `description` | Only the alternative: `status: done` to `status: draft` is exact. The sentence itself is a placeholder (`"<one sentence>"`). | A description is author content; no rule can derive it. Exactness means offering a stand-in the tool is allowed to write, e.g. an explicit operation `set-status draft` (R-4: writes are explicit), or a project decision that the title may seed the description (then the line is exact). |
| wrong endpoint | No. It names the rule and lists existing candidate Affordance pages, but which one is the author's choice. | A tie-breaker the author has approved: e.g. only one candidate exists, or the tool may propose the candidates already reachable from the page's other links, ranked and shown as numbered exact replacements the author picks by number. Deleting the line is exact but may not be wanted. |
| dangling link | Exact when a close-name page exists (`[[safety-briefings]]` to `[[safety-briefing]]`, edit distance based; 0.8 cutoff): a literal replace. Otherwise the stub file content is exact for frontmatter links (the class gives `type`), the title is a guess. | Confirmation that the near match is meant (the tool cannot know a typo from a new page), and for body links a decision on the stub's type, which the body does not state. |
| missing required link type | No. Candidates are derived from pages this page already links (concerns' `addresses`), printed as an exact YAML block, marked "confirm they fit". | The domain rule that says the derived set is the right set (a TBox axiom, e.g. coded-scenario affordances = union of its concerns' addresses). Without that axiom the block is a suggestion, not a fix. |

Line numbers are not reported: PyYAML's safe load drops them. Reporting them needs `yaml.compose`
(node marks) or ruamel; not done in the spike.

## Honest limits

- Timings are cold-parse per repeat, warm OS file cache, one machine (printed by the bench).
- `description`, the status values and the type slugs live in the models only; the TBox does not state them,
  so the R-13 test cannot hold them equal (flagged in `../../r13/README.md`).
- Body wikilinks are untyped: only resolution is checked.
