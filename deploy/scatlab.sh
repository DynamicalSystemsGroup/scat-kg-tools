#!/bin/sh
# SCATLAB launcher: start, stop, status, copy-key, copy-address, change-vault. POSIX sh.
#
# The coder double-clicks SCATLAB.app (a menu-bar item), which calls this script with these verbs only, never with
# a value; nobody types a command. Every message says what happened and what to click next. The script keeps
# $STATE/ui (state, vault, address, then a problem line; never the key) for the app to show.
# Stop always runs: the menu's Stop, quitting the app, and any failure
# after start end in the same teardown (tunnel off, container removed, Mac allowed to sleep, key deleted,
# clipboard cleared), which is safe to run twice and when nothing is running.
#
# Every outside program is found through an environment override, so a test can replace it:
#   SCATLAB_DOCKER, SCATLAB_COLIMA, SCATLAB_TAILSCALE, SCATLAB_OPENSSL, SCATLAB_CURL,
#   SCATLAB_PBCOPY, SCATLAB_PBPASTE, SCATLAB_CAFFEINATE, SCATLAB_OSASCRIPT, SCATLAB_OPEN,
#   SCATLAB_SECURITY (the macOS keychain tool; only the key_* functions call it)
# Other settings: SCATLAB_SEARCH_PATH (folders searched first for the programs; for tests), SCATLAB_HOME (state folder), SCATLAB_CONTEXT (the source to build), SCATLAB_PORT,
#   SCATLAB_WAIT, SCATLAB_TUNNEL_WAIT, SCATLAB_UI.
# SCATLAB_VAULT is for tests only: it names the vault and skips the "Serve <vault>?" question, which every start
# otherwise asks. It works only when SCATLAB_UI=plain, which the app never sets.
# SCATLAB_UI=plain prints instead of showing dialogs, and takes answers from SCATLAB_A_<KEY> or stdin:
#   USE (Use it / Choose another: the question about the remembered vault), VAULT (a folder), COPY (copy), OPEN (open),
#   COPYKEY (copy: the Copy key menu item), STOP (stop). In plain mode start returns once the session is up,
#   unless SCATLAB_A_STOP=stop (the Stop menu item), which tears down at once.

# Where `docker` may live: Homebrew (Intel, Apple silicon) and Docker Desktop's own folder.
SEARCH=${SCATLAB_SEARCH_PATH:-/usr/local/bin:/opt/homebrew/bin:/Applications/Docker.app/Contents/Resources/bin}
PATH="$SEARCH:$PATH"
export PATH

HERE=$(cd "$(dirname "$0")" && pwd -P)
if [ -n "${SCATLAB_CONTEXT:-}" ]; then
    CTX=$SCATLAB_CONTEXT
elif [ -d "$HERE/context" ]; then
    CTX=$HERE/context
else
    CTX=$(cd "$HERE/.." && pwd -P)
fi
STATE=${SCATLAB_HOME:-$HOME/Library/Application Support/SCATLAB}
PORT=${SCATLAB_PORT:-8765}
UI=${SCATLAB_UI:-dialog}
WAIT=${SCATLAB_WAIT:-60}
TUNNEL_WAIT=${SCATLAB_TUNNEL_WAIT:-20}
DOCKER=${SCATLAB_DOCKER:-docker}
COLIMA=${SCATLAB_COLIMA:-colima}
TAILSCALE=${SCATLAB_TAILSCALE:-tailscale}
OPENSSL=${SCATLAB_OPENSSL:-openssl}
CURL=${SCATLAB_CURL:-curl}
PBCOPY=${SCATLAB_PBCOPY:-pbcopy}
PBPASTE=${SCATLAB_PBPASTE:-pbpaste}
CAFFEINATE=${SCATLAB_CAFFEINATE:-caffeinate}
OSASCRIPT=${SCATLAB_OSASCRIPT:-osascript}
OPEN=${SCATLAB_OPEN:-open}
SECURITY=${SCATLAB_SECURITY:-/usr/bin/security}

IMAGE=scatlab-mcp
# The published image: one per package version, read from the pyproject.toml that travels with the launcher.
REGISTRY_IMAGE=ghcr.io/dynamicalsystemsgroup/scat-tools
CONTAINER=scatlab
KEY_SERVICE=scatlab # the keychain item: service and account
FUNNEL_POLICY_PAGE=https://login.tailscale.com/f/funnel
DNS_PAGE=https://login.tailscale.com/admin/dns
INIT='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"scatlab","version":"0"}}}'

