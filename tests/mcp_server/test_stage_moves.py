"""WP30-R4, R5, R6, R7: the detect readers, which_stage, set_stage (every transition L1 to L12), persistence, schema."""

import tomllib

import pytest
from mcputil import snapshot
from test_stage_common import (
    INST,
    STAGES,
    all_done,
    call_all,
    call_one,
    fix_text,
    valid,
    vault,
)

import scat_tools
from scat_tools import guides
from scat_tools.mcp_server import detects, stage

DONE = "every narrative is done and the whole-vault check has no errors"


def _lifecycle(root, text):
    (root / "lifecycle.toml").write_text(text, encoding="utf-8")


def _in(root, stage_name, extra=""):
    _lifecycle(root, f'stage = "{stage_name}"\nset_by = "Ada"\n{extra}')


# ---- R4: the detect readers


def test_every_detect_has_a_reader_and_every_reader_a_detect():
    assert set(detects.READERS) == set(INST["detects"]) == {DONE}


def test_narratives_done_holds_and_does_not(tmp_path):
    ok = vault(tmp_path / "ok")
    all_done(ok)
    assert scat_tools.check(root=ok).ok
    assert detects.evaluate(DONE, ok) == (True, "3 of 3 narratives done; the check has 0 errors")
    # one narrative is not done (the example as it is: one draft)
    one = vault(tmp_path / "one")
    assert detects.evaluate(DONE, one) == (False, "2 of 3 narratives done; the check has 0 errors")
    # a stub narrative
    stub = vault(tmp_path / "stub")
    all_done(stub)
    page = stub / "narrative" / "saturday-at-the-lending-desk.md"
    page.write_text(
        page.read_text("utf-8").replace("status: done", "status: stub"), encoding="utf-8"
    )
    assert detects.evaluate(DONE, stub)[0] is False
    assert "2 of 3 narratives done" in detects.evaluate(DONE, stub)[1]
    # every narrative done but the check has errors
    bad = vault(tmp_path / "bad")
    page = bad / "narrative" / "funders-meeting.md"
    page.write_text(
        page.read_text("utf-8").replace("status: draft", "status: done"), encoding="utf-8"
    )
    holds, detail = detects.evaluate(DONE, bad)
    assert holds is False and detail == "3 of 3 narratives done; the check has 2 errors"


def test_narratives_done_with_no_narrative_does_not_hold(tmp_path):
    root = vault(tmp_path / "v")
    for page in (root / "narrative").glob("*.md"):
        page.unlink()
    holds, detail = detects.evaluate(DONE, root)
    assert holds is False and "no narratives" in detail


def _exits(root, name="code"):
    return {e["id"]: e for e in call_one(root, "which_stage")["exits"]}


def test_which_stage_shows_each_detect_with_holds_and_detail(tmp_path):
    root = vault(tmp_path / "v", cap=3)
    ex = _exits(root)
    assert ex["L5"]["predicate"] == {
        "kind": "detect",
        "check": DONE,
        "holds": False,
        "detail": "2 of 3 narratives done; the check has 0 errors",
    }
    assert ex["L7"]["predicate"]["kind"] == "person"
    assert ex["L7"]["decides"] == "organiser"
    all_done(root)
    assert _exits(root)["L5"]["predicate"]["holds"] is True


# ---- which_stage


def test_which_stage_in_a_stage(tmp_path):
    root = vault(tmp_path / "v", stage="capture")
    _in(root, "capture")
    doc = call_one(root, "which_stage")
    spec = INST["stages"]["capture"]
    assert (
        valid(doc)
        and doc["kind"] == "stage"
        and doc["operation"] == "which-stage"
        and doc["ok"] is True
    )
    assert doc["stage"] == "capture" and doc["set_by"] == "Ada"
    assert "set_at" not in doc and "pending" not in doc and doc["mode"] == "disallowed"
    assert doc["work"] == spec["work"] and doc["required_inputs"] == spec["required_inputs"]
    assert doc["tools"] == spec["tools"] and doc["prompts"] == spec["prompts"]
    assert [e["id"] for e in doc["exits"]] == ["L4", "L12"] and doc[
        "guide"
    ] == "scat://guide/capture"
    assert "capture" in doc["text"]


