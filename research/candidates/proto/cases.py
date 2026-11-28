"""G1: per narrative, candidates and how many carry evidence, by cause. Run: uv run python research/candidates/proto/cases.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import evidence

print(
    "| vault | narrative | cause | nodes | rows | account links | candidates | with evidence | in prose, not a list | in one paragraph |"
)
print("|---|---|---|---|---|---|---|---|---|---|")
totals: dict = {}
for vault, (g, _) in evidence.load_all().items():
    for c in evidence.cases(g, vault):
        print(
            f"| {vault} | {c.narrative} | {c.cause} | {c.nodes} | {c.rows} | {len(c.account_nodes)} "
            f"| {len(c.candidates)} | {len(c.with_evidence)} | {len(c.in_prose)} | {len(c.same_para)} |"
        )
        t = totals.setdefault((vault, c.cause), [0, 0, 0, 0, 0])
        t[0] += 1
        t[1] += len(c.candidates)
        t[2] += len(c.with_evidence)
        t[3] += len(c.in_prose)
        t[4] += len(c.same_para)
print()
print("| vault | cause | narratives | candidates | with evidence | in prose | one paragraph |")
print("|---|---|---|---|---|---|---|")
for (vault, cause), (n, k, e, pr, sp) in sorted(totals.items()):
    print(f"| {vault} | {cause} | {n} | {k} | {e} | {pr} | {sp} |")
