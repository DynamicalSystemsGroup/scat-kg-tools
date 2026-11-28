# WP37 landing: the exact steps, in order

Everything for WP37 is prepared on two **unmerged** branches. Nothing has been renamed on GitHub, merged, tagged or
published. The steps below take minutes. Commands assume `gh` is signed in as the chief engineer.

| | Tools | Template |
|---|---|---|
| Branch | `wp37/rename` (origin: `DynamicalSystemsGroup/scat-kg-tools`) | `wp37/rename` (origin: `DynamicalSystemsGroup/scat-kg-template`) |
| Tip when this file was written | the commit that adds this file (`git rev-parse origin/wp37/rename`) | `9defb3f1fed10da1a16229f3bd84020341d92b9c` |
| Worktree | `/Users/z/Documents/GitHub/scat-wt/wp37-tools` | `/Users/z/Documents/GitHub/scat-wt/wp37-tpl` |

**The two pins are already set on the branches; after the merges below nothing needs changing**, provided the template
is merged fast-forward and the tools branch with a merge commit (neither squashed):
- the template's `pyproject.toml` and `uv.lock` pin tools commit `abc349f1a7eced52d8e0586811dc14eff1557b2c` (the rename,
  first commit of the tools branch; its `src/` and `deploy/` are the branch tip's), by the address
  `https://github.com/DynamicalSystemsGroup/scat-tools`;
- the tools `tests/docs/conftest.py` has `TEMPLATE_COMMIT = "9defb3f1fed10da1a16229f3bd84020341d92b9c"` and
  `TEMPLATE_URL` `https://github.com/DynamicalSystemsGroup/scat-template`.
If the template's `dev` head is not `9defb3f` after its merge (a merge commit or a squash), set `TEMPLATE_COMMIT` to that
head in a follow-up commit on tools `dev` and run `uv run pytest tests/docs -q`.

Both pins name addresses that do not exist until step 1 is done. That is why CI on both branches is **red until then**,
for these reasons only: the tools tests that clone the template (`tests/docs`) cannot reach `scat-template`, and the
template's CI cannot fetch `scat-tools`. With the addresses mapped to the local clones the same tests pass (below).

## Steps

1. **Chief engineer, in GitHub (an account action).** Settings > General > Repository name, for each:
   `DynamicalSystemsGroup/scat-kg-tools` to `scat-tools`, then `DynamicalSystemsGroup/scat-kg-template` to
   `scat-template`. Check the template is still marked as a template (Settings > General > "Template repository") and
   its default branch is `dev`. GitHub redirects the old git and web addresses; the old Pages address does not redirect.
