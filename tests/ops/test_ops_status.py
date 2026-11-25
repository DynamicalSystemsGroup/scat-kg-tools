import difflib

import pytest
from opsutil import fm, narrative

from scat_kg.ops import StatusReport, read_status, set_status


def lines_changed(old: bytes, new: bytes) -> list[str]:
    return [
        l for l in difflib.unified_diff(old.decode().splitlines(True), new.decode().splitlines(True), n=0)
        if l[0] in "+-" and l[:3] not in ("+++", "---")
    ]  # fmt: skip


@pytest.fixture
def vault(make_vault):
    return make_vault(
        {
            "scat.toml": "stakeholder_group_cap = 3\n",
            "concern/a.md": fm("concern", "A", "stub", "", "Pulls against [[b]]; see [[c]]\n"),
            "concern/b.md": fm("concern", "B", "done"),
            "concern/c.md": fm("concern", "C", "draft"),
            "concern/d.md": fm("concern", "D", "stub"),
            "narrative/h.md": narrative("H", ["| holds | [[g]] | [[a]] | |"], "draft"),
            "group/g.md": fm("group", "G", "done"),
            "concern/far.md": fm("concern", "Far", "done", "", "Pulls against [[d]]\n"),
        }
    )


def rows(report):
    return {r.name: r.status for r in report.rows}


def test_status_page_scope(vault):
    r = read_status("page", "a", root=vault)
    assert isinstance(r, StatusReport) and r.ok
    assert rows(r) == {"a": "stub"}
    assert read_status("page", "concern/a.md", root=vault).rows == r.rows  # by path too


def test_status_neighborhood_is_one_link_either_direction(vault):
    r = read_status("neighborhood", "a", root=vault)
    # out: b and c (body); in: h (a narrative whose row ends link a). Not g (two away), not d, far.
    assert [x.name for x in r.rows] == ["a", "b", "c", "h"]
    assert rows(r) == {"a": "stub", "b": "done", "c": "draft", "h": "draft"}
    assert r.counts == {"stub": 1, "draft": 2, "done": 1, "other": 0}


def test_status_neighborhood_follows_inbound_only_links(vault):
    assert [x.name for x in read_status("neighborhood", "d", root=vault).rows] == ["d", "far"]


def test_status_vault_scope_counts_every_page_by_status(vault):
    r = read_status("vault", root=vault)
    assert len(r.rows) == 7
    assert r.counts == {
        "stub": 2,
        "draft": 2,
        "done": 3,
        "other": 0,
    }  # no `none`: every type has a status
    assert "(no status" not in str(r)


def test_status_missing_and_invalid_count_as_other(make_vault):
    root = make_vault(
        {"concern/x.md": "---\ntype: concern\ntitle: X\n---\n", "concern/y.md": "---\ntype: concern\nstatus: Done\n---\n"}
    )  # fmt: skip
    r = read_status("vault", root=root)
    assert r.counts["other"] == 2
    assert "(missing)" in str(r) and "Done" in str(r)


def test_status_refusals(vault):
    assert not read_status("page", "nope", root=vault).ok
    assert not read_status("page", None, root=vault).ok
    assert not read_status("planet", "a", root=vault).ok
    assert not read_status("vault", root=vault / "missing").ok


def test_status_never_writes(vault, snap):
    before = snap(vault)
    for scope in ("page", "neighborhood", "vault"):
        read_status(scope, "a", root=vault)
    assert snap(vault) == before


# set_status


def test_set_status_edits_only_the_status_line(vault, snap, diff):
    before = snap(vault)
    old = (vault / "concern/a.md").read_bytes()
    r = set_status("a", "draft", root=vault)
    assert r.ok and r.changed == ("concern/a.md",)
    assert diff(before, snap(vault)) == {"concern/a.md": "changed"}  # nothing else, byte for byte
    assert lines_changed(old, (vault / "concern/a.md").read_bytes()) == [
        "-status: stub\n",
        "+status: draft\n",
    ]


def test_set_status_is_idempotent_and_reports_it(vault, snap):
    set_status("a", "draft", root=vault)
    before = snap(vault)
    r = set_status("a", "draft", root=vault)
    assert r.ok and r.unchanged == ("concern/a.md",) and not r.changed
    assert snap(vault) == before  # not even rewritten (mtime too)


def test_set_status_keeps_crlf_bom_comment_and_quotes(make_vault):
    text = (
        '---\r\ntype: concern\r\nstatus: "stub"   # to do\r\ntitle: "A"\r\n---\r\nBody\r\n\r\nend'
    )
    root = make_vault({"a.md": b"\xef\xbb\xbf" + text.encode()})
    set_status("a", "draft", root=root)
    assert (root / "a.md").read_bytes() == b"\xef\xbb\xbf" + text.replace(
        '"stub"', "draft"
    ).encode()


def test_set_status_adds_the_key_after_type_with_the_files_line_ending(make_vault):
    root = make_vault({"a.md": b'---\r\ntype: concern\r\ntitle: "A"\r\n---\r\nBody'})
    r = set_status("a", "draft", root=root)
    assert r.ok
    assert (
        root / "a.md"
    ).read_bytes() == b'---\r\ntype: concern\r\nstatus: draft\r\ntitle: "A"\r\n---\r\nBody'


def test_set_status_fills_an_empty_status_value(make_vault):
    root = make_vault({"a.md": '---\ntype: concern\nstatus:\ntitle: "A"\n---\n'})
    set_status("a", "stub", root=root)
    assert (root / "a.md").read_text() == '---\ntype: concern\nstatus: stub\ntitle: "A"\n---\n'


def test_set_status_does_not_touch_status_text_in_the_body(make_vault):
    root = make_vault({"a.md": "---\ntype: concern\nstatus: stub\n---\nstatus: stub\n"})
    set_status("a", "draft", root=root)
    assert (root / "a.md").read_text() == "---\ntype: concern\nstatus: draft\n---\nstatus: stub\n"


@pytest.mark.parametrize(
    "files, ref, status, word",
    [
        ({"concern/a.md": fm("concern", "A")}, "a", "finished", "not a status"),
        ({"concern/a.md": fm("concern", "A")}, "zzz", "done", "no page"),
        ({"x/a.md": fm("concern", "A"), "y/a.md": fm("concern", "A")}, "a", "done", "more than one"),
        ({"a.md": "---\ntype: index\n---\n"}, "a", "done", "not the type of a page"),
        ({"a.md": "---\ntype: [oops\n---\n"}, "a", "done", "frontmatter cannot be read"),
        ({"a.md": "---\ntype: 5\n---\n"}, "a", "done", "not the type of a page"),
        ({"a.md": b"---\ntype: concern\ntitle: \xff\n---\n"}, "a", "draft", "UTF-8"),
        ({"a.md": "---\ntype: concern\nstatus: >\n  stub\n---\n"}, "a", "draft", "will not rewrite"),
    ],
)  # fmt: skip
def test_set_status_refuses_and_writes_nothing(make_vault, snap, files, ref, status, word):
    root = make_vault(files)
    before = snap(root)
    r = set_status(ref, status, root=root)
    assert not r.ok and word in str(r) and "Fix:" in str(r)
    assert snap(root) == before


def test_set_status_message_names_file_and_fix(make_vault):
    root = make_vault({"concern/a.md": fm("concern", "A")})
    text = str(set_status("a", "finished", root=root))
    assert "stub, draft, done" in text and "signed off by the coder" in text
