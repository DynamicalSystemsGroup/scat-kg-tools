# Round 1: consolidated findings (PM digest, for the ACE to disposition)

Candidate: tools `9fad960` (docs and code), template `89af44a`, Pages live. Reports: `r1-p1.md` (Haiku, said it used the
command line), `r1-p2.md` (Haiku, command line), `r1-p3.md` (Sonnet control, REPL), `r1-cold-read.md` (Haiku). Void
check: no tester reused a worked-example name (the only grep hits are their own statements that they did not).
Every report states that uv was preinstalled (gap held for the chief engineer, D-040, D-041). Docs source was the live
Pages site in every report.

## Pass-bar position
- All three personas reached a clean whole-vault check (`no problems`), stage by stage through J6.
- **J7 not fully reached by anyone.** The environment's permission classifier refused `git push` for all three, and
  refused `git commit` for p1 (p2 and p3 committed locally). The refusals came from the tester sessions, not from the
  docs or tools. Nothing was worked around. This is an environment limit, not a docs finding; see item A.
- **REPL coverage gap.** No Haiku tester used the Python REPL (p1 said so; p3 on Sonnet did, by piping lines into
  `python -i`). MISSION requires at least one Haiku REPL tester. Rerun p1 on the REPL.
- **R-15 cold read:** names jazz unprompted (all four reports). But the cold reader flagged two places where a phrase
  made an instruction harder, so R-15's 'no such place' is not yet met (items C1, C2). The cold reader also saw
  question 2 before answering question 1 (the brief file shows both); the protocol must deliver Q2 only after Q1.

## Findings that need a docs fix (proposed for U11; none blocking by the MISSION definition)
| Id | Source | Finding | Proposed fix |
|---|---|---|---|
| C1 | cold | facilitate-architectures: 'a player in a jazz combo builds on what the others play' sits beside scripted lines ('Say these in this order'); unclear whether to follow the script or improvise | state plainly: the lines are the script; the jazz image comes after the instruction and is not part of it |
| C2 | cold | facilitate-scenarios: 'Yes, and' tag: required wording or style? | say the exact words to say, once, plainly |
| C3 | cold | planning: 'the chart before the gig', 'before anyone counts in' hard to parse | plain wording for the instruction; keep the image in a heading or aside |
| P1 | p1, p2, p3 | planning: where the plan is saved is not stated (vault root file chosen by all three) | one sentence: keep it anywhere outside the pages, it is not a SCAT page; a text file in the folder is fine |
| P2 | p1, p2, p3 | coding: relation page file names are cut at about 70 characters, not mentioned | one sentence saying so, with the full title kept in `title:` |
| P3 | p1, p3 | coding: whether raw pages and tool-created stubs must reach `done` is not said | state which pages must be done for a clean finish |
| P4 | p2, p3 | facilitate pages say 'paste into the page in Obsidian'; no route without Obsidian | add 'or any text editor' |
| P5 | p1, p3 | coding: how to choose a concern/affordance/technology pair and what a relation page description says | one worked sentence each |
| P6 | p1 | coding commit example 'Code the Saturday notes' reuses the example's name | neutral placeholder |
| P7 | p1, p2 | planning does not place 'clear the example' in order (it is in getting-started step 5) | link or order sentence |
| P8 | p3, p1 | facilitate pages: one raw page per story vs several groups' accounts of one evening; group examples ('operators') may be copied | clarify one sentence each |
| P9 | p1, p2 | the Facilitating nav label has no page of its own; testers guessed URLs and hit 404 | the home or planning page links both pages by name (check it already does) |

## Items for the ACE
- **A. Commit and push in tester sessions.** Options: (1) accept that J7's commit and push are unreachable by agents
  here, record in sitting 4 as known-weak, and count the clean check plus the local commit as the agent bar; the
  chief engineer's UA-M covers the push; (2) a tester whose commit is refused is rerun. The unit does not work
  around the classifier.
- **B. Rerun scope.** Round 2 would rerun fresh testers after the U11 fixes: p1 (Haiku, REPL, mandatory), p2, p3, the
  cold read with Q2 delivered after Q1. A tester-environment limit that the REPL tester pipes lines into
  `python -i` (no interactive terminal) should be stated in the brief.
- **C. Tool notes** (not docs): `stub-pair` truncates long names; U1 (held) changes `stub` and `set-status done`.