CLEANUP=0
FAILMSG=""
SIGNALED=0
DPID=""
RESULT=""
VAULT=""
URL=""

have() { command -v "$1" >/dev/null 2>&1; }

# shellcheck source=/dev/null
. "$HERE/retire-old.sh" # retire_old: an installed copy of the earlier name is replaced, once per Mac

# ---------------------------------------------------------------- UI

ui_note() { # message: shown until the coder clicks OK
    if [ "$UI" = plain ]; then
        printf '%s\n' "$1"
    else
        "$OSASCRIPT" -e 'on run argv' \
            -e 'display dialog (item 1 of argv) with title "SCATLAB" buttons {"OK"} default button "OK"' \
            -e 'end run' "$1" >/dev/null 2>&1 || true
    fi
}

ui_progress() { # message: no click needed
    if [ "$UI" = plain ]; then
        printf '%s\n' "$1"
    else
        "$OSASCRIPT" -e 'on run argv' \
            -e 'display notification (item 1 of argv) with title "SCATLAB"' \
            -e 'end run' "$1" >/dev/null 2>&1 || true
    fi
}

plain_answer() { # KEY: the answer from SCATLAB_A_<KEY>, else a line of stdin
    eval "plain_a=\${SCATLAB_A_$1:-}"
    if [ -z "$plain_a" ]; then
        IFS= read -r plain_a || plain_a=""
    fi
    printf '%s' "$plain_a"
}

ui_choice() { # KEY message button1 button2: prints the button clicked, or nothing
    if [ "$UI" = plain ]; then
        printf '%s\n[%s / %s]\n' "$2" "$3" "$4" >&2
        plain_answer "$1"
    else
        "$OSASCRIPT" -e 'on run argv' \
            -e 'try' \
            -e 'return button returned of (display dialog (item 1 of argv) with title "SCATLAB" buttons {item 3 of argv, item 2 of argv} default button (item 2 of argv))' \
            -e 'on error' -e 'return ""' -e 'end try' \
            -e 'end run' "$2" "$3" "$4" 2>/dev/null || true
    fi
}

ui_folder() { # KEY message: prints the folder chosen, or nothing
    if [ "$UI" = plain ]; then
        printf '%s\n' "$2" >&2
        plain_answer "$1"
    else
        "$OSASCRIPT" -e 'on run argv' \
            -e 'try' \
            -e 'return POSIX path of (choose folder with prompt (item 1 of argv))' \
            -e 'on error' -e 'return ""' -e 'end try' \
            -e 'end run' "$2" 2>/dev/null | sed 's|/$||' || true
    fi
}

hold() { # message (never the key): dialog mode waits here until a signal (the Stop verb) ends the session
    if [ "$UI" = plain ]; then
        printf '%s\n' "$1"
        if [ "$(plain_answer_env COPYKEY)" = copy ]; then
            copy_key
            printf 'The key is on your clipboard.\n'
        fi
        if [ "$(plain_answer_env STOP)" = stop ]; then
            return 0
        fi
        printf 'SCATLAB is running. To stop it: %s stop\n' "$0"
        CLEANUP=0
        exit 0
    fi
    ui_progress "SCATLAB is running. Click its dot in the menu bar: Copy address, then Copy key, and paste each into the chat."
    while :; do
        sleep 86400 &
        DPID=$!
        wait "$DPID" 2>/dev/null
        DPID=""
    done
}

ui_state() { # state [problem]: the app's state file, by a rename so the app never reads half of it (never the key)
    us_p=$(printf '%s' "${2:-}" | tr '\n' ' ')
    {
        printf '%s\n%s\n%s\n' "$1" "$(printf '%s' "$VAULT" | tr '\n' ' ')" "$(printf '%s' "$URL" | tr '\n' ' ')"
        [ -z "$us_p" ] || printf '%s\n' "$us_p"
    } >"$STATE/ui.tmp" && mv -f "$STATE/ui.tmp" "$STATE/ui"
}

first_note() { # once per Mac (the marker is in the state folder): where the app now lives
    [ ! -f "$STATE/menubar-note" ] || return 0
    ui_note "SCATLAB now lives in the menu bar, at the top of your screen, near the clock: look for a small dot (grey while it starts, green when it is running, red if there is a problem). Click the dot for its menu: Copy address, Copy key, Change vault and Stop. There is no window."
    : >"$STATE/menubar-note"
}

