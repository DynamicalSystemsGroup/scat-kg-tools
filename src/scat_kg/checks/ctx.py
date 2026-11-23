"""What a rule sees: the vault, plus the lookups the rules share. Reading only; nothing here writes."""

import re
from collections import defaultdict
from collections.abc import Callable

from scat_kg.checks.problem import SEVERITY, Problem
from scat_kg.checks.text import LINK_ITEM
from scat_kg.tbox import TBOX
from scat_kg.vault import Link, Page, Vault

PAGE_RULES: list[Callable[["Ctx", Page], list[Problem]]] = []
VAULT_RULES: list[Callable[["Ctx"], list[Problem]]] = []

# Rules in the catalogue that are not implemented here, and why. Each needs an operation another unit owns.
# SCAT-INDEX-STALE needs the index renderer (WP5-U4). To add it: write a function `(ctx, page) -> [Problem]`
# for class pages (decorate it with @page_rule) and one `(ctx) -> [Problem]` for the seven class pages the
# vault lacks (@vault_rule), build its Problems with `ctx.problem("SCAT-INDEX-STALE", ...)`, and delete the
# entry below. Nothing else changes: the three check functions pick registered rules up.
DEFERRED = {
    "SCAT-INDEX-STALE": "compares a class page with what `index` writes; needs the index renderer (U4)"
}


def page_rule(fn):
    """Register a rule that reports on one page (it may read others)."""
    PAGE_RULES.append(fn)
    return fn


def vault_rule(fn):
    """Register a rule that reports on the vault (SCAT-CAP, SCAT-CAP-CONFIG)."""
    VAULT_RULES.append(fn)
    return fn


