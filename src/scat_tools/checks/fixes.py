"""Shared builders for fixes as data: commands, edits, options, and the phrase a command gives in text.

A rule builds its fix from these, so the sentence a person reads and the data a tool applies share one source:
the command phrase is generated from the `Command`, the line to put from the `Edit`'s value.
"""

from scat_tools.fix import Command, Edit, Fix, FixOption

# commands: argv is what follows `scat`, repl is the same call in Python


def phrase(cmd: Command) -> str:
    """How text names a command: `scat set-status x draft` (REPL: `scat_tools.set_status("x", "draft")`)."""
    return f"`scat {' '.join(cmd.argv)}` (REPL: `{cmd.repl}`)"


def set_status(name: str, status: str = "draft", *, slot: str | None = None) -> Command:
    return Command(
        ("set-status", name, status), f'scat_tools.set_status("{name}", "{status}")', slot
    )


def stub(name: str, type_key: str, *, slot: str | None = None) -> Command:
    return Command(
        ("stub", name, "--type", type_key), f'scat_tools.stub("{name}", type="{type_key}")', slot
    )


def index() -> Command:
    return Command(("index",), "scat_tools.index()")


# edits: the actions of the contract


def set_field(file: str, field: str, value: object, *, author_slot: str | None = None) -> Edit:
    return Edit("set-field", file, field=field, value=value, author_slot=author_slot)


def delete_field(file: str, field: str) -> Edit:
    return Edit("delete-field", file, field=field)


def replace_text(
    file: str,
    line: int,
    find: str,
    replace: str,
    *,
    column: int | None = None,
    author_slot: str | None = None,
) -> Edit:
    return Edit(
        "replace-text",
        file,
        line=line,
        column=column,
        find=find,
        replace=replace,
        author_slot=author_slot,
    )


def delete_line(file: str, line: int, find: str) -> Edit:
    """Remove one whole line (a table row); `find` is the line as written, a guard."""
    return Edit("delete-line", file, line=line, find=find)


def rename_file(file: str, to: str) -> Edit:
    return Edit("rename-file", file, to=to)


def delete_file(file: str) -> Edit:
    return Edit("delete-file", file)


# options and fixes


def option(kind: str, text: str, *edits: Edit, command: Command | None = None) -> FixOption:
    return FixOption(kind, text, command=command, edits=edits)


def run_option(cmd: Command, prefix: str = "run ", suffix: str = "") -> FixOption:
    """An option that runs `cmd`: its text is `<prefix><phrase><suffix>`; a slot command makes it a slot option."""
    return FixOption(
        "slot" if cmd.author_slot else "exact", f"{prefix}{phrase(cmd)}{suffix}", command=cmd
    )


def single(opt: FixOption) -> Fix:
    """A fix of one option: its kind is the option's."""
    return Fix.one(opt.kind, opt)


def alternatives(
    opts: list[FixOption], head: str | None = None, notes: tuple[str, ...] = ()
) -> Fix:
    """A fix of alternatives (kind `options`); one option left is the fix, and its kind is the fix's (the schema
    wants two or more for `options`). The notes follow either way."""
    kind = opts[0].kind if len(opts) == 1 else "options"
    return Fix.choose(kind, opts, head, notes)


def inline(opts: list[FixOption], head: str = "Fix, choose one:") -> Fix:
    """Alternatives told on one line, `<head> <text>, <text>`. The text is made from the options' own."""
    return Fix("options", tuple(opts), head, inline=True)


# put this line


def put_line(ctx, page, key: str, line: str) -> str:
    """The catalogue's add-or-replace: add the line when the key is absent, replace it when empty."""
    if key not in page.fields:
        return f"add the line `{line}`"
    return f"replace the line `{f'{key}: {ctx.current(page, key)}'.rstrip()}` with `{line}`"


def put_field(
    ctx,
    page,
    key: str,
    value: object,
    line: str,
    *,
    tail: str = "",
    slot: str | None = None,
) -> FixOption:
    """Put `line` for front-matter `key`, as data (set-field of `value`) and as the sentence `put_line` gives."""
    return option(
        "slot" if slot else "exact",
        put_line(ctx, page, key, line) + tail,
        set_field(page.path, key, value, author_slot=slot),
    )
