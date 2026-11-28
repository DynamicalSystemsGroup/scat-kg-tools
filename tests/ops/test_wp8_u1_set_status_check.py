"""WP8-U1: `set-status done` reports the page's own check (R-8: API and `scat` give the same text)."""

import shutil

import pytest
from opsutil import fm

from scat_tools import cli
from scat_tools.ops import set_status

CAP = {"scat.toml": "attribution = 'disallowed'\nstakeholder_group_cap = 3\n"}
GOOD = {**CAP, "concern/a.md": fm("concern", "A", "draft", 'description: "Fine."\n')}
# already done by hand: set-status refuses to make a page with errors done (SCAT-DONE-REFUSED)
BARE_DONE = {**CAP, "concern/a.md": fm("concern", "A", "done")}


def run(capsys, *argv, root):
    code = cli.main([*argv, "--root", str(root)])
    return code, capsys.readouterr().out


def test_done_reports_the_errors_the_page_has_with_their_fix(make_vault, snap):
    root = make_vault(BARE_DONE)
    before = snap(root)
    r = set_status("a", "done", root=root)
    text = str(r)
    assert r.ok and r.unchanged == ("concern/a.md",)  # not a refusal: the status was already done
    assert "error [SCAT-DONE-FIELD] concern/a.md field `description`" in text
    assert 'add the line `description: "<one sentence you write>"`' in text
    assert text.endswith("check of concern/a.md: 1 error, 0 warnings")
    assert snap(root) == before  # the check wrote nothing


def test_done_on_a_page_that_passes_says_so(make_vault):
    r = set_status("a", "done", root=make_vault(GOOD))
    assert r.ok and r.changed == ("concern/a.md",)
    assert str(r).splitlines()[-1] == "check of concern/a.md: no problems"


def test_done_when_already_done_and_passing_reports_the_check(make_vault, snap):
    root = make_vault(GOOD)
    set_status("a", "done", root=root)
    before = snap(root)
    r = set_status("a", "done", root=root)
    assert r.unchanged == ("concern/a.md",)
    assert str(r).splitlines()[-1] == "check of concern/a.md: no problems"
    assert snap(root) == before


@pytest.mark.parametrize("status", ["stub", "draft"])
def test_other_statuses_do_not_report_a_check(make_vault, status):
    r = set_status(
        "a", status, root=make_vault({**GOOD, "concern/a.md": fm("concern", "A", "done")})
    )
    assert "check of" not in str(r) and not r.problems


def test_done_cli_prints_the_api_text_and_exits_zero(make_vault, tmp_path_factory, capsys):
    root = make_vault(BARE_DONE)
    twin = tmp_path_factory.mktemp("twin") / "v"
    shutil.copytree(root, twin)
    code, out = run(capsys, "set-status", "a", "done", root=root)
    assert code == 0
    assert out == str(set_status("a", "done", root=twin)) + "\n"
    assert "check of concern/a.md: 1 error, 0 warnings" in out
