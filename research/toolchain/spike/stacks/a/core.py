"""Stack A: markdown+frontmatter+wikilink parser -> pyoxigraph store; rules are SPARQL queries.

Throwaway spike code. Scopes: page, neighborhood (page + pages one link away, either direction),
full. Each check loads only the pages it needs, then runs the rule queries restricted to the
subject pages of the scope.
"""

import difflib
import re
from pathlib import Path

import frontmatter
import pyoxigraph as ox

SPIKE = Path(__file__).resolve().parents[2]
TBOX = SPIKE / "placeholder-tbox.ttl"
S = "https://example.org/scat-placeholder#"
V = "https://example.org/scat-vault/"
TYPE_CLASS = {
    "stakeholder-group": "StakeholderGroup",
    "concern": "Concern",
    "affordance": "Affordance",
    "technology": "Technology",
    "scenario-raw": "RawScenario",
    "scenario-coded": "CodedScenario",
    "architecture-raw": "RawArchitecture",
    "architecture-coded": "CodedArchitecture",
}
WIKI = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
PREFIX = (
    f"PREFIX scat: <{S}>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
    "PREFIX owl: <http://www.w3.org/2002/07/owl#>\n"
)


def node(stem):
    return ox.NamedNode(V + stem)


def stem_of(iri):
    return iri.removeprefix(V)


def scan_links(text):
    return [m.strip() for m in WIKI.findall(text)]


def parse_page(path):
    """-> (stem, file, fields: {name: str}, edges: [(field, target stem)]); body links as 'body'."""
    post = frontmatter.load(path)
    fields, edges = {}, []
    for k, v in post.metadata.items():
        if isinstance(v, list):
            edges += [(k, t) for item in v for t in scan_links(str(item))]
        elif v is not None:
            fields[k] = str(v)
    edges += [("body", t) for t in scan_links(post.content)]
    return path.stem, path.name, fields, edges


def add_page(store, parsed):
    stem, fname, fields, edges = parsed
    s = node(stem)
    q = [ox.Quad(s, ox.NamedNode(S + "file"), ox.Literal(fname))]
    for k, v in fields.items():
        if k == "type" and v in TYPE_CLASS:
            q.append(ox.Quad(s, ox.NamedNode(RDF_TYPE), ox.NamedNode(S + TYPE_CLASS[v])))
        q.append(ox.Quad(s, ox.NamedNode(S + k), ox.Literal(v)))
    for k, t in edges:
        q.append(ox.Quad(s, ox.NamedNode(S + ("mentions" if k == "body" else k)), node(t)))
        q.append(ox.Quad(s, ox.NamedNode(S + "linksTo"), node(t)))
    store.extend(q)


RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

# ---- rules: each is (id, SPARQL). #SCOPE# is replaced by a VALUES clause on ?s (or nothing).
RULES = {
    "SCAT-REQ-FIELD": """SELECT ?s ?file ?field WHERE {
  #SCOPE# ?s scat:file ?file .
  VALUES (?field ?pred) { ("type" scat:type) ("status" scat:status) ("title" scat:title) }
  FILTER NOT EXISTS { ?s ?pred ?v } }""",
    "SCAT-DONE-DESCRIPTION": """SELECT ?s ?file WHERE {
  #SCOPE# ?s scat:file ?file ; scat:status "done" . FILTER NOT EXISTS { ?s scat:description ?d } }""",
    "SCAT-DONE-LINK": """SELECT ?s ?file ?link ?c WHERE {
  #SCOPE# ?s scat:file ?file ; scat:status "done" ; a ?c . ?c scat:requiresLink ?link .
  FILTER NOT EXISTS { ?s ?link ?o } }""",
    "SCAT-LINK-DANGLING": """SELECT ?s ?file ?p ?o WHERE {
  #SCOPE# ?s scat:file ?file ; ?p ?o . ?p a owl:ObjectProperty .
  FILTER NOT EXISTS { ?o scat:file ?f } }""",
    "SCAT-LINK-ENDPOINT": """SELECT ?s ?file ?p ?o ?range ?oc WHERE {
  #SCOPE# ?s scat:file ?file ; ?p ?o . ?p rdfs:range ?range . ?o scat:file ?f .
  OPTIONAL { ?o a ?oc } FILTER NOT EXISTS { ?o a ?range } }""",
    "SCAT-LINK-DOMAIN": """SELECT ?s ?file ?p ?domain ?sc WHERE {
  #SCOPE# ?s scat:file ?file ; ?p ?o . ?p rdfs:domain ?domain .
  OPTIONAL { ?s a ?sc } FILTER NOT EXISTS { ?s a ?domain } }""",
}


def loc(iri):
    return iri.value.rsplit("#", 1)[-1].rsplit("/", 1)[-1]


def new_store():
    st = ox.Store()
    st.load(TBOX.read_bytes(), format=ox.RdfFormat.TURTLE)
    st.add(
        ox.Quad(
            ox.NamedNode(S + "mentions"),
            ox.NamedNode(RDF_TYPE),
            ox.NamedNode("http://www.w3.org/2002/07/owl#ObjectProperty"),
        )
    )
    return st


