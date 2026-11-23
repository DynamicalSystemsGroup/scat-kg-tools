"""Demonstrate R-13: edit a SCRATCH COPY of the TBox and run the equality test against it.

    uv run --directory research/toolchain/spike python -m r13.demo
Prints the test on the unchanged TBox (passes), then on a scratch copy that adds a required
link `scat:raw` to CodedScenario (fails, naming the difference). The real TBox is never written.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

from .equality import DEFAULT_TBOX

OLD = "scat:CodedScenario   scat:requiresLink scat:groups,"
NEW = "scat:CodedScenario   scat:requiresLink scat:raw, scat:groups,"


def run(label, env_tbox=None):
    env = dict(os.environ)
    env.pop("SCAT_TBOX", None)
    if env_tbox:
        env["SCAT_TBOX"] = str(env_tbox)
    print(f"--- {label}")
    r = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "r13/test_equality.py::test_models_equal_tbox",
            "-q",
            "--no-header",
            "-p",
            "no:cacheprovider",
        ],
        check=False,
        env=env,
        capture_output=True,
        text=True,
    )
    print(r.stdout.strip() or r.stderr.strip())
    print(f"exit code {r.returncode}\n")


def main():
    run("unchanged placeholder TBox")
    text = DEFAULT_TBOX.read_text(encoding="utf-8")
    assert text.count(OLD) == 1, "demo edit target drifted"
    with tempfile.TemporaryDirectory() as tmp:
        scratch = Path(tmp) / "tbox-scratch.ttl"
        scratch.write_text(text.replace(OLD, NEW), encoding="utf-8", newline="\n")
        run("scratch copy: CodedScenario requiresLink += scat:raw", scratch)


if __name__ == "__main__":
    main()
