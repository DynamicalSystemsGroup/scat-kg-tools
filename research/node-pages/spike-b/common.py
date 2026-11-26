"""Shared helpers for the spike-b scripts (throwaway)."""

import itertools
import math
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

import scat_kg

REPO = Path(__file__).resolve().parents[3]
VAULTS = {
    "seeded": REPO / "research/node-pages/vault/disallowed",
    "range": REPO / "research/range/koi/vault",
}
SEEDS = {
    ("members-not-replying", "unanswered-direct-messages"): "synonym",
    ("weekly-digest", "digest-email"): "duplicate-row",
    ("data-retention", "data-retention-schedule"): "decoy",
}
HOMONYM = "community-members"
STOP = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "of",
    "to",
    "in",
    "on",
    "for",
    "with",
    "by",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "it",
    "its",
    "that",
    "this",
    "as",
    "at",
    "from",
    "their",
    "they",
    "them",
    "his",
    "her",
    "he",
    "she",
    "not",
    "but",
    "which",
    "who",
    "what",
    "when",
    "where",
    "how",
    "than",
    "then",
    "so",
    "such",
    "into",
    "out",
    "up",
    "one",
    "two",
    "also",
    "here",
    "there",
    "has",
    "have",
    "had",
    "can",
    "could",
    "would",
    "may",
    "more",
    "most",
    "only",
    "own",
    "same",
    "other",
    "no",
    "do",
    "does",
    "did",
    "if",
    "about",
    "over",
    "after",
    "before",
    "between",
    "both",
    "each",
    "across",
    "through",
}


def key(a, b):
    return tuple(sorted((a, b)))


def seed_label(a, b):
    for (x, y), lab in SEEDS.items():
        if key(x, y) == key(a, b):
            return lab
    return ""


def load(name):
    return scat_kg.load(VAULTS[name])


def jac(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


def toks(t):
    return [w for w in re.findall(r"[a-z]+", t.lower()) if w not in STOP and len(w) > 2]


def cos(a, b):
    num = sum(v * b.get(k, 0) for k, v in a.items())
    da = math.sqrt(sum(v * v for v in a.values()))
    db = math.sqrt(sum(v * v for v in b.values()))
    return num / (da * db) if da and db else 0.0


def nodes_of(g):
    return [n for ns in g.nodes.values() for n in ns]


def same_type_pairs(g):
    for ns in g.nodes.values():
        yield from itertools.combinations([n.name for n in ns], 2)


def signals(g):
    """Per node: narratives that link it, edge keys it sits in, adjacent nodes."""
    nar, edg, adj = defaultdict(set), defaultdict(set), defaultdict(set)
    for n in g.narratives:
        for x in n.nodes:
            nar[x].add(n.name)
    for e in g.edges:
        for me, other in ((e.from_node, e.to_node), (e.to_node, e.from_node)):
            edg[me].add((e.type, other, "out" if me == e.from_node else "in"))
            adj[me].add(other)
    return nar, edg, adj


def body(root, node):
    t = (Path(root) / node.path).read_text()
    return t.split("\n---\n", 1)[1] if "\n---\n" in t else ""


def desc(root, node):
    m = re.search(r'^description: "(.*)"$', (Path(root) / node.path).read_text(), re.MULTILINE)
    return m.group(1) if m else ""


def timed(label):
    t0 = time.perf_counter()
    return lambda: print(f"[runtime {label}: {time.perf_counter() - t0:.2f}s]", file=sys.stderr)


def vaults():
    return [(v, load(v)) for v in VAULTS]


sys.dont_write_bytecode = True
