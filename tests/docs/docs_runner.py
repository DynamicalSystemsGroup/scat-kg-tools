"""R-9: run the docs the way the reader does, and diff the CLI reference against `--help`.

Convention (see the docs pages): ```python blocks of a page run in order in one session; ```bash
blocks are `uv run scat ...` lines, mapped to the tools under test; ```text blocks are never run;
any other tag is ignored.
"""

import contextlib
import io
import os
import re
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass

HELP_COLUMNS = "80"  # `--help` wraps to the terminal width; the reference is checked at this width

_FENCE = re.compile(r"^(?P<indent>[ \t]*)(?P<mark>`{3,}|~{3,})[ \t]*(?P<tag>[^\s`]*)")
_SCAT = ("uv run scat ", "scat ")


@dataclass(frozen=True)
class Block:
    tag: str
    text: str
    line: int  # 1-based line of the opening fence


def fenced_blocks(markdown: str) -> list[Block]:
    """Every fenced block, in order; indentation of the opening fence (content tabs) is removed."""
    blocks, lines, i = [], markdown.splitlines(), 0
    while i < len(lines):
        m = _FENCE.match(lines[i])
        if not m:
            i += 1
            continue
        indent, mark, start, body = m["indent"], m["mark"], i, []
        i += 1
        while i < len(lines) and not (lines[i].strip() and not lines[i].strip().strip(mark[0])):
            body.append(
                lines[i][len(indent) :] if lines[i].startswith(indent) else lines[i].lstrip()
            )
            i += 1
        i += 1  # the closing fence
        blocks.append(Block(m["tag"], "\n".join(body) + "\n", start + 1))
    return blocks


def scat_argv(line: str) -> list[str]:
    """`uv run scat check` -> the tools under test."""
    for prefix in _SCAT:
        if line.startswith(prefix):
            return [sys.executable, "-m", "scat_tools.cli", *shlex.split(line[len(prefix) :])]
    raise AssertionError(
        f"not a `uv run scat ...` command: {line!r} (put non-runnable text in ```text)"
    )


def run_page(page: str, markdown: str, cwd) -> None:
    """Run the page's python and bash blocks in order; raise AssertionError naming page and block."""
    namespace: dict = {"__name__": "__docs__"}
    here = os.getcwd()
    os.chdir(cwd)
    try:
        for n, block in enumerate(fenced_blocks(markdown), 1):
            where = f"{page} block {n} (line {block.line}, {block.tag}):\n{block.text}"
            if block.tag == "python":
                try:
                    exec(compile(block.text, f"{page}#{n}", "exec"), namespace)  # noqa: S102
                except Exception as e:
                    raise AssertionError(f"{where}\n{type(e).__name__}: {e}") from e
            elif block.tag == "bash":
                for line in filter(None, (ln.strip() for ln in block.text.splitlines())):
                    try:
                        argv = scat_argv(line)
                    except (AssertionError, ValueError) as e:
                        raise AssertionError(f"{where}\n$ {line}\n{e}") from e
                    done = subprocess.run(
                        argv, check=False, cwd=cwd, capture_output=True, text=True
                    )
                    if done.returncode != 0:
                        raise AssertionError(
                            f"{where}\n$ {line}\nexit {done.returncode}\n{done.stdout}{done.stderr}"
                        )
    finally:
        os.chdir(here)


def copy_template(template, dest):
    """A fresh working tree (no .git) to run a page in."""
    shutil.copytree(template, dest, ignore=shutil.ignore_patterns(".git"))


def has_runnable(markdown: str) -> bool:
    return any(b.tag in ("python", "bash") for b in fenced_blocks(markdown))


def live_help(parser) -> dict[str, str]:
    """{"scat": text, "scat <command>": text, ...}, the subcommands read from the live parser."""
    import argparse

    subs = next(a for a in parser._actions if isinstance(a, argparse._SubParsersAction))
    out = {}
    env = {"COLUMNS": HELP_COLUMNS, "NO_COLOR": "1"}
    saved = {k: os.environ.get(k) for k in env}
    os.environ.update(env)
    try:
        for name, argv in [("scat", [])] + [(f"scat {c}", [c]) for c in subs.choices]:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), contextlib.suppress(SystemExit):
                parser.parse_args([*argv, "--help"])
            out[name] = buf.getvalue()
    finally:
        for k, v in saved.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
    return out


def reference_problems(markdown: str, live: dict[str, str]) -> list[str]:
    """Differences between the reference page's `## scat ...` sections and the live help."""
    sections: dict[str, str | None] = {}
    for part in re.split(r"(?m)^## ", markdown)[1:]:
        head, _, rest = part.partition("\n")
        if re.fullmatch(r"scat( \S+)?", head.strip()):
            sections[head.strip()] = next(
                (b.text for b in fenced_blocks(rest) if b.tag == "text"), None
            )
    problems = []
    for name, want in live.items():
        if name not in sections:
            problems.append(f"missing section: ## {name}")
        elif sections[name] is None:
            problems.append(f"## {name}: no ```text block")
        elif sections[name].rstrip("\n") != want.rstrip("\n"):
            problems.append(f"## {name}: text differs from `{name} --help`")
    problems += [f"extra section: ## {n}" for n in sections if n not in live]
    return problems
