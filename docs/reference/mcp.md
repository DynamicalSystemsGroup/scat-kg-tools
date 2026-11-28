# MCP server reference

!!! tip "Your next step"
    To use it from a chat, read [The chat path](../chat-path.md). This page is for looking things up.

The MCP server offers the tool's operations to a chat or an agent. It is a front end to the tool, not part of it:
every tool below calls one operation of the Python package and returns that call's own data, unchanged. It holds no
authority, so it never sets a narrative to `done`. The two stage tools are the exception: they belong to the server.

## Starting it

The server is the `scat-mcp` command, in an optional extra of the package (`scat-kg[mcp]`). The core install does
not include it. The chat path's launcher runs it inside a container for you; you start it yourself only to try it.

| Setting | Meaning |
|---|---|
| `--vault PATH` or `SCAT_VAULT` | The vault folder. One server serves one vault, read afresh on each call. |
| `--host`, `--port` | The HTTP address. Defaults: `127.0.0.1`, `8765`. |
| `SCAT_MCP_KEY` | The key. When set, every HTTP request must carry it as `Authorization: Bearer <key>` or `X-API-Key: <key>`. |
| `--stdio` | Serve over standard input and output instead, with no key, for a local agent. |

The transport is streamable HTTP at the path `/mcp`. Without a key, the server serves HTTP only on the local
address and refuses to start on any other.

## Tools

