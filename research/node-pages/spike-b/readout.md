# Spike B: possible duplicates and two-node pages

Seeded vault: 24 narratives, 311 same-type pairs. Range vault: 9 narratives, 113 pairs; it holds none of the seeds, so its numbers show noise only, not recall. Each method runs in 0.1 s or less.

## Possible duplicates (proposed seeded/range; seeds found)

- 1 adjacent-node Jaccard 0.5+, both pages 2+ adjacent nodes: 4/3; synonym yes (1.00), duplicate row no (0.33), decoy no.
- 1 narrative Jaccard 0.5+: 10/8; synonym, row yes; decoy no.
- 1b twin row in one narrative: 16/7; synonym, row yes; decoy no.
- 2 description cosine 0.5+: 2/1; synonym no (0.25), row yes (0.62); decoy no.
- 2 body reuse: nothing to compare.
- 4 link-text overlap: synonym not in top 5, row top.
- 5 passage tf-idf 0.3+: 10/7; ranks synonym 3, row 2, decoy 296, but the top hits are pages co-mentioned in one paragraph. Without them nothing reaches 0.3.
- Union (1 at 0.5, 2 at 0.5, 1b with narrative Jaccard 0.5+): 9/6; synonym, row yes; decoy no.

Edge Jaccard equals adjacent-node Jaccard, so it is dropped. Read by hand, the seven non-seeded seeded-vault proposals and six range proposals are related pages, none a duplicate; two of the seven (obsidian and telescope; the attention-limit and consent concerns) are fair prompts.

Adjacent-node Jaccard 1.00 is not unique to the twin: how-members-figure-in-koi and what-integration-does-to-the-protocol also score 1.00, on two shared hub groups. The 2+ floor only removes pages with one adjacent node; it does not remove hubs. The output must show the shared adjacent nodes and mark hubs.

## Two-node pages (community-members)

- A narratives joined by any shared node or edge: 4 flagged seeded, 2 range; misses it.
- B joined by a shared other end: 11/7; finds it.
- C as B, only narratives that tell an edge of the page: 8/5; finds it (groups 4, 1, 1). The other seven seeded flags: ethnographers, technical-team, obsidian, vendor-lock-in, koi-doctrine, forum-bot, scheduler.
- Rule 4+ narratives telling its edges and common-end share 0.3 or less: 4 pages flagged on the seeded vault (technical-team, obsidian, ethnographers, community-members), one is the seed: precision 1 of 4. On the range vault it flags ethnographers and technical-team; its community-members has 3 narratives and is not listed.

Link text cannot help: 7 of 8 narratives say "community members".

## Recommendation

1. Possible duplicates, same type only: propose when adjacent-node Jaccard is 0.5+ (2+ adjacent nodes each), or description cosine 0.5+, or a twin row with narrative Jaccard 0.5+.
2. Per proposal: both pages, type, the four numbers (narrative Jaccard, adjacent-node Jaccard, description cosine, twin rows), shared adjacent nodes with hubs marked, one reason line. Wording is "may be one node".
3. Thresholds are fitted to one positive each (0.5 description, 0.3 homonym share) and are provisional; a second vault with known duplicates would settle them.
4. Homonyms: a coder-facing list of pages whose accounts tell different other ends, with the narrative groups. It is weak evidence, cheap to build, and claims nothing about two nodes.
5. Link text is the coder's words, not node names; it may be shown beside a structural proposal, never generate one.
6. Tests: the synonym pair (twin, different names) is proposed; the duplicate-row pair is proposed; the decoy (near names, no shared structure) is not; renaming every page leaves proposals unchanged; community-members is listed with groups 4, 1, 1.

## Commands

    uv run python research/node-pages/spike-b/m1_structure.py
    uv run python research/node-pages/spike-b/m1b_twin_rows.py
    uv run python research/node-pages/spike-b/m2_reuse.py
    uv run python research/node-pages/spike-b/m3_homonym.py
    uv run python research/node-pages/spike-b/m3b_rate.py
    uv run python research/node-pages/spike-b/m4_linktext.py
    uv run python research/node-pages/spike-b/m5_tfidf.py
    uv run python research/node-pages/spike-b/m6_combined.py
