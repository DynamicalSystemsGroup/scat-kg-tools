# WP22-U6: cold read of the chat-path guides

Candidates: `docs/chat-path.md` and `docs/leave-no-trace.md` at `wp22/u5` 4eb43d1 (the address step of 42d5a1d was added after this read, from finding 1 below). Two fresh Haiku testers, isolated copies of the two files only, no other file read, nothing run. Persona A: neighbourhood organiser, comfortable on a Mac. Persona B: hurried organiser who skims. The PM condensed their answers; the nine questions of A and eight of B were answered from the pages with quotes.

## What the readers got right

- What SCAT Chat is (no window, a dot in the menu bar, runs the SCAT MCP server), where it is (Applications), the first-start order (note, then the folder picker), the dot colours (grey, green, red), the two things to paste and how to copy each, "Serve <vault>?" with Use it / Choose another, the two kinds of problem (a start problem: choose Stop, then open SCAT Chat again; a Stop not confirmed: stays open, red dot, choose Stop again, do not open it again), the Stop alert "SCAT Chat stopped" and the check that the `/mcp` address no longer loads.
- B named the server form's fields, the consent tick, the header format, Connect, the skill form's required Description and its source, why the saved agent's tool is added again, and why step 54 exists.

## Findings and dispositions

| # | Finding | Disposition |
|---|---|---|
| 1 | Change vault updated only the key, though the page says the address changes each session (A) | Fixed in `wp22/u5` 42d5a1d (Copy address, paste if different). Whether the address really changes each session needs the sitting. |
| 2 | Where the app comes from if nobody built it (A, B) | Answered in the page ("ask the person who set up your tools"); no change. |
| 3 | "Connected" has no on-screen description (B) | The chat's own form; only the sitting can say what it shows. |
| 4 | Jargon unexplained in the walkthrough (container, Funnel, Colima, keychain, collection, Agent Builder) (A, B) | Left to the ACE: the walkthrough links to the guide; no change in this package. |
| 5 | "Look where you created it" and "look for a file library" name no place (B) | The chat's layout was not run end to end; the sitting. |
| 6 | Step 28 has two actions; step 30 two outcomes with no note of which was chosen (B) | Left to the ACE (steps are WP21-R7's rule; a unit or WP26's user-test loops). |
| 7 | Colima "left running" next to "nothing left running" (B) | Left to the ACE. |

Guesses counted as findings: A: 6 (restart vs Stop again, clipboard after a second copy, what Use it changes, what the first-open step does, vault location, address change); B: 9. None blocks R7.

## Confirmed by the sitting only

The real alerts and their wording, the red and green dots, that reopening the app after an unconfirmed Stop starts a new session, the chat form's real labels and Connect, and whether the address changes each session.
