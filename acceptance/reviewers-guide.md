# Reviewer's guide for the chief engineer (D-6)

*Four short sittings, taken one at a time.*

Read one sitting, tick its boxes, stop. Each sitting has one entry point. Nothing here asks you to trust a claim: every
claim names a command to run or a file to open. Paths are from the root of `scat-kg-tools`. Facts were checked on `dev`
at `PIN-PENDING`. The tools' candidate commit (the last commit that changed `src/` or `docs/`) is `PIN-PENDING`, and
the template's `dev` is `PIN-PENDING`, which pins it. Check both before you start:
`git log --first-parent -1 --format=%h -- src docs` prints `PIN-PENDING`, `git diff PIN-PENDING dev -- src docs` prints
nothing, and `git ls-remote https://github.com/DynamicalSystemsGroup/scat-kg-template refs/heads/dev` shows `PIN-PENDING`.

Terms: J1 to J7 (the user journey), UA-A and UA-M (the AI tests and your walkthrough) are in `MISSION.md`, "User
acceptance". R-1 to R-15 are in `MISSION.md`, "Requirements". The ACE and your sign-offs are in `MISSION.md`,
"Governance". The PM (project manager agent) is in `ORG.md`.

| Sitting | Entry point |
|---|---|
| 1. The end-to-end walkthrough | `acceptance/walkthrough.md` |
| 2. The docs site | https://dynamicalsystemsgroup.github.io/scat-kg-tools/ |
| 3. The tools and checks | the command block at the head of sitting 3 |
| 4a. The ACE's calls | the table in sitting 4a |
| 4b. What is known to be weak | the list in sitting 4b |
| 4c. The checkpoint, the conformance principle and the rule audit | the section "Sitting 4c" |

Sittings 4a, 4b and 4c are one sitting in three parts.

---

## Sitting 1. The end-to-end walkthrough (UA-M)

**Entry point.** `acceptance/walkthrough.md`. It starts at https://dynamicalsystemsgroup.github.io/scat-kg-tools/ and
tells you, for each stage, where to enter, what "done" looks like, what to note if it fails, and a resume check.

You run J1 to J7 yourself, from the docs, without help, on a small elicitation of your own: at least one scenario and
one architecture, in your own words and group names. The nine stages:

1. Find (J1): read the home page and say what style it evokes before you read the section that explains the name.
2. Create (J2): make your repository from the template, private, and clone it.
3. Set up (J3): install uv, run the one setup command, get a working `scat_kg`.
4. Obsidian (J3): open the folder as a vault, then clear the example before you add any page of your own.
5. Plan and capture (J4, J5): plan an event, then write raw scenario and architecture notes.
6. Code in the REPL (J6): turn the raw notes into coded pages.
7. Code with the CLI (J6): the same operations, as `scat` commands.
8. Clean check, commit, push (J7): whole-vault check to 0 errors, then commit and push.
9. The graph in Obsidian (J7): backlinks, graph view and class pages.

**What only you can do.** No agent did these (log D-040, D-044): create a real private repository from the template
(stage 2), run uv's installer (stage 3), push (stage 8), and open Obsidian (stages 4 and 9). Agents tested the same
journey from files, with uv already installed and a clone that has no remote.

**Split and resume.** Each stage ends in a state you can stop in. To resume, run that stage's "Resume check". If a
stage fails, do not work around it. Note the page, the step, what you typed and what printed. Fixes go on `dev`, the
candidate is refreshed, and you resume from the affected stage.

**Checklist.**

- [ ] Stage 1: the home page told me what SCAT is for and how to start.
- [ ] Stage 1: I wrote down the style I thought it evoked, before the page explained the name.
- [ ] Stage 2: my repository exists and is private.
- [ ] Stage 3: uv installed from the docs' command, and `uv sync` finished.
- [ ] Stage 4: Obsidian opened the vault, and the example is cleared before my own pages.
- [ ] Stage 5: I wrote raw notes for one scenario and one architecture.
- [ ] Stage 6: I coded in the Python REPL.
- [ ] Stage 7: I coded with the CLI.
- [ ] Stage 8: `uv run scat check` ends `0 errors`, and the commit is on GitHub.
- [ ] Stage 9: I navigated the graph in Obsidian without help.

