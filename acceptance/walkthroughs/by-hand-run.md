# Run record: by hand (WP25-U3), page `docs/coding.md`

Date: 2026-11-26. Environment: macOS 15 (Darwin 24.6), Obsidian (installed app, background control only), Bash for shell commands.
Material: lab only. Template `scat-kg-template` cloned at the commit pinned in `tests/docs/conftest.py` (0a765a8), narrative `groups-under-a-cap-pitch` (template case study). No account, no key, no AI in the loop.

## What was run, and what was not

| Step | Run? | Outcome |
|---|---|---|
| Clone template, `uv sync` | yes (Bash) | vault set up; `uv run scat check` printed `no problems` before any edit |
| 1 Open the vault in Obsidian | NO | refused, see below |
| 2 Open the narrative in Obsidian | NO | same cause |
| 3 `status` done to draft | edit made on the file with a script, not typed in Obsidian | file changed as the page says |
| 4 Add the link line | same | `[[project-leads|Project leads]]` line added |
| 5 Add the `Edges told` row | same | row added (first with the typo `projct-leads`) |
| 6 `scat check <page>` | yes (Bash) | typo run: `SCAT-DRAFT-END-NOPAGE`, 0 errors, 1 warning; output pasted on the page is that output. After the fix: `no problems` |
| 7 REPL `import scat_kg` | yes (piped into `uv run python -q`) | `no problems` |
| 8 `status` back to done | script edit | file changed |
| 9 `uv run scat check` whole vault | yes | `no problems`, exit 0 |

Steps 1 to 5 and 8 on the page are therefore written from the file-level result of the same edits, not from clicks in Obsidian. The menu names in step 1 (Manage vaults, Open folder as vault) are from Obsidian's menus as known, not seen on this machine.

## Why Obsidian steps were not run

- Obsidian could not open the lab vault in background control: `File > Open Vault...` is disabled when the app is not frontmost, and `obsidian://open?path=...` answered "Vault not found" for a folder that is not registered.
- Full-screen control was requested (reason: file dialog) and no answer came within the time limit. It was not requested again.
- Writing the vault into Obsidian's `obsidian.json` and opening it by id was tried; the running app did not re-read the file ("Vault not found"). That entry was removed and the file restored (content equal to the backup taken first).
- Terminal access was requested and not granted by the tool: it only offers click tier (no typing), so no real Terminal window was shown. The check output on the page is real pasted output from Bash, not a screenshot, and is not presented as one.
- The Obsidian window that was open showed the user's own vaults and notes, so no screenshot of it was taken.

## Screenshot slots not taken (docs/assets/walkthroughs/by-hand/)

| File | Must show | Step |
|---|---|---|
| 01-vault-open.png | Obsidian with the lab vault open, folders in the left pane | 1 |
| 02-narrative-page.png | `groups-under-a-cap-pitch` with properties and the `Edges told` table | 2 |
| 03-link-added.png | the new `[[project-leads|Project leads]]` line | 4 |
| 04-row-added.png | the new row in `Edges told` | 5 |
| 05-check-terminal.png | Terminal window with `uv run scat check` and `no problems` (genuine window only) | 9 |

The page has no image references; add them with the slots when the sitting is done. Crop out the user name in paths.

## Deviations and steps a script could remove

- The template's narratives are all `done`, so the example sets `draft` and back; a coder's own new narrative would not need steps 3 and 8.
- Step 3 and 8 (status) could be a single command (`scat set-status`), which is the assistant-path spelling; by hand the coder edits the property.
- Step 6 and 9 differ only in scope; both kept as the quick check and the whole-vault check.

## Installed and removed

- Cloned `scat-kg-template` and ran `uv sync` (a `.venv` and uv cache entries) in the scratchpad folder `u3/vault`: removed at the end (the uv cache under the user's cache folder is shared and was left).
- Temporary entry in Obsidian's `obsidian.json`: removed, file restored from backup, backup deleted.
