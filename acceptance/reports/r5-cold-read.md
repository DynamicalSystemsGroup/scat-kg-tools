# UA-A round 5 (final cold read): R-15 (two fresh Haiku readers, home page left out)

Candidate: tools `a4ebb63` (the D-048 wording), template `313ceac`, Pages preview. For each reader the two messages were sent in order: `briefs/cold-read-part1.md` alone, and only after the reader had answered it, `briefs/cold-read-part2.md` (unchanged since U14b, so it asks what caused each place). The PM added to the part 1 message a line telling the reader to take the page list from `sitemap.xml`, to read each page in full, and to fetch nothing else from the site (no search index, no home page), because reader D of round 4 had seen home-page text through the search index. Answers are the readers' own, unedited. In reader E's reply, the second paragraph headed "Answer 2, pages read" is the reader's own label for its list of pages read; its answer to question 2 is the later message.

## Reader E

### Answer 1 (with its page list, as the reader wrote it)

Answer 1 (Question 1, open): the pages evoke jazz first, and the Chatham House rule second. Jazz is named outright and repeated. Planning says "Planning borrows one habit from jazz: settle who plays, and in what order, before the music starts". Facilitating scenarios says "This guide borrows 'yes, and' from jazz improvisation". Facilitating architectures says "This guide borrows the taking of turns from jazz". Coding says "Coding borrows one habit from jazz: hear a phrase, then play its meaning back in your own voice." The REPL and CLI pages are framed as music too: "Sheet music for the REPL" and "The same tune at the command line." The "Your next step" headings and the "Playing it back" line keep that register.

The Chatham House rule is named explicitly and used as a working rule, not decoration. Planning says "Say Chatham House, aloud and on the page", and the notes must say "groups, not individuals." Facilitating scenarios opens with "Whatever is said here can be used. Nobody is named."

The pages also have a noticeable anti-ranking stance. Planning says "Nothing here is ranked, voted on or adjudicated." Facilitating architectures says "You never ask the room to pick a design." Holding disagreement is handled by writing both accounts ("Tension: ...") rather than settling them. That reads to me as a participatory or deliberative-facilitation tradition, though no page names one.

The definition of "affordance" as "something a tool or arrangement lets someone do" (Coding, "What the pages are"; also Planning) resembles the Gibsonian/design-affordance usage. No page cites Gibson or Norman, so this is my inference from wording only.

I came to the pages with no prior idea of what the project is. I did not read the home page, so my understanding comes only from what the other pages say. They say SCAT stands for Stakeholder groups, Concerns, Affordances and Technologies, and that it is a graph-based knowledge vault built from facilitated sessions (scenario and architecture stories) that are coded into linked pages. The pages say "Pre-release candidate" at the top.

Answer 2, pages read. I fetched the sitemap at https://dynamicalsystemsgroup.github.io/scat-kg-tools/sitemap.xml. It lists 8 URLs. I read these 7 in full, excluding the home page:
- /coding/ (Coding)
- /facilitate-architectures/ (Facilitating architectures)
- /facilitate-scenarios/ (Facilitating scenarios)
- /getting-started/ (Getting started)
- /planning/ (Planning)
- /reference/api/ (Python API reference)
- /reference/cli/ (CLI reference)

Caveats: I converted each page's HTML to text and kept the article or main element, so navigation, scripts and styling were dropped. Within that text I read every line of each page. I did not read any page not on the list. I did not follow or fetch the home page, not even to check its status, and I did not open any project source folder, decision log or other file from the repository. I ran no commands from the docs.

### Answer 2

Answer 2 (cold read, question 2). Same pages as part 1. I re-checked the text files I read; quotes are from those.

