# Morning list for the chief engineer

Updated 28 November (overnight). Earlier versions are in git history. Words follow `GLOSSARY.md`.

## Where things stand

| Package | State |
|---|---|
| WP27, WP28, WP29, WP32 to WP36, WP38, RS5, RS6 | accepted (latest: WP36 D-212, WP38 D-210, WP29 D-187) |
| WP30 stages on the server | built and trimmed (D-194, D-209); accepted once its on-screen check runs in your sitting |
| WP37 the rename (SCATLAB, scat-tools, scat-template) | prepared overnight on branches, not merged; lands after you rename the two repositories |
| WP39 a narrative is its account | scoped (D-208); waits for your approval |
| WP31 the assistant's habits | waits on WP30's acceptance |
| RS7 how a tool asks the person | desk parts done (likely cause: our spike's call, not Claude); client trials in your sitting |
| RS8 candidate evidence | desk parts done; its question was settled by D-205 and D-208 |

## Decisions waiting (one at a time)

1. **WP39's scope**: retire the list; one rule (every table node is linked in the account); candidates from the
   account only; one sentence in the coding guide. Approve?
2. **RS8's assistant readings**: they compare designs (a) to (e), all replaced by D-208's rule. Drop them and accept
   RS8 on its desk parts, or keep them?

## Your sitting (one session)

1. **Land WP37** (a few minutes; `work-packages/WP37-landing.md` on the `wp37/rename` branch): you rename
   `scat-kg-tools` to `scat-tools` and `scat-kg-template` to `scat-template` in GitHub's settings; I merge, re-pin and
   check the docs site.
2. **SCATLAB over SCAT Chat** (WP37-R2, `acceptance/walkthroughs/rename-run.md` on the branch): build, install over the
   old app, start a session; one app, one keychain item, one image.
3. **The stages on screen** (WP30-R6, `acceptance/walkthroughs/stages-run.md`): steps 1 to 9 in Claude, then in
   inference.coop, on a copy of the examples served by SCATLAB.
4. **How a tool asks the person** (RS7, `research/asking/readout.md` Appendix C): the trial runner instead of SCATLAB;
   Claude up to 16 messages, inference.coop up to 12, human-paced.
5. **Teardown**: the server and the public route off, the connectors removed, the key deleted.

You paste keys and sign in; I drive and record. inference.coop stays gentle: one chat, one step at a time.
