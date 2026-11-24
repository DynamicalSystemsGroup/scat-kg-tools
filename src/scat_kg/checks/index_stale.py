"""SCAT-INDEX-STALE: a class page is missing, has no marker pair, or its table is not what `index` writes.

The comparison is the index operation's own (`index_problem`), so the check and the fix cannot disagree.
"""

from scat_kg.checks import fixes
from scat_kg.checks.ctx import Ctx, page_rule, vault_rule
from scat_kg.ops.index import index_problem
from scat_kg.ops.names import CLASS_PAGES
from scat_kg.vault import Page

WHERE = "index table"
FIX = fixes.single(fixes.run_option(fixes.index()))
MISSING = "the page is missing"


@page_rule
def stale_class_page(ctx: Ctx, page: Page):
    """A class page that exists, is the only page of its name, and is stale."""
    if not (
        ctx.whole or page is ctx.focus
    ):  # a local check of another page is a fast linter for it (D-035)
        return []
    if page.type_key != "class" or page.name not in CLASS_PAGES or ctx.page(page.name) is not page:
        return []
    why = index_problem(ctx.vault, page.name)
    if why is None or why == MISSING:
        return []
    return [ctx.problem("SCAT-INDEX-STALE", page.path, WHERE, why, FIX)]


@vault_rule
def missing_class_pages(ctx: Ctx):
    """At whole-vault scope only: a class page no file holds. A name another file holds is that file's problem (SCAT-NAME, SCAT-FM-PARSE)."""
    if not ctx.whole:  # a local check of another page is a fast linter for that page (D-035)
        return []
    out = []
    for name in sorted(CLASS_PAGES):
        if name in ctx.taken:
            continue
        out.append(ctx.problem("SCAT-INDEX-STALE", f"class/{name}.md", WHERE, MISSING, FIX))
    return out
