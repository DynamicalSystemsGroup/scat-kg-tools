"""R-13 mechanism: pydantic models built at import time from placeholder-tbox.ttl.

The TBox is the single source. Nothing here lists a class, field or status by hand, so a TBox
change shows up in the models on the next import. Pass `tbox=` to build from another file.

Usage: uv run --locked python r13/models.py [vault-dir]   (validates every page)
"""
import re
import sys
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, create_model
from rdflib import OWL, RDF, RDFS, Graph, Namespace

SP = Namespace("https://example.org/scpt-spike#")
SPIKE = Path(__file__).resolve().parent.parent
TBOX = SPIKE / "placeholder-tbox.ttl"
WIKILINK_ONLY = r"^\[\[[^\]|#]+?(#[^\]|]*)?(\|[^\]]*)?\]\]$"


def _local(uri):
    return str(uri).removeprefix(str(SP))


def load(tbox=TBOX):
    """Return (models by class name, status values in rank order, link ranges).

    link ranges: {class name: {field: range class name}} from the ObjectProperty
    domain/range, matched to fields by the property's rdfs:label.
    """
    g = Graph().parse(tbox)
    statuses = [_local(s) for s in sorted(g.subjects(RDF.type, SP.Status),
                                          key=lambda s: int(g.value(s, SP.rank)))]
    Status = Literal[tuple(statuses)]  # type: ignore[valid-type]

    ranges = {}
    for p in g.subjects(RDF.type, OWL.ObjectProperty):
        dom, rng = g.value(p, RDFS.domain), g.value(p, RDFS.range)
        if dom is not None and rng is not None:
            ranges.setdefault(_local(dom), {})[str(g.value(p, RDFS.label))] = _local(rng)

    models = {}
    for cls in g.subjects(RDF.type, SP.Class):
        if cls == SP.Class:
            continue
        name = _local(cls)
        fields = {"type": (Literal[name], ...), "name": (str, ...), "status": (Status, ...)}
        for key in sorted(map(str, g.objects(cls, SP.requiredField))):
            fields[key] = (_field_type(key, name, ranges), ...)
        for key in sorted(map(str, g.objects(cls, SP.optionalField))):
            fields[key] = (_field_type(key, name, ranges) | None, None)
        models[name] = create_model(name, __config__=ConfigDict(extra="forbid"), **fields)
    return models, statuses, ranges


def _field_type(key, cls, ranges):
    if key in ranges.get(cls, {}):
        return Annotated[str, Field(pattern=WIKILINK_ONLY)]
    return str


MODELS, STATUSES, LINK_RANGES = load()


def link_target(value):
    return re.match(r"\[\[([^\]|#]+)", value).group(1).strip()


def validate_vault(vault_dir, models=None, link_ranges=None):
    """Validate every page; return a list of error strings (empty = all pass).

    Also checks each link field points at a page whose type is the property's range class.
    """
    sys.path.insert(0, str(SPIKE))
    from common import parse_vault

    models, link_ranges = models or MODELS, link_ranges or LINK_RANGES
    pages = parse_vault(vault_dir)
    types = {p["name"]: p["meta"].get("type") for p in pages}
    errors = []
    for p in pages:
        t = p["meta"].get("type")
        if t not in models:
            errors.append(f"{p['name']}: unknown type {t!r}")
            continue
        try:
            m = models[t](**p["meta"])
        except Exception as e:  # pydantic.ValidationError
            errors.append(f"{p['name']}: {e}")
            continue
        for field, want in link_ranges.get(t, {}).items():
            tgt = link_target(getattr(m, field))
            if types.get(tgt) != want:
                errors.append(f"{p['name']}: {field} -> {tgt!r} is {types.get(tgt)!r}, want {want}")
    return errors


if __name__ == "__main__":
    vault = sys.argv[1] if len(sys.argv) > 1 else SPIKE / "vault"
    errs = validate_vault(vault)
    n = len(list(Path(vault).glob("*.md")))
    print(f"classes={sorted(MODELS)} statuses={STATUSES}")
    print(f"pages={n} failed={len(errs)}")
    print(*errs, sep="\n")
    sys.exit(1 if errs else 0)
