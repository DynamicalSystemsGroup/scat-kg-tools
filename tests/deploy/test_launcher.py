"""deploy/scat-chat.sh driven in plain mode with stand-ins for every outside program (WP18-R2)."""

import os
import shutil
import subprocess

import pytest
from conftest import REPO, STATUS_NO_HTTPS, STATUS_STOPPED

STOP = {"SCAT_CHAT_A_STOP": "stop"}


def test_start_order_flags_and_stop_button(rig):
    r = rig.run("start", **STOP)
    assert r.returncode == 0, r.stdout + r.stderr
    calls = rig.calls_list()
    order = [
        rig.called("colima status")[0],
        rig.called("colima start")[0],
        rig.called("docker build")[0],
        rig.called("docker run")[0],
        rig.called("tailscale funnel --bg")[0],
        rig.called("tailscale funnel --https=443 off")[0],
        rig.called("docker rm -f scat-chat")[-1],
    ]
    assert order == sorted(order) and len(set(order)) == len(order), calls
    run = calls[rig.called("docker run")[0]]
    for flag in [
        "--read-only", "--tmpfs /tmp", "--security-opt no-new-privileges", "--cap-drop ALL",
        f"-p 127.0.0.1:{rig.server.port}:8765", f"-v {rig.vault.resolve()}:/vault", "--env-file /dev/stdin",
    ]:  # fmt: skip
        assert flag in run, (flag, run)
    assert "UID" not in calls[rig.called("docker build")[0]]  # no host uid baked into the image
    assert f"--user {os.getuid()}:{os.getgid()}" in run  # the user is set at run time
    assert "Stopped." in r.stdout
    rig.nothing_left()


def test_key_is_kept_in_the_keychain_and_not_shown_or_copied(rig):
    r = rig.run("start")  # stays up
    assert r.returncode == 0, r.stdout + r.stderr
    key = rig.key()
    assert len(key) == 64 and rig.keys_seen() == [key]
    assert key not in r.stdout  # the dialog never shows it
    assert rig.clip() == ""  # and it is on the clipboard only on request
    assert "https://fake-mac.tail1234.ts.net/mcp" in r.stdout
    assert "Paste this address" in r.stdout and "Copy key" in r.stdout
    assert rig.run("status").returncode == 0
    rig.run("stop")
    rig.nothing_left()


def test_keychain_calls_go_through_security_with_the_item_on_stdin(rig):
    rig.run("start", **STOP)
    calls = rig.calls_list()
    assert "security -i" in calls  # the item is written by a command on stdin
    assert "security(stdin) add-generic-password -s scat-chat" in calls
    assert any(
        c.startswith("security find-generic-password -s scat-chat") and c.endswith(" -w")
        for c in calls
    )
    assert any(c.startswith("security delete-generic-password -s scat-chat") for c in calls)
    for c in calls:
        if c.startswith("security") and "add-generic-password" in c:
            assert " -w " not in c + " " or c.startswith("security(stdin)"), c


def test_key_reaches_the_container_on_stdin_only(rig):
    rig.run("start", **STOP)
    (key,) = rig.keys_seen()
    assert (rig.stub / "env-in").read_text() == f"SCAT_MCP_KEY={key}\n"
    assert "--env-file /dev/stdin" in rig.calls_list()[rig.called("docker run")[0]]


def all_files_text(folder):
    return b"".join(p.read_bytes() for p in folder.rglob("*") if p.is_file())


def test_key_is_in_no_argument_of_any_program_and_in_no_file_of_the_state_folder(rig):
    # dialog mode, so the osascript stand-in sees what the real dialog would be given; the coder copies the key, then stops
    (rig.stub / "osa-answers").write_text("Copy key\nStop\n")
    r = rig.run("start", SCAT_CHAT_UI="dialog")
    assert r.returncode == 0, r.stdout
    (key,) = rig.keys_seen()
    calls = rig.calls_list()
    for program in ["docker", "osascript", "security", "tailscale", "colima", "curl"]:
        assert any(c.startswith(program) for c in calls), program
    assert not [c for c in calls if key in c], "the key is on a command line"
    assert rig.clip() == ""  # Copy key put it there on stdin; Stop cleared it
    assert key.encode() not in all_files_text(rig.state)
    assert key not in r.stdout


