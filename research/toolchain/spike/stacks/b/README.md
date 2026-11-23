# Stack B: rdflib + SHACL (pyshacl)

Throwaway spike. `python-frontmatter` parses a page; `check.py` builds an rdflib graph (page, its links as
typed edges, link targets' types, `scat:Missing` for links to nonexistent pages, plus the placeholder TBox);
`shapes.ttl` holds the rules as SHACL; pyshacl validates; a mapping layer (`diagnose` in `check.py`) turns
results into messages.

Scopes: `check_page` (page + type of each link target), `check_neighborhood` (page + every page within one
link either direction; needs one read of the whole vault to find inbound links), `check_vault`.

## Commands (repository root)

```
# R-5 timings on the generated 500-page vault (generates out/vault500 if missing); default: core shapes
uv run --directory research/toolchain/spike python -m stacks.b.bench
uv run --directory research/toolchain/spike python -m stacks.b.bench --shapes sparql --repeats 3

# messages for the four seeded defects, plus clean mini-vault (add `sparql` for the other shape file)
uv run --directory research/toolchain/spike python -m stacks.b.messages
```

## Rules (rule ids in messages)

SCAT-001 required field (title, status always; description when done) | SCAT-002 relation endpoint class |
SCAT-003 link to nonexistent page (frontmatter or body) | SCAT-004 required link type on a done coded record.
Not implemented (spike): unknown `type`/`status` values, scenario-links-technology prohibition.

## Two shape files, one finding

`shapes-sparql.ttl` writes the conditional rules as `sh:sparql` constraints (readable, one query each).
pyshacl re-parses a constraint's query for every focus node (1500 parses at 500 pages, ~80% of the time in
the SPARQL parser): full vault median about 12.9 s, over R-5's 5 s. `shapes.ttl` (default) uses only
`minCount`/`class`/`not` plus SHACL-AF `sh:SPARQLTarget` for the "status is done and class is X" condition
(parsed once per shape): full vault about 0.5 s. Both give byte-identical messages on the mini-vault defects
and on a mutated 500-page vault. Cost of the fast variant: more shapes, and rule intent ("done only") lives
in target queries.

## What the mapping layer costs, and why

Plain SHACL results give focus node, path, value, shape and component; a custom `sh:message` cannot
interpolate any of those (only `sh:sparql` can, and that is the slow variant). So `diagnose` (about 100
lines of Python) rebuilds every message: file name from the page IRI, line number by searching the file text,
rule id from `scat:ruleId` on the shape (or by component), the fix from graph/vault lookups. Fix quality
needs a whole-vault read (candidate lists), done only on the error path and not part of the page-scope
timing; a neighborhood run always pays it already.

## What it takes to make each fix exact (WP2-R8)

| Defect | Exact today? | What it takes |
|---|---|---|
| missing `description` | No (value is author knowledge) | The exact applicable alternative is `status: draft` (R-3), offered as the second option. A single exact fix would need a tool-supplied value (e.g. a command `scat set description "<text>"` taking the author's text); no check can invent the sentence. |
| wrong endpoint | Partly: exact edit, candidate not unique | The edit location (file:line, field) and replacement shape are exact; which affordance is intended is a judgement. Candidates are those related to the wrong target (here two: `repair-queue`, `reserve-online`, both really attribute `booking-app`). Making it exact needs a rule to pick one (e.g. unique candidate only) or a prompt; reported honestly as a choice. |
| dangling link | Yes when a near-miss stem exists (difflib, cutoff 0.8: `safety-briefings` -> `safety-briefing`); otherwise the exact stub file text is given for typed fields | Body links have no field, so the stub's `type:` is unknowable: needs the author. Near-miss matching can be wrong (a different page with a similar stem); the message offers it as replace-or-create. |
| missing link type | Yes when derivable: `affordances` from the page's `concerns` -> their `addresses` (reproduces the seeded original exactly); `technologies`, `groups` similarly | The derivation table (`DERIVE` in `check.py`) is hand-written per link type; for `concerns` with no `groups` there is none, and the message says "no value derivable". Derived lists can be larger than the author intended. |

## Platform notes

Pure Python (`pathlib`, `\n` assumed on read but `read_text` handles `\r\n`); the bench's machine line shells
out to `sysctl` only on macOS, and reads `/proc/cpuinfo` on Linux; Windows falls back to `platform`.
