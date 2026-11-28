"""R-9, WP7-R2: every runnable snippet in docs/ runs against the template vault, and the CLI
reference equals `--help`. The template is cloned at a pinned commit (WP8 re-pins it)."""

from pathlib import Path

import pytest
from docs_runner import copy_template, has_runnable, live_help, reference_problems, run_page

from scat_tools.cli import _parser

DOCS = Path(__file__).resolve().parents[2] / "docs"
PAGES = sorted(DOCS.rglob("*.md"))


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.relative_to(DOCS).as_posix())
def test_page_snippets_run(page, request, tmp_path):
    markdown = page.read_text(encoding="utf-8")
    if not has_runnable(markdown):
        return
    scratch = tmp_path / "vault"
    copy_template(request.getfixturevalue("template"), scratch)
    run_page(page.relative_to(DOCS).as_posix(), markdown, scratch)


def test_cli_reference_matches_help():
    markdown = (DOCS / "reference" / "cli.md").read_text(encoding="utf-8")
    problems = reference_problems(markdown, live_help(_parser()))
    assert not problems, "docs/reference/cli.md is out of step with `scat --help`:\n" + "\n".join(
        problems
    )
