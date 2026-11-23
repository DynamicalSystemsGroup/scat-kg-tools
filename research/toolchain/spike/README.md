# WP2 toolchain spike: shared base

Throwaway spike code. Own uv project (`pyproject.toml`, `uv.lock`); Python >= 3.12; deps are only the pre-approved list.
Run everything from this directory.

## Layout

- `placeholder-tbox.ttl` – placeholder TBox (namespace `sp:` = `https://example.org/scpt-spike#`, not an adopted ontology).
  Seven classes; relations are classes with object properties (domain = relation, range = endpoint class).
  `sp:requiredField` / `sp:optionalField` list frontmatter keys per class. Status vocabulary `sp:stub|draft|done` (`sp:rank` 0-2).
- `vault/` – mini-vault, 22 pages (all seven classes; stub/draft/done mixed). Flat directory.
- `gen_vault.py` – synthetic 500-page vault generator (deterministic, fixed seed).
- `common.py` – `parse_page(path)` / `parse_vault(dir)`; reuse from stacks.
- Other units add `stacks/`, `okf/`, `r13/` (not here).

## Page format

One `.md` per page; page name = filename stem. YAML frontmatter keys: `type` (class name, e.g. `Concern`), `name`,
`status` (`stub|draft|done`), then class fields (`description`, ...). Relation pages hold endpoint links as quoted
strings: Heldby `stakeholder`, `concern`; Addresses `concern`, `affordance`; Attributes `affordance`, `technology`
(e.g. `concern: "[[Anonymity]]"`). Link syntax: `[[Page name]]` (also `[[Page#heading|alias]]`, target = name part),
in frontmatter values and body.

`parse_page` returns `{name, path, meta, body, fm_links, body_links, links}`.

## Commands

```
uv sync
uv run python gen_vault.py /tmp/scpt-vault-500     # 500 pages (default dir /tmp/scpt-vault-500)
uv run python common.py vault                      # prints pages=<n> links=<n>
uv run python -c "import rdflib; g=rdflib.Graph().parse('placeholder-tbox.ttl'); print(len(g))"
```
