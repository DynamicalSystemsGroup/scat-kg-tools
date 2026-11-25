# deploy: the chat path's image and launcher

What is here:

- `Dockerfile` (+ `Dockerfile.dockerignore`): the MCP server (`scat-mcp`) as a read-only image. Non-root user with
  the host's uid (build arg `UID`, default 501); writes only to `/tmp` (tmpfs) and the mounted `/vault`.
- `scat-chat.sh`: the launcher logic, `start`, `stop`, `status`, `change-vault`. Start checks the container runtime (Docker Desktop, or Colima), and
  Tailscale, refuses a vault macOS hides from the container (Documents, Desktop, Downloads, iCloud) and offers a
  copy to `~/SCAT/vault`, builds the image once, makes a fresh key, runs the container on `127.0.0.1`, opens the
  Funnel link, keeps the Mac awake, and shows the address and key. Stop (also on quit or any failure) turns it all
  off, replaces the key and clears the clipboard.
- `SCAT Chat.applescript`, `build-app.sh`: a thin applet; `deploy/build-app.sh` writes `deploy/build/SCAT Chat.app`
  with the launcher and the server source inside. The built app is not committed.

How it is tested: `tests/deploy` runs the script with stand-ins for docker, colima, tailscale, openssl, pbcopy and
caffeinate (environment overrides `SCAT_CHAT_*`; `SCAT_CHAT_UI=plain` replaces dialogs with text and
`SCAT_CHAT_A_<KEY>` answers) against a fake server, and checks order, flags, refusals, teardown, key rotation.
The AppleScript compile test is skipped where `osacompile` is absent. A real build and run against Colima, with a
stand-in `tailscale`, is done by hand before acceptance; the real Tailscale is not run by any test.
