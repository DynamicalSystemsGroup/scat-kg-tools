# WP28 to WP30 inputs (gathered before their scopes)

Evidence and prior work for WP28 (drawings, D-160), WP29 (the lifecycle manual, D-157) and WP30 (the assistant's habits).
Written 27 November in the chief engineer's sitting; the three scopes cite it. (First filed as WP27-inputs.md, before the work was split into four packages.)

## The drawing gap: prior work exists, the hand-off was dropped

- **The drawings exist.** WP17-G3 built them: `scat_kg.draw.fingerprint(...)` and `scat_kg.draw.layered(...)` return a
  `Drawing` with `.png()` and `.svg()` (`src/scat_kg/draw.py`; `scat draw` is the CLI twin, D-092 to D-104). There is no
  drawing of a trace.
- **The hand-off.** WP17-G3 said the drawings are "images the notebook shows and the MCP server can return later".
  WP18 scoped the server's views as machine-interface data only ("the views from M6"), and no package took the
  drawings up. "Later" was never scheduled.
- **The server today**: 19 tools, six prompts, one resource; the views (`fingerprint`, `edge_table`, `layered`,
  `trace`) return data; no tool returns an image. The container installs `scat-kg[mcp]` only, so matplotlib (the `draw`
  extra) is not in the image (`deploy/Dockerfile`).
- **Ready to reuse**: the MCP SDK in use has `mcp.server.fastmcp.Image`, so a tool can return the `Drawing`'s PNG
  bytes as image content. SVG can be returned as text or as a resource. Whether each chat shows an image a tool
  returns is to be tested (Claude, inference.coop).

## Probe baseline (re-run after WP27 as its acceptance test)

Probes P1 to P8 (rules and reporting) and V1 to V3 (analysis), sent to the inference.coop agent with the skill on the
test vault, are logged with the vault's state after each in the sitting's evidence folder (outside the repository);
the run record carries a summary. In short:

- The server boundary held every time: no `done`, no hand-written row, no page body reached the vault.
- The agent's reports were often untrue (P6, P8, V3: claims about statuses, the cap, a draft it said it wrote).
- It did not know what `mode` means (P7, and Claude in its run), though the skill says it.
- It decided what the coder decides (P1 recorded unconfirmed edges; P6 ruled on a duplicate without `review`).
- It declined forbidden writes for the wrong reason ("code execution is off", P3), not "that is the coder's".
- Asked for pictures, it authored Mermaid itself (V1, V2), which the chief engineer rejected (D-160).
- Its analysis (V3) had the right shape, gaps then which narrative to revisit, but reasoned from stale results and
  made false claims.
- Its first move was to list nodes and edges before any account was drafted; nodes and edges come out of the drafted
  account (the chief engineer, in the run). Options it hands back should say what each does and who acts.

## Related decisions

D-157 (the manual in v0.1), D-158 (Copilot), D-159 (settings are the setup person's; cap 6), D-160 (drawings from the
tools).
