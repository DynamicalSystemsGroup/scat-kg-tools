"""Method 3b: for each node, the share of narrative pairs (among narratives that tell an edge of it) that tell it to
a common other end. Low share = the accounts of the node do not overlap. Rank of the seeded homonym."""

import itertools

from common import HOMONYM, jac, nodes_of, timed, vaults

done = timed("m3b")
for vname, g in vaults():
    narr = {n.name: n for n in g.narratives}
    rows = []
    for node in nodes_of(g):
        me = node.name
        ends = {
            n.name: {
                (k.to_node if k.from_node == me else k.from_node)
                for k in n.edges
                if me in (k.from_node, k.to_node)
            }
            for n in g.narratives
            if me in n.nodes
        }
        ends = {k: v for k, v in ends.items() if v}
        if len(ends) < 3:
            continue
        pairs = list(itertools.combinations(ends, 2))
        share = sum(bool(ends[a] & ends[b]) for a, b in pairs) / len(pairs)
        mj = sum(jac(ends[a], ends[b]) for a, b in pairs) / len(pairs)
        rows.append((share, mj, me, len(ends)))
    rows.sort()
    print(
        f"== {vname}: {len(rows)} nodes told in >=3 narratives; lowest first (share of pairs with a common end / mean Jaccard)"
    )
    for i, (s, mj, me, n) in enumerate(rows[:8], 1):
        print(
            f"  {i}. {me} narratives={n} share={s:.2f} meanJ={mj:.2f}{'  <- seeded homonym' if me == HOMONYM else ''}"
        )
    print("  rank of", HOMONYM, [i for i, r in enumerate(rows, 1) if r[2] == HOMONYM])
done()
