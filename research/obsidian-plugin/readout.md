# RS1 readout: a SCAT linter inside Obsidian

Sources are the official developer docs (repo `obsidianmd/obsidian-developer-docs`; several docs.obsidian.md URLs return "not found", so I read the repo files) and the sample plugin. Unverified items are listed last.

## 1. What the plugin API offers a linter

| Need | API | Source |
|---|---|---|
| Commands (palette; active-note only) | `addCommand` with `callback`, `checkCallback`, `editorCallback`, `editorCheckCallback`; do not set default hotkeys | [Commands](https://github.com/obsidianmd/obsidian-developer-docs/blob/main/en/Plugins/User%20interface/Commands.md) |
| Side panel of diagnostics | custom `ItemView` registered with `registerView`, opened in a sidebar leaf; never hold view references, use `getLeavesOfType` | [Views](https://github.com/obsidianmd/obsidian-developer-docs/blob/main/en/Plugins/User%20interface/Views.md) |
| Status bar count | `addStatusBarItem`; **not supported on mobile** | [Status bar](https://github.com/obsidianmd/obsidian-developer-docs/blob/main/en/Plugins/User%20interface/Status%20bar.md) |
| Inline squiggles | CodeMirror 6 editor extensions via `registerEditorExtension`; mark, widget, replace and line decorations; a state field is needed to decorate outside the viewport | [Editor extensions](https://github.com/obsidianmd/obsidian-developer-docs/blob/main/en/Plugins/Editor/Editor%20extensions.md), [Decorations](https://github.com/obsidianmd/obsidian-developer-docs/blob/main/en/Plugins/Editor/Decorations.md) |
| Events (check on save / open / edit) | `registerEvent(this.app.vault.on(...))`; `Vault` offers `create`, `modify`, `delete`, `rename`; `Workspace` offers `file-open`, `active-leaf-change`, `editor-change`, `quick-preview` ("React to file changes before they are saved to disk"); `MetadataCache` offers `changed`, `resolved` | [Events](https://github.com/obsidianmd/obsidian-developer-docs/blob/main/en/Plugins/Events.md), [Vault](https://github.com/obsidianmd/obsidian-developer-docs/blob/main/en/Reference/TypeScript%20API/Vault.md), [Workspace](https://github.com/obsidianmd/obsidian-developer-docs/blob/main/en/Reference/TypeScript%20API/Workspace.md), [MetadataCache](https://github.com/obsidianmd/obsidian-developer-docs/blob/main/en/Reference/TypeScript%20API/MetadataCache.md) |
| Applying a fix | the guidelines say: Editor API for the active note, `Vault.process` for atomic background edits, `FileManager.processFrontMatter` for frontmatter | [Plugin guidelines](https://github.com/obsidianmd/obsidian-developer-docs/blob/main/en/Plugins/Releasing/Plugin%20guidelines.md) |

There is no built-in "diagnostics" or "code action" API as in an LSP. A quick fix is our own UI (a button in the panel, or a widget) that calls the editor or `Vault.process`.

## 2. The community-plugin path

- Steps: public GitHub repo with `README.md`, `LICENSE`, `manifest.json`; a GitHub release whose tag equals the manifest `version` (no `v`), with `main.js`, `manifest.json` and optional `styles.css` attached; submit at community.obsidian.md; an automated review must pass before the plugin is installable ([Submit your plugin](https://docs.obsidian.md/Plugins/Releasing/Submit+your+plugin), fetched; sample-plugin [README](https://raw.githubusercontent.com/obsidianmd/obsidian-sample-plugin/master/README.md)).
- Requirements: accurate `minAppVersion`, description of 250 characters or fewer ending in a period, no plugin id in command ids, remove all sample code, and **"Node.js and Electron APIs are only allowed on desktop"; if used, `isDesktopOnly` must be `true`** ([Submission requirements](https://github.com/obsidianmd/obsidian-developer-docs/blob/main/en/Community%20directory/Submission%20requirements%20for%20plugins.md)).
- Policies: no obfuscation, no client-side telemetry, **no installing or updating themselves or their dependencies**; network use, access to files outside the vault, and closed source must be disclosed in the README ([Developer policies](https://github.com/obsidianmd/obsidian-developer-docs/blob/main/en/Community%20directory/Developer%20policies.md)).
- Mobile: Node and Electron APIs "aren't available on mobile devices", and calls made by your plugin or its dependencies "can cause your plugin to crash". `isDesktopOnly: true` stops installation on mobile ([Mobile development](https://github.com/obsidianmd/obsidian-developer-docs/blob/main/en/Plugins/Getting%20started/Mobile%20development.md)).
- **Shelling out is not named anywhere** in the policies or requirements I read. It falls under the Node API rule, so a subprocess plugin is permitted if desktop-only. Whether review accepts a plugin that needs a user-installed binary is undocumented. A plugin that *downloads* a runtime on first run would hit "install or update themselves or their dependencies".
- Release assets are three files. A bundled binary or Wasm runtime must be inlined in `main.js` or fetched at run time (network disclosure, probably the self-install rule). No size limit found.

## 3. Trade study

Criteria: setup burden, single source (R-13), mobile, maintenance, store acceptance, speed on 500 pages.

| | (a) subprocess to Python | (b) TypeScript port | (c) Pyodide/Wasm | (d) hybrid (a now, b later) |
|---|---|---|---|---|
| Setup burden | **Medium.** The user already needs uv and the tools for the REPL (MISSION), so no new install; but a GUI-launched Obsidian may not inherit the shell PATH, so a "path to scat" setting is needed (unverified) | **Low.** Install the plugin only | **Low to medium.** Install only, but a large runtime must ship inside `main.js` or be fetched | Medium, falling to low once (b) lands |
| Single source (R-13) | **Strong.** The one implementation, the one TBox, the one catalogue; plugin holds no rules | **Weak by default.** About 2,800 lines of Python checks (28 rules) are re-implemented; needs a generated TBox module plus a golden-test harness running both implementations on the same vaults, forever | **Strong.** Runs the same Python and `scat.ttl` | Strong now; weak later unless the golden harness exists |
| Mobile | **None.** `isDesktopOnly: true` required | **Full** (if it avoids Node APIs) | **Possible in principle**, unproven: the scat code needs pydantic, PyYAML (both in the Pyodide package list, [packages](https://pyodide.org/en/stable/usage/packages-in-pyodide.html)) and rdflib (not in that list; would need a wheel via micropip, i.e. network, or bundling). | None now, full later |
| Maintenance | **Lowest.** Thin client over a JSON contract | **Highest.** Every rule change lands twice | **Medium.** Runtime upgrades, wheel bundling, and a fragile build | Low now, high later |
| Store acceptance | **Likely accepted** if desktop-only and disclosed (policy silent on shelling out; see section 2 caveat) | **Cleanest.** Pure plugin | **At risk.** Size and "installs its dependencies" concern | As (a), then as (b) |
| Speed, 500 pages | **Good.** The repo's R-5 bench holds one page under 1 s, neighborhood under 2 s, vault under 5 s on a generated 500-page vault, including reading it, process start included ([`tests/bench/test_r5_thresholds.py`](../../tests/bench/test_r5_thresholds.py), thresholds only; I did not run it). Each check pays a process start | **Best.** In-process, and Obsidian's metadata cache can supply links | **Poor to unknown.** Wasm start-up plus rdflib parse of the 39 KB TTL on each load; no measurement | As (a) now |

## 4. What the tools would need

Today `scat check` prints `Report.render()` text and exits 0 or 1 (`src/scat_kg/cli.py`, `main`), with no machine-readable output. Needed, smallest first:

1. **`scat check --json`.** `Problem` is already a frozen record with `rule`, `severity`, `file`, `where`, `what`, `fix`, `line`, `column`, `repeat` (`checks/problem.py`): serialise `Report.problems` plus `ok`. Include a `schema_version`. Rule ids are already stable (`SEVERITY` table).
2. **A check of an unsaved buffer.** `read_vault(root)` reads from disk (`vault.py`). Needed: `scat check PAGE --stdin` that overlays the buffer text for that page on the on-disk vault. Without it, the plugin checks only on save (`vault.on('modify')`), a reasonable first delivery.
3. **Structured fixes.** `fix` is prose ("add the line `X`"). A quick fix needs `edits: [{file, line, op, text}]` for rules whose fix is exact; the catalogue says which. Rules whose fix is a command (for example `scat stub`) can map to a plugin command that runs it.
4. **Line and column on every problem.** `line` and `column` are optional today.
5. **A version handshake**, so the plugin can refuse an incompatible version.

## 5. Recommendation

Choose **(d), starting as (a)**: a desktop-only plugin that is a thin client over `scat check --json`, with no rules in TypeScript. The audience is a macOS facilitator-analyst who already installs uv and the tools (MISSION), mobile is not v0.1, and (a) is the only option that keeps R-13 free. Revisit (b) only if mobile becomes a stated need, with the golden-equality harness; do not start (c) without a measured spike.

## 6. First delivery package (sketch)

1. Tools: `scat check --json` with stable schema, line and column, `--stdin` overlay (items 1 to 5 above).
2. Plugin core loop: settings (path to `scat`, vault root); on `file-open` and on `vault.on('modify')` (debounced) run `scat check <page> --neighborhood --json`; an `ItemView` panel listing problems, click to jump to line; status bar count; a launch-failure notice with the fix ("set the path to `scat`").
3. Quick fix v1: for rules with an exact single-line edit, a panel button calling `Vault.process`; others show the fix text and a "copy command" button.
4. README disclosures: runs a local program, no network.
5. Release: GitHub release with the three assets, after a user test on a real vault. Not in it: inline decorations, mobile.

## 7. Prototype (`prototype/`)

A desktop-only plugin in the sample-plugin layout: `main.ts` handles lifecycle, and an injectable spawn runner runs `uv run --quiet --project <vault> python scat_json.py <note>`. `scat_json.py` is a small Python shim that uses only scat_kg's public `check`, because `scat check --json` does not exist yet (core is consumed as pinned); `prototype/JSON-CONTRACT.md` defines the shim's output, derived from `Problem`. Parsing, grouping and message text are pure modules; there are 31 JS tests plus 8 pytest tests. It shows output in a panel, notice and status bar, on command, `file-open` and `modify`. Build: `npm ci && npm run build && npm test`, on Node v26.13.1 LTS. Install from `dist/scat/`.

It was never run inside Obsidian. Not shown:

- that the plugin loads, or that panel rendering, click-to-jump, status bar and events work;
- spawning uv from Obsidian (macOS GUI PATH; a path setting exists);
- real-vault latency, store review of a subprocess plugin;
- mobile, inline decorations, quick-fix writes.

## Claims I could not verify

- Whether the directory review accepts or rejects plugins that spawn processes (policy text is silent).
- Obsidian GUI PATH inheritance on macOS (expected, not tested).
- Any size cap on `main.js` or release assets.
- Pyodide support for rdflib and for the whole scat stack; mobile memory limits.
- The speed numbers in the table: I read the bench's thresholds but did not run it.
