# WP26 round 2: findings and dispositions

Candidate: tools `dev` 71a0faf (after the wave push) and template 0b8b4c4 on `dev`; for this round the template's tools pin
was moved to 71a0faf in a local, unpushed commit (c48302d), because the pinned tools (fd0a39e) predate WP24. Same
testers and setup as round 1, fresh agents. Reports: `wp26-r2-<persona>.md`, the testers' returned text (none of them
could write its file; the text is what each returned). p1, p2 and p3 reached J10 with a clean check; c1 to c3 ran J1 to J4
and J6. **No blocking finding.** The PM's filing, not the ACE's dispositions.

| Finding (testers) | Severity | Disposition |
|---|---|---|
| Round 1's blocking items (evidence, copy-share, review, merge, split-plan missing from the pinned tools; no Terminal-free pointer) | was blocking | Re-tested: the commands ran with the moved pin (p1, p2, p3 used `fingerprint`, `review`, `edges addressed-by`); c1 to c3 followed the new "Before you start" bullet. **Open request to the ACE: move the template's pin on `dev`.** |
| p1 F-16/F-19, p2 F-7/F-8, p3 F-13 | not blocking | Accepted: a group's `holds` edge for a concern heard only in a design session, and the capture-stage "do not link" against Coding's links, are the coder's judgement (`MISSION.md`); Coding adds links after capture. Listed in the reviewer's guide. |
| c1 F-4/F-6, c2 F-7, c3 F-6 to F-8 (where the consent records are; who approves an AI service; children as participants; what the provider keeps) | not blocking | Accepted: the organiser's own policy; the pages give the choices, not the answers. Children as participants noted for the ACE as a possible later page. |
| c1 F-8/F-9, c2 F-10, c3 F-9/F-10 (AI wording; prompt examples; note-taker with none named; notes folder) | not blocking | Accepted: the planning page gives patterns, one example each, by design (1,500-word cap). |
| c2 F-3/F-5, c3 F-3/F-4 (the website path ends in Terminal; Install once uses a terminal) | not blocking | Accepted: the "Before you start" bullet and the chat-path page say it; the chief engineer's sitting confirms who does the one-time install. |
| p2 F-3, p3 (font-cache line from `draw`) | not blocking | Accepted: Matplotlib's own first-run message. |
| p1 F-17 (`edge_table("is addressed by")` refused) | not blocking | Accepted: the refusal names the three types. |
| p3 F-14 (candidates list long), F-18 (template tags in a clone) | not blocking | Accepted as in round 1. |
| All: `page.py index` 404, refused pushes, no remote | harness | Not findings. |

Pass bar: no blocking finding in round 2, every finding dispositioned. A third round is not needed.
