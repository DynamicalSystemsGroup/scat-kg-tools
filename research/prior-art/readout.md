# Prior-art readout

Purpose: give the architecture (WP15) and the ontology and layout (WP16) the lessons of earlier work.
Each recommendation is traced to a mission goal or requirement; WP15 and WP16 decide.

Read prior art as a way of thinking, not as parts to carry over. Where a source uses "edge" in its own sense, this
readout says so; otherwise words follow `GLOSSARY.md`.

## Q1. How was work split between human and AI, and how was authority kept with the human?

**What the sources show.** The INCOSE paper has the assistant generate and analyse, while the author states that
architecture, questions and every accountability decision were his. It makes authority structural: the paper's edge
(a typed relation between documents) of the validation kind cannot exist without a named human approver, enforced by
a required field, a script matching approvers to a whitelist, and CI that blocks a merge when signer and approver
differ. ant-rdf says assertions about the field come from humans and structural correctness from the CLI. It lists
what the assistant must not do: make claims, auto-extract actants (the people and things in an ethnographic account) without confirmation, bypass dry-run, hand-edit
generated files, supply waiver reasons. Ingest lands as candidates for the human to confirm. assurances-audits-accountability
tells its assistant not to sign validations, but its `signed_by` field is optional, so nothing forces it. Earlier
private work found the same: a rule that the assistant prepares and the person signs held only once a field and a
check enforced it, and that each approval had to be traceable to a named person.

**Keep.** A required field naming who confirmed, plus a check that fails without it. Machine output that arrives as
a candidate for the human to confirm, never as a finished result. A written list of what the assistant may not do.

**Leave.** Identity whitelists, git-commit-as-signature and CI signer matching: they serve many approvers across an
organisation, and the organiser starts alone. Optional authority fields.

**Recommendation (G14, R-19).** Make the coder's authority something the tool enforces, not a house rule: only the
coder's act sets `done`, no tool command or assistant path writes it, and the tool refuses `done` while the check
fails. Put the assistant's permitted and forbidden acts in one short file the tool's docs and the assistant's
instructions both cite. Every path (alone, tool-assisted, assistant-assisted) goes through the same fields, so a
project with no assistant loses only speed.

## Q2. How were model, view and control separated, and what loops ran?

