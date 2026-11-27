# Coverage check: the 27 November sitting's notes against WP27 to WP31 and RS5

Every note, finding and decision from the visual pass and the chief engineer's sitting on 27 November, and where it
went. "Done" means fixed and pushed during the day; a package means it is in that scope.

| # | Note | Where it went |
|---|---|---|
| 1 | V1: Obsidian rewrote `.obsidian` settings files; the first `git add .` swept them in | Done (template 87accad, D-156) |
| 2 | V2: Obsidian rewrote `index/*.base` into its own form | Done on his "B" (tools 5e4ab16, template 6ccfd9d, D-156) |
| 3 | V3: the stub's timeframe hint was invisible in Obsidian | Done on his "Yes, that" (tools 5e4ab16) |
| 4 | V4: node pages stay stubs when narratives are done | Decided: independent statuses, no change (D-156) |
| 5 | V6: sign in to GitHub before **Use this template** | Done (tools 65c733b) |
| 6 | V7: the website path run; **Commit to dev** | Done (tools 4c6cbf3) |
| 7 | SCAT Chat should offer to move itself to Applications | Done (tools 71c8417; D-161) |
| 8 | The folder-access prompt when choosing the vault | Done, in his words (tools d832b62) |
| 9 | Claude's screens renamed (Plugins); the key in an `x-api-key` header | Done (tools 3ba11c2); run record |
| 10 | The skill upload accepts a `SKILL.md` alone (not tried) | WP30 (default: the upload stays, the server's guides make it optional) |
| 11 | Claude did not know what `mode` means | WP30-G4, WP31-G1 |
| 12 | The server has tools but no lifecycle manual | RS5, WP29, WP30 (D-157, D-162) |
| 13 | The IDE example is Copilot in VS Code | Done (D-158; tools ae29efa; mission lines) |
| 14 | A page of pros and cons of each path, IDE's weak enforcement first | Done (tools eeb1a99; D-161) |
| 15 | Leave no trace: notes attached to the temporary chat, not a collection | Done (tools f237b15) |
| 16 | The regular chat pass uses collections | WP30-G6 |
| 17 | Choosing a model at the top replaced the agent | Done (tools f25a8f3) |
| 18 | The assistant listed nodes and edges before any account; they are found while coding | WP30-G4 (the coding guide's order), WP31-G2 |
| 19 | Options handed back without "what would happen" | WP31-G2 |
| 20 | The group cap stopped a non-coder; settings are the setup person's job; default cap 6 | WP27 (D-159) |
| 21 | The assistant offered to edit `scat.toml` and to "enable code execution" | WP31-G3 |
| 22 | The assistant tried the chat's own file tools on the vault | WP31-G3 (the boundary held; WP30's stage scoping narrows it further) |
| 23 | Probes P1 to P8: untrue reports, deciding for the coder, declining for the wrong reason, careless drafts | WP31-G1 to G4; the probes are WP31-G5's test, judged per stage |
| 24 | V1 and V2: the assistant authored Mermaid; the server has no drawing tool | WP28 (D-160) |
| 25 | V3: analysis reasoned from stale results, false claims | WP31-G1; WP30-G4 (analysis guide) |
| 26 | Drawings were built in WP17 but never handed to the server; the container lacks matplotlib | WP28-G1, G3 |
| 27 | No drawing of a trace | WP28-G2 |
| 28 | Why Claude's `Bearer` header failed is not known | WP28 (the on-screen check of R5 tries both header forms in Claude; agent's default) |
| 29 | Hunt down prior work before building | WP28 reuses `draw`; RS5 reads the flow, journeys and runs first; WP30 reuses the prompts and `assistant-rules` |
| 30 | Screenshots for the docs' walkthrough slots (crop and blur) | Stays with WP25-U10, not these packages |
| 31 | "Install once uses Terminal" judgement | Stays open for the chief engineer (D-155), not these packages |
| 32 | The chat path's live stages (c1 to c3) | Stay for a sitting (WP20-UC1), not these packages |
| 33 | Research, then design, then implementation for the lifecycle; implementation depends on design, habits on implementation | RS5 → WP29 → WP30 → WP31 (D-162) |
| 34 | The lifecycle is a small finite state machine; stage narrows inputs, outputs, tools and skills; predicates detect or request transitions; a formal model with a concrete instance | RS5-G1, G2, G5; WP29-G1, G2 |
| 35 | Stage may travel in a header on MCP requests; an unknown stage gets a result asking for clarification | RS5-G3; WP29-G3; WP30-G1 |
| 36 | Stage alters what tools and skills are exposed, the required inputs and the allowed outputs | RS5-G4; WP30-G2, G5 |
| 37 | Moves between stages, backward included, at the user's discretion | WP29-G2 (transitions); WP30-G3 |

Gap found by this check: item 28 was in no scope. WP28's agent's defaults now carry it.
