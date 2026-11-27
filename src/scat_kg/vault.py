"""Reading a vault: the pages, links, backlinks and configuration of a directory, as data.

Reading never writes, and never raises for what is wrong in a vault: a frontmatter that cannot be read,
a missing or malformed `scat.toml`, a name that is ambiguous or absent are all represented in the result,
for the checks to grade. The contract is `contracts/page-contracts.md`; "section N" below means its sections.
This is the page reader behind the public loader (`scat_kg.graph.load`).
"""

import os
import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from pydantic import BaseModel, ValidationError

from scat_kg.models import MODELS
from scat_kg.tbox import TBOX

_BODY_LINK = re.compile(r"\[\[([^\[\]\n]*)\]\]")
_CODE_SPAN = re.compile(r"(`+)(?!`)((?:(?!\n[ \t]*\n).)*?)(?<!`)\1(?!`)", re.DOTALL)
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_KEY_LINE = re.compile(r"""^(?:"([^"]*)"|'([^']*)'|([^\s#:'"-][^:]*?))\s*:(?:\s|$)""")


# The Obsidian page-template folder, skipped whole; `.obsidian/` is a dot-folder, skipped too.
DEFAULT_TEMPLATES_FOLDER = "templates"

# The attribution modes (section 10): a vault declares one in `scat.toml`, key `attribution`.
ATTRIBUTION_KEY = "attribution"
MODES = ("required", "optional", "disallowed")

# The link field that names a narrative's contributors, and the page type it links (the TBox's).
ATTRIBUTED_KEY = "attributed_to"
CONTRIBUTOR = TBOX.page_types["narrative"].field(ATTRIBUTED_KEY).target_type


@dataclass(frozen=True)
class Link:
    target: str  # the page name inside the brackets, trimmed, alias, heading and block reference stripped
    line: int  # 1-based line in the file
    column: int  # 1-based column of the first `[` of the link


@dataclass(frozen=True)
class FrontmatterError:
    reason: str  # the parser's reason, or "the closing --- line is missing"
    line: int | None  # 1-based file line the parser rejected, when it says


@dataclass(frozen=True, eq=False)
class Page:
    path: str  # vault-relative, `/` separators: the catalogue's <file>
    name: str  # the file name without `.md`
    fields: dict[str, Any]  # the frontmatter mapping as YAML read it; {} when unreadable
    field_lines: dict[str, int]  # 1-based file line of each top-level key
    frontmatter_error: FrontmatterError | None
    body: str  # everything after the closing `---`, with LF line endings
    body_line: int  # 1-based file line of the first body line
    body_links: tuple[
        Link, ...
    ]  # page links in the body, in file order (section 3): the only links
    model: (
        BaseModel | None
    )  # the page type's model of the fields; None if type unknown or shape wrong
    model_error: ValidationError | None

    @property
    def type(self) -> Any:
        """The `type` value as written (None for a page whose frontmatter is unreadable)."""
        return self.fields.get("type")

    @property
    def type_key(self) -> str | None:
        """The `type`, when it is one of the TBox's page types."""
        t = self.type
        return t if isinstance(t, str) and t in TBOX.page_types else None

    @property
    def status(self) -> Any:
        return self.fields.get("status")

    @property
    def links(self) -> tuple[Link, ...]:
        """Every page link: frontmatter links are never read (section 3)."""
        return self.body_links


@dataclass(frozen=True)
class VaultConfig:
    """`scat.toml` (section 10). `problem` is None when the cap is a usable value; the attribution mode
    has its own fields."""

    problem: str | None  # "missing", "invalid-toml", "key-missing" or "bad-value"
    detail: str | None  # the parser's reason (invalid-toml); the value as TOML shows it (bad-value)
    cap: int | None  # stakeholder_group_cap when usable
    templates_folder: str = DEFAULT_TEMPLATES_FOLDER  # vault-relative folder the reader skips
    link_suggestions: bool = False  # true turns SCAT-MENTION on
    link_suggestions_bad: str | None = None  # the value as TOML shows it when it is not a boolean
    attribution: str | None = None  # the attribution mode (one of MODES) when declared and known
    attribution_problem: str | None = (
        None  # "key-missing" or "bad-value"; None when usable, or no file
    )
    attribution_detail: str | None = None  # the value as TOML shows it (bad-value)


@dataclass(frozen=True)
class Backlink:
    source: str  # path of the page that links
    line: int
    column: int


@dataclass(frozen=True)
class Lookup:
    """The answer to addressing a page: zero, one or several pages."""

    ref: str
    pages: tuple[Page, ...]

    @property
    def page(self) -> Page | None:
        return self.pages[0] if len(self.pages) == 1 else None

    @property
    def not_found(self) -> bool:
        return not self.pages

    @property
    def ambiguous(self) -> bool:
        return len(self.pages) > 1


