# Run record: local LLM (Ollama in Docker with Open WebUI)

Page: `docs/local-llm.md`. Unit WP25-U4. Run on 26 to 27 Nov 2026.

## Environment
- Intel iMac (x86_64), macOS 15.7, Colima (Docker VM 6 CPUs, 11.7 GiB). Docker Compose v2.40.
- Ollama 0.40.18 (image `ollama/ollama`), Open WebUI 0.13.5 (`ghcr.io/open-webui/open-webui:main`), SCAT server built from this
  branch with `deploy/Dockerfile` (unchanged). Chrome headless driven by a scratch playwright for screenshots.
- Material: `contracts/examples` copied to a scratch vault under the home folder. Throwaway key `lab-<hex>`. No sign-ins.
- Real check of the vault: `0 errors, 2 warnings` (two SCAT-DRAFT-FIELD warnings on narrative/funders-meeting.md).

## Steps as run
1. Compose file written (as on the page, plus nothing else); `docker compose up -d --build`: images pulled (Open WebUI layers
   about 40 minutes on this link; Ollama and Python base quick), server built, three containers up.
2. `ollama pull llama3.2:3b` (2.0 GB), later `qwen2.5:7b` (4.7 GB): both succeeded.
3. Open WebUI at 127.0.0.1:3000 with WEBUI_AUTH=False: no account, no sign-in. First start downloads an embedding model (page waits a minute or two).
4. Registered the server (Settings > Integrations > External Tool Servers > +, type MCP Streamable HTTP, Bearer key): saved. Server returned 401 without key.
5. Chat turns:
   - llama3.2:3b, default function calling, no rules: answered with invented code, no tool call.
   - llama3.2:3b, native, no rules: tried a tool name that does not exist ("Failed to create tool"), then said "0 errors and 1 warnings" (wrong: 2).
   - qwen2.5:7b, native, rules as system prompt, default context: Ollama log "truncating input prompt, prompt=9339 limit=2050": the model said the check tool was not provided. Fixed by OLLAMA_CONTEXT_LENGTH=8192 (now on the page).
   - qwen2.5:7b, same, vault mounted from a folder Colima does not share (a /private/tmp path): the server saw an empty /vault, `scat_check` returned an error, the model reported it faithfully. Vault moved under the home folder (now on the page).
   - qwen2.5:7b, final: one `scat_check` call, result `ok: true`, 2 warnings; the model listed both warnings correctly and called the vault "not fully conformant". Real `scat check`: `0 errors, 2 warnings`. First turn about 5 minutes (prompt about 7,400 tokens at about 36 tokens/s, then generation at about 6 tokens/s); Ollama container 5.9 GiB, Open WebUI 0.9 GiB, server 55 MiB.
6. Function Name Filter List `check, status` was set before the last two runs; its effect on the prompt size was not measured (prompt about 7,400 tokens with it).

## Screenshots (docs/assets/walkthroughs/local-llm/)
01-open-webui-home (step 4), 02-tool-server (step 5), 03-tool-on (step 7), 04-chat-controls (step 8), 05-tool-result and 06-answer (step 9). The lab key is hidden by the form; the key was a throwaway.

## Deviations
- 01 was taken before the 7B was pulled and showed llama3.2:3b in the model picker; after review the model name was painted out of the picture (stack already removed, not re-run), and the alt text and step 4 say 'your model's name'.
- The Docker host here is Colima, not Docker.app.
- Reached Settings by address, not by the avatar menu.

## Steps a script could remove
Writing compose.yaml and the four `export` lines (a `scat-local-llm.sh` or published image would cut them); the server image build (a published image would remove it); registering the tool server (Open WebUI can take it from `TOOL_SERVER_CONNECTIONS` environment variable, not tried); Function Calling = Native and the system prompt (a model preset could carry both, not tried); pasting the key.

## Installed and removed
See the cleanup section below.

### Cleanup
Installed or pulled: images `ollama/ollama` (about 5 GB), `ghcr.io/open-webui/open-webui:main` (about 8 GB), `scatlocal-scat-mcp` (built, about 177 MB); models llama3.2:3b and qwen2.5:7b in the volume `scatlocal_ollama`; volume `scatlocal_open-webui`; network `scatlocal_default`; three containers; scratch vault `~/u4-lab`; scratch playwright venv (playwright, pillow); the worktree `.venv` created by `uv run`; `site/`.
Removed: all of the above (`docker compose down --volumes`, `docker rmi` of the three images, the folders). Before and after lists of `docker images`, containers, networks and volumes are identical. Not removed: Docker's build cache from the one server build (shared with other builds), and the native Ollama, its models and the other containers, which were there before and untouched. Port 11434 (native Ollama) was never used; the Ollama container was not published.

## Cold-reader fixes (branch wp25/fix4)
Page edited from this record, stack not restarted: step 11 now says the new key must be pasted into the SCAT row (the gear on the row opens the same edit form used to add the filter list, seen in the run; the saved key persists in Open WebUI's volume); step 10 uses `uv run --project ~/scat-kg-tools scat check`, the form used in the run; the filter list names are the server's (`check`, `status`) and Open WebUI shows `scat_check` (the connection ID prefix, seen in the run; the `status` tool was never called); clone and compose folders named; first-start downloads named from the run (the helper model all-MiniLM-L6-v2 was fetched from huggingface.co by Open WebUI, seen in its log); about 40 minutes for the first start was on a slow connection. Not checked in the run: whether anything else leaves the Mac; the page says only that chat text goes to the model in the Ollama container.
