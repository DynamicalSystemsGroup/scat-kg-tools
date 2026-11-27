# Run record: leave no trace (example: inference.coop)

Status: waiting for the chief engineer's sitting. Not run: inference.coop was off limits for the writing unit
(WP25-U7). The page `docs/leave-no-trace.md` was written from the existing page, the chat path's life cycle and the
lab run of 25 November; it carries no screenshot references yet.

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
