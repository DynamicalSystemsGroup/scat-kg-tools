"""The TBox, read from ontology/scat.ttl: the single source the models are built from (R-13).

The file ships inside the wheel as ``scat_kg/scat.ttl`` (built from ``ontology/scat.ttl``, never copied
by hand) and is read with rdflib when this module is imported.
"""

from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from rdflib import RDFS, Graph, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import RDF, SKOS

SCAT = Namespace("https://w3id.org/scat#")
ONTOLOGY = URIRef("https://w3id.org/scat")


@dataclass(frozen=True)
class Field:
    key: str  # the frontmatter key
    definition: str
    target_type: str | None  # slug of the page type every target must have (a link field)
    single: bool  # a link field holding exactly one wikilink, not a list
    required_from: str  # status from which the field is required when listed as required
    value_set: tuple[str, ...] | None  # allowed values, in order (status, indexes)

    @property
    def is_link(self) -> bool:
        return self.target_type is not None


@dataclass(frozen=True)
class PageType:
    slug: str  # the value of a page's `type` field
    label: str
    definition: str
    description: str  # scat:pageDescription
    carries_status: bool
    required: tuple[Field, ...]
    optional: tuple[Field, ...]
    discouraged: tuple[Field, ...]
    discouraged_body_links: tuple[str, ...]  # slugs of page types the body should not link to
    endpoint_order: tuple[str, ...] | None  # relation pages: endpoint field keys, first then second
    verb: str | None = None  # relation pages: joins the endpoint titles in a stub's title

    @property
    def fields(self) -> tuple[Field, ...]:
        return self.required + self.optional + self.discouraged

    def field(self, key: str) -> Field | None:
        return next((f for f in self.fields if f.key == key), None)


@dataclass(frozen=True)
class ClassPageName:
    name: str  # the reserved page name
    indexes: str  # slug of the page type its table lists
    title: str  # the default title


@dataclass(frozen=True)
class TBox:
    page_types: dict[str, PageType]  # by slug
    class_pages: dict[str, ClassPageName]  # the seven class pages, by name (contract section 8)
    statuses: tuple[str, ...]  # in lifecycle order
    unlisted_link_level: str
    wrong_target_level: str

    @property
    def relations(self) -> dict[str, tuple[str, ...]]:
        """Relation slug -> endpoint field keys, first endpoint then second."""
        return {s: t.endpoint_order for s, t in self.page_types.items() if t.endpoint_order}


def _text(g: Graph, s, p) -> str | None:
    o = g.value(s, p)
    return None if o is None else str(o)


def _field(g: Graph, node) -> Field:
    target = g.value(node, SCAT.targetType)
    vs = g.value(node, SCAT.valueSet)
    values = None
    if vs is not None:
        if (vs, RDF.type, SKOS.OrderedCollection) in g:
            members = Collection(g, g.value(vs, SKOS.memberList))
            values = tuple(str(g.value(m, SKOS.notation)) for m in members)
        else:
            values = tuple(str(v) for v in Collection(g, vs))
    required_from = g.value(node, SCAT.requiredFrom)
    return Field(
        key=_text(g, node, SCAT.key),
        definition=_text(g, node, SKOS.definition),
        target_type=None if target is None else _text(g, target, SCAT.key),
        single=_text(g, node, SCAT.single) == "true",
        required_from="done" if required_from is None else _text(g, required_from, SKOS.notation),
        value_set=values,
    )


def parse(g: Graph) -> TBox:
    """Build the TBox from a parsed scat.ttl."""

    def fields(cls, prop) -> tuple[Field, ...]:
        return tuple(sorted((_field(g, f) for f in g.objects(cls, prop)), key=lambda f: f.key))

    page_types = {}
    for cls in g.subjects(SCAT.key, None):
        if (cls, SCAT.key, None) not in g or (cls, RDF.type, None) not in g:
            continue
        if SCAT.Field in g.objects(cls, RDF.type):
            continue
        order = g.value(cls, SCAT.endpointOrder)
        carries = _text(g, cls, SCAT.carriesStatus)
        slug = _text(g, cls, SCAT.key)
        page_types[slug] = PageType(
            slug=slug,
            label=_text(g, cls, SKOS.prefLabel) or str(g.value(cls, RDFS.label)),
            definition=_text(g, cls, SKOS.definition),
            description=_text(g, cls, SCAT.pageDescription),
            carries_status=carries != "false",
            required=fields(cls, SCAT.requiredField),
            optional=fields(cls, SCAT.optionalField),
            discouraged=fields(cls, SCAT.discouragedField),
            discouraged_body_links=tuple(
                sorted(_text(g, t, SCAT.key) for t in g.objects(cls, SCAT.discouragedBodyLink))
            ),
            endpoint_order=None
            if order is None
            else tuple(_text(g, f, SCAT.key) for f in Collection(g, order)),
            verb=_text(g, cls, SCAT.verb),
        )
    class_pages = {
        str(g.value(c, RDFS.label)): ClassPageName(
            name=str(g.value(c, RDFS.label)),
            indexes=_text(g, c, SCAT.indexesKey),
            title=_text(g, c, SCAT.defaultTitle),
        )
        for c in g.subjects(RDF.type, SCAT.ClassPageName)
    }
    status_set = g.value(SCAT.status, SCAT.valueSet) or g.value(SCAT["field-status"], SCAT.valueSet)
    statuses = tuple(
        str(g.value(m, SKOS.notation)) for m in Collection(g, g.value(status_set, SKOS.memberList))
    )
    return TBox(
        page_types=dict(sorted(page_types.items())),
        class_pages=dict(sorted(class_pages.items())),
        statuses=statuses,
        unlisted_link_level=_text(g, ONTOLOGY, SCAT.unlistedLinkLevel),
        wrong_target_level=_text(g, ONTOLOGY, SCAT.wrongTargetLevel),
    )


def ttl_text() -> str:
    """The shipped scat.ttl, read from the installed package.

    An editable install (a source checkout) has no copy inside the package, so it reads the one
    file in the repo directly.
    """
    shipped = resources.files("scat_kg").joinpath("scat.ttl")
    if shipped.is_file():
        return shipped.read_text(encoding="utf-8")
    return (Path(__file__).parents[2] / "ontology" / "scat.ttl").read_text(encoding="utf-8")


def load() -> TBox:
    return parse(Graph().parse(data=ttl_text(), format="turtle"))


TBOX = load()
