"""The launcher's side of the menu-bar app (WP22 G3 to G5, G7; D-130): the state file, the two copy verbs, change vault,
the vault question at every start, the key's safety, and the once-only first-start note. Stand-ins only."""

import pytest

STOP = {"SCATLAB_A_STOP": "stop"}
ADDRESS = "https://fake-mac.tail1234.ts.net/mcp"
NOTE = "lives in the menu bar"


def other_vault(rig, name="other"):
    v = rig.tmp / name
    v.mkdir()
    (v / "scat.toml").write_text("x = 1\n")
    return v


def remember(rig, vault):
    (rig.state / "vault").write_text(f"{vault.resolve()}\n")


# ---------------------------------------------------------------- $STATE/ui (WP22-R3)


def test_ui_file_at_running_holds_state_vault_and_address_and_never_the_key(rig):
    assert rig.run("start").returncode == 0  # stays up
    assert rig.ui_lines() == ["running", str(rig.vault.resolve()), ADDRESS]
    assert rig.key().encode() not in (rig.state / "ui").read_bytes()
    rig.run("stop")


def test_ui_file_at_a_problem_has_the_problem_line_and_never_the_key(rig):
    r = rig.run("start", STUB_FAIL_RUN="1")
    assert r.returncode == 1
    lines = rig.ui_lines()
    assert len(lines) == 4, lines
    assert lines[0] == "problem" and lines[1] == str(rig.vault.resolve()) and lines[2] == ""
    assert "The server would not start" in lines[3] and "port in use" in lines[3]
    (key,) = rig.keys_seen()
    assert key not in (rig.state / "ui").read_text()


def test_ui_file_after_the_stop_verb_says_stopped_with_no_vault_or_address(rig):
    rig.run("start")
    assert rig.ui_lines()[0] == "running"
    assert rig.run("stop").returncode == 0
    assert rig.ui_lines() == ["stopped", "", ""]


def test_ui_file_after_a_stop_button_start_says_stopped_without_a_problem_line(rig):
    assert rig.run("start", **STOP).returncode == 0
    lines = rig.ui_lines()
    assert lines[0] == "stopped" and len(lines) == 3, lines
    (key,) = rig.keys_seen()
    assert key not in (rig.state / "ui").read_text()


# ---------------------------------------------------------------- Copy address, Copy key (WP22-R4)


def test_copy_address_puts_exactly_the_address_on_the_clipboard_and_not_the_key(rig):
    rig.run("start")
    assert rig.clip() == ""
    r = rig.run("copy-address")
    assert r.returncode == 0, r.stdout
    assert rig.clip() == ADDRESS  # exactly: no newline, no key, nothing else
    assert rig.key() not in rig.clip()
    rig.run("stop")


def test_copy_address_when_nothing_runs_says_so_and_leaves_the_clipboard_alone(rig):
    (rig.stub / "clip").write_text("mine")
    r = rig.run("copy-address")
    assert r.returncode == 1 and "not running" in r.stdout
    assert rig.clip() == "mine"


def test_copy_key_puts_exactly_the_key_on_the_clipboard_and_only_on_request(rig):
    rig.run("start")
    key = rig.key()
    assert rig.clip() == ""  # nothing asked, nothing copied
    r = rig.run("copy-address")
    assert rig.clip() == ADDRESS != key  # the other button does not copy the key
    r = rig.run("copy-key")
    assert r.returncode == 0, r.stdout
    assert rig.clip() == key and len(key) == 64  # exactly the key
    assert key not in r.stdout
    rig.run("stop")


def test_copy_key_when_nothing_runs_says_so_and_leaves_the_clipboard_alone(rig):
    (rig.stub / "clip").write_text("mine")
    r = rig.run("copy-key")
    assert r.returncode == 1 and "no key" in r.stdout
    assert rig.clip() == "mine"


# ---------------------------------------------------------------- Change vault (D-130)


def test_change_vault_stops_then_starts_and_offers_the_vault_chooser(rig):
    second = other_vault(rig)
    rig.run("start")  # the first session, on the rig's vault
    first_key = rig.key()
    r = rig.run("change-vault", SCATLAB_VAULT=None, SCATLAB_A_VAULT=str(second))
    assert r.returncode == 0, r.stdout
    assert "Choose your vault" in r.stdout  # the chooser, not the remembered vault
    assert "Serve " not in r.stdout
    runs = rig.called("docker run")
    assert len(runs) == 2, rig.calls_list()
    (off,) = rig.called("tailscale funnel --https=443 off")
    (drop,) = rig.called("security delete-generic-password")
    assert runs[0] < off < runs[1] and runs[0] < drop < runs[1]  # stop between the two starts
    assert f"-v {second.resolve()}:/vault" in rig.calls_list()[runs[1]]
    assert rig.key() != first_key  # a new session key
    assert rig.ui_lines()[:2] == ["running", str(second.resolve())]
    assert (rig.state / "vault").read_text().strip() == str(second.resolve())
    rig.run("stop")
    rig.nothing_left()


