"""WP37-R2, G2: started over an installed copy of the app's earlier name, SCATLAB leaves one app, one keychain item and
one image, and keeps the remembered vault. deploy/retire-old.sh is the one file that names the earlier app (R1), so this
test names it too. The earlier app, state folder and keychain item are scratch ones: never this Mac's."""

import subprocess
import time

import pytest
from conftest import STANDINS

OLD_REGISTRY = "ghcr.io/dynamicalsystemsgroup/scat-kg-tools"

# The base docker stand-in does not know the earlier names: this one answers for them (a file for the earlier
# container, a list of images) and hands everything else to the base.
OLD_DOCKER = r"""#!/bin/sh
S="$STUB_STATE"
case "$1" in
ps) case "$*" in *"name=^scat-chat"*) echo "docker $*" >> "$CALLS"; [ -f "$S/old-container" ] && echo old123; exit 0 ;; esac ;;
rm) case "$*" in *scat-chat*) echo "docker $*" >> "$CALLS"; rm -f "$S/old-container"; exit 0 ;; esac ;;
images) echo "docker $*" >> "$CALLS"; cat "$S/images" 2>/dev/null; exit 0 ;;
rmi) echo "docker $*" >> "$CALLS"; grep -vxF "$3" "$S/images" > "$S/images.new"; mv "$S/images.new" "$S/images"; exit 0 ;;
esac
exec "$(dirname "$0")/docker-base" "$@"
"""


@pytest.fixture
def old(rig):
    """A Mac with the earlier app installed and a session crashed: its app, state folder, key, container, images."""
    docker = rig.bin / "docker"
    (rig.bin / "docker-base").write_text(STANDINS["docker"])
    (rig.bin / "docker-base").chmod(0o755)
    docker.write_text(OLD_DOCKER)
    docker.chmod(0o755)
    app = rig.tmp / "earlier-apps" / "app"
    (app / "Contents" / "MacOS").mkdir(parents=True)
    (app / "Contents" / "MacOS" / "applet").write_text("x")
    home = rig.tmp / "earlier-home"
    home.mkdir()
    (home / "vault").write_text(f"{rig.vault.resolve()}\n")
    (home / "menubar-note").touch()
    (home / "ui").write_text("running\n")
    (home / "tunnel").touch()
    (home / "caffeinate.pid").write_text("999999\n")
    (rig.state / "vault").unlink(
        missing_ok=True
    )  # so the move of the remembered vault is what puts it there
    (rig.stub / "keychain").mkdir(exist_ok=True)
    (rig.stub / "keychain" / "scat-chat").write_text("oldkey")
    (rig.stub / "old-container").touch()
    (rig.stub / "images").write_text(f"scat-chat-mcp:abc123\n{OLD_REGISTRY}:0.1.0\nredis:7\n")
    rig.old_app, rig.old_home = app, home
    return rig


def test_the_earlier_install_is_replaced(old):
    r = old.run("start", SCATLAB_A_STOP="stop")
    assert r.returncode == 0, r.stdout + r.stderr
    assert not old.old_app.exists()  # one app
    assert not old.old_home.exists()
    assert not (old.stub / "old-container").exists()
    assert not (
        old.stub / "keychain" / "scat-chat"
    ).exists()  # one keychain item (the session's own is gone at Stop)
    assert (old.stub / "images").read_text().split() == [
        "redis:7"
    ]  # the earlier images go, other images stay
    assert (old.state / "vault").read_text().strip() == str(
        old.vault.resolve()
    )  # the remembered vault moved over
    assert (old.state / "menubar-note").exists()
    assert old.called(
        "tailscale funnel --https=443 off"
    )  # a crashed session's public link is switched off
    old.nothing_left()


def test_the_new_session_keeps_exactly_one_keychain_item_while_it_runs(old):
    r = old.run("start")
    assert r.returncode == 0, r.stdout + r.stderr
    assert sorted(p.name for p in (old.stub / "keychain").iterdir()) == ["scatlab"]
    old.run("stop")
    old.nothing_left()


def test_it_is_said_nowhere(old):
    r = old.run("start", SCATLAB_A_STOP="stop")
    assert (
        "SCAT Chat" not in r.stdout and "scat-chat" not in r.stdout
    )  # an upgrade shows only the new name


def test_it_runs_once_per_mac(old):
    old.run("start", SCATLAB_A_STOP="stop")
    (old.stub / "keychain").mkdir(exist_ok=True)
    (old.stub / "keychain" / "scat-chat").write_text("later")
    old.run("start", SCATLAB_A_STOP="stop")
    assert (
        old.stub / "keychain" / "scat-chat"
    ).exists()  # the marker in the state folder ends the retiring


def test_a_clean_mac_is_left_alone(rig):
    r = rig.run("start", SCATLAB_A_STOP="stop")
    assert r.returncode == 0, r.stdout + r.stderr
    assert not rig.called("docker rmi")
    assert not [
        c for c in rig.calls_list() if c.startswith("security delete-generic-password -s scat-chat")
    ]
    assert (rig.state / "retired-old").exists()


def test_a_session_of_the_earlier_app_still_running_is_stopped_by_its_own_teardown(old):
    marker = old.tmp / "torn-down"
    script = old.tmp / "scat-chat.sh"
    script.write_text(
        f"#!/bin/sh\ntrap 'echo done > {marker}; exit 0' TERM\nwhile :; do sleep 0.1; done\n"
    )
    proc = subprocess.Popen(["/bin/sh", str(script)])
    try:
        time.sleep(0.5)
        (old.old_home / "session").write_text(f"{proc.pid}\n")
        r = old.run("start", SCATLAB_A_STOP="stop")
        assert r.returncode == 0, r.stdout + r.stderr
        assert marker.read_text().strip() == "done"
        assert proc.wait(timeout=10) == 0
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()
