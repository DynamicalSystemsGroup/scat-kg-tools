import subprocess

import pytest

TEMPLATE_URL = "https://github.com/DynamicalSystemsGroup/scat-kg-template"
TEMPLATE_COMMIT = "a8f7287e1a4b1ac43ffd1abc1d19976318dbca34"  # pins tools 6df6bdd


@pytest.fixture(scope="session")
def template(tmp_path_factory):
    """The template at the pinned commit. A clone failure is an error, not a skip."""
    dest = tmp_path_factory.mktemp("template") / "vault"
    subprocess.run(["git", "clone", "--quiet", TEMPLATE_URL, str(dest)], check=True)
    subprocess.run(["git", "-C", str(dest), "checkout", "--quiet", TEMPLATE_COMMIT], check=True)
    return dest
