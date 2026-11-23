"""R-13 equality test. Passes iff the stack C models equal the TBox (placeholder, or the scratch
copy named by $SCAT_TBOX). The mutation tests prove the comparison can fail, with no scratch file.

    uv run --directory research/toolchain/spike python -m pytest r13 -q
"""

import pytest

from r13.equality import DEFAULT_TBOX, differences, tbox_path


def test_models_equal_tbox():
    d = differences()
    assert not d, f"models differ from {tbox_path()}:\n" + "\n".join(d)


MUTATIONS = {
    "new required link": (
        "scat:CodedScenario   scat:requiresLink scat:groups,",
        "scat:CodedScenario   scat:requiresLink scat:raw, scat:groups,",
    ),
    "new class": (
        "scat:Technology       a owl:Class ;",
        "scat:Venue a owl:Class .\nscat:Technology       a owl:Class ;",
    ),
    "changed range": (
        "rdfs:domain scat:Concern ; rdfs:range scat:Affordance .",
        "rdfs:domain scat:Concern ; rdfs:range scat:Technology .",
    ),
    "new property": (
        "scat:raw   a owl:ObjectProperty",
        "scat:owner a owl:ObjectProperty .\nscat:raw   a owl:ObjectProperty",
    ),
}


@pytest.mark.parametrize("name", MUTATIONS)
def test_tbox_change_is_detected(name, tmp_path):
    old, new = MUTATIONS[name]
    text = DEFAULT_TBOX.read_text(encoding="utf-8")
    assert text.count(old) == 1, "mutation target drifted"
    scratch = tmp_path / "tbox.ttl"
    scratch.write_text(text.replace(old, new), encoding="utf-8", newline="\n")
    assert differences(scratch), f"mutation {name!r} went undetected"
