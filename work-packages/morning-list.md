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

1. **A chat-path sitting (after WP21):** the three chat-path user tests (D-098), the "leave no trace" walkthrough run,
   and loading the skill package. You sign in and paste each key; I drive.
2. **After the release:** the w3id namespace registration PR from your fork, citing the release (D-116).

Settled today: D-102 to D-108, D-110, D-116 (release scope C1 to C8; U3b; Colima default; the published image and
the mission edits; leave no trace; the uv test; WP8-U1; history rewrites dropped; no further chat clean-up; your
template checkout's scratch edits discarded; commit-as-trigger noted as candidate C9).

## For your walkthrough (UA-M)

Start from `acceptance/reviewers-guide.md`: sitting 1 is your walkthrough on both paths, with scripts in
`acceptance/`. Sitting 4 lists every call I made with its evidence and revert tag.
