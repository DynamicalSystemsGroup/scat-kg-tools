# Reviewer's guide for the chief engineer (D-6)

*Four sittings, taken one at a time. Draft for this release: the PM and the ACE finish the parts marked below.*

**Where the release stands (D-098).** WP20-U1 is on `dev` (92b64d7): whole-vault views now refuse a page whose
frontmatter cannot be read, naming the file, and the architecture sentences are added (see 4c, "Closed since D-095").
UA-A on the manual path has not run: round 1 waits on the candidate, and a later unit fills section 4d from the
reports. The chat path's UA-A has three testers, two on Haiku and one on Sonnet; the ACE runs their sessions, light
and spaced, in your sittings. WP20-U8, the docs unit for the five defects the reviewers found (4c, item 9), is done, has
passed review and is merged to `dev`; the candidate pin follows. Until the candidate is pinned, treat every "result
when written" below as stale.

Read one sitting, tick its boxes, stop. Each sitting has an entry point, a short list of what to look at, and one
decision that is yours. Nothing here asks you to trust a claim: each claim names a command to run or a file to open.
Paths are from the root of `scat-kg-tools` unless they say otherwise.

Terms: J1 to J10 (the journey), UA-A and UA-M (the AI tests and your walkthroughs), and R-1 to R-23 (the requirements)
are in `MISSION.md`, "User acceptance" and "Requirements". The ACE and your two sign-offs are in `MISSION.md`,
"Governance". The PM is in `ORG.md`. Words follow `GLOSSARY.md`.

## Before you start: the candidate

> **The candidate (refreshed 27 November, D-156).**
>
> - Tools candidate commit (the last commit that changed `src/` or `docs/`): `5e4ab16`
> - Template `dev`, which pins tools `5e4ab16`: `6ccfd9d`
> - Pages URL: https://dynamicalsystemsgroup.github.io/scat-kg-tools/ (pre-release banner on)

Check them yourself:

```text
git log --first-parent -1 --format=%h -- src docs
git diff <candidate> dev -- src docs
git ls-remote https://github.com/DynamicalSystemsGroup/scat-kg-template refs/heads/dev
```

The first prints the tools candidate, the second prints nothing, the third shows the template's `dev` commit. The
template pins the candidate itself (`rev` in its `pyproject.toml`). The
figures quoted in sittings 2 and 3 were taken earlier, on `dev` at `66d8dc3` (before WP21 to WP26); sitting 3's
command block reruns every one on the candidate, so read its output rather than the quoted numbers. The packages'
own acceptance entries (D-121 to D-156) give their test counts on their own heads.

| Sitting | Entry point | The decision you make |
|---|---|---|
| 1. The walkthroughs (UA-M) | `acceptance/walkthrough-manual.md`, then `acceptance/walkthrough-chat.md` | Do you pass UA-M on each path? |
| 2. The docs site | the Pages URL above | Are the docs clear and navigable, and is the style light enough (R-15)? |
| 3. The tools and checks | the command block at the head of sitting 3 | Is each requirement R-1 to R-23 accepted, or noted? |
| 4. The ACE's calls, the glossary, what is weak | the table in 4a | Which calls do you keep or revert, and what do you do about each weak item? |

---

## Sitting 1. The end-to-end walkthroughs (UA-M)

**Entry point.** Two scripts, one per path. `acceptance/walkthrough-manual.md` is the manual path: it starts at the
Pages URL and gives, for each stage J1 to J10, where to enter, the steps, what "done" looks like, what to record and
where to resume. `acceptance/walkthrough-chat.md` is the chat path, J1 to J10 with no terminal from J5 on; its docs
entry is `docs/chat-path.md`. (The older single `acceptance/walkthrough.md` is gone.) Each script splits its walk into
its own sittings and says where you may stop: the manual script has five (A solo trial J1-J2; B terms and set-up
J3-J5; C plan and capture J6-J7; D code J8; E analyse and hand over J9-J10) and the chat script has three (A J1-J4; B
J5-J7; C J8-J10), the same three for each chat tester, nine tester sittings in all, run by the ACE inside yours. These are walk sittings inside
this guide's sitting 1.

**What to look at.**

- **Manual path (J1 to J10).** You run it yourself from the docs, without help, on a small elicitation of your own: at
  least one scenario and one architecture, in your own words and group names. Real steps only you can do (no agent
  did them, log D-040 and D-044): create a real private repository from the template, run uv's installer, push, and
  open Obsidian.
- **Chat path (J1 to J10, G14).** You run it as you would use it: the field notes uploaded to the chat as a
  collection, the coding loop in the chat and in Obsidian, views through the MCP server, ending with Stop
  confirmed and the key deleted. This needs your sign-ins and a key you paste; it is also WP18-R4 (the live run),
  which has not been done (see 4c, item 2). Its UA-A is three testers, two on Haiku and one on Sonnet, run by the ACE
  in these sittings.
- **Hand-over (J10).** Each path ends with you deciding the model is finished and locking a version with a tag.
- **Gaps the docs unit closed (WP20-U8, D-098 ruling 3).** Three of the five defects touched these walks: the solo
  trial (J2) had no section of its own in the docs; no command was shown to see which commit a tag pins; and the chat
  path had no no-terminal route (GitHub Desktop) for clone, commit, push and removing the example. WP20-U8 adds them.
  Record what you actually did where the docs still fall short.

**Split and resume.** Each stage ends in a state you can stop in. To resume, run that stage's "Resume check". If a
stage fails, do not work around it: note the page, the step, what you typed and what printed. Fixes go on `dev`, the
candidate is refreshed, the ACE decides and logs whether UA-A reruns (`MISSION.md`, Governance), and you resume from
the affected stage.

**Checklist.**

- [ ] Manual path: I reached a clean whole-vault check (`uv run scat check` ends `0 errors`), the commit is on GitHub,
  and my repository is still private.
- [ ] Manual path: I navigated the graph and the index pages in Obsidian without help (R-21).
- [ ] Manual path: I locked a version with a tag and named what it pins and who receives it.
- [ ] Chat path: the coding loop ran in the chat, a clean check followed, Stop was confirmed, and the key
  was deleted.
- [ ] Anything I flagged is written down with its stage.

**Your decision.** Pass UA-M, or name the stage that failed. The pass (`MISSION.md`) is that you complete the journey
on both paths from the documentation without help, and judge the documentation clear and navigable and the journeys
clear.

---

## Sitting 2. The docs site

**Entry point.** The Pages URL, marked "Pre-release candidate.", deployed from `dev`.

For the checks below, from a checkout: `git clone https://github.com/DynamicalSystemsGroup/scat-kg-tools && cd scat-kg-tools && git checkout dev && uv sync --all-groups`.

**What to look at.** Open each page at desktop width and at phone width (browser developer tools, 375 px). The site
has 16 pages (`mkdocs.yml`, `nav`): Home; The flow; Data, rights and consent; Getting started; Planning; Facilitating
(Scenarios, Architectures); Coding; Coding in a chat; Coding in an IDE; Analysis; Reference (Python API, CLI, MCP
server, Terms, Architecture). Look for:

- the banner;
- a "Your next step" box at the top and a "Where next" section at the foot of each journey page (R-10, R-11);
- the REPL and the CLI side by side (R-8);
- no page-level sideways scroll at 375 px (long code lines may scroll inside their block);
- no dead link;
- the rendered tables of past and future phrases and the JSON blocks on the CLI and API reference pages, which no
  reviewer has seen in a browser (play-test finding F-6; the reviewers measured the DOM only);
- no step that ranks, votes on or judges stories or architectures (R-14), and no page that prescribes a data policy
  (`docs/data-and-consent.md` names each activity as a dependency and gives "for example" answers, D-069 to D-073).

**The checks behind the docs.**

