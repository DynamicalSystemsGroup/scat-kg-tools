import pytest
from opsutil import fm, narrative

from scat_kg.ops import stub, stub_links
from scat_kg.ops.names import derive_name, name_problem, stem_of
from scat_kg.vault import read_vault

CAP3 = {"scat.toml": "stakeholder_group_cap = 3\n"}


def group(name, title):
    return {f"group/{name}.md": fm("group", title)}


# names (section 2)


def test_name_rules():
    assert [name_problem(n) for n in ("a", "a-b", "x" * 64)] == [None] * 3
    for bad in (
        "",
        "A",
        "a--b",
        "-a",
        "a-",
        "a b",
        "a.b",
        "é",
        "x" * 65,
        "con",
        "com3",
        "lpt9",
    ):
        assert name_problem(bad), bad
    assert stem_of("Safe handling of tools") == "safe-handling-of-tools"
    assert stem_of("École Ångström ß ø") == "ecole-angstrom"
    assert stem_of("日本語") == ""
    assert stem_of("a" * 63 + " b") == "a" * 63
    assert derive_name("Con", set()) == "con-2"
    assert name_problem("concerns") is None  # no class pages now (D-088): not reserved
    assert derive_name("Same", {"same", "same-2"}) == "same-3"
    long = "a" * 64
    assert derive_name(long, {long}) == "a" * 62 + "-2"
    assert derive_name("日本語", set()) is None


# stub


def test_stub_creates_exactly_the_skeleton_in_the_types_folder(make_vault, snap, diff):
    root = make_vault({"README.md": "x\n", **CAP3})
    before = snap(root)
    r = stub("safety-briefing", "affordance", root=root)
    assert r.ok and r.created == ("affordance/safety-briefing.md",)
    assert (root / "affordance/safety-briefing.md").read_bytes() == (
        b'---\ntype: affordance\nstatus: stub\ntitle: "Safety briefing"\n---\n'
    )
    assert set(diff(before, snap(root))) == {"affordance", "affordance/safety-briefing.md"}


def test_stub_twice_changes_nothing_the_second_time(make_vault, snap):
    root = make_vault(CAP3)
    stub("a", "concern", root=root)
    before = snap(root)
    r = stub("a", "concern", root=root)
    assert r.ok and r.unchanged == ("concern/a.md",) and "already" in str(r) and not r.created
    assert snap(root) == before


@pytest.mark.parametrize(
    "name, type_, word",
    [
        ("Bad Name", "concern", "a-z"),
        ("con", "concern", "reserved"),
        ("x" * 65, "concern", "64"),
        ("a", "holds", "record-edge"),
        ("a", "index", "scat index"),
        # retired on purpose: the removed relation type is refused
        ("a", "heldby", "use one of"),
        ("a", "nonsense", "use one of"),
        ("taken", "affordance", "already"),
        ("TAKEN", "concern", "a-z"),  # not a slug: the fix offers the derived name
        ("notes", "concern", "already"),  # a Markdown file that is not a page still blocks the name
    ],
)
def test_stub_refuses_and_creates_nothing(make_vault, snap, name, type_, word):
    root = make_vault(
        {"concern/taken.md": fm("concern", "T"), "docs/notes.md": "# no frontmatter\n"}
    )
    before = snap(root)
    r = stub(name, type_, root=root)
    assert not r.ok and word in str(r) and "Fix:" in str(r)
    assert snap(root) == before


def test_stub_refuses_a_name_that_differs_only_by_case_from_a_page(make_vault, snap):
    root = make_vault({"concern/Quick.md": fm("concern", "Q")})
    assert "already" in str(stub("quick", "concern", root=root))


def test_stub_never_overwrites_an_existing_page(make_vault):
    root = make_vault({"concern/a.md": fm("concern", "Mine")})
    stub("a", "concern", root=root)
    assert (root / "concern/a.md").read_text() == fm("concern", "Mine")


@pytest.mark.parametrize("slug", ["group", "concern", "affordance", "technology", "narrative"])
def test_stub_every_accepted_type(make_vault, slug):
    root = make_vault(CAP3)
    assert stub("thing", slug, root=root).created == (f"{slug}/thing.md",)
    assert read_vault(root).by_name["thing"][0].type == slug


def test_stub_refuses_a_group_over_the_cap_and_creates_nothing(make_vault, snap):
    root = make_vault({**CAP3, **group("a", "A"), **group("b", "B"), **group("c", "C")})
    before = snap(root)
    r = stub("d", "group", root=root)
    assert (
        not r.ok
        and "cap of 3" in str(r)
        and "SCAT-CAP" in str(r)
        and "stakeholder_group_cap = 4" in str(r)
    )
    assert snap(root) == before
    assert stub("d", "concern", root=root).ok  # only groups are capped


def test_stub_group_under_the_cap_and_with_unusable_cap(make_vault):
    root = make_vault({**CAP3, **group("a", "A")})
    assert stub("b", "group", root=root).ok
    nocap = root.parent / "nocap"
    nocap.mkdir()
    r = stub("b", "group", root=nocap)  # no scat.toml: the cap is unknown
    assert not r.ok and "stakeholder_group_cap" in str(r) and "missing" in str(r)
    assert not (nocap / "group").exists()


def test_stub_without_a_type_creates_nothing_and_says_what_to_give(make_vault, snap):
    root = make_vault(CAP3)
    before = snap(root)
    r = stub("a", root=root)
    assert not r.ok and "needs its type" in str(r) and "one of: group, concern" in str(r)
    assert snap(root) == before


def test_stub_of_a_narrative_has_the_timeframe_line_after_the_title(make_vault):
    root = make_vault(CAP3)
    stub("story", "narrative", root=root)
    assert (root / "narrative/story.md").read_text() == (
        '---\ntype: narrative\nstatus: stub\ntitle: "Story"\ntimeframe: # past | future | mixed\n---\n'
    )


