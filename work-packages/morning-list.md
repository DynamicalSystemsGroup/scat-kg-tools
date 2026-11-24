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

## Held for you

- None so far.

## Coming up that will need you (WP8)

- Whether AI testers may run the uv installer (`curl … | sh`) in a clean environment. Running a downloaded install
  script needs your explicit permission. The alternative is to hand testers a pre-installed uv.
- Submitting the w3id namespace registration PR from your fork, at release.
- Your walkthrough (UA-M), including opening the vault in Obsidian, which no agent can do.
