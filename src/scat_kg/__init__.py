"""scat_kg: check and work on a SCAT knowledge-graph vault from the Python REPL.

    import scat_kg

    scat_kg.check()                     # the whole vault in the current directory
    scat_kg.check("concern/x.md")       # one page (a name or a path)
    scat_kg.check("x", neighborhood=True)
    scat_kg.status()                    # the same three scopes, for status
    scat_kg.set_status("x", "draft")
    scat_kg.index()
    scat_kg.stub("x", type="concern")
    scat_kg.stub_links()                # or stub_links("x")
    scat_kg.record_edge("holds", "a", "b", ["narrative-name"], note="")
    scat_kg.remove_edge("a", "b")       # or remove_edge("a", "b", ["narrative-name"])

Each call takes `root=` (the vault folder; default: the current directory) and returns an object whose
`str()` is the message the `scat` command prints, and which prints as that message. `.ok` is False when
there is an error or a refusal (warnings alone leave it True): it is what the command's exit code is.
"""

from pathlib import Path

from scat_kg.checks import Report, check_neighborhood, check_page, check_vault
from scat_kg.contract import SCHEMA_VERSION
from scat_kg.ops import (
    EdgeResult,
    StatusReport,
    index,
    record_edge,
    remove_edge,
    set_status,
    stub,
    stub_links,
)
from scat_kg.ops import read_status as _read_status
from scat_kg.ops.common import find_page, open_vault
from scat_kg.ops.result import Result, refused

# At the REPL the result prints as its message (R-8), not as a dataclass dump.
for _cls in (Result, StatusReport, EdgeResult):
    _cls.__repr__ = lambda self: str(self)


class CheckResult:
    """What `check` returns: the report of problems, in the catalogue's order, and the text the CLI prints."""

    def __init__(self, report: Report):
        self.report = report

    @property
    def problems(self):
        return self.report.problems

    @property
    def errors(self):
        return self.report.errors

    @property
    def warnings(self):
        return self.report.warnings

    @property
    def ok(self) -> bool:
        return self.report.ok

    def to_dict(self) -> dict:
        return {
            "schema_version": SCHEMA_VERSION,
            "kind": "check",
            "operation": "check",
            "ok": self.ok,
            "problems": [p.to_dict() for p in self.problems],
        }

    def __str__(self) -> str:
        e, w = len(self.errors), len(self.warnings)
        if not self.problems:
            return "no problems"
        total = f"{e} error{'' if e == 1 else 's'}, {w} warning{'' if w == 1 else 's'}"
        return f"{self.report.render()}\n{total}"

    __repr__ = __str__


def check(
    page: str | None = None, *, neighborhood: bool = False, root: str | Path = "."
) -> CheckResult | Result:
    """Check the vault; one page (`page`: a name or a path); or a page and everything one link away."""
    op = "check"
    vault, bad = open_vault(op, root)
    if bad:
        return bad
    if page is None:
        if neighborhood:
            return refused(
                op, "neighborhood", "this scope needs a page", "give the page's name or path"
            )
        return CheckResult(check_vault(vault))
    found, bad = find_page(op, vault, page)
    if bad:
        return bad
    run = check_neighborhood if neighborhood else check_page
    return CheckResult(run(vault, found))


def status(
    page: str | None = None, *, neighborhood: bool = False, root: str | Path = "."
) -> StatusReport | Result:
    """The status of the vault; of one page; or of a page and everything one link away."""
    if page is None:
        scope = "neighborhood" if neighborhood else "vault"
    else:
        scope = "neighborhood" if neighborhood else "page"
    return _read_status(scope, page, root=root)


__all__ = [
    "CheckResult",
    "EdgeResult",
    "Result",
    "StatusReport",
    "check",
    "index",
    "record_edge",
    "remove_edge",
    "set_status",
    "status",
    "stub",
    "stub_links",
]
