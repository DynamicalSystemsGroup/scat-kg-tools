# RS5-G1: the smallest sufficient form for the lifecycle

Lead: a flat machine is enough. One current stage (or `unknown`), a table of stages, a table of named moves, and a table of named predicates. Hierarchy, concurrency, history and timers are not needed for a lifecycle of about ten steps. The sources agree that loops are the norm, the stop is a person's judgement, backward moves are explicit, and a default is needed when no rule fires. Source tags [S1] to [S21] are in the table at the end.

## Findings by source family

### (a) Qualitative-analysis cycles

- **Loops without a built-in end.** The hermeneutic circle moves between part and whole and has no firm start; the stop is the interpreter's judgement, and no external judge is named [S1]. Saldaña says coding is cyclical: first-cycle codes are revisited, merged, relabelled or dropped in later cycles [S2]. Principle: a backward move from a later pass to an earlier one is ordinary, not an error.
- **Stop is judged, not computed.** Grounded theory's saturation is the stopping idea, but Bowen finds explicit guidelines for it almost nonexistent and asks researchers to explain how they judged it [S3]. Principle: "enough" is a request predicate (the coder's word), never a detection.
- **Sequential but recursive.** Braun and Clarke give six phases, say analysis moves back and forth between them, and say experienced analysts blur phases [S4]. Principle: forward order is the default path; do not forbid moves just because they skip a phase, but name each allowed move.

### (b) Action research and design research loops

- **Fixed cycle, repeated.** Action research is described as plan, act, evaluate, then plan again [S8]; Susman and Evered's five phases (diagnose, plan, act, evaluate, specify learning) are known to me only through secondary summaries [S9]. Principle: the cycle closes by returning to an earlier stage, and the last stage records what was learned.
- **No fixed entry.** Kolb's four modes can be entered at any point and are followed in sequence [S5]. The design science process model names four entry points and allows iterating back from evaluation [S7]. Hevner et al. describe build and evaluate as a loop run several times before the final artefact [S6]. Principle: a coder may arrive mid-lifecycle, so the machine needs an honest `unknown`, not an assumed start.
- **Who decides.** In all four the researcher or practitioner decides to iterate or stop; none computes it [S5][S6][S7][S8]. Boyd's OODA loop is left out: I did not read it and it adds no gating idea.

### (c) Workflow and process state machines

- **States and transitions are explicit; backward is a separate move.** Jira workflows allow a move only if a transition exists, transitions run one way, and a move back needs its own transition [S11]. Stage-Gate has stages that produce deliverables and gates that test them; a gate ends in go, kill, hold or recycle, where recycle means repeat the earlier stage; a group of gatekeepers decides [S15]. Principle: backward moves are listed moves with their own rules, not "undo".
- **Guards sit on moves.** Statecharts: a guard is a condition on a transition, false means ignored [S10]. BPMN: each outgoing flow carries its own true-or-false condition, a default flow is taken when none holds, and with no default the process stops [S13]. Principle: an unmatched case must have a defined result; this is our `unknown` stage and our clarification result.
- **Who triggers.** CMMN: a sentry guards entry or exit of an item; an item with manual activation waits for a person to start it [S12]. LangGraph: routing functions decide by code; a person enters through an interrupt [S16]. Jira separates validation and condition rules from other behaviour on a transition [S11]. Principle: a move needs two things, a condition (machine-checkable or not) and a trigger (person or program); keep them apart.
- **Soundness.** Workflow nets require a start and an end, every task on a path between them, guaranteed termination and no dead tasks, checkable on the graph [S14]. Principle: a plain reachability check over our own table gives the useful part, without Petri nets.
- **Extras are separate.** Statecharts add hierarchy, parallel regions, history, entry and exit actions and timed transitions to flat machines [S10]; Harel's original could not be fetched.

### Agents: tool restriction per stage

- **Gates between steps are programmatic checks; start with the simplest workflow** [S17].
- **The protocol can change a tool list.** The MCP server may announce a changed tool list and the client re-lists; execution errors travel in the result [S18]. Whether clients honour it is G4, not read here.
- **Harness restriction is per turn.** In Claude Code a skill can pre-approve tools or remove tools, and both clear at the next message [S19]. So the harness cannot hold a stage across turns; the stage must live in our data.
- **Sequence rules exist and are heavier than we need.** Agent-C checks tool calls against time-ordered rules with a solver [S20]; another paper derives rules on tool-call sequences, with labelled tools [S21]. Both are about safety, not lifecycle.
- **"Tool restriction as enabling constraint": no formal literature found** under that name in one search; the nearest results are S20 and S21. That is a gap, not evidence of absence.

## The smallest sufficient form

Argument. D-162 needs stage-scoped content, forward and backward moves, two kinds of predicate, an unknown stage, and an answer for a call the tool cannot place. A flat machine with a move table carries all of that. The sources that carry more (hierarchy, regions, history, timers) do so for state explosion or time; ten steps have neither problem. The harness evidence says the stage must live in a table the server holds [S19].

