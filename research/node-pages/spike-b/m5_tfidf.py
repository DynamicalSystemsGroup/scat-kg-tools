"""Method 5: passage tf-idf. Each node is the bag of words of the paragraphs that link it (names and link syntax removed)."""

import math
import re
from collections import Counter

from common import (
    VAULTS,
    cos,
    jac,
    nodes_of,
    same_type_pairs,
    seed_label,
    signals,
    timed,
    toks,
    vaults,
)


def weigh(c, df, n_docs):
    return {x: (1 + math.log(n)) * math.log(n_docs / df[x]) for x, n in c.items()}


done = timed("m5")
for vname, g in vaults():
    root = VAULTS[vname]
    nar, _, adj = signals(g)
    docs = {n.name: Counter() for n in nodes_of(g)}
    paras = {n.name: {} for n in nodes_of(g)}  # node -> {paragraph id: words}
    for p in g.narratives:
        text = (root / p.path).read_text().split("\n---\n", 1)[1].split("## Edges told")[0]
        for para in text.split("\n\n"):
            for t in re.findall(r"\[\[([a-z0-9-]+)(?:\|[^\]]*)?\]\]", para):
                if t in docs:
                    clean = re.sub(
                        r"\[\[[^\]]*\]\]", " ", para
                    )  # drop link text and names: words of the account only
                    docs[t].update(toks(clean))
                    paras[t][(p.name, para)] = Counter(toks(clean))
    df = Counter(w for c in docs.values() for w in c)
    N = len(docs)
    vec = {
        k: {w: (1 + math.log(c)) * math.log(N / df[w]) for w, c in cnt.items()}
        for k, cnt in docs.items()
    }
    rows = sorted(((cos(vec[a], vec[b]), a, b) for a, b in same_type_pairs(g)), reverse=True)
    print(f"== {vname}: {len(rows)} same-type pairs; top 8 (cos, narr-J, adj-J)")
    for s, a, b in rows[:8]:
        print(
            f"  {s:.2f} {a} ~ {b} narr-J={jac(nar[a], nar[b]):.2f} adj-J={jac(adj[a], adj[b]):.2f} {seed_label(a, b)}"
        )
    for t in (0.3, 0.4, 0.5):
        hit = [(a, b) for s, a, b in rows if s >= t]
        print(
            f"  cos>={t}: proposed={len(hit)} seeds={[seed_label(a, b) for a, b in hit if seed_label(a, b)]}"
        )
    for lab in ("synonym", "duplicate-row", "decoy"):
        for i, (s, a, b) in enumerate(rows, 1):
            if seed_label(a, b) == lab:
                print(f"  seed {lab}: cos={s:.2f} rank {i}/{len(rows)}")

    # variant: leave out the paragraphs that link both nodes (shared paragraphs make identical text, not evidence)
    def excl(a, b, paras, df, n_docs):
        va, vb = Counter(), Counter()
        for k, c in paras[a].items():
            if k not in paras[b]:
                va.update(c)
        for k, c in paras[b].items():
            if k not in paras[a]:
                vb.update(c)

        return cos(weigh(va, df, n_docs), weigh(vb, df, n_docs))

    rows = sorted(((excl(a, b, paras, df, N), a, b) for a, b in same_type_pairs(g)), reverse=True)
    print(f"-- {vname} without shared paragraphs; top 6")
    for s, a, b in rows[:6]:
        print(f"  {s:.2f} {a} ~ {b} narr-J={jac(nar[a], nar[b]):.2f} {seed_label(a, b)}")
    for t in (0.2, 0.3, 0.4):
        hit = [(a, b) for s, a, b in rows if s >= t]
        print(
            f"  cos>={t}: proposed={len(hit)} seeds={[seed_label(a, b) for a, b in hit if seed_label(a, b)]}"
        )
    for lab in ("synonym", "duplicate-row", "decoy"):
        for i, (s, a, b) in enumerate(rows, 1):
            if seed_label(a, b) == lab:
                print(f"  seed {lab}: cos={s:.2f} rank {i}/{len(rows)}")
done()
