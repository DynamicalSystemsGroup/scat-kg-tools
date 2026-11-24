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
