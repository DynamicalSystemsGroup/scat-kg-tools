"""WP5-R7 (R-13): the TBox and the models built from it equal ontology/scat.ttl.

The TTL is parsed here, separately, with rdflib and SPARQL, and not through `scat_tools.tbox`. It is compared
with `TBOX` (slugs, descriptions, definitions, fields, requiredFrom, status values, edge types with their
slugs, verbs and ends, the table heading and columns, value sets) and with the pydantic models built from it.
"""

from pathlib import Path
from typing import Literal, get_args, get_origin

import pytest
from rdflib import RDF, Graph

from scat_tools.models import MODELS
from scat_tools.tbox import TBOX

TTL = Path(__file__).parents[1] / "ontology" / "scat.ttl"
PREFIX = """
PREFIX scat: <https://w3id.org/scat#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""


@pytest.fixture(scope="module")
def g():
    graph = Graph()
    graph.parse(TTL, format="turtle")
    return graph


def q(g, text, **bind):
    return list(g.query(PREFIX + text, initBindings=bind))


def ttl_types(g):
    """slug -> page type node: every subject with a scat:key that is an owl:Class, not a Field."""
    rows = q(g, "SELECT ?c ?k WHERE { ?c scat:key ?k ; a <http://www.w3.org/2002/07/owl#Class> "
                "FILTER NOT EXISTS { ?c a scat:Field } }")  # fmt: skip
    return {str(k): c for c, k in rows}


def ttl_fields(g, cls, prop):
    """key -> (field node) for the fields one page type lists under `prop` (requiredField, ...)."""
    rows = q(g, f"SELECT ?f ?k WHERE {{ ?c scat:{prop} ?f . ?f scat:key ?k }}", c=cls)
    return {str(k): f for f, k in rows}


def one(g, node, prop):
    rows = q(g, f"SELECT ?v WHERE {{ ?n {prop} ?v }}", n=node)
    assert len(rows) <= 1, (node, prop)
    return rows[0].v if rows else None


def rdf_list(g, head):
    items = []
    while head != RDF.nil:
        (first,) = g.objects(head, RDF.first)
        items.append(first)
        (head,) = g.objects(head, RDF.rest)
    return items


def test__r7__page_type_slugs_and_descriptions_equal_the_ttl(g):
    types = ttl_types(g)
    assert set(TBOX.page_types) == set(types) and len(types) == 7
    for slug, node in types.items():
        t = TBOX.page_types[slug]
        assert t.slug == slug
        assert t.description == str(one(g, node, "scat:pageDescription"))
        assert t.definition == str(one(g, node, "skos:definition"))


@pytest.mark.parametrize("prop,attr", [
    ("requiredField", "required"), ("optionalField", "optional"),
])  # fmt: skip
def test__r7__the_fields_of_each_page_type_equal_the_ttl(g, prop, attr):
    for slug, node in ttl_types(g).items():
        want = ttl_fields(g, node, prop)
        have = getattr(TBOX.page_types[slug], attr)
        assert {f.key for f in have} == set(want), (slug, prop)
        assert [f.key for f in have] == sorted(want)  # a stable order: by key
        for f in have:
            fnode = want[f.key]
            assert f.definition == str(one(g, fnode, "skos:definition")), (slug, f.key)


def test__r7__no_page_type_lists_a_discouraged_field_and_one_link_field_is_attributed_to(g):
    assert not q(g, "SELECT ?c WHERE { ?c scat:discouragedField ?f }")
    rows = q(g, "SELECT ?k ?t WHERE { ?f scat:key ?k ; scat:targetType ?t }")
    assert [(str(r.k), str(r.t)) for r in rows] == [("attributed_to", "contributor")]
    (field,) = (f for t in TBOX.page_types.values() for f in t.fields if f.target_type)
    assert (field.key, field.target_type) == ("attributed_to", "contributor")
    assert field.target_type in TBOX.page_types


def test__r7__each_field_carries_its_required_from_and_value_set(g):
    seen = 0
    for slug, node in ttl_types(g).items():
        for prop in ("requiredField", "optionalField"):
            for key, fnode in ttl_fields(g, node, prop).items():
                f = TBOX.page_types[slug].field(key)
                from_ = one(g, fnode, "scat:requiredFrom")
                want_from = "done" if from_ is None else str(one(g, from_, "skos:notation"))
                assert f.required_from == want_from, (slug, key)
                assert (f.value_set is not None) == (one(g, fnode, "scat:valueSet") is not None)
                seen += 1
    assert seen == 4 * 4 + 5 + 1 + 1 + 3  # nodes, narrative, kind, attributed_to, contributor


def test__r7__status_values_in_lifecycle_order_equal_the_ttl(g):
    (row,) = q(g, "SELECT ?l WHERE { scat:StatusValues skos:memberList ?l }")
    members = [str(one(g, m, "skos:notation")) for m in rdf_list(g, row.l)]
    assert members == ["stub", "draft", "done"]
    assert TBOX.statuses == tuple(members)
    assert g.query(
        PREFIX + "ASK { ?f scat:key 'status' ; scat:valueSet scat:StatusValues }"
    ).askAnswer
    assert TBOX.page_types["concern"].field("status").value_set == tuple(members)


def test__r7__the_edge_types_equal_the_ttl(g):
    rows = q(g, "SELECT ?e ?l ?s ?v ?o WHERE { ?e a scat:EdgeType ; rdfs:label ?l ; scat:slug ?s ; "
                "scat:verb ?v ; scat:endpointOrder ?o }")  # fmt: skip
    want = {}
    for r in rows:
        first, second = (str(one(g, n, "scat:key")) for n in rdf_list(g, r.o))
        want[str(r.s)] = (str(r.l), str(r.v), first, second, str(r.e).rsplit("#", 1)[1])
    assert len(want) == 3
    assert {
        s: (e.label, e.verb, e.from_type, e.to_type, e.name) for s, e in TBOX.edge_types.items()
    } == want
    for e in TBOX.edge_types.values():
        assert {e.from_type, e.to_type} <= set(TBOX.page_types)
    assert set(TBOX.layers) == {
        t for e in TBOX.edge_types.values() for t in (e.from_type, e.to_type)
    }


def test__r7__the_table_heading_and_columns_equal_the_ttl(g):
    rows = q(g, "SELECT ?c ?h ?l WHERE { ?c scat:tableHeading ?h ; scat:tableColumns ?l }")
    assert len(rows) == 1
    (row,) = rows
    assert str(row.h) == TBOX.table.heading
    assert str(one(g, row.c, "scat:key")) == TBOX.table_type.slug
    cols = [
        (str(one(g, c, "rdfs:label")), str(one(g, c, "scat:cellHolds"))) for c in rdf_list(g, row.l)
    ]
    assert cols == [(c.name, c.holds) for c in TBOX.table.columns]
    assert {h for _, h in cols} == {"edge-type", "from", "to", "note"}


def test__r7__carries_status_equals_the_ttl(g):
    for slug, node in ttl_types(g).items():
        t = TBOX.page_types[slug]
        carries = one(g, node, "scat:carriesStatus")
        assert t.carries_status == (str(carries) != "false"), slug
    assert {s for s, t in TBOX.page_types.items() if not t.carries_status} == {"index"}


def test__r7__the_timeframe_and_kind_value_sets_and_pages_equal_the_ttl(g):
    for field, want, pages in [
        ("timeframe", ("past", "future", "mixed"), {"narrative"}),
        ("kind", ("scenario", "architecture"), {"narrative"}),
    ]:
        (row,) = q(g, f"SELECT ?l WHERE {{ scat:field-{field} scat:valueSet ?l }}")
        values = tuple(str(v) for v in rdf_list(g, row.l))
        assert values == want
        ttl_pages = {
            str(r.k)
            for r in q(
                g,
                f"SELECT ?k WHERE {{ ?c scat:requiredField|scat:optionalField scat:field-{field} ;"
                " scat:key ?k }",
            )
        }
        assert ttl_pages == pages
        assert {s for s, t in TBOX.page_types.items() if t.field(field)} == pages
        assert TBOX.page_types["narrative"].field(field).value_set == values


def test__r7__the_models_are_the_ttls_fields_and_value_sets(g):
    assert set(MODELS) == set(ttl_types(g))
    for slug, node in ttl_types(g).items():
        keys = {"type"}
        for prop in ("requiredField", "optionalField"):
            keys |= set(ttl_fields(g, node, prop))
        model = MODELS[slug]
        assert set(model.model_fields) == keys, slug
        assert get_args(model.model_fields["type"].annotation) == (slug,)
        for key, field in model.model_fields.items():
            literal = [a for a in get_args(field.annotation) if get_origin(a) is Literal]
            if key == "status":
                assert literal and get_args(literal[0]) == ("stub", "draft", "done")
            elif key == "timeframe":
                assert literal and get_args(literal[0]) == ("past", "future", "mixed")
            elif key == "kind":
                assert literal and get_args(literal[0]) == ("scenario", "architecture")
            elif key != "type":
                assert not literal, (slug, key)
