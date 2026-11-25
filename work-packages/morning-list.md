# Morning list for the chief engineer

Updated 25 November, afternoon. Earlier versions are in git history. Words follow `GLOSSARY.md`.

## Where the release stands

| Package | State |
|---|---|
| WP14 to WP19, WP21 | accepted (WP17 D-111, WP18 D-122, WP21 D-121) |
| WP20 candidate and user acceptance | manual path passes UA-A; uv gap closed (D-112); chat-path UA-A waits on your sitting |

Candidate: tools `dev` 834490f (CI green), template `dev` 271c3e9 pinning tools 7f0ed05, Pages preview current.
Before the release PRs: your chat-path sitting (item 1).

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
