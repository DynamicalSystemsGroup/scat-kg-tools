"""Check a vault. uv run --directory research/toolchain/spike python -m stacks.a.check VAULT [--page STEM] [--neighborhood STEM]"""

import argparse
import sys

from .core import check, messages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vault")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--page")
    g.add_argument("--neighborhood")
    a = ap.parse_args()
    scope, page = (
        ("page", a.page)
        if a.page
        else ("neighborhood", a.neighborhood)
        if a.neighborhood
        else ("full", None)
    )
    st, found = check(a.vault, scope, page)
    msgs = messages(st, found, a.vault)
    print("\n".join(msgs) if msgs else f"ok: no errors ({scope})")
    sys.exit(1 if msgs else 0)


if __name__ == "__main__":
    main()
