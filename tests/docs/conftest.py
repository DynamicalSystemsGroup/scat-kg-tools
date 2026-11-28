import subprocess

import pytest

TEMPLATE_URL = "https://github.com/DynamicalSystemsGroup/scat-template"
TEMPLATE_COMMIT = "9defb3f1fed10da1a16229f3bd84020341d92b9c"  # pins tools abc349f


@pytest.fixture(scope="session")
def template(tmp_path_factory):
    """The template at the pinned commit. A clone failure is an error, not a skip."""
    dest = tmp_path_factory.mktemp("template") / "vault"
    subprocess.run(["git", "clone", "--quiet", TEMPLATE_URL, str(dest)], check=True)
    subprocess.run(["git", "-C", str(dest), "checkout", "--quiet", TEMPLATE_COMMIT], check=True)
    return dest
