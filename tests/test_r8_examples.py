"""WP5-R8: every page in contracts/examples/ checks clean, except where an example shows a warning.

Most of this is covered already (tests/checks/test_scopes.py: the whole vault, and each page and
neighborhood, have no error and only the draft's two warnings; tests/test_paths.py: the CLI exits 0). What this
adds: the allowed warnings are the ones the README names (the draft narrative has no `description` and no
`timeframe`), each page is checked through the public `scat_tools.check` by path, every page type has an example, and
no example page is left out of the check.
"""

from pathlib import Path

import pytest

import scat_tools
from scat_tools.tbox import TBOX
from scat_tools.vault import read_vault

EXAMPLES = Path(__file__).parents[1] / "contracts" / "examples"
README = (EXAMPLES / "README.md").read_text(encoding="utf-8")
WARNED = "narrative/funders-meeting.md"
WARNED_FIELDS = [
    ("SCAT-DRAFT-FIELD", WARNED),
    ("SCAT-DRAFT-FIELD", WARNED),
]  # `description`, then `timeframe`
PAGES = sorted(
    p.relative_to(EXAMPLES).as_posix() for p in EXAMPLES.rglob("*.md") if p.name != "README.md"
)


def test__r8__the_one_draft_is_the_example_the_readme_says_is_a_draft():
    assert "`funders-meeting.md` (neither, a `draft`)" in README
    drafts = [p.path for p in read_vault(EXAMPLES).pages if p.status != "done"]
    assert sorted(drafts) == (["group/funders.md", WARNED])  # the draft, and the `funders` stub


def test__r8__the_warnings_are_the_two_missing_fields_of_the_example_the_readme_says_is_a_draft():
    assert WARNED.split("/")[1] in README and "no `description`, no `timeframe`" in README
    report = scat_tools.check(root=EXAMPLES)
    assert [(p.rule, p.file) for p in report.problems] == WARNED_FIELDS
    assert [p.where for p in report.problems] == ["field `description`", "field `timeframe`"]
    assert report.ok and report.errors == ()


@pytest.mark.parametrize("page", PAGES)
def test__r8__each_example_page_checks_clean_but_the_draft(page):
    result = scat_tools.check(page, root=EXAMPLES)
    assert result.ok
    expected = WARNED_FIELDS if page == WARNED else []
    assert [(p.rule, p.file) for p in result.problems] == expected


def test__r8__every_example_page_is_read_and_every_page_type_has_one():
    v = read_vault(EXAMPLES)
    assert sorted(p.path for p in v.pages) == PAGES
    assert {p.type for p in v.pages} == set(TBOX.page_types) - {
        "index",
        "contributor",
    }  # an index is a Base, no page; the example vault is `disallowed`: no contributor page
