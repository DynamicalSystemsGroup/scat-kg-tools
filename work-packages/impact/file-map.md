# File map

Kept by the change consultant (`.claude/agents/change-consultant.md`). For each package in flight, the files it owns.
The PM checks a unit's blast zone against this map before dispatch; an overlap is reported at once. Updated at
2026-11-25 (WP17 added, WP16 accepted and merged at D-091; WP17-U7 check at the start of WP17) from `work-packages/plan.md`,
`work-packages/board.md`, the scopes `WP14.md`, `WP17.md`, `RS3-chat-path.md` and `impact/WP16.md`. Words follow `GLOSSARY.md`. Paths are in `scat-kg-tools` unless a repository is named.

## Packages in flight

| Package | State | Owns (files) |
|---|---|---|
| WP14 prior-art readout | scope approved (D-079) | `research/prior-art/` (new). Also, as PM-only edits: `work-packages/board.md`, `work-packages/metrics.jsonl`. |
| WP15 architecture document and review | no scope file yet | The architecture document (deliverable D-2; **path not set**) and the architecture reviewers' review record (**path not set**). Also PM-only: `board.md`, `metrics.jsonl`. |
| RS3 chat-path spike | scope approved (D-080) | Branch `spike/chat-path` (anything on it, never merged into `dev`); on `dev`: `research/chat-path/`. Also PM-only: `board.md`, `metrics.jsonl`. |
| WP16 ontology and layout (absorbs WP13) | **accepted and merged into `dev` (D-091); released**: no unit owns its files; WP17 may write there | Released. For the record, it owned `ontology/scat.ttl`, `contracts/`, `src/scat_kg/`, `tests/`, `docs/`, `mkdocs.yml`, `acceptance/`, `work-packages/WP16.md`, `work-packages/impact/`, and in `scat-kg-template` the vault pages, `class/`, `.obsidian/`, `.gitignore`, `README.md`, `scat.toml`, `pyproject.toml`, `uv.lock`. Detail and counts: `impact/WP16.md`. |
| WP17 the views | scope approved (D-092); units U1 to U7r planned on `pm-wp17`, backed up to `origin/wp17/build` | **By unit, tools** (`scat-kg-tools`): U1 `src/scat_kg/views.py`, `src/scat_kg/__init__.py` (export), `tests/views/`. U2 `src/scat_kg/export.py`, `src/scat_kg/cli.py`, `contracts/machine-interface.md`, `contracts/machine-interface.schema.json`, `contracts/architecture.md` (the one `[OPEN: WP17]` line), `docs/reference/cli.md`, tests (`tests/views/`, and the CLI-help and machine-schema tests only if they must follow the new commands and document kind). U3 `src/scat_kg/draw.py`, `pyproject.toml` (optional extra `draw`, and `dev` group), `uv.lock`, `src/scat_kg/cli.py` (the draw command), `docs/reference/cli.md`, tests. U5 `docs/analysis.md`, `docs/reference/api.md`, `mkdocs.yml`. U6 `docs/flow.md`, `ontology/scat.ttl` (the comment only), `docs/reference/terms.md` (the SCAT entry). **Template** (`scat-kg-template`, branch `wp17/u4`): U4 the notebook (new), `.github/workflows/ci.yml`, `pyproject.toml`, `uv.lock` (the tools pin). Also PM-only: `work-packages/board.md`, `work-packages/metrics.jsonl`; U7 owns this file for WP17. Not touched: `tests/docs/conftest.py` (the template pin stays, PM default 3), `contracts/rule-catalogue.md`, `contracts/page-contracts.md`, `src/scat_kg/ops/`. |

WP16's files are released: WP16 is accepted and merged into `dev` (D-091), so nothing under the WP16 list is owned any
longer and WP17 may write there; the stale hits in `impact/WP16.md` section 9 go back to a unit only by the PM's dispatch. WP13 is absorbed into WP16 (D-078): it owns nothing of its own and is not dispatched. Packages not yet in flight (WP18 to
WP20) are not listed; WP18 and WP19 read the model WP16 writes and start after it (plan.md).

## Files owned by no package, kept as they are

