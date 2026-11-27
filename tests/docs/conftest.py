import subprocess

import pytest

TEMPLATE_URL = "https://github.com/DynamicalSystemsGroup/scat-kg-template"
TEMPLATE_COMMIT = "6ccfd9dd4d7020da7d0d3825b8c57154c8d97792"  # pins tools 5e4ab16


@pytest.fixture(scope="session")
def template(tmp_path_factory):
    """The template at the pinned commit. A clone failure is an error, not a skip."""
    dest = tmp_path_factory.mktemp("template") / "vault"
    subprocess.run(["git", "clone", "--quiet", TEMPLATE_URL, str(dest)], check=True)
    subprocess.run(["git", "-C", str(dest), "checkout", "--quiet", TEMPLATE_COMMIT], check=True)
    return dest
