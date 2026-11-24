# CLI reference

!!! tip "Your next step"
    Open a terminal in your vault folder and type `uv run scat --help`.

## Before you start

- A vault folder with a `scat.toml` file in it, for example a copy of the template. [Getting started](../getting-started.md) makes one.
- You type every command in that folder, starting with `uv run`, as in `uv run scat check`. The `--help` blocks below show `scat` alone, which is what the program calls itself.
- Every command has a twin you call from Python: `import scat_kg` in `uv run python`. The twins are in the [Python API reference](api.md), and they give the same messages.

The blocks below hold the exact output of `--help`. If your window is narrower or wider than 80 columns, your own `--help` wraps the lines differently.

## scat

```text
usage: scat [-h] <command> ...

Check and work on a SCAT knowledge-graph vault. Every command has a REPL twin
(`import scat_kg`) that gives the same messages.

positional arguments:
  <command>
    check       Check the vault against the rules. PAGE is a page name or its
                path from the vault folder; without it, the whole vault.
                Writes nothing.
    status      Show each page's status and the counts. PAGE is a page name or
                its path from the vault folder; without it, the whole vault.
    set-status  Set a page's status to stub, draft or done.
    index       Rewrite the generated table of every class page, creating a
                missing class page.
    stub        Create a stub page (a concern, affordance, technology,
                stakeholder-group or record page).
    stub-pair   Create the relation page for a pair, stubbing an endpoint that
                does not exist.
    stub-links  Create the pages that link fields name and the vault lacks.
                PAGE limits it to one page.

options:
  -h, --help    show this help message and exit

Run `scat <command> --help` for a command.
```

`scat` has seven commands. Each prints a message and exits with a code:

| Exit code | Meaning |
|---|---|
| 0 | No error and no refusal. Warnings alone give 0. |
| 1 | An error was found, or the command refused: it says why and gives a `Fix:` line. |
| 2 | The command line cannot be read (a missing argument, an unknown command). Nothing is run. |

Every command takes `--root ROOT`, the vault folder (default: the current folder). A command that refuses writes nothing.

=== "Python"

    ```python
    import scat_kg

    print(scat_kg.__doc__)
    ```

    ```text
    scat_kg: check and work on a SCAT knowledge-graph vault from the Python REPL.

        import scat_kg

        scat_kg.check()                     # the whole vault in the current directory
        scat_kg.check("concern/x.md")       # one page (a name or a path)
        scat_kg.check("x", neighborhood=True)
        scat_kg.status()                    # the same three scopes, for status
        scat_kg.set_status("x", "draft")
        scat_kg.index()
        scat_kg.stub("x", type="concern")
        scat_kg.stub_pair("heldby", "a", "b")
        scat_kg.stub_links()                # or stub_links("x")

    Each call takes `root=` (the vault folder; default: the current directory) and returns an object whose
    `str()` is the message the `scat` command prints, and which prints as that message. `.ok` is False when
    there is an error or a refusal (warnings alone leave it True): it is what the command's exit code is.
    ```

=== "CLI"

    ```bash
    uv run scat --help
    ```

    The output is the block above.

## scat check

```text
usage: scat check [-h] [--root ROOT] [--neighborhood] [PAGE]

Check the vault against the rules. PAGE is a page name or its path from the vault folder; without it, the whole vault. Writes nothing.

positional arguments:
  PAGE            check this page only

options:
  -h, --help      show this help message and exit
  --root ROOT     the vault folder, the one with scat.toml (default: here)
  --neighborhood  check PAGE and every page one link away, in either direction

REPL: `scat_kg.check()`, `scat_kg.check("<page>")`, `scat_kg.check("<page>", neighborhood=True)`
```

Checks the whole vault, one page, or one page and every page one link away. It writes nothing. It prints each problem with its rule id and a `Fix:` line, then a count line, or `no problems`.

Exit codes: 0 when there are no errors (warnings are fine), 1 when there is an error or a refusal (a page that is not there, a vault folder that is not there, `--neighborhood` without `PAGE`).

=== "Python"

    ```python
    scat_kg.check()
    scat_kg.check("anonymity", neighborhood=True)
    ```

    ```text
    no problems
    no problems
    ```

=== "CLI"

    ```bash
    uv run scat check
    uv run scat check anonymity --neighborhood
    ```

    ```text
    no problems
    no problems
    ```

## scat status

```text
usage: scat status [-h] [--root ROOT] [--neighborhood] [PAGE]

Show each page's status and the counts. PAGE is a page name or its path from the vault folder; without it, the whole vault.

positional arguments:
  PAGE            show this page only

options:
  -h, --help      show this help message and exit
  --root ROOT     the vault folder, the one with scat.toml (default: here)
  --neighborhood  show PAGE and every page one link away, in either direction

REPL: `scat_kg.status()`, `scat_kg.status("<page>")`, `scat_kg.status("<page>", neighborhood=True)`
```

Shows the status of each page, then the counts. It writes nothing. The status is `stub`, `draft` or `done`; a class page shows `(no status: class page)`.

Exit codes: 0, or 1 for a refusal (a page that is not there, a vault folder that is not there, `--neighborhood` without `PAGE`).

=== "Python"

    ```python
    scat_kg.status("anonymity")
    ```

    ```text
    done         concern/anonymity.md
    1 done
    ```

=== "CLI"

    ```bash
    uv run scat status anonymity
    ```

    ```text
    done         concern/anonymity.md
    1 done
    ```

## scat set-status

