# File map

Kept by the change consultant (`.claude/agents/change-consultant.md`). For each package in flight, the files it owns.
The PM checks a unit's blast zone against this map before dispatch; an overlap is reported at once. Refreshed on
2026-11-26 at `dev` 6183e29 (WP23 accepted, D-143), from `work-packages/plan.md`, `board.md`, the scopes `WP24.md` to
`WP26.md` and `impact/WP23.md`, `impact/WP24.md`. It was stale since WP17 (2026-11-25). Words follow `GLOSSARY.md`. Paths
are in `scat-kg-tools` unless a repository is named.

## Packages in flight

Nothing on `dev` is owned by a unit now. WP1 to WP23 are accepted or merged; WP22 and WP23 are on `dev` (D-141, D-143).
The remote branches `wp17/build`, `wp18/build`, `wp20/build`, `wp20/u2` to `u8` are 0 commits ahead of `origin/dev`
(merged; delete at the next branch clean-up). The spikes `spike/analysis`, `spike/chat-path`, `spike/layout`,
`spike/node-pages`, `spike/obsidian-plugin` are never merged and own `research/` folders only.

| Package | State | Owns (files) |
|---|---|---|
| WP20-UC1 chat-path UA-A | queued, waits on the chief engineer's sitting | `acceptance/` (new reports only); no source file. PM-only: `board.md`, `metrics.jsonl`. |
| WP24 node-page help and merge | draft scope, awaiting approval | By map `impact/WP24.md`: `src/scat_kg/views.py` (or new view modules), `src/scat_kg/ops/merge.py` (new), `src/scat_kg/__init__.py`, `cli.py`, `src/scat_kg/mcp_server/{server,prompts}.py`, `contracts/{assistant,page-contracts,architecture,machine-interface}.*`, `skills/scat-coding/SKILL.md`, `docs/{norms,coding,analysis}.md`, `docs/reference/{cli,api,mcp}.md`, `acceptance/reviewers-guide.md`, `research/node-pages/` (new vault), tests (`tests/views/`, `tests/ops/`, `tests/mcp_server/`, `tests/skills/`, `tests/docs/test_norms.py`, `test_mcp_tools.py` `TOOLS`, schema tests), `GLOSSARY.md` and `MISSION.md` G4 only by an ACE call. |
| WP25 docs: coding approaches, facilitating (C14, C15) | not scoped; after WP23 and WP24 | Expected: `mkdocs.yml`, `docs/{coding,chat-path,ide,leave-no-trace,planning,facilitate-scenarios,facilitate-architectures}.md`, new pages, `docs/assets/`. |
| WP26 prompt-residue sweep and user-test loops | draft scope; after WP25 | Every user-facing page, the skill text, CLI help and messages, template pages (`wp26/template`), `acceptance/`. |

PM-only files for every package: `work-packages/board.md`, `work-packages/metrics.jsonl`. ACE-only: `decisions/log.md`,
`work-packages/plan.md`, `candidates.md`, `pyproject.toml`, `uv.lock`.

## Files owned by no package

`decisions/log.md` (append only), accepted readouts under `research/` (`research/node-pages/` gains a vault under WP24
only), `acceptance/reports/` (past reports; new ones are added), `work-packages/WP1.md` to `WP23.md` and the `RS` scopes,
`MISSION.md` and `GLOSSARY.md` (changed only by the chief engineer's merge or an ACE-logged call), `ORG.md`, the agent
role files, the template repository (WP26 only).

## Overlaps found

| Files | Between | Kind | Recommendation |
|---|---|---|---|
| `docs/coding.md`, `docs/planning.md`, `docs/facilitate-*.md` | WP24, WP25 | shared | WP24 first (plan order); WP24 limits itself to the node-page lines in `coding.md` and `analysis.md`. WP25 branches from WP24's merge. |
| `docs/*`, `skills/scat-coding/SKILL.md`, `mcp_server/prompts.py`, CLI help | WP24, WP26 | shared | WP26 sweeps what WP24 wrote; WP26 starts after WP25. No parallel run. |
| `contracts/assistant.md`, SKILL.md, `prompts.RULES` | units inside WP24 | same text in three files | One unit at a time; the drift tests join them. |
| `cli.py`, `server.py`, `__init__.py`, `machine-interface.*`, `docs/reference/*` | units inside WP24 | serialised | Each unit adds its entry after the last is merged (the WP17 rule). |
| `MISSION.md` G4 | WP24 | amendment | The chief engineer's mission; ACE rules whether merge is inside G4 before approval. |
| `tests/docs/conftest.py` `TEMPLATE_COMMIT` | WP24 snippets, WP26 template fixes | pin | Moves only with a template commit; WP24 does not touch the template. |

## Ordering rules inside WP24 (files two units write)

| File | Writers, in order |
|---|---|
| `src/scat_kg/cli.py`, `__init__.py`, `mcp_server/server.py` | evidence, copy-share, merge, review view |
| `contracts/machine-interface.*`, `docs/reference/*` | the same order; the unit adding an operation writes its entry |
| `contracts/assistant.md`, SKILL.md, `prompts.py` | rules and prompt unit (A), then the merge and review rules unit (B) |
| `docs/norms.md`, `contracts/page-contracts.md` | norm unit only |

## Branch check at 6183e29

`git diff --stat origin/dev...<branch>` for every remote branch: the merged unit branches show nothing; the five spikes touch
`research/` only (plus old copies of `impact/file-map.md` and `impact/WP16.md` on `spike/chat-path`, never merged: no
conflict). `spike/node-pages` holds RS4's notes (throwaway `merge.py` rewrites links in every page, contributor and index
pages included: not to be carried into the tool). No overlap with a unit of WP24.
