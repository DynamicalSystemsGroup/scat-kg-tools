# SCAT plugin source (RS1-U3)

Source and tests of the Obsidian plugin. The installable folder is `../dist/scat/`; read `../README.md` to install it.

```
export PATH=$HOME/.local/opt/node-v26.13.1-darwin-x64/bin:$PATH   # this machine only: /usr/local/bin/node is broken
npm ci
npm run build       # tsc --noEmit, then esbuild to main.js
npm test            # vitest: unit tests plus an end-to-end test that installs the package into a scratch vault
npm run test:py     # pytest: runs scat_json.py in a scratch copy of the template (needs uv)
npm run package     # build, then copy main.js, manifest.json, styles.css, scat_json.py to ../dist/scat
```

- `src/main.ts` lifecycle only. `src/contract.ts` tolerant JSON parsing. `src/runner.ts` builds and runs the `uv run` command.
  `src/paths.ts` finds uv and maps a problem's file to a vault path. `src/format.ts`, `src/group.ts` text and grouping.
  `src/view.ts`, `src/settings.ts` panel and settings. Only `main.ts`, `view.ts`, `settings.ts` import `obsidian`.
- `scat_json.py` is the shim. `JSON-CONTRACT.md` is its output.
- The end-to-end and shim tests read the template at `$SCAT_TEMPLATE` (default `~/Documents/GitHub/scat-kg-template`) and write
  only under `$SCAT_RS1_SCRATCH` (default `scat-rs1` in the system temp folder). They skip when uv or the template is missing.
- Dev dependencies, npm registry only: `obsidian` (types), `typescript`, `esbuild`, `@types/node`, `vitest`.
