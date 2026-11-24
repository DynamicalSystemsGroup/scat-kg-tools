"""WP5-R5 (R-5): the thresholds on a generated 500-page vault, on a laptop.

One page under 1 s, a neighborhood under 2 s, the whole vault under 5 s. The vault is generated into a
temp directory here, with no fixture committed. Each timing is the whole public call (`scat_kg.check`),
reading the vault included, as the `scat` command does it. It takes a few seconds, so it runs in the
default `uv run pytest`; `uv run pytest tests/bench -s` shows the timings.
"""

import time
from collections import Counter

import scat_kg
from scat_kg.vault import read_vault

LIMITS = {"page": 1.0, "neighborhood": 2.0, "vault": 5.0}  # seconds, R-5


def _page(type_, title, extra="", body=""):
    return f'---\ntype: {type_}\nstatus: done\ntitle: "{title}"\ndescription: "{title}."\n{extra}---\n{body}'


def _link(key, *names):
    return f"{key}:\n" + "".join(f'  - "[[{n}]]"\n' for n in names)


def generate(root):
    """500 pages: 20 groups, 149 concerns, 100 affordances, 60 technologies, 160 relation pages,
    4 records, and the 7 class pages `index` writes. Concern c000 is a hub, linked from many pages."""
    (root / "scat.toml").write_text("stakeholder_group_cap = 25\n", encoding="utf-8")
    g = [f"group-{i:03d}" for i in range(20)]
    c = [f"concern-{i:03d}" for i in range(149)]
    a = [f"affordance-{i:03d}" for i in range(100)]
    t = [f"technology-{i:03d}" for i in range(60)]
    pages = {}
    for names, type_ in (
        (g, "stakeholder-group"),
        (c, "concern"),
        (a, "affordance"),
        (t, "technology"),
    ):
        for n in names:
            extra = _link("conflicts", c[(c.index(n) + 1) % len(c)]) if type_ == "concern" else ""
            pages[f"{type_}/{n}.md"] = _page(type_, n, extra)
    hub = c[0]
    for i in range(60):
        n = f"heldby-{i:03d}"
        e = f'group: "[[{g[i % 20]}]]"\nconcern: "[[{hub if i < 30 else c[i]}]]"\n'
        pages[f"heldby/{n}.md"] = _page("heldby", n, e)
    for i in range(55):
        n = f"addresses-{i:03d}"
        e = f'concern: "[[{hub if i < 25 else c[i]}]]"\naffordance: "[[{a[i]}]]"\n'
        pages[f"addresses/{n}.md"] = _page("addresses", n, e)
    for i in range(45):
        n = f"attributes-{i:03d}"
        pages[f"attributes/{n}.md"] = _page(
            "attributes", n, f'affordance: "[[{a[i]}]]"\ntechnology: "[[{t[i]}]]"\n'
        )
    pages["scenario-raw/day.md"] = _page(
        "scenario-raw", "day", "timeframe: past\n" + _link("coded", "day-coded")
    )
    pages["scenario-coded/day-coded.md"] = _page(
        "scenario-coded",
        "day-coded",
        _link("raw", "day") + _link("groups", *g[:5]) + _link("concerns", hub, *c[1:5])
        + _link("affordances", *a[:5]),
    )  # fmt: skip
    pages["architecture-raw/pitch.md"] = _page(
        "architecture-raw", "pitch", "timeframe: future\n" + _link("coded", "pitch-coded")
    )
    pages["architecture-coded/pitch-coded.md"] = _page(
        "architecture-coded",
        "pitch-coded",
        _link("raw", "pitch") + _link("concerns", hub, *c[1:5]) + _link("affordances", *a[:5])
        + _link("technologies", *t[:5]),
    )  # fmt: skip
    for rel, text in pages.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    assert scat_kg.index(root=root).ok  # writes the seven class pages


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
        "page": lambda: scat_kg.check(hub, root=tmp_path),
        "neighborhood": lambda: scat_kg.check(hub, neighborhood=True, root=tmp_path),
        "vault": lambda: scat_kg.check(root=tmp_path),
    }.items():
        runs = [timed(call) for _ in range(3)]
        best[scope] = min(r[0] for r in runs)
        result = runs[0][1]
        assert not result.errors, str(result)  # a generated vault that checks clean of errors
    size = len(scat_kg.check(hub, neighborhood=True, root=tmp_path).report.problems)
    with capsys.disabled():
        print("\nR-5 on a generated vault of", len(vault.pages), "pages (best of 3, whole call)")
        for scope, limit in LIMITS.items():
            print(f"  {scope:13} {best[scope] * 1000:8.1f} ms   limit {limit * 1000:.0f} ms")
        print("  problems in the neighborhood of", hub, ":", size)
    for scope, limit in LIMITS.items():
        assert best[scope] < limit, f"{scope}: {best[scope]:.2f} s, limit {limit} s"
