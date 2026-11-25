"""What an operation returns: what it created, changed and refused, and why, with the exact next step.

The API returns it and the CLI prints `str(result)`, so both paths show the same text (R-8).
Paths are vault-relative with `/` separators, as the catalogue's `<file>`.
"""

from dataclasses import dataclass

from scat_kg.contract import SCHEMA_VERSION
from scat_kg.fix import Command, Fix, FixOption

# The operation's internal name, when it differs from the command name the CLI and the contract use.
_COMMAND_NAME = {"read-status": "status"}


@dataclass(frozen=True)
class Refusal:
    subject: str  # the file, field or name the refusal is about
    why: str
    fix: str  # exact next-step text; with a `rule`, the whole fix block, from "Fix" on
    fix_data: Fix | None = None  # the same fix as data; None means one manual option holding `fix`
    rule: str | None = (
        None  # the catalogue rule that gives the refusal (SCAT-DONE-REFUSED); else None
    )
    problems: tuple = ()  # the problems that make it, each a `Problem`, with its own fix

    def to_dict(self) -> dict:
        fix = self.fix_data or Fix.legacy(self.fix)
        out = {"subject": self.subject, "why": self.why, "fix": fix.to_dict()}
        if self.rule is not None:
            out["rule"] = self.rule
            out["problems"] = [p.to_dict() for p in self.problems]
        return out

    def __str__(self) -> str:
        if self.rule is None:
            return f"refused {self.subject}: {self.why}\n  Fix: {self.fix}"
        lines = [f"refused [{self.rule}] {self.subject}: {self.why}"]
        for p in self.problems:
            lines += ["  " + ln for ln in p.render().split("\n")]
        lines += ["  " + ln for ln in self.fix.split("\n")]
        return "\n".join(lines)


@dataclass(frozen=True)
class Result:
    operation: str
    created: tuple[str, ...] = ()
    changed: tuple[str, ...] = ()
    unchanged: tuple[str, ...] = ()  # looked at and already right: nothing written
    refused: tuple[Refusal, ...] = ()
    notes: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.refused

    def to_dict(self) -> dict:
        return {
            "schema_version": SCHEMA_VERSION,
            "kind": "operation",
            "operation": _COMMAND_NAME.get(self.operation, self.operation),
            "ok": self.ok,
            "created": list(self.created),
            "changed": list(self.changed),
            "unchanged": list(self.unchanged),
            "refused": [r.to_dict() for r in self.refused],
            "notes": list(self.notes),
        }

    def lines(self) -> list[str]:
        out = [f"created {p}" for p in self.created]
        out += [f"changed {p}" for p in self.changed]
        out += [f"unchanged {p}" for p in self.unchanged]
        out += [str(r) for r in self.refused]
        out += [f"note: {n}" for n in self.notes]
        if not (self.created or self.changed or self.unchanged or self.refused):
            out.append(f"{self.operation}: nothing to do")
        return out

    def __str__(self) -> str:
        return "\n".join(self.lines())


def refused(operation: str, subject: str, why: str, fix: str) -> Result:
    return Result(operation, refused=(Refusal(subject, why, fix),))


@dataclass(frozen=True)
class RowRef:
    """One row of a narrative's table that an operation added or removed."""

    narrative: str  # the narrative's name
    file: str  # its path
    line: int  # the row's line: in the file as written (added), or before the write (removed)
    note: str = ""

    def to_dict(self) -> dict:
        return {
            "narrative": self.narrative,
            "file": self.file,
            "line": self.line,
            "note": self.note,
        }


@dataclass(frozen=True)
class EdgeRef:
    """The edge as an operation leaves it: one per (type, from, to), with every narrative that tells it."""

    type: str  # the edge type's slug
    from_node: str
    to_node: str
    narratives: tuple[str, ...] = ()  # in byte order; empty once the last row is gone

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "from": self.from_node,
            "to": self.to_node,
            "narratives": list(self.narratives),
        }


@dataclass(frozen=True)
class EdgeResult(Result):
    """What record-edge and remove-edge return: an operation, and when it ran, the edge and the rows it wrote."""

    edge: EdgeRef | None = None
    rows_added: tuple[RowRef, ...] = ()
    rows_removed: tuple[RowRef, ...] = ()

    def to_dict(self) -> dict:
        out = super().to_dict()
        if self.ok and self.edge is not None:
            out["edge"] = self.edge.to_dict()
            out["rows_added"] = [r.to_dict() for r in self.rows_added]
            out["rows_removed"] = [r.to_dict() for r in self.rows_removed]
        return out


def run_option(text: str, argv: tuple[str, ...], repl: str, slot: str | None = None) -> FixOption:
    """An option that is a command: exact, or a slot when argv holds a placeholder the author replaces."""
    return FixOption("exact" if slot is None else "slot", text, Command(argv, repl, slot))


def refusal(
    subject: str, why: str, text: str, *options: FixOption, sequence: bool = False
) -> Refusal:
    """A refusal whose fix is `text` (shown as is), with the same fix as data: the options in order.

    One option is the fix; several are alternatives, or steps when `sequence`. A manual option is
    `FixOption("manual", text)`.
    """
    if sequence:  # steps: manual as a whole when any step needs the person
        kind = "manual" if any(o.kind == "manual" for o in options) else "exact"
        data = Fix.steps(kind, options)
    else:
        data = Fix(options[0].kind if len(options) == 1 else "options", options)
    return Refusal(subject, why, text, data)