def test_which_stage_when_unknown(tmp_path):
    root = vault(tmp_path / "v", stage=None)
    doc = call_one(root, "which_stage")
    assert valid(doc) and doc["stage"] == "unknown" and doc["set_by"] is None
    assert "set_at" not in doc and "pending" not in doc
    assert [s["name"] for s in doc["stages"]] == STAGES
    assert [e["id"] for e in doc["exits"]] == ["L1"] and doc["exits"][0]["to"] == "any"
    assert "problem" not in doc
    _lifecycle(root, "stage = [[[\n")
    bad = call_one(root, "which_stage")
    assert valid(bad) and bad["stage"] == "unknown" and "not valid TOML" in bad["problem"]
    assert "not valid TOML" in bad["text"]


# ---- set_stage: every transition


def _state(root):
    return stage.read_state(root)


def _check_made(root, doc, frm, to, tid, by="Dana Quill"):
    assert valid(doc), doc
    assert doc["kind"] == "stage" and doc["operation"] == "set-stage" and doc["ok"] is True
    assert (
        doc["moved"] is True and doc["from"] == frm and doc["to"] == to and doc["transition"] == tid
    )
    assert doc["stage"] == to and doc["set_by"] == by
    assert "set_at" not in doc and "pending" not in doc
    assert doc["decides"] == next(t["decides"] for t in INST["transitions"] if t["id"] == tid)
    assert [e["id"] for e in doc["exits"]] == [
        t["id"] for t in INST["transitions"] if t["from"] == to
    ]
    st = _state(root)
    assert (st.stage, st.set_by) == (to, by)
    assert tomllib.loads((root / "lifecycle.toml").read_text("utf-8")) == {
        "stage": to,
        "set_by": by,
    }


CASES = [
    (t["id"], t["from"], to)
    for t in INST["transitions"]
    for to in (STAGES if t["to"] == "any" else [t["to"]])
]


def test_the_cases_cover_l1_to_l12():
    assert {c[0] for c in CASES} == {f"L{n}" for n in range(1, 13)} and len(CASES) == 16


@pytest.mark.parametrize(("tid", "frm", "to"), CASES)
def test_every_listed_move_is_made_with_by_and_written(tmp_path, tid, frm, to):
    root = vault(tmp_path / "v", stage=None if frm == "unknown" else frm)
    if frm != "unknown":
        # an old file's `set_at` and `[pending]` table are ignored, and the write keeps `stage` and `set_by` only
        _in(
            root,
            frm,
            'set_at = "2026-02-03T04:05:06Z"\n\n[pending]\nto = "plan"\nrequested_at = "2026-02-03T05:00:00Z"\n',
        )
    doc = call_one(root, "set_stage", {"to": to, "by": "  Dana Quill "})
    _check_made(root, doc, frm, to, tid)


@pytest.mark.parametrize("cap", [3, 4, None])
def test_code_to_plan_is_l7_on_a_persons_word_with_or_without_the_cap(tmp_path, cap):
    root = vault(tmp_path / "v", stage="code", cap=cap)
    doc = call_one(root, "set_stage", {"to": "plan", "by": "Dana Quill"})
    _check_made(root, doc, "code", "plan", "L7")
    assert doc["decides"] == "organiser" and doc["advisory"] == []
    assert len([t for t in INST["transitions"] if (t["from"], t["to"]) == ("code", "plan")]) == 1


def test_a_failed_detect_gives_an_advisory_and_the_move_is_still_made(tmp_path):
    root = vault(tmp_path / "v", stage="code")  # one narrative is a draft: L5 does not hold
    doc = call_one(root, "set_stage", {"to": "analyse", "by": "Dana"})
    _check_made(root, doc, "code", "analyse", "L5", by="Dana")
    assert len(doc["advisory"]) == 1 and "2 of 3 narratives done" in doc["advisory"][0]
    assert "L5" in doc["advisory"][0] and "anyway" in doc["advisory"][0]
    ready = vault(tmp_path / "w", stage="code")
    all_done(ready)
    doc = call_one(ready, "set_stage", {"to": "analyse", "by": "Dana"})
    assert doc["moved"] is True and doc["advisory"] == []


