# WP12-R3 round 3: persona 4 (project manager, reading the Terms page, Haiku)

Candidate: `docs/reference/terms.md` as merged at tools `dev` `6e4cc02` (600 words), after the round 2 fix (WP12-U8, "every page `done`"). A fresh Haiku tester, not the round 1 or round 2 tester. Persona and brief: `acceptance/personas/p4-event-coordinator-haiku.md` and `acceptance/briefs/p4-event-coordinator-haiku.md`. The tester was given the brief and the page text only, pasted into its prompt (the four guide links were marked as not available), and used no tools (0 tool calls). Docs source: the Markdown text of the page. No tool was run, so the uv and clone setup of the other UA-A reports does not apply. The report below is the tester's final message, unedited.

---

# Persona 4 (project manager) reading the glossary page, Haiku run

Method: only the page text in the brief was used. No files, searches or other sources were opened. Every answer below quotes the page. No answer is void.

## The five answers

**1. What must I have in place before a session?**
- **Answer:** A written plan, my stakeholder groups, a note-taker for each session, and a vault that passes its clean check. The groups must also fit under a cap, but the page gives no number for it.
- **Quotes:** "before a session, have a written plan, your stakeholder groups, a note-taker per session, and a vault that passes its clean check." / "the groups fit under the vault's cap, the most groups it allows."
- **Not told, and guessed:** Not told: the cap's value and where it is set. Guessed: a fixed number per vault. Not told: what a "written plan" must contain; the Planning guide is a link I do not have. Not told: what a note-taker must do beyond producing "the notes as told". Guessed: one note-taker per session means one person.
- **Confidence:** medium. I can name the four items, but I cannot confirm the group-count check.

**2. What must a raw page hold before it can be coded?**
- **Answer:** The notes as told, each account under its group, no names or links, and the past or future mark. Every raw page carries that mark.
- **Quotes:** "before coding, a raw page holds the notes as told, each account under its group, no names or links, and the past or future mark." / "every raw page has it."
- **Not told, and guessed:** Not told: whether a raw page must be `done` before coding. Guessed: no. Not told: what "as told" and "name" mean. Guessed: "as told" means verbatim. Not told: whether an account's group must match a stakeholder-group page. Guessed: yes. Not told: which page type elicitation notes go into; the page says "The notes become raw records." but Elicitation has "Vault: none." Not told: who checks "no names or links", since the tool checks only structure. Guessed: the author.
- **Confidence:** medium.

**3. What does "done" mean for a page, and who decides it?**
- **Answer:** `done` is the sign-off status. The person who wrote or coded the page sets it. The tool does not, and it only checks that required fields and links are present.
- **Quotes:** "`done` (the sign-off)." / "the person who wrote or coded the page sets `done`, not the tool, which only checks that the fields and links the page type requires are present"
- **Not told, and guessed:** Not told: what "sign-off" means beyond a status value, or whether a supervisor or reviewer must agree. Guessed: "the person" is the page's author or coder. Not named: which tool. Guessed: the `scat check` run.
- **Confidence:** high.

**4. What must be true before analysis can start?**
- **Answer:** A clean check with zero errors, and every page `done`. Warnings do not block it.
- **Quotes:** "analysis needs a clean check and every page `done`." / "A whole-vault read with zero errors. Warnings do not stop it." / "a gate before analyse."
- **Not told, and guessed:** Not told: whether "every page" includes index tables. The status line excludes them, but the gate sentence does not. Guessed: excluded. Not told: whether the code-stage link checks (one page per pair, each tension as a `conflicts` link) must pass before analysis. Guessed: no. Not told: what analysis is, since the page names an analyse stage but has no entry for it.
- **Confidence:** medium.

**5. How does a concern reach a technology?**
- **Answer:** Only through an affordance. The concern is addressed by an affordance, and that affordance is attributed to the technology. These are two separate links, each on its own page.
- **Quotes:** "So a concern reaches a technology only through an affordance: addressed by it, then attributed to the technology." / "`addresses`, with `concern` and `affordance`." / "`attributes`, with `affordance` and `technology`."
- **Not told, and guessed:** Not told: whether "reaches" is a derived path or a stored link. Guessed: derived from the two stored links. Not told: what happens to a concern whose affordance is never attributed to a technology. Not told: what the "lists" on a coded page are.
- **Confidence:** high.

## Findings table

