"""Print stack C's actual messages for the four seeded defects, plus the clean mini-vault.

    uv run --directory research/toolchain/spike python -m stacks.c.messages
Defects are injected into scratch copies (system temp dir), never into vault/.
"""

import sys
import tempfile
from pathlib import Path

from defects.__main__ import DEFECTS, inject

from .checks import Vault, check_vault

SRC = Path("vault")


def main():
    clean = check_vault(Vault(SRC))
    print(f"== clean mini-vault ({len(Vault(SRC).stems)} pages): {len(clean)} violations")
    for x in clean:
        print(x)
    bad = bool(clean)
    with tempfile.TemporaryDirectory() as tmp:
        for name in sorted(DEFECTS):
            out = Path(tmp) / name
            inject(name, SRC, out)
            res = check_vault(Vault(out))
            print(f"\n== defect {name}: {len(res)} violation(s)")
            for x in res:
                print(x)
            bad = bad or len(res) != 1
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
