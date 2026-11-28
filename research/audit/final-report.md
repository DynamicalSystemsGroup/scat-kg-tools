# WP40 final report: what the chief engineer decided, and why

**This is the direction.** It records the chief engineer's decisions from the WP40 audit (decisions/log.md D-216 to
D-238), each with his reason in his own words. The [readout](readout.md) and the [reviews](reviews/) are background.
Where a reviewer proposed a cut that is not listed here as decided, it was **not** adopted. Do not act on a reviewer's
verdict. Act on this page and the log.

## The purpose every package is tested against

In the chief engineer's words (D-230): "this whole exercise is one where humans telling their own accounts of their own
experiences, provides the details. the coding work is to organize many detailed things into an expression of common
patterns. our tool + facilitation and planning provides the metamodel; then the humans at the events provide the
details and those details are captured as field notes and organized into narratives which are then coded. coding
focuses on identifying and interrelating common elements. this is the purpose of what we're doing. the resulting output
is a synthesis. that is why it requires human judgement: synthesis is interpretive; recognizing two things that look
different are structurally the same, or that two things that sound the same are structurally different requires human
intuition. our metamodel (ontology) provides the language for describing structure so the human coder can draw out
those patterns."

**The two tests for any change:**
- Does it help organize detail into patterns?
- Does it push toward more detail? The tools must not.

**What went wrong.** In his words: "working with the LLM to build this caused a tendency to add detail and to ask for
details".

**Structure is not clutter.** He also said the reviewers were "thinking like coders and user. none like systems engineers"
(D-218). The lifecycle state machine and a tight ontology are "the scaffolding that breaks the problem into simple
peices. keeping it and having a tight ontology that is respected across the lifecycle is what allows all the other
pieces to be simple." Judge a part by what it holds up, not by how much of it there is.

## What stays, and why

These were proposed for cutting and are kept. Each reason is the intent the part serves; keep it in view.

| Part | Kept because (his words) | Log |
|---|---|---|
| The lifecycle stages, `lifecycle.toml`, the stage tools and refusals | "what makes it possible to stabilize the behavior ... the scaffolding that breaks the problem into simple peices" | D-218 |
| Attribution: three modes, contributor pages, `attributed_to`, the ATTR rules and view | "minimalist structure for distinguishing two modes ... one that involves activists that needs to explicitly reject named contributions and one for a community that explicitly wants to surface and track contributions. this dimension is there to protect that variety" | D-219 |
| The table's `type` column | "the type of node provides important semantic information and the names of the types are literally the description of what from-to means" | D-222 |
| Structured fixes (fix kinds, edits, the JSON schema) | "this is what makes the right way the easy way ... like a mini ci/cd framework for the content ... every check has a gaurd and a remediation, with clear instructions to returned to the AI assistant, including clarity about what is conformance and what is coder judgement is central to the architecture" | D-226 |
| ASCII slug names | Chosen: "Keep ASCII slugs"; the `title` carries the label as said | D-228 |
| Every command except two (below) | "keep the rest as built" | D-227 |
| The chat-path setup as built | "Say a helper is needed" | D-232 |
| The narrative-to-node link page (C22) | "keep this as decided but these are not required pages. they are optional ... its a slot to address notes not a required page" | D-233 |

## What changes, and why

| Change | Why (his words, or his choice) | Log | Package |
|---|---|---|---|
| The S layer is the **stakeholder** everywhere: class, key, folder, `type:`, cap key, docs, template, tests; existing vaults migrated | "its supposed to be stakeholder, calling it group breaks the acronym ... full rename. i asked for this earlier but it seems you lost it" | D-237 | WP41 |
| The TTL holds the model only | "Strip to the model" | D-231 | WP42 |
| One id per rule, severity set by status; TABLE-SECOND, TABLE-DUPLICATE, MENTION, SUGGEST-CONFIG cut | "Merge twins and cut four" | D-223 | WP43 |
| **The table is the coding of record.** Prose links are optional, and those made are a subset of the table's nodes (warning in draft, error at done) | "the tables are the coding of record. linking the prose is desired but not required ... the prose links should be a subset (potentially empty) of the table. the table is structural ... the prose is interpretive and connective tissue" | D-220, D-221 | WP39 (amended) |
| Merge synthesizes one node: no carried body, git keeps the history | "there should only be one node ... letting the git history do that work ... the expected behavior is to synthesize them into one node" | D-216 | WP44 |
| An optional narrative-to-node link page for notes; the assistant is guided on every note slot | "think of this as reifying that narrative to node edge with space for notes ... we should ensure the assistant get guidance for where, when and how to put notes in the addressed slots" | D-216, D-233 | WP44 |
| `rename`, a recurrence view, `where-used` (was `split-plan`), `copy-share` cut, `review` on plain signals | "guide page and rename"; "Separate view"; "rename it where-used"; "Cut copy-share; plain review" | D-230, D-229, D-227, D-225 | WP44 |
| A sixth stage, **`synthesise`**, between code and analyse | "it almost seems like we're missing a stage between code and analyze that is focused on exactly this activity" | D-235 | WP45 |
| The template starts in `plan`; the stage holds at the same strength on every path | His choices (a) and (b) | D-234 | WP45 |
| **Roles replace authority tables.** The organiser is accountable; each role's responsibility is set per stage | "the organizer is the project lead the (Accountable) for the whole project ... reorganize this as roles. describe what each role is responsible for in each stage. the Organizer remains responsible for ensuring overall project success (and making good on any promises regarding data use, release, retention, attribution, etc)" | D-234 | WP45 |
| `timeframe` becomes actual / hypothetical / unclassified; it and `kind` are analysis filters that gate nothing and change no output silently | "the filter we need is to tease apart things people are actually only conjecturing versus facts about the world that could be independently verified ... we cannot strictly force the narratives into these buckets but we're guiding them" | D-224, D-238 | WP46 |
| The verified contradictions are settled by the contracts | "Yes, one package" | D-236 | WP47 |
| A guide page on patterns, synthesis and abstraction ("broken drill" to "unsafe equipment"); a docs pass; core glossary terms | "i think these concepts of patterns, synthesis and abstraction where what was missing ... we will need to go back through the documentation to make sure this is clear"; ""synthesis", "abstract vs concrete" and "pattern" OR similiar may need to make it into the core glossary" | D-230, D-232 | WP48 |
| Structured fixes reviewed item by item against their purpose | "i am okay with an itemwise review of this to make sure what is there is doing its job" | D-226 | WP49 |

## Guidance for the agents doing this work

- **Default to the decision, never the review.**
- **A request that names a term applies across the whole vocabulary** (D-237).
- **Don't reverse a newer decision with an older one** (D-238).
- **Every addressed slot for notes is optional:** the row note, the relationship annotation, the link page. None adds a
  required page or field.
- **Never propose more detail, more required fields or more links.** Propose structure that helps a person see a pattern,
  and keep the stages and the ontology tight.
