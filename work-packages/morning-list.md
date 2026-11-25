# Morning list for the chief engineer

Updated 25 November, morning. Earlier versions are in git history. Words follow `GLOSSARY.md`.

## Where the release stands

Every work package of Mission Amendment 5 is built and on `dev`, CI green in both repositories (tools 490ba13,
template 31667fc, Pages preview current):

| Package | State |
|---|---|
| WP14 prior art, WP15 architecture, RS3 chat-path spike, WP16 ontology and layout, WP19 range vault | accepted |
| WP17 views (fingerprint, edge tables, layered view, traces; notebook in the template) | built; held only on WP17-U3b (item 1) |
| WP18 chat path (MCP server, assistant's file, container, launcher, guides) | built; waits only on its live run (item 3) |
| WP20 candidate and user acceptance | manual path passes UA-A (two rounds, D-100, D-101); chat path waits on item 3; reviewer's guide current |

What is left before I open the release PRs: items 1 and 3 below.

## Waiting on you

1. **WP17-U3b, a guard-refused one-line schema edit (D-093).** `scat draw --out` can save a drawing outside the
   vault, which the machine-interface schema doesn't allow for `draw`. Either (a) you allow the edit, or (b) I rule
   that drawings are saved only inside the vault (as the chat path already does) and the code changes instead.
2. **Permission to install Docker Desktop (D-096)**, so the chat path's graphical container runtime is tested once
   before release. Without it, the guide keeps saying it is untested.
3. **The chat path.** WP18's live run (WP18-R4) ran on 25 November and is torn down
   (`acceptance/chat-path/live-run-wp18-r4.md`). Left: delete the "Scat Lab" MCP entry in the chat by hand; the
   three chat-path user tests (D-098) in a later sitting. Your UX observations from the run are harvested as
   candidates C1 to C7 in `work-packages/candidates.md`.
4. **The uv gap (D-040, D-041):** every UA-A tester had uv pre-installed, where the mission says "uv not installed".
   Accept it as a known gap, or permit one fresh tester to run uv's official installer.
5. **History rewrites, all optional:** `main` (commit `c58113b`, the pilot line) and `dev` (commit `20ff07a`, private
   repository names; an old log entry, now redacted). Each needs a force-push only you can authorise.
6. **Your template checkout:** a `git pull` will stop on your uncommitted `.obsidian/` edits (`core-plugins.json`,
   `app.json`). Settle them before pulling.
7. **WP8-U1 (D-042):** the held test edit in `tests/ops/test_ops_stub.py` (its assertions are untouched).
8. **At release:** the w3id namespace registration PR from your fork.

## For your walkthrough (UA-M)

Start from `acceptance/reviewers-guide.md`: sitting 1 is your walkthrough on both paths, with scripts in
`acceptance/`. Sitting 4 lists every call I made with its evidence and revert tag.
