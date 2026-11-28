"""The clean fixture gives zero messages at every status and scope; the CLI process gives the same as the API call."""

import json
import subprocess
import sys
from pathlib import Path

import pytest
from indep_kit import NARRATIVE_FILE, STATUSES


@pytest.mark.parametrize("st", STATUSES)
def test_clean_vault_has_zero_messages(make_base, st):
    v = make_base(st)
    assert [p.brief() for p in v.check()] == []
    assert [p.brief() for p in v.check(NARRATIVE_FILE)] == []
    assert [p.brief() for p in v.check("saturday", neighborhood=True)] == []


def test_real_process_prints_what_the_entry_point_returns(make_base):
    v = make_base("done")
    v.edit(NARRATIVE_FILE, "| [[borrowers]] | holds", "| borrowers | holds")
    v.edit(NARRATIVE_FILE, "[[borrowers]] queued", "people queued")  # the account links no non-end
    scat = Path(sys.executable).parent / "scat"
    proc = subprocess.run(
        [str(scat), "check", "--json", "--root", str(v.root)],
        check=False,
        capture_output=True,
        text=True,
    )
    doc = json.loads(proc.stdout)
    assert proc.returncode == 1 and doc["schema_version"] == 3
    assert [p["text"] for p in doc["problems"]] == [p.text for p in v.check()]
    assert doc["problems"][0]["rule"] == "SCAT-DONE-END-NOLINK"
