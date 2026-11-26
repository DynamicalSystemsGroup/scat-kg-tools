"""Method 4: link-text profile: the display texts the coder wrote in [[node|text]], per node (not node names)."""

import re
from collections import Counter, defaultdict

from common import VAULTS, cos, nodes_of, same_type_pairs, seed_label, timed, toks, vaults

done = timed("m4")
for vname, g in vaults():
    root = VAULTS[vname]
    ntype = {n.name: n.type for n in nodes_of(g)}
    texts = defaultdict(Counter)
    by_text = defaultdict(lambda: defaultdict(set))
    for p in (root / "narrative").glob("*.md"):
        for tgt, txt in re.findall(r"\[\[([a-z0-9-]+)\|([^\]]+)\]\]", p.read_text()):
            texts[tgt][txt.lower()] += 1
            by_text[txt.lower()][tgt].add(p.stem)
    print(f"== {vname}: nodes with link texts {len(texts)}; texts used for >1 node:")
    for t, d in by_text.items():
        if len(d) > 1:
            print(f"  {t!r}: { {k: sorted(v) for k, v in d.items()} }")
    print("  nodes whose link texts differ by >=3 distinct strings:")
    for k, c in sorted(texts.items(), key=lambda kv: -len(kv[1]))[:5]:
        print(f"    {k}: {len(c)} distinct {dict(c)}")
    vec = {
        k: Counter(w for t, n in c.items() for w in toks(t) for _ in range(n))
        for k, c in texts.items()
    }
    rows = sorted(
        ((cos(vec[a], vec[b]), a, b) for a, b in same_type_pairs(g) if a in vec and b in vec),
        reverse=True,
    )
    print("  same-type pairs by link-text word overlap (top 5):")
    for s, a, b in rows[:5]:
        print(f"    {s:.2f} {a} ~ {b} {seed_label(a, b)}")
    print("  link texts for the seeded homonym, by narrative:")
    for p in sorted((root / "narrative").glob("*.md")):
        found = re.findall(r"\[\[community-members\|([^\]]+)\]\]", p.read_text())
        if found:
            print(f"    {p.stem}: {found}")
done()
