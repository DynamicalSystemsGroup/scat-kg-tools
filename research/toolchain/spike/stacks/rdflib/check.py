"""STACK B: rdflib store; rules in SHACL (shapes generated from the placeholder TBox), run by pyshacl.
Throwaway spike code.

Load phase (`load`): parse every page, build one rdflib Graph (the store) + the shapes graph.
Check phase: local / neighborhood = extract a subgraph from the store (checked pages' triples + type/name stubs of
their link targets), full = validate the store itself; then map pyshacl's raw report to R-2 messages (`to_violations`).

Graph model (not the TBox; check-only vocabulary, namespace sp:):
  page node  PAGE/<name>   sp:pageName "<name>"   sp:pageType sp:<Class>   sp:linksTo <target page node> (every link)
  checked    additionally  rdf:type sp:<Class>, FIELD/<key> "<value>" per plain frontmatter field,
             and the TBox object property (e.g. sp:addressesConcern) -> target page node per endpoint field.
  A link target with no page has no sp:pageName (it is only ever an object).
"""
import difflib
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, unquote

import pyshacl
from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SH

SPIKE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SPIKE))
from common import WIKILINK, parse_vault  # noqa: E402

SP = Namespace("https://example.org/scpt-spike#")
PAGE = Namespace("https://example.org/scpt-spike/page/")
FIELD = Namespace("https://example.org/scpt-spike/field#")
SHP = Namespace("https://example.org/scpt-spike/shape/")
R_FIELD, R_ENDPOINT, R_LINK = "missing-required-field", "wrong-endpoint-class", "broken-link"
LAST_RAW = None  # pyshacl's own text report from the latest full-scope check (for defects.py)


@dataclass(frozen=True)
class Violation:
    file: str
    field: str
    rule: str
    problem: str
    fix: str

    def __str__(self):
        return f'{self.file}: field "{self.field}" [{self.rule}] {self.problem} Fix: {self.fix}'


def art(w):
    return ("an " if w[0] in "AEIOU" else "a ") + w


class Store:
    def __init__(self, vault_dir, tbox=SPIKE / "placeholder-tbox.ttl"):
        self.tbox = Graph().parse(tbox)
        # (class, frontmatter key) -> (object property, range class IRI)
        self.endpoint = {(d, str(self.tbox.value(p, RDFS.label))): (p, self.tbox.value(p, RDFS.range))
                         for p in self.tbox.subjects(RDF.type, OWL.ObjectProperty)
                         for d in self.tbox.objects(p, RDFS.domain)}
        self.classes = set(self.tbox.subjects(SP.requiredField, None))
        self.shapes = build_shapes(self.tbox, self.endpoint, self.classes)
        self.g = Graph()
        for p in parse_vault(vault_dir):
            self.add_page(p)

    def add_page(self, p):
        g, n, meta = self.g, PAGE[quote(p["name"], safe="")], p["meta"]
        cls = SP[meta["type"]] if meta.get("type") else None
        g.add((n, SP.pageName, Literal(p["name"])))
        if cls in self.classes:
            g.add((n, SP.pageType, cls))
            g.add((n, RDF.type, cls))
        for t in p["links"]:
            g.add((n, SP.linksTo, PAGE[quote(t, safe="")]))
        for k, v in meta.items():
            if (cls, k) in self.endpoint:
                m = WIKILINK.search(str(v))
                if m:
                    g.add((n, self.endpoint[(cls, k)][0], PAGE[quote(m.group(1).strip(), safe="")]))
            elif v not in (None, ""):
                g.add((n, FIELD[k], Literal(str(v))))

    def name(self, node):
        return str(self.g.value(node, SP.pageName) or unquote(str(node)[len(PAGE):]))

    def of_class(self, cls_iri, n=3):
        return sorted(str(self.g.value(s, SP.pageName)) for s in self.g.subjects(SP.pageType, cls_iri))[:n]


def build_shapes(tbox, endpoint, classes):
    sh = Graph()
    for cls in classes:
        ns = SHP[str(cls).split("#")[1]]
        sh.add((ns, RDF.type, SH.NodeShape))
        sh.add((ns, SH.targetClass, cls))
        for f in sorted(str(o) for o in tbox.objects(cls, SP.requiredField)):
            ps = URIRef(f"{ns}/{f}")
            sh.add((ns, SH.property, ps))
            sh.add((ps, SH.minCount, Literal(1)))
            if (cls, f) in endpoint:
                prop, rng = endpoint[(cls, f)]
                sh.add((ps, SH.path, prop))
                rs, rp = BNode(), BNode()  # endpoint must be a page whose pageType is the range class
                sh.add((ps, SH.node, rs))
                sh.add((rs, SH.property, rp))
                sh.add((rp, SH.path, SP.pageType))
                sh.add((rp, SH.hasValue, rng))
            else:
                sh.add((ps, SH.path, FIELD[f]))
    ln, lp, ex, ep = SHP["Links"], SHP["Links/linksTo"], BNode(), BNode()
    sh.add((ln, SH.targetSubjectsOf, SP.linksTo))  # every page that links anywhere
    sh.add((ln, SH.property, lp))
    sh.add((lp, SH.path, SP.linksTo))
    sh.add((lp, SH.node, ex))  # each link target must be a page (has sp:pageName)
    sh.add((ex, SH.property, ep))
    sh.add((ep, SH.path, SP.pageName))
    sh.add((ep, SH.minCount, Literal(1)))
    return sh