2. **Local remotes**, for each clone (worktrees share their clone's remote, so these six cover them all):
   ```
   git -C /Users/z/Documents/GitHub/scat-kg-tools remote set-url origin https://github.com/DynamicalSystemsGroup/scat-tools.git
   for d in tpl-pin2 tpl-pin3 wp21-tpl wp23-template wp26-template; do
     git -C /Users/z/Documents/GitHub/scat-wt/$d remote set-url origin https://github.com/DynamicalSystemsGroup/scat-template.git
   done
   git -C /Users/z/Documents/GitHub/scat-kg-tools remote -v
   ```
   (The clones `scat-kg-template` and `tpl-pin2-verify` point at local folders; leave them.) The folders keep their old
   names; renaming a folder needs `git worktree repair` and is not needed.
3. **Re-run CI on both branches** and wait for green:
   ```
   gh run list -R DynamicalSystemsGroup/scat-template --branch wp37/rename -L 1
   gh run rerun -R DynamicalSystemsGroup/scat-template <run id>
   gh run list -R DynamicalSystemsGroup/scat-tools --branch wp37/rename -L 3
   gh run rerun -R DynamicalSystemsGroup/scat-tools <run id of CI>
   gh run watch -R DynamicalSystemsGroup/scat-tools <run id>
   ```
   Both must be green. If the template's CI cannot build, stop: the tools address or the pinned commit is wrong.
4. **Merge the template** (fast-forward, so `9defb3f` stays its head):
   ```
   cd /Users/z/Documents/GitHub/scat-wt/tpl-pin3 && set -e -o pipefail && test ! -d .git/rebase-merge
   git fetch origin && git checkout dev && git merge --ff-only origin/wp37/rename && git push origin dev
   git rev-parse HEAD    # expect 9defb3f1fed10da1a16229f3bd84020341d92b9c
   ```
5. **Merge the tools** (with a merge commit, the PM's gate, after tier 1 is green on the branch):
   ```
   cd /Users/z/Documents/GitHub/scat-wt/wp37-tools && set -e -o pipefail && test ! -d .git/rebase-merge
   git fetch origin && git checkout wp37/rename && git merge --no-ff origin/dev   # clean; origin/dev should not have moved
   uv run ruff format --check . && uv run ruff check . && uv run pytest -q -p no:cacheprovider
   uv run --group docs mkdocs build --strict
   git checkout dev && git merge --no-ff -m "WP37: the rename (SCATLAB, scat-tools, scat-template)" wp37/rename && git push origin dev
   ```
   If `origin/dev` has moved, the merge may conflict where new work used old names: apply "The rename rules" below to
   the conflicting files and run `uv run pytest tests/test_wp37_names.py`, which lists every remaining old name.
6. **Metrics and board, on `dev`, now** (the ACE). The branch's `work-packages/metrics.jsonl` already holds the five units
   and the iteration record with the iteration number **63 assumed**; if `dev`'s last iteration is not 62, renumber the
   `"iteration": 63` fields in those lines, then run `python3 work-packages/check_metrics.py --accept WP37`. Add to
   `work-packages/board.md`: the five rows (WP37-U1, U2, U3, U4, U1r; points as in the log; state done) and the iteration
   row `| 63 | WP37-U1 to WP37-U1r | 22 | 21 | 0.95 | 0.7 h | 30.0 |` (match the table's column order). Log the entries
   (the ACE's: this file writes none).
7. **Pages and the image.** The push to `dev` runs the Pages workflow (it triggers on `docs/**`, `mkdocs.yml`):
   ```
   gh run watch -R DynamicalSystemsGroup/scat-tools $(gh run list -R DynamicalSystemsGroup/scat-tools --workflow Pages -L 1 --json databaseId -q '.[0].databaseId')
   curl -sI https://dynamicalsystemsgroup.github.io/scat-tools/ | head -1     # expect HTTP/2 200
   curl -sI https://dynamicalsystemsgroup.github.io/scat-tools/chat-path/ | head -1
   ```
   The published image has not shipped yet (the release workflow is gated), so the launcher builds from source until a
   `v*` tag publishes `ghcr.io/dynamicalsystemsgroup/scat-tools:<version>` under the new name.
8. **The on-screen run (R2)**, the chief engineer and the ACE: follow `acceptance/walkthroughs/rename-run.md`
   (install over the earlier app; one app, one keychain item, one image; connect in Claude). It needs the merged `dev`.
9. **Clean up** (hygiene, ORG.md): after steps 4 and 5,
   ```
   git push origin --delete wp37/rename                      # in the tools clone, then the template clone
   git worktree remove /Users/z/Documents/GitHub/scat-wt/wp37-tools && git worktree remove /Users/z/Documents/GitHub/scat-wt/wp37-tpl
   git worktree prune && git branch -d wp37/rename
   ```
   Every other live branch and worktree (the `pm-*`, `wp20-*`, `spike/*` and `ace-*` ones) still uses the old names; a
   branch that will be merged later needs the rename applied to it first ("The rename rules" below).

## The rename rules (for a branch that must catch up)

In every tracked file outside `decisions/`, `acceptance/`, `work-packages/`, `research/`, in this order:
`SCAT_CHAT_` to `SCATLAB_`; `SCAT Chat` to `SCATLAB`; `scat-chat` and `scat_chat` to `scatlab`; `scat-kg-tools` to
`scat-tools`; `scat-kg-template` to `scat-template`; `scat-kg-vault` to `scat-vault`; `scat_kg` to `scat_tools`;
`scat-kg` to `scat-tools`. Move `src/scat_kg` to `src/scat_tools`, `deploy/SCAT Chat.applescript` to
`deploy/scatlab.applescript`, `deploy/scat-chat.sh` to `deploy/scatlab.sh`. Then `uv lock`, `uv run python
scripts/glossary.py`, `uv run ruff format .`. `deploy/retire-old.sh` and the two tests named in
`tests/test_wp37_names.py` keep the old names on purpose.

## Evidence the branches pass once the addresses exist

With git told that the new addresses are the local clones (no repository content changed), the full suite passes on the
tools branch and the template installs, checks and runs its notebook against the pinned tools commit:
`GIT_CONFIG_GLOBAL=<file with url.<local clone>.insteadOf = https://github.com/DynamicalSystemsGroup/scat-template> uv run pytest`.
