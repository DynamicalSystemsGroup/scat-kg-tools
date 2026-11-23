"""Print stack A's messages for the clean mini-vault and the four seeded defects.

uv run --directory research/toolchain/spike python -m stacks.a.messages
"""

import subprocess
import sys

from .core import SPIKE, check, messages

DEFECTS = ("missing-field", "wrong-endpoint", "dangling-link", "missing-link-type")


def report(label, vault):
    st, found = check(vault)
    msgs = messages(st, found, vault)
    print(f"== {label}: {len(msgs)} message(s)")
    for m in msgs:
        print(m)


def main():
    report("clean mini-vault (vault/)", SPIKE / "vault")
    for d in DEFECTS:
        out = SPIKE / "out" / f"a-defect-{d}"
        subprocess.run(
            [sys.executable, "-m", "defects", d, "--out", str(out)],
            cwd=SPIKE,
            check=True,
            capture_output=True,
        )
        report(d, out)


if __name__ == "__main__":
    main()
