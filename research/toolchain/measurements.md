# WP2-D2: toolchain measurements

Everything below was rerun on 2026-11-23 from the worktree of branch `wp2/u6` (base commit `6aac532`). Each
block is pasted verbatim from the command printed above it. Commands run from the repository root and the
benches ran one at a time, with nothing else running. `uv run --directory research/toolchain/spike` is
written `UV` below to keep lines short; type it in full.

## Machine

| | |
|---|---|
| Machine | Intel Core i9-10910, 3.60 GHz, 20 logical cores, 64 GB, x86_64 (a desktop, not a laptop) |
| OS | macOS 15.7.7 (Darwin 24.6.0) |
| Python / uv | CPython 3.14.3 (uv-managed venv) / uv 0.13.1 |
| Libraries | pyoxigraph 0.5.13, rdflib 7.6.0, pyshacl 0.40.2, python-frontmatter 1.3.0 |
| Rerun | the first line of each bench prints the same details |

## 500-page vault

```
$ UV python -m gen --out out/vault500
wrote 500 pages to out/vault500
$ UV python -m gen.lint_links out/vault500
500 pages, 0 dangling links
```

## Timings (WP2-G2, R-5: page < 1 s, neighborhood < 2 s, full < 5 s)

Every repeat is cold (file scan, parse, load, rules). The stacks pick their own page and neighborhood centre, so
the page and neighborhood rows are not the same page across stacks.

### Stack A (pyoxigraph + SPARQL)

```
$ UV python -m stacks.a.bench
machine: Darwin 24.6.0 x86_64; CPU Intel(R) Core(TM) i9-10910 CPU @ 3.60GHz; 20 logical cores; Python 3.14.3; pyoxigraph 0.5.13
vault: out/vault500 (500 pages); page under test: scenario-coded-000; 7 repeats, each run is cold (parse + load + rules); thresholds: R-5
page          median 0.026s  min 0.024s  max 0.027s  (limit 1s, PASS at max)  pages loaded 9; findings 0
neighborhood  median 0.028s  min 0.027s  max 0.030s  (limit 2s, PASS at max)  pages loaded 21; findings 0
full          median 0.133s  min 0.129s  max 0.142s  (limit 5s, PASS at max)  pages loaded 500; findings 0
```

### Stack B (rdflib + pyshacl), default (core) shapes

```
$ UV python -m stacks.b.bench
== machine
os: macOS-15.7.7-x86_64-i386-64bit-Mach-O
cpu: Intel(R) Core(TM) i9-10910 CPU @ 3.60GHz (x86_64), logical cores: 20
python: CPython 3.14.3
libs: rdflib 7.6.0, pyshacl 0.40.2, python-frontmatter 1.3.0
== stack B (rdflib + pyshacl, core shapes) on out/vault500: 500 pages, 7 repeats
median-size neighborhood page: affordance-080 (5 pages); worst case: concern-092 (15)
scope                          min s  median s   max s  R-5 limit  verdict
page (affordance-080)          0.012     0.014   0.015        1 s  within
page (concern-092)             0.012     0.013   0.020        1 s  within
neighborhood (affordance-080)   0.037     0.039   0.041        2 s  within
neighborhood (concern-092)     0.057     0.059   0.080        2 s  within
full vault                     0.489     0.495   0.508        5 s  within
(full-vault check reports 0 message(s) on the generated vault)
```

### Stack B, `sh:sparql` shapes variant (3 repeats)

```
$ UV python -m stacks.b.bench --shapes sparql --repeats 3
== machine
os: macOS-15.7.7-x86_64-i386-64bit-Mach-O
cpu: Intel(R) Core(TM) i9-10910 CPU @ 3.60GHz (x86_64), logical cores: 20
python: CPython 3.14.3
libs: rdflib 7.6.0, pyshacl 0.40.2, python-frontmatter 1.3.0
== stack B (rdflib + pyshacl, sparql shapes) on out/vault500: 500 pages, 3 repeats
median-size neighborhood page: affordance-080 (5 pages); worst case: concern-092 (15)
scope                          min s  median s   max s  R-5 limit  verdict
page (affordance-080)          0.026     0.026   0.026        1 s  within
page (concern-092)             0.025     0.025   0.025        1 s  within
neighborhood (affordance-080)   0.147     0.147   0.154        2 s  within
neighborhood (concern-092)     0.424     0.427   0.436        2 s  within
full vault                    12.268    12.648  12.922        5 s  OVER
(full-vault check reports 0 message(s) on the generated vault)
```

