# UA-M walkthrough: the chief engineer's script

You do the journey yourself, from the documentation, without help. This script does not teach it. For each stage it
says where to enter, what "done" looks like, what to note if it fails, and gives a short checklist. The docs are the
instructions; this script only points at them.

**Pass (MISSION.md, UA-M):** you complete J1 to J7 from the docs without help, and judge the documentation clear and
navigable and the journey clear. Anything you flag is fixed on `dev`, the candidate is refreshed, and you resume from
the affected stage.

## How to use it

- **Start page:** the Pages preview, <https://dynamicalsystemsgroup.github.io/scat-kg-tools/>. Follow the docs'
  own links from there. Do not open `src/`, `tests/` or this script's source to find an answer.
- **Stop and resume.** Each stage ends in a state you can stop in. To resume, run the stage's "Resume check" and read
  what it says.
- **Your notes.** Send your notes on each stage as plain text. There is no required format.
- **Failing.** Where a stage fails, do not work around it. Note the page, the exact step, the exact text you typed,
  and the exact output. Say what you expected from the docs. Then either stop or carry on if you can. The fix is the
  team's job, not yours.
- **Your own elicitation.** Choose a small topic of your own for stages 5 to 9: at least one scenario and one
  architecture. Use your own words and group names, not the worked example's.

## Gaps held for you

1. **Pages preview.** The preview is live (deployed by the ACE). The ACE rechecks it before your sitting.
2. **uv install (D-040, D-041).** The agents did not run uv's downloaded installer script
   (`curl -LsSf https://astral.sh/uv/install.sh | sh`). Running a downloaded installer needs your explicit
   permission, so the automated user tests started with `uv` already on the path. **Stage 3 is the first time that
   command is exercised for real.** It is your call to run it. The step is untested by the team.
3. **Obsidian.** The automated tests checked the Obsidian steps only through the files. **Stages 4 and 9 are the
   first time Obsidian opens the vault.**

## Stages at a glance

| Stage | Journey | Where you start |
|---|---|---|
| 1 | J1 Find | The Pages preview, home |
| 2 | J2 Create | Getting started, step 1 |
| 3 | J3 Set up | Getting started, steps 2 and 3 |
| 4 | J3 Obsidian, clear the example | Getting started, steps 4 and 5 |
| 5 | J4 Plan, J5 Capture | Planning, then the facilitation guides |
| 6 | J6 Code, the REPL | Coding, "The operations" |
| 7 | J6 Code, the CLI | Coding, same page |
| 8 | J7 Finish | Coding, "Reaching a clean whole-vault check" |
| 9 | J7 Finish in Obsidian | Coding, "Look at it in Obsidian" |

---

## Stage 1. Find (J1)

**Entry point.** Open <https://dynamicalsystemsgroup.github.io/scat-kg-tools/> in a browser. This is the home page.

**What you do.** Read the home page. Look at the navigation. You are checking that a newcomer would understand what
SCAT is for and how to start, without anyone telling them. Before you read the "Why it is called SCAT" section, say what style or reference the
page evokes, and note it; the section explains the name, so answer first, or stop reading at it until you have. The
opening of the page already uses band language. That is fine and part of what you should notice.

**Done looks like.**

- You can say in a sentence what SCAT turns into what (a facilitated discussion into a graph you can walk through).
- You can say what S, C, A and T stand for.
- You can see the top "Your next step" box, and it sends you to Getting started.
- The navigation lists Home, Getting started, Planning, Facilitating (Scenarios, Architectures), Coding and
  Reference (Python API, CLI).

**If it fails.** Note what you expected to find and where you looked. Note any dead link (page and link text), any
broken image, and anything on the page that blocked an instruction.

**Resume check.** None. Reopen the home page.

**Checklist.**

- [ ] The Pages preview URL loaded.
- [ ] I understood what SCAT is for.
- [ ] I could see how to start.
- [ ] I followed the "Your next step" link to Getting started.

---

## Stage 2. Create your repository (J2)

