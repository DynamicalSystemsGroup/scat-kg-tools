# How the team runs

This follows the tradespace org (`DynamicalSystemsGroup/tradespace`, `work-packages/PM-BRIEF.md`, Nov 2026), made
leaner. The formal structure here is settled and the work is simple, so the ACE answers most questions and very
little is escalated.

The mission's core heuristics govern every call made here: for the users, "make the right way the easy way"; for
the builders, "as simple as possible but no simpler".

## The chain

**Chief engineer → ACE → PM → workers to spec.** In agile terms: the chief engineer is the product owner,
the ACE is the product manager, the PM is the scrum master, and the workers are the team.

Workers report to the PM, the PM reports to the ACE, and the ACE reports to the chief engineer. No level is skipped.

| Role | Who | Model |
|---|---|---|
| **Chief engineer** | `mzargham` | — |
| **ACE** (assistant to the chief engineer, the driver) | The main Claude session | the main session's model |
| **PM** | One persistent subagent (`.claude/agents/pm.md`), spawned and managed by the ACE. It is swapped for a fresh PM when it slows or its context grows large. | Sonnet |
| **Workers** | Fresh subagents the PM instantiates per unit, each with one bounded task: spike, design, build, test, write, user-test, review | Sonnet, or Haiku for mechanical work. User testers run on the models UA-A sets. Opus only on the ACE's word, for a named reason. |

## Who answers what

- **The PM decides** how a unit is built inside its scope, the order of units, which worker owns which files,
  fixes to defects against a stated requirement, and procedural merge conflicts.
