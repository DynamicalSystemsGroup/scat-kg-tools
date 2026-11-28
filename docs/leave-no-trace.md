---
provider: inference.coop
---

# Leave no trace

!!! note "For a strict data policy"
    This page is for projects whose data policy asks that nothing stays on the chat platform. If yours does not, you
    do not need it: the chat path's own "Clean up" is enough.

Some projects work under a strict data policy: an AI platform **non-retention** policy (nothing you put into the
platform stays there), or an **approved chatbot only** policy. "Leave no trace" is a way to meet such a policy: a chat run sets up what it needs in the chat platform, does the
coding, and then removes all of it from the platform. Your local copies stay on your Mac.

Removing means removing it from the chat platform, in this example inference.coop's chat. It does not claim to remove
anything from every system the platform's model provider runs; what your policy requires there is for your policy to
say. See [Data, rights and consent](data-and-consent.md).

## What this path needs

A leave-no-trace chat run needs everything [The chat path](chat-path.md#what-the-chat-path-is-and-what-it-needs)
needs: a Mac, a vault, a container runtime, Tailscale, SCAT Chat, and a chat that accepts an MCP server and an API
key. The chat path's [Install once](chat-path.md#install-once) is done once per Mac. A strict data policy adds four
things:

- A **temporary chat** to code in, so the chat run does not stay in your history.
- Your **field notes attached to the temporary chat**, not kept in a collection, and deleted from the chat's file
  library at the end.
- **Nothing left on the platform at the end**: the server entry, the saved agent, the skill and any prompts you saved
  are removed.
- **Local copies kept**: your field notes folder and your vault stay on your Mac.

Your field notes sit in a folder on your Mac, and the vault is outside Documents, Desktop, Downloads and iCloud, as the chat path says.

## Worked example: inference.coop

The steps below take the chat run through inference.coop's chat. Another chat has its own names for these controls; the
order is the same: set up, code, remove.

### The walkthrough

Each numbered step names where it is done and one outcome. It begins with where you do it: **In SCAT Chat** (the small Mac app that runs the server), **In the menu bar** (its dot and menu), **In the
chat**, **In Finder**, **In Obsidian**, **In GitHub Desktop** or **In a web browser**.

#### Set up for the chat run

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
27. **In the chat:** open the **Agent Builder**.
28. **In the chat:** name the agent something you will recognise, for example "SCAT coder".
29. **In the chat:** in the agent's settings, choose a model.
30. **In the chat:** add the server "SCAT" as a tool of the agent. (If you delete the server entry and add it again, the agent's tool does not survive: add the tool again.)
31. **In the chat:** add the chat's Ask User tool (it lets the assistant ask you a question), if the chat offers one.
32. **In the chat:** choose the `scat-coding` skill as the agent's only skill.
33. **In the chat:** save the agent.
34. **In the chat:** turn on the Temporary Chat setting (look for the control).
35. **In the chat:** check that its note says the chat will not appear in your history and will be deleted
    automatically.
36. **In the chat:** open the Agent Builder and use its **Select** control to pick the agent; a new chat starts with it.
    (On inference.coop's instance agents start from that Select, not from the model menu or from typing `@`. If the
    saved agent cannot be chosen inside a temporary chat, start the chat with the model and the server entry instead.)
    The message box then names the agent. The model menu at the top may still say **Select a model**: leave it, since
    the agent brings its own model, and choosing a model there replaces the agent.
37. **In the chat:** attach your field notes to this chat: the paperclip in the message box, then the file from your
    field notes folder. The chat shows the file attached.

#### Do the coding

38. **In the chat:** name the narrative and ask the assistant to help you code it from the notes attached to this
    chat.
39. **In the chat:** answer the assistant's questions, one step per reply, as in [the coding
    loop](chat-path.md#the-coding-loop-in-the-chat-and-in-obsidian).
40. **In the chat:** confirm or change the nodes and links the assistant proposes.
41. **In Obsidian:** paste the account the assistant drafted into the narrative's page.
42. **In Obsidian:** read the page against your notes.
43. **In Obsidian:** set `status` yourself (`done` or `draft`).
44. **In the chat:** ask the assistant to check the whole vault.
45. **In the chat:** ask the assistant to name the pages you worked on with their status.
46. **In GitHub Desktop:** commit your work. This is your local copy of the result; it stays.

#### Tear everything down

47. **In the menu bar:** open SCAT Chat's menu and click **Stop**. Stop shows the result in one alert.
48. **In SCAT Chat:** read the alert titled "SCAT Chat stopped". It says the public link is off, the server is removed,
    the key was deleted and your clipboard holds no key. Click **OK**: SCAT Chat quits and its dot leaves the menu bar.
    If the alert is titled "SCAT Chat has a problem" instead, the stop was not confirmed: see "Stop" on the chat path,
    and do not go on until it is.
49. **In a web browser:** open the address that ended in `/mcp`. It should not load.
50. **In the chat:** end the temporary chat (close it or leave it). It is deleted automatically.
51. **In the chat:** open your history list and check the temporary chat is not there. If it is, delete it from its
    menu.
52. **In the chat:** in **MCP Settings**, next to the server "SCAT", click **Edit**.
53. **In the chat:** click the red **delete** button.
54. **In the chat:** confirm.
55. **In the chat:** delete the saved agent. (The chat's Agent Builder holds it; look there for its delete control.)
56. **In the chat:** delete the skill `scat-coding`. (Look where you created it.)
57. **In the chat:** in the file library, delete the notes you attached: they stay after the temporary chat is deleted.
58. **In the chat:** check that the file library holds no other file from this chat run, and delete any that is there.
59. **In the chat:** delete any prompt you saved for this chat run. If you saved none, there is nothing to do.
60. **In the chat:** look once more at each place you set something up (MCP Settings, the Agent Builder, the skills,
    the files, the history) and check that nothing from this chat run remains.

#### Check what stays on your Mac

61. **In Finder:** check that your field notes folder and your vault are still there, with your work in them.

### What is removed and what stays

| Removed from the chat platform | Stays on your Mac |
|---|---|
| The temporary chat, the server entry, the saved agent, the skill, the attached field notes, any prompts you saved | Your field notes folder |
| | Your vault, with every page and commit |
| The key (deleted from your keychain by Stop) | Colima, which keeps running, and the server's image |

If a step finds something that did not go, delete it by hand and do not start the next chat run until it is gone.
If your policy asks you to show the result, the list of steps above is your record: note the date and tick each one.
