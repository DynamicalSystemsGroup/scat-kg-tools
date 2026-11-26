"""split-plan: what a coder must re-link to split one node page in two. A plan only: it writes nothing.

For each narrative (and node page) that links the page it gives every link (file, line) and, for a narrative, every
`Edges told` row that names the page. The coder assigns each narrative to the page or to a new page and edits by
hand. A contributor page is never listed. The plan does not refuse a group for the cap: it notes the cap.
"""

from dataclasses import dataclass
from pathlib import Path

from scat_kg.graph import load
from scat_kg.ops.common import open_vault
from scat_kg.ops.merge import NARRATIVE, error_refusals, linking_pages, resolve_node
from scat_kg.ops.result import Result, reports_mode

OP = "split-plan"


@dataclass(frozen=True)
class SplitPage:
    file: str
    name: str
    type: str
    status: str | None
    links: tuple[tuple[int, int], ...]  # (line, column) of each link
    rows: tuple[
        tuple[int, int, str], ...
    ]  # (row number, line, text) of each row that names the page

    def to_dict(self) -> dict:
        return {
            "file": self.file,
            "name": self.name,
            "type": self.type,
            "status": self.status,
            "links": [{"line": ln, "column": c} for ln, c in self.links],
            "rows": [{"row": n, "line": ln, "text": t} for n, ln, t in self.rows],
        }


@dataclass(frozen=True)
class SplitPlan(Result):
    node: str = ""
    node_type: str = ""
    pages: tuple[SplitPage, ...] = ()

    def to_dict(self) -> dict:
        out = super().to_dict()
        if self.ok:
            out["node"] = self.node
            out["node_type"] = self.node_type
            out["pages"] = [p.to_dict() for p in self.pages]
        return out

    def lines(self) -> list[str]:
        if self.refused:
            return super().lines()
        links = sum(len(p.links) for p in self.pages)
        rows = sum(len(p.rows) for p in self.pages)
        out = [
            (
                f"split plan for `{self.node}` ({self.node_type}): {len(self.pages)} "
                f"page{'' if len(self.pages) == 1 else 's'}, {links} link{'' if links == 1 else 's'}, "
                f"{rows} row{'' if rows == 1 else 's'} to re-link; nothing is written"
            )
        ]
        for p in self.pages:
            at = ", ".join(str(ln) for ln, _ in p.links)
            out.append(f"  {p.file} ({p.type}, {p.status}): links at line {at}")
            out += [f"    row {n}, line {ln}: {t.strip()}" for n, ln, t in p.rows]
        out += [f"note: {n}" for n in self.notes]
        return out


@reports_mode
def split_plan(a: str, *, root: str | Path = ".") -> Result:
    """The places to re-link to split node page `a`. Writes nothing."""
    vault, bad = open_vault(OP, root)
    if bad:
        return bad
    page, refusal = resolve_node(OP, vault, a)
    if refusal:
        return Result(OP, refused=(refusal,))
    pages, contributors = linking_pages(
        vault, page.name
    )  # contributor pages are never listed as places
    if bad := error_refusals(vault, {page.path} | {p.path for p in pages}):
        return Result(OP, refused=tuple(bad))
    graph = load(root)
    narratives = {n.path: n for n in graph.narratives}
    out = []
    for p in pages:
        n = narratives.get(p.path)
        rows = tuple(
            (r.n, r.line, r.text)
            for r in (n.rows if n else ())
            if any(page.name in c.links for c in r.cells)
        )
        links = tuple((link.line, link.column) for link in p.links if link.target == page.name)
        out.append(SplitPage(p.path, p.name, p.type, p.fields.get("status"), links, rows))
    notes = [
        (
            f"you assign each narrative to `{page.name}` or to a new page: make the new page with "
            f"`scat stub <name> --type {page.type}`, then edit each link and row by hand"
        )
    ]
    people = sorted({c.path for c, _ in contributors})
    if people:
        notes.append(
            "a contributor page links this page and is never changed by the tool: "
            + ", ".join(people)
        )
    done = [p.name for p in out if p.type == NARRATIVE and p.status == "done"]
    if done:
        notes.append(
            "narratives that are `done` are yours to reopen before you edit them: "
            + ", ".join(done)
        )
    if page.type == "group" and vault.config.cap is not None:
        have = len(vault.of_type("group"))
        notes.append(
            f"the vault allows {vault.config.cap} groups and has {have}; a new group page makes "
            f"{have + 1}"
            + (
                "; raise `stakeholder_group_cap` in `scat.toml` first"
                if have + 1 > vault.config.cap
                else ""
            )
        )
    return SplitPlan(OP, notes=tuple(notes), node=page.name, node_type=page.type, pages=tuple(out))
