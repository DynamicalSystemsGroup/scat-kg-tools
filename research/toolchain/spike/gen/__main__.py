"""Generate a deterministic synthetic vault that follows the spike's frontmatter contract.

uv run --directory research/toolchain/spike python -m gen --out out/vault500
"""

import argparse
import random
from pathlib import Path

import yaml

# page counts per type; the default sums to 500
COUNTS = {
    "stakeholder-group": 30,
    "concern": 100,
    "affordance": 100,
    "technology": 50,
    "scenario-raw": 55,
    "scenario-coded": 55,
    "architecture-raw": 55,
    "architecture-coded": 55,
}
STATUSES = ["stub", "draft", "done"]


def link(stem):
    return f"[[{stem}]]"


def build(seed=1):
    rng = random.Random(seed)
    names = {t: [f"{t}-{i:03d}" for i in range(n)] for t, n in COUNTS.items()}

    def pick(t, k):
        return [link(s) for s in sorted(rng.sample(names[t], k))]

    pages = {}

    def add(t, stem, rel, body):
        status = rng.choice(STATUSES)
        fm = {"type": t, "status": status, "title": stem.replace("-", " ").capitalize()}
        if status != "stub":
            fm["description"] = f"Synthetic {t} page."
        if status == "done" or rng.random() < 0.5:
            fm.update(rel)
        pages[stem] = (fm, body)

    for s in names["stakeholder-group"]:
        add("stakeholder-group", s, {"heldby": pick("concern", 3)}, "Synthetic group.")
    for s in names["concern"]:
        add("concern", s, {"addresses": pick("affordance", 2)}, "Synthetic concern.")
    for s in names["affordance"]:
        add("affordance", s, {"attributes": pick("technology", 2)}, "Synthetic affordance.")
    for s in names["technology"]:
        add("technology", s, {}, "Synthetic technology.")
    for kind in ("scenario", "architecture"):
        for i, raw in enumerate(names[f"{kind}-raw"]):
            coded = names[f"{kind}-coded"][i]
            mention = pick("concern", 1)[0]
            add(f"{kind}-raw", raw, {"coded": [link(coded)]}, f"Notes mentioning {mention}.")
            if kind == "scenario":
                rel = {
                    "groups": pick("stakeholder-group", 2),
                    "concerns": pick("concern", 3),
                    "affordances": pick("affordance", 2),
                }
            else:
                rel = {
                    "concerns": pick("concern", 3),
                    "affordances": pick("affordance", 2),
                    "technologies": pick("technology", 2),
                }
            # coded records must carry the full contract once done: add() guarantees it
            add(f"{kind}-coded", coded, {"raw": [link(raw)], **rel}, "Synthetic coded record.")
    return pages


def write(pages, out):
    out.mkdir(parents=True, exist_ok=True)
    for stem in sorted(pages):
        fm, body = pages[stem]
        text = yaml.safe_dump(fm, sort_keys=False, default_flow_style=False, allow_unicode=True)
        (out / f"{stem}.md").write_text(f"---\n{text}---\n{body}\n", newline="\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, required=True, help="output directory (created)")
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    pages = build(a.seed)
    write(pages, a.out)
    print(f"wrote {len(pages)} pages to {a.out}")


if __name__ == "__main__":
    main()