With `sh:sparql` shapes the full vault takes about 12.6 s median and fails R-5. Page and neighborhood still pass.

### Stack C (pydantic + plain Python)

```
$ UV python -m stacks.c.bench
machine: macOS-15.7.7-x86_64-i386-64bit-Mach-O; Intel(R) Core(TM) i9-10910 CPU @ 3.60GHz; 20 logical CPUs; Python 3.14.3 (CPython)
vault: out/vault500 (500 pages); repeats: 7
page = concern-040; neighborhood centre = concern-050
scope           median s     min s     max s  limit s  verdict  (violations)
page              0.0004    0.0003    0.0008      1.0  within   (0)
neighborhood      0.0275    0.0271    0.0285      2.0  within   (0)
vault             0.0594    0.0580    0.0600      5.0  within   (0)
```

### Summary (median seconds)

| Scope | A | B core | B `sh:sparql` | C | R-5 |
|---|---|---|---|---|---|
| page | 0.026 | 0.014 | 0.026 | 0.0004 | 1 s |
| neighborhood | 0.028 | 0.039 (0.059 worst case) | 0.147 (0.427 worst case) | 0.0275 | 2 s |
| full | 0.133 | 0.495 | 12.648 (OVER) | 0.0594 | 5 s |

All three meet R-5 with at least 8x headroom on this machine, except B's `sh:sparql` variant at full scope. The
stacks differ in what the page scope loads (A loads the page and its link targets, 9 pages; C reads the page and
its targets lazily), so compare orders of magnitude, not single digits. Stack C's neighborhood needs inbound links,
so it reads every file's text once; the table shows that cost is small at 500 pages.

All three stacks run on this machine; none was skipped (WP2-R2).

## Messages (WP2-G3, WP2-R3)

The four defects are injected by `python -m defects` into a copy of the 20-page mini-vault. Each stack's
`messages` script first checks the clean mini-vault.

### Stack A

```
$ UV python -m stacks.a.messages
== clean mini-vault (vault/): 0 message(s)
== missing-field: 1 message(s)
access-cost.md: [SCAT-DONE-DESCRIPTION] field `description` is missing on a page with `status: done`; fix: either set `status: draft` in access-cost.md (exact), or add `description: "<one sentence the author writes>"`
== wrong-endpoint: 1 message(s)
access-cost.md: [SCAT-LINK-ENDPOINT] field `addresses` links [[booking-app]], class Technology; this field needs class Affordance; fix: replace `- "[[booking-app]]"` in `addresses` with a page of class Affordance; candidates (pages of class Affordance that already link [[booking-app]]): [[repair-queue]], [[reserve-online]]
== dangling-link: 1 message(s)
tool-safety.md: [SCAT-LINK-DANGLING] field `addresses` links [[safety-briefings]], but no page safety-briefings.md exists; fix: write [[safety-briefing]] (closest existing page) or create safety-briefings.md
== missing-link-type: 1 message(s)
scenario-1-coded.md: [SCAT-DONE-LINK] required link field `affordances` is missing on a `done` CodedScenario record; fix: add `affordances:` with at least one wikilink list item; candidates derived from this page's concerns' `addresses`: `- "[[reserve-online]]"`, `- "[[safety-briefing]]"`
```

### Stack B