copy_key() { # the only way the key reaches the clipboard: the coder asked for it
    ck=$(key_get) || return 1
    [ -n "$ck" ] || return 1
    printf '%s' "$ck" | "$PBCOPY"
}

plain_answer_env() { # KEY: the environment answer only (never reads stdin)
    eval "printf '%s' \"\${SCATLAB_A_$1:-}\""
}

die() { # message: stop here; the exit handler shows it with the teardown's sentence
    FAILMSG=$1
    exit 1
}

# ---------------------------------------------------------------- the key
# The session key lives in the macOS login keychain for one session. Only these functions name `security`; it is the
# macOS-specific part (a Linux version replaces just these four). The key never goes on a command line: it is written
# as a command on the stdin of `security -i`, and read with `find-generic-password -w` into a pipe.

new_key() {
    if have "$OPENSSL"; then
        "$OPENSSL" rand -hex 32
    else
        od -An -N32 -tx1 /dev/urandom | tr -d ' \n'
    fi
}

key_put() { # key: store it (replacing any item left by a crashed session)
    printf 'add-generic-password -U -s "%s" -a "%s" -w "%s"\n' "$KEY_SERVICE" "$KEY_SERVICE" "$1" |
        "$SECURITY" -i >/dev/null 2>&1
}

key_get() { # prints the key, or nothing when there is none
    kg=$("$SECURITY" find-generic-password -s "$KEY_SERVICE" -a "$KEY_SERVICE" -w 2>/dev/null) || return 1
    printf '%s' "$kg"
}

key_drop() { # deletes the item; safe when there is none
    "$SECURITY" delete-generic-password -s "$KEY_SERVICE" -a "$KEY_SERVICE" >/dev/null 2>&1 || true
}

key_present() {
    "$SECURITY" find-generic-password -s "$KEY_SERVICE" -a "$KEY_SERVICE" >/dev/null 2>&1
}

# ---------------------------------------------------------------- checks of the outside world

in_private() { # path: a folder macOS privacy hides from the container runtime (RS3 finding 1)
    case "$1" in
    "$HOME_REAL/Documents" | "$HOME_REAL/Documents/"* | "$HOME_REAL/Desktop" | "$HOME_REAL/Desktop/"* | \
        "$HOME_REAL/Downloads" | "$HOME_REAL/Downloads/"* | "$HOME_REAL/Library/Mobile Documents" | \
        "$HOME_REAL/Library/Mobile Documents/"*) return 0 ;;
    esac
    return 1
}

tailscale_json() { "$TAILSCALE" status --json 2>/dev/null; }

json_first() { # key: the first string value of "key" in the JSON on stdin
    sed -n 's/.*"'"$1"'": *"\([^"]*\)".*/\1/p' | head -1
}

https_on() { # status JSON in $1: the tailnet has HTTPS certificates (CertDomains is not empty)
    printf '%s\n' "$1" | grep '"CertDomains"' | grep -q '\[$' || return 1
    printf '%s\n' "$1" | sed -n '/"CertDomains"/,/\]/p' | sed 1d | grep -q '"'
}

funnel_status() { "$TAILSCALE" funnel status 2>&1; }

funnel_url() { # the public https address now published, if any
    funnel_status | grep -Eo 'https://[A-Za-z0-9._-]+(:[0-9]+)?' | head -1
}

http_code() { # 0|1: the status of a POST to the server, without the key (0) or with it (1)
    if [ "$1" = 1 ]; then
        printf 'header = "Authorization: Bearer %s"\n' "$(key_get)" |
            "$CURL" -s -m 5 -K - -o /dev/null -w '%{http_code}' -X POST \
                -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
                -d "$INIT" "http://127.0.0.1:$PORT/mcp" 2>/dev/null
    else
        "$CURL" -s -m 5 -o /dev/null -w '%{http_code}' -X POST \
            -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
            -d "$INIT" "http://127.0.0.1:$PORT/mcp" 2>/dev/null
    fi
}

container_running() {
    [ -n "$("$DOCKER" ps -q --filter "name=^${CONTAINER}\$" 2>/dev/null)" ]
}

# ---------------------------------------------------------------- teardown