**The tuple, in plain words.** A stage machine is a list of stages, a list of moves, a list of predicates, and one current stage.

1. **Stages.** A fixed list of names, plus the reserved name `unknown`. Each stage lists: the inputs it expects (which pages, fields or arguments), the outputs it should leave (pages changed, checks passed), the tools allowed in it, the prompt text for it, and the skill sections that apply. All of these are plain lists of names or paths; no logic lives in a stage.
2. **Moves.** Each move has a from-stage, a to-stage, a direction (forward or back), a name, and the names of the predicates that must hold. Backward moves are listed one by one, as forward ones are. There is no "go anywhere" move except into and out of `unknown`.
3. **Predicates.** Each predicate has a name, a mode, and a question. Mode `detect`: the tool evaluates it, read-only, and answers true, false, or the reason. Mode `request`: the tool cannot evaluate it, so it returns the question to the coder, and the coder's answer is recorded. A predicate never changes anything.
4. **Current stage.** One value, held by the server in data (not in the model's memory and not in the harness), or carried on the request. If absent or not in the list, it is `unknown`.
5. **Triggers.** The coder says "move" (the person is the trigger). The tool may suggest a move when every `detect` predicate holds, and refuses it when one fails. Only the coder answers `request` predicates. The assistant holds no authority over any move.
6. **Unknown.** In `unknown` the only allowed tools are those that read and report the current stage and list the stages. Any other call, or any call outside the current stage's tools, returns a clarification result: the stage it sees, the stage list, and the legal moves from here. Nothing is executed.
7. **Entry.** On entering a stage the tool returns that stage's prompt and tool list; nothing else happens.

Checks on the table: every stage is reachable, every stage can reach the last, each tool named exists. This is the useful core of soundness [S14].

How this maps to SCAT without choosing it. The ten steps are the likely stage list; Analyse back to Code and done back to draft are two backward moves. A narrative's status (stub, draft, done) is data on a page and is not the stage; "done" stays the coder's attestation, so the move to it is a `request` predicate, plus a `detect` predicate that the check passes. Whether stage is per vault or per narrative is not decided here.

## What each extra feature would cost

- **Hierarchy (stage inside stage).** Gains shared tools and prompts. Costs inheritance rules and entry and exit at several levels [S10]. SCAT test: the coding loop (interpret, author, code, review) is four substeps. A flat design can treat them as one stage whose prompt names them, or four stages; hierarchy is not needed either way. A short shared list of always-allowed tools covers the one benefit.
- **Concurrency (orthogonal regions).** Costs a product of states and a rule for how regions interact [S10]. SCAT test: several narratives progress independently, but each narrative's progress is its status, which is data. Needed only if the stage must differ per narrative at the same time; that is not known.
- **History states.** Return to the last substate.  SCAT test: "Analyse back to Code" must return to a narrative, but which narrative is a field of data, not a stage memory. Not needed.
- **Timers.** Costs a clock, non-repeatable behaviour and tests that wait. Nothing in SCAT is time-driven; the coder is human-paced. Not needed.
- **Guards with side effects.** Costs predictability: a predicate evaluated twice (once to suggest, once to move) would act twice, and a refused move might still change the vault. BPMN and Jira keep conditions apart from other behaviour on a transition [S11][S13]. Keep predicates pure; if actions on a move are ever wanted, make them a separate named step run only after the move is accepted.

## Not known

- Whether the lifecycle is better as about ten stages or with the coding loop split further; the sources do not say.
- Whether stage is per vault, per narrative or per session. Concurrency cost depends on it.
- Whether stage is better carried on each request or held by the server (G3), and whether clients honour a tool-list change (G4); S18 gives only the protocol side.
- Whether any formal literature treats tool restriction as an enabling constraint; one search found none.
- Whether the weakly sourced items hold: Susman and Evered [S9] was not read; Harel's original was not read; Stage-Gate [S15] is a summary of Cooper, not Cooper; the hermeneutics authors [S1] were not checked on the page.
- Whether this structure helps weaker models stay on track; S17 argues for simplicity but is not evidence about our case.

## Sources

| Tag | Title | Author | Year | URL | Accessed | Principle taken |
|---|---|---|---|---|---|---|
| S1 | Hermeneutics (SEP entry) | Authors per entry, not re-checked | rev. | https://plato.stanford.edu/entries/hermeneutics/ | 2026-11-27 | Loop with no firm start or stop; judgement is the interpreter's |
| S2 | The Coding Manual for Qualitative Researchers (front matter, ch. 1 excerpt) | Johnny Saldaña | 2009 | https://cfacaa.human.cornell.edu/dea.arl/linked docs/Coding Manual_excerpts.pdf | 2026-11-27 | Coding is cyclical; recoding revises earlier codes |
| S3 | Naturalistic inquiry and the saturation concept: a research note | Glyn A. Bowen | 2008 | https://study.sagepub.com/sites/default/files/Bowen_2008.pdf | 2026-11-27 | Saturation as stop, with almost no explicit guidance; must be explained |
| S4 | Doing reflexive TA (companion to the 2006 paper) | Virginia Braun, Victoria Clarke | web page, undated | https://www.thematicanalysis.net/doing-reflexive-ta/ | 2026-11-27 | Sequential phases with back-and-forth; phases may blur |
| S5 | Experiential Learning, ch. 2 The Process of Experiential Learning | David A. Kolb | 2014 (2nd ed.) | https://astec.arizona.edu/sites/default/files/2024-08/Kolb_ProcessOfExperientialLearning.pdf | 2026-11-27 | Four-mode cycle entered at any point |
| S6 | Design Science in Information Systems Research | Hevner, March, Park, Ram | 2004 | https://www.in.th-nuernberg.de/professors/Holl/Personal/Hevner_DesignScience_ISRes.pdf | 2026-11-27 | Build-and-evaluate loop iterated before the final artefact |
| S7 | A Design Science Research Methodology for Information Systems Research | Peffers, Tuunanen, Rothenberger, Chatterjee | 2007/08 | https://wise.vub.ac.be/sites/default/files/thesis_info/Design_Science_Research_Methodology_2008.pdf | 2026-11-27 | Four entry points; iterate back from evaluation |
| S8 | Action Research in the Academy: Why and Whither? | David Coghlan | 2004 | https://mural.maynoothuniversity.ie/id/eprint/20206/1/2004%20issue%202%20article%201.pdf | 2026-11-27 | Action research as plan, act, evaluate, then plan again |
| S9 | An Assessment of the Scientific Merits of Action Research (not read; via search summaries) | Susman, Evered | 1978 | https://sswm.info/node/4959 | 2026-11-27 | Five-phase cycle ending in specifying learning (secondary only) |
| S10 | What is a statechart (statecharts.dev) | Site authors not stated on page | undated | https://statecharts.dev/what-is-a-statechart.html | 2026-11-27 | Guards; hierarchy, regions, history, entry/exit, delayed transitions as extras over flat machines |
| S11 | Work with issue workflows (Jira Cloud) | Atlassian | undated | https://support.atlassian.com/jira-cloud-administration/docs/work-with-issue-workflows/ | 2026-11-27 | One-way transitions; back needs its own; condition and validation rules |
| S12 | CMMN (Flowable open source docs) | Flowable | undated | https://www.flowable.com/open-source/docs/cmmn/ch06-cmmn | 2026-11-27 | Sentries guard entry and exit; manual activation waits for a person |
| S13 | Exclusive gateway (Flowable BPMN reference) | Flowable | undated | https://documentation.flowable.com/latest/model/bpmn/reference/exclusive-gateway | 2026-11-27 | Conditions on outgoing flows; default flow; process stalls with none |
| S14 | The Application of Petri Nets to Workflow Management | W. M. P. van der Aalst | 1998 | https://users.cs.northwestern.edu/~robby/courses/395-495-2017-winter/Van Der Aalst 1998 The Application of Petri Nets to Workflow Management.pdf | 2026-11-27 | Soundness: start, end, every task on a path, termination, no dead tasks |
| S15 | REF-010 Stage-Gate Systems (summary of Cooper 1990, AIWG) | Summarises R. G. Cooper | 1990 | https://unpkg.com/aiwg@2026.2.11/docs/references/REF-010-stage-gate-systems.md | 2026-11-27 | Gate decisions go/kill/hold/recycle; deliverables per stage; people decide |
| S16 | Graph API overview (LangGraph) | LangChain | undated | https://docs.langchain.com/oss/python/langgraph/graph-api | 2026-11-27 | Nodes work, edges route; code routing vs human interrupt; do not mix static and dynamic |
| S17 | Building effective agents | Anthropic | 2024 | https://www.anthropic.com/engineering/building-effective-agents | 2026-11-27 | Programmatic gates between steps; start with the simplest workflow |
| S18 | MCP specification, Tools (2025-06-18) | Model Context Protocol | 2025 | https://modelcontextprotocol.io/specification/2025-06-18/server/tools | 2026-11-27 | List-changed notice; execution errors in results |
| S19 | Skills (Claude Code docs) | Anthropic | undated | https://code.claude.com/docs/en/skills | 2026-11-27 | Tool grants and removals last one turn, so stage must live elsewhere |
| S20 | Enforcing Temporal Constraints for LLM Agents (arXiv 2512.23738) | Kamath et al. | 2025 | https://arxiv.org/abs/2512.23738 | 2026-11-27 | Order rules checked on tool calls; heavier than needed (abstract only) |
| S21 | Towards Verifiably Safe Tool Use for LLM Agents (arXiv 2601.08012) | Doshi et al. | 2026 | https://arxiv.org/abs/2601.08012 | 2026-11-27 | Rules over tool-call sequences, labelled tools (abstract only) |
