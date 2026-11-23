"""STACK C: no graph store at check time. Rules = pydantic models (required fields) + plain Python
(endpoint class, missing link). Throwaway spike code.

Load phase (`load`): parse every page, build name->page and backlink index. Check phase: pure dict lookups + pydantic.
"""
import difflib
import sys
from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, ValidationError

SPIKE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SPIKE))
from common import WIKILINK, parse_vault  # noqa: E402

R_FIELD, R_ENDPOINT, R_LINK = "missing-required-field", "wrong-endpoint-class", "broken-link"
Req = Field(min_length=1)


class _Page(BaseModel):
    model_config = ConfigDict(extra="allow")


class StakeholderGroup(_Page):
    name: str = Req
    description: str = Req


class Concern(_Page):
    name: str = Req
    description: str = Req


class Affordance(_Page):
    name: str = Req
    description: str = Req


class Technology(_Page):
    name: str = Req
    description: str = Req


class Heldby(_Page):
    stakeholder: str = Req
    concern: str = Req


class Addresses(_Page):
    concern: str = Req
    affordance: str = Req


class Attributes(_Page):
    affordance: str = Req
    technology: str = Req


MODELS = {m.__name__: m for m in (StakeholderGroup, Concern, Affordance, Technology, Heldby, Addresses, Attributes)}
# relation class -> {endpoint field: required class of the linked page}
ENDPOINTS = {"Heldby": {"stakeholder": "StakeholderGroup", "concern": "Concern"},
             "Addresses": {"concern": "Concern", "affordance": "Affordance"},
             "Attributes": {"affordance": "Affordance", "technology": "Technology"}}


@dataclass
class Violation:
    file: str
    field: str
    rule: str
    problem: str
    fix: str

    def __str__(self):
        return f'{self.file}: field "{self.field}" [{self.rule}] {self.problem} Fix: {self.fix}'


class Index:
    def __init__(self, pages):
        self.pages = {p["name"]: p for p in pages}
        self.backlinks = {}
        for p in pages:
            for t in p["links"]:
                self.backlinks.setdefault(t, set()).add(p["name"])

    def of_class(self, cls, n=3):
        return [p for p in sorted(self.pages) if self.pages[p]["meta"].get("type") == cls][:n]


def load(vault_dir):
    return Index(parse_vault(vault_dir))


def art(w):
    return ("an " if w[0] in "AEIOU" else "a ") + w


def _link(value):
    m = WIKILINK.search(value) if isinstance(value, str) else None
    return m.group(1).strip() if m else None


def _check_fields(page, cls):
    """pydantic validates the class's required fields; raw ValidationError -> Violation."""
    f = f'{page["name"]}.md'
    try:
        MODELS[cls].model_validate(page["meta"])
        return []
    except ValidationError as e:
        out = []
        for err in e.errors():
            fld = str(err["loc"][0])
            if cls in ENDPOINTS and fld in ENDPOINTS[cls]:
                ex = f'{fld}: "[[<name of a {ENDPOINTS[cls][fld]} page>]]"'
            else:
                ex = f"{fld}: <text>"
            out.append(Violation(f, fld, R_FIELD, f"{cls} pages require \"{fld}\" ({err['msg']}).",
                                 f"add this line between the two --- lines at the top of {f}: {ex}"))
        return out


def check_page(idx, page):
    f = f'{page["name"]}.md'
    cls = page["meta"].get("type")
    out = _check_fields(page, cls) if cls in MODELS else []
    for fld, want in ENDPOINTS.get(cls, {}).items():
        t = _link(page["meta"].get(fld))
        if t and t in idx.pages:
            got = idx.pages[t]["meta"].get("type")
            if got != want:
                eg = idx.of_class(want, 1)
                eg = f'for example {fld}: "[[{eg[0]}]]"' if eg else f"to a page whose type is {want}"
                out.append(Violation(f, fld, R_ENDPOINT,
                                     f'{cls}.{fld} links to [[{t}]], which is a {got}; it must be {art(want)}.',
                                     f"in {f} change field {fld} to the link of {art(want)} page, {eg}."))
    for t in page["links"]:
        if t not in idx.pages:
            fld = next((k for k, v in page["meta"].items() if t in [m.strip() for m in WIKILINK.findall(str(v))]),
                       "(body)")
            near = difflib.get_close_matches(t, list(idx.pages), n=1)
            alt = f"change [[{t}]] to [[{near[0]}]] in {f}, or " if near else ""
            want = ENDPOINTS.get(cls, {}).get(fld)
            ty = want or "<one of StakeholderGroup, Concern, Affordance, Technology>"
            out.append(Violation(f, fld, R_LINK, f"link [[{t}]] points to no page.",
                                 f'{alt}create the file "{t}.md" starting with these lines: '
                                 f"--- / type: {ty} / name: {t} / status: stub / ---"))
    return out


def neighborhood(idx, name):
    p = idx.pages[name]
    return {name} | {t for t in p["links"] if t in idx.pages} | idx.backlinks.get(name, set())


def check_local(idx, name):
    return check_page(idx, idx.pages[name])


def check_neighborhood(idx, name):
    return [v for n in sorted(neighborhood(idx, name)) for v in check_page(idx, idx.pages[n])]


def check_full(idx):
    return [v for n in sorted(idx.pages) for v in check_page(idx, idx.pages[n])]


def models_match_tbox(tbox=SPIKE / "placeholder-tbox.ttl"):
    """R-13 stand-in: hand-written models/ENDPOINTS equal the TBox (uses rdflib at load time only)."""
    import rdflib
    g = rdflib.Graph().parse(tbox)
    SP = rdflib.Namespace("https://example.org/scpt-spike#")
    for cls, m in MODELS.items():
        req = {str(o) for o in g.objects(SP[cls], SP.requiredField)}
        have = {k for k, v in m.model_fields.items() if v.is_required()}
        assert req == have, (cls, req, have)
    for cls, eps in ENDPOINTS.items():
        for p in g.subjects(rdflib.RDFS.domain, SP[cls]):
            fld, rng = str(g.value(p, rdflib.RDFS.label)), g.value(p, rdflib.RDFS.range)
            assert eps[fld] == str(rng).split("#")[1], (cls, fld)
    return True


if __name__ == "__main__":
    idx = load(sys.argv[1])
    vs = check_full(idx)
    print("\n".join(map(str, vs)) or "ok: 0 violations", f"({len(idx.pages)} pages)")
