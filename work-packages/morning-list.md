# Morning list for the chief engineer

Items the ACE decided overnight that you may want to look at, and anything held for you. Each one names its decision
log entry and, where the ruling changed direction, the `divergence/` tag to revert to. Appended through the night.

## Rulings you may want to reverse

- **D-028:** the concern conflict is a relation plus a warning, not an OWL disjointness axiom. Disjointness would
  make a tension an inconsistency.
- **D-030** (`divergence/D-030`): relations stay page types with their own notes, per your sketch, overruling the
  worker's link fields. The namespace is `https://w3id.org/scat#`; registering it is a PR from your w3id fork, at
  release.
- **D-031** (`divergence/D-031`): relation pages are created only for pairs the author names. No pairing is inferred.
- **D-033:** rdflib is a runtime dependency (the tools read `scat.ttl` directly). The template's `main` got a
  bootstrap README stub.
- **D-034** (`divergence/D-034`): Obsidian's template folder and `.obsidian/` are outside the vault scan.
- **D-037** (`divergence/D-037`, on the template): the case study no longer quotes you verbatim. It paraphrases in a
  neutral voice, because your words in the public log made the quotes identify you.
- **WP6 content:**
  - the concerns "staying faithful to intent" and "avoiding drift" are merged as "Intent without drift", to stay
    within 3 concerns;
  - "Attribution" has no sourced holder, which is left as a recorded gap.

- **D-038:** WP6 accepted after the paraphrase. A few lines still echo the gist of public mission wording, which
  was judged acceptable. The docs' address is fixed as `https://dynamicalsystemsgroup.github.io/scat-kg-tools/`, and
  the docs test clones the template at a pinned commit.

- **D-039:** WP7 (docs) accepted after the ACE's browser pass over all 8 pages. Two things are carried into WP8:
  - every cold read named jazz unprompted, but flagged 5–7 phrases where the jazz figure of speech made an
    instruction less plain;
  - four small tool gaps the doc writers found.

  The coding guide is long, at about 5,000 words.
- **D-040:** AI testers don't run uv's downloaded installer. They use the existing uv in a clean home directory, and
  the install step is left to your walkthrough. No agent creates repositories from the template.

- **D-042 / D-043:** the candidate stage is live.
  - Pages serves the pre-release docs.
  - The template repo is now a GitHub template, with `dev` as its default branch.
  - The Obsidian page templates are removed from the template repo (`divergence/D-043`). They held frontmatter only,
    so they couldn't serve as body skeletons, and the docs had to tell people not to use them. `scat stub` is the one
    way to create pages.

- **D-044: UA-A round 1 passed with nothing blocking** (3 testers to a clean check; the cold read named jazz). For
  agents, J7 is a clean check plus a local commit, because UA-A clones have no remote by design; the push is in your
  walkthrough. 12 docs fixes are going into U11, and round 2 adds a mandatory Haiku REPL tester. The WP8 metrics
  timestamps were placeholders and are being corrected by appended records.

- **D-045:** the round-1 fixes are merged. Confirmed: one raw page per story or pitch, holding every group's
  account, each labelled with its group.

- **D-046: UA-A round 2.** All three testers reached a clean check, including the Haiku REPL tester, with nothing
  blocking. But R-15 (jazz styling) failed: the cold reader said "improv theatre". The fix is a placement rule: jazz
  lives only in framing (epigraphs, one plain sentence per guide naming jazz), and instructions are always plain. A
  focused round 3 rechecks it.

- **D-047: round 3.** Both cold readers named jazz from the new framing sentences, and the Haiku REPL tester was clean.
  The ACE reviewed the four framing sentences and kept them. Two plain instruction defects get the ACE's wording,
  including a clearer "Yes, and" rule: "ask a question that adds to it; do not ask whether it is true, right or
  complete". R-15 is now read as concerning style elements only, which ends the round loop.

- **D-048: round 4.** Readers named jazz again, but flagged three style-in-instruction phrases. One was a framing
  sentence the ACE had approved, which contradicted "restate in your own words"; that was partly the ACE's error and
  is now fixed. A stop rule applies: one last reader pair, then the ACE dispositions anything left directly, as
  known-weak in the guide.

- **D-049: round 5, then the stop rule.** Every reader in rounds 3 to 5 named jazz. The ACE fixed the last coding
  framing sentence ("play its meaning back in plain words") and folded in plain wording fixes. "Yes, and" and the CLI
  epigraph are kept as known-weak for your judgement. There are no more reader rounds.

- **D-050: local paths redacted.** Scratch paths embedding your machine username had been committed in 11 UA-A
  reports, the PM handover note and one log quote. They are now `<scratch>` or `<local>`. They remain in git history,
  and removing them would need a force-push, which is your call.

## Held for you

- **D-040 / D-041: UA-A ran with uv preinstalled,** whereas `MISSION.md` UA-A says "uv not installed". Only you
  can waive that. Either accept it as a known gap at acceptance, or permit one fresh tester to run uv's official
  installer, and a rerun closes the gap.

- **WP8-U1 is held: a test edit only you can authorise (D-042).** D-039's fixes make `stub` on an existing page of the
  same type a no-op, and `set-status done` report the page's check. Two existing assertions in
  `tests/ops/test_ops_stub.py` assert the old behaviour, and the guard rightly refuses an agent's authorisation.
  The intended edits are as strong as before:
  - `not r.ok` becomes `r.ok and r.unchanged == ("concern/a.md",)`;
  - the same-type refusal row becomes a different-type row (`affordance`).

  Fixes are on `wp8/u1` (`3ed3163`, `9e6ca44`). Your "yes" lets it land as a pin move with a UA-A rerun.

## Coming up that will need you (WP8)

- Whether AI testers may run the uv installer (`curl … | sh`) in a clean environment. Running a downloaded install
  script needs your explicit permission. The alternative is to hand testers a pre-installed uv.
- Submitting the w3id namespace registration PR from your fork, at release.
- Your walkthrough (UA-M), including opening the vault in Obsidian, which no agent can do.
