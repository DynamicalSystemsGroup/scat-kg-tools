"""Throwaway: synonym/homonym candidates in a vault without matching names (RS4 Q3). Pure stdlib.
Run: uv run python research/node-pages/notes/synonyms.py <vault>
Methods:
 A  structural role: nodes of one layer compared by the edges they sit in (neighbour sets), not by words.
 B  context split (homonym): for a node in >=2 narratives, how much do the nodes co-linked in each narrative overlap?
 C  link-text profile: the display texts the coder wrote in [[node|text]] per node, and texts used for >1 node.
 D  passage similarity: tf-idf cosine over the paragraphs that link each node (words of the account, not of the names),
    reported only for pairs the names do not share a word with, and with the pair's narrative overlap.
 E  description reuse: near-identical `description` fields across pages (copying, and cross-layer conflation)."""
import re, sys, math, itertools
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, "research/node-pages/notes")
from evidence import evidence
import scat_kg
root = sys.argv[1]
g = scat_kg.load(root)
allnodes = [n for ns in g.nodes.values() for n in ns]
STOP = set("the a an and or of to in on for with by is are was were be been it its that this as at from their they them his her he she not but which who what when where how than then so such into out up one two also here there has have had can could would may more most only own same other no do does did if about over after before between both each across through not".split())
def toks(t): return [w for w in re.findall(r"[a-z]+", t.lower()) if w not in STOP and len(w) > 2]
def jac(a, b): return len(a & b) / len(a | b) if a | b else 0.0
def cos(a, b):
    num = sum(a[k] * b.get(k, 0) for k in a); da = math.sqrt(sum(v*v for v in a.values())); db = math.sqrt(sum(v*v for v in b.values()))
    return num / (da * db) if da and db else 0.0

print("== A. structural role (neighbour sets over edges; same layer)")
nb = defaultdict(set)
for e in g.edges: nb[e.from_node].add(e.to_node); nb[e.to_node].add(e.from_node)
for layer, ns in g.nodes.items():
    for a, b in itertools.combinations([n.name for n in ns], 2):
        j = jac(nb[a], nb[b])
        if j > 0: print(f"  {layer[:4]} {a} ~ {b}  jaccard={j:.2f} shared={sorted(nb[a]&nb[b])}")

print("\n== B. context split: per node, co-linked nodes in each narrative; overlap between narratives")
for n in allnodes:
    ctx = {nar.name: set(nar.nodes) - {n.name} for nar in g.narratives if n.name in nar.nodes}
    if len(ctx) < 2: continue
    ps = [jac(ctx[x], ctx[y]) for x, y in itertools.combinations(ctx, 2)]
    print(f"  {n.name:30s} narr={len(ctx)} mean-overlap={sum(ps)/len(ps):.2f} min={min(ps):.2f}")

print("\n== C. link-text profile")
text_for = defaultdict(set); node_for = defaultdict(lambda: defaultdict(set))
for p in Path(root).glob("narrative/*.md"):
    for tgt, txt in re.findall(r"\[\[([a-z0-9-]+)\|([^\]]+)\]\]", p.read_text()):
        text_for[tgt].add(txt.lower()); node_for[txt.lower()][tgt].add(p.stem)
for t, d in node_for.items():
    if len(d) > 1: print(f"  text {t!r} used for several nodes: {dict((k, sorted(v)) for k, v in d.items())}")
for k, v in sorted(text_for.items()):
    if len(v) > 1: print(f"  {k}: {sorted(v)}")

print("\n== D. passage tf-idf similarity (pairs sharing no word in their names; cross-layer included)")
docs = {}
for n in allnodes:
    ev = evidence(root, n.name); docs[n.name] = (n.type, Counter(toks(" ".join(re.sub(r"\[\[[^\]]*\]\]", " ", p) if False else p for x in ev["narratives"] for p in x["paras"]))), {x["name"] for x in ev["narratives"]})
df = Counter(w for _, c, _ in docs.values() for w in c)
N = len(docs)
vec = {k: {w: (1 + math.log(c)) * math.log(N / df[w]) for w, c in cnt.items()} for k, (_, cnt, _) in docs.items()}
rows = []
for a, b in itertools.combinations(docs, 2):
    if set(a.split("-")) & set(b.split("-")): continue
    rows.append((cos(vec[a], vec[b]), a, b))
for s, a, b in sorted(rows, reverse=True)[:12]:
    print(f"  {s:.2f} {a} ({docs[a][0][:4]}) ~ {b} ({docs[b][0][:4]}) shared-narr={sorted(docs[a][2] & docs[b][2])}")

print("\n== E. description reuse (cosine of description words, across all pages)")
desc = {}
for n in allnodes:
    m = re.search(r'^description: "(.*)"$', (Path(root) / n.path).read_text(), re.M)
    if m: desc[n.name] = Counter(toks(m.group(1)))
rows = sorted(((cos(desc[a], desc[b]), a, b) for a, b in itertools.combinations(desc, 2)), reverse=True)[:6]
for s, a, b in rows: print(f"  {s:.2f} {a} ~ {b}")

print("\n== D2. same layer, no shared narrative (the only pairs where 'same concept, different words' can hide)")
for s, a, b in sorted(((cos(vec[a], vec[b]), a, b) for a, b in itertools.combinations(docs, 2)
                       if docs[a][0] == docs[b][0] and not (docs[a][2] & docs[b][2])), reverse=True)[:8]:
    print(f"  {s:.2f} {docs[a][0][:4]} {a} ~ {b}  nbr-jaccard={jac(nb[a], nb[b]):.2f}")
print("  nodes in >=2 narratives:", sum(len(d[2]) >= 2 for d in docs.values()), "of", len(docs))
