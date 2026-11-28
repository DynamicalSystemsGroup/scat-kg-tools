# Getting started

!!! tip "Your next step"
    Create your private repository from the template (step 1 below).

## Before you start

- A Mac, and a GitHub account. If you have none, make one at <https://github.com>.
- Terminal. Open it from Applications, then Utilities. Type every command below in Terminal, one at a time, and press
  Return after each.
- [Obsidian](https://obsidian.md), the app you will read the vault in. It is free to install.
- To code in a chat window instead of Terminal, make the repository as step 1 shows, then follow the [chat path](chat-path.md).

SCAT stands for Stakeholder groups, Concerns, Affordances and Technologies: the four node types your notes are coded into. If you have not read what that means, start at the [home page](index.md).

## 1. Create your private repository

Your discussions are your data, so make your repository **private**. A private repository can be seen only by you and
the people you invite. A public one can be read by anyone on the internet, and your notes are about real groups of
people. Both paths below set it for you, and the website path shows it as a choice you confirm.

Pick one path.

**With the GitHub command line, `gh`.** `gh` is installed separately. If you use Homebrew, `brew install gh` installs it. Without Homebrew, use the website path below instead. You also need a one-time `gh auth login`. This creates the repository
and downloads it, in one command. `my-vault` is the name you are choosing for your repository and its folder.

```text
gh repo create my-vault --template DynamicalSystemsGroup/scat-template --private --clone
cd my-vault
```

**On the GitHub website.** No `gh`? Use this path.

1. Sign in to GitHub, then open <https://github.com/DynamicalSystemsGroup/scat-template>. Signed out, GitHub does
   not show **Use this template**.
2. Choose **Use this template**, then **Create a new repository**.
3. Set the name (for example `my-vault`) and set the visibility to **Private**.
4. Create the repository. GitHub shows its page.
5. Find the address: choose the green **Code** button and copy the address under **HTTPS**.

Then download it, using that address. The first time you clone a private repository, GitHub may ask you to sign in:

```text
git clone <the address of your new repository>
cd my-vault
```

Check that you are in the right folder:

```text
ls
```

You should see `scat.toml` in the list, with folders such as `concern` and `narrative`.

!!! note "Your folder name"
    The folder is named after the repository you created. These pages say `my-vault`. If you chose another name,
    use that name wherever you see `my-vault`.

!!! note "If you see only `README.md`"
    The template's working branch is `dev`; `main` holds only a README. If `ls` shows nothing but `README.md`, you are on `main`. Run this, then `ls` again:

    ```text
    git checkout dev
    ```

## 2. Install what you need

You need `git` (you used it above; macOS offers to install it the first time you run it) and `uv`, a tool that
installs the right Python and the SCAT tools for you. Install `uv` once:

```text
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close Terminal and open a new Terminal window. A new window opens in your home folder, not in your vault, so go back to the folder where you cloned it (use the name you chose):

```text
cd my-vault
```

If Terminal now says `uv: command not found`, the installer's closing message tells you how to make `uv` available. Read that message, follow it, and open another new window. You can also run the installer command again.

Run the one setup command. It downloads Python and the SCAT tools from the internet into this folder, so it needs a connection, and it takes a minute or two:

```text
uv sync
```

## 3. Run your first check

Every `uv sync` and `uv run` command in these pages runs inside your vault folder (`my-vault`). If a command misbehaves, check first that Terminal is in that folder.

Run the check from inside your vault folder. It looks at every page and prints what it found, in plain words:

```bash
uv run scat check
```

The template ships with a worked example, so you can see what a vault looks like. A clean result for it is this:

```text
attribution mode: disallowed
no problems
```

That is a pass. A **clean** check prints the vault's attribution mode, then `no problems`. **Errors** block you: a vault with errors is not clean.
**Warnings** do not block you. They are to-dos, such as a draft page that still needs a sentence.

The check looks at structure only: that each page has what its type needs, that links point at pages that exist,
and that names and counts follow the rules. It does not judge what your notes say. Where concerns pull against each
other, or match, or leave a gap, that is for analysis later, after the check passes and a coder has signed off the
content. You can record that two concerns pull apart with a relationship annotation, a plain line in the body of one
concern with a link to the other; the tool gives it no meaning.

Run the check again after every change you make.

### The same check in the Python REPL

Prefer working interactively? The REPL (a Python session where you type one line at a time) does the same check.
Start it with `uv run python`. The prompt changes to `>>>`. Type the lines below one at a time, and the result prints beneath them. Type `exit()` to leave.

```python
import scat_tools
scat_tools.check()
```

It prints the same text as `uv run scat check`:

```text
attribution mode: disallowed
no problems
```
 Every `scat` command has a twin in the REPL; the
[reference](reference/cli.md) lists them.

### Two things the tools do that may surprise you

`scat.toml` is required. It sits in the vault folder and holds two keys: `stakeholder_group_cap`, the cap on groups, and
`attribution`, the vault's attribution mode (`required`, `optional` or `disallowed`). The template sets the cap to 6 and the
mode to `disallowed`; [Planning](planning.md#choose-the-attribution-mode) says how to choose yours. The person who set up your tools changes these two keys (you, if you set them up
yourself). If either key is missing, the check reports an error (`SCAT-CAP-CONFIG` or `SCAT-MODE-CONFIG`). If the whole file is missing, you are probably in the wrong folder, or the file
was deleted. In a wrong (empty) folder the check ends with `1 error, 0 warnings`:

```text
attribution mode: not declared
error [SCAT-CAP-CONFIG] scat.toml field `stakeholder_group_cap`: the file is missing
  Fix: add the line `stakeholder_group_cap = <number you choose>` (author) in scat.toml; choose a whole number of 1 or more (the vault has 0 group pages now)
1 error, 0 warnings
```

Do not run `scat index` to fix this: it would write five files into the wrong folder. `cd` into your vault folder instead.

`scat index` writes the index pages, one Obsidian Base for each type, in the `index` folder, and only the ones that are missing. It never rewrites one. The template already holds all five, so on the untouched example every line says `unchanged`, and that is correct:

```bash
uv run scat index
```

```text
unchanged index/group.base
unchanged index/concern.base
unchanged index/affordance.base
unchanged index/technology.base
unchanged index/narrative.base
```

## 4. Open the vault in Obsidian

Open Obsidian (version 1.9 or later, which the index pages need), choose **Open folder as vault**, and pick your
folder (`my-vault`). Open a page in the `narrative` folder and click its links: you are walking the graph. Open a file in
the `index` folder to see every page of one type. Create pages with `scat stub`.
[Coding](coding.md#where-narratives-and-their-edges-come-from) says more.

## 5. Start your own content

The example is only there to show you the shape. You will use it as a pattern while you plan, then remove it from your
own vault before you code your own notes. Do this step **before you add any page of your own**. Do not do it yet if
you want the example open while you read the other guides. You can remove it at any time.

When you are ready, type these commands in your vault folder. The first deletes the example page folders and keeps
`index`, whose Bases read whatever pages the vault holds. The second checks:

```text
git rm -r affordance concern group narrative technology
uv run scat check
```

`scat check` then prints:

```text
attribution mode: disallowed
no problems
```

If you already added narratives of your own, `git rm` leaves them where they are, and `scat check` prints a
`SCAT-DRAFT-FIELD` warning for each of those pages that is still a draft, then `0 errors` and the number of warnings. That is correct: warnings do not block you.

`git rm` has already staged the removal of the example pages. Save it as a commit, so your vault keeps the change. `git commit` saves what is staged, and nothing else, so pages and files of your own are not swept in:

```text
git commit -m "Remove the example"
```

Your vault now holds no example pages. The five folders went with them, so `narrative` and the others are not there
to list: each comes back when the first stub of its type is made. You do not write the folders or pages for your own content by hand. The tools
create each one as a stub, as you will see in the [coding guide](coding.md).

## The solo trial

Try SCAT alone, on your own notes, before you plan an event with others. The trial fits in one sitting. By the end,
one narrative is coded, you have seen its fingerprint, and it is `done`. Nothing leaves your private repository.

The commands below show your names in capitals: `NARRATIVE`, `GROUP`, `CONCERN` and `AFFORDANCE`. Replace each with a
name of your own before you run the line. The pages and outputs show a made-up account, `saturday-at-the-tool-library`,
a Saturday at a community tool library, so you can see what each step looks like. A name is lower-case letters,
digits and single hyphens, so a command run with a capitalised name is refused and nothing is written. Your vault holds at most the number of groups that `scat.toml` allows (6 in the
template), so name a broad group such as `workshop-participants`, never a person.

**1. Set up.** Do steps 1 to 5 above: create your private repository, run `uv sync`, run `uv run scat check`, open the
folder in Obsidian, and remove the example. Stay in your vault folder in Terminal for everything below.

**2. Make the page for your narrative.** One command makes the empty page:

```text
uv run scat stub NARRATIVE --type narrative
```

For the made-up account it prints `created narrative/saturday-at-the-tool-library.md`. Yours prints your name in its place.
The `narrative` folder did not exist after step 5, and this command makes it.

**3. Write the account.** Open that page in Obsidian and write one account from your notes, as it was told, under the
front matter. Set `kind` to `scenario`, set `timeframe` to `past`, set `status` to `draft` and add a one-sentence
`description`. The page then reads:

```text
---
type: narrative
kind: scenario
status: draft
title: "Saturday at the tool library"
description: "Loans go unrecorded when the sheet runs out."
timeframe: past
---

From the point of view of Workshop participants (about 10:20)

- Saturday, desk opens at 9. Three people ask for the same drill.
- Concern: "tools must come back in good order."
- The sign-out sheet lets us see who has what. It stops us seeing tools that are late.
```

**4. Record the edges.** An edge the account tells is a row on the page. These two commands write the rows and make
the group, concern and affordance pages they name, as stubs. You do not write the rows or the pages by hand:

```text
uv run scat record-edge holds GROUP CONCERN --told-by NARRATIVE --note "Said twice in the first hour."
uv run scat record-edge addressed-by CONCERN AFFORDANCE --told-by NARRATIVE
```

The made-up account's two edges are `workshop-participants` holds `tools-come-back-in-good-order`, which is addressed by `sign-out-sheet`.

Each prints `created ...`, `changed ...` and a `note:` line saying which row it added. Then, in Obsidian, link each
name where the account says it, as `[[workshop-participants|Workshop participants]]`,
`[[tools-come-back-in-good-order|tools must come back in good order]]` and `[[sign-out-sheet|The sign-out sheet]]`.
[Coding](coding.md#4-link-the-names) shows the page with its links. Then check:

```text
uv run scat check
```

It prints the mode line, `attribution mode: disallowed`, then `no problems`.

**5. See its fingerprint.** The fingerprint is the nodes the narrative links and the edges it tells:

```text
uv run scat fingerprint NARRATIVE
```

For the made-up account it prints:

```text
fingerprint saturday-at-the-tool-library (scenario, draft)
  group
    workshop-participants [stub]
  concern
    tools-come-back-in-good-order [stub]
  affordance
    sign-out-sheet [stub]
  edges
    holds: workshop-participants -> tools-come-back-in-good-order [draft; told by saturday-at-the-tool-library]
    addressed-by: tools-come-back-in-good-order -> sign-out-sheet [draft; told by saturday-at-the-tool-library]
```

To see it in Obsidian, draw it into your vault and open the picture there:

```text
uv run scat draw fingerprint --out fingerprint.png NARRATIVE
```

It prints `created fingerprint.png`. In Obsidian, open `fingerprint.png` from the file list. The narrative page's
Outgoing links panel shows the same nodes as a list. A dashed line in the picture would be a pair of nodes the account links with no row joining them; this
narrative has none.

**6. Set it done.** `done` means you have read the account against your notes and it is complete, and it is your call,
not the tool's. When you decide it is, run:

```text
uv run scat set-status NARRATIVE done
uv run scat check
```

The first prints `changed narrative/saturday-at-the-tool-library.md`, a note that `status` was set to `done`, and `check of narrative/saturday-at-the-tool-library.md: no problems`. The
second prints `attribution mode: disallowed`, then `no problems`. The group, concern and affordance pages are still stubs. That does not stop a clean check,
and you fill them in as you code more narratives.

**7. Save it.** Commit the work in your vault folder:

```text
git add .
git commit -m "My first narrative"
```

`git add .` stages everything in the folder that git does not ignore, so it also stages a drawing such as `fingerprint.png` and a plan file if you have one, not only your pages. To leave one out, name the files you want instead (`git add narrative group concern affordance`) or list the file in `.gitignore`. To keep one, do nothing: it goes into the commit with the rest. Run `git status` first to see which files are in.

That is the solo trial. If it worked, plan your first event in [Planning](planning.md), or code more notes with
[Coding](coding.md). To hand the finished vault over, see [Lock a version](coding.md#lock-a-version).

## Where next

Set up? Then pick where to go next:

- [The solo trial](#the-solo-trial): code one narrative of your own, start to finish, in one sitting.
- [Planning](planning.md): decide your sessions, your groups and your framing, before the event.
- [Coding paths](coding-paths.md): when you already have field notes, by hand or with an assistant.
- [Home](index.md): what SCAT is and why it has its name.
