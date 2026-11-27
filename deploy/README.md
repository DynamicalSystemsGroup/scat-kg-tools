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
  red a problem); its menu shows State, Vault and Address, a "Problem:" line only in a problem, then Copy address, Copy key, Change vault and Stop. A problem raises one alert. Stop in the menu runs the launcher's stop and shows its result in one alert, then quits; if the stop cannot be confirmed the alert says so, the dot stays red and the app stays, so Stop can be chosen again. Quitting any other way (Cmd-Q, the system) runs the stop silently, once. It reads `ui` while it idles and calls the launcher's verbs. `deploy/build-app.sh [output folder]` writes `SCAT Chat.app`
  (default `deploy/build`) with the launcher and the server source inside, sets `LSUIElement` (no Dock icon) and signs it ad hoc (no certificate). The built app is not committed.

Settings for tests (a double-clicked app has none of them): `SCAT_CHAT_VAULT` names the vault and skips the "Serve <vault>?" question; it works only with `SCAT_CHAT_UI=plain`, which the app never sets, so the app always asks. The app reads `SCAT_CHAT_LAUNCHER` (another launcher to call),
`SCAT_CHAT_HOME` (the state folder) and `SCAT_CHAT_APPLET_LOG` (a file that receives its menu lines).

`tests/deploy` runs the script with replacements for docker, colima, tailscale, openssl, security, osascript, curl, pbcopy and
caffeinate (environment overrides `SCAT_CHAT_*`; `SCAT_CHAT_UI=plain` replaces dialogs with text and
`SCAT_CHAT_A_<KEY>` answers). It checks order, flags, refusals, teardown, and that the session key is in no argument and no file.
The AppleScript compile test is skipped where `osacompile` is absent.

The macOS-only tools sit behind the launcher's own functions or in the app: `security` (the session key) is called only from the `key_*` functions of
`scat-chat.sh` (`SCAT_CHAT_SECURITY` replaces the program). `plutil` and `codesign` are used only in `build-app.sh`, and AppleScriptObjC
(the menu-bar item) only in `SCAT Chat.applescript`. The tests do not run the real versions of these tools or of Tailscale; check the built app by hand on a Mac.
