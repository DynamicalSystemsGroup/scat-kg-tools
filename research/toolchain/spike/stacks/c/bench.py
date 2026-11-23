"""Time the three stack C checks on a vault (default: out/vault500).

    uv run --directory research/toolchain/spike python -m stacks.c.bench [--vault DIR] [--repeats N]

Each repeat builds a fresh Vault (nothing cached between repeats); the OS file cache is warm.
R-5 limits: page < 1 s, neighborhood < 2 s, whole vault < 5 s.
"""

import argparse
import os
import platform
import statistics
import sys
import time
from pathlib import Path

from .checks import Vault, check_neighborhood, check_page, check_vault

LIMITS = {"page": 1.0, "neighborhood": 2.0, "vault": 5.0}


def timed(fn):
    t = time.perf_counter()
    r = fn()
    return time.perf_counter() - t, r


def machine():
    cpu = platform.processor() or platform.machine()
    if sys.platform == "darwin":
        import subprocess

        try:
            cpu = (
                subprocess.run(
                    ["sysctl", "-n", "machdep.cpu.brand_string"],
                    check=False,
                    capture_output=True,
                    text=True,
                ).stdout.strip()
                or cpu
            )
        except OSError:
            pass
    return (
        f"{platform.platform()}; {cpu}; {os.cpu_count()} logical CPUs; "
        f"Python {platform.python_version()} ({platform.python_implementation()})"
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--vault", type=Path, default=Path("out/vault500"))
    ap.add_argument("--repeats", type=int, default=7)
    a = ap.parse_args()
    if not a.vault.is_dir():
        sys.exit(
            f"{a.vault} not found; generate it: uv run --directory research/toolchain/spike "
            f"python -m gen --out {a.vault}"
        )
    stems = sorted(p.stem for p in a.vault.glob("*.md"))
    mid = stems[len(stems) // 2]
    # a hub: the page with the most inbound+outbound links is the worst-case neighborhood
    v0 = Vault(a.vault)
    biggest = max(stems[:: max(1, len(stems) // 50)], key=lambda s: len(v0.inbound(s)))
    print(f"machine: {machine()}")
    print(f"vault: {a.vault} ({len(stems)} pages); repeats: {a.repeats}")
    cases = {
        "page": lambda v: check_page(v, mid),
        "neighborhood": lambda v: check_neighborhood(v, biggest),
        "vault": lambda v: check_vault(v),
    }
    print(f"page = {mid}; neighborhood centre = {biggest}")
    print(
        f"{'scope':14}{'median s':>10}{'min s':>10}{'max s':>10}{'limit s':>9}  verdict  (violations)"
    )
    for name, fn in cases.items():
        ts = []
        n = 0
        for _ in range(a.repeats):
            v = Vault(a.vault)  # includes directory listing + cold parse
            dt, res = timed(lambda fn=fn, v=v: fn(v))
            ts.append(dt)
            n = len(res)
        med = statistics.median(ts)
        ok = "within" if max(ts) < LIMITS[name] else "OVER"
        print(
            f"{name:14}{med:10.4f}{min(ts):10.4f}{max(ts):10.4f}{LIMITS[name]:9.1f}  {ok:7}  ({n})"
        )


if __name__ == "__main__":
    main()