| Id | Page place | What happened | Guess? (yes/no) | Severity (blocking/not blocking) |
|---|---|---|---|---|
| F1 | Stakeholder group, Check | The cap is named ("the most groups it allows") but has no value, so I cannot confirm the groups fit under it. | yes (assumed a fixed number per vault) | blocking |
| F2 | Raw and coded records, Check | Not told whether a raw page must be `done` before coding. Q2 depends on this. | yes (guessed no) | blocking |
| F3 | Status, Vault line vs Clean check, Check | "every page except the index tables" and "every page `done`" conflict or leave index tables undefined. "Index tables" is never explained. | yes (guessed excluded) | blocking |
| F4 | Clean check, Check | Not told whether code-stage link checks (one page per pair; `conflicts` links) gate analysis. | yes (guessed no) | blocking |
| F5 | Elicitation, Vault | "The notes become raw records." but "Vault: none". The page does not say which raw page type elicitation notes go into. | yes | not blocking |
| F6 | Raw and coded records, Check | "as told", "name", "link" and "each account under its group" are undefined. I guessed verbatim, and that the group must match a stakeholder-group page. | yes | not blocking |
| F7 | Raw and coded records, Check; Status, Check | Only structure is tool-checked. Nothing says who checks "no names or links" or "as told". | yes (guessed the author) | not blocking |
| F8 | Status, Check | "sign-off" and "the person" are undefined. No reviewer or approver is named. | yes | not blocking |
| F9 | Clean check, Stage | The "analyse" stage is named, but there is no entry and "analysis" is never defined. | yes | not blocking |
| F10 | Whole page | "stage" is used as a field on every entry but never defined. | no | not blocking |
| F11 | Clean check, Check | "uv" and "scat" are not explained, and it is unclear whether they need installing. | no | not blocking |
| F12 | Clean check | "Warnings" is never defined. | yes (guessed non-error messages) | not blocking |
| F13 | Three links, Check | "a coded page's lists" uses "lists", which is never defined. | yes | not blocking |
| F14 | Three links | "reaches ... only through" does not say whether a concern-to-technology path is stored or derived. | yes (guessed derived) | not blocking |
| F15 | Elicitation, Check | "a written plan" is required, but its contents are not given. The Planning guide is a link I do not have. | no | not blocking |
| F16 | Elicitation | "session" is never defined. I equated it with "A facilitated event". | yes | not blocking |
| F17 | Intro vs Elicitation, Check | The vault is defined as "your folder of linked pages", yet Elicitation has "Vault: none" and still requires "a vault that passes its clean check". I assumed these refer to the same folder. | yes | not blocking |
| F18 | Scenario, Architecture, Elicitation | Words used before they are defined: "concern", "affordances", "groups", "technologies", "raw records", "clean check". Each is defined later on the page. | no | not blocking |

## Words used before the page explained them

- **"concern", "affordances", "groups"**: first in the Scenario entry, "Coded, it links groups, concerns, affordances." They are defined later.
- **"technologies"**: first in the Architecture entry, "Coded, it links concerns, affordances, technologies." Defined later.
- **"raw records"**: first in Elicitation, "The notes become raw records." Defined later under "Raw and coded records".
- **"clean check"**: first in the Elicitation check. Defined later.
- **"stage"**: never defined, though every entry has one.
- **"analyse" and "analysis"**: the stage is named, but there is no entry and no definition.
- **"index tables"**: first in the Status vault line. Never defined.

## Words I could not place under plan, capture, code or analyse

- **"index tables"**: no stage given.
- **"warnings"**: no stage given.
- **"uv" and "scat"**: the tool is named in the clean check, but no stage is given.
- **"lists"** (a coded page's lists): would fall under code, but the word is never defined.
- **"cap"**: falls under plan, but the value is missing.

"Sign-off" I placed under capture, since it is in the Status entry, which is a capture-stage entry.

## Whether the page helped me relate the pieces

**Helped:**
- The plan, capture, code and analyse ordering, through the stage fields and the stated gate.
- A group holds a concern (`heldby`), stated as "a group holds a concern".
- The raw-to-coded link (`raw` and `coded`), and the three link pages.
- Analysis is gated on a clean check and every page `done`.

**Did not help:**
- What a facilitation plan contains, or how a session runs.
- How note-taking happens during a session beyond "the notes as told".
- How the groups named on raw pages connect to the stakeholder-group pages.
- What analysis produces, or what it requires beyond the gate.
- Where elicitation notes are stored.

---

## PM note (not part of the tester's words)

All five questions were again answered correctly from the page. Of the four findings the tester marked blocking: F3 is a defect the round 2 fix created ("every page `done`" against "every page except the index tables"); it is fixed in WP12-U10 ("every page you made", the coding guide's own words). F1 (the cap's value is set per vault in a file the page does not and need not show), F2 (the tester guessed "no", which is correct, and the page states what a raw page must hold, not when `done` is set) and F4 (the page names the gate, a clean check and every page done, and nothing more; the tester's guess "no" beyond that is correct) are guesses the tester resolved correctly; they are accepted, with the reason, not defects. The rest ask for teaching or definitions the guides carry (WP12 non-goals).
