"""The three scopes: one page, its neighborhood, the whole vault. Checks read; they never write.

TODO(WP16-U6): the rules of the old model are not run; U6 rebuilds the checks for the row model.
"""

from scat_kg.ops.result import Result
from scat_kg.ops.result import not_built as _not_built
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


def check_page(vault: Vault, page: Page | str) -> Result:
    """TODO(WP16-U6): every rule that reports on this page."""
    return _not_built("check")


def neighborhood(vault: Vault, page: Page | str) -> list[Page]:
    """The page and every page one link away in either direction (its links and its backlinks)."""
    p = _resolve(vault, page)
    names = {l.target for l in p.links}
    paths = {p.path}
    for n in names:
        paths |= {q.path for q in vault.by_name.get(n, ())}
    paths |= {b.source for b in vault.inbound(p.name)}
    return [q for q in vault.pages if q.path in paths]


def check_neighborhood(vault: Vault, page: Page | str) -> Result:
    """TODO(WP16-U6): the page and everything one link away, in either direction (G4)."""
    return _not_built("check")


def check_vault(vault: Vault) -> Result:
    """TODO(WP16-U6): every page, and the vault-level rules."""
    return _not_built("check")
