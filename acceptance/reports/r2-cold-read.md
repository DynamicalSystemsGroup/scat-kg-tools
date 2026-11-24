# UA-A round 2: R-15 cold read (Haiku, fresh reader, home page left out)

Candidate: tools `2a9cc07`, template `81940e1`, Pages preview. The two messages were sent in order: `briefs/cold-read-part1.md` alone, and only after the reader had answered it, `briefs/cold-read-part2.md`. Answers are the reader's, unedited.

## Answer 1 (open question, as given before any follow-up)

The pages evoke a facilitated deliberation method, with a participatory stakeholder-dialogue tradition behind it and a theatre-script or improvisation flavour on top. Nothing on the pages names a single school, so these are resemblances I noticed, not stated references.

What I noticed, with the page each comes from:
- Chatham House rule. planning: "Say Chatham House, aloud and on the page". scenarios: "Whatever is said here can be used. Nobody is named". This is a named convention for closed-door meetings, and the pages use it as the frame for every session.
- "Yes, and" as a required stance. architectures: "Yes, and. Write down whatever is pitched, as offered... Never ask a question that tests it." The phrase is borrowed from improv, and the page makes it a rule for the facilitator.
- Script and performance vocabulary. architectures: "The lines under 'Say' are your script". api: "Sheet music for the REPL". cli: "The same tune at the command line". The facilitator is treated as a performer working from a score.
- "Affordance" in the Gibson/Norman sense. planning: "An affordance is something a tool or arrangement lets someone do." scenarios: "what a tool let people do, or stopped them doing. That is an affordance."
- Two session types, scenario and architecture, which resemble scenario-based design in HCI. planning: "Two kinds of session". architectures: "Architectures are structural. They are parts and wholes". The pages do not cite that literature.
- Non-adjudication and pluralism. planning, architectures, scenarios: "Nothing here is ranked, voted on or adjudicated." coding: "Holding both sides is allowed and is what the warning marks".
- Anonymity by aggregation. planning: "A cap keeps groups large enough that nobody can be picked out." The rule is that data is entered as groups, never individuals.

Prior idea of the project: I came with none. I did not recognise "SCAT" or "scat-kg-tools". After reading, I understand it as a tool for turning notes from facilitated workshops into a linked graph of stakeholder groups, concerns, affordances and technologies. The acronym is expanded on getting-started: "Stakeholder groups, Concerns, Affordances and Technologies".

Pages read (each fetched with curl from https://dynamicalsystemsgroup.github.io/scat-kg-tools/ and read as text):
1. /getting-started/
2. /planning/
3. /coding/
4. /facilitate-architectures/
5. /facilitate-scenarios/
6. /reference/api/ (I read the intro and the body in full; the title block and nav were the only parts I skimmed)
7. /reference/cli/

Pages not on the list: I fetched /sitemap.xml to get the page list. It is an index, not a documentation page, so I count it as a navigation aid, not a read page.

Home page: not read. The home page was not fetched, and no link to it was followed, even though planning, coding and getting-started link to it ("the home page defines these"). The definitions I used came from the pages' own inline definitions, so my reading of the four terms is from those.

Other: I did not open the project's source folders, its decision log, or anything outside the listed pages. I ran nothing from the project.

Gaps: the coding page's middle sections were read in two passes, and I may have skimmed the repeated navigation text. The api page's parameter tables were read but not checked against any code.

## Answer 2

Answer 2, from the same seven pages read for Answer 1. The home page was not read and no link to it was followed. Answer 1 was delivered in an earlier handback and is not changed here.

Places where an image, phrase or metaphor made an instruction harder to follow:

1. /facilitate-architectures/ and /facilitate-scenarios/, "Two moves keep the whole session in time." "In time" is ambiguous. I first read it as a pacing instruction, such as keeping to a schedule. The two moves that follow are "Yes, and" and "From this perspective", so it means the two stances keep the session on track. The sentence alone does not make that clear.

2. /facilitate-architectures/, "The lines under 'Say' are your script: say them in the order given, as written, or in your own words, except that the words 'Yes, and' stay as written." The script image is clear, but the permission to paraphrase is not. Some lines are questions that must be asked one at a time with a wait, and the page also says "Say these in this order." I took the order as strict and the wording as flexible, but a facilitator could read the block either way.

3. /facilitate-architectures/, "Yes, and. Write down whatever is pitched, as offered." and "If a design seems wrong to you, do not correct it or rank it." Saying "Yes, and" aloud to a design the facilitator thinks is wrong is the hardest instruction to carry out. The page resolves it with "ask what it adds, and set another perspective beside it." I read "Yes, and" as a stance of acceptance, not agreement. The page never says so directly.

4. /planning/, "The chart: who plays, and in what order, before anyone counts in." The theatre image is unclear. I took it to mean a cast-and-order list written before the event. The page never says what a "chart" is or where it goes. The plan file it asks for appears later as plan.txt.

5. /reference/api/, "Sheet music for the REPL: every call, as written." and /reference/cli/, "The same tune at the command line." These are decorative. They say the REPL and CLI are two forms of one thing. The music image adds nothing to the instruction.

6. /coding/, "Playing it back: raw notes, read again as coded pages." The replay image is unnecessary. The next sentence states the instruction: write each raw page again as a coded page. It is not harmful.

7. /facilitate-scenarios/, "Scenarios are behavioural. Technology stays out of view." "Out of view" could be read as a rule to hide technology from the notes. The following sentences show it means technology is not the subject: "What you hear of a tool is what it let people do, or stopped them doing."

Hardest instruction: "Yes, and" with "do not correct it" on /facilitate-architectures/. It asks the facilitator to affirm a design in words while keeping their own view out of it, and the page does not say how to do both in one turn.

Nothing was run. Quotes come from the curl text of each page, so punctuation and line breaks may differ slightly from the live site.
