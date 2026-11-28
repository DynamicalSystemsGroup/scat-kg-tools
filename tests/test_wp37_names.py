"""WP37-R1: no file outside the history paths names the app, the repositories or the package by an old name; no file is
called by one either. The history paths keep the names they used. deploy/retire-old.sh must name the earlier app to
remove it (WP37-G2), and its test and this one must name it to check it, so they are the only other files allowed."""

import re
import subprocess
from pathlib import Path

REPO = Path(__file__).parents[1]
HISTORY = ("decisions/", "acceptance/", "work-packages/", "research/")
ALLOWED = {
    "deploy/retire-old.sh",
    "tests/deploy/test_retire_old.py",
    "tests/test_wp37_names.py",
}
# The earlier names: the app (SCAT Chat, scat-chat, SCAT_CHAT_*) and the package and repositories (scat-kg, scat_kg,
# scat-kg-tools, scat-kg-template). SCAT alone, the method's name, stays.
OLD = re.compile(r"scat[ _-]?chat|scat[_-]kg", re.IGNORECASE)


def tracked():
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout
    return [f for f in out.split("\0") if f and (REPO / f).is_file()]


def outside_history(files):
    return [f for f in files if not f.startswith(HISTORY)]


def old_names_in(path):
    hits = [f"its name: {path}"] if OLD.search(path) else []
    try:
        text = (REPO / path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return hits  # a binary file has no words to read
    return hits + [
        f"{path}:{n}: {line.strip()[:100]}"
        for n, line in enumerate(text.splitlines(), 1)
        if OLD.search(line)
    ]


def test_no_file_outside_the_history_paths_uses_an_old_name():
    found = [h for f in outside_history(tracked()) if f not in ALLOWED for h in old_names_in(f)]
    assert not found, "\n".join(found[:40])


def test_the_history_paths_exist_and_keep_their_old_names():
    files = tracked()
    assert any(f.startswith("decisions/") for f in files)
    assert any(
        OLD.search((REPO / f).read_text(encoding="utf-8"))
        for f in files
        if f.startswith("decisions/")
    )


def test_each_allowed_file_still_needs_its_allowance():
    for f in sorted(ALLOWED):
        assert (REPO / f).is_file(), f
        assert old_names_in(f), f"{f} no longer names an old name: remove it from ALLOWED"


def test_the_check_sees_an_old_name():
    """The check itself is not blind: each form of the old names is caught."""
    for s in (
        "SCAT Chat",
        "scat-chat.sh",
        "SCAT_CHAT_UI",
        "scat_kg.check",
        "scat-kg-tools",
        "scat-kg-template",
    ):
        assert OLD.search(s), s
    for s in ("SCATLAB", "scat-tools", "scat_tools", "scat-template", "SCAT", "chat path"):
        assert not OLD.search(s), s
