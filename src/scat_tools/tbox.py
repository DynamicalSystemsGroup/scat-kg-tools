"""The TBox, read from ontology/scat.ttl: the single source the models are built from (R-13).

The file ships inside the wheel as ``scat_tools/scat.ttl`` (built from ``ontology/scat.ttl``, never copied
by hand) and is read with rdflib when this module is imported.
"""

from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from rdflib import RDFS, Graph, Namespace
from rdflib.collection import Collection
from rdflib.namespace import RDF, SKOS

SCAT = Namespace("https://w3id.org/scat#")


@dataclass(frozen=True)
class Field:
    key: str  # the frontmatter key
    definition: str
    required_from: str  # status from which the field is required when listed as required
    value_set: tuple[str, ...] | None  # allowed values, in order (status, timeframe, kind)
    target_type: str | None = (
        None  # a link field (attributed_to): the page type its links must reach
    )


@dataclass(frozen=True)
class Column:
    name: str  # the column's name in the header row
    holds: str  # what its cells hold: "edge-type", "from", "to" or "note"


@dataclass(frozen=True)
class TableSpec:
    """How a narrative's table of edges is read: the heading it sits under and its columns, in order."""

    heading: str
    columns: tuple[Column, ...]

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(c.name for c in self.columns)

    def index_of(self, holds: str) -> int:
        return next(i for i, c in enumerate(self.columns) if c.holds == holds)


@dataclass(frozen=True)
class EdgeType:
    name: str  # the local name of the property in the TTL
    label: str  # the plain word (rdfs:label)
    slug: str  # its spelling in the command line and the API
    verb: str  # the verb a row's type cell may hold
    from_type: str  # slug of the node type at the first end
    to_type: str  # slug of the node type at the second end
    definition: str

    @property
    def spellings(self) -> tuple[str, str]:
        return (self.verb, self.slug)


@dataclass(frozen=True)
class PageType:
    slug: str  # the value of a page's `type` field
    label: str
    definition: str
    description: str  # scat:pageDescription
    carries_status: bool
    required: tuple[Field, ...]
    optional: tuple[Field, ...]
    table: TableSpec | None = None  # the type's table of edges, when it has one

    @property
    def fields(self) -> tuple[Field, ...]:
        return self.required + self.optional

    def field(self, key: str) -> Field | None:
        return next((f for f in self.fields if f.key == key), None)


@dataclass(frozen=True)
class TBox:
    page_types: dict[str, PageType]  # by slug
    edge_types: dict[str, EdgeType]  # by slug, in layer order
    statuses: tuple[str, ...]  # in lifecycle order
    layers: tuple[str, ...]  # the node types, in the order the edge types chain them

    @property
    def node_types(self) -> tuple[str, ...]:
        return self.layers

    @property
    def table_type(self) -> PageType:
        """The one page type that tells edges: the one with a table."""
        return next(t for t in self.page_types.values() if t.table is not None)

    @property
    def table(self) -> TableSpec:
        return self.table_type.table

    def edge_type_named(self, text: str) -> EdgeType | None:
        """The edge type whose verb or slug is `text`, compared without regard to case."""
        low = text.casefold()
        return next(
            (e for e in self.edge_types.values() if low in (e.verb.casefold(), e.slug.casefold())),
            None,
        )

    def edge_type_between(self, from_type: str, to_type: str) -> EdgeType | None:
        return next(
            (
                e
                for e in self.edge_types.values()
                if (e.from_type, e.to_type) == (from_type, to_type)
            ),
            None,
        )


def _text(g: Graph, s, p) -> str | None:
    o = g.value(s, p)
    return None if o is None else str(o)


def _field(g: Graph, node) -> Field:
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
        required_from="done" if required_from is None else _text(g, required_from, SKOS.notation),
        value_set=values,
        target_type=_text(g, node, SCAT.targetType),
    )


def _table(g: Graph, cls) -> TableSpec | None:
    heading = _text(g, cls, SCAT.tableHeading)
    columns = g.value(cls, SCAT.tableColumns)
    if heading is None or columns is None:
        return None
    return TableSpec(
        heading=heading,
        columns=tuple(
            Column(str(g.value(c, RDFS.label)), _text(g, c, SCAT.cellHolds))
            for c in Collection(g, columns)
        ),
    )


def _edge_types(g: Graph) -> tuple[dict[str, EdgeType], tuple[str, ...]]:
    key_of = {c: _text(g, c, SCAT.key) for c in g.subjects(SCAT.key, None)}
    found = []
    for e in g.subjects(RDF.type, SCAT.EdgeType):
        if e == SCAT.EdgeType:
            continue
        first, second = (key_of[n] for n in Collection(g, g.value(e, SCAT.endpointOrder)))
        found.append(
            EdgeType(
                name=str(e).removeprefix(str(SCAT)),
                label=str(g.value(e, RDFS.label)),
                slug=_text(g, e, SCAT.slug),
                verb=_text(g, e, SCAT.verb),
                from_type=first,
                to_type=second,
                definition=_text(g, e, SKOS.definition),
            )
        )
    # layer order: the edge types chain the node types, the one that is never a `to` comes first
    by_from = {e.from_type: e for e in found}
    tos = {e.to_type for e in found}
    layers: list[str] = []
    ordered: list[EdgeType] = []
    start = sorted(t for t in by_from if t not in tos)
    if start:
        t = start[0]
        layers.append(t)
        while t in by_from:
            ordered.append(by_from[t])
            t = by_from[t].to_type
            layers.append(t)
    return {e.slug: e for e in ordered}, tuple(layers)


def parse(g: Graph) -> TBox:
    """Build the TBox from a parsed scat.ttl."""

    def fields(cls, prop) -> tuple[Field, ...]:
        return tuple(sorted((_field(g, f) for f in g.objects(cls, prop)), key=lambda f: f.key))

    page_types = {}
    for cls in g.subjects(SCAT.key, None):
        if (cls, RDF.type, None) not in g or SCAT.Field in g.objects(cls, RDF.type):
            continue
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
            table=_table(g, cls),
        )
    status_set = g.value(SCAT.status, SCAT.valueSet) or g.value(SCAT["field-status"], SCAT.valueSet)
    statuses = tuple(
        str(g.value(m, SKOS.notation)) for m in Collection(g, g.value(status_set, SKOS.memberList))
    )
    edge_types, layers = _edge_types(g)
    return TBox(
        page_types=dict(sorted(page_types.items())),
        edge_types=edge_types,
        statuses=statuses,
        layers=layers,
    )


def ttl_text() -> str:
    """The shipped scat.ttl, read from the installed package.

    An editable install (a source checkout) has no copy inside the package, so it reads the one
    file in the repo directly.
    """
    shipped = resources.files("scat_tools").joinpath("scat.ttl")
    if shipped.is_file():
        return shipped.read_text(encoding="utf-8")
    return (Path(__file__).parents[2] / "ontology" / "scat.ttl").read_text(encoding="utf-8")


def load() -> TBox:
    return parse(Graph().parse(data=ttl_text(), format="turtle"))


TBOX = load()
