import pytest


@pytest.fixture
def make_vault(tmp_path):
    """Write {relative path: text or bytes} under a fresh directory and return it."""

    def make(files: dict[str, str | bytes]):
        for rel, content in files.items():
            path = tmp_path / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))
        return tmp_path

    return make
