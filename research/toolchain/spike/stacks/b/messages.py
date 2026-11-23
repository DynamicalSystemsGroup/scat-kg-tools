"""Print stack B's messages for the four seeded defects (and confirm the clean mini-vault is clean).

uv run --directory research/toolchain/spike python -m stacks.b.messages
"""

from pathlib import Path

from defects.__main__ import DEFECTS, inject

from .check import Vault, check_neighborhood, check_page, check_vault, use_shapes


def main():
    import sys

    use_shapes(sys.argv[1] if len(sys.argv) > 1 else "core")
    clean = Path("vault")
    errs = check_vault(Vault(clean))
    print(f"clean mini-vault ({len(Vault(clean).stems())} pages): {len(errs)} errors")
    for d in errs:
        print("  " + d.message)
    for name, (page, _, _, expect) in DEFECTS.items():
        out = Path("out") / "stack-b" / name
        inject(name, clean, out)
        v = Vault(out)
        stem = page[:-3]
        full = check_vault(v)
        print(f"\n== {name}  (page {page})\nexpected by injector: {expect}")
        print(f"stack B, whole vault: {len(full)} message(s)")
        for d in full:
            print("  " + d.message)
        mine = sorted(d.message for d in full if d.file.split(":")[0] == page)
        agree = (
            sorted(d.message for d in check_page(v, stem)) == mine
            and sorted(
                d.message for d in check_neighborhood(v, stem) if d.file.split(":")[0] == page
            )
            == mine
        )
        print(f"page and neighborhood scopes give the same message(s) for {page}: {agree}")


if __name__ == "__main__":
    main()
