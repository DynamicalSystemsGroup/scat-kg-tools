"""Generate a deterministic synthetic vault (500 pages) into a directory.

Usage: uv run python gen_vault.py [OUT_DIR]   (default /tmp/scpt-vault-500)
Same structure as vault/: flat dir, one .md per page, type in frontmatter.
"""
import random
import sys
from pathlib import Path

COUNTS = {"StakeholderGroup": 40, "Concern": 80, "Affordance": 60, "Technology": 40,
          "Heldby": 100, "Addresses": 100, "Attributes": 80}  # sums to 500
PREFIX = {"StakeholderGroup": "Group", "Concern": "Concern", "Affordance": "Affordance",
          "Technology": "Tech"}
STATUSES = ["done"] * 6 + ["draft"] * 3 + ["stub"]
RELS = {"Heldby": ("stakeholder", "StakeholderGroup", "concern", "Concern"),
        "Addresses": ("concern", "Concern", "affordance", "Affordance"),
        "Attributes": ("affordance", "Affordance", "technology", "Technology")}


def page(meta, body):
    fm = "\n".join(f"{k}: {v}" for k, v in meta.items())
    return f"---\n{fm}\n---\n{body}\n"


def main(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20261123)
    names = {}
    for cls, pre in PREFIX.items():
        names[cls] = [f"{pre} {i:03d}" for i in range(1, COUNTS[cls] + 1)]
        for n in names[cls]:
            d = f"Synthetic {cls} number {n.split()[1]}."
            meta = {"type": cls, "name": n, "status": rng.choice(STATUSES), "description": d}
            (out / f"{n}.md").write_text(page(meta, f"# {n}\n\n{d}"))
    for rel, (k1, c1, k2, c2) in RELS.items():
        for i in range(1, COUNTS[rel] + 1):
            a, b = rng.choice(names[c1]), rng.choice(names[c2])
            n = f"{rel} {i:03d}"
            meta = {"type": rel, "name": n, "status": rng.choice(STATUSES),
                    k1: f'"[[{a}]]"', k2: f'"[[{b}]]"', "rationale": "Synthetic."}
            (out / f"{n}.md").write_text(page(meta, f"# {n}\n\n[[{a}]] and [[{b}]]: synthetic."))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/scpt-vault-500")