```text
usage: scat set-status [-h] [--root ROOT] PAGE STATUS

Set a page's status to stub, draft or done.

positional arguments:
  PAGE         the page's name or path
  STATUS       stub, draft or done

options:
  -h, --help   show this help message and exit
  --root ROOT  the vault folder, the one with scat.toml (default: here)

REPL: `scat_kg.set_status("<page-name>", "<status>")`
```

Changes the `status:` line of one page and nothing else in the file. `PAGE` is a name or a path.

Exit codes: 0 when the status was changed or already was that value, 1 for a refusal (not a status, no such page, a class page).

=== "Python"

    ```python
    scat_kg.set_status("anonymity", "draft")
    ```

    ```text
    changed concern/anonymity.md
    note: `status` set to draft (was done)
    ```

=== "CLI"

    ```bash
    uv run scat set-status attribution draft
    ```

    ```text
    changed concern/attribution.md
    note: `status` set to draft (was done)
    ```

The CLI example uses a different page from the Python one, so both can run in one vault. Running either again prints `unchanged` and a note that the status is already `draft`, and still exits with 0.

## scat index

```text
usage: scat index [-h] [--root ROOT]

Rewrite the generated table of every class page, creating a missing class page.

options:
  -h, --help   show this help message and exit
  --root ROOT  the vault folder, the one with scat.toml (default: here)

REPL: `scat_kg.index()`
```

Rewrites the generated table in each of the seven class pages, and creates a class page that is missing. It prints one line per class page: `created`, `changed` or `unchanged`. A page it did not need to rewrite prints `unchanged`.

Exit codes: 0, or 1 for a refusal (another file holds a class page's name, or a class page has no readable table markers).

=== "Python"

    ```python
    scat_kg.index()
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

=== "CLI"

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

## scat stub

```text
usage: scat stub [-h] [--root ROOT] --type TYPE NAME

Create a stub page (a concern, affordance, technology, stakeholder-group or record page).

positional arguments:
  NAME         the new page's name: a-z, 0-9 and hyphens

options:
  -h, --help   show this help message and exit
  --root ROOT  the vault folder, the one with scat.toml (default: here)
  --type TYPE  the page type key, one of: affordance, architecture-coded,
               architecture-raw, concern, scenario-coded, scenario-raw,
               stakeholder-group, technology

REPL: `scat_kg.stub("<page-name>", type="<type-key>")`
```

Creates one page with `status: stub`. The `--type` option is required. Use [`scat stub-pair`](#scat-stub-pair) for a relation page; a class page comes only from [`scat index`](#scat-index).

Exit codes: 0 when the page was created, 1 for a refusal (not a legal name, a file already has the name, not a stubbable type, or the group cap). A missing `--type` is a command line that cannot be read: exit code 2.

The CLI example uses a different name from the Python one, so both can run in one vault.

=== "Python"

    ```python
    scat_kg.stub("reading-group", type="concern")
    ```

    ```text
    created concern/reading-group.md
    ```

=== "CLI"

    ```bash
    uv run scat stub study-circle --type concern
    ```

    ```text
    created concern/study-circle.md
    ```

## scat stub-pair

```text
usage: scat stub-pair [-h] [--root ROOT] RELATION ENDPOINT-A ENDPOINT-B

Create the relation page for a pair, stubbing an endpoint that does not exist.

positional arguments:
  RELATION     one of: addresses (concern then affordance), attributes
               (affordance then technology), heldby (group then concern)
  ENDPOINT-A
  ENDPOINT-B

options:
  -h, --help   show this help message and exit
  --root ROOT  the vault folder, the one with scat.toml (default: here)

REPL: `scat_kg.stub_pair("<relation>", "<endpoint-a>", "<endpoint-b>")`
```

Creates the relation page for a pair, and a stub for an endpoint that does not exist. If a page already states this pair, it prints `unchanged` and creates nothing.

Exit codes: 0 when it created pages or found the pair already stated, 1 for a refusal (an endpoint of the wrong type, a name that is not legal, the same name twice, an unknown relation).

=== "Python"

    ```python
    scat_kg.stub_pair("heldby", "project-leads", "reading-group")
    ```

    ```text
    created heldby/project-leads-holds-reading-group.md
    note: write `description`, `notes` and the body in heldby/project-leads-holds-reading-group.md; the endpoints are filled
    ```

=== "CLI"

    ```bash
    uv run scat stub-pair heldby project-leads study-circle
    ```

    ```text
    created heldby/project-leads-holds-study-circle.md
    note: write `description`, `notes` and the body in heldby/project-leads-holds-study-circle.md; the endpoints are filled
    ```

## scat stub-links

```text
usage: scat stub-links [-h] [--root ROOT] [PAGE]

Create the pages that link fields name and the vault lacks. PAGE limits it to one page.

positional arguments:
  PAGE         look at this page's links only

options:
  -h, --help   show this help message and exit
  --root ROOT  the vault folder, the one with scat.toml (default: here)

REPL: `scat_kg.stub_links()`, `scat_kg.stub_links("<page>")`
```

Creates the pages that link fields name and the vault lacks, from one page or the whole vault. Links to pages that exist create nothing. When there is nothing to create it prints `stub-links: nothing to do`.

Exit codes: 0 when it created pages or had nothing to do, 1 for a refusal (links that name one page as two types, the group cap, a page that is not there).

=== "Python"

    ```python
    scat_kg.stub_links()
    ```

    ```text
    stub-links: nothing to do
    ```

=== "CLI"

    ```bash
    uv run scat stub-links
    ```

    ```text
    stub-links: nothing to do
    ```

## Where next

Keep the reference close:

- [Python API reference](api.md): every operation, with its parameters and what it returns.
- [Coding guide](../coding.md): how to use these commands while you code your notes.
- [Home](../index.md)