```
$ UV python -m stacks.b.messages
clean mini-vault (20 pages): 0 errors

== missing-field  (page access-cost.md)
expected by injector: access-cost.md: required field `description` missing on a `done` concern; fix: add `description: "<one sentence>"`
stack B, whole vault: 1 message(s)
  access-cost.md [SCAT-001] required field `description` is missing. Fix: in access-cost.md either add `description: "<one sentence you write>"` or, if the page is unfinished, change `status: done` to `status: draft`
page and neighborhood scopes give the same message(s) for access-cost.md: True

== wrong-endpoint  (page access-cost.md)
expected by injector: access-cost.md field `addresses`: [[booking-app]] is a technology, an affordance is required; fix: link an affordance, e.g. [[reserve-online]]
stack B, whole vault: 1 message(s)
  access-cost.md:7 [SCAT-002] field `addresses`: [[booking-app]] is a technology, an affordance is required. Fix: under `addresses:` replace `- "[[booking-app]]"` with one of (related to [[booking-app]]): `- "[[repair-queue]]"` or `- "[[reserve-online]]"`
page and neighborhood scopes give the same message(s) for access-cost.md: True

== dangling-link  (page tool-safety.md)
expected by injector: tool-safety.md field `addresses`: page [[safety-briefings]] does not exist; fix: write [[safety-briefing]] (or create the page)
stack B, whole vault: 1 message(s)
  tool-safety.md:7 [SCAT-003] field `addresses`: page [[safety-briefings]] does not exist. Fix: replace [[safety-briefings]] with [[safety-briefing]], or create safety-briefings.md
page and neighborhood scopes give the same message(s) for tool-safety.md: True

== missing-link-type  (page scenario-1-coded.md)
expected by injector: scenario-1-coded.md: coded scenario has no `affordances` link; fix: add `affordances:` with at least one affordance, e.g. `- "[[reserve-online]]"`
stack B, whole vault: 1 message(s)
  scenario-1-coded.md [SCAT-004] coded record has no `affordances` link (required when status is done). Fix: add to the frontmatter of scenario-1-coded.md:
      affordances:
        - "[[reserve-online]]"
        - "[[safety-briefing]]"
page and neighborhood scopes give the same message(s) for scenario-1-coded.md: True
```

### Stack C

```
$ UV python -m stacks.c.messages
== clean mini-vault (20 pages): 0 violations

== defect dangling-link: 1 violation(s)
tool-safety.md: field `addresses`: [SCAT-LINK-DANGLING] [[safety-briefings]] does not exist (no file safety-briefings.md)
    fix: replace `[[safety-briefings]]` with `[[safety-briefing]]` (the closest existing page name; if you meant a new page instead, create safety-briefings.md)

== defect missing-field: 1 violation(s)
access-cost.md: field `description`: [SCAT-DONE-DESCRIPTION] required field is missing on a page with `status: done`
    fix: add the line `description: "<one sentence>"` (only you can write the sentence); or, if the page is not finished, change `status: done` to `status: draft`

== defect missing-link-type: 1 violation(s)
scenario-1-coded.md: field `affordances`: [SCAT-DONE-LINK] CodedScenario with `status: done` needs at least one `affordances` link (to an Affordance page)
    fix: add `affordances:` listing at least one Affordance page (which one is your choice; found via pages this page already links, confirm they fit:
      affordances:
      - "[[reserve-online]]"
      - "[[safety-briefing]]"
    ) -- or change `status: done` to `status: draft`

== defect wrong-endpoint: 1 violation(s)
access-cost.md: field `addresses`: [SCAT-LINK-ENDPOINT] [[booking-app]] is a Technology page, but `addresses` must link Affordance pages
    fix: replace `[[booking-app]]` with an Affordance page (your choice; e.g. [[repair-queue]], [[reserve-online]], [[safety-briefing]]; 3 available), or delete that line if the link is wrong
```

All three stacks report 0 messages on the clean mini-vault and exactly 1 message per seeded defect.

## Stack x defect, judged against R-2 (WP2-R3)

R-2's four elements: **F** file; **L** field or link; **R** rule id; **X** an exact fix with no placeholders
(a literal reader can apply it). Y = present. For X: "exact" means a pasteable edit exists in the message;
"exact alt" means a pasteable alternative is present but the message's main fix contains a placeholder or a choice.
Line numbers are not an R-2 element; stack B gives them for link fields (`:7`), A and C give none.

| Defect | A | B | C |
|---|---|---|---|
| missing-field | F Y, L Y (`description`), R Y (SCAT-DONE-DESCRIPTION), X: exact alt (`status: draft`); main fix has `<one sentence the author writes>` | F Y, L Y, R Y (SCAT-001), X: exact alt; main fix has `<one sentence you write>` | F Y, L Y, R Y (SCAT-DONE-DESCRIPTION), X: exact alt; main fix has `<one sentence>` |
| wrong-endpoint | F Y, L Y, R Y (SCAT-LINK-ENDPOINT), X: no; "a page of class Affordance", two candidates named in prose | F Y (with line 7), L Y, R Y (SCAT-002), X: near; two pasteable replacement lines, author picks one | F Y, L Y, R Y (SCAT-LINK-ENDPOINT), X: no; three candidates, "your choice", or delete the line |
| dangling-link | F Y, L Y, R Y (SCAT-LINK-DANGLING), X: exact (`write [[safety-briefing]]`) | F Y (line 7), L Y, R Y (SCAT-003), X: exact | F Y, L Y, R Y (SCAT-LINK-DANGLING), X: exact |
| missing-link-type | F Y, L Y, R Y (SCAT-DONE-LINK), X: near; candidate lines, but the instruction line is generic | F Y, L Y, R Y (SCAT-004), X: near; one pasteable YAML block, applied as written it is a complete fix | F Y, L Y, R Y (SCAT-DONE-LINK), X: near; pasteable YAML block, "which one is your choice, confirm", or `status: draft` |

