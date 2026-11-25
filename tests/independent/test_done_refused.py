"""SCAT-DONE-REFUSED (catalogue section 5): an operation rule, never printed by `scat check`."""

from indep_kit import NARRATIVE_FILE as NF
from indep_kit import page_text


def _refusal(doc):
    assert doc["ok"] is False and doc["kind"] == "operation"
    (r,) = doc["refused"]
    assert r["rule"] == "SCAT-DONE-REFUSED"
    return r


def test_refused_lists_every_error_and_writes_nothing(make_base):
    v = make_base("draft")
    v.edit(NF, 'description: "A Saturday at the lending desk."\n', "")
    v.edit(NF, "| [[borrowers]] | holds", "| borrowers | holds")
    before = v.snapshot()
    code, doc = v.scat("set-status", "saturday", "done")
    assert code == 1
    r = _refusal(doc)
    assert (
        r["subject"] == NF and r["why"] == "2 error(s) would stand at status done; status unchanged"
    )
    assert sorted(p["rule"] for p in r["problems"]) == ["SCAT-DONE-END-NOLINK", "SCAT-DONE-FIELD"]
    assert all(p["severity"] == "error" for p in r["problems"])
    assert v.snapshot() == before
    texts = [o["text"] for o in r["fix"]["options"]]
    assert len(texts) == 2 and "scat set-status saturday draft" in texts[1]
    assert r["fix"]["options"][1]["kind"] == "exact"
    # each listed problem is exactly as `scat check` prints it once the page stands at done
    v.edit(NF, "status: draft", "status: done")
    assert sorted(p["text"] for p in r["problems"]) == sorted(p.text for p in v.check())


def test_the_same_page_with_both_fixed_is_set_done(make_base):
    v = make_base("draft")
    code, doc = v.scat("set-status", "saturday", "done")
    assert code == 0 and doc["ok"] and NF in doc["changed"]
    assert v.status_of("saturday") == "done"


def test_node_page_without_description_is_refused(make_base):
    v = make_base("draft")
    v.write("concern/lending-desk.md", page_text("concern", "Lending desk", "draft", None))
    _code, doc = v.scat("set-status", "lending-desk", "done")
    r = _refusal(doc)
    assert [p["rule"] for p in r["problems"]] == ["SCAT-DONE-FIELD"]


def test_only_warnings_at_done_do_not_block(make_base):
    v = make_base("draft")
    v.edit(
        NF,
        "through [[self-checkout]].",
        "through [[self-checkout]]. The safe handling of tools mattered.",
    )
    assert [p.rule for p in v.check()] == ["SCAT-MENTION"]
    code, doc = v.scat("set-status", "saturday", "done")
    assert code == 0 and doc["ok"]
    assert [p.rule for p in v.check()] == ["SCAT-MENTION"]


def test_invalid_status_is_refused_with_the_status_error_listed(make_base):
    v = make_base("draft")
    v.write("concern/odd-page.md", page_text("concern", "Odd page", "finished"))
    _code, doc = v.scat("set-status", "odd-page", "done")
    r = _refusal(doc)
    assert "SCAT-FM-STATUS" in [p["rule"] for p in r["problems"]]


def test_stub_and_draft_are_never_refused(make_base):
    v = make_base("done")
    v.edit(NF, "| [[borrowers]] | holds", "| borrowers | holds")
    for target in ("draft", "stub"):
        code, doc = v.scat("set-status", "saturday", target)
        assert code == 0 and doc["ok"], doc
        assert v.status_of("saturday") == target


def test_check_never_prints_the_refusal_rule(make_base):
    v = make_base("done")
    v.edit(NF, "| [[borrowers]] | holds", "| borrowers | holds")
    assert all(p.rule != "SCAT-DONE-REFUSED" for p in v.check())


def test_vault_wide_cap_error_is_not_listed_in_the_refusal(make_base):
    v = make_base("draft", cap=1)  # two groups over a cap of one
    v.write("group/elders.md", page_text("group", "Elders", "draft"))
    code, doc = v.scat("set-status", "elders", "done")
    assert (
        code == 0 and doc["ok"]
    )  # description present: only the cap would be wrong, and it is not listed
    assert any(p.rule == "SCAT-CAP" for p in v.check())
