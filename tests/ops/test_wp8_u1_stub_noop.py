"""WP8-U1: `stub` on an existing page of the same type is a no-op (R-8: API and `scat` give the same text)."""

from opsutil import fm

from scat_kg import cli
from scat_kg.ops import stub

GOOD = {
    "scat.toml": "attribution = 'disallowed'\nstakeholder_group_cap = 3\n",
    "concern/a.md": fm("concern", "A", "draft", 'description: "Fine."\n'),
}


def run(capsys, *argv, root):
    code = cli.main([*argv, "--root", str(root)])
    return code, capsys.readouterr().out


def test_stub_same_type_is_a_no_op_with_a_plain_message(make_vault, snap):
    root = make_vault(GOOD)
    before = snap(root)
    r = stub("a", "concern", root=root)
    assert r.ok and not r.created and not r.changed and r.unchanged == ("concern/a.md",)
    assert str(r) == (
        "unchanged concern/a.md\nnote: concern/a.md already exists, so nothing was written"
    )
    assert snap(root) == before  # not even mtime


def test_stub_other_type_on_an_existing_page_is_still_refused(make_vault, snap):
    root = make_vault(GOOD)
    before = snap(root)
    r = stub("a", "affordance", root=root)
    assert not r.ok and "already" in str(r) and "Fix:" in str(r)
    assert snap(root) == before


def test_stub_same_type_cli_prints_the_api_text_and_exits_zero(make_vault, snap, capsys):
    root = make_vault(GOOD)
    before = snap(root)
    code, out = run(capsys, "stub", "a", "--type", "concern", root=root)
    assert code == 0 and out == str(stub("a", "concern", root=root)) + "\n"
    assert "already exists, so nothing was written" in out
    assert snap(root) == before
    code, out = run(capsys, "stub", "a", "--type", "affordance", root=root)
    assert code == 1 and "refused" in out
