"""A fix as data (contracts/machine-interface.md): what kind it is, the command, the edits. The text is generated from it."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Command:
    argv: tuple[str, ...]  # the scat command line, without the leading `scat`
    repl: str  # the same call in the Python REPL
    author_slot: str | None = None  # the placeholder in argv the author must replace

    def to_dict(self) -> dict:
        out: dict = {"argv": list(self.argv), "repl": self.repl}
        if self.author_slot is not None:
            out["author_slot"] = self.author_slot
        return out


@dataclass(frozen=True)
class Edit:
    """One change a tool can apply. `action` is one of set-field, delete-field, replace-text, rename-file,
    delete-file; the other fields are the ones that action takes, and absent ones stay None."""

    action: str
    file: str
    field: str | None = None  # set-field, delete-field
    value: object = None  # set-field: a string, number, boolean or list
    author_slot: str | None = None  # set-field: the placeholder in value the author must replace
    line: int | None = None  # replace-text
    column: int | None = None  # replace-text
    find: str | None = None  # replace-text
    replace: str | None = None  # replace-text
    to: str | None = None  # rename-file

    def to_dict(self) -> dict:
        out: dict = {}
        for key in (
            "action",
            "file",
            "field",
            "value",
            "author_slot",
            "line",
            "column",
            "find",
            "replace",
            "to",
        ):
            v = getattr(self, key)
            if v is not None:
                out[key] = list(v) if isinstance(v, tuple) else v
        return out


@dataclass(frozen=True)
class FixOption:
    kind: str  # exact, slot, advisory or manual
    text: str  # the sentence shown today
    command: Command | None = None
    edits: tuple[Edit, ...] = ()

    def to_dict(self) -> dict:
        out: dict = {"kind": self.kind, "text": self.text}
        if self.command is not None:
            out["command"] = self.command.to_dict()
        if self.edits:
            out["edits"] = [e.to_dict() for e in self.edits]
        return out


@dataclass(frozen=True)
class Fix:
    kind: str  # exact, options, slot, advisory or manual
    options: tuple[FixOption, ...]
    head: str | None = None  # the line that introduces the options; None means the shape's default
    notes: tuple[str, ...] = ()  # unnumbered lines after the options
    sequence: bool = False  # True: do every option in order (steps)
    verbatim: str | None = (
        None  # a legacy fix's text, returned as is by render(); not part of the data
    )
    inline: bool = (
        False  # render the options on one line, `<head> <text>, <text>`; not part of the data
    )

    @classmethod
    def one(cls, kind: str, option: FixOption) -> "Fix":
        return cls(kind, (option,))

    @classmethod
    def choose(
        cls,
        kind: str,
        options: tuple[FixOption, ...] | list[FixOption],
        head: str | None = None,
        notes: tuple[str, ...] = (),
    ) -> "Fix":
        return cls(kind, tuple(options), head, tuple(notes))

    @classmethod
    def steps(
        cls, kind: str, options: tuple[FixOption, ...] | list[FixOption], head: str | None = None
    ) -> "Fix":
        return cls(kind, tuple(options), head, sequence=True)

    @classmethod
    def legacy(cls, text: str) -> "Fix":
        """An already-rendered fix: one manual option holding the text, which render() returns verbatim."""
        return cls("manual", (FixOption("manual", text),), verbatim=text)

    def render(self) -> str:
        if self.verbatim is not None:
            return self.verbatim
        if self.inline:
            return f"{self.head or 'Fix, choose one:'} " + ", ".join(o.text for o in self.options)
        if self.sequence:
            head, indent = self.head or "Fix, two steps:", "     "
        elif len(self.options) == 1 and self.head is None:
            return "\n".join([f"Fix: {self.options[0].text}", *self.notes])
        else:
            head, indent = self.head or "Fix, choose one:", "  "
        rows = [head]
        for i, o in enumerate(self.options, 1):
            first, *more = o.text.split("\n")
            rows.append(f"{indent}{i}. {first}")
            rows.extend(more)
        return "\n".join([*rows, *self.notes])

    def to_dict(self) -> dict:
        out: dict = {"kind": self.kind}
        if self.head is not None:
            out["head"] = self.head
        if self.sequence:
            out["sequence"] = True
        out["options"] = [o.to_dict() for o in self.options]
        out["notes"] = list(self.notes)
        return out
