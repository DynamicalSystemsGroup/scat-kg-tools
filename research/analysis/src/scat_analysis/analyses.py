"""The analyses: one function each, returning a tidy DataFrame or plain data.

Every function describes structure. None orders stories, groups or architectures as better or worse, and none
returns a rank or a score column; rows come out in alphabetical order. Each docstring says what the result reads
as and what it does NOT mean.
"""

import networkx as nx
import pandas as pd

from .graph import RECORD_ROLES, ScatGraph

CHAIN_STATES = ["complete", "addressed, no technology", "unaddressed"]


def _holders(sg, concern):
    return sorted(p for p in sg.G.predecessors(concern) if sg.G.nodes[p]["layer"] == "stakeholder-group")


# ---- 1. traceability and gaps ----------------------------------------------------------------------------

def traceability(sg: ScatGraph) -> pd.DataFrame:
    """Per concern: who holds it, which affordances address it, which technologies those are attributed to.

    Columns: holders, n_holders, affordances, n_affordances, technologies, n_technologies, chain
    (`complete`, `addressed, no technology` or `unaddressed`). Index: concern.

    Reads as: how far each concern is followed in what has been coded.
    Does NOT mean: that an unaddressed concern is neglected or unmet; the vault may simply not be coded further.
    """
    G = sg.G
    rows = []
    for c in sg.nodes("concern"):
        holders = _holders(sg, c)
        affs = sorted(G.successors(c))
        techs = sorted({t for a in affs for t in G.successors(a)})
        rows.append(dict(concern=c, holders=holders, n_holders=len(holders), affordances=affs, n_affordances=len(affs),
                         technologies=techs, n_technologies=len(techs),
                         chain=CHAIN_STATES[0] if techs else CHAIN_STATES[1] if affs else CHAIN_STATES[2]))
    cols = ["concern", "holders", "n_holders", "affordances", "n_affordances", "technologies", "n_technologies", "chain"]
    return pd.DataFrame(rows, columns=cols).set_index("concern")


def group_coverage(sg: ScatGraph) -> pd.DataFrame:
    """Per group: how many of its concerns reach each depth of the chain (columns: concerns_held, then one per chain state).

    Reads as: a group whose concerns are all `unaddressed` holds concerns no recorded affordance addresses.
    Does NOT mean: that the group is neglected, or that more `complete` concerns means a group is better served.
    """
    tr = traceability(sg)
    rows = []
    for g in sg.nodes("stakeholder-group"):
        cs = sorted(sg.G.successors(g))
        counts = tr.loc[cs, "chain"].value_counts() if cs else pd.Series(dtype=int)
        rows.append(dict(group=g, concerns_held=len(cs), **{k: int(counts.get(k, 0)) for k in CHAIN_STATES}))
    return pd.DataFrame(rows, columns=["group", "concerns_held", *CHAIN_STATES]).set_index("group")


def gaps(sg: ScatGraph) -> dict:
    """Nodes with no link to the neighbouring layer of the chain, as {label: [names]} (empty list: none).

    Labels: groups holding no concern; concerns held by no group; concerns no affordance addresses; affordances
    addressing no concern; affordances attributed to no technology; technologies attributed to no affordance;
    groups whose concerns are all unaddressed.

    Reads as: where the coded chain stops.
    Does NOT mean: a defect. A gap is in what has been coded, not in the real system.
    """
    G, tr = sg.G, traceability(sg)
    gc = group_coverage(sg)
    layer = lambda n: G.nodes[n]["layer"]
    return {
        "groups holding no concern": [g for g in sg.nodes("stakeholder-group") if G.out_degree(g) == 0],
        "concerns held by no group": [c for c in sg.nodes("concern") if not tr.loc[c, "n_holders"]],
        "concerns no affordance addresses": [c for c in sg.nodes("concern") if not tr.loc[c, "n_affordances"]],
        "affordances addressing no concern": [a for a in sg.nodes("affordance") if not any(layer(p) == "concern" for p in G.predecessors(a))],
        "affordances attributed to no technology": [a for a in sg.nodes("affordance") if G.out_degree(a) == 0],
        "technologies attributed to no affordance": [t for t in sg.nodes("technology") if G.in_degree(t) == 0],
        "groups whose concerns are all unaddressed": [g for g in gc.index if gc.loc[g, "concerns_held"] and gc.loc[g, "unaddressed"] == gc.loc[g, "concerns_held"]],
    }


# ---- 2. projections --------------------------------------------------------------------------------------

