# SCAT for Obsidian

A plugin that checks the note you have open against the SCAT rules and lists the messages in a side panel, with a count in the
status bar. It never writes to your notes. The first time, `uv run` may create a `.venv` folder and update `uv.lock` in the vault.

Status: built and tested on a Mac without Obsidian. Read "Never exercised inside Obsidian" below before you rely on it.

## What you need first

1. **uv** installed. In a terminal, `uv --version` should print a version. If it does not, install uv from its own site, then try again.
2. **A SCAT vault**: a copy of the template case study (a folder with `scat.toml`, `pyproject.toml` and `uv.lock` in it), opened in Obsidian as a vault.
3. **Once, in a terminal inside that vault folder**: `uv run python -c "import scat_kg"`. It builds the vault's environment and needs
   the network the first time. If it prints nothing and returns, the plugin can work.
4. Obsidian on a desktop (macOS was the only system considered). Not for phones or tablets.

## Install

0. **Get the folder** (if you do not already have the repository). The plugin lives on the branch `spike/obsidian-plugin` of the
   scat-kg-tools repository, in `research/obsidian-plugin/dist/scat/`. In a terminal, from the folder that holds your clone of the
   repository (or `git clone <repository address>` first, then `cd` into the clone):
   ```
   git fetch
   git checkout spike/obsidian-plugin
   cd research/obsidian-plugin
   ```
   `git fetch` and `git checkout` run from the top folder of the clone; `cd` then moves you to `research/obsidian-plugin`, and the two
   commands after it run from there. Replace `<vault>` with your vault's full path, keeping the quotes (they handle spaces):
   ```
   mkdir -p "<vault>/.obsidian/plugins"
   cp -R dist/scat "<vault>/.obsidian/plugins/scat"
   ```

Then the other steps:

1. Find the folder `research/obsidian-plugin/dist/scat/` in the repository. It holds `main.js`, `manifest.json`, `styles.css` and `scat_json.py`.
2. Check that `main.js` is at `<your vault>/.obsidian/plugins/scat/main.js` (step 0 put it there).
   (`.obsidian` is hidden in Finder; press Cmd+Shift+. to show it.)
3. In Obsidian: Settings > Community plugins > turn off restricted mode ("Turn on community plugins").
4. In the same screen, click the reload icon next to "Installed plugins".
5. Find "SCAT" in the list and switch it on.

Then open a page such as `concern/anonymity.md`. The status bar (bottom right) shows `SCAT: clean` after a moment.

## How to read it

- **Status bar**: `SCAT: 1 error, 2 warnings`, `SCAT: clean`, or a short state (see Troubleshooting).
- **Panel**: open it with Cmd+P, then "SCAT: Open panel". It lists errors first, then warnings. Each message shows
  `severity [RULE-ID] file:line field: what is wrong`, and under it the exact **Fix** text, unchanged from the SCAT catalogue.
  Click a message to open that file at that line.
- **Errors block, warnings do not.** A warning can stay.
- **When it runs**: when you open a note, and about half a second after you save or the autosave fires. Cmd+P, "SCAT: Check active note"
  runs it now and shows a pop-up summary.
- **Settings > SCAT**: "Include neighbors" also checks the pages one link away (messages from those pages are listed too).
  "Path to uv" is for the case below.

It checks the saved file, not what you are typing this second.

## Troubleshooting

| You see | Why | What to do |
|---|---|---|
| `SCAT: check failed`, panel says "Could not start uv" | Obsidian opened from the Dock does not see your terminal's PATH. | In a terminal run `which uv`. Paste that path into Settings > SCAT > "Path to uv". The plugin already looks in `~/.local/bin`, `/opt/homebrew/bin`, `/usr/local/bin` and `~/.cargo/bin` first. |
| `SCAT: not a SCAT vault` | No `scat.toml` in the note's folder or any folder above it. | Open the note from a vault that is a copy of the template. Nothing is checked. |
| `SCAT: not a page` | The note has no `type:` in its frontmatter (for example `README.md`). | Nothing to do: only SCAT pages are checked. |
| `SCAT: scat_kg missing` | The Python that ran does not have scat_kg. | In a terminal inside the vault: `uv run python -c "import scat_kg"`. If that fails, the vault's `pyproject.toml` is missing or does not pin `scat-kg`. |
| `SCAT: check failed`, panel says "uv did not return a result" and shows uv's last lines | uv could not build the environment (often no network or no git on the first run). | Run `uv run python -c "import scat_kg"` in a terminal inside the vault and read its message. |
| "The check took too long" | The first run builds the environment and passed 3 minutes. | Run the same command in a terminal once, then check again. |
| `SCAT: refused` | scat_kg declined the request. The panel shows its words. | Follow its Fix line. |
| Nothing at all, no status bar text | The plugin is not enabled or not loaded. | Settings > Community plugins: is "SCAT" switched on? Is `main.js` at `.obsidian/plugins/scat/main.js`? Cmd+Option+I opens the developer console for errors. |

## How it works, and the choice made

The plugin runs `uv run --quiet --project <vault> python <vault>/.obsidian/plugins/scat/scat_json.py <note> [--neighborhood]`.
The shim `scat_json.py` calls `scat_kg.check` (public API only) and prints JSON; the plugin draws it. No rules live in the plugin.
Chosen over a "path to Python" setting because uv uses the vault's own pinned scat-kg and its own environment without the user
knowing where that environment is. The cost is that uv has to be found, hence the "Path to uv" setting.

## Never exercised inside Obsidian

Nobody could open Obsidian where this was built. What did run: the TypeScript build, 31 unit and end-to-end tests, and the shim
(8 pytest tests) in a scratch copy of the template, using the same command line the plugin builds, from a copy of `dist/scat`
placed at `.obsidian/plugins/scat/`. Never run:

- That Obsidian loads the plugin and accepts `manifest.json`.
- The panel rendering, the click that opens a file at a line, and the status-bar text.
- The `file-open` and save events, and the 0.5 second debounce.
- Spawning uv from Obsidian's own process (the Dock-launch PATH problem is handled in code, not seen).
- The settings screen, the pop-up summary, the command names.
- "Include neighbors" inside Obsidian; a SCAT folder above the Obsidian vault; Windows and Linux; vaults with spaces in the path inside Obsidian.
- Timing on a large vault.
- The `refused` and `scat_kg missing` states with real scat_kg (they are covered with a stand-in module only).

## What the core would simplify (for the ACE)

- `scat check --json` would remove the shim and the `scat_kg` import: the plugin could run `scat` directly.
- `scat check --stdin` (or an unsaved-text argument) would check what is on screen, not only the saved file.
- Machine-readable states (`not-a-page`, `not-a-vault`) from the CLI would replace the shim's own `type:` and `scat.toml` sniffing.
- `Problem` fields for structured fixes (target line, replacement text) would allow quick-fix buttons, not just Fix text.
- A `uv tool install` or released wheel for `scat` would drop the need to find `uv` and the vault's pinned environment.
