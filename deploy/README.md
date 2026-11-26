# deploy: the chat path's image and launcher

What is here:

- `Dockerfile` (+ `Dockerfile.dockerignore`): the MCP server (`scat-mcp`) as a read-only image. Unprivileged
  by default; the launcher sets the host's uid and gid at run time (`--user`), so the image carries no uid; writes only to `/tmp` (tmpfs) and the mounted `/vault`.
- `scat-chat.sh`: the launcher logic, verbs `start`, `stop`, `status`, `copy-key`, `copy-address`, `change-vault` (verbs only, never a
  value as an argument). Start shows once per Mac that SCAT Chat lives in the menu bar, checks the container runtime (Docker Desktop, or Colima), and
  Tailscale, asks "Serve <vault>?" at every start ("Use it" or "Choose another"; with no remembered vault it goes straight to the folder chooser),
  refuses a vault macOS hides from the container (Documents, Desktop, Downloads, iCloud) and offers a
  copy to `~/SCAT/vault`, uses the published image of its package version (`ghcr.io/dynamicalsystemsgroup/scat-kg-tools`), or builds one once when none is published, makes a fresh session key and keeps it in the login keychain, runs the container on `127.0.0.1`, opens the
  Funnel link, and keeps the Mac awake. It keeps `ui` in its state folder (state, vault, address, then a problem line; never the key),
  written by a rename, for the app to show. `copy-key` is the one path of the session key to the clipboard; `copy-address` copies the address; `change-vault` is stop, then start with the vault chooser (the key is new, so the chat's server entry needs updating).
  Stop (also on quit or any failure) turns it all off, deletes the session key and clears the clipboard if it still holds it.
- `SCAT Chat.applescript`, `build-app.sh`: a menu-bar app (AppleScriptObjC, no window). Its title is a coloured dot (grey starting or stopped, green running,
  red a problem); its menu shows State, Vault and Address, a "Problem:" line only in a problem, then Copy address, Copy key, Change vault and Stop. A problem raises one alert. It reads `ui` while it idles and calls the launcher's verbs. `deploy/build-app.sh [output folder]` writes `SCAT Chat.app`
  (default `deploy/build`) with the launcher and the server source inside, sets `LSUIElement` (no Dock icon) and signs it ad hoc (no certificate). The built app is not committed.

Test-only settings (a double-clicked app has none of them): `SCAT_CHAT_VAULT` names the vault and skips the "Serve <vault>?" question,
which breaks the rule that every start shows the coder the vault (the tests use it; the app never sets it); the applet reads `SCAT_CHAT_LAUNCHER` (a stand-in launcher),
`SCAT_CHAT_HOME` (the state folder) and `SCAT_CHAT_APPLET_LOG` (a file that receives its menu lines).

How it is tested: `tests/deploy` runs the script with stand-ins for docker, colima, tailscale, openssl, security, osascript, curl, pbcopy and
caffeinate (environment overrides `SCAT_CHAT_*`; `SCAT_CHAT_UI=plain` replaces dialogs with text and
`SCAT_CHAT_A_<KEY>` answers) against a fake server, and checks order, flags, refusals, teardown, and that the session key is in no argument and no file.
The AppleScript compile test is skipped where `osacompile` is absent. A real build and run against Colima, with a
stand-in `tailscale`, is done by hand before acceptance; the real Tailscale is not run by any test.

## What is not verified

The macOS-only tools sit behind the launcher's own functions or in the app: `security` (the session key) lives only in the `key_*` functions of
`scat-chat.sh` (`SCAT_CHAT_SECURITY` replaces the program), and the tests use a stand-in. `plutil` and `codesign` are used only in `build-app.sh`, and AppleScriptObjC
(the menu-bar item) only in `SCAT Chat.applescript`. The tests do not run them; the built app is checked by hand on a Mac. Not verified by any test or
by hand:

- the dot's look and a real click on a menu item (they need a screen);

- a keychain prompt when the launcher runs from the built app (a different parent process), or when the login
  keychain is locked;
- that the item is not synchronised to iCloud Keychain;
- Docker Desktop (the runs were against Colima and stand-ins).
