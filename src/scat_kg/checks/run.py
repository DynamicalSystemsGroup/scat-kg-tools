"""The three scopes: one page, its neighborhood, the whole vault. Checks read; they never write.

A scope is a set of pages: every rule that reports on one of them runs (reading other pages where it needs to), so
the same page gives the same messages at every scope. The vault-level rules (SCAT-CAP, SCAT-CAP-CONFIG) run at
vault scope, and at the other two when a `group` page is in the set. `check_page_at_done` is the done check
(catalogue section 5): the page as it would stand at `done`.
"""

from scat_kg.checks import (  # noqa: F401  (register the rules)
    attribution,
    completeness,
    dangling,
    ends,
    frontmatter,
    mention,
    noedges,
    table,
    vaultwide,
)
from scat_kg.checks.ctx import NODE_TYPES, PAGE_RULES, VAULT_RULES, Ctx
from scat_kg.checks.problem import Problem, Report, finalize
from scat_kg.vault import Page, Vault


def _resolve(vault: Vault, page: Page | str) -> Page:
    if isinstance(page, Page):
        return page
    found = vault.address(page)
    if found.page is None:
        raise LookupError(
            f"no page `{page}`" if found.not_found else f"`{page}` names more than one page"
        )
    return found.page


def _run(
    vault: Vault,
    pages: list[Page],
    whole: bool,
    focus: Page | None = None,
    as_done: Page | None = None,
    vault_rules: bool | None = None,
) -> Report:
    ctx = Ctx(vault, as_done)
    ctx.whole, ctx.focus = whole, focus
    problems: list[Problem] = []
    for p in pages:
        for rule in PAGE_RULES:
            problems += rule(ctx, p)
    # the vault-level rules run at vault scope, and at the other scopes when a group page is checked
    if vault_rules is None:
        vault_rules = whole or any(p.type_key == NODE_TYPES[0] for p in pages)
    if vault_rules:
        for rule in VAULT_RULES:
            problems += rule(ctx)
    return Report(finalize(problems))


def check_page(vault: Vault, page: Page | str) -> Report:
    """Every rule that reports on this page (reading other pages where a rule needs them)."""
    found = _resolve(vault, page)
    return _run(vault, [found], False, found)


def neighborhood(vault: Vault, page: Page | str) -> list[Page]:
    """The page and every page one link away in either direction (its links and its backlinks)."""
    p = _resolve(vault, page)
    names = {l.target for l in p.links}
    paths = {p.path}
    for n in names:
        paths |= {q.path for q in vault.by_name.get(n, ())}
    paths |= {b.source for b in vault.inbound(p.name)}
    return [q for q in vault.pages if q.path in paths]


def check_neighborhood(vault: Vault, page: Page | str) -> Report:
    """The page and everything one link away, in either direction."""
    return _run(vault, neighborhood(vault, page), False, _resolve(vault, page))


def check_vault(vault: Vault) -> Report:
    """Every page, and the vault-level rules."""
    return _run(vault, list(vault.pages), True)


def check_page_at_done(vault: Vault, page: Page | str) -> Report:
    """The page judged as it would stand at `done` (catalogue section 5): every rule that reports on it, with its
    status taken as `done` whatever it says. The problems the refusal to set `done` lists are `.errors` of the
    report; its warnings do not block.

    The pages one link away are read and add nothing, and the vault-wide rules (SCAT-CAP, SCAT-CAP-CONFIG) are
    left out: they do not depend on this page's status. Reads only; nothing is written.
    """
    found = _resolve(vault, page)
    return _run(vault, [found], False, found, as_done=found, vault_rules=False)
