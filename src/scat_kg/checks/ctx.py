"""What a rule sees: the vault, plus the lookups the rules share. Reading only; nothing here writes."""

import re
from collections import defaultdict
from collections.abc import Callable

from scat_kg.checks.problem import SEVERITY, Problem
from scat_kg.fix import Fix
from scat_kg.graph import TableReading, read_table
from scat_kg.tbox import TBOX
from scat_kg.vault import Page, Vault

PAGE_RULES: list[Callable[["Ctx", Page], list[Problem]]] = []
VAULT_RULES: list[Callable[["Ctx"], list[Problem]]] = []

# Rules in the catalogue that are not implemented here, and why: none. A rule is added by writing a function
# in a module of this package, decorating it with @page_rule or @vault_rule, and importing the module in
# `checks/run.py`.
DEFERRED: dict[str, str] = {}

# The page types a Markdown file can have: the TBox's types that carry a status (`index` is a generated Base).
PAGE_TYPES: tuple[str, ...] = tuple(k for k, t in TBOX.page_types.items() if t.carries_status)
NODE_TYPES: tuple[str, ...] = TBOX.layers  # the four layers, in order
NARRATIVE: str = TBOX.table_type.slug


def page_rule(fn):
    """Register a rule that reports on one page (it may read others)."""
    PAGE_RULES.append(fn)
    return fn


def vault_rule(fn):
    """Register a rule that reports on the vault (SCAT-CAP, SCAT-CAP-CONFIG)."""
    VAULT_RULES.append(fn)
    return fn


