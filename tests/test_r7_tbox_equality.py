"""WP5-R7 (R-13): the TBox and the models built from it equal ontology/scat.ttl.

The TTL is parsed here, separately, with rdflib and SPARQL, and not through `scat_kg.tbox`. It is compared
with `TBOX` (slugs, descriptions, definitions, fields, requiredFrom, status values, link rules,
endpoint order, value sets) and with the pydantic models built from it.
"""

from pathlib import Path
from typing import Literal, get_args, get_origin

import pytest
from rdflib import RDF, Graph

from scat_kg.models import MODELS
from scat_kg.tbox import TBOX

TTL = Path(__file__).parents[1] / "ontology" / "scat.ttl"
PREFIX = """
PREFIX scat: <https://w3id.org/scat#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
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
    assert set(TBOX.page_types) == set(types) and len(types) == 12
    for slug, node in types.items():
        t = TBOX.page_types[slug]
        assert t.slug == slug
        assert t.description == str(one(g, node, "scat:pageDescription"))
        assert t.definition == str(one(g, node, "skos:definition"))


@pytest.mark.parametrize("prop,attr", [
    ("requiredField", "required"), ("optionalField", "optional"), ("discouragedField", "discouraged"),
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


def test__r7__each_field_carries_its_link_rules_and_required_from(g):
    seen = 0
    for slug, node in ttl_types(g).items():
        for prop in ("requiredField", "optionalField", "discouragedField"):
            for key, fnode in ttl_fields(g, node, prop).items():
                f = TBOX.page_types[slug].field(key)
                target = one(g, fnode, "scat:targetType")
                assert f.is_link == (target is not None), (slug, key)
                assert f.target_type == (
                    None if target is None else str(one(g, target, "scat:key"))
                ), (slug, key)
                assert f.single == (str(one(g, fnode, "scat:single")) == "true"), (slug, key)
                from_ = one(g, fnode, "scat:requiredFrom")
                want_from = "done" if from_ is None else str(one(g, from_, "skos:notation"))
                assert f.required_from == want_from, (slug, key)
                seen += 1
    assert seen > 50


def test__r7__status_values_in_lifecycle_order_equal_the_ttl(g):
    (row,) = q(g, "SELECT ?l WHERE { scat:StatusValues skos:memberList ?l }")
    members = [str(one(g, m, "skos:notation")) for m in rdf_list(g, row.l)]
    assert members == ["stub", "draft", "done"]
    assert TBOX.statuses == tuple(members)
    assert g.query(
        PREFIX + "ASK { ?f scat:key 'status' ; scat:valueSet scat:StatusValues }"
    ).askAnswer
    assert TBOX.page_types["concern"].field("status").value_set == tuple(members)


def test__r7__the_link_levels_equal_the_ttl(g):
    (row,) = q(g, "SELECT ?u ?w WHERE { <https://w3id.org/scat> scat:unlistedLinkLevel ?u ; "
                  "scat:wrongTargetLevel ?w }")  # fmt: skip
    assert (TBOX.unlisted_link_level, TBOX.wrong_target_level) == (str(row.u), str(row.w))
    assert {str(row.u), str(row.w)} <= {"error", "warning"}


def test__r7__relation_endpoint_order_equals_the_ttl(g):
    want = {}
    for slug, node in ttl_types(g).items():
        rows = q(g, "SELECT ?l WHERE { ?c scat:endpointOrder ?l }", c=node)
        if rows:
            want[slug] = tuple(str(one(g, f, "scat:key")) for f in rdf_list(g, rows[0].l))
    assert set(want) == {"heldby", "addresses", "attributes"}
    assert all(len(v) == 2 for v in want.values())
    assert TBOX.relations == want
    assert {s for s, t in TBOX.page_types.items() if t.endpoint_order} == set(want)


def test__r7__carries_status_and_discouraged_body_links_equal_the_ttl(g):
    for slug, node in ttl_types(g).items():
        t = TBOX.page_types[slug]
        carries = one(g, node, "scat:carriesStatus")
        assert t.carries_status == (str(carries) != "false"), slug
        rows = q(g, "SELECT ?k WHERE { ?c scat:discouragedBodyLink ?t . ?t scat:key ?k }", c=node)
        assert t.discouraged_body_links == tuple(sorted(str(r.k) for r in rows)), slug
    assert {s for s, t in TBOX.page_types.items() if not t.carries_status} == {"class"}


def test__r7__the_class_page_indexes_value_set_equals_the_ttl(g):
    (row,) = q(g, "SELECT ?l WHERE { scat:field-indexes scat:valueSet ?l }")
    values = tuple(str(v) for v in rdf_list(g, row.l))
    assert values == TBOX.page_types["class"].field("indexes").value_set
    assert set(values) <= set(TBOX.page_types)


def test__r7__the_timeframe_value_set_and_pages_equal_the_ttl(g):
    (row,) = q(g, "SELECT ?l WHERE { scat:field-timeframe scat:valueSet ?l }")
    values = tuple(str(v) for v in rdf_list(g, row.l))
    assert values == ("past", "future", "mixed")
    ttl_pages = {
        str(r.k)
        for r in q(
            g, "SELECT ?k WHERE { ?c scat:requiredField scat:field-timeframe ; scat:key ?k }"
        )
    }
    assert ttl_pages == {"scenario-raw", "architecture-raw"}
    assert {s for s, t in TBOX.page_types.items() if t.field("timeframe")} == ttl_pages
    for slug in ttl_pages:
        field = TBOX.page_types[slug].field("timeframe")
        assert field.value_set == values and field.required_from == "done"


def test__r7__the_models_are_the_ttls_fields_and_value_sets(g):
    assert set(MODELS) == set(ttl_types(g))
    for slug, node in ttl_types(g).items():
        keys = {"type"}
        for prop in ("requiredField", "optionalField", "discouragedField"):
            keys |= set(ttl_fields(g, node, prop))
        model = MODELS[slug]
        assert set(model.model_fields) == keys, slug
        assert get_args(model.model_fields["type"].annotation) == (slug,)
        for key, field in model.model_fields.items():
            literal = [a for a in get_args(field.annotation) if get_origin(a) is Literal]
            if key == "status":
                assert literal and get_args(literal[0]) == ("stub", "draft", "done")
            elif key == "indexes":
                assert (
                    literal
                    and get_args(literal[0]) == TBOX.page_types["class"].field("indexes").value_set
                )
            elif key == "timeframe":
                assert literal and get_args(literal[0]) == ("past", "future", "mixed")
            elif key != "type":
                assert not literal, (slug, key)
