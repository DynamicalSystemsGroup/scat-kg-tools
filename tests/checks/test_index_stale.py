"""SCAT-INDEX-STALE: a class page is missing, has no marker pair, or its table is not what `index` writes.

Each test starts from the clean fixture vault with its seven class pages written by `index` (zero messages),
seeds one defect, and expects exactly the catalogue's message and no other.
"""

import pytest
from helpers import base, doc

import scat_kg
from scat_kg.checks import check_neighborhood, check_page, check_vault
from scat_kg.ops.names import CLASS_PAGES
from scat_kg.vault import read_vault

RULE = "SCAT-INDEX-STALE"
FIX = "Fix: run `scat index` (REPL: `scat_kg.index()`)"
CONCERNS = "class/concerns.md"


@pytest.fixture
def root(make_vault):
    path = make_vault(base())
    assert scat_kg.index(root=path).ok
    return path


def golden(file, why):
    return [(RULE, file, "index table", FIX)] if why else []


def stale(root, scope="vault", page=None):
    v = read_vault(root)
    report = {
        "vault": lambda: check_vault(v),
        "page": lambda: check_page(v, page),
        "neighborhood": lambda: check_neighborhood(v, page),
    }[scope]()
    assert all(p.severity == "warning" for p in report.problems)
    assert report.ok
    return report, [p.elements for p in report.problems]


def test__scat_index_stale__clean_fixture_gives_nothing(root):
    assert stale(root)[1] == []
    assert {p.name for p in read_vault(root).of_type("class")} == set(CLASS_PAGES)


def test__scat_index_stale__an_instance_page_added_without_running_index(root):
    (root / "concern/new-one.md").write_text(doc("concern", "New one"), encoding="utf-8")
    report, got = stale(root)
    assert got == golden(CONCERNS, True)
    assert report.problems[0].what == "the table differs from the concern pages"
    assert report.problems[0].render() == (
        f"warning [{RULE}] {CONCERNS} index table: the table differs from the concern pages\n  {FIX}"
    )


def test__scat_index_stale__a_class_page_deleted(root):
    (root / CONCERNS).unlink()
    report, got = stale(root)
    assert got == golden(CONCERNS, True)
    assert report.problems[0].what == "the page is missing"


def test__scat_index_stale__a_marker_deleted(root):
    text = (root / CONCERNS).read_text(encoding="utf-8")
    (root / CONCERNS).write_text(text.replace("<!-- scat:index:end -->", ""), encoding="utf-8")
    report, got = stale(root)
    assert got == golden(CONCERNS, True)
    assert report.problems[0].what == "no well-formed marker pair"


def test__scat_index_stale__end_marker_before_start_is_no_pair(root):
    start, end = "<!-- scat:index:start -->", "<!-- scat:index:end -->"
    text = (root / CONCERNS).read_text(encoding="utf-8")
    swapped = text.replace(start, "@@").replace(end, start).replace("@@", end)
    (root / CONCERNS).write_text(swapped, encoding="utf-8")
    assert stale(root)[0].problems[0].what == "no well-formed marker pair"


def test__scat_index_stale__a_stray_extra_marker_after_a_good_pair_is_not_stale(root):
    with (root / CONCERNS).open("a", encoding="utf-8") as f:
        f.write("\n<!-- scat:index:end -->\n<!-- scat:index:start -->\n")
    assert stale(root)[1] == []


def test__scat_index_stale__running_index_and_checking_again_gives_nothing(root):
    (root / "concern/new-one.md").write_text(doc("concern", "New one"), encoding="utf-8")
    (root / "affordance/another.md").write_text(doc("affordance", "Another"), encoding="utf-8")
    (root / "class/technologies.md").unlink()
    assert len(stale(root)[1]) == 3
    assert scat_kg.index(root=root).ok
    assert stale(root)[1] == []


def test__scat_index_stale__a_table_aligned_with_extra_spaces_is_not_stale(root):
    text = (root / CONCERNS).read_text(encoding="utf-8")
    padded = text.replace("| Name |", "|   Name   |").replace("|---|", "| --- |")
    assert padded != text
    (root / CONCERNS).write_text(padded, encoding="utf-8")
    assert stale(root)[1] == []


def test__scat_index_stale__text_outside_the_markers_is_not_checked(root):
    text = (root / CONCERNS).read_text(encoding="utf-8")
    (root / CONCERNS).write_text(
        text.replace("---\n\n", "---\n\nThe author's own words.\n\n", 1), encoding="utf-8"
    )
    assert stale(root)[1] == []


def test__scat_index_stale__a_changed_title_makes_the_row_stale(root):
    page = root / "concern/quick-checkout.md"
    page.write_text(page.read_text(encoding="utf-8").replace("Quick checkout", "Fast checkout"))
    assert stale(root)[1] == golden(CONCERNS, True)


def test__scat_index_stale__the_page_scope_reports_the_class_page_and_not_the_missing_one(root):
    (root / "concern/new-one.md").write_text(doc("concern", "New one"), encoding="utf-8")
    (root / "class/technologies.md").unlink()
    assert stale(root, "page", CONCERNS)[1] == golden(CONCERNS, True)
    assert stale(root, "page", "concerns")[1] == golden(CONCERNS, True)
    assert (
        stale(root, "page", "booking-app")[1] == []
    )  # an instance page: the class pages are not its rules
    assert len(stale(root)[1]) == 2  # the vault scope reports both
    got = stale(root)[1]
    assert (RULE, "class/technologies.md", "index table", FIX) in got


def test__scat_index_stale__one_message_per_class_page_when_every_class_page_is_missing(make_vault):
    root = make_vault(base())
    report, got = stale(root)
    assert got == [(RULE, f"class/{n}.md", "index table", FIX) for n in sorted(CLASS_PAGES)]
    assert {p.what for p in report.problems} == {"the page is missing"}
    assert report.ok  # a warning never blocks
