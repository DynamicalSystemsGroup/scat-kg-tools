#!/bin/sh
# SCAT Chat launcher: start, stop, status. POSIX sh.
#
# The coder double-clicks SCAT Chat.app, which calls this script; nobody types a command. Every message says
# what happened and what to click next. Stop always runs: the Stop button, quitting the app, and any failure
# after start end in the same teardown (tunnel off, container removed, Mac allowed to sleep, key deleted,
# clipboard cleared), which is safe to run twice and when nothing is running.
#
# Every outside program is found through an environment override so tests can use stand-ins:
#   SCAT_CHAT_DOCKER, SCAT_CHAT_COLIMA, SCAT_CHAT_TAILSCALE, SCAT_CHAT_OPENSSL, SCAT_CHAT_CURL,
#   SCAT_CHAT_PBCOPY, SCAT_CHAT_PBPASTE, SCAT_CHAT_CAFFEINATE, SCAT_CHAT_OSASCRIPT, SCAT_CHAT_OPEN,
#   SCAT_CHAT_SECURITY (the macOS keychain tool; only the key_* functions call it)
# Other settings: SCAT_CHAT_SEARCH_PATH (folders searched first for the programs; for tests), SCAT_CHAT_HOME (state folder), SCAT_CHAT_CONTEXT (the source to build), SCAT_CHAT_PORT,
#   SCAT_CHAT_VAULT, SCAT_CHAT_WAIT, SCAT_CHAT_TUNNEL_WAIT, SCAT_CHAT_UI.
# SCAT_CHAT_UI=plain prints instead of showing dialogs, and takes answers from SCAT_CHAT_A_<KEY> or stdin:
#   VAULT (a folder), COPY (copy), OPEN (open), COPYKEY (copy: the Copy key button), STOP (stop). In plain mode start returns once the session is up,
#   unless SCAT_CHAT_A_STOP=stop (the Stop button), which tears down at once.

# Where `docker` may live: Homebrew (Intel, Apple silicon) and Docker Desktop's own folder.
SEARCH=${SCAT_CHAT_SEARCH_PATH:-/usr/local/bin:/opt/homebrew/bin:/Applications/Docker.app/Contents/Resources/bin}
PATH="$SEARCH:$PATH"
export PATH

HERE=$(cd "$(dirname "$0")" && pwd -P)
if [ -n "${SCAT_CHAT_CONTEXT:-}" ]; then
    CTX=$SCAT_CHAT_CONTEXT
elif [ -d "$HERE/context" ]; then
    CTX=$HERE/context
else
    CTX=$(cd "$HERE/.." && pwd -P)
fi
STATE=${SCAT_CHAT_HOME:-$HOME/Library/Application Support/SCAT Chat}
PORT=${SCAT_CHAT_PORT:-8765}
UI=${SCAT_CHAT_UI:-dialog}
WAIT=${SCAT_CHAT_WAIT:-60}
TUNNEL_WAIT=${SCAT_CHAT_TUNNEL_WAIT:-20}
DOCKER=${SCAT_CHAT_DOCKER:-docker}
COLIMA=${SCAT_CHAT_COLIMA:-colima}
TAILSCALE=${SCAT_CHAT_TAILSCALE:-tailscale}
OPENSSL=${SCAT_CHAT_OPENSSL:-openssl}
CURL=${SCAT_CHAT_CURL:-curl}
PBCOPY=${SCAT_CHAT_PBCOPY:-pbcopy}
PBPASTE=${SCAT_CHAT_PBPASTE:-pbpaste}
CAFFEINATE=${SCAT_CHAT_CAFFEINATE:-caffeinate}
OSASCRIPT=${SCAT_CHAT_OSASCRIPT:-osascript}
OPEN=${SCAT_CHAT_OPEN:-open}
SECURITY=${SCAT_CHAT_SECURITY:-/usr/bin/security}

IMAGE=scat-chat-mcp
# The published image (WP21-G6): one per package version, read from the pyproject.toml that travels with the launcher.
REGISTRY_IMAGE=ghcr.io/dynamicalsystemsgroup/scat-kg-tools
CONTAINER=scat-chat
KEY_SERVICE=scat-chat # the keychain item: service and account
FUNNEL_POLICY_PAGE=https://login.tailscale.com/f/funnel
DNS_PAGE=https://login.tailscale.com/admin/dns
INIT='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"scat-chat","version":"0"}}}'

CLEANUP=0
FAILMSG=""
SIGNALED=0
DPID=""
RESULT=""

have() { command -v "$1" >/dev/null 2>&1; }

# ---------------------------------------------------------------- UI

