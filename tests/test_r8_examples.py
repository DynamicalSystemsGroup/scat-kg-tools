"""WP5-R8: every page in contracts/examples/ checks clean, except where an example shows a warning.

Most of this is covered already (tests/checks/test_scopes.py: the whole vault, and each page and
neighborhood, have no error and only the one draft warning; tests/test_paths.py: the CLI exits 0). What this
adds: the one allowed warning is the one the README names, each page is checked through the public
`scat_kg.check` by path, every page type has an example, and no example page is left out of the check.
"""

# TODO(WP16-U6/U7) lift: the check-based tests below are skipped (UNBUILT) until U6 rebuilds the checks.

from pathlib import Path

import pytest

import scat_kg
from scat_kg.tbox import TBOX
from scat_kg.vault import read_vault

EXAMPLES = Path(__file__).parents[1] / "contracts" / "examples"
README = (EXAMPLES / "README.md").read_text(encoding="utf-8")
WARNED = "narrative/funders-meeting.md"
UNBUILT = pytest.mark.skip(reason="TODO(WP16-U6): the checks are rebuilt for the row model in U6")
PAGES = sorted(
    p.relative_to(EXAMPLES).as_posix() for p in EXAMPLES.rglob("*.md") if p.name != "README.md"
)


def test__r8__the_one_draft_is_the_example_the_readme_says_is_a_draft():
    assert "`funders-meeting.md` (neither, a `draft`)" in README
    drafts = [p.path for p in read_vault(EXAMPLES).pages if p.status != "done"]
    assert sorted(drafts) == (["group/funders.md", WARNED])  # the draft, and the `funders` stub


@UNBUILT
def test__r8__the_one_warning_is_the_example_the_readme_says_is_a_draft():
    assert WARNED.split("/")[1] in README and "draft" in README
    report = scat_kg.check(root=EXAMPLES)
    assert [(p.rule, p.file) for p in report.problems] == [("SCAT-DRAFT-FIELD", WARNED)]
    assert report.ok and report.errors == ()


@UNBUILT
@pytest.mark.parametrize("page", PAGES)
def test__r8__each_example_page_checks_clean_but_the_draft(page):
    result = scat_kg.check(page, root=EXAMPLES)
    assert result.ok
    expected = [("SCAT-DRAFT-FIELD", WARNED)] if page == WARNED else []
    assert [(p.rule, p.file) for p in result.problems] == expected


def test__r8__every_example_page_is_read_and_every_page_type_has_one():
    v = read_vault(EXAMPLES)
    assert sorted(p.path for p in v.pages) == PAGES
    assert {p.type for p in v.pages} == set(TBOX.page_types) - {
        "index"
    }  # an index is a Base, no page