| Check | Command | Result when written |
|---|---|---|
| Strict build, which fails on a broken link | `uv run --group docs mkdocs build --strict` | clean (re-run at the candidate) |
| Every `bash` and `python` block runs | `uv run pytest tests/docs -q` | passes; needs network (it clones the template). **Only `bash` and `python` blocks run** (D-043); `text` and `json` blocks do not |
| CLI reference equals `--help` | `uv run pytest tests/docs/test_docs.py::test_cli_reference_matches_help -q` | passes |
| The Terms page agrees with the glossary and the ontology | `uv run pytest tests/docs/test_terms.py -q` | passes |

**Checklist.**

- [ ] All 16 pages opened at desktop width, and at 375 px.
- [ ] Every journey page has "Your next step" and "Where next".
- [ ] I ran the strict build and the docs test.
- [ ] I found no step that ranks or adjudicates, and no policy the pages choose for the organiser.
- [ ] I read `docs/reference/terms.md` as a project manager who coordinates an event (field finding F-8).
- [ ] I looked at the rendered phrase tables and the two JSON blocks (F-6).
- [ ] The style is light, and nothing in it gets in the way of an instruction (R-15, your judgement, D-052).
- [ ] I wrote down my list of changes.

**Your decision.** Are the docs clear and navigable (R-10, R-11, R-14), and is the style acceptable (R-15)? Every box
ticked, with a list of anything you would change.

---

## Sitting 3. The tools and checks

**Entry point.** From the checkout set up in sitting 2 (`uv sync --all-groups`), with network:

```text
uv run pytest -q && uv lock --check && uv run ruff check && uv run ruff format --check && uv run --group docs mkdocs build --strict
```

Result when written (on `dev` at `66d8dc3`, not the candidate): see the line below; the PM re-runs the block at the
candidate and replaces it.

```text
uv run pytest -q: 2258 passed, 107 warnings in 171 s (pytest only; lock, ruff and strict build not re-run for this draft)
```

The ACE's count on `dev` at 92b64d7, after WP20-U1, is 2,264 passed (D-098); I did not re-run it. The benchmark alone
is `uv run pytest tests/bench -s -q` (R-5).

**What to look at.** The table. For each row you doubt, open the named file or run the named command. Status is the
PM's and the ACE's reading, not yours.

| Req | Requirement | Evidence you can run or open | Status |
|---|---|---|---|
| R-1 | Conformance checks structure, never content; errors block, warnings don't; every rule has an id and severity | `uv run python tests/scripts/rules_without_tests.py` lists none (exit 0); `contracts/rule-catalogue.md`; `tests/checks/`; the audit in sitting 4c's note (D-052, D-053) | met |
| R-2 | Messages name file, field, rule id and an exact fix | `tests/checks/test_end_rules.py`, `tests/test_paths.py`; `tests/independent/test_all_fixes_apply.py` | met; golden tests pin id, file, field and fix, not full prose (D-032) |
| R-3 | Unfinished pages are never errors; links and edge ends checked always | `tests/checks/test_link_rules.py`, `tests/checks/test_done_check.py` | met |
| R-4 | Checks never write; writes are explicit operations | `tests/test_r4_snapshots.py` | met |
| R-5 | 500 pages: page under 1 s, neighbourhood 2 s, vault 5 s | `tests/bench/test_r5_thresholds.py` | met on one laptop and Linux CI when last written (D-063); re-run at the candidate |
| R-6 | Fresh template clone, one setup command, clean check | the WP20-R1 clean-clone trial (**PM pastes its output into `acceptance/reports/` and links it here**) | **open until WP20-R1 runs.** Caveats: uv was preinstalled and the uv installer, `gh` and website creation were never run by agents (D-040, D-041); see 4c items 3 and 4 |
| R-7 | Both repositories commit `uv.lock`; CI runs on every push | `gh run list --commit <sha>` on each repository; `.github/workflows/ci.yml` | **open until the candidate exists** (CI green on `dev` at 3686a14 per D-097) |
| R-8 | REPL and CLI are equal paths with the same messages | `tests/test_paths.py`; the docs test runs both | met |
| R-9 | Docs snippets run as shown; CLI reference matches `--help` | sitting 2's checks | met with a caveat: only `bash` and `python` blocks run (D-043) |
| R-10 | No dead ends or broken links | strict build; your sitting 2 | **needs your sitting 2.** The ACE's browser pass predates the new pages (the WP18 and WP17 pages were reviewed without a browser, board note on WP18) |
| R-11 | One obvious way to make each page | UA-A reports (section "UA-A results" in sitting 4); `scat stub`; `acceptance/reports/r1-p1.md` to `r3-p1.md` are the earlier release's history | **open until UA-A reports are in** |
| R-12 | Template repositories are private; docs recommend it | `docs/getting-started.md` step 1; the template README; `gh api repos/DynamicalSystemsGroup/scat-kg-template --jq '{default_branch,is_template}'` gives `dev`, `true` | met with a caveat: the website path relies on you choosing Private; only your sitting 1 exercises it |
| R-13 | The TBox is the one schema source | `tests/test_r7_tbox_equality.py`; `ontology/scat.ttl` | met |
| R-14 | Guides hold the stance and never rank or adjudicate | your sitting 2; `research/facilitation/readout.md` | met on reading only; no test |
| R-15 | A light musical reference, clarity first | D-052; `docs/index.md` (the logo and one aside) | your judgement (sitting 2); no cold-read bar since D-052 |
| R-16 | A stable machine interface | `contracts/machine-interface.md` and `.schema.json`; `uv run pytest tests/machine -q`; `uv run scat check --json` on a seeded defect; the built wheel lists only `pydantic`, `pyyaml`, `rdflib` (D-066) | met at `schema_version` 1; **`schema_version` 2 since WP16** (D-089): re-run the wheel check at the candidate. One part is held: WP17-U3b (4c item 1) |
| R-17 | The notebook runs on the template's vault; fingerprint view, three edge tables, traces | `tests/views/`; the template's CI artifact `analysis-executed` (board, WP17 note) | **not accepted: WP17 is held on WP17-U3b** (D-093, D-095). Tests pass on `dev`, and whole-vault views now refuse on an unreadable page (WP20-U1); the notebook is on the template's branch `wp17/notebook` per the board, and **the PM confirms at staging that it is on template `dev`** |
| R-18 | Ripple-complete changes: an impact map before approval, a clean sweep before acceptance | `work-packages/impact/WP16.md`, `work-packages/impact/file-map.md`; the re-sweep in D-091 | met for WP16 (22 remaining hits are named keeps, D-091); no other package changed a term, contract or rule since |
| R-19 | Manual first: every step can be done by hand, no LLM | UA-M manual path; the docs test, which runs with no LLM | met in tests; **your sitting 1** is the walk |
| R-20 | The chat path works, at lab and range level | automated: `uv run pytest tests/mcp_server tests/deploy -q`; lab run: `research/chat-path/readout.md` (D-090); range vault: `research/range/` (D-097) | **open.** The automated part and the lab run are met. The live run in the chat on the shipped launcher (WP18-R4) has not been done, and the range-level run depends on it |
| R-21 | Coding happens in Obsidian | `research/layout/review.md`, "Acceptance walk" (D-088, D-091); your sitting 1 | met by the ACE's walk; yours is the one that counts |
| R-22 | Architecture before detailed design | `contracts/architecture.md`; `research/architecture/review.md` (three reviewers); D-085 | met |
| R-23 | Links and edges reconcile | `tests/checks/`, `tests/independent/test_mismatch_pairs.py`, `tests/independent/test_coding_order.py`, `tests/independent/test_done_refused.py` | met; the ACE's Obsidian walk covers the incremental coding session (D-091) |

**Also look at.** The research readouts exist: `research/ontology/`, `research/toolchain/`, `research/facilitation/`,
`research/prior-art/readout.md`, `research/chat-path/readout.md`. The ontology's four class definitions are marked
`unverified` in `ontology/scat.ttl` (D-032).

**Checklist.**

- [ ] The command block ran green on my machine.
- [ ] I opened one evidence file per row I doubt.
- [ ] I read each "open" or caveat and accept it, or I note it.