ui_note() { # message: shown until the coder clicks OK
    if [ "$UI" = plain ]; then
        printf '%s\n' "$1"
    else
        "$OSASCRIPT" -e 'on run argv' \
            -e 'display dialog (item 1 of argv) with title "SCAT Chat" buttons {"OK"} default button "OK"' \
            -e 'end run' "$1" >/dev/null 2>&1 || true
    fi
}

ui_progress() { # message: no click needed
    if [ "$UI" = plain ]; then
        printf '%s\n' "$1"
    else
        "$OSASCRIPT" -e 'on run argv' \
            -e 'display notification (item 1 of argv) with title "SCAT Chat"' \
            -e 'end run' "$1" >/dev/null 2>&1 || true
    fi
}

plain_answer() { # KEY: the answer from SCAT_CHAT_A_<KEY>, else a line of stdin
    eval "plain_a=\${SCAT_CHAT_A_$1:-}"
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
            -e 'return button returned of (display dialog (item 1 of argv) with title "SCAT Chat" buttons {item 3 of argv, item 2 of argv} default button (item 2 of argv))' \
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

ui_hold() { # message (never the key): the dialog with the Copy key and Stop buttons; returns when the coder clicks Stop
    if [ "$UI" = plain ]; then
        printf '%s\n' "$1"
        if [ "$(plain_answer_env COPYKEY)" = copy ]; then
            copy_key
            printf 'The key is on your clipboard.\n'
        fi
        if [ "$(plain_answer_env STOP)" = stop ]; then
            return 0
        fi
        printf 'SCAT Chat is running. To stop it: %s stop\n' "$0"
        CLEANUP=0
        exit 0
    fi
    while :; do
        "$OSASCRIPT" -e 'on run argv' \
            -e 'try' \
            -e 'return button returned of (display dialog (item 1 of argv) with title "SCAT Chat" buttons {"Copy key", "Stop"} default button "Stop")' \
            -e 'on error' -e 'return "Stop"' -e 'end try' \
            -e 'end run' "$1" >"$STATE/hold.out" 2>/dev/null &
        DPID=$!
        wait "$DPID" 2>/dev/null
        DPID=""
        hold_a=$(cat "$STATE/hold.out" 2>/dev/null)
        rm -f "$STATE/hold.out"
        [ "$hold_a" = "Copy key" ] || break
        copy_key
        ui_progress "The key is on your clipboard."
    done
}

copy_key() { # the only way the key reaches the clipboard: the coder asked for it
    key_get | "$PBCOPY"
}

plain_answer_env() { # KEY: the environment answer only (never reads stdin)
    eval "printf '%s' \"\${SCAT_CHAT_A_$1:-}\""
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
        RESULT="Stopped, but I could not confirm:$bad click SCAT Chat again, then Stop, or restart your Mac, to be sure."
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
        if [ "$SIGNALED" = 0 ]; then
            if [ -n "$FAILMSG" ]; then
                ui_note "$FAILMSG

$RESULT"
            else
                ui_note "$RESULT"
            fi
        else
            printf '%s\n' "$RESULT"
        fi
    fi
    exit "$rc"
}

# ---------------------------------------------------------------- start

step_tools() {
    if ! have "$DOCKER"; then
        die "SCAT Chat needs a container runtime: Colima (recommended) or Docker Desktop. Neither is installed. Install one once, as the chat-path guide shows under 'Install once', then click SCAT Chat again."
    fi
    if have "$COLIMA"; then
        if ! "$COLIMA" status >/dev/null 2>&1; then
            ui_progress "Starting Colima, the program that runs the server's container. This can take a minute."
            "$COLIMA" start >"$STATE/colima.log" 2>&1 ||
                die "Colima would not start. Restart your Mac, then click SCAT Chat again. If it still fails, tell the person who set this up that Colima's start failed."
        fi
    elif ! "$DOCKER" info >/dev/null 2>&1; then
        die "Docker Desktop is not running. Open Docker Desktop from your Applications folder, wait until it says it is running, then click SCAT Chat again."
    fi
    "$DOCKER" info >/dev/null 2>&1 ||
        die "Docker does not answer. Restart your Mac, then click SCAT Chat again."

    if ! have "$TAILSCALE"; then
        die "SCAT Chat needs Tailscale, which makes the public link, and it is not installed. Install it once, as the chat-path guide shows under 'Install once', sign in, then click SCAT Chat again."
    fi
    TS_JSON=$(tailscale_json)
    if ! printf '%s\n' "$TS_JSON" | grep -q '"BackendState": *"Running"'; then
        die "Tailscale is not running or you are not signed in. Open Tailscale from the menu bar at the top of your screen, sign in, then click SCAT Chat again."
    fi
    MACHINE=$(printf '%s\n' "$TS_JSON" | json_first HostName)
    NODE_ID=$(printf '%s\n' "$TS_JSON" | json_first ID)
    if ! https_on "$TS_JSON"; then
        ans=$(ui_choice OPEN "Tailscale needs HTTPS switched on, once, before the public link can work.

First look at the name: Tailscale calls this Mac \"$MACHINE\". Switching HTTPS on puts that name in a public record that can never be erased. If it has your name or anything private in it, rename the Mac first in Tailscale (Machines, then Edit machine name), and only then switch HTTPS on.

SCAT Chat never switches HTTPS on for you. When the name is right, click 'Open the page', switch on Enable HTTPS, then click SCAT Chat again." "Open the page" "Close")
        if [ "$ans" = "Open the page" ]; then
            "$OPEN" "$DNS_PAGE" >/dev/null 2>&1
        fi
        die "Nothing was started: HTTPS is not switched on in Tailscale yet (the page is $DNS_PAGE)."
    fi
}

step_vault() {
    VAULT=${SCAT_CHAT_VAULT:-}
    if [ -z "$VAULT" ] && [ -f "$STATE/vault" ]; then
        VAULT=$(cat "$STATE/vault")
    fi
    if [ -n "$VAULT" ] && [ ! -d "$VAULT" ]; then
        ui_note "The vault folder I remembered is gone ($VAULT). Choose it again on the next screen."
        VAULT=""
    fi
    if [ -z "$VAULT" ]; then
        VAULT=$(ui_folder VAULT "Choose your vault: the folder that holds your narratives (it has a file called scat.toml).")
        [ -n "$VAULT" ] || die "No vault was chosen, so nothing was started. Click SCAT Chat again and choose your vault folder."
    fi
    VAULT=$(cd "$VAULT" 2>/dev/null && pwd -P) || die "I cannot open that folder. Click SCAT Chat again and choose your vault folder."

    if in_private "$VAULT"; then
        COPY_TO=$HOME_REAL/SCAT/vault
        if [ -e "$COPY_TO" ]; then
            die "Your vault is in a folder that macOS protects, so the server cannot read it, and ~/SCAT/vault already exists, so I will not copy over it. Click SCAT Chat again and choose ~/SCAT/vault, or a folder outside Documents, Desktop, Downloads and iCloud."
        fi
        ans=$(ui_choice COPY "Your vault is in $VAULT, a folder that macOS keeps private from the server's container, so the server cannot read it there.

I can make a copy in ~/SCAT/vault and use the copy. Your original stays where it is; I never move it. Edits you make in the copy have to be brought back to your original through git: commit and push from the copy, then pull in the original.

Make the copy now?" "Copy" "Cancel")
        [ "$ans" = "Copy" ] || [ "$ans" = "copy" ] || die "Nothing was copied or started. Move your vault outside Documents, Desktop, Downloads and iCloud, or click SCAT Chat again and say Copy."
        if ! { mkdir -p "$COPY_TO" && cp -R "$VAULT/." "$COPY_TO/"; }; then
            rm -rf "$COPY_TO"
            die "The copy failed, so nothing was started. If macOS asked whether SCAT Chat may use your Documents folder, click Allow; then click SCAT Chat again."
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
    [ -f "$CTX/deploy/Dockerfile" ] || die "The server's recipe is missing from this copy of SCAT Chat. Download the app again."
    ui_progress "Building the server, once. The first time takes a few minutes."
    if ! "$DOCKER" build -f "$CTX/deploy/Dockerfile" -t "$TAG" "$CTX" >"$STATE/build.log" 2>&1; then
        die "Building the server failed. The last lines say: $(tail -n 5 "$STATE/build.log" | tr '\n' ' ')
Check that you are online, then click SCAT Chat again."
    fi
}

step_server() {
    if ! { key_put "$(new_key)" && key_present; }; then
        die "I could not keep a new key in your keychain. If macOS asked for permission, click Allow; then click SCAT Chat again."
    fi
    "$DOCKER" rm -f "$CONTAINER" >/dev/null 2>&1
    printf 'SCAT_MCP_KEY=%s\n' "$(key_get)" |
        "$DOCKER" run -d --name "$CONTAINER" --read-only --tmpfs /tmp --user "$HOST_UID:$HOST_GID" \
        --security-opt no-new-privileges --cap-drop ALL \
        -p "127.0.0.1:$PORT:8765" -v "$VAULT:/vault" --env-file /dev/stdin "$TAG" >/dev/null 2>"$STATE/run.log" ||
        die "The server would not start: $(tail -n 3 "$STATE/run.log" | tr '\n' ' ')
Make sure no other SCAT Chat is open and port $PORT is free, then click SCAT Chat again."

    ui_progress "Waiting for the server to answer."
    i=0
    code=""
    while [ "$i" -lt $((WAIT * 5)) ]; do
        code=$(http_code 0)
        [ "$code" = 401 ] && break
        if ! container_running; then
            die "The server stopped right after starting. Its last words: $("$DOCKER" logs --tail 5 "$CONTAINER" 2>&1 | tr '\n' ' ')
Click SCAT Chat again; if it repeats, tell the person who set this up."
        fi
        i=$((i + 1))
        sleep 0.2
    done
    [ "$code" = 401 ] || die "The server did not answer within $WAIT seconds. Click SCAT Chat again; if it repeats, tell the person who set this up."
    [ "$(http_code 1)" = 200 ] || die "The server answers but does not accept its own key. Click SCAT Chat again; if it repeats, tell the person who set this up."
}

step_tunnel() {
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
        ans=$(ui_choice OPEN "The public link did not start. The usual reason is that Funnel is not allowed on your Tailscale account yet. That takes one click, once: click 'Open the page', approve Funnel there, then click SCAT Chat again." "Open the page" "Close")
        if [ "$ans" = "Open the page" ]; then
            "$OPEN" "$page" >/dev/null 2>&1
        fi
        die "The public link did not start (Funnel is probably not allowed yet: $page)."
    fi
    URL=$PUBLIC/mcp
}

step_awake() {
    "$CAFFEINATE" -i -s </dev/null >/dev/null 2>&1 &
    printf '%s\n' "$!" >"$STATE/caffeinate.pid"
}

cmd_start() {
    mkdir -p "$STATE" && chmod 700 "$STATE" || exit 1
    if [ -f "$STATE/session" ]; then
        old=$(cat "$STATE/session")
        if [ "$UI" = dialog ] && ! kill -0 "$old" 2>/dev/null; then
            teardown # a crashed earlier session: clean up, then go on
        else
            ui_note "SCAT Chat is already running. Click Stop in its window (or quit the app) before starting it again."
            exit 0
        fi
    fi
    printf '%s\n' "$$" >"$STATE/session"
    CLEANUP=1
    trap on_exit EXIT
    trap 'SIGNALED=1; exit 1' INT TERM HUP

    HOME_REAL=$(cd "$HOME" && pwd -P)
    HOST_UID=$(id -u)
    HOST_GID=$(id -g)

    step_tools
    step_vault
    step_image
    step_server
    step_tunnel
    step_awake

    printf '%s\n' "$URL" >"$STATE/session.txt"
    ui_hold "SCAT Chat is running.

1. In the chat, open MCP settings and add a server.
2. Paste this address:
$URL
3. Choose API key as the authentication. Click Copy key below, then paste the key in the chat. The key is never shown on screen.

Vault: $VAULT
Your Mac stays awake while this window is open. Click Stop when you are done: that switches everything off and deletes the key."
}

# ---------------------------------------------------------------- stop, status

cmd_stop() {
    mkdir -p "$STATE" || exit 1
    HOME_REAL=$(cd "$HOME" && pwd -P)
    if [ -f "$STATE/session" ]; then
        sp=$(cat "$STATE/session")
        if [ -n "$sp" ] && [ "$sp" != "$$" ] && kill -0 "$sp" 2>/dev/null && ps -p "$sp" -o command= 2>/dev/null | grep -q 'scat-chat'; then
            kill "$sp" 2>/dev/null
            wait_dead "$sp"
        fi
    fi
    teardown
    printf '%s\n' "$RESULT"
    case "$RESULT" in "Stopped, but"*) exit 1 ;; esac
}

cmd_status() {
    if [ -f "$STATE/session" ]; then
        if [ -f "$STATE/session.txt" ]; then
            printf 'SCAT Chat is running at %s\n' "$(cat "$STATE/session.txt")"
        else
            printf 'SCAT Chat is starting.\n'
        fi
        exit 0
    fi
    printf 'SCAT Chat is not running.\n'
    exit 1
}

cmd_change_vault() {
    rm -f "$STATE/vault"
    printf 'The next start will ask you to choose the vault folder again.\n'
}

case "${1:-}" in
start) cmd_start ;;
stop) cmd_stop ;;
status) cmd_status ;;
change-vault) cmd_change_vault ;;
*)
    printf 'usage: %s start | stop | status | change-vault\n' "$0" >&2
    exit 2
    ;;
esac
