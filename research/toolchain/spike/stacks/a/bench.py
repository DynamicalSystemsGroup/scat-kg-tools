"""Time stack A's three scopes on the 500-page vault. Generates it first if absent.

uv run --directory research/toolchain/spike python -m stacks.a.bench
"""

import os
import platform
import statistics
import subprocess
import sys
import time
from pathlib import Path

import pyoxigraph

from .core import SPIKE, check

REPEATS = 7
VAULT = SPIKE / "out" / "vault500"


def machine():
    cpu = platform.processor() or platform.machine()
    try:
        if sys.platform == "darwin":
            cpu = (
                subprocess.run(
                    ["sysctl", "-n", "machdep.cpu.brand_string"],
                    check=False,
                    capture_output=True,
                    text=True,
                ).stdout.strip()
                or cpu
            )
        elif Path("/proc/cpuinfo").exists():
            for line in Path("/proc/cpuinfo").read_text().splitlines():
                if line.startswith("model name"):
                    cpu = line.split(":", 1)[1].strip()
                    break
    except OSError:
        pass
    return (
        f"{platform.system()} {platform.release()} {platform.machine()}; CPU {cpu}; "
        f"{os.cpu_count()} logical cores; Python {platform.python_version()}; "
        f"pyoxigraph {pyoxigraph.__version__}"
    )


def timeit(fn):
    ts = []
    for _ in range(REPEATS):
        t = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t)
    return ts


def main():
    if not VAULT.exists():
        subprocess.run([sys.executable, "-m", "gen", "--out", str(VAULT)], cwd=SPIKE, check=True)
    n = len(list(VAULT.glob("*.md")))
    # a mid-vault page that has links in both directions
    page = (
        "scenario-coded-000"
        if (VAULT / "scenario-coded-000.md").exists()
        else sorted(p.stem for p in VAULT.glob("*.md"))[n // 2]
    )
    print(f"machine: {machine()}")
    print(
        f"vault: {VAULT.relative_to(SPIKE)} ({n} pages); page under test: {page}; "
        f"{REPEATS} repeats, each run is cold (parse + load + rules); thresholds: R-5"
    )
    for name, scope, limit in (
        ("page", "page", 1.0),
        ("neighborhood", "neighborhood", 2.0),
        ("full", "full", 5.0),
    ):
        st, found = check(VAULT, scope, page)
        ts = timeit(lambda scope=scope: check(VAULT, scope, page))
        loaded = len(
            list(
                st.quads_for_pattern(
                    None, pyoxigraph.NamedNode("https://example.org/scat-placeholder#file"), None
                )
            )
        )
        med, mn = statistics.median(ts), min(ts)
        print(
            f"{name:13s} median {med:.3f}s  min {mn:.3f}s  max {max(ts):.3f}s  "
            f"(limit {limit:.0f}s, {'PASS' if max(ts) < limit else 'FAIL'} at max)  "
            f"pages loaded {loaded}; findings {len(found)}"
        )


if __name__ == "__main__":
    main()