def load(vault_dir):
    return Store(vault_dir)


def subgraph(st, checked):
    """Copy the checked pages' triples from the store; add pageName/pageType stubs for link targets outside."""
    sub, g = Graph(), st.g
    for n in checked:
        for t in g.triples((n, None, None)):
            sub.add(t)
    for n in checked:
        for o in g.objects(n, SP.linksTo):
            if o not in checked:
                for p in (SP.pageName, SP.pageType):
                    for t in g.triples((o, p, None)):
                        sub.add(t)
    return sub


def validate(st, data):
    global LAST_RAW
    conforms, report, text = pyshacl.validate(data, shacl_graph=st.shapes, inference="none", advanced=False)
    LAST_RAW = None if conforms else text
    return report


def to_violations(st, report):
    """pyshacl raw report graph -> R-2 messages. This function is the whole mapping layer."""
    out, label = set(), lambda p: str(st.tbox.value(p, RDFS.label) or str(p).split("#")[-1])
    nested = set(report.objects(None, SH.detail))  # sub-results of sh:node; the parent result already says it
    for r in report.subjects(RDF.type, SH.ValidationResult):
        if r in nested:
            continue
        focus, path, val = (report.value(r, k) for k in (SH.focusNode, SH.resultPath, SH.value))
        comp = report.value(r, SH.sourceConstraintComponent)
        f, cls = f"{st.name(focus)}.md", st.g.value(focus, SP.pageType)
        cname = str(cls).split("#")[1]
        if path == SP.linksTo:  # broken link
            t = st.name(val)
            fld = next((label(p) for p in st.g.predicates(focus, val) if p != SP.linksTo), "(body)")
            near = difflib.get_close_matches(t, [st.name(s) for s in st.g.subjects(SP.pageName, None)], n=1)
            alt = f"change [[{t}]] to [[{near[0]}]] in {f}, or " if near else ""
            want = next((str(rg).split("#")[1] for (c, k), (p, rg) in st.endpoint.items() if c == cls and k == fld),
                        "<one of StakeholderGroup, Concern, Affordance, Technology>")
            out.add(Violation(f, fld, R_LINK, f"link [[{t}]] points to no page.",
                              f'{alt}create the file "{t}.md" starting with these lines: '
                              f"--- / type: {want} / name: {t} / status: stub / ---"))
        elif comp == SH.MinCountConstraintComponent:  # missing required field
            fld = label(path)
            rng = next((rg for (c, k), (p, rg) in st.endpoint.items() if c == cls and k == fld), None)
            ex = f'{fld}: "[[<name of a {str(rng).split("#")[1]} page>]]"' if rng else f"{fld}: <text>"
            out.add(Violation(f, fld, R_FIELD, f'{cname} pages require "{fld}" (Less than 1 values on the path).',
                              f"add this line between the two --- lines at the top of {f}: {ex}"))
        elif comp == SH.NodeConstraintComponent and (val, SP.pageName, None) in st.g:  # wrong endpoint class
            fld, want = label(path), str(st.tbox.value(path, RDFS.range)).split("#")[1]
            got = str(st.g.value(val, SP.pageType)).split("#")[1]
            eg = st.of_class(SP[want], 1)
            eg = f'for example {fld}: "[[{eg[0]}]]"' if eg else f"to a page whose type is {want}"
            out.add(Violation(f, fld, R_ENDPOINT,
                              f"{cname}.{fld} links to [[{st.name(val)}]], which is {art(got)}; it must be {art(want)}.",
                              f"in {f} change field {fld} to the link of {art(want)} page, {eg}."))
        # NodeConstraint on an endpoint whose target page does not exist: covered by the broken-link result.
    return sorted(out, key=lambda v: (v.file, v.field, v.rule))


def _neighborhood(st, name):
    n = PAGE[quote(name, safe="")]
    return ({n} | {o for o in st.g.objects(n, SP.linksTo) if (o, SP.pageName, None) in st.g}
            | set(st.g.subjects(SP.linksTo, n)))


def check_local(st, name):
    n = PAGE[quote(name, safe="")]
    return to_violations(st, validate(st, subgraph(st, {n})))


def check_neighborhood(st, name):
    return to_violations(st, validate(st, subgraph(st, _neighborhood(st, name))))


def check_full(st):
    return to_violations(st, validate(st, st.g))


if __name__ == "__main__":
    st = load(sys.argv[1])
    vs = check_full(st)
    print("\n".join(map(str, vs)) or "ok: 0 violations", f"({len(list(st.g.subjects(SP.pageName, None)))} pages)")
