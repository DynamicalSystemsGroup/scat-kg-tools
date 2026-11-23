# How the team runs

This org is deliberately lean. The formal structure is settled and the work is simple, so most questions are
answered by the ACE, not escalated.

## Roles

| Role | Who | Does | Never |
|---|---|---|---|
| **Chief engineer** | `mzargham` | Approves `MISSION.md` and its amendments; answers escalations; accepts v0.1 | — |
| **ACE** (assistant to the chief engineer) | The main Claude session | Writes and approves work-package scopes; answers the team's questions; accepts work packages; decides what reaches the chief engineer; keeps `decisions/log.md` | Widens the mission; accepts v0.1 |
| **PM** | Subagent, `.claude/agents/pm.md` | Process: holds scopes to the scope rules, writes work contracts, provisions workers, takes delivery, holds the merge gate, merges, resolves procedural conflicts | Decides design questions (they go to the ACE) |
| **Workers** | Subagents the PM instantiates per contract | One SDLC activity each: spike, design, programming, testing, writing, user testing, review | Merge, push, or work outside their blast zone |

## The loop

1. The ACE writes the next work package's scope (`work-packages/WPn.md`, from the `scope-of-work` template) inside the mission.
2. The PM checks it against the scope rules (below) and returns PASS or the items to fix. The ACE fixes them and approves it by logging the approval.
3. The PM splits the package into contracts and provisions a worker for each; the main session launches them.
4. Workers deliver on their branches. The PM runs the merge gate: an independent review on a different model, re-running the acceptance checks, and a diff that stays inside the blast zone. It then merges into the package branch.
5. The ACE reviews the package against its scope (`work-acceptance`), accepts it, merges the package branch into `main`, and revises the breakdown in `MISSION.md` if needed.
6. After WP6, the ACE prepares the v0.1 review and the chief engineer accepts or sends feedback.

## Scope rules (what the PM enforces)

Each scope must have:
- one clear, bounded intent;
- goals and non-goals that don't contradict each other;
- deliverables at stated paths, each traced to a goal;
- requirements, each with a check that a reviewer can run;
- a blast radius (the paths it may touch);
- a definition of good and a concrete definition of good enough;
- nothing outside `MISSION.md`.

## Questions and escalation

- A worker's question goes to the PM. The PM answers it if it's procedural; otherwise it goes to the ACE.
- The ACE answers from `MISSION.md`, the decision log and engineering judgement, and logs the answer.
- Only an **intent gap** goes to the chief engineer: a question that `MISSION.md` and the chief engineer's recorded statements don't settle, and that changes what is built or whether it serves its purpose. The chief engineer signs off on the mission scope and on the mission's delivery, and on nothing else. Escalations come one at a time, with a recommendation, while other work continues.

## Branches and records

- `main` is the integrated state. No direct edits to `main`, by anyone, ACE included: everything arrives through the merge gate.
- Each work package works on branch `wp<n>/<slug>`. Each task works on `wp<n>/<slug>/<task>`, in its own worktree outside the repository, created by the PM from a named base.
- Merges use `--no-ff`. Commits are plain, with no AI co-author trailers.
- Records:
  - `work-packages/WPn.md` holds the scope, contracts and review;
  - `decisions/log.md` holds the ACE's rulings and approvals;
  - `decisions/adr-*.md` holds toolchain decisions with evidence.

## Standing rules (lessons from earlier DSG projects)

- Create worktrees explicitly with `git worktree add`. Never rely on default harness isolation; it once started from a stale commit.
- Pin every worker's model in the launch. Author and reviewer run on different models.
- Probe before asserting: a claim about a tool holds only once it has been run, and the output is pasted.
- Never mask a check (`|| true` is banned). Report red as red.
- Simulated-user tests:
  - write the persona in the user's own words, not the tool's vocabulary;
  - use a different domain from the worked example;
  - use an isolated `git clone --no-hardlinks` with the remote removed;
  - forbid reading `src/` and `tests/`;
  - require pasted command output;
  - count what the user had to guess as defects.
