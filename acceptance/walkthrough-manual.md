# UA-M walkthrough, manual path: the chief engineer's script

You run the journey J1 to J10 yourself, from the documentation, on the candidate, without help. This script does not
teach it. For each stage it gives where to enter, the steps, what "done" looks like, what to record, and where to
resume. The docs are the instructions; this script only points at them. The chat path has its own script,
`walkthrough-chat.md`.

**Pass (MISSION.md, UA-M):** you complete J1 to J10 on both paths from the docs without help, and judge the
documentation clear and navigable and the journeys clear. Anything you flag is fixed on `dev`, the candidate is
refreshed, and you resume from the affected stage.

## How to split the walk into sittings and resume

- **Start page:** the Pages preview, <https://dynamicalsystemsgroup.github.io/scat-kg-tools/>, marked pre-release.
  Follow the docs' own links from there. Do not open `src/` or `tests/` to find an answer.
- **Sittings.** Stop only at the end of a stage; J8 also has a stop between its REPL half and its CLI half.

| Sitting | Stages | You are done when |
|---|---|---|
| A. Solo trial | J1, J2 | one narrative of your own is `done` in a throwaway repository |
| B. Terms and set-up | J3, J4, J5 | your real private repository is cloned, clean and open in Obsidian |
| C. Plan and capture | J6, J7 | a plan and your field notes for one scenario and one architecture exist |
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

**Enter.** Open <https://dynamicalsystemsgroup.github.io/scat-kg-tools/> (`index.md`, the home page).

**Steps.**
1. Before you read "Why it is called SCAT", say what style or reference the page evokes, and write it down.
2. Read the page, then look at the navigation.

**Done.** You can say in a sentence what SCAT turns into what; what S, C, A and T stand for; and where to go next. The
navigation lists Home, The flow, Data, rights and consent, Getting started, Planning, Facilitating, Coding, Coding in a
chat, Coding in an IDE, Analysis and Reference.

**Record.** The style you named, before the explanation. Any broken web link (page and its text), broken image, or anything
that blocked an instruction.

**Resume.** Nothing to resume; reopen the home page.

## J2 Try

**Enter.** `flow.md`, "First try" (steps 5, 2 and 8, in that order), then `getting-started.md`, "1. Create your private
repository". Use a **throwaway** repository, named `my-vault` as the docs do. Delete it after J5.

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

   If `ls` shows only `README.md`, the docs have a note for it; say whether it was easy to find.
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
5. Remove the example before any page of your own (`getting-started.md`, "5. Start your own content"):

   ```text
   git rm -r affordance concern group narrative technology
   uv run scat check
   ```

   ```text
   git commit -m "Remove the example"
   ```
6. Code one narrative from notes of your own, by `coding.md`, "A narrative, start to finish", steps 1 to 6, with the REPL
   or the CLI as you prefer. Fix each problem from its message.
7. In Obsidian, open your narrative and look at its Outgoing links panel. With its `Edges told` table, those are its
   fingerprint.
8. Set the narrative to `done` (step 6 of the same section).

**Done.**
- GitHub shows a **Private** badge on the repository.
- `uv run scat check` prints `no problems` on the untouched example, and again after the example is removed.
- The Outgoing links panel lists the nodes your narrative links, and its table lists the edges it tells.
- `scat status` lists the narrative as `done`; the whole-vault check shows no errors.

**Record.** Which path you took; any sign-in prompt the docs did not prepare you for; how long `uv sync` took; what the
uv installer's closing message said; what Obsidian showed on first open (any prompt about plugins); each message you
fixed and whether its `Fix:` line was enough; anything you guessed.

**Resume.** In a new Terminal window: `cd my-vault`, then `uv run scat check`, then `git status`. A narrative at
`done` means you are past step 8; `no problems` with no pages of your own means you are before step 6.

## J3 Decide

**Enter.** `flow.md`, the steps table, step 3, and the sentence after it about following through on commitments.

**Steps.**
1. Read the whole table, steps 1 to 10, and what each depends on.
2. Decide whether to use SCAT to organise a facilitated elicitation, and on what.

**Done.** You can state yes or no, and for yes, the elicitation you will run and which of steps 4 to 10 you now
expect to do.

**Record.** Whether the page gave you enough to decide; any step you could not place.

**Resume.** Nothing to resume; reopen `flow.md`.

## J4 Set terms

**Enter.** `data-and-consent.md`, "The choices", then its "Before you start" checklist.

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

**Enter.** `getting-started.md`, steps 1 to 5, for your **real** repository, with a name of your own in place of
`my-vault`.

**Steps.**
1. Create it **private** from `scat-kg-template`, and clone it, as in J2 step 1 with your name.
2. `uv` is already installed from J2; open a new Terminal window, `cd` into your folder and run `uv sync`, then
   `uv run scat check`, as in J2 steps 2 and 3.
3. Open the folder in Obsidian (version 1.9 or later) as in J2 step 4.
4. Remove the example as in J2 step 5.

**Done.** A **Private** repository on GitHub; a working `scat_kg` (the REPL's `scat_kg.check()` and the CLI's
`uv run scat check` both print `no problems`); the folder open as a vault in Obsidian; no example pages; the removal
committed. Now delete the throwaway repository from J2 (GitHub, **Settings**, **Delete this repository**; your action).

**Record.** Anything the docs left unsaid that the J2 pass had not already found; whether the second pass was easier.

