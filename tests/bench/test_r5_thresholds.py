"""WP5-R5 (R-5): the thresholds on a generated 500-page vault, on a laptop.

One page under 1 s, a neighborhood under 2 s, the whole vault under 5 s. The vault is generated into a
temp directory here, with no fixture committed. Each timing is the whole public call (`scat_tools.check`),
reading the vault included, as the `scat` command does it. It takes a few seconds, so it runs in the
default `uv run pytest`; `uv run pytest tests/bench -s` shows the timings.
"""

import time
from collections import Counter

import scat_tools
from scat_tools.vault import read_vault

LIMITS = {"page": 1.0, "neighborhood": 2.0, "vault": 5.0}  # seconds, R-5


def _page(type_, title, extra="", body=""):
    return f'---\ntype: {type_}\nstatus: done\ntitle: "{title}"\ndescription: "{title}."\n{extra}---\n{body}'


def _narrative(title, rows, timeframe="past", body=""):
    table = "\n## Edges told\n\n| from | type | to | note |\n|---|---|---|---|\n" + "".join(
        f"| [[{a}]] | {t} | [[{b}]] | note |\n" for t, a, b in rows
    )
    return _page("narrative", title, f"timeframe: {timeframe}\n", body + table)


def generate(root):
    """500 pages: 20 groups, 149 concerns, 100 affordances, 60 technologies and 171 narratives, each with a table of
    edges. Concern c000 is a hub, linked from many narratives. Then `index` writes the Base files."""
    (root / "scat.toml").write_text(
        "attribution = 'disallowed'\nstakeholder_group_cap = 25\n", encoding="utf-8"
    )
    g = [f"group-{i:03d}" for i in range(20)]
    c = [f"concern-{i:03d}" for i in range(149)]
    a = [f"affordance-{i:03d}" for i in range(100)]
    t = [f"technology-{i:03d}" for i in range(60)]
    pages = {}
    for names, type_ in ((g, "group"), (c, "concern"), (a, "affordance"), (t, "technology")):
        for n in names:
            body = (
                f"Pulls against [[{c[(c.index(n) + 1) % len(c)]}]].\n" if type_ == "concern" else ""
            )
            pages[f"{type_}/{n}.md"] = _page(type_, n, "", body)
    hub = c[0]
    for i in range(171):
        rows = [
            ("holds", g[i % 20], hub if i % 3 == 0 else c[i % 149]),
            ("is addressed by", hub if i % 2 == 0 else c[(i + 1) % 149], a[i % 100]),
            ("is provided by", a[i % 100], t[i % 60]),
        ]
        links = " ".join(f"[[{n}]]" for n in rows[0][1:])  # the ends of its first row
        n = f"narrative-{i:03d}"
        pages[f"narrative/{n}.md"] = _narrative(n, rows, body=f"The account names {links}.\n")
    for rel, text in pages.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    assert scat_tools.index(root=root).ok  # writes the five Base files


def timed(fn):
    start = time.perf_counter()
    result = fn()
    return time.perf_counter() - start, result


def test__r5__page_neighborhood_and_vault_meet_the_thresholds_on_500_pages(tmp_path, capsys):
    generate(tmp_path)
    vault = read_vault(tmp_path)
    assert len(vault.pages) == 500, Counter(p.type for p in vault.pages)
    hub = "concern-000"
    best = {}
    for scope, call in {
        "page": lambda: scat_tools.check(hub, root=tmp_path),
        "neighborhood": lambda: scat_tools.check(hub, neighborhood=True, root=tmp_path),
        "vault": lambda: scat_tools.check(root=tmp_path),
    }.items():
        runs = [timed(call) for _ in range(3)]
        best[scope] = min(r[0] for r in runs)
        result = runs[0][1]
        assert not result.errors, str(result)  # a generated vault that checks clean of errors
    size = len(scat_tools.check(hub, neighborhood=True, root=tmp_path).report.problems)
    with capsys.disabled():
        print("\nR-5 on a generated vault of", len(vault.pages), "pages (best of 3, whole call)")
        for scope, limit in LIMITS.items():
            print(f"  {scope:13} {best[scope] * 1000:8.1f} ms   limit {limit * 1000:.0f} ms")
        print("  problems in the neighborhood of", hub, ":", size)
    for scope, limit in LIMITS.items():
        assert best[scope] < limit, f"{scope}: {best[scope]:.2f} s, limit {limit} s"
