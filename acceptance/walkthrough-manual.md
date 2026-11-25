# UA-M walkthrough, manual path: the chief engineer's script

You run the journey J1 to J10 yourself, from the documentation, on the candidate, without help. This script does not
teach it. For each stage it gives where to enter, the steps, what "done" looks like, what to record, and where to
resume. The docs are the instructions; this script only points at them. The chat path has its own script,
[`walkthrough-chat.md`](walkthrough-chat.md).

**Pass (MISSION.md, UA-M):** you complete J1 to J10 on both paths from the docs without help, and judge the
documentation clear and navigable and the journeys clear. Anything you flag is fixed on `dev`, the candidate is
refreshed, and you resume from the affected stage.

## Docs fixes pending

Another unit has fixed five documentation defects (log D-098, ruling 3) on its branch; they reach the candidate when
that branch merges. The links below go to where each fix lands. Until it is merged, a mismatch on these is known and is
not a new finding; once it is, it is.

1. The fingerprint view's command: [coding](../docs/coding.md#5-a-link-without-a-row), step 5, now runs
   `uv run scat fingerprint <narrative>`, as [analysis](../docs/analysis.md#the-notebook) and the
   [CLI reference](../docs/reference/cli.md#scat-fingerprint) do.
2. The command to run the notebook, `uv run jupyter lab analysis.ipynb`, is in [analysis](../docs/analysis.md#the-notebook),
   with a headless form (`jupyter nbconvert --to html --execute`) (J9 step 2).
3. The solo trial has a section of its own: [The solo trial](../docs/getting-started.md#the-solo-trial) (J2).
4. [See which commit a tag pins](../docs/coding.md#see-which-commit-a-tag-pins): `git rev-parse v1^{commit}`,
   `git show --stat v1` and `git ls-remote --tags origin v1` (J10 step 4).
5. A no-terminal route (GitHub Desktop) is on the chat path: [Your vault with no
   terminal](../docs/chat-path.md#your-vault-with-no-terminal-github-desktop); see the chat script.

## How to split the walk into sittings and resume

- **Start page:** the Pages preview, <https://dynamicalsystemsgroup.github.io/scat-kg-tools/>, marked pre-release.
  Follow the docs' own links from there. Do not open `src/` or `tests/` to find an answer. The links below go to the
  same pages in this repository, for checking this script.
- **Sittings.** Stop only at the end of a stage; J8 also has a stop between its REPL half and its CLI half.

| Sitting | Stages | You are done when |
|---|---|---|
| A. Solo trial | J1, J2 | one narrative of your own is `done` in a throwaway repository |
| B. Terms and set-up | J3, J4, J5 | your real private repository is cloned, its check clean, and open in Obsidian |
| C. Plan and capture | J6, J7 | a plan exists, the example is cleared and committed, and you hold field notes for one scenario and one architecture |
| D. Code | J8 | every narrative is `done`, coded by the REPL and by the CLI |
| E. Analyse and hand over | J9, J10 | a version is locked and handed over |

- **Resume.** Every stage ends in a state you can see. Reopen the stage's entry, read its **Resume** line, and check
  that state before you go on. The vault is a git repository, so `git status` and the last commit show where you
  stopped. If the state is not there, redo the stage from its first step.
- **Your own elicitation.** Choose a small topic of your own for J2 and J6 to J10: at least one scenario and one
  architecture, in your own words and group names, not the worked example's.
- **Failing.** Do not work around a failure. Record the page, the exact step, the exact text you typed and the exact
  output, and what you expected from the docs. Then stop or carry on. The fix is the team's job.
- **Your notes.** Send them as plain text, stage by stage. There is no required format.

## What only you can do (held for you)

1. **uv installer (D-040, D-041).** The team never ran uv's downloaded installer, because running a downloaded
   installer needs your permission. J2 is the first real run of the docs' command. Running it is your call.
2. **A real private repository and a real push.** The team's tests used a clone with no remote. J2, J5 and J10 are the
   first real use of GitHub.
3. **Obsidian.** The team checked Obsidian steps through the files only. J2, J5, J8, J9 and J10 are the first time
   Obsidian opens the vault.

---

## J1 Discover

**Enter.** Open <https://dynamicalsystemsgroup.github.io/scat-kg-tools/> ([`index.md`](../docs/index.md), the home page).

**Steps.**
1. Before you read [Why it is called SCAT](../docs/index.md#why-it-is-called-scat), say what style or reference the page evokes, and write it down.
2. Read the page, then look at the navigation.

**Done.** You can say in a sentence what SCAT turns into what; what S, C, A and T stand for; and where to go next
([Where next](../docs/index.md#where-next)). The navigation lists Home, The flow, Data, rights and consent, Getting
started, Planning, Facilitating (Scenarios, Architectures), Coding, Coding in a chat, Coding in an IDE, Analysis and
Reference.

**Record.** The style you named, before the explanation. Any broken web link (page and its text), broken image, or anything
that blocked an instruction.

**Resume.** Nothing to resume; reopen the home page.

## J2 Try

**Enter.** [`flow.md`](../docs/flow.md#first-try), "First try" (steps 5, 2 and 8, in that order), then
[`getting-started.md`](../docs/getting-started.md#1-create-your-private-repository), "1. Create your private
repository". The solo trial has its own section there, [The solo trial](../docs/getting-started.md#the-solo-trial) (docs fix 3). Use a **throwaway** repository, named
`my-vault` as the docs do. Delete it after J5.

**Steps.**
1. Create the repository, private, by the website path or the `gh` path, and clone it. The `gh` path is one command:

   ```text
   gh repo create my-vault --template DynamicalSystemsGroup/scat-kg-template --private --clone
   cd my-vault
   ```

   The website path ends at the address under **Code**, **HTTPS**; then:

   ```text
   git clone <the address of your new repository>
   cd my-vault
   ```

   ```text
   ls
   ```

   If `ls` shows only `README.md`, the docs have a note for it
   ([If you see only `README.md`](../docs/getting-started.md#1-create-your-private-repository)); say whether it was
   easy to find.
2. Install uv (your call, see "held for you"), close Terminal, open a new window, return to the folder, and set up:

   ```text
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   ```text
   cd my-vault
   ```

   ```text
   uv sync
   ```
3. Run the first check, and the same check in the REPL (`exit()` leaves it):

   ```bash
   uv run scat check
   ```

   ```text
   uv run python
   ```

   ```python
   import scat_kg
   scat_kg.check()
   ```
4. Obsidian: choose **Open folder as vault**, pick `my-vault`, open a page in `narrative` and click its links.
5. Remove the example before any page of your own ([`getting-started.md`, "5. Start your own
   content"](../docs/getting-started.md#5-start-your-own-content)):

   ```text
   git rm -r affordance concern group narrative technology
   uv run scat check
   ```

   ```text
   git commit -m "Remove the example"
   ```
6. Code one narrative from notes of your own, by [`coding.md`, "A narrative, start to
   finish"](../docs/coding.md#a-narrative-start-to-finish), steps 1 to 5, with the REPL or the CLI as you prefer. Fix
   each problem from its message.
7. In Obsidian, open your narrative and look at its Outgoing links panel. With its `Edges told` table, those are its
   fingerprint (step 5 of the same section; without a narrative name, `uv run scat fingerprint` shows every narrative; docs fix 1).
8. Set the narrative to `done` (step 6 of the same section).

**Done.**
- GitHub shows a **Private** badge on the repository.
- `uv run scat check` prints `no problems` on the untouched example, and again after the example is removed.
- The Outgoing links panel lists the nodes your narrative links, and its table lists the edges it tells.
- `scat status` lists the narrative as `done`; the whole-vault check shows no errors.

**Record.** Which path you took; whether the docs let you find the solo trial as one run; any sign-in prompt the docs did not prepare you for; how long `uv sync` took; what the
uv installer's closing message said; what Obsidian showed on first open (any prompt about plugins); each message you
fixed and whether its `Fix:` line was enough; anything you guessed.

**Resume.** In a new Terminal window: `cd my-vault`, then `uv run scat check`, then `git status`. A narrative at
`done` means you are past step 8; `no problems` with no pages of your own means you are before step 6.

## J3 Decide

**Enter.** [`flow.md`](../docs/flow.md#the-steps), the steps table, step 3, and the sentence after it about following through on commitments.

**Steps.**
1. Read the whole table, steps 1 to 10, and what each depends on.
2. Decide whether to use SCAT to organise a facilitated elicitation, and on what.

**Done.** You can state yes or no, and for yes, the elicitation you will run and which of steps 4 to 10 you now
expect to do.

**Record.** Whether the page gave you enough to decide; any step you could not place.

**Resume.** Nothing to resume; reopen `flow.md`.

## J4 Set terms

**Enter.** [`data-and-consent.md`](../docs/data-and-consent.md#the-choices), "The choices", then its [Before you
start](../docs/data-and-consent.md#before-you-start) checklist.

**Steps.**
1. Answer each of the nine choices for your elicitation: collection, storage, consent, use of contributions, AI,
   release, licence, rights holders, and commitments to participants.
2. Write the answers down in a plain text file outside the vault. Tick the checklist as you go.

**Done.** The nine "Before you start" boxes are ticked and each answer is written down, including the AI answer
(it decides whether the chat path is open to you) and the release, licence and rights answers (J10 uses them).

**Record.** Any choice the page did not let you answer; any term used before it was defined; anywhere it gave legal
advice or made a choice for you.

**Resume.** Open your answers file. Redo from the first unticked box.

## J5 Set up

**Enter.** [`getting-started.md`](../docs/getting-started.md#1-create-your-private-repository), steps 1 to 4, for your
**real** repository, with a name of your own in place of `my-vault`. Step 5, removing the example, waits until the
plan is done (J6), as [planning](../docs/planning.md#groups-and-the-cap) says.

**Steps.**
1. Create it **private** from `scat-kg-template`, and clone it, as in J2 step 1 with your name.
2. `uv` is already installed from J2; open a new Terminal window, `cd` into your folder and run `uv sync`, then
   `uv run scat check`, as in J2 steps 2 and 3.
3. Open the folder in Obsidian (version 1.9 or later) as in J2 step 4.
4. Keep the example for now: it is the model you plan with in J6, and it fills the cap of 3 groups that J6 uses.

**Done.** A **Private** repository on GitHub; a working `scat_kg` (the REPL's `scat_kg.check()` and the CLI's
`uv run scat check` both print `no problems` on the example); the folder open as a vault in Obsidian. Now delete the throwaway repository from J2 (GitHub, **Settings**, **Delete this repository**; your action).

**Record.** Anything the docs left unsaid that the J2 pass had not already found; whether the second pass was easier.

**Resume.** `cd` into your folder, `uv run scat check` prints `no problems`, `git status` is clean, and the vault is
open in Obsidian with the example in it.

## J6 Plan

**Enter.** [`planning.md`](../docs/planning.md).

**Steps.**
1. Read [Two kinds of session](../docs/planning.md#two-kinds-of-session) and [Groups and the
   cap](../docs/planning.md#groups-and-the-cap); open `scat.toml` and read the cap.
2. See the cap work, as the page shows. The example vault holds three groups and its cap is 3, so this command is
   refused and creates nothing:

   ```text
   uv run scat stub --type group harbour-crews
   ```

   The page gives the message; yours should say the vault is at its cap of 3 groups, name `SCAT-CAP`, and carry a
   `Fix:` line. Then run `git status`: nothing should have changed.
3. Plan at least one session for scenarios and one for architectures: who takes part, the groups (by role, within the
   cap), the participation terms from J4, the order, and how the notes will be kept (a note-taker for each session).
4. Save the plan as `plan.txt` in your vault folder, outside the page folders, as the page says. It is not a SCAT
   page and the check does not read it.
5. The plan is done, so clear the example, as [`getting-started.md`, "5. Start your own
   content"](../docs/getting-started.md#5-start-your-own-content) says (as in J2 step 5), and commit it:

   ```text
   git rm -r affordance concern group narrative technology
   uv run scat check
   git commit -m "Remove the example"
   ```

**Done.** The cap message appeared as the page shows and nothing was created; `plan.txt` names the sessions, the
groups within the cap, the participation terms and how the notes are kept; nothing in it ranks or votes on anything;
the example is removed and committed, and `uv run scat check` prints `no problems`.

**Record.** Any instruction you could not follow; whether the cap message matched the page's; anywhere the music
language hid an instruction.

**Resume.** `plan.txt` exists in the vault folder. If not, start at "Planning" again. `git log --oneline` shows
"Remove the example" once step 5 is done; if the example is still there, do step 5.

## J7 Capture

**Enter.** [`facilitate-scenarios.md`](../docs/facilitate-scenarios.md), then
[`facilitate-architectures.md`](../docs/facilitate-architectures.md).

**Steps.** You are not running a workshop. Read each guide as a facilitator would, then write, in plain sentences
outside the vault, field notes of your own, in the shape each guide's [Take the notes into a narrative
page](../docs/facilitate-scenarios.md#take-the-notes-into-a-narrative-page) gives: one scenario and one architecture,
each headed by the group, never a name, with no `[[link]]` yet. Mark each past, future or mixed, using the [phrase
list](../docs/facilitate-scenarios.md#past-or-future-one-at-a-time).

**Done.** You hold field notes for one scenario and one architecture, each marked past, future or mixed, in the
guides' shape. Making the narrative page is the last step of each guide and the first step of J8; do it at either
point, and record which.

**Record.** Anything that asked you to rank, vote or adjudicate; any term used before it was defined.

**Resume.** Find your two sets of field notes. If missing, start at the first guide.

## J8 Code

**Enter.** [`coding.md`](../docs/coding.md#where-narratives-and-their-edges-come-from), "Where narratives and their
edges come from", then [A narrative, start to finish](../docs/coding.md#a-narrative-start-to-finish) and [The
operations](../docs/coding.md#the-operations), where each step shows the REPL spelling and the CLI spelling together.
For exact forms: [`reference/api.md`](../docs/reference/api.md) and [`reference/cli.md`](../docs/reference/cli.md).

**Steps.**
1. Half one, the REPL: code your **scenario**. Start the REPL and import the package once:

   ```text
   uv run python
   ```

   ```python
   import scat_kg
   ```

   Make the narrative page (type `narrative`), write the account in Obsidian with a `[[link]]` wherever it names a
   node, set `kind`, `timeframe` and `status: draft`, record each edge it tells, and make the missing node pages with
   `scat_kg.stub_links()`. After each step, check the page, then its neighbourhood. Fix each problem from its message.
2. Half two, the CLI: code your **architecture**, the same way, with `scat` commands. Make the missing node pages:

   ```bash
   uv run scat stub-links
   ```

3. In Obsidian, open each narrative as you go and read it against your field notes. Set each page to `done` only when
   you judge both things: the account matches your notes, and the coding is a correct use of SCAT. The tool checks
   structure only.
4. See the machine form once ([`reference/cli.md`, "Machine-readable
   output"](../docs/reference/cli.md#machine-readable-output)):

   ```text
   uv run scat check --json
   ```

**Done.**
- Every message names the file, the rule and a fix, and you can do the `Fix:` line literally.
- At least one problem occurred and you fixed it from its message alone.
- The REPL and the CLI gave the same messages for the same operation.
- Each edge is a row of its narrative's `Edges told` table, and you wrote no node page by hand.
- Both narratives are `done`, and the whole-vault check shows no errors.
- The `--json` command prints one JSON document, whose first field is `schema_version`, and nothing else.

**Record.** The exact call or command, the message, and whether `Fix:` was enough; every guess; any message that
differed between the REPL and the CLI; any command in the reference that did not behave as shown.

**Resume.** Run `uv run scat status` for each page's status and `uv run scat check`. Half one is finished when the
scenario is `done`; half two when the architecture is.

## J9 Analyse

**Enter.** [`analysis.md`](../docs/analysis.md).

**Steps.**
1. Check the whole vault is clean, and your narratives are `done`, as [Before you trust a
   view](../docs/analysis.md#before-you-trust-a-view) says: `uv run scat check`.
2. Open `analysis.ipynb` in the vault and run all cells. The command is in
   [analysis](../docs/analysis.md#the-notebook) (docs fix 2) and the template's README:

   ```text
   uv run jupyter lab analysis.ipynb
   ```

   In the window it opens, choose **Run**, then **Run All Cells**. Every cell should end without an
   `AssertionError`. Headless, with no browser session, the page also gives
   `uv run jupyter nbconvert --to html --execute analysis.ipynb --output-dir executed`, then `open executed/analysis.html`.
3. Generate the four views with the CLI and the REPL. These are
   [analysis's own forms](../docs/analysis.md#the-notebook); use your own narrative and node names in place of
   the page's `groups-under-a-cap-pitch` and `anonymity`:

   ```text
   uv run scat fingerprint <your-narrative>
   uv run scat edges holds
   uv run scat layered
   uv run scat trace <your-node> --direction up
   uv run scat export-edges --out exports
   ```

   ```python
   import scat_kg
   scat_kg.fingerprint("<your-narrative>")
   scat_kg.edge_table("holds")
   scat_kg.layered()
   scat_kg.trace("<your-node>", "up")
   ```
4. Interpret the views: what do they say about your groups, concerns, affordances and technologies? If a view sends
   you back to your field notes, go round the coding loop once more (J8) before you go on.

**Done.** The notebook ran to the end; the fingerprint, edge table, layered view and trace each printed without an
error; the three edge tables exist in `exports/` (the notebook writes them there too; git ignores the folder, so
`git add .` in J10 does not commit them); you can say, in your own
words, what one view told you and whether it sent you back. The page does not tell you a narrative is better, and
you did not read it that way.

**Record.** How you opened the notebook and whether the page said how; whether the commands matched the page; whether
[`coding.md`](../docs/coding.md#5-a-link-without-a-row), step 5, and `analysis.md` both give `uv run scat fingerprint`
(docs fix 1); what the views read like.

**Resume.** `exports` exists with files in it, and `uv run scat check` shows no errors. The notebook can be run
again at any time: it writes nothing into your pages.

## J10 Hand over

**Enter.** [`coding.md`](../docs/coding.md#reaching-a-clean-whole-vault-check), "Reaching a clean whole-vault check",
then [Commit and push](../docs/coding.md#commit-and-push) and [Lock a version](../docs/coding.md#lock-a-version); and
[`flow.md`](../docs/flow.md#the-steps), step 10; and your J4 release, licence and rights answers.

**Steps.**
1. Reach a clean whole-vault check with the index pages generated:

   ```text
   uv run scat check
   uv run scat index
   uv run scat check
   ```
2. Open the vault in Obsidian and look at it as [`coding.md`, "Look at it in
   Obsidian"](../docs/coding.md#look-at-it-in-obsidian) says: links, Backlinks, Outgoing links, graph view (it draws
   every page as a dot, narratives included) and the index pages. Open a concern and read its Backlinks panel.
3. Read `git status`, then commit and push:

   ```text
   git status
   git add .
   git commit -m "Code the notes from my first session"
   git push
   ```
4. Take a hand-over case: a contract delivery, a paper submission, or a class project hand-in. Decide, as the coder,
   whether the model is a good representation of your field notes. If so, lock the version and push the tag:

   ```text
   git tag v1
   git push origin v1
   ```

   Then see which commit the tag pins, and that GitHub holds the same one
   ([See which commit a tag pins](../docs/coding.md#see-which-commit-a-tag-pins), docs fix 4):

   ```text
   git rev-parse v1^{commit}
   git show --stat v1
   git ls-remote --tags origin v1
   ```

   The first and third print the same hash.
5. Hand it over to the recipient the case names, at the release level your J4 answers set.

**Done.** The final whole-vault check ends `0 errors`, with the five index pages unchanged or created; `git status`
before `git add .` listed only changes you meant; the commit and the tag `v1` are on GitHub in a repository that is
still private; and you can name the tag, the commit it pins and the recipient. In Obsidian, a concern's Backlinks panel
lists the narratives that name it ("who tells this?"), with no second list. Which groups hold it is read from the
`Edges told` tables and the views, not from Backlinks.

**Record.** The tag, the commit it pins and the recipient; any push or sign-in error, with its full text; how you found the commit the tag
pins and whether the docs showed it; whether the page told you a hand-over is a release after which work can
continue (`flow.md` says "release").

**Resume.** `git status`, then `git log --oneline` and the repository's tags on GitHub. A pushed `v1` means you are
done; a clean check with no commit means redo from step 3.

---

## When you are done

Judge, in your own words: is the documentation clear and navigable, and are the journeys clear? List each stage you
flagged, with your notes. The fixes go to `dev` and the candidate is refreshed. Then, when you accept, you merge the
release pull requests the ACE has opened from `dev` to `main`, as merge commits: your merges are the acceptance.