**Resume.** `cd` into your folder, `uv run scat check` prints `no problems`, `git status` is clean, and the vault is
open in Obsidian.

## J6 Plan

**Enter.** `planning.md`.

**Steps.**
1. Read "Two kinds of session" and "Groups and the cap"; open `scat.toml` and read the cap.
2. Plan at least one session for scenarios and one for architectures: who takes part, the groups (by role, within the
   cap), the participation terms from J4, and the order.
3. Save the plan as `plan.txt` in your vault folder, as the page says.

**Done.** `plan.txt` names the sessions, the groups within the cap, and the participation terms. Nothing in it ranks
or votes on anything.

**Record.** Any instruction you could not follow; anywhere the music language hid an instruction.

**Resume.** `plan.txt` exists in the vault folder. If not, start at "Planning" again.

## J7 Capture

**Enter.** `facilitate-scenarios.md`, then `facilitate-architectures.md`.

**Steps.** You are not running a workshop. Read each guide as a facilitator would, then write, in plain sentences
outside the vault, field notes of your own: one scenario and one architecture, told by groups and not individuals.
Mark each past, future or mixed, using the guides' phrase list.

**Done.** You hold field notes for one scenario and one architecture, each marked past, future or mixed, and no
vault page for them yet.

**Record.** Anything that asked you to rank, vote or adjudicate; any term used before it was defined.

**Resume.** Find your two sets of field notes. If missing, start at the first guide.

## J8 Code

**Enter.** `coding.md`, "Where narratives and their edges come from", then "The operations", where each step shows
the REPL spelling and the CLI spelling together. For exact forms: `reference/api.md` and `reference/cli.md`.

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
4. See the machine form once (`reference/cli.md`, "Machine-readable output"):

   ```text
   uv run scat check --json
   ```

**Done.**
- Every message names the file, the rule and a fix, and you can do the `Fix:` line literally.
- At least one problem occurred and you fixed it from its message alone.
- The REPL and the CLI gave the same messages for the same operation.
- Each edge is a row of its narrative's `Edges told` table, and you wrote no node page by hand.
- Both narratives are `done`, and the whole-vault check shows no errors.
- The `--json` command prints one JSON document, starting with `schema_version`, and nothing else.

**Record.** The exact call or command, the message, and whether `Fix:` was enough; every guess; any message that
differed between the REPL and the CLI; any command in the reference that did not behave as shown.

**Resume.** Run `uv run scat status` for each page's status and `uv run scat check`. Half one is finished when the
scenario is `done`; half two when the architecture is.

## J9 Analyse

**Enter.** `analysis.md`. Run `uv run scat index` first if you added pages since it last ran.

**Steps.**
1. Check the whole vault is clean, and your narratives are `done`, as the page's "Before you trust a view" says.
2. Open `analysis.ipynb` in the vault and run all cells; the page does not say with what, so record what you used.
3. Generate the views with the REPL and the CLI. These are the docs' forms; use your own names where a page or node
   is named:

   ```text
   uv run scat layered
   ```

   ```text
   uv run scat edges holds
   ```

   ```text
   uv run scat export-edges --out edge-tables
   ```

   ```python
   scat_kg.layered()
   ```

   ```python
   scat_kg.edge_table("holds")
   ```
4. Interpret the views: what do they say about your groups, concerns, affordances and technologies? If a view sends
   you back to your field notes, go round the coding loop once more (J8) before you go on.

**Done.** The notebook ran to the end; the layered view and the three edge tables exist; you can say, in your own
words, what one view told you and whether it sent you back. The page does not tell you a narrative is better, and
you did not read it that way.

**Record.** How you opened the notebook; whether the commands matched the page; whether `coding.md` ("That view is not
one of the `scat` commands yet") and `analysis.md` (a `fingerprint` command) agree; what the views read like.

**Resume.** `edge-tables` exists with files in it, and `uv run scat check` shows no errors.

## J10 Hand over

**Enter.** `coding.md`, "Reaching a clean whole-vault check", then "Commit and push" and "Lock a version"; and your
J4 release, licence and rights answers.

**Steps.**
1. Reach a clean whole-vault check with the index pages generated:

   ```text
   uv run scat check
   uv run scat index
   uv run scat check
   ```
2. Open the vault in Obsidian and look at it as `coding.md`, "Look at it in Obsidian", says: links, Backlinks,
   Outgoing links, graph view (it draws every page as a dot, narratives included) and the index pages.
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
5. Hand it over to the recipient the case names, at the release level your J4 answers set.

**Done.** The final whole-vault check ends `0 errors`, with the five index pages unchanged or created; `git status`
before `git add .` listed only changes you meant; the commit and the tag `v1` are on GitHub in a repository that is
still private; and you can name the tag, the commit it pins and the recipient. Obsidian answers "who holds this
concern?" from its Backlinks panel, with no second list.

**Record.** The tag, the commit it pins and the recipient; any push or sign-in error, with its full text; whether
the page told you a hand-over is a release after which work can continue.

**Resume.** `git status`, then `git log --oneline` and the repository's tags on GitHub. A pushed `v1` means you are
done; a clean check with no commit means redo from step 3.

---

## When you are done

Judge, in your own words: is the documentation clear and navigable, and are the journeys clear? List each stage you
flagged, with your notes. The fixes go to `dev` and the candidate is refreshed. Then, when you accept, you merge the
release pull requests the ACE has opened from `dev` to `main`, as merge commits: your merges are the acceptance.
