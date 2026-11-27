"""WP28-R4: the container image imports matplotlib and serves the drawing tools. Runs the real image, exactly as the
launcher runs it (read-only, tmpfs /tmp, a non-root --user, the vault at /vault). Skipped unless docker answers AND
SCAT_IMAGE_TEST=1 asks for it; SCAT_IMAGE names the image (default scat-kg-tools:ci);
SCAT_IMAGE_TMP names where the vault copy goes when the docker VM does not share the system temp dir (Colima shares $HOME). Standard library only."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

IMAGE = os.environ.get("SCAT_IMAGE", "scat-kg-tools:ci")
EXAMPLES = Path(__file__).parents[2] / "contracts" / "examples"

# Runs inside the image with the installed package: imports matplotlib, builds the server the entrypoint serves,
# lists its tools and calls the view tools asking for the plot, which must return PNG bytes.
PROBE = r"""
import asyncio, base64
import matplotlib
from scat_kg.mcp_server.server import build

async def main():
    import os
    assert os.listdir("/vault"), "the vault is empty: the docker VM cannot see the folder (set SCAT_IMAGE_TMP to one it shares, e.g. under $HOME)"
    server = build("/vault")
    names = {t.name for t in await server.list_tools()}
    assert {"fingerprint", "layered", "trace"} <= names, names
    assert not {"draw_fingerprint", "draw_layered", "draw_trace"} & names, names
    for tool, args in (
        ("layered", {"output": "plot"}),
        ("trace", {"node": "self-checkout", "output": "plot"}),
    ):
        content = await server.call_tool(tool, args)
        content = getattr(content, "content", content)  # a CallToolResult, or the content list
        content = content[0] if isinstance(content, tuple) else content
        assert len(content) == 1 and content[0].type == "image", content
        data = base64.b64decode(content[0].data)
        assert data.startswith(b"\x89PNG\r\n\x1a\n"), data[:16]
        print(tool, "png", len(data))

asyncio.run(main())
print("matplotlib", matplotlib.__version__)
"""


def docker_answers() -> bool:
    if not shutil.which("docker"):
        return False
    try:
        return (
            subprocess.run(
                ["docker", "info"], check=False, capture_output=True, timeout=30
            ).returncode
            == 0
        )
    except (OSError, subprocess.TimeoutExpired):
        return False


pytestmark = pytest.mark.skipif(
    os.environ.get("SCAT_IMAGE_TEST") != "1" or not docker_answers(),
    reason="set SCAT_IMAGE_TEST=1 (and SCAT_IMAGE) with a running docker to test the built image",
)


def test_the_image_imports_matplotlib_and_serves_the_drawing_tools():
    with tempfile.TemporaryDirectory(dir=os.environ.get("SCAT_IMAGE_TMP")) as tmp:
        vault = Path(tmp) / "vault"
        shutil.copytree(EXAMPLES, vault)
        vault.chmod(0o777)  # the container runs as the host's uid:gid; the server may write views/
        user = f"{os.getuid()}:{os.getgid()}" if hasattr(os, "getuid") else "1000:1000"
        run = subprocess.run(
            ["docker", "run", "--rm", "--read-only", "--tmpfs", "/tmp", "--user", user]
            + ["--security-opt", "no-new-privileges", "--cap-drop", "ALL", "-v", f"{vault}:/vault"]
            + ["--entrypoint", "python", IMAGE, "-c", PROBE],
            check=False,
            capture_output=True,
            text=True,
            timeout=300,
        )
    sys.stdout.write(run.stdout)
    assert run.returncode == 0, run.stderr[-2000:]
    assert "layered png" in run.stdout and "trace png" in run.stdout