**Done looks like.** All nine ticked, the repository still private, and your judgement in your own words: is the
documentation clear and navigable, and is the journey clear? That is the UA-M pass in `MISSION.md`.

---

## Sitting 2. The docs site

**Entry point.** https://dynamicalsystemsgroup.github.io/scat-kg-tools/ (marked "Pre-release candidate.", deployed from
`dev`).

From a checkout of `scat-kg-tools` on `dev` (needed for the checks below): `git clone https://github.com/DynamicalSystemsGroup/scat-kg-tools && cd scat-kg-tools && git checkout dev && uv sync --all-groups`. `--all-groups` installs the `dev` and `docs` groups that `pyproject.toml` defines.

**The eight pages.** Home; Getting started; Planning; Facilitating, with Scenarios and Architectures; Coding;
Reference, with Python API and CLI. Source: `docs/` and `mkdocs.yml`.

**What to look at.** Open each page at desktop width and at phone width (browser developer tools, 375 px wide).
Look for:

- the banner;
- a "Your next step" box at the top and a "Where next" section at the foot;
- REPL and CLI shown side by side;
- no page-level sideways scroll at 375 px (long code lines scroll inside their block);
- no dead link.

**The checks behind the docs.** Run from the tools repository.

| Check | Command | Result when written |
|---|---|---|
| Strict build, which fails on a broken link | `uv run --group docs mkdocs build --strict` | built, no warning |
| Every `bash` and `python` block runs | `uv run pytest tests/docs -q` | 23 passed (needs network: it clones the template) |
| CLI reference equals `--help` | `uv run pytest tests/docs/test_docs.py::test_cli_reference_matches_help -q` | passes (inside the 23) |

**The five docs requirements, in plain terms.**

- **R-10.** No dead ends. Each page says what you need first and where to go next.
- **R-11.** One obvious way to make each page: `scat stub`. You never hand-write structure the tools can make.
- **R-12.** Repositories made from the template are private, and the docs and the template README say so.
- **R-14.** The guides use "yes, and" and "from this perspective", and contain no step that ranks, votes on or
  judges stories or architectures.
- **R-15.** The style is music and improvisation, kept light and never at the cost of clarity: the music-note logo and
  one brief aside on improvisation (the "yes, and" stance), with plain words elsewhere (D-052). The cold-read bar gave
  way to your own judgement, see sitting 4c.

**Checklist.**

- [ ] All eight pages opened at desktop width.
- [ ] All eight pages opened at 375 px.
- [ ] Every page has "Your next step" and "Where next".
- [ ] I ran the strict build and the docs test.
- [ ] I found no step that ranks or adjudicates (R-14).
- [ ] The style is light and nothing in it gets in the way of an instruction (R-15, your own judgement, D-052).
- [ ] I wrote down my list of changes.

**Done looks like.** Every box ticked, and a list of anything you would change.

---

## Sitting 3. The tools and checks

**Entry point.** From the checkout of `dev` set up in sitting 2 (`uv sync --all-groups`), with network:

```text
uv run pytest -q && uv lock --check && uv run ruff check && uv run ruff format --check && uv run --group docs mkdocs build --strict
```

Result when written: 522 passed in 76 s; lock check clean; ruff clean on 60 files; strict build clean. The benchmark
alone: `uv run pytest tests/bench -s -q` printed page 359 ms, neighborhood 248 ms, vault 289 ms, against 1, 2 and 5 s.

