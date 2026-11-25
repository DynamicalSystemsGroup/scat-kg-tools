import os
from collections import Counter
from pathlib import Path

from scat_kg.models import MODELS
from scat_kg.tbox import TBOX
from scat_kg.vault import read_vault

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
    assert len(v.pages) == 13
    assert Counter(p.type for p in v.pages) == {
        "group": 3, "concern": 3, "affordance": 2, "technology": 2, "narrative": 3,
    }  # fmt: skip
    assert set(Counter(p.type for p in v.pages)) == set(TBOX.page_types) - {
        "index"
    }  # an index is no page
    assert v.non_pages == ("README.md",)  # the `index/*.base` files are not read at all
    assert all(p.frontmatter_error is None and p.model_error is None for p in v.pages)
    assert all(p.model is not None for p in v.pages)


def test_example_vault_every_link_resolves():
    v = read_vault(EXAMPLES)
    assert v.dangling() == ()
    assert sum(len(p.links) for p in v.pages) == 38
    for p in v.pages:
        for link in p.links:
            assert len(v.by_name[link.target]) == 1


def test_example_vault_links_backlinks_and_config():
    v = read_vault(EXAMPLES)
    careful = v.address("careful-record-keeping").page
    assert [(l.target, l.line) for l in careful.body_links] == [("quick-checkout", 8)]
    sources = {b.source for b in v.inbound("quick-checkout")}
    assert "concern/careful-record-keeping.md" in sources
    assert "narrative/self-service-kiosk-pitch.md" in sources
    # a link in a table cell is a link of the page: the alias and the escaped bar are read as the name
    pitch = v.address("self-service-kiosk-pitch").page
    assert "self-checkout" in {l.target for l in pitch.body_links}
    assert v.config.cap == 3 and v.config.problem is None
    assert [p.name for p in v.of_type("group")] == ["borrowers", "funders", "volunteer-staff"]


def test_non_markdown_files_are_ignored(make_vault):
    root = make_vault({
        "index/concern.base": "filters:\n  and:\n    - 'note.type == \"concern\"'\n",
        "notes.txt": "---\ntype: concern\n---\n",
        "concern/a.md": page("concern"),
    })  # fmt: skip
    v = read_vault(root)
    assert [p.path for p in v.pages] == ["concern/a.md"] and v.non_pages == ()


def test_models_come_from_the_tbox():
    assert set(MODELS) == set(TBOX.page_types)
    for slug, t in TBOX.page_types.items():
        assert set(MODELS[slug].model_fields) == {f.key for f in t.fields} | {"type"}


def test_model_shape_errors_are_data(make_vault):
    root = make_vault({
        "narrative/a.md": page("narrative", extra="timeframe: someday\n"),  # outside its value set
        "narrative/h.md": page("narrative", extra="kind: report\n"),  # outside its value set
        "concern/s.md": "---\ntype: concern\nstatus: soon\ntitle: x\n---\n",
        "concern/ok.md": page("concern", extra="color: red\n"),  # unlisted plain key is ignored
    })  # fmt: skip
    v = read_vault(root)
    assert {p.name for p in v.pages if p.model_error} == {"a", "h", "s"}
    assert v.address("ok").page.model is not None


# the cases the reader must represent


def test_crlf_reads_like_lf(make_vault):
    lf = page("concern", body="See [[other]].\nmore\n")
    root = make_vault({"a/lf.md": lf, "a/crlf.md": lf.replace("\n", "\r\n").encode()})
    v = read_vault(root)
    lf_page, crlf_page = v.address("lf").page, v.address("crlf").page
    assert crlf_page.frontmatter_error is None
    assert crlf_page.fields == lf_page.fields
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
    root = make_vault({"a.md": page("narrative", body=body)})
    p = read_vault(root).address("a").page
    assert [(l.target, l.line) for l in p.body_links] == [
        ("a", 6), ("b", 6), ("c", 6), ("d", 6), ("e", 6),
        ("i", 8), ("l", 15), ("Safety Briefing", 16),
    ]  # fmt: skip
    assert p.body_links[0].column == 7 and p.body_links[1].column == 17  # 1-based, of the `[[`
    assert p.body_links[4].column == 63  # the `[[` of an embed, not its `!`


def test_links_in_the_frontmatter_are_never_read(make_vault):
    fm = 'concerns:\n  - "[[g1]]"\nconcern: "[[Single]]"\nnote: "[[ignored]]"\n'
    root = make_vault({"a.md": page("narrative", extra=fm, body="[[g1]]\n")})
    v = read_vault(root)
    p = v.address("a").page
    assert [(l.target, l.line) for l in p.links] == [("g1", 10)] and p.links == p.body_links
    assert p.fields["concerns"] == ["[[g1]]"]  # kept as the YAML read it
    assert [(b.source, b.line) for b in v.inbound("g1")] == [("a.md", 10)]
    assert v.inbound("Single") == () and v.inbound("ignored") == ()


def test_spaces_and_an_escaped_bar_in_a_link_are_read_as_the_name(make_vault):
    body = "| a | [[ spaced ]] | [[cell\\|alias]] | [[ x \\| y ]] |\n"
    p = read_vault(make_vault({"a.md": page("narrative", body=body)})).address("a").page
    assert [l.target for l in p.body_links] == ["spaced", "cell", "x"]


def test_dangling_and_case(make_vault):
    root = make_vault({
        "a.md": page("concern", body="[[Safety]] [[b]] [[gone]]\n"),
        "b.md": page("concern"),
        "safety.md": page("concern"),
    })  # fmt: skip
    v = read_vault(root)
    assert [(p.name, l.target) for p, l in v.dangling()] == [("a", "Safety"), ("a", "gone")]


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


def test_unhashable_type_does_not_abort_the_read(make_vault):
    root = make_vault({
        "list.md": "---\ntype: [concern, x]\n---\n",
        "map.md": "---\ntype:\n  a: b\n---\n",
        "ok.md": page("concern"),
    })  # fmt: skip
    v = read_vault(root)
    assert [p.name for p in v.pages] == ["list", "map", "ok"]
    for name in ("list", "map"):
        p = v.address(name).page
        assert p.frontmatter_error is None and p.type_key is None and p.model is None
    assert v.address("list").page.type == ["concern", "x"]
