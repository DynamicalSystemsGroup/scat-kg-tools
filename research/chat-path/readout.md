# Chat path readout (RS3)

Sources: the four notes on `spike/chat-path` (`notes-docs.md`, `notes-live.md`, `notes-tunnel.md`, `notes-lab-run.md`,
cited as docs, live, tunnel, lab run) and decisions D-084 and D-090. V = tried or read in the source; I = inferred.

## The route

**Build now (WP18):** the coder's own machine runs the MCP server in a read-only container under Colima; Tailscale
Funnel publishes it at a fixed `https://` address; an API key gates it (D-084, D-090). The lab run took this route end to
end (lab run, Result).

**Preferred long-term, after v0.1:** the same server on governed compute, so no machine of the coder's needs to stay
awake or exposed (D-084, the chief engineer's words: "we do prefer that mcp via governed computer later just put it
after v0.1"). Deferred because the compute is not yet set up (D-084).

Why this route now: the chat's server calls the MCP server, so the server needs a public address (live, Findings).
Funnel's address is fixed, its cost is $0 and TLS ends on the coder's machine, so the relay cannot read field notes
(tunnel, Part A). The container limits what the server can touch: a read-only root, a non-root user, the vault mounted
read-only (lab run, Set-up).

## 1. The chat itself

- **It is LibreChat, not Open WebUI.** Open WebUI survives only as a legacy read-only instance (docs, Headline
  correction; docs.inference.coop/operations/infrastructure).
- **Tried (live, 24 November; V):** members can add their own MCP server in MCP Settings, "Add MCP": URL (`https://`),
  transport Streamable HTTPS or SSE, authentication none, API key or OAuth. Agent Builder is open to members: model,
  instructions (a system prompt), tools including MCP servers, skills, and file context (files attach once the agent is
  created). Files attach to a conversation by paperclip or drag and drop. Code execution was not offered.
- **Not tried:** downloading files the chat makes; knowledge collections as such (File Context and File Search exist in
  the software, but whether the co-op enables File Search is unknown); file retention (the privacy pages do not say)
  (docs, Not documented).
- inference.coop's own documentation never mentions MCP in the chat (docs, Q1); the live check is the evidence.

## 2. Reaching the tool

- **The co-op's chat server calls the MCP server** over the network, sending the configured headers; the coder's
  browser does not (docs, Q2; LibreChat docs, "MCP"). A server on the coder's machine is unreachable without a public
  tunnel, and private addresses are refused unless an administrator allows them (docs, Private addresses).
- **Tunnel choice** (tunnel, Part A): Funnel fits best (fixed name, free, port 443). Runner-up ngrok free: the provider
  likely sees traffic and an agent is needed. Quick Cloudflare Tunnel changes address each run and lacks SSE. Pinggy's
  free tunnel dies hourly. Funnel's macOS documentation contradicts itself; the lab run settled it for the
  command-line install (V).
- **What passes through:** every tool result goes via the co-op's chat server and the chosen model provider as part of
  the conversation, as uploaded files already do (live, last paragraph). The gateway keeps prompts in memory, not logs;
  the chat server keeps saved chats until deleted; the co-op "can technically read chat history" and promises not to;
  providers differ (Tinfoil uses enclaves; others rely on policy) (docs, Data handling). The inputs are therefore
  disclosed to the co-op and the provider chosen: the coder picks a provider that fits the project's data rights, and
  where those rule it out, the manual path (R-19) remains.
- **Lab run findings** that WP18's launcher must handle (lab run, Findings):
  1. macOS privacy blocks Colima's mount of `~/Documents`; keep the vault elsewhere or copy it.
  2. Funnel failed silently until the tailnet had the Funnel policy (one console click). HTTPS and the policy are set
     once; the machine is renamed before HTTPS, because HTTPS publishes the machine name in a public certificate ledger
     permanently.
  3. The coder pastes the API key into the chat's form by hand.
  4. After a container restart the chat's session saw 404s, then re-initialised itself.
- **The coder's machine must be awake** when the chat is used (I; tunnel, Mac sleeps). This is the main reason governed
  compute is preferred.

## 3. The workflow

The loop uses the coding loop's words (`GLOSSARY.md`). The lab run exercised the connection and one check call; the
rest follows the design (`contracts/architecture.md`, M8) and is not yet tried.

1. The coder attaches field notes to a conversation or to an agent's file context (live) and tells the assistant what
   to draft. The assistant holds no authority.
2. The assistant drafts a narrative; the MCP server's operations create the stubs and write the pages (M5, the only
   writer). The assistant never writes a narrative's text through the tool, and the server cannot move a narrative
   into or out of `done` (M8).
