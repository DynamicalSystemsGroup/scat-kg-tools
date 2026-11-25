"""Every option of every fix of every seeded defect, applied from its data to a copy of the vault: the edits must
find their text where they say it is (machine interface, 'Fixes'), and the fix must clear its message and create no
other. Options of kind advisory or manual carry no edits and are skipped; author slots are filled."""

import pytest
from indep_kit import check_fix_clears
from test_seeded_defects import SEEDS

SLOTS = {
    "<node you choose>": "borrowers",
    "<one sentence you write>": "A sentence.",
    "<heading you choose>": "Told edges",
    "<number you choose>": "9",
}


@pytest.mark.parametrize("fn,st,allow", SEEDS)
def test_every_fix_of_every_seed_applies_and_clears(make_base, tmp_factory, fn, st, allow):
    v = make_base(st)
    fn(v, st)
    before = v.check()
    failures = []
    for p in before:
        if p.rule == "SCAT-CAP-CONFIG":
            continue  # the slot is the author's number, and the file is rewritten whole: covered by its own test
        failures += check_fix_clears(v, tmp_factory, p, before, SLOTS, no_other=False)
    assert not failures, "\n".join(failures)
