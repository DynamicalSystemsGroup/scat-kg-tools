# WP12-R3 round 2: persona 4 (project manager, reading the Terms page, Haiku)

Candidate: `docs/reference/terms.md` as merged at tools `dev` `e6977f6` (599 words), after the round 1 fixes (WP12-U6). A fresh Haiku tester, not the round 1 tester. Persona and brief: `acceptance/personas/p4-event-coordinator-haiku.md` and `acceptance/briefs/p4-event-coordinator-haiku.md`. The tester was given the brief and the page text only, pasted into its prompt (the four guide links were marked as not available), and used no tools (0 tool calls). Docs source: the Markdown text of the page. No tool was run, so the uv and clone setup of the other UA-A reports does not apply. The report below is the tester's final message, unedited.

---

Persona 4 report: project manager reading the glossary page (Haiku). Answers come only from the page text in the brief. I did not open the linked guides (Planning, scenarios, architectures, Coding) or any project files.

result: Glossary page read as a project manager. Five answers given, each quoted from the page. Five blocking-or-not findings logged; one blocking (which pages must be `done` before analysis).

## 1. What must I have in place before a session?

**Answer:** A written plan, your stakeholder groups, a note-taker for each session, and a vault that has passed its clean check.

**Quotes:**
- "before a session, have a written plan, your stakeholder groups, a note-taker per session, and a vault that passes its clean check." (Elicitation, Check)
- "named by role, never a person" (Stakeholder group)
- "the groups fit under the vault's cap, the most groups it allows" (Stakeholder group, Check)
- "A whole-vault read with zero errors. Warnings do not stop it." (Clean check)

**Not told, and guessed:**
- Not told: the value of the cap. I cannot count whether my groups fit.
- Guessed: that "written plan" is a document I write before the session, and what it must contain. The page gives no content list.
- Guessed: that the clean check must be run and pass before the session. The page says only "from the start, rechecked after coding" (Clean check, Stage).
- Not told: who the note-taker is, or what the note-taker must be briefed on.

**Confidence:** medium. The list is clear. The meaning of "written plan" and the cap are not.

## 2. What must a raw page hold before it can be coded?

**Answer:** The notes as told, with each account under its group, no names or links, and the past or future mark. It also needs a `description` and a `timeframe`.

**Quotes:**
- "before coding, a raw page holds the notes as told, each account under its group, no names or links, and the past or future mark." (Raw and coded records, Check)
- "`description` always, `timeframe` on a raw page, `raw` and the lists of what it names on a coded page." (Status, Check)
- "Whether an account is real (`past`), intended but not yet real (`future`), or both (`mixed`)." (Past or future mark)

**Not told, and guessed:**
- Not told: what "as told" looks like on the page, or how an account is marked under its group.
- Not told: how to remove names or links from notes that have them.
- Guessed: that a raw page must be `done` before coding starts. The page does not say this. The Status check covers fields only.

**Confidence:** high for the list, low for the format and for whether `done` is required before coding.

## 3. What does "done" mean for a page, and who decides it?

**Answer:** `done` is the sign-off for a page. The person who wrote or coded the page sets it. The tool does not. The tool only checks that the required fields and links are present.

**Quotes:**
- "`done` (the sign-off)" (Status)
- "the person who wrote or coded the page sets `done`, not the tool, which only checks that the fields and links the page type requires are present" (Status, Check)

**Not told, and guessed:**
- Not told: what the sign-off consists of beyond the required fields and links.
- Guessed: that I, as project manager, am not the decider unless I write or code a page myself. The page does not name a supervisor.
- Not told: what state a page is in before `done` beyond "stub" and "draft", which are only defined as "just started" and "being written".

**Confidence:** high.

## 4. What must be true before analysis can start?

**Answer:** The clean check must pass, and the pages must be `done`. The clean check is a whole-vault structure check with zero errors. It does not test content.

**Quotes:**
- "analysis needs a clean check and `done` pages." (Clean check, Check)
- "Stage: from the start, rechecked after coding; a gate before analyse." (Clean check)
- "The check tests structure, not content." (Clean check)
- "Run: uv run scat check." (Clean check)

**Not told, and guessed:**
- Not told: which pages must be `done`. The page does not say all pages, or only coded pages. This is the blocking gap.
- Guessed: that all pages must be `done`.
- Not told: what checks cover content, or who reviews content before analysis.
- Not told: what "uv" is or what installing it requires.

**Confidence:** medium. The two conditions are clear. Their scope is not.

## 5. How does a concern reach a technology?

**Answer:** Only through an affordance. The concern is addressed by an affordance, and that affordance is attributed to the technology.

