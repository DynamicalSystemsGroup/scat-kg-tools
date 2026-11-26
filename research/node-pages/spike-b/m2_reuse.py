"""Method 2: description and body reuse between same-type pages (cosine of word counts; stubs have no description)."""

from collections import Counter

from common import (
    VAULTS,
    body,
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

done = timed("m2")
for vname, g in vaults():
    root = VAULTS[vname]
    nar, edg, adj = signals(g)
    nd = {n.name: n for n in nodes_of(g)}
    dv = {k: Counter(toks(desc(root, n))) for k, n in nd.items()}
    bv = {k: Counter(toks(body(root, n))) for k, n in nd.items()}
    for label, vec in (("description", dv), ("body", bv)):
        rows = [(cos(vec[a], vec[b]), a, b) for a, b in same_type_pairs(g) if vec[a] and vec[b]]
        rows.sort(reverse=True)
        print(f"== {vname} {label}: {len(rows)} same-type pairs with text on both; top 6")
        for s, a, b in rows[:6]:
            print(f"  {s:.2f} {a} ~ {b} {seed_label(a, b)} narr-J={jac(nar[a], nar[b]):.2f}")
        for t in (0.5, 0.7, 0.9):
            hit = [(a, b) for s, a, b in rows if s >= t]
            print(
                f"  cos>={t}: proposed={len(hit)} seeds={[seed_label(a, b) for a, b in hit if seed_label(a, b)]}"
            )
    ds = sorted(
        ((cos(dv[a], dv[b]), a, b) for a in nd for b in nd if a < b and dv[a] and dv[b]),
        reverse=True,
    )[:3]
    print(
        "  any-type top descriptions:",
        [(round(s, 2), a, b, nd[a].type, nd[b].type) for s, a, b in ds],
    )
done()
