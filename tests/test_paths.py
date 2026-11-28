"""Both paths, one answer (R-8): every operation through the Python API and through the CLI, on copies of
the same fixture, gives the same message, the same files and the exit code the CLI promises.

The CLI is run through `cli.main(argv)` (no subprocess), and once for real as `uv run scat`.
"""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

import scat_tools
from scat_tools import cli

ROOT = Path(__file__).parents[1]
EXAMPLES = ROOT / "contracts" / "examples"
BAD_LINK = "[[no-such-concern]]"
SEEDED_NARRATIVE = "narrative/saturday-at-the-lending-desk.md"  # the page the defect is seeded in
NO_FOLDER = "/no/such/scat-vault"


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
        page = root / SEEDED_NARRATIVE
        text = page.read_text(encoding="utf-8")
        page.write_text(text.replace("[[careful-record-keeping]]", BAD_LINK), encoding="utf-8")
    return root


# name -> (API call given the vault root, the same as CLI arguments, exit code, vault has a defect)
CASES = {
    "check-clean-vault": (lambda r: scat_tools.check(root=r), ["check"], 0, False),
    "check-vault-with-error": (lambda r: scat_tools.check(root=r), ["check"], 1, True),
    "check-page": (
        lambda r: scat_tools.check(SEEDED_NARRATIVE, root=r),
        ["check", SEEDED_NARRATIVE],
        1,
        True,
    ),
    "check-page-by-name": (
        lambda r: scat_tools.check("quick-checkout", root=r),
        ["check", "quick-checkout"],
        0,
        False,
    ),
    "check-neighborhood": (
        lambda r: scat_tools.check("quick-checkout", neighborhood=True, root=r),
        ["check", "quick-checkout", "--neighborhood"],
        0,
        False,
    ),
    "check-neighborhood-with-error": (
        lambda r: scat_tools.check(SEEDED_NARRATIVE, neighborhood=True, root=r),
        ["check", SEEDED_NARRATIVE, "--neighborhood"],
        1,
        True,
    ),
    "check-neighborhood-needs-a-page": (
        lambda r: scat_tools.check(neighborhood=True, root=r),
        ["check", "--neighborhood"],
        1,
        False,
    ),
    "check-no-such-page": (
        lambda r: scat_tools.check("nope", root=r),
        ["check", "nope"],
        1,
        False,
    ),
    "status-vault": (lambda r: scat_tools.status(root=r), ["status"], 0, False),
    "status-page": (
        lambda r: scat_tools.status("quick-checkout", root=r),
        ["status", "quick-checkout"],
        0,
        False,
    ),
    "status-neighborhood": (
        lambda r: scat_tools.status("quick-checkout", neighborhood=True, root=r),
        ["status", "quick-checkout", "--neighborhood"],
        0,
        False,
    ),
    "status-neighborhood-needs-a-page": (
        lambda r: scat_tools.status(neighborhood=True, root=r),
        ["status", "--neighborhood"],
        1,
        False,
    ),
    "set-status": (
        lambda r: scat_tools.set_status("quick-checkout", "draft", root=r),
        ["set-status", "quick-checkout", "draft"],
        0,
        False,
    ),
    "set-status-not-a-status": (
        lambda r: scat_tools.set_status("quick-checkout", "finished", root=r),
        ["set-status", "quick-checkout", "finished"],
        1,
        False,
    ),
    "set-status-no-such-page": (
        lambda r: scat_tools.set_status("nope", "draft", root=r),
        ["set-status", "nope", "draft"],
        1,
        False,
    ),
    "index-current": (lambda r: scat_tools.index(root=r), ["index"], 0, False),
    "stub": (
        lambda r: scat_tools.stub("lending-rules", type="concern", root=r),
        ["stub", "lending-rules", "--type", "concern"],
        0,
        False,
    ),
    "stub-illegal-name": (
        lambda r: scat_tools.stub("Lending Rules", type="concern", root=r),
        ["stub", "Lending Rules", "--type", "concern"],
        1,
        False,
    ),
    "stub-index-type-refused": (
        lambda r: scat_tools.stub("x", type="index", root=r),
        ["stub", "x", "--type", "index"],
        1,
        False,
    ),
    "set-status-done-refused": (
        lambda r: scat_tools.set_status("funders-meeting", "done", root=r),
        ["set-status", "funders-meeting", "done"],
        1,
        False,
    ),
    "record-edge": (
        lambda r: scat_tools.record_edge(
            "holds", "borrowers", "lending-rules", ["story"], "n", root=r
        ),
        ["record-edge", "holds", "borrowers", "lending-rules", "--told-by", "story", "--note", "n"],
        0,
        False,
    ),
    "record-edge-two-narratives": (
        lambda r: scat_tools.record_edge(
            "addressed-by", "quick-checkout", "self-checkout", ["funders-meeting", "x"], root=r
        ),
        [
            "record-edge",
            "addressed-by",
            "quick-checkout",
            "self-checkout",
            "--told-by",
            "funders-meeting",
            "--told-by",
            "x",
        ],
        0,
        False,
    ),
    "record-edge-unchanged": (
        lambda r: scat_tools.record_edge(
            "holds", "borrowers", "quick-checkout", "saturday-at-the-lending-desk", root=r
        ),
        [
            "record-edge",
            "holds",
            "borrowers",
            "quick-checkout",
            "--told-by",
            "saturday-at-the-lending-desk",
        ],
        0,
        False,
    ),
    "record-edge-bad-type": (
        lambda r: scat_tools.record_edge("owns", "a", "b", "n", root=r),
        ["record-edge", "owns", "a", "b", "--told-by", "n"],
        1,
        False,
    ),
    "record-edge-into-done": (
        lambda r: scat_tools.record_edge(
            "holds", "funders", "lending-rules", "saturday-at-the-lending-desk", root=r
        ),
        [
            "record-edge",
            "holds",
            "funders",
            "lending-rules",
            "--told-by",
            "saturday-at-the-lending-desk",
        ],
        1,
        False,
    ),
    "remove-edge": (
        lambda r: scat_tools.remove_edge("funders", "careful-record-keeping", root=r),
        ["remove-edge", "funders", "careful-record-keeping"],
        0,
        False,
    ),
    "remove-edge-told-by": (
        lambda r: scat_tools.remove_edge(
            "funders", "careful-record-keeping", ["funders-meeting"], root=r
        ),
        ["remove-edge", "funders", "careful-record-keeping", "--told-by", "funders-meeting"],
        0,
        False,
    ),
    "remove-edge-from-done": (
        lambda r: scat_tools.remove_edge("borrowers", "quick-checkout", root=r),
        ["remove-edge", "borrowers", "quick-checkout"],
        1,
        False,
    ),
    "remove-edge-no-such-node": (
        lambda r: scat_tools.remove_edge("ghost", "quick-checkout", root=r),
        ["remove-edge", "ghost", "quick-checkout"],
        1,
        False,
    ),
    "stub-links-vault": (lambda r: scat_tools.stub_links(root=r), ["stub-links"], 0, True),
    "stub-links-page": (
        lambda r: scat_tools.stub_links(SEEDED_NARRATIVE, root=r),
        ["stub-links", SEEDED_NARRATIVE],
        0,
        True,
    ),
    "no-vault-folder": (
        lambda r: scat_tools.check(root=NO_FOLDER),
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
    result, code, out, a, b = run_both(tmp_path, capsys, api, argv, defect)
    assert out == str(result) + "\n"
    assert repr(result) == str(result)  # at the REPL it prints as its message
    assert code == exit_code
    assert code == (0 if result.ok else 1)
    assert tree(a) == tree(b)  # the same files written, byte for byte


def test__every_operation_is_covered():
    commands = {argv[0] for _, argv, _, _ in CASES.values()}
    assert commands == {
        "check", "status", "set-status", "index", "stub", "stub-links", "record-edge", "remove-edge",
    }  # fmt: skip


def test__a_warning_alone_exits_zero_and_an_error_exits_nonzero(tmp_path, capsys):
    clean = make(tmp_path, "clean", False)
    assert cli.main(["check", "--root", str(clean)]) == 0
    assert "warning [SCAT-DRAFT-FIELD]" in capsys.readouterr().out
    bad = make(tmp_path, "bad", True)
    assert cli.main(["check", "--root", str(bad)]) == 1
    assert "error [SCAT-LINK-DANGLING-BODY]" in capsys.readouterr().out
    assert scat_tools.check(root=clean).ok and not scat_tools.check(root=bad).ok
    # the draft narrative has no `description` and no `timeframe`: two warnings, no error
    assert (
        len(scat_tools.check(root=clean).warnings) == 2 and not scat_tools.check(root=clean).errors
    )


def test__a_session_of_edges_gives_the_same_messages_and_files_on_both_paths(tmp_path, capsys):
    """record, remove, refuse then accept `done`, index and stub-links: the CLI and the API twin, step by step."""
    a, b = make(tmp_path, "api", False), make(tmp_path, "cli", False)
    (a / "index/concern.base").unlink()
    (b / "index/concern.base").unlink()
    steps = [
        (lambda r: scat_tools.record_edge("holds", "funders", "lending-rules", "story", "n", root=r),
         ["record-edge", "holds", "funders", "lending-rules", "--told-by", "story", "--note", "n"]),
        (lambda r: scat_tools.record_edge("holds", "funders", "lending-rules", "story", "n", root=r),
         ["record-edge", "holds", "funders", "lending-rules", "--told-by", "story", "--note", "n"]),
        (lambda r: scat_tools.set_status("story", "done", root=r), ["set-status", "story", "done"]),
        (lambda r: scat_tools.remove_edge("funders", "lending-rules", root=r),
         ["remove-edge", "funders", "lending-rules"]),
        (lambda r: scat_tools.set_status("story", "draft", root=r), ["set-status", "story", "draft"]),
        (lambda r: scat_tools.remove_edge("funders", "lending-rules", root=r),
         ["remove-edge", "funders", "lending-rules"]),
        (lambda r: scat_tools.index(root=r), ["index"]),
        (lambda r: scat_tools.stub_links(root=r), ["stub-links"]),
    ]  # fmt: skip
    for api, argv in steps:
        result = api(a)
        capsys.readouterr()
        code = cli.main([*argv, "--root", str(b)])
        assert capsys.readouterr().out == str(result) + "\n", argv
        assert code == (0 if result.ok else 1) and tree(a) == tree(b), argv


def test__the_vault_root_defaults_to_the_current_directory(tmp_path, capsys, monkeypatch):
    api, via_cli = make(tmp_path, "api", True), make(tmp_path, "cli", True)
    monkeypatch.chdir(api)
    result = scat_tools.status()
    monkeypatch.chdir(via_cli)
    assert cli.main(["status"]) == 0
    assert capsys.readouterr().out == str(result) + "\n"
    assert scat_tools.set_status(
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
    first = scat_tools.check(root=a)
    assert not first.ok
    problem = first.errors[0]
    assert problem.rule == "SCAT-DONE-FIELD" and problem.file == page
    assert (
        '`scat set-status quick-checkout draft` (REPL: `scat_tools.set_status("quick-checkout", "draft")`)'
        in problem.fix
    )
    assert scat_tools.set_status("quick-checkout", "draft", root=a).ok  # the printed REPL fix
    assert (
        cli.main(["set-status", "quick-checkout", "draft", "--root", str(b)]) == 0
    )  # the printed command
    capsys.readouterr()
    assert tree(a) == tree(b)
    after = scat_tools.check(root=a)
    assert after.ok and cli.main(["check", "--root", str(b)]) == 0
    assert capsys.readouterr().out == str(after) + "\n"


@pytest.mark.parametrize(
    "command",
    ["check", "status", "set-status", "index", "stub", "stub-links", "record-edge", "remove-edge"],
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
    for c in (
        "check", "status", "set-status", "index", "stub", "stub-links", "record-edge", "remove-edge",
    ):  # fmt: skip
        assert c in out
    assert "stub-pair" not in out


def test__a_command_line_that_cannot_be_read_exits_two(capsys):
    for argv in (
        [],
        ["nonsense"],
        ["stub", "x"],
        ["set-status", "x"],
        ["stub-pair", "heldby", "a", "b"],
        ["record-edge", "holds", "a", "b"],  # --told-by is required
        ["remove-edge", "a"],
    ):
        with pytest.raises(SystemExit) as e:
            cli.main(argv)
        assert e.value.code == 2
    capsys.readouterr()


def test__a_real_scat_invocation_gives_the_same_message_and_exit_code(tmp_path):
    api, real = make(tmp_path, "api", True), make(tmp_path, "real", True)
    expected = str(scat_tools.check(root=api))
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
    assert ok.stdout == str(scat_tools.set_status("quick-checkout", "draft", root=api)) + "\n"
    assert tree(api) == tree(real)
