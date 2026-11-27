# Analysis in practice: what the figures show a coder (27 November)

The ACE drew the figures of the chief engineer's inference.coop session again at full size from the lab vault
(`my-vault`: three narratives, two events) and read them as a coder would, asking what each answers and where it sends
the coder next. Input for WP29 (the analysis stage and its moves) and WP30 (the analysis guide and the drawing tools).

## What each figure answers

- **Layered view (the whole vault): "what is the shape of what we heard?"** It showed two islands that share no node:
  the market (three groups, four concerns, four affordances, four technologies) and the community fridge (two groups,
  two concerns, two affordances, two technologies). In a real vault, separate islands mean separate domains or a missing
  bridge; the coder decides which. Crossing lines (nodes in alphabetical order) make the fan hard to read; whom an edge
  came from is not shown.
- **Fingerprint (one narrative): "did I code what this account tells?"** The fridge note's fingerprint is two
  unconnected pairs (group→concern, affordance→technology) with an empty middle: nothing addresses food spoilage or
  trust. The note itself says the dated whiteboard and the clear-out rota address food going off, so the gap is
  uncoded, not untold. That is the clearest Analyse → Code trigger seen: the picture pointed at a sentence.
- **Trace (one node): "who wants this, and does it reach anything?"** A group traced down that stops at its concerns
  (mutual-aid-group → food-spoilage, then nothing) is an unmet need in the vault as coded. An affordance traced up
  (whiteboard-at-gate → fair-to-newcomers → market-committee) is the justification path. A concern traced both ways
  (keep-usual-place: stallholders above; numbered-places, then two technologies below) is a complete chain, and two
  technologies under one affordance show redundancy.

## Reading a gap depends on the narrative's kind

A scenario tells groups, concerns and affordances; an architecture tells concerns, affordances and technologies (the
home page). So in a scenario's fingerprint an empty technology column is expected (stories-about-a-market-morning), and
in an architecture's a group with no line is expected (numbered-pitches: market-committee alone). Both chat assistants
read these as gaps. The analysis guide must teach kind-aware reading, and the drawing could show it (for example the
layers a kind does not tell drawn as not expected).

## What the figures hide

- **Pages with no row.** The fridge vault has a `whiteboard` technology page (a stub) that no row tells, so it is in no
  figure. Orphan pages are invisible in every view.
- **Candidate links** (links the text names with no row) are not drawn by default; the assistant listed them from text.
  The fingerprint has a candidates option; the guide should use it when revisiting.
- **Near-duplicates.** `whiteboard` (technology, fridge) and `whiteboard-at-gate` (affordance, market) are different
  nodes by layer, and the figures cannot say whether a coder meant them as one thing seen two ways; `review` can.

## Where a figure sends the coder (moves out of Analyse)

| Seen in a figure | Move | Who decides |
|---|---|---|
| A gap the account's text names (a candidate link) | Analyse → Code: record the edge | the coder |
| A page in no figure (an orphan) | Analyse → Code: link it or remove it | the coder |
| Two nodes that may be one | Analyse → Code: `review`, then a merge plan | the coder |
| An unmet concern no account answers | Analyse → Capture or Plan: ask in the next session | the organiser |
| An island, or a layer a kind does not tell | No move: read it as the kind and the domains say | the coder |
| A whole picture the coder accepts | Analyse → Hand over (report out) | the coder |

## Every figure with its table

The chief engineer: "any figure generated can be matched with a set of tables containing explicit nodes and edges",
and "it's also worth ensuring every image we can generate has an associated data dump method that returns its nodes
and edges which could be viewed as a table". Each drawing already has its view (`draw_fingerprint` ↔ `fingerprint`,
`draw_layered` ↔ `layered`, `draw_trace` ↔ `trace`), and WP28's tests hold the drawn nodes and lines equal to the
view's. Missing: the pairing in one place. Today the picture and the table are two calls, and the assistant gave one
without the other. Options for WP29/WP30: each drawing tool returns its nodes and edges beside the image in the same
result; a test that every drawing has a table twin (and any new drawing must ship one).

## Drawing improvements seen (candidates, not scoped)

Order nodes to cut crossings; separate islands; mark edges by the narrative that tells them; show candidate links as
dashed; list orphan pages beside a figure; show which layers a narrative's kind does not tell.
