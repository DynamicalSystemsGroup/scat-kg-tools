"""Throwaway prototype of `merge A into B` on a COPY of a vault (RS4 Q3). Not the tool; shows the operation and
its conformance test. Run: uv run python research/node-pages/notes/merge.py <vault> <A> <B> [apply]
Plan: (1) refuse unless A and B exist and have the same type; (2) rewrite every body link to A as a link to B, keeping
the shown text (a bare [[A]] in prose becomes [[B|A]]; inside a table cell, the alias bar is escaped); (3) drop A's page,
appending its body to B under a heading; (4) post-check: no new error, and the graph after equals the graph before
with A renamed B (edges, fingerprints, edge tellings), else the copy is thrown away."""
import re, shutil, sys, tempfile
from pathlib import Path
import scat_kg

def rewrite(text, a, b):
    """Rewrite links to page a as links to page b, keeping the text a reader saw. Skips frontmatter and code fences."""
    link = re.compile(r"(!?\[\[)" + re.escape(a) + r"((?:[#^|\\][^\]]*)?)\]\]")
    out, hits, fence = [], 0, False
    fm = text.startswith("---")
    for i, line in enumerate(text.split("\n")):
        if fm and i > 0 and line == "---": fm = False; out.append(line); continue
        if line.lstrip().startswith("```"): fence = not fence
        if fence or fm or i == 0 and line == "---":
            out.append(line); continue
        in_cell = line.lstrip().startswith("|")
        def sub(m):
            nonlocal hits
            hits += 1
            rest = m.group(2)
            if not rest:   # bare link: in prose keep the shown text with an alias; in a table end keep it bare
                rest = "" if in_cell else "|" + a
            return f"{m.group(1)}{b}{rest}]]"
        out.append(link.sub(sub, line))
    return "\n".join(out), hits

def snapshot(g, rename=None):
    """Edges (type, from, to) with the narratives that tell them (names only), and each narrative's fingerprint;
    with `rename` = (a, b) the image under a -> b, tellings of edges that coincide united."""
    r = (lambda n: rename[1] if rename and n == rename[0] else n)
    edges = {}
    for e in g.edges:
        edges.setdefault((e.type, r(e.from_node), r(e.to_node)), set()).update(t.narrative for t in e.tellings)
    fps = {n.name: (sorted({r(x) for x in n.nodes}), sorted({(e.type, r(e.from_node), r(e.to_node)) for e in n.edges}))
           for n in g.narratives}
    return edges, fps

def errors(root):
    rep = scat_kg.check(root=root)
    return [str(p) for p in getattr(rep.report, "problems", [])] if hasattr(rep, "report") else []

if __name__ == "__main__":
    src, a, b = sys.argv[1:4]
    tmp = Path(tempfile.mkdtemp(dir="research/node-pages/notes/scratch")) / "v"
    shutil.copytree(src, tmp)
    g0 = scat_kg.load(str(tmp)); na, nb = g0.node(a), g0.node(b)
    assert na and nb, "both must exist"
    if na.type != nb.type: sys.exit(f"REFUSED: {a} is a {na.type}, {b} is a {nb.type}")
    before = snapshot(g0, (a, b))
    touched = {}
    for p in tmp.rglob("*.md"):
        if p.name == a + ".md": continue
        t = p.read_text(); new, hits = rewrite(t, a, b)
        if hits: touched[p.relative_to(tmp).as_posix()] = hits; p.write_text(new)
    pa = tmp / na.path; body = pa.read_text().split("---", 2)[2].strip()
    pb = tmp / nb.path
    if body: pb.write_text(pb.read_text().rstrip() + f"\n\n## Merged from {a}\n\n{body}\n")
    pa.unlink()
    print("links rewritten:", touched)
    r = scat_kg.check(root=str(tmp)); print("check after:", str(r).splitlines()[-1])
    g1 = scat_kg.load(str(tmp)); after = snapshot(g1)
    e0, f0 = before; e1, f1 = after
    merged_edges = {k for k in e0 if k not in e1 or e0[k] != e1[k]}
    print("graph equal under rename:", e0 == e1 and f0 == f1)
    if e0 != e1:
        print("  edge keys lost/changed:", sorted(set(e0) - set(e1))[:5], "| new:", sorted(set(e1) - set(e0))[:5])
    print("skipped rows after:", [(s.narrative, s.reason) for s in g1.skipped])
    print("copy at", tmp)