Reading the table: file, field and rule id are present in all 12 cells. The only fully exact fix, in every stack, is
the dangling link. The other three are exact only as an alternative (missing field) or as a candidate the author
confirms (wrong endpoint, missing link type). B's two candidate messages are the closest to pasteable. A's are the
least pasteable. The differences are in the Python message text, not in the stack's rule language; any stack could
be given B's wording.

## What it takes to make each fix exact (WP2-R8)

Derived from the messages above; the stacks' own README tables say the same (not copied from them).

| Defect | Why the fix is not exact today | What it takes |
|---|---|---|
| missing-field | The value of `description` is the author's prose; no rule derives it. The only exact fix is the alternative `status: draft`. | A project decision on one of: (a) the tool may offer `status: draft` as the single fix (exact, but changes the page's meaning); (b) the title or first body sentence may seed the description, shown as a candidate the author accepts; (c) an explicit write operation (`set-status draft`). The prose itself cannot be exact. |
| wrong-endpoint | Several pages of the right class exist; which one is meant is the author's intent. | A tie-break rule the author has approved: a single candidate, or a ranking (for example pages the page already reaches through its other links, or the class's page that also appears in the body), shown as numbered exact replacements. Deleting the line is exact but may not be wanted. |
| dangling-link | Exact when a near-match page exists (all three stacks reach `[[safety-briefing]]`). The tool cannot tell a typo from a page the author means to create. | The author's confirmation that the near match is intended, or a rule that a frontmatter dangling link has the single exact fix "create the stub" with the type from the field's range. For body links, the stub's type is not stated, so it needs a decision. |
| missing-link-type | The derived set (concerns' `addresses`) is a suggestion, not a fix. | A domain axiom in the TBox that makes the derived set the right set (for example coded-scenario affordances = union of its concerns' `addresses`). Without it, the YAML block needs the author's confirmation. This is ontology content (WP1), not decided here. |

## R-13 mechanism (WP2-G5, WP2-R5)

```
$ UV python -m pytest r13 -q
.....                                                                    [100%]
5 passed in 0.49s
```

```
$ UV python -m r13.demo
--- unchanged placeholder TBox
.                                                                        [100%]
1 passed in 0.50s
exit code 0

--- scratch copy: CodedScenario requiresLink += scat:raw
F                                                                        [100%]
=================================== FAILURES ===================================
____________________________ test_models_equal_tbox ____________________________

    def test_models_equal_tbox():
        d = differences()
>       assert not d, f"models differ from {tbox_path()}:\n" + "\n".join(d)
E       AssertionError: models differ from /var/folders/lj/bwnwlztd2xxbytr07s3gffww0000gn/T/tmplfv2vv5y/tbox-scratch.ttl:
E         class CodedScenario: TBox requiresLink ['affordances', 'concerns', 'groups', 'raw'], models REQUIRED_LINKS ['affordances', 'concerns', 'groups']
E       assert not ["class CodedScenario: TBox requiresLink ['affordances', 'concerns', 'groups', 'raw'], models REQUIRED_LINKS ['affordances', 'concerns', 'groups']"]

r13/test_equality.py:14: AssertionError
=========================== short test summary info ============================
FAILED r13/test_equality.py::test_models_equal_tbox - AssertionError: models differ from /var/folders/lj/bwnwlztd2xxbytr07s3gffww0000gn/T/tmplfv2vv5y/tbox-scratch.ttl:
```

