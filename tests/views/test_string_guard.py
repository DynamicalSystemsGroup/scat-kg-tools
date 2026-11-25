"""A name, a type or a direction is text, and a set of narratives is a list: anything else is refused with a fix."""

import pytest

import scat_kg


@pytest.mark.parametrize(
    "call",
    [
        lambda r: scat_kg.layered("dry", root=r),
        lambda r: scat_kg.layered(["dry", 3], root=r),
        lambda r: scat_kg.layered(7, root=r),
        lambda r: scat_kg.edge_table(["holds"], root=r),
        lambda r: scat_kg.edge_table(None, root=r),
        lambda r: scat_kg.trace("farmers", ["up"], root=r),
        lambda r: scat_kg.trace(5, root=r),
        lambda r: scat_kg.fingerprint(["dry"], root=r),
    ],
)
def test_a_value_of_the_wrong_kind_is_refused_with_a_fix(vault, call):
    r = call(vault)
    assert not r.ok
    d = r.to_dict()
    assert d["kind"] == "operation" and d["ok"] is False and len(d["refused"]) == 1
    assert "Fix: pass " in str(r)


def test_a_bare_string_is_not_iterated_as_characters(vault):
    r = scat_kg.layered("dry", root=vault)
    assert "pass a list of narrative names" in str(r)
    assert r.to_dict()["refused"][0]["subject"] == "'dry'"  # the whole value is named, not a letter