| Req | Requirement | Evidence you can run or open | Status |
|---|---|---|---|
| R-1 | Errors block, warnings don't; every rule has id and severity | `uv run python tests/scripts/rules_without_tests.py` lists none (exit 0); 27 rule ids in `contracts/rule-catalogue.md`, audited in sitting 4c; `tests/checks/` | met |
| R-2 | Messages name file, field, rule id and an exact fix | `tests/checks/test_wp8_u2_messages.py`; `tests/test_paths.py` | met; golden tests pin id, file, field and fix, not full prose (D-032) |
| R-3 | Unfinished pages are never errors; links checked always | `tests/checks/test_status_rules.py`, `tests/checks/test_link_rules.py` | met |
| R-4 | Checks never write; writes are explicit operations | `tests/test_r4_snapshots.py` | met |
| R-5 | 500 pages: page under 1 s, neighborhood 2 s, vault 5 s | `tests/bench/test_r5_thresholds.py` | met; one laptop, plus Linux CI |
| R-6 | Fresh template clone, one setup command, clean check | board rows WP8-U9, U12, U15, U15b, U15c, U15d; my rerun: clone of the template at `PIN-PENDING`, `uv run scat check`: `no problems` | met with a caveat: uv was preinstalled and the uv installer, `gh` and website creation were never run by agents (D-040); no U9 or U12 report file exists, only board rows |
| R-7 | Both repositories commit `uv.lock`; CI runs on every push | `gh run list --limit 3`: tools CI run `PIN-PENDING` on the `dev` head `PIN-PENDING`; template CI run `PIN-PENDING`; both repos hold `uv.lock` | met |
| R-8 | REPL and CLI are equal paths with the same messages | `tests/test_paths.py` (same message, files, exit code; every operation covered); docs test runs both | met |
| R-9 | Docs snippets run as shown; CLI reference matches `--help` | `uv run pytest tests/docs -q` | met with a caveat: only `bash` and `python` blocks run (D-043) |
| R-10 | No broken links or dead ends | strict build clean; the 5 distinct external links I fetched returned 200; your sitting 2 | met with a caveat: the ACE's browser pass (D-039) predates the U11 to U14 edits, and I ran no browser |
| R-11 | One obvious way to make each page | `acceptance/reports/r1-p1.md` to `acceptance/reports/r3-p1.md`: all reached a clean check; D-043 removed the page templates | met with a caveat: the coding guide is long (about 5,600 words), see 4b (k) |
| R-12 | Template repos private; docs recommend it | `docs/getting-started.md` step 1; template `README.md` step 1; `gh api repos/DynamicalSystemsGroup/scat-kg-template --jq '{default_branch,is_template}'` gives `dev`, `true` | met with a caveat: the website path relies on you choosing Private (the page calls it a choice you confirm); only your stage 2 exercises either path |
| R-13 | The TBox is the one schema source | `tests/test_r7_tbox_equality.py` (named for WP5-R7); tools read `ontology/scat.ttl` at load (D-033) | met |
| R-14 | Guides hold the stance and never rank or adjudicate | `grep -n 'ranked, voted on' docs/planning.md docs/facilitate-*.md` (3 disclaimers); `research/facilitation/readout.md` | met with a caveat: grep and reading only, no test |
| R-15 | The style is music and improvisation, never at the cost of clarity | log D-052; the docs after WP9-U3 (logo, one aside, plain words); earlier cold reads `acceptance/reports/r3-cold-read.md`, `r4-cold-read.md`, `r5-cold-read.md`, kept as history | the cold-read bar gave way to your own judgement (D-052), so there is no bar to meet here: the judgement is yours, in sitting 2; the cold-read briefs are retained for reference only |

**Checklist.**

- [ ] The command block ran green on my machine.
- [ ] I opened one evidence file per row I doubt.
- [ ] I read each caveat and accept it, or I note it.
- [ ] Research readouts exist: `research/ontology/readout.md`, `research/toolchain/readout.md`, `research/facilitation/readout.md`.

**Done looks like.** The block ends green, and each row is accepted, or has a note from you.

---

## Sitting 4a. The ACE's calls

