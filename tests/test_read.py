import os
from collections import Counter
from pathlib import Path

from scat_kg.models import MODELS
from scat_kg.tbox import TBOX
from scat_kg.vault import LINK_KEYS, read_vault

EXAMPLES = Path(__file__).parents[1] / "contracts" / "examples"


def page(type_: str, title: str = "T", extra: str = "", body: str = "") -> str:
    return f'---\ntype: {type_}\nstatus: draft\ntitle: "{title}"\n{extra}---\n{body}'


def snapshot(root: Path) -> dict[str, tuple]:
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for n in dirnames:
            out[str(Path(dirpath, n))] = ("dir",)
        for n in filenames:
            p = Path(dirpath, n)
            st = p.stat()
            out[str(p)] = ("file", st.st_size, st.st_mtime_ns, p.read_bytes())
    return out


# the example vault


def test_example_vault_pages_and_types():
    v = read_vault(EXAMPLES)
    assert len(v.pages) == 25
    assert Counter(p.type for p in v.pages) == {
        "stakeholder-group": 3, "concern": 3, "affordance": 1, "technology": 1,
        "heldby": 4, "addresses": 1, "attributes": 1,
        "scenario-raw": 1, "scenario-coded": 1, "architecture-raw": 1, "architecture-coded": 1,
        "class": 7,
    }  # fmt: skip
    assert set(Counter(p.type for p in v.pages)) == set(TBOX.page_types)
    assert v.non_pages == ("README.md",)
    assert all(p.frontmatter_error is None and p.model_error is None for p in v.pages)
    assert all(p.model is not None for p in v.pages)


def test_example_vault_every_link_resolves():
    v = read_vault(EXAMPLES)
    assert v.dangling() == ()
    assert sum(len(p.links) for p in v.pages) == 39
    for p in v.pages:
        for link in p.links:
            assert len(v.by_name[link.target]) == 1


def test_example_vault_links_backlinks_and_config():
    v = read_vault(EXAMPLES)
    heldby = v.address("volunteer-staff-holds-safe-handling-of-tools").page
    assert {k: [l.target for l in ls] for k, ls in heldby.fm_links.items()} == {
        "group": ["volunteer-staff"],
        "concern": ["safe-handling-of-tools"],
    }
    assert heldby.fm_links["group"][0].line == heldby.field_lines["group"] == 6
    careful = v.address("careful-record-keeping").page
    assert careful.fm_links["conflicts"][0].target == "quick-checkout"
    sources = {(b.source, b.field) for b in v.inbound("quick-checkout")}
    assert ("concern/careful-record-keeping.md", "conflicts") in sources
    assert ("class/concerns.md", None) in sources
    assert v.config.cap == 3 and v.config.problem is None
    assert [p.name for p in v.of_type("stakeholder-group")] == [
        "borrowers", "funders", "volunteer-staff",
    ]  # fmt: skip


def test_models_come_from_the_tbox():
    assert set(MODELS) == set(TBOX.page_types)
    for slug, t in TBOX.page_types.items():
        assert set(MODELS[slug].model_fields) == {f.key for f in t.fields} | {"type"}
    assert LINK_KEYS == {"group", "concern", "affordance", "technology", "conflicts", "groups",
                         "concerns", "affordances", "technologies", "raw", "coded"}  # fmt: skip


def test_model_shape_errors_are_data(make_vault):
    root = make_vault({
        "concern/a.md": page("concern", extra="conflicts: \"[[b]]\"\n"),  # a list field, written scalar
        "heldby/h.md": page("heldby", extra="group:\n  - \"[[a]]\"\n"),  # single field, written list
        "concern/s.md": "---\ntype: concern\nstatus: soon\ntitle: x\n---\n",
        "concern/ok.md": page("concern", extra="color: red\n"),  # unlisted plain key is ignored
    })  # fmt: skip
    v = read_vault(root)
    assert {p.name for p in v.pages if p.model_error} == {"a", "h", "s"}
    assert v.address("ok").page.model is not None


# the cases the reader must represent


