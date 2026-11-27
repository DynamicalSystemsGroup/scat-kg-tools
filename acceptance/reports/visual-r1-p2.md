# Visual pass, round 1, persona p2 (by-hand path, Terminal)

27 November. Persona p2: an organiser new to the command line, on the Terminal path (no Python session); the
tester is a Haiku subagent. Earlier AI user tests read pages and files as text; in this pass the ACE acted as the
tester's hands on the real interfaces and saved a screenshot or the exact output for every request. Screenshots and
outputs are kept outside the repository, in the lab evidence folder; this report quotes what matters.

## How it ran

- **Pages:** the live Pages site in Chrome, read as rendered (a screenshot of each page used, plus its rendered text).
- **Obsidian:** two vaults opened with File, Open Vault, "Open folder as vault". Every page edit was made in
  Obsidian's editor: properties through the Properties panel ("Add property", values edited in place); bodies typed
  with Obsidian's list continuation; links typed over the words (Obsidian closes `]]` by itself). Each saved page was
  compared with the tester's requested text: all six matched exactly.
- **Terminal:** every command the tester asked for, with its full output.
- **Covered afterwards:** creating the private repository on GitHub's website (V7). In the run itself the test lead
  made clones with the remote removed, as in earlier rounds, so both pushes failed with "No configured push destination". Clipboard paste was not used (no
  grant), so text was typed.

## Result

J1 to J10 reached. The solo trial (J2) coded one narrative, drew its fingerprint and opened it in Obsidian, set it
done and committed it. The full run (J5 to J10) set up `my-vault`, removed the example, wrote a plan, drafted a
scenario and an architecture in Obsidian, recorded 12 edges, linked both pages in Obsidian, set both done, ran the
Analysis views, opened the narrative Base, and tagged `market-model-v1` on a clean check and a clean `git status`. No
blocking finding.

## Findings

| # | Finding | Seen | Disposition |
|---|---|---|---|
| V1 | Opening a vault in Obsidian rewrote the template's `.obsidian/app.json` (trailing newline) and `core-plugins.json` (the full plugin list) and created `appearance.json`; the first `git add .` committed them with the user's narrative. Reproduced in both vaults. | Terminal (`git status`) after Obsidian opened the vault | **Fixed:** the template ships both files in the form Obsidian writes; `appearance.json` is ignored (template `dev` 87accad). Checked on screen: a fresh clone opened in Obsidian leaves both files unchanged. |
| V2 | Viewing the narrative index in Obsidian can rewrite `index/narrative.base` into Obsidian's own YAML form (no quotes; `note.title` as `title`). Seen in two of three vaults. `scat index` reads the two forms as the same, so the tool and Obsidian do not fight over it, but the change shows in `git status`. | Terminal after the Base was opened | **For the chief engineer:** have `scat index` write Obsidian's form (a tools change), or accept. |
| V3 | `scat stub` writes `timeframe: # past \| future \| mixed`; Obsidian shows the property as empty, so the hint is invisible there. | Obsidian, Properties panel | **For the chief engineer:** accept (the Coding page shows the hint) or change the stub. |
| V4 | Node pages made by `record-edge` stay stubs when their narratives are set done; no page says whether a node page must be written first, and the views show every node as `[stub]` without saying that is expected. | Terminal (views) | **For the chief engineer:** a page sentence, or accept. |
| V5 | The persona's terms did not settle the attribution question, so the mode was a guess at planning. | Text | Accept: the page asks the question; the persona's terms did not answer it. |
| V6 | Signed out, GitHub's template page shows no **Use this template** button; `getting-started`'s website path listed a GitHub account but did not say to sign in first. Checked on the live repository page by the ACE after the run (the tester's clones skipped this step). | Chrome, the template's page signed out | **Fixed:** the step now says to sign in first (tools `dev`). |
| V7 | The website path, run afterwards in the built-in browser, where the chief engineer is signed in: Use this template, Create a new repository, a name, visibility set to Private (the form showed Public until it was changed), Create. The repository came out private with one branch, `dev`; cloned, `scat check` reported no problems. The chat path's GitHub Desktop steps named the button **Commit to main**, which such a repository never shows. | Browser and Terminal | **Fixed:** the steps name **Commit to dev** (tools `dev`). |

The tester's other items (gaps in its own terms and plan, a transcription detail, the git identity in a clone with no
setup) are not page or tool faults.

## What the earlier text-only tests could not have seen

V1 to V3 appear only when Obsidian itself opens the vault or renders the page: the earlier rounds checked
`.obsidian/` "through files". The Obsidian steps the docs describe (Properties panel, typing links, opening a PNG and
a Base) all worked as the pages say.
