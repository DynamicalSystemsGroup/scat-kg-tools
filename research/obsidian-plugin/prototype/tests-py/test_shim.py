"""End-to-end tests of scat_json.py on a copy of the template case study.

Needs `uv` on PATH and the template at $SCAT_TEMPLATE (default: ~/Documents/GitHub/scat-kg-template).
The template is copied to a scratch folder and never modified. Run: python3 -m pytest tests-py -q
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
SHIM = HERE.parent / "scat_json.py"
TEMPLATE = Path(os.environ.get("SCAT_TEMPLATE", Path.home() / "Documents/GitHub/scat-kg-template"))
SCRATCH = Path(os.environ.get("SCAT_RS1_SCRATCH", Path(tempfile.gettempdir()) / "scat-rs1"))

pytestmark = pytest.mark.skipif(
    shutil.which("uv") is None or not (TEMPLATE / "scat.toml").is_file(),
    reason="needs uv on PATH and the scat-kg-template folder",
)

SEEDED = """---
type: concern
status: done
title: "Seeded"
description: "A page with planted defects."
conflicts:
  - "[[no-such-page]]"
---

Mentions [[also-missing]] in the body.
"""


@pytest.fixture(scope="module")
def vault():
    dest = SCRATCH / "pytest-vault"
    shutil.rmtree(dest, ignore_errors=True)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(TEMPLATE, dest, ignore=shutil.ignore_patterns(".git", ".venv"))
    # install the plugin folder the way a user does, and run the shim from there
    plugin = dest / ".obsidian" / "plugins" / "scat"
    plugin.mkdir(parents=True)
    shutil.copy(SHIM, plugin / "scat_json.py")
    (dest / "concern" / "seeded.md").write_text(SEEDED)
    return dest


def run(vault, note, *extra):
    """The command line the plugin builds (see commandLine in src/runner.ts)."""
    shim = vault / ".obsidian" / "plugins" / "scat" / "scat_json.py"
    cmd = ["uv", "run", "--quiet", "--project", str(vault), "python", str(shim), str(vault / note), *extra]
    print("COMMAND:", " ".join(cmd))
    p = subprocess.run(cmd, cwd=vault, capture_output=True, text=True, timeout=300)
    assert p.returncode == 0, p.stderr
    lines = p.stdout.strip().splitlines()
    assert len(lines) == 1, "stdout holds one JSON object only"
    return json.loads(lines[0])


def test_clean_page(vault):
    d = run(vault, "concern/anonymity.md")
    assert (d["status"], d["ok"], d["problems"], d["page"]) == ("ok", True, [], "concern/anonymity.md")
    assert d["schema_version"] == 1 and d["root"] == str(vault)


def test_case_study_warning(vault):
    d = run(vault, "scenario-coded/notes-at-a-chatham-house-session-coded.md")
    assert d["ok"] is True  # warnings do not block
    [p] = d["problems"]
    assert p["rule"] == "SCAT-CONFLICT-BOTH" and p["severity"] == "warning"
    assert p["file"] == "scenario-coded/notes-at-a-chatham-house-session-coded.md"
    assert p["line"] == 11 and p["column"] is None and p["repeat"] == 1
    assert p["where"] == "field `concerns`"
    assert p["fix"].startswith("Fix: none needed if both belong in this record.")
    assert "order" not in p


def test_seeded_defects(vault):
    d = run(vault, "concern/seeded.md")
    assert d["status"] == "ok" and d["ok"] is False
    assert [(p["rule"], p["severity"], p["line"]) for p in d["problems"]] == [
        ("SCAT-LINK-DANGLING", "error", 7),
        ("SCAT-LINK-DANGLING-BODY", "error", 10),
    ]
    assert d["problems"][0]["fix"] == (
        'Fix: run `scat stub no-such-page --type concern` '
        '(REPL: `scat_kg.stub("no-such-page", type="concern")`) to create it as a stub'
    )
    assert "\n" in d["problems"][1]["fix"]  # the whole multi-line fix block is kept


def test_neighborhood_reaches_other_files(vault):
    d = run(vault, "concern/anonymity.md", "--neighborhood")
    assert d["status"] == "ok"
    files = {p["file"] for p in d["problems"]}
    assert "scenario-coded/notes-at-a-chatham-house-session-coded.md" in files


def test_note_without_type_is_not_a_page(vault):
    d = run(vault, "README.md")
    assert d["status"] == "not-a-page" and d["problems"] == [] and "Nothing is checked" in d["message"]


def test_note_outside_a_vault(tmp_path):
    note = tmp_path / "loose.md"
    note.write_text("---\ntype: concern\n---\n")
    p = subprocess.run([sys.executable, str(SHIM), str(note)], capture_output=True, text=True)
    d = json.loads(p.stdout)
    assert d["status"] == "not-a-vault" and d["problems"] == []


def test_python_without_scat_kg(tmp_path):
    (tmp_path / "scat.toml").write_text("")
    note = tmp_path / "a.md"
    note.write_text("---\ntype: concern\n---\n")
    p = subprocess.run([sys.executable, "-I", str(SHIM), str(note)], capture_output=True, text=True)
    assert json.loads(p.stdout)["status"] == "no-scat-kg"


def test_a_refusal_is_passed_through(tmp_path):
    fake = tmp_path / "fake"
    fake.mkdir()
    (fake / "scat_kg.py").write_text("def check(page, neighborhood=False, root='.'):\n    return 'refused x: no page has this name'\n")
    (tmp_path / "scat.toml").write_text("")
    note = tmp_path / "a.md"
    note.write_text("---\ntype: concern\n---\n")
    env = {**os.environ, "PYTHONPATH": str(fake)}
    p = subprocess.run([sys.executable, str(SHIM), str(note)], capture_output=True, text=True, env=env)
    d = json.loads(p.stdout)
    assert d["status"] == "refused" and d["message"].startswith("refused x")