wait_dead() { # pid
    wd_i=0
    while kill -0 "$1" 2>/dev/null && [ "$wd_i" -lt 20 ]; do
        sleep 0.1
        wd_i=$((wd_i + 1))
    done
    ! kill -0 "$1" 2>/dev/null
}

live_launcher() { # pid: true only for a live launcher (a reused pid of some other program does not count)
    [ -n "$1" ] && kill -0 "$1" 2>/dev/null && ps -p "$1" -o command= 2>/dev/null | grep -q 'scatlab'
}

# Everything the session started, off; each step verified. Sets RESULT to one plain sentence.
teardown() {
    bad=""
    oldkey=$(key_get)

    if [ -f "$STATE/tunnel" ]; then
        if have "$TAILSCALE"; then
            "$TAILSCALE" funnel --https=443 off >/dev/null 2>&1
            if [ -n "$(funnel_url)" ]; then
                "$TAILSCALE" funnel reset >/dev/null 2>&1
            fi
            if [ -n "$(funnel_url)" ]; then
                bad="$bad the public link may still be on (open Tailscale and switch Funnel off);"
            else
                rm -f "$STATE/tunnel"
            fi
        else
            bad="$bad the public link could not be checked because Tailscale was not found;"
        fi
    fi

    if have "$DOCKER" && "$DOCKER" info >/dev/null 2>&1; then
        "$DOCKER" rm -f "$CONTAINER" >/dev/null 2>&1
        if [ -n "$("$DOCKER" ps -a -q --filter "name=^${CONTAINER}\$" 2>/dev/null)" ]; then
            bad="$bad the server container is still there (restart your Mac to be sure);"
        fi
    fi

    if [ -f "$STATE/caffeinate.pid" ]; then
        cp_pid=$(cat "$STATE/caffeinate.pid")
        if [ -n "$cp_pid" ] && ps -p "$cp_pid" -o command= 2>/dev/null | grep -q "$(basename "$CAFFEINATE")"; then
            kill "$cp_pid" 2>/dev/null
            wait "$cp_pid" 2>/dev/null
            wait_dead "$cp_pid" || kill -9 "$cp_pid" 2>/dev/null
        fi
        if [ -n "$cp_pid" ] && kill -0 "$cp_pid" 2>/dev/null && ps -p "$cp_pid" -o command= | grep -q "$(basename "$CAFFEINATE")"; then
            bad="$bad your Mac may stay awake (restart it to be sure);"
        else
            rm -f "$STATE/caffeinate.pid"
        fi
    fi

    key_drop
    if key_present; then
        bad="$bad the key could not be deleted (open Keychain Access and delete the item named $KEY_SERVICE);"
    fi
    rm -f "$STATE/key.env" # a key file left by an earlier version of this launcher

    if [ -n "$oldkey" ] && [ "$("$PBPASTE" 2>/dev/null)" = "$oldkey" ]; then
        printf '' | "$PBCOPY"
        if [ "$("$PBPASTE" 2>/dev/null)" = "$oldkey" ]; then
            bad="$bad the key is still on your clipboard (copy something else over it);"
        fi
    fi

    rm -f "$STATE/session" "$STATE/session.txt"
    if [ -z "$bad" ]; then
        RESULT="Stopped. The public link is off, the server is removed, your Mac may sleep again, the key was deleted, and your clipboard holds no key."
    else
        RESULT="Stopped, but I could not confirm:$bad choose Stop in the SCATLAB menu to try again, or restart your Mac, to be sure."
    fi
}

on_exit() {
    rc=$?
    trap - EXIT
    if [ -n "$DPID" ]; then
        kill "$DPID" 2>/dev/null
    fi
    if [ "$CLEANUP" = 1 ]; then
        teardown
        if [ -z "$FAILMSG" ] && [ "$SIGNALED" = 0 ] && [ "$rc" != 0 ]; then
            FAILMSG="SCATLAB stopped unexpectedly."
        fi
        if [ -n "$FAILMSG" ]; then # the app shows a problem as a red dot and one alert; plain mode prints it
            case "$RESULT" in
            "Stopped, but"*) ui_state problem "$FAILMSG $RESULT" ;;
            *) ui_state problem "$FAILMSG" ;;
            esac
        else
            ui_state stopped
        fi
        if [ "$UI" = plain ]; then
            if [ "$SIGNALED" != 0 ]; then
                printf '%s\n' "$RESULT"
            elif [ -n "$FAILMSG" ]; then
                ui_note "$FAILMSG

