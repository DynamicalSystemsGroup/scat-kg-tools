# How the team runs

This follows the tradespace org (`DynamicalSystemsGroup/tradespace`, `work-packages/PM-BRIEF.md`, Nov 2026), made
leaner. The formal structure here is settled and the work is simple, so the ACE answers most questions and very
little is escalated.

## The chain

**Chief engineer → ACE → PM → workers to spec.** Workers report to the PM, the PM reports to the ACE, and the ACE
reports to the chief engineer. No level is skipped.

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
  - writing and approving every work-package scope and amendment inside `MISSION.md`;
  - a detail a scope leaves open;
  - conflicts between packages over files or order;
  - dependencies (`pyproject.toml` and `uv.lock` are the ACE's);
  - whether a reported problem is a defect (fix it) or a question about the bar;
  - accepting each package on its own independent verification;
  - running a spike when the evidence for a call is missing.

  Every such call goes in `decisions/log.md` with its evidence, for the chief engineer's review at acceptance.
- **The chief engineer decides** two things only: the mission (and its amendments), and acceptance of the delivery,
  by merging the release PRs. Before then the ACE goes to him only for an **intent gap**: something that contradicts
  his recorded words, or a trade-off his words don't settle that changes what is built or whether it serves its
  purpose. He gets one question at a time, with what was tried and a recommendation. His words are quoted verbatim
  in `decisions/log.md`.

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
5. The ACE verifies the package independently, accepts it, and revises the breakdown in `MISSION.md` if the package
   taught something.
6. When the packages are in, the ACE runs the candidate stage (`MISSION.md`, Governance) and the UA-A rounds to their pass
   bar, writes the reviewer's guide (D-6), and opens the release PRs (`dev` → `main`). The chief engineer then does his
   walkthrough (UA-M). Anything he flags is fixed on `dev`. Only he merges.

The ACE creates `work-packages/` (with `board.md` and `INDEX.md`) at the start of WP1.

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

## Verification

- **Tier 0, the author, before each commit:** `uv run ruff check`, `uv run ruff format --check` and `uv lock --check`
  on the changed files, plus the tests mapped to them.
- **Tier 1, the PM, before pushing to `dev`:** the full suite.
- **Tier 2, the ACE, at each package acceptance and before the release PRs:** CI green on the exact commit, a
  clean-clone trial of the template, and a browser pass over every rendered page.

**Reviews run the thing.** A reviewer runs the CLI on real vaults, opens the docs pages in a browser (desktop and
375 px), and opens the vault in Obsidian where the unit touches what a reader sees. Screenshots or pasted output go
in the review record. Reading the code or the Markdown is not a review. A reviewer without a browser says so and
does not sign off the rendered part.

## Limits

- Nothing outside the two repositories and the session scratchpad is changed.
- No merge to `main`, no tag and no publishing, except the chief engineer's merges and the candidate stage defined
  in `MISSION.md` (governance), which the ACE carries out.
- No edit to a test or record that weakens a requirement; a test changes only when its requirement changed by a
  recorded decision.
- No AI attribution anywhere.
- Stop and report rather than improvise when a step would cross a limit.

## Hygiene

- **Worktrees** are created explicitly (`git worktree add <path> -b <branch> dev`) outside the repository. Each one
  is removed (`git worktree remove`, then `git worktree prune`) as soon as its unit is pushed.
- **No scratch** is left in the tree.
- **The repository holds the present; git holds the history.** A package's scratch, spike workings and raw reports
  leave the tree when it is accepted (the readouts and decision records of deliverable D-5 stay), recorded in `work-packages/INDEX.md` with the commits where its scope was approved and
  its result accepted.
- **Negative edits are welcome.** Every piece of content must earn its place, including what is already there.
  When something is stuck, consider removing it before another round of rework.
- **State lives in files** (the board, the scopes, the log), not in conversation. A PM handover is: this file,
  `pm.md`, the board with its states true, the log, and the outgoing PM's one-page note. The outgoing PM finishes
  the units it has in flight and starts nothing new.

## User tests

AI user tests run exactly as `MISSION.md` (User acceptance, UA-A) defines: mostly Haiku testers, isolated clones, no
reading of `src/` or `tests/`, pasted output, and guesses counted as findings. The PM provisions the testers; the ACE
reads every report and dispositions the findings.
