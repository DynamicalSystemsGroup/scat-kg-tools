"""Ground-truth wikilink resolution check (not a stack): every [[x]] must be a page stem.

    uv run --directory research/toolchain/spike python -m gen.lint_links vault
Exit 1 and list file:link on any dangling link.
"""

import re
import sys
from pathlib import Path

WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")


def dangling(vault):
    stems = {p.stem for p in vault.glob("*.md")}
    bad = []
    for p in sorted(vault.glob("*.md")):
        for m in WIKILINK.finditer(p.read_text()):
            if m.group(1).strip() not in stems:
                bad.append((p.name, m.group(1)))
    return bad


def main():
    vault = Path(sys.argv[1])
    bad = dangling(vault)
    n = len(list(vault.glob("*.md")))
    for f, t in bad:
        print(f"{f}: dangling link [[{t}]]")
    print(f"{n} pages, {len(bad)} dangling links")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