**Entry point.** [Getting started](https://dynamicalsystemsgroup.github.io/scat-kg-tools/getting-started/), "1. Create your private repository". On the live
site this is the Getting started page, step 1.

**What you do.** Make a **real** private repository from `scat-kg-template`, through one of the two documented paths,
and clone it. Use a throwaway name you will delete afterwards. The page shows both paths; pick the one a facilitator
would. The website path is:

1. Open <https://github.com/DynamicalSystemsGroup/scat-kg-template>.
2. Choose **Use this template**, then **Create a new repository**.
3. Set the name and set the visibility to **Private**.
4. Create it, then copy the address under **Code**, **HTTPS**.

The `gh` path is one command, and it also clones:

```text
gh repo create my-vault --template DynamicalSystemsGroup/scat-kg-template --private --clone
cd my-vault
```

Or, after the website path:

```text
git clone <the address of your new repository>
cd my-vault
```

Then:

```text
ls
```

**Done looks like.**

- GitHub shows your new repository with a **Private** badge.
- You are in the cloned folder in Terminal, and `ls` lists `scat.toml` and folders such as `concern` and `class`.
- If `ls` shows only `README.md`, the docs have a note for that (the preview's default branch is `dev`, and `main`
  is a stub). Note that you hit it; it is a finding if it was not obvious from the page.

**If it fails.** Note whether the visibility was a clear choice on the creation page, and whether the docs said it
would be. Note any sign-in prompt on the first clone and whether the docs prepared you for it. Note the exact
error text and which path you used. Note whether the template's own README (which you see on GitHub) agreed with the
docs page.

**Resume check.** In Terminal: `cd my-vault`, then `ls`. You should see `scat.toml`.

**Checklist.**

- [ ] I created the repository through a documented path.
- [ ] It is private.
- [ ] I cloned it.
- [ ] `ls` shows `scat.toml`.
- [ ] Every step was in the docs; I guessed nothing.

---

## Stage 3. Install and set up (J3)

**Entry point.** [Getting started](https://dynamicalsystemsgroup.github.io/scat-kg-tools/getting-started/), "2. Install what you need", then "3. Run your first
check". Start in Terminal, in a new window with no tools set up beforehand if you can. A clean user account is the
best test.

**Held gap.** This is where the uv installer runs (see "Gaps held for you"). The command is the docs' command,
unchanged. You decide whether to run it:

```text
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then, as the docs say: close Terminal, open a new Terminal window, and go back to your folder.

```text
cd my-vault
uv sync
uv run scat check
```

**Done looks like.**

- After the new window, `uv` is found. If Terminal says `uv: command not found`, the docs say to read the
  installer's closing message, follow it and open another new window. Follow only that.
- `uv sync` downloads Python and the tools and finishes without an error. This needs a connection and takes a minute
  or two.
- `uv run scat check` ends with:

```text
0 errors, 1 warning
```

The one warning is `SCAT-CONFLICT-BOTH` on the worked example. The docs say it may stay.

- In the REPL, the same result. Start it, then type the two lines (`>>>` is the prompt; `exit()` leaves it):

```text
uv run python
import scat_kg
scat_kg.check()
```

**If it fails.** Note which command, the full output, and whether the page told you what to do next. Note how long
`uv sync` took. If the installer changed your shell setup, note what its closing message said and whether the docs
matched it. Note if you needed to know anything the page did not say.

**Resume check.** In a new Terminal window: `cd my-vault`, then `uv run scat check`. It should end `0 errors, 1 warning`.

**Checklist.**

- [ ] I decided about the uv installer and ran it (or noted that I did not).
- [ ] `uv sync` finished cleanly.
- [ ] `uv run scat check` ended `0 errors, 1 warning`.
- [ ] The REPL gave the same result.
- [ ] I did not need to read anything outside the docs.

---

## Stage 4. Obsidian, and clearing the example (J3)

**Entry point.** [Getting started](https://dynamicalsystemsgroup.github.io/scat-kg-tools/getting-started/), "4. Open the vault in Obsidian", then "5. Start your
own content". This is the first real use of Obsidian in the acceptance.

**Order.** The docs say to remove the example before you code your own notes, and that you may keep it open while you
read the other guides and remove it at any time. This script follows the docs' step order, so you clear it here. You
may instead do it after stage 5 and before stage 6; the docs allow either. Do not start stage 6 with the example still
in the vault.

**What you do.** Install Obsidian if you do not have it. Choose **Open folder as vault**, pick `my-vault`, and open a
page in the `concern` folder. Click a link. Then, in Terminal in your vault folder, remove the example as the page
says. These are the docs' commands:

```text
git rm -r addresses affordance architecture-coded architecture-raw attributes concern heldby scenario-coded scenario-raw stakeholder-group technology
uv run scat index
uv run scat check
git add .
git commit -m "Remove the example"
```

**Done looks like.**

- Obsidian opens the folder as a vault with no complaint, and you can follow links between pages.
- `uv run scat index` prints `changed` for each of the seven class pages.
- `uv run scat check` prints:

```text
no problems
```

- `git commit` succeeds. The vault is empty and clean.

**If it fails.** Note what Obsidian showed on first open: any prompt (for example about trusting the vault's
plugins or settings), any page that looked wrong, any link that did not follow. Note whether the page templates for
the four kinds of record were there as the docs say. For a command, note the full output.

**Resume check.** `uv run scat check` should print `no problems`.

**Checklist.**

- [ ] Obsidian opened the folder as a vault.
- [ ] I clicked through at least one link.
- [ ] I removed the example, and `check` printed `no problems`.
- [ ] I committed the removal.

---

## Stage 5. Plan and capture (J4, J5)

**Entry point.** [Planning](https://dynamicalsystemsgroup.github.io/scat-kg-tools/planning/), then [Facilitating scenarios](https://dynamicalsystemsgroup.github.io/scat-kg-tools/facilitate-scenarios/) and
[Facilitating architectures](https://dynamicalsystemsgroup.github.io/scat-kg-tools/facilitate-architectures/).

**What you do.** You are not running a real workshop. Read the pages as a facilitator would, and make a small plan
and raw notes of your own:

- From Planning: the sessions (one that elicits scenarios, one that elicits architectures), the groups in each,
  named by role and within the cap, and the Chatham House framing.
- From the two facilitation guides: write one raw scenario and one raw architecture in plain sentences, as they
  would have been told, with groups and no individuals' names.
- Keep the groups to a short list. You will name them again in stages 6 and 7.

You are checking that the pages say what to do, that nothing is ranked, voted on or adjudicated, and that the
"yes, and" and "from this perspective" stance is easy to follow without obscuring an instruction.

**Done looks like.** You hold, on paper or in a file outside the vault: a short plan (sessions, groups within the cap,
the framing line) and the plain-sentence raw notes for one scenario and one architecture. You have not yet made any
pages. Stage 6 does that.

**If it fails.** Note any instruction you could not follow, any term used before it was defined, and any place the
jazz language made an instruction harder to follow. Note anything that asked you to rank or choose between stories or
architectures, because the guides must not.

**Resume check.** Find your plan and raw notes. If you have not written them, start again at Planning.

**Checklist.**

- [ ] I made a plan with groups within the cap.
- [ ] I have raw notes for one scenario and one architecture.
- [ ] No page asked me to rank, vote or adjudicate.
- [ ] No metaphor hid an instruction.

---

## Stage 6. Code in the REPL (J6)

**Entry point.** [Coding](https://dynamicalsystemsgroup.github.io/scat-kg-tools/coding/), "Where raw and coded pages come from" and "The operations, in the order
you meet them". Every step shows the REPL spelling first and the CLI spelling beside it.

**What you do.** Code your **scenario** in the Python REPL. Start it:

```text
uv run python
```

Then `import scat_kg` once. In the REPL, with your own page and group names, do what the page shows: create the raw
page (`scat_kg.stub`, type `scenario-raw`) and its coded page (type `scenario-coded`), write your notes into the raw
page and the links into the coded page, then `scat_kg.stub_pair(...)` for each pair you find (the pair order is group
then concern, concern then affordance, affordance then technology), or `scat_kg.stub_links()` after you write the
coded page. Move pages from stub through draft to done with `scat_kg.set_status("<page>", "draft")` and so on. After
each step, `scat_kg.check(...)` the page, then its neighbourhood (`neighborhood=True`). Fix each problem from its
message.

**Done looks like.**

- Every command prints a message that names the file, the rule and a fix. The `Fix:` line is something you can do
  literally.
- The pages exist, with their relation pages. You wrote none of the structure by hand.
- At least one problem occurred and you fixed it from its message alone.
- Your scenario's pages are `done`, and `scat_kg.check()` on the neighbourhood of the coded page shows no errors.

**If it fails.** Note the call you typed, the message, and whether the `Fix:` line was enough. Note any time you
had to guess, or look anywhere other than the coding page and the [Python API reference](https://dynamicalsystemsgroup.github.io/scat-kg-tools/reference/api/).
A message that is correct but unclear is a finding too. Note the status of each page at that moment.

**Resume check.** `uv run scat status` (CLI) lists the pages by status, and `uv run scat check` shows where you are.

**Checklist.**

- [ ] I used the REPL for every operation in this stage.
- [ ] I coded one scenario, raw and coded.
- [ ] I hit at least one message and fixed it from the message alone.
- [ ] Pages moved from stub to draft to done.
- [ ] I did not read `src/` or `tests/`.

---

## Stage 7. Code with the CLI (J6)

**Entry point.** [Coding](https://dynamicalsystemsgroup.github.io/scat-kg-tools/coding/) again, same sections, now the **CLI** spelling beside each REPL step.
For exact forms, [CLI reference](https://dynamicalsystemsgroup.github.io/scat-kg-tools/reference/cli/).

**What you do.** Code your **architecture** with the CLI, from your raw notes. The forms are the docs' forms, with
your own names:

```text
uv run scat stub <name> --type architecture-raw
uv run scat stub <name>-coded --type architecture-coded
uv run scat stub-pair <relation> <first> <second>
uv run scat stub-links
uv run scat set-status <page> draft
uv run scat check <page> --neighborhood
```

Use `addresses` and `attributes` for the relations in an architecture (a coded architecture relates concerns,
affordances and technologies).

**Done looks like.**

- The same kinds of message as stage 6, from the CLI, with the same wording.
- Your architecture's pages exist and are `done` or `draft`, as you judge them.
- You can say whether the REPL and CLI felt equal, with the same messages.

**If it fails.** As in stage 6. Also note any message that differed between the REPL and CLI, and any command in the
CLI reference that did not behave as shown.

**Resume check.** `uv run scat status`, then `uv run scat check`.

**Checklist.**

- [ ] I used the CLI for every operation in this stage.
- [ ] I coded one architecture, raw and coded.
- [ ] The messages matched the REPL's.
- [ ] I fixed each problem from its message.

---

## Stage 8. Clean check, commit, push (J7)

**Entry point.** [Coding](https://dynamicalsystemsgroup.github.io/scat-kg-tools/coding/), "Reaching a clean whole-vault check", then "Commit and push".

**What you do.** The docs' order, in your vault folder:

```text
uv run scat check
uv run scat index
uv run scat check
```

Fix each error from its `Fix:` line until the check ends `0 errors`. Warnings may stay. Then:

```text
git status
git add .
git commit -m "<short description of what you coded>"
git push
```

Replace the placeholder with your own commit message. Read `git status` before you add anything. If git asks who you are, it prints the two
lines to type.

**Done looks like.**

- The final whole-vault `uv run scat check` ends `0 errors`. Warnings may remain.
- `git status` before `git add .` lists only changes you meant.
- `git push` succeeds, and on GitHub your private repository shows the commit.

**If it fails.** Note the check's full output and the one you last fixed. Note any change in `git status` you did not
expect, and any push error with its full text.

**Resume check.** `uv run scat check`, then `git status` and `git log --oneline`.

**Checklist.**

- [ ] The whole-vault check ends `0 errors`.
- [ ] I read `git status` before `git add .`.
- [ ] The commit is on GitHub.
- [ ] The repository is still private.

---

## Stage 9. The graph in Obsidian (J7)

**Entry point.** [Coding](https://dynamicalsystemsgroup.github.io/scat-kg-tools/coding/), "Look at it in Obsidian". Run `uv run scat index` first if you added
pages after the last index.

**What you do.** Open the vault in Obsidian (or reopen it). Follow the page's four items: links, backlinks, graph
view, class pages. Open a concern page and read its Backlinks panel. Open the graph view. Open `class/concerns.md`.
This is also where you judge whether the result reads well in Obsidian, as the mission's definition of good asks.

**Done looks like.**

- A concern page lists, in Backlinks, the pages that point at it (who holds it, what addresses it, which coded pages
  name it).
- The graph view shows your pages as dots and links as lines, with a relation page sitting between a group and a
  concern.
- `class/concerns.md` lists every concern with its description and a link.
- You can answer "who holds this concern?" from Obsidian, without a second list.

**If it fails.** Note what you expected and what Obsidian showed. Note whether the page told you where to click.
Note whether the graph was legible at this size, and any page that looked wrong.

**Resume check.** Reopen the vault in Obsidian and the graph view.

**Checklist.**

- [ ] Obsidian showed backlinks for a concern.
- [ ] The graph view showed my pages and their links.
- [ ] `class/concerns.md` was complete.
- [ ] I could navigate the graph without help.

---

## When you are done

Delete the throwaway repository if you wish (GitHub, repository **Settings**, **Delete this repository**). That is
your action.

Then judge, in your own words: Is the documentation clear and navigable? Is the journey clear? Note each stage you
flagged, with the notes above. The fixes go to `dev`, the candidate is refreshed, and you resume from the affected
stage.
