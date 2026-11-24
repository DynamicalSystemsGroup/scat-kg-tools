"""WP5-U8 (D-035 ruling 3): a `type:` key that is present but empty reports SCAT-FM-TYPE."""

import pytest
from helpers import report_of

C = "concern/safe-handling.md"
TYPE = "SCAT-FM-TYPE"


@pytest.mark.parametrize("line", ["type:", "type: null", 'type: ""', 'type: "   "'])
def test__scat_fm_type__an_empty_type_is_an_error(make_vault, line):
    page = f"---\n{line}\nstatus: done\ntitle: Safe handling\ndescription: D\n---\n"
    r = report_of(make_vault, {C: page})
    assert [p.rule for p in r.problems] == [TYPE]
    (p,) = r.problems
    assert p.severity == "error" and p.elements[1:3] == (C, "field `type`")
    assert "the value is empty, which is not a page type" in r.render()
    assert p.fix.startswith(
        "Fix, choose the one that describes this page:\n  1. `type: addresses` ("
    )
    assert len(p.fix.split("\n")) == 13  # head plus the twelve keys
