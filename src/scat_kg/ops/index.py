"""Class pages and their index tables (contract section 8).

`index_region` is pure: it says what the generated region of a class page must be, so a rule can
compare against it. `index` writes: it replaces the region (markers included) and nothing outside
it, appends a fresh region when there is no well-formed marker pair, and creates a missing class page.
"""

import re
from pathlib import Path

from scat_kg.ops.common import open_vault
from scat_kg.ops.files import (
    NotUtf8,
    create_files,
    join_lines,
    line_ending,
    read_lines,
    replace_file,
)
from scat_kg.ops.names import CLASS_PAGES, quote
from scat_kg.ops.result import Refusal, Result
from scat_kg.tbox import TBOX
from scat_kg.vault import Page, Vault

START = "<!-- scat:index:start -->"
END = "<!-- scat:index:end -->"
HEADER = ("| Name | Description | Link |", "|---|---|---|")


def _cell(value: object) -> str:
    text = value if isinstance(value, str) else ""
    return re.sub(r"\s*[\r\n]+\s*", " ", text).strip().replace("|", "\\|")


def _row(page: Page) -> str:
    return f"| {_cell(page.fields.get('title'))} | {_cell(page.fields.get('description'))} | [[{page.name}]] |"


def index_region(vault: Vault, name: str) -> str:
    """The generated region of the class page `name`: start marker to end marker, LF, no final newline.

    Rows are every page whose `type` is the class page's `indexes` value, at any status, by page name.
    """
    slug = CLASS_PAGES[name][0]
    pages = sorted(vault.of_type(slug), key=lambda p: p.name)
    return "\n".join([START, *HEADER, *(_row(p) for p in pages), END])


def find_region(lines: list[tuple[str, str]], first: int = 0) -> tuple[int, int] | None:
    """(start, end) line indexes of the first well-formed pair, or None.

    The pair is the first end marker that has a start marker before it, with the nearest start marker
    before it. So a stray start marker above the pair, or a fresh region appended after a stray one,
    never swallows the author's text between them (and running `index` again finds the same pair).
    Marker lines are exact.
    """
    start = None
    for i in range(first, len(lines)):
        if lines[i][0] == START:
            start = i
        elif lines[i][0] == END and start is not None:
            return start, i
    return None


def _norm(line: str) -> str:
    """A table line with padding ignored: spaces around each cell and at the line's ends."""
    cells = re.split(r"(?<!\\)\|", line.strip())
    return "|".join(c.strip() for c in cells)


def same_table(actual: list[str], expected: list[str]) -> bool:
    return [_norm(x) for x in actual] == [_norm(x) for x in expected]


def class_page_text(name: str, region: str) -> str:
    """A new class page: default title, `indexes`, default description, empty body, the region."""
    slug, title = CLASS_PAGES[name]
    return (
        f"---\ntype: class\ntitle: {quote(title)}\n"
        f"description: {quote(TBOX.page_types[slug].description)}\nindexes: {slug}\n---\n\n{region}\n"
    )


def _frontmatter_close(lines: list[tuple[str, str]]) -> int | None:
    if not lines or lines[0][0] != "---":
        return None
    return next((i for i in range(1, len(lines)) if lines[i][0] == "---"), None)


def _class_pages(vault: Vault, name: str) -> tuple[Page | None, str | None]:
    """The class page called `name`, or why the name cannot be used (another page or file has it)."""
    found = vault.by_name.get(name, ())
    others = [p for p in vault.non_pages if p.rsplit("/", 1)[-1] == f"{name}.md"]
    if len(found) == 1 and found[0].type == "class" and not others:
        return found[0], None
    if not found and not others:
        return None, None
    held = [p.path for p in found] + others
    return None, f"`{name}` is the name of a class page, but {', '.join(held)} already has it"


def index_problem(vault: Vault, name: str) -> str | None:
    """Why the class page `name` is stale (SCAT-INDEX-STALE's reason text), or None when it is current.

    Padding is ignored: a table aligned with extra spaces is not stale.
    """
    page, _ = _class_pages(vault, name)
    if page is None:
        return "the page is missing"
    try:
        lines, _bom = read_lines(vault.root / page.path)
    except NotUtf8:
        return "no well-formed marker pair"
    span = find_region(lines, (_frontmatter_close(lines) or 0) + 1)
    if span is None:
        return "no well-formed marker pair"
    actual = [t for t, _ in lines[span[0] + 1 : span[1]]]
    expected = index_region(vault, name).split("\n")[1:-1]
    if same_table(actual, expected):
        return None
    return f"the table differs from the {CLASS_PAGES[name][0]} pages"


def index(*, root: str | Path = ".") -> Result:
    op = "index"
    vault, bad = open_vault(op, root)
    if bad:
        return bad
    created, changed, unchanged, refusals = [], [], [], []
    to_create: list[tuple[Path, str]] = []
    for name in sorted(CLASS_PAGES):
        region = index_region(vault, name)
        page, clash = _class_pages(vault, name)
        if clash:
            refusals.append(
                Refusal(
                    f"class/{name}.md",
                    clash,
                    "rename or move that file (Obsidian rewrites the links to it), then run "
                    "`scat index` (REPL: `scat_kg.index()`) again",
                )
            )
        elif page is None:
            to_create.append((vault.root / "class" / f"{name}.md", class_page_text(name, region)))
            created.append(f"class/{name}.md")
        else:
            outcome = _rewrite(vault, page, name, region)
            if isinstance(outcome, Refusal):
                refusals.append(outcome)
            elif outcome:
                changed.append(page.path)
            else:
                unchanged.append(page.path)
    try:
        create_files(to_create)
    except OSError as e:
        refusals.append(
            Refusal(
                "class/",
                f"could not create the missing class pages: {e}",
                "check the folder's permissions",
            )
        )
        created = []
    return Result(
        op,
        created=tuple(created),
        changed=tuple(changed),
        unchanged=tuple(unchanged),
        refused=tuple(refusals),
    )


def _rewrite(vault: Vault, page: Page, name: str, region: str) -> bool | Refusal:
    """Bring one existing class page's region up to date. True when the file was written."""
    path = vault.root / page.path
    try:
        lines, bom = read_lines(path)
    except NotUtf8 as e:
        return Refusal(page.path, str(e), "save the file as UTF-8, then run `scat index` again")
    close = _frontmatter_close(lines)
    if close is None or page.frontmatter_error:
        return Refusal(
            page.path,
            "its frontmatter cannot be read, so the body cannot be told from it",
            "repair the frontmatter (a block of `key: value` lines between two `---` lines at the "
            "top), then run `scat index` (REPL: `scat_kg.index()`) again",
        )
    eol = line_ending(lines)
    new_rows = region.split("\n")
    span = find_region(lines, close + 1)
    if (
        span is None
    ):  # a fresh region at the end of the body; stray markers and text stay as they are
        if lines[-1][1] == "":
            lines[-1] = (lines[-1][0], eol)
        if lines[-1][0].strip():
            lines.append(("", eol))
        lines += [(row, eol) for row in new_rows]
    else:
        start, end = span
        if same_table([t for t, _ in lines[start + 1 : end]], new_rows[1:-1]):
            return False
        inner = lines[start][1] or eol
        fresh = [(row, inner) for row in new_rows]
        fresh[-1] = (
            new_rows[-1],
            lines[end][1],
        )  # the file may end at the end marker, unterminated
        lines[start : end + 1] = fresh
    try:
        replace_file(path, join_lines(lines, bom))
    except OSError as e:
        return Refusal(page.path, f"could not write: {e}", "check the file's permissions")
    return True
