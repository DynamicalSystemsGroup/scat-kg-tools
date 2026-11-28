"""Helpers the operations share: opening the vault, finding a page, the names that are taken."""

from pathlib import Path

from scat_tools.ops.result import Result, refused
from scat_tools.vault import Page, Vault, read_vault

ADDRESS_HINT = (
    "give the page's name (the file name without `.md`) or its path from the vault folder"
)


def open_vault(operation: str, root: str | Path) -> tuple[Vault | None, Result | None]:
    path = Path(root)
    if not path.is_dir():
        return None, refused(
            operation,
            str(path),
            "the vault folder does not exist",
            "pass the vault folder (the one that holds `scat.toml`), or run from inside it",
        )
    return read_vault(path), None


def find_page(operation: str, vault: Vault, ref: str) -> tuple[Page | None, Result | None]:
    found = vault.address(ref)
    if found.page is not None:
        return found.page, None
    if found.not_found:
        return None, refused(
            operation,
            ref,
            "no page has this name or path",
            ADDRESS_HINT,
        )
    paths = ", ".join(p.path for p in found.pages)
    return None, refused(
        operation,
        ref,
        f"more than one page has this name: {paths}",
        "give the page's path from the vault folder, e.g. `" + found.pages[0].path + "`",
    )


def taken_names(vault: Vault) -> set[str]:
    """Lower-cased names of every `.md` file in the vault, pages or not (section 2, step 4)."""
    names = {p.name.lower() for p in vault.pages}
    names |= {n.rsplit("/", 1)[-1].removesuffix(".md").lower() for n in vault.non_pages}
    return names
