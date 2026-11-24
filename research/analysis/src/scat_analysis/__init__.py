"""scat_analysis: describe a SCAT vault as a graph (research spike RS2, developed under D-054).

    from scat_analysis import load_graph, traceability, tension
    sg = load_graph("path/to/vault")            # status="done" keeps signed-off pages only
    traceability(sg)                            # one function per analysis, each returns a DataFrame or plain data

Nothing here ranks stories, groups or architectures. Run `scat check` on the vault and have the coder sign off
the content before trusting any result. Plotting helpers live in `scat_analysis.plots`.
"""

from .analyses import (centrality, community_agreement, communities, conflict_records, gaps, group_coverage, projection,
                       projections, provenance, provenance_matrix, tension, traceability)
from .graph import LAYERS, ScatGraph, load_graph

__all__ = ["load_graph", "ScatGraph", "LAYERS", "traceability", "group_coverage", "gaps", "projections", "projection",
           "tension", "centrality", "communities", "community_agreement", "provenance", "provenance_matrix",
           "conflict_records"]
