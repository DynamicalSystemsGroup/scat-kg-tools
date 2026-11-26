"""Method 1: possible duplicates from shared structure (same type only). Never reads names."""

from common import (
    jac,
    nodes_of,
    same_type_pairs,
    seed_label,
    signals,
    timed,
    vaults,
)

done = timed("m1")
for vname, g in vaults():
    nar, edg, adj = signals(g)
    ntype = {n.name: n.type for n in nodes_of(g)}
    rows = []
    for a, b in same_type_pairs(g):
        jn, je, ja = jac(nar[a], nar[b]), jac(edg[a], edg[b]), jac(adj[a], adj[b])
        # edge Jaccard: the edge, with the node itself masked, so shared adjacent+type counts
        rows.append((a, b, jn, je, ja, (jn + je + ja) / 3, min(len(nar[a]), len(nar[b]))))
    print(f"== {vname}: {len(rows)} same-type pairs, {len(nodes_of(g))} nodes")
    print("pair | narr-J | edge-J | adj-J | mean | seed")
    for r in sorted(rows, key=lambda r: -r[5])[:8]:
        print(
            f"  {r[0]} ~ {r[1]} | {r[2]:.2f} | {r[3]:.2f} | {r[4]:.2f} | {r[5]:.2f} | {seed_label(r[0], r[1])}"
        )
    print("threshold sweep (proposed pairs: total / seeded found / decoy proposed)")
    for rule, f in (
        ("adj-J>=t", lambda r: r[4]),
        ("edge-J>=t", lambda r: r[3]),
        ("narr-J>=t", lambda r: r[2]),
        ("mean>=t", lambda r: r[5]),
        ("adj-J>=t and narr-J>=0.3", lambda r: r[4] if r[2] >= 0.3 else -1),
        (
            "adj-J>=t and each has >=2 adjacent",
            lambda r, adj=adj: r[4] if min(len(adj[r[0]]), len(adj[r[1]])) >= 2 else -1,
        ),
    ):
        for t in (0.3, 0.5, 0.7, 1.0):
            got = [r for r in rows if f(r) >= t and f(r) > 0]
            found = [seed_label(r[0], r[1]) for r in got if seed_label(r[0], r[1])]
            print(f"  {rule} t={t}: proposed={len(got)} seeds={sorted(found)}")
    print("proposed at adj-J>=0.5 and each has >=2 adjacent nodes:")
    for r in sorted(rows, key=lambda r: -r[4]):
        if r[4] >= 0.5 and min(len(adj[r[0]]), len(adj[r[1]])) >= 2:
            print(
                f"  {r[0]} ~ {r[1]} ({ntype[r[0]]}) adj-J={r[4]:.2f} narr-J={r[2]:.2f} edge-J={r[3]:.2f} adjacent={sorted(adj[r[0]] & adj[r[1]])} {seed_label(r[0], r[1])}"
            )
done()
