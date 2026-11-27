# Residue sweep (WP26-G1)

Prompt residue is wording that echoes how the work was explained to the agents, not what a coder needs (D-139), and
test or work status in a user page (D-146). The sweep reads every page a coder sees: `docs/`, the template's README,
`AGENTS.md` and example vault, `deploy/` messages, `skills/`, `contracts/assistant.md`, and the CLI's help and
messages. Words follow `GLOSSARY.md`. `git grep -E` on macOS has no `\b`: use `-w` or Python `re`.

## What counts as residue

1. **Deontic keywords** (SHALL, SHALL NOT, SHOULD, MUST, MAY) outside the assistant's rules, the skill and the
   catalogue's mode rule. A rule's keyword stays only there.
2. **Meta-talk** about options and recommendations beyond one plain line ("this is one policy option", "we recommend").
3. **Quoted instruction phrasing** ("as asked", "as instructed").
4. **Decision-log language**: "as decided", `D-nnn`, log numbers, "the decision log", work-package numbers, role names
   (ACE, chief engineer) in a user page.
5. **Test and work status**: what has or has not been tried, "untested", "the lab run of", "not recorded", "nobody has
   yet run", "stand-in", "first run is the real test". The page says what a coder does and what to do if a step fails.
6. **Design-conversation asides**: "we decided", "in this release", "candidate", "reviewer", "the sitting", "UA-A",
   "cold read", "spike".

A hit is **fixed** (rewritten for the reader, or removed) or **kept with a reason** (the word is plain English doing
its ordinary work, for example "candidate" for a candidate name in a vault, or a keyword in the assistant's rules).

## Patterns (Python `re`, case-insensitive; the test `tests/docs/test_residue_patterns.py` runs them)

| ID | Pattern |
|---|---|
| P1 | `\b(SHALL NOT\|SHALL\|SHOULD\|MUST\|MAY)\b` (case-sensitive) |
| P2 | `recommend\|one option\|policy option\|you may prefer` |
| P3 | `as instructed\|as asked\|as requested\|you were told` |
| P4 | `\bD-\d{3}\b\|decision log\|as decided\|\bACE\b\|chief engineer\|\bWP\d+` |
| P5 | `not been tried\|untested\|lab run\|not recorded\|nobody has yet\|first run is the real test\|stand-in\|not yet (run\|tried\|tested)` |
| P6 | `we decided\|we chose\|in this release\|reviewer\|the sitting\|UA-[AM]\|cold read\|\bspike\b` |

Scope of the test: `docs/*.md`, `docs/reference/*.md`, the template's text pages where a clone is present, `deploy/`
messages, `skills/`, every command's `--help`. Marked keeps live in the test's `KEPT` table, each with its reason.

## Record

(Filled in as the sweep runs: pattern, hits found, fixed, kept with reason.)
