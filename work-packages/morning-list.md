# Morning list for the chief engineer

Updated 25 November, afternoon. Earlier versions are in git history. Words follow `GLOSSARY.md`.

## Where the release stands

| Package | State |
|---|---|
| WP14, WP15, RS3, WP16, WP19 | accepted |
| WP17 views | **accepted** (D-111): U3b applied after your D-104 |
| WP18 chat path | built; live run done 25 November (`acceptance/chat-path/live-run-wp18-r4.md`); acceptance waits on the key fix (C7, in WP21) |
| WP20 candidate and user acceptance | manual path passes UA-A; the uv gap is closed (D-112); chat-path UA-A waits on your sitting |
| WP21 rules and norms, life cycle, image (C1 to C8, D-102 to D-107, D-110) | scope revised after the PM's check; impact map in progress; then approval and build |

Before the release PRs: WP21 built and accepted, WP18 accepted, the chat-path sitting below.

## Waiting on you

1. **History rewrites (D-109 is held, D-113).** Sizing them showed costs the question didn't state. `c58113b` is in
   `dev` as well as `main`, so removing it re-hashes about 754 commits on `dev` and 59 on `main`. That orphans the
   template's pinned tools commit, the 23 revert tags and the hashes cited across the log, board and metrics. GitHub
   also keeps the old commits reachable through PR #8's head ref, so the text would not be fully gone without asking
   GitHub support. Do you still want both rewrites, knowing this?
2. **One more lab conversation in inference.coop.** This run's uploaded note and its two conversations are deleted
   there (local copies kept). A third conversation, "Vault Check Results Summary", is from the overnight server test,
   with lab material only. Delete it too?
3. **A one-line mission edit for D-106:** Release step 3 would also publish the MCP server image when the ACE tags
   `v0.1.0`. The mission is yours to change; I'll draft the sentence for your merge.
4. **A chat-path sitting (after WP21):** the three chat-path user tests (D-098), the "leave no trace" walkthrough run,
   and loading the skill package. You sign in and paste each key; I drive.
5. **Your template checkout:** a `git pull` will stop on your uncommitted `.obsidian/` edits (`core-plugins.json`,
   `app.json`). Settle them before pulling.
6. **At release:** the w3id namespace registration PR from your fork.

Settled today: D-102 to D-108, D-110 (release scope C1 to C8, U3b, Colima default, the published image, leave no
trace, the uv test, WP8-U1's two assertions).

## For your walkthrough (UA-M)

Start from `acceptance/reviewers-guide.md`: sitting 1 is your walkthrough on both paths, with scripts in
`acceptance/`. Sitting 4 lists every call I made with its evidence and revert tag.
