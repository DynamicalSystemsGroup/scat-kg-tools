"""WP26-R3: a docs page quotes only commands and options the CLI has.

Every `scat <command>` in a fenced block or in backticks names a real subcommand, and every `--option` written
on the same line is one that command (or the top-level parser) accepts.
"""

import argparse
import re
from pathlib import Path

import pytest

from scat_kg.cli import _parser

ROOT = Path(__file__).resolve().parents[2]


def _options(parser: argparse.ArgumentParser) -> set[str]:
    """The long options of a parser and of every command nested under it."""
    out = {o for a in parser._actions for o in a.option_strings if o.startswith("--")}
    for a in parser._actions:
        if isinstance(a, argparse._SubParsersAction):
            for sub in a.choices.values():
                out |= _options(sub)
    return out


def _commands() -> dict[str, set[str]]:
    top = _parser()
    out: dict[str, set[str]] = {}
    for action in top._actions:
        if isinstance(action, argparse._SubParsersAction):
            for name, sub in action.choices.items():
                out[name] = _options(sub)
    out[""] = {o for a in top._actions for o in a.option_strings if o.startswith("--")}
    return out


COMMANDS = _commands()
GLOBAL = COMMANDS[""]
USE = re.compile(r"\bscat ([a-z][a-z-]*)((?: [^`\n]*)?)")
PAGES = sorted(p for pat in ("docs/*.md", "docs/reference/*.md") for p in ROOT.glob(pat))
# Words that follow "scat" in prose, not a command.
PROSE = {
    "kg",
    "chat",
    "is",
    "and",
    "the",
    "tool",
    "does",
    "checks",
    "to",
    "on",
    "in",
    "or",
    "can",
    "will",
    "has",
    "a",
}


def _uses(text: str):
    for ln in text.splitlines():
        for m in USE.finditer(ln):
            if (
                "`" in ln
                or ln.startswith((" ", "\t", "$"))
                or ln.lstrip().startswith(("scat ", "uv run scat"))
            ):
                yield m.group(1), m.group(2)


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_quoted_commands_and_options_exist(page):
    bad = []
    for name, rest in _uses(page.read_text(encoding="utf-8")):
        if name in PROSE:
            continue
        if name not in COMMANDS:
            bad.append(f"no command `scat {name}`")
            continue
        for opt in re.findall(r"(?<![\w-])(--[a-z][a-z-]*)", rest):
            if opt not in COMMANDS[name] | GLOBAL:
                bad.append(f"`scat {name}` has no {opt}")
    assert not bad, f"{page.name}: {sorted(set(bad))}"


def test_the_scan_sees_commands():
    seen = {n for p in PAGES for n, _ in _uses(p.read_text(encoding="utf-8")) if n in COMMANDS}
    assert {"check", "stub", "evidence"} <= seen
