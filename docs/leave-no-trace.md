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

Each numbered step is one action. It begins with where you do it: **In SCAT Chat** (the launcher app), **In the
chat**, **In Finder**, **In Obsidian**, **In GitHub Desktop** or **In a web browser**.

### Set up for the session

1. **In Finder:** check that your field notes are in a folder on your Mac. This is your local copy.
2. **In SCAT Chat:** open the app and wait for the window that says "SCAT Chat is running." (Start a session, on the
   chat path.)
3. **In the chat:** in the bar of icons on the left, click **MCP Settings**, then choose to add an MCP server.
4. **In SCAT Chat:** click **Copy key**.
5. **In the chat:** fill in the form: the address from the SCAT Chat window (it ends in `/mcp`), the Streamable HTTPS
   transport, API key as the authentication, and the key from your clipboard. Save.
6. **In the chat:** create the skill `scat-coding`, as steps 1 to 3 of "Set up the skill and the saved agent" on the
   chat path say.
7. **In the chat:** create the saved agent, as steps 4 to 6 of the same section say.
8. **In the chat:** upload your field notes as one collection, if the chat offers collections. If it does not, skip
   this step and attach the notes to the temporary chat in step 11 instead. (Collections were not tried; look for a
   file or knowledge area where you can group files under one name.)
9. **In the chat:** turn on the Temporary Chat setting (the chat shows the control; the shortcut seen was Cmd-Shift-Y).
   Check that its note says the chat will not appear in your history and will be deleted automatically.
10. **In the chat:** start a chat with the saved agent, as step 7 of the same section says. (Whether the saved agent
    can be chosen inside a temporary chat was not tried.)

### Do the coding

11. **In the chat:** name the narrative and ask the assistant to help you code it, with your collection (or, if you
    skipped step 8, the notes attached to this chat).
12. **In the chat:** answer the assistant's questions and confirm the nodes and links it proposes, one step per reply,
    as in [the coding loop](chat-path.md#the-coding-loop-in-the-chat-and-in-obsidian).
13. **In Obsidian:** paste the account the assistant drafted into the narrative's page, read the page against your
    notes, and set `status` yourself (`done` or `draft`).
14. **In the chat:** ask the assistant to check the whole vault and to name the pages you worked on with their status.
15. **In GitHub Desktop:** commit your work. This is your local copy of the result; it stays.

### Tear everything down

16. **In SCAT Chat:** click **Stop**. The window says the public link is off, the server is removed, the key was
    deleted and your clipboard holds no key.
17. **In a web browser:** open the address that ended in `/mcp`. It should not load.
18. **In the chat:** end the temporary chat (close it or leave it). It is deleted automatically.
19. **In the chat:** open your history list and check the temporary chat is not there. If it is, delete it from its
    menu.
20. **In the chat:** in **MCP Settings**, next to the server you added, click **Edit**, then the red **delete** button,
    and confirm.
21. **In the chat:** delete the saved agent. (The chat's Agent Builder holds it; where its delete control is was not
    recorded, so look there.)
22. **In the chat:** delete the skill `scat-coding`. (Look where you created it in step 6.)
23. **In the chat:** delete the collection you uploaded, and any file left in the chat's file library from this
    session. (Where these are was not recorded; look for a file library.)
24. **In the chat:** delete any prompt you saved for this session. If you saved none, there is nothing to do.
25. **In the chat:** look once more at each place you set something up (MCP Settings, the Agent Builder, the skills,
    the files, the history) and check that nothing from this session remains.

### Check what stays on your Mac

26. **In Finder:** check that your field notes folder and your vault are still there, with your work in them.

## What is removed and what stays

| Removed from the chat platform | Stays on your Mac |
|---|---|
| The temporary chat, the server entry, the saved agent, the skill, the collection and its files, any prompts you saved | Your field notes folder |
| | Your vault, with every page and commit |
| The key (deleted from your keychain by Stop) | Colima and the server's image |

If a step finds something that did not go, delete it by hand and do not start the next session until it is gone.
If your policy asks you to show the result, the list of steps above is your record: note the date and tick each one.
