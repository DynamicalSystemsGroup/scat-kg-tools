"""Method 3: homonym check by structure. For a node, split the narratives that link it into groups.
A: two narratives are joined if they share another node (any link) or an edge, apart from the node itself.
B: joined if they tell an edge of the node to the same other end (adjacent node).
C: B, but narratives that tell no edge of the node are dropped first (they only mention it)."""

from collections import defaultdict

from common import HOMONYM, nodes_of, timed, vaults


def components(items, joined):
    items, seen, out = list(items), set(), []
    for s in items:
        if s in seen:
            continue
        comp, stack = set(), [s]
        while stack:
            x = stack.pop()
            if x in comp:
                continue
            comp.add(x)
            stack += [y for y in items if y not in comp and joined(x, y)]
        seen |= comp
        out.append(sorted(comp))
    return out


done = timed("m3")
for vname, g in vaults():
    narr = {n.name: n for n in g.narratives}
    print(f"== {vname}")
    flagged = defaultdict(dict)
    for node in nodes_of(g):
        me = node.name
        linking = [n.name for n in g.narratives if me in n.nodes]
        if len(linking) < 2:
            continue
        other = {x: set(narr[x].nodes) - {me} for x in linking}
        ends = {
            x: {
                (k.to_node if k.from_node == me else k.from_node)
                for k in narr[x].edges
                if me in (k.from_node, k.to_node)
            }
            for x in linking
        }
        flagged["A"][me] = components(linking, lambda x, y, other=other: bool(other[x] & other[y]))
        flagged["B"][me] = components(linking, lambda x, y, ends=ends: bool(ends[x] & ends[y]))
        told = [x for x in linking if ends[x]]
        flagged["C"][me] = (
            components(told, lambda x, y, ends=ends: bool(ends[x] & ends[y]))
            if len(told) >= 2
            else []
        )
    for m, d in flagged.items():
        hit = {k: v for k, v in d.items() if len(v) >= 2}
        print(
            f"method {m}: nodes with >=2 narratives {len(d)}; flagged (>=2 groups) {len(hit)}; {HOMONYM} flagged: {HOMONYM in hit}"
        )
        for k, v in sorted(hit.items(), key=lambda kv: -len(kv[1])):
            print(f"    {k}: {len(v)} groups {[len(c) for c in v]}")
            if m == "C" or k == HOMONYM:
                for c in v:
                    print(f"        {c}")
done()