**Entry point.** The table. Each call is a log entry in `decisions/log.md`. To revert one, check out its tag, for
example `git checkout divergence/D-030`. The checkpoint tag `checkpoint/v0.1-rc1` is the revert point for D-052 (sitting 4c). The tags exist: tools has D-030, D-031, D-034, D-035, D-041; the template has
D-037 and D-043 (`git ls-remote --tags <repo> | grep divergence`).

| Log | The call | Evidence | Revert tag |
|---|---|---|---|
| D-002 | The mission's defaults are the ACE's sign-off | his standing instruction | none |
| D-004 | Adopt tradespace's branches, chain of command, tiered review | its history, read | none |
| D-005 | Add candidate stage; read "terminal/repl" as REPL plus CLI | D-007 confirms | none |
| D-009, D-012, D-019, D-020 | Mission cruft and drift passes, including cross-type links as warnings | cold-reader passes | none |
| D-010 | No group stands for one identifiable person | the ACE's reading of his Chatham House statement | none |
| D-014 | Seven changes against the two heuristics | his answer, item 2 reversed | none |
| D-017 | Scenario links S, C, A; architecture links C, A, T | his sketch | none |
| D-023 | Approve WP1 to WP3; pin models by alias | fresh PM's 12 fixes | none |
| D-024, D-025, D-026, D-027 | Hourly report; smoothing weight 0.5; log holds observations only | his requests | none |
| D-028 | Accept WP1 to WP3; stack C; conflict is a relation (its warning was removed, D-052) | spike rerun; readouts | none |
| D-029 | Approve WP4; no new axiom for missing link types | fresh PM's 6 fixes | none |
| D-030 | Namespace `w3id.org/scat#`; relations stay page types | his brief | `divergence/D-030` |
| D-031 | Relation pages only for pairs the author names | options a to c in entry | `divergence/D-031` |
| D-032 | Accept WP4; four class definitions unverified, accepted | catalogue and examples rerun | none |
| D-033 | rdflib runtime dependency; README stub on template `main` | scope check | none |
| D-034 | Tools skip the Obsidian template folder and `.obsidian/` | WP6-U1 block | `divergence/D-034` |
| D-035 | Rule four WP5 gaps; test edits authorised by you | your typed "Yes, authorise" | `divergence/D-035` |
| D-037 | Accept WP5; case study paraphrased, no verbatim quotes | 490 tests; clean clone | `divergence/D-037` (template) |
| D-038 | Accept WP6; docs address fixed; docs test pins template | greps on `f446a02` | none |
| D-039 | Accept WP7; R-15 residue and four tool gaps to WP8 | 513 tests; browser pass | none |
| D-040 | Testers use existing uv; no installer, no repositories created | permission rule | none |
| D-041 | Approve WP8; define candidate commit; D-040 left to you | fresh PM's 8 fixes | `divergence/D-041` |
| D-042 | Enable Pages; hold WP8-U1 for you | reviewed workflow; deploy | none |
| D-043 | Template flag, `dev` default; remove Obsidian page templates | `gh api` read-back | `divergence/D-043` (template) |
| D-044 | J7 for agents is clean check plus local commit | `acceptance/reports/r1-findings.md` | none |
| D-045 | Merge U11 on re-run greps; epigraph is framing | reviewer's greps | none |
| D-046 | R-15 unmet in round 2; style only in framing | `acceptance/reports/r2-findings.md` | none |
| D-047 | Keep framing sentences; read R-15 as about style elements | `acceptance/reports/r3-findings.md` | none |
| D-048 | Fix style inside `Do:` lines (U14c); no cold reads after round 5 | `acceptance/reports/r4-findings.md` | none |
| D-049 | Fix T1; accept T2 and T3 as known-weak; R-15 recorded met | `acceptance/reports/r5-findings.md` | none |
| D-050 | Candidate verified; round-3 findings accepted; local paths redacted from public records (still in git history; removing them needs a force-push, your call) | ACE reruns; re-grep returns 0 | none |
| D-052 | Checkpoint rc1; conformance checks structure, never content; jazz toned down; WP9; two research spikes | your two corrections, quoted in sitting 4c | `checkpoint/v0.1-rc1` on both repositories |
| D-053 | Rule audit: 22 rules clearly structural, four borderline rules kept, one removed | the table in sitting 4c | none |
| D-054 | The spikes may continue into feature development on their branches, outside v0.1 | your typed direction | none |

