"""The view generator (M6): the data of each view, built once for every front end.

    scat_kg.fingerprint("dry-july")      # a narrative's nodes, edges and rule-4 candidates; none: every narrative
    scat_kg.edge_table("holds")          # every edge of one type
    scat_kg.layered(["dry-july"])        # the union of fingerprints, as four layers; none: the whole vault
    scat_kg.trace("farmers", "down")     # what a node reaches, up, down or both

A view is data first: `to_dict()` is the document (`kind` `view`), `str(view)` is a short text, one line per node
or edge. The knowledge graph is derived on every call (`load`) and nothing is written. A view refuses, as a
`Result` that carries the problems, on a name that is unknown or ambiguous, an unknown edge type or direction, a
missing vault folder, on any error in the pages it draws, and on a row of a narrative it draws that tells no edge
(one refusal for each, naming the file and the row; the edge table and the trace draw every narrative); warnings do
not refuse. Relationship annotations
appear in no view. Names are plain text, never `[[links]]`.

Order is deterministic: layer order, then name; edges in graph order; narratives in path order.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from scat_kg.checks import Problem, check_vault
from scat_kg.contract import SCHEMA_VERSION
from scat_kg.graph import Edge, Graph, Node, load
from scat_kg.ops.result import Refusal, Result
from scat_kg.tbox import TBOX

DIRECTIONS = ("up", "down", "both")


@dataclass(frozen=True)
class Refused(Result):
    """A refusal that carries the problems that make it: the operation document's `problems` field."""

    problems: tuple[Problem, ...] = ()

    def to_dict(self) -> dict:
        out = super().to_dict()
        out["problems"] = [p.to_dict() for p in self.problems]
        return out

    def lines(self) -> list[str]:
        out = super().lines()
        for p in self.problems:
            out += ["  " + ln for ln in p.render().split("\n")]
        return out


def _refuse(
    op: str, subject: str, why: str, fix: str, problems: tuple[Problem, ...] = ()
) -> Refused:
    return Refused(op, refused=(Refusal(subject, why, fix),), problems=problems)


@dataclass(frozen=True)
class View:
    """What a view returns: the document's content, and the text the CLI prints."""

    operation: str  # "fingerprint", "edges", "layered" or "trace"
    data: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return True

    def to_dict(self) -> dict:
        return {
            "schema_version": SCHEMA_VERSION,
            "kind": "view",
            "operation": self.operation,
            "ok": True,
            **self.data,
        }

    def __str__(self) -> str:
        return "\n".join(_TEXT[self.operation](self.data))

    __repr__ = __str__


# ---------------------------------------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------------------------------------


def _node(n: Node) -> dict:
    return {"name": n.name, "type": n.type, "status": n.status}


def _edge(e: Edge) -> dict:
    return {
        "type": e.type,
        "from": e.from_node,
        "to": e.to_node,
        "narratives": list(e.narratives),
        "status": e.status,
    }


def _nodes(g: Graph, names) -> list[Node]:
    """The nodes of these names, in layer order then name."""
    want = set(names)
    return [n for ns in g.nodes.values() for n in ns if n.name in want]


def _check(op: str, g: Graph, narratives, nodes, edges) -> Refused | None:
    """Refuse on an error in a page drawn: the narratives, the nodes, and the narratives that tell the edges."""
    paths = {n.path for n in nodes}
    names = set(narratives) | {x for e in edges for x in e.narratives}
    paths |= {n.path for n in g.narratives if n.name in names}
    errors = tuple(p for p in check_vault(g.vault).errors if p.file in paths)
    if not errors:
        return None
    files = sorted({p.file for p in errors})
    return _refuse(
        op,
        ", ".join(files),
        f"{len(errors)} error(s) in the pages this view draws",
        "fix the problems below, then run this again",
        errors,
    )


def _skipped(op: str, g: Graph, names) -> Refused | None:
    """Refuse when a row of a narrative drawn tells no edge: one refusal for each such row."""
    names = set(names)
    rows = [k for k in g.skipped if k.narrative in names]
    if not rows:
        return None
    return Refused(
        op,
        refused=tuple(
            Refusal(
                f"{k.path} row {k.row}",
                k.reason,
                k.fix or f"fix the row (`scat check {k.path}` says how), then run this again",
            )
            for k in rows
        ),
    )


def _drawn(op: str, g: Graph, narratives, nodes, edges, scope) -> Refused | None:
    """The refusals of a view: an error in a page drawn first, else a skipped row in the narratives of `scope`."""
    return _check(op, g, narratives, nodes, edges) or _skipped(op, g, scope)


