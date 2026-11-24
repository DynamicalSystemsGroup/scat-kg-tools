"""Load a SCAT vault into a typed graph (networkx) for analysis.

The only reach into `scat_kg` beyond its public API is `scat_kg.vault.read_vault`: core has no public loader.
Nothing here parses frontmatter; pages arrive as `scat_kg.vault.Page` objects with their links already read.

The graph describes what has been coded. It is not a measurement of the real system, and nothing here
orders stories, groups or architectures as better or worse.
"""

from dataclasses import dataclass, field
from pathlib import Path

import networkx as nx
import pandas as pd
from scat_kg.vault import read_vault  # internal to scat_kg; the one thing this package reaches for

LAYERS = ["stakeholder-group", "concern", "affordance", "technology"]
LAYER_LABEL = {"stakeholder-group": "group", "concern": "concern", "affordance": "affordance", "technology": "technology"}
# relation page type -> (link field naming the source node, link field naming the target node)
RELATIONS = {"heldby": ("group", "concern"), "addresses": ("concern", "affordance"), "attributes": ("affordance", "technology")}
RECORD_TYPES = ["scenario-coded", "architecture-coded"]
RECORD_ROLES = ["groups", "concerns", "affordances", "technologies"]


@dataclass
class ScatGraph:
    """A vault read as a graph.

    G: directed typed graph (group -> concern -> affordance -> technology). Nodes carry `layer`, `title`, `status`;
       edges carry `kind` (the relation page type) and `page` (the relation page's name).
    conflicts: undirected graph over concerns (the symmetric closure of the declared `conflicts` links);
       edge attribute `declared_by` lists the concern page(s) that wrote the link.
    records: one row per coded scenario or architecture record, with the nodes it names (provenance).
    status_counts: pages in the vault per status value (before any status filter).
    dangling: relation pages dropped because an end was missing or filtered out.
    """

    G: nx.DiGraph
    conflicts: nx.Graph
    records: pd.DataFrame
    status_counts: dict = field(default_factory=dict)
    dangling: list = field(default_factory=list)

    def nodes(self, layer):
        """Sorted names of the nodes in `layer` (alphabetical: the order carries no meaning)."""
        return sorted(n for n, d in self.G.nodes(data=True) if d["layer"] == layer)

    def summary(self):
        """Counts of nodes by layer, edges by relation, conflict pairs and coded records, as a one-column table."""
        rows = [(LAYER_LABEL[l], len(self.nodes(l))) for l in LAYERS]
        rows += [(f"{k} edges", sum(1 for *_, d in self.G.edges(data=True) if d["kind"] == k)) for k in RELATIONS]
        rows += [("conflict pairs", self.conflicts.number_of_edges()), ("coded records", len(self.records))]
        return pd.DataFrame(rows, columns=["item", "count"]).set_index("item")


def _targets(page, key):
    return [l.target for l in page.fm_links.get(key, ())]


def load_graph(root, status=None):
    """Read the vault at `root` and return a `ScatGraph`.

    `status`: None keeps every page; a string or a collection of strings keeps only pages with those `status`
    values (for example "done" for signed-off pages). A relation page whose end was filtered out is dropped and
    listed in `ScatGraph.dangling`.

    Reads as: what the vault says, as nodes and links. Does not mean: that the vault is conformant or its content
    signed off; run `scat check` and have the coder sign off the content first.
    """
    keep_status = {status} if isinstance(status, str) else (set(status) if status is not None else None)
    keep = lambda p: keep_status is None or p.status in keep_status
    vault = read_vault(Path(root))
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
                            **{role: _targets(p, role) for role in RECORD_ROLES}))
    cols = ["record", "kind", "raw", *RECORD_ROLES]
    return ScatGraph(G, C, pd.DataFrame(rec, columns=cols), status_counts, dangling)
