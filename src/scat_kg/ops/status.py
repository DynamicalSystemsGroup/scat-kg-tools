"""Status: read it at three scopes, and set it on one page (R-3).

Setting a status edits the one `status:` line of the frontmatter (adding that line when it is absent)
and nothing else in the file; line endings stay as they were.
"""

import re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from scat_kg.checks import check_page, check_page_at_done, fixes
from scat_kg.contract import SCHEMA_VERSION
from scat_kg.fix import FixOption
from scat_kg.ops.common import find_page, open_vault
from scat_kg.ops.files import NotUtf8, join_lines, line_ending, read_lines, replace_file
from scat_kg.ops.result import Refusal, Result, refused
from scat_kg.tbox import TBOX
from scat_kg.vault import Page, Vault, read_vault

SCOPES = ("page", "neighborhood", "vault")

_STATUS_LINE = re.compile(r"""^(?P<key>"status"|'status'|status)[ \t]*:[ \t]*(?P<rest>.*)$""")
_VALUE = re.compile(r"""^(?:"[^"]*"|'[^']*'|[^\s#][^#]*?)?(?P<comment>[ \t]*#.*)?[ \t]*$""")


@dataclass(frozen=True)
class StatusRow:
    path: str
    name: str
    type: Any  # as written; None when the page has no readable type
    status: Any  # as written; None when missing

    def to_dict(self) -> dict:
        """A type or status that is not a string is null."""
        return {
            "path": self.path,
            "name": self.name,
            "type": self.type if isinstance(self.type, str) else None,
            "status": self.status if isinstance(self.status, str) else None,
        }


@dataclass(frozen=True)
class StatusReport(Result):
    scope: str = "page"
    rows: tuple[StatusRow, ...] = ()

    @property
    def counts(self) -> dict[str, int]:
        """Pages per status; `other` is a missing or invalid status."""
        counts = {s: 0 for s in TBOX.statuses} | {"other": 0}
        for r in self.rows:
            if isinstance(r.status, str) and r.status in TBOX.statuses:
                counts[r.status] += 1
            else:
                counts["other"] += 1
        return counts

    def to_dict(self) -> dict:
        if self.refused:
            return super().to_dict()
        return {
            "schema_version": SCHEMA_VERSION,
            "kind": "status",
            "operation": "status",
            "ok": True,
            "scope": self.scope,
            "rows": [r.to_dict() for r in self.rows],
            "counts": self.counts,
            "notes": list(self.notes),
        }

    def lines(self) -> list[str]:
        if self.refused:
            return super().lines()
        out = []
        for r in self.rows:
            out.append(f"{_shown(r.status):<12} {r.path}")
        out.append(", ".join(f"{n} {k}" for k, n in self.counts.items() if n) or "no pages")
        return out + [f"note: {n}" for n in self.notes]


def _shown(status: Any) -> str:
    return "(missing)" if status is None else str(status)


def _row(page: Page) -> StatusRow:
    return StatusRow(page.path, page.name, page.type, page.status)


def _neighborhood(vault: Vault, page: Page) -> list[Page]:
    """The page, then every page one link away, either direction, in path order."""
    paths = {page.path}
    for link in page.links:  # out: what this page links, frontmatter and body
        paths.update(p.path for p in vault.by_name.get(link.target, ()))
    paths.update(b.source for b in vault.inbound(page.name))  # in: who links here
    paths.discard(page.path)
    by_path = {p.path: p for p in vault.pages}
    return [page] + [by_path[p] for p in sorted(paths) if p in by_path]


def read_status(
    scope: str = "vault", ref: str | None = None, *, root: str | Path = "."
) -> StatusReport | Result:
    """Status of one page, of a page and everything one link away, or of the whole vault."""
    op = "read-status"
    if scope not in SCOPES:
        return refused(op, scope, "this is not a scope", f"use one of: {', '.join(SCOPES)}")
    vault, bad = open_vault(op, root)
    if bad:
        return bad
    if scope == "vault":
        pages = list(vault.pages)
    else:
        if ref is None:
            return refused(op, scope, "this scope needs a page", "give the page's name or path")
        page, bad = find_page(op, vault, ref)
        if bad:
            return bad
        pages = [page] if scope == "page" else _neighborhood(vault, page)
    return StatusReport(op, scope=scope, rows=tuple(_row(p) for p in pages))


def _continues(lines: list[tuple[str, str]], first: int, stop: int) -> bool:
    """Whether lines[first:stop] hold anything but blanks and comments (a value over several lines)."""
    return any(t.strip() and not t.lstrip().startswith("#") for t, _ in lines[first:stop])