def test_copy_key_puts_the_key_on_the_clipboard_only_when_the_coder_asks(rig):
    rig.run("start", **STOP)
    assert rig.clip() == ""  # started and stopped without asking: never copied
    r = rig.run(
        "start", SCAT_CHAT_A_COPYKEY="copy"
    )  # the coder clicks Copy key, then leaves the session up
    assert r.returncode == 0, r.stdout
    assert rig.clip() == rig.key()
    assert rig.key() not in r.stdout
    assert not [c for c in rig.calls_list() if rig.key() in c]
    rig.run("stop")


def test_the_dialog_copy_key_button_copies_and_asks_again_until_stop(rig):
    (rig.stub / "osa-answers").write_text("Copy key\nCopy key\nStop\n")
    r = rig.run("start", SCAT_CHAT_UI="dialog")
    assert r.returncode == 0, r.stdout
    assert len([c for c in rig.calls_list() if 'buttons {"Copy key", "Stop"}' in c]) == 3
    assert not rig.item()
    rig.nothing_left()
    # the dialog without a Copy key answer leaves the clipboard empty
    r = rig.run("start", SCAT_CHAT_UI="dialog")
    assert rig.clip() == ""


def test_stop_deletes_the_key_clears_the_clipboard_and_is_idempotent(rig):
    rig.run("start", SCAT_CHAT_A_COPYKEY="copy")
    assert rig.item() and rig.clip() == rig.key()
    r = rig.run("stop")
    assert r.returncode == 0 and "Stopped." in r.stdout, r.stdout
    assert "the key was deleted" in r.stdout and "replaced" not in r.stdout
    assert not rig.item()
    assert rig.clip() == ""
    rig.nothing_left()
    assert rig.called("tailscale funnel --https=443 off")
    assert rig.called("security delete-generic-password")
    r2 = rig.run("stop")  # twice
    assert r2.returncode == 0 and "Stopped." in r2.stdout
    assert not rig.item()


def test_a_dry_run_stop_leaves_no_keychain_item(rig):
    r = rig.run("start", **STOP)  # plain mode, stand-ins: a dry run
    assert r.returncode == 0 and "Stopped." in r.stdout
    assert rig.keys_seen() and not rig.item()
    rig.nothing_left()


def test_a_key_that_cannot_be_kept_stops_the_start(rig):
    r = rig.run("start", STUB_FAIL_KEYCHAIN="1")
    assert r.returncode == 1 and "keychain" in r.stdout
    assert not rig.called("docker run")


def test_stop_when_nothing_ever_ran(rig):
    r = rig.run("stop")
    assert r.returncode == 0 and "Stopped." in r.stdout
    assert not rig.item()
    assert not rig.called("tailscale funnel")  # never touches a tunnel it did not start


def test_clipboard_not_cleared_when_it_holds_something_else(rig):
    rig.run("start", SCAT_CHAT_A_COPYKEY="copy")
    (rig.stub / "clip").write_text("my own text")
    rig.run("stop")
    assert rig.clip() == "my own text"


def test_second_start_while_running_is_refused_politely(rig):
    rig.run("start")
    r = rig.run("start")
    assert r.returncode == 0 and "already running" in r.stdout
    assert len(rig.called("docker run")) == 1
    rig.run("stop")


