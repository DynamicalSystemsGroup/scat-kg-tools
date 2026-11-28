"""Tests for the defects the WP22 review found (D-130 follow-ups): the wording of the next step, stale markers, a
relaunch while a session runs, the test-only vault override, an unconfirmed Stop, and a reused process id.
Stand-ins only; nothing real runs."""

import re
import shutil
import subprocess
import sys

import pytest
from conftest import REPO, STATUS_NO_HTTPS, STATUS_OK

STOP = {"SCATLAB_A_STOP": "stop"}
ADDRESS = "https://fake-mac.tail1234.ts.net/mcp"
LAUNCHER = (REPO / "deploy" / "scatlab.sh").read_text()
APPLET = (REPO / "deploy" / "scatlab.applescript").read_text()
README = (REPO / "deploy" / "README.md").read_text()
MENU_STEP = "choose Stop in the SCATLAB menu, then open SCATLAB again"


def other_vault(rig, name="other"):
    v = rig.tmp / name
    v.mkdir()
    (v / "scat.toml").write_text("x = 1\n")
    return v


def dead_pid():
    p = subprocess.Popen(["true"])
    p.wait()
    return p.pid


class Unrelated:
    """A live process that is not a launcher (a reused process id), killed at the end of the test."""

    def __enter__(self):
        self.proc = subprocess.Popen(["sleep", "60"])
        return self.proc

    def __exit__(self, *exc):
        self.proc.kill()
        self.proc.wait()


# ---------------------------------------------------------------- (a) the next step is in the menu


@pytest.mark.parametrize("name", ["script", "applet", "readme"])
def test_nothing_tells_the_coder_to_click_scatlab(name):
    text = {"script": LAUNCHER, "applet": APPLET, "readme": README}[name]
    assert not re.search(r"click\s+SCATLAB\b(?!\s+(menu|in))", text, re.IGNORECASE)


def die_messages():
    return re.findall(r'\bdie "(.*?)"(?=\s*(?:\n|\|\||$))', LAUNCHER, re.DOTALL)


def test_every_die_message_says_to_open_scatlab_again_through_the_menu():
    messages = die_messages()
    assert len(messages) >= 12, len(messages)  # the pattern still finds them all
    # These two end a dialog that has just said it (checked in the next test); their alert line is short.
    # "The server's recipe is missing" says to download the app again: opening it again cannot help.
    dialog_first = (
        "Nothing was started: HTTPS",
        "The public link did not start",
        "The server's recipe is missing",
    )
    for m in messages:
        if m.startswith(dialog_first):
            continue
        assert re.search(r"[Cc]hoose Stop in the SCATLAB menu, then open SCATLAB again", m), m


def test_the_two_dialog_first_failures_say_it_in_the_dialog(rig):
    (rig.stub / "ts-status.json").write_text(STATUS_NO_HTTPS)
    assert MENU_STEP in rig.run("start").stdout
    (rig.stub / "ts-status.json").write_text(STATUS_OK)
    assert MENU_STEP in rig.run("start", STUB_FUNNEL_BLOCKED="1").stdout


@pytest.mark.parametrize(
    "scenario",
    [
        {"SCATLAB_DOCKER": "nope"},
        {"SCATLAB_TAILSCALE": "nope"},
        {"STUB_FAIL_BUILD": "1"},
        {"STUB_FAIL_RUN": "1"},
        {"STUB_FAIL_KEYCHAIN": "1"},
        {"SCATLAB_VAULT": None},
    ],
    ids=["no-docker", "no-tailscale", "build-fails", "run-fails", "no-key", "no-vault"],
)
def test_a_failed_start_says_to_open_scatlab_again_through_the_menu(rig, scenario):
    env = {k: (str(rig.bin / v) if k.startswith("SCATLAB_D") or k == "SCATLAB_TAILSCALE" else v)
           for k, v in scenario.items()}  # fmt: skip
    r = rig.run("start", **env)
    assert r.returncode == 1, r.stdout
    assert re.search(r"[Cc]hoose Stop in the SCATLAB menu, then open SCATLAB again", r.stdout)


