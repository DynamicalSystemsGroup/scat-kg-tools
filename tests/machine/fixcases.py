"""What every fix-data family test shares: seed a defect in the fixture vault, take the problems of one rule, and hold
each fix to the machine interface.

For every problem of the named rule the fix is typed data (not the legacy wrapper); its kind is the catalogue's or a
named deviation; `field` is set exactly when `where` names a field; its `to_dict()` validates against the schema;
every command parses with `scat` and every command and edit value appears in the text. And the edits themselves are
applied, on a copy of the vault, as the interface says (`replace-text` at its column and guarded by `find`,
`delete-line` guarded by the whole line, `set-field`, `delete-field`, `rename-file`): every option that is exact
(not a slot, not command-only) clears its problem, which is the test that the line, the column and the `find` of an
edit are right.
"""

import re
import shutil
import sys
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "checks"))
import helpers as H
import scat_harness as h

from scat_tools.checks import check_vault
from scat_tools.cli import _parser
from scat_tools.vault import read_vault

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = Draft202012Validator(h.SCHEMA)
CATALOGUE_KIND = h.catalogue_kinds()


def problems_of(make_vault, files, remove, rule):
    v = H.vault(make_vault, files, remove)
    return v, [p for p in check_vault(v).problems if p.rule == rule]


def check_doc(p):
    d = {
        "schema_version": 3,
        "kind": "check",
        "operation": "check",
        "ok": p.severity != "error",
        "mode": "disallowed",
        "problems": [p.to_dict()],
    }
    assert VALIDATOR.is_valid(d), [e.message for e in VALIDATOR.iter_errors(d)]


def assert_matches_text(opt, text):
    if opt.command is not None:
        assert f"`scat {' '.join(opt.command.argv)}`" in text
        _parser().parse_args(list(opt.command.argv))  # scat accepts the command line
        assert opt.command.repl in text
    for e in opt.edits:
        if e.action == "set-field" and e.value is not None:
            v = str(e.value).lower() if isinstance(e.value, bool) else str(e.value)
            for part in v.split(e.author_slot) if e.author_slot else [v]:
                assert part in text, (part, text)
        if e.action == "rename-file":
            assert e.to.rsplit("/", 1)[-1] in text
        if e.action == "replace-text" and e.author_slot:
            assert e.author_slot in e.replace


# applying the edits of a fix, as the machine interface says


def _lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").split("\n")


def apply_edits(root: Path, edits) -> None:
    moved: dict[str, str] = {}

    def at(file: str) -> Path:
        return root / moved.get(file, file)

    for e in edits:
        path = at(e.file)
        if e.action == "rename-file":
            (root / e.to).parent.mkdir(parents=True, exist_ok=True)
            path.rename(root / e.to)
            moved[e.file] = e.to
        elif e.action == "delete-file":
            path.unlink()
        elif e.action == "replace-text":
            lines = _lines(path)
            text = lines[e.line - 1]
            if e.column is None:
                assert e.find in text, (e.find, text)
                new = text.replace(e.find, e.replace)
            else:
                assert text[e.column - 1 : e.column - 1 + len(e.find)] == e.find, (e, text)
                new = text[: e.column - 1] + e.replace + text[e.column - 1 + len(e.find) :]
            lines[e.line - 1 : e.line] = new.split("\n")
            path.write_text("\n".join(lines), encoding="utf-8")
        elif e.action == "delete-line":
            lines = _lines(path)
            assert lines[e.line - 1] == e.find, (e.find, lines[e.line - 1])
            del lines[e.line - 1]
            path.write_text("\n".join(lines), encoding="utf-8")
        elif e.action in ("set-field", "delete-field"):
            _set_field(path, e)
        else:  # pragma: no cover
            raise AssertionError(f"unknown action {e.action}")


def _set_field(path: Path, e) -> None:
    lines = _lines(path)
    if path.suffix == ".md" and e.action == "set-field" and lines[0] != "---":
        lines = ["---", "---", *lines]  # no frontmatter: a block between two `---` lines at the top
    close = lines.index("---", 1) if lines[0] == "---" else None
    key = re.compile(rf"^{re.escape(e.field)}:")
    found = next((i for i, ln in enumerate(lines[: close or 0]) if key.match(ln)), None)
    if e.action == "delete-field":
        del lines[found]
    else:
        value = (
            e.value
            if isinstance(e.value, str)
            else str(e.value).lower()
            if isinstance(e.value, bool)
            else str(e.value)
        )
        plain = re.fullmatch(r"[\w-]+", value) and isinstance(yaml.safe_load(value), str)
        text = f"{e.field}: {value}" if plain else f'{e.field}: "{value}"'
        if path.suffix == ".toml":
            text = f"{e.field} = {value}"
            found = next((i for i, ln in enumerate(lines) if ln.startswith(e.field)), None)
            close = len(lines)
        if found is None:
            lines.insert(close, text)
        else:
            lines[found] = text
    path.write_text("\n".join(lines), encoding="utf-8")


def clears(tmp_path: Path, root: Path, problem, option) -> bool:
    """Whether applying the option's edits on a copy of the vault leaves no problem of the rule at that place."""
    copy = tmp_path / "copy"
    shutil.copytree(root, copy, dirs_exist_ok=True)
    apply_edits(copy, option.edits)
    left = [
        q
        for q in check_vault(read_vault(copy)).problems
        if (q.rule, q.file, q.where) == (problem.rule, problem.file, problem.where)
    ]
    shutil.rmtree(copy)
    return not left


def verify(make_vault, tmp_path, rule, files, remove=(), clearing=True):
    """Hold every problem of `rule` that the seed gives to the machine interface; returns the problems."""
    v, found = problems_of(make_vault, files, remove, rule)
    assert found, f"the seed gave no {rule}"
    for p in found:
        fix = p.fix_data
        assert fix.verbatim is None
        assert (fix.kind == CATALOGUE_KIND[rule]) or (rule, fix.kind) in h.DEVIATIONS, (
            rule,
            fix.kind,
        )
        assert len(fix.options) >= 1 and (fix.kind != "options" or len(fix.options) >= 2)
        for o in fix.options:
            assert o.kind != "manual" or (o.command is None and not o.edits)
            if o.kind == "advisory":
                assert o.command is None and not o.edits
            if o.kind == "exact":
                assert o.command or o.edits
            if o.kind == "slot":
                assert o.command.author_slot if o.command else any(e.author_slot for e in o.edits)
            assert_matches_text(o, p.fix)
            if clearing and o.kind == "exact" and o.edits and not o.command:
                assert clears(tmp_path, v.root, p, o), (
                    f"{rule}: `{o.text}` does not clear its problem"
                )
        assert (p.field is not None) == p.where.startswith("field `")
        if p.field:
            assert p.where == f"field `{p.field}`"
        d = p.to_dict()
        assert d["fix"]["options"] and d["text"] == p.render()
        check_doc(p)
    return found


def family(cases):
    """The parametrize mark and ids for a list of (id, rule, files, remove) cases."""
    return pytest.mark.parametrize("case", cases, ids=[c[0] for c in cases])
