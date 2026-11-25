# Morning list for the chief engineer

Updated 24 November, late, after Mission Amendment 5 merged. Earlier versions are in git history. Nothing here blocks
the team; each item waits for you when you have a moment.

## Waiting on you

1. **A commit on `main` carries a line you asked to keep out of the public repo.** PR #8 merged as a merge commit,
   not a squash, so its branch's early commit `c58113b` (since corrected by `74e36ba`) is in `main`'s history.
   Removing it means rewriting `main` with a force-push, which only you can authorise. Leaving it is also fine; the
   current text is clean.
1a. **The same applies to commit `20ff07a` on `dev`:** WP14's first scope named six private repositories. The file is
   corrected (D-081); the names stay in `dev`'s history unless you choose a rewrite. Likewise one early log entry named a private
   repository; it is redacted in the file (D-082) and stays in history.
2. **Sign-ins for the chat-path spike (RS3), when it reaches live use:** inference.coop and GitHub in the browser
   pane. Use stays light and human-paced. I'll ask in chat when the spike is ready, not before.
2a. **Done: RS3's lab run worked end to end** (D-090). Tailscale stays installed and signed in; HTTPS and the Funnel
   policy stay enabled on your tailnet; Funnel itself is off and the lab MCP entry is deleted.
1b. **A guard refused a one-line schema edit (WP17-U3b, D-093).** `scat draw --out` can write a drawing outside the
   vault; the machine-interface schema lets only `export-edges` report such a path. Two ways on: (a) you allow the
   edit (add `draw` beside `export-edges` in `OperationResult`'s path rule), or (b) I rule that `draw` writes only
   inside the vault, as the chat path already keeps views there, and the code changes instead. Until then WP17 stays
   unaccepted; everything else in it is on `dev` and green.
2b. **Your template checkout will conflict on pull.** The migrated template on `dev` adds `bases: true` to
   `.obsidian/`; your uncommitted edits in `scat-kg-template/.obsidian/` (`core-plugins.json`, `app.json`) were left
   untouched, so a `git pull` there will stop on them. Commit, stash or discard them as you prefer before pulling.
3. **WP8-U1, held since D-042:** a test edit only you can authorise. (WP16 had to touch the file to drop a removed
   import; the held assertions are byte-identical.) Two assertions in `tests/ops/test_ops_stub.py`
   assert old behaviour (`stub` on an existing page of the same type is now a no-op; `set-status done` reports the
   page's check). The intended edits are as strong as before: `not r.ok` becomes
   `r.ok and r.unchanged == ("concern/a.md",)`, and the same-type refusal row becomes a different-type row. Fixes are
   on `wp8/u1`. WP16 will touch these files, so your "yes" or "no" decides whether it lands there.
4. **The uv gap (D-040, D-041):** UA-A ran with uv preinstalled, where the mission says "uv not installed". Accept it
   as a known gap, or permit one fresh tester to run uv's official installer at the next UA-A round (WP20).
5. **Paths in git history:** local paths are redacted from the files but remain in history; removing them needs a
   force-push. Your call, any time.
6. **At release:** submit the w3id namespace registration PR from your fork.

## Where the work stands

- **Mission:** Amendment 5 merged (0e74f19) with `GLOSSARY.md`; `dev` synced (D-076); revert point
  `divergence/D-076`.
- **Accepted:** WP12, the terms page (D-077).
- **Accepted since:** WP14, the prior-art readout (D-082). WP16's impact map and RS3's offline part are done.
- **In flight:** WP15, the architecture document and its review (D-083).
- **Next:** WP15 architecture document and review, with the chat-path spike (RS3) beside it; then WP16 ontology and
  layout. See `work-packages/plan.md`.
- **Hourly status reports** come in chat at about :07 past each hour.
