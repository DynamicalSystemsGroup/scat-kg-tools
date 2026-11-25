"""`scat stub --help` lists the valid --type keys, `record-edge --help` the edge types, from the TBox."""

import pytest

from scat_kg.cli import _parser
from scat_kg.tbox import TBOX


def help_of(command, capsys):
    with pytest.raises(SystemExit):
        _parser().parse_args([command, "--help"])
    return " ".join(capsys.readouterr().out.split())


def test_stub_help_lists_every_type_key(capsys):
    out = help_of("stub", capsys)
    keys = [s for s, t in TBOX.page_types.items() if t.carries_status]
    assert len(keys) == 5
    for k in keys:
        assert k in out
    assert "one of: " + ", ".join((*TBOX.layers, "narrative")) in out


def test_record_edge_help_lists_the_edge_types(capsys):
    out = help_of("record-edge", capsys)
    for slug, e in TBOX.edge_types.items():
        assert f"{slug} ({e.from_type} then {e.to_type})" in out
    assert "--told-by" in out and "--note" in out and "REPL: " in out


def test_remove_edge_help_names_its_options(capsys):
    out = help_of("remove-edge", capsys)
    assert "FROM" in out and "TO" in out and "--told-by" in out and "REPL:" in out
