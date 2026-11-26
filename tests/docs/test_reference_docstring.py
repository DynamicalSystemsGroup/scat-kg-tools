"""The package docstring shown in the CLI reference is the docstring, line for line."""

from pathlib import Path

from docs_runner import fenced_blocks

import scat_kg

CLI = Path(__file__).resolve().parents[2] / "docs" / "reference" / "cli.md"


def test_the_cli_reference_shows_the_package_docstring_as_written():
    blocks = fenced_blocks(CLI.read_text("utf-8"))
    shown = next(
        b.text for b in blocks if b.tag == "text" and b.text.startswith("scat_kg: check and work")
    )
    assert shown.rstrip("\n") == (scat_kg.__doc__ or "").strip("\n")
