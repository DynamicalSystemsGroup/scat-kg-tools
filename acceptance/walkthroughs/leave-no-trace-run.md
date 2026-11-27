# Run record: leave no trace (example: inference.coop)

Status: **run 27 Nov 2026 in the chief engineer's sitting**, end to end, set-up to teardown (chat.inference.coop in
the built-in browser, his account; SCAT Chat serving the test vault `my-vault`; the synthetic note
`lab-note-community-fridge.md` as field notes). Screenshots and the probe log are in the sitting's evidence folder,
outside the repository. Earlier status, kept: the page was first written from the existing page, the chat path's life
cycle and the lab run of 25 November.

## The run, 27 November

| Steps | What happened | Finding and disposition |
|---|---|---|
| 6 to 18 | MCP Settings, +, name, address, Streamable HTTPS, API Key with the **Bearer** header format; he pasted the key and ticked I trust; Create; **Connect**: "MCP server 'scat' initialized successfully", entry "SCAT - Connected" | Passed as written |
| 20 to 26 | Skills, +, **Write skill instructions**: name, description, the skill file's text; "Skill created", **Available to agent** on | Passed |
| 27 to 33 | Agent Builder: name SCAT coder, model as given, Tool Library: **scat** (19 tools) and **Ask User**; skills **Selected**, `scat-coding` only; Create: "Successfully created SCAT coder" | Passed |
| 34 (old) | The page made a collection the main route for the notes; My Files has no collections, and the chief engineer: collections are for the regular pass, the temporary chat for leave no trace | Page fixed (tools f237b15): notes attached to the temporary chat, deleted from the file library at the end |
| 34 to 36 | Temporary Chat on; its note: "This chat won't appear in your history and will be deleted automatically"; Agent Builder **Select** started the chat with the agent | Passed |
| 37 to 38 | Notes attached by paperclip. First try: choosing a model in **Select a model** replaced the agent, so a plain model answered with no tools, no skill and no sight of the file | Page fixed (tools f25a8f3): leave the model menu alone once the agent is picked |
| 38 to 40 | With the agent: it read the note and asked through **Ask User**; the group cap (3, already full) refused a new group; it could not edit `scat.toml` and handed that back | Cap and settings: D-159. The coding behaviour, probed (P1 to P8, V1 to V3): `work-packages/WP27-inputs.md` |
| analysis | Asked for pictures, it called the views and wrote Mermaid itself; the server has no drawing tool | D-160: the tools draw (into WP27) |
| 47 to 49 | Stop: "SCAT Chat stopped"; the address no longer connects; the container is gone; the app quit | Passed |
| 50 to 60 | Neither temporary chat in history; server entry deleted; agent deleted; skill deleted ("Skill deleted"); two copies of the note were in My Files (one per try) and were deleted; no prompts | Passed. The two copies confirm step 57: attachments outlive the temporary chat |
| 61 | Field notes folder and vault still on the Mac; no SCAT Chat key in the keychain; Colima still running | Passed. Step 46's commit was not made (a lab vault) |

To fill at the sitting: date, environment (Mac, macOS, Colima version, Tailscale, SCAT Chat build), material used
(lab only: `contracts/examples` or the template case study; a throwaway key), every step as run with its outcome,
deviations, steps a script could remove, what was installed and removed.

Not confirmed before the sitting: the chat's Temporary Chat setting in a session, the chat's collections, whether the
saved agent can be chosen inside a temporary chat, and where the skill, collection and file-library delete controls are.

## Screenshot slots

Files go under `docs/assets/walkthroughs/leave-no-trace/`, PNG, each under about 300 KB. Crop or blur usernames,
addresses, keys and machine paths. After the sitting, reference each from the page with alt text that describes what it shows.

| File | Must show | Step (section) |
|---|---|---|
| `01-mcp-settings-form.png` | The filled MCP server form: name SCAT, Streamable HTTPS, API key, header format, "I trust this application" ticked; key hidden | Set up for the session: the server entry form |
| `02-server-connected.png` | The entry "SCAT" showing connected | Set up for the session: check the entry is connected |
| `03-skill-form.png` | The new-skill form with name `scat-coding` and its Description filled | Set up for the session: create the skill |
| `04-agent-builder.png` | The saved agent with the server "SCAT" tool and the `scat-coding` skill | Set up for the session: the saved agent |
| `05-collection-upload.png` | The field notes uploaded as one collection | Set up for the session: upload as a collection |
| `06-temporary-chat-note.png` | Temporary Chat on, with the note that the chat will not appear in history and is deleted automatically | Set up for the session: the temporary chat |
| `07-agent-in-temporary-chat.png` | The agent chosen with Select inside the temporary chat (or the model and entry if the agent cannot be chosen) | Set up for the session: start with the agent |
| `08-scat-chat-stopped-alert.png` | The "SCAT Chat stopped" alert | Tear everything down: read the alert |
| `09-history-without-chat.png` | The history list with no temporary chat in it | Tear everything down: check history |
| `10-delete-server-entry.png` | The delete confirmation for the server entry "SCAT" | Tear everything down: delete the entry |
| `11-agent-skill-collection-gone.png` | The Agent Builder, skills list and collection/file library, each empty of this session's items | Tear everything down: final look at each place |
