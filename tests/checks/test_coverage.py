"""Every rule in the catalogue has a seeded-defect test.

A seeded-defect test is named `test__<rule id, lower case, - as _>__<what is seeded>`. A pair of rules (a
`SCAT-DRAFT-X` and a `SCAT-DONE-X`) has one seed set, run at each status, and its tests carry the DRAFT id: the DONE
id is covered when the same tests run at `done`, which the coverage test below checks by what the session saw.
"""

import re

from helpers import CATALOGUE, catalogue_severities

from scat_kg.checks import DEFERRED, SEVERITY


def catalogue_ids() -> list[str]:
    text = CATALOGUE.read_text(encoding="utf-8")
    return re.findall(r"^\| (SCAT-[A-Z-]+) \| (?:error|warning) \|", text, re.MULTILINE)


def test__the_registry_knows_every_rule_in_the_catalogue():
    ids = catalogue_ids()
    assert len(ids) == len(set(ids)) == 33
    assert set(ids) == set(SEVERITY)
    assert catalogue_severities() == SEVERITY


def test__every_rule_has_a_seeded_test(request, capsys):
    seeded = {}
    for item in request.session.items:
        parts = (item.originalname or item.name).split("__")
        if parts[0] == "test" and len(parts) >= 3 and parts[1].startswith("scat_"):
            seeded.setdefault(parts[1].upper().replace("_", "-"), set()).add(item.name)
    ids = catalogue_ids()
    # a pair is covered by its DRAFT form's tests, which run at the three statuses (and so produce the DONE id)
    covered = {i: seeded.get(i) or seeded.get(i.replace("-DONE-", "-DRAFT-")) for i in ids}
    uncovered = [i for i in ids if not covered[i]]
    with capsys.disabled():
        print("\nrule ids in the catalogue:", len(ids))
        print("rule ids with a seeded-defect test:", len(ids) - len(uncovered))
        for i in ids:
            print(f"  {i:34} {len(covered[i] or ()):3} test(s)")
        print("without a test:", uncovered)
    assert uncovered == []
    assert DEFERRED == {}
    assert {i.replace("-DONE-", "-DRAFT-") for i in seeded} <= {
        i.replace("-DONE-", "-DRAFT-") for i in ids
    }
