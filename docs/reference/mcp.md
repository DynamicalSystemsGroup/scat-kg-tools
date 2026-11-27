# MCP server reference

!!! tip "Your next step"
    To use it from a chat, read [The chat path](../chat-path.md). This page is for looking things up.

The MCP server offers the tool's operations to a chat or an agent. It is a front end to the tool, not part of it:
every tool below calls one operation of the Python package and returns that call's own data, unchanged. It holds no
authority, so it never sets a narrative to `done`.

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

Nineteen tools. Each returns the operation's own document.

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
| `fingerprint` | View: a narrative's fingerprint, or every narrative's. |
| `edge_table` | View: every edge of one type, with the narratives that tell it. |
| `layered` | View: the layered view of some narratives, or all. |
| `trace` | View: follow edges up, down or both from a node. |
| `evidence` | View: one node page's narratives with the paragraph around each link, its edges with the narratives that tell them, and its adjacent nodes. Reads no `attributed_to` and lists no contributor page. |
| `copy_share` | View: for each node page (or the one `node` named), the share of its text that repeats a narrative word for word, and the narratives it comes from, the most repeated first. The narratives named are those whose text the page repeats, whether or not they link the node. Reads no `attributed_to` and lists no contributor page. |
| `review` | View: pairs of node pages of one type that may be one node (overlaps, twin rows, shared adjacent nodes with hubs marked, link texts), and pages whose accounts tell them to different other ends, with the narratives grouped. A prompt to read, not a finding. Reads no `attributed_to` and lists no contributor page. |
| `attribution` | View: the narratives by contributor, and the narratives that name none. Refused where the attribution mode is `disallowed`. |
| `export_edges` | Write the three edge tables as CSV and Markdown into `views/`. |

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

The server also offers one resource, `scat://assistant-rules`, the assistant's rules as text.

## What it refuses

A refusal is a result, not an error, and says what to do instead.

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
nothing to it and takes nothing away. The fields are in the
[machine interface contract](https://github.com/DynamicalSystemsGroup/scat-kg-tools/blob/dev/contracts/machine-interface.md).