Your own decisions or directions, which the ACE only recorded and applied: D-001, D-003, D-006, D-007, D-008, D-011,
D-013, D-018, D-021, D-022, D-036. D-015 and D-016 were rolled back with `dev` (see D-017), so no entry
exists for them.

**Checklist.**

- [ ] I read every row, and I name the calls I reverse.
- [ ] I checked one revert tag with `git ls-remote`.

**Done looks like.** Every call is kept or reverted.

---

## Sitting 4b. What is known to be weak

**Entry point.** The list below, items (a) to (l). Each names the file or log entry that backs it.

- **(a) uv.** UA-A testers had uv preinstalled. No agent ran uv's installer (D-040, D-041). `MISSION.md` UA-A says "uv
  not installed". This departure is yours to disposition. Close it with one fresh tester rerun after you permit the
  official installer, or with your own stage 3.
- **(b) Push.** For agents J7 is a clean check plus a local commit. Testers' clones have no remote, so no agent pushed
  (D-044). Your stage 8 covers it.
- **(c) Output blocks.** The docs test runs only `bash` and `python` blocks. The `text` blocks that show tool output
  are pinned by reviewers' real runs, not CI (D-043).
- **(d) Obsidian.** No agent opened it. Stages 4 and 9 are the first time.
- **(e) WP8-U1 is held.** Branch `wp8/u1`, commits `3ed3163`, `9e6ca44`. It needs your authorisation to change two
  assertions in `tests/ops/test_ops_stub.py` (`not r.ok` becomes `r.ok and r.unchanged == ("concern/a.md",)`, and the
  same-type refusal row becomes a different-type row). Until it lands, `set-status done` exits 0 even when the page
  fails its check. When it lands, `src/` changes, the pins move, UA-A's rerun is the ACE's call (WP8-R8), and these
  docs spots change: `docs/coding.md`, the section "Status, and set-status" and message 7, and `docs/reference/api.md`, the `set_status` and `stub`
  sections.
- **(f) R-15 history.** (Superseded by D-052: the cold-read bar gave way to your own judgement. What follows is what the cold reads found.) Round 1 named jazz (from a phrase later removed) and listed 2 places; round 2 did not
  ("improv theatre"), 7 places; round 3 named it, 5 places; round 4 named it, 4 style places, and reader D glimpsed a
  home-page fragment in the search index (it says it did not use it; the PM tightened the fetch rule); round 5 named it
  with no home page seen, and left T1 to T3. Rules: placement (D-046), style elements only (D-047), stop rule (D-048).
  D-049 fixed T1 and accepted T2 and T3 as known-weak, for you to judge: T2 is the term "Yes, and", the mission's own
  stance, defined on the page; T3 is the CLI epigraph "The same tune at the command line". Every reader is Haiku and
  has named something each round. No reader saw the final wording (U14d).
- **(g) Clone history.** The template clone shows internal commit subjects (for example "WP8-U15 ...") to testers.
  Accepted in D-046 on the claim that a repository made from the template starts with fresh history. I did not
  verify that. Run `git log --oneline` in your new repository at stage 2.
- **(h) Review shortcuts.** The PM verified small deltas without a second full review: U11 (D-045), U14, U18, WP5-U10 and
  the last WP4-U3 round (D-032). The PM merged WP8-U8c locally after a guard refused a worker's push.
