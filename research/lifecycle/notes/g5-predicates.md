# RS5-G5: which transition predicates the tools can evaluate

27 Nov 2026, worktree `rs5-u2`. All runs on copies of `contracts/examples` (3 groups, cap 3, mode disallowed) under `scratchpad/rs5u2/`; fixtures untouched. `scat X` below is `uv run --frozen --extra mcp scat X --root <copy>`; MCP calls went through `build(root).call_tool`.

## Findings first

- **Complete (tool alone):** vault folder exists, `scat.toml` cap and mode present, a narrative's status, narrative coded, check passes, would-`done` passes, views run without page errors.
- **Partial:** "set up" (the tool sees `scat.toml` and pages, not the install, Obsidian or git), cap met, all narratives done, views generated.
- **User's word:** terms set, field notes taken, model finished, committed, pushed, tagged.
- **Biggest gap:** no tool reads `scat.toml`. Mode reaches the assistant in every result (`mode`); the cap value never does. "Cap met" shows only as a refused write.

## Predicates

| # | Wording | Evaluator | Evidence | Verdict |
|---|---|---|---|---|
| 1 | The vault folder exists | `check` | `scat check --root .../nonexistent` -> `refused ...: the vault folder does not exist`, rc=1 | complete |
| 2 | The vault is set up | `check` (needs `scat.toml`, pages) | on an empty folder: `error [SCAT-CAP-CONFIG] scat.toml ...: the file is missing`; `attribution mode: not declared`; `1 error`, rc=1. `status` there: `no pages`, rc=0 | partial: not install, Obsidian, git |
| 3 | `scat.toml` has the cap | `check` | file with only `attribution`: `error [SCAT-CAP-CONFIG] ... the key is missing`, rc=1 | complete (presence; value is not exposed) |
| 4 | `scat.toml` has the attribution mode | `check`; field `mode` in every MCP result | file with only the cap: `attribution mode: not declared`, `error [SCAT-MODE-CONFIG] ... the key is missing`, rc=1. Good vault: `"mode": "disallowed"` | complete |
| 5 | Stakeholder-group cap met | none direct; `stub` refuses at the cap; `status` rows can be counted; `check` errors only when exceeded | at 3 of 3: `scat stub fourth-group --type group` -> `refused scat.toml ...: the vault is at its cap of 3 groups ... raise ... in scat.toml`, rc=1. Cap 2, 3 groups: `error [SCAT-CAP] ... holds 3 group pages, over the cap of 2` | partial: over cap complete; "met" only by a refused write; cap value unreadable |
| 6 | A narrative page exists, and is stub, draft or done | `status [page]` | `scat stub new-notes --type narrative` -> `created narrative/new-notes.md`; `scat status new-notes` -> `stub  narrative/new-notes.md` / `1 stub`. MCP rows: `{"name","type","status"}`; `counts` `{'stub':2,'draft':1,'done':11,'other':0}` | complete |
| 7 | The narrative is coded (links at least one node) | `check` (SCAT-UNCODED), `fingerprint` | new stub: `warning [SCAT-UNCODED] ... links no node page, so it is excluded`; `scat fingerprint new-notes` -> `refused ... the narrative is excluded`, rc=1. After `scat record-edge holds borrowers quick-checkout --told-by new-notes`: UNCODED count 0; fingerprint lists `holds: borrowers -> quick-checkout` | complete |
| 8 | The check passes with no errors | `check` (`ok`, rc) | good copy: `0 errors, 2 warnings`, rc=0, MCP `"ok": true`, `problems` = 2 warnings. Cap-2 copy: `1 error`, rc=1 | complete (structure only; warnings do not count) |
| 9 | The narrative may be set to done | `set-status X done` (CLI) | on a stub: `refused [SCAT-DONE-REFUSED] ... 2 error(s) would stand at status done` (description, timeframe), status unchanged. MCP `set_status done`: `"ok": false`, `this server never sets a page to done` | complete on CLI as a dry test; MCP never moves it |
| 10 | All narratives done | none; derive from `status` rows | rows give `[('funders-meeting','draft'),('new-notes','stub'),('saturday-...','done'),('self-service-...','done')]`, so `all done: False`; `counts` mixes node pages and narratives | partial: caller aggregates |
| 11 | Views generated | `layered`, `fingerprint`, `edge_table`, `trace` run on demand; `export_edges` writes files | `scat layered` -> `layered view of funders-meeting, ...`. MCP `export_edges` -> `created: views/holds.csv, holds.md, addressed-by.*, provided-by.*`; no tool reports that `views/` exists | partial: a view is computed, not stored; files exist only after export |
| 12 | Views can be trusted (no page errors) | views refuse | a dangling `[[no-such-page]]`: `scat layered` -> `refused ...: 1 error(s) in the pages this view draws`. A cap error alone did not stop `layered` (cap-2 copy ran) | complete for drawn pages; not vault-wide errors |
| 13 | A done narrative is changed or reopened | `record_edge`, `remove_edge` refuse; no history | `scat record-edge ... --told-by self-service-kiosk-pitch` -> `refused ...: the narrative is done and this row would change it`, rc=1. Reopen is the coder's `set-status draft`; a change of status is visible only against an earlier `status` | partial |
| 14 | Terms are set (nine choices) | coder's word | `plan.txt` is outside the page folders and "the check does not read it" (planning.md:5); no tool reads terms | user's word |
| 15 | Field notes taken | coder's word | the assistant touches inputs only by reading what the coder gave (SKILL.md A12); no tool lists them | user's word |
| 16 | The coder says the model is finished | coder's word | stated outside the tool (`ace-org/MISSION.md:85`; coding.md:989); `check` and `status` do not carry it | user's word |
| 17 | Committed, pushed, tagged | git, not the tool | no operation reads git; the copy is not a git repository (not run) | user's word |

## Counts

17 predicates; 13 run (1 to 13). Complete 7 (1, 3, 4, 6, 7, 8, 12); 9 complete on the CLI, never on the server; partial 5 (2, 5, 10, 11, 13); user's word 4 (14 to 17).

## Gaps

1. No server read of `scat.toml`; "cap met" needs one, or a group count against the cap in `status`.
2. No stored or derived vault stage; "all done" and "views generated" are the caller's aggregates.
3. Check is structure only; it cannot show interpretation is right.
4. Not run: git; a chat client calling these.
