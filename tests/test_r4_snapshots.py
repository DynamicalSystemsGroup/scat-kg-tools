"""WP5-R4 (R-4): checks never write; each operation writes only what it should.

Every check scope and every operation, through the public Python API and through the CLI, on a copy of the
example vault with defects seeded (a dangling link, a missing index file). The vault is
snapshotted before and after (bytes, size and mtime of every file and folder), and the paths that changed
are compared with exactly the set the operation is meant to write. A refusal writes nothing.
"""

# TODO(WP16-U6/U7) lift: UNBUILT makes the unbuilt calls expect no writes; restore the intended expectations.

import shutil
from pathlib import Path

import pytest

import scat_kg
from scat_kg import cli

EXAMPLES = Path(__file__).parents[1] / "contracts" / "examples"
HELDBY = "narrative/saturday-at-the-lending-desk.md"  # the page the defect is seeded in

# The calls U6 (checks) and U7 (operations) rebuild return the standard refusal until then, which writes
# nothing: for these the expected changes below are the intended ones and are asserted only once built.
# TODO(WP16-U6, WP16-U7): drop UNBUILT.
UNBUILT = {"check", "index", "stub", "stub-pair", "stub-links"}


def snapshot(root: Path) -> dict[str, tuple]:
    out = {}
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).as_posix()
        if p.is_dir():
            out[rel] = ("dir",)
        else:
            out[rel] = ("file", p.stat().st_mtime_ns, p.read_bytes())
    return out


def changes(before: dict, after: dict) -> dict[str, str]:
    out = {}
    for k in before.keys() | after.keys():
        if k not in before:
            out[k] = "created"
        elif k not in after:
            out[k] = "removed"
        elif before[k] != after[k]:
            out[k] = "changed"
    return out


def seeded_vault(tmp_path: Path, name: str) -> Path:
    """The examples with one dangling link and a missing index file."""
    root = tmp_path / name
    shutil.copytree(EXAMPLES, root)
    page = root / HELDBY
    page.write_text(
        page.read_text(encoding="utf-8").replace("[[careful-record-keeping]]", "[[ghost]]"),
        encoding="utf-8",
    )
    (root / "index/concern.base").unlink()
    return root


NONE: dict[str, str] = {}

# name -> (API call, the same as CLI arguments, the paths it may write and how)
CASES = {
    "check-vault": (lambda r: scat_kg.check(root=r), ["check"], NONE),
    "check-page": (lambda r: scat_kg.check(HELDBY, root=r), ["check", HELDBY], NONE),
    "check-neighborhood": (
        lambda r: scat_kg.check(HELDBY, neighborhood=True, root=r),
        ["check", HELDBY, "--neighborhood"],
        NONE,
    ),
    "status-vault": (lambda r: scat_kg.status(root=r), ["status"], NONE),
    "status-page": (lambda r: scat_kg.status(HELDBY, root=r), ["status", HELDBY], NONE),
    "status-neighborhood": (
        lambda r: scat_kg.status(HELDBY, neighborhood=True, root=r),
        ["status", HELDBY, "--neighborhood"],
        NONE,
    ),
    "set-status": (
        lambda r: scat_kg.set_status("quick-checkout", "draft", root=r),
        ["set-status", "quick-checkout", "draft"],
        {"concern/quick-checkout.md": "changed"},
    ),
    "index": (
        lambda r: scat_kg.index(root=r),
        ["index"],
        {"index/concern.base": "created"},
    ),
    "stub": (
        lambda r: scat_kg.stub("lending-rules", type="concern", root=r),
        ["stub", "lending-rules", "--type", "concern"],
        {"concern/lending-rules.md": "created"},
    ),
    "stub-pair": (
        lambda r: scat_kg.stub_pair("heldby", "borrowers", "lending-rules", root=r),
        ["stub-pair", "heldby", "borrowers", "lending-rules"],
        {
            "concern/lending-rules.md": "created",  # the missing endpoint, stubbed
        },
    ),
    "stub-links-vault": (
        lambda r: scat_kg.stub_links(root=r),
        ["stub-links"],
        {"concern/ghost.md": "created"},
    ),
    "stub-links-page": (
        lambda r: scat_kg.stub_links(HELDBY, root=r),
        ["stub-links", HELDBY],
        {"concern/ghost.md": "created"},
    ),
    # refusals write nothing
    "set-status-refused": (
        lambda r: scat_kg.set_status("quick-checkout", "finished", root=r),
        ["set-status", "quick-checkout", "finished"],
        NONE,
    ),
    "stub-refused": (
        lambda r: scat_kg.stub("Lending Rules", type="concern", root=r),
        ["stub", "Lending Rules", "--type", "concern"],
        NONE,
    ),
    "stub-existing-page-refused": (
        lambda r: scat_kg.stub("quick-checkout", type="concern", root=r),
        ["stub", "quick-checkout", "--type", "concern"],
        NONE,
    ),
    "stub-pair-refused": (
        lambda r: scat_kg.stub_pair("owns", "a", "b", root=r),
        ["stub-pair", "owns", "a", "b"],
        NONE,
    ),
    "check-no-such-page": (lambda r: scat_kg.check("nope", root=r), ["check", "nope"], NONE),
}


@pytest.mark.parametrize("path", ["api", "cli"])
@pytest.mark.parametrize("case", CASES)
def test__r4__each_operation_and_check_writes_only_what_it_should(case, path, tmp_path, capsys):
    api, argv, expected = CASES[case]
    root = seeded_vault(tmp_path, "vault")
    before = snapshot(root)
    if path == "api":
        api(root)
    else:
        cli.main([*argv, "--root", str(root)])
    capsys.readouterr()
    assert changes(before, snapshot(root)) == (NONE if argv[0] in UNBUILT else expected)


def test__r4__every_check_scope_and_operation_is_covered():
    commands = {argv[0] for _, argv, _ in CASES.values()}
    assert commands == {"check", "status", "set-status", "index", "stub", "stub-pair", "stub-links"}
    for command in ("check", "status"):
        flags = {tuple(a for a in argv if a.startswith("--n")) for _, argv, _ in CASES.values()
                 if argv[0] == command}  # fmt: skip
        assert flags == {(), ("--neighborhood",)}  # whole vault and page, and neighborhood
    assert {len(argv) for _, argv, _ in CASES.values() if argv[0] == "check"} >= {1, 2, 3}


def test__r4__a_second_run_of_every_writing_operation_writes_nothing(tmp_path, capsys):
    for case, (api, _argv, expected) in CASES.items():
        if not expected:
            continue
        root = seeded_vault(tmp_path, case)
        api(root)  # (a refusal until built: nothing written, so the second run is the same)
        before = snapshot(root)
        api(root)
        capsys.readouterr()
        assert changes(before, snapshot(root)) == {}, case
