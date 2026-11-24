"""The record a check returns, and the catalogue's message format (section 1, "Order and format")."""

from dataclasses import dataclass, replace

from scat_kg.fix import Fix

# Every rule in the catalogue and its severity (section 3). SCAT-INDEX-STALE is listed so the id is known
# and its severity is fixed, but no check function is registered for it yet (see registry.DEFERRED).
SEVERITY = {
    "SCAT-FM-PARSE": "error",
    "SCAT-FM-REQUIRED": "error",
    "SCAT-FM-TYPE": "error",
    "SCAT-FM-REQUIRED-LINK": "error",
    "SCAT-FM-STATUS": "error",
    "SCAT-FM-INDEXES": "error",
    "SCAT-FM-TIMEFRAME": "error",
    "SCAT-FM-SHAPE": "error",
    "SCAT-NAME": "error",
    "SCAT-DONE-FIELD": "error",
    "SCAT-DONE-LINK": "error",
    "SCAT-DRAFT-FIELD": "warning",
    "SCAT-DRAFT-LINK": "warning",
    "SCAT-LINK-SHAPE": "error",
    "SCAT-LINK-UNLISTED": "error",
    "SCAT-LINK-ENDPOINT": "error",
    "SCAT-LINK-DANGLING": "error",
    "SCAT-LINK-DANGLING-BODY": "error",
    "SCAT-LINK-DISCOURAGED": "warning",
    "SCAT-LINK-DISCOURAGED-BODY": "warning",
    "SCAT-CAP": "error",
    "SCAT-CAP-CONFIG": "error",
    "SCAT-CONFLICT-SELF": "warning",
    "SCAT-REL-DUPLICATE": "warning",
    "SCAT-MENTION": "warning",
    "SCAT-RAW-BACKLINK": "warning",
    "SCAT-RAW-UNCODED": "warning",
    "SCAT-INDEX-STALE": "warning",
}


@dataclass(frozen=True)
class Problem:
    rule: str
    severity: str  # "error" blocks; "warning" does not
    file: str  # the catalogue's <file>: vault-relative, `/` separators (or `scat.toml`)
    where: str  # "field `x`", "link [[t]]", "fields `a` and `b`", "frontmatter", "text `...`"
    what: str  # what is wrong
    fix: str  # the whole fix block, from "Fix" on; always the text of `fix_data`
    line: int | None = None
    column: int | None = None
    order: tuple = ()  # (file position of the key, target, field): the tail of the sort key
    repeat: int = 1  # how many identical messages this one stands for
    fix_data: Fix | None = None  # the fix as data; None builds `Fix.legacy(fix)` from the string
    field: str | None = (
        None  # the front-matter field the problem is about; None for a link, name, etc.
    )

    def __post_init__(self):
        if self.fix_data is None:
            object.__setattr__(self, "fix_data", Fix.legacy(self.fix))
        else:
            object.__setattr__(self, "fix", self.fix_data.render())

    @property
    def elements(self) -> tuple[str, str, str, str]:
        """The four elements a golden test compares: rule id, file, field or link, exact fix."""
        return (self.rule, self.file, self.where, self.fix)

    @property
    def sort_key(self) -> tuple:
        return (
            self.file.encode(),
            -1 if self.line is None else self.line,
            -1 if self.column is None else self.column,
            self.rule,
            *self.order,
        )

    def render(self) -> str:
        loc = self.file
        if self.line is not None:
            loc += f":{self.line}"
            if self.column is not None:
                loc += f":{self.column}"
        again = f" (x{self.repeat})" if self.repeat > 1 else ""
        head = f"{self.severity} [{self.rule}] {loc} {self.where}: {self.what}{again}"
        return head + "\n" + "\n".join("  " + ln for ln in self.fix.split("\n"))

    def to_dict(self) -> dict:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "file": self.file,
            "line": self.line,
            "column": self.column,
            "field": self.field,
            "where": self.where,
            "what": self.what,
            "repeat": self.repeat,
            "fix": self.fix_data.to_dict(),
            "text": self.render(),
        }


def finalize(problems: list[Problem]) -> tuple[Problem, ...]:
    """Merge identical messages into one with a count, then sort into the catalogue's total order."""
    merged: dict[tuple, Problem] = {}
    for p in problems:
        key = (p.rule, p.file, p.line, p.column, p.where, p.what)
        if key in merged:
            merged[key] = replace(merged[key], repeat=merged[key].repeat + 1)
        else:
            merged[key] = p
    return tuple(sorted(merged.values(), key=lambda p: p.sort_key))


@dataclass(frozen=True)
class Report:
    """What a check returns: the problems in the catalogue's order, and whether the checked set is ok."""

    problems: tuple[Problem, ...]

    @property
    def errors(self) -> tuple[Problem, ...]:
        return tuple(p for p in self.problems if p.severity == "error")

    @property
    def warnings(self) -> tuple[Problem, ...]:
        return tuple(p for p in self.problems if p.severity == "warning")

    @property
    def ok(self) -> bool:
        """Errors block; warnings do not."""
        return not self.errors

    def render(self) -> str:
        return "\n".join(p.render() for p in self.problems)
