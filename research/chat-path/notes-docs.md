# RS3-U1: docs notes on the chat and its tool routes

Sources: public documentation only, read 2026-11-24. No sign-in, no chat session, no API call to inference.coop's
service was made; only its public docs and marketing page, and the public docs of the software, were fetched.
Anything not stated in a cited page is marked "not documented".

## Headline correction

The member chat at chat.inference.coop is **LibreChat, not Open WebUI**. Open WebUI runs only as a legacy, read-only
instance that holds older history and file attachments.
- https://docs.inference.coop/operations/infrastructure/ (LibreChat main chat; Open WebUI legacy; LiteLLM gateway; Cloudron on a co-op server at Infomaniak)
- https://docs.inference.coop/guides/getting-started/ (the previous Open WebUI instance remains readable)

So the Open WebUI documentation (below, for contrast) does not describe the live chat. LibreChat's does, but the
co-op's own settings are not documented, so LibreChat features are "available in the software", not "confirmed on".

## Q1. What the chat offers a coder

What inference.coop itself documents:
- Attach a document with the paperclip and ask about it; web search via a globe button; a Tools menu "lists everything the chat can do"; choose model and where it runs (private or green). https://docs.inference.coop/guides/getting-started/
- Marketing page lists web search, "File uploads & documents", model/provider choice per session. https://inference.coop
- Not documented by inference.coop: knowledge collections, custom models or system prompts, MCP or tool servers in the chat, file downloads, code execution. The only MCP mention on the site is a bot's key. https://docs.inference.coop/operations/agentic-systems/
- The API docs do not mention MCP; they say "Any tool that speaks the OpenAI API works", bearer key `sk-...`. https://docs.inference.coop/guides/api-access/

What LibreChat offers (software docs; whether the co-op enables each is not documented):
| Need | LibreChat | URL |
|---|---|---|
| Files as a collection | Agents: "File Search" turns attached files into a searchable knowledge base (needs the RAG API; not suited to CSV/Excel); "File Context" extracts text at upload and sends it every turn. Files can be attached only after the agent is created. | https://www.librechat.ai/docs/features/agents |
| Custom model / system prompt | Agent Builder (side panel): name, model, category, instructions typed or from a saved prompt. Private until shared. Admins control per role who may use, create, share. | https://www.librechat.ai/docs/features/agents |
| Tool servers | Agents can attach admin-configured MCP servers or ones the user added, with per-tool selection. | https://www.librechat.ai/docs/features/agents |
| Files the chat makes | Code interpreter ("Run Code") writes files; rows in the message open in the Artifacts panel or download. Needs a separate sandbox service the admin deploys; runs fail until then. Artifacts render HTML/Markdown/SVG etc. in a side panel. | https://www.librechat.ai/docs/features/code_interpreter |

Open WebUI, for contrast only (legacy instance): knowledge bases, Models wrapper, MCP from v0.6.31.
https://docs.openwebui.com/llms.txt

## Q2. Routes to an MCP server

LibreChat (the live chat's software):
- **Server-side.** Remote servers are reached over the network from the LibreChat server, which sends the configured headers; stdio servers run as a child process on the LibreChat host. https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/mcp_servers
- **Transports.** Config types: `stdio`, `websocket`, `streamable-http` (alias `http`), `sse`. The UI offers Streamable HTTPS and SSE. Local stdio must be defined in `librechat.yaml` (admin). https://www.librechat.ai/docs/features/mcp
- **Who adds.** Admins in `librechat.yaml` (restart needed). Users may add remote servers via MCP Settings, "if their role allows it"; UI-created servers can reach remote URLs only. https://www.librechat.ai/docs/features/mcp
- **Authentication.** None (auto-detects OAuth), API key (shared or per user; Bearer, Basic or Custom header), OAuth (dynamic client registration if client fields empty), On-Behalf-Of (admin-granted, needs OpenID sign-in), per-user variables. Connections are per user. https://www.librechat.ai/docs/features/mcp
- **Private addresses.** Internal IPs and local hostnames "must be explicitly allowed" (`mcpSettings.allowedAddresses`/`allowedDomains`). A server on the coder's own machine is therefore not reachable by the co-op's chat server unless exposed publicly (a tunnel) and allowed. https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/mcp_servers (the "own machine" reading is my inference from "called from the LibreChat server")
- **Browser-called route.** Not documented for LibreChat; its docs describe only server-side calls.

Open WebUI (legacy, for the record):
- Streamable HTTP only; SSE does not work directly; stdio not native. The backend opens the connection, so the URL must be reachable from the backend, not the browser. Only admins add instance servers; users add their own through the Tether app. Auth: none, bearer, session, OAuth, OAuth 2.1. https://docs.openwebui.com/features/extensibility/mcp
- mcpo proxy exposes stdio/SSE MCP servers as OpenAPI servers. https://docs.openwebui.com/features/extensibility/plugin/tools/openapi-servers/mcp

**What passes through.** The model's tool calls and the tool's results go via the chat server and then to the chosen model provider as part of the conversation; the docs say model providers process inputs under their own terms. https://docs.inference.coop/governance/privacy-policy/

## Data handling bearing on field notes
- Gateway keeps prompts in memory only, not in logs or the database; keeps usage records (model, tokens, cost, key); no retention period given. "We do not train on your data or sell it." https://docs.inference.coop/guides/what-happens-with-your-data/
- Chat server keeps saved chats until deleted; temporary chats removed after about an hour (may linger in backups); nightly encrypted backups kept seven days; the co-op "can technically read chat history" and promises not to (policy, not architecture). Same page.
- Providers differ: Tinfoil (US) uses hardware enclaves; GreenPT (FR/FI) and Regolo (IT) rely on policy; Regolo cites a zero-data-retention audit. Same page.
- Web search sends queries to Yahoo and stores them with the conversation. Same page.
- Uploaded files: not addressed on the data page or in the privacy policy. https://docs.inference.coop/governance/privacy-policy/

## Transport finding

The chat is LibreChat, whose documented route is server-side: the LibreChat server connects to a remote MCP server over streamable HTTP (or SSE), with headers, API key or OAuth; stdio exists only as an admin-configured child process on the co-op's host, so it is not a route for a coder's own machine. A browser-to-localhost route is not documented anywhere. Confidence: high that LibreChat supports streamable HTTP server-side; medium that the co-op's instance exposes MCP to members at all, since inference.coop's own docs never mention MCP in the chat. A tool on the coder's machine would need a public, authenticated HTTPS endpoint (or a tunnel) that passes the private-address rules; the route is not yet shown to work.

## Not documented / needs the live check
- Does the co-op's LibreChat show MCP Settings / Add MCP to a member role? Which transports does the form offer?
- Are Agent Builder, File Search (RAG API), File Context and Run Code (sandbox) enabled for members?
- Can a member attach several files as one collection, and what size or type limits apply?
- Are uploaded files retained, where, and for how long (not stated)?
- Are `allowedDomains`/`allowedAddresses` set, so would a tunnelled endpoint be accepted?
- Which models support tool calling, and do the enclave models (Tinfoil) allow external tool calls?
- Can generated files be downloaded, and in which formats?
- LibreChat and LiteLLM versions (not given).
