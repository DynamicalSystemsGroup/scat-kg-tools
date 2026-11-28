# Record: what each path's model can see in a drawing (WP36)

No new run. This record gathers the two existing runs that settle what a model receives from a drawing, and says what
each claim on `docs/path-pros-and-cons.md` and `docs/analysis.md` rests on (D-197: the IDE and local LLM paths are not
run here; their rows describe our side of the interface).

| Claim on the pages | Source record | What it shows |
|---|---|---|
| In Claude, the model receives the PNG a tool returns and can describe it. | `mvc-loop-claude.md`, step "View" and Findings | Claude (claude.ai, Opus 5.5) described the picture itself: nodes, statuses, legend, the lines, and the absence of a link between two columns, with no text view called. |
| In inference.coop's chat, the model receives nothing from a PNG; the person sees it. | `analysis-session-inference-coop.md`, turn 9 and "Learnings" | Asked "can you not view the images?", `tinfoil/deepseek-v4-1-flash` said it cannot see them; the tool result reached it as nothing. |
| In inference.coop's chat, the model reads an SVG as text. | the same, turns 9 and 10 | With SVG it read the drawing as text, labels and path coordinates; the chief engineer: "svg is a fine output". |
| Leave no trace: same as inference.coop's chat. | the same | That path's walkthrough uses inference.coop's chat; no separate run. |
| Show with PNG; SVG to save (D-170) or for a model to read as structure (the chief engineer's "Learnings"). | D-170; `analysis-session-inference-coop.md`, "Observations" and "Learnings" | The model chose SVG unasked and nothing was shown as a picture. |
| The table is the companion of every figure. | D-172; `docs/reference/mcp.md`, "Drawings" | One call returns the plot, the table or both from one query (`output`, `format`, WP33). |
| IDE and local LLM rows: what our side returns. | `docs/reference/mcp.md`, "Drawings"; `docs/reference/cli.md`, `scat draw` | A PNG as MCP image content, an SVG as text, the table as JSON text; `scat draw --out` writes a `.png` or `.svg` file. No client trial (D-197). |

The earlier line in `analysis-session-inference-coop.md` that Claude's model was not tested is settled by `mvc-loop-claude.md`.

Not claimed: that other models on either platform behave the same (each run is one model), or that any other chat, IDE or local model does or does not receive an image.
