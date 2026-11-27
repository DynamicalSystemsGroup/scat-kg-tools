# Run record: the chatbot path (example Claude)

Page: `docs/chat-path.md`, sections "What this path needs" and "Worked example: Claude".

Status: waiting for the chief engineer's sitting. The Claude screens were not run. Written 26 Nov 2026 from Claude's
help articles (fetched, not signed in). No screenshot is referenced on the page yet.

## Screenshot slots (docs/assets/walkthroughs/chatbot/)

Throwaway lab key only; crop or blur the address, account name and any key; each file under about 300 KB.

| File | Must show | Step |
|---|---|---|
| 01-connectors.png | Customize > Connectors with the **+ Add** menu open and **Add custom connector** visible | 2 |
| 02-connector-form.png | The one form, Name `SCAT` and URL (blurred) filled | 3 |
| 03-authentication.png | The same form, Authentication set to **No sign in** | 4 |
| 04-request-headers.png | **Request headers** with `Authorization` and a masked value | 6 |
| 05-skill-upload.png | Customize > Skills with **Upload a skill** and `scat-coding.zip` chosen | 10 |
| 06-chat-connector-on.png | A new chat, the **+** menu, **Connectors**, SCAT switched on | 11 |
| 07-first-check.png | The reply to the check request | 12 |

## Doc facts relied on

- Custom connector, Pro/Max steps (Customize > Connectors > + Add > Add custom connector; name; URL; Continue;
  authentication; OAuth client; Request headers; Add): <https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp>
- Same article: the call comes from Anthropic's cloud, so the server must be public on port 443 (another port, such
  as 8443, will not connect); a connector cannot be edited, only removed and added again; per chat, **+** at the lower
  left > Connectors toggles it; Free accounts get one custom connector; on Team and Enterprise only owners add it
  (Organization settings > Connectors > Add > Custom > Web), then members click **Connect** under Customize >
  Connectors.
- Skills: Customize > Skills > + > Create skill > Upload a skill, a ZIP holding the skill folder; code execution must be
  on (Settings > Capabilities): <https://support.claude.com/en/articles/12512180-using-skills-in-claude>
  and <https://support.claude.com/en/articles/12512198-how-to-create-custom-skills>

## Left unclear by the docs (for the sitting)

- Which plan is needed: the connector article lists Free to Enterprise; the Free limit is one connector. Whether the
  Free plan really offers **Request headers** is not stated.
- What the form asks for headers: the articles say "add fixed credentials such as an API key or bearer token" but
  not whether it is one name field and one value field, or a single line. Step 6 assumes name and value.
- Which authentication choice a server with no OAuth shows by default, and whether **No sign in** hides **Request
  headers** (the article puts headers in the same step list, after the OAuth client).
- The Desktop app: no separate menu path given; the page says "Claude in the browser".
- Skill file name: the creation article writes `skill.md`, the other `SKILL.md`; the repo's file is `SKILL.md`.
- Whether the skill upload accepts a name that differs from the folder name; the page uses `scat-coding` for both.
- Whether Safari or Chrome saves the raw file as `SKILL.md` (not `.txt` or `.html`) with File > Save As; step 8 may need
  a better way.
- Whether Claude can take the rules by pasting text (a Project's instructions); the docs fetched do not say.
- Whether a bearer header named `Authorization` or `X-API-Key` is accepted by the form; the SCAT server accepts both.
- Whether the connector survives a new session without remove-and-add when only the key changes; the docs say edit is
  not possible.

## Sitting items added after review

- Steps 3 to 6 are one form filled top to bottom, then **Add** (the article lists name, URL, authentication, OAuth
  client, request headers, Add). The sitting checks whether a **Continue** appears between the URL and the rest.
- The page keeps `SKILL.md` (the repo's file; the page's folder `scat-coding` equals the skill's front-matter `name`).
  The creation article writes `skill.md`: the sitting checks that the upload accepts `SKILL.md`.
- Code execution: Free/Pro/Max, Settings > Capabilities, "Code execution and file creation" (newer layout: "Create and
  edit files"); Team/Enterprise owner, Organization settings > Plugins & skills > Policy; Enterprise also needs Skills
  on there. Toggle wording differs between the article's sections.
- The step-8 raw URL is on branch `dev`, the same source `docs/chat-path.md` ("Set up the skill") and
  `docs/leave-no-trace.md` use, i.e. the template repo's `skills/scat-coding/SKILL.md`. It follows `dev` until a
  release tag exists; the ACE confirms that is the stable source.

## Added after the cold read

- Plan wording: connector and skill both listed Free to Enterprise; Free one connector; Team/Enterprise owners add the
  connector. The article also lets an owner turn off user-created skills (the upload option then disappears): not on the
  page; the sitting notes whether it shows.
- Reachability sentence links "The session key"; the existing page says the address is public while a session runs
  (What the chat path is, Start a session).

## Steps a script could remove

- Steps 8 and 9 (save the file in a folder, compress it): a downloadable `scat-coding.zip` from the release.

## Installed and removed

Nothing.
