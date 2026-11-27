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

Run 1 (units U1 to U5, `dev` 932d3fb). Each unit read every page in its zone in full, not only the pattern hits.

| Zone | Hits found | Fixed | Kept, with reason |
|---|---|---|---|
| `docs/chat-path.md`, `docs/leave-no-trace.md` | 21 (P2, P5: warning boxes, "untested alternative", "lab run" x2, "first run is the real test", "one option") | all: boxes became "If a step fails"; one Docker Desktop line; status removed | none |
| Other `docs/` pages and `contracts/architecture.md` (symlinked as `docs/architecture.md`) | P4 21 (work-package, log and role names in the architecture page), P2 1, P5 3 ("stand-in for one person" in a script: another sense, reworded) | all; the architecture page's "Needed by" column and status words removed | "in one sitting" (ordinary English, not a test sitting) |
| Template example narratives, `docs/reference/api.md`, `cli.md` samples | 9 notes and source lines quoting "(D-nnn)" or "the decision log"; "Reason given in the record" | all; edges unchanged | none |
| `deploy/`, `skills/`, `contracts/assistant.md`, `src/scat_kg/` strings | 14 (launcher comments and dialog "recommended", test-override notes, `deploy/README.md` status list, WP and D numbers in code comments) | all; the status list removed | the assistant's rule keywords (P1) in `assistant.md` and `SKILL.md`; the mode rule in `checks/attribution.py`; "option" in fix messages (ordinary use) |
| CLI `--help` (25 commands) | 0 | none needed | none |

Not changed, with reason: the check, fix and operation messages (about 150 strings) and the MCP tool descriptions read
plainly and are pinned by tests; the `--json` help line "(machine-interface contract)" and the footer "REPL" are
pinned by the CLI reference's exact help output and by about 10 tests (a later finding if a tester trips on them).
