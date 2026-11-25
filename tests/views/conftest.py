import pytest
from viewutil import base_files, write


@pytest.fixture
def vault(tmp_path):
    return write(tmp_path / "vault", base_files())


@pytest.fixture
def make(tmp_path):
    """A fresh vault: the base files, with `over` replacing or adding pages (None removes one)."""

    def build(over: dict[str, str | None] | None = None):
        files = base_files() | (over or {})
        return write(tmp_path / "made", {k: v for k, v in files.items() if v is not None})

    return build
