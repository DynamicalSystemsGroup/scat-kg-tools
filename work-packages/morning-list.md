# Morning list for the chief engineer

Updated 27 November. Earlier versions are in git history. Words follow `GLOSSARY.md`.

## Where the release stands

| Package | State |
|---|---|
| WP14 to WP24, WP26 | accepted (latest: WP22 D-141, WP23 D-143, WP24 D-150, WP26 D-155) |
| WP25 coding paths, facilitating, planning | built; accepted when its account-bound walkthrough runs (U10) are done in your sitting |
| WP20 candidate and user acceptance | AI user tests pass on both paths (by hand to J10; chat path J1 to J4 and J6); the live chat stages wait on your sitting |

Candidate: tools `dev` (CI green), template `dev` 87accad pinning tools bc66409, Pages preview current. A visual
user-test pass (persona p2, by-hand path, on screen in Pages, Obsidian and Terminal) reached J10 with no blocking
finding; two fixes applied (D-156, `acceptance/reports/visual-r1-p2.md`). The reviewer's
guide is current to D-155; D-156's two fixes are not yet in it.

## Your sitting (the next step)

1. **SCAT Chat by eye** (WP22): open it from `deploy/build` or copy it to Applications; the menu-bar dot's colours, the
   menu, Copy address and Copy key, the vault confirmation, the first-start note, the alerts, a Stop, the Gatekeeper and
   keychain prompts.
2. **The walkthrough runs with your accounts** (WP25-U10), each taking its screenshots:
   - the AI chatbot path with **Claude**;
   - the AI IDE path with **Codex**;
   - **leave no trace** with **inference.coop**;
   - the by-hand screenshots in Obsidian (or let me take them with full-screen control).
3. **The chat-path user tests' live stages** (c1 to c3, J5 and J7 to J10), human-paced, as `acceptance/chat-path/plan.md`
   says; you sign in and paste each key, I drive.
4. **The GitHub website path** of `getting-started` step 1 (Use this template, Private), never yet run on screen: it
   needs your account. I drive; you are signed in.
5. **Four judgements for you:** from the visual pass, V2 (Obsidian may rewrite `index/narrative.base` into its own
   form), V3 (the stub's timeframe hint is invisible in Obsidian), V4 (no page says whether node pages must be written
   before their narratives are done); and the chat path's "Install once" uses Terminal (the pages say a person who sets it up does
   it); the mission says the organiser must not be required to open a terminal on that path (D-155).

Then: your walkthrough (UA-M) from `acceptance/reviewers-guide.md`, and I open the release PRs.

## After the release

- The w3id namespace registration PR from your fork, citing the release (D-116).
- Candidate C9 (a commit as the trigger to read written content into the knowledge graph) stays a candidate.