def _open(op: str, root: str | Path) -> tuple[Graph | None, Refused | None]:
    g = load(root)
    if g.refusal is not None:
        return None, Refused(op, refused=(g.refusal,))
    return g, None


def _page_named(op: str, g: Graph, name: str, kind: str) -> Refused | None:
    """Refuse when `name` is not exactly one page of this kind (`narrative` or `node`)."""
    pages = g.vault.by_name.get(name, ())
    if len(pages) > 1:
        paths = ", ".join(p.path for p in pages)
        return _refuse(
            op,
            name,
            f"more than one page has this name: {paths}",
            "rename one of the pages, then run this again",
        )
    found = g.narrative(name) is not None if kind == "narrative" else g.node(name) is not None
    if not found:
        return _refuse(
            op,
            name,
            f"no {kind} has this name",
            "give the name of a page (the file name without `.md`) that is a "
            + ("narrative" if kind == "narrative" else "group, concern, affordance or technology"),
        )
    return None


def _text(op: str, value: object, what: str) -> Refused | None:
    """Refuse a value that is not a string: a name, an edge type or a direction is always text."""
    if isinstance(value, str):
        return None
    return _refuse(op, repr(value), f"{what} must be a string", f"pass {what} as a string")


def fingerprint(narrative: str | None = None, *, root: str | Path = ".") -> View | Result:
    """A narrative's fingerprint: its nodes, the edges its rows tell, and its rule-4 candidates.

    With no name: the fingerprint of every narrative, in path order.
    """
    op = "fingerprint"
    g, bad = _open(op, root)
    if bad:
        return bad
    if narrative is not None:
        bad = _text(op, narrative, "a narrative name") or _page_named(op, g, narrative, "narrative")
        if bad:
            return bad
        chosen = [g.narrative(narrative)]
    else:
        chosen = list(g.narratives)
    by_key = {e.key: e for e in g.edges}
    items, nodes, edges = [], set(), []
    for nar in chosen:
        es = [by_key[k] for k in nar.edges]
        items.append(
            {
                "name": nar.name,
                "kind": nar.kind,
                "status": nar.status,
                "nodes": [_node(n) for n in _nodes(g, nar.nodes)],
                "edges": [_edge(e) for e in es],
                "candidates": [
                    {"type": c.type, "from": c.from_node, "to": c.to_node}
                    for c in g.candidates
                    if c.narrative == nar.name
                ],
            }
        )
        nodes |= set(nar.nodes)
        edges += es
    names = [n.name for n in chosen]
    bad = _drawn(op, g, names, _nodes(g, nodes), edges, names)
    return bad or View(op, {"narratives": items})


def edge_table(type: str, *, root: str | Path = ".") -> View | Result:
    """Every edge of one type (`holds`, `addressed-by`, `provided-by`), in graph order."""
    op = "edges"
    if bad := _text(op, type, "an edge type"):
        return bad
    if type not in TBOX.edge_types:
        return _refuse(
            op,
            type,
            "this is not an edge type",
            f"use one of: {', '.join(TBOX.edge_types)}",
        )
    g, bad = _open(op, root)
    if bad:
        return bad
    et = TBOX.edge_types[type]
    rows = [e for e in g.edges if e.type == type]
    ends = {x for e in rows for x in (e.from_node, e.to_node)}
    bad = _drawn(op, g, [], _nodes(g, ends), rows, [n.name for n in g.narratives])
    return bad or View(
        op,
        {
            "edge_type": type,
            "from_layer": et.from_type,
            "to_layer": et.to_type,
            "rows": [_edge(e) for e in rows],
        },
    )


def layered(narratives: list[str] | None = None, *, root: str | Path = ".") -> View | Result:
    """The union of the fingerprints of the named narratives (none: every narrative), as four layers."""
    op = "layered"
    if narratives is not None and not (
        isinstance(narratives, list | tuple) and all(isinstance(n, str) for n in narratives)
    ):
        return _refuse(
            op,
            repr(narratives),
            "narratives must be a list of narrative names",
            'pass a list of narrative names, for example `["dry-july"]`, or nothing for every narrative',
        )
    g, bad = _open(op, root)
    if bad:
        return bad
    if narratives is None:
        chosen = list(g.narratives)
    else:
        for name in narratives:
            bad = _page_named(op, g, name, "narrative")
            if bad:
                return bad
        chosen = [n for n in g.narratives if n.name in set(narratives)]
    keys = {k for n in chosen for k in n.edges}
    edges = [e for e in g.edges if e.key in keys]
    nodes = _nodes(g, {x for n in chosen for x in n.nodes})
    names = [n.name for n in chosen]
    bad = _drawn(op, g, names, nodes, edges, names)
    return bad or View(
        op,
        {
            "narratives": names,
            "nodes": {layer: [_node(n) for n in nodes if n.type == layer] for layer in TBOX.layers},
            "edges": [_edge(e) for e in edges],
        },
    )


