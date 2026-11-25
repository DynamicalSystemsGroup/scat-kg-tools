"""Both paths, one answer (R-8): every operation through the Python API and through the CLI, on copies of
the same fixture, gives the same message, the same files and the exit code the CLI promises.

The CLI is run through `cli.main(argv)` (no subprocess), and once for real as `uv run scat`.
"""

# TODO(WP16-U7) lift: UNBUILT and the forced exit code 1 for unbuilt commands.

import os
import shutil
import subprocess
from pathlib import Path

import pytest

import scat_kg
from scat_kg import cli

ROOT = Path(__file__).parents[1]
EXAMPLES = ROOT / "contracts" / "examples"
BAD_LINK = "[[no-such-concern]]"
HELDBY = "narrative/saturday-at-the-lending-desk.md"  # the page the defect is seeded in
NO_FOLDER = "/no/such/scat-vault"

# The calls U7 (operations) rebuilds: until then each returns the standard refusal, so its exit code is 1.
# TODO(WP16-U7): drop this.
UNBUILT = {"index", "stub", "stub-pair", "stub-links"}


def tree(root: Path) -> dict[str, bytes]:
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def make(tmp_path: Path, name: str, defect: bool) -> Path:
    root = tmp_path / name
    shutil.copytree(EXAMPLES, root)
    if defect:  # one error: a link to a page that does not exist
        page = root / HELDBY
        text = page.read_text(encoding="utf-8")
        page.write_text(text.replace("[[careful-record-keeping]]", BAD_LINK), encoding="utf-8")
    return root


# name -> (API call given the vault root, the same as CLI arguments, exit code, vault has a defect)
CASES = {
    "check-clean-vault": (lambda r: scat_kg.check(root=r), ["check"], 0, False),
    "check-vault-with-error": (lambda r: scat_kg.check(root=r), ["check"], 1, True),
    "check-page": (lambda r: scat_kg.check(HELDBY, root=r), ["check", HELDBY], 1, True),
    "check-page-by-name": (
        lambda r: scat_kg.check("quick-checkout", root=r),
        ["check", "quick-checkout"],
        0,
        False,
    ),
    "check-neighborhood": (
        lambda r: scat_kg.check("quick-checkout", neighborhood=True, root=r),
        ["check", "quick-checkout", "--neighborhood"],
        0,
        False,
    ),
    "check-neighborhood-with-error": (
        lambda r: scat_kg.check(HELDBY, neighborhood=True, root=r),
        ["check", HELDBY, "--neighborhood"],
        1,
        True,
    ),
    "check-neighborhood-needs-a-page": (
        lambda r: scat_kg.check(neighborhood=True, root=r),
        ["check", "--neighborhood"],
        1,
        False,
    ),
    "check-no-such-page": (
        lambda r: scat_kg.check("nope", root=r),
        ["check", "nope"],
        1,
        False,
    ),
    "status-vault": (lambda r: scat_kg.status(root=r), ["status"], 0, False),
    "status-page": (
        lambda r: scat_kg.status("quick-checkout", root=r),
        ["status", "quick-checkout"],
        0,
        False,
    ),
    "status-neighborhood": (
        lambda r: scat_kg.status("quick-checkout", neighborhood=True, root=r),
        ["status", "quick-checkout", "--neighborhood"],
        0,
        False,
    ),
    "status-neighborhood-needs-a-page": (
        lambda r: scat_kg.status(neighborhood=True, root=r),
        ["status", "--neighborhood"],
        1,
        False,
    ),
    "set-status": (
        lambda r: scat_kg.set_status("quick-checkout", "draft", root=r),
        ["set-status", "quick-checkout", "draft"],
        0,
        False,
    ),
    "set-status-not-a-status": (
        lambda r: scat_kg.set_status("quick-checkout", "finished", root=r),
        ["set-status", "quick-checkout", "finished"],
        1,
        False,
    ),
    "set-status-no-such-page": (
        lambda r: scat_kg.set_status("nope", "draft", root=r),
        ["set-status", "nope", "draft"],
        1,
        False,
    ),
    "index-current": (lambda r: scat_kg.index(root=r), ["index"], 0, False),
    "stub": (
        lambda r: scat_kg.stub("lending-rules", type="concern", root=r),
        ["stub", "lending-rules", "--type", "concern"],
        0,
        False,
    ),
    "stub-illegal-name": (
        lambda r: scat_kg.stub("Lending Rules", type="concern", root=r),
        ["stub", "Lending Rules", "--type", "concern"],
        1,
        False,
    ),
    "stub-relation-type-refused": (
        lambda r: scat_kg.stub("x-holds-y", type="heldby", root=r),
        ["stub", "x-holds-y", "--type", "heldby"],
        1,
        False,
    ),
    "stub-pair": (
        lambda r: scat_kg.stub_pair("heldby", "borrowers", "quick-checkout", root=r),
        ["stub-pair", "heldby", "borrowers", "quick-checkout"],
        0,
        False,
    ),
    "stub-pair-stubs-a-missing-endpoint": (
        lambda r: scat_kg.stub_pair("heldby", "borrowers", "lending-rules", root=r),
        ["stub-pair", "heldby", "borrowers", "lending-rules"],
        0,
        False,
    ),
    "stub-pair-not-a-relation": (
        lambda r: scat_kg.stub_pair("owns", "a", "b", root=r),
        ["stub-pair", "owns", "a", "b"],
        1,
        False,
    ),
    "stub-links-vault": (lambda r: scat_kg.stub_links(root=r), ["stub-links"], 0, True),
    "stub-links-page": (
        lambda r: scat_kg.stub_links(HELDBY, root=r),
        ["stub-links", HELDBY],
        0,
        True,
    ),
    "no-vault-folder": (
        lambda r: scat_kg.check(root=NO_FOLDER),
        ["check", "--root", NO_FOLDER],
        1,
        False,
    ),
}