def test_change_vault_with_no_vault_chosen_leaves_it_stopped(rig):
    rig.run("start")
    r = rig.run("change-vault", SCATLAB_VAULT=None)
    assert r.returncode == 1 and "No vault was chosen" in r.stdout
    assert len(rig.called("docker run")) == 1
    rig.nothing_left()


# ---------------------------------------------------------------- the vault at every start (WP22-R5)


def test_a_remembered_vault_is_asked_about_and_use_it_serves_it(rig):
    remember(rig, rig.vault)
    r = rig.run("start", SCATLAB_VAULT=None, SCATLAB_A_USE="Use it", **STOP)
    assert r.returncode == 0, r.stdout
    assert (
        f"Serve {rig.vault.resolve()}?" in r.stdout
        and "Use it" in r.stdout
        and "Choose another" in r.stdout
    )
    assert f"-v {rig.vault.resolve()}:/vault" in rig.calls_list()[rig.called("docker run")[0]]
    assert "Choose your vault" not in r.stdout


def test_choose_another_goes_to_the_chooser_and_serves_the_new_vault(rig):
    second = other_vault(rig)
    remember(rig, rig.vault)
    r = rig.run(
        "start",
        SCATLAB_VAULT=None,
        SCATLAB_A_USE="Choose another",
        SCATLAB_A_VAULT=str(second),
        **STOP,
    )
    assert r.returncode == 0, r.stdout
    assert "Choose your vault" in r.stdout
    run = rig.calls_list()[rig.called("docker run")[0]]
    assert f"-v {second.resolve()}:/vault" in run and str(rig.vault.resolve()) not in run
    assert (rig.state / "vault").read_text().strip() == str(second.resolve())


@pytest.mark.parametrize("answer", [None, "yes", "maybe"])
def test_a_remembered_vault_is_never_served_without_the_coders_use_it(rig, answer):
    remember(rig, rig.vault)
    env = {} if answer is None else {"SCATLAB_A_USE": answer}
    r = rig.run("start", SCATLAB_VAULT=None, **env)
    assert r.returncode == 1, r.stdout
    assert f"Serve {rig.vault.resolve()}?" in r.stdout and "No vault was confirmed" in r.stdout
    assert not rig.called("docker run") and not rig.called("docker build")
    rig.nothing_left()


def test_the_vault_question_comes_at_every_start_not_only_the_first(rig):
    remember(rig, rig.vault)
    for _ in range(2):
        r = rig.run("start", SCATLAB_VAULT=None, SCATLAB_A_USE="Use it", **STOP)
        assert f"Serve {rig.vault.resolve()}?" in r.stdout, r.stdout


# ---------------------------------------------------------------- the key (WP22-G7, WP21-R5)


def test_the_key_is_deleted_at_stop_and_never_written_to_the_state_folder(rig):
    rig.run("start")
    key = rig.key()
    rig.run("copy-key")
    files = [p for p in rig.state.rglob("*") if p.is_file()]
    assert files and not [p for p in files if key.encode() in p.read_bytes()], files
    rig.run("stop")
    assert not rig.item() and rig.clip() == ""
    assert not [p for p in rig.state.rglob("*") if p.is_file() and key.encode() in p.read_bytes()]
    assert any(c.startswith("security delete-generic-password") for c in rig.calls_list())


# ---------------------------------------------------------------- the first-start note


def test_the_first_start_note_appears_once_per_state_folder(rig):
    first = rig.run("start", **STOP)
    assert NOTE in first.stdout and (rig.state / "menubar-note").exists()
    assert NOTE not in rig.run("start", **STOP).stdout  # the same state folder: not again
    assert NOTE not in rig.run("start", **STOP).stdout
    elsewhere = rig.tmp / "other-state"
    assert (
        NOTE in rig.run("start", SCATLAB_HOME=str(elsewhere), **STOP).stdout
    )  # a new folder: once more
    assert NOTE not in rig.run("start", SCATLAB_HOME=str(elsewhere), **STOP).stdout
