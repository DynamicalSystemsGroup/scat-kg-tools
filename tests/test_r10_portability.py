"""WP5-R10: nothing in src/ puts Linux or Windows support at risk.

A grep-style inspection of the source (no shell calls, paths through pathlib, text read and written as
UTF-8) and a behavior check (a vault with CRLF line endings reads and checks the same as with LF). CI on
Linux is the other half of R10 and is not tested here.
"""

import ast
import re
import shutil
from pathlib import Path

import scat_kg
from scat_kg.vault import read_vault

ROOT = Path(__file__).parents[1]
SRC = ROOT / "src" / "scat_kg"
EXAMPLES = ROOT / "contracts" / "examples"
FILES = sorted(SRC.rglob("*.py"))


def imports(tree) -> set[str]:
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    return names


def test__r10__the_source_is_found():
    assert len(FILES) >= 20


def test__r10__no_shell_or_process_calls_in_src():
    process_calls = re.compile(r"(system|popen|exec\w*|spawn\w*|posix_spawn\w*|startfile|fork)$")
    used = {}
    for f in FILES:
        text = f.read_text(encoding="utf-8")
        tree = ast.parse(text)
        bad = imports(tree) & {"subprocess", "pty", "shlex", "pexpect", "sh", "plumbum"}
        for node in ast.walk(tree):
            is_os_attr = isinstance(node, ast.Attribute) and getattr(node.value, "id", "") == "os"
            if is_os_attr and process_calls.match(node.attr):
                bad.add(f"os.{node.attr}")
        if "shell=True" in text.replace(" ", ""):
            bad.add("shell=True")
        if bad:
            used[f.name] = bad
    assert used == {}


def test__r10__paths_come_from_pathlib_not_os_path():
    offenders = []
    for f in FILES:
        text = f.read_text(encoding="utf-8")
        for node in ast.walk(ast.parse(text)):
            is_os_path = (
                isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and node.value.id == "os"
                and node.attr == "path"
            )
            if is_os_path:
                offenders.append(f"{f.name}:{node.lineno} os.path")
        names = {n.id for n in ast.walk(ast.parse(text)) if isinstance(n, ast.Name)}
        if "Path" in names and "pathlib" not in imports(ast.parse(text)):
            offenders.append(f"{f.name}: Path without a pathlib import")
    assert offenders == []
    assert "from pathlib import" in (SRC / "vault.py").read_text(encoding="utf-8")


def test__r10__text_is_read_and_written_as_utf8():
    offenders = []
    for f in FILES:
        for node in ast.walk(ast.parse(f.read_text(encoding="utf-8"))):
            if not isinstance(node, ast.Call):
                continue
            keys = {k.arg for k in node.keywords}
            name = getattr(node.func, "attr", getattr(node.func, "id", ""))
            if name in {"read_text", "write_text"} and "encoding" not in keys:
                offenders.append(f"{f.name}:{node.lineno} {name} without encoding")
            if name == "open":
                modes = [a.value for a in node.args[1:2] if isinstance(a, ast.Constant)]
                modes += [k.value.value for k in node.keywords if k.arg == "mode"]
                if not any("b" in m for m in modes) and "encoding" not in keys:
                    offenders.append(f"{f.name}:{node.lineno} text open() without encoding")
    assert offenders == []


def crlf_copy(tmp_path) -> Path:
    root = tmp_path / "crlf"
    shutil.copytree(EXAMPLES, root)
    for p in root.rglob("*.md"):
        p.write_bytes(p.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    return root


def test__r10__a_crlf_vault_reads_and_checks_the_same_as_an_lf_vault(tmp_path):
    crlf = crlf_copy(tmp_path)
    assert b"\r\n" in (crlf / "concern/quick-checkout.md").read_bytes()
    lf_pages = {
        p.path: (p.type, p.fields.get("status"), p.fields.get("title"))
        for p in read_vault(EXAMPLES).pages
    }
    crlf_pages = {
        p.path: (p.type, p.fields.get("status"), p.fields.get("title"))
        for p in read_vault(crlf).pages
    }
    assert crlf_pages == lf_pages
    assert all(p.frontmatter_error is None for p in read_vault(crlf).pages)
    assert str(scat_kg.check(root=crlf)) == str(scat_kg.check(root=EXAMPLES))


def test__r10__index_leaves_a_crlf_vault_unchanged(tmp_path):
    crlf = crlf_copy(tmp_path)
    before = {p: p.read_bytes() for p in crlf.rglob("*.md")}
    result = scat_kg.index(root=crlf)
    assert result.ok
    assert {p: p.read_bytes() for p in crlf.rglob("*.md")} == before
