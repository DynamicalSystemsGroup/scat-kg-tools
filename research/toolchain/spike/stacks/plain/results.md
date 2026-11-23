# STACK C (plain): no graph store at check time; pydantic models + plain Python

Unit WP2-U3. All commands run from `research/toolchain/spike/` with the locked environment. Machine, library versions
and run counts are printed inside the `measure.py` output below. Numbers are one run of the command shown; rerun gives
the same shape, not identical digits.

## Thresholds (MISSION R-5, default thresholds) vs measured

Command (every number in the table):

```
uv run --locked python stacks/plain/measure.py
```

What is timed: one call of the check function at that scope on the 500-page synthetic vault (`gen_vault.py`, fixed
seed; generated fresh into a temp dir by `measure.py`), after `load()` and one untimed warm-up call per row. Each row
is `perf_counter` around the whole check call (for B this includes subgraph extraction, pyshacl and the report
mapping to messages). `load` (parse all 500 pages with `common.parse_vault`, build the stack's index or store) is
reported on its own row and is not in the check rows; the last line adds load + one check for a cold single invocation
(no cache is assumed). "hub" is the page with most links in + out (degree 7 in this vault: the generator makes
sparse, flat links, so neighborhoods are small); "typical" is the median-degree page. Sanity: every cell is asserted to
return 0 violations on the clean vault.

```
# measure.py: stack `plain`

- CPU: Intel(R) Core(TM) i9-10910 CPU @ 3.60GHz; cores: 20; RAM: 64 GiB
- OS: macOS-15.7.7-x86_64-i386-64bit-Mach-O
- Python: 3.14.3 (CPython)
- Libraries: rdflib=7.6.0, pyshacl=0.40.2, pydantic=2.14.4, python-frontmatter=1.3.0, pyyaml=6.0.4
- Vault: 500 pages, 560 links (gen_vault.py, seed fixed)
- Pages: hub = 'Affordance 003' (degree 7), typical = 'Attributes 075' (degree 2)
- Runs: 7 per local/neighborhood cell, 5 for full, plus 1 untimed warm-up each

| what is timed | median ms | min ms | max ms | n | threshold ms | verdict |
|---|---|---|---|---|---|---|
| load (parse + build, not a check) | 56.318 | 55.386 | 60.493 | 5 | - | - |
| local, hub | 0.003 | 0.002 | 0.008 | 7 | < 1000 | PASS |
| neighborhood, hub | 0.045 | 0.044 | 0.049 | 7 | < 2000 | PASS |
| local, typical | 0.006 | 0.006 | 0.006 | 7 | < 1000 | PASS |
| neighborhood, typical | 0.012 | 0.012 | 0.013 | 7 | < 2000 | PASS |
| full (500 pages) | 2.176 | 1.998 | 2.377 | 5 | < 5000 | PASS |

Cold single invocation (load + one check, medians added): local, hub = 56.3 ms; neighborhood, hub = 56.4 ms; full (500 pages) = 58.5 ms
Check outputs on the clean vault: 0 violations in every cell (asserted).
```

## How the rules are implemented

- missing required field: one pydantic model per class (`check.py`, `MODELS`); `model_validate(page.meta)`; each
  `ValidationError.errors()` entry becomes one message (field = `loc[0]`).
- relation endpoint of the wrong class: plain Python over `ENDPOINTS` (relation class -> field -> required class) and
  the in-memory name -> page index.
- link to a missing page: plain Python; every link in frontmatter and body must be a key of the index.
- Both tables (`MODELS`, `ENDPOINTS`) are hand-written copies of the TBox. `check.models_match_tbox()` (rdflib, load time
  only, not in the timings) asserts they equal the TBox; it returns True today. This is only the R-13 equality-test idea,
  not an R-13 decision.
- Custom code: the whole stack is `check.py`, 187 lines (rules and message text together; the models are 44 of them).
  There is no mapping layer: the rule code writes R-2 messages directly.
- Scopes: `load` parses the vault and builds a name -> page dict and a backlinks dict. Local = rules on one page with
  dict lookups for targets; neighborhood = rules on the page, its link targets and its backlinks (from the backlinks
  dict); full = rules on every page. No subgraph is needed.

## Seeded defects: real output

Command:

```
uv run --locked python stacks/plain/defects.py
```

Each defect is made in a temp copy of `spike/vault` (the vault itself is never edited; baseline is 0 violations).
Output, unedited:

```
baseline spike/vault: 0 violations

=== defect 1 missing required field (Anonymity.md loses `description`)
--- final output (1 violation(s))
Anonymity.md: field "description" [missing-required-field] Concern pages require "description" (Field required). Fix: add this line between the two --- lines at the top of Anonymity.md: description: <text>
--- same defect seen at narrower scopes on page 'Anonymity': local=1, neighborhood=1

=== defect 2 wrong endpoint class (Addresses.affordance -> a Concern)
--- final output (1 violation(s))
Anonymity addressed by Pseudonymous records.md: field "affordance" [wrong-endpoint-class] Addresses.affordance links to [[Attribution]], which is a Concern; it must be an Affordance. Fix: in Anonymity addressed by Pseudonymous records.md change field affordance to the link of an Affordance page, for example affordance: "[[Locked dependencies]]".
--- same defect seen at narrower scopes on page 'Anonymity addressed by Pseudonymous records': local=1, neighborhood=1

=== defect 3 link to a missing page (Attribution.md body)
--- final output (1 violation(s))
Attribution.md: field "(body)" [broken-link] link [[Nonexistent page]] points to no page. Fix: create the file "Nonexistent page.md" starting with these lines: --- / type: <one of StakeholderGroup, Concern, Affordance, Technology> / name: Nonexistent page / status: stub / ---
--- same defect seen at narrower scopes on page 'Attribution': local=1, neighborhood=1
```


The last line of each block shows the same defect found when only the defective page is checked at local scope
and at neighborhood scope.

## Judgement against R-2 (file; field or link; rule id; fix a literal reader can apply)

| defect | file | field/link | rule id | exact fix | verdict |
|---|---|---|---|---|---|
| 1 missing field | yes (`Anonymity.md`) | yes (`description`) | yes (`missing-required-field`) | yes: names the line and where it goes; the value is `<text>`, which only the author can write | meets R-2; the value is a placeholder by necessity |
| 2 wrong endpoint class | yes | yes (`affordance`, and the offending `[[Attribution]]`) | yes (`wrong-endpoint-class`) | partly: exact field and a literal example link, but the example (first Affordance page alphabetically) is not necessarily the one the author means | meets R-2 for a literal reader; the example is a guess |
| 3 missing page | yes | the link `[[Nonexistent page]]` is named; field is `(body)` (no line number) | yes (`broken-link`) | partly: two options (retarget to the closest page, or create the file with given first lines); for a body link `type:` is `<one of ...>` because the right class is unknown; no command, since the spike has no `scpt stub` | meets R-2 except the class of the new page |

Rule ids here are the spike's own (`missing-required-field`, `wrong-endpoint-class`, `broken-link`), not final ids.

## Reproduce

```
cd research/toolchain/spike
uv run --locked python stacks/plain/check.py vault        # baseline: ok: 0 violations (22 pages)
uv run --locked python stacks/plain/defects.py             # the three defect outputs
uv run --locked python stacks/plain/measure.py             # the timing table
```

Baseline output:

```
ok: 0 violations (22 pages)
```

## Not covered (spike scope)

Status strictness (R-3: all missing fields are errors here), pages without a `type` or with an unknown `type` (silently
skipped), an endpoint value that is not a `[[link]]` (reported as a missing field), line numbers, R-13, OKF.
