# Notes: the chief engineer's analysis session in inference.coop (27 November)

One conversation, chat.inference.coop, model `tinfoil/deepseek-v4-1-flash` (the chat's default, no saved agent, no
skill), the SCAT server from SCAT Chat (tools `dev` a2f089c, with the drawing tools) on the lab vault `my-vault`. The
chief engineer sent prompts 3 and 5; the ACE sent prompt 1. Read by the ACE from the screen and the page text;
screenshots in the sitting's evidence folder (`r5/`), outside the repository.

## What happened, turn by turn

1. **"Use the SCAT tools to draw the layered view of my whole vault and show me the picture."** One tool call
   (`draw_layered`); the PNG shown inline under the call. The model also wrote its own markdown image link, shown as a
   broken placeholder. Its reading was careful: it named every node by layer, noted that nearly all are stubs, and
   quoted the drawing's footer ("a line is an edge a row of a drawn narrative tells") to say an absent line is an
   untold link, not an absent one. It declined to trace crossing lines by eye and offered the text view.
2. **"show me some fingerprints and some traces"** (his). Eight tool calls. It asked for the drawings as **SVG**, so
   none was shown as a picture, then said "what the draw tools returned here is the SVG source … not a rendered bitmap
   this channel can display", which is true of SVG but wrong as a statement about the channel (the PNG in turn 1 was
   shown). It answered with tables: three fingerprints and two traces, each read against the text views, with the
   candidate links (links with no row) listed. The readings checked out against the views: lab-note-community-fridge
   tells no addressed-by row; numbered-pitches tells no holds row, so market-committee stands alone; stories tells no
   provided-by row; the two traces stop where G12 says.
3. **"i wanted the plots not the tables though since these are graphs any figure generated can be matched with a set
   of tables containing explicit nodes and edges"** (his). Six tool calls, now PNG: six figures shown stacked (the
   whole-vault layered view, three fingerprints, two traces), then one paragraph per figure pairing it with the table
   given before, and the caveat that a gap is an untold link, not an absent one.

## Observations for the next packages

- **Pictures first.** Asked for "fingerprints and traces", the model gave tables; the chief engineer wanted the plots,
  with tables as the explicit companion ("any figure generated can be matched with a set of tables containing explicit
  nodes and edges"). The analysis guide (WP30) should lead with the drawing and pair it with its table, not the other
  way round.
- **Format.** The model chose SVG unasked and then could not show it. Show with PNG; SVG only to save (D-170).
- **No re-embedding.** It re-embedded a tool's image as its own markdown link (a broken placeholder).
- **True statements about the channel.** "Not a rendered bitmap this channel can display" was a wrong general claim
  (WP31-G1, true reports).
- **Good habits seen, worth keeping in the guide:** reading only what the drawing shows, refusing to trace crossings by
  eye, naming the footer's caveat, pairing each figure with its explicit nodes and edges, listing candidate links as
  the coder's call ("Whether any of those unrowed links should be rows is the coder's call").
- **Legibility at chat width.** Stacked in the chat column the figures are narrow and node labels are small; whether a
  click enlarges them was not checked. A question for WP30 (figure size, or one figure per reply).
- **No skill or agent was used** in this session; the behaviour above is the model with the server's tool descriptions
  only. That is a useful baseline for WP30: what the server alone gets right and wrong.

## Turns 7 to 14 (read later the same afternoon)

7. **The chief engineer, on the model's caveat** ("a line means a row a narrative tells … the candidate lists … are
   where those live"): "this is precisely why we expect a feedback loop between analysis and coding. this is in essence
   an MVC loop where the views inform exercise of the available controls". The model mapped it: model (node pages, and
   edges only as rows), views (everything that writes nothing: the draw tools, fingerprint with candidates, layered,
   trace, edge tables, evidence, copy-share, review), controls (record and remove an edge, stub, set status, index). It
   noted the controls are partial in its hands (no `done`, plan-only merges), so on a `done` narrative the loop closes
   only after the coder moves it back to `draft`.
8. **"suggest to me some potential revisions in the coded data based on the visualizations"**: six calls, grounded in
   `review`, the edge tables, `layered` and `check`. It separated what the tools report (two merge candidates:
   painted-ground-numbers and printed-plan-at-gate at Jaccard 1.0, which it read as plausibly one; fair-to-newcomers and
   not-decide-every-week at 0.5, which it read as distinct; two missing fields that block `done`) from its own readings
   (the two fridge concerns are dead ends in the whole vault; whiteboard-at-gate is the only affordance with no
   technology; market-committee is attached in one narrative and not the other; one concern linked under two phrasings).
   It named the one edit it could make without a demotion and left the interpretation to the coder. Its "dead end"
   reading did not account for the scenario's kind (D-172).
9. **"can you not view the images?"**: the model said it cannot see them. With PNG the tool result reached the model as
   nothing (the chat showed the picture to the person, not to the model); with SVG it read the drawing as text (labels
   and path coordinates). It corrected its earlier "this channel can't display a bitmap" as a guess stated too firmly.
10. **The chief engineer**: "svg is a fine output. we should record that as a learning. we also need to note that this
    platform currently lacks visual inspection capabilities. that is OK but it is something we need to note as compared
    to the alternativs". The model noted the vault has no page type for a learning (rightly: the graph models the
    domain, not the tooling) and offered wording for a separate note.

## Learnings recorded here (the chief engineer's)

- **SVG is a fine output**: the model can read it as structure (which node, which line), and it renders as a figure
  when saved.
- **inference.coop's model does not see images**: the chat shows a PNG to the person, but the model receives nothing
  from it; Claude, by contrast, shows the image and can look at it. This is a difference between the paths to state
  beside the others (the pros-and-cons page).
