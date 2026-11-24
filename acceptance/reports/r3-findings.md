# UA-A round 3: findings digest (PM, for the ACE to disposition)

Candidate: tools `01d9231` (last change to `src/` and `docs/`), template `3bd5d5b`, Pages preview with the banner. uv was preinstalled (D-040, D-041). Reports: `r3-p1.md` (fresh Haiku, Python session, flood-readiness domain), `r3-cold-read.md` (two fresh Haiku readers, A and B, two messages sent in order). Void check: hits only in the untouched example's own output (`scenario-coded/notes-at-a-chatham-house-session-coded.md` in the check output, and the removed example's file names in the tester's own `git rm` output). No report is void.

## Pass bar

| Bar | Result |
|---|---|
| Fresh Haiku REPL tester reaches J7 (clean check, local commit) | Met. `no problems`, 28 done, local commit; push impossible (no remote). 16 findings, none blocking, no docs command failed. |
| Cold read names jazz or improvised music unprompted | **Met by both readers**, from the new framing sentences ("borrows one habit from jazz", "jazz improvisation"). |
| Cold read reports no place where a metaphor obscured an instruction | **Not met by either reader.** Both list places, none stopped them. |

## The places the cold readers list (both readers agree on the first three)

| Id | Page and words | What the readers said | Origin |
|---|---|---|---|
| C1 | facilitate-architectures, example line "Yes, and which concern would you say this answers, and what does it leave open?" next to "Never ask a question that tests it" | A: the example reads as a probe of the design, contradicting the rule it illustrates; hardest instruction. B: "Yes, and" can be heard as agreement; the page needs a second paragraph to undo it; hardest instruction. | The probe-shaped example was written by U14 (the worker's own wording). Plain defect. |
| C2 | coding, framing sentence "play a phrase back as it was played. Each coded page keeps the meaning of the raw wording and adds no judgement of your own." | A: copy or restate? B: could mean replaying notes verbatim. | The framing sentence carries instruction content (the second clause), against the placement rule. U14 wording. |
| C3 | planning, epigraph "The chart: who plays, and in what order, before anyone counts in." | B: a fragment with no verb, hard to tell caption from instruction (the instruction follows in the next paragraph and was plain). A: not hard. | Epigraph (allowed in framing, D-045 item 2). |
| C4 | "script" with "in your own words" (B), "build on" (A), "Tuning up" heading under "Your next step" (B), "as written" in the API epigraph (B) | Minor; each resolved by the neighbouring sentence. | Mixed. |
| C5 | coding, SCAT-CONFLICT-BOTH: "belong" undefined (B) | Minor content wording. | Existing. |

## Persona findings

All 16 non-blocking; the same kinds as round 2 (judgement calls in coding, environment artefacts, internal commit subjects in the clone history). Two to note: F-10 (J5 before the example is cleared; the page tells the reader to clear it before adding pages but J5 comes first in the brief's order, and clearing late was safe) and F-14 (no rule for a concern with no answering affordance; the check accepts it). Neither blocks.

## PM recommendation (the ACE decides; D-046 says to message the ACE if R-15 fails again)

R-15 is half met: jazz is now named unprompted by both readers. The remaining failure is instruction wording, and C1 and C2 are defects I introduced in U14. Proposed U14b (small, est. 3): (1) replace the probe-shaped example in both facilitation pages with one that adds without testing, for example "Yes, and what did that design let people do?"; (2) cut the coding framing sentence to framing only ("Coding borrows one habit from jazz: play a phrase back as it was played"), moving "keep the meaning of the raw wording; add no judgement of your own" into the instruction text where it belongs, with "restate in plain words, do not copy the raw text" stated plainly; (3) leave C3 to D-045 item 2 or make the planning epigraph a full sentence; (4) re-pin (U15b) and one more pair of fresh cold readers. Alternatively the ACE accepts C3 to C5 as minor and takes C1 and C2 as the only fixes.
