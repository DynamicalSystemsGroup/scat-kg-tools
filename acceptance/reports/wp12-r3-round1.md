# WP12-R3 round 1: persona 4 (project manager, reading the Terms page, Haiku)

Candidate: `docs/reference/terms.md` as merged at tools `dev` `aaf7bca` (600 words). Tester model: Haiku. Persona and brief: `acceptance/personas/p4-event-coordinator-haiku.md` and `acceptance/briefs/p4-event-coordinator-haiku.md`. The tester was given the brief and the page text only, pasted into its prompt (the four guide links were marked as not available), and used no tools (0 tool calls). No repository, no `src/`, `tests/` or `contracts/`. Docs source: the Markdown text of the page. No tool was run, so the uv and clone setup of the other UA-A reports does not apply. The report below is the tester's final message, unedited.

---

PERSONA 4 REPORT: project manager reading the glossary page (Haiku 5.5). Answers use the page text only. No files, searches or other sources were used.

## 1. What must I have in place before a session?

**Answer:** Before a session I need a written plan, my stakeholder groups, a note-taker for each session, and a clean check. The plan must give each group a prompt, and it must keep scenario and architecture sessions apart. Each group must fit under the vault's cap.

**Quotes:**
- Elicitation, Check: "before a session, have a written plan, your stakeholder groups, a note-taker per session, and a clean check."
- Scenario, Check: "the plan gives each group a prompt."
- Architecture, Check: "the plan keeps scenario and architecture sessions apart."
- Stakeholder group, Check: "the groups fit under the vault's cap."

**Not told, and guessed:**
- Not told: what "the vault's cap" is. I cannot check that item, so I did not invent a number.
- Not told: what a "written plan" must contain, or where it is kept. Guess: the plan is a document I write myself. The page does not say so.
- Not told: what a "prompt" is.
- Not told: who a "note-taker" is. Guess: a person who will write raw pages. The page does not say so.
- Conflict: Elicitation asks for "a clean check" before a session. Clean check says its stage is "code; a gate before analyse," and it is "A whole-vault read with zero errors." A session comes before any vault pages exist, so I could not see how a clean check can be in place before a session. I took the Elicitation line at face value and flagged the conflict.

**Confidence:** medium.

## 2. What must a raw page hold before it can be coded?

**Answer:** Before coding, a raw page must hold the notes as told, with each account under its group. It must have no names or links. It must carry the past or future mark. The status check also requires a `description` and a `timeframe` on a raw page.

**Quotes:**
- Raw and coded records, Check: "before coding, a raw page holds the notes as told, each account under its group, no names or links, and the past or future mark."
- Status, Check: "`description` always, `timeframe` on a raw page"
- Past or future mark, Check: "every raw page has it."
- Past or future mark definition: "Whether an account is real (`past`), intended but not yet real (`future`), or both (`mixed`)."

**Not told, and guessed:**
- Not told: what "as told" means in practice, or what counts as a name.
- Not told: what goes into `description`.
- Not told: whether status must be `done` before coding starts. The page lists `description` and `timeframe` for raw pages and says nothing about status. Guess: coding does not wait for `done`. The page's `done` wording is about analysis, not coding.
- Not told: what a "raw page" is called in the vault, beyond "`scenario-raw` or `architecture-raw`."

**Confidence:** high.

## 3. What does "done" mean for a page, and who decides it?

**Answer:** `done` is the sign-off. The author sets it. The tool does not decide it. The tool only checks that the required fields and links are present, and the Clean check section says it "tests structure, not content."

**Quotes:**
- Status: "How finished a page is: `stub` (just started), `draft` (being written) or `done` (the sign-off)."
- Status, Check: "the author sets `done` as the sign-off; the tool only checks that the fields and links the page type requires are present"
- Clean check: "The check tests structure, not content."

**Not told, and guessed:**
- Not told: who "the author" is. Guess: the note-taker who wrote the page. The page does not say whether that is me, the supervisor, or the note-taker.
- Not told: what the sign-off requires beyond setting the field.
- Not told: what "class" is. Status applies to "every page except `class`," and no entry defines it.

**Confidence:** high for the answer, medium for who the author is.

## 4. What must be true before analysis can start?

**Answer:** Analysis needs a clean check and `done` pages. A clean check is a whole-vault read with zero errors. Warnings do not stop it.

**Quotes:**
- Clean check: "analysis needs a clean check and `done` pages."
- Clean check: "A whole-vault read with zero errors. With nothing to report it prints \"no problems\". Warnings do not stop it."
- Clean check stage: "code; a gate before analyse."

**Not told, and guessed:**
- Not told: what "analysis" or "analyse" involves. The page uses "analyse" only as a stage name and never describes it.
- Not told: whether "`done` pages" means every page in the vault or only some. Guess: every page that the analysis uses.
- Not told: who runs the clean check or how. The page says "the tool" in the Status entry, but does not say how to run it.
- Conflict with Q1: the clean check is listed as a pre-session requirement and as a gate before analysis.

**Confidence:** medium.

