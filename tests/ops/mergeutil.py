"""Helpers for the merge and split-plan tests: copies of the node-page vaults, tree hashes, and the graph under a rename."""

import hashlib
import shutil
from pathlib import Path

import scat_kg

REPO = Path(__file__).parents[2]
VAULTS = REPO / "research" / "node-pages" / "vault"
RANGE = REPO / "research" / "range" / "koi" / "vault"
MODES = ("disallowed", "optional", "required")
SOURCES = {**{m: VAULTS / m for m in MODES}, "range": RANGE}

# (a, b) that merge cleanly: the node-page vaults (in all three modes), and the range vault
CLEAN = ("right-to-be-forgotten", "data-retention")  # a done narrative changes
WITH_BODY = ("forum-bot", "scheduler")  # a has a body
RANGE_CLEAN = ("closing-the-loop", "requisite-variety")
DUPLICATE_SEED = ("weekly-digest", "digest-email")


def tree(root: Path) -> dict[str, str]:
    """Every file under root: its path and the hash of its bytes."""
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def copy_of(source: str, tmp_path: Path) -> Path:
    dest = tmp_path / "vault"
    shutil.copytree(SOURCES[source], dest)
    return dest


def image(g, a: str, b: str, renamed: bool):
    """Edges with their tellings, and the fingerprints, with `a` read as `b` when `renamed`."""

    def r(n):
        return b if renamed and n == a else n

    edges: dict = {}
    for e in g.edges:
        edges.setdefault((e.type, r(e.from_node), r(e.to_node)), set()).update(
            t.narrative for t in e.tellings
        )
    fps = {
        n.name: (
            {r(x) for x in n.nodes},
            {(k.type, r(k.from_node), r(k.to_node)) for k in n.edges},
        )
        for n in g.narratives
    }
    nodes = {r(n.name) for ns in g.nodes.values() for n in ns}
    return edges, fps, nodes


def assert_graph_equal(before, root: Path, a: str, b: str):
    after = scat_kg.load(root)
    assert image(before, a, b, True) == image(after, a, b, False)
