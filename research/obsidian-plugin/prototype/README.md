# SCAT Check: Obsidian plugin prototype (RS1-U2)

A minimal, desktop-only plugin that runs `scat check` for the active note and shows the messages in a side panel,
as a notice, and as a status-bar count. It follows the readout's recommended architecture: a thin client over
`scat check --json`, with no rules in TypeScript. `scat check --json` does not exist yet; see `JSON-CONTRACT.md`.

**It has never been run inside Obsidian.** Nobody could open Obsidian here. Only the build and the unit tests ran.

## Build and test

```
npm install        # or: npm ci
npm run build      # typecheck (tsc --noEmit) then bundle to main.js with esbuild
npm test           # vitest
```

Built and tested on Node v26.13.1 LTS. `main.js` and `node_modules` are git-ignored.

## Layout

- `src/main.ts`: lifecycle only (command, events, status bar, notice).
- `src/contract.ts`: types and tolerant JSON parsing. `src/group.ts`, `src/format.ts`: grouping, message and status text.
- `src/runner.ts`: injectable `Runner` (spawn without a shell) and `runCheck`.
- `src/view.ts`, `src/settings.ts`: the `ItemView` panel and the settings tab (the only files besides main that import `obsidian`).
- Modules other than `main.ts`, `view.ts` and `settings.ts` do not import `obsidian`; the tests cover them.

## Dev dependencies (npm registry only)

`obsidian` (type definitions), `typescript`, `esbuild` and `@types/node` are the sample plugin's own toolchain
(`@types/node` types `child_process`). `vitest`: the unit-test runner, chosen because it runs TypeScript with no extra setup.

## Not exercised

- That the plugin loads in Obsidian, or that the manifest is accepted.
- `ItemView` rendering, click-to-jump (`openFile` with `eState`), and the status-bar item.
- The events (`file-open`, `vault.on("modify")`, debounce) and whether they fire as documented.
- Spawning `scat` from Obsidian's process on macOS, where a GUI launch may not inherit the shell PATH (hence the path setting).
- A real `scat check --json` (the tool does not emit it yet), latency on a real vault, mobile, quick fixes, inline decorations.
