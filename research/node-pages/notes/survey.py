"""Throwaway: survey of the range vault for RS4 Q1/Q3. Run: uv run python research/node-pages/notes/survey.py <vault>"""
import sys, itertools, math
from collections import defaultdict, Counter
sys.path.insert(0, "research/node-pages/notes")
from evidence import evidence
import scat_kg
root = sys.argv[1]
g = scat_kg.load(root)
names = [n.name for ns in g.nodes.values() for n in ns]
print("nodes", {k: len(v) for k, v in g.nodes.items()}, "narratives", len(g.narratives), "edges", len(g.edges))
print("\nnode: narratives(in account / row-only), edges, status, description chars")
for n in [n for ns in g.nodes.values() for n in ns]:
    ev = evidence(root, n.name)
    acc = sum(x["in_account"] for x in ev["narratives"])
    print(f"{n.type[:4]} {n.name:45s} narr={len(ev['narratives'])} acct={acc} edges={len(ev['edges'])} {n.status}")
