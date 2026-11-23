# WP2-U5: Open Knowledge Format (OKF) trial (WP2-G4, WP2-R4)

Throwaway trial, 2026-11-23. Trial machine: macOS 24.6 (Darwin), x86_64, system Python 3.10.5, uv 0.13.1.

## Verdict (two lines)

**Not as the format between vault and graph.** OKF is a plain markdown-plus-YAML-frontmatter convention whose own spec says `[[wikilinks]]` are not links, so it cannot see 41 of the vault's 47 wikilinks (every typed edge), and it reports 0 edges for the vault as written.
**What is usable:** its small stdlib+PyYAML `validate.py` parses the vault's frontmatter without error (it adds nothing the stacks' own checks do not already do), and none of the four seeded defects trips it; so the checking, the typed edges and the `status` vocabulary would all be ours to write around it.

## Evidence

### Source and pin

```
$ git clone https://github.com/open-knowledge-format/open-knowledge-format okf-clone     # in <scratch>/okf-clone
$ git rev-parse HEAD
527e81aff55992be21507e97004286789126f88c
$ git log -1 --format='%ci %s'
2026-11-18 09:00:25 -0800 Update SPEC.md
```

Pinned commit: **527e81aff55992be21507e97004286789126f88c** (spec v0.3). The integrator is also to copy this pinned commit into `measurements.md`. Clone is 1.6 MB, kept outside the repository
(`<scratch>/okf-clone`, where `<scratch>` is the session scratchpad directory); nothing from it is committed.
Licence: Apache 2.0 (Google LLC headers).

### What "install" is, and what I ran

README "Install" is `python3.13 -m venv .venv; pip install -e .[dev]`. That installs the **reference agent**
(`pyproject.toml`: `google-adk>=2.0`, `google-cloud-bigquery`, `markdownify`, `pyyaml`, `pydantic`; Python >= 3.11).
That agent is a BigQuery-plus-Gemini producer (needs gcloud credentials and `GEMINI_API_KEY`); it is not the format and not
what the vault needs. I did **not** install it (Google ADK and BigQuery are far beyond the pre-approved list, need credentials,
and the system Python is 3.10). The format itself is a spec (`SPEC.md`) plus three small consumers I read before running:

