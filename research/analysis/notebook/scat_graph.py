"""Load a SCAT vault through scat_kg and build a typed graph for analysis (RS2 spike).

The only reach into scat_kg beyond the public API is `scat_kg.vault.read_vault` (there is no public loader).
Nothing here parses frontmatter: pages arrive as `scat_kg.vault.Page` objects with their links already read.
"""

from dataclasses import dataclass, field
from pathlib import Path

import networkx as nx
import pandas as pd
from scat_kg.vault import read_vault  # internal, but scat_kg: the one thing the notebook reaches for

LAYERS = ["stakeholder-group", "concern", "affordance", "technology"]
LAYER_LABEL = {"stakeholder-group": "group", "concern": "concern", "affordance": "affordance", "technology": "technology"}
# relation page type -> (field of the source node, field of the target node)
RELATIONS = {"heldby": ("group", "concern"), "addresses": ("concern", "affordance"), "attributes": ("affordance", "technology")}
RECORD_TYPES = ["scenario-coded", "architecture-coded"]


@dataclass
class ScatGraph:
    """G: directed typed graph (group -> concern -> affordance -> technology), each edge with `kind` and `page`.
    conflicts: undirected graph over concerns (symmetric closure); edge attr `declared_by` lists the declaring concerns.
    records: one row per coded scenario/architecture record (provenance), with the nodes it names.
    """

    G: nx.DiGraph
    conflicts: nx.Graph
    records: pd.DataFrame
    status_counts: dict = field(default_factory=dict)
    dangling: list = field(default_factory=list)

    def nodes(self, layer):
        return sorted(n for n, d in self.G.nodes(data=True) if d["layer"] == layer)

    def summary(self):
        rows = [(LAYER_LABEL[l], len(self.nodes(l))) for l in LAYERS]
        rows += [(f"{k} edges", sum(1 for *_, d in self.G.edges(data=True) if d["kind"] == k)) for k in RELATIONS]
        rows += [("conflict pairs", self.conflicts.number_of_edges()), ("coded records", len(self.records))]
        return pd.DataFrame(rows, columns=["item", "count"]).set_index("item")


def _targets(page, key):
    return [l.target for l in page.fm_links.get(key, ())]


def load(root, statuses=None):
    """Read the vault at `root` and return a ScatGraph. `statuses`: keep only pages with these status values."""
    vault = read_vault(Path(root))
    keep = lambda p: statuses is None or p.status in statuses
    G, C = nx.DiGraph(), nx.Graph()
    status_counts, dangling = {}, []
    for p in vault.pages:
        status_counts[p.status] = status_counts.get(p.status, 0) + 1
    for p in vault.pages:
        if p.type in LAYERS and keep(p):
            G.add_node(p.name, layer=p.type, title=p.fields.get("title", p.name), status=p.status)
    for p in vault.pages:
        if p.type in RELATIONS and keep(p):
            a, b = RELATIONS[p.type]
            (s,), (t,) = _targets(p, a), _targets(p, b)  # one link per field on a relation page
            if s in G and t in G:
                G.add_edge(s, t, kind=p.type, page=p.name)
            else:
                dangling.append(p.name)
    for n in G.nodes:
        if G.nodes[n]["layer"] == "concern":
            C.add_node(n)
    for p in vault.pages:
        if p.type == "concern" and p.name in G:
            for t in _targets(p, "conflicts"):
                if t in G:
                    if C.has_edge(p.name, t):
                        C[p.name][t]["declared_by"].append(p.name)
                    else:
                        C.add_edge(p.name, t, declared_by=[p.name])
    rec = []
    for p in vault.pages:
        if p.type in RECORD_TYPES and keep(p):
            rec.append(dict(record=p.name, kind=p.type.split("-")[0], raw=_targets(p, "raw"),
                            groups=_targets(p, "groups"), concerns=_targets(p, "concerns"),
                            affordances=_targets(p, "affordances"), technologies=_targets(p, "technologies")))
    cols = ["record", "kind", "raw", "groups", "concerns", "affordances", "technologies"]
    return ScatGraph(G, C, pd.DataFrame(rec, columns=cols), status_counts, dangling)


# ---- analyses: each returns data frames or graphs; plotting stays in the notebook ----------------------

def traceability(sg):
    """Per concern: who holds it, what addresses it, what technologies stand behind those affordances."""
    G = sg.G
    rows = []
    for c in sg.nodes("concern"):
        holders = sorted(G.predecessors(c))
        affs = sorted(G.successors(c))
        techs = sorted({t for a in affs for t in G.successors(a)})
        rows.append(dict(concern=c, holders=holders, n_holders=len(holders), affordances=affs, n_affordances=len(affs),
                         technologies=techs, n_technologies=len(techs),
                         chain=("complete" if techs else "addressed, no technology" if affs else "unaddressed")))
    return pd.DataFrame(rows).set_index("concern")


