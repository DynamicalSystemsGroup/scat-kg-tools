# Proposed packages from the 27 November analysis session (not scoped)

Drawn from `acceptance/walkthroughs/analysis-session-inference-coop.md` and `analysis-in-practice.md`, and the chief
engineer's words recorded in D-160, D-172 and the session notes. Each has one purpose and a narrow blast radius. Already
queued and unchanged: WP29 (design of the stage model), WP30 (implementation), WP31 (the assistant's habits), the
glossary cleanup (after WP29).

| Proposed | Purpose | Blast radius | Order |
|---|---|---|---|
| WP32 | Fingerprints follow the narrative's kind (architecture: no stakeholder column; scenario: no technology column; none: all four), and every drawing's columns read stakeholder, concern, affordance, technology (D-172) | `src/scat_kg/draw.py`, its tests, the docs that show a drawing's column names | first; independent |
| WP33 | Each drawing comes with its table: a drawing tool's result carries the drawing and its nodes and edges, so the person sees the picture and the model, which may not see images (inference.coop), can read the same thing exactly | the server's three drawing tools, their tests, `docs/reference/mcp.md` | parallel with WP32 (different files) |
| WP34 | What the figures hide, shown: candidate links (named in the text, no row) drawn dashed when asked; pages no row tells listed beside a figure | `src/scat_kg/views.py` (orphans), `draw.py`, tests | after WP32 (same file) |
| WP35 | Legible layouts: nodes ordered to cut crossings, islands drawn apart, an edge marked by the narrative that tells it | `draw.py` layout only, tests | after WP34 (same file) |
| WP36 | The paths' visual capabilities on the pros-and-cons page: what the person sees and what the model receives on each path, and SVG as the form a model can read; needs one short trial of whether Claude's model receives a tool's image | `docs/path-pros-and-cons.md`, `docs/analysis.md`, a run record | parallel; one trial with his keys |

Inputs for WP29's design rather than packages: the chief engineer's MVC framing ("this is in essence an MVC loop where
the views inform exercise of the available controls"): Analyse is the views, Code the controls; moving a `done`
narrative back to `draft` is the coder's transition that reopens the controls; `review`'s merge candidates and `check`'s
missing fields are analysis outputs that send the coder back to Code.

Candidate for later: a place for the organiser's session notes and learnings outside the graph (the model noted the
vault has no page type for one, rightly: the graph models the domain, not the tooling).
