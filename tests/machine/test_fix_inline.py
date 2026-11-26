"""WP11-U5b: the one-line fix is a rendering flag on typed options, not a verbatim text."""

import importlib.util
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from scat_kg.checks import check_vault, fixes
from scat_kg.contract import SCHEMA_VERSION
from scat_kg.fix import Fix

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "seed_helpers", ROOT / "tests" / "checks" / "helpers.py"
)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)
VALIDATOR = Draft202012Validator(
    json.loads((ROOT / "contracts" / "machine-interface.schema.json").read_text(encoding="utf-8"))
)

STATUSES = (("stub", "just started"), ("draft", "being written"), ("done", "finished"))


def opts(n):
    return [
        fixes.option("exact", f"`status: {s}` ({why})", fixes.set_field("c.md", "status", s))
        for s, why in STATUSES[:n]
    ]


@pytest.mark.parametrize("n", [1, 2, 3])
def test_inline_render_is_the_old_single_line(n):
    old = "Fix, choose one: " + ", ".join(f"`status: {s}` ({why})" for s, why in STATUSES[:n])
    fix = fixes.inline(opts(n))
    assert fix.verbatim is None
    assert fix.render() == old


def test_inline_head_is_used():
    assert fixes.inline(opts(2), head="Pick:").render().startswith("Pick: `status: stub`")


def check_doc(p):
    d = {
        "schema_version": SCHEMA_VERSION,
        "kind": "check",
        "operation": "check",
        "ok": p.severity != "error",
        "mode": "disallowed",
        "problems": [p.to_dict()],
    }
    assert VALIDATOR.is_valid(d), [e.message for e in VALIDATOR.iter_errors(d)]


def status_problems(make_vault):
    v = H.vault(
        make_vault, {"concern/safe-handling.md": H.doc("concern", "S", status="finished")}, ()
    )
    return [p for p in check_vault(v).problems if p.rule == "SCAT-FM-STATUS"]


def test_the_flag_is_not_data(make_vault):
    d = fixes.inline(opts(3)).to_dict()
    assert "inline" not in d
    assert d == Fix("options", tuple(opts(3)), "Fix, choose one:").to_dict()
    found = status_problems(make_vault)
    assert found
    for p in found:
        assert "inline" not in p.to_dict()["fix"]
        check_doc(p)


def test_status_no_near_match_problems_are_not_verbatim(make_vault):
    found = status_problems(make_vault)
    assert found
    for p in found:
        assert p.fix_data.verbatim is None
        assert p.fix_data.inline is True
        assert p.fix_data.render().startswith("Fix, choose one: `status: stub` (just started)")
