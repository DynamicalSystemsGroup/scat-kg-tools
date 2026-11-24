# UA-A round 4: R-15 cold reads (two fresh Haiku readers, home page left out)

Candidate: tools `e1faae3` (the D-047 wording), template `ad502ed`, Pages preview. For each reader the two messages were sent in order: `briefs/cold-read-part1.md` alone, and only after the reader had answered it, `briefs/cold-read-part2.md` (which now also asks, for each place listed, whether a figure of speech or a musical term caused the difficulty). The PM added one line to the part 1 message: read each page in full. Answers are the readers' own, unedited.

**Contamination note (reader D).** Reader D reports that, while checking the site, it printed the start of the site's search index (`search/search_index.json`), which holds home-page text, so it saw a fragment of the home page ("Every voice gets a chorus..." and "the tune the rest of these pages riff on."). It says it did not use those lines, and its Answer 1 quotes only the four framing sentences and the reference epigraphs. Reader C also fetched the home page URL once for its status code and discarded the body. The ACE judges whether reader D counts.

## Reader C

### Answer 1

The pages evoke jazz, specifically jazz improvisation as played in a group, and the Chatham House rule as a second, smaller tradition.

What I noticed:
- coding page: "Coding borrows one habit from jazz: play a phrase back as it was played." Its headings and text use "Playing it back" and "Your next step".
- facilitate-architectures page: "This guide borrows the taking of turns from jazz: each proposer's design is heard in full, one at a time".
- facilitate-scenarios page: "This guide borrows 'yes, and' from jazz improvisation: you accept what each group offers as it is, and add to it." "Yes, and" is a scripted line the facilitator must say verbatim.
- planning page: "Planning borrows one habit from jazz: settle who plays, and in what order, before the music starts", and "The chart: who plays, and in what order, before anyone counts in."
- reference/api page: "Sheet music for the REPL: every call, as written." reference/cli page: "The same tune at the command line."
- getting-started page: "Tuning up: get everything ready before your first session."
The musical vocabulary recurs throughout and the pages name the borrowing themselves. "Yes, and" is improv-theatre phrasing that the pages attribute to jazz.

Second, the Chatham House rule, on facilitate-scenarios, facilitate-architectures and planning: "Whatever is said here can be used. Nobody is named," and the notes header "Chatham House: groups, not individuals." This is a confidentiality convention for workshop discussion.

Third, the reference pages (reference/api, reference/cli) use "usage:" blocks, exit-code tables and "Fix:" lines in the style of ordinary command-line reference documentation. The split into getting-started, how-to guides and reference is a common software documentation layout. I do not recognise a specific academic school or named method lineage in these pages beyond the above.

Prior idea of the project: I had none before reading. From the getting-started page ("SCAT stands for Stakeholder groups, Concerns, Affordances and Technologies") I took it to be a tool for coding facilitated workshop notes into a linked graph of those four kinds of thing, delivered as a Python package (scat_kg) and a scat command line tool, working in a private git-backed vault read in Obsidian.

