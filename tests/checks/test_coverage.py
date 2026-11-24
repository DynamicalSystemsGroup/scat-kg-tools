"""Every rule in the catalogue has a seeded-defect test.

A seeded-defect test is named `test__<rule id, lower case, - as _>__<what is seeded>`.
"""

import re

from helpers import CATALOGUE, catalogue_severities

from scat_kg.checks import DEFERRED, SEVERITY


def catalogue_ids() -> list[str]:
    text = CATALOGUE.read_text(encoding="utf-8")
    return re.findall(r"^\| (SCAT-[A-Z-]+) \| (?:error|warning) \|", text, re.MULTILINE)


def test__the_registry_knows_every_rule_in_the_catalogue():
    ids = catalogue_ids()
    assert len(ids) == len(set(ids)) == 27
    assert set(ids) == set(SEVERITY)
    assert catalogue_severities() == SEVERITY


def test__every_rule_has_a_seeded_test(request, capsys):
    seeded = {}
    for item in request.session.items:
        parts = (item.originalname or item.name).split("__")
        if parts[0] == "test" and len(parts) >= 3 and parts[1].startswith("scat_"):
            seeded.setdefault(parts[1].upper().replace("_", "-"), set()).add(item.name)
    ids = catalogue_ids()
    uncovered = [i for i in ids if i not in seeded]
    with capsys.disabled():
        print("\nrule ids in the catalogue:", len(ids))
        print("rule ids with a seeded-defect test:", len([i for i in ids if i in seeded]))
        for i in ids:
            print(f"  {i:28} {len(seeded.get(i, ())):3} test(s)")
        print("without a test:", uncovered)
    assert uncovered == []
    assert DEFERRED == {}
    assert set(seeded) <= set(ids)