- **(i) Accepted findings.**
  - r1 A, C: no agent could push at J7 (D-044); long relation names are cut (documented).
  - r2 P3: internal commit subjects in clone history, as (g).
  - r2 P4, P5: the "Tuning up" epigraph; tester environment artefacts (terminals, piped REPL, refused push, network).
  - r2 P6: judgement left to the facilitator: story or concern line, pair choice, relation text (R-14).
  - r2 P7: relation file names cut at 64 characters, documented in `docs/coding.md`.
  - r4 S2, S4: planning epigraph; "Yes, and" (D-048).
  - r3 C3, C4, C5: planning epigraph fragment, minor wording, one more word choice (D-047).
  - r3 persona findings (16, in `acceptance/reports/r3-p1.md`): accepted by the ACE (D-050), for the reasons D-046
    gives for the same kinds (judgement calls in coding, environment artefacts, internal commit subjects in the clone's
    history, no rule for a concern with no answering affordance). The "clear the example" timing was fixed in U14.
- **(j) Found while verifying.**
  - `docs/getting-started.md` says "Both paths below set it for you, and the website path shows it as a choice you
    confirm". The `gh` command passes `--private`, but the website path relies on you choosing Private. Only your stage 2
    exercises it.
  - The four class definitions are marked `unverified` in `ontology/scat.ttl` (D-032).
  - The concern conflict is an explicit link (`conflicts`), checked for type and existence, not the disjointness axiom you named (D-028). Its warning was removed (D-052).
  - My R-6 rerun used my own home and uv cache, so it is weaker than UA-A.
- **(k) Coding guide length.** The coding guide is long (about 5,600 words) and no ruling splits it. The Haiku
  testers in rounds 1 to 3 all finished it.
- **(l) w3id.** `https://w3id.org/scat` is unregistered. `acceptance/w3id-registration.md` holds the pull request for you to
  submit after the release merge. `ontology/scat.ttl` still says the IRI base is unregistered until release.

**Checklist.**

- [ ] I gave (a) my answer.
- [ ] I gave (e) my answer.
- [ ] I read (b) to (d) and (f) to (l) and accept each, or I note it.

**Done looks like.** (a) and (e) each have your answer, and every other item is accepted or noted.

---

## Sitting 4c. The checkpoint, the conformance principle and the rule audit

**Entry point.** Log entries D-052 and D-053 in `decisions/log.md`, and the table below.

**The checkpoint.** `checkpoint/v0.1-rc1` is tagged on both repositories: tools `169061b`, template `9e9bad8`. It is the
revert point if you want the first candidate back. Check with `git ls-remote --tags <repo> | grep checkpoint`. D-052
names no `divergence` tags, so there are none for it.

**Your two corrections (D-052).**

1. Conformance checks structure, never content. You said: "we should not be getting warnings about conflicting
   concerns." The `conflicts` link stays as an explicit link, checked only for type and existence. The warning
   about a record that holds two conflicting concerns was removed from the rules, the contract, the tests, the docs, the walkthrough and this guide
   (WP9-U1, U1b, U4). The checks of a correctly built model now print `no problems` on the template's worked example.
   Where tensions are sharpest, or where concerns match or leave a gap, is analysis. It comes after conformance
   passes and a coder signs off the content. No analysis tool is part of v0.1.
2. The jazz framing was too heavy. You said it was "a little heavy handed", and "music note logo is good". The logo
   and one brief aside on improvisation stay. The page epigraphs and the other jazz framing were replaced with plain
   words (WP9-U3).

**R-15 gave way to your judgement.** D-052 records that the R-15 cold-read bar gave way to your own judgement. No
cold read is run for this release. The cold-read briefs (`acceptance/briefs/cold-read-part1.md` and `part2.md`) are
kept, marked as retained for reference only. The old reports in `acceptance/reports/` are history and are untouched.

**The rule audit (D-053).** All 27 rule ids in `contracts/rule-catalogue.md` were checked for any content judgement. A
verdict STRUCTURE means the rule looks at pages, fields, names, counts or links, and never at what a note says. The
ids below are the same 27 that the catalogue lists (`grep -o 'SCAT-[A-Z-]*' contracts/rule-catalogue.md | sort -u |
wc -l` prints 27).

