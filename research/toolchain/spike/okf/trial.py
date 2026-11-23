"""Trial driver. usage: python -I trial.py CLONE_DIR {roundtrip|graph|wikilinks} DIR
Imports OKF's own code (reference_agent.bundle.document / viewer.generator) from the pinned clone."""
import json, re, sys
from collections import Counter
from pathlib import Path
clone, cmd, d = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
sys.path.insert(0, str(clone / "src"))

if cmd == "roundtrip":
    from reference_agent.bundle.document import OKFDocument
    same = diff = 0
    for p in sorted(d.glob("*.md")):
        t = p.read_text(encoding="utf-8")
        out = OKFDocument.parse(t).serialize()
        if out == t: same += 1
        else:
            diff += 1
            if diff <= 2:
                print(f"--- first difference in {p.name}")
                import difflib
                print("".join(difflib.unified_diff(t.splitlines(1), out.splitlines(1), "orig", "okf-serialized", n=1)))
    print(f"parse->serialize identical={same} different={diff}")
elif cmd == "graph":
    from reference_agent.viewer import generator as g
    cs = g._walk_concepts(d)
    gr = g._build_graph(cs)
    print("concepts:", len(cs), " edges:", len(gr["edges"]))
    print("types:", dict(Counter(c.type for c in cs)))
    print("status as seen by OKF:", dict(Counter(c.status for c in cs)))
    print("trust tiers:", dict(Counter(c.trust_tier for c in cs)))
    print("edge sample:", sorted((e["data"]["source"], e["data"]["target"]) for e in gr["edges"])[:5])
    print("nodes with no edge:", sorted(set(c.id for c in cs) - {e["data"][k] for e in gr["edges"] for k in ("source","target")}))
elif cmd == "wikilinks":
    # baseline, independent of OKF: distinct (page -> target) wikilink pairs in body and frontmatter
    W = re.compile(r"\[\[([^\]|#]+)")
    body_pairs, fm_pairs = set(), set()
    for p in d.glob("*.md"):
        t = p.read_text(encoding="utf-8"); end = t.index("\n---\n", 4) + 5
        for m in W.finditer(t[end:]): body_pairs.add((p.stem, m.group(1)))
        for m in W.finditer(t[:end]): fm_pairs.add((p.stem, m.group(1)))
    print(f"pages={len(list(d.glob('*.md')))} body_link_pairs={len(body_pairs)} frontmatter_link_pairs={len(fm_pairs)} total_distinct={len(body_pairs|fm_pairs)}")
