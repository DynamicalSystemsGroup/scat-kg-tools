# WP2-U4: Open Knowledge Format (OKF) trial

Serves WP2-G4 / WP2-R4. Everything below was produced by `okf/run.sh`; the full output of one run is in
`okf/run-output.txt` (235 lines). Excerpts are pasted here.

## Pinned source

- Repo: https://github.com/open-knowledge-format/open-knowledge-format (only source used)
- **Commit: `527e81aff55992be21507e97004286789126f88c`** (2026-11-18, "Update SPEC.md"), OKF spec v0.3
- Cloned into `okf/clone/` (new, empty dir, gitignored). Never run from inside it; all paths are arguments
  (`python -I script.py PATH`; `-I` also blocks cwd/PYTHONPATH imports; our driver inserts `clone/src` explicitly).

## What the clone contains (read before running)

README + `SPEC.md` (v0.3, 54 KB) + sample bundles; two Agent Skills (`skills/okf-generate`, `skills/okf-consume`)
with stdlib+PyYAML scripts `validate.py` (conformance checker) and `scan.py` (concept lister with trust/freshness);
and a "reference agent" (`src/reference_agent`) that produces bundles from BigQuery + Gemini and has a
`visualize` command. README install: `python3.13 -m venv .venv; pip install -e .[dev]`.

Not run, on purpose: the `enrich` command (needs `gcloud` application-default credentials for BigQuery and
`GEMINI_API_KEY`/Vertex, plus web fetches). The README says so; the scope says stop if credentials are asked for.
Nothing else in the clone asked for credentials or network services. (The README's plugin install lines for
Claude Code/Codex were not followed: they are beyond "install and run on the mini-vault".) The viewer HTML
loads Cytoscape and marked from cdn.jsdelivr.net when opened in a browser; it was generated, not opened.

There is no OKF library or CLI that reads a vault. What exists to exercise: `validate.py`, `scan.py`, and the
reference agent's `OKFDocument` (parse/serialize) and viewer (`_walk_concepts`, `_build_graph`,
`generate_visualization`). The viewer is importable without google-adk (cli.py imports adk at top level, so the
`reference-agent visualize` entry point itself would need the full install; we import the module directly).

## Throwaway environment

`okf/venv/` (gitignored), created by `uv venv` + `uv pip install pyyaml` (only `pyyaml 6.0.4`). Nothing was
installed into the spike project; `pyproject.toml`/`uv.lock` untouched. The full reference-agent install was
only dry-run: `uv pip install --dry-run clone` reports **63 packages** (google-adk, google-cloud-bigquery,
uvicorn, websockets, ...), pulled in for a feature we do not need.

## Commands

