"""Method 1b: one narrative tells the same edge type to the same other end from two same-type pages."""

from collections import defaultdict

from common import jac, nodes_of, seed_label, signals, timed, vaults

done = timed("m1b")
for vname, g in vaults():
    nar, edg, adj = signals(g)
    ntype = {n.name: n.type for n in nodes_of(g)}
    hits = defaultdict(list)
    for n in g.narratives:
        ends = defaultdict(set)
        for k in n.edges:
            ends[(k.type, k.to_node, "to")].add(k.from_node)
            ends[(k.type, k.from_node, "from")].add(k.to_node)
        for (t, other, d), us in ends.items():
            us = sorted(u for u in us)
            for i, a in enumerate(us):
                for b in us[i + 1 :]:
                    if ntype[a] == ntype[b]:
                        hits[(a, b)].append((n.name, t, other))
    print(f"== {vname}: pairs with a twin row in one narrative: {len(hits)}")
    for (a, b), h in sorted(hits.items()):
        print(
            f"  {a} ~ {b} ({ntype[a]}) rows={len(h)} narr-J={jac(nar[a], nar[b]):.2f} "
            f"adj-J={jac(adj[a], adj[b]):.2f} {seed_label(a, b)} e.g. {h[0]}"
        )
done()
