# Analysis

!!! tip "Your next step"
    In your vault folder, run `uv run jupyter lab analysis.ipynb`, then choose **Run**, then **Run All Cells**.

A **view** is a purposeful picture or table made from a conformant vault. The tool generates it. You interpret it: a view never says that a story, a group or an architecture is better.

## Before you trust a view

- `uv run scat check` passes. A view refuses on any error in the pages it draws, and on any row of them that tells no edge, and says which.
- You have signed off the content (`done`). A view of `draft` pages shows the draft.

## The four views

**Fingerprint.** What does this narrative touch? It shows the nodes the narrative links and the edges it tells, in columns, one for each layer. The columns follow the narrative's kind: an architecture has concern, affordance and technology, with no stakeholder column; a scenario has stakeholder, concern and affordance, with no technology column; a narrative with no kind has all four. A missing column is the kind's, not a gap in the coding; a note under the drawing says which column is not drawn and how many linked nodes of that layer it leaves out. It does not mean the narrative is complete or wrong.

**Edge table.** Which edges of one type exist, and who tells them? Read it as a table, one row per edge. Exported as CSV, it feeds documents. It does not rank the edges.

**Layered view.** What is the big picture across several narratives? It joins their fingerprints in the four layers. Read across a column to see what is shared. It does not weigh a node by how many lines meet it.

The picture hides three things, and the view shows each. **Orphans:** a node page that no row tells has no line, so no column shows it; the view names it in the footer (at most ten, then "and N more") and lists it in the table, whichever narratives you chose. **Candidates:** a pair of nodes that the account links, with no row joining them, has no line either; with `candidates`, the picture draws it dashed and the table lists it, so you see what is left to code.

![The layered view of four narratives, as four columns: groups, concerns, affordances and technologies, with a line for each edge between neighbouring columns.](assets/layered-case-study.png)

**Trace.** What does this node reach? Following edges up goes toward groups, down toward technologies. It does not say how strongly a node depends on what it reaches.

Two more views serve the node pages. **Evidence** (`scat evidence <node>`) shows every narrative that links one node, with the paragraph around each link, its edges and its adjacent nodes: read it before you write the page. **Copy-share** (`scat copy-share`) shows, for each node page, how much of its text repeats a narrative word for word, and which narratives. A high share is a prompt to look at the page, not a fault. **Review** (`scat review`) lists node pages of one type that may be one node, and pages whose accounts tell them to different other ends; both are prompts to look, not findings.

## The notebook

The vault template holds `analysis.ipynb` at its root. It shows each view with a short paragraph and exports the three edge tables. Its tools are already installed: the one setup command, `uv sync`, installs JupyterLab and what the notebook needs, so there is nothing more to install. Run it from your vault folder, in Terminal:

```text
uv run jupyter lab analysis.ipynb
```

JupyterLab opens the notebook in your browser and keeps running in Terminal until you press Control and C there. In the browser, choose **Run**, then **Run All Cells**, then read. A cell that stops with an `AssertionError` means the picture and the pages disagree: run `uv run scat check`. If the browser does not open, copy the address that starts `http://localhost:` from Terminal into it.

To get the finished notebook as a page to read, with no browser tab to keep open, run it from Terminal:

```text
uv run jupyter nbconvert --to html --execute analysis.ipynb --output-dir executed
open executed/analysis.html
```

The first command runs every cell and writes `executed/analysis.html`; the second opens it. The `executed` folder is ignored by git, as is `exports`, where the edge tables are written.

The same views are one call away in the REPL and one command away on the CLI:

```python
import scat_tools

scat_tools.fingerprint("groups-under-a-cap-pitch")
scat_tools.edge_table("holds")
scat_tools.layered()
scat_tools.trace("anonymity", "up")
```

```bash
uv run scat fingerprint groups-under-a-cap-pitch
uv run scat edges holds
uv run scat layered
uv run scat trace anonymity --direction up
uv run scat export-edges --out exports
```

