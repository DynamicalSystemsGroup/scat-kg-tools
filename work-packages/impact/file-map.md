# File map

Kept by the change consultant (`.claude/agents/change-consultant.md`). For each package in flight, the files it owns.
The PM checks a unit's blast zone against this map before dispatch; an overlap is reported at once. Updated at
2026-11-24 from `work-packages/plan.md`, `work-packages/board.md`, the scopes `WP13.md`, `WP14.md`, `RS3-chat-path.md`
and `impact/WP16.md`. Words follow `GLOSSARY.md`. Paths are in `scat-kg-tools` unless a repository is named.

## Packages in flight

| Package | State | Owns (files) |
|---|---|---|
| WP14 prior-art readout | scope approved (D-079) | `research/prior-art/` (new). Also, as PM-only edits: `work-packages/board.md`, `work-packages/metrics.jsonl`. |
| WP15 architecture document and review | no scope file yet | The architecture document (deliverable D-2; **path not set**) and the architecture reviewers' review record (**path not set**). Also PM-only: `board.md`, `metrics.jsonl`. |
| RS3 chat-path spike | scope approved (D-080) | Branch `spike/chat-path` (anything on it, never merged into `dev`); on `dev`: `research/chat-path/`. Also PM-only: `board.md`, `metrics.jsonl`. |
| WP16 ontology and layout (absorbs WP13) | impact map built (this unit); no scope yet | `ontology/scat.ttl`; `contracts/` (all four documents and `contracts/examples/`); `src/scat_kg/`; `tests/` (including `tests/docs/conftest.py`); `docs/` (all pages, plus new `docs/flow.md` and `docs/data-and-consent.md`) and `mkdocs.yml`; `acceptance/` (README, reviewers-guide, walkthrough, `briefs/`, `personas/`, `playtest-findings.md`, new briefs and reports); `work-packages/WP16.md` and `work-packages/impact/`; in `scat-kg-template`: the vault pages, `class/`, `.obsidian/`, `.gitignore`, `README.md`, `scat.toml`, `pyproject.toml`, `uv.lock`. At acceptance only: `plan.md` item 4 (the ACE). PM-only: `board.md`, `metrics.jsonl`. Detail and counts: `impact/WP16.md`. |

WP13 is absorbed into WP16 (D-078): it owns nothing of its own and is not dispatched. Packages not yet in flight (WP17 to
WP20) are not listed; WP17, WP18 and WP19 read the model WP16 writes and start after it (plan.md).

## Files owned by no package, kept as they are

`decisions/log.md` (append only, by the ACE), `research/` (the accepted readouts; WP14 and RS3 add new folders only),
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

No other overlap: WP14 and RS3 own only new folders under `research/`.
