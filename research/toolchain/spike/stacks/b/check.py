"""STACK B: markdown+frontmatter+wikilink parser -> rdflib graph -> SHACL (pyshacl) -> messages.

Throwaway spike code. Three scopes: check_page, check_neighborhood, check_vault.
Rules live in shapes.ttl (SHACL); the "mapping layer" (diagnose) turns pyshacl results into
R-2 messages (file, field/link, rule id, fix) and is where all the fix-exactness work happens.
"""

import difflib
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, unquote

import frontmatter
import pyshacl
from rdflib import RDF, RDFS, Graph, Literal, Namespace, URIRef

HERE = Path(__file__).resolve().parent
TBOX_PATH = HERE.parent.parent / "placeholder-tbox.ttl"
SCAT = Namespace("https://example.org/scat-placeholder#")
SH = Namespace("http://www.w3.org/ns/shacl#")
PAGE = "https://example.org/scat-placeholder/page/"
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
TYPE_RE = re.compile(r"^type:\s*[\"']?([a-z-]+)", re.MULTILINE)

TYPE_CLASS = {
    "stakeholder-group": SCAT.StakeholderGroup,
    "concern": SCAT.Concern,
    "affordance": SCAT.Affordance,
    "technology": SCAT.Technology,
    "scenario-raw": SCAT.RawScenario,
    "scenario-coded": SCAT.CodedScenario,
    "architecture-raw": SCAT.RawArchitecture,
    "architecture-coded": SCAT.CodedArchitecture,
}
CLASS_TYPE = {v: k for k, v in TYPE_CLASS.items()}
# frontmatter field -> class its values must have (for the page-type of a missing link target)
FIELD_RANGE = {
    "heldby": SCAT.Concern,
    "addresses": SCAT.Affordance,
    "attributes": SCAT.Technology,
    "groups": SCAT.StakeholderGroup,
    "concerns": SCAT.Concern,
    "affordances": SCAT.Affordance,
    "technologies": SCAT.Technology,
}
# required link field -> (source field on this page, relation on that page's targets, direction)
DERIVE = {
    "affordances": ("concerns", "addresses", "fwd"),
    "technologies": ("affordances", "attributes", "fwd"),
    "groups": ("concerns", "heldby", "inv"),
    "concerns": ("groups", "heldby", "fwd"),
}
SCALARS = {"type", "status", "title", "description"}

TBOX = Graph().parse(TBOX_PATH)
SHAPES = Graph().parse(HERE / "shapes.ttl")


def use_shapes(name):
    """Select "core" (shapes.ttl, default) or "sparql" (shapes-sparql.ttl: sh:sparql constraints)."""
    global SHAPES
    SHAPES = Graph().parse(HERE / ("shapes.ttl" if name == "core" else "shapes-sparql.ttl"))


@dataclass
class Page:
    stem: str
    meta: dict
    body: str
    links: dict  # field -> [target stems]; "(body)" holds untyped body mentions


def page_iri(stem):
    return URIRef(PAGE + quote(stem, safe=""))


def stem_of(iri):
    return unquote(str(iri)[len(PAGE) :])


def links_in(value):
    vals = value if isinstance(value, list) else [value]
    return [m.group(1).strip() for v in vals if isinstance(v, str) for m in WIKILINK.finditer(v)]


def parse_page(stem, text):
    post = frontmatter.loads(text)
    links = {}
    for field, value in post.metadata.items():
        found = links_in(value)
        if found:
            links[field] = found
    body = [m.group(1).strip() for m in WIKILINK.finditer(post.content)]
    if body:
        links["(body)"] = body
    return Page(stem, post.metadata, post.content, links)


def peek_type(text):
    m = TYPE_RE.search(text[:400])
    return TYPE_CLASS.get(m.group(1)) if m else None


