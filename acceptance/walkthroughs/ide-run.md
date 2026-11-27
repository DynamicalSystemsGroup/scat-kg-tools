# IDE path run record (Codex)

Status: waiting for the chief engineer's sitting. The Codex screens have not been run; `docs/ide.md` has no
screenshot references yet. Template side: `AGENTS.md` added on branch `wp25/template` of scat-kg-template (not pushed).

Environment, date, material (lab only, `contracts/examples`), steps as run, deviations and steps a script could remove:
to be filled at the sitting. Nothing installed or removed so far.

## Screenshot slots

Files go under `docs/assets/walkthroughs/ide/`, each under about 300 KB, with personal details, usernames, paths and
any key cropped or blurred. Add each to the page with real alt text.

| File | Must show | Step |
|---|---|---|
| `01-extension-installed.png` | The Codex extension page in the editor, installed | 1 |
| `02-sign-in.png` | The sign-in choice Codex offers (no account details) | 3 |
| `03-sidebar-open.png` | The vault open, the Codex icon and the chat panel | 2 |
| `04-setup-result.png` | Codex's reply after "Set yourself up": `uv sync`, `uv run scat check` and the tool's words | 4 |
| `05-rules-answer.png` | Codex's answer to what it may not do (no `done`, no `set-status`) | 5 |
| `06-cli-session.png` | The `codex` command running in the vault folder (terminal alternative) | In a terminal paragraph |

## Doc facts (fetched 26 Nov 2026; the old developers.openai.com addresses redirect to learn.chatgpt.com)

- IDE page, <https://learn.chatgpt.com/docs/codex/ide>: VS Code and compatible editors use the extension; Cursor and
  Windsurf are listed beside VS Code; Xcode and JetBrains have built-in integrations instead. Open with the Codex
  icon, or "Codex: Open Codex Sidebar". Recommends Git checkpoints around a task.
- CLI page, <https://learn.chatgpt.com/docs/codex/cli>: macOS and Linux install `curl -fsSL https://chatgpt.com/codex/install.sh | sh`;
  Windows, npm and Homebrew tabs exist but their commands did not come through the fetch. Start with `codex` in the
  project folder; first run offers "Sign in with ChatGPT" or another method.
- AGENTS.md, <https://learn.chatgpt.com/docs/agent-configuration/agents-md>: global file in `~/.codex`, then one file per
  folder from the project root down to the working folder (`AGENTS.override.md`, then `AGENTS.md`); later files
  override earlier; combined limit `project_doc_max_bytes`, 32 KiB by default.
- MCP, <https://learn.chatgpt.com/docs/extend/mcp?surface=ide>: gear menu, MCP servers, Add server (STDIO or Streamable
  HTTP), Restart extension; CLI `codex mcp add`; shared `~/.codex/config.toml` or a trusted project's
  `.codex/config.toml`. The page does not call MCP required; servers are opt-in.

Differences from the U1 readout: the readout's two docs addresses now redirect; the IDE page does not cover MCP (the
MCP page does); the readout's note on the form having no token field was not re-confirmed.

## What the docs leave unclear (for the sitting)

- Sign-in in the extension: the page says to sign in, with no steps. Which accounts or plans work is not stated.
- Supported editors: named VS Code, Cursor, Windsurf, VS Code Insiders; exact versions and whether other VS Code
  forks work are not stated.
- Whether the extension shows the AGENTS.md it loaded (step 4 relies on Codex following it); check at the sitting.
- Windows install commands and requirements.
