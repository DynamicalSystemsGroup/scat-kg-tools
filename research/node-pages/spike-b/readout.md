# Spike B: possible duplicates and two-node pages

Seeded vault: 24 narratives, 311 same-type pairs. Range vault: 9 narratives, 113 pairs. Each method runs in 0.1 s or less.

## Results: possible duplicates

| Method | Proposed (seeded / range) | Synonym | Duplicate row | Decoy |
|---|---|---|---|---|
| 1 adjacent-node Jaccard 0.5 or more, both pages with 2+ adjacent nodes | 4 / 3 | found (1.00) | missed (0.33) | no |
| 1 narrative Jaccard 0.5 or more | 10 / 8 | found | found | no |
| 1b twin row in one narrative | 16 / 7 | found | found | no |
| 2 description cosine 0.5 or more | 2 / 1 | missed (0.25) | found (0.62) | no |
| 4 link-text overlap | - | not in top 5 | top (0.50) | no |
| 5 passage tf-idf, 0.3 or more | 10 / 7 | rank 3 | rank 2 | rank 296 |
| Union: 1 at 0.5, 2 at 0.5, 1b with narrative Jaccard 0.5 or more | 9 / 6 | found | found | no |

Edge Jaccard equals adjacent-node Jaccard, so it is dropped. Body reuse has nothing to compare (one same-type pair has bodies). Passage tf-idf ranks shared paragraphs first; without them nothing reaches 0.3 and the seeds fall to rank 7 and 272.

Read by hand, the seven non-seeded seeded-vault proposals and the six range proposals are related pages, none a duplicate. Two of the seven (obsidian and telescope; the attention-limit and consent concerns) are fair prompts; five are noise.

## Results: two-node pages (community-members)

| Method | Flagged (seeded / range) | community-members |
|---|---|---|
| A narratives joined by any shared node or edge | 4 / 2 | not flagged |
| B joined by a shared other end of its edges | 11 / 7 | flagged |
| C as B, only narratives that tell an edge of the node | 8 / 5 | flagged, groups 4, 1, 1 |
| Share of narrative pairs with a common other end | rank 4 of 16 / 3 of 3 | 0.27 |

C also flags ethnographers, technical-team, obsidian and forum-bot: hubs look like two-sense pages. Link text cannot help: seven of eight narratives call it "community members".

## What works and what does not

- Shared adjacent nodes find the structural twin and never the near-name decoy.
- The duplicate row needs a twin row or description reuse.
- No structural method separates a two-sense page from a hub: one flag in eight is the seed.

## Recommendation

1. Possible duplicates, same type only: propose a pair when adjacent-node Jaccard is 0.5 or more (both pages 2+ adjacent nodes), or description cosine is 0.5 or more, or a twin row sits in one narrative with narrative Jaccard 0.5 or more.
2. Per proposal: both pages, type, the four numbers (narrative Jaccard, adjacent-node Jaccard, description cosine, twin rows), shared adjacent nodes, one reason line. Wording is "may be one node", never "are".
3. Homonyms: feasible only as method C, worded "accounts tell this page to different other ends", listing the narrative groups, for pages with 4+ narratives telling its edges and a common-end share of 0.3 or less. It claims nothing about two nodes.
4. Link text is the coder's words about the node, not node names, so it may be shown beside a proposal made by structure, never generate one.
5. Tests: the synonym pair (twin, different names) is proposed at adjacent Jaccard 1.00; the duplicate-row pair is proposed; the decoy pair (near names, no shared structure) is not; renaming every page leaves the proposals unchanged; community-members is listed with groups 4, 1, 1.

## Commands

    uv run python research/node-pages/spike-b/m1_structure.py
    uv run python research/node-pages/spike-b/m1b_twin_rows.py
    uv run python research/node-pages/spike-b/m2_reuse.py
    uv run python research/node-pages/spike-b/m3_homonym.py
    uv run python research/node-pages/spike-b/m3b_rate.py
    uv run python research/node-pages/spike-b/m4_linktext.py
    uv run python research/node-pages/spike-b/m5_tfidf.py
    uv run python research/node-pages/spike-b/m6_combined.py
