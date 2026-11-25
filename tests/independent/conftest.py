"""Fixtures of the independent suite (WP16-U8). Own conftest: nothing from tests/checks is used."""

import itertools
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from indep_kit import build_base


@pytest.fixture
def base(tmp_path):
    """The clean vault, narrative at `done`."""
    return build_base(tmp_path / "v")


@pytest.fixture
def make_base(tmp_path):
    counter = itertools.count()

    def make(status="done", cap=3):
        return build_base(tmp_path / f"v{next(counter)}", status, cap)

    return make


@pytest.fixture
def tmp_factory(tmp_path):
    counter = itertools.count()
    return lambda: tmp_path / f"copy{next(counter)}"
