import shutil

from opsutil import EXAMPLES, fm

from scat_kg.ops import index, index_problem, index_region
from scat_kg.ops.index import END, START, same_table
from scat_kg.ops.names import CLASS_PAGES
from scat_kg.tbox import TBOX
from scat_kg.vault import read_vault

HEAD = '---\ntype: class\ntitle: "Concerns"\ndescription: "d"\nindexes: concern\n---\n'


def concerns_page(make_vault, region: str | bytes, extra_files=None, head=HEAD):
    body = region if isinstance(region, bytes) else region.encode()
    files = {"class/concerns.md": head.encode() + body, **(extra_files or {})}
    return make_vault(files)


def test_index_output_equals_example_class_pages_byte_for_byte(example_vault):
    shutil.rmtree(example_vault / "class")
    r = index(root=example_vault)
    assert r.ok and len(r.created) == 7
    for name in CLASS_PAGES:
        assert (example_vault / "class" / f"{name}.md").read_bytes() == (
            EXAMPLES / "class" / f"{name}.md"
        ).read_bytes()


def test_index_on_the_current_example_changes_nothing(example_vault, snap):
    before = snap(example_vault)
    r = index(root=example_vault)
    assert r.ok and not r.created and not r.changed and len(r.unchanged) == 7
    assert snap(example_vault) == before  # bytes and mtimes


def test_default_descriptions_are_the_tboxs():
    assert set(CLASS_PAGES) == {
        "stakeholder-groups", "concerns", "affordances", "technologies",
        "heldby-pairs", "addresses-pairs", "attributes-pairs",
    }  # fmt: skip
    assert {s for s, _ in CLASS_PAGES.values()} == set(TBOX.page_types) - {
        "class", "scenario-raw", "scenario-coded", "architecture-raw", "architecture-coded",
    }  # fmt: skip


def test_index_region_is_pure_and_sorted_with_every_status_and_escaping(make_vault, snap):
    root = make_vault(
        {
            "concern/zed.md": fm("concern", "Zed", "stub"),
            "concern/alpha.md": fm("concern", "A | B\\ndescription", "done", 'description: "x | y"\n'),
            "concern/mid.md": fm("concern", "Mid", "draft"),
            "affordance/other.md": fm("affordance", "Other"),
        }
    )  # fmt: skip
    before = snap(root)
    region = index_region(read_vault(root), "concerns")
    rows = [
        "| Name | Description | Link |", "|---|---|---|",
        "| A \\| B description | x \\| y | [[alpha]] |",
        "| Mid |  | [[mid]] |",
        "| Zed |  | [[zed]] |",
    ]  # fmt: skip
    assert region.split("\n") == [START, *rows, END]
    assert snap(root) == before


def test_empty_class_has_header_and_separator_only(make_vault):
    root = make_vault({"concern/a.md": fm("concern", "A")})
    assert (
        index_region(read_vault(root), "technologies")
        == f"{START}\n| Name | Description | Link |\n|---|---|---|\n{END}"
    )


def test_index_creates_missing_class_pages_only(make_vault, snap, diff):
    root = make_vault({"concern/a.md": fm("concern", "A"), "README.md": "hi\n"})
    before = snap(root)
    r = index(root=root)
    assert len(r.created) == 7 and not r.changed
    assert set(diff(before, snap(root))) == {"class"} | {f"class/{n}.md" for n in CLASS_PAGES}
    page = (root / "class/concerns.md").read_text()
    assert page.startswith(
        '---\ntype: class\ntitle: "Concerns"\ndescription: "One page per concern'
    )
    assert "[[a]]" in page and page.endswith(f"{END}\n")
    assert index_problem(read_vault(root), "concerns") is None


def test_index_twice_changes_nothing_the_second_time(make_vault, snap):
    root = make_vault(
        {"concern/a.md": fm("concern", "A"), "stakeholder-group/g.md": fm("stakeholder-group", "G")}
    )
    index(root=root)
    before = snap(root)
    r = index(root=root)
    assert r.ok and not r.created and not r.changed
    assert snap(root) == before


def test_stale_region_is_rewritten_between_the_markers_only(make_vault, snap, diff):
    old = f"Intro text\n\n{START}\n| Name | Description | Link |\n|---|---|---|\n| Gone |  | [[gone]] |\n{END}\n\nAfter the table\n"
    root = concerns_page(make_vault, old, {"concern/a.md": fm("concern", "A"), "README.md": "x\n"})
    index(root=root)
    before = snap(root)
    assert before  # sanity
    new = (root / "class/concerns.md").read_text()
    assert new == (
        HEAD
        + "Intro text\n\n"
        + index_region(read_vault(root), "concerns")
        + "\n\nAfter the table\n"
    )
    assert "[[gone]]" not in new and "[[a]]" in new


def test_only_the_class_pages_change_when_a_page_is_added(example_vault, snap, diff):
    before = snap(example_vault)
    (example_vault / "concern/new.md").write_text(fm("concern", "New one"))
    mid = snap(example_vault)
    r = index(root=example_vault)
    assert r.changed == ("class/concerns.md",)
    assert diff(mid, snap(example_vault)) == {"class/concerns.md": "changed"}
    assert diff(before, mid) == {"concern/new.md": "created"}


