"""Plotting helpers. Each draws onto a matplotlib Axes you pass in (or creates one) and returns it.

Position, ring order and colour are drawing conveniences, never measurements. Nothing is sorted by a measured value.
"""

import textwrap

try:
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.ticker import MaxNLocator
except ImportError as e:  # the analyses work without plotting; say how to add it
    raise ImportError(
        "scat_analysis.plots needs the 'plot' extra: install scat-analysis[plot] "
        "(or, in this checkout, `uv sync --extra plot`)."
    ) from e
import networkx as nx

from .analyses import CHAIN_STATES, centrality, communities, conflict_records, group_coverage, projection, provenance_matrix
from .graph import LAYER_LABEL, LAYERS

COLORS = {"stakeholder-group": "#4c78a8", "concern": "#f58518", "affordance": "#54a24b", "technology": "#b279a2"}
CHAIN_COLORS = {"complete": "#54a24b", "addressed, no technology": "#e6b800", "unaddressed": "#bbbbbb"}


def _ax(ax):
    return ax if ax is not None else plt.subplots(figsize=(7, 5))[1]


def draw_layered(sg, ax=None, title=""):
    """The four layers as columns, one dot per page, one line per relation page. Position within a column is alphabetical."""
    ax = _ax(ax)
    pos = {}
    for x, layer in enumerate(LAYERS):
        ns = sg.nodes(layer)
        pos.update({n: (x, -(i - (len(ns) - 1) / 2)) for i, n in enumerate(ns)})
    for u, v in sg.G.edges:
        ax.plot(*zip(pos[u], pos[v]), color="#999", lw=0.6, alpha=0.7, zorder=1)
    for layer in LAYERS:
        ns = sg.nodes(layer)
        ax.scatter([pos[n][0] for n in ns], [pos[n][1] for n in ns], s=45, color=COLORS[layer], zorder=2)
        for n in ns:   # page name beside each dot; small so ~50 nodes stay readable
            ax.text(pos[n][0] + 0.04, pos[n][1] + 0.08, n, fontsize=6, ha="left", va="bottom", zorder=3,
                    bbox=dict(boxstyle="round,pad=0.05", fc="white", ec="none", alpha=0.7))
    ax.set_title(title); ax.set_xticks(range(4)); ax.set_xticklabels([LAYER_LABEL[l] for l in LAYERS]); ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    return ax


def plot_coverage(sg, ax=None, title=""):
    """Stacked bars: each group's concerns by how far the chain reaches (green, yellow, grey)."""
    ax = _ax(ax)
    group_coverage(sg)[CHAIN_STATES].plot.barh(stacked=True, ax=ax, color=[CHAIN_COLORS[k] for k in CHAIN_STATES], width=0.7)
    ax.set_title(title); ax.set_ylabel(""); ax.set_xlabel("concerns held"); ax.xaxis.set_major_locator(MaxNLocator(integer=True)); ax.legend(fontsize=8, loc="lower right")
    return ax


def draw_projection(sg, layer_keep, via, ax=None, title=""):
    """A one-mode projection on a ring (ring order is alphabetical); edge width is the number of shared neighbours."""
    ax = _ax(ax)
    B = projection(sg, layer_keep, via)
    iso = sorted(nx.isolates(B)); B = B.subgraph([n for n in B if n not in iso])
    ns = sorted(B)
    pos = {n: (np.cos(2 * np.pi * i / len(ns)), np.sin(2 * np.pi * i / len(ns))) for i, n in enumerate(ns)}
    mx = max([d["weight"] for *_, d in B.edges(data=True)] or [1])
    nx.draw_networkx_edges(B, pos, ax=ax, width=[0.4 + 3.2 * d["weight"] / mx for *_, d in B.edges(data=True)], edge_color="#999999", alpha=0.45)
    nx.draw_networkx_nodes(B, pos, ax=ax, node_color=COLORS[layer_keep], node_size=110)
    for n, (x, y) in pos.items():
        ax.text(1.14 * x, 1.14 * y, n, fontsize=6.5, ha="left" if x > 0.05 else "right" if x < -0.05 else "center", va="center")
    ax.set_xlim(-1.9, 1.9); ax.set_ylim(-1.35, 1.35)
    if not B.number_of_edges():
        ax.text(0, 0, "no links at all in this projection", ha="center", color="#666666")
    ax.set_title(textwrap.fill(title + (" | not linked: " + ", ".join(iso) if iso else ""), 75), fontsize=8); ax.axis("off")
    return ax