| # | Rule id | Severity | What it looks at | Verdict |
|---|---|---|---|---|
| 1 | SCAT-FM-PARSE | error | frontmatter is not a readable mapping | STRUCTURE |
| 2 | SCAT-FM-REQUIRED | error | a required text field is missing | STRUCTURE |
| 3 | SCAT-FM-TYPE | error | `type` is not one of the twelve keys | STRUCTURE |
| 4 | SCAT-FM-REQUIRED-LINK | error | a relation page lacks an endpoint field | STRUCTURE |
| 5 | SCAT-FM-STATUS | error | `status` is not `stub`, `draft` or `done` | STRUCTURE |
| 6 | SCAT-FM-INDEXES | error | a class page's `indexes` value is outside its set | STRUCTURE |
| 7 | SCAT-FM-SHAPE | error | a text field is not one non-empty string | STRUCTURE |
| 8 | SCAT-NAME | error | a file name is illegal or not unique | STRUCTURE |
| 9 | SCAT-DONE-FIELD | error | a done page lacks a text field | STRUCTURE |
| 10 | SCAT-DONE-LINK | error | a done page lacks a link field | STRUCTURE |
| 11 | SCAT-DRAFT-FIELD | warning | a draft page lacks a text field it needs by done | STRUCTURE |
| 12 | SCAT-DRAFT-LINK | warning | a draft page lacks a link field it needs by done | STRUCTURE |
| 13 | SCAT-LINK-SHAPE | error | a link field is not a list of well-formed links | STRUCTURE |
| 14 | SCAT-LINK-UNLISTED | error | a page has a non-empty link field its type does not list | STRUCTURE |
| 15 | SCAT-LINK-ENDPOINT | error | a link target is the wrong page type | STRUCTURE |
| 16 | SCAT-LINK-DANGLING | error | a frontmatter link target does not exist | STRUCTURE |
| 17 | SCAT-LINK-DANGLING-BODY | error | a body link target does not exist | STRUCTURE |
| 18 | SCAT-CAP | error | stakeholder-group pages exceed the cap | STRUCTURE |
| 19 | SCAT-CAP-CONFIG | error | `scat.toml` or its cap is missing or malformed | STRUCTURE |
| 20 | SCAT-REL-DUPLICATE | warning | two relation pages state the same pair | STRUCTURE |
| 21 | SCAT-RAW-BACKLINK | warning | a coded page lists a raw page that does not list it back | STRUCTURE |
| 22 | SCAT-INDEX-STALE | warning | a class page's table is missing or differs from what `index` writes | STRUCTURE |
| 23 | SCAT-LINK-DISCOURAGED | warning | a link field the TBox discourages for this page type is non-empty | STRUCTURE (ACE ruling B1, kept) |
| 24 | SCAT-LINK-DISCOURAGED-BODY | warning | a body link goes to a class the TBox discourages for this page type | STRUCTURE (ACE ruling B1, kept) |
| 25 | SCAT-CONFLICT-SELF | warning | a concern lists itself under `conflicts`; the message states only that fact | STRUCTURE (ACE ruling B2, kept, message trimmed) |
| 26 | SCAT-MENTION | warning | text names an existing page without linking it | STRUCTURE (ACE ruling B3, kept) |
| 27 | SCAT-RAW-UNCODED | warning | a done raw page has no coded page and no coded page lists it | STRUCTURE (ACE ruling B4, kept) |

Rows 1 to 22 are the ones D-053 calls unambiguously structural. Rows 23 to 27 are the borderline rules the ACE ruled
on (B1 covers two rules). All are kept. The 28th rule, the warning about a record that holds two conflicting concerns, was content and is removed (D-052, D-053).

**Checklist.**

- [ ] I checked that `checkpoint/v0.1-rc1` exists on both repositories.
- [ ] I read the table and accept every verdict, or I name the rule I would change.
- [ ] I accept that R-15 rests on my own judgement (sitting 2).

**Done looks like.** The checkpoint is confirmed, and each verdict is accepted or noted.
