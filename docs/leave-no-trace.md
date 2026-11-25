# Leave no trace

!!! warning "This is one policy option, a MAY"
    This page shows **one option** for a strict data policy. It is not a recommendation and it is not a default.
    Projects that prefer lower friction need not follow it, and should not jump through these extra steps. Read it
    only when your project's data policy asks for it.

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
    control that was not seen, it says what to look for, and the chief engineer's sitting is where it is confirmed.

## What this option does

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

Each numbered step names where it is done and one outcome. It begins with where you do it: **In SCAT Chat** (the launcher app), **In the
chat**, **In Finder**, **In Obsidian**, **In GitHub Desktop** or **In a web browser**.

### Set up for the session

1. **In Finder:** check that your field notes are in a folder on your Mac. This is your local copy.
2. **In SCAT Chat:** open the app and wait for the window that says "SCAT Chat is running." (Start a session, on the
   chat path.)
3. **In the chat:** in the bar of icons on the left, click **MCP Settings**.
4. **In the chat:** choose to add an MCP server, and type `SCAT` as its name.
5. **In the chat:** type the address from the SCAT Chat window (it ends in `/mcp`) into the address field.
6. **In the chat:** choose the Streamable HTTPS transport (the way the chat talks to a server over a secure web
   address).
7. **In the chat:** choose API key as the authentication.
8. **In SCAT Chat:** click **Copy key**.
9. **In the chat:** paste the key into the API key field.
10. **In the chat:** save.
11. **In any app:** copy a word from anywhere, so your clipboard no longer holds the key.
12. **In a web browser:** open the skill file, <https://raw.githubusercontent.com/DynamicalSystemsGroup/scat-kg-tools/dev/skills/scat-coding/SKILL.md>.
13. **In a web browser:** select all (Cmd-A) and copy (Cmd-C) its text. Keep the tab open.
14. **In the chat:** look for **Skills** (in the chat's menus or settings; this page has not recorded where) and choose to create a new skill.
15. **In the chat:** name the skill `scat-coding` and paste the text you copied. (If the form offers an upload instead, upload the file; whether the chat takes the file as it stands was not recorded.)
16. **In the chat:** save the skill.
17. **In the chat:** open the **Agent Builder** and name the agent something you will recognise, for example "SCAT coder".
18. **In the chat:** in the agent's settings choose a model, and add as tools the server "SCAT" and the chat's Ask User tool, if it offers one.
19. **In the chat:** choose the `scat-coding` skill as the agent's only skill, and save the agent.
20. **In the chat:** upload your field notes as one collection, if the chat offers collections. If it does not, skip
    this step and attach the notes to the temporary chat when you start coding instead. (Collections were not tried; look for a
    file or knowledge area where you can group files under one name.)
21. **In the chat:** turn on the Temporary Chat setting (the chat shows the control; the shortcut seen was Cmd-Shift-Y).
22. **In the chat:** check that its note says the chat will not appear in your history and will be deleted
    automatically.
23. **In the chat:** open the Agent Builder and use its **Select** control to pick the agent; a new chat starts with it.
    (On inference.coop's instance agents start from that Select, not from the model menu or from typing `@`. Whether
    the saved agent can be chosen inside a temporary chat was not tried.)

### Do the coding

24. **In the chat:** name the narrative and ask the assistant to help you code it, with your collection (or, if you
    skipped the collection, the notes attached to this chat).
25. **In the chat:** answer the assistant's questions, one step per reply, as in [the coding
    loop](chat-path.md#the-coding-loop-in-the-chat-and-in-obsidian).
26. **In the chat:** confirm or change the nodes and links the assistant proposes.
27. **In Obsidian:** paste the account the assistant drafted into the narrative's page.
28. **In Obsidian:** read the page against your notes.
29. **In Obsidian:** set `status` yourself (`done` or `draft`).
30. **In the chat:** ask the assistant to check the whole vault.
31. **In the chat:** ask the assistant to name the pages you worked on with their status.
32. **In GitHub Desktop:** commit your work. This is your local copy of the result; it stays.

### Tear everything down

33. **In SCAT Chat:** click **Stop**. The window says the public link is off, the server is removed, the key was
    deleted and your clipboard holds no key.
34. **In a web browser:** open the address that ended in `/mcp`. It should not load.
35. **In the chat:** end the temporary chat (close it or leave it). It is deleted automatically.
36. **In the chat:** open your history list and check the temporary chat is not there. If it is, delete it from its
    menu.
37. **In the chat:** in **MCP Settings**, next to the server "SCAT", click **Edit**.
38. **In the chat:** click the red **delete** button.
39. **In the chat:** confirm.
40. **In the chat:** delete the saved agent. (The chat's Agent Builder holds it; where its delete control is was not
    recorded, so look there.)
41. **In the chat:** delete the skill `scat-coding`. (Look where you created it.)
42. **In the chat:** delete the collection you uploaded, and any file left in the chat's file library from this
    session. (Where these are was not recorded; look for a file library.)
43. **In the chat:** delete any prompt you saved for this session. If you saved none, there is nothing to do.
44. **In the chat:** look once more at each place you set something up (MCP Settings, the Agent Builder, the skills,
    the files, the history) and check that nothing from this session remains.

### Check what stays on your Mac

45. **In Finder:** check that your field notes folder and your vault are still there, with your work in them.

## What is removed and what stays

| Removed from the chat platform | Stays on your Mac |
|---|---|
| The temporary chat, the server entry, the saved agent, the skill, the collection and its files, any prompts you saved | Your field notes folder |
| | Your vault, with every page and commit |
| The key (deleted from your keychain by Stop) | Colima and the server's image |

If a step finds something that did not go, delete it by hand and do not start the next session until it is gone.
If your policy asks you to show the result, the list of steps above is your record: note the date and tick each one.
