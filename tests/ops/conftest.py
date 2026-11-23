import shutil

import pytest
from opsutil import EXAMPLES, changes, snapshot


@pytest.fixture
def snap():
    return snapshot


@pytest.fixture
def diff():
    return changes


@pytest.fixture
def example_vault(tmp_path):
    root = tmp_path / "vault"
    shutil.copytree(EXAMPLES, root)
    return root