class Ctx:
    def __init__(self, vault: Vault):
        self.vault = vault
        self._lines: dict[str, list[str]] = {}
        self._relations: dict[str, list[dict[str, str]]] = {}
        self.cache: dict[str, object] = {}  # per-check scratch for the rules
        self.by_type: dict[str, list[Page]] = defaultdict(list)
        for p in vault.pages:
            if p.type_key:
                self.by_type[p.type_key].append(p)
        self.typeless: dict[str, str] = {}  # name -> path of a `.md` file that is not a page
        for path in vault.non_pages:
            self.typeless.setdefault(path.rsplit("/", 1)[-1].removesuffix(".md"), path)
        self.taken = {n.lower() for n in vault.by_name} | {n.lower() for n in self.typeless}
        self.groups = tuple(self.by_type["stakeholder-group"])
        cap = vault.config.cap
        self.at_cap = cap is not None and len(self.groups) >= cap

    # problems

    def problem(
        self,
        rule: str,
        file: str,
        where: str,
        what: str,
        fix: str,
        *,
        line: int | None = None,
        column: int | None = None,
        pos: int = 0,
        target: str = "",
        field: str = "",
    ) -> Problem:
        return Problem(
            rule, SEVERITY[rule], file, where, what, fix, line, column, (pos, target, field)
        )

    # pages

    def page(self, name: str) -> Page | None:
        """The page of that name, when there is exactly one."""
        pages = self.vault.by_name.get(name, ())
        return pages[0] if len(pages) == 1 else None

    def page_at(self, path: str) -> Page | None:
        return self.vault.address(path).page

    def type_of(self, name: str) -> str | None:
        """The page type of the page named `name`: None when it has none, is unreadable or is ambiguous."""
        p = self.page(name)
        return p.type_key if p else None

    def names_of_type(self, *types: str) -> list[str]:
        return sorted({p.name for t in types for p in self.by_type[t]}, key=lambda s: s.encode())

    def shares_name(self, page: Page) -> bool:
        """Whether another `.md` file has this page's name, compared without regard to case."""
        low = page.name.lower()
        others = [p for p in self.vault.pages if p is not page and p.name.lower() == low]
        return bool(others) or low in {n.lower() for n in self.typeless}

    def relations(self, slug: str) -> list[dict[str, str]]:
        """The pairs the pages of a relation type state: endpoint field -> target (well-formed pages only)."""
        if slug not in self._relations:
            keys = TBOX.page_types[slug].endpoint_order
            rows = []
            for p in self.by_type[slug]:
                ends = {k: self.links(p, k) for k in keys}
                if all(len(v) == 1 for v in ends.values()):
                    rows.append({k: v[0].target for k, v in ends.items()})
            self._relations[slug] = rows
        return self._relations[slug]

    # what the cascade guard asks (catalogue section 1)

    @staticmethod
    def typed(page: Page) -> bool:
        """Readable frontmatter and a valid `type`: a source for rules that need the type."""
        return page.frontmatter_error is None and page.type_key is not None

    @staticmethod
    def status_of(page: Page) -> str | None:
        """The status the status rules read: `done` for a class page, None when missing or invalid."""
        t = TBOX.page_types[page.type_key]
        if not t.carries_status:
            return "done"
        s = page.status
        return s if isinstance(s, str) and s in TBOX.statuses else None

    # the file as written (the reader keeps parsed values, not text)

    def file_lines(self, path: str) -> list[str]:
        if path not in self._lines:
            text = (self.vault.root / path).read_bytes().decode("utf-8", errors="replace")
            self._lines[path] = re.split(r"\r\n|\n", text.removeprefix("\ufeff"))
        return self._lines[path]

    def lines(self, page: Page) -> list[str]:
        return self.file_lines(page.path)

    def current(self, page: Page, key: str) -> str:
        """`<current>`: the text after the colon of the key's line, as written."""
        n = page.field_lines.get(key)
        if n is None:
            return ""
        return self.lines(page)[n - 1].split(":", 1)[-1].strip()

    def list_state(self, page: Page, key: str) -> str:
        """`absent`, `block` (a non-empty block list) or `other` (empty, `[]` or a flow list)."""
        if key not in page.fields:
            return "absent"
        v = page.fields[key]
        return "block" if isinstance(v, list) and v and self.current(page, key) == "" else "other"

    # links

    def links(self, page: Page, key: str) -> list[Link]:
        """The items of a link field that are exactly `[[page-name]]`: the ones other rules can follow."""
        return [l for l in page.fm_links.get(key, ()) if LINK_ITEM.fullmatch(f"[[{l.target}]]")]

    def targets(self, page: Page, key: str) -> list[str]:
        return [l.target for l in page.fm_links.get(key, ())]

    def item(self, page: Page, key: str, target: str) -> str:
        """The item line as the catalogue writes it: `- "[[t]]"`, or `<field>: "[[t]]"` for a single field."""
        f = TBOX.page_types[page.type_key].field(key)
        return f'{key}: "[[{target}]]"' if f and f.single else f'- "[[{target}]]"'

    def pos(self, page: Page, key: str | None) -> int:
        return page.field_lines.get(key, 0) if key else 0

    def add_items(self, page: Page, key: str, targets: list[str], in_file: bool = False) -> str:
        """The edit that puts `targets` into list field `key` (the catalogue's add-or-replace wording)."""
        state = self.list_state(page, key)
        where = f" in {page.path}" if in_file else ""
        if state == "block":
            return f"add under `{key}:`{where} {lines_of(targets)}"
        if state == "absent":
            return f"{'in ' + page.path + ' ' if in_file else ''}add `{key}:` and under it {lines_of(targets)}"
        listed = [l.target for l in page.fm_links.get(key, ())]
        return (
            f"{'in ' + page.path + ' ' if in_file else ''}replace the line `{key}: "
            f"{self.current(page, key)}` with `{key}:` and under it {lines_of(listed + targets)}"
        )


def lines_of(targets: list[str]) -> str:
    items = [f'`- "[[{t}]]"`' for t in targets]
    if len(items) == 1:
        return "the line " + items[0]
    return "the lines " + " then ".join(items)


__all__ = ["DEFERRED", "PAGE_RULES", "VAULT_RULES", "Ctx", "page_rule", "vault_rule"]
