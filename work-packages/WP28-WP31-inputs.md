# WP28 to WP31 inputs (gathered before their scopes)

Evidence and prior work for WP28 (drawings, D-160), RS5, WP29 and WP30 (the lifecycle as a state machine and the manual, D-157, D-162) and WP31 (the assistant's habits).
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

## ACE addendum to RS5's readout, for WP29 (27 November)

The ACE re-read the 2026-07-28 tools page at source: "MUST NOT vary per-connection or as a side effect of other
requests on the connection. The set MAY vary by the authorization presented on the request — for example, returning
only the tools the caller's granted scopes permit — since credentials are per-request input, not connection state."
The readout carries the exception (G4, Appendix D) but does not list it among Q2's carriers. WP29 should weigh it:
**stage carried as authorization**, a per-stage key or a key scoped to a stage, issued by SCAT Chat. It is legal in
both spec eras, sits close to the chief engineer's "header for messages to the mcp server to carry stage", and bears on
Q11 (the stage word's authority), since only the coder pastes a key. Its costs (a key per stage, or re-issuing a key
to move stage; how each chat holds several connectors) are for WP29 to weigh, and the client trials can try it.

## Input for WP29: a structure-aware commit at hand-over (the chief engineer, 27 November)

Asked whether the WP27 guard denial was the development environment or the app (it was the development environment:
Claude Code's auto-mode classifier on the build agents), the chief engineer said (typed by the agent): "if its our app
then we should probably provide explicit tools with git commit, but we are committing to repos we know are templated so
we can create narrow commands and checks that the applicable rules are passed before committing. between stages within
the session, the template structures, and the page status, we should have all the structure we need for clean
contextually relevant and contextually enforced rules". Asked where it goes: "Into WP29's design". WP29 designs a
structure-aware commit as a stage tool (staging only the vault's template paths, never `.obsidian/` churn or stray files;
running the checks the stage requires and refusing if they fail; still the coder's act, which the assistant may propose
but not run). Evidence: V1 (a first `git add .` swept Obsidian's files in). Implementing it needs an amendment to WP30's
scope once the design lands.

## From WP28-R5's on-screen run (27 November)

Both Claude and inference.coop show a PNG the server returns. In inference.coop the model also re-embedded the picture
as its own markdown image (a broken placeholder), and on a second request it chose SVG, which a chat shows as text, not
a picture. For WP30's analysis guide and WP31's habits: ask for PNG to show, SVG only to save; never re-embed a tool's
image. Claude: `authorization: Bearer <key>` fails to connect twice; `x-api-key` works.

## From the chief engineer's analysis session in inference.coop (27 November)

See `acceptance/walkthroughs/analysis-session-inference-coop.md`. For WP30's analysis stage: lead with the drawing and
pair it with its table of explicit nodes and edges (his words: "any figure generated can be matched with a set of
tables containing explicit nodes and edges"); PNG to show; figure legibility at chat width. For WP31: no re-embedding,
no wrong claims about what the channel can show. Baseline: no skill or agent, the server's tool descriptions only.

## Analysis in practice, and every figure with its table (27 November)

See `acceptance/walkthroughs/analysis-in-practice.md`: what each figure answers, kind-aware reading of gaps, what the
figures hide (orphans, candidates, near-duplicates), the moves out of Analyse (to Code, Capture or Plan, Hand over),
and the chief engineer's ask that every image have a data dump of its nodes and edges viewable as a table (each view
already is one; the pairing in one result is missing). For WP29's transitions and WP30's analysis guide and tools.

## For WP29: the MVC loop (27 November)

The chief engineer, in the inference.coop session: "this is precisely why we expect a feedback loop between analysis
and coding. this is in essence an MVC loop where the views inform exercise of the available controls". Analyse is the
views (everything that writes nothing), Code the controls; moving a `done` narrative to `draft` is the coder's
transition that reopens them; `review`'s merge candidates and `check`'s missing fields are analysis outputs that send
the coder back to Code.

## For WP29: two lifecycles, not one (27 Nov, during RS5's client trials)

The chief engineer (typed by the agent): "i am worried we're mixing the two abstraction levels. the lifecycle from the
facilitators view is not the same as the lifecycle for a page". Where the drafts mix them: WP29-G2's backward moves list
"Analyse to Code; `done` to `draft`" side by side, as if both were stage transitions; the MVC note above calls "moving a
`done` narrative to `draft`" "the coder's transition that reopens the controls"; and RS5's router spike gates plan to
code on one successful `stub`. A page's status (`stub`, `draft`, `done`) is a per-page lifecycle the tool already
enforces; the organiser's stages are the work's lifecycle. Open for WP29: how the two relate.

## For WP29: rules by stage (D-178)

Shared tools across stages; drawing tools in coding (the visual loop is part of coding); analysis draws and
synthesises but does not edit existing content; stages are the human's work, aided by the assistant; a review-and-revise
loop for every piece of content at every stage. The MVC note above ("Analyse is the views, Code the controls") is
superseded where it implies the views belong to analysis only.