3. The check runs through the server and returns problems as data (lab run: `check_vault` answered "7 errors, 0
   warnings", matching the tool run directly).
4. The coder reads the page in Obsidian, interprets, edits, and sets `done` there. Authority stays with the coder
   (interpretation) and the tool (conformance).

Copying is reduced to two acts: attaching the notes, and pulling the repository in Obsidian. Because the server holds
one clone and reads it afresh on each call, an edit made in Obsidian shows in the next call once git brings it
(M8).

Open: how field notes reach the vault. The server's clone must hold them or the assistant must read them from the
chat; this needs a WP18 decision.

## 4. No terminal

From tunnel, Part B (read in documentation, V for each step; not yet run by a coder):

- **Create** the private repository from the template on github.com ("Use this template", choose private).
- **Clone, commit, push, pull** with GitHub Desktop (browser sign-in, token in the keychain). After web edits: Fetch
  origin, then Pull origin.
- **Lock a version** on github.com: Releases, Draft, "Create new tag", Publish. This is the tagging act in "a finished
  model". GitHub Desktop can also tag.
- The Obsidian Git plugin ranks last: it needs Git installed and a Terminal step for the keychain.
- **Setup of the tool itself.** The lab run needed a terminal only for installing Tailscale (an administrator password
  prompt). Everything else can be a launcher's job (lab run, Finding 4). WP18's launcher must start the container, run
  the Funnel command, print the address and show where to paste the key. Whether the Funnel step can run from a
  launcher without the coder's input is not shown; the one-time browser approval in Funnel's command-line step cannot
  be skipped (tunnel, Could not verify).
- **Not verified:** whether the template's private option is offered to the coder's account; Desktop's automatic
  fetch; Desktop pushing a tag without a commit.

## 5. Views

- The fingerprint view, edge tables, layered view and traces come from one generator (M6), deterministic and built
  only from a conformant vault; it refuses, returning the problems, when the pages drawn have errors (architecture,
  M6).
- The MCP server returns view data as a result and writes view files through M5 into the private repository, so they
  are versioned with the model and open in Obsidian after a pull (M8; section 1 of the architecture).
- Not built or tried in RS3: the lab run covered only two read-only checks (lab run, Set-up). WP17 builds M6 and WP18
  exposes it. Renderings that need a drawing are an optional extra; the CSV tables work with no LLM.

## Run log (RS3-R3)

| Date | What | Material |
|---|---|---|
| 24 Nov | Docs read, no sign-in (docs); chat interface inspected, no message sent, nothing saved (live) | None |
| 25 Nov | One session, two messages to the chat; spike MCP server in a container, through Funnel; afterwards Funnel off, container removed, MCP entry deleted (lab run, Clean-up) | Synthetic lab vault only |

HTTPS and the Funnel policy stay enabled on the tailnet; the machine keeps its neutral name (lab run). Use was light
and sequential: one session, human-paced.

## Flags for WP18

Fixed vault location outside `~/Documents`; the Funnel policy and rename steps in the first-run guide; a decision on
how field notes reach the vault; a provider choice stated to the coder before any real material is used; the
`ts.net` address was accepted by the chat (lab run) but the co-op's allowed-address rules are still unknown, so a
change there could break the route.
