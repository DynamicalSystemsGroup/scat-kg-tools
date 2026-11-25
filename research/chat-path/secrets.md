# The chat path's session key: how the launcher keeps it (WP21-G5 spike)

Spike for WP21-G5 / R5 (C7, F15). macOS 15.7.7, Docker 28.5.1 on Colima, 25 November 2026. Every test used the dummy value `DUMMY-NOT-A-KEY` and the keychain service `scat-kg-spike-DUMMY`. No real key or existing keychain item was read.

## Recommendation

Keep the key in the login keychain for the session, and let it reach every consumer through pipes. The launcher writes it with `security -i` fed on stdin (never `-w VALUE`), reads it with `security find-generic-password -w` into a pipe, starts the container with `--env-file /dev/stdin`, copies it to the clipboard only when the coder clicks a "Copy key" button, and deletes the item at Stop. The leak F15 reports is a single line: `ui_hold` passes the dialog text, key included, to `osascript` as an argument. That line must go under every option, so the dialog shows the address and a Copy key button, never the key. Fallback, if the ACE wants no macOS-specific code: the existing 0600 file in the 0700 state folder already meets points 1 to 4 once the dialog is fixed (see Open questions).

## Evidence

All rows are tested on this Mac unless marked "cited". "Other users" is inferred from the man page and the permissions shown; no second account was used.

| Mechanism | In argv (`ps -ww -o args`) | In environment (`ps -E`) | In a file | Other users | Source |
|---|---|---|---|---|---|
| `osascript -e '...' "$KEY"` (today's dialog) | **Yes**, whole key | No (Apple binary: `ps -E` shows no environment at all) | No | Argv of any process is listed by `ps`; the key shows to every local account | Tested: `osascript -e delay 5 -e -- DUMMY-NOT-A-KEY` in `ps` |
| `security add-generic-password -w VALUE` | **Yes** | No | Keychain only | Same as above | Tested: sampled `ps` for the pid, saw `-w DUMMY-NOT-A-KEY`; man page says "Put at end of command to be prompted (recommended)" |
| `security -i`, command on stdin | No (argv is `security -i`) | No | Keychain only | No | Tested, same sampling; item created, rc 0 |
| `security add-generic-password ... -w` (prompt) | No | No | Keychain only | No | Cited (`man security`). Not tested: it prompts on the terminal, no terminal in a launcher |
| `security find-generic-password -s S -w` (read) | No | No | No | No | Tested: prints value on stdout, rc 0, no dialog |
| `docker run --env-file /dev/stdin`, key piped | No | No | No | No | Tested: argv `... --env-file /dev/stdin <image>`; `docker inspect` shows the key (same user only) |
| `docker run -e SCAT_MCP_KEY` (inherited) | No | **Yes**, docker CLI's environment | No | Environment of a process is shown to its owner only (`man ps` -E) | Tested |
| `docker run -e SCAT_MCP_KEY=VALUE` | **Yes** | Yes | No | Shown to all | Tested |
| `--env-file FILE`, file in 0700 dir, mode 0600 | No | No | **Yes**, plain text | Not readable: `drwx------` dir, `-rw-------` file | Tested with `mktemp -d` under `umask 077`; this is today's `write_key` |
| `curl -K -` with the header on stdin (today's `http_code`) | No | No | No | No | Read from the script: `printf` is a built-in, so no process carries it |

Limits: a same-user process can still read the key with `docker inspect` or `security find-generic-password -w` (`/usr/bin/security` is trusted by default; no prompt appeared). Nothing here defends against malware running as the coder. Apple binaries hide their environment from `ps -E`; others (python, docker) show it to their owner.

## Alternatives and why not

- **0600 file in a private directory (today's design, dialog fixed).** Meets 1 to 4, no macOS code. Not chosen: the key is plain text under `~/Library/Application Support` for the whole session (backed up, and left behind by a crash until the next start).
- **Inherited `-e VAR`.** Out of argv, but in the docker CLI's environment (tested). No gain over stdin.
- **`-e VAR=VALUE`, `security -w VALUE`.** Key in argv. Refused.
- **Key held only in a shell variable.** Simplest, but a crashed launcher cannot clear the clipboard afterwards, and a restart cannot reach the key.
- **Key still shown in the dialog, script fed on stdin.** Keeps the key out of argv (tested: argv was just `osascript`) but puts it on screen, against "on the clipboard only when the coder asks".

## What is macOS-specific, and where it is isolated

Already macOS-specific and already behind overrides: `osascript`, `pbcopy`, `pbpaste`, `caffeinate`, `open`. This adds `security`, behind a new override `SCAT_CHAT_SECURITY`.

In `deploy/scat-chat.sh` the section `# ---- the key` holds `new_key`, `write_key`, `read_key`, `file_mode_ok`. Replace it with four functions and nothing else may name `security` or `KEYFILE`:

- `key_put KEY` (stdin to `security -i`), `key_get` (stdout), `key_drop` (delete), `key_present` (exit status).

Callers change by name only: `step_server` (put, then `key_get | docker run --env-file /dev/stdin`), `http_code` and `cmd_start` (get), `teardown` (read old key for the clipboard check, then drop; the key rotation can go, because the item is deleted and the container is gone). `ui_hold` loses `$KEY` and gains a Copy key button that loops. A later Linux version replaces only these four with `secret-tool`, or a 0600 file under `$XDG_RUNTIME_DIR`. MISSION, Platforms, should record `security` among the isolated tools; that edit is the ACE's.

## How to test it (R5)

- Stand-in `security` in `tests/deploy/conftest.py`: `-i` reads stdin and stores the value under `$STUB_STATE`; `find` prints it or exits 44; `delete` removes it. `FakeServer` reads that store instead of `key.env`.
- Assert the key string appears in no logged argument: the stand-ins already append `$*` to `$CALLS`, so grep that log (and the dialog stand-in's arguments) for the key after start and after Stop.
- Assert no `key.env` exists, the docker call has `--env-file /dev/stdin`, the clipboard stays empty until the Copy key answer, and the item is gone after Stop, after a crash and after a second Stop.
- By hand once: run the real launcher in `SCAT_CHAT_UI=plain` with stand-ins for docker and tailscale, sample `ps -ww -o args` for the key, then `security find-generic-password -s scat-chat` before Stop (found) and after (rc 44). A dry run leaves one login-keychain item, service `scat-chat`, until Stop or the next start's crash clean-up removes it.

## Open questions for the ACE

1. The 0600 file already meets all four points once the dialog is fixed; the keychain's gain is "never plain text on disk". Is that gain worth a macOS-specific store and its stand-in, given the key is rotated at Stop either way? R5 as approved presumes the keychain.
2. At Stop, is deleting the item (and removing the container) enough, or must the launcher also rotate a key that no longer exists anywhere?

## What was not verified

- Whether a keychain prompt appears when the launcher runs from the built applet (a different parent process), when the login keychain is locked, or on a Mac with a corporate keychain policy. The terminal test showed no prompt.
- That the item is not synchronised to iCloud Keychain (generic passwords added by `security` are local by default; cited from memory, not tested).
- `security add-generic-password -w` prompt mode (needs a terminal), Linux, Docker Desktop, and a real second user account.
