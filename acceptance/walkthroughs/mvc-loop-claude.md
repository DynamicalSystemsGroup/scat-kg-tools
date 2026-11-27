# Run record: the analysis-to-coding (MVC) loop in Claude (27 November)

Asked by the chief engineer before shutting the session down: "test the MVC loop with claude chat where you should be
able to "see" the images". claude.ai, Opus 5.5, no skill loaded for this chat, the SCAT connector (`x-api-key`) to SCAT
Chat on the lab vault; the ACE as coder (his rule for chat-app runs). Screenshots in the sitting's evidence folder.

| Step | Sent | What Claude did |
|---|---|---|
| View | "Draw the fingerprint of … lab-note-community-fridge as a PNG, and tell me what you see in the picture itself. Don't call the text views yet" | One call (`draw_fingerprint`, png). Described the picture itself: title and its stub tag, all 8 nodes with statuses, the legend, four solid lines, and visual facts no table holds ("all horizontal, with no fan-in, fan-out or crossings"). Found the gap: "Nothing links the concern column to the affordance column". Listed what the image cannot tell (direction, evidence, whether the gap is omission or untold) and left that to the coder. **Claude's model receives the image** (inference.coop's did not). |
| View with candidates | "Redraw it with candidates, and tell me what the picture adds." | Read 8 dashed lines from the picture, by column gap, and noticed they are the full complement of the coded edges: "I suspect it comes from listing every unlinked adjacent pair rather than from anything specific in the narrative … the candidates show where links are possible, not which ones the text supports". Right: this narrative has no account text, so its only links are the rows, and the candidate rule cannot discriminate. |
| Control | The coder's call, from the field note: food-spoilage is addressed by donation-tracking; record it and redraw | `record_edge`, reported as the tool returned it (row added at line 16; nothing created, unchanged or refused); `draw_fingerprint` again; described the change in the picture: one new solid line, and an unbroken path across all four columns (mutual-aid-group → food-spoilage → donation-tracking → community-fridge). Handed back a doubt without resolving it (the note says the volunteers worry about food, but food-spoilage hangs off mutual-aid-group), suggested the empty note cell, and named the coder's next act. The vault shows the row. |

## Findings

- The loop works end to end in Claude: view, the coder's decision, control, view again, with the change visible.
- Claude sees tool images; inference.coop's model does not (`analysis-session-inference-coop.md`). A difference
  between the paths for the pros-and-cons page (proposal WP36), now settled.
- Candidates are uninformative on a narrative with no account text (every adjacent pair is a candidate). For WP34 and
  the analysis guide: candidates mean something once the account is written; with no text, say so.
- The model could have set the note when recording (`record_edge` takes one); it suggested the coder edit it instead.
  For WP31: offer the note in the record call when the coder gave the reason.
- Habits already right here, with no skill loaded: reporting tool results as returned, handing back an interpretive
  doubt, naming the coder's next act.