def test_vault_in_documents_refused_then_copied_on_ok(rig):
    docs = rig.home / "Documents" / "myvault"
    docs.mkdir(parents=True)
    (docs / "n.md").write_text("hello")
    env = {"SCAT_CHAT_VAULT": str(docs)}
    r = rig.run("start", SCAT_CHAT_A_COPY="Cancel", **env)
    assert r.returncode == 1
    assert "~/SCAT/vault" in r.stdout and "git" in r.stdout and "never move" in r.stdout
    assert not (rig.home / "SCAT").exists()
    assert not rig.called("docker run")
    rig.nothing_left()

    r = rig.run("start", SCAT_CHAT_A_COPY="Copy", **env, **STOP)
    assert r.returncode == 0, r.stdout
    copy = rig.home / "SCAT" / "vault"
    assert (copy / "n.md").read_text() == "hello"
    assert (docs / "n.md").exists()  # copied, never moved
    assert (rig.state / "vault").read_text().strip() == str(copy.resolve())
    run = rig.calls_list()[rig.called("docker run")[0]]
    assert f"-v {copy.resolve()}:/vault" in run and "Documents" not in run


@pytest.mark.parametrize(
    "folder", ["Desktop", "Downloads", "Library/Mobile Documents/com~apple~CloudDocs"]
)
def test_other_private_folders_refused(rig, folder):
    v = rig.home / folder / "v"
    v.mkdir(parents=True)
    r = rig.run("start", SCAT_CHAT_VAULT=str(v), SCAT_CHAT_A_COPY="Cancel")
    assert r.returncode == 1 and not rig.called("docker run")


def test_copy_never_overwrites_existing_copy(rig):
    docs = rig.home / "Documents" / "v"
    docs.mkdir(parents=True)
    (rig.home / "SCAT" / "vault").mkdir(parents=True)
    (rig.home / "SCAT" / "vault" / "keep.md").write_text("mine")
    r = rig.run("start", SCAT_CHAT_VAULT=str(docs), SCAT_CHAT_A_COPY="Copy")
    assert r.returncode == 1 and "already exists" in r.stdout
    assert (rig.home / "SCAT" / "vault" / "keep.md").read_text() == "mine"


def test_first_run_asks_for_the_vault_and_remembers_it(rig):
    r = rig.run("start", SCAT_CHAT_VAULT=None, SCAT_CHAT_A_VAULT=str(rig.vault), **STOP)
    assert r.returncode == 0, r.stdout
    assert (rig.state / "vault").read_text().strip() == str(rig.vault.resolve())
    # second run: no answer given, none needed
    r = rig.run("start", SCAT_CHAT_VAULT=None, **STOP)
    assert r.returncode == 0, r.stdout
    rig.run("change-vault")
    assert not (rig.state / "vault").exists()
    r = rig.run("start", SCAT_CHAT_VAULT=None)  # asks again; no answer: nothing starts
    assert r.returncode == 1 and "No vault was chosen" in r.stdout


def test_colima_not_started_when_already_running_and_image_built_once(rig):
    (rig.stub / "colima-up").touch()
    rig.run("start", **STOP)
    assert not rig.called("colima start")
    assert len(rig.called("docker build")) == 1
    (rig.stub / "image").touch()  # image present for the same source
    n = len(rig.called("docker build"))
    rig.run("start", **STOP)
    assert len(rig.called("docker build")) == n  # the image is there: not built again


PUBLISHED = "ghcr.io/dynamicalsystemsgroup/scat-kg-tools:"


def package_version():
    return next(
        line.split('"')[1] for line in (REPO / "pyproject.toml").read_text().splitlines()
        if line.startswith("version")
    )  # fmt: skip


def test_published_image_is_pulled_and_not_built(rig):
    r = rig.run("start", STUB_PUBLISHED="1", **STOP)
    assert r.returncode == 0, r.stdout
    ref = PUBLISHED + package_version()
    assert rig.called(f"docker pull {ref}")
    assert not rig.called("docker build")
    assert rig.calls_list()[rig.called("docker run")[0]].endswith(f" {ref}")


