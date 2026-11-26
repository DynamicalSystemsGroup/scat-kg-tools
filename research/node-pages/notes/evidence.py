"""Throwaway: the evidence for one node, from what the vault already holds (RS4 Q1).
Run: uv run python research/node-pages/notes/evidence.py <vault> <node>
Returns: node page; narratives that link it (status, kind, timeframe); for each, the paragraphs of the account that
link it (with alias text used); its edges with narratives+notes; neighbours by layer; and narratives that tell nothing of it."""
import re, sys
from pathlib import Path
import scat_kg

def evidence(root, name):
    g = scat_kg.load(root)
    n = g.node(name)
    out = {"node": n, "narratives": [], "edges": [], "neighbours": {}}
    for nar in g.narratives:
        if name not in nar.nodes:
            continue
        text = (Path(root) / nar.path).read_text()
        body = re.split(r"^#{1,6}\s*Edges told\s*$", text, flags=re.M | re.I)[0]
        body = body.split("---", 2)[-1]
        paras = [p.strip() for p in re.split(r"\n\s*\n", body) if re.search(r"\[\[%s(\||\]\]|#)" % re.escape(name), p)]
        pat = r"\[\[%s(\||\]\]|#)" % re.escape(name)
        sents = [x.strip() for p in paras for x in re.split(r"(?<=[.!?])\s+", p.replace("\n", " ")) if re.search(pat, x)]
        aliases = sorted({m for p in paras for m in re.findall(r"\[\[%s\|([^\]]+)\]\]" % re.escape(name), p)})
        out["narratives"].append(dict(name=nar.name, status=nar.status, kind=nar.kind, timeframe=nar.timeframe,
                                      paras=paras, sentences=sents, aliases=aliases, in_account=bool(paras)))
    for e in g.edges:
        if name in (e.from_node, e.to_node):
            out["edges"].append(e)
            other = e.to_node if e.from_node == name else e.from_node
            out["neighbours"].setdefault(g.node(other).type, set()).add(other)
    return out

if __name__ == "__main__":
    root, name = sys.argv[1:3]
    ev = evidence(root, name)
    n = ev["node"]
    print(f"# {n.title} ({n.type}, {n.status})  — {len(ev['narratives'])} narratives, {len(ev['edges'])} edges")
    for x in ev["narratives"]:
        print(f"\n## {x['name']} [{x['status']}, {x['kind']}, {x['timeframe']}] aliases={x['aliases']} in_account={x['in_account']}")
        for p in x["sentences"]:
            print("  >", p)
    print("\n## Edges")
    for e in ev["edges"]:
        print(f"  {e.from_node} {e.type} {e.to_node} [{e.status}]")
        for t in e.tellings:
            print(f"     - {t.narrative}: {t.note}")
    print("\n## Neighbours", {k: sorted(v) for k, v in ev["neighbours"].items()})