# ---------------------------------------------------------------- (b) a stale `changing`


def test_status_clears_a_stale_changing_marker_and_does_not_say_starting(rig):
    (rig.state / "changing").write_text(f"{dead_pid()}\n")
    for ui in ("dialog", "plain"):
        (rig.state / "changing").write_text(f"{dead_pid()}\n")
        r = rig.run("status", SCATLAB_UI=ui)
        assert r.returncode == 1 and "not running" in r.stdout, (ui, r.stdout)
        assert "starting" not in r.stdout
        assert not (rig.state / "changing").exists()


def test_a_live_changing_marker_is_still_between_two_sessions(rig):
    with Unrelated() as p:
        (rig.state / "changing").write_text(f"{p.pid}\n")
        r = rig.run("status")
        assert r.returncode == 0 and "starting" in r.stdout


def test_a_new_start_clears_a_stale_changing_marker(rig):
    (rig.state / "changing").write_text(f"{dead_pid()}\n")
    assert rig.run("start", **STOP).returncode == 0
    assert not (rig.state / "changing").exists()
    assert "starting" not in rig.run("status").stdout


# ---------------------------------------------------------------- (c) a relaunch while a session runs


def test_relaunching_while_running_shows_the_live_session_after_the_ui_file_is_deleted(rig):
    proc = rig.start_bg()
    assert rig.ui_lines() == ["running", str(rig.vault.resolve()), ADDRESS]
    (rig.state / "ui").unlink()  # what the app does when it starts
    r = rig.run("start", SCATLAB_UI="dialog")
    assert r.returncode == 0, r.stdout
    assert rig.ui_lines() == ["running", str(rig.vault.resolve()), ADDRESS]
    assert any("already running" in c for c in rig.calls_list() if c.startswith("osascript"))
    assert len(rig.called("docker run")) == 1  # nothing else was started
    assert rig.stop_bg(proc).returncode == 0
    rig.nothing_left()


# ---------------------------------------------------------------- (d) SCATLAB_VAULT is a plain-mode override


def test_scatlab_vault_is_ignored_in_dialog_mode(rig):
    wrong = other_vault(rig, "wrong")
    proc = rig.start_bg(
        remembered=False, SCATLAB_VAULT=str(wrong), STUB_OSA_FOLDER=str(rig.vault)
    )  # the folder chooser answers with the rig's vault
    run = rig.calls_list()[rig.called("docker run")[0]]
    assert f"-v {rig.vault.resolve()}:/vault" in run and str(wrong.resolve()) not in run
    assert any("choose folder" in c for c in rig.calls_list() if c.startswith("osascript"))
    assert rig.stop_bg(proc).returncode == 0


def test_scatlab_vault_does_not_replace_the_remembered_question_in_dialog_mode(rig):
    wrong = other_vault(rig, "wrong")
    proc = rig.start_bg(
        SCATLAB_VAULT=str(wrong)
    )  # remembered: the rig's vault; the stand-in says "Use it"
    assert any(f"Serve {rig.vault.resolve()}?" in c for c in rig.calls_list())
    run = rig.calls_list()[rig.called("docker run")[0]]
    assert f"-v {rig.vault.resolve()}:/vault" in run and str(wrong.resolve()) not in run
    assert rig.stop_bg(proc).returncode == 0


def test_scatlab_vault_is_honoured_in_plain_mode_without_the_question(rig):
    chosen = other_vault(rig, "chosen")
    (rig.state / "vault").write_text(f"{rig.vault.resolve()}\n")  # a different remembered vault
    r = rig.run("start", SCATLAB_VAULT=str(chosen), **STOP)
    assert r.returncode == 0, r.stdout
    assert "Serve " not in r.stdout
    assert f"-v {chosen.resolve()}:/vault" in rig.calls_list()[rig.called("docker run")[0]]


# ---------------------------------------------------------------- (e) an unconfirmed Stop is a problem, and Stop can be retried


