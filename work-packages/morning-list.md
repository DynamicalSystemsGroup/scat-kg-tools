# Morning list for the chief engineer

Updated 27 November. Earlier versions are in git history. Words follow `GLOSSARY.md`.

## Where the release stands

| Package | State |
|---|---|
| WP14 to WP24, WP26 | accepted (latest: WP22 D-141, WP23 D-143, WP24 D-150, WP26 D-155) |
| WP25 coding paths, facilitating, planning | built; accepted when its account-bound walkthrough runs (U10) are done in your sitting |
| WP20 candidate and user acceptance | AI user tests pass on both paths (by hand to J10; chat path J1 to J4 and J6); the live chat stages wait on your sitting |

Candidate: tools `dev` (CI green), template `dev` 6ccfd9d pinning the tools candidate 5e4ab16, Pages preview current. A visual
user-test pass (persona p2, by-hand path, on screen in Pages, Obsidian and Terminal) reached J10 with no blocking
finding; its fixes and your answers on V2 to V4 are in D-156 (`acceptance/reports/visual-r1-p2.md`). The reviewer's
guide is current to D-156.

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
4. **One ruling (D-166):** in WP27 the auto-mode classifier denied a worker's broad `git add -A && git commit`; the PM
   then committed the same in-scope diff with named paths. Keep, or revert and redo? Also for your review: the glossary
   call on **cap** and **attribution mode** (organiser chooses, setup person writes).
5. **When you're back from errands:** a short sitting for the account-bound trials held from WP28 (images in Claude
   and inference.coop; Claude's two header forms) and RS5 (client trials, from its trial plan); then WP29's stage
   model for your approval.

Then: your walkthrough (UA-M) from `acceptance/reviewers-guide.md`, and I open the release PRs.

## After the release

- The w3id namespace registration PR from your fork, citing the release (D-116).
- Candidate C9 (a commit as the trigger to read written content into the knowledge graph) stays a candidate.
