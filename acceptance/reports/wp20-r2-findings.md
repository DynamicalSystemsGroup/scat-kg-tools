# WP20 UA-A round 2 (manual path): findings and proposed dispositions

Candidate: tools `dev` 7d17534 (docs candidate; `f6b79b8` adds only the docs-test pin), template `dev` 826bc99 (pins 7d17534). CI green in both; R-6 passed on a fresh template clone (clone, `uv sync`, `scat check` prints `no problems`; `uv` preinstalled, declared). Pages preview: https://dynamicalsystemsgroup.github.io/scat-kg-tools/. Round 2 carries the D-100 fixes (docs W1 to W7, candidates on request, the mention rule). Reports, unedited: `wp20-r2-p1.md` (Haiku, Python session from J3), `wp20-r2-p1b.md` (Haiku, Python session from J3, a second Haiku in the Python session), `wp20-r2-p2.md` (Haiku, command line), `wp20-r2-p3.md` (Sonnet, Python session). Fresh agents, not the round 1 ones. Dispositions below are the PM's proposals; the ACE decides.

## Void checks
- Reused names: none from the worked example; no solo-trial command ran with the example's name (W1 holds: all four used their own names). The example's names appear only in pre-removal output.
- `src/` and `tests/`: no tester read either (grep hits are the testers' own "I did not read" lines).
- Claims without pasted output: none found. p1b disclosed that it downloaded every docs page's text before its J1 answer (a cold-read order slip, not a void). Pushes were refused or failed (no remote), per the kit not findings.
- Haiku in the Python session through J10: p1 and p1b, both used the Python session for every tool step from J3 (shell only for `uv sync` and git; one file editor for text). Covered.
- No report is void.

## Pass bar
| Line | Result |
|---|---|
| Every tester reaches J10 with a clean check, a tag, the commit it pins and the recipient | Met by p1, p1b, p2, p3 |
| Blocking findings | None |
| D-100 fixes seen working | W2 (all four listed `narrative` after the first stub); W4 not exercised by anyone; candidates off by default (no tester saw them unasked; p3, p2, p1b asked for them); no tester reported a SCAT-MENTION problem |

## Findings (new; round 1's are not repeated)
| Id | Reports | What | Proposed disposition |
|---|---|---|---|
| X1 | p1 F-4, F-15; p1b F-12; p2 F-6 | `git add .` (the page's command) also commits files that are not the model: a drawing (`fingerprint.png`, `layered.png`) or the organiser's plan file. The pages do not say where drawings go or whether a plan file belongs in the repository. 3 of 4 | Fix (docs, a sentence in the solo trial step 5 and in Commit and push: draw into the ignored `exports` folder, or say the drawing is committed on purpose; and plan files) |
| X2 | p1b F-7; p2 F-5 | The facilitation pages script the Chatham House rule as the worked example's default; a tester whose terms name another rule found no wording to use. The pages say "yours says what you agreed" | Accept: the pages say it; the scripts are examples |
| X3 | p1b F-5 | Not said whether narrative pages that quote the notes are inputs or the model, which matters for release | For you: a question about the bar (the glossary defines inputs, model, analysis); accept for v0.1 and list as known weak, or a docs sentence |
| X4 | p3 F-12 | The Analysis page gives no rule for when a view should send you back round the coding loop | Accept: judgement is the coder's; testers still went back round the loop where a view showed a gap |
| X5 | p3 F-13; p3, p2, p1, p1b | Tag name `v1` is the page's example and the page never says the name is the organiser's | Fix (docs one clause: "or a name of your own") |
| X6 | p1b F-9 | A coder's guess row with a note ("Coder guess") passes the check | Accept: a row is the coder's statement (the page says so) |
| X7 | p1 F-13, p3, p2 F-2 | Obsidian steps checked through files, as the kit says; `uv sync` reaches GitHub (W16); clone history shows WP commits and tags (W15, accepted in D-100) | Accept, as D-100 |
| X8 | p1b F-10; p2 F-7; p3 F-11 | Candidates asked for with `--candidates` are long for a short page; correct by the page's definition | Accept: asked for only; no longer default |
| X9 | p3 F-4 to F-6; p1b F-4, F-6; p2 F-4 | Gaps in the testers' own "Your terms" notes (attribution, licence for the model, rights by material, consent filing, a conflict between release and commitments) | Accept: brief content, not docs; W5's docs sentence let all four answer |
| X10 | p1 F-8, F-10 (p1b F-8 stub status typed by hand) | Tester wording and slips: own wording for names, labels, status typed by hand so `set-status` printed `unchanged` | Accept: what the briefs ask |

Fix list proposed: X1 and X5 (two docs sentences plus one re-pin, est. 2), then a short round 3 with fresh testers for those two lines only, or accept both and list them. Round 2 leaves no blocking finding, so the pass bar is met on its own terms; X1 touched three of four testers and is the only repeat.