def test_an_unconfirmed_stop_writes_problem_and_a_retry_writes_stopped(rig):
    rig.run("start")
    r = rig.run("stop", STUB_FUNNEL_STUCK="1")
    assert r.returncode == 1 and "could not confirm" in r.stdout, r.stdout
    lines = rig.ui_lines()
    assert lines[0] == "problem" and len(lines) == 4, lines
    assert "could not confirm" in lines[3] and "public link may still be on" in lines[3]
    assert not rig.item()  # the key is gone even though the link could not be confirmed off
    r = rig.run("stop")  # the retry, the link now answers
    assert r.returncode == 0 and "Stopped." in r.stdout, r.stdout
    assert rig.ui_lines() == ["stopped", "", ""]
    rig.nothing_left()


def test_an_unconfirmed_stop_in_change_vault_stays_a_problem_and_a_retry_stops(rig):
    rig.run("start")
    r = rig.run("change-vault", STUB_FUNNEL_STUCK="1", SCATLAB_VAULT=None)
    assert r.returncode == 1 and "could not confirm" in r.stdout, r.stdout
    assert rig.ui_lines()[0] == "problem" and "could not confirm" in rig.ui_lines()[3]
    assert len(rig.called("docker run")) == 1  # no new session was started on top
    assert not (rig.state / "changing").exists()  # and no marker is left behind
    assert rig.run("stop").returncode == 0
    assert rig.ui_lines() == ["stopped", "", ""]
    rig.nothing_left()


# ---------------------------------------------------------------- (f) a reused process id is not a session


def test_a_live_unrelated_process_in_the_session_file_is_not_a_running_session(rig):
    with Unrelated() as p:
        (rig.state / "session").write_text(f"{p.pid}\n")
        r = rig.run("status", SCATLAB_UI="dialog")
        assert r.returncode == 1 and "not running" in r.stdout and "starting" not in r.stdout


def test_start_proceeds_over_an_unrelated_process_and_never_kills_it(rig):
    with Unrelated() as p:
        (rig.state / "session").write_text(f"{p.pid}\n")
        proc = rig.start_bg()
        assert rig.ui_lines()[0] == "running"
        assert rig.called("docker run")
        assert p.poll() is None
        assert rig.stop_bg(proc).returncode == 0
        assert p.poll() is None  # Stop did not kill a process that is not a launcher


def test_stop_does_not_kill_an_unrelated_process_in_the_session_file(rig):
    with Unrelated() as p:
        (rig.state / "session").write_text(f"{p.pid}\n")
        assert rig.run("stop").returncode == 0
        assert p.poll() is None


# ---------------------------------------------------------------- (g) the applet's Stop path


def stop_handler():
    return APPLET[APPLET.index("on stopIt_") : APPLET.index("on idle")]


def test_the_applets_stop_quits_only_on_a_confirmed_stop_and_stays_on_a_problem():
    h = stop_handler()
    ok, failed = h.split("on error msg")
    assert "stopDone to true" in ok and re.search(r"^\s*quit\s*$", ok, re.MULTILINE)
    assert "stopDone" not in failed and not re.search(r"^\s*quit\s*$", failed, re.MULTILINE)
    assert "critical" in failed  # the alert says it is a problem
    assert 'launcher & " stop 2>&1"' in h  # a non-zero exit is what lands in `on error`


def test_the_applets_quit_runs_stop_once_and_never_after_the_stop_item():
    q = APPLET[APPLET.index("on quit") :]
    assert re.search(r"if not stopDone then\s+set stopDone to true", q)
    assert q.count('launcher & " stop') == 1


@pytest.mark.skip(
    reason="The applet's Stop path cannot run hermetically: it needs a window server and puts a status item in the real "
    "menu bar (no existing test starts the applet; test_menubar.py drives the launcher only). Its text is checked above."
)
def test_the_applets_stop_path_with_a_scratch_compiled_stand_in():
    assert sys.platform == "darwin" and shutil.which("osacompile")
