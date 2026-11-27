# WP25-U1 readout: a local-LLM path, and Claude's and Codex's MCP set-up

Spike for the ACE's logged decision (WP25). Run on the ACE's Intel iMac (i9-10910, 64 GB, macOS 15.7, Colima 12 GiB), 26-27 Nov 2026. Lab material only: `contracts/examples` copied to a scratch folder. Nothing was signed in to; no key but a throwaway local `SCAT_MCP_KEY`.

## What was tried

`probe_local_client.py` (this folder) acts as a local chat client: it connects to `scat-mcp` over streamable HTTP with the bearer key, offers the 16 tools to an Ollama model, runs the calls the model asks for. Ollama 0.9.6 (native, already on this Mac) was used. 401 without the key: confirmed.

| Model (native, 100% CPU) | Result on "check the vault, say if conformant and how many narratives" |
|---|---|
| llama3.2:3b | first turn 160 s (load plus 1,978 prompt tokens). Called `check` with wrong arguments, then answered "not conformant, no narratives": wrong. 175 s. |
| qwen2.5:7b | first turn 335 s, second 126 s, 461 s in all (machine also loaded, load average about 11). Called `status`, not `check`, and answered "conformant, no issues, 3 narratives". The narrative count is right; "conformant" is wrong: `scat check` reports 2 warnings. |

Docker against native, llama3.2:1b, same prompt: 21.5 vs 23 tokens/s; load 1.1 s vs 1.6 s. On this Intel Mac the container costs nothing and gains nothing. The Docker image is 5.1 GB on disk (`ollama/ollama`). Ollama's own blog says Docker on a Mac cannot use the GPU ([Ollama Docker image post](https://ollama.com/blog/ollama-is-now-available-as-an-official-docker-image)); the Apple-silicon speed gap of Docker against native was **not tested** here.

## Findings

1. **The mechanism works end to end**: model, MCP, bearer key, tools, results. The tool descriptions were enough for a 7B model to pick a tool; not enough to pick the right one (it chose `status` for "conformant"). A small local model is a weak coder's helper and must be told the coder checks its claims; the tool, not the model, decides conformance (A-rules).
2. **Hardware**: a 3B model needs about 5 GB, a 7B about 6.5 GB of memory in use. On this CPU-only Mac a tool question takes 3 to 8 minutes. The guide can say: 16 GB of memory for a 7B model, Apple silicon for tolerable speed (untested), expect minutes per turn on an Intel Mac, and use the 3B only to see the plumbing work.
3. **Docker is optional.** The route C14 names (Ollama in Docker) works, but native Ollama is simpler and, on Apple silicon, the only one with the GPU. Recommendation: the page leads with native Ollama and offers Docker for those who want one runtime (Colima is already there for SCAT Chat).
4. **The launcher is the gap.** `deploy/scat-chat.sh` stops with an error if Tailscale is missing, and publishes the server on `127.0.0.1` only. A local client in a container (Open WebUI) cannot reach a host `127.0.0.1` port by `host.docker.internal` (not tried); a desktop client can. So either the local path starts `scat-mcp` by hand (`docs/reference/mcp.md` allows it "to try it"; a terminal), or the launcher gains a no-tunnel mode (`deploy/` is outside WP25). The ACE decides.
5. **Clients (read from docs, not run: no GUI or sign-in was driven)**:
   - Open WebUI (container, browser UI): native MCP over streamable HTTP, v0.6.31 or later, admin adds it under Settings > Integrations > External Tool Servers, auth None or Bearer; the URL must be reachable from the backend ([docs](https://docs.openwebui.com/features/extensibility/mcp.md)).
   - LM Studio: remote servers by `url` and `headers` in `mcp.json` since 0.3.17 ([docs](https://lmstudio.ai/docs/app/mcp)); runs its own models, so no Ollama; Intel Mac support not checked.
   - Jan: MCP through `mcp_config.json`; the docs do not show static headers ([docs](https://docs.jan.ai/agent/mcp)).
   - `ollmcp` (terminal) accepts streamable HTTP URLs (PyPI page, not read in full).
   Suggested example: Open WebUI with Bearer auth, since its header is documented; its first run needs an admin account made in the browser, a step for the sitting.

## Claude, from its docs

- Chat (claude.ai and Desktop): Customize > Connectors > Add custom connector; name and URL; "Request headers" take a fixed bearer key. The server must be reachable from Anthropic's cloud on the standard port 443; a private network or custom port will not connect. Free accounts get one custom connector ([support article](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp)). SCAT Chat's Tailscale public address fits.
- Claude Code: `claude mcp add --transport http <name> <url> --header "Authorization: Bearer <key>"`; scopes local, project, user; check with `/mcp` ([docs](https://code.claude.com/docs/en/mcp)).

## Codex, from its docs

- Config `~/.codex/config.toml` (or `.codex/config.toml`, trusted projects), shared by CLI and IDE extension: `[mcp_servers.<name>]` with `url` and `bearer_token_env_var` (or `http_headers`) ([MCP page](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)).
- IDE extension: gear menu > MCP servers > Add server > Streamable HTTP > URL > Restart extension; the form has no token field, so the key goes in `config.toml` ([IDE page](https://learn.chatgpt.com/docs/extend/mcp?surface=ide)).
- Instructions come from `AGENTS.md` in the project, root down to the working folder ([guide](https://developers.openai.com/codex/guides/agents-md)); that is the template's `AGENTS.md` (WP25 scope). Which editors the extension supports, and what sign-in needs, the pages do not say: for the sitting.

## Installed and removed

Installed by me: nothing system-wide. Pulled `ollama/ollama` (5.1 GB) and `llama3.2:1b` into a container and volume, then removed the container, volume and image. Native Ollama, its models and the Docker containers on this Mac were there before and untouched. The scratch vault and server are gone.

## For the ACE's decision

(a) Local client example: Open WebUI, or a desktop client. (b) Server start for the local path: terminal `scat-mcp`, or a launcher no-tunnel mode (a `deploy/` change). (c) Ollama native first, Docker second. (d) What the page says of hardware (finding 2). Not shown: any client's screens; any Apple-silicon timing.