```
bash research/toolchain/spike/okf/run.sh          # from any cwd; ~2 s; wipes and recreates clone/ venv/ work/
```
It runs, on `work/vault-copy` (a `cp -R` of `spike/vault`, 22 pages; the vault itself is never touched):
`python -I clone/skills/okf-generate/scripts/validate.py DIR`, `python -I clone/skills/okf-consume/scripts/scan.py DIR`,
`python -I trial.py clone {wikilinks|graph|roundtrip} DIR` (calls OKF's own parser and graph builder),
`python -I wiki2md.py {to-md|to-wiki} SRC DST` (our adapter: body wikilinks to markdown links and back),
and the OKF viewer generator. Config needed by OKF: none (no config file, no flags used besides the path).
Our own additions: `trial.py` (60 lines) and `wiki2md.py` (40 lines).

## Results (pasted from run-output.txt)

### A. The vault as it stands (wikilinks, spike frontmatter): conformant, but no graph

```
22 files checked: 0 errors, 16 warnings, 22 info. The bundle is conformant.
   .: warning W125 add a bundle-root index.md with okf_version: "0.3" (section 8.1)
   Anonymity.md:1: warning W105 status is draft, stable, or deprecated; consumers treat 'done' as not current (section 5.4)
   Anonymity.md:1: info I203 extension keys without the x- prefix: name (section 4.1)
Bundle vault-copy: 22 concepts ...
Types: Concern 4, Addresses 3, Heldby 3, StakeholderGroup 3, Attributes 3, Affordance 3, Technology 3
Trust: human-reviewed 0, machine-confirmed 0, unverified 22. Stale 0, deprecated 0, draft 7, not current 15.
baseline wikilinks (independent regex): pages=22 body_link_pairs=19 frontmatter_link_pairs=18 total_distinct=19
OKF graph builder: concepts: 22  edges: 0        <- all 22 nodes isolated
```
- Typed pages: yes. `type: Concern` etc. become concepts of that type; types are free strings (SPEC 4.1:
  "OKF does not register type values"). `scan.py --type Concern` returns the 4 Concern pages.
- YAML frontmatter: parses; our keys (`name`, `concern`, `stakeholder`, ...) are kept as extension keys (info I203
  suggests renaming to `x-<producer>-<name>`; not required).
- **Wikilinks: not ingested.** SPEC 6.1: "Only `[text](target)` links ... are links. Other syntaxes, for example
  `[[wikilinks]]`, are not links in OKF." Result: 0 edges where the vault has 19 distinct links. Links in
  frontmatter values (our typed relation endpoints, `concern: "[[Anonymity]]"`) are not links either; OKF
  only treats named path fields (`resource`, `superseded_by`, ...) as edges (SPEC 6.2/6.4), and the viewer ignores even those.
- Our `status: stub|draft|done` collides with OKF's `status: draft|stable|deprecated` (SPEC 5.4): `done` and `stub`
  warn W105 and are "not current" in scan.py (15 of 22 pages). The value is kept, the vault stays conformant.
  `--strict` makes the warning exit 1.

### B. With body wikilinks rewritten to markdown links (our adapter, frontmatter untouched)

```
[Facilitators](Facilitators.md) and [Anonymity](Anonymity.md): Chatham House setting.     <- body after to-md
22 files checked: 0 errors, 16 warnings, 22 info. The bundle is conformant.
concepts: 22  edges: 19  ... nodes with no edge: []
{'concepts': 22, 'edges': 19, 'bytes': 32476}            <- generate_visualization -> work/viz.html
round trip wikilinks->md->wikilinks: byte-identical
```
Once links are markdown links the graph is right: 22 nodes, 19 directed edges, same 19 as the independent
count. Edges are untyped (SPEC 6.1: "The link itself does not [tell the kind]"). The viewer's graph is a
Cytoscape HTML page with an embedded JSON blob (nodes with type/status/trust, edges `{source,target}`); there
is no RDF, JSON-LD, GraphML or other serialisation. A graph store would need our own bundle-to-RDF mapper.
Our two-way adapter is lossless on bodies in this vault (page names with spaces need `%20`; `[[X#h|alias]]` survives).
Caveat: in this vault each relation page repeats its endpoints in the body, so body links happen to cover all
typed edges. If the real vault keeps endpoints only in frontmatter (as the format spec says it may), the
adapter would also have to rewrite frontmatter, and OKF would still not read it as typed edges.

### Round-trip through OKF's own parser

```
parse->serialize identical=0 different=22
-concern: "[[Anonymity]]"        +concern: '[[Anonymity]]'      (quote style changed)
 ---                             +                              (blank line inserted after frontmatter)
```
`OKFDocument.parse().serialize()` rewrites every file (quote style, blank line). Cosmetic, content equal, but
SPEC 4 says producers SHOULD NOT re-serialize unchanged values: do not let OKF's writer touch the vault.

### C. Placeholder-TBox classes

```
Bogus.md:1: warning W105 status is draft, stable, or deprecated; consumers treat 'wibble' as not current
Bogus.md:6: warning W115 link target 'Nope.md' is not in the bundle (section 6.1)
23 files checked: 0 errors, 18 warnings, 22 info. The bundle is conformant.   strict: exit 1
```
Probe pages: `type: NotAClassInTheTBox` (accepted silently), a Concern with its `description` removed (no finding),
a link to a missing page (W115 warning, still conformant). **OKF checks nothing against the TBox**: no class
vocabulary, no required fields per class, no endpoint-class check. It has no schema mechanism at all by design
(non-goal: "Define a fixed taxonomy of concept types"). The three WP2 defects (missing field, wrong endpoint
class, missing page) are caught by OKF only for the missing page, and only as a warning.

## Other evidence

- License: Apache-2.0 (LICENSE.md; code headers "Copyright 2026 Google LLC").
- Maintenance (GitHub, 2026-11-23): created 2026-10-07 (first commit 2026-08-14), 29 commits, 3 authors (16/14
  commits from two people, one maintainer pair), 183 stars, 15 forks, **0 releases/tags**, spec at v0.3 after
  a breaking v0.2 to v0.3 change (SPEC 13.1); last push 2026-11-18. Open: 2 issues, 3 PRs (incl. issue #11 "Typed
  concept relations: a possible extension shape, following 12.2", i.e. typed relations are explicitly deferred,
  SPEC 12.2). Six weeks old, pre-1.0, backed by one company's team.
- Dependency footprint: for our use, PyYAML only (1.0 MB venv). Full install: 63 packages.
- Config effort: zero to run; but to be useful we must add an adapter (wikilinks) and our own TBox check.
- "Make the right way the easy way": OKF makes `[text](path.md)` the easy way; our authors write `[[wikilinks]]`
  (Obsidian-style) and typed relations as frontmatter fields. OKF would force either giving up wikilinks in
  authoring or maintaining a rewrite step on every export, and it offers nothing for the typing we need.

## Verdict: NOT YET (cannot be the vault-to-graph format today)

Deciding evidence:
1. 0 of 19 links ingested from the vault as written; the spec explicitly excludes wikilinks (6.1) and does not
   read frontmatter references as edges.
2. Edges are untyped; typed relations are an open extension issue (#11) and a deferred item (SPEC 12.2). Our
   relations (Heldby, Addresses, Attributes) with endpoint classes are exactly the typed part.
3. No schema/class validation, and no graph serialisation (only a viewer HTML); nothing replaces the SHACL/SPARQL
   stacks or the pydantic models (R-13).
4. Its `status` vocabulary conflicts with ours, and pre-1.0 spec churn (v0.2 to v0.3 breaking).

What it does well: the page format is nearly the same as ours (md + YAML + `type`), our vault is already
conformant with 0 errors, and it costs nothing to run. So it is compatible as an outer layer (a bundle can be
exported), but it carries none of the semantics.

Cost to us:
- **Adopt OKF as the format between vault and graph:** keep wikilinks and typed frontmatter, add (a) a
  wikilink-to-markdown-link export (`wiki2md.py` is ~40 lines, lossless here), (b) typed-relation extension keys
  and our own bundle-to-RDF mapper (OKF gives no help), (c) rename `status` or live with W105 on 15 of 22
  pages, (d) our own TBox check regardless. Net: all the real work is still ours, plus a dependency on a
  six-week-old spec that may change. Benefit: interop with OKF consumers/skills and the `validate.py` hygiene checks.
- **Not adopt:** nothing lost for WP2. Keep the spike's own format (md + YAML + wikilinks, `parse_page`), keep the
  vault conformant-by-accident so an OKF export remains a later option. Revisit when OKF has typed relations (#11)
  and a release.

## Flagged, not fixed

- `reference-agent` CLI and `enrich` untested (credentials). Viewer HTML not opened in a browser (CDN scripts).
- Probe C used synthetic pages in `work/probe` only; the vault is unchanged (`git status` clean for `spike/vault`).
- `run.sh` needs network (git clone, PyPI) and `uv`; it checks out the pinned commit, so it is reproducible as long
  as the upstream repo does not delete that commit.