def test_no_published_image_builds_the_source_locally(rig):
    r = rig.run("start", **STOP)
    assert r.returncode == 0, r.stdout
    assert rig.called(f"docker pull {PUBLISHED}{package_version()}")  # tried first
    assert len(rig.called("docker build")) == 1
    assert rig.called("docker pull")[0] < rig.called("docker build")[0]
    assert rig.calls_list()[rig.called("docker run")[0]].endswith(
        " scat-chat-mcp:"
        + rig.calls_list()[rig.called("docker build")[0]].split("-t scat-chat-mcp:")[1].split()[0]
    )


def test_missing_docker(rig):
    r = rig.run("start", SCAT_CHAT_DOCKER=str(rig.bin / "nope"))
    assert r.returncode == 1
    assert "needs Docker Desktop" in r.stdout and "click SCAT Chat again" in r.stdout
    assert not rig.called("tailscale")


def test_docker_is_found_in_docker_desktops_own_folder(rig, tmp_path):
    folder = tmp_path / "Docker.app" / "Contents" / "Resources" / "bin"
    folder.mkdir(parents=True)
    shutil.copy(rig.bin / "docker", folder / "docker")
    # no SCAT_CHAT_DOCKER: the launcher must find `docker` on its own, only in the folders it was told (not the real ones on this Mac)
    r = rig.run("start", SCAT_CHAT_DOCKER=None, SCAT_CHAT_SEARCH_PATH=str(folder), **STOP)
    assert "needs Docker Desktop" not in r.stdout
    assert rig.called("docker build") and rig.called("docker run")


def path_without_docker(folder):
    """A folder of links to every program in /usr/bin and /bin except docker, so a real docker cannot be found."""
    folder.mkdir()
    for src in ("/usr/bin", "/bin"):
        for name in os.listdir(src):
            p = os.path.join(src, name)
            if name != "docker" and os.access(p, os.X_OK) and not (folder / name).exists():
                (folder / name).symlink_to(p)
    return str(folder)