`decisions/log.md` (append only, by the ACE), `research/` (the accepted readouts; WP14 and RS3 add new folders only), `contracts/rule-catalogue.md` and `contracts/page-contracts.md` (WP17 reads them),
`acceptance/reports/` (past reports; new ones are added), `work-packages/WP1.md` to `WP12.md`, `RS1`, `RS2`,
`MISSION.md` and `GLOSSARY.md` (changed only by the chief engineer's merge or an ACE-logged glossary call),
`ORG.md`, the agent role files, the branches `spike/analysis` and `spike/obsidian-plugin`.

## Overlaps found

| Files | Between | Kind | Recommendation |
|---|---|---|---|
| `work-packages/board.md`, `work-packages/metrics.jsonl` | WP14, WP15, RS3, WP16 | shared, append-only | The PM alone edits them; no unit does. `board.md` today holds no rows for WP13 to WP16 or RS3; the PM adds them. |
| the architecture document's path | WP15 and WP16 | unset path | Set it in the WP15 scope, outside WP16's list (not under `docs/`, which WP16 edits throughout, and not in `contracts/`). If it is under `docs/`, its nav entry in `mkdocs.yml` joins WP16's one-line edit set. |
| order, not files | WP15 before WP16 | R-22 | No further package starts detailed design before the architecture document is approved. Whether WP16's spike stage may run first is the ACE's call (impact/WP16.md, Open question 1). |
| `research/prior-art/` | WP14 and WP16 | read only | WP16 reads it, never edits it. WP14 accepted before WP16's decide stage. |
| the machine interface (`contracts/machine-interface.*`, result shapes) | RS3 and WP16 | soft dependency | RS3's throwaway MCP server calls today's interface; it stays pinned to a pre-WP16 commit. No file is shared. |
| template `.obsidian/` | WP16 and the user's uncommitted edits (`app.json`, `core-plugins.json`, new `appearance.json`) in the template checkout | uncommitted work | Settle those edits before a WP16 unit touches the same files; no unit writes in that checkout's working tree. |
| the tools commit pin (`tests/docs/conftest.py`) and the template's pin (`pyproject.toml`, `uv.lock`) | WP16's two repositories | two-repository cycle | The PM schedules the re-pin order (impact/WP16.md, section 5). |

## WP17 ordering rules (files two units both write)

Not overlaps: the units run in the board's order, and the later unit starts from the earlier one's merged result.

| File | Writers, in order | Rule |
|---|---|---|
| `src/scat_kg/cli.py` | U1 (done), U2, then U3, serialised (PM decision) | U3's `draw` command is added after U2's commands land (U3 is queued behind U1 only, so the PM starts U3's cli edit after U2 is merged on `pm-wp17`). |
| `docs/reference/cli.md` | U2, then U3, serialised (PM decision) (then U5 only for wording, if it touches it at all) | The unit that adds a command writes its entry (PM default 3); the drift test ties it to `scat --help`. U5 owns `api.md`, not `cli.md`. |
| `src/scat_kg/__init__.py` | U1 (done), U2, then U3, serialised (PM decision) | U1 exports the views and the loader; U2 and U3 add their one export line each, only after the previous unit is merged (U2 and U3 both queue behind U1, so they must not run on the same base in parallel for this file). |
| `pyproject.toml`, `uv.lock` (tools) | U3 only | Nobody else in tools; the template's two files are U4's, a separate repository. |
| `docs/reference/` | U2/U3 (`cli.md`), U5 (`api.md`), U6 (`terms.md`) | Three different files, no shared one. |
| `tests/views/` | U1, then U2, U3 | U1 creates the small vault and its hand-computed tests; U2 and U3 add files beside it, not edits to U1's. |

## Check at the start of WP17 (U7)

Checked against `origin/dev` (at WP17 scope approval, 2573a34), `origin/wp17/build`, the remote spikes and the local `wp*`, `rs3`, `ace` and `pm` branches (`git diff --stat origin/dev...<branch>`). No overlap with a unit's files.

| Branch | Touches | Overlap with WP17 |
|---|---|---|
| `origin/wp17/build` | `work-packages/WP17.md`, `board.md`, `metrics.jsonl` | PM-only files; none |
| `origin/spike/analysis` (never merged) | `research/analysis/` only (221 files) | none |
| `origin/spike/obsidian-plugin` (never merged) | `research/obsidian-plugin/` only | none |
| `origin/spike/layout` (never merged) | `research/layout/` only | none |
| `origin/spike/chat-path` (RS3, never merged) | `research/chat-path/`, `spike/chat-path-server/`, and old copies of `work-packages/impact/file-map.md` and `impact/WP16.md` | **This file**, on paper: the spike carries an earlier copy. The spike is never merged, so there is no conflict; U7's branch is the one that merges. |
| `wp16/cfix` (local, unmerged, 2 commits) | `contracts/rule-catalogue.md` | none (WP17 does not write it); it is unmerged work, listed for the PM |
| `wp8/u1` (local, unmerged, 2 commits) | `src/scat_kg/ops/result.py`, `status.py`, `stub.py`, `tests/ops/` | none by file; WP17's views and exports return `Result` (read only, `ops/result.py`), so a later merge of `wp8/u1` could change it under them: the PM merges or retires `wp8/u1` before U1 starts, or U1 treats `Result` as fixed |
| `rs3-work` (local, 7 ahead of `origin/dev`) | `research/chat-path/` (4 notes), `spike/chat-path-server/`, old copies of `work-packages/impact/WP16.md` and `impact/file-map.md` | spike material, never merged; same paper overlap on this file as `spike/chat-path`; no conflict |
| `rs3-u3-work` (local, 6 ahead) | `research/chat-path/` (3 notes), `spike/chat-path-server/`, old copies of `impact/WP16.md` and `impact/file-map.md` | same as `rs3-work` |
| `wp12/u5`, `pm-wp16fix`, `ace-work`, `pm-work` | 0 commits ahead of `origin/dev` | none |
| template `origin/dev` (3cdbe60) | read only here | none: no package is in flight there; U4 adds the notebook (new file) and edits `ci.yml`, `pyproject.toml`, `uv.lock` |

## Files the units write that WP17's blast radius does not list

| File | Unit | Marking | Status |
|---|---|---|---|
| `contracts/architecture.md` | U2 | the `[OPEN: WP17]` slot (line 148 on `dev`) | in the PM scope check, item 1; listed here |
| `docs/reference/cli.md` | U2, U3 | the blast radius lists `docs/reference/` as a whole, so covered in words; named here because it is two units' file | PM default 3 |
| tests that follow the new commands and document kind (`tests/test_u8_cli_help.py`, `tests/test_machine_schema.py`, `tests/machine/`) | U2 | covered by `tests/` | listed so U2 knows they may need an edit |
| template `README.md` and `.gitignore` | U4 | change: the README names the notebook; the `.gitignore` ignores executed outputs | PM decision (after this check): both are in U4's zone; not in `WP17.md`'s text |
| the template's tools pin (in the template's `pyproject.toml` and `uv.lock`) | U4 | listed in WP17.md ("pin"); U4 pins a commit on `origin/wp17/build`, which needs a second move to `dev` after the merge | two-repository cycle as in WP16; the PM schedules the re-pin. The tools side (`tests/docs/conftest.py`, the template pin) stays unchanged |

No other overlap: WP14 and RS3 own only new folders under `research/`.
