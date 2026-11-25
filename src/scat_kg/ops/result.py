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
    fix: str  # exact next-step text
    fix_data: Fix | None = None  # the same fix as data; None means one manual option holding `fix`

    def to_dict(self) -> dict:
        fix = self.fix_data or Fix.legacy(self.fix)
        return {"subject": self.subject, "why": self.why, "fix": fix.to_dict()}

    def __str__(self) -> str:
        return f"refused {self.subject}: {self.why}\n  Fix: {self.fix}"


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


NOT_BUILT = "not built yet (WP16-U6 / WP16-U7)"


def not_built(operation: str) -> Result:
    """The standard refusal of a call that is not rebuilt for the row model yet (WP16-U6 checks, WP16-U7 operations)."""
    return refused(
        operation,
        operation,
        NOT_BUILT,
        "read the vault with `scat_kg.graph.load` until the call is rebuilt",
    )


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
