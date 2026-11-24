# UA-A round 2: findings digest (PM, for the ACE to disposition)

Candidate: tools `2a9cc07`, template `81940e1`, Pages preview (banner present). uv was preinstalled in every run (D-040, D-041). Reports: `r2-p1.md` (Haiku, Python session), `r2-p2.md` (Haiku, command line), `r2-p3.md` (Sonnet control), `r2-cold-read.md` (Haiku, two messages sent in order). Void check (the README grep): hits only in the untouched example's own output and one tester self-check list; none in names the testers chose. No report is void.

## Result against the pass bar

| Bar | Result |
|---|---|
| Every tester reaches J7 (clean check, local commit) | Met by p1, p2, p3. Each: `no problems`, local commit, push refused or impossible (not a finding, D-044). The p1 and p3 pushes were refused by the tester environment's classifier; p2's failed for want of a remote. |
| Haiku REPL tester | Met: p1 used the Python session for J5 to J7 (piped into `python -i`). |
| No blocking finding in the persona reports | Met: none of the three marks any finding blocking, and no docs command failed as shown. |
| Cold read names jazz or improvised music unprompted | **Not clearly met.** Reader 1 named "improvisation", "improv", "theatre-script" and a performance vocabulary ("Sheet music", "tune", "score"), but not jazz. See C1. |
| Cold read reports no instruction obscured | **Not met as asked**: 7 places listed (see C2). None stopped the reader. |

## Clusters (persona reports)

| Id | Finding | Reports | PM view |
|---|---|---|---|
| P1 | Clearing the example (Getting started step 5) is met after J5, when the tester's raw drafts already exist. Its `git add .` sweeps drafts and `plan.txt` into "Remove the example", and its "no problems" is not what prints (2 draft warnings). The coding page's Before-you-start does not repeat the step, so p3 found it only through the cap message. | p1 F-4, p2 F-8 F-9, p3 F-6 | Docs fix, 3 of 3 testers. Not blocking (all reached J7). Proposed: step 5 says to do it before adding your own pages, and says what prints if drafts exist; coding Before-you-start points back to it. |
| P2 | The briefs say to show "the page templates", which D-043 removed. Testers reported it as a gap. | p1 F-1, p2 F-4, p3 F-2 | Kit fix (brief wording), not a docs finding. Fix in `acceptance/briefs/`. |
| P3 | The clone's `git log` shows internal commit subjects ("WP8-U12 ..."). | p1 F-2, p2 F-14 | Accept: a repository made from the template on GitHub starts with fresh history; this is an artefact of the local-clone simulation. List in the reviewer's guide. |
| P4 | "Tuning up" epigraph looks like a missing link. | p2 F-1 | Accept (style in framing, D-045 item 2). |
| P5 | Environment artefacts: close Terminal and open a new window; "Type exit() to leave" in a piped session; Obsidian editing with a script; the push refused by the environment; `uv sync` needs network. | p2 F-3 F-5 F-10, p3 F-1, p1 F-8, p3 F-9 | Accept: tester environment, not docs. |
| P6 | Judgement left to the facilitator, not an instruction gap: how to tell a story line from a concern line; which group proposed a pitch heard by several; how to decide an addresses or attributes pair from loose notes; what to write in a relation page's description; no note-taker available; session header lines. | p1 F-3 F-5 F-7, p2 F-6 F-7, p3 F-3 F-4 F-5 F-7 F-8 | Accept as coding judgement (R-14 forbids adjudicating; the pages say so). Optional small additions are the ACE's call. |
| P7 | Relation file names cut at 64 characters mid-word. | p2 F-11 | Accept: documented in the coding page. |

## Cold read (R-15)

- **C1. The word jazz is on the home page only.** `grep -rn -i 'jazz\|improvis' docs/` finds it in `docs/index.md` (lines 50, 53) and nowhere else. The cold read excludes the home page by design (MISSION R-15). Round 1's reader named jazz because `facilitate-architectures.md` said "a player in a jazz combo", which U11 removed as an obscuring phrase. The acceptance README says the guide text carries the word jazz in one plain sentence. That is no longer true. So the cold read as specified can no longer name jazz from the word, and reader 1 did not infer it from the music vocabulary.
- **C2. Places reader 1 listed as making an instruction harder** (page, words, what to do): (1) both facilitation pages, "Two moves keep the whole session in time" (ambiguous: pacing or stance?); (2) architectures, "say them ... as written, or in your own words, except ... 'Yes, and'" read with "Say these in this order"; (3) architectures, "Yes, and" with "do not correct it" (hardest instruction); (4) planning epigraph "The chart ... before anyone counts in"; (5) api and cli epigraphs ("Sheet music", "The same tune"), decorative; (6) coding, "Playing it back"; (7) scenarios, "Technology stays out of view" (could mean hide technology).
- **PM recommendation (the ACE decides):** the persona runs need no U14 fix for blocking findings, but P1 and P2 are cheap, the cold read is the open item. Plan U14 (est. 5): P1 and P2; plain wording for C2 items 1, 2, 4, 7 (instruction sentences, not epigraphs); and one plain sentence naming jazz in the framing of each guide (outside any instruction), so the cold read has the word to find. Then U15 (re-pin) and U16 (round 3) limited to fresh cold readers (two) plus one fresh Haiku REPL tester on the changed pages.
