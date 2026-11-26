"""Throwaway: does a draft paste from the narratives? Shares of the draft's 5-word shingles found verbatim in any
narrative of the vault (links stripped to their shown text). Run: uv run python copycheck.py <vault> <draft.md>..."""
import re, sys
from pathlib import Path
def words(t):
    t = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", t); t = re.sub(r"\[\[([^\]]*)\]\]", r"\1", t)
    return re.findall(r"[a-z0-9']+", t.lower())
def shingles(w, n=5): return {tuple(w[i:i+n]) for i in range(len(w) - n + 1)}
vault = Path(sys.argv[1])
corp = set()
for p in vault.glob("narrative/*.md"): corp |= shingles(words(p.read_text().split("---", 2)[2]))
for d in sys.argv[2:]:
    body = Path(d).read_text().split("---", 2)[2]
    sh = shingles(words(body)); hit = sh & corp
    print(f"{Path(d).name:35s} 5-word shingles verbatim in narratives: {len(hit)}/{len(sh)} = {len(hit)/max(1,len(sh)):.0%}")
