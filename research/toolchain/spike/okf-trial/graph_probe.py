"""Probe OKF's reference graph builder on a vault. Usage: graph_probe.py OKF_SRC_DIR BUNDLE_DIR OUT_HTML
Imports reference_agent.viewer.generator from a clone (path passed as arg), reports nodes/edges, writes viz html."""
import sys
from pathlib import Path
src, bundle, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(src))
from reference_agent.viewer import generator as g
concepts = g._walk_concepts(bundle)
graph = g._build_graph(concepts)
print("concepts:", len(concepts))
print("types:", sorted({c.type for c in concepts}))
edges = [e["data"] for e in graph["edges"]] if isinstance(graph, dict) and "edges" in graph else graph
print("edges:", len(edges))
for e in edges[:10]:
    print("  ", e)
print("trust tiers:", sorted({c.trust_tier for c in concepts}))
g.generate_visualization(bundle, out)
print("wrote", out)