1. Facilitating scenarios, "The stance". Quote: "Yes, and. Write down whatever someone offers, as offered." Also: "Saying 'Yes, and' means you accept what was offered and add to it. It does not mean you agree with it." Instruction: say the words "Yes, and" aloud, exactly, at the start of the question that adds to what was offered. What I think it meant: accept and build, without endorsing. Cause: a figure of speech (an improvisation term). The page has to add a sentence to stop "Yes, and" being read as agreement, and it is then used in "Holding disagreement" for opposing accounts ("Yes, and let's hear what each one is protecting."). This is the hardest instruction on the pages for me, because the required literal words carry an agreement meaning that the page then has to take back.

2. Facilitating scenarios, "3. Taking up". Quote: "Yes, that happened, and here is what it looked like from where you sit?" Instruction: say this line. I could not tell whether it is a statement with a stray question mark or a question. Cause: an unclear instruction (ambiguous sentence form), not a figure of speech. The same problem appears in "4. Placing in perspective", where the Say line "From where the borrowers sit, what did that morning look like?" is a question but the page's "Eliciting" section says its lines "are questions" in a different register.

3. Coding, "The linking rules" / relation pairs. Quote: "If the notes name no group for a concern, use the group the session plan seated for that note." Instruction: pick a group when the notes name none. What I think it meant: the group a prompt was planned for in the Planning page ("Plan a prompt for each group"). Cause: an undefined term ("seated"). Planning never describes seating; it only describes prompts per group. The word is a theatre or music image, but the real gap is that the term is not defined, so the instruction is hard to follow.

4. Planning, "Two kinds of session" table. Quote: "Technology stays in the background; what is heard is what it lets people do." Instruction: choose between the Scenarios and Architectures columns. Once my text extraction flattened the table, the rows read badly, so I could not reliably tell which cell belonged to which kind. Cause: most likely layout (table flattened in extraction, so this may be partly my artifact), not a metaphor.

Places where the jazz framing did not make an instruction harder: "Playing it back: raw notes, read again as coded pages" and "hear a phrase, then play its meaning back in your own voice" (Coding). The instruction under it, "Restate each raw page in your own plain words," was clear. The jazz lines in Planning and the turn-taking line in Facilitating architectures are also introductions that do not change any step.

Summary: the figure of speech that caused real difficulty is the exact "Yes, and" wording (item 1). The other difficulties (items 2 to 4) came from unclear sentence form, an undefined term, and possibly table layout, not from metaphor. The hardest single instruction for me was item 1.

## Reader F

### Answer 1 (with its page list, as the reader wrote it)

Brief part 1: cold read of the scat-kg-tools documentation (R-15 check)

WHAT I READ
The sitemap at https://dynamicalsystemsgroup.github.io/scat-kg-tools/sitemap.xml lists eight URLs. I did not fetch the home page (the sitemap's first entry, /scat-kg-tools/). I read the other seven in full, as plain text extracted from the HTML, with nothing cut short:
1. /coding/
2. /facilitate-architectures/
3. /facilitate-scenarios/
4. /getting-started/
5. /planning/
6. /reference/api/
7. /reference/cli/
I did not read the home page, and I did not follow any link to it. I read no page outside the sitemap list, no source folder and no decision log. I ran nothing. The only fetches were the sitemap and those seven pages. The working directory name (scat-kg-tools) was in my environment, but I did not open the repository.

PRIOR IDEA OF THE PROJECT
I came with none. Before the pages I knew only the URL and this brief. What the pages say the project is: SCAT, "Stakeholder groups, Concerns, Affordances and Technologies: the four kinds of thing your notes are coded into" (/getting-started/, opening section). It is a vault of Markdown pages, checked by a Python tool (`scat`, `scat_kg`), for facilitated workshops.

QUESTION 1 (answer as given; not revised)
The pages evoke jazz, and in particular the way a jazz session takes turns and improvises on what the last player said. The pages name this themselves:
- /planning/: "Planning borrows one habit from jazz: settle who plays, and in what order, before the music starts, so that every group gets a turn."
- /facilitate-scenarios/: "This guide borrows "yes, and" from jazz improvisation: you accept what each group offers as it is, and add to it."
- /facilitate-architectures/: "This guide borrows the taking of turns from jazz".
- /coding/: "Coding borrows one habit from jazz: hear a phrase, then play its meaning back in your own voice."
The musical wording recurs in the reference pages and in the set-up page: /reference/api/ has "Sheet music for the REPL: every call, as written."; /reference/cli/ has "The same tune at the command line."; /getting-started/ has "Tuning up: get everything ready before your first session."