| Entry point | Lines | What it does | Dependencies |
|---|---|---|---|
| `skills/okf-generate/scripts/validate.py BUNDLE` | 605 | conformance and field-shape checker | PyYAML |
| `skills/okf-consume/scripts/scan.py BUNDLE` | 346 | lists concepts with trust/freshness | PyYAML |
| `reference_agent.viewer.generator` (the `visualize` subcommand's engine) | 231 | builds the bundle graph and a viz.html | PyYAML plus package-internal modules |

Read before running: no network, subprocess or exec calls in the three scripts (`git grep -E "curl|wget|subprocess|os.system|eval\(|exec\("
over skills/ and src/` returned nothing). viz.html loads Cytoscape and marked from cdn.jsdelivr.net at view time (not opened here).

Environment (own venv, outside the clone and outside the spike project; the only dependency is PyYAML, which is pre-approved):

```
$ uv venv okf-venv && uv pip install --python okf-venv/bin/python pyyaml
Creating virtual environment at: okf-venv
Resolved 1 package in 358ms
Installed 1 package in 7ms
 + pyyaml==6.0.4
```

Every run: `cd /tmp; <scratch>/okf-venv/bin/python -I <clone>/<script> <bundle path>` (no interpreter run inside the clone;
`-I` isolated mode). `$S` below is `<scratch>`; `$V` is `research/toolchain/spike/vault`.

### Run 1: validate.py on the clean mini-vault (unchanged)

```
$ python -I $OKF/skills/okf-generate/scripts/validate.py $V
.: warning W125 add a bundle-root index.md with okf_version: "0.3" (section 8.1)
access-cost.md:1: warning W105 status is draft, stable, or deprecated; consumers treat 'done' as not current (section 5.4)
access-cost.md:1: info I203 extension keys without the x- prefix: addresses (section 4.1)
architecture-1-coded.md:1: warning W105 status is draft, stable, or deprecated; consumers treat 'done' as not current (section 5.4)
architecture-1-coded.md:1: info I203 extension keys without the x- prefix: affordances, concerns, raw, technologies (section 4.1)
architecture-1-raw.md:1: warning W105 status is draft, stable, or deprecated; consumers treat 'done' as not current (section 5.4)
architecture-1-raw.md:1: info I203 extension keys without the x- prefix: coded (section 4.1)
architecture-2-coded.md:1: info I203 extension keys without the x- prefix: affordances, concerns, raw, technologies (section 4.1)
architecture-2-raw.md:1: warning W105 status is draft, stable, or deprecated; consumers treat 'stub' as not current (section 5.4)
architecture-2-raw.md:1: info I203 extension keys without the x- prefix: coded (section 4.1)
booking-app.md:1: warning W105 status is draft, stable, or deprecated; consumers treat 'done' as not current (section 5.4)
borrower-privacy.md:1: warning W105 status is draft, stable, or deprecated; consumers treat 'stub' as not current (section 5.4)
borrower-privacy.md:1: info I203 extension keys without the x- prefix: addresses (section 4.1)
borrowers.md:1: warning W105 status is draft, stable, or deprecated; consumers treat 'done' as not current (section 5.4)
borrowers.md:1: info I203 extension keys without the x- prefix: heldby (section 4.1)
local-council.md:1: info I203 extension keys without the x- prefix: heldby (section 4.1)
repair-queue.md:1: warning W105 status is draft, stable, or deprecated; consumers treat 'stub' as not current (section 5.4)
repair-queue.md:1: info I203 extension keys without the x- prefix: attributes (section 4.1)
reserve-online.md:1: warning W105 status is draft, stable, or deprecated; consumers treat 'done' as not current (section 5.4)
reserve-online.md:1: info I203 extension keys without the x- prefix: attributes (section 4.1)
safety-briefing.md:1: info I203 extension keys without the x- prefix: attributes (section 4.1)
scenario-1-coded.md:1: warning W105 status is draft, stable, or deprecated; consumers treat 'done' as not current (section 5.4)
scenario-1-coded.md:1: info I203 extension keys without the x- prefix: affordances, concerns, groups, raw (section 4.1)
scenario-1-raw.md:1: warning W105 status is draft, stable, or deprecated; consumers treat 'done' as not current (section 5.4)
scenario-1-raw.md:1: info I203 extension keys without the x- prefix: coded (section 4.1)
scenario-2-coded.md:1: info I203 extension keys without the x- prefix: affordances, concerns, groups, raw (section 4.1)
scenario-2-raw.md:1: info I203 extension keys without the x- prefix: coded (section 4.1)
tool-safety.md:1: warning W105 status is draft, stable, or deprecated; consumers treat 'done' as not current (section 5.4)
tool-safety.md:1: info I203 extension keys without the x- prefix: addresses (section 4.1)
upkeep-burden.md:1: info I203 extension keys without the x- prefix: addresses (section 4.1)
volunteer-stewards.md:1: warning W105 status is draft, stable, or deprecated; consumers treat 'done' as not current (section 5.4)
volunteer-stewards.md:1: info I203 extension keys without the x- prefix: heldby (section 4.1)
20 files checked: 0 errors, 14 warnings, 18 info. The bundle is conformant.
exit=0
```

Reading: all 20 files parse (frontmatter is valid YAML mapping with non-empty `type`: the vault's `type:` is a free string, so
the 8 vault types are accepted). The 14 warnings are all one finding: the vault's `status: done|stub` is outside OKF's
`draft|stable|deprecated`; OKF reads `done` and `stub` as "not current". The 18 info lines are the relation fields
(`heldby`, `addresses`, `attributes`, `coded`, `groups`, `concerns`, `affordances`, `technologies`, `raw`) flagged as
extension keys that should be `x-` prefixed. The root-index warning is W125 (no `index.md` with `okf_version`).

### Run 2: the four seeded defects (WP2-G3 injector, copies in scratchpad)

```
$ uv run --directory research/toolchain/spike python -m defects <name> --out $S/defects/<name>     # x4
injected missing-field into $S/defects/missing-field
injected wrong-endpoint into $S/defects/wrong-endpoint
injected dangling-link into $S/defects/dangling-link
injected missing-link-type into $S/defects/missing-link-type
```
validate.py on each, diffed against Run 1's output on the clean vault:
```
== missing-field      exit=0   (diff against clean output: empty)
== wrong-endpoint     exit=0   (diff against clean output: empty)
== dangling-link      exit=0   (diff against clean output: empty)
== missing-link-type  exit=0   diff:
23c23
< scenario-1-coded.md:1: info I203 extension keys without the x- prefix: concerns, groups, raw (section 4.1)
---
> scenario-1-coded.md:1: info I203 extension keys without the x- prefix: affordances, concerns, groups, raw (section 4.1)
```
So **0 of 4 defects detected**. OKF has no required-field-by-status rule, no link-field endpoint-type rule, no check of
wikilinks, and no required link type. Missing `description` on a `done` page is silent (description is optional in OKF);
the dropped `affordances` field changes only an info line listing which keys exist.

### Run 3: scan.py and the graph builder on the vault as written

`scan.py` on the as-written vault was not needed; the graph builder was:
```
$ python -I okf-trial/graph_probe.py $OKF/src $V $S/vault-viz.html
concepts: 20
types: ['affordance', 'architecture-coded', 'architecture-raw', 'concern', 'scenario-coded', 'scenario-raw', 'stakeholder-group', 'technology']
edges: 0
trust tiers: ['unverified']
wrote $S/vault-viz.html
```
The vault has 47 `[[wikilinks]]`, 41 of them in frontmatter (the typed edges) and 6 in bodies:
```
$ cat *.md | grep -o '\[\[' | wc -l          -> 47
frontmatter only                              -> 41
```
OKF found **0** of them. This is by design: SPEC.md section 6.1: "Only `[text](target)` links (and reference-style links) are links.
Other syntaxes, for example `[[wikilinks]]`, are not links in OKF." Frontmatter lists are not links either; OKF's only
frontmatter edges are the fixed path fields (`resource`, `superseded_by`, `computation`, `executor.resource`,
`attester.resource`, `sources[].resource`; section 6.2), none of which is a relation.

### Run 4: the vault rewritten with markdown links (a copy, `sed` of every `[[x]]` to `[x](x.md)`)

```
$ sed -E -i '' 's/\[\[([^]|#]+)(\|[^]]*)?(#[^]]*)?\]\]/[\1](\1.md)/g' *.md      # in a copy, $S/vault-md
$ python -I okf-trial/graph_probe.py $OKF/src $S/vault-md $S/vault-md-viz.html
concepts: 20
types: [... same 8 ...]
edges: 6
   {'id': 'architecture-1-raw__booking-app', 'source': 'architecture-1-raw', 'target': 'booking-app'}
   {'id': 'architecture-1-raw__qr-labels', 'source': 'architecture-1-raw', 'target': 'qr-labels'}
   {'id': 'architecture-2-raw__qr-labels', 'source': 'architecture-2-raw', 'target': 'qr-labels'}
   {'id': 'scenario-1-raw__borrowers', 'source': 'scenario-1-raw', 'target': 'borrowers'}
   {'id': 'scenario-2-raw__volunteer-stewards', 'source': 'scenario-2-raw', 'target': 'volunteer-stewards'}
   {'id': 'scenario-2-raw__local-council', 'source': 'scenario-2-raw', 'target': 'local-council'}
$ python -I validate.py $S/vault-md | tail -1
20 files checked: 0 errors, 14 warnings, 18 info. The bundle is conformant.
$ python -I scan.py $S/vault-md | head -4
Bundle vault-md: 20 concepts, okf_version not declared, now 2026-11-23T20:27:53.270779+00:00
Types: concern 4, stakeholder-group 3, affordance 3, architecture-coded 2, architecture-raw 2, technology 2, scenario-coded 2, scenario-raw 2
Trust: human-reviewed 0, machine-confirmed 0, unverified 20. Stale 0, deprecated 0, draft 7, not current 13.
```
Even after rewriting, only the 6 body links become edges (the generator scans body text only: `_LINK_RE` in
`viewer/generator.py`); the 41 typed frontmatter edges stay invisible, and every edge is untyped (spec 6.1: "the link itself does not" say the kind).
(`scan.py` also reads `done` as an unknown status: "not current".)

## Judgement against the questions asked

| Question | Answer, with evidence |
|---|---|
| Parses markdown + YAML frontmatter + wikilinks into something checkable? | Frontmatter: yes (Run 1: 20 files, 0 errors). Wikilinks: no, by spec (Run 3: 0 edges of 47). "Checkable": its checks are conformance and provenance/freshness hygiene, not the vault's ontology rules (Run 2: 0 of 4 defects). |
| Does the vault's contract fit? | Partly. Flat directory of `<stem>.md` and free `type:` fit. `status` vocabulary clashes (14 warnings; `done` means "not current" to OKF). Relation fields are "extension keys" (must be `x-`-prefixed to be quiet). Typed frontmatter wikilink edges have no home: OKF edges are untyped body links. |
| What breaks | Typed edges (all 41), `[[stem]]` resolution, required-by-status rules, endpoint type rules, required link types, the dangling-link check on frontmatter. |
| What we would write around it | A wikilink resolver, the typed-edge extraction, the status/required-field/endpoint/link-type checks: i.e. the whole checker the stacks already are. OKF would contribute only a conventional directory/frontmatter shape we already have. Adopting it fully would also mean changing the contract: markdown links in place of wikilinks (breaks Obsidian-style authoring and R-8/R-11 ergonomics), `status` values renamed or ignored, relation keys renamed to `x-...` or tolerated as info lines. |
| Cost to the user (R-8, R-11) | Net negative if adopted as the interchange: authors would have to write `[text](path.md)` instead of `[[stem]]`, or accept a conversion step; no gain in messages (the validator's messages are about OKF fields, not the user's four defect classes). Zero cost if used only as a loose "this is a markdown+frontmatter bundle" label. |
| Cost to the builders | Low to read (three small stdlib+PyYAML scripts, Apache 2.0, one commit pinned), but the half we need is not there; the half it has (provenance, trust tiers, staleness, attested computations) is not in WP2's contract. Spec is young (v0.3, `okf_version`), so churn risk; our `status`/relations would need extension keys that "future versions will not define" only under the `x-` prefix. |

## Flagged

- I did not install or run the reference agent (README "Install"): it pulls `google-adk`, `google-cloud-bigquery`, `markdownify` (not on the
  pre-approved list), needs Python >= 3.11 and cloud credentials, and is a producer, not the format. The format's consumers were run instead (PyYAML only).
- `graph_probe.py` imports the clone's internal modules (`reference_agent.viewer.generator`, private helpers `_walk_concepts`, `_build_graph`, `_LINK_RE`
  logic) via `sys.path` insertion; the clone's `__init__` files were read first and import only stdlib/PyYAML on this path. That is the API a builder would call
  or reimplement; the repo ships no stable library API for it.
- viz.html (written to the scratchpad) was generated but not opened; it loads two scripts from a CDN at view time.
- `uv run --directory research/toolchain/spike ...` created `research/toolchain/spike/.venv` (git-ignored) and left `uv.lock` unchanged.

## Files in this directory

- `notes.md` (this file)
- `graph_probe.py`: the only script written; usage `python -I graph_probe.py OKF_SRC_DIR BUNDLE_DIR OUT_HTML`, run from outside the clone.
