"""R-13 mechanism: the pydantic models of stack C are HELD EQUAL to the placeholder TBox.

The TBox (placeholder-tbox.ttl) is authoritative. `tbox_facts` reads the facts the models must
mirror; `model_facts` reads the same facts off the models; `differences` lists every mismatch.
Compared: the set of page classes, the set of link properties, each property's range and domain,
and which links each class requires. Not in the TBox (so not compared): `type` slugs,
`description`, status values, which classes have link fields at all beyond domains.
"""

import os
from pathlib import Path

from rdflib import OWL, RDF, RDFS, Graph, Namespace

from stacks.c.models import MODELS

SCAT = Namespace("https://example.org/scat-placeholder#")
DEFAULT_TBOX = Path(__file__).resolve().parent.parent / "placeholder-tbox.ttl"
# classes in the TBox that are not page types
NOT_PAGE_TYPES = {"Record", "Status"}


def tbox_path():
    """The TBox under test: $SCAT_TBOX if set (a scratch copy), else the placeholder."""
    return Path(os.environ.get("SCAT_TBOX") or DEFAULT_TBOX)


def _local(uri):
    return str(uri).split("#")[-1]


def tbox_facts(path):
    g = Graph().parse(path, format="turtle")
    props = {_local(p) for p in g.subjects(RDF.type, OWL.ObjectProperty)}
    return {
        "classes": {_local(c) for c in g.subjects(RDF.type, OWL.Class)} - NOT_PAGE_TYPES,
        "properties": props,
        "range": {_local(p): _local(o) for p, o in g.subject_objects(RDFS.range)},
        "domain": {_local(p): _local(o) for p, o in g.subject_objects(RDFS.domain)},
        "requires": _group((_local(c), _local(p)) for c, p in g.subject_objects(SCAT.requiresLink)),
    }


def _group(pairs):
    out = {}
    for k, v in pairs:
        out.setdefault(k, set()).add(v)
    return out


def model_facts():
    props, rng, owners, requires = set(), {}, {}, {}
    for m in MODELS.values():
        for f, target in m.LINKS.items():
            props.add(f)
            rng.setdefault(f, set()).add(target)
            owners.setdefault(f, set()).add(m.CLASS)
        if m.REQUIRED_LINKS:
            requires[m.CLASS] = set(m.REQUIRED_LINKS)
    return {
        "classes": {m.CLASS for m in MODELS.values()},
        "properties": props,
        "range": rng,
        "owners": owners,
        "requires": requires,
    }


def differences(path=None):
    """Every way the models disagree with the TBox at `path`; empty list means held equal."""
    t, m = tbox_facts(path or tbox_path()), model_facts()
    d = []
    for c in sorted(t["classes"] - m["classes"]):
        d.append(
            f"TBox class {c} has no model: add a model with CLASS = {c!r} in stacks/c/models.py"
        )
    for c in sorted(m["classes"] - t["classes"]):
        d.append(
            f"model for class {c} is not a class in the TBox: remove it or add {c} to the TBox"
        )
    for p in sorted(t["properties"] - m["properties"]):
        d.append(f"TBox property {p} is not a link field of any model: add it to a model's LINKS")
    for p in sorted(m["properties"] - t["properties"]):
        d.append(f"link field {p} is not an ObjectProperty in the TBox")
    for p, want in sorted(t["range"].items()):
        got = m["range"].get(p)
        if got is not None and got != {want}:
            d.append(f"property {p}: TBox range is {want}, models target {sorted(got)}")
    for p, want in sorted(t["domain"].items()):
        got = m["owners"].get(p)
        if got is not None and got != {want}:
            d.append(f"property {p}: TBox domain is {want}, models declare it on {sorted(got)}")
    for c in sorted(set(t["requires"]) | set(m["requires"])):
        want, got = t["requires"].get(c, set()), m["requires"].get(c, set())
        if want != got:
            d.append(
                f"class {c}: TBox requiresLink {sorted(want)}, models REQUIRED_LINKS {sorted(got)}"
            )
    return d
