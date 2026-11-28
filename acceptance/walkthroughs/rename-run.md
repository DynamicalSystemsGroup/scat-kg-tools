# Run plan: SCATLAB installed over SCAT Chat (WP37-R2, G2)

Status: **a plan, not run.** It is held for the chief engineer and the ACE, on screen, after the rename has landed
(`work-packages/WP37-landing.md`). The tests already cover the launcher against stand-ins for every outside program
(`tests/deploy/test_retire_old.py`) and the build (`tests/deploy/test_app_build.py`); this run is what they cannot
show: the real app, the real keychain, the real container runtime, and the chat connecting to the new server.

The aim: an organiser who has the earlier app installed opens SCATLAB once and ends with **one app, one keychain item
and one image**, the same vault remembered, and sees nothing but the new name. Words follow `GLOSSARY.md`. The run uses
the chief engineer's accounts and keys, with the ACE as the coder (WP37, Agent's defaults). A lab vault only; the
public link (Tailscale Funnel) is switched on by the chief engineer, and off at the end.

## Before

| Item | Check |
|---|---|
| The earlier app, built from the tools commit before the rename (`6915de7`), is in `/Applications` | `ls -d /Applications/SCAT*` shows one app named with the earlier name |
| One session of it has been started and left running (so there is a key, a container and an image), then the earlier app's launcher killed so the session is a **crashed** one, as in a power cut | `security find-generic-password -s scat-chat` finds an item; `docker ps -a` lists the container `scat-chat`; `docker images` lists `scat-chat-mcp` |
| It remembers a lab vault | the earlier state folder holds a `vault` file naming it |
| The rename has landed on `dev`; the new app is built from `dev` | `sh deploy/build-app.sh ~/Desktop` gives `~/Desktop/SCATLAB.app` |

To get the earlier app: `git worktree add /tmp/earlier 6915de7`, then `sh /tmp/earlier/deploy/build-app.sh ~/Desktop/earlier`,
drag the result to `/Applications`, open it, answer its questions, wait for the green dot, then
`pkill -9 -f "Contents/MacOS/applet"` and `pkill -9 -f scat-chat.sh` (its app and its launcher). Remove the worktree
after the run.

## The run

Each step names where it is done and what to see. Record the time and a screenshot for each check marked (S).

| # | Where | Do | See |
|---|---|---|---|
| 1 | Terminal | Record the starting state: `ls -d /Applications/SCAT*`; `security find-generic-password -s scat-chat >/dev/null && echo item`; `docker images --format '{{.Repository}}:{{.Tag}}'`; `ls ~/Library/Application\ Support` | one earlier app, the item, the earlier image, the earlier state folder (S) |
| 2 | Finder | Drag `~/Desktop/SCATLAB.app` into Applications and open it from there | macOS stops it once (not signed): right-click, Open; the person-facing text says only SCATLAB |
| 3 | Menu bar | Watch the dot | grey, then (after the question) green; the menu title is SCATLAB |
| 4 | SCATLAB | The question `Serve <vault>?` | it names the lab vault remembered by the earlier app, with no first-time note, no folder picker |
| 5 | Terminal | Repeat step 1's commands | `/Applications` holds `SCATLAB.app` only; the keychain has `scatlab` and no `scat-chat`; `docker images` has no `scat-chat-mcp` and no `scat-kg-tools` image, and one image for SCATLAB; `~/Library/Application Support` has `SCATLAB` and no earlier folder (S) |
| 6 | SCATLAB menu | Click Copy address, then Copy key, and connect in Claude (the connector steps of `docs/chat-path.md`) | Claude lists the server's tools; ask it to run the check on the lab vault: "no problems found" |
| 7 | SCATLAB menu | Stop | the alert says what was switched off; the dot goes; the keychain has no `scatlab` item; `docker ps -a` lists no container; Funnel is off (`tailscale funnel status`) |
| 8 | Terminal | Start SCATLAB again from Applications, then Stop | no question about the earlier app, no earlier item reappears, one image still |
| 9 | Finder | Open SCATLAB from `~/Desktop` while a copy is in Applications | it offers to move itself and replaces the copy in Applications; there is still one app |

## Pass

Steps 5, 7 and 8 show one app, one keychain item (during a session) and one image, with the remembered vault used at
step 4; step 6 connects. Anything else is a finding; a defect against WP37-R2 is fixed on `dev` and the run repeated.

## What is not covered

An earlier app kept outside `/Applications` (a Downloads folder, say) is not found and not removed: the new app removes
the one at `/Applications`. If the chief engineer has one elsewhere, remove it by hand and note it here.
