# WP12-R3 round 4: persona 4 (project manager, reading the Terms page, Haiku)

Candidate: `docs/reference/terms.md` as merged at tools `dev` `bb7e4c9` (600 words), after the round 3 fix (WP12-U10, "every page you made `done`"). A fresh Haiku tester, not one of rounds 1 to 3. Persona and brief: `acceptance/personas/p4-event-coordinator-haiku.md` and `acceptance/briefs/p4-event-coordinator-haiku.md`. The tester was given the brief and the page text only, pasted into its prompt (the four guide links were marked as not available), and used no tools (0 tool calls). Docs source: the Markdown text of the page. No tool was run, so the uv and clone setup of the other UA-A reports does not apply. The report below is the tester's final message, unedited.

---

# User-test report: Persona 4, project manager, reading the glossary page (Haiku 5.5)

No tools were used. Every answer below rests on the page text in the brief. No answer is void.

## 1. What must I have in place before a session?

- **Answer:** Before a session I need a written plan, my stakeholder groups, one note-taker per session, and a vault that passes its clean check. The page gives this as the Elicitation check, and the groups must fit under a cap whose size the page does not state.
- **Quotes:** "before a session, have a written plan, your stakeholder groups, a note-taker per session, and a vault that passes its clean check." / "the groups fit under the vault's cap, the most groups it allows."
- **Not told, and guessed:** Not told what the written plan must contain, or how many groups the cap allows. Not told where the note-taker comes from. Guessed that the note-taker is someone I supervise, which comes from my persona, not the page. Not told what "passes its clean check" means before the tool exists, since the Elicitation entry says "Vault: none".
- **Confidence:** medium.

## 2. What must a raw page hold before it can be coded?

- **Answer:** A raw page must hold the notes as told, with each account under its group, no names or links, and the past or future mark. The page also requires a `timeframe` field on a raw page.
- **Quotes:** "before coding, a raw page holds the notes as told, each account under its group, no names or links, and the past or future mark." / "`timeframe` on a raw page"
- **Not told, and guessed:** Not told what "as told" means, verbatim transcription or a summary. Guessed verbatim. Not told which field holds "its group" on a raw page. Not told what to do with a name that appears in the notes (remove, replace with a role, or hold back). Not told whether the raw page needs `description` as well.
- **Confidence:** medium.

## 3. What does "done" mean for a page, and who decides it?

- **Answer:** `done` is the sign-off for a page. The person who wrote or coded the page sets it. The tool does not set it; the tool only checks that required fields and links are present.
- **Quotes:** "`done` (the sign-off)" / "the person who wrote or coded the page sets `done`, not the tool, which only checks that the page type's required fields and links are present"
- **Not told, and guessed:** Not told whether I, as the supervisor, may set or approve `done`, or whether the author always does. Not told which tool is meant; guessed it is the `scat check` command in the Clean check entry. Not told what "the lists of what it names" contains on a coded page.
- **Confidence:** medium-high.

## 4. What must be true before analysis can start?

- **Answer:** A clean check must pass, and every page I made must be `done`. A clean check means zero errors across the whole vault; warnings do not block it. The check tests structure, not content, so it does not confirm the coding is right.
- **Quotes:** "analysis needs a clean check and every page you made `done`." / "A whole-vault read with zero errors. Warnings do not stop it." / "It tests structure, not content."
- **Not told, and guessed:** Not told whether "every page you made" means every page in the vault or only pages I created. Guessed the vault-wide reading. Not told what counts as an error versus a warning. Not told whether the `conflicts` links must be complete before analysis, though the Conflict entry requires that each tension appear as a link.
- **Confidence:** high.

## 5. How does a concern reach a technology?

- **Answer:** Only through an affordance. A concern is addressed by an affordance (`addresses`), and that affordance is attributed to a technology (`attributes`). Each link is its own page.
- **Quotes:** "So a concern reaches a technology only through an affordance: addressed by it, then attributed to the technology." / "Each is one fact, on its own page."
- **Not told, and guessed:** Not told how many affordances a concern may have, or whether one affordance may serve several concerns. Not told whether a technology may provide more than one affordance. Guessed none of these; they are gaps.
- **Confidence:** high.

