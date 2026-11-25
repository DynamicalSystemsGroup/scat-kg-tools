"""Setting `done` is judged as the page would stand at `done` (catalogue section 5, SCAT-DONE-REFUSED)."""

import json

import pytest
from opsutil import CAP3, fm, narrative
from tests_schema import VALIDATOR

import scat_kg
from scat_kg.cli import main
from scat_kg.ops import set_status
from scat_kg.vault import read_vault

DESC = 'description: "d"\n'
NARR_OK = 'description: "d"\ntimeframe: past\n'


def seed(make_vault, rows):
    """A draft narrative with `rows` and no description and no timeframe, with a group and a concern."""
    return make_vault(
        {
            **CAP3,
            "group/g.md": fm("group", "G", "done", DESC),
            "concern/c.md": fm("concern", "C", "done", DESC),
            "narrative/n.md": narrative("N", rows, "draft"),
        }
    )


def test_a_draft_with_an_end_that_is_no_link_and_no_description_is_refused_and_unchanged(
    make_vault, snap
):
    root = seed(make_vault, ["| holds | [[g]] | c | |"])
    before = snap(root)
    r = set_status("n", "done", root=root)
    assert not r.ok and snap(root) == before
    (ref,) = r.refused
    assert ref.rule == "SCAT-DONE-REFUSED" and ref.subject == "narrative/n.md"
    assert {p.rule for p in ref.problems} == {"SCAT-DONE-FIELD", "SCAT-DONE-END-NOLINK"}
    assert all(p.severity == "error" for p in ref.problems)
    text = str(r)
    assert text.startswith(
        "refused [SCAT-DONE-REFUSED] narrative/n.md: 3 error(s) would stand at status done; status unchanged\n"
    )
    assert "  error [SCAT-DONE-FIELD] narrative/n.md field `description`" in text
    assert text.endswith(
        "  Fix, choose one:\n"
        "    1. fix the problems above, then run `scat set-status n done` again\n"
        "    2. leave the page at `draft`: run `scat set-status n draft` "
        '(REPL: `scat_kg.set_status("n", "draft")`)'
    )


def test_the_same_narrative_with_both_fixed_is_set(make_vault):
    root = seed(make_vault, ["| holds | [[g]] | [[c]] | |"])
    page = root / "narrative/n.md"
    page.write_text(
        page.read_text(encoding="utf-8").replace(
            'title: "N"\n', 'title: "N"\ndescription: "d"\ntimeframe: past\n'
        ),
        encoding="utf-8",
    )
    r = set_status("n", "done", root=root)
    assert r.ok and r.changed == ("narrative/n.md",)
    assert read_vault(root).by_name["n"][0].status == "done"


def test_a_node_page_with_no_description_is_refused(make_vault, snap):
    root = make_vault({"concern/a.md": fm("concern", "A")})
    before = snap(root)
    r = set_status("a", "done", root=root)
    assert not r.ok and "SCAT-DONE-FIELD" in str(r) and snap(root) == before


def test_a_narrative_with_only_warnings_at_done_is_set(make_vault):
    root = make_vault(
        {
            **CAP3,
            "concern/quick.md": fm("concern", "Quick checkout", "done", DESC),
            "narrative/n.md": fm("narrative", "N", "draft", NARR_OK, "A quick checkout here.\n"),
        }
    )
    assert [p.rule for p in scat_kg.check("n", root=root).problems] == ["SCAT-MENTION"]
    assert set_status("n", "done", root=root).ok


def test_a_page_with_an_invalid_status_is_refused_and_the_status_error_is_listed(make_vault, snap):
    root = make_vault({"concern/a.md": fm("concern", "A", "finished", DESC)})
    before = snap(root)
    r = set_status("a", "done", root=root)
    assert not r.ok and "SCAT-FM-STATUS" in str(r)
    assert snap(root) == before


@pytest.mark.parametrize("status", ["stub", "draft"])
def test_stub_and_draft_are_never_refused(make_vault, status):
    root = seed(make_vault, ["| holds | [[g]] | c | |"])
    set_status("n", "done", root=root)  # refused; the page stays as it was
    assert set_status("n", "stub", root=root).ok
    assert set_status("n", status, root=root).ok


def test_vault_wide_errors_are_not_listed_and_do_not_block(make_vault):
    root = make_vault(
        {
            "scat.toml": "stakeholder_group_cap = 1\n",
            "group/a.md": fm("group", "A", "draft", DESC),
            "group/b.md": fm("group", "B", "draft", DESC),
        }
    )
    assert any(p.rule == "SCAT-CAP" for p in scat_kg.check(root=root).problems)
    assert set_status("a", "done", root=root).ok


def test_a_page_already_done_is_unchanged_not_judged_again(make_vault):
    root = make_vault(
        {"concern/a.md": fm("concern", "A", "done")}
    )  # no description: an error at done
    r = set_status("a", "done", root=root)
    assert r.ok and r.unchanged == ("concern/a.md",)


def test_the_refusal_data_and_the_cli_say_the_same(make_vault, capsys):
    a = seed(make_vault, ["| holds | [[g]] | c | |"])
    r = set_status("n", "done", root=a)
    doc = r.to_dict()
    assert VALIDATOR.is_valid(doc), list(VALIDATOR.iter_errors(doc))[:1]
    (ref,) = doc["refused"]
    assert ref["rule"] == "SCAT-DONE-REFUSED" and len(ref["problems"]) == 3
    assert ref["fix"]["kind"] == "options"
    adv, cmd = ref["fix"]["options"]
    assert adv["kind"] == "advisory" and cmd["kind"] == "exact"
    assert cmd["command"] == {
        "argv": ["set-status", "n", "draft"],
        "repl": 'scat_kg.set_status("n", "draft")',
    }
    assert [p["text"] for p in ref["problems"]] == [p.render() for p in r.refused[0].problems]
    code = main(["set-status", "n", "done", "--json", "--root", str(a)])
    assert code == 1 and json.loads(capsys.readouterr().out) == doc
    code = main(["set-status", "n", "done", "--root", str(a)])
    assert code == 1 and capsys.readouterr().out == str(r) + "\n"
