"""R-13 tests: models agree with the TBox; a TBox change propagates (on a temp copy only)."""
import shutil
import sys
from pathlib import Path

import pytest
from rdflib import RDF, Graph

sys.path.insert(0, str(Path(__file__).resolve().parent))
import models  # noqa: E402

SPIKE = models.SPIKE
VAULT = SPIKE / "vault"
CONVENTION = {"type", "name", "status"}  # required on every model; not in the TBox field lists
CLASSES = {"StakeholderGroup", "Concern", "Affordance", "Technology", "Heldby", "Addresses", "Attributes"}


def tbox_fields(path):
    """Independent read of the TBox: {class: (required, optional)} by SPARQL, not by models.py."""
    g = Graph().parse(path)
    out = {}
    for row in g.query("""PREFIX sp: <https://example.org/scpt-spike#>
        SELECT ?c ?r ?o WHERE { ?c a sp:Class . FILTER(?c != sp:Class)
          OPTIONAL { ?c sp:requiredField ?r } OPTIONAL { ?c sp:optionalField ?o } }"""):
        req, opt = out.setdefault(str(row.c).split("#")[1], (set(), set()))
        if row.r: req.add(str(row.r))
        if row.o: opt.add(str(row.o))
    return {c: (r - CONVENTION, o) for c, (r, o) in out.items()}


def model_fields(ms):
    return {n: ({k for k, f in m.model_fields.items() if f.is_required()} - CONVENTION,
                {k for k, f in m.model_fields.items() if not f.is_required()})
            for n, m in ms.items()}


def test_seven_classes():
    assert set(models.MODELS) == CLASSES


def test_models_agree_with_tbox():
    assert model_fields(models.MODELS) == tbox_fields(models.TBOX)


def test_status_values_and_order():
    assert models.STATUSES == ["stub", "draft", "done"]
    with pytest.raises(Exception):
        models.MODELS["Concern"](type="Concern", name="x", status="finished", description="d")


def test_required_missing_and_unknown_field_rejected():
    with pytest.raises(Exception):
        models.MODELS["Concern"](type="Concern", name="x", status="stub")  # no description
    with pytest.raises(Exception):
        models.MODELS["Concern"](type="Concern", name="x", status="stub", description="d", bogus=1)


def test_mini_vault_validates():
    assert models.validate_vault(VAULT) == []


def test_bad_link_target_class_is_caught(tmp_path):
    shutil.copytree(VAULT, tmp_path / "v")
    page = tmp_path / "v" / "Anonymity addressed by Pseudonymous records.md"
    page.write_text(page.read_text().replace('concern: "[[Anonymity]]"', 'concern: "[[Oxigraph]]"'))
    errs = models.validate_vault(tmp_path / "v")
    assert len(errs) == 1 and "want Concern" in errs[0]


def test_tbox_change_shows_up_in_models(tmp_path):
    """Drift demo on a temporary copy: add an optional field and a status to the TBox."""
    tmp = tmp_path / "tbox.ttl"
    shutil.copy(models.TBOX, tmp)
    text = tmp.read_text()
    text = text.replace('sp:optionalField "category" .', 'sp:optionalField "category", "severity" .')
    text += '\nsp:review a sp:Status ; sp:rank 3 .\n'
    tmp.write_text(text)
    changed, statuses, _ = models.load(tmp)
    assert "severity" in changed["Concern"].model_fields
    assert "severity" not in models.MODELS["Concern"].model_fields  # real TBox untouched
    assert statuses == ["stub", "draft", "done", "review"]
    assert model_fields(changed) == tbox_fields(tmp)
