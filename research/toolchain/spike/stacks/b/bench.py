"""Time stack B at the three scopes on the generated 500-page vault (R-5: 1 s / 2 s / 5 s).

uv run --directory research/toolchain/spike python -m stacks.b.bench [--repeats N] [--vault DIR]
Generates out/vault500 first if it is missing. Each repeat uses a fresh Vault (no carried cache);
the OS file cache is warm after the first read. Import/setup cost is not in the timings.
"""

import argparse
import platform
import statistics
import subprocess
import sys
import time
from importlib.metadata import version
from pathlib import Path

from .check import Vault, check_neighborhood, check_page, check_vault, use_shapes

LIMITS = {"page": 1.0, "neighborhood": 2.0, "full": 5.0}


def machine():
    cpu = platform.processor() or platform.machine()
    if sys.platform == "darwin":
        r = subprocess.run(
            ["sysctl", "-n", "machdep.cpu.brand_string"],
            capture_output=True,
            text=True,
            check=False,
        )
        cpu = r.stdout.strip() or cpu
    elif Path("/proc/cpuinfo").exists():
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.startswith("model name"):
                cpu = line.split(":", 1)[1].strip()
                break
    libs = ", ".join(f"{p} {version(p)}" for p in ("rdflib", "pyshacl", "python-frontmatter"))
    return [
        f"os: {platform.platform()}",
        f"cpu: {cpu} ({platform.machine()}), logical cores: {__import__('os').cpu_count()}",
        f"python: {platform.python_implementation()} {platform.python_version()}",
        f"libs: {libs}",
    ]


def time_it(fn, repeats):
    runs = []
    for _ in range(repeats):
        t = time.perf_counter()
        fn()
        runs.append(time.perf_counter() - t)
    return runs


def pick_pages(vault):
    """Median-degree page and the worst-case (largest neighborhood) page."""
    sizes = {s: len(vault.neighbors(s)) for s in vault.stems()}
    ordered = sorted(sizes, key=lambda s: (sizes[s], s))
    return ordered[len(ordered) // 2], ordered[-1], sizes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeats", type=int, default=7)
    ap.add_argument("--vault", type=Path, default=Path("out/vault500"))
    ap.add_argument("--shapes", choices=["core", "sparql"], default="core")
    a = ap.parse_args()
    use_shapes(a.shapes)
    if not a.vault.exists():
        subprocess.run([sys.executable, "-m", "gen", "--out", str(a.vault)], check=True)
    print("== machine")
    print("\n".join(machine()))
    n = len(list(a.vault.glob("*.md")))
    mid, worst, sizes = pick_pages(Vault(a.vault))
    print(
        f"== stack B (rdflib + pyshacl, {a.shapes} shapes) on {a.vault}: {n} pages, {a.repeats} repeats"
    )
    print(
        f"median-size neighborhood page: {mid} ({sizes[mid]} pages); worst case: {worst} ({sizes[worst]})"
    )
    print(f"{'scope':<28}{'min s':>8}{'median s':>10}{'max s':>8}  {'R-5 limit':>9}  verdict")
    cases = [
        (f"page ({mid})", "page", lambda: check_page(Vault(a.vault), mid)),
        (f"page ({worst})", "page", lambda: check_page(Vault(a.vault), worst)),
        (f"neighborhood ({mid})", "neighborhood", lambda: check_neighborhood(Vault(a.vault), mid)),
        (
            f"neighborhood ({worst})",
            "neighborhood",
            lambda: check_neighborhood(Vault(a.vault), worst),
        ),
        ("full vault", "full", lambda: check_vault(Vault(a.vault))),
    ]
    for name, scope, fn in cases:
        fn()  # untimed warm-up (imports, OS cache)
        r = time_it(fn, a.repeats)
        med = statistics.median(r)
        ok = "within" if med < LIMITS[scope] else "OVER"
        print(f"{name:<28}{min(r):>8.3f}{med:>10.3f}{max(r):>8.3f}  {LIMITS[scope]:>7.0f} s  {ok}")
    diags = check_vault(Vault(a.vault))
    print(f"(full-vault check reports {len(diags)} message(s) on the generated vault)")


if __name__ == "__main__":
    main()