**Your decision.** Each row accepted, or noted. The rows marked "open" are not ready for acceptance; they close when
the PM or you finish the step they name.

---

## Sitting 4. The ACE's calls, the glossary, and what is weak

Four parts. 4a is the calls, 4b the glossary changes, 4c what is known to be weak, 4d the UA-A results, 4e the ACE's
calls on those results.

### 4a. The ACE's calls

**Entry point.** The table. Each row is an entry in `decisions/log.md`; the log gives the full text and, for each call,
the chief engineer's words or the ACE's evidence. "Yours" marks an entry where you gave the direction and the ACE
recorded and applied it (you may still change it); "ACE" marks a ruling the ACE made under `MISSION.md`, Governance.

**To revert a call.** Check out its tag: `git checkout divergence/D-030`. Reverting to a tag returns `dev` to that
point and so undoes the call and everything on `dev` after it, which is coarse; ask the ACE for a narrower revert if
you want one call undone. The tags are listed in the second table below, with what each marks.

The log has no entries D-015, D-016 and D-075. D-015 and D-016 were rolled back with `dev` (see D-017). D-075 was never
written (**flag for the ACE**: confirm it was skipped and not lost).

| Log | Who | The call | Evidence | Revert tag |
|---|---|---|---|---|
| D-001 | Yours | Repositories are public under the group; the mission is approved by merging its PR | his typed answer in the entry | none |
| D-002 | ACE, on his standing instruction | The mission's defaults are the ACE's sign-off; only intent gaps escalate | his standing instruction in the entry | none |
| D-003 | Yours | Repository names and the four-concept framing (the repositories were later renamed) | his typed words | none |
| D-004 | ACE | Adopt a branch scheme, chain of command and tiered review from an earlier team; reviewer's guide in sittings by output | the entry lists each adopted item | none |
| D-005 | ACE + yours | Add the candidate stage; read "terminal/repl" as REPL plus CLI; licence Apache-2.0 (yours) | D-007 confirms the reading; his typed licence answer | none |
| D-006 | Yours | Haiku testers; "make the right way the easy way" | his typed words | none |
| D-007 | Yours | CLI and REPL are equal paths | his typed words | none |
| D-008 | Yours | The user pattern is documented | his typed request | none |
| D-009, D-012, D-019, D-020 | ACE | Mission cruft and drift passes, including making cross-type links warnings (D-012 also: no licence handling for standards, yours) | cold-reader passes recorded in each entry | none |
| D-010 | ACE | No stakeholder group stands for one identifiable person | his Chatham House statement, read | none |
| D-011 | Yours | No date until velocity; story points | his typed words | none |
| D-013 | Yours | The two core heuristics | his typed words | none |
| D-014 | ACE | Seven changes against the two heuristics; REPL leads in the docs | his answer, item 2 reversed | none |
| D-017 | ACE + yours | Amendment 1: SCAT; scenarios behavioural, architectures structural; roll back and restart | his typed intent; the entry names what was rolled back | none |
| D-018 | Yours | The improvisational-jazz stance and holding disagreement; the facilitation research brief | his typed words (**the entry quotes private document titles: flagged, not repeated here**) | none |
| D-021 | Yours | macOS supported, CI on Linux, nothing that risks later Linux or Windows | his typed words | none |
| D-022 | Yours + ACE | Amendment 1 approved; branches cleaned up periodically | merge commit named in the entry | none |
| D-023 | ACE | Approve WP1 to WP3; models pinned by alias | a fresh PM's 12 fixes | none |
| D-024, D-025, D-026, D-027 | Yours | Hourly report; estimated and realized points; raw then smoothed velocity; a JSON log of the planning data | his typed requests | none |
| D-028 | ACE | Accept WP1 to WP3; stack C chosen; conflict is a relation (its warning was removed, D-052) | the spike rerun and the readouts | none |
| D-029 | ACE | Approve WP4; no new axiom for missing link types | a fresh PM's 6 fixes | none |
| D-030 | ACE | Namespace `w3id.org/scat#`; relations are page types (reshaped by WP16, D-088) | his brief | `divergence/D-030` |
| D-031 | ACE | Relation pages only for pairs the author names (replaced by edges, D-088) | options a to c in the entry | `divergence/D-031` |
| D-032 | ACE | Accept WP4; four class definitions unverified, accepted | catalogue and examples rerun | none |
| D-033 | ACE | rdflib as a runtime dependency; README stub on template `main` | scope check | none |
| D-034 | ACE | Tools skip the Obsidian template folder and `.obsidian/` | WP6-U1 block | `divergence/D-034` |
| D-035 | ACE + yours | Rule on four WP5 gaps; test-fixture edits authorised by you | his typed authorisation | `divergence/D-035` |
| D-036 | Yours | Append-only posture; autonomous overnight operation; `divergence` tags before direction changes | his typed words; `ORG.md` | none |
| D-037 | ACE | Accept WP5; case study paraphrased, no verbatim quotes | 490 tests; clean clone | `divergence/D-037` (template repository) |
| D-038 | ACE | Accept WP6; docs address fixed; docs test pins the template | greps on the candidate commit | none |
| D-039 | ACE | Accept WP7; R-15 residue and four tool gaps to WP8 | 513 tests; browser pass | none |
| D-040 | ACE | Testers use the existing uv; no installer, no repositories created | permission rule | none |
| D-041 | ACE | Approve WP8; define the candidate commit; D-040 left to you | fresh PM's 8 fixes | `divergence/D-041` |
| D-042 | ACE | Enable Pages; hold WP8-U1 for you | reviewed workflow; deploy | none |
| D-043 | ACE | Template flag set, `dev` default; Obsidian page templates removed | `gh api` read-back | `divergence/D-043` (template repository) |
| D-044 | ACE | J7 for agents is a clean check plus a local commit | `acceptance/reports/r1-findings.md` | none |
| D-045 | ACE | Merge U11 on re-run greps; epigraph is framing | reviewer's greps | none |
| D-046, D-047, D-048, D-049 | ACE | R-15 rounds 2 to 5: placement rule, style elements only, stop rule; T1 fixed, T2 and T3 accepted | `acceptance/reports/r2-findings.md` to `r5-findings.md` | none (superseded by D-052) |
| D-050 | ACE | Candidate verified; round-3 findings accepted; local paths redacted from public records (still in git history) | ACE reruns; re-grep returns 0 | none |
| D-051 | ACE | Release PRs opened (later closed, D-074) | CI green on both heads | none |
| D-052 | Yours + ACE | Checkpoint rc1; conformance checks structure, never content; jazz toned down; WP9; two research spikes | your typed corrections, quoted in the entry | `checkpoint/v0.1-rc1` on both repositories |
| D-053 | ACE | Rule audit of 28 ids: 22 structural, 4 borderline kept, 1 removed | the entry's B1 to B4 | none |
| D-054 | Yours | The spikes may continue on their branches, outside v0.1 | his typed direction | none |
| D-055 | ACE | WP9 accepted; feature branches tried; Amendment 2 drafted | 522 tests; clean clones | none |
| D-056 | ACE | Each layer brings only the dependencies it uses | wheel built from `dev` lists three dependencies | none |
| D-057 | Yours | The past/future grounding axis goes into v0.1; play test paused | his typed answers | `divergence/D-057` |
| D-058 | Yours + ACE | Amendment 3 merged; WP10 approved; test edits authorised; architecture phrases | "Yes, authorise" | `divergence/D-057` |
| D-059 | Yours | The play test runs on the template mid-WP10 | his typed words | none |
| D-060 | Yours | A stable machine interface before release (Amendment 4, R-16) | his typed words | `divergence/D-060` |
| D-061 | Yours | The estimation data is an operational requirement, checked in CI | `python3 work-packages/check_metrics.py` | none |
| D-062 | ACE | Amendment 4 merged; WP11 approved behind WP10 | PR #6, merge `519ff5a` | `divergence/D-060` |
| D-063 | ACE | WP10 accepted; rulings on the PM's flags | `check_metrics.py --accept WP10`; 560 tests | none |
| D-064 | Yours | The trial phrase names its intended outcome ("in order to stop drills going missing") | his typed words | none |
| D-065 | Yours | The template pin edit in `tests/docs/conftest.py` authorised for WP11 | his typed words | none |
| D-066 | ACE | WP11 accepted; rulings on the PM's flags | `check_metrics.py --accept WP11`; 982 tests | `divergence/D-060` |
| D-067 | Yours + ACE | A terms reference for the project manager, first as a mission amendment (superseded by D-068) | his typed words | none |
| D-068 | Yours + ACE | The terms page is a fix for field finding F-8, not a mission change; WP12 approved | his typed words | none |
| D-069 | Yours + ACE | Two more pages for F-8: the flow, and data, rights and consent (WP13) | his typed words | none |
| D-070 | Yours + ACE | Chatham House and personal attribution are example policies, not the rule | his typed words | `divergence/D-070` |
| D-071, D-072, D-073 | Yours + ACE | WP13 widened: AI use, publication levels and licence, follow-through, three classes of material, a "Before you start" checklist | his typed words in each entry | none |
| D-074 | Yours + ACE | WP12-U5 corrections made by the ACE; stale release PRs closed | his typed instruction | none |
| D-076 | Yours + ACE | Amendment 5 merged (mission rewritten, `GLOSSARY.md` added); `dev` synced | merge `0e74f19` | `divergence/D-076` |
| D-077 | ACE | WP12 accepted; terms page to be rewritten in WP16 | `check_metrics.py --accept WP12` | none |
| D-078 | ACE | Team set up for Amendment 5 (two new roles, impact maps); Pages deploys trimmed to save runner minutes | `ORG.md`, `.claude/agents/` | none |
| D-079, D-080, D-083 | ACE | WP14, RS3 and WP15 approved | scope files | none |
| D-081 | ACE | WP14 scope corrected; the ACE's calls on the WP16 impact map | `work-packages/impact/WP16.md`, section 8 | none |
| D-082 | ACE | WP14 accepted; a private name redacted from an old log entry (the one edit to a past record) | grep of the repository, outside `decisions/`, finds nothing | none |
| D-084 | Yours | The chat route for v0.1 is the coder's own machine, reached from the chat service; governed compute after v0.1 | his typed words | none |
| D-085 | ACE + yours | WP15 accepted; architecture approved (R-22); rule 4; the IDE path's `set-status` residual risk | three reviewers; `research/architecture/review.md` | none |
| D-086 | ACE | WP16 approved | scope file | `divergence/D-086` |
| D-087 | ACE | WP16 scope fixed; the connection method for the chat route | PM's scope check | none |
| D-088 | ACE | The layout: a narrative is one page with an "Edges told" table; edges one per pair, built by the tool; index pages are Bases | `research/layout/review.md` | none |
| D-089 | ACE | WP16 PM's defaults confirmed; `schema_version` 2; machine-interface page cut to 600 words; glossary gains "cap" | the entry's six rulings | none |
| D-090 | Yours + ACE | RS3 lab run worked; the MCP server runs in a container; permissions for the run | `research/chat-path/` notes on `spike/chat-path`, summarised in `research/chat-path/readout.md` | none |
| D-091 | ACE | WP16 and RS3 accepted; glossary gains "SCAT" | `research/layout/review.md`, "Acceptance walk"; 1,770 tests | `divergence/D-091` |
| D-092 | ACE | WP17 (the views) approved; dependencies in an optional extra or the template | scope file | `divergence/D-091` |
| D-093 | ACE | WP17 held on a guard refusal (WP17-U3b); 45 future-stamped metrics records to be corrected; two check gaps | the entry; `work-packages/morning-list.md` item 1b | `divergence/D-093` |
| D-094 | ACE | WP18 (the chat path) and WP19 (the range vault) approved | scope files | `divergence/D-093` |
| D-095 | ACE | WP17 follow-ups landed: metrics corrected, two check gaps closed (two tests changed with the behaviour); two items left for WP20 (the views item is now done, WP20-U1) | `check_metrics.py` passes on 536 records; CI green | none |
| D-096 | ACE | Rulings on the PM's defaults; **Docker Desktop is the documented container runtime**, untested here; the launcher never changes the coder's network account settings | the entry | `divergence/D-096` |
| D-097 | ACE | WP19 accepted; WP18 built, waiting on its live run; WP20 approved | `check_metrics.py --accept WP19`; `research/range/` | `divergence/D-096` |
| D-098 | ACE | WP20 mid-way rulings: the template branch may be pushed by URL to the template's `dev`; the stray "Remove the example" commit is not published (the pin is rebased and the pushed tree checked); five docs gaps are defects against R-9, R-10, R-11 and G9, fixed by a docs unit before the pin is redone; the chat path's UA-A has three testers (two Haiku, one Sonnet), run by the ACE in your sittings | the entry; WP20-U1 on `dev` at 92b64d7 | none |
| D-099 | ACE | A stop rule for reviews of the test kits, scripts and guide: no checkable defect against a stated requirement; targeted re-reviews, at most two rounds | the entry | none |
| D-100 | ACE | UA-A round 1 dispositions: seven docs fixes; fingerprint candidates off by default; the mention rule no longer suggests a discouraged link; history in clones and no rename/delete of node pages accepted | `acceptance/reports/wp20-r1-findings.md` | none |
| D-101 | ACE | UA-A round 2 passes on the manual path; three docs sentences fixed after it without a round 3 | `acceptance/reports/wp20-r2-findings.md` | none |
| D-102, D-103 | Yours | Release scope: candidates C1 to C8 from the chat-path live run all in v0.1; C2 split into a rule (uncoded narratives excluded) and norms | `work-packages/candidates.md`; `acceptance/chat-path/live-run-wp18-r4.md` | `divergence/D-114` |
| D-104 | Yours | WP17-U3b: `draw` may write outside the vault (schema edit allowed) | tools `b739347` | none |
| D-105, D-106 | Yours | Colima the default runtime; the MCP server image published at release | `.github/workflows/image.yml`, `release-image.yml` | `divergence/D-114` |
| D-107 | Yours | "Leave no trace" uses the temporary chat; an option, not a recommendation | `docs/leave-no-trace.md` | `divergence/D-114` |
| D-108, D-112 | Yours / ACE | uv's installer tested once by a fresh tester; the gap is closed (the tester's FAIL was the harness, checked by the ACE) | D-112 | none |
| D-109, D-113, D-116 | Yours | History rewrites asked, held when their cost was sized, then dropped | D-113 | none |
| D-110 | Yours | WP8-U1's two assertion changes allowed (first asked on a wrong description, corrected and re-asked) | tools `32bfa71` | none |
| D-111 | ACE | WP17 accepted | `check_metrics.py --accept WP17` | none |
| D-114 | ACE | WP21 approved after two scope-check rounds and an impact map | `work-packages/WP21.md`, `impact/WP21.md` | `divergence/D-114` |
| D-115 | ACE | The session key in the login keychain, never in arguments, deleted at Stop | `research/chat-path/secrets.md` | `divergence/D-114` |
| D-116 | Yours | Mission edits (image publish at release; the launcher's macOS tools); your template checkout's scratch edits discarded; C9 noted; w3id after release | `MISSION.md` | none |
| D-117, D-118 | ACE / Yours | The glossary's eleven new terms; "Edges told" and "edge table" kept apart; done is adequately coded as the coder judges | `GLOSSARY.md` | `divergence/D-114` |
| D-119 | ACE | WP21-R7 reworded after three reviews read it three ways; SCAT-UNCODED warns at every status | `work-packages/WP21.md` | none |
| D-120 | Yours | Iteration 36's metrics record corrected, after the guard refused the PM | `work-packages/metrics.jsonl` | none |
| D-121, D-122 | ACE | WP21 and WP18 accepted | D-121, D-122 | none |
| D-123 | Yours | Node-page help (C12): a research spike first, then a decision | his typed choice "A spike first" in the entry | none |
| D-124 | Yours | The launcher fixes (C10) come before the release PRs; WP22 scoped | his typed choice in the entry | none |
| D-125 | ACE | WP22 approved (SCAT Chat as a small, clear local app) after nine scope-check fixes | `work-packages/WP22.md`, `impact/WP22.md` | `divergence/D-125` |
| D-126, D-127 | Yours | Attribution of narratives (C13) in v0.1; three disjoint attribution modes (required, optional, disallowed; Chatham House is disallowed); `scat:Attributes` renamed; the mission's non-goal rewritten | his typed words, quoted in D-127 | none |
| D-128 | ACE | The ontology gains one optional narrative field, `attributed_to`; TBox version 0.3.0 | `ontology/scat.ttl`; the entry | none |
| D-129 | ACE | WP23 approved after eight scope-check fixes | `work-packages/WP23.md`, `impact/WP23.md` | `divergence/D-129` |
| D-130 | ACE | SCAT Chat is a menu-bar item with a status dot, no window; one first-start note | `research/chat-path/launcher-ui.md` | none |
| D-131 | ACE | The terms page's word cap rises from 820 to 850 for the two attribution terms | `tests/docs/test_terms.py` | none |
| D-132 | ACE | The node-page research spike (RS4) approved | `work-packages/RS4-node-pages.md` | none |
| D-133, D-134, D-135 | Yours + ACE | The deontic pass comes before release; the attribution mode is a repository metaparameter that sets what is conformant; contributor pages when attribution is on; the mission's attribution line rewritten; WP23 revised | his typed words, quoted in D-133 | none |
| D-136, D-137 | Yours | Node-page help (RS4's packages A and B) in v0.1; merge leaves `done` narratives `done`; one docs package (WP25) after WP23 and WP24 | his typed choices in each entry | none |
| D-138 | Yours + ACE | The mission's line about people in the data rewritten; the knowledge graph widened to hold contributor pages; the attribution view; terms cap raised again (see 4b) | his typed "Yes, use that" in the entry | none |
| D-139 | Yours | User-test loops and a sweep for prompt residue before your walkthrough (planned as WP26) | his typed words, quoted in the entry | none |
| D-140, D-142 | ACE / Yours | A guard refusal in WP23 held for you; the command may be retried as separate steps | his typed choice in D-142 | none |
| D-141 | ACE | WP22 accepted; the chat-path guide's session flow corrected (keep the server entry, paste the new key) | `check_metrics.py --accept WP22` | none |
| D-143 | ACE | WP23 accepted | `check_metrics.py --accept WP23` | none |
| D-144 | Yours | Merge of two node pages added to the mission's G4, with a plan shown first | `MISSION.md` G4 | none |
| D-145 | ACE | WP24 approved: twelve scope-check fixes applied | `work-packages/WP24.md`, `impact/WP24.md` | `divergence/D-145` |
| D-146 | Yours | Test and work status belongs in the plans and this guide, not in the user pages | the entry; WP24's keyword test | none |
| D-147 | ACE | Possible duplicates by structure; homonyms as pages to re-read; the thresholds are code defaults | `research/node-pages/spike-b/readout.md` | none |
| D-148 | Yours | Four coding paths in the mission (by hand, AI IDE, AI chatbot, local LLM), each with a walkthrough; leave no trace is an option of the chatbot path | his typed "Yes, amend it"; `MISSION.md` G14 | none |
| D-149 | ACE | WP25 approved after thirteen scope-check fixes | `work-packages/WP25.md`, `impact/WP25.md` | `divergence/D-149` |
| D-150 | ACE | WP24 accepted, with five rulings (the cold users' reports are a condensed record, see 4c) | `check_metrics.py --accept WP24`; `acceptance/reports/wp24-r1-findings.md` | none |
| D-151, D-152 | Yours | The local-LLM path: Docker only, a terminal is fine; the coder brings their own model and Ollama in Docker is one worked example; every path page has one shape | his typed words, quoted in D-152; `research/approaches/readout.md` | none |
| D-153 | ACE | WP25 built; U10 waits on your sitting; two more mission lines brought in line with D-148 | the entry | none |
| D-154 | ACE | WP26 approved after nine scope-check fixes | `work-packages/WP26.md` | `divergence/D-154` |
| D-155 | ACE | WP26 accepted; the template's tools pin moved to `bc66409`; glossary gains "timeframe" | `acceptance/residue-sweep.md`; `acceptance/reports/wp26-r1-*`, `wp26-r2-*` | none |
| D-156 | ACE | Visual pass round 1 (p2) on screen; two fixes (the template's Obsidian settings; sign in before Use this template); three items for you | `acceptance/reports/visual-r1-p2.md` | none |
| WP10 default | ACE | `SCAT-DRAFT-FIELD` fires at `stub` for a field with a value set, so a fresh stub warns until `timeframe` is filled. An ACE default, for you to confirm | `contracts/rule-catalogue.md` | none |

Your own decisions or directions that the ACE only recorded and applied are marked "Yours" above. D-015 and D-016 are
absent (see above).

**The tags.** All exist on `origin` for the tools repository. Check with
`git ls-remote --tags origin | grep divergence` (19 lines expected), and for the template repository with
`git ls-remote --tags https://github.com/DynamicalSystemsGroup/scat-kg-template | grep -E 'divergence|checkpoint'`.

| Tag | Commit | Marks (the commit's subject) |
|---|---|---|
| `divergence/D-030` | `9f47ce6` | WP4: U1 done; U2 and U3 in flight |
| `divergence/D-031` | `4b2d2be` | WP4: U2 and U3 reworking against merged TBox |
| `divergence/D-034` | `60b506e` | WP5-U2: vault reader and TBox-built page models |
| `divergence/D-035` | `5b251fe` | Board and metrics: WP5-U2 to U4 and U9, WP6-U1 done; WP5-U5 blocked |
| `divergence/D-041` | `b26fb57` | Morning list: D-039, D-040 |
| `divergence/D-057` | `6f54c0c` | Log: D-056 header in the log's format (the point before the grounding axis) |
| `divergence/D-060` | `a3edae4` | WP10 accepted (log D-063); findings F-5, F-6 (the point before WP11) |
| `divergence/D-070` | `8071d8d` | a merge of `dev`, the commit before D-070's ruling |
| `divergence/D-076` | `778e070` | WP12-U5 persona counts and items (log D-074); the `dev` commit before Amendment 5 |
| `divergence/D-086` | `456f2f4` | WP16 layout review in Obsidian and the layout decision (log D-088) |
| `divergence/D-091` | `1c6c9f3` | WP16 and RS3 accepted; glossary gains SCAT (log D-091) |
| `divergence/D-093` | `171baaf` | WP17 held on a guard refusal; metrics correction and check gaps (log D-093) |
| `divergence/D-096` | `3686a14` | WP18-U7f: make the missing-docker launcher test hermetic; WP20's named revert point |
| `divergence/D-114` | `43d2669` | Morning list rewritten: WP17 accepted, history rewrites held (WP21's revert point, log D-114) |
| `divergence/D-125` | `169e8db` | WP22 scope drafted (log D-125) |
| `divergence/D-129` | `5ad54e8` | WP23 scope drafted (log D-129) |
| `divergence/D-145` | `6183e29` | D-143: WP23 accepted; the point before WP24 (log D-145) |
| `divergence/D-149` | `fb487d0` | D-148: four coding paths in the mission (log D-149) |
| `divergence/D-154` | `9e247cf` | WP26: carried items added (log D-154) |
| `divergence/D-037`, `divergence/D-043` | template repository | the template before D-037 and D-043 |
| `checkpoint/v0.1-rc1` | tools `169061b`, template `9e9bad8` | the first candidate, the revert point for D-052 |

A flag for the ACE: `divergence/D-086` and `divergence/D-096` point at commits that sit later in time than their
entry's own ruling (the first at the layout decision, D-088; the second at the head when WP18 and WP19 were midway).
The log's text names them as revert points (D-092, D-097), so they are listed as such.

**Checklist.**

- [ ] I read every row, and I name the calls I reverse.
- [ ] I checked one revert tag with `git ls-remote`.

**Your decision.** Every call is kept or reverted.

### 4b. The glossary changes, for your review

`MISSION.md` (Governance, "The glossary") says a glossary change is a logged ACE call, listed for your review at
acceptance.

| Change | Log | What it is |
|---|---|---|
| The glossary itself | D-076 | Added with Amendment 5 (PR #8, merge `0e74f19`), which you merged. Its drafting commits (plain terms mapped once to formal concepts, then wording rounds on model, layout, layered graph, coding, fingerprint, loop, tool and MCP server) were reviewed in that PR's thread, not in the log. **Flag for the ACE: the log holds no list of those wording changes.** |
| **cap** added | D-089, ruling 2 | "The most stakeholder groups one vault may hold, set by the organiser in the vault's `scat.toml`." An addition, not a change of sense; the sweep for "cap" found it used only in that sense. The key `stakeholder_group_cap` keeps its name. |
| **SCAT** added | D-091 | The four node types, with a nod to scat singing. An addition: the docs expanded the name and the glossary did not. |
| "index page" for what a user sees | D-081, call 4 | Messages, docs, the folder and the `type` value say "index page"; the ontology's own identifiers may keep formal names. Not a glossary edit; a use rule. |
| Eleven terms added (WP21-G9) | D-117, D-118 | coded and uncoded, excluded, Edges told, rule and norm, skill, saved agent, session key, leave no trace, range vault. "Edges told" names a narrative's own table; "edge table" keeps its sense (the view). "Coded" is at least one node link; done means adequately coded as the coder judges. The assistant's rules are norms the server enforces only where it refuses an act. |

| **knowledge graph** widened; **contributor page** added | D-138 | The knowledge graph now holds contributor pages as well as the nodes, edges and narratives; contributor pages are in it but not in the layered graph. **Contributor page** is a new term: a page outside the four layers naming a person a narrative is attributed to, present only where the attribution mode allows it. "Contributor" alone keeps its sense of a participant. |
| **attribution mode** and **attribution** added | D-128, D-131 | Attribution mode: required, optional or disallowed, set in `scat.toml`; disallowed is the Chatham House rule. Attribution: the people a narrative is attributed to, held as its `attributed_to` links; never a node or an edge of the four layers. The glossary rows name D-129 as their ACE call; the field is D-128 and the room on the terms page is D-131. |
| **timeframe** added | D-155 | "Whether a narrative's account tells what happened (`past`), what would or will happen (`future`), or both (`mixed`). It is the narrative's `timeframe` field, required at `done`, and the author's reading of the text." An addition: the term had no entry (D-153). |
| The terms page's word cap, 820 to 850 to 910 | D-131, D-138 | Each rise is a logged ACE call (the first, 811 of 820 words to 820, is D-117). 850 fits the two attribution terms with real definitions; 910 fits the contributor page and the wider knowledge graph. The cap is `WORD_CAP` in `tests/docs/test_terms.py`. |

To see each edit as text: `git log -p --follow -- GLOSSARY.md`, or `git show a8356a8 -- GLOSSARY.md` (cap) and
`git show 1c6c9f3 -- GLOSSARY.md` (SCAT). The WP23 and WP26 rows: `git log -p -- GLOSSARY.md` from `ad8f961` on, and
`git log -p -- tests/docs/test_terms.py` for the cap.

- [ ] I read the two additions, the three further terms and the widened knowledge graph, and the cap moves, and accept them, or I note the entry I would change.

**Your decision.** Accept the additions, the widened term, the use rule and the cap moves, or name the one you would change.

### 4c. What is known to be weak

**Entry point.** The list. Each item names the file or log entry that backs it.

**Closed since D-095**

- **Whole-vault views and unreadable frontmatter (D-095's carried item, WP20-U1, on `dev` at 92b64d7).** A whole-vault
  view now refuses on a page whose frontmatter cannot be read and names the file, where it had left the narrative out
  silently. The two architecture sentences that needed the new refusals are in `contracts/architecture.md`. Evidence:
  `tests/views/test_views_unreadable_frontmatter.py`; D-098 gives the 2,264-test run.

**Carried over, still true:** WP17-U3b is still held (item 1); Docker Desktop is still untested (item 3); the
live chat-path run, WP18-R4, still waits on the chief engineer's key (item 2).

**Open and needs your answer**

1. **WP17-U3b is held (D-093, D-095).** `scat draw --out` can write a drawing outside the vault; the machine-interface
   schema lets only `export-edges` report such a path. A permission guard refused the one-line edit to
   `contracts/machine-interface.schema.json` twice. Two ways on: (a) you allow the edit (add `draw` beside
   `export-edges` in `OperationResult`'s path rule); or (b) the ACE rules that `draw` writes only inside the vault,
   as the chat path already keeps views there (D-090), and the code changes. Until then WP17 is not accepted, and so
   R-17 is not met. Everything else in WP17 is on `dev` and green (board; `work-packages/morning-list.md` item 1b).
   **Your answer:** (a) or (b).
2. **The live chat-path run, WP18-R4, has not been done.** It needs you to paste a key and sign in. WP18 is built
   and green but cannot be accepted until it runs (D-097). It is also R-20's end-to-end part. It is the chat half of
   your sitting 1.
3. **Docker Desktop is untested (D-096; superseded by D-105: Colima is now the documented runtime and Docker Desktop the
   untested alternative; see item 25).** The chat path's documented container runtime, chosen because it has a
   graphical installer, has never been installed or run here. The container itself ran under Colima (D-090). Installing
   Docker Desktop needs your permission (`work-packages/morning-list.md` item 2c). **Your answer:** permit one install
   and a local test, or accept the gap.
4. **The uv gap (D-040, D-041).** UA-A testers had uv preinstalled; `MISSION.md` says "uv not installed". No agent ran
   uv's installer. The docs' install step is exercised only by you (sitting 1). **Your answer:** accept the gap, or
   permit one fresh tester to run the official installer in a UA-A round (morning list item 4).
5. **WP8-U1 is held since D-042.** Branch `wp8/u1`. It needs your authorisation to change two assertions in
   `tests/ops/test_ops_stub.py` (`not r.ok` becomes `r.ok and r.unchanged == ("concern/a.md",)`, and the same-type
   refusal row becomes a different-type row). The file still holds the old assertions (checked on `dev`). **Your
   answer:** authorise or refuse (morning list item 3). **Flag for the ACE:** that file and the docs it touches
   (`docs/coding.md`, `docs/reference/api.md`) changed in WP16; confirm the held branch still applies.

**Known gaps, for you to accept or note**

6. **Push is unreachable for agents (D-044).** Testers' clones have no remote. For agents, J7 is a clean check plus a
   local commit (and J10 locks a version with `git tag`). Only your sitting 1 pushes.
7. **The docs test runs only `bash` and `python` blocks (D-043).** The `text` blocks that show tool output, and the
   `json` blocks on the CLI and API reference pages, are pinned by reviewers' real runs, not CI.
8. **Obsidian and the rendered pages are unseen by agents.** No agent opened Obsidian (the ACE's walk in D-091 is the
   exception for the layout). The rendered phrase tables and JSON blocks (F-6), and the WP17 to WP19 pages at desktop
   and 375 px, were measured without a browser. Your sitting 2 is the first look.
9. **Five docs defects, fixed by a docs unit (D-098, ruling 3).** The reviewers found, against R-9, R-10, R-11 and G9:
   the fingerprint view's command contradicts itself between the coding guide and the analysis guide; no command is
   shown to run the notebook; the solo trial (J2) has no section of its own; no way is shown to see which commit a tag
   pins; and the chat path has no no-terminal route for clone, commit, push and removing the example (GitHub Desktop,
   D-087). **Status: done.** WP20-U8 fixes all five and passed review; it is merged to `dev`, and
   the candidate is pinned after it, before UA-A runs.
10. **The play-test findings file is stale.** `acceptance/playtest-findings.md` still lists F-1 to F-8 with proposed
    dispositions. The board says WP16-U13 and U7f took F-1, F-3, F-5 and F-7; F-4 became R-16; F-8 became WP12 and WP13;
    F-2 (docs theme end of life, 5 May 2027) is a later package; F-6 is your sitting 2. I did not verify the fixes.
11. **History holds things you asked to keep out (`work-packages/morning-list.md` items 1, 1a, 5; D-050, D-081,
    D-082).** A line in `main`'s history (commit `c58113b`), private repository names in `dev` (`20ff07a`), one old
    log entry, and local paths in older commits. The files are clean now; removing them from history needs a
    force-push, which only you can authorise. **Your answer:** leave, or rewrite.
12. **Your template checkout will conflict on pull** (morning list item 2b): uncommitted edits in
    `.obsidian/core-plugins.json` and `app.json` against the migrated template.
13. **w3id.** `w3id.org/scat` is unregistered. `acceptance/w3id-registration.md` holds the pull request for you to
    submit after the release merge (morning list item 6).
14. **Review shortcuts.** The PM verified small deltas without a second full review in earlier packages (D-032, D-045).
    WP16-U4's fixes got a second, independent review (D-089, ruling 6).
15. **WP19's review.** The range vault's narratives were coded by workers standing in for the coder; the ACE read one
    against its source, and a review sample of at least a third was checked (D-096, D-097). A coder has not signed off
    its content.
16. **Rule 4 and the IDE path (D-085, call b).** An agent on the IDE path can run `set-status`; authority there holds
    by the assistant's file and git review. The chat path holds it by construction (the MCP server never sets `done`).
    Accepted as a residual risk.
17. **The `timeframe` tags are an author's judgement (WP10).** Nothing checks them against the text.
18. **An edge refusal stays a manual fix (WP11, D-066 ruling 2).** `scat stub` refuses a relation-type edge and names
    the command, but the fix is typed `manual`.
19. **Coding guide length.** About 5,600 words at the last count and no ruling splits it (the count predates WP16 and
    WP18; **PM re-counts at the candidate**).
20. **The mission's own gaps.** Four class definitions in `ontology/scat.ttl` are `unverified` (D-032).
21. **Earlier-release weaknesses that stand only as history.** The R-15 cold-read rounds, the clone history showing
    internal commit subjects (D-046; the check is your stage 2 `git log --oneline` in the new repository), and the
    round 1 to 5 findings in `acceptance/reports/r1-findings.md` to `r5-findings.md` were accepted in D-044 to D-050.
    The PM's WP12 cold reads of the Terms page are in `acceptance/reports/wp12-r3-round1.md` to `round4.md`.
22. **Merging two same-type node pages exists (a plan first); a split is a plan only; rename and delete stay file edits (UA-A round 1, W11; D-100).** Accepted for v0.1: a real
    organiser edits files and uses git. Evidence: `acceptance/reports/wp20-r1-findings.md`. Since WP24 two node pages of
    one type can be merged (`scat merge A B`, a plan first with `--plan`); a split is a plan only (`scat split-plan A`);
    a rename stays an Obsidian action.
23. **Small accepted findings from UA-A round 1 (D-100).** W8: `scat_kg.check(neighborhood=False)` works but the API page
    does not show it. W12: a concern with no addressing row is not named by the Analysis page; the views show it by
    absence. W13: the layered drawing has lines through other nodes' boxes. W14: testers' own wording for prompts, plan
    files and link text, Obsidian checked through files, a candidate pair left without a row as the page says. W16:
    `uv sync` reaches GitHub for the tools dependency, though a tester's clone has no remote, because the dependency is a
    git URL.
24. **A clone of the template shows work-package commits and `divergence/` tags (W15; D-100).** Accepted: the
    documented path ("Use this template") starts with fresh history; the UA-A testers cloned directly.
25. **WP21 chat-path life cycle: not verified, left to the chief engineer's sitting or the release (D-115, D-116).** (a)
    A keychain prompt when the launcher runs from the built app, or with a locked login keychain. (b) Whether the key's
    keychain item syncs to iCloud Keychain. (c) Docker Desktop, the untested alternative to Colima. (d) R4: the
    `scat-coding` skill loading in the chat, and the saved agent. (e) R7: the leave-no-trace walkthrough
    (`docs/leave-no-trace.md`), including the chat's Temporary Chat setting and collections, neither tried. (f) R6: the
    first push of the published image, which also waits on the mission's Release step 3. (g) WP22: SCAT Chat as a menu-bar app (the dot, its menu, the first-start note, `Serve <vault>?`, Change
    vault) and the guides' account of the chat's forms (the consent, the header format, Connect, the skill's
    Description, the saved agent's tool added again), none confirmed on a real Mac and chat.
26. **Node-page help and merge (WP24; D-144 to D-147).** What shipped: the views `evidence`, `copy-share` and `review`;
    `merge` (plan first, then applied by the coder) and `split-plan`; the assistant's rules A16 to A20 in the contract,
    the skill and the server's rules text; the prompts `draft-a-node-page`, `fill-in-node-pages` and
    `look-for-duplicates`; the norms page's line for each node type. The review view's basis is provisional: its
    thresholds are code defaults, fitted to the seeded cases of the G6 vault (`research/node-pages/vault`) and checked
    on two small vaults (the spike readout is `research/node-pages/spike-b/readout.md`). Each rests on one seeded
    positive; a second vault with known duplicates would settle them. The pages-to-re-read list had a precision of 1
    of 4 on the G6 vault, and the range vault's `community-members` has three narratives, so it is not listed. UA-A
    round 1 (`acceptance/reports/wp24-r1-findings.md`): no blocking finding; X1 to X10 dispositioned there (X2 fixed
    in the copy-share entries). Open grey spots for you: `schema_version` 3 with new operations; the machine
    interface contract page's word cap raised from 646 to 774 over the package; the command-line `scat set-status
    done` works, as it is the coder's own tool, and the refusal of `done` is the MCP server's and the assistant's
    rules (X1).

27. **SCAT Chat as a menu-bar app, and the chat-path guide: left for your sitting (D-130, D-141).** Not confirmed on a
    real Mac: the dot's colours and look and a real click with no flicker; the menu and the alerts; the Stop alert in
    front; reopening after an unconfirmed Stop; the Gatekeeper prompt and copying the app to Applications; keychain
    prompts; real Colima and Tailscale; the chat's form labels. Item 25 (g) holds the earlier part of this list.
28. **Attribution: grey spots (D-143).** `schema_version` stays 2 with the new `attribution` operation, which the
    contract's closed-list wording allows; the machine-schema page's word cap is 646 in D-143 and 774 after WP24 (item
    26). WP23's cold read was one Haiku reader.
29. **Reviews without a fresh reviewer (D-141, D-150).** WP22's two late commits (`99e15cf`, `42d5a1d`) were checked by
    the PM without a fresh review, and in WP24 the void check (U9) and U10 had none. The ACE's own read of the chat-path
    guide found the defect corrected in D-141.
30. **The cold users' records for WP24 and WP25 are the PM's condensed record, not their originals (D-150, D-153).** Weaker
    evidence than the originals filed for WP26 (`acceptance/reports/wp26-r1-*`, `wp26-r2-*`). WP24's are in
    `acceptance/reports/wp24-r1-findings.md`.
31. **WP25 unit U10 is not done: your sitting runs it (D-153).** The Claude, Codex and inference.coop walkthrough runs
    with screenshots, and the by-hand Obsidian screenshots. WP25 is accepted when U10 is done (`check_metrics.py --accept
    WP25` fails only on U10). Claude's and Codex's set-up steps follow the cited docs and are corrected in the sitting
    (D-151). The local server image is built from a clone until the release publishes it.
32. **The local-LLM path (D-151, D-153).** Local models drive the tools but pick them unreliably; on a Mac, Ollama in
    Docker has no GPU; SCAT Chat publishes only through Tailscale, which a local client may not reach. The walkthrough
    ran once for real and was removed after. Open WebUI ran with its login off on 127.0.0.1, which the ACE confirmed
    for a single person's local run; the page says so for that case.
33. **Departures in WP26's UA-A rounds (D-155).** Docs served from a local build of the same commit; uv preinstalled (the
    uv gap is closed separately, D-112); the chat testers ran a pages-and-files pass for J1 to J4 and J6; the GitHub
    steps of J2 were not reached. Round 1's two blocking findings are fixed (the template's tools pin; a pointer to
    the chat path from `getting-started`).
34. **"Install once" on the chat path uses Terminal (D-155), answered (D-164).** It is the setup person's job; one-time
    Terminal use at setup is tolerated for v0.1, not wanted; a terminal-free install is candidate C16.
35. **The duplicate-finding thresholds rest on one seeded positive each (D-147).** This is item 26's last point, kept
    here because the docs do not say it (D-146): the thresholds are code defaults, fitted to the G6 vault and checked
    on two small vaults; a second vault with known duplicates would settle them.
36. **The visual pass's items (D-156), answered by you.** V2: `scat index` now writes Obsidian's own form, so opening
    an index no longer changes it. V3: the stub writes a plain empty `timeframe:`. V4: statuses stay independent. The
    GitHub website path ran on screen (V7). Nothing left to answer here.

**The note on the rule audit (D-052, D-053).** The audit covered the v0.1 catalogue as it stood then. The rules in
force, with their ids and severities, are in `contracts/rule-catalogue.md`; `SCAT-NOEDGES` (G1, added in WP18-U6) and
the table rules came after the audit.

**Checklist.**

- [ ] I gave items 1, 3, 4, 5 and 11 my answer.
- [ ] I read items 2, 6 to 10, 12 to 36 and accept each, or I note it.

**Your decision.** Items 1, 3, 4, 5 and 11 each have your answer, and every other item is accepted or noted.

### 4d. UA-A results

The pass bar is in `MISSION.md` ("User acceptance", "Pass bar"): every tester reaches the end with a clean check and a
hand-over, every finding is dispositioned, and the last round leaves no blocking finding. **The manual path meets it
after round 2.** The chat path's rounds run in your sittings (D-098), so their rows are empty until then.

| Round | Persona | Model | Path | Report | Clean check | Hand-over | Blocking | Dispositioned |
|---|---|---|---|---|---|---|---|---|
| 1 | p1, the organiser, Python session | Haiku | manual | `reports/wp20-r1-p1.md` | yes | tag, commit, recipient | none | yes (D-100) |
| 1 | p2, the organiser, command line | Haiku | manual | `reports/wp20-r1-p2.md` | yes | tag, commit, recipient | none | yes (D-100) |
| 1 | p3, control | Sonnet | manual | `reports/wp20-r1-p3.md` | yes | tag, commit, recipient | none | yes (D-100) |
| 2 | p1, Python session (fresh tester) | Haiku | manual | `reports/wp20-r2-p1.md` | yes | tag, commit, recipient | none | yes (D-101) |
| 2 | p1b, Python session (fresh tester) | Haiku | manual | `reports/wp20-r2-p1b.md` | yes | tag, commit, recipient | none | yes (D-101) |
| 2 | p2, command line (fresh tester) | Haiku | manual | `reports/wp20-r2-p2.md` | yes | tag, commit, recipient | none | yes (D-101) |
| 2 | p3, control (fresh tester) | Sonnet | manual | `reports/wp20-r2-p3.md` | yes | tag, commit, recipient | none | yes (D-101) |
| visual 1 | p2, command line, on screen (Pages, Obsidian, Terminal) | Haiku | manual | `reports/visual-r1-p2.md` | yes | tag, commit, recipient | none | yes (D-156) |
| | chat tester 1 | Haiku | chat | your sitting | | | | |
| | chat tester 2 | Haiku | chat | your sitting | | | | |
| | chat tester 3 | Sonnet | chat | your sitting | | | | |

- Rounds run on the manual path: two. Round 1 against template a8f7287; round 2 against template 826bc99 (tools
  7d17534). The last docs fixes after round 2 move the pin without a rerun (D-101).
- No report was void. In round 1, p1 ran some tool steps on the command line against its brief, so round 2 added a
  second Haiku tester in the Python session through J10.
- uv was pre-installed for every tester and every report says so (D-040, D-041): a gap only you can waive.

### 4e. The ACE's calls on the UA-A findings

| Log | Finding | The call | Evidence |
|---|---|---|---|
| D-100 | W1 to W7: docs gaps (the solo-trial command, the example's folders, a link, the Analysis page's output folder, answers between the terms examples, nothing to commit at hand-over, stubs and the lock) | Fixed in the docs | `reports/wp20-r1-findings.md` |
| D-100 | W9: fingerprint candidates are noisy (three of three testers) | A defect against R-11: candidates off by default, an option everywhere | the same |
| D-100 | W10a: the mention rule asked for a group link on an architecture page | A defect: no suggestion of a discouraged link | the same |
| D-100 | W10b: a hyphenated title not offered | A defect (a literal title compare): fixed | the same |
| D-100 | W11: no documented rename or delete of a node page | Accepted for v0.1; listed in 4c | the same |
| D-100 | W15: work-package commits and tags in a clone's history | Accepted: "Use this template" starts fresh history | the same |
| D-100 | W8, W12 to W14, W16 | Accepted as the PM proposed (wording, visual polish, expected behaviour) | the same |
| D-101 | X1: `git add .` sweeps in drawings and plan files (three of four testers) | Fixed in the docs, without prescribing | `reports/wp20-r2-findings.md` |
| D-101 | X5: the tag name is the organiser's own | Fixed in the docs | the same |
| D-101 | X3: a narrative quoting the notes | Fixed: the consent page says, as fact, that quoted text enters the model and its rules | the same |
| D-101 | The rest of round 2 | Accepted as the PM proposed | the same |

**Your decision.** Keep or revert each call, as in 4a.

### 4f. WP26: what the sweep moved here, and what only your sitting can confirm

Moved out of the user pages (D-146), so the pages say only what a coder does:

- **Chat path.** The launcher was run against Colima with a stand-in for the public-link service; Docker Desktop was
  not tried; the first real run of the pages by a coder is the sitting. The launcher's search folders for `docker`
  (`/usr/local/bin`, `/opt/homebrew/bin`, Docker.app) are no longer on the page.
- **`deploy/README.md`** no longer lists what is unverified: iCloud Keychain sync of the session key, the locked-keychain
  prompt, Docker Desktop, and the checks that need a screen. Each is yours to confirm.
- **Leave no trace.** "Seen in the lab run" is gone from the file-library step; the Temporary Chat shortcut is no longer
  named (it was not confirmed). The chat's form labels and control names are yours to check against the live chat.
- **UA-A in WP26** (reports `acceptance/reports/wp26-r1-*.md`, `wp26-r2-*.md`, dispositions in `wp26-r*-findings.md`):
  docs served from a local build, not the Pages deploy; uv preinstalled; the template pin was moved for the test only
  (a request to the ACE, not pushed); the chat-path testers ran Sitting A (J1 to J4) and J6 as a read-and-write-files pass
  with no chat, browser, key or sign-in, so the chat, J2's GitHub steps, J5 and J7 to J10 are yours.
- **New wording the sweep added for you to confirm** (found by testers, not stated before): `docs/planning.md` says to tell
  people if an assistant will read the notes; `docs/data-and-consent.md` says to keep the nine answers with the consent
  records, outside the vault; `docs/flow.md` step 7 says field notes are plain text files that step 8 takes in;
  `docs/getting-started.md` points a reader who will not use Terminal to the chat path.