$RESULT"
            else
                ui_note "$RESULT"
            fi
        fi
    fi
    exit "$rc"
}

# ---------------------------------------------------------------- start

step_tools() {
    ui_state starting
    if ! have "$DOCKER"; then
        die "SCATLAB needs a container runtime: Colima or Docker Desktop. Neither is installed. Install one once, as the chat-path guide shows under 'Install once', then choose Stop in the SCATLAB menu, then open SCATLAB again."
    fi
    if have "$COLIMA"; then
        if ! "$COLIMA" status >/dev/null 2>&1; then
            ui_progress "Starting Colima, the program that runs the server's container. This can take a minute."
            "$COLIMA" start >"$STATE/colima.log" 2>&1 ||
                die "Colima would not start. Restart your Mac, then choose Stop in the SCATLAB menu, then open SCATLAB again. If it still fails, tell the person who set this up that Colima's start failed."
        fi
    elif ! "$DOCKER" info >/dev/null 2>&1; then
        die "Docker Desktop is not running. Open Docker Desktop from your Applications folder, wait until it says it is running, then choose Stop in the SCATLAB menu, then open SCATLAB again."
    fi
    "$DOCKER" info >/dev/null 2>&1 ||
        die "Docker does not answer. Restart your Mac, then choose Stop in the SCATLAB menu, then open SCATLAB again."

    if ! have "$TAILSCALE"; then
        die "SCATLAB needs Tailscale, which makes the public link, and it is not installed. Install it once, as the chat-path guide shows under 'Install once', sign in, then choose Stop in the SCATLAB menu, then open SCATLAB again."
    fi
    TS_JSON=$(tailscale_json)
    if ! printf '%s\n' "$TS_JSON" | grep -q '"BackendState": *"Running"'; then
        die "Tailscale is not running or you are not signed in. Open Tailscale from the menu bar at the top of your screen, sign in, then choose Stop in the SCATLAB menu, then open SCATLAB again."
    fi
    MACHINE=$(printf '%s\n' "$TS_JSON" | json_first HostName)
    NODE_ID=$(printf '%s\n' "$TS_JSON" | json_first ID)
    if ! https_on "$TS_JSON"; then
        ans=$(ui_choice OPEN "Tailscale needs HTTPS switched on, once, before the public link can work.

First look at the name: Tailscale calls this Mac \"$MACHINE\". Switching HTTPS on puts that name in a public record that can never be erased. If it has your name or anything private in it, rename the Mac first in Tailscale (Machines, then Edit machine name), and only then switch HTTPS on.

SCATLAB never switches HTTPS on for you. When the name is right, click 'Open the page', switch on Enable HTTPS, then choose Stop in the SCATLAB menu, then open SCATLAB again." "Open the page" "Close")
        if [ "$ans" = "Open the page" ]; then
            "$OPEN" "$DNS_PAGE" >/dev/null 2>&1
        fi
        die "Nothing was started: HTTPS is not switched on in Tailscale yet (the page is $DNS_PAGE). Once that is done, choose Stop in the SCATLAB menu, then open SCATLAB again."
    fi
}

step_vault() {
    ui_state starting
    VAULT=""
    if [ "$UI" = plain ]; then
        VAULT=${SCATLAB_VAULT:-} # test override only: honoured in plain mode, which the app never sets
    fi
    if [ -z "$VAULT" ] && [ -f "$STATE/vault" ]; then
        VAULT=$(cat "$STATE/vault")
        if [ ! -d "$VAULT" ]; then
            ui_note "The vault folder I remembered is gone ($VAULT). Choose it again on the next screen."
            VAULT=""
        else # a remembered vault is offered, never used silently
            ans=$(ui_choice USE "Serve $VAULT?" "Use it" "Choose another")
            case "$ans" in
            "Use it" | use) ;;
            "Choose another" | another) VAULT="" ;;
            *) die "No vault was confirmed, so nothing was started. Choose Stop in the SCATLAB menu, then open SCATLAB again and say whether to use $VAULT." ;;
            esac
        fi
    fi
    if [ -z "$VAULT" ]; then
        VAULT=$(ui_folder VAULT "Choose your vault: the folder that holds your narratives (it has a file called scat.toml).")
        [ -n "$VAULT" ] || die "No vault was chosen, so nothing was started. Choose Stop in the SCATLAB menu, then open SCATLAB again and choose your vault folder."
    fi
    VAULT=$(cd "$VAULT" 2>/dev/null && pwd -P) || die "I cannot open that folder. Choose Stop in the SCATLAB menu, then open SCATLAB again and choose your vault folder."

    if in_private "$VAULT"; then
        COPY_TO=$HOME_REAL/SCAT/vault
        if [ -e "$COPY_TO" ]; then
            die "Your vault is in a folder that macOS protects, so the server cannot read it, and ~/SCAT/vault already exists, so I will not copy over it. Choose Stop in the SCATLAB menu, then open SCATLAB again and choose ~/SCAT/vault, or a folder outside Documents, Desktop, Downloads and iCloud."
        fi
        ans=$(ui_choice COPY "Your vault is in $VAULT, a folder that macOS keeps private from the server's container, so the server cannot read it there.

I can make a copy in ~/SCAT/vault and use the copy. Your original stays where it is; I never move it. Edits you make in the copy have to be brought back to your original through git: commit and push from the copy, then pull in the original.

Make the copy now?" "Copy" "Cancel")
        [ "$ans" = "Copy" ] || [ "$ans" = "copy" ] || die "Nothing was copied or started. Move your vault outside Documents, Desktop, Downloads and iCloud, or choose Stop in the SCATLAB menu, then open SCATLAB again and say Copy."
        if ! { mkdir -p "$COPY_TO" && cp -R "$VAULT/." "$COPY_TO/"; }; then
            rm -rf "$COPY_TO"
            die "The copy failed, so nothing was started. If macOS asked whether SCATLAB may use your Documents folder, click Allow; then choose Stop in the SCATLAB menu, then open SCATLAB again."
        fi
        VAULT=$COPY_TO
        ui_progress "Copied your vault to ~/SCAT/vault. Remember: edits made there must be pulled back through git."
    fi
    printf '%s\n' "$VAULT" >"$STATE/vault"
}

