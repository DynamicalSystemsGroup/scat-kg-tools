"""WP24-R4: the review view never reads a narrative's `attributed_to` and never lists a contributor page.

The vaults are those of the evidence attribution tests, the G6 vault's three copies among them. For each, the
document is the same, byte for byte, with contributor pages added, with `attributed_to` stripped (where the mode
allows a narrative to name no one) and with `attributed_to` naming other contributors; and no contributor's name is
in it.
"""

import json
import shutil

import pytest
from test_evidence_attribution import (
    G6_PEOPLE,
    PEOPLE,
    VAULTS,
    add_contributors,
    names_in,
    set_attributed,
    strip_attributed,
)

import scat_tools


def document(root):
    view = scat_tools.review(root=root)
    assert view.ok, str(view)
    return view.to_dict()


def without_lines(d):
    """The document without the line of each twin row: a variant that adds or removes frontmatter lines moves it."""
    d = json.loads(json.dumps(d))
    for p in d["proposals"]:
        for t in p["twin_rows"]:
            del t["lines"]
    return d


@pytest.fixture(params=VAULTS, ids=[v[0] for v in VAULTS])
def made(request, tmp_path):
    _name, build, mode = request.param
    return build(tmp_path), mode


def test_the_document_carries_the_mode(made):
    root, mode = made
    d = document(root)
    assert d["mode"] == mode and d["proposals"] is not None
    assert str(scat_tools.review(root=root)).startswith(f"attribution mode: {mode}\n")


def test_adding_contributor_pages_changes_nothing(made, tmp_path):
    root, _ = made
    before = document(root)
    other = tmp_path / "with-pages"
    shutil.copytree(root, other)
    add_contributors(other, ("di-fox", "ed-wren", "zz-last", "aa-first"))
    assert document(other) == before


def test_no_contributor_is_in_the_document(made, tmp_path):
    root, _ = made
    other = tmp_path / "with-pages"
    shutil.copytree(root, other)
    add_contributors(other, ("di-fox", "ed-wren"))
    strings = names_in(document(other))
    for who in (*PEOPLE, *G6_PEOPLE, "di-fox", "ed-wren"):
        assert not any(who in s for s in strings), who


def test_stripping_attributed_to_changes_nothing(made, tmp_path):
    root, mode = made
    if mode == "required":
        pytest.skip("a required-mode narrative that names no one is an error")
    before = document(root)
    other = tmp_path / "stripped"
    shutil.copytree(root, other)
    strip_attributed(other)
    assert without_lines(document(other)) == without_lines(before)


def test_naming_other_contributors_changes_nothing(made, tmp_path):
    root, mode = made
    if mode == "disallowed":
        pytest.skip("a disallowed-mode narrative cannot name a contributor")
    before = document(root)
    other = tmp_path / "renamed"
    shutil.copytree(root, other)
    add_contributors(other, ("di-fox",))
    set_attributed(other, ("di-fox",))
    assert without_lines(document(other)) == without_lines(before)