class Vault:
    """A vault directory. Reads are lazy; each timed run makes a fresh one (no carried cache)."""

    def __init__(self, path):
        self.path = Path(path)
        self._texts = None

    def stems(self):
        return sorted(p.stem for p in self.path.glob("*.md"))

    def read(self, stem):
        if self._texts is not None:
            return self._texts[stem]
        return (self.path / f"{stem}.md").read_text(encoding="utf-8")

    def exists(self, stem):
        return (self.path / f"{stem}.md").exists()

    def texts(self):
        if self._texts is None:
            self._texts = {s: self.read(s) for s in self.stems()}
        return self._texts

    def neighbors(self, stem):
        """Pages within one link of `stem`, either direction (reads the whole vault's text)."""
        texts = self.texts()
        out = {t.strip() for t in WIKILINK.findall(texts[stem])}
        inn = {s for s, x in texts.items() if stem in {t.strip() for t in WIKILINK.findall(x)}}
        return ((out | inn) & set(texts)) | {stem}


def add_page(g, page, vault):
    """Add one page and the type facts of its link targets (existing, or scat:Missing)."""
    node = page_iri(page.stem)
    g.add((node, RDF.type, SCAT.Page))
    cls = TYPE_CLASS.get(str(page.meta.get("type")))
    if cls:
        g.add((node, RDF.type, cls))
    for key in ("status", "title", "description"):
        if page.meta.get(key) is not None:
            g.add((node, SCAT[key], Literal(str(page.meta[key]))))
    for field, targets in page.links.items():
        pred = SCAT["mentions" if field == "(body)" else field]
        for t in targets:
            tnode = page_iri(t)
            g.add((node, pred, tnode))
            if vault.exists(t):
                tcls = peek_type(vault.read(t))
                if tcls:
                    g.add((tnode, RDF.type, tcls))
            else:
                g.add((tnode, RDF.type, SCAT.Missing))


def validate(pages, vault):
    g = Graph()
    g += TBOX
    for p in pages:
        add_page(g, p, vault)
    _, report, _ = pyshacl.validate(g, shacl_graph=SHAPES, inplace=True, advanced=True)
    return g, report


# ---- the three scopes -------------------------------------------------------------------------


def check_page(vault, stem):
    return diagnose(*validate([parse_page(stem, vault.read(stem))], vault), vault)


def check_neighborhood(vault, stem):
    pages = [parse_page(s, vault.read(s)) for s in sorted(vault.neighbors(stem))]
    return diagnose(*validate(pages, vault), vault)


def check_vault(vault):
    pages = [parse_page(s, vault.read(s)) for s in vault.stems()]
    return diagnose(*validate(pages, vault), vault)


# ---- mapping layer: SHACL results -> R-2 messages ---------------------------------------------


@dataclass
class Diagnostic:
    file: str
    rule: str
    field: str
    message: str


def _a(word):
    return ("an " if word[:1] in "aeiou" else "a ") + word


def humanize(stem):
    s = stem.replace("-", " ")
    return s[:1].upper() + s[1:]


def label(cls):
    return str(TBOX.value(cls, RDFS.label) or cls).lower()


def find_line(text, needle):
    for i, line in enumerate(text.splitlines(), 1):
        if needle in line:
            return i
    return None


def candidates(vault, cls, near=None):
    """Stems of pages of class `cls`; those linked to/from `near` first."""
    texts = vault.texts()
    want = CLASS_TYPE[cls]
    pool = sorted(
        s for s, t in texts.items() if (m := TYPE_RE.search(t[:400])) and m.group(1) == want
    )
    if near:
        linked = {
            s
            for s in pool
            if s != near
            and (
                any(x.strip() == near for x in WIKILINK.findall(texts[s]))
                or any(x.strip() == s for x in WIKILINK.findall(texts.get(near, "")))
            )
        }
        return sorted(linked), [s for s in pool if s not in linked]
    return [], pool


def derive_links(vault, page, field):
    """Exact values for a missing required link field, derived from the page's other links."""
    src, rel, direction = DERIVE.get(field, (None, None, None))
    if src is None or src not in page.links:
        return []
    texts = vault.texts()
    out = []
    for t in page.links[src]:
        if direction == "fwd" and t in texts:
            out += parse_page(t, texts[t]).links.get(rel, [])
        elif direction == "inv":
            out += [s for s, x in texts.items() if t in parse_page(s, x).links.get(rel, [])]
    return sorted(set(out))