src_tag() { # a tag that changes when the source changes (the image runs as any user: --user is set at run time)
    st_hash=$(
        cd "$CTX" || exit 1
        {
            find src -type f -not -name '*.pyc' -not -path '*/__pycache__/*'
            echo pyproject.toml
            echo ontology/scat.ttl
            echo deploy/Dockerfile
        } | LC_ALL=C sort | tr '\n' '\0' | xargs -0 cat | shasum -a 256 | cut -c1-12
    )
    printf '%s:%s' "$IMAGE" "$st_hash"
}

pkg_version() { # default: the first `version = "..."` line of pyproject.toml; empty when there is none
    sed -n 's/^version *= *"\([^"]*\)".*/\1/p' "$CTX/pyproject.toml" 2>/dev/null | head -n 1
}

step_image() {
    ui_state starting
    # Use the published image of this version when there is one; build the source here only when there is none,
    # so a candidate works before its release.
    TAG=$(src_tag)
    PUBLISHED=$REGISTRY_IMAGE:$(pkg_version)
    if [ -n "$(pkg_version)" ] && "$DOCKER" image inspect "$PUBLISHED" >/dev/null 2>&1; then
        TAG=$PUBLISHED
        return 0
    fi
    "$DOCKER" image inspect "$TAG" >/dev/null 2>&1 && return 0
    if [ -n "$(pkg_version)" ]; then
        ui_progress "Fetching the server, once."
        if "$DOCKER" pull "$PUBLISHED" >"$STATE/build.log" 2>&1; then
            TAG=$PUBLISHED
            return 0
        fi
    fi
    [ -f "$CTX/deploy/Dockerfile" ] || die "The server's recipe is missing from this copy of SCATLAB. Download the app again."
    ui_progress "Building the server, once. The first time takes a few minutes."
    if ! "$DOCKER" build -f "$CTX/deploy/Dockerfile" -t "$TAG" "$CTX" >"$STATE/build.log" 2>&1; then
        die "Building the server failed. The last lines say: $(tail -n 5 "$STATE/build.log" | tr '\n' ' ')
Check that you are online, then choose Stop in the SCATLAB menu, then open SCATLAB again."
    fi
}