Pages read in full (read as text extracted from each page's main content via curl; I did not view them rendered):
1. coding
2. facilitate-architectures
3. facilitate-scenarios
4. getting-started
5. planning
6. reference/api
7. reference/cli

I read no page outside this list.

Disclosures:
- I got the page list from https://dynamicalsystemsgroup.github.io/scat-kg-tools/sitemap.xml. That is a site index, not a documentation page.
- I ran one curl against the home page URL to check its HTTP status (200), discarding the body. I did not read the home page and did not follow any link to it. The brief said not to read it, and I should have avoided even requesting it; flagging that plainly.
- No home page content or source folders were read.

### Answer 2

1. Coding page, "Coding borrows one habit from jazz: play a phrase back as it was played." Instruction it gave me: restate each raw page "in your own plain words" and "add no judgement". I read "played back as it was played" as meaning copy it out verbatim, which contradicts the restate instruction two paragraphs later. Meaning, as far as I can tell from the rest of the page: keep the meaning, change the wording. Cause: the musical figure (a figure of speech), not an unclear instruction.

2. Facilitate-scenarios and facilitate-architectures, "Yes, and". The page requires "Yes, and" to be said aloud, exactly, and defines it as "accept the design as offered and add to it. It does not mean you agree with it." The phrase is an improv-theatre term borrowed from jazz. Reading "Yes, and is there a concern this was not aimed at?" I first took it as a probing question. The definition resolved it, but only after the figure of speech had raised the doubt. Cause: figure of speech, partly cured by the in-text definition.

3. Planning page, "The chart: who plays, and in what order, before anyone counts in." and "settle who plays, and in what order, before the music starts". I could not tell what "before anyone counts in" asked me to do beyond the ordering already given in the text. The rest of the paragraph carries the actual instruction (plan the sessions and order). Cause: musical figure; no missing step.

4. Facilitate-scenarios and facilitate-architectures, "Say the Chatham House frame aloud" and the Opening script that follows. The term "Chatham House" is used as a known instruction ("Say the Chatham House frame", "Open the session by reading the Chatham House lines aloud") and is not defined on either facilitation page. The fuller script only appears on the planning page ("Say Chatham House, aloud and on the page"). I had to infer what to read aloud from the planning page. Cause: an undefined term, not a figure of speech.

5. Coding page, linking back to the raw page. The text says "The raw page lists its coded pages in coded, so a reader can walk both ways. The tools check this and tell you if one side is missing." It also says "The tools do the bookkeeping". Later, the page's own message walkthrough (message 2, SCAT-RAW-BACKLINK) requires a hand edit to the raw page's frontmatter. So the instruction that the tools do the work is incomplete. Cause: a missing step, not a figure of speech.

Hardest instruction: the coding page's "Restate each raw page in your own plain words. Keep its meaning, and add no judgement of your own" set against "play a phrase back as it was played" (item 1). Cause of the difficulty: the musical figure.

## Reader D

### Answer 1

The style these pages evoke most strongly is jazz, and the pages say so themselves. Quotes:
- facilitate-architectures: "This guide borrows the taking of turns from jazz: each proposer's design is heard in full, one at a time."
- facilitate-scenarios: "This guide borrows "yes, and" from jazz improvisation."
- planning: "Planning borrows one habit from jazz: settle who plays, and in what order, before the music starts."
- coding: "Coding borrows one habit from jazz: play a phrase back as it was played."
- reference (Python API page): "Sheet music for the REPL: every call, as written." Reference (CLI page): "The same tune at the command line."

Beyond the jazz framing, I noticed a stage-script style. facilitate-architectures says "The lines under 'Say' are your script," and both facilitation pages give numbered stages with "Do:", "Say:" and "Note-taker writes:". The planning page frames sessions around "Chatham House" and says to "Say Chatham House, aloud and on the page." That is a named convention the pages refer to. Coding and the CLI reference read as a software reference, with rule ids such as SCAT-DONE-FIELD and exit-code tables. I do not recognise a specific named facilitation method from the pages alone, and I am not guessing one.

Prior idea of the project: I came to the pages with no prior knowledge of the project. From the pages I read, I take it to be a tool that turns facilitated workshop notes into a linked set of pages (stakeholder groups, concerns, affordances, technologies), with a Python package scat_kg and a scat command, and a checker. That understanding comes from getting-started, planning and coding.

Caveat on the cold read: while checking the site, I ran a curl that printed roughly the first 1,500 characters of the site's search index (search/search_index.json). That index includes home-page text, so I saw a fragment of the home page, including the lines "Every voice gets a chorus..." and "the tune the rest of these pages riff on." I did not use those lines as the basis for Answer 1; the jazz evidence above comes only from the pages I read in full. I did not follow any link to the home page and I did not open it as a page.

PAGES READ (in full, as extracted text; I read the article body of each HTML page and the Read tool reached each page's "Where next" section, with no truncation):
1. getting-started (https://dynamicalsystemsgroup.github.io/scat-kg-tools/getting-started/)
2. facilitate-architectures
3. facilitate-scenarios
4. planning
5. coding
6. reference/api (Python API reference)
7. reference/cli (CLI reference)

Page list came from the site's sitemap.xml (https://dynamicalsystemsgroup.github.io/scat-kg-tools/sitemap.xml), which lists the home page and these seven pages. The brief's "navigation lists the pages" was not used; the sitemap was.

PAGES NOT ON THE LIST: I fetched sitemap.xml and search/search_index.json for discovery. Neither is a documentation page; the search index is the one that leaked home-page text, as described above. I did not read the project's source folders, decision log, or any local file. I ran nothing from the project. The HTML extraction may have dropped images or layout, which I could not see, so my reading is of text only.

### Answer 2

1. coding: "Coding borrows one habit from jazz: play a phrase back as it was played." The instruction then says "Restate each raw page in your own plain words." Difficulty: the metaphor says replay as played (verbatim), while the instruction says restate in your own words. The pages mean the second: keep the meaning and add no judgement. Cause: a figure of speech (the jazz framing) that clashes with the instruction, and the page never reconciles them.

2. facilitate-architectures, "Taking up": "take it up as a companion. It is not a challenger." The instruction: when a second design comes for the same concern, say "Yes, that answers it, and here is another way to answer it?" "Take up" is a music term with no definition. I read it as "build on it, add it alongside," which is what the scripted line does. Cause: musical term, undefined.

3. facilitate-scenarios, "Holding disagreement": "name the tension aloud as a margin." The instruction is to say the tension aloud and write both accounts. "As a margin" is unclear: whether to say it, or write it in the notes margin. Cause: figure of speech with no definition.

4. facilitate-architectures and facilitate-scenarios, "Yes, and": the stance says "Do not ask whether it is true, right or complete," yet the scripted lines include "Yes, and is there a concern this was not aimed at?" and the page says "Saying 'Yes, and' means you accept... It does not mean you agree." The improv term makes it hard to tell whether the phrase is a required words-to-say device or only a stance. The script resolves it (say the words aloud where a line contains them), so the difficulty is mainly the figure of speech. Cause: a term borrowed from improvisation, explained only partly.

5. planning, "Tuning up" appears on getting-started only as a subtitle; no instruction depends on it. Not a difficulty.

Hardest instruction that is not figurative: coding, "Choose each pair from the notes... take a group and one concern that group voiced in its own words." It does not say what to do if the notes name no group for a concern; it assumes they always do. Cause: a missing step, not a metaphor.

Summary: the figures that cost the most were the jazz framing on coding (point 1), and the undefined "take up" and "as a margin" (points 2 and 3). In those three the cause is a figure of speech or an undefined term, not a missing step. The coding pair-choice gap is a missing step.
