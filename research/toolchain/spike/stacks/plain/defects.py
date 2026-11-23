"""Seeded-defect copies of the mini-vault (temp dir; spike/vault is never edited). Prints the real output.

Usage (from the spike dir): uv run --locked python stacks/<stack>/defects.py
"""
import re
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPIKE = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SPIKE))
import check  # noqa: E402

VAULT = SPIKE / "vault"


def d1(v):  # missing required field: drop `description` from a Concern
    p = v / "Anonymity.md"
    p.write_text(re.sub(r"^description:.*\n", "", p.read_text(), flags=re.M))


def d2(v):  # relation endpoint of the wrong class: an Addresses page whose affordance is a Concern
    p = v / "Anonymity addressed by Pseudonymous records.md"
    p.write_text(p.read_text().replace('affordance: "[[Pseudonymous records]]"', 'affordance: "[[Attribution]]"'))


def d3(v):  # link to a missing page
    p = v / "Attribution.md"
    p.write_text(p.read_text().rstrip("\n") + "\n\nSee also [[Nonexistent page]].\n")


DEFECTS = [("1 missing required field (Anonymity.md loses `description`)", d1, "Anonymity"),
           ("2 wrong endpoint class (Addresses.affordance -> a Concern)", d2,
            "Anonymity addressed by Pseudonymous records"),
           ("3 link to a missing page (Attribution.md body)", d3, "Attribution")]


def main():
    base = check.check_full(check.load(VAULT))
    print(f"baseline spike/vault: {len(base)} violations\n")
    for title, mutate, page in DEFECTS:
        with tempfile.TemporaryDirectory() as t:
            v = Path(t) / "vault"
            shutil.copytree(VAULT, v)
            mutate(v)
            print(f"=== defect {title}")
            out = check.check_full(check.load(v))
            raw = getattr(check, "LAST_RAW", None)  # stacks with a raw engine report (SHACL) expose it
            if raw:
                print("--- raw engine report (pyshacl, unmodified)")
                print(raw.rstrip())
            print(f"--- final output ({len(out)} violation(s))")
            print("\n".join(map(str, out)) or "NONE REPORTED")
            st = check.load(v)
            print(f"--- same defect seen at narrower scopes on page {page!r}: "
                  f"local={len(check.check_local(st, page))}, neighborhood={len(check.check_neighborhood(st, page))}")
            print()


if __name__ == "__main__":
    main()
