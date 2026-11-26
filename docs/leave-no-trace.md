# Leave no trace

!!! note "For a strict data policy"
    This page is for projects whose data policy asks that nothing stays on the chat platform. If yours does not, you
    do not need it: the chat path's own "Clean up" is enough.

Some projects work under a strict data policy: an AI platform **non-retention** policy (nothing you put into the
platform stays there), or an **approved chatbot only** policy. "Leave no trace" is the life cycle of a chat-path
session that fits such a policy. A session sets up everything it needs in the chat platform, does the coding, and then
removes all of it from the platform. Your local copies stay on your Mac.

Removing means removing it from the chat platform, in this example inference.coop's chat. It does not claim to remove
anything from every system the platform's model provider runs; what your policy requires there is for your policy to
say. See [Data, rights and consent](data-and-consent.md).

The page follows [The chat path](chat-path.md), which has the one session start to clean-up that every project uses.
This page only adds what a strict policy needs.

!!! note "What has and has not been tried"
    No one has yet run this walkthrough end to end. Its pieces were seen separately in the lab run of 25 November
    (the server entry, the skill and the saved agent, an uploaded file, the removal of the server entry). Two things
    were not tried: the chat's Temporary Chat setting in a session, and the chat's collections. Where a step names a
    control that was not seen, it says what to look for, and your first run is where it is confirmed.

## What this page does

1. A **temporary chat**: the coding session runs in the chat's Temporary Chat setting, whose own text says the chat
   will not appear in your history and is deleted automatically.
2. The **field notes are uploaded as a collection**, so they can be removed as one thing.
3. The **server entry, the saved agent, the skill and any prompts** are set up for this session only.
4. The coding work.
5. **Every one of them is removed from the platform** at the end.
6. **Local copies stay** on your machine: your field notes, and your vault with every change.

## Before you start

- You have done "Install once" on [The chat path](chat-path.md) (once per Mac).
- Your field notes are in a folder on your Mac. They stay there; the clean-up never touches that folder.
- Your vault is outside Documents, Desktop, Downloads and iCloud, as the chat path says.

## The walkthrough

Each numbered step names where it is done and one outcome. It begins with where you do it: **In SCAT Chat** (the small Mac app that runs the server), **In the menu bar** (its dot and menu), **In the
chat**, **In Finder**, **In Obsidian**, **In GitHub Desktop** or **In a web browser**.

### Set up for the session

1. **In Finder:** check that your field notes are in a folder on your Mac. This is your local copy.
2. **In Finder:** open SCAT Chat from Applications. (Start a session, on the chat path.)
3. **In SCAT Chat:** at the first start on this Mac, read the note that SCAT Chat lives in the menu bar, and click
   **OK**. It is shown once per Mac. (At a later start there is no note.)
4. **In SCAT Chat:** at the first start, choose the folder that holds `scat.toml` in the folder picker. At a later start,
   answer the question `Serve <vault>?` with **Use it**, or with **Choose another** and the folder that holds
   `scat.toml`.
5. **In the menu bar:** wait until SCAT Chat's dot is green.
6. **In the chat:** in the bar of icons on the left, click **MCP Settings**.
7. **In the chat:** choose to add an MCP server, and type `SCAT` as its name.
8. **In the menu bar:** open SCAT Chat's menu and click **Copy address**. A notification says "The address is on your clipboard."
9. **In the chat:** paste the address (it ends in `/mcp`) into the address field.
10. **In the chat:** choose the Streamable HTTPS transport (the way the chat talks to a server over a secure web
   address).
