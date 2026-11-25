# WP16-U11 (WP13-R4): cold read of the flow page and the data, rights and consent page

Candidates: `docs/flow.md` and `docs/data-and-consent.md` as merged on the tools integration branch `wp16/build` at the commit of this report's parent. Tester model: Haiku. Persona: `acceptance/personas/p4-event-coordinator-haiku.md` (project manager). The tester was given the persona, the five WP13-R4 questions and the Markdown text of the two pages only, in an isolated folder, and used four tool calls (reading those four files). No repository, no `src/`, `tests/` or `contracts/`. Links to other pages were not available to it. The report below is the tester's final message, unedited. Dispositions of its findings are the ACE's.

---

Persona: project manager (Haiku), reading flow.md and data-and-consent.md only. Note: the persona file describes a glossary page called "Terms", but the two pages I was given are the flow and the data/consent page. I answered from those two only. The Terms page is linked from flow step 9 but I did not have it.

**1. What do I settle before the first session?**
Answer: Steps 4 to 6 come first. Step 4 "Set terms" is the set of up-front answers: participation terms, AI use, how each kind of material is kept and released, and the commitments to participants. Step 5 is setup (private repo from the template, cloned, opened as a vault). Step 6 is planning the sessions, held to the stakeholder-group cap in scat.toml. Step 3 (the organiser decides to run a facilitated elicitation) comes before step 4.
Quotes: flow step 4 "The organiser answers and documents the up-front questions"; data page "Questions to have answered and documented before a project starts, one for each choice above."
Not told / guesses: The pages never say "complete the whole checklist before session 1". I inferred that from step 7 (capture) depending on step 6 and "what participants were told". I also guessed that the consent conversation happens before any session, because the data page says participants are "told before they take part". Neither point is stated outright. The page also does not say who signs off that step 4 is complete.
Confidence: medium-high on the order of steps; medium on "must be complete before session 1".

**2. What depends on consent?**
Answer: Capture (step 7) depends on consent: the data page says "Capture depends on it", and flow step 7 depends on "what participants were told". The AI choice (5) is "matched to what participants were told", so it depends on consent too. The contributions-use choice (4) includes attribution, and the flow says follow-through on commitments (after step 10) depends on step 4.
Quotes: "SCAT describes consent as informed: the organisers choose the terms up front, every participant works within the same terms, and they are told before they take part."; "Consent has no field in the vault, and git keeps every committed version of a page."
Not told / guesses: The pages say consent is "documented" but give only examples (a signed form each, a read-aloud statement noted, terms in the invitation). They do not say which one is required. They do not say what happens if someone withdraws. Also, if the consent record is not in the vault, where it is kept is not stated. I guessed it lives with the field notes, which the flow says stay "outside the tool".
Confidence: high that capture and AI use depend on consent; low on how consent is recorded or withdrawn.

**3. Where does the data live by default?**
Answer: The model (the git repository: narratives, nodes, edges, graph) defaults to a private repository, made from the template, "visible to the owner and the people invited." The field notes (inputs) are kept "outside the tool, in the form step 4 allowed." The analysis (reports, figures) has no stated default.
Quotes: "The template's default is a private repository, visible to the owner and the people invited."; flow step 7 "They stay outside the tool, in the form step 4 allowed."
Not told / guesses: The pages do not name the host of the repository, and I guessed it is a hosted git service. They do not say where the inputs are kept by default, and I guessed "outside the vault, wherever I choose". The data page says the scat commands "make no network calls" and "do not read the field notes", but on the chat path "the field notes go to the chat provider's service". So the default may differ if AI is used, and the page does not say which path is the default.
Confidence: high for the model; low for inputs and analysis.

