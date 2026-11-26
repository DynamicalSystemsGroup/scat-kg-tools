"""The recommended rule set for possible duplicates, as one output list (fields the review view would show).
R1 shared structure: adjacent-node Jaccard >= 0.5 and each page has >= 2 adjacent nodes.
R2 reuse: description word cosine >= 0.5.
R3 twin row: one narrative tells the same edge type to the same other end for both pages, and narrative Jaccard >= 0.5."""

from collections import Counter, defaultdict

from common import (
    VAULTS,
    cos,
    desc,
    jac,
    nodes_of,
    same_type_pairs,
    seed_label,
    signals,
    timed,
    toks,
    vaults,
)

done = timed("m6")
for vname, g in vaults():
    root = VAULTS[vname]
    nar, edg, adj = signals(g)
    nd = {n.name: n for n in nodes_of(g)}
    dv = {k: Counter(toks(desc(root, n))) for k, n in nd.items()}
    twin = defaultdict(int)
    for n in g.narratives:
        ends = defaultdict(set)
        for k in n.edges:
            ends[(k.type, k.to_node, "to")].add(k.from_node)
            ends[(k.type, k.from_node, "from")].add(k.to_node)
        for us in ends.values():
            us = sorted(us)
            for i, a in enumerate(us):
                for b in us[i + 1 :]:
                    if nd[a].type == nd[b].type:
                        twin[(a, b)] += 1
    out = []
    for a, b in same_type_pairs(g):
        a, b = sorted((a, b))
        s_adj, s_nar, s_desc, s_twin = (
            jac(adj[a], adj[b]),
            jac(nar[a], nar[b]),
            cos(dv[a], dv[b]),
            twin[(a, b)],
        )
        why = []
        if s_adj >= 0.5 and min(len(adj[a]), len(adj[b])) >= 2:
            why.append(f"{len(adj[a] & adj[b])} of {len(adj[a] | adj[b])} adjacent nodes shared")
        if s_desc >= 0.5:
            why.append(f"descriptions share {s_desc:.2f} of their words")
        if s_twin and s_nar >= 0.5:
            why.append(f"a narrative tells the same row for both ({s_twin}x)")
        if why:
            out.append((a, b, nd[a].type, s_nar, s_adj, s_desc, s_twin, "; ".join(why)))
    print(
        f"== {vname}: {len(out)} possible duplicates proposed of {sum(1 for _ in same_type_pairs(g))} same-type pairs"
    )
    print("a | b | type | narr-J | adj-J | desc-cos | twin rows | reason | seed")
    for r in sorted(out, key=lambda r: -(r[3] + r[4] + r[5])):
        print(
            f"  {r[0]} | {r[1]} | {r[2]} | {r[3]:.2f} | {r[4]:.2f} | {r[5]:.2f} | {r[6]} | {r[7]} | {seed_label(r[0], r[1])}"
        )
    found = {seed_label(r[0], r[1]) for r in out} - {""}
    print(f"  seeds proposed: {sorted(found)}; decoy proposed: {'decoy' in found}")
done()