def trace(node: str, direction: str = "both", *, root: str | Path = ".") -> View | Result:
    """Follow edges from a node up (toward groups), down (toward technologies) or both; the node itself is left out."""
    op = "trace"
    if bad := _text(op, direction, "a direction") or _text(op, node, "a node name"):
        return bad
    if direction not in DIRECTIONS:
        return _refuse(
            op, direction, "this is not a direction", f"use one of: {', '.join(DIRECTIONS)}"
        )
    g, bad = _open(op, root)
    if bad:
        return bad
    bad = _page_named(op, g, node, "node")
    if bad:
        return bad
    walked: dict[Any, Edge] = {}

    def walk(up: bool) -> set[str]:
        seen, todo = set(), [node]
        while todo:
            here = todo.pop()
            for e in g.edges:
                near, far = (e.to_node, e.from_node) if up else (e.from_node, e.to_node)
                if near == here:
                    walked[e.key] = e
                    if far not in seen:
                        seen.add(far)
                        todo.append(far)
        return seen

    ups = walk(True) if direction in ("up", "both") else set()
    downs = walk(False) if direction in ("down", "both") else set()
    edges = [e for e in g.edges if e.key in walked]
    shown = _nodes(g, ups | downs | {node})
    bad = _drawn(op, g, [], shown, edges, [n.name for n in g.narratives])
    return bad or View(
        op,
        {
            "node": node,
            "direction": direction,
            "up": [_node(n) for n in _nodes(g, ups)],
            "down": [_node(n) for n in _nodes(g, downs)],
            "edges": [_edge(e) for e in edges],
        },
    )


# ---------------------------------------------------------------------------------------------------------
# Text: one line per node or edge, grouped by layer
# ---------------------------------------------------------------------------------------------------------


def _node_line(n: dict) -> str:
    return f"    {n['name']} [{n['status']}]"


def _edge_line(e: dict) -> str:
    told = ", ".join(e["narratives"])
    return f"    {e['type']}: {e['from']} -> {e['to']} [{e['status']}; told by {told}]"


def _layer_lines(nodes: list[dict]) -> list[str]:
    out = []
    for layer in TBOX.layers:
        mine = [n for n in nodes if n["type"] == layer]
        if mine:
            out += [f"  {layer}", *map(_node_line, mine)]
    return out


def _text_fingerprint(d: dict) -> list[str]:
    out = []
    for n in d["narratives"]:
        says = ", ".join(x for x in (n["kind"], n["status"]) if x)
        out.append(f"fingerprint {n['name']} ({says})")
        out += _layer_lines(n["nodes"])
        if n["edges"]:
            out += ["  edges", *map(_edge_line, n["edges"])]
        if n["candidates"]:
            out.append("  candidates (linked, no row)")
            out += [f"    {c['type']}: {c['from']} -> {c['to']}" for c in n["candidates"]]
    return out or ["fingerprint: no narratives"]


def _text_edges(d: dict) -> list[str]:
    out = [f"edges {d['edge_type']} ({d['from_layer']} -> {d['to_layer']}): {len(d['rows'])}"]
    return out + [_edge_line(e) for e in d["rows"]]


def _text_layered(d: dict) -> list[str]:
    out = ["layered view of " + (", ".join(d["narratives"]) or "no narratives")]
    for layer in TBOX.layers:
        if d["nodes"][layer]:
            out += [f"  {layer}", *map(_node_line, d["nodes"][layer])]
    if d["edges"]:
        out += ["  edges", *map(_edge_line, d["edges"])]
    return out


def _text_trace(d: dict) -> list[str]:
    out = [f"trace {d['node']} ({d['direction']})"]
    for side in ("up", "down"):
        if d[side]:
            out += [f" {side}", *_layer_lines(d[side])]
    if d["edges"]:
        out += ["  edges", *map(_edge_line, d["edges"])]
    return out


_TEXT = {
    "fingerprint": _text_fingerprint,
    "edges": _text_edges,
    "layered": _text_layered,
    "trace": _text_trace,
}
