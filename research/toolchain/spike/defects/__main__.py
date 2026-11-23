"""Inject one seeded defect into a COPY of a vault (the source is never modified).

    uv run --directory research/toolchain/spike python -m defects missing-field --out out/d1
    uv run --directory research/toolchain/spike python -m defects --list

Defects are exact text edits of one page of vault/ (the mini-vault); each asserts its
target text occurs exactly once, so a drifted vault fails loudly instead of silently.
"""

import argparse
import shutil
import sys
from pathlib import Path

# name -> (page, old text, new text, what a checker must report)
DEFECTS = {
    "missing-field": (
        "access-cost.md",
        'description: "Borrowing should stay affordable."\n',
        "",
        (
            "access-cost.md: required field `description` missing on a `done` concern; "
            'fix: add `description: "<one sentence>"`'
        ),
    ),
    "wrong-endpoint": (
        "access-cost.md",
        'addresses:\n  - "[[reserve-online]]"',
        'addresses:\n  - "[[booking-app]]"',
        (
            "access-cost.md field `addresses`: [[booking-app]] is a technology, "
            "an affordance is required; fix: link an affordance, e.g. [[reserve-online]]"
        ),
    ),
    "dangling-link": (
        "tool-safety.md",
        '"[[safety-briefing]]"',
        '"[[safety-briefings]]"',
        (
            "tool-safety.md field `addresses`: page [[safety-briefings]] does not exist; "
            "fix: write [[safety-briefing]] (or create the page)"
        ),
    ),
    "missing-link-type": (
        "scenario-1-coded.md",
        'affordances:\n  - "[[reserve-online]]"\n  - "[[safety-briefing]]"\n',
        "",
        (
            "scenario-1-coded.md: coded scenario has no `affordances` link; "
            'fix: add `affordances:` with at least one affordance, e.g. `- "[[reserve-online]]"`'
        ),
    ),
}


def inject(name, src, out):
    page, old, new, _ = DEFECTS[name]
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(src, out)
    path = out / page
    text = path.read_text()
    if text.count(old) != 1:
        sys.exit(f"{page}: expected target text exactly once, found {text.count(old)}")
    path.write_text(text.replace(old, new), newline="\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("name", nargs="?", choices=sorted(DEFECTS))
    ap.add_argument("--src", type=Path, default=Path("vault"), help="clean vault (default: vault)")
    ap.add_argument("--out", type=Path, help="directory for the defective copy (replaced)")
    ap.add_argument("--list", action="store_true", help="print defects and expected diagnoses")
    a = ap.parse_args()
    if a.list or not a.name:
        for n, (_, _, _, expect) in sorted(DEFECTS.items()):
            print(f"{n}: {expect}")
        return
    if not a.out:
        ap.error("--out is required")
    inject(a.name, a.src, a.out)
    print(f"injected {a.name} into {a.out}")


if __name__ == "__main__":
    main()
