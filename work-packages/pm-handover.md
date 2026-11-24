# PM handover (outgoing PM, after WP8-U11)

Read first: `ORG.md`, `MISSION.md`, `work-packages/WP8.md`, `decisions/log.md` D-041 to D-044, the board, `acceptance/README.md`,
`acceptance/reports/r1-findings.md`.

## Where things stand (tools `dev` 2a9cc07, template `dev` 89af44a)
- WP8 units U2 to U11, U8b, U8c done and merged. Iteration 8 is open. Velocity so far on this package: 55 estimated
  points landed, 59 realized.
- **U1 is held**: the chief engineer's authorisation is needed to edit two existing assertions in
  `tests/ops/test_ops_stub.py` (D-042 morning list). Branch `wp8/u1` (commits `3ed3163`, `9e6ca44`) and its worktree
  `scat-wt/wp8-u1` (beside the repository folder) stay as they are. Never delete them. When it lands, `src/` changes, so
  every pin moves and the U1-dependent docs spots listed in the U3 report change (coding.md about lines 190, 361, 382,
  message 7; reference/api.md about lines 247 and 276 to 282).
- **Pins are one step behind.** The candidate tools commit is the last tools commit that changes `src/` or `docs/`
  (log D-041). U11 changed docs, so that is now `2a9cc07`. The template still pins `9fad960` and the docs test pins
  template `89af44a`. **Next step is U12 (re-pin):** (1) template worktree, branch `wp8/u12`: set the `rev` in
  `pyproject.toml` to the full sha of the candidate, `uv lock`, verify in a fresh clone of the local repo (`uv sync`,
  `scat check` = 0 errors and only SCAT-CONFLICT-BOTH, `scat index` leaves `git status` empty, `uv lock --check`),
  merge to template `dev` and push it yourself; (2) tools worktree, branch `wp8/u12`: `TEMPLATE_COMMIT` in
  `tests/docs/conftest.py` to the new template merge sha; full suite, mkdocs strict; merge and push. A worker's
  branch push may be refused by the guard: do not retry, merge the local branch yourself and push `dev` (your normal
  role). Then rerun U9 (clean clone, Pages banner).
- Settings (Pages, template flag, default branch) are done and are the ACE's; the Pages site deploys from `dev` on every push.
- Branches: only `main`, `dev` remain on both remotes, plus the held `wp8/u1` locally.

## UA-A round 2 (next after U12)
Provision with `<scratch>/provision.sh <name>`
(fresh HOME, uv on PATH, clone of the local template with its remote removed; it prints the shell preamble; it sets
`UV_PYTHON_INSTALL_DIR` to the existing Python store so no downloads). Copy the persona brief and
`acceptance/report-template.md` into the tester's folder (not the repo); give the tester the preamble and the two file
paths (the prompt used in round 1 is in the scratchpad `tester-prompt.txt`, and the round-1 agent prompts follow the
same shape). Use fresh testers; the briefs carry fixed domains (flood readiness, farmers' market, bicycle co-op) and reusing them is fine because no tester remembers a round. Models: p1 Haiku (Python REPL is mandatory for J5 to J7, piped into
`python -i`), p2 Haiku (CLI), p3 Sonnet control. The cold read is two messages: send `briefs/cold-read-part1.md`
alone, and only after it is answered send `cold-read-part2.md`; assemble answers 1 and 2 into the report. Save reports
as `acceptance/reports/r2-<persona>.md` (extract the report from the agent's final message). Void check with the grep in
`acceptance/README.md`. J7 for agents is a clean check plus a local commit; the push is never a finding (D-044). Every
report must say plainly that uv was preinstalled (gap held for the chief engineer, D-040, D-041).
Pass bar: every tester reaches J7 (clean check, local commit); every guess is a finding, each dispositioned by the ACE;
the cold read names jazz unprompted and reports no instruction obscured. If round 2 leaves a blocking finding, plan U14
(fix, est. 5), a re-pin (U15), and round 3 (U16, est. 12); otherwise skip them and record that.

## Remaining units after round 2 (estimates on the board)
U17 reviewer's guide (est. 8, sittings 1 to 4, `acceptance/reviewers-guide.md`; sitting 3 has a table of R-1 to R-15
with evidence; sitting 4 lists every ACE call with log id and `divergence/` tag, and the known weaknesses: uv
preinstalled (D-040, D-041), push unreachable for agents (D-044), docs tests run only bash and python blocks (D-043),
Obsidian untested, shown `$` message blocks pinned only by manual runs, the held U1, any accepted findings); U18 w3id
registration file in `acceptance/` (est. 2, prepared for him to submit, the ACE does not submit it; check the
`../w3id.org` checkout for the format); U19 private-string and attribution sweep (Haiku, est. 1). Then hand back to the
ACE before the release PRs.

## Standing rules for the next PM (unchanged)
No private titles, owners or links in any file or commit. No AI attribution anywhere. Board Units table, the Current line
and `metrics.jsonl` true at every state change; write real times (use the merge commit time, never a placeholder);
metrics are read last-per-unit in file order. Both core heuristics in every brief. Estimation lessons: units others
align with cost 8; every user test gets a planned fix unit; changing a shared fixture costs the tests it disturbs.
Never work around a guard refusal: take the additive route or hold the unit and message the ACE. Agents never run
downloaded installer scripts and never create repositories from the template. Reviewers look at rendered pages in a
browser. Do not contact the chief engineer.

## Cost notes
Round 1 cost about 50 to 90 thousand tokens per tester. A small fix unit with a fresh review costs about 250 thousand
across worker and reviewer. Scratch files live in the session scratchpad (`ua/`, `v*`, `provision.sh`).