def test_padding_and_trailing_spaces_are_not_stale_and_not_rewritten(make_vault, snap):
    aligned = f"{START}\n| Name | Description | Link |   \n| ---|--- |---|\n|  A   |    | [[a]]   |\n{END}\n"
    root = concerns_page(make_vault, aligned, {"concern/a.md": fm("concern", "A")})
    assert index_problem(read_vault(root), "concerns") is None
    before = snap(root)
    r = index(root=root)
    assert "class/concerns.md" in r.unchanged
    assert snap(root)["class/concerns.md"] == before["class/concerns.md"]


def test_same_table_ignores_only_padding():
    assert same_table(["|  a | b  |"], ["| a | b |"])
    assert not same_table(["| a | b |"], ["| a | c |"])
    assert not same_table(["| a \\| b |"], ["| a | b |"])


def test_crlf_page_stays_crlf(make_vault):
    text = (HEAD + f"Intro\n\n{START}\n| old |\n{END}\nTail\n").replace("\n", "\r\n")
    root = concerns_page(make_vault, "", head=text)
    (root / "concern").mkdir()
    (root / "concern/a.md").write_text(fm("concern", "A"))
    index(root=root)
    data = (root / "class/concerns.md").read_bytes()
    assert b"\r\n" in data and data.replace(b"\r\n", b"").count(b"\n") == 0
    assert data.endswith(b"Tail\r\n") and b"[[a]]" in data


def test_missing_end_marker_appends_a_fresh_region_and_leaves_strays(make_vault):
    body = f"Author text\n{START}\nmore author text\n"
    root = concerns_page(make_vault, body, {"concern/a.md": fm("concern", "A")})
    assert index_problem(read_vault(root), "concerns") == "no well-formed marker pair"
    index(root=root)
    new = (root / "class/concerns.md").read_text()
    assert new.startswith(HEAD + body + "\n" + START + "\n| Name")
    assert new.count(START) == 2 and new.count(END) == 1
    assert index_problem(read_vault(root), "concerns") is None


def test_end_before_start_gets_a_fresh_region_and_unterminated_file_is_ended(make_vault):
    body = f"{END}\nx\n{START}"  # no final newline
    root = concerns_page(make_vault, body)
    index(root=root)
    new = (root / "class/concerns.md").read_text()
    assert new.startswith(HEAD + f"{END}\nx\n{START}\n\n{START}\n| Name")
    assert new.endswith(f"{END}\n")
    assert new.count(END) == 2


def test_stray_marker_after_a_good_pair_is_left_alone_and_not_stale(make_vault, snap):
    good = f"{START}\n| Name | Description | Link |\n|---|---|---|\n{END}\nNotes\n{START}\nstray\n"
    root = concerns_page(make_vault, good)
    assert index_problem(read_vault(root), "concerns") is None
    before = snap(root)
    index(root=root)
    assert (root / "class/concerns.md").read_bytes() == before["class/concerns.md"][2]


def test_markers_inside_the_frontmatter_are_not_a_region(make_vault):
    head = "---\ntype: class\ntitle: C\nindexes: concern\nnote: x\n---\n"
    root = concerns_page(make_vault, "", head=head.replace("note: x", "note: x"))
    assert index_problem(read_vault(root), "concerns") == "no well-formed marker pair"


def test_index_problem_reasons(make_vault):
    root = make_vault({"concern/a.md": fm("concern", "A")})
    v = read_vault(root)
    assert index_problem(v, "concerns") == "the page is missing"
    root2 = concerns_page(
        make_vault,
        f"{START}\n| Name | Description | Link |\n|---|---|---|\n{END}\n",
        {"concern/a.md": fm("concern", "A")},
    )
    assert (
        index_problem(read_vault(root2), "concerns") == "the table differs from the concern pages"
    )


def test_name_taken_by_another_page_refuses_that_class_and_goes_on(make_vault, snap):
    root = make_vault(
        {"concern/concerns.md": fm("concern", "Mine"), "notes/technologies.md": "# not a page\n"}
    )
    r = index(root=root)
    assert not r.ok and len(r.refused) == 2 and len(r.created) == 5
    assert (
        "concern/concerns.md" in str(r) and "notes/technologies.md" in str(r) and "Fix:" in str(r)
    )
    assert (root / "concern/concerns.md").read_text() == fm("concern", "Mine")


def test_unreadable_frontmatter_on_a_class_page_refuses_and_writes_nothing_there(make_vault):
    root = concerns_page(make_vault, "", head="---\ntype: [oops\n---\n")
    before = (root / "class/concerns.md").read_bytes()
    r = index(root=root)
    assert any("class/concerns.md" in x.subject for x in r.refused)
    assert (root / "class/concerns.md").read_bytes() == before


def test_a_stray_start_above_the_pair_does_not_swallow_author_text(make_vault):
    body = f"{START}\nauthor text\n{START}\n| Name | Description | Link |\n|---|---|---|\n{END}\n"
    root = concerns_page(make_vault, body)
    assert index_problem(read_vault(root), "concerns") is None
    index(root=root)
    assert (root / "class/concerns.md").read_text() == HEAD + body