**What the sources show.** The paper uses no model-view-controller words. It gives its own four layers (not the glossary's) and
seven functions, and a loop of generate, verify, evaluate, validate: a failed check returns to generation for structure, a failed
validation returns for content. Its automation re-propagates changes after merges. ant-rdf has the explicit split:
the model is the ontology plus its validation rules, the control is the `ant` CLI, the views are briefs and a wiki that are
generated and never hand-edited. Its loop runs description, CLI, deterministic output, check, regenerate views, human
reviews the rendered view, accept or revise in their own words. CI regenerates everything and fails on any diff.
knowledgecomplex hides its formal machinery behind a Python package and runs validation on every write with
rollback. assurances-audits-accountability treats a chart page as a stored query, that is, a view. Earlier
private work found that derived views were trusted and hand-kept ones went stale, and that checks drifted from the
written rules until they came from one rule source.

**Keep.** The three-way table, stated on one page. Views generated after each passing check, never edited. A CI step
that regenerates and fails on a diff. Two return paths in the coding loop: tool failure back to coding, doubt about
content back to interpreting.

**Leave.** Layer and function taxonomies, the two-by-two of formal languages, query languages exposed to users,
re-propagating edits automatically.

**Recommendation (G16).** WP15 should state model, view and control in a table of a few lines, make the ontology file
the single source from which checks are generated, regenerate every view after each passing check, and add the
regenerate-and-diff gate to the tool's own tests.

## Q3. How were vaults laid out in Obsidian, and how were links and edges kept in step?

**What the sources show, and where they are silent.** Only knowledgecomplex writes pages for Obsidian: one Markdown
file per element, fields for identity and attributes, `##` sections for prose, all of knowledgecomplex's edges (elements joining two vertices, not the glossary's edge) in one flat directory. It
writes no links, so which vertices an edge joins lives only in the graph; its sync reports a missing file, an orphan
file or what it calls an attribute mismatch. ant-rdf generates a flat wiki of kind-prefixed pages with plain links, and a test
checks every internal link; link and edge agree because the pages are generated from the graph. A flat layout was
adopted to fix broken links. assurances-audits-accountability is a package with example content, not a committed
vault. It uses numbered folders by dimension, one page per entry, and its edge pages (the package's own typed connections) hold their ends as id strings in
fields. Its guidance asks for links and file names equal to ids; its own example does neither, which is a gap
between guidance and example. No source says how hand-written links and edges were kept in step: the answer comes
from generation by construction, from the broken links, and from earlier private work, where numbered folders and id
prefixes helped navigation only while file names matched ids, and nested embeds grew noisy as items grew.

**Keep.** One page per entry, content in fields and prose sections. File name equals id equals link target. Index pages
generated by the tool. Numbered or prefixed ids, kept honest by a check. A test that every link resolves.

**Leave.** Nested embeds beyond one direction. Prose that restates structure in a page body (it goes stale). Any layout
the architecture cannot show in Obsidian alone.

**Recommendation (G15, G17, R-21, R-23).** Treat links and edges as unsolved by prior art: it offers no tested pattern
for hand-coded links, so the spike must produce one. Until then: file name equals id, a page's body never restates
what another page's fields already hold (R-21), index pages are generated, and the tool reports each mismatch in the
closed list of R-23 with a fix. Give WP16 the assurances-audits-accountability guidance-versus-example gap as a test case.

## Q4. How was machine verification kept apart from human validation?

**What the sources show.** The paper makes verification automated and binary and validation a human judgment with a
signature, and adds a machine "evaluate" step that writes a report for the human. CI checks that a signature exists,
not that the judgment was good. ant-rdf is plainest: violations that break the check cannot be waived; warnings can be
waived with a human's justification, kept append-only; lint stays advisory; CI fails on warnings only when asked.
Its planned human testing regime is not yet run. In assurances-audits-accountability the example has a person tick
the verification checklist, so the machine's run and the human's tick are easy to confuse; a documented accountability
command is absent from the code. Earlier private work found that keeping the machine's findings and the person's judgment apart, with different owners, was
clearest, and that it broke when the two were mistaken for each other. The paper's own audit reported 85.7% instead
of 100% because it inferred targets from naming conventions.

**Keep.** Errors that block and cannot be waived, warnings that can be waived with a coder's recorded reason. Separate
fields for what the tool found and what the coder confirmed. Explicit fields instead of inference from names.

**Leave.** Assurance triangles, coverage percentages, a separate evaluate stage, signed attestations.

**Recommendation (R-1).** Keep the tool's report and the coder's confirmation in different places with different
writers: the tool writes a report on every run; the coder's `done` is a separate act on the page. Grade rules as
error or warning, require a coder-written reason to waive a warning, and let no rule read content or infer
anything from a name.

## Q5. What went wrong or was abandoned, and why?

**What the sources show.** ant-rdf deferred temporality, multiple graphs, rule-based tagging and prose parsing, and
holds a rule of "no speculative features"; unbuilt parts raise an error instead of pretending. It names the risk that
a toolkit changes what it amplifies. The paper's assistant-driven forward propagation caused edit cascades, and
self-referring foundations produced degenerate results until an axiomatic root was added; its evidence is one
self-demonstration with no user testing, and it says scaling is uncharacterised. assurances-audits-accountability
shows large purges of code, stale docs and a stale test README, and limits it lists itself: no time-ordered
revisions, no partial assurance. Earlier private work found that development scratch piled up beside content and cost more to purge than to keep out,
that docs went stale after refactors, and that overlapping doc trees with a mixed audience duplicated each other.

**Keep.** Deferral recorded as a decision. Failing loudly on unbuilt features. Regression tests before any automated
change touching many entries.

**Leave.** Formal machinery a note-taker never touches: simplicial boundary rules, Betti numbers, PageRank,
named graphs, provenance alignments, query templates, a server layer shipped before the CLI is solid. Time-ordering,
partial assurance and automatic cascades: out until a package asks for them.

**Recommendation (the builders' heuristic, "as simple as possible but no simpler", MISSION.md; R-1 for the checks).** Build the smallest set that
carries the three actors and the two checks. Add a test that every command a doc names exists; keep scratch outside
the repository's tracked content; give each doc tree one audience; never let the assistant rewrite entries the coder
has marked `done`. Where a source's formal result is the reason for a rule, copy the rule, not the machinery.

## Sources

| Source | What was read |
|---|---|
| INCOSE IS 2026, "Formalizing Document Assurance: A Topological Framework for Verification, Validation, and Human Accountability", M. Zargham | The full 14-page paper |
| ant-rdf, Zargham and Rennie, https://github.com/mzargham/ant-rdf | README model-view-control table, CLAUDE.md, decision records, future-work notes, the wiki generator and its tests, git history |
| knowledgecomplex 0.2.0, https://github.com/DynamicalSystemsGroup/knowledgecomplex | The Markdown codec, the audit code, and the repository's stated design notes |
| assurances-audits-accountability, Zargham, https://github.com/DynamicalSystemsGroup/assurances-audits-accountability (the mission's link; v1.0.0 as read) | Package source, the paper-authoring example content, assistant guidance, git history |
| earlier private work | Principles only |
