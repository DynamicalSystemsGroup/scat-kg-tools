# Getting started

!!! tip "Your next step"
    Create your private repository from the template (step 1 below).

*Tuning up: get everything ready before your first session.*
{ .epigraph }

## Before you start

- A Mac, and a GitHub account. If you have none, make one at <https://github.com>.
- Terminal. Open it from Applications, then Utilities. Type every command below in Terminal, one at a time, and press
  Return after each.
- [Obsidian](https://obsidian.md), the app you will read the vault in. It is free to install.

SCAT stands for Stakeholder groups, Concerns, Affordances and Technologies: the four kinds of thing your notes are coded into. If you have not read what that means, start at the [home page](index.md).

## 1. Create your private repository

Your discussions are your data, so make your repository **private**. A private repository can be seen only by you and
the people you invite. A public one can be read by anyone on the internet, and your notes are about real groups of
people. Both paths below set it for you, and the website path shows it as a choice you confirm.

Pick one path.

**With the GitHub command line, `gh`.** `gh` is installed separately. If you use Homebrew, `brew install gh` installs it. Without Homebrew, use the website path below instead. You also need a one-time `gh auth login`. This creates the repository
and downloads it, in one command. `my-vault` is the name you are choosing for your repository and its folder.

```text
gh repo create my-vault --template DynamicalSystemsGroup/scat-kg-template --private --clone
cd my-vault
```

**On the GitHub website.** No `gh`? Use this path.

1. Open <https://github.com/DynamicalSystemsGroup/scat-kg-template>.
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

You should see `scat.toml` in the list, with folders such as `concern` and `class`.

!!! note "Your folder name"
    The folder is named after the repository you created. These pages say `my-vault`. If you chose another name,
    use that name wherever you see `my-vault`.

!!! note "If you see only `README.md`"
    SCAT is a preview that is still being tried before its first release (version 0.1.0). In this preview, the
    template's default branch is `dev`, and `main` is only a stub that holds a README. If `ls` shows nothing but `README.md`, you are on the stub. Run this, then `ls` again:

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

The template ships with a worked example, so you can see what a vault looks like. A clean result for it is this. A clean check means **0 errors**; warnings may stay:

```text
warning [SCAT-CONFLICT-BOTH] scenario-coded/notes-at-a-chatham-house-session-coded.md:11 field `concerns`: this record holds both [[anonymity]] and [[attribution]], which conflict (declared on [[anonymity]])
  Fix: none needed if both belong in this record. Holding both sides is allowed and is what the warning marks, a place where two concerns pull apart. If one was coded here by mistake, delete its line `- "[[anonymity]]"` or `- "[[attribution]]"` under `concerns`.
0 errors, 1 warning
```

That is a pass. **Errors** block you: a vault with errors is not clean. **Warnings** do not block you. This
warning, `SCAT-CONFLICT-BOTH`, is the first one you meet. A clean vault may keep it. It marks a place where one record holds two concerns that pull
against each other, and holding both is the point of SCAT, so you leave it in place.

Run the check again after every change you make.

### The same check in the Python REPL

Prefer working interactively? The REPL (a Python session where you type one line at a time) does the same check.
Start it with `uv run python`. The prompt changes to `>>>`. Type the lines below one at a time, and the result prints beneath them. Type `exit()` to leave.

```python
import scat_kg
scat_kg.check()
```

It prints the same text as `uv run scat check`:

```text
warning [SCAT-CONFLICT-BOTH] scenario-coded/notes-at-a-chatham-house-session-coded.md:11 field `concerns`: this record holds both [[anonymity]] and [[attribution]], which conflict (declared on [[anonymity]])
  Fix: none needed if both belong in this record. Holding both sides is allowed and is what the warning marks, a place where two concerns pull apart. If one was coded here by mistake, delete its line `- "[[anonymity]]"` or `- "[[attribution]]"` under `concerns`.
0 errors, 1 warning
```
 Every `scat` command has a twin in the REPL; the
[reference](reference/cli.md) lists them.

### Two things the tools do that may surprise you

`scat.toml` is required. It sits in the vault folder and holds the cap on stakeholder groups. If it is missing, the
check reports an error (`SCAT-CAP-CONFIG`). If you see that error, you are probably in the wrong folder, or the file
was deleted. In a wrong (empty) folder the check also prints seven `SCAT-INDEX-STALE` warnings, one per class page, like this one, and ends with `1 error, 7 warnings`:

```text
warning [SCAT-INDEX-STALE] class/addresses-pairs.md index table: the page is missing
  Fix: run `scat index` (REPL: `scat_kg.index()`)
```

Do not run `scat index` to fix this. `cd` into your vault folder instead.

`scat index` rebuilds the tables on the class pages from the pages themselves. It prints `unchanged` for each class
page it did not need to rewrite. On the untouched example, every line says `unchanged`, and that is correct:

```bash
uv run scat index
```

```text
unchanged class/addresses-pairs.md
unchanged class/affordances.md
unchanged class/attributes-pairs.md
unchanged class/concerns.md
unchanged class/heldby-pairs.md
unchanged class/stakeholder-groups.md
unchanged class/technologies.md
```

## 4. Open the vault in Obsidian

Open Obsidian, choose **Open folder as vault**, and pick your folder (`my-vault`). Open a page in the `concern`
folder and click its links: you are walking the graph. Create pages with `scat stub`. [Coding](coding.md#where-raw-and-coded-pages-come-from) says more.

## 5. Start your own content

The example is only there to show you the shape. You will use it as a model while you plan, then remove it from your
own vault before you code your own notes. When you are ready, type these commands in your vault folder. The first
deletes the example page folders and keeps `class`. The second rebuilds the class tables. The third
checks:

```text
git rm -r addresses affordance architecture-coded architecture-raw attributes concern heldby scenario-coded scenario-raw stakeholder-group technology
uv run scat index
uv run scat check
```

`scat index` prints `changed` for each of the seven class pages, and `scat check` then prints:

```text
no problems
```

`git rm` only stages the removal. Save it as a commit, so your vault keeps the change and the removal is not lost.
`git add .` also stages the rebuilt class tables:

```text
git add .
git commit -m "Remove the example"
```

Your vault is now empty and clean. You do not write the folders or pages for your own content by hand. The tools
create each one, as you will see in the [coding guide](coding.md).

Do not do this yet if you want the example open while you read the other guides. You can remove it at any time.

## Where next

Set up? Then pick where to go next:

- [Planning](planning.md): decide your sessions, your groups and your framing, before anyone counts in.
- [Coding](coding.md): when you already have raw notes.
- [Home](index.md): what SCAT is and why it has its name.