def run_rules(store, subjects=None):
    """-> list of (rule id, row dict). subjects: iterable of stems, or None for all pages."""
    scope = ""
    if subjects is not None:
        scope = "VALUES ?s { " + " ".join(f"<{V}{x}>" for x in sorted(subjects)) + " }"
    out = []
    for rid, q in RULES.items():
        res = store.query(PREFIX + q.replace("#SCOPE#", scope))
        for sol in res:
            row = {v.value: sol[v] for v in res.variables if sol[v] is not None}
            out.append((rid, row))
    return out


def link_index(vault):
    """Cheap pass over all files: stem -> set of stems it links to (frontmatter or body)."""
    return {p.stem: set(scan_links(p.read_text(encoding="utf-8"))) for p in vault.glob("*.md")}


def load(vault, stems):
    st = new_store()
    for stem in sorted(stems):
        f = vault / f"{stem}.md"
        if f.exists():
            add_page(st, parse_page(f))
    return st


def check(vault, scope="full", page=None):
    """scope: 'page' | 'neighborhood' | 'full'. Returns (store, findings)."""
    vault = Path(vault)
    if scope == "full":
        stems = [p.stem for p in vault.glob("*.md")]
        st = load(vault, stems)
        return st, run_rules(st)
    index = link_index(vault)
    out = index.get(page, set())
    if scope == "page":
        subj = {page}
    else:
        subj = {page} | out | {s for s, ts in index.items() if page in ts}
    needed = set(subj)
    for s in subj:
        needed |= index.get(s, set())
    st = load(vault, needed)
    return st, run_rules(st, subj)


# ---- messages (R-2): file, field/link, rule id, fix
def stems_of_class(store, cls):
    q = f"{PREFIX} SELECT ?x WHERE {{ ?x a scat:{cls} }}"
    return sorted(stem_of(s["x"].value) for s in store.query(q))


def _single(store, q):
    return sorted({stem_of(s["x"].value) for s in store.query(PREFIX + q)})


def message(store, rid, r, names):
    s = stem_of(r["s"].value)
    f = r["file"].value
    if rid == "SCAT-REQ-FIELD":
        fld = r["field"].value
        return (
            f"{f}: [{rid}] required field `{fld}` is missing (needed at every status); "
            f"fix: add `{fld}: <value>` to the frontmatter of {f} (the value is the author's)"
        )
    if rid == "SCAT-DONE-DESCRIPTION":
        return (
            f"{f}: [{rid}] field `description` is missing on a page with `status: done`; "
            f"fix: either set `status: draft` in {f} (exact), or add "
            f'`description: "<one sentence the author writes>"`'
        )
    if rid == "SCAT-DONE-LINK":
        fld = loc(r["link"])
        q = (
            f"SELECT DISTINCT ?x WHERE {{ <{V}{s}> scat:concerns ?c . ?c scat:addresses ?x }}"
            if fld == "affordances"
            else "SELECT ?x WHERE { ?x scat:file ?none FILTER(false) }"
        )
        cand = _single(store, q)
        hint = (
            (
                "; candidates derived from this page's concerns' `addresses`: "
                + ", ".join(f'`- "[[{c}]]"`' for c in cand)
            )
            if cand
            else ""
        )
        return (
            f"{f}: [{rid}] required link field `{fld}` is missing on a `done` {loc(r['c'])} "
            f"record; fix: add `{fld}:` with at least one wikilink list item{hint}"
        )
    if rid == "SCAT-LINK-DANGLING":
        fld = "body" if loc(r["p"]) == "mentions" else loc(r["p"])
        t = stem_of(r["o"].value)
        near = difflib.get_close_matches(t, names, n=1, cutoff=0.8)
        fix = (
            f"write [[{near[0]}]] (closest existing page) or create {t}.md"
            if near
            else f"create {t}.md, or remove the link; no close page name exists"
        )
        return f"{f}: [{rid}] field `{fld}` links [[{t}]], but no page {t}.md exists; fix: {fix}"
    if rid == "SCAT-LINK-ENDPOINT":
        fld, t = loc(r["p"]), stem_of(r["o"].value)
        want, got = loc(r["range"]), loc(r["oc"]) if "oc" in r else "unknown"
        q = f"SELECT DISTINCT ?x WHERE {{ ?x scat:file ?f ; a <{r['range'].value}> ; ?q <{V}{t}> }}"
        cand = _single(store, q)
        hint = (
            (
                f"; candidates (pages of class {want} that already link [[{t}]]): "
                + ", ".join(f"[[{c}]]" for c in cand)
            )
            if cand
            else ""
        )
        return (
            f"{f}: [{rid}] field `{fld}` links [[{t}]], class {got}; this field needs class {want}; "
            f'fix: replace `- "[[{t}]]"` in `{fld}` with a page of class {want}{hint}'
        )
    dom = loc(r["domain"])
    return (
        f"{f}: [{rid}] field `{loc(r['p'])}` is only allowed on {dom} pages; "
        f"fix: remove `{loc(r['p'])}` from {f}"
    )


def messages(store, findings, vault):
    names = [p.stem for p in Path(vault).glob("*.md")]
    out = []
    for rid, r in findings:
        out.append(message(store, rid, r, names))
    return out
