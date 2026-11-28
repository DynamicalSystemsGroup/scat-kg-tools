# Retire an installed copy of the app's earlier name, once per Mac. POSIX sh; scatlab.sh sources this file and calls
# retire_old after its tools check. Delete this file, its call in scatlab.sh, its line in build-app.sh and
# tests/deploy/test_retire_old.py when nobody runs the earlier name any more.
#
# It leaves one app, one keychain item and one image: the earlier app, its keychain item, its container, its images and
# its state folder are removed. The remembered vault moves over, so the first start of the new app asks nothing new.
# Every step is safe when its target is not there. Nothing here prints or asks: an upgrade shows only the new name.
#
# This is the one place outside the history paths that names the earlier app, repositories and package (WP37-R1).
# From scatlab.sh it uses: STATE, DOCKER, TAILSCALE, SECURITY, CAFFEINATE, have.
# Settings for tests: SCATLAB_OLD_HOME (the earlier state folder), SCATLAB_OLD_APP (the earlier app's path).

OLD_STATE=${SCATLAB_OLD_HOME:-$HOME/Library/Application Support/SCAT Chat}
OLD_APP=${SCATLAB_OLD_APP:-/Applications/SCAT Chat.app}
OLD_KEY=scat-chat # the keychain item: service and account
OLD_CONTAINER=scat-chat
OLD_IMAGE=scat-chat-mcp
OLD_REGISTRY_IMAGE=ghcr.io/dynamicalsystemsgroup/scat-kg-tools

retire_old() {
    [ ! -f "$STATE/retired-old" ] || return 0

    # An earlier session still running: stop it the way it stops itself (its launcher tears down on TERM), then
    # the earlier app, which would otherwise find its launcher gone and quit by itself.
    if [ -f "$OLD_STATE/session" ]; then
        ro_pid=$(cat "$OLD_STATE/session" 2>/dev/null)
        if [ -n "$ro_pid" ] && kill -0 "$ro_pid" 2>/dev/null &&
            ps -p "$ro_pid" -o command= 2>/dev/null | grep -q 'scat-chat'; then
            kill "$ro_pid" 2>/dev/null
            wait_dead "$ro_pid" || kill -9 "$ro_pid" 2>/dev/null
        fi
    fi
    if have pkill; then
        pkill -f "$OLD_APP/Contents/MacOS/applet" 2>/dev/null || true
        ro_i=0 # its quit runs its own stop, which writes to its state folder: let it finish before that folder goes
        while have pgrep && pgrep -f "$OLD_APP/Contents/MacOS/applet" >/dev/null 2>&1 && [ "$ro_i" -lt 30 ]; do
            sleep 0.1
            ro_i=$((ro_i + 1))
        done
    fi

    # What a crashed earlier session may have left (the teardown above covers a live one): the public link, the
    # awake-lock, the server container, the key.
    if [ -f "$OLD_STATE/tunnel" ] && have "$TAILSCALE"; then
        "$TAILSCALE" funnel --https=443 off >/dev/null 2>&1 || true
    fi
    if [ -f "$OLD_STATE/caffeinate.pid" ]; then
        ro_cp=$(cat "$OLD_STATE/caffeinate.pid" 2>/dev/null)
        if [ -n "$ro_cp" ] && ps -p "$ro_cp" -o command= 2>/dev/null | grep -q "$(basename "$CAFFEINATE")"; then
            kill "$ro_cp" 2>/dev/null || true
        fi
    fi
    if have "$DOCKER" && "$DOCKER" info >/dev/null 2>&1; then
        if [ -n "$("$DOCKER" ps -a -q --filter "name=^${OLD_CONTAINER}\$" 2>/dev/null)" ]; then
            "$DOCKER" rm -f "$OLD_CONTAINER" >/dev/null 2>&1 || true
        fi
        for ro_img in $("$DOCKER" images --format '{{.Repository}}:{{.Tag}}' 2>/dev/null); do
            case "$ro_img" in
            "$OLD_IMAGE":* | "$OLD_REGISTRY_IMAGE":*) "$DOCKER" rmi -f "$ro_img" >/dev/null 2>&1 || true ;;
            esac
        done
    fi
    if "$SECURITY" find-generic-password -s "$OLD_KEY" -a "$OLD_KEY" >/dev/null 2>&1; then
        "$SECURITY" delete-generic-password -s "$OLD_KEY" -a "$OLD_KEY" >/dev/null 2>&1 || true
    fi

    # The remembered vault and the one-time note move over; the rest of the earlier state folder goes.
    for ro_f in vault menubar-note; do
        if [ -f "$OLD_STATE/$ro_f" ] && [ ! -f "$STATE/$ro_f" ]; then
            cp "$OLD_STATE/$ro_f" "$STATE/$ro_f"
        fi
    done
    rm -rf "$OLD_STATE"
    rm -rf "$OLD_APP"
    : >"$STATE/retired-old"
}
