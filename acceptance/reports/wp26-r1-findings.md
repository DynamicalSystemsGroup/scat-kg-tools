# WP26 round 1: findings and dispositions

Candidate: tools `pm-wp26` d11856d plus the fixes below; template 0b8b4c4. Docs served from a local build of the same commit
(known-weak: the Pages deploy is skipped). uv preinstalled. Testers: p1 Haiku, p2 Haiku, p3 Sonnet (CLI or Python, the
whole journey); c1 Haiku, c2 Sonnet, c3 Haiku (chat path, stages J1 to J4 and J6 only, run as a pages-and-files reading:
no chat, browser, key or sign-in; the site stages are marked "not reached"). Reports are the testers' own text, in
`wp26-r1-<persona>.md` (p3's is its saved file; the others are its returned message; c1 and c2 differ from their saved
files only by the closing notes). The PM's filing, not the ACE's dispositions.

| Id | Finding | Severity | Disposition |
|---|---|---|---|
| p1 F-1, p2 F-1 | The Analysis and Coding pages describe `scat evidence`, `copy-share`, `review`, `merge`, `split-plan`; the template's pinned tools (fd0a39e, WP23) lack them. | blocking | Not a page defect: the template's pin predates WP24. Request to the ACE: move the template's tools pin (`pyproject.toml` and `uv.lock`) to the tools `dev` head after this wave. Re-tested in round 2 with the pin moved. |
| c1 F-3, c2 F-7, c3 F-7 | Choice 5 (AI) says the answer must match what participants were told; the planning terms had no AI line. | not blocking | Fixed: `docs/planning.md` says to tell people if an assistant will read the notes. |
| c1 F-2, c2 F-8, c3 F-6 | No page says where the nine answers are kept. | not blocking | Fixed: `docs/data-and-consent.md` (with the consent records, outside the vault). |
| c2 F-2 | `getting-started` requires Terminal; no pointer to the chat path for a person who will not use it. | blocking for the persona | Fixed: one bullet in "Before you start" points to the chat path. Re-test in round 2. |
| p3 F-4 | `flow` step 7 said field notes stay outside the tool; Planning pastes them into narrative pages. | not blocking | Fixed: the flow says they are plain text files that step 8 takes in. |
| p3 F-1 | The home page's next step (the repository) and the flow's first try (the solo trial) read as two starts. | not blocking | Accepted: the repository is the first action of both (the flow names "Setup, as in step 5"). Raise again if round 2 trips on it. |
| c2 F-4, c2 F-11 | GitHub Desktop is not said to be installed; "Install once" uses Terminal although the page opens with "no terminal". | not blocking | Accepted for round 2: the chat-path page says the install is done once by the person who sets it up; the chief engineer's sitting confirms. |
| p1 F-2, p2 F-4/F-5, p3 F-5 | The tester's own terms leave attribution, licence or release form open. | not blocking | Accepted: the brief's terms, not the page; the pages say the answer is the organiser's own. |
| p1 F-5, p3 F-7 | No page says where the first draft goes or to commit it. | not blocking | Accepted for round 2; a repeat there is fixed. |
| p2 F-2, p2 F-3, p3 F-2 | Where to put a link inside a quotation and the `description:` line. | not blocking | Accepted: the page's worked examples show both; repeat in round 2 is fixed. |
| p3 F-9, F-11, F-12 to F-16 | Candidate list length, edge table as lines, template tags, modelling judgements. | not blocking | Accepted: judgements are the coder's (`MISSION.md`); the tags come from cloning (GitHub's "Use this template" copies none). |
| All | `page.py index` returns 404. | harness | Harness only; the home page is the site root. |
| p1 F-9, p2, p3 | `git push` refused by the environment's classifier at J10. | environment | Not a finding (the clones have no remote). |