def test_a_move_without_a_name_is_refused_and_writes_nothing(tmp_path):
    asks = ({"to": "analyse"}, {"to": "analyse", "by": ""}, {"to": "analyse", "by": "  \t "})
    for n, args in enumerate(asks):
        root = vault(tmp_path / f"v{n}", stage="code")
        _in(root, "code")
        before = snapshot(root)
        doc = call_one(root, "set_stage", args)
        assert valid(doc) and doc["kind"] == "operation" and doc["ok"] is False
        assert doc["operation"] == "set-stage" and "`by` is needed" in doc["refused"][0]["why"]
        assert "name" in fix_text(doc) and snapshot(root) == before
        assert "pending" not in (root / "lifecycle.toml").read_text("utf-8")
        assert "pending" not in call_one(root, "which_stage")
    unknown = vault(tmp_path / "u", stage=None)
    before = snapshot(unknown)
    doc = call_one(unknown, "set_stage", {"to": "plan"})
    assert doc["ok"] is False and "`by` is needed" in doc["refused"][0]["why"]
    assert snapshot(unknown) == before and _state(unknown).stage is None


@pytest.mark.parametrize(
    ("frm", "to", "says"),
    [
        ("plan", "analyse", "no transition from plan to analyse"),
        ("code", "code", "already in the code stage"),
        ("plan", "launch", "not a stage"),
        ("report", "plan", "no transition from report to plan"),
    ],
)
def test_an_unlisted_move_the_same_stage_and_an_unknown_name_are_refused_and_write_nothing(
    tmp_path, frm, to, says
):
    root = vault(tmp_path / "v", stage=frm)
    _in(root, frm)
    for by in ("Dana", None):
        before = snapshot(root)
        doc = call_one(root, "set_stage", {"to": to, **({"by": by} if by else {})})
        assert valid(doc) and doc["ok"] is False and doc["kind"] == "operation"
        assert doc["operation"] == "set-stage" and says in doc["refused"][0]["why"]
        assert snapshot(root) == before
    exits = [t["id"] for t in INST["transitions"] if t["from"] == frm]
    if to == "launch":
        assert all(s in doc["refused"][0]["why"] for s in STAGES)
    else:
        assert all(e in fix_text(doc) for e in exits)


def test_a_malformed_file_is_overwritten_only_by_a_move_with_a_name(tmp_path):
    root = vault(tmp_path / "v", stage=None)
    _lifecycle(root, "stage = [[[\n")
    before = snapshot(root)
    doc = call_one(root, "set_stage", {"to": "code"})
    assert doc["ok"] is False and "`by` is needed" in doc["refused"][0]["why"]
    assert snapshot(root) == before
    doc = call_one(root, "set_stage", {"to": "code", "by": "Dana"})
    _check_made(root, doc, "unknown", "code", "L1", by="Dana")


def test_an_old_file_with_set_at_and_pending_is_read_and_stray_keys_are_dropped_on_write(tmp_path):
    root = vault(tmp_path / "v", stage=None)
    _lifecycle(
        root,
        'stage = "code"\nset_by = "Ada"\nset_at = "2026-02-03T04:05:06Z"\nextra = 1\n\n'
        '[pending]\nto = "analyse"\nrequested_at = "2026-02-03T05:00:00Z"\n',
    )
    assert (_state(root).stage, _state(root).set_by) == ("code", "Ada")
    doc = call_one(root, "which_stage")
    assert valid(doc) and doc["stage"] == "code" and doc["set_by"] == "Ada"
    assert "set_at" not in doc and "pending" not in doc
    call_one(root, "set_stage", {"to": "analyse", "by": "Dana"})
    assert tomllib.loads((root / "lifecycle.toml").read_text("utf-8")) == {
        "stage": "analyse",
        "set_by": "Dana",
    }


def test_a_file_with_an_unknown_stage_name_is_replaced_by_a_move_with_a_name(tmp_path):
    root = vault(tmp_path / "v", stage=None)
    _lifecycle(root, 'stage = "launch"\n')
    doc = call_one(root, "set_stage", {"to": "plan", "by": "Dana"})
    _check_made(root, doc, "unknown", "plan", "L1", by="Dana")


def test_by_is_written_as_a_toml_string_whatever_it_holds(tmp_path):
    root = vault(tmp_path / "v", stage=None)
    odd = 'Dana "the coder" \\ Quill\u00e9\u2603'
    call_one(root, "set_stage", {"to": "plan", "by": odd})
    assert _state(root).set_by == odd