def group_coverage(sg):
    """Per group: how many of its concerns reach each depth of the chain."""
    tr = traceability(sg)
    rows = []
    for g in sg.nodes("stakeholder-group"):
        cs = sorted(sg.G.successors(g))
        counts = tr.loc[cs, "chain"].value_counts() if cs else pd.Series(dtype=int)
        rows.append(dict(group=g, concerns_held=len(cs), **{k: int(counts.get(k, 0)) for k in ["complete", "addressed, no technology", "unaddressed"]}))
    return pd.DataFrame(rows).set_index("group")


def orphans(sg):
    """Nodes with no edge to the neighbouring layer(s) of the chain."""
    G = sg.G
    return {
        "groups holding no concern": [g for g in sg.nodes("stakeholder-group") if G.out_degree(g) == 0],
        "concerns held by no group": [c for c in sg.nodes("concern") if not any(G.nodes[p]["layer"] == "stakeholder-group" for p in G.predecessors(c))],
        "affordances addressing no concern": [a for a in sg.nodes("affordance") if not any(G.nodes[p]["layer"] == "concern" for p in G.predecessors(a))],
        "technologies attributed to no affordance": [t for t in sg.nodes("technology") if G.in_degree(t) == 0],
    }


def projection(sg, layer_keep, via):
    """Weighted one-mode projection: nodes of `layer_keep` linked by shared neighbours in layer `via` (weight = count shared)."""
    U = sg.G.to_undirected()
    B = nx.Graph()
    for n in sg.nodes(layer_keep):
        B.add_node(n)
    for v in sg.nodes(via):
        nb = sorted(x for x in U[v] if U.nodes[x]["layer"] == layer_keep)
        for i, a in enumerate(nb):
            for b in nb[i + 1:]:
                w = B[a][b]["weight"] + 1 if B.has_edge(a, b) else 1
                B.add_edge(a, b, weight=w)
    return B


def tension(sg):
    """Conflict pairs with their holders; groups holding both sides; group pairs on opposite sides."""
    G, C = sg.G, sg.conflicts
    holders = lambda c: sorted(p for p in G.predecessors(c) if G.nodes[p]["layer"] == "stakeholder-group")
    pairs, both, opposite = [], [], []
    for a, b in sorted(tuple(sorted(e)) for e in C.edges):
        ha, hb = holders(a), holders(b)
        pairs.append(dict(concern_a=a, concern_b=b, declared_by=", ".join(C[a][b]["declared_by"]), holders_a=ha, holders_b=hb))
        for g in sorted(set(ha) & set(hb)):
            both.append(dict(group=g, concern_a=a, concern_b=b))
        for x in ha:
            for y in hb:
                if x != y:
                    opposite.append(dict(group_x=x, concern_x=a, group_y=y, concern_y=b))
    one_sided = [(a, b) for a, b in C.edges if len(C[a][b]["declared_by"]) == 1]
    return pd.DataFrame(pairs), pd.DataFrame(both), pd.DataFrame(opposite), len(one_sided)


def carriage(sg):
    """For affordances and technologies: concerns carried (reached upstream), groups behind them, and degrees."""
    G = sg.G
    rows = []
    for n, d in G.nodes(data=True):
        if d["layer"] in ("affordance", "technology"):
            anc = nx.ancestors(G, n)
            rows.append(dict(node=n, layer=d["layer"],
                             concerns_carried=sum(G.nodes[x]["layer"] == "concern" for x in anc),
                             groups_behind=sum(G.nodes[x]["layer"] == "stakeholder-group" for x in anc),
                             degree=G.degree(n)))
    df = pd.DataFrame(rows).set_index("node")
    bc = nx.betweenness_centrality(G.to_undirected())
    df["betweenness"] = [round(bc[n], 3) for n in df.index]
    return df


def communities(sg):
    """Two community algorithms (greedy modularity, Louvain) on the undirected typed graph (isolates dropped); returns {name: list of sets}."""
    from networkx.algorithms import community as nxc
    U = sg.G.to_undirected()
    U.remove_nodes_from([n for n in list(U) if U.degree(n) == 0])
    return U, {"greedy modularity": [set(c) for c in nxc.greedy_modularity_communities(U)],
               "louvain (seed 1)": [set(c) for c in nxc.louvain_communities(U, seed=1)]}


def same_partition_pairs(parts_a, parts_b):
    """Share of node pairs placed together by both algorithms among pairs placed together by either (Jaccard on pairs)."""
    def pairs(parts):
        return {frozenset((a, b)) for p in parts for a in p for b in p if a < b}
    pa, pb = pairs(parts_a), pairs(parts_b)
    return len(pa & pb) / len(pa | pb) if pa | pb else 1.0
