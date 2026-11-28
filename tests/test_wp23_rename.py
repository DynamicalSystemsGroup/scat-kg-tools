"""WP23-U1: the affordance-to-technology edge type is scat:ProvidedBy; TBox 0.3.0."""

from pathlib import Path

from rdflib import OWL, RDF, RDFS, Graph, URIRef

from scat_tools.tbox import SCAT, TBOX

TTL = Path(__file__).parents[1] / "ontology" / "scat.ttl"
OLD = URIRef(str(SCAT) + "Attri" + "butes")


def test_provided_by_is_the_affordance_to_technology_edge_type():
    g = Graph().parse(TTL)
    assert (SCAT.ProvidedBy, RDF.type, SCAT.EdgeType) in g
    assert (SCAT.ProvidedBy, RDFS.domain, SCAT.Affordance) in g
    assert (SCAT.ProvidedBy, RDFS.range, SCAT.Technology) in g
    assert TBOX.edge_types["provided-by"].verb == "is provided by"


def test_the_old_name_is_gone():
    g = Graph().parse(TTL)
    assert not set(g.triples((OLD, None, None)))
    assert not set(g.triples((None, None, OLD)))


def test_version_is_0_3_0():
    g = Graph().parse(TTL)
    assert {str(o) for o in g.objects(None, OWL.versionInfo)} == {"0.3.0"}