A view's data is the same in the notebook, the CLI and in chat.

## Drawings

Drawings need the extra `draw`: `pip install "scat-tools[draw]"`. In the vault template it is already installed.

```python
from scat_tools import draw

draw.fingerprint("groups-under-a-cap-pitch").save("fingerprint.png")
draw.layered().save("layered.png")
```

Both `draw.fingerprint` and `draw.layered` take `candidates=True` (CLI: `--candidates`), which adds the candidates as dashed lines. A drawing is made from a view's result. To have the picture and the table from one query, run the view once and draw that result: `draw.render(scat_tools.layered())`.

Within each column, a drawing orders the nodes to reduce the number of crossing lines, not alphabetically; the order is the same every time for the same vault. Parts of the graph that share no node are drawn as separate bands, one above the other, largest first; the nodes that no line reaches are together in the last band. A drawing with one connected part and no node that no line reaches is one band. Read each band on its own: nothing in one band is joined to anything in another.

In the layered drawing the lines can be marked by the narrative that tells each edge. From Python, call `draw.layered(mark_narratives=True)`, or `draw.render(result, mark_narratives=True)` for a result you hold. It is off by default. There are nine marks, three colours by three line styles, chosen to be told apart by colour-blind readers, and each narrative that tells a drawn edge takes the next one in name order; with ten or more narratives the marks repeat, so two narratives can share a mark; an edge that several narratives tell has one shared mark; a key under the drawing names each narrative that tells a drawn edge. Dashed lines still mean candidates. The command line and the chat tools do not offer this option.

Every drawing labels its columns stakeholder, concern, affordance and technology, in that order. A fingerprint drawing follows its narrative's kind and leaves out one column (see Fingerprint above); the layered and trace drawings mix narratives and keep all four. SVG and PNG are the same drawing in two formats.

In chat, the tools `fingerprint`, `layered` and `trace` each take `output`: `table` (the default), `plot` or `both`. A plot comes as `png` (the default) or, with `format`, as `svg`. One call asks the vault one question and returns the picture, the table or both, and they always agree. In `both`, the picture comes first, then the table. `fingerprint` and `layered` also take `candidates`. Ask for one by naming the view and what it shows, for example "plot the fingerprint of groups-under-a-cap-pitch". A plot of a fingerprint needs the name of one narrative. The picture comes back in the chat and is not saved in your vault. If your chat does not show the image, ask for `format` svg, which returns the plot as text, or for the table, or save the picture from Terminal with `uv run scat draw fingerprint --out fingerprint.png NARRATIVE`, or from the notebook. A name the vault does not have, or an error in the pages drawn, comes back as the same refusal the CLI gives, with what to do.

### When the assistant cannot see the drawing

Not every assistant's model receives the picture. In claude.ai the model received it in the recorded run; in inference.coop's chat you see the PNG and its default
model received nothing from it (see [Pros and cons](path-pros-and-cons.md#what-the-model-sees-in-a-drawing)). If you are not sure,
ask it whether it can view the images. Then choose by what you need:

- **The table.** `output` `table` (the default) gives every node and edge the drawing shows, as text. Ask for it when the
  model is to read or check the result, since a drawing is only the table's picture.
- **The plot.** `output` `plot` gives only the picture.
- **Both.** `output` `both` gives the picture for you and the table for the model, from one query, so they agree.
- **SVG.** `format` svg returns the plot as text, which a model reads as structure: which node, which line. Saved, it is a figure you can open.
- **PNG.** The default `format`. Use it to show a drawing to a person; it is the one to look at.

Show with PNG; use SVG to save a drawing or for a model to read as structure.

## Where next

- [Python API](reference/api.md) and [CLI](reference/cli.md): every call and command.
- [Terms](reference/terms.md): the words used here.
- [Coding](coding.md): back round the loop, where a view sends you.