@dataclass(frozen=True)
class Vault:
    root: Path
    pages: tuple[Page, ...]  # sorted by path
    by_name: dict[str, tuple[Page, ...]]  # more than one page under a name is a duplicate
    non_pages: tuple[str, ...]  # paths of `.md` files that are not pages: they still take a name
    config: VaultConfig
    backlinks: dict[str, tuple[Backlink, ...]] = field(default_factory=dict)  # by target name

    def of_type(self, slug: str) -> tuple[Page, ...]:
        return tuple(p for p in self.pages if p.type == slug)

    def inbound(self, name: str) -> tuple[Backlink, ...]:
        return self.backlinks.get(name, ())

    def dangling(self) -> tuple[tuple[Page, Link], ...]:
        """Every page link whose target is not the name of a page."""
        return tuple((p, l) for p in self.pages for l in p.links if l.target not in self.by_name)

    def address(self, ref: str) -> Lookup:
        """Find a page by name or by path. A name never contains a dot (section 2), a path ends in `.md`.

        A path is vault-relative with `/` (the catalogue's <file>), or absolute inside the vault.
        """
        if not ref.endswith(".md") and "/" not in ref and "\\" not in ref:
            return Lookup(ref, self.by_name.get(ref, ()))
        path = Path(ref)
        if path.is_absolute():
            try:
                path = path.relative_to(self.root)
            except ValueError:
                return Lookup(ref, ())
        rel = PurePosixPath(*path.parts).as_posix() if len(path.parts) else ""
        return Lookup(ref, tuple(p for p in self.pages if p.path == rel))


def _lines(text: str) -> list[str]:
    return re.split(r"\r\n|\n", text)


def _split(lines: list[str]) -> tuple[int | None, bool]:
    """(index of the closing `---` line, whether the file opens with `---`)."""
    if lines[0] != "---":
        return None, False
    for i in range(1, len(lines)):
        if lines[i] == "---":
            return i, True
    return None, True


def _parse_frontmatter(lines: list[str], close: int | None) -> tuple[dict, FrontmatterError | None]:
    if close is None:
        return {}, FrontmatterError("the closing --- line is missing", None)
    try:
        data = yaml.safe_load("\n".join(lines[1:close]))
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        reason = getattr(e, "problem", None) or str(e)
        return {}, FrontmatterError(reason, None if mark is None else mark.line + 2)
    if not isinstance(data, dict):
        return {}, FrontmatterError("the frontmatter is not a mapping of keys to values", None)
    return data, None


def _key_lines(lines: list[str], close: int) -> dict[str, int]:
    found: dict[str, int] = {}
    for i in range(1, close):
        m = _KEY_LINE.match(lines[i])
        if m:
            found.setdefault(next(g for g in m.groups() if g is not None), i + 1)
    return found


def blank_code(body: str) -> str:
    """The body with fenced code blocks and code spans turned to spaces (line breaks kept)."""
    out, fence = [], None
    for line in body.split("\n"):
        m = _FENCE.match(line)
        if fence is None and m:
            fence = (m.group(1)[0], len(m.group(1)))
            out.append(" " * len(line))
        elif fence is not None:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1]:
                fence = None
            out.append(" " * len(line))
        else:
            out.append(line)
    text = "\n".join(out)
    return _CODE_SPAN.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)


def link_target(inner: str) -> str | None:
    """The page name a link's text (between the brackets) reaches, or None when it is not a page link.

    The alias, heading and block reference are stripped, an escaped bar (`\\|`, as in a table cell) with
    them, and the name is read trimmed (section 3).
    """
    target = re.split(r"[|#^]", inner, maxsplit=1)[0].rstrip("\\").strip()
    if not target or "." in target or "/" in target:
        return None
    return target


def fenced_lines(lines: list[str]) -> list[bool]:
    """For each line, whether it is part of a fenced code block (its fence lines included)."""
    out, fence = [], None
    for line in lines:
        m = _FENCE.match(line)
        if fence is None and m:
            fence = (m.group(1)[0], len(m.group(1)))
            out.append(True)
        elif fence is not None:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1]:
                fence = None
            out.append(True)
        else:
            out.append(False)
    return out


_ENTRY_LINK = re.compile(r"^!?\[\[(.*)\]\]$", re.DOTALL)


def entry_target(entry: str) -> str | None:
    """The page name a link-field entry (`"[[ada-quill]]"`) reaches, or None when it is not a link to a page.

    A link field is the one place a link outside the body is read (section 3); it is read as text, never as a link
    of the page: it is in no `links`, no backlink and no fingerprint.
    """
    m = _ENTRY_LINK.match(entry.strip())
    if m is None or "[[" in m.group(1) or "]]" in m.group(1):
        return None
    return link_target(m.group(1))


