"""Every view document and every export result validates against the machine-interface schema."""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from viewutil import narrative, page, row

import scat_tools

SCHEMA = json.loads(
    (Path(__file__).resolve().parents[2] / "contracts" / "machine-interface.schema.json").read_text(
        encoding="utf-8"
    )
)
VALIDATOR = Draft202012Validator(SCHEMA)

VIEWS = {
    "fingerprint-all": lambda r: scat_tools.fingerprint(root=r),
    "fingerprint-one": lambda r: scat_tools.fingerprint("dry", root=r),
    "fingerprint-empty": lambda r: scat_tools.fingerprint("empty", root=r),
    "fingerprint-candidates": lambda r: scat_tools.fingerprint("dry", candidates=True, root=r),
    "fingerprint-all-candidates": lambda r: scat_tools.fingerprint(candidates=True, root=r),
    "edges-holds": lambda r: scat_tools.edge_table("holds", root=r),
    "edges-addressed-by": lambda r: scat_tools.edge_table("addressed-by", root=r),
    "edges-provided-by": lambda r: scat_tools.edge_table("provided-by", root=r),
    "layered-all": lambda r: scat_tools.layered(root=r),
    "layered-some": lambda r: scat_tools.layered(["dry", "split"], root=r),
    "layered-candidates": lambda r: scat_tools.layered(candidates=True, root=r),
    "layered-some-candidates": lambda r: scat_tools.layered(
        ["dry", "split"], candidates=True, root=r
    ),
    "layered-none-named": lambda r: scat_tools.layered([], root=r),
    "trace-both": lambda r: scat_tools.trace("farmers", root=r),
    "trace-up": lambda r: scat_tools.trace("probe", "up", root=r),
    "trace-down": lambda r: scat_tools.trace("water", "down", root=r),
    "trace-idle": lambda r: scat_tools.trace("idle", root=r),
}
REFUSALS = {
    "unknown-narrative": lambda r: scat_tools.fingerprint("nope", root=r),
    "unknown-node": lambda r: scat_tools.trace("nope", root=r),
    "unknown-type": lambda r: scat_tools.edge_table("loves", root=r),
    "unknown-direction": lambda r: scat_tools.trace("farmers", "sideways", root=r),
    "layered-unknown": lambda r: scat_tools.layered(["nope"], root=r),
    "missing-folder": lambda r: scat_tools.fingerprint(root=r / "gone"),
}


def errors(doc):
    return [f"{'/'.join(map(str, e.path))}: {e.message}" for e in VALIDATOR.iter_errors(doc)]


@pytest.mark.parametrize("name", VIEWS)
def test_a_view_validates(vault, name):
    view = VIEWS[name](vault)
    assert view.ok
    assert errors(view.to_dict()) == []
    assert view.to_dict()["kind"] == "view"


@pytest.mark.parametrize("name", REFUSALS)
def test_a_view_refusal_validates(vault, name):
    r = REFUSALS[name](vault)
    assert not r.ok
    assert errors(r.to_dict()) == []
    assert r.to_dict()["kind"] == "operation"


def test_a_refusal_with_problems_validates(make):
    root = make({"concern/water.md": page("concern", "W", "bogus")})
    r = scat_tools.edge_table("holds", root=root)
    d = r.to_dict()
    assert d["problems"] and errors(d) == []
    r = scat_tools.export_edges(root / "t", root=root)
    d = r.to_dict()
    assert d["problems"] and errors(d) == []


def test_export_results_validate_outside_and_inside_the_vault(vault, tmp_path):
    for out in (tmp_path / "out", vault / "tables"):
        r = scat_tools.export_edges(out, root=vault)
        assert r.created and errors(r.to_dict()) == [], out
        again = scat_tools.export_edges(out, root=vault)  # unchanged this time
        assert again.unchanged and errors(again.to_dict()) == []


def test_export_refusals_validate(vault, tmp_path):
    f = tmp_path / "file"
    f.write_text("x", encoding="utf-8")
    assert errors(scat_tools.export_edges(f, root=vault).to_dict()) == []
    assert errors(scat_tools.export_edges(tmp_path / "o", root=tmp_path / "gone").to_dict()) == []


def test_the_other_operations_still_demand_vault_paths():
    doc = scat_tools.index(root="/nonexistent-vault").to_dict()
    assert errors(doc) == []
    bad = {**doc, "created": ["/abs/path.md"]}
    assert errors(bad) != []
    export = {**doc, "operation": "export-edges", "created": ["/abs/tables/holds.csv"]}
    assert errors(export) == []


def test_a_view_document_missing_its_fields_is_rejected(vault):
    d = scat_tools.trace("farmers", root=vault).to_dict()
    del d["up"]
    assert errors(d) != []
    d = scat_tools.edge_table("holds", root=vault).to_dict()
    del d["rows"]
    assert errors(d) != []
    d = scat_tools.layered(root=vault).to_dict()
    d["nodes"] = [d["nodes"]]
    assert errors(d) != []


def test_a_view_is_not_an_operation_document_and_unknown_fields_are_allowed(vault):
    d = scat_tools.fingerprint("dry", root=vault).to_dict()
    d["extra"] = 1
    d["narratives"][0]["extra"] = 1
    assert errors(d) == []


BARE = narrative(
    "Bare", "", [row("holds", "farmers", "water"), row("addressed-by", "water", "alert")]
)


def test_the_new_keys_validate_and_are_checked(make):
    root = make({"narrative/bare.md": BARE})
    lay = scat_tools.layered(candidates=True, root=root).to_dict()
    assert {"orphans", "candidates", "no_account"} <= set(lay) and lay["no_account"] == ["bare"]
    assert errors(lay) == []
    fp = scat_tools.fingerprint("bare", candidates=True, root=root).to_dict()
    assert fp["narratives"][0]["no_account"] is True and errors(fp) == []
    # wrong shapes are rejected
    assert errors({**lay, "orphans": [{"name": "x"}]}) != []
    assert errors({**lay, "candidates": [{**lay["candidates"][0], "narrative": ""}]}) != []
    assert errors({**lay, "candidates": [{"type": "holds", "from": "a", "to": "b"}]}) != []
    assert errors({**lay, "no_account": "bare"}) != []
    bad = {**fp, "narratives": [{**fp["narratives"][0], "no_account": False}]}
    assert errors(bad) != []
