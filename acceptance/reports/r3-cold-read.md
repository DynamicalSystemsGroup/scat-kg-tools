# UA-A round 3: R-15 cold reads (two fresh Haiku readers, home page left out)

Candidate: tools `01d9231`, template `3bd5d5b`, Pages preview. For each reader the two messages were sent in order: `briefs/cold-read-part1.md` alone, and only after the reader had answered it, `briefs/cold-read-part2.md`. In the part 2 message to each reader the PM added one line to the rules, asking it to read the pages in full if its first read had not (reader A read the coding and reference pages only in part for part 1; reader B's first extraction cut pages short). Answers are the readers' own, unedited.

## Reader A

### Answer 1

The pages evoke jazz, specifically jazz improvisation and the idea of taking turns in a session. This is stated outright, and it recurs across pages:
- Getting started and the coding page: "Coding borrows one habit from jazz: play a phrase back as it was played." (coding page)
- Planning: "Planning borrows one habit from jazz: settle who plays, and in what order, before the music starts, so that every group gets a turn." (planning page)
- Facilitating scenarios: "This guide borrows "yes, and" from jazz improvisation: you accept what each group offers as it is, and add to it." (facilitating scenarios page)
- Facilitating architectures: "This guide borrows the taking of turns from jazz: each proposer's design is heard in full, one at a time, and none is set against another." (facilitating architectures page)
- Reference pages use musical framing: "Sheet music for the REPL: every call, as written." (Python API reference page) and "The same tune at the command line." (CLI reference page).
The "Yes, and" stance is the most distinctive device, repeated on both facilitation pages as a required spoken phrase.

What else I noticed: the pages also invoke the Chatham House rule ("Whatever is said here can be used. Nobody is named...", planning and facilitation pages), so the framing is part of a deliberation and participatory-workshop tradition as well as improvisation. The pages are careful to say nothing is "ranked, voted on or adjudicated" (planning and both facilitation pages). The vocabulary of "stakeholder groups, concerns, affordances and technologies" (getting-started page: "SCAT stands for Stakeholder groups, Concerns, Affordances and Technologies") reads to me as an affordance-style design vocabulary, but I cannot tie it to a named tradition from these pages alone, so I am not claiming one. Nothing on them says what SCAT is an acronym of beyond that expansion, and the coding page's tooling (Obsidian vault, markdown pages with [[links]], a checker with error codes like SCAT-LINK-DANGLING) reads as a knowledge-graph / personal-notes tool.

Prior idea of the project: none. I came to the pages with no knowledge of the project. From the pages alone I took it to be a method and toolset for facilitated group sessions (scenarios and architectures) whose notes are coded into a linked graph in a private Obsidian vault.

Pages read:
1. https://dynamicalsystemsgroup.github.io/scat-kg-tools/getting-started/ (read in full)
2. https://dynamicalsystemsgroup.github.io/scat-kg-tools/planning/ (read in full)
3. https://dynamicalsystemsgroup.github.io/scat-kg-tools/facilitate-scenarios/ (read in full)
4. https://dynamicalsystemsgroup.github.io/scat-kg-tools/facilitate-architectures/ (read in full)
5. https://dynamicalsystemsgroup.github.io/scat-kg-tools/coding/ (read the opening sections and grepped the rest for style cues; not read end to end)
6. https://dynamicalsystemsgroup.github.io/scat-kg-tools/reference/api/ (read the opening and grepped; not read end to end)
7. https://dynamicalsystemsgroup.github.io/scat-kg-tools/reference/cli/ (read the opening and grepped; not read end to end)

The list of pages came from the site's sitemap.xml (it lists eight URLs including the home page). Note on the home page: I did one curl request to https://dynamicalsystemsgroup.github.io/scat-kg-tools/ with output discarded, only to check it returned HTTP 200. I did not read its content and did not follow any link from it. I read no page outside the seven above, and I did not open the project's source folders, decision log, or anything else.

Caveats: the coding page and the two reference pages were not read end to end, so a claim about their full content would need a complete read. The site banner on the pages says "Pre-release candidate ... may change before release," which I noted but did not weigh in the answer.

### Answer 2

Yes, there are places. The hardest is the "Yes, and" device, not a single image.

1. Facilitating architectures page (/scat-kg-tools/facilitate-architectures/). The stance section says: "Yes, and" is "required wherever a line under 'Say' contains them: say those two words aloud, exactly", and it also says "Never ask a question that tests it." It then defines "Yes, and" as accepting a design "as offered" without agreeing: "Saying 'Yes, and' means you accept the design as offered and add to it. It does not mean you agree with it." Then it gives the script line: "Yes, and which concern would you say this answers, and what does it leave open?" I was asked to do two things at once. Say the phrase aloud as the opener to a question, and the question must add rather than test. But the scripted question asks what a design "leaves open," which reads as a probe of the design. What I think it asked: open with the words, then ask about what the design answers and what it omits, without judging. What I think it meant: a gap question, asked as a fact about the design, recorded without blame, which the page calls a "gap you record, not a result." The jazz borrowing is what makes the phrase feel like an acceptance, and the page's own definition is narrower than the everyday meaning of "yes, and."

2. Facilitating scenarios page (/scat-kg-tools/facilitate-scenarios/). "This guide borrows 'yes, and' from jazz improvisation." "Yes, and" is an improv-theatre phrase more than a jazz one. This is a small mismatch, and it did not block an instruction. I took the source as a label for the device, not as a rule.

3. Coding page (/scat-kg-tools/coding/). "Coding borrows one habit from jazz: play a phrase back as it was played. Each coded page keeps the meaning of the raw wording and adds no judgement of your own." Then: "You do not summarise or judge." The relation-page step says "The description of a relation page is one sentence saying that fact in plain words." Playing a phrase back "as it was played" could mean copying wording, but a one-sentence description is a paraphrase. I read the instruction as "keep the meaning, re-state in plain words." The metaphor did not say which. This is the one place where the image left a real question about whether to copy or restate.

4. Facilitating architectures page, also: "Each proposer plays a design in turn, and you build on what you hear." "Build on" could mean the facilitator adds content, but the same page says to write designs "as offered" and to ask questions only. I read "build on" as "ask a follow-up," which matched the rest of the page.

5. Planning page (/scat-kg-tools/planning/). "settle who plays, and in what order, before the music starts, so that every group gets a turn." I did not find this hard to act on. The instruction it leads into is a list of steps, and the image only motivates them.

6. Reference pages (/scat-kg-tools/reference/api/ and /scat-kg-tools/reference/cli/). "Sheet music for the REPL: every call, as written." and "The same tune at the command line." These images helped me read them as "same operation, same output." They did not make any instruction harder. The reference prose itself is plain.

Hardest instruction overall: the architectures "Yes, and" rule in item 1. The page asks for a required spoken phrase, forbids testing questions, and then uses a probe-shaped line as its own example.

Coverage note: I read the getting-started, planning, facilitate-scenarios and facilitate-architectures pages in full. I read the coding page in full, including the relation and message sections. For the reference API and CLI pages I read the opening sections in full and searched the rest for the metaphor and instruction words from part 1. A complete read of those two pages could still add a point, but I found no further metaphor-driven instruction in what I read. I did not read the home page, and I did not follow any link to it.

## Reader B

### Answer 1

The pages evoke jazz and improvisational theatre, with a facilitation-protocol flavour on top. What made me say so:
- Coding page: "Coding borrows one habit from jazz: play a phrase back as it was played."
- Planning page: "Planning borrows one habit from jazz: settle who plays, and in what order, before the music starts."
- Facilitating architectures page: "This guide borrows the taking of turns from jazz: each proposer's design is heard in full, one at a time."
- Facilitating scenarios page: "This guide borrows 'yes, and' from jazz improvisation: you accept what each group offers as it is, and add to it."
- The section headings repeat the music metaphor: "Playing it back", "Tuning up", "Sheet music for the REPL" (Python API page), "The same tune at the command line" (CLI page).
- The "Yes, and" and "From this perspective" stance recurs across the facilitation pages, and the scenario and architecture pages both say "Nothing here is ranked, voted on or adjudicated."
- The facilitation pages also use the Chatham House Rule ("Chatham House: groups, not individuals.", "Whatever is said here can be used. Nobody is named"), which reads as a deliberate deliberation or public-consultation convention, separate from the jazz vocabulary.

Pages read (all fetched with curl, text-extracted, and read):
1. https://dynamicalsystemsgroup.github.io/scat-kg-tools/coding/
2. https://dynamicalsystemsgroup.github.io/scat-kg-tools/facilitate-architectures/
3. https://dynamicalsystemsgroup.github.io/scat-kg-tools/facilitate-scenarios/
4. https://dynamicalsystemsgroup.github.io/scat-kg-tools/getting-started/
5. https://dynamicalsystemsgroup.github.io/scat-kg-tools/planning/
6. https://dynamicalsystemsgroup.github.io/scat-kg-tools/reference/api/
7. https://dynamicalsystemsgroup.github.io/scat-kg-tools/reference/cli/

Not on the list: I fetched https://dynamicalsystemsgroup.github.io/scat-kg-tools/sitemap.xml to get the page list. It is not a documentation page, but it is the only way I found the list without touching the home page. I did not fetch the home page, and I did not follow any link to it. I did not open any source folder, decision log, or repository file.

Caveats on coverage: my extraction printed roughly the first 6,000 characters of each page's text, so the tails of several pages were cut off before I read them. The coding page's operations section and the rest of the Python API and CLI reference were only partly read. Facilitate-architectures and facilitate-scenarios were read through the stages, but not to the end. The planning and getting-started pages were read through most of their sections. The answer above rests on the portions I did read, which are enough to support it. I did not run anything.

Prior idea of the project: I had none beyond the URL name (scat-kg-tools). Getting started states that SCAT stands for "Stakeholder groups, Concerns, Affordances and Technologies: the four kinds of thing your notes are coded into." The site calls itself a "Pre-release candidate."

This is my answer as first written, and I have not revised it.

### Answer 2

Yes. I found four places, and the strongest is the first.

1. Facilitate-architectures page (https://dynamicalsystemsgroup.github.io/scat-kg-tools/facilitate-architectures/), under "The stance". The page says: "Saying 'Yes, and' means you accept the design as offered and add to it. It does not mean you agree with it." Under "Yes, and." it also says: "Write down whatever is pitched, as offered. Then ask a question that adds to it." What it asked me to do: say "Yes, and" aloud at the start of a question, and never let it signal agreement. What I think it meant: "Yes, and" is an improv acceptance move, which records and builds on an offer without endorsing it. The jazz and improv framing is not explained where the rule is stated, so a reader with no improv background will most likely hear "Yes, and" as agreement. The page then needs a second paragraph to undo that reading. The same instruction appears on the facilitate-scenarios page ("Saying 'Yes, and' means you accept what was offered and add to it.").

2. Facilitate-architectures page, under "2. Eliciting" and the scripts. The page says: "The lines under 'Say' are your script. Their order is fixed: say them in the order given. Their wording is yours: say a line as written or in your own words, except 'Yes, and', which you say exactly as written." What it asked: say the lines in fixed order, but in your own words where you like, except one phrase. What I think it meant: the order is fixed and the wording is free, apart from "Yes, and". This is not a metaphor problem, but "script" plus "sheet" and "tune" language (see 4) makes "script" read as verbatim, which contradicts "in your own words". The same contradiction appears on the facilitate-scenarios page.

3. Planning page (https://dynamicalsystemsgroup.github.io/scat-kg-tools/planning/), under "Your next step". The page says: "The chart: who plays, and in what order, before anyone counts in." and "settle who plays, and in what order, before the music starts". What it asked: write an event plan naming who takes part, which session, and in what order, saved as plan.txt. What I think it meant: decide the group order before the sessions. "Chart" (an arrangement) and "count in" (the spoken beat that starts a piece) are music terms, and the sentence is a fragment with no verb, so it is hard to tell whether it is an instruction or a caption. The actual task is only in the next paragraph ("Write your event plan..."). I think the jazz line is decoration here, and the sentence before it carries the instruction.

4. Coding page (https://dynamicalsystemsgroup.github.io/scat-kg-tools/coding/), under "Your next step" and "Playing it back". The page says: "Coding borrows one habit from jazz: play a phrase back as it was played. Each coded page keeps the meaning of the raw wording and adds no judgement of your own." What it asked: turn each raw page into a coded page. What I think it meant: "play it back as it was played" is an analogy for faithful restatement. But "play back" could also mean replaying the notes verbatim, which is the opposite of coding into links and types. The sentence after it resolves this ("You read each raw ... and write each raw page again as a coded page"), so the metaphor misleads for only a moment. The Coding page also says "Your next step" and then "Playing it back" as separate headings, so the reader has to work out which is the task.

Smaller points, not counted as blocking:
- Getting started page: "Tuning up: get everything ready before your first session." sits under a heading "Your next step" and reads as a title rather than a step.
- Python API page: "Sheet music for the REPL: every call, as written." and CLI page: "The same tune at the command line." These are decorative. They say the two paths match, but "as written" suggests copy-paste, and nothing on those pages says the outputs can differ.
- Coding page, the SCAT-CONFLICT-BOTH section: "Holding both sides is allowed" and "If both belong in the record, leave the warning in place" are clear, but "belong" is not defined, so a reader cannot tell whether a warning should be fixed or kept.
- Facilitating pages: "the Chatham House lines" and "Say the Chatham House frame aloud" refer to text that is defined only on the planning page ("Say Chatham House, aloud and on the page"). The reference is clear once found, but the facilitation page does not point there.

The instruction I found hardest to follow is the first one: to say "Yes, and" aloud at the start of a question, and to understand that it accepts an offer without agreeing with it. The rule is stated clearly, but the improv metaphor it depends on is never explained, and the page's own wording pulls against it ("accept the design as offered" versus "does not mean you agree").

I read every page in full this time (the first extraction had truncated them).