def link_entries(page: "Page", key: str) -> list[str] | None:
    """A link field's entries as written, blank ones dropped; None when it is not a list of text."""
    v = page.fields.get(key)
    if v is None or (isinstance(v, str) and not v.strip()) or v == []:
        return []
    if isinstance(v, list) and all(isinstance(n, str) for n in v):
        return [n for n in v if n.strip()]
    return None


def _body_links(body: str, first_line: int) -> tuple[Link, ...]:
    blanked = blank_code(body)
    links = []
    for m in _BODY_LINK.finditer(blanked):
        target = link_target(m.group(1))
        if target is None:
            continue
        line_start = blanked.rfind("\n", 0, m.start()) + 1
        links.append(
            Link(target, first_line + body.count("\n", 0, m.start()), m.start() - line_start + 1)
        )
    return tuple(links)


def _read_page(path: Path, rel: str) -> Page | None:
    """The page in a file, or None when the file is not a page (section 1)."""
    text = path.read_bytes().decode("utf-8", errors="replace").removeprefix("﻿")
    lines = _lines(text)
    close, opens = _split(lines)
    if not opens:
        return None
    fields, error = _parse_frontmatter(lines, close)
    if error is None and "type" not in fields:
        return None
    body, body_line = "", len(lines) + 1
    field_lines, body_links = {}, ()
    if error is None:
        field_lines = _key_lines(lines, close)
        body, body_line = "\n".join(lines[close + 1 :]), close + 2
        body_links = _body_links(body, body_line)
    model, model_error = None, None
    if error is None and isinstance(fields["type"], str) and fields["type"] in MODELS:
        try:
            model = MODELS[fields["type"]].model_validate(fields)
        except ValidationError as e:
            model_error = e
    return Page(
        path=rel,
        name=rel.rsplit("/", 1)[-1].removesuffix(".md"),
        fields=fields,
        field_lines=field_lines,
        frontmatter_error=error,
        body=body,
        body_line=body_line,
        body_links=body_links,
        model=model,
        model_error=model_error,
    )


def _read_config(root: Path) -> VaultConfig:
    file = root / "scat.toml"
    if not file.is_file():
        return VaultConfig("missing", None, None)
    try:
        data = tomllib.loads(file.read_bytes().decode("utf-8", errors="replace"))
    except tomllib.TOMLDecodeError as e:
        return VaultConfig("invalid-toml", str(e), None)
    folder = data.get("templates_folder")
    if not isinstance(folder, str) or not folder.strip("/ "):
        folder = DEFAULT_TEMPLATES_FOLDER
    folder = folder.strip("/ ")
    suggest = data.get("link_suggestions", False)
    extra = (suggest, None) if isinstance(suggest, bool) else (False, repr(suggest))
    if ATTRIBUTION_KEY not in data:
        extra += (None, "key-missing", None)
    elif isinstance(data[ATTRIBUTION_KEY], str) and data[ATTRIBUTION_KEY] in MODES:
        extra += (data[ATTRIBUTION_KEY], None, None)
    else:
        extra += (None, "bad-value", repr(data[ATTRIBUTION_KEY]))
    if "stakeholder_group_cap" not in data:
        return VaultConfig("key-missing", None, None, folder, *extra)
    value = data["stakeholder_group_cap"]
    if isinstance(value, int) and not isinstance(value, bool) and value >= 1:
        return VaultConfig(None, None, value, folder, *extra)
    return VaultConfig("bad-value", repr(value), None, folder, *extra)


def read_mode(root: str | Path) -> str | None:
    """The vault's attribution mode, or None when it is not declared (or is unknown). Reads only `scat.toml`."""
    try:
        return _read_config(Path(root)).attribution
    except OSError:
        return None


def read_vault(root: str | Path) -> Vault:
    root = Path(root)
    config = _read_config(root)
    skip = PurePosixPath(config.templates_folder).parts
    pages, non_pages = [], []
    for dirpath, dirnames, filenames in os.walk(root):
        here = Path(dirpath).relative_to(root).parts
        dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and (*here, d) != skip)
        for filename in filenames:
            if not filename.endswith(".md"):
                continue
            path = Path(dirpath, filename)
            rel = path.relative_to(root).as_posix()
            page = _read_page(path, rel)
            if page is None:
                non_pages.append(rel)
            else:
                pages.append(page)
    pages.sort(key=lambda p: p.path)
    by_name: dict[str, list[Page]] = {}
    inbound: dict[str, list[Backlink]] = {}
    for p in pages:
        by_name.setdefault(p.name, []).append(p)
        for l in p.links:
            inbound.setdefault(l.target, []).append(Backlink(p.path, l.line, l.column))
    return Vault(
        root=root,
        pages=tuple(pages),
        by_name={n: tuple(ps) for n, ps in by_name.items()},
        non_pages=tuple(sorted(non_pages)),
        config=config,
        backlinks={n: tuple(b) for n, b in inbound.items()},
    )