def run_both(tmp_path, capsys, api, argv, defect):
    a, b = make(tmp_path, "api", defect), make(tmp_path, "cli", defect)
    result = api(a)
    capsys.readouterr()
    code = cli.main(argv if "--root" in argv else [*argv, "--root", str(b)])
    out = capsys.readouterr().out
    return result, code, out, a, b


@pytest.mark.parametrize("case", CASES)
def test__the_api_and_the_cli_give_the_same_message_files_and_exit_code(case, tmp_path, capsys):
    api, argv, exit_code, defect = CASES[case]
    if argv[0] in UNBUILT:
        exit_code = 1  # the refusal; the intended code is the one in CASES
    result, code, out, a, b = run_both(tmp_path, capsys, api, argv, defect)
    assert out == str(result) + "\n"
    assert repr(result) == str(result)  # at the REPL it prints as its message
    assert code == exit_code
    assert code == (0 if result.ok else 1)
    assert tree(a) == tree(b)  # the same files written, byte for byte


def test__every_operation_is_covered():
    commands = {argv[0] for _, argv, _, _ in CASES.values()}
    assert commands == {"check", "status", "set-status", "index", "stub", "stub-pair", "stub-links"}


def test__a_warning_alone_exits_zero_and_an_error_exits_nonzero(tmp_path, capsys):
    clean = make(tmp_path, "clean", False)
    assert cli.main(["check", "--root", str(clean)]) == 0
    assert "warning [SCAT-DRAFT-FIELD]" in capsys.readouterr().out
    bad = make(tmp_path, "bad", True)
    assert cli.main(["check", "--root", str(bad)]) == 1
    assert "error [SCAT-LINK-DANGLING-BODY]" in capsys.readouterr().out
    assert scat_kg.check(root=clean).ok and not scat_kg.check(root=bad).ok
    # the draft narrative has no `description` and no `timeframe`: two warnings, no error
    assert len(scat_kg.check(root=clean).warnings) == 2 and not scat_kg.check(root=clean).errors