(The demo's own exit code is 0; the `F` and the failure are the intended demonstration.) The test holds the stack C
pydantic models equal to the placeholder TBox on classes, link properties, ranges, domains and required link sets.
It cannot compare type slugs, `description` or status values, because the placeholder TBox does not state them. The
mechanism was demonstrated only for stack C's models. Stack A's rules are hand-written SPARQL and stack B's rules are
hand-written SHACL; no equality test was run for them (not part of this unit).

## OKF trial (WP2-G4, WP2-R4)

The trial's notes are in `research/toolchain/spike/okf-trial/notes.md`. The clone lives outside the repository
and was reused for these reruns.

**Pinned commit** (the repository's `open-knowledge-format/open-knowledge-format` at spec v0.3):

```
$ git -C <clone> rev-parse HEAD
527e81aff55992be21507e97004286789126f88c
```

I did not install the reference agent (`pip install -e .[dev]` pulls google-adk and google-cloud-bigquery, needs
Python 3.11+ and cloud credentials, and is a producer, not the format). I ran the format's own consumers in a venv
holding only PyYAML (`uv venv okf-venv && uv pip install --python okf-venv/bin/python pyyaml`), isolated mode
(`python -I`), from outside the clone.

Rerun (`$OKF` is the clone, `$V` is `research/toolchain/spike/vault`, `$D/<name>` is a copy made by
`UV python -m defects <name> --out $D/<name>`):

```
$ python -I $OKF/skills/okf-generate/scripts/validate.py $V | tail -1
20 files checked: 0 errors, 14 warnings, 18 info. The bundle is conformant.
```

Diff of the validator output on each defect copy against the clean output:

```
missing-field      exit=0  diff lines: 0
wrong-endpoint     exit=0  diff lines: 0
dangling-link      exit=0  diff lines: 0
missing-link-type  exit=0  diff lines: 4
23c23
< scenario-1-coded.md:1: info I203 extension keys without the x- prefix: affordances, concerns, groups, raw (section 4.1)
---
> scenario-1-coded.md:1: info I203 extension keys without the x- prefix: concerns, groups, raw (section 4.1)
```

OKF detects 0 of the 4 defects; the one difference is an info line listing which keys exist. Its graph builder on
the vault as written (`python -I okf-trial/graph_probe.py $OKF/src $V <out.html>`):

```
concepts: 20
types: ['affordance', 'architecture-coded', 'architecture-raw', 'concern', 'scenario-coded', 'scenario-raw', 'stakeholder-group', 'technology']
edges: 0
trust tiers: ['unverified']
```

The vault has 47 `[[` occurrences, 41 in frontmatter (`cat vault/*.md | grep -o '\[\[' | wc -l`). OKF's spec
(section 6.1) says wikilinks are not links. The 14 warnings are the vault's `status: done|stub` values, which OKF
reads as "not current". The longer evidence (a copy rewritten to markdown links gives 6 untyped edges and still
none of the 41 typed ones) is in the notes file, run by the earlier unit and not rerun here.

## One extra check: CRLF line endings (ad hoc, not a spike script)

For the readout's platform item. A CRLF copy of the mini-vault, checked with stack C. The helper lives outside the
spike (a 5-line script run from the spike directory):

```
$ file <crlf-copy>/access-cost.md
...: ASCII text, with CRLF line terminators
$ UV python <helper> <crlf-copy>        # Vault(dir); check_vault(v); prints pages and violation count
20 pages; 0 violations
```

## One extra check: bad `status` and `type` values (ad hoc, not a spike script)

A copy of the mini-vault with `status: finished` on `access-cost.md` and `type: gadget` on `booking-app.md`.

```
$ UV python -m stacks.a.check <bad-copy>
reserve-online.md: [SCAT-LINK-ENDPOINT] field `attributes` links [[booking-app]], class unknown; this field needs class Technology; fix: replace `- "[[booking-app]]"` in `attributes` with a page of class Technology
(3 more lines of the same kind, for repair-queue, architecture-2-coded, architecture-1-coded)
exit=1
```

Stack A does not report the bad `status` at all, and reports the bad `type` only as four misleading endpoint errors on
other pages. Stack B has no check entry point (its README says unknown `type`/`status` are not implemented); not run.
Stack C, via a 5-line helper that calls `Vault(dir)` and `check_vault(v)` (not a spike script):

```
20 pages; 2 violations
access-cost.md status SCAT-FM-STATUS | `status` is 'finished'
booking-app.md type SCAT-FM-TYPE | `type` is 'gadget', not a known page type
```

So stack C checks both values; A and B do not. (The messages' fix lines were not pasted here.)

## Not measured

- A typical laptop; the benches ran on a 20-core desktop.
- Memory use.
- Bad `status` or `type` values beyond the one spot check above; they are not among the four seeded defects.
- Warm repeats, larger vaults, and Windows or Linux runs.