Twenty-one tools. Nineteen are the operations; `which_stage` and `set_stage` are the stage tools (see [Stages](#stages)). Each returns the operation's own document. The three view tools `fingerprint`, `layered` and `trace` can return a picture, or both, instead (see [Drawings](#drawings)).

| Tool | What it does |
|---|---|
| `check` | Check the vault, one page, or a page and every page one link away. Writes nothing. |
| `status` | Show each page's status and the counts. Writes nothing. |
| `set_status` | Set a page to `stub` or `draft`. |
| `stub` | Create a stub page of a type, never a narrative's text. A contributor page only where the vault's attribution mode is `required` or `optional`. |
| `stub_links` | Create the node pages that links name and the vault lacks. |
| `record_edge` | Record an edge by adding its row to each narrative that tells it. |
| `remove_edge` | Remove an edge by deleting its rows from the narratives that tell it. |
| `merge` | Show the plan of folding node page `a` into node page `b`, two pages of one type: the files that would change, the links that would be rewritten, the `done` narratives whose text would change, or why it is refused. Writes nothing. Applying a merge (`plan` false) is refused, and the refusal names the coder's command, `scat merge a b`. |
| `split_plan` | Show what must be re-linked to split node page `a`: the narratives that link it, with every link and every `Edges told` row that names it. Lists no contributor page. Writes nothing. |
| `index` | Write the index page of each type that has none. |
| `fingerprint` | View: a narrative's fingerprint, or every narrative's. Takes `output` (`table`, `plot` or `both`) and `format` (`png` or `svg`). |
| `edge_table` | View: every edge of one type, with the narratives that tell it. |
| `layered` | View: the layered view of some narratives, or all. Takes `candidates` (also the links with no row; default false), `output` and `format`. The document lists the orphans (node pages no row tells) and, with `candidates`, each narrative with no account text, whose candidates say nothing about the text. |
| `trace` | View: follow edges up, down or both from a node. Takes `output` and `format`. |
| `evidence` | View: one node page's narratives with the paragraph around each link, its edges with the narratives that tell them, and its adjacent nodes. Reads no `attributed_to` and lists no contributor page. |
| `copy_share` | View: for each node page (or the one `node` named), the share of its text that repeats a narrative word for word, and the narratives it comes from, the most repeated first. The narratives named are those whose text the page repeats, whether or not they link the node. Reads no `attributed_to` and lists no contributor page. |
| `review` | View: pairs of node pages of one type that may be one node (overlaps, twin rows, shared adjacent nodes with hubs marked, link texts), and pages whose accounts tell them to different other ends, with the narratives grouped. A prompt to read, not a finding. Reads no `attributed_to` and lists no contributor page. |
| `attribution` | View: the narratives by contributor, and the narratives that name none. Refused where the attribution mode is `disallowed`. |
| `export_edges` | Write the three edge tables as CSV and Markdown into `views/`. |
| `which_stage` | Show the project's stage, who set it, the stage's work, tools and prompts, and each move out of it with whether its predicate holds now. Works in every stage. Writes nothing. |
| `set_stage` | Move the project to a stage, only when a person has said so. Takes `to` and `by`. Writes `lifecycle.toml` and nothing else. |

Every tool's description ends with the stages that offer it, for example `Stages: code, analyse.`, or `Stages: all.` The list of tools is the same in every stage and does not change between calls; a call the stage does not offer is refused (see [Stages](#stages)).

## Drawings

`fingerprint`, `layered` and `trace` each take two arguments besides their own (`fingerprint` and `layered` also take `candidates`, which draws the links with no row dashed):

- `output`: `table` (the default), `plot` or `both`.
- `format`: `png` (the default) or `svg`; it applies to the plot.

One call runs the view's query once and gives what `output` asks of that one result. `table` is the view's document, exactly what the tool returns without `output`. `plot` is only the picture `scat draw` and the notebook make for the same vault and arguments, byte for byte: a `png` is MCP image content, so a client shows or passes on the picture as it does any image, and an `svg` is the drawing's text. `both` is two items: the plot first, then the table as text, the JSON of the same document `table` returns. The plot and the table of one call tell the same nodes and edges, since both come from the one result.

These three tools declare no output schema, since a plot is not JSON: their table comes as text content, the JSON of
the view's document.

A drawing is never written to the vault. To keep a picture as a file, the coder runs `scat draw ... --out`, or saves it from the notebook.

A refusal is returned as the refusal document, as for every other tool, and no image, for every `output`: a name that is not a page, a narrative given to `trace`, a narrative that is excluded, a `direction`, `output` or `format` that is not offered, a plot of no narrative (or of every narrative) from `fingerprint`, which draws one narrative, a vault whose pages the view refuses (the document lists the problems), and a server without the `draw` extra (the document says how to install it). `fingerprint` as a `table` with no `narrative` still returns every narrative's view.

`draw_fingerprint`, `draw_layered` and `draw_trace` are not offered. Ask for the plot from the view tool: `fingerprint` with `output` set to `plot`, `layered` with `output` set to `plot`, and `trace` with `output` set to `plot`.

## Prompts and the rules

Six prompts, each citing `contracts/assistant.md`:

| Prompt | What it gives the assistant |
|---|---|
| `code-a-narrative` | The coding loop for one narrative, each step handed back to the coder. |
| `explain-a-problem` | How to explain a problem the tool reported, quoting it as reported. |
| `review-before-done` | A review of a narrative before the coder sets `done`. |
| `draft-a-node-page` | A draft of one node page as text in the reply, from the evidence view, across the narratives and citing them. You write it into the vault and set `done`. |
| `fill-in-node-pages` | The same for each stub node page in turn, one page per step, each handed back to you before the next. |
| `look-for-duplicates` | The possible duplicates and pages to re-read from `review`, one proposal per step, with the merge plan shown. You run the merge yourself, and each step is handed back to you. |

Each prompt's description also ends with the stages it belongs to. The prompt list is stable too, and a prompt is never refused.

The server offers these resources, all as text:

| Resource | What it gives |
|---|---|
| `scat://assistant-rules` | The assistant's rules. |
| `scat://guide/index` | The five stages, one line each, and every move between them. |
| `scat://guide/<stage>` | One stage's guide, for `plan`, `capture`, `code`, `analyse` or `report`. |

The guide resources carry the same text as `scat guide` and `scat_kg.guide()`. The server also sends the index as its instructions when a client connects.

## Stages

A project is in one stage at a time: `plan`, `capture`, `code`, `analyse` or `report`. A stage is where the project is in its lifecycle; it is not a page's status, and neither sets the other. The stage is kept for the whole vault, so it is the same in every chat and after a restart.

- **`lifecycle.toml`**, at the vault's root, holds `stage` and `set_by`; git keeps when. The server reads it afresh on every call. `set_stage` is the only writer, and it rewrites the file with these keys only: any other key or comment in it is not kept. `scat check` and `scat status` ignore the file.
- **No stage recorded.** The file is missing, has no `stage`, names something that is not one of the five stages, or cannot be read. Every tool except the two stage tools is refused, and the refusal names the five stages and says the person decides which one.
- **A call the stage does not offer.** The tool is refused, nothing runs and nothing is written. The refusal says the tool is not offered in this stage, names the stages that offer it, and says a move is the person's say-so.
- **`which_stage`** works in every stage. For each move out of the stage it gives the trigger, who decides, and whether the move's predicate holds now. A predicate the server can read from the vault (every narrative is `done` and the check has no errors) only advises. A predicate that only a person can say is shown as words.
- **`set_stage(to, by)`** records a move after the person has said so. `by` is the name the person gave; it is a signature, not proof of consent. Without `by` (missing, empty or blank) the call is refused and nothing is written: the person says so and gives the name to sign with. A stage that is not one of the five, the stage the project is already in, or a move the model does not list is refused, and the refusal names the stage's exits. A move whose predicate is read from the vault and does not hold is made and carries an advisory line; it is not blocked. From no stage, any stage may be named. An argument of the wrong type, such as a number for `to` or `by`, is rejected by the SDK's own argument check as an error result, like any other tool's.

The assistant never moves the stage itself. See [The chat path](../chat-path.md#stages) for how a coder uses this.

## What it refuses

A refusal is a result, not an error, and says what to do instead.

- **A call the stage does not offer**, or any call while no stage is recorded (see [Stages](#stages)).

- **A request without the key** gets HTTP status 401 with a short "unauthorised" message and nothing else, when a key is set.
- **`done`.** `set_status` refuses to set a page to `done` and refuses to move a page out of `done`. No other tool
  does either. The coder sets `done` in Obsidian. `record_edge` and `remove_edge` refuse a narrative that is `done`.
- **Paths outside the vault.** A page is named by its name or its path from the vault folder; anything else is
  refused ("no page has this name or path"). `export_edges` writes only inside `views/`, and refuses any other
  folder.
- **A narrative's text.** No tool writes it; the coder pastes it.
- **A node page's body.** No tool writes it either; `stub` creates a page with an empty body, and you write the text into the vault.

## The data is the tool's own

A result is the document the same call returns from the command line with `--json` or from Python. The server adds
nothing to it and takes nothing away. The two stage tools return their own documents, of kind `stage`. The fields are in the
[machine interface contract](https://github.com/DynamicalSystemsGroup/scat-kg-tools/blob/dev/contracts/machine-interface.md).
