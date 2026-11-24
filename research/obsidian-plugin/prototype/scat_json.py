#!/usr/bin/env python3
"""scat_json.py: print the result of `scat_kg.check` for one note as JSON (see JSON-CONTRACT.md).

Usage:  python scat_json.py NOTE.md [--neighborhood]

NOTE is a path to a note (absolute, or relative to the current folder). The SCAT vault is the nearest folder
above the note that holds a `scat.toml`. Only the public API of `scat_kg` is used (`scat_kg.check`).

Stdout holds one JSON object and nothing else. The exit code is 0 whenever the JSON was printed,
including when the note has errors. `status` says what happened:

  ok            the note was checked; `problems` holds the messages (possibly none)
  not-a-vault   no `scat.toml` in the note's folder or above it
  not-a-page    the note has no `type:` in its frontmatter, so nothing is checked
  refused       scat_kg declined the request; `message` holds its words
  no-scat-kg    this Python cannot import scat_kg
  error         anything else; `message` holds the exception
"""

import json
import os
import re
import sys

SCHEMA_VERSION = 1


def emit(status, message="", **extra):
    out = {"schema_version": SCHEMA_VERSION, "status": status, "message": message, "ok": True, "problems": []}
    out.update(extra)
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")


def find_root(note):
    """The nearest folder at or above the note's folder that holds scat.toml, or None."""
    folder = os.path.dirname(note)
    while True:
        if os.path.isfile(os.path.join(folder, "scat.toml")):
            return folder
        parent = os.path.dirname(folder)
        if parent == folder:
            return None
        folder = parent


def has_type(text):
    """True when the note opens with a frontmatter block that has a `type:` key."""
    lines = text.lstrip("﻿").splitlines()
    if not lines or lines[0].strip() != "---":
        return False
    for line in lines[1:]:
        if line.strip() in ("---", "..."):
            return False
        if re.match(r"type\s*:", line):
            return True
    return False


def problem_json(p):
    return {
        "rule": p.rule,
        "severity": p.severity,
        "file": p.file,
        "where": p.where,
        "what": p.what,
        "fix": p.fix,
        "line": p.line,
        "column": p.column,
        "repeat": p.repeat,
    }


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    neighborhood = "--neighborhood" in argv
    if len(args) != 1:
        emit("error", "usage: scat_json.py NOTE.md [--neighborhood]")
        return 0
    note = os.path.abspath(args[0])
    root = find_root(note)
    if root is None:
        emit("not-a-vault", "No scat.toml in this note's folder or any folder above it.")
        return 0
    try:
        with open(note, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        emit("error", f"cannot read the note: {e}", root=root)
        return 0
    if not has_type(text):
        emit("not-a-page", "This note has no `type:` in its frontmatter, so it is not a SCAT page. Nothing is checked.", root=root)
        return 0
    try:
        import scat_kg
    except ImportError as e:
        emit("no-scat-kg", f"This Python cannot import scat_kg ({e}). Run the plugin through `uv run` in a vault that pins scat-kg.", root=root)
        return 0
    rel = os.path.relpath(note, root).replace(os.sep, "/")
    result = scat_kg.check(rel, neighborhood=neighborhood, root=root)
    if not hasattr(result, "problems"):  # a refusal: scat_kg returns it, it does not raise
        emit("refused", str(result), root=root)
        return 0
    emit(
        "ok",
        root=root,
        page=rel,
        ok=bool(result.ok),
        problems=[problem_json(p) for p in result.problems],
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as e:  # the plugin reads stdout; never leave it empty
        emit("error", f"{type(e).__name__}: {e}")
        sys.exit(0)