## 5. How does a concern reach a technology?

**Answer:** A concern reaches a technology only through an affordance. First the affordance addresses the concern, then the affordance is attributed to the technology. Those are two links, each one fact on its own page.

**Quotes:**
- Three links: "So a concern reaches a technology only through an affordance: addressed by it, then attributed to the technology."
- Addressed by: "a concern is addressed by an affordance. `addresses`, with `concern` and `affordance`."
- Attributed to: "an affordance is attributed to a technology. `attributes`, with `affordance` and `technology`."
- Check: "one page per pair; a coded page's lists do not make them."

**Not told, and guessed:**
- Not told: how a link page is created. The page gives the link fields but no procedure.
- Not told: what "a coded page's lists" are in practice, beyond the Architecture entry's "Coded, it links concerns, affordances, technologies."
- Guess: the links are made at the code stage, since the three-links entry gives "Stage: code."

**Confidence:** high.

## Findings table

| Id | Page place | What happened | Guess? | Severity |
|---|---|---|---|---|
| F1 | Elicitation Check vs Clean check (stage: "code; a gate before analyse") | Clean check is required before a session, but its stage is code/analyse. I could not see how it can hold before any vault pages exist. | no (conflict, not a guess) | blocking (Q1) |
| F2 | Stakeholder group Check | "the vault's cap" is never defined. I cannot verify this check. | no | blocking (Q1) |
| F3 | Elicitation Check | "a written plan" has no stated contents or location. | yes | not blocking |
| F4 | Elicitation Check | "note-taker" is never defined. I assumed a raw-page writer. | yes | not blocking |
| F5 | Status Check | "the author" is never identified. I assumed the note-taker. | yes | not blocking (Q3) |
| F6 | Raw and coded records Check / Status Check | Status is not stated as required before coding. I assumed coding does not wait for `done`. | yes | not blocking (Q2) |
| F7 | Status Check | `description` is required, but its contents are not described. | no | not blocking |
| F8 | Clean check | "`done` pages" does not say whether every page or some pages. I assumed every page. | yes | not blocking (Q4) |
| F9 | Clean check / Status | "analysis" and "analyse" are never described. | yes (I assumed analysis follows code) | not blocking (Q4) |
| F10 | Clean check | Who runs the check, and how, is not stated. | yes | not blocking (Q4) |
| F11 | Status | "class" is excluded from the status rule and never defined. | no | not blocking |
| F12 | Three links | Link pages are not explained as to how they are created. | yes (guessed stage: code) | not blocking (Q5) |
| F13 | Intro, Guides line | The page links to four guides (Planning, scenarios, architectures, Coding). I did not have them and did not open them. | no | not blocking |

## Words the page used before explaining them

- "raw records": used in Elicitation ("The notes become raw records."), defined later in "Raw and coded records."
- "group" and "stakeholder groups": used in Elicitation and Scenario, defined later in "Stakeholder group."
- "concern" and "affordance": used in Scenario and Architecture ("links groups, concerns, affordances"), defined later.
- "timeframe": first in Status, Check; defined later in "Past or future mark."
- "sign-off": used in Status, never explained.
- "analyse" / "analysis": appears as a stage in the intro, never defined.
- "Coding": appears in the guide list, never defined.

## Words I could not place under plan, capture, code or analyse

- "class": named as a page type that is excluded from `status`, with no entry and no stage. I could not place it.
- "the vault's cap": appears only in a plan-stage check, with no definition. I placed it under plan by its entry's stage line, but I could not tell what the cap limits.
- "prompt": appears in the Scenario check, with no definition. I placed it under plan by inference.
- "description": required on every page, with no definition and no stage stated. I placed it under capture by inference from the Status entry's stage.

## Did the page help me relate the pieces?

Yes, for these:
- Plan: Elicitation, Scenario, Architecture and Stakeholder group checks tie my facilitation plan to groups, prompts and sessions.
- Note taking (capture): raw page requirements, `timeframe`, `status`, and "as told" tie note taking to the raw record.
- Coding: the three links, the coded-page lists and the conflicts field tie coding to concerns, affordances and technologies.
- Analysis: the clean check and `done` pages are named as the gate.

Not helped:
- How the clean check can be in place before a session (F1).
- Who the author is, and whether that is me or the note-taker (F5).
- What analysis consists of (F9), and how the clean check is run (F10).
- Whether pages must be `done` before coding (F6).

Overall, I could follow the chain from session to notes to coding to analysis. Two gaps block a full check: the vault cap (F2) and the clean-check timing conflict (F1).

---

## PM note (not part of the tester's words)

The tester's own severity marks are kept above. The PM's reading against WP12-R3's five questions: Q2, Q3 (what "done" means) and Q5 answered correctly from the page; Q1 and Q4 answered, with the tester unable to reconcile the clean check's place; "who decides" in Q3 is answered ("the author") but the tester guessed who that is. Some findings (F9 analysis is never described, F13 guide links) are by design: the page states what analysis needs and links the guides. The fix list for WP12-U6 is in the PM's report to the ACE.