def test_crlf_reads_like_lf(make_vault):
    lf = page("concern", extra='conflicts:\n  - "[[quick]]"\n', body="See [[other]].\nmore\n")
    root = make_vault({"a/lf.md": lf, "a/crlf.md": lf.replace("\n", "\r\n").encode()})
    v = read_vault(root)
    lf_page, crlf_page = v.address("lf").page, v.address("crlf").page
    assert crlf_page.frontmatter_error is None
    assert crlf_page.fields == lf_page.fields
    assert crlf_page.fm_links == lf_page.fm_links
    assert crlf_page.body_links == lf_page.body_links
    assert crlf_page.body == lf_page.body and "\r" not in crlf_page.body


def test_utf8(make_vault):
    root = make_vault({"a.md": page("concern", title="Café 日本", body="é [[b]]\n")})
    p = read_vault(root).address("a").page
    assert p.fields["title"] == "Café 日本" and p.body_links[0].target == "b"


def test_broken_frontmatter_is_represented(make_vault):
    root = make_vault({
        "yaml.md": "---\ntype: concern\ntitle: a: b\n---\nbody [[x]]\n",
        "tab.md": "---\ntype: concern\n\tstatus: draft\n---\n",
        "open.md": "---\ntype: concern\ntitle: t\n\nno closing line [[x]]\n",
        "list.md": "---\n- a\n- b\n---\n",
        "empty.md": "---\n---\n",
        "fine.md": page("concern"),
    })  # fmt: skip
    v = read_vault(root)
    assert [p.name for p in v.pages] == ["empty", "fine", "list", "open", "tab", "yaml"]
    bad = {p.name: p for p in v.pages if p.frontmatter_error}
    assert set(bad) == {"empty", "list", "open", "tab", "yaml"}
    assert bad["open"].frontmatter_error.reason == "the closing --- line is missing"
    assert bad["yaml"].frontmatter_error.line == 3
    assert bad["list"].frontmatter_error.reason.endswith("not a mapping of keys to values")
    # an unreadable page is a source of no links and has no fields
    assert all(p.fields == {} and p.links == () for p in bad.values())
    assert v.dangling() == ()


def test_not_pages_are_ignored(make_vault):
    root = make_vault({
        "README.md": "# Readme\n\nSee [[a]].\n",
        "notes/no-type.md": "---\ntitle: x\n---\nbody [[a]]\n",
        "a.md": page("concern"),
        "x.txt": "---\ntype: concern\n---\n",
        "UP.MD": page("concern"),
    })  # fmt: skip
    v = read_vault(root)
    assert [p.path for p in v.pages] == ["a.md"]
    assert v.non_pages == ("README.md", "notes/no-type.md")
    assert v.inbound("a") == ()  # a non-page links nothing


def test_dot_folders_are_skipped(make_vault):
    root = make_vault({
        ".obsidian/p.md": page("concern"),
        ".trash/q.md": page("concern"),
        "deep/.hidden/r.md": page("concern"),
        "deep/s.md": page("concern"),
    })  # fmt: skip
    assert [p.path for p in read_vault(root).pages] == ["deep/s.md"]


def test_duplicate_names_and_addressing(make_vault):
    root = make_vault({
        "concern/x.md": page("concern", "one"),
        "other/x.md": page("affordance", "two"),
        "concern/y.md": page("concern", "y"),
    })  # fmt: skip
    v = read_vault(root)
    assert [p.path for p in v.by_name["x"]] == ["concern/x.md", "other/x.md"]
    by_name = v.address("x")
    assert by_name.ambiguous and by_name.page is None and not by_name.not_found
    assert [p.path for p in by_name.pages] == ["concern/x.md", "other/x.md"]
    # by path
    assert v.address("other/x.md").page.fields["title"] == "two"
    assert v.address(str(root / "concern" / "y.md")).page.name == "y"
    assert v.address("y").page is v.address("concern/y.md").page
    # not found, by name and by path; a name is exact, and a path is not a name
    for ref in ("z", "Y", "concern/z.md", "y.md", str(root.parent / "y.md"), "concern/x"):
        assert v.address(ref).not_found, ref


