"""The three scopes: one page, its neighborhood, the whole vault. Checks read; they never write."""

from scat_kg.checks import (  # noqa: F401  (register the rules)
    completeness,
    dangling,
    frontmatter,
    graph,
    links,
    vaultwide,
)
from scat_kg.checks.ctx import PAGE_RULES, VAULT_RULES, Ctx
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


def _run(vault: Vault, pages: list[Page], whole: bool) -> Report:
    ctx = Ctx(vault)
    problems: list[Problem] = []
    for p in pages:
        for rule in PAGE_RULES:
            problems += rule(ctx, p)
    # the vault-level rules run at vault scope, and at the other scopes when a group page is checked
    if whole or any(p.type_key == "stakeholder-group" for p in pages):
        for rule in VAULT_RULES:
            problems += rule(ctx)
    return Report(finalize(problems))


def check_page(vault: Vault, page: Page | str) -> Report:
    """Every rule that reports on this page (reading other pages where a rule needs them)."""
    return _run(vault, [_resolve(vault, page)], False)


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
    """The page and everything one link away, in either direction (G4)."""
    return _run(vault, neighborhood(vault, page), False)


def check_vault(vault: Vault) -> Report:
    """Every page, and the vault-level rules."""
    return _run(vault, list(vault.pages), True)
