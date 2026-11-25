# WP20 UA-A round 1 (manual path): findings and proposed dispositions

Candidate: tools `dev` ef092ea (docs candidate 6df6bdd, src unchanged since 241ab43); template `dev` a8f7287 (pins 6df6bdd). Pages preview: https://dynamicalsystemsgroup.github.io/scat-kg-tools/. Reports, unedited: `wp20-r1-p1.md` (p1, Haiku, Python session), `wp20-r1-p2.md` (p2, Haiku, command line), `wp20-r1-p3.md` (p3, Sonnet, Python session). uv was preinstalled in every run (D-040, D-041). Dispositions below are the PM's proposals; the ACE decides.

## Void check

- Reused names: no tester used a worked-example name for its own pages. p1 ran the docs' own solo-trial command with the example's name, then deleted that page and started again (finding W1). Greps for the example's words hit only prose ("attribution") and pre-removal output of the untouched example.
- `src/` and `tests/`: no tester read either (grep empty).
- Claims without a block: J1 and J3 (reading stages) in all three, and p3's J4 (answers listed inline, not fenced); read in context, none void.
- Tester slips, not docs findings: p1 ran J5 to J7 tool steps on the command line against its brief (rechecked in the Python session at J8 to J10), so Haiku in the Python session covers J8 to J10 only, while p3 (Sonnet) covers J3 to J10 in it; p1 wrote and deleted a file under `/tmp`.
- The agents' pushes were refused by the environment and there is no remote; per the kit, not a finding.

## Pass bar

| Line | Result |
|---|---|
| Every tester reaches J10 with a clean check, a tag, the commit it pins and the recipient | Met by p1, p2, p3 |
| Blocking findings (stopped short, or a docs command fails as shown) | None |
| Guesses are findings | Listed below |

## Findings

| Id | Reports | Page and words | Proposed disposition |
|---|---|---|---|
| W1 | p1 F-2 | Getting started, solo trial step 2: the literal command uses the worked example's name `saturday-at-the-tool-library`, though the page says to use your own | Fix (docs): show a placeholder or name it as a made-up example in the command line itself |
| W2 | p1 F-3, p2 F-1, p3 | Solo trial and Getting started step 5: after `git rm -r` the five folders, including `narrative`, no longer exist; the brief expects a list of pages | Fix (docs one sentence: the folders go with the example and come back with the first stub) and fix the brief's wording |
| W3 | p1 F-1 | The flow, step 9: the guide column links "Terms", not the Analysis page | Fix (docs) |
| W4 | p2 F-11 | Analysis: "the folder `exports` is ignored by git", but the page's own command writes to `edge-tables`, which the template does not ignore, so `git add -A` committed it | Fix (docs: use `--out exports`) |
| W5 | p1 F-5, p2 F-5, p3 F-2 to F-5 | Data, rights and consent: the rule says each answer is one the page allows or shows, but all three testers' answers to choices 3, 4, 6, 7 and 8 fall between the examples (release to a client; rights split by material; licence for the model) | Fix (docs: say the examples are not exhaustive and what an answer must hold), three of three |
| W6 | p2 F-13 | Coding, hand over: no sentence for when there is nothing left to commit | Fix (docs one sentence) |
| W7 | p1 F-9 | Lock a version: not said whether stub node pages block the lock | Fix (docs one sentence), or accept: stubs are allowed by the architecture |
| W8 | p3 F-9 | `scat_kg.check(neighborhood=False)` works but the API page does not show it | Accept (reference page; a guess that worked) |
| W9 | p1 F-7, p2 F-10, p3 F-7 | Fingerprint "candidates (linked, no row)": 10 to 30 pairs, mostly not edges anyone would tell; hard to read | Tool behaviour, three of three; outside WP20's blast radius. Accept for this release with the reason, and list as a follow-up package |
| W10 | p2 F-8, p3 F-6 | SCAT-MENTION on an architecture page asks for group links though the page says architectures set people aside; a hyphenated group title was not offered | Accept the first (the warning is a warning) pending your read; the second is a tool question for you |
| W11 | p2 F-9, F-12 | No documented way to rename or delete a node page | Accept as outside v0.1 (a real organiser edits files and uses git) or follow-up |
| W12 | p1 F-8 | A concern with no addressing row is not named by the Analysis page | Accept: the views show it by absence |
| W13 | p3 F-8 | The layered drawing has lines through other nodes' boxes | Accept, visual polish |
| W14 | p1 F-4, F-6; p2 F-6, F-7; p3 F-1 | Own wording for prompts, plan files, link text; Obsidian absent (files checked); a candidate pair left without a row as the page says; "set `timeframe:` too" is correct English (p1's typo claim is not a defect) | Accept: these are what the briefs ask, not defects |
| W15 | p1, p2, p3 | A user cloning the template sees work-package commit messages ("WP20-U2: pin the tools commit ...") and tags such as `divergence/D-037` in its history | For you: leave, squash on the template, or accept. Not a requirement today |
| W16 | p2, p1 | `uv sync` reaches GitHub for the tools dependency though the clone has no remote | Accept: expected, the dependency is a git URL |

Proposed fixes W1 to W7 are docs sentences plus one brief line; one unit (est. 3), a re-pin (the docs change moves the candidate) and round 2 with fresh testers. Not run, waiting for your dispositions (D-099).
