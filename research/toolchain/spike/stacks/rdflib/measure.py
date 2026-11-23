"""Measure one stack (identical file in stacks/plain and stacks/rdflib; imports the sibling check.py).

Usage (from the spike dir): uv run --locked python stacks/<stack>/measure.py [--runs N] [--full-runs N]
Generates the 500-page vault (gen_vault.py, fixed seed) into a temp dir. Timed: each check call alone
(local / neighborhood / full), after `load`. `load` (parse every page + build the stack's in-memory
index/store) is timed separately and is NOT in the check columns. One untimed warm-up call per cell.
"""
import argparse
import importlib.metadata as md
import platform
import statistics as st
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPIKE = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SPIKE))
import check  # noqa: E402
import gen_vault  # noqa: E402
from common import parse_vault  # noqa: E402

LIMITS = {"local": 1.0, "neighborhood": 2.0, "full": 5.0}


def machine():
    def sh(c):
        return subprocess.run(c, shell=True, capture_output=True, text=True).stdout.strip()
    mem = int(sh("sysctl -n hw.memsize") or 0) / 2**30
    libs = ", ".join(f"{p}={md.version(p)}" for p in ("rdflib", "pyshacl", "pydantic", "python-frontmatter", "pyyaml"))
    return [f"- CPU: {sh('sysctl -n machdep.cpu.brand_string')}; cores: {sh('sysctl -n hw.ncpu')}; RAM: {mem:.0f} GiB",
            f"- OS: {platform.platform()}",
            f"- Python: {platform.python_version()} ({platform.python_implementation()})",
            f"- Libraries: {libs}"]


def timeit(fn, n):
    fn()  # untimed warm-up
    ts = []
    for _ in range(n):
        t = time.perf_counter()
        r = fn()
        ts.append(time.perf_counter() - t)
    return ts, r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=7)
    ap.add_argument("--full-runs", type=int, default=5)
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as d:
        gen_vault.main(d)
        pages = parse_vault(d)
        deg = {p["name"]: len(p["links"]) for p in pages}
        for p in pages:
            for t in p["links"]:
                deg[t] = deg.get(t, 0) + 1
        ranked = sorted(deg, key=lambda n: (deg[n], n))
        picks = {"hub": ranked[-1], "typical": ranked[len(ranked) // 2]}

        print(f"# measure.py: stack `{HERE.name}`\n")
        print("\n".join(machine()))
        print(f"- Vault: {len(pages)} pages, {sum(len(p['links']) for p in pages)} links (gen_vault.py, seed fixed)")
        print(f"- Pages: hub = {picks['hub']!r} (degree {deg[picks['hub']]}), "
              f"typical = {picks['typical']!r} (degree {deg[picks['typical']]})")
        print(f"- Runs: {a.runs} per local/neighborhood cell, {a.full_runs} for full, plus 1 untimed warm-up each\n")

        lt, idx = timeit(lambda: check.load(d), a.full_runs)
        rows = [("load (parse + build, not a check)", "-", lt, None)]
        cells = []
        for label, name in picks.items():
            cells.append((f"local, {label}", "local", lambda n=name: check.check_local(idx, n), a.runs))
            cells.append((f"neighborhood, {label}", "neighborhood",
                          lambda n=name: check.check_neighborhood(idx, n), a.runs))
        cells.append(("full (500 pages)", "full", lambda: check.check_full(idx), a.full_runs))
        for label, scope, fn, n in cells:
            ts, res = timeit(fn, n)
            assert not res, f"clean synthetic vault must have 0 violations, got {len(res)}: {res[0]}"
            rows.append((label, scope, ts, LIMITS[scope]))

        print("| what is timed | median ms | min ms | max ms | n | threshold ms | verdict |")
        print("|---|---|---|---|---|---|---|")
        for label, scope, ts, lim in rows:
            m = st.median(ts)
            v = "-" if lim is None else ("PASS" if max(ts) < lim else "FAIL (max)" if m < lim else "FAIL")
            print(f"| {label} | {m*1e3:.3f} | {min(ts)*1e3:.3f} | {max(ts)*1e3:.3f} | {len(ts)} | "
                  f"{'-' if lim is None else '< ' + str(int(lim*1000))} | {v} |")
        lm = st.median(lt)
        print("\nCold single invocation (load + one check, medians added): "
              + "; ".join(f"{lab} = {(lm + st.median(ts))*1e3:.1f} ms" for lab, sc, ts, _ in rows[1:] if sc != "-"
                          and lab in ("local, hub", "neighborhood, hub", "full (500 pages)")))
        print("Check outputs on the clean vault: 0 violations in every cell (asserted).")


if __name__ == "__main__":
    main()
