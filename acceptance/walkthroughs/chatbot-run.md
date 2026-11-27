# Run record: the chatbot path (example Claude)

Page: `docs/chat-path.md`, sections "What this path needs" and "Worked example: Claude".

Status: **run 27 Nov 2026 in the chief engineer's sitting** (claude.ai in the built-in browser, his account; SCAT Chat
serving the test vault `my-vault`). Passed to step 24: SCAT connected with its 19 tools, the skill installed, and the
check in a chat answered "no problems found". The first draft below was written 26 Nov from Claude's help articles;
the run found its menu names out of date (below). Screenshots are kept outside the repository (the sitting's evidence
folder, `s2-claude-*`); the docs' slots are not filled yet (crop and blur first).

## The run, 27 November

| Step | What happened | Finding and disposition |
|---|---|---|
| 13 | **Customize** > **Connectors** now opens **Plugins** (tabs All, Connectors, Skills; an **Add** menu: Upload plugin, Add custom connector, ...) | Page updated (tools 3ba11c2) |
| 14 to 15 | Two screens: name and **MCP server URL**, **Continue**; then Authentication, where **No sign-in** warns that the server required sign-in | Page updated |
| 17 | **Add header** gives a list of header names (`authorization`, `x-api-key`, ...); value masked. With `authorization` and `Bearer <key>`, Claude could not connect ("Couldn't reach SCAT"); the server log showed no session, so the key never passed. Removed and added again with `x-api-key` and the key alone: **Connected**, 19 tools listed. Whether the first try failed on the paste or on Claude's handling of that header is not known. | Page now uses `x-api-key` and the bare key |
| 22 | No "Create skill": **Plugins** > **Add** > **Upload plugin**, **browse**, the zip, **Upload**; listed as the plugin **Scat coding**. The page says a `SKILL.md` alone is also accepted (not tried). | Page updated; WP27 (D-157) reworks how the skill reaches the client |
| Capabilities | The switch is **Run code in the cloud** ("Required for skills"), under **Code execution and file creation**; it was on | Page updated |
| 23 | **+** > **Plugins** (not Connectors) > SCAT, already on; `scat-coding` listed too | Page updated |
| 24 | "Run the SCAT check on my vault and tell me what it says." Claude called SCAT: Check and reported `ok: true`, no problems, and that the check tests structure only. It did not know what `mode: "disallowed"` means and guessed wrongly (an allowance for stubs or links). | Evidence for D-157: nothing the server sends explains the attribution mode |


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
