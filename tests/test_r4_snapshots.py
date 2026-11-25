"""WP5-R4 (R-4): checks never write; each operation writes only what it should.

Every check scope and every operation, through the public Python API and through the CLI, on a copy of the
example vault with defects seeded (a dangling link, a missing index file). The vault is
snapshotted before and after (bytes, size and mtime of every file and folder), and the paths that changed
are compared with exactly the set the operation is meant to write. A refusal writes nothing.
"""

import shutil
from pathlib import Path

import pytest

import scat_kg
from scat_kg import cli

EXAMPLES = Path(__file__).parents[1] / "contracts" / "examples"
SEEDED_NARRATIVE = "narrative/saturday-at-the-lending-desk.md"  # the page the defect is seeded in


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
    page = root / SEEDED_NARRATIVE
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
    "check-page": (
        lambda r: scat_kg.check(SEEDED_NARRATIVE, root=r),
        ["check", SEEDED_NARRATIVE],
        NONE,
    ),
    "check-neighborhood": (
        lambda r: scat_kg.check(SEEDED_NARRATIVE, neighborhood=True, root=r),
        ["check", SEEDED_NARRATIVE, "--neighborhood"],
        NONE,
    ),
    "status-vault": (lambda r: scat_kg.status(root=r), ["status"], NONE),
    "status-page": (
        lambda r: scat_kg.status(SEEDED_NARRATIVE, root=r),
        ["status", SEEDED_NARRATIVE],
        NONE,
    ),
    "status-neighborhood": (
        lambda r: scat_kg.status(SEEDED_NARRATIVE, neighborhood=True, root=r),
        ["status", SEEDED_NARRATIVE, "--neighborhood"],
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
    "record-edge": (
        lambda r: scat_kg.record_edge("holds", "borrowers", "lending-rules", "story", root=r),
        ["record-edge", "holds", "borrowers", "lending-rules", "--told-by", "story"],
        {
            "concern/lending-rules.md": "created",  # the missing end, stubbed
            "narrative/story.md": "created",  # the missing narrative, stubbed, with the row
        },
    ),
    "record-edge-existing-narrative": (
        lambda r: scat_kg.record_edge(
            "holds", "funders", "lending-rules", "funders-meeting", root=r
        ),
        ["record-edge", "holds", "funders", "lending-rules", "--told-by", "funders-meeting"],
        {"concern/lending-rules.md": "created", "narrative/funders-meeting.md": "changed"},
    ),
    "remove-edge": (
        lambda r: scat_kg.remove_edge("funders", "careful-record-keeping", root=r),
        ["remove-edge", "funders", "careful-record-keeping"],
        {"narrative/funders-meeting.md": "changed"},
    ),
    "stub-links-vault": (
        lambda r: scat_kg.stub_links(root=r),
        ["stub-links"],
        {"concern/ghost.md": "created"},
    ),
    "stub-links-page": (
        lambda r: scat_kg.stub_links(SEEDED_NARRATIVE, root=r),
        ["stub-links", SEEDED_NARRATIVE],
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
    "set-status-done-refused": (
        lambda r: scat_kg.set_status("funders-meeting", "done", root=r),
        ["set-status", "funders-meeting", "done"],
        NONE,
    ),
    "record-edge-refused": (
        lambda r: scat_kg.record_edge("owns", "a", "b", "n", root=r),
        ["record-edge", "owns", "a", "b", "--told-by", "n"],
        NONE,
    ),
    "record-edge-into-done-refused": (
        lambda r: scat_kg.record_edge(
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
        NONE,
    ),
    "remove-edge-refused": (
        lambda r: scat_kg.remove_edge("borrowers", "quick-checkout", root=r),
        ["remove-edge", "borrowers", "quick-checkout"],
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
    assert changes(before, snapshot(root)) == expected


def test__r4__every_check_scope_and_operation_is_covered():
    commands = {argv[0] for _, argv, _ in CASES.values()}
    assert commands == {
        "check", "status", "set-status", "index", "stub", "stub-links", "record-edge", "remove-edge",
    }  # fmt: skip
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
        api(root)
        before = snapshot(root)
        api(root)
        capsys.readouterr()
        assert changes(before, snapshot(root)) == {}, case
