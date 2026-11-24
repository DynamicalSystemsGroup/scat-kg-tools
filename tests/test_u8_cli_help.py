"""WP5-U8: `scat stub --help` lists the valid --type keys and `stub-pair --help` the relations, from the TBox."""

import pytest

from scat_kg.cli import _parser
from scat_kg.tbox import TBOX


def help_of(command, capsys):
    with pytest.raises(SystemExit):
        _parser().parse_args([command, "--help"])
    return " ".join(capsys.readouterr().out.split())


def test_stub_help_lists_every_type_key(capsys):
    out = help_of("stub", capsys)
    keys = [s for s, t in TBOX.page_types.items() if t.endpoint_order is None and s != "class"]
    assert len(keys) == 8
    for k in keys:
        assert k in out
    assert "one of: " + ", ".join(keys) in out


def test_stub_pair_help_lists_the_relations(capsys):
    out = help_of("stub-pair", capsys)
    for r, (a, b) in TBOX.relations.items():
        assert f"{r} ({a} then {b})" in out
