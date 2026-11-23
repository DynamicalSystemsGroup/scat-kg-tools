"""What an operation returns: what it created, changed and refused, and why, with the exact next step.

The API returns it and the CLI prints `str(result)`, so both paths show the same text (R-8).
Paths are vault-relative with `/` separators, as the catalogue's `<file>`.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Refusal:
    subject: str  # the file, field or name the refusal is about
    why: str
    fix: str  # exact next-step text

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