class Ctx:
    def __init__(self, vault: Vault, as_done: Page | None = None):
        self.vault = vault
        self.as_done = as_done  # the page judged as it would stand at `done` (catalogue section 5)
        self.whole = False  # True when the whole vault is being checked
        self.focus: Page | None = None  # the page a page or neighborhood check is of
        self._lines: dict[str, list[str]] = {}
        self._tables: dict[str, TableReading] = {}
        self._row_layers: dict[str, set[str]] | None = None
        self.by_type: dict[str, list[Page]] = defaultdict(list)
        for p in vault.pages:
            if p.type_key in PAGE_TYPES:
                self.by_type[p.type_key].append(p)
        self.typeless: dict[str, str] = {}  # name -> path of a `.md` file that is not a page
        for path in vault.non_pages:
            self.typeless.setdefault(path.rsplit("/", 1)[-1].removesuffix(".md"), path)
        self.taken = {n.lower() for n in vault.by_name} | {n.lower() for n in self.typeless}
        self.groups = tuple(self.by_type[NODE_TYPES[0]])
        cap = vault.config.cap
        self.at_cap = cap is not None and len(self.groups) >= cap

    # problems

    def problem(
        self,
        rule: str,
        file: str,
        where: str,
        what: str,
        fix: str | Fix,
        *,
        line: int | None = None,
        column: int | None = None,
        pos: int = 0,
        target: str = "",
        field: str = "",  # a sort-key tail; the front-matter field's name when `on` is given
        on: str | None = None,  # the front-matter field the problem is about
    ) -> Problem:
        data = Fix.legacy(fix) if isinstance(fix, str) else fix
        return Problem(
            rule,
            SEVERITY[rule],
            file,
            where,
            what,
            data.render(),
            line,
            column,
            (pos, target, field or on or ""),
            fix_data=data,
            field=on,
        )

    # pages

    def page(self, name: str) -> Page | None:
        """The page of that name, when there is exactly one."""
        pages = self.vault.by_name.get(name, ())
        return pages[0] if len(pages) == 1 else None

    def type_of(self, name: str) -> str | None:
        """The page type of the page named `name`: None when it has none, is unreadable or is ambiguous."""
        p = self.page(name)
        return self.type_key(p) if p else None

    def names_of_type(self, *types: str) -> list[str]:
        return sorted({p.name for t in types for p in self.by_type[t]}, key=lambda s: s.encode())

    def shares_name(self, page: Page) -> bool:
        """Whether another `.md` file has this page's name, compared without regard to case."""
        low = page.name.lower()
        others = [p for p in self.vault.pages if p is not page and p.name.lower() == low]
        return bool(others) or low in {n.lower() for n in self.typeless}

    # what the cascade guard asks (catalogue section 1)

    @staticmethod
    def type_key(page: Page) -> str | None:
        """The page's `type` when it is one of the five page types of a Markdown page."""
        return page.type_key if page.type_key in PAGE_TYPES else None

    @classmethod
    def typed(cls, page: Page) -> bool:
        """Readable frontmatter and a valid `type`: a source for rules that need the type."""
        return page.frontmatter_error is None and cls.type_key(page) is not None

    def is_narrative(self, page: Page) -> bool:
        return self.typed(page) and page.type_key == NARRATIVE

    def status_of(self, page: Page) -> str | None:
        """The status the status rules read: None when missing or invalid (they then say nothing).

        The page judged as it would stand at `done` reads `done` whatever it says (section 5).
        """
        if page is self.as_done:
            return "done"
        s = page.status
        return s if isinstance(s, str) and s in TBOX.statuses else None

    def pair(self, page: Page, stem: str) -> str | None:
        """The id of a pair rule `stem` (`TABLE-ROW`) for the page: `DRAFT` while it is a stub or draft, `DONE` once
        done; None when the page's status is missing or invalid (the status error is the page's, once)."""
        status = self.status_of(page)
        if status is None:
            return None
        return f"SCAT-{'DONE' if status == 'done' else 'DRAFT'}-{stem}"

    # the file as written (the reader keeps parsed values, not text)

    def file_lines(self, path: str) -> list[str]:
        if path not in self._lines:
            text = (self.vault.root / path).read_bytes().decode("utf-8", errors="replace")
            self._lines[path] = re.split(r"\r\n|\n", text.removeprefix("﻿"))
        return self._lines[path]

    def lines(self, page: Page) -> list[str]:
        return self.file_lines(page.path)

    def current(self, page: Page, key: str) -> str:
        """`<current>`: the text after the colon of the key's line, as written."""
        n = page.field_lines.get(key)
        if n is None:
            return ""
        return self.lines(page)[n - 1].split(":", 1)[-1].strip()

    def pos(self, page: Page, key: str | None) -> int:
        return page.field_lines.get(key, 0) if key else 0

    # a narrative's table (page contracts 4)

    def reading(self, page: Page) -> TableReading | None:
        """The table of a narrative as the loader reads it; None for a page that tells no table (not a narrative)."""
        if not self.is_narrative(page):
            return None
        if page.path not in self._tables:
            self._tables[page.path] = read_table(page.body.split("\n"), page.body_line)
        return self._tables[page.path]

    def body_text(self, page: Page, line: int) -> str:
        """The body line at file line `line`, as written (LF; the table reader's lines)."""
        return page.body.split("\n")[line - page.body_line]

    @property
    def row_layers(self) -> dict[str, set[str]]:
        """For each name some row end of the vault names: the layers (node types) those rows fix for it."""
        if self._row_layers is None:
            found: dict[str, set[str]] = defaultdict(set)
            for p in self.by_type[NARRATIVE]:
                reading = self.reading(p)
                for row in reading.table.rows if reading and reading.table else ():
                    et = TBOX.edge_types.get(row.edge_type or "")
                    if et is None or not row.well_formed:
                        continue
                    for target, layer in (
                        (row.from_target, et.from_type),
                        (row.to_target, et.to_type),
                    ):
                        if target:
                            found[target].add(layer)
            self._row_layers = dict(found)
        return self._row_layers

    def row_ends(self, page: Page) -> set[tuple[int, int]]:
        """(file line, column) of the first character of every `from` and `to` cell of the rows read: the links
        there are row ends, graded by the end rules and not by SCAT-LINK-DANGLING-BODY."""
        reading = self.reading(page)
        if reading is None or reading.table is None:
            return set()
        spots = set()
        for row in reading.table.rows:
            for holds in ("from", "to"):
                cell = row.cell(holds)
                if cell is not None:
                    spots |= {
                        (cell.line, c) for c in range(cell.column, cell.column + len(cell.raw))
                    }
        return spots


__all__ = [
    "DEFERRED",
    "NARRATIVE",
    "NODE_TYPES",
    "PAGE_RULES",
    "PAGE_TYPES",
    "VAULT_RULES",
    "Ctx",
    "page_rule",
    "vault_rule",
]