def test_docker_not_in_docker_desktops_folder_is_still_missing(rig, tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    r = rig.run(
        "start",
        SCAT_CHAT_DOCKER=None,
        SCAT_CHAT_SEARCH_PATH=str(empty),
        PATH=path_without_docker(tmp_path / "nodocker"),
    )
    assert r.returncode == 1 and "needs Docker Desktop" in r.stdout
    assert not rig.called("docker")


def test_docker_desktops_real_folder_is_the_default():
    text = (REPO / "deploy" / "scat-chat.sh").read_text()
    assert "/Applications/Docker.app/Contents/Resources/bin" in text
    assert (
        "/usr/local/bin:/opt/homebrew/bin:/Applications/Docker.app/Contents/Resources/bin" in text
    )


def test_missing_colima_and_no_docker_running(rig):
    r = rig.run("start", SCAT_CHAT_COLIMA=str(rig.bin / "nope"))
    assert r.returncode == 1 and "Docker Desktop is not running" in r.stdout


def test_stop_that_cannot_confirm_says_what_to_click(rig):
    rig.run("start")
    r = rig.run("stop", SCAT_CHAT_TAILSCALE=str(rig.bin / "nope"))
    assert "could not confirm" in r.stdout
    assert "click SCAT Chat again, then Stop, or restart your Mac" in r.stdout


def test_missing_tailscale(rig):
    r = rig.run("start", SCAT_CHAT_TAILSCALE=str(rig.bin / "nope"))
    assert r.returncode == 1 and "needs Tailscale" in r.stdout
    assert not rig.called("docker run")
    rig.nothing_left()


def test_tailscale_not_signed_in(rig):
    (rig.stub / "ts-status.json").write_text(STATUS_STOPPED)
    r = rig.run("start")
    assert r.returncode == 1 and "sign in" in r.stdout
    assert not rig.called("docker run")


def test_https_not_enabled_shows_the_name_and_never_enables_it(rig):
    (rig.stub / "ts-status.json").write_text(STATUS_NO_HTTPS)
    r = rig.run("start", SCAT_CHAT_A_OPEN="Open the page")
    assert r.returncode == 1
    assert (
        '"fake-mac"' in r.stdout
        and "public record" in r.stdout
        and "never switches HTTPS on" in r.stdout
    )
    assert any(c.startswith("open https://login.tailscale.com/admin/dns") for c in rig.calls_list())
    assert not rig.called("tailscale funnel") and not rig.called("docker run")
    rig.nothing_left()


def test_funnel_policy_missing_points_to_the_one_page_and_tears_down(rig):
    r = rig.run("start", STUB_FUNNEL_BLOCKED="1", SCAT_CHAT_A_OPEN="Open the page")
    assert r.returncode == 1
    assert "https://login.tailscale.com/f/funnel?node=nTEST123CNTRL" in r.stdout
    assert any(c.startswith("open https://login.tailscale.com/f/funnel") for c in rig.calls_list())
    assert "Stopped." in r.stdout
    rig.nothing_left()
    assert rig.called("docker rm -f scat-chat")[-1] > rig.called("docker run")[0]


def test_teardown_after_failed_container_start(rig):
    r = rig.run("start", STUB_FAIL_RUN="1")
    assert r.returncode == 1 and "would not start" in r.stdout and "Stopped." in r.stdout
    rig.nothing_left()
    assert not rig.called("tailscale funnel --bg")


def test_teardown_when_server_never_answers(rig):
    rig.server.close()
    r = rig.run("start", SCAT_CHAT_WAIT="2")
    assert r.returncode == 1 and "did not answer" in r.stdout
    rig.nothing_left()
    assert not rig.called("tailscale funnel --bg")
    assert rig.keys_seen() and not rig.item()  # the key made for the failed start was deleted


def test_failed_build_says_what_to_click(rig):
    r = rig.run("start", STUB_FAIL_BUILD="1")
    assert (
        r.returncode == 1
        and "Building the server failed" in r.stdout
        and "click SCAT Chat again" in r.stdout
    )
    assert not rig.called("docker run")


def test_every_stop_leaves_no_key_after_failed_start(rig):
    rig.run("start", STUB_FAIL_RUN="1")
    assert rig.keys_seen() == [f"{1:064d}"] and not rig.item()


def test_script_syntax():
    for f in ["scat-chat.sh", "build-app.sh"]:
        assert subprocess.run(["sh", "-n", str(REPO / "deploy" / f)], check=False).returncode == 0
    sc = shutil.which("shellcheck")
    if sc:
        assert (
            subprocess.run([sc, str(REPO / "deploy" / "scat-chat.sh")], check=False).returncode == 0
        )


def test_dockerfile_contract():
    d = (REPO / "deploy" / "Dockerfile").read_text()
    assert "UID" not in d and "useradd" not in d and "USER 65534:65534" in d and "[mcp]" in d
    assert '"scat-mcp", "--vault", "/vault", "--host", "0.0.0.0", "--port", "8765"' in d
    ig = (REPO / "deploy" / "Dockerfile.dockerignore").read_text().splitlines()
    assert ig[1] == "*" or "*" in ig  # allow-list: only what the Dockerfile copies


@pytest.mark.skipif(shutil.which("osacompile") is None, reason="osacompile is absent (not macOS)")
def test_applescript_compiles_and_app_builds(tmp_path):
    r = subprocess.run(
        ["sh", str(REPO / "deploy" / "build-app.sh"), str(tmp_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    app = tmp_path / "SCAT Chat.app"
    assert (app / "Contents" / "MacOS" / "applet").exists()
    res = app / "Contents" / "Resources"
    assert os.access(res / "scat-chat.sh", os.X_OK)
    assert (res / "context" / "deploy" / "Dockerfile").exists()
    assert (res / "context" / "src" / "scat_kg" / "mcp_server" / "server.py").exists()
    assert not list(res.rglob("__pycache__"))