11. **In the chat:** choose API key as the authentication.
12. **In the chat:** choose the header format the form offers for the key (`X-API-Key` or `Authorization: Bearer`; the server accepts either).
13. **In the menu bar:** open SCAT Chat's menu and click **Copy key**. A notification says "The key is on your clipboard."
14. **In the chat:** paste the key into the API key field.
15. **In the chat:** tick the consent **I trust this application**. The form requires it.
16. **In the chat:** save.
17. **In the chat:** click **Connect** on the new entry. A new entry stays unconnected until you do.
18. **In the chat:** check that the entry "SCAT" shows connected.
19. **In any app:** copy a word from anywhere, so your clipboard no longer holds the key.
20. **In a web browser:** open the skill file, <https://raw.githubusercontent.com/DynamicalSystemsGroup/scat-kg-tools/dev/skills/scat-coding/SKILL.md>.
21. **In a web browser:** select all (Cmd-A) and copy (Cmd-C) its text. Keep the tab open.
22. **In the chat:** look for **Skills** (in the chat's menus or settings) and choose to create a new skill.
23. **In the chat:** name the skill `scat-coding`.
24. **In the chat:** fill in the **Description**, which the form requires, with the text after `description:` in the skill file's first lines (it begins "Rules and habits for the assistant").
25. **In the chat:** paste the text you copied into the skill's text field. (If the form offers an upload instead, upload the file; if the chat does not accept the file as it stands, paste its text instead.)
26. **In the chat:** save the skill.
27. **In the chat:** open the **Agent Builder** and name the agent something you will recognise, for example "SCAT coder".
28. **In the chat:** in the agent's settings choose a model, and add as tools the server "SCAT" and the chat's Ask User tool, if it offers one. (If you delete the server entry and add it again, the agent's tool does not survive: add the tool again.)
29. **In the chat:** choose the `scat-coding` skill as the agent's only skill, and save the agent.
30. **In the chat:** upload your field notes as one collection, if the chat offers collections. If it does not, skip
    this step and attach the notes to the temporary chat when you start coding instead. (Look for a
    file or knowledge area where you can group files under one name.)
31. **In the chat:** turn on the Temporary Chat setting (the chat shows the control; the shortcut seen was Cmd-Shift-Y).
32. **In the chat:** check that its note says the chat will not appear in your history and will be deleted
    automatically.
33. **In the chat:** open the Agent Builder and use its **Select** control to pick the agent; a new chat starts with it.
    (On inference.coop's instance agents start from that Select, not from the model menu or from typing `@`. If the
    saved agent cannot be chosen inside a temporary chat, start the chat with the model and the server entry instead.)

### Do the coding

34. **In the chat:** name the narrative and ask the assistant to help you code it, with your collection (or, if you
    skipped the collection, the notes attached to this chat).
35. **In the chat:** answer the assistant's questions, one step per reply, as in [the coding
    loop](chat-path.md#the-coding-loop-in-the-chat-and-in-obsidian).
36. **In the chat:** confirm or change the nodes and links the assistant proposes.
37. **In Obsidian:** paste the account the assistant drafted into the narrative's page.
38. **In Obsidian:** read the page against your notes.
39. **In Obsidian:** set `status` yourself (`done` or `draft`).
40. **In the chat:** ask the assistant to check the whole vault.
41. **In the chat:** ask the assistant to name the pages you worked on with their status.
42. **In GitHub Desktop:** commit your work. This is your local copy of the result; it stays.

### Tear everything down

43. **In the menu bar:** open SCAT Chat's menu and click **Stop**. Stop shows the result in one alert.
44. **In SCAT Chat:** read the alert titled "SCAT Chat stopped". It says the public link is off, the server is removed,
    the key was deleted and your clipboard holds no key. Click **OK**: SCAT Chat quits and its dot leaves the menu bar.
    If the alert is titled "SCAT Chat has a problem" instead, the stop was not confirmed: see "Stop" on the chat path,
    and do not go on until it is.
45. **In a web browser:** open the address that ended in `/mcp`. It should not load.
46. **In the chat:** end the temporary chat (close it or leave it). It is deleted automatically.
47. **In the chat:** open your history list and check the temporary chat is not there. If it is, delete it from its
    menu.
48. **In the chat:** in **MCP Settings**, next to the server "SCAT", click **Edit**.
49. **In the chat:** click the red **delete** button.
50. **In the chat:** confirm.
51. **In the chat:** delete the saved agent. (The chat's Agent Builder holds it; look there for its delete control.)
52. **In the chat:** delete the skill `scat-coding`. (Look where you created it.)
53. **In the chat:** delete the collection you uploaded. (Look for a file library.)
54. **In the chat:** delete any file left in the chat's file library from this session. This step is needed because field notes you attached to a temporary chat stay in the file library after the chat is deleted (seen in the lab run).
55. **In the chat:** delete any prompt you saved for this session. If you saved none, there is nothing to do.
56. **In the chat:** look once more at each place you set something up (MCP Settings, the Agent Builder, the skills,
    the files, the history) and check that nothing from this session remains.

### Check what stays on your Mac

57. **In Finder:** check that your field notes folder and your vault are still there, with your work in them.

## What is removed and what stays

| Removed from the chat platform | Stays on your Mac |
|---|---|
| The temporary chat, the server entry, the saved agent, the skill, the collection and its files, any prompts you saved | Your field notes folder |
| | Your vault, with every page and commit |
| The key (deleted from your keychain by Stop) | Colima and the server's image |

If a step finds something that did not go, delete it by hand and do not start the next session until it is gone.
If your policy asks you to show the result, the list of steps above is your record: note the date and tick each one.