def draw_tension(sg, ax=None, title=""):
    """Concerns in conflict (red edges) and the groups holding them (grey edges). Layout is a seeded spring layout."""
    ax = _ax(ax)
    C, G = sg.conflicts, sg.G
    sub = nx.Graph(C.edges)
    for g in sg.nodes("stakeholder-group"):
        sub.add_edges_from((g, c) for c in G.successors(g) if c in sub)
    is_conflict = lambda e: C.has_edge(*e)
    pos = nx.spring_layout(sub, seed=4, k=0.9)
    nx.draw_networkx_edges(sub, pos, ax=ax, edgelist=[e for e in sub.edges if is_conflict(e)], edge_color="#d62728", width=2.2)
    nx.draw_networkx_edges(sub, pos, ax=ax, edgelist=[e for e in sub.edges if not is_conflict(e)], edge_color="#bbbbbb", width=1)
    nx.draw_networkx_nodes(sub, pos, ax=ax, node_color=[COLORS[G.nodes[n]["layer"]] for n in sub], node_size=150)
    nx.draw_networkx_labels(sub, pos, ax=ax, font_size=6.5, verticalalignment="bottom")
    ax.set_title(title); ax.axis("off")
    return ax


def plot_carriage(sg, layer, ax=None, title=""):
    """Horizontal bars of concerns carried, one per node of `layer` (alphabetical)."""
    ax = _ax(ax)
    d = centrality(sg).query("layer == @layer").sort_index(ascending=False)
    ax.barh(d.index, d["concerns_carried"], color=COLORS[layer]); ax.tick_params(axis="y", labelsize=7); ax.set_title(title)
    ax.set_xlabel("concerns carried"); ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    return ax


def draw_communities(sg, ax=None, title="", algorithm="greedy_modularity", seed=1):
    """The undirected typed graph, coloured by cluster of `algorithm`; shape marks the layer."""
    ax = _ax(ax)
    comm = communities(sg, seed=seed).set_index("node")
    U = sg.G.to_undirected(); U = U.subgraph(comm.index)
    pos = nx.spring_layout(U, seed=5, k=1.1, iterations=200)
    cmap = matplotlib.colormaps["tab10"]
    nx.draw_networkx_edges(U, pos, ax=ax, edge_color="#cccccc", width=0.8)
    for layer, shape in zip(LAYERS, "so^D"):
        ns = [n for n in U if U.nodes[n]["layer"] == layer]
        nx.draw_networkx_nodes(U, pos, nodelist=ns, ax=ax, node_shape=shape, node_size=90,
                               node_color=[cmap(int(comm.loc[n, algorithm]) % 10) for n in ns], edgecolors="k", linewidths=0.4)
    nx.draw_networkx_labels(U, pos, ax=ax, font_size=6, verticalalignment="bottom",
                            bbox=dict(boxstyle="round,pad=0.05", fc="white", ec="none", alpha=0.7))
    ax.set_title(textwrap.fill(title + " (colour: cluster; shape: square group, circle concern, triangle affordance, diamond technology; "
                               "positions carry no meaning)", 60), fontsize=8)
    ax.axis("off")
    return ax


def plot_provenance(sg, ax=None, title=""):
    """Heat map of which concerns each coded record names (dark = named)."""
    ax = _ax(ax)
    M = provenance_matrix(sg)
    ax.imshow(M.values, cmap="Blues", aspect="auto", vmin=0, vmax=1)
    ax.set_xticks(range(M.shape[1])); ax.set_xticklabels(M.columns, rotation=90, fontsize=6.5)
    ax.set_yticks(range(M.shape[0])); ax.set_yticklabels(M.index, fontsize=7); ax.set_title(title)
    return ax