**4. What are the steps after capture?**
Answer:
- Step 8 Code: each narrative goes round the coding loop (interpreting, authoring, coding, reviewing). This makes a narrative page, node pages, and one "Edges told" row per edge. The tool checks conformance and the coder owns interpretation.
- Step 9 Analyse: views of the knowledge graph (fingerprint, edge table, layered view, trace) are read. Reading can send the coder back to step 8. It depends on "a conformant vault".
- Step 10 Hand over: a clean whole-vault check, scat index, commit and push. The coder states the model is finished and tags the version. This is a release "at the level step 4 set".
- After step 10: following through on commitments to participants (e.g. sharing findings back).
Not told / guesses: "Interpreting, authoring, coding, reviewing" is not defined here. I guessed "interpreting" means deciding what the account means and "coding" means assigning nodes. "Conformant" and "conformance" are not defined on these two pages. I guessed it means the tool's checks pass. The pages do not say how to tag a version or what the release levels are, beyond "between private and public".
Confidence: high on the order; low on what each coding sub-step means and what "conformant" requires.

**5. Where do I go to learn each step?**
Per the flow table (I could not open the links):
- 1 Discover: Home (index.md)
- 2 Try and 5 Set up: Getting started
- 3 Decide: this page (flow)
- 4 Set terms: Data, rights and consent (data-and-consent.md)
- 6 Plan: Planning
- 7 Capture: Scenarios and Architectures pages
- 8 Code: Coding and the CLI reference
- 9 Analyse: Terms (reference/terms.md), the page under test
- 10 Hand over: Coding
Guess: Step 9 sends the reader to the Terms page for "views", which I did not have, so I could not check whether it explains them.
Confidence: high for the mapping; I could not verify any linked page.

**Prescriptive sentences**
- Data page: "Questions to have answered and documented before a project starts, one for each choice above." (must be done before the project)
- Data page: "Tick each when it is documented." (instructs a checklist action)
- Flow step 4: "The organiser answers and documents the up-front questions."
- Flow step 10: "the coder states the model is finished and tags the version." (instruction, no method given)
- Flow: "A reader trying the approach alone ... can skip the consent steps and go from step 2 to step 8." (permits skipping)

**Words I did not understand**
- "Vault" (used as a thing I open in Obsidian, never defined)
- "Fingerprint"
- "Elicitation"
- "Conformant" / "conformance" / "clean whole-vault check"
- "scat index", "scat.toml"
- "Interpreting", "authoring", "coding" (as loop stages)
- "Edges told" (column name)
- "Knowledge graph", "layered view", "trace"
- "Chat path", "chat provider"
- "Chatham House rule", "CC BY 4.0", "Apache-2.0" (I can guess, but the pages do not explain them)
- "SCAT" (never expanded)
- "Tell scenarios" and "architectures"
- "Release level" (only "between private and public")

**Places where the two pages disagree or do not line up**
1. The flow says a solo reader can go "from step 2 to step 8", but the flow table says step 8 depends on steps 5 and 7 (capture). A solo reader on their own notes would have no step 7 as the flow describes it, so this is unclear.
2. Step 2 "Try" depends on "Setup, as in step 5", yet the solo path skips step 5 as well. Again, the dependency and the path do not agree.
3. The data page's checklist has 10 items. The numbered choices have 7. The checklist adds "participation terms told to participants", "licence", and "who holds the rights", which are not numbered choices. The rights item is also not a numbered choice in the text.
4. Flow step 4 lists participation terms, AI use, keeping and release, and commitments. It does not list rights holders or licence, which the data page treats as part of the same set.
5. Choice 4 (contributions use) says "Coding and analysis depend on it", but the flow table gives step 9 (analysis) only the dependency "a conformant vault", with no link back to step 4.

**Guesses I made (summary)**
- That step 4 must be complete before session 1 (not stated).
- That consent records live with the field notes (not stated).
- The repository host, and that it is a hosted git service (not stated).
- The meaning of the coding sub-steps and "conformant" (not defined).
- That inputs are kept outside the vault by default (stated only as "outside the tool").

**Overall confidence**
High on the order of the ten steps and which choices feed which steps. Low on the mechanics: how consent is recorded or withdrawn, what conformance means, how a version is tagged, and where inputs and analysis are kept by default.
The pages say "the page did not tell me" in these places. I did not fill those gaps with outside knowledge.