Two other things I noticed. The facilitation pages are written as a fixed script: "The lines under 'Say' are your script. Their order is fixed" (/facilitate-scenarios/ and /facilitate-architectures/). The stages are Opening, Eliciting, Taking up, Placing in perspective, Capturing, Closing. The "Chatham House" rule is named by the pages as the basis for anonymity (/planning/: "Say Chatham House, aloud and on the page"). Beyond the jazz framing, the pages read to me as a facilitation-script manual with a confidentiality rule. I did not recognise any specific named method beyond those.

The word "affordance" is used in the sense of "something a tool or arrangement lets someone do" (/coding/, "What the pages are" section). That sense may bring to mind ecological or HCI usage, but the pages do not cite either, so I am not claiming a source.

Nothing in the pages is ranked, voted on or adjudicated, and they say so repeatedly (for example /planning/: "Nothing here is ranked, voted on or adjudicated."). I did not guess an answer to please anyone.

LIMITS
- Every page was read in full as extracted text. Fetching by curl returned the complete HTML, and no page was truncated.
- The "Yes, and" phrase is also a stock improv-theatre phrase. The pages credit jazz, so I report that and not the other tradition.
- The only tool-side noise was a sitemap that is already complete, so no fallback was needed.

### Answer 2

Answer 2 (cold read of the scat-kg-tools documentation, part 2). Pages used are the same seven read in full for part 1 (/coding/, /facilitate-architectures/, /facilitate-scenarios/, /getting-started/, /planning/, /reference/api/, /reference/cli/). Home page not read, no other page fetched.

1. /coding/, "What the pages are" section. A figure of speech caused the difficulty. The page says: "Coding borrows one habit from jazz: hear a phrase, then play its meaning back in your own voice." The same page instructs: "Restate each raw page in your own plain words. Keep its meaning, and add no judgement of your own." "In your own voice" can be read as permission to add your own interpretation, which the later rule forbids. I think the intent was "restate in your own words." The metaphor made the instruction harder to follow.

2. /facilitate-scenarios/ and /facilitate-architectures/, "The stance" section. The jazz idiom partly caused the difficulty. The pages say "Yes, and" must be said aloud, "exactly", and the same words open the Opening script: "Yes, and: several designs can answer one concern" (architectures) and "Yes, and: whatever you tell us will be written down and added to" (scenarios). It is unclear whether "Yes, and" is a required spoken cue or part of the sentence. I think it is a cue that accepts what was offered. The idiom makes it hard to tell.

3. /facilitate-architectures/, Eliciting stage. Unclear instruction, not a figure. The page gives "Yes, and is there a concern this was not aimed at?" and says it "is asked as an addition, never as a test of the design." It then gives a second wording, "Yes, and what else would you want it to cover?", without saying which to use. I think either works and the second is safer, but the page does not say so.

4. /facilitate-architectures/, intro. Unclear instruction, not a figure. The page says the script's "order is fixed," and also "Their wording is yours: say a line as written or in your own words." It is not clear whether lines may be reordered or skipped. I read order as fixed and only wording as flexible, but the page does not state that split.

5. /facilitate-architectures/, "The stance" section. Unclear and mildly figurative. "set another perspective beside it: 'from this perspective, ...'". I read "set beside" as "say, in addition," not as a contrary view. The page does not say whether to state a contrary view or only offer a different angle.

6. /reference/cli/, opening. Figure of speech, minor. "The same tune at the command line." I read it as "same operations, different spelling," but "tune" suggests a stylistic match rather than equivalence. It did not block any step.

Hardest instruction: item 1. The figure of speech sits directly against an explicit rule on the same page.
