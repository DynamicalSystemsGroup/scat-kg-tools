import subprocess

import pytest

TEMPLATE_URL = "https://github.com/DynamicalSystemsGroup/scat-kg-template"
TEMPLATE_COMMIT = "f446a023cacb9a628bab0354c6a7d9b69ff9f701"  # the template's `dev`; WP8 re-pins it


@pytest.fixture(scope="session")
def template(tmp_path_factory):
    """The template at the pinned commit. A clone failure is an error, not a skip."""
    dest = tmp_path_factory.mktemp("template") / "vault"
    subprocess.run(["git", "clone", "--quiet", TEMPLATE_URL, str(dest)], check=True)
    subprocess.run(["git", "-C", str(dest), "checkout", "--quiet", TEMPLATE_COMMIT], check=True)
    return dest
