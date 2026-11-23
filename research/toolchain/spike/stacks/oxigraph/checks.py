"""Stack A checks: three rules as SPARQL queries, three scopes. Messages follow R-2:
file, field (or link), rule id, exact fix.

Usage: uv run --locked python stacks/oxigraph/checks.py <vault-dir> [local|neighborhood|full] [page name]
"""
import sys
from urllib.parse import unquote

import pyoxigraph as ox

from loader import BASE, SP, load_vault, page_iri

PFX = f"PREFIX sp: <{SP}>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"

# Scope = a pattern that binds ?page to the pages whose rules are evaluated.
def scope_clause(scope, name):
    if scope == "full":
        return "?page sp:file ?file ."
    iri = page_iri(name).value
    if scope == "local":
        return f"VALUES ?page {{ <{iri}> }} ?page sp:file ?file ."
    if scope == "neighborhood":  # page + pages it links to + pages linking to it (one hop each way)
        return (f"{{ SELECT DISTINCT ?page WHERE {{ {{ BIND(<{iri}> AS ?page) }} "
                f"UNION {{ <{iri}> sp:linksTo ?page }} UNION {{ ?page sp:linksTo <{iri}> }} }} }} "
                f"?page sp:file ?file .")
    raise ValueError(scope)


RULE_FIELD = "SPK-FIELD-REQUIRED"
RULE_CLASS = "SPK-ENDPOINT-CLASS"
RULE_LINK = "SPK-LINK-MISSING"

Q_FIELD = """SELECT ?file ?cname ?field WHERE {
  %s ?page a ?cls . ?cls sp:requiredField ?field .
  FILTER NOT EXISTS { ?page sp:hasField ?field }
  BIND(STRAFTER(STR(?cls), "#") AS ?cname) }"""

Q_CLASS = """SELECT ?file ?cname ?field ?target ?rname WHERE {
  %s ?page a ?cls . ?page ?p ?target . ?p rdfs:domain ?cls ; rdfs:range ?range ; rdfs:label ?field .
  ?target sp:file ?tfile .
  FILTER NOT EXISTS { ?target a ?range }
  BIND(STRAFTER(STR(?cls), "#") AS ?cname) BIND(STRAFTER(STR(?range), "#") AS ?rname) }"""

Q_LINK = """SELECT ?file ?target ?field ?rname WHERE {
  %s ?page sp:linksTo ?target .
  FILTER NOT EXISTS { ?target sp:file ?x }
  OPTIONAL { ?page ?p ?target . ?p rdfs:label ?field ; rdfs:range ?range . BIND(STRAFTER(STR(?range), "#") AS ?rname) } }"""


def _name(iri_node):
    return unquote(iri_node.value[len(BASE):])


def _example(store, cname):
    for r in store.query(PFX + f"SELECT ?n WHERE {{ ?t a sp:{cname} ; sp:pageName ?n }} ORDER BY ?n LIMIT 1"):
        return r["n"].value
    return "<name>"


def run_check(store, scope="full", name=None):
    """Return a sorted list of message strings (empty = clean)."""
    sc = scope_clause(scope, name)
    out = []
    for r in store.query(PFX + Q_FIELD % sc):
        f, c, k = r["file"].value, r["cname"].value, r["field"].value
        out.append((f, 0, k, f"{f}: field '{k}': [{RULE_FIELD}] class {c} requires field '{k}' and it is missing or empty. "
                   f"Fix: in the frontmatter of {f} add the line `{k}: <text>` (replace <text> with the value)."))
    for r in store.query(PFX + Q_CLASS % sc):
        f, c, k, t, rc = (r["file"].value, r["cname"].value, r["field"].value, _name(r["target"]), r["rname"].value)
        ex = _example(store, rc)
        out.append((f, 1, k, f"{f}: field '{k}': [{RULE_CLASS}] '[[{t}]]' is not a {rc}, but field '{k}' of class {c} must link a {rc}. "
                   f"Fix: in the frontmatter of {f} change the line to `{k}: \"[[{ex}]]\"` (any existing {rc} page works; "
                   f"'{ex}' is one), or change the type of '{t}' to {rc}."))
    for r in store.query(PFX + Q_LINK % sc):
        f, t = r["file"].value, _name(r["target"])
        k = r["field"].value if r["field"] else None
        rc = r["rname"].value if r["rname"] else None
        where = f"field '{k}'" if k else "body link"
        cls = rc or "<Class>"
        d = f.rsplit("/", 1)[0] if "/" in f else "."
        fix = (f"Fix: run `printf '---\\ntype: {cls}\\nname: {t}\\nstatus: stub\\n---\\n' > \"{d}/{t}.md\"` "
               f"to create the page, or edit [[{t}]] in {f} to the name of an existing page.")
        out.append((f, 2, k or "", f"{f}: {where}: [{RULE_LINK}] link [[{t}]] points to no page named '{t}'. {fix}"))
    return [m for *_, m in sorted(out)]


if __name__ == "__main__":
    vault = sys.argv[1]
    scope = sys.argv[2] if len(sys.argv) > 2 else "full"
    st, *_ = load_vault(vault)
    msgs = run_check(st, scope, sys.argv[3] if len(sys.argv) > 3 else None)
    print("\n".join(msgs) if msgs else "OK: no violations")
    sys.exit(1 if msgs else 0)