def _done_refusal(page: Page, errors) -> Refusal:
    """SCAT-DONE-REFUSED (catalogue section 5): the errors the page would have at `done`, and the two ways on."""
    n = len(errors)
    draft = fixes.set_status(page.name, "draft")
    fix = fixes.alternatives(
        [
            FixOption(
                "advisory",
                f"fix the problems above, then run `scat set-status {page.name} done` again",
            ),
            fixes.run_option(draft, prefix="leave the page at `draft`: run "),
        ]
    )
    return Refusal(
        page.path,
        f"{n} error(s) would stand at status done; status unchanged",
        fix.render(),
        fix,
        "SCAT-DONE-REFUSED",
        tuple(errors),
    )


def _with_check(result: Result, status: str, root: Path, path: str) -> Result:
    """At `done`, add the page's own check outcome (page scope, read after the write; nothing is written)."""
    if status != "done":
        return result
    vault = read_vault(root)
    page = next(p for p in vault.pages if p.path == path)
    return replace(result, checked=path, problems=check_page(vault, page).problems)


def set_status(name: str, status: str, *, root: str | Path = ".") -> Result:
    op = "set-status"
    if status not in TBOX.statuses:
        return refused(
            op,
            f"status `{status}`",
            "this is not a status",
            f"use one of: {', '.join(TBOX.statuses)} (stub: a name, perhaps some metadata; draft: "
            "content, not yet complete; done: complete, conformant and signed off by the coder)",
        )
    vault, bad = open_vault(op, root)
    if bad:
        return bad
    page, bad = find_page(op, vault, name)
    if bad:
        return bad
    path = vault.root / page.path
    if page.frontmatter_error:
        return refused(
            op,
            page.path,
            f"its frontmatter cannot be read ({page.frontmatter_error.reason})",
            "repair the frontmatter by hand (a block of `key: value` lines between two `---` lines "
            "at the top), then run this again",
        )
    ptype = TBOX.page_types.get(page.type) if isinstance(page.type, str) else None
    if ptype is None or not ptype.carries_status:
        types = ", ".join(k for k, t in TBOX.page_types.items() if t.carries_status)
        return refused(
            op,
            page.path,
            f"its `type` is {page.type!r}, which is not the type of a page",
            f"set `type:` to one of: {types}, then run this again",
        )
    if status == "done" and page.status != "done":
        report = check_page_at_done(vault, page)
        if report.errors:
            return Result(op, refused=(_done_refusal(page, report.errors),))
    try:
        lines, bom = read_lines(path)
    except NotUtf8 as e:
        return refused(op, page.path, str(e), "save the file as UTF-8, then run this again")
    close = next(i for i in range(1, len(lines)) if lines[i][0] == "---")
    key_lines = sorted(page.field_lines.values())

    def value_end(
        line: int,
    ) -> int:  # 0-based index just past the lines that belong to the key at `line`
        later = [n for n in key_lines if n > line]
        return (later[0] if later else close + 1) - 1

    at = page.field_lines.get("status")
    if at is None:  # add the key: after `type:` when that is one line, else before the closing ---
        t = page.field_lines["type"]
        if _continues(lines, t, value_end(t)):
            idx, eol = close, line_ending(lines)
        else:
            idx, eol = t, lines[t - 1][1] or line_ending(lines)
        lines.insert(idx, (f"status: {status}", eol))
        was = "no status line"
    else:
        text, eol = lines[at - 1]
        m = _STATUS_LINE.match(text)
        v = _VALUE.match(m["rest"]) if m else None
        if not m or not v or _continues(lines, at, value_end(at)):
            return refused(
                op,
                f"{page.path}:{at} field `status`",
                "the value is written in a form this operation will not rewrite",
                f"replace the line with `status: {status}` yourself",
            )
        comment = v["comment"] or ""
        if comment and not comment[0].isspace():
            comment = " " + comment
        was = f"was {page.status}" if isinstance(page.status, str) else "was empty"
        if page.status == status and isinstance(page.status, str):
            same = Result(op, unchanged=(page.path,), notes=(f"status is already {status}",))
            return _with_check(same, status, vault.root, page.path)
        lines[at - 1] = (f"{m['key']}: {status}{comment}", eol)
    try:
        replace_file(path, join_lines(lines, bom))
    except OSError as e:
        return Result(
            op,
            refused=(Refusal(page.path, f"could not write: {e}", "check the file's permissions"),),
        )
    done = Result(op, changed=(page.path,), notes=(f"`status` set to {status} ({was})",))
    return _with_check(done, status, vault.root, page.path)