## Findings table

| Id | Page place | What happened | Guess? (yes/no) | Severity (blocking/not blocking) |
|---|---|---|---|---|
| F1 | Stakeholder group, Check | The cap on groups is referred to but its size is never stated, so I cannot say how many groups I may have. | no (gap) | blocking |
| F2 | Elicitation, Vault and Check | Vault is "none", but the Check requires "a vault that passes its clean check". This reads as a contradiction. | no | not blocking |
| F3 | Raw and coded records, Check | "as told" is undefined; guessed verbatim. | yes | not blocking |
| F4 | Raw and coded records, Check | "its group" names no field. | yes | not blocking |
| F5 | Raw and coded records, Check | No rule for names found in notes, beyond "no names". | no (gap) | not blocking |
| F6 | Status, Check | "the tool" is not named; guessed it means `scat check`. | yes | not blocking |
| F7 | Clean check, Check | "every page you made" is ambiguous (vault-wide or my pages); guessed vault-wide. | yes | not blocking |
| F8 | Coded record, Status Check | "the lists of what it names" is not specified. | no (gap) | not blocking |
| F9 | Three links | Cardinality (how many affordances per concern, and so on) is not stated. | no (gap) | not blocking |
| F10 | Terms intro | Links to Planning, scenarios, architectures and Coding guides are not in the page; the written plan may be defined there. | no (gap) | not blocking |
| F11 | Scenario and Architecture, Stage | Both are marked Stage "plan", but their coded forms link concerns and affordances, which are coded. The page does not explain how a plan-stage term holds code-stage links. | no | not blocking |
| F12 | Status | Whether I, as supervisor, may set `done` is not stated. | no (gap) | not blocking |
| F13 | Conflict between concerns | "One side counts for both" is not explained. | no | not blocking |
| F14 | Clean check | `uv run scat check` is given with no explanation of `uv` or `scat`. | no | not blocking |

## Words used before the page explained them

- "clean check" appears in the Elicitation Check before the Clean check entry defines it.
- "stakeholder groups" appears in the Elicitation Check before the Stakeholder group entry.
- "raw" and "coded" appear in the Scenario Vault line before the Raw and coded records entry.
- "concerns" and "affordances" appear in the Scenario Vault line before their entries.
- "past or future mark" appears in the Raw and coded records Check before its entry.
- "note-taker" is never explained.

## Words I could not place under plan, capture, code or analyse

- "note-taker" has no stage and no entry.
- "written plan" has no definition. It is presumably plan-stage, but the page does not say.
- "Stage" itself, and the words "capture" and "analyse", are used as stage names but never defined.
- "Scenario" and "Architecture" are marked plan, but their meaning as coded records sits at code; I could not tell where the term sits.
- "Clean check" spans stages ("from the start, rechecked after coding; a gate before analyse"), so I placed it at analyse only by reading the gate wording.

## Did the page help me relate the pieces?

- **Facilitation plan:** Partly. The Elicitation entry lists what to have before a session, but it does not say what the facilitation plan must contain.
- **Note taking:** Yes, in part. The raw record rules say what the note takers' output must hold. It does not say who checks it before it is coded.
- **Coding:** Yes. The concern, affordance and technology chain and the three links are clear.
- **Analysis:** Yes, as a gate. The clean check plus `done` pages is the stated condition. It does not say what analysis consists of.
- **Not related:** The page does not connect the plan to the raw record, nor say who the note-taker reports to. The Planning and Coding guides it links to are not in my copy, so anything they add is unknown to me.

---

## PM note (not part of the tester's words)

All five questions were answered correctly from the page, with quotes, in all four rounds. In round 4 the tester's one blocking mark is F1, the cap's size: it is set per vault in the vault's own configuration file, which a glossary neither holds nor needs to show, so the page says what the cap is and where the guides carry the number. It is accepted, with that reason, not a page defect. Round 4 has no new defect against the five questions. Findings F2 to F14 ask for teaching, definitions the guides carry, or placements of stage that are a one-value-per-entry device (WP12 non-goals); F7 and F12 are guesses the tester resolved correctly. The loop stopped here: four rounds, each by a fresh tester, with one page defect fixed per round from round 1 to round 3.