step_server() {
    ui_state starting
    if ! { key_put "$(new_key)" && key_present; }; then
        die "I could not keep a new key in your keychain. If macOS asked for permission, click Allow; then choose Stop in the SCATLAB menu, then open SCATLAB again."
    fi
    "$DOCKER" rm -f "$CONTAINER" >/dev/null 2>&1
    printf 'SCAT_MCP_KEY=%s\n' "$(key_get)" |
        "$DOCKER" run -d --name "$CONTAINER" --read-only --tmpfs /tmp --user "$HOST_UID:$HOST_GID" \
        --security-opt no-new-privileges --cap-drop ALL \
        -p "127.0.0.1:$PORT:8765" -v "$VAULT:/vault" --env-file /dev/stdin "$TAG" >/dev/null 2>"$STATE/run.log" ||
        die "The server would not start: $(tail -n 3 "$STATE/run.log" | tr '\n' ' ')
Make sure no other SCATLAB is open and port $PORT is free, then choose Stop in the SCATLAB menu, then open SCATLAB again."

    ui_progress "Waiting for the server to answer."
    i=0
    code=""
    while [ "$i" -lt $((WAIT * 5)) ]; do
        code=$(http_code 0)
        [ "$code" = 401 ] && break
        if ! container_running; then
            die "The server stopped right after starting. Its last words: $("$DOCKER" logs --tail 5 "$CONTAINER" 2>&1 | tr '\n' ' ')
Choose Stop in the SCATLAB menu, then open SCATLAB again; if it repeats, tell the person who set this up."
        fi
        i=$((i + 1))
        sleep 0.2
    done
    [ "$code" = 401 ] || die "The server did not answer within $WAIT seconds. Choose Stop in the SCATLAB menu, then open SCATLAB again; if it repeats, tell the person who set this up."
    [ "$(http_code 1)" = 200 ] || die "The server answers but does not accept its own key. Choose Stop in the SCATLAB menu, then open SCATLAB again; if it repeats, tell the person who set this up."
}

step_tunnel() {
    ui_state starting
    : >"$STATE/tunnel"
    ui_progress "Switching on the public link."
    "$TAILSCALE" funnel --bg "$PORT" >"$STATE/funnel.log" 2>&1 &
    fpid=$!
    i=0
    while [ "$i" -lt $((TUNNEL_WAIT * 5)) ]; do
        PUBLIC=$(funnel_url)
        [ -n "$PUBLIC" ] && break
        i=$((i + 1))
        sleep 0.2
    done
    if kill -0 "$fpid" 2>/dev/null; then
        kill "$fpid" 2>/dev/null
    fi
    wait "$fpid" 2>/dev/null
    if [ -z "$PUBLIC" ]; then
        page=$(grep -Eo 'https://login\.tailscale\.com/[^ ]*' "$STATE/funnel.log" | head -1)
        if [ -z "$page" ]; then
            page=$FUNNEL_POLICY_PAGE
            [ -n "$NODE_ID" ] && page="$page?node=$NODE_ID"
        fi
        ans=$(ui_choice OPEN "The public link did not start. The usual reason is that Funnel is not allowed on your Tailscale account yet. That takes one click, once: click 'Open the page', approve Funnel there, then choose Stop in the SCATLAB menu, then open SCATLAB again." "Open the page" "Close")
        if [ "$ans" = "Open the page" ]; then
            "$OPEN" "$page" >/dev/null 2>&1
        fi
        die "The public link did not start (Funnel is probably not allowed yet: $page). Once that is done, choose Stop in the SCATLAB menu, then open SCATLAB again."
    fi
    URL=$PUBLIC/mcp
}

step_awake() {
    ui_state starting
    "$CAFFEINATE" -i -s </dev/null >/dev/null 2>&1 &
    printf '%s\n' "$!" >"$STATE/caffeinate.pid"
}

