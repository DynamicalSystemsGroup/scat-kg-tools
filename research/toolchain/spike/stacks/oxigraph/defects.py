"""Seeded defects on temp copies of the mini-vault (spike/vault is never edited). Prints the actual output.

Usage: uv run --locked python stacks/oxigraph/defects.py
"""
import os
import shutil
import tempfile
from pathlib import Path

from checks import run_check
from loader import load_vault

VAULT = Path(__file__).resolve().parents[2] / "vault"

DEFECTS = [
    ("1. missing required field", "Anonymity.md",
     lambda t: t.replace("description: Participants must not be identifiable from the records.\n", "")),
    ("2. relation endpoint of the wrong class", "Facilitators hold Anonymity.md",
     lambda t: t.replace('concern: "[[Anonymity]]"', 'concern: "[[Technologists]]"')),
    ("3. link to a missing page", "Facilitators hold Anonymity.md",
     lambda t: t.replace('concern: "[[Anonymity]]"', 'concern: "[[Anonymty]]"')),
]

for title, fname, edit in DEFECTS:
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)  # so messages show short relative paths
        d = Path("vault")
        shutil.copytree(VAULT, d)
        p = d / fname
        old = p.read_text()
        new = edit(old)
        assert new != old, f"defect did not change {fname}"
        p.write_text(new)
        store, *_ = load_vault(d)
        print(f"== Defect {title} (file {fname}) ==")
        for m in run_check(store, "full"):
            print(m)
        print()