**Quotes:**
- "So a concern reaches a technology only through an affordance: addressed by it, then attributed to the technology." (The three links)
- "Addressed by: a concern is addressed by an affordance. `addresses`, with `concern` and `affordance`." (The three links)
- "Attributed to: an affordance is attributed to a technology. `attributes`, with `affordance` and `technology`." (The three links)
- "one page per pair; a coded page's lists do not make them." (The three links, Check)

**Not told, and guessed:**
- Not told: how a link page is formatted or where it lives, beyond its field names.
- Not told: what "pair" means in the check. I guessed it means one page for each link type between two named things.
- Guessed: that the link to the group (`heldby`) is not part of the route to a technology. The page does not say so.

**Confidence:** high.

## Findings table

| Id | Page place | What happened | Guess? (yes/no) | Severity (blocking/not blocking) |
|---|---|---|---|---|
| F1 | Stakeholder group, Check | The cap on the number of groups is not stated, so I cannot check the groups fit. | no | not blocking |
| F2 | Elicitation, Check | "written plan" has no content list. I guessed what it must contain. | yes | not blocking |
| F3 | Elicitation, Check; Clean check, Stage | I guessed the clean check must pass before a session. The page gives "from the start" only. | yes | not blocking |
| F4 | Raw and coded records, Check | "as told" has no format description. | yes | not blocking |
| F5 | Raw and coded records; Status, Check | I guessed a raw page must be `done` before coding. The page does not say this. | yes | not blocking |
| F6 | Raw and coded records, Check | No method for removing names or links from notes. | no | not blocking |
| F7 | Status, Check | I guessed I am not the decider of `done`. The page does not name a supervisor. | yes | not blocking |
| F8 | Clean check, Check | Not told which pages must be `done` before analysis: all, or only coded ones. | yes | blocking |
| F9 | Clean check | The clean check tests structure only. No content check is named. | no | not blocking |
| F10 | The three links, Check | "pair" and link page format are not explained. | yes | not blocking |
| F11 | Elicitation, Stage | Stage is "plan", but the same entry says "The notes become raw records", which happen at capture. Placement is unclear. | no | not blocking |
| F12 | Clean check, Run | "uv" and "scat" are not explained. | no | not blocking |
| F13 | Status | "sign-off" is defined only by a parenthesis. Stage is "capture", but the signer is the coder, who works at code. | no | not blocking |
| F14 | Clean check | "Warnings" are mentioned with no definition. | no | not blocking |
| F15 | Elicitation, Check | "note-taker" is named but never defined or placed in a stage. | no | not blocking |

## Words used before the page explained them

- "stakeholder group": used in Elicitation (Check) before its own entry.
- "raw records": used in Elicitation before "Raw and coded records".
- "concern", "affordance", "technology": used in Scenario and Architecture before their entries.
- "past or future mark" and "timeframe": used in the Raw and coded records check and the Status check before their entries.
- "clean check": used in Elicitation before its entry.
- "cap": used in Stakeholder group, never defined.

## Words I could not place under plan, capture, code or analyse

- "note-taker": named in Elicitation but has no stage or definition.
- "warnings": no definition or stage.
- "uv run scat check": a tool command with no stage. The clean check's stage ("from the start, rechecked after coding") spans plan, capture, code and analyse, so it does not sit under one stage.

## Did the page help me relate the pieces?

- **Facilitation plan:** Yes, partly. Elicitation's Check lists the written plan, the stakeholder groups and a note-taker per session. It does not say how the plan is tied to the vault.
- **Note taking:** Yes, partly. The Raw and coded records check and the Past or future mark entry describe what a raw page holds. They do not say how a note-taker produces it or who checks it.
- **Coding:** Yes. The three links and the rule "a concern reaches a technology only through an affordance" show the route. The format of the link pages is not given.
- **Analysis:** Yes, partly. The gate is "a clean check and `done` pages". Which pages must be `done` is not given (F8).

The page did not connect the facilitation plan to the raw pages, or the note-taker's output to `done`.

---

## PM note (not part of the tester's words)

All five questions were answered correctly from the page. The tester's one blocking mark (F8, which pages must be `done` before analysis) is a real ambiguity: the coding guide says "Aim to bring every page you made to `done`". The fix, in WP12-U8, is one phrase: "every page `done`". Findings F2, F4, F6, F10, F12, F14 and F15 ask for teaching or definitions of words the page links to the guides for (a written plan, the note format, the command, the note-taker's role); the page defines, the guides teach (WP12 non-goals), so they are accepted. F1: the cap is per vault, so the value is set there, not in a glossary. F9: the check is structural by design; analysis is a mission non-goal. F11 and F13: stage placements are a one-value-per-entry device; the tester's reading ("sign-off at code") is the accepted placement of `done`; F13's "capture" for Status is the PM's flagged judgement. F3, F5 and F7 are guesses the tester resolved correctly or harmlessly.
