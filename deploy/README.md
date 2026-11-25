# deploy: the chat path's image and launcher

What is here:

- `Dockerfile` (+ `Dockerfile.dockerignore`): the MCP server (`scat-mcp`) as a read-only image. Unprivileged
  by default; the launcher sets the host's uid and gid at run time (`--user`), so the image carries no uid; writes only to `/tmp` (tmpfs) and the mounted `/vault`.
- `scat-chat.sh`: the launcher logic, `start`, `stop`, `status`, `change-vault`. Start checks the container runtime (Docker Desktop, or Colima), and
  Tailscale, refuses a vault macOS hides from the container (Documents, Desktop, Downloads, iCloud) and offers a
  copy to `~/SCAT/vault`, uses the published image of its package version (`ghcr.io/dynamicalsystemsgroup/scat-kg-tools`), or builds one once when none is published, makes a fresh session key and keeps it in the login keychain, runs the container on `127.0.0.1`, opens the
  Funnel link, keeps the Mac awake, and shows the address and a Copy key button (the session key is never shown; it reaches the clipboard only when the coder clicks the button). Stop (also on quit or any failure) turns it all
  off, deletes the session key and clears the clipboard if it still holds it.
- `SCAT Chat.applescript`, `build-app.sh`: a thin applet; `deploy/build-app.sh` writes `deploy/build/SCAT Chat.app`
  with the launcher and the server source inside. The built app is not committed.

How it is tested: `tests/deploy` runs the script with stand-ins for docker, colima, tailscale, openssl, security, osascript, curl, pbcopy and
caffeinate (environment overrides `SCAT_CHAT_*`; `SCAT_CHAT_UI=plain` replaces dialogs with text and
`SCAT_CHAT_A_<KEY>` answers) against a fake server, and checks order, flags, refusals, teardown, and that the session key is in no argument and no file.
The AppleScript compile test is skipped where `osacompile` is absent. A real build and run against Colima, with a
stand-in `tailscale`, is done by hand before acceptance; the real Tailscale is not run by any test.

## What is not verified

The `security` calls are the macOS-specific part of the session key; they live only in the `key_*` functions of
`scat-chat.sh` (`SCAT_CHAT_SECURITY` replaces the program), and the tests use a stand-in. Not verified by any test or
by hand:

- a keychain prompt when the launcher runs from the built app (a different parent process), or when the login
  keychain is locked;
- that the item is not synchronised to iCloud Keychain;
- Docker Desktop (the runs were against Colima and stand-ins).