- **The ACE decides**:
  - writing and approving every work-package scope, and every work-package scope amendment, inside `MISSION.md`;
  - keeping `work-packages/plan.md`, the ordered work packages, within the orderings `MISSION.md` sets;
  - a detail a scope leaves open;
  - conflicts between packages over files or order;
  - dependencies (`pyproject.toml` and `uv.lock` are the ACE's);
  - whether a reported problem is a defect (fix it) or a question about the bar;
  - accepting each package on its own independent verification;
  - running a spike when the evidence for a call is missing.

  Every such call goes in `decisions/log.md` with its evidence, for the chief engineer's review at acceptance.
- **The chief engineer decides** two things only: the mission (and its amendments), and acceptance of the delivery,
  by merging the release PRs. Before then the ACE goes to him only for an **intent gap**, as `MISSION.md`
  (Governance) defines it. He gets one question at a time, with what was tried and a recommendation. His words are
  quoted verbatim in `decisions/log.md`.

**Escalation** (his words, from tradespace): "don't just stop and complain to me. interrogate and resolve if
possible, escalate to me only once there is no path forward that you can stand behind." This holds at every level:
find the cause, fix what can be stood behind, record it. Escalate with what was tried and the options left, not the
bare problem.

## The loop

1. The ACE writes a one-page scope for the next work package (`work-packages/WPn.md`, `scope-of-work` shape). The PM
   checks it against the scope rules below. The ACE approves it and logs the approval.
2. The PM splits the package into **units** and gives each one story points. Each unit has one tight scope and one
   set of files, and units with disjoint files run in parallel. The PM keeps `work-packages/board.md` current: every unit, its owner, branch,
   state and points; the velocity per iteration; and the forecast to the candidate (`MISSION.md`, Timeline).
3. For each unit, a worker builds it in its own worktree. A fresh reviewer then checks it against the requirements
   by running the stated checks. Defects against a stated requirement are fixed and re-reviewed without asking
   anyone.
4. The PM checks that the unit works with the rest, merges it into `dev` and pushes. Nothing waits uncommitted or
   unpushed. A red head on `dev` is fixed forward straight away by the unit that owns it.
5. The ACE verifies the package independently, accepts it, and revises `work-packages/plan.md` if the package taught
   something.
6. When the packages are in, the ACE runs the candidate stage (`MISSION.md`, Governance) and the UA-A rounds to their pass
   bar, writes the reviewer's guide (D-6), and opens the release PRs (`dev` → `main`). The chief engineer then does his
   walkthrough (UA-M). Anything he flags is fixed on `dev`. Only he merges.

The ACE creates `work-packages/` (with `board.md`) at the start of WP1. Work-package records stay there for v0.1.

## Scope rules (what the PM enforces)

Each scope must have:
- purpose, goals and non-goals, with no contradictions between them;
- deliverables at stated paths, each traced to a goal;
- requirements, each with a check a reviewer can run;
- a definition of good, and a concrete definition of good enough;
- a **blast radius**: the files it owns, and nothing else;
- nothing outside `MISSION.md`.

Bigger changes (a new mechanism, an ontology change, a new tool) are scoped in stages: spike, decide (the ACE),
build, quality control, integrate, and review the cascade to a clean merged state.

## Status reports

The chief engineer gets a periodic report: recently completed work, what is in flight and which actor is working on
it, and what is queued and what it is waiting on. The ACE builds it from `work-packages/board.md` and the git history
of `dev`, so the PM keeps the board's Units table true at every state change: actor, state, what a queued or blocked
unit is waiting on, and when each unit was done.

**Estimated and realized points.** Each unit is given estimated points when it is planned, and they are never
revised. When the unit lands, the PM scores its realized points on the same scale, from what it actually took: elapsed
time, revision and push-back cycles, and the worker's tool use. The PM records the basis in one line. Estimates and
realized points are expected to differ, and that's allowed: the gap is the data we learn from. Velocity is realized
points per wall-clock hour. The running ratio of realized to estimated points corrects the forecast. At each package
acceptance the PM notes which kinds of unit ran over or under, so the next estimates improve.

## Verification

- **Tier 0, the author, before each commit:** `uv run ruff check`, `uv run ruff format --check` and `uv lock --check`
  on the changed files, plus the tests mapped to them.
- **Tier 1, the PM, before pushing to `dev`:** the full suite.
- **Tier 2, the ACE, at each package acceptance and before the release PRs:** CI green on the exact commit, plus,
  once they exist, a clean-environment trial of the template and a browser pass over every rendered page.

**Reviews run the thing.** A reviewer runs the CLI on real vaults, opens the docs pages in a browser (desktop and
375 px), and opens the vault in Obsidian where the unit touches what a reader sees. Screenshots or pasted output go
in the review record. Reading the code or the Markdown is not a review. A reviewer without a browser says so and
does not sign off the rendered part.

## Limits

- Nothing outside the two repositories and the session scratchpad is changed.
- No merge to `main`, no tag and no publishing, except the chief engineer's merges, and the candidate stage and
  release steps that `MISSION.md` (Governance) assigns to the ACE.
- No edit to a test or record that weakens a requirement; a test changes only when its requirement changed by a
  recorded decision.
- No AI attribution anywhere.
- Stop and report rather than improvise when a step would cross a limit.

## Hygiene

- **Worktrees** are created explicitly (`git worktree add <path> -b <branch> dev`) outside the repository. Each one
  is removed (`git worktree remove`, then `git worktree prune`) as soon as its unit is pushed.
- **Branches are cleaned up periodically** (the chief engineer's guideline). A unit branch is deleted, locally and on
  `origin`, once it's merged. A package branch is deleted once the package is accepted. At each package acceptance
  the ACE checks that only `main`, `dev` and live work remain. Work that is abandoned rather than merged is kept as a
  tag under `archive/` before its branch is deleted.
- **No scratch** is left in the tree.
- **Negative edits are welcome.** Every piece of content must earn its place, including what is already there.
  When something is stuck, consider removing it before another round of rework.
- **State lives in files** (the board, the scopes, the log), not in conversation. A PM handover is: this file,
  `pm.md`, the board with its states true, the log, and the outgoing PM's one-page note. The outgoing PM finishes
  the units it has in flight and starts nothing new.

## User tests

AI user tests run exactly as `MISSION.md` (User acceptance, UA-A) defines: mostly Haiku testers, isolated clones, no
reading of `src/` or `tests/`, pasted output, and guesses counted as findings. The PM provisions the testers; the ACE
reads every report and dispositions the findings.