cmd_start() {
    mkdir -p "$STATE" && chmod 700 "$STATE" || exit 1
    if [ -f "$STATE/session" ]; then
        old=$(cat "$STATE/session")
        if [ "$UI" = dialog ] && ! live_launcher "$old"; then
            teardown # a crashed earlier session: clean up, then go on
        else
            VAULT=$(cat "$STATE/vault" 2>/dev/null) # the app may have just deleted ui: show the live session again
            URL=$(cat "$STATE/session.txt" 2>/dev/null)
            if [ -n "$URL" ]; then ui_state running; else ui_state starting; fi
            ui_note "SCATLAB is already running. Click Stop in its menu (or quit the app) before starting it again."
            exit 0
        fi
    fi
    printf '%s\n' "$$" >"$STATE/session"
    rm -f "$STATE/changing"
    CLEANUP=1
    trap on_exit EXIT
    trap 'SIGNALED=1; exit 1' INT TERM HUP

    HOME_REAL=$(cd "$HOME" && pwd -P)
    HOST_UID=$(id -u)
    HOST_GID=$(id -g)

    ui_state starting
    first_note
    step_tools
    retire_old
    step_vault
    step_image
    step_server
    step_tunnel
    step_awake

    printf '%s\n' "$URL" >"$STATE/session.txt"
    ui_state running
    hold "SCATLAB is running.

1. In the chat, open MCP settings and add a server.
2. Paste this address:
$URL
3. Choose API key as the authentication. Click Copy key in the SCATLAB menu, then paste the key in the chat. The key is never shown on screen.

Vault: $VAULT
Your Mac stays awake while SCATLAB is open. Click Stop in its menu when you are done: that switches everything off and deletes the key."
}

# ---------------------------------------------------------------- stop, status

do_stop() { # the teardown with the session's own process stopped first; returns 1 when it could not confirm
    mkdir -p "$STATE" || exit 1
    HOME_REAL=$(cd "$HOME" && pwd -P)
    if [ -f "$STATE/session" ]; then
        sp=$(cat "$STATE/session")
        if [ "$sp" != "$$" ] && live_launcher "$sp"; then
            kill "$sp" 2>/dev/null
            wait_dead "$sp"
        fi
    fi
    teardown
    VAULT=""
    URL=""
    printf '%s\n' "$RESULT"
    case "$RESULT" in
    "Stopped, but"*) # not confirmed: a red dot and one alert, and the app stays so that Stop can try again
        ui_state problem "$RESULT"
        return 1
        ;;
    esac
    ui_state stopped
    return 0
}

cmd_stop() {
    mkdir -p "$STATE" || exit 1
    rm -f "$STATE/changing"
    do_stop || exit 1
}

cmd_status() {
    cm=$(cat "$STATE/changing" 2>/dev/null) # Change vault is between two sessions, while its process lives
    if [ -n "$cm" ] && ! kill -0 "$cm" 2>/dev/null; then
        rm -f "$STATE/changing"
        cm=""
    fi
    sp=$(cat "$STATE/session" 2>/dev/null)
    if [ "$UI" = dialog ] && [ -n "$sp" ] && ! live_launcher "$sp"; then
        sp="" # the launcher was killed: a dead session is not "starting"; the app then quits, and its stop cleans up
        [ -n "$cm" ] || { printf 'SCATLAB is not running.\n'; exit 1; }
    fi
    if [ -n "$sp" ] || [ -n "$cm" ]; then
        if [ -f "$STATE/session" ] && [ -f "$STATE/session.txt" ]; then
            printf 'SCATLAB is running at %s\n' "$(cat "$STATE/session.txt")"
        else
            printf 'SCATLAB is starting.\n'
        fi
        exit 0
    fi
    printf 'SCATLAB is not running.\n'
    exit 1
}

cmd_copy_key() {
    if ! copy_key; then
        printf 'There is no key: SCATLAB is not running.\n'
        exit 1
    fi
    ui_progress "The key is on your clipboard."
}

cmd_copy_address() {
    ca=$(cat "$STATE/session.txt" 2>/dev/null)
    if [ -z "$ca" ]; then
        printf 'There is no address yet: SCATLAB is not running.\n'
        exit 1
    fi
    printf '%s' "$ca" | "$PBCOPY"
    ui_progress "The address is on your clipboard."
}

cmd_change_vault() { # stop, then start again with the vault chooser; the session key is new, so the chat's server entry needs updating
    mkdir -p "$STATE" || exit 1
    printf '%s\n' "$$" >"$STATE/changing" # this process's pid: a marker whose process is gone is stale
    if ! do_stop; then
        rm -f "$STATE/changing"
        exit 1
    fi
    rm -f "$STATE/vault"
    cmd_start
}

case "${1:-}" in
start) cmd_start ;;
stop) cmd_stop ;;
status) cmd_status ;;
copy-key) cmd_copy_key ;;
copy-address) cmd_copy_address ;;
change-vault) cmd_change_vault ;;
*)
    printf 'usage: %s start | stop | status | copy-key | copy-address | change-vault\n' "$0" >&2
    exit 2
    ;;
esac
