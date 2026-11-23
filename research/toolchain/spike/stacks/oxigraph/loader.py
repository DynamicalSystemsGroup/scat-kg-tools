"""Stack A loader: vault -> RDF in a pyoxigraph Store, using the placeholder TBox terms.

Graph shape (default graph, TBox and ABox together):
  page IRI  rdf:type sp:<Class>        (only when frontmatter `type` names a TBox class)
            sp:file "<path>"           (exists only for pages that exist; link targets without it are missing)
            sp:pageName "<name>"
            sp:hasField "<key>"        (one per non-empty frontmatter key)
            sp:linksTo <target IRI>    (every wikilink, frontmatter or body; target may be missing)
            <sp:objectProperty> <target>   (relation endpoint, chosen by (class, key) from the TBox)
"""
import sys
import time
from pathlib import Path
from urllib.parse import quote

import pyoxigraph as ox

SPIKE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SPIKE))
from common import WIKILINK, _strings, parse_vault  # noqa: E402

SP = "https://example.org/scpt-spike#"
BASE = "https://example.org/scpt-vault/"
TBOX = SPIKE / "placeholder-tbox.ttl"
RDF_TYPE = ox.NamedNode("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")


def sp(name):
    return ox.NamedNode(SP + name)


def page_iri(name):
    return ox.NamedNode(BASE + quote(name))


def parse(vault_dir):
    return parse_vault(vault_dir)


def build_store(pages, tbox=TBOX):
    store = ox.Store()
    store.load(path=str(tbox), format=ox.RdfFormat.TURTLE)
    # (class local name, key) -> object property, read from the TBox itself
    props = {}
    for row in store.query(
        f"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?p ?l ?d WHERE "
        f"{{ ?p a <http://www.w3.org/2002/07/owl#ObjectProperty> ; rdfs:label ?l ; rdfs:domain ?d }}"
    ):
        props[(row["d"].value[len(SP):], row["l"].value)] = row["p"]
    classes = {r["c"].value[len(SP):] for r in store.query(f"SELECT ?c WHERE {{ ?c a <{SP}Class> }}")}
    quads = []

    def add(s, p, o):
        quads.append(ox.Quad(s, p, o, ox.DefaultGraph()))

    for pg in pages:
        s = page_iri(pg["name"])
        cls = str(pg["meta"].get("type", ""))
        if cls in classes:
            add(s, RDF_TYPE, sp(cls))
        add(s, sp("file"), ox.Literal(pg["path"]))
        add(s, sp("pageName"), ox.Literal(pg["name"]))
        for key, val in pg["meta"].items():
            if val is None or val == "" or val == []:
                continue
            add(s, sp("hasField"), ox.Literal(key))
            prop = props.get((cls, key))
            if prop is not None:
                for target in (m.strip() for v in _strings(val) for m in WIKILINK.findall(v)):
                    add(s, prop, page_iri(target))
        for target in pg["links"]:
            add(s, sp("linksTo"), page_iri(target))
    store.bulk_extend(quads)
    return store


def load_vault(vault_dir):
    """Return (store, parse_seconds, build_seconds)."""
    t0 = time.perf_counter()
    pages = parse(vault_dir)
    t1 = time.perf_counter()
    store = build_store(pages)
    t2 = time.perf_counter()
    return store, t1 - t0, t2 - t1


if __name__ == "__main__":
    st, a, b = load_vault(sys.argv[1])
    print(f"quads={len(st)} parse={a:.3f}s build={b:.3f}s")