def test_link_extraction(make_vault):
    body = (
        "plain [[a]] and [[b|shown]] and [[c#Head]] and [[d^blk]] and ![[e]]\n"
        "skipped: [[photo.png]] [[v1.2-notes]] [[dir/x]] [[#Here]] [[^blk]] [[|a]] [md](f)\n"
        "code `[[g]]` and ``[[h]]`` and `unmatched [[i]]\n"
        "```\n[[j]]\n```\n"
        "~~~py\n[[k]]\n~~~\n"
        "    indented [[l]]\n"
        "bad case [[Safety Briefing]]\n"
    )
    root = make_vault({"a.md": page("scenario-raw", body=body)})
    p = read_vault(root).address("a").page
    assert [(l.target, l.line) for l in p.body_links] == [
        ("a", 6), ("b", 6), ("c", 6), ("d", 6), ("e", 6),
        ("i", 8), ("l", 15), ("Safety Briefing", 16),
    ]  # fmt: skip
    assert all(l.field is None for l in p.body_links)


def test_frontmatter_links_keep_what_is_written(make_vault):
    fm = (
        'groups:\n  - "[[g1]]"\n  - "[[g2]]"\n'
        'concerns: ["[[c1]]", "[[c2]]"]\n'
        "affordances: []\n"
        'concern: "[[Single]]"\n'
        'raw:\n  - "[[a|alias]]"\n  - plain\n'
        'note: "[[ignored]]"\n'
    )
    root = make_vault({"a.md": page("scenario-coded", extra=fm, body="[[g1]]\n")})
    p = read_vault(root).address("a").page
    seen = {k: [(l.target, l.line) for l in ls] for k, ls in p.fm_links.items()}
    assert seen == {
        "groups": [("g1", 6), ("g2", 7)],
        "concerns": [("c1", 8), ("c2", 8)],
        "affordances": [],
        "concern": [("Single", 10)],
        "raw": [("a|alias", 12)],  # as written: not a bare name, so it will not resolve
    }
    assert p.fields["raw"] == ["[[a|alias]]", "plain"]
    assert p.fields["groups"] == ["[[g1]]", "[[g2]]"]
    assert "note" not in p.fm_links
    assert [b.field for b in read_vault(root).inbound("g1")] == ["groups", None]


def test_nested_list_from_unquoted_link_is_kept_raw(make_vault):
    root = make_vault({"a.md": page("concern", extra="conflicts: [[x]]\n")})
    p = read_vault(root).address("a").page
    assert p.fields["conflicts"] == [["x"]] and p.fm_links["conflicts"] == ()


def test_dangling_and_case(make_vault):
    root = make_vault({
        "a.md": page("concern", extra="conflicts:\n  - \"[[Safety]]\"\n  - \"[[b]]\"\n", body="[[gone]]\n"),
        "b.md": page("concern"),
        "safety.md": page("concern"),
    })  # fmt: skip
    v = read_vault(root)
    assert [(p.name, l.target, l.field) for p, l in v.dangling()] == [
        ("a", "Safety", "conflicts"),
        ("a", "gone", None),
    ]


def test_config(make_vault, tmp_path):
    def config(text: str | None):
        d = tmp_path / str(abs(hash(text)))
        d.mkdir()
        if text is not None:
            (d / "scat.toml").write_text(text)
        return read_vault(d).config

    assert config(None).problem == "missing"
    assert config("stakeholder_group_cap = 3\nother = 1\n").cap == 3
    assert config("stakeholder_group_cap = 1\r\n").cap == 1
    bad = config("stakeholder_group_cap = = 3")
    assert (bad.problem, bad.cap) == ("invalid-toml", None) and bad.detail
    assert config("x = 1").problem == "key-missing"
    assert config("[t]\nstakeholder_group_cap = 3").problem == "key-missing"
    for text, shown in [
        ("= 0", "0"),
        ("= 3.0", "3.0"),
        ('= "three"', "'three'"),
        ("= true", "True"),
    ]:
        c = config(f"stakeholder_group_cap {text}")
        assert (c.problem, c.detail, c.cap) == ("bad-value", shown, None)


def test_reading_leaves_the_tree_unchanged(make_vault):
    root = make_vault({
        "concern/a.md": page("concern", body="[[b]]\n"),
        "concern/broken.md": "---\ntype: concern\ntitle: a: b\n---\n",
        "other/crlf.md": page("concern").replace("\n", "\r\n").encode(),
        ".obsidian/x.md": page("concern"),
        "README.md": "hi\n",
        "scat.toml": "stakeholder_group_cap = 2\n",
    })  # fmt: skip
    for tree in (root, EXAMPLES):
        before = snapshot(tree)
        v = read_vault(tree)
        v.address("a"), v.dangling(), v.inbound("b")
        assert snapshot(tree) == before
