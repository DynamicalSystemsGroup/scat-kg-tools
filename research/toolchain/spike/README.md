# WP2 toolchain spike (throwaway)

Scaffold for WP2. A uv project of its own; `pyproject.toml` already declares every pre-approved dependency
(pyoxigraph, rdflib, pyshacl, pydantic, pyyaml, python-frontmatter, pytest) plus `ruff` as a dev dependency.
Other units do not edit `pyproject.toml`; add code in your own directory.

## Layout

| Path | What |
|---|---|
| `placeholder-tbox.ttl` | PLACEHOLDER TBox (not D-1): classes, relations, record types, required link types |
| `vault/` | hand-built mini-vault, 20 pages (flat directory) |
| `gen/` | `python -m gen` synthetic vault generator; `python -m gen.lint_links` wikilink ground truth |
| `defects/` | `python -m defects` seeded-defect injector |
| `out/` | generated output, git-ignored |

## Commands

All run from the repository root and are re-runnable. `--directory` makes the spike the working directory,
so every path below is relative to `research/toolchain/spike/`.

```
# 500-page vault (deterministic; --seed N to vary; default 1)
uv run --directory research/toolchain/spike python -m gen --out out/vault500

# one seeded defect injected into a copy of the mini-vault
uv run --directory research/toolchain/spike python -m defects --list
uv run --directory research/toolchain/spike python -m defects missing-field --out out/defect-missing-field
#   names: missing-field | wrong-endpoint | dangling-link | missing-link-type

# ground-truth wikilink check of any vault directory (exit 1 if dangling)
uv run --directory research/toolchain/spike python -m gen.lint_links vault
```

## Frontmatter contract (stacks A, B and C build against this)

- A vault is a flat directory of `<stem>.md`. A page's identity is its filename stem; stems are unique.
  `[[stem]]` links to it (optionally `[[stem|alias]]`/`[[stem#heading]]`; the alias or heading is ignored).
- **Class/type:** `type:` is one of `stakeholder-group`, `concern`, `affordance`, `technology`,
  `scenario-raw`, `scenario-coded`, `architecture-raw`, `architecture-coded`
  (TBox classes StakeholderGroup, Concern, Affordance, Technology, RawScenario, CodedScenario,
  RawArchitecture, CodedArchitecture). Class index pages are out of scope for the spike.
- **Status:** `status:` is one of `stub`, `draft`, `done`.
- **Always required (every status):** `type`, `status`, `title`.
- **Required when `status: done`:** `description` (string) and the page's required link fields (below).
  Stub and draft pages may omit them (R-3); links and endpoints that are present are checked at every status.
- **Relations are frontmatter list fields whose values are quoted wikilinks** (`- "[[stem]]"`).
  A frontmatter wikilink is a typed edge, named by its field; the field belongs to the source page.

| Page type | Link fields (each a list of wikilinks) | Target type |
|---|---|---|
| stakeholder-group | `heldby` | concern (Heldby) |
| concern | `addresses` | affordance (Addresses) |
| affordance | `attributes` | technology (Attributes) |
| technology | none | |
| scenario-raw / architecture-raw | `coded` (optional) | the coded record of the same kind |
| scenario-coded | `groups`, `concerns`, `affordances` (required at done), `raw` (optional) | group, concern, affordance; raw scenario |
| architecture-coded | `concerns`, `affordances`, `technologies` (required at done), `raw` (optional) | concern, affordance, technology; raw architecture |

- A scenario never links technologies, an architecture never links stakeholder groups (MISSION).
  Pages are groups only; no individuals.
- **Body wikilinks** (outside frontmatter) are untyped mentions: they exist for resolution and for the
  neighborhood (one link in either direction), not for ontology rules.
- Frontmatter strings are JSON-style quoted where they contain `:`; parse with `python-frontmatter`/`yaml`.
- Generated pages are plain `\n` files with no timestamps; the generator is deterministic for a given seed.

## Seeded defects (WP2-G3)

Each is an exact one-place edit to the clean mini-vault; `python -m defects --list` prints the expected diagnosis
(file, field, fix) a checker should reach.

| Name | Page | Edit |
|---|---|---|
| `missing-field` | `access-cost.md` | removes required `description` (page is `done`) |
| `wrong-endpoint` | `access-cost.md` | `addresses` points at technology `booking-app` instead of an affordance |
| `dangling-link` | `tool-safety.md` | `addresses` links `[[safety-briefings]]`, which does not exist |
| `missing-link-type` | `scenario-1-coded.md` | removes the required `affordances` field |
