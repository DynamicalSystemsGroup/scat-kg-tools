"""G2: the alternatives, drawn on the same narratives. Spike branch only; nothing here ships.

Run: uv run python research/candidates/proto/render.py   (writes research/candidates/img/ and prints the table)

Each alternative is a function from (the fingerprint's data, what the account links) to a drawing (`draw._Mark`),
drawn with the shipped renderer `draw._render`. Alternatives:
  0  no candidates (the baseline: rows only)
  a  as built: every candidate dashed; the flag when there is no account text
  b  the flag when the account links no node; every candidate dashed
  c  no flag; a candidate is drawn only when the account links both its nodes
  d  every candidate drawn; dashed when the account links both nodes, dotted grey when it does not; no flag
  e  as c, and one line says how many candidates were not drawn
"""

import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import evidence
from PIL import Image, ImageDraw

from scat_kg import draw, views

OUT = Path(__file__).resolve().parents[1] / "img"
DOT = ("#8a8a8a", (0, (1, 2.5)), 0.9)
ALTS = {
    "0": "no candidates (rows only)",
    "a": "as built: flag when no account text",
    "b": "flag when the account links no node",
    "c": "no flag; draw only with evidence",
    "d": "mark each candidate: evidence or not",
    "e": "as c, with a count of those not drawn",
}


def mark(alt: str, data: dict, acct: set) -> draw._Mark:
    n = data["narratives"][0]
    cands = n.get("candidates", [])
    has = lambda c: c["from"] in acct and c["to"] in acct
    flag = n.pop("no_account", False)
    n = dict(n)
    if alt == "0":
        n = {k: v for k, v in n.items() if k != "candidates"}
        return draw._fingerprint_mark({"narratives": [n]})
    if alt == "a":
        return draw._fingerprint_mark(
            {"narratives": [{**n, "candidates": cands, **({"no_account": True} if flag else {})}]}
        )
    if alt == "b":
        m = draw._fingerprint_mark({"narratives": [{**n, "candidates": cands}]})
        if not acct:
            m = draw._Mark(
                m.title,
                m.columns,
                m.lines,
                m.legend + "\nthe account links no node: every candidate "
                "for it is just a pair the rows link, not evidence.",
                m.styles,
                m.keys,
            )
        return m
    if alt in ("c", "e"):
        shown = [c for c in cands if has(c)]
        m = draw._fingerprint_mark({"narratives": [{**n, "candidates": shown}]})
        if alt == "e" and len(shown) < len(cands):
            k = len(cands) - len(shown)
            m = draw._Mark(
                m.title,
                m.columns,
                m.lines,
                m.legend + f"\n{k} more pair{'s' if k > 1 else ''} the rows link, "
                "with no row and no account link to both: not drawn.",
                m.styles,
                m.keys,
            )
        return m
    if alt == "d":
        m = draw._fingerprint_mark({"narratives": [{**n, "candidates": cands}]})
        styles = [draw.PLAIN] * len(n["edges"]) + [draw.CANDIDATE if has(c) else DOT for c in cands]
        keys = []
        if any(has(c) for c in cands):
            keys.append(("account links both nodes", draw.CANDIDATE))
        if any(not has(c) for c in cands):
            keys.append(("account does not link both", DOT))
        legend = m.legend.replace(
            "dashed line: a link with no row (a candidate).",
            "a link with no row (a candidate) is dashed or dotted, as keyed below.",
        )
        return draw._Mark(m.title, m.columns, m.lines, legend, tuple(styles), tuple(keys))
    raise ValueError(alt)


def png(alt, name, root, case) -> bytes:
    data = views.fingerprint(name, candidates=True, root=root).to_dict()
    return draw._render(mark(alt, data, set(case.account_nodes)), "png")


def sheet(name, root, case, alts, scale=0.62) -> Image.Image:
    ims = []
    for a in alts:
        im = Image.open(io.BytesIO(png(a, name, root, case))).convert("RGB")
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
        band = Image.new("RGB", (im.width, im.height + 22), "white")
        ImageDraw.Draw(band).text((6, 4), f"({a}) {ALTS[a]}", fill="#b00000")
        band.paste(im, (0, 22))
        ims.append(band)
    W = max(i.width for i in ims)
    out = Image.new("RGB", (W, sum(i.height for i in ims) + 6 * len(ims)), "white")
    y = 0
    for i in ims:
        out.paste(i, (0, y))
        y += i.height + 6
    return out


SHOW = [
    ("fixtures", "f1-rows-only"),
    ("fixtures", "f2-prose-no-links"),
    ("fixtures", "f3-prose-some-links"),
    ("fixtures", "f5-link-list-only"),
    ("examples", "saturday-at-the-lending-desk"),
    ("lab", "self-infrastructuring"),
]

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    allv = evidence.load_all()
    by = {
        (v, c.narrative): (c, root) for v, (g, root) in allv.items() for c in evidence.cases(g, v)
    }
    for v, name in SHOW:
        case, root = by[(v, name)]
        im = sheet(name, root, case, list(ALTS))
        im = im.quantize(colors=48, method=Image.MEDIANCUT)
        p = OUT / f"{name}.png"
        im.save(p, optimize=True)
        print(p.name, im.size, p.stat().st_size)


def table() -> str:
    """The alternatives on the same narratives: dashed lines drawn, grey dotted lines, the flag, the count line."""
    allv = evidence.load_all()
    rows = [
        "| narrative | candidates (evidence) | "
        + " | ".join(f"({a})" for a in ALTS if a != "0")
        + " |",
        "|---|---|" + "---|" * (len(ALTS) - 1),
    ]
    for v, name in SHOW + [
        ("fixtures", "f4-prose-all-links"),
        ("fixtures", "f6-all-told"),
        ("lab", "forget-incident"),
    ]:
        g, root = allv[v]
        case = next(c for c in evidence.cases(g, v) if c.narrative == name)
        data = views.fingerprint(name, candidates=True, root=root).to_dict()
        cells = []
        for a in ALTS:
            if a == "0":
                continue
            m = mark(a, data, set(case.account_nodes))
            dashed = sum(1 for _, _, d in m.lines if d)
            dotted = sum(1 for s in m.styles if s == DOT) if m.styles else 0
            if m.styles:
                dashed -= dotted
            bits = [f"{dashed} dashed"]
            if dotted:
                bits.append(f"{dotted} dotted")
            if "no account text" in m.legend or "links no node" in m.legend:
                bits.append("flag")
            if "more pair" in m.legend:
                bits.append("count line")
            cells.append(", ".join(bits))
        rows.append(
            f"| {name} | {len(case.candidates)} ({len(case.with_evidence)}) | "
            + " | ".join(cells)
            + " |"
        )
    return "\n".join(rows)


if __name__ == "__main__":
    print()
    print(table())