def test_the_write_is_atomic_and_leaves_no_temp_file(tmp_path):
    root = vault(tmp_path / "v", stage=None)
    call_one(root, "set_stage", {"to": "plan", "by": "Dana"})
    assert not [p for p in root.iterdir() if p.name.startswith(".lifecycle-")]
    # a failed replace leaves the old file and no temp file
    before = snapshot(root)
    import os

    real = os.replace
    os.replace = lambda *a: (_ for _ in ()).throw(OSError("disk"))
    try:
        with pytest.raises(OSError):
            stage.write_state(root, "code", "x")
    finally:
        os.replace = real
    assert snapshot(root) == before


# ---- R5: the stage is the file


def test_a_second_server_and_a_restart_see_the_stage_the_first_one_set(tmp_path):
    root = vault(tmp_path / "v", stage=None)
    first = call_one(root, "set_stage", {"to": "capture", "by": "Dana"})
    assert first["moved"] is True
    for _ in range(2):  # each call builds a new server on the vault
        doc = call_one(root, "which_stage")
        assert (doc["stage"], doc["set_by"]) == ("capture", "Dana")
    assert call_one(root, "status")["ok"] is True
    assert (
        call_one(root, "stub", {"name": "x-group", "type": "group"})["refused"][0]["subject"]
        == "tool `stub`"
    )


def test_a_move_by_hand_in_the_file_is_seen_at_once(tmp_path):
    root = vault(tmp_path / "v", stage="plan")
    docs = call_all(root, [("which_stage", {})])
    _in(root, "analyse")
    assert docs[0]["stage"] == "plan" and call_one(root, "which_stage")["stage"] == "analyse"


# ---- R6: check and status do not see lifecycle.toml


def test_check_and_status_give_the_same_documents_with_and_without_lifecycle_toml(tmp_path):
    variants = {
        "none": None,
        "valid": 'stage = "code"\nset_by = "Ada"\n',
        "old-keys": 'stage = "plan"\nset_at = "2026-02-03T04:05:06Z"\n\n[pending]\nto = "capture"\n',
        "unknown-name": 'stage = "launch"\n',
        "malformed": "stage = [[[\n\x00\n",
    }
    docs = {}
    for name, text in variants.items():
        root = vault(tmp_path / name, stage=None)
        if text is not None:
            _lifecycle(root, text)
        docs[name] = [
            scat_tools.check(root=root).to_dict(),
            scat_tools.status(root=root).to_dict(),
            scat_tools.check("funders-meeting", neighborhood=True, root=root).to_dict(),
        ]
    assert all(d == docs["none"] for d in docs.values())
    root = vault(tmp_path / "served", stage=None)
    _lifecycle(root, variants["valid"])
    assert (
        call_one(root, "check") == docs["none"][0] and call_one(root, "status") == docs["none"][1]
    )


# ---- R7: the documents validate


def test_the_stage_documents_and_refusals_validate_against_the_schema(tmp_path):
    root = vault(tmp_path / "v", stage=None)
    docs = call_all(
        root,
        [
            ("which_stage", {}),
            ("check", {}),
            ("set_stage", {"to": "plan"}),
            ("set_stage", {"to": "nowhere", "by": "D"}),
            ("which_stage", {}),
            ("set_stage", {"to": "plan", "by": "D"}),
            ("which_stage", {}),
            ("set_stage", {"to": "plan", "by": "D"}),
            ("set_stage", {"to": "analyse", "by": "D"}),
            ("set_stage", {"to": "capture"}),
            ("set_stage", {"to": "code", "by": "D"}),
            ("set_stage", {"to": "analyse", "by": "D"}),
            ("stub", {"name": "a", "type": "concern"}),
            ("which_stage", {}),
        ],
    )
    kinds = [(d["kind"], d["operation"], d["ok"]) for d in docs]
    assert ("stage", "which-stage", True) in kinds and ("stage", "set-stage", True) in kinds
    assert ("operation", "set-stage", False) in kinds and ("operation", "check", False) in kinds
    assert ("operation", "stub", False) in kinds
    for d in docs:
        assert valid(d), d
    assert any(d.get("moved") is True and d["advisory"] for d in docs)
    assert not any("pending" in d or "set_at" in d for d in docs)


def test_the_guide_names_every_move_the_server_can_make():
    assert {t["id"] for t in INST["transitions"]} == {f"L{n}" for n in range(1, 13)}
    assert guides.STAGES == tuple(STAGES)