@pytest.mark.parametrize("slug", ["group", "concern", "affordance", "technology"])
def test_stub_of_a_node_has_no_timeframe_line(make_vault, slug):
    root = make_vault({**CAP3})
    stub("story", slug, root=root)
    assert "timeframe" not in (root / f"{slug}/story.md").read_text()


def test_stub_refusals_name_the_command_that_does_it_and_carry_it_as_data(make_vault):
    root = make_vault(CAP3)
    r = stub("a", "index", root=root)
    assert r.refused[0].fix_data.options[0].command.argv == ("index",)
    assert "scat_kg.index()" in r.refused[0].fix
    assert "scat record-edge" in str(stub("a", "addressed-by", root=root))


# stub_links


@pytest.fixture
def linked(make_vault):
    return make_vault(
        {
            **CAP3,
            "narrative/n.md": narrative(
                "N",
                [
                    "| holds | [[volunteers]] | [[safety]] | |",
                    "| is addressed by | [[safety]] | [[briefing]] | |",
                    "| holds | [[Bad Name]] | [[here]] | |",
                    "| is provided by | [[briefing]] | [[here]] | |",
                    "| nonsense | [[unknown-type]] | [[also-unknown]] | |",
                    "| holds | plain text | [[no-link-end]] | |",
                ],
                "done",
                "",
            ).replace("The account.", "The account names [[bodyonly]] and [[told]]."),
            "concern/here.md": fm("concern", "Here"),
            "narrative/other.md": narrative("O", None),
        }
    )


def test_stub_links_creates_each_entailed_node_by_the_layer_of_its_row_end(linked, snap, diff):
    before = snap(linked)
    r = stub_links(root=linked)
    assert r.ok and set(r.created) == {
        "group/volunteers.md", "concern/safety.md", "affordance/briefing.md", "concern/no-link-end.md",
    }  # fmt: skip
    assert set(diff(before, snap(linked))) - {"group", "affordance"} >= set(r.created)
    assert (
        linked / "concern/safety.md"
    ).read_text() == '---\ntype: concern\nstatus: stub\ntitle: "Safety"\n---\n'
    text = str(r)
    assert "[[Bad Name]]" in text and "not a legal name" in text  # entails nothing, says why
    assert not list(linked.glob("*/unknown-type.md"))  # an unknown type entails no node
    assert (linked / "narrative/n.md").read_bytes() == before["narrative/n.md"][
        2
    ]  # no page is changed


def test_stub_links_reports_an_untyped_link_and_creates_nothing_for_it(linked):
    r = stub_links(root=linked)
    assert "[[bodyonly]] reaches no page" in str(r) and "scat stub bodyonly --type <type>" in str(r)
    assert not (linked / "concern/bodyonly.md").exists()
    assert not list(linked.glob("*/bodyonly.md")) and not list(linked.glob("*/told.md"))


def test_stub_links_twice_changes_nothing_the_second_time(linked, snap):
    stub_links(root=linked)
    before = snap(linked)
    r = stub_links(root=linked)
    assert not r.created and not r.changed
    assert snap(linked) == before


def test_stub_links_for_one_page_only(linked):
    r = stub_links("other", root=linked)
    assert not r.created
    assert set(stub_links("n", root=linked).created) >= {"group/volunteers.md"}


def test_stub_links_an_end_that_reaches_a_page_of_another_type_entails_nothing(make_vault):
    root = make_vault(
        {
            "narrative/n.md": narrative("N", ["| holds | [[tech]] | [[c]] | |"]),
            "technology/tech.md": fm("technology", "Tech"),
        }
    )
    r = stub_links(root=root)
    assert r.created == ("concern/c.md",) and not (root / "group/tech.md").exists()


def test_stub_links_target_named_as_two_types_is_refused_alone(make_vault):
    root = make_vault(
        {
            **CAP3,
            "narrative/s.md": narrative("S", ["| holds | [[ok]] | [[x]] | |", "| is addressed by | [[y]] | [[x]] | |"]),
        }
    )  # fmt: skip
    r = stub_links(root=root)
    assert not r.ok and "different types" in str(r)
    assert set(r.created) == {"group/ok.md", "concern/y.md"} and not list(root.glob("*/x.md"))


def test_stub_links_over_the_cap_creates_nothing_from_the_call(make_vault, snap):
    root = make_vault(
        {
            "scat.toml": "stakeholder_group_cap = 2\n",
            **group("g1", "G1"),
            "narrative/s.md": narrative("S", ["| holds | [[g2]] | [[c]] | |", "| holds | [[g3]] | [[c]] | |"]),
        }
    )  # fmt: skip
    before = snap(root)
    r = stub_links(root=root)
    assert not r.ok and "SCAT-CAP" in str(r) and not r.created
    assert snap(root) == before  # not even the concern stub


def test_stub_links_a_malformed_row_and_a_table_on_another_type_entail_nothing(make_vault):
    root = make_vault(
        {
            "narrative/n.md": narrative("N", ["| holds | [[g]] | [[c]] |"]),  # three cells
            "concern/x.md": fm("concern", "X", "draft", "", "## Edges told\n\n| type | from | to | note |\n|---|---|---|---|\n| holds | [[g2]] | [[c2]] | |\n"),
        }
    )  # fmt: skip
    assert not stub_links(root=root).created


def test_stub_links_for_a_missing_page_or_folder_is_a_refusal(make_vault, tmp_path):
    root = make_vault(CAP3)
    assert "no page" in str(stub_links("zzz", root=root))
    assert not stub_links(root=tmp_path / "nowhere").ok
