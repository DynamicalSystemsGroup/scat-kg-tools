"""Edits of a link as written: the literal `[[...]]` at a place, and the same with another page name."""

import re
from dataclasses import dataclass

from scat_kg.checks.ctx import Ctx
from scat_kg.vault import Link, Page

_LITERAL = re.compile(r"\[\[([^\[\]\n]*)\]\]")


@dataclass(frozen=True)
class Literal:
    column: int  # 1-based column of the first `[` in the line
    text: str  # the link as written, `[[ name |alias]]`
    inner: str  # the text between the brackets

    def with_name(self, name: str) -> str:
        """The literal with its page name replaced; the spaces, alias, heading and block reference are kept."""
        cut = next((i for i, c in enumerate(self.inner) if c in "|#^"), len(self.inner))
        head, tail = self.inner[:cut], self.inner[cut:]
        if head.endswith("\\") and tail.startswith("|"):  # a bar escaped for a table cell
            head, tail = head[:-1], "\\" + tail
        lead = head[: len(head) - len(head.lstrip())]
        trail = head[len(head.rstrip()) :]
        return f"[[{lead}{name}{trail}{tail}]]"

    @property
    def shown(self) -> str:
        """The words a reader sees: the alias, else the page name."""
        cut = next((i for i, c in enumerate(self.inner) if c in "|#^"), len(self.inner))
        head, tail = self.inner[:cut], self.inner[cut:]
        if tail.startswith("|"):
            return tail[1:].strip()
        return head.rstrip("\\").strip()


def literal(ctx: Ctx, page: Page, link: Link) -> Literal:
    """The link as written in the page (the body's own line, which the table reader's columns refer to)."""
    line = ctx.body_text(page, link.line)
    m = _LITERAL.match(line, link.column - 1)
    assert m is not None  # the reader found the link at this place
    return Literal(link.column, m.group(0), m.group(1))