def test__the_vault_root_defaults_to_the_current_directory(tmp_path, capsys, monkeypatch):
    api, via_cli = make(tmp_path, "api", True), make(tmp_path, "cli", True)
    monkeypatch.chdir(api)
    result = scat_kg.status()
    monkeypatch.chdir(via_cli)
    assert cli.main(["status"]) == 0
    assert capsys.readouterr().out == str(result) + "\n"
    assert scat_kg.set_status(
        "quick-checkout", "draft"
    ).ok  # the default root is here for every operation


def test__the_message_is_the_one_the_catalogue_prints_and_its_fix_runs_on_both_paths(
    tmp_path, capsys
):
    """A session: check, seed a defect, check (error + exact fix), apply the printed fix, check clean."""
    a, b = make(tmp_path, "api", False), make(tmp_path, "cli", False)
    page = "concern/quick-checkout.md"
    for root in (a, b):  # the defect: a done page loses its description
        p = root / page
        p.write_text(
            p.read_text(encoding="utf-8").replace("description:", "notes:", 1), encoding="utf-8"
        )
    first = scat_kg.check(root=a)
    assert not first.ok
    problem = first.errors[0]
    assert problem.rule == "SCAT-DONE-FIELD" and problem.file == page
    assert (
        '`scat set-status quick-checkout draft` (REPL: `scat_kg.set_status("quick-checkout", "draft")`)'
        in problem.fix
    )
    assert scat_kg.set_status("quick-checkout", "draft", root=a).ok  # the printed REPL fix
    assert (
        cli.main(["set-status", "quick-checkout", "draft", "--root", str(b)]) == 0
    )  # the printed command
    capsys.readouterr()
    assert tree(a) == tree(b)
    after = scat_kg.check(root=a)
    assert after.ok and cli.main(["check", "--root", str(b)]) == 0
    assert capsys.readouterr().out == str(after) + "\n"


@pytest.mark.parametrize(
    "command", ["check", "status", "set-status", "index", "stub", "stub-pair", "stub-links"]
)
def test__every_command_has_help(command, capsys):
    with pytest.raises(SystemExit) as e:
        cli.main([command, "--help"])
    assert e.value.code == 0
    out = capsys.readouterr().out
    assert f"usage: scat {command}" in out and "REPL:" in out and "--root" in out


def test__the_top_level_help_lists_every_command(capsys):
    with pytest.raises(SystemExit) as e:
        cli.main(["--help"])
    assert e.value.code == 0
    out = capsys.readouterr().out
    for c in ("check", "status", "set-status", "index", "stub", "stub-pair", "stub-links"):
        assert c in out


def test__a_command_line_that_cannot_be_read_exits_two(capsys):
    for argv in ([], ["nonsense"], ["stub", "x"], ["set-status", "x"]):
        with pytest.raises(SystemExit) as e:
            cli.main(argv)
        assert e.value.code == 2
    capsys.readouterr()


def test__a_real_scat_invocation_gives_the_same_message_and_exit_code(tmp_path):
    api, real = make(tmp_path, "api", True), make(tmp_path, "real", True)
    expected = str(scat_kg.check(root=api))
    done = subprocess.run(
        ["uv", "run", "--locked", "scat", "check", "--root", str(real)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert done.returncode == 1, done.stderr  # the seeded defect is an error
    assert done.stdout == expected + "\n"
    ok = subprocess.run(
        ["uv", "run", "--locked", "scat", "set-status", "quick-checkout", "draft"],
        cwd=real,
        env={**os.environ, "UV_PROJECT": str(ROOT)},
        capture_output=True,
        text=True,
        check=False,
    )
    assert ok.returncode == 0, ok.stderr
    assert ok.stdout == str(scat_kg.set_status("quick-checkout", "draft", root=api)) + "\n"
    assert tree(api) == tree(real)