def diagnose(g, rg, vault):
    out = []
    for r in rg.subjects(RDF.type, SH.ValidationResult):
        focus = rg.value(r, SH.focusNode)
        path = rg.value(r, SH.resultPath)
        value = rg.value(r, SH.value)
        shape = rg.value(r, SH.sourceShape)
        comp = rg.value(r, SH.sourceConstraintComponent)
        rule = str(SHAPES.value(shape, SCAT.ruleId) or "")
        if not rule:
            rule = "SCAT-003" if comp == SH.NotConstraintComponent else "SCAT-002"
        stem = stem_of(focus)
        field = str(path).split("#")[-1] if path else ""
        if comp == SH.ClassConstraintComponent and (value, RDF.type, SCAT.Missing) in g:
            continue  # same fault is reported as SCAT-003; keep the more precise one
        out.append(_message(vault, stem, rule, field, value, shape))
    return sorted(out, key=lambda d: (d.file, d.rule, d.field, d.message))


def _message(vault, stem, rule, field, value, shape):
    file = f"{stem}.md"
    text = vault.read(stem)
    page = parse_page(stem, text)
    if rule == "SCAT-001":
        if field == "description":
            fix = (
                f'in {file} either add `description: "<one sentence you write>"` or, if the page '
                f"is unfinished, change `status: done` to `status: draft`"
            )
        elif field == "title":
            fix = f'in {file} add `title: "{humanize(stem)}"`'
        else:
            fix = f"in {file} add `status: stub`"
        msg = f"required field `{field}` is missing. Fix: {fix}"
    elif rule == "SCAT-003":
        target = stem_of(value)
        where = "body link" if field == "mentions" else f"field `{field}`"
        line = find_line(text, f"[[{target}")
        file = f"{file}:{line}" if line else file
        close = difflib.get_close_matches(target, vault.stems(), n=1, cutoff=0.8)
        if close:
            fix = f"replace [[{target}]] with [[{close[0]}]], or create {target}.md"
        elif field in FIELD_RANGE:
            t = CLASS_TYPE[FIELD_RANGE[field]]
            fix = (
                f"create {target}.md containing exactly the five lines:\n"
                f'      ---\n      type: {t}\n      status: stub\n      title: "{humanize(target)}"\n      ---'
            )
        else:
            fix = f"create {target}.md (type unknown for a body link) or remove the link"
        msg = f"{where}: page [[{target}]] does not exist. Fix: {fix}"
        field = "body" if field == "mentions" else field
    elif rule == "SCAT-004":
        vals = derive_links(vault, page, field)
        if vals:
            lines = "".join(f'\n        - "[[{v}]]"' for v in vals)
            fix = f"add to the frontmatter of {file}:\n      {field}:{lines}"
        else:
            fix = f"add `{field}:` with at least one wikilink list item to {file} (no value derivable)"
        msg = f"coded record has no `{field}` link (required when status is done). Fix: {fix}"
    else:  # SCAT-002
        target = stem_of(value)
        required = SHAPES.value(shape, SH["class"])
        vtype = [label(c) for c in _classes(vault, target)] or ["(no valid type)"]
        line = find_line(text, f"[[{target}")
        file = f"{file}:{line}" if line else file
        near, rest = candidates(vault, required, near=target)
        pick = near[:3] or rest[:3]
        eg = " or ".join(f'`- "[[{c}]]"`' for c in pick)
        why = f"related to [[{target}]]" if near else "any, none is related"
        req = label(required)
        msg = (
            f"field `{field}`: [[{target}]] is {_a(vtype[0])}, {_a(req)} is required. "
            f'Fix: under `{field}:` replace `- "[[{target}]]"` with one of '
            f"({why}): {eg}"
        )
    return Diagnostic(file, rule, field, f"{file} [{rule}] {msg}")


def _classes(vault, stem):
    if not vault.exists(stem):
        return []
    c = peek_type(vault.read(stem))
    return [c] if c else []