def projection(sg: ScatGraph, layer_keep: str, via: str) -> nx.Graph:
    """One-mode projection as a graph: nodes of `layer_keep` linked when they share a neighbour in layer `via` (edge `weight` = number shared)."""
    U = sg.G.to_undirected()
    B = nx.Graph()
    B.add_nodes_from(sg.nodes(layer_keep))
    for v in sg.nodes(via):
        nb = sorted(x for x in U[v] if U.nodes[x]["layer"] == layer_keep)
        for i, a in enumerate(nb):
            for b in nb[i + 1:]:
                B.add_edge(a, b, weight=B[a][b]["weight"] + 1 if B.has_edge(a, b) else 1)
    return B


def projections(sg: ScatGraph) -> pd.DataFrame:
    """Two one-mode views as one edge table: groups linked by shared concerns, concerns linked by shared affordances.

    Columns: projection, node_a, node_b, shared (how many), via (the shared nodes). Nodes with no edge do not appear;
    see `projection` for the graph, which keeps them.

    Reads as: two nodes of the same kind that reach a common node of the next kind.
    Does NOT mean: agreement. Groups sharing a concern may want it for opposite ends; a hub makes a clique of its neighbours.
    """
    rows = []
    for name, keep, via in [("groups by shared concern", "stakeholder-group", "concern"),
                            ("concerns by shared affordance", "concern", "affordance")]:
        B = projection(sg, keep, via)
        for a, b in sorted(tuple(sorted(e)) for e in B.edges):
            shared = sorted(set(sg.G.successors(a)) & set(sg.G.successors(b)))
            rows.append(dict(projection=name, node_a=a, node_b=b, shared=B[a][b]["weight"], via=shared))
    return pd.DataFrame(rows, columns=["projection", "node_a", "node_b", "shared", "via"])


# ---- 3. tension ------------------------------------------------------------------------------------------

def tension(sg: ScatGraph) -> dict:
    """Declared conflicts and who stands where. Returns three tables.

    - `pairs`: concern_a, concern_b, declared_by, n_declarations, holders_a, holders_b (the symmetric closure: one row per pair).
    - `both_sides`: group, concern_a, concern_b (the group holds both ends of a pair).
    - `opposite_sides`: group_x, concern_x, group_y, concern_y (the groups hold opposite ends).
      One row per (group, concern, group, concern); the same two groups can recur across several conflicts,
      so count distinct unordered group pairs separately (synthetic vault: 14 rows, 8 distinct unordered group pairs).

    Reads as: where the vault says concerns pull against each other, and which groups sit at which end.
    Does NOT mean: a disagreement that has occurred, or a flaw. A group holding both sides carries a trade-off.
    Opposite sides are not adversaries; a concern with no conflict may just not have been compared.
    """
    C = sg.conflicts
    pairs, both, opposite = [], [], []
    for a, b in sorted(tuple(sorted(e)) for e in C.edges):
        ha, hb = _holders(sg, a), _holders(sg, b)
        decl = sorted(C[a][b]["declared_by"])
        pairs.append(dict(concern_a=a, concern_b=b, declared_by=", ".join(decl), n_declarations=len(decl), holders_a=ha, holders_b=hb))
        both += [dict(group=g, concern_a=a, concern_b=b) for g in sorted(set(ha) & set(hb))]
        opposite += [dict(group_x=x, concern_x=a, group_y=y, concern_y=b) for x in ha for y in hb if x != y]
    return {"pairs": pd.DataFrame(pairs, columns=["concern_a", "concern_b", "declared_by", "n_declarations", "holders_a", "holders_b"]),
            "both_sides": pd.DataFrame(both, columns=["group", "concern_a", "concern_b"]),
            "opposite_sides": pd.DataFrame(opposite, columns=["group_x", "concern_x", "group_y", "concern_y"])}


# ---- 4. centrality and brokerage -------------------------------------------------------------------------

def centrality(sg: ScatGraph) -> pd.DataFrame:
    """For each affordance and technology: concerns_carried (every concern upstream), groups_behind, degree, betweenness.

    Betweenness is the share of shortest paths between other nodes that pass through the node, on the undirected
    typed graph, rounded to 3 places. Rows are alphabetical.

    Reads as: where recorded concerns concentrate (a change there touches many of them) and which nodes sit between
    otherwise separate parts of the graph.
    Does NOT mean: importance, quality or risk. The counts depend on how finely concerns were written and how many
    records were coded. Do not compare counts across vaults.
    """
    G = sg.G
    bc = nx.betweenness_centrality(G.to_undirected())
    rows = []
    for n, d in sorted(G.nodes(data=True)):
        if d["layer"] in ("affordance", "technology"):
            anc = nx.ancestors(G, n)
            rows.append(dict(node=n, layer=d["layer"],
                             concerns_carried=sum(G.nodes[x]["layer"] == "concern" for x in anc),
                             groups_behind=sum(G.nodes[x]["layer"] == "stakeholder-group" for x in anc),
                             degree=G.degree(n), betweenness=round(bc[n], 3)))
    return pd.DataFrame(rows, columns=["node", "layer", "concerns_carried", "groups_behind", "degree", "betweenness"]).set_index("node")


