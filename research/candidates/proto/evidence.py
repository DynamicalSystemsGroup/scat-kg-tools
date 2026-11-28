"""RS8 prototype (spike branch only): what the account links, and which candidates carry evidence.

A candidate carries evidence when the account (the body outside the `Edges told` section) links both its nodes.
"""

import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from scat_kg import graph
from scat_kg.graph import _headings
from scat_kg.tbox import TBOX
from scat_kg.vault import fenced_lines

ROOT = Path(__file__).resolve().parents[3]
VAULTS = {
    "examples": ROOT / "contracts/examples",
    "lab": ROOT / "research/range/koi/vault",
}


def fixture_vault() -> Path:
    """The contract examples plus the small fixtures, in a temporary folder."""
    dst = Path(tempfile.mkdtemp(prefix="rs8-fx-")) / "vault"
    shutil.copytree(ROOT / "contracts/examples", dst)
    for f in (ROOT / "research/candidates/fixtures/narrative").glob("*.md"):
        shutil.copy(f, dst / "narrative" / f.name)
    return dst


def outside_table(g, nar) -> tuple[list[int], set[int], dict[int, int], set[int]]:
    """(the file lines of the body outside the `Edges told` section, those that hold text, each line's
    paragraph number, the lines that are list items)."""
    page = next(p for p in g.vault.pages if p.path == nar.path)
    lines = page.body.split("\n")
    fenced = fenced_lines(lines)
    heads = _headings(lines, fenced)
    drop = {i for i, _, _ in heads}  # headings are not text
    named = [h for h in heads if h[2].casefold() == TBOX.table.heading.casefold()]
    if named:
        start, level, _ = named[0]
        end = next((i for i, lv, _ in heads if i > start and lv <= level), len(lines))
        table = set(range(start, end))
    else:
        table = set()
    keep = [i for i in range(len(lines)) if i not in table]
    text = {i for i in keep if i not in drop and lines[i].strip()}
    base = page.body_line
    para, n = {}, 0
    for i in keep:
        if not lines[i].strip():
            n += 1
        else:
            para[base + i] = n
    items = {base + i for i in keep if re.match(r"\s*([-*+]|\d+[.)])\s", lines[i])}
    return [base + i for i in keep], {base + i for i in text}, para, items


@dataclass(frozen=True)
class Case:
    vault: str
    narrative: str
    kind: str | None
    nodes: int  # the fingerprint
    rows: int  # edges the narrative tells
    account_nodes: frozenset  # nodes the account links
    candidates: tuple  # graph.Candidate
    with_evidence: tuple  # the candidates whose two nodes the account links
    in_prose: (
        tuple  # of those, the ones whose two nodes are linked in lines that are not list items
    )
    same_para: (
        tuple  # of those, the ones whose two nodes are linked in one paragraph of the account
    )
    has_text: bool  # text outside the table (the flag as built is the opposite)

    @property
    def cause(self) -> str:
        if not self.candidates:
            return "no candidates"
        if not self.has_text:
            return "no account"
        if not self.account_nodes:
            return "prose, no links"
        if len(self.with_evidence) == len(self.candidates):
            return "prose links all"
        return "prose links some"


def cases(g, vault: str) -> list[Case]:
    out = []
    for nar in g.narratives:
        keep, text, para, items = outside_table(g, nar)
        keep = set(keep)
        mine = [l for l in nar.links if l.line in keep and l.target in set(nar.nodes)]
        acct = frozenset(l.target for l in mine)
        prose = frozenset(l.target for l in mine if l.line not in items)
        where = {}
        for l in mine:
            where.setdefault(l.target, set()).add(para[l.line])
        cands = tuple(c for c in g.candidates if c.narrative == nar.name)
        ev = tuple(c for c in cands if c.from_node in acct and c.to_node in acct)
        pr = tuple(c for c in ev if c.from_node in prose and c.to_node in prose)
        sp = tuple(c for c in ev if where[c.from_node] & where[c.to_node])
        out.append(
            Case(
                vault,
                nar.name,
                nar.kind,
                len(nar.nodes),
                len(nar.edges),
                acct,
                cands,
                ev,
                pr,
                sp,
                bool(text),
            )
        )
    return out


def load_all() -> dict[str, tuple]:
    roots = {**VAULTS, "fixtures": fixture_vault()}
    return {k: (graph.load(v), v) for k, v in roots.items()}
