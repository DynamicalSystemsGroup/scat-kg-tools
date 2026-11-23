"""Writing files safely: UTF-8, existing line endings kept, new files never overwrite, edits are atomic."""

import os
import re
import shutil
import tempfile
from pathlib import Path

_SPLIT = re.compile(r"(\r\n|\n)")


class NotUtf8(ValueError):
    pass


def read_lines(path: Path) -> tuple[list[tuple[str, str]], bool]:
    """The file as [(line text, its own line ending)], and whether it began with a BOM.

    Only `\\n` and `\\r\\n` end a line (as the reader says). A last line with no ending has "".
    """
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as e:
        raise NotUtf8(f"{path.name} is not valid UTF-8") from e
    bom = text.startswith("﻿")
    parts = _SPLIT.split(text.removeprefix("﻿"))
    lines = [
        (parts[i], parts[i + 1] if i + 1 < len(parts) else "") for i in range(0, len(parts), 2)
    ]
    if lines and lines[-1] == ("", ""):
        lines.pop()
    return lines, bom


def join_lines(lines: list[tuple[str, str]], bom: bool) -> bytes:
    return (("﻿" if bom else "") + "".join(t + e for t, e in lines)).encode("utf-8")


def line_ending(lines: list[tuple[str, str]]) -> str:
    """The file's line ending: that of its first line that has one, LF if none does."""
    return next((e for _, e in lines if e), "\n")


def replace_file(path: Path, data: bytes) -> None:
    """Replace an existing file whole and atomically, keeping its permissions."""
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        shutil.copymode(path, tmp)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def create_files(files: list[tuple[Path, str]]) -> None:
    """Create new files (UTF-8, LF), all or none: a file that exists is never touched.

    If any write fails, the files this call already made are removed and the error is raised.
    """
    made: list[Path] = []
    try:
        for path, text in files:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "xb") as f:  # exclusive: raises if the path appeared meanwhile
                made.append(path)
                f.write(text.encode("utf-8"))
    except BaseException:
        for p in made:
            p.unlink(missing_ok=True)
        raise
