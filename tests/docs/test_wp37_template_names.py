"""WP37-R1 for the template: nothing in the vault to clone names the package or the repositories by an old name."""

import re

OLD = re.compile(r"scat[ _-]?chat|scat[_-]kg", re.IGNORECASE)


def test_the_template_uses_no_old_name(template):
    found = []
    for p in sorted(template.rglob("*")):
        rel = p.relative_to(template)
        if ".git" in rel.parts or not p.is_file():
            continue
        if OLD.search(str(rel)):
            found.append(f"its name: {rel}")
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        found += [
            f"{rel}:{n}: {ln.strip()[:100]}"
            for n, ln in enumerate(text.splitlines(), 1)
            if OLD.search(ln)
        ]
    assert not found, "\n".join(found[:40])