# ---- 5. communities --------------------------------------------------------------------------------------

def communities(sg: ScatGraph, seed: int = 1) -> pd.DataFrame:
    """Cluster the undirected typed graph (isolated nodes dropped) with two standard algorithms.

    Columns: node, layer, greedy_modularity, louvain (cluster numbers, numbered by each cluster's first member
    in alphabetical order, so the table is the same on every run for the same vault and `seed`).

    Reads as: sets of nodes more densely linked to each other than to the rest.
    Does NOT mean: teams, workstreams or architectures, or a better grouping. Where the two algorithms agree on few
    pairs (see `community_agreement`) the graph is not sharply clustered and any partition is held loosely.
    """
    from networkx.algorithms import community as nxc
    U = sg.G.to_undirected()
    U.remove_nodes_from([n for n in list(U) if U.degree(n) == 0])
    parts = {"greedy_modularity": [set(c) for c in nxc.greedy_modularity_communities(U)],
             "louvain": [set(c) for c in nxc.louvain_communities(U, seed=seed)]}
    labels = {}
    for name, ps in parts.items():
        for i, c in enumerate(sorted(ps, key=min)):
            labels.update({(name, n): i for n in c})
    rows = [dict(node=n, layer=U.nodes[n]["layer"], greedy_modularity=labels[("greedy_modularity", n)], louvain=labels[("louvain", n)])
            for n in sorted(U)]
    return pd.DataFrame(rows, columns=["node", "layer", "greedy_modularity", "louvain"])


def community_agreement(comm: pd.DataFrame) -> float:
    """Share of node pairs put together by both algorithms among pairs put together by either (Jaccard on pairs; 1.0 if none)."""
    def pairs(col):
        out = set()
        for _, grp in comm.groupby(col):
            ns = sorted(grp["node"])
            out |= {(a, b) for i, a in enumerate(ns) for b in ns[i + 1:]}
        return out
    pa, pb = pairs("greedy_modularity"), pairs("louvain")
    return len(pa & pb) / len(pa | pb) if pa | pb else 1.0


# ---- 6. provenance ---------------------------------------------------------------------------------------

def provenance(sg: ScatGraph) -> pd.DataFrame:
    """The coded records as a long table: record, kind (scenario or architecture), role (groups, concerns, affordances, technologies), node.

    Records are hyperedges (one record, many nodes); they are not turned into pairwise graph edges, which nobody wrote.

    Reads as: which nodes each coded record names.
    Does NOT mean: that a record naming more nodes is a fuller or better account. Records differ in what they were written to cover.
    """
    rows = [dict(record=r.record, kind=r.kind, role=role, node=n)
            for r in sg.records.itertuples() for role in RECORD_ROLES for n in getattr(r, role)]
    return pd.DataFrame(rows, columns=["record", "kind", "role", "node"]).sort_values(["record", "role", "node"], ignore_index=True)


def provenance_matrix(sg: ScatGraph) -> pd.DataFrame:
    """Records (rows) by concerns (columns), 1 where the record names the concern. Concerns no record names are all-zero columns."""
    cs = sg.nodes("concern")
    rows = {r.record: [int(c in r.concerns) for c in cs] for r in sg.records.sort_values("record").itertuples()}
    return pd.DataFrame.from_dict(rows, orient="index", columns=cs)


def conflict_records(sg: ScatGraph) -> pd.DataFrame:
    """Records that name both ends of a declared conflict (columns: record, concern_a, concern_b).

    Reads as: where a declared tension surfaces in the coded evidence.
    Does NOT mean: that the tension was resolved or argued out in that record.
    """
    rows = [dict(record=r.record, concern_a=a, concern_b=b)
            for r in sg.records.sort_values("record").itertuples()
            for a, b in sorted(tuple(sorted(e)) for e in sg.conflicts.edges) if a in r.concerns and b in r.concerns]
    return pd.DataFrame(rows, columns=["record", "concern_a", "concern_b"])
