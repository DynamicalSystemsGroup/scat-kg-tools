# The chat path

!!! tip "Your next step"
    Read "What the chat path is, and what it needs", then do "Install once". You do that one time per Mac. After that,
    every session runs the same way: start, connect the chat, use, stop, clean up.

The chat path lets you code a narrative by talking to an assistant in a chat window in your browser, with no
terminal in the coding itself. Obsidian stays where you read and decide. This page walks one session from start to
clean-up. Each numbered step names one outcome and says where you do it: **In the chat**, **In SCAT Chat** (the launcher
app), **In Finder**, **In GitHub Desktop**, **In Obsidian**, **In Tailscale** or **In a terminal**.

!!! warning "What has and has not been tried"
    The launcher was run against Colima with a stand-in for Tailscale. A first connection to a chat worked in a
    lab run with lab material only. Version 0.1 is for the Mac only. **Docker Desktop is the untested alternative to
    Colima** and has not been run end to end with this launcher. Nobody has yet run the whole path as a coder
    following this page, so your first run is the real test. Where this page cannot vouch for a step, it says so. If
    a step fails and its message does not help, tell the person who set this up for you which step and what the
    window said.
    One more thing not checked: the launcher looks for the `docker` command in `/usr/local/bin`, `/opt/homebrew/bin`
    and Docker Desktop's own folder (`/Applications/Docker.app/Contents/Resources/bin`). If it says Docker is not
    installed although it is, that is the likely cause; tell the person who set this up.

If your project's data policy is strict (an AI platform that must keep nothing, or "approved chatbot only"), see
[Leave no trace](leave-no-trace.md). It is one option for such a policy, not something you need for a session.

## What the chat path is, and what it needs

A small program, the server, runs on your own Mac, inside a container, and offers the tool's operations to a chat.
The chat's own service calls the server over the internet, so the server gets a public address for the time you are
working. Every request must carry a key; without it the server answers with a 401 status and a short "unauthorised"
message, and nothing else.

You need:

- A Mac that stays awake and online while you work (the launcher keeps it awake while its window is open).
- A vault, as in [Getting started](getting-started.md) or, with no terminal, [GitHub Desktop](#your-vault-with-no-terminal-github-desktop), kept in a folder outside Documents, Desktop, Downloads and
  iCloud (macOS hides those from the server's container; the launcher offers a copy if yours is there).
- A container runtime: Colima (the one this page uses). Docker Desktop is the untested alternative.
- Tailscale, with its command line.
- A chat that accepts an MCP server and an API key, and your own account there. This page uses
  inference.coop's chat as one example, because it is the one that was tried. Any chat that works with the
  OpenAI API and lets you add an MCP server should do; that has not been checked for any other.
- The app `SCAT Chat.app` (under "Install once").

## The three actors

- The chat **helps**. The assistant drafts text, proposes nodes and links, and calls the tool's operations. It holds
  no authority.
- You, the coder, **decide**. You read, interpret, and set `done` yourself.
- The tool **checks**. It owns conformance: whether the vault fits the structure.

The server cannot set a narrative to `done` or move one out of `done`, so the assistant cannot, by construction.
The rules the assistant follows are in `contracts/assistant.md`; what is a rule and what is a norm is on the [norms](norms.md) page.

## Your vault with no terminal: GitHub Desktop

Getting started types its git commands in Terminal. On the chat path you can do the same four jobs, clone, remove
the example, commit and push, with [GitHub Desktop](https://desktop.github.com), a free app from GitHub, and with
Finder. **These steps were not run for this page.** They use the app's standard menu and button names, and the
wording on your version may differ. If a name here is not on your screen, use the nearest one and tell the person
who set this up what you saw.

**Create your private repository first, on the website.** Do the **On the GitHub website** path of [Getting started](getting-started.md)
(creating your private repository): **Use this template**, then **Create a new repository**, with visibility **Private**.
Your notes are about real groups of people.

**Clone it.** Cloning downloads your repository to your Mac.

1. **In GitHub Desktop:** open the app.
2. **In GitHub Desktop:** sign in to your GitHub account when it asks.
3. **In GitHub Desktop:** choose **File** > **Clone Repository...** (the dialog is titled "Clone a Repository").
4. **In GitHub Desktop:** pick your new repository from the list under **GitHub.com**, or paste its address under
   **URL**.
5. **In GitHub Desktop:** set **Local path** to a folder outside Documents, Desktop, Downloads and iCloud (see "What
   you need").
6. **In GitHub Desktop:** choose **Clone**.

Your vault is the cloned folder. It holds `scat.toml`. In the preview, the template's default branch is `dev`; GitHub
Desktop shows the current branch at the top, and if it shows `main` choose `dev` from that list.

**Remove the example: your hands do it.** The template holds a worked example that you remove before you add your own
pages. **The assistant never deletes anything**, and the server has no operation that deletes a page or a folder (it can remove an edge's row, which only you ask for). You delete.

1. **In GitHub Desktop:** choose **Repository** > **Show in Finder**.
2. **In Finder:** drag these five folders to the Trash: `affordance`, `concern`, `group`, `narrative` and
   `technology`. Keep the `index` folder and everything else.
3. **In GitHub Desktop:** in the **Summary** box type `Remove the example`. (The **Changes** list above it shows the
   deleted pages.)
4. **In GitHub Desktop:** choose the button at the bottom left of the list, **Commit to main**. On a branch called
   `dev` it reads **Commit to dev**: it carries the current branch's name.
5. **In GitHub Desktop:** choose **Push origin** in the top bar.

Then, in the chat once the session is running, ask the assistant to run the check. It should say there are no problems.

**Commit and push your work, any time.** After the assistant records edges and you have read and set pages to `done`
in Obsidian, GitHub Desktop's **Changes** list shows every changed page. Read it. Type a summary, such as
`Code the notes from my first session`, choose **Commit to main** (or the branch's name), then **Push origin**. The
assistant does not commit or push; you do. Check the whole vault is clean first.

## Install once

You do these steps one time per Mac. Each ends with what you should see.

### 0. Get SCAT Chat.app

Today the app is not a download. The person who set this up builds it from the `scat-kg-tools` repository with
`deploy/build-app.sh` and hands it to you. The built app is not kept in the repository. If no one has built it for you, ask the person who set up your tools;
this guide cannot build it for you.

1. **In Finder:** drag `SCAT Chat.app` into your Applications folder. You should see an app called SCAT Chat there.

### 1. A container runtime: Colima

The server runs inside a container, a sealed box that can only reach the vault. Something on your Mac has to run
containers. Version 0.1 is for the Mac only, and this page uses Colima, which the launcher was run against. Docker
Desktop is the untested alternative: if you use it, open it and wait for it to say running before every session, and
tell the person who set this up what happened.

Colima has no graphical installer. It comes through Homebrew, the Mac's package manager.

1. **In a terminal:** open one: press Cmd-Space, type `Terminal`, and press Return. (Every "In a terminal" step below
   uses this window.)
2. **In a terminal:** run `brew --version`.
3. **In a terminal:** if step 2 printed nothing useful, install Homebrew by following the one command on
   <https://brew.sh>.
4. **In a terminal:** run the next command. It installs Colima and the `docker` command it needs.

    ```text
    brew install colima docker
    ```

5. **In a terminal:** run `colima version`. You should see a version number.

You do not start Colima yourself: SCAT Chat starts it (the first start takes a minute) and leaves it running when you
stop. If both Colima and Docker Desktop are installed, the launcher uses Colima.

### 2. Tailscale

Tailscale makes the public address.

1. **In a web browser:** download the Tailscale app from <https://tailscale.com/download>.
2. **In Finder:** open the downloaded file and install the app as it shows.
3. **In Tailscale:** open the app.
4. **In Tailscale:** sign in. You should see the Tailscale icon in the menu bar.
5. **In Tailscale:** open the menu from the menu bar icon (its wording may differ by version).
6. **In Tailscale:** choose the menu item that installs the command line tool, and accept any prompt. SCAT Chat needs
   the `tailscale` command and will say so if it is missing.

This page could not confirm the exact name of that menu item, so follow what your version of the app shows.

### 3. The one-time settings in your Tailscale account

The launcher never changes these itself. You will meet each of these when you first click SCAT Chat: if
one is missing, the launcher stops, says which, and offers to open the page. You may also do them now. Do not
change anything it does not name.

**HTTPS certificates.** What it does: gives your Mac a proper secure address. Why it is needed: the chat only
talks to secure addresses. **It publishes your Mac's name in a public record that cannot be erased.** If the name
has your name or anything private in it, rename the Mac in Tailscale first (the launcher's own words: Machines,
then Edit machine name; that is in Tailscale's admin page in a web browser, which the launcher's dialog opens), and
only then switch HTTPS on. On the page the launcher opens, choose Enable HTTPS. If it is missing the launcher says
"Tailscale needs HTTPS switched on, once, before the public link can work." Click **Open the page**.

**Funnel.** What it does: lets the internet reach the one address the launcher publishes. Why it is needed: the
chat's service has to reach your server. On the page the launcher opens, approve Funnel (one click). If it is
missing, the launcher says "The public link did not start." and that Funnel is probably not allowed yet. Click
**Open the page**, approve it, then click SCAT Chat again.

### 4. Open the app the first time

SCAT Chat is not signed with an Apple developer certificate, so macOS stops it the first time. It is not harmful:
it is unsigned. What you can check is that it is the file the person who set this up gave you.

1. **In Finder:** right-click (or Control-click) SCAT Chat.
2. **In Finder:** choose **Open**.
3. **In Finder:** choose **Open** again in the dialog. macOS asks only once.

If macOS offers no **Open** button, open System Settings, then Privacy and Security, scroll down and look for
SCAT Chat with an **Open Anyway** button. This page could not check your version of macOS.

## Start a session

Colima needs no start by hand: SCAT Chat starts it. (With Docker Desktop, open it and wait for it to say running
first; the launcher does not start it.)

1. **In Finder:** open SCAT Chat from Applications.
2. **In SCAT Chat:** the first time, a window asks you to choose your vault: choose the folder that holds `scat.toml`.
   The launcher remembers it. (`change-vault` forgets it.)
3. **In SCAT Chat:** wait. The first time it needs the internet to get the server. It fetches the published image
   for its version ("Fetching the server, once."), and when none is published yet, as with a candidate before its
   release, it builds the server on your Mac ("Building the server, once.", a few minutes). Later sessions reuse
   it. The server runs as your own Mac user, set each time it starts, so it can read and write your vault.
4. **In SCAT Chat:** read the window that says "SCAT Chat is running." It shows an address, your vault, and two
   buttons, **Copy key** and **Stop**. It never shows the key. Leave the window open: your Mac stays awake while it is.

If your vault is in Documents, Desktop, Downloads or iCloud, the launcher offers to copy it to `~/SCAT/vault`.
Your original stays where it is. Work in the copy and bring edits back through git (commit and push from the copy,
pull in the original).

## Connect the chat

Every session you add the address and the key to the chat. The key is new each session, so an entry from an earlier
session no longer works: you delete it at the end ("Clean up"), and add a new one now.

As an example, in inference.coop's chat (lab run, 24 and 25 November, with lab material only):

1. **In the chat:** in the bar of icons on the left, click **MCP Settings**.
2. **In the chat:** choose to add an MCP server.
3. **In the chat:** where the form asks for a name, type `SCAT`.
4. **In SCAT Chat:** read the address in the window. It ends in `/mcp`.
5. **In the chat:** type the address into the server's address field.
6. **In the chat:** choose the Streamable HTTPS transport (the way the chat talks to a server over a secure web
   address).
7. **In the chat:** choose API key as the authentication.
8. **In SCAT Chat:** click **Copy key**. The key is now on your clipboard.
9. **In the chat:** paste the key into the API key field.
10. **In the chat:** save.
11. **In any app:** copy a word from anywhere, so your clipboard no longer holds the key.

Your chat's form may be worded differently. The fields are the same: address, transport, key. Where the chat asks
for a name for the server, use one you will recognise, for example "SCAT".

Do not paste the key anywhere else: see "The session key".

## Set up the skill and the saved agent

A **skill** is a package of instructions the chat loads for the assistant. A **saved agent** is the chat's feature
that keeps an assistant set up for a purpose (its instructions, skills and tools) so a new chat starts from it. The
assistant is still the actor and holds no authority. The skill here carries the assistant's rules and the norms
from `skills/scat-coding/SKILL.md`; a saved agent that uses it saves you from setting the chat up by hand each time.
You do this once. What you set up stays in the chat after Stop (see "Clean up").

The live run used inference.coop's chat, which has Skills and an Agent Builder. Where this page has not seen a
button's name, it says what to look for.

1. **In a web browser:** open the skill file,
   <https://raw.githubusercontent.com/DynamicalSystemsGroup/scat-kg-tools/dev/skills/scat-coding/SKILL.md>.
2. **In a web browser:** select all (Cmd-A).
3. **In a web browser:** copy (Cmd-C). Keep the tab open.
4. **In the chat:** look for **Skills** (in the chat's menus or settings; this page has not recorded where).
5. **In the chat:** choose to create a new skill.
6. **In the chat:** name it `scat-coding`.
7. **In the chat:** paste the text you copied. (If the form offers an upload instead, upload the file; whether the
   chat takes the file as it stands or asks for a different form was not recorded.)
8. **In the chat:** save the skill.
9. **In the chat:** open the **Agent Builder**.
10. **In the chat:** name the agent something you will recognise, for example "SCAT coder".
11. **In the chat:** choose a model in the agent's settings.
12. **In the chat:** add, as a tool, the server you added under "Connect the chat".
13. **In the chat:** add the chat's Ask User tool, if it offers one.
14. **In the chat:** choose the `scat-coding` skill as the agent's only skill.
15. **In the chat:** save the agent.
16. **In the chat:** open the Agent Builder and find its **Select** control. On inference.coop's instance, agents
    start from that Select, not from the model menu or from typing `@`.
17. **In the chat:** use **Select** to pick the agent. A new chat starts with it.

An agent keeps the server entry you chose when you saved it. The server's address and key change each session, so
each session you add a new entry (as in "Connect the chat") and, if the saved agent no longer lists a working server,
choose the new entry in the agent's tools again. This was not yet tried.

## Use

1. **In the chat:** start a chat with your saved agent (steps 16 and 17 below, in "Set up the skill and the saved agent").
   If you have no saved agent, start a chat with the model and the server entry instead, and say in your first
   message to follow the coding loop and the assistant's rules from the `scat-kg` server.
2. **In the chat:** attach your field notes with the paperclip (or drag and drop).
3. **In the chat:** write your request, naming the narrative. For example:

    ```text
    Help me code the narrative "dry-july". My field notes are attached. Draft the account as text in your reply; I
    will paste it into Obsidian myself.
    ```

4. **In the chat:** send it.

Then follow the coding loop below, one step per reply.

Whether your chat offers the server's three prompts (`code-a-narrative`, `explain-a-problem`, `review-before-done`)
was not tried. If it does, `code-a-narrative` starts the loop.

### The coding loop, in the chat and in Obsidian

This is the [coding loop](coding.md#the-coding-loop) with an assistant. What is a rule and what is a norm is on the [norms](norms.md) page.

1. **In the chat:** answer what the assistant asks about anything unclear. This is *interpreting*; it decides nothing.
2. **In the chat:** read the account the assistant drafts as text in its reply. This is *authoring*. It does not
   write the account into the vault.
3. **In Obsidian:** paste the account into the narrative page, and edit it there.
4. **In the chat:** confirm or change the nodes and links the assistant proposes from the account. This is *coding*.
5. **In the chat:** let the assistant make the pages that are missing and record each edge you confirmed, by the
   tool's operations. It never types a table row by hand.
6. **In the chat:** read the check the assistant runs on the narrative and its neighbours. This is *reviewing*. It
   quotes each problem as the tool reports it. A passing check means the structure fits. It does not mean the
   narrative is correct.
7. **In Obsidian:** read the page and decide whether the account matches the notes.
8. **In Obsidian:** set `status: done` yourself. The assistant never does, and the server refuses it if asked.

The server and Obsidian use the same folder, so what the assistant records appears in Obsidian. How quickly
Obsidian shows a change was not tried; if a page looks stale, reopen it. If you work in a copy (see above), the
same is true of that copy.

### Views

Ask the assistant for a view: a fingerprint, an edge table, the layered view or a trace. They come back as data in
the chat. To keep them, ask it to export the edge tables. That writes CSV and Markdown files into the `views/`
folder of your vault, which open in Obsidian like any file and are versioned with the rest.

### Lock a version

Locking a version is tagging a commit once the model is finished (see [Coding](coding.md#lock-a-version)). With
GitHub's features and no terminal:

**A GitHub Release, on the website.** Push your work first. Then open your repository on github.com, choose
**Releases**, then **Draft a new release**, then in the tag box type a name such as `v1` and choose the option to
create that new tag. Add a title and choose **Publish release**. The tag now names that commit.

**GitHub Desktop** commits and pushes, as shown under [your vault with no terminal](#your-vault-with-no-terminal-github-desktop); this page does not give its clicks for tagging.

This was read in GitHub's documentation, not run by a coder, and GitHub's wording changes.

## The session key

The session key is the key the chat sends with every request, so the server answers only the chat you connected. It
exists for one session. Here is where it lives and what to do with it.

- **Where it lives.** SCAT Chat makes a new key at each start and keeps it in your Mac's login keychain. It is never
  written to a file in your vault or in the repository, and it is never put where another program on your Mac can
  read it from the process list.
- **Where it is shown.** The launcher window shows the address and a **Copy key** button, never the key. The key
  reaches your clipboard only when you click **Copy key**.
- **At Stop.** Stop deletes the key from the keychain and clears your clipboard if it still holds the key. The message
  says "the key was deleted".

Good practice, for the key:

- Paste it only into the chat's server entry (the API key field in the chat's MCP settings). Do not paste it into a
  message to the assistant, an email, a document or a note, and do not save it anywhere.
- Click **Copy key** only when you are about to paste. After pasting, copy something else (a word from anywhere), so
  the clipboard no longer holds it.
- Do not screenshot or share your screen while you paste it.
- If you think the key has been seen by someone, click **Stop** at once, then start again. A new session has a new
  key; the old one no longer works.
- You never need to look at, write down or reuse a key. The next session has its own.

What each Stop removes, and what stays:

| Removed by Stop | Stays until you remove it |
|---|---|
| The public link (Funnel), the server's container, the key in your keychain, the key on your clipboard, the keep-awake | The server entry in the chat (you delete it: "Clean up") |
| | A skill or a saved agent you set up in the chat |
| | Your uploaded field notes, and your conversations, in the chat |
| | Your vault, and every change in it, on your Mac |
| | Colima (left running), Docker Desktop if you use it, and the server's image |

## Stop

Stopping has two parts here: stop the session on your Mac, and check that it stopped. Then clean up the chat
platform (next section).

1. **In SCAT Chat:** click **Stop**. (Quitting SCAT Chat does the same thing.) The public link goes off, the server is
   removed, your Mac may sleep again, the key was deleted, and your clipboard is cleared of the key. A message then
   says "Stopped. The public link is off, the server is removed, your Mac may sleep again, the key was deleted, and
   your clipboard holds no key."
2. **In a web browser:** open the address that ended in `/mcp`. It should not load. If it does, do step 1 again.

If the message says "Stopped, but I could not confirm:" followed by something, click SCAT Chat again, then Stop, or
restart your Mac. If it says the public link may still be on, open Tailscale and switch Funnel off. If it says the key
could not be deleted, open Keychain Access and delete the item it names.

Colima keeps running after Stop; it is not in your way. Closing Docker Desktop, if you use it, is up to you.

## Clean up

Clean up the chat platform each time, even in a relaxed project: the server entry holds a key that no longer works,
so delete it rather than leave it. This section is the default flow: delete the server entry, and the rest is your
choice. If your data policy needs everything removed from the platform, follow the strict option, [Leave no
trace](leave-no-trace.md), instead.

1. **In the chat:** in the bar of icons on the left, click **MCP Settings** (the last icon above your initials).
2. **In the chat:** next to the server you added ("SCAT"), click **Edit**.
3. **In the chat:** at the bottom left of the form, click the red **delete** button.
4. **In the chat:** confirm.

That is the clean-up the lab run did on 25 November. Delete only the server entry; the rest is optional:

- **A skill or a saved agent you set up stays** unless you remove it. Leave them for the next session, or remove them
  in the chat where you made them (where the chat keeps them for removal was not recorded; look where you created
  them).
- **Your uploaded field notes and conversations** stay in the chat account until you delete them there. Whether and how long the chat
  provider keeps them is not recorded here (to confirm). How to delete an uploaded file and a conversation was not
  recorded for this page; look for a file library and the conversation's menu in the chat.
- **Your vault** is on your Mac and is not touched.

Next session, add the new server entry (see "Connect the chat"); if the saved agent no longer lists a working server,
choose the new entry in its tools again (not yet tried).

## What leaves your machine

Your field notes, and everything the assistant reads from your vault through the tool, go to the chat provider's
service and to the model provider behind it. Settle what is allowed before you begin: see
[Data, rights and consent](data-and-consent.md). If the terms do not allow it, code without the assistant, as in
[Coding](coding.md). A strict policy can also ask that nothing stays on the platform afterwards: see
[Leave no trace](leave-no-trace.md). The key protects the server only from people who do not have it.

## When something goes wrong

The launcher's messages, and what to do.

| The window says | Do this |
|---|---|
| "SCAT Chat needs Docker Desktop, which is not installed." | The launcher found no `docker` command. Install Colima and docker as under "Install once", step 1 (or Docker Desktop), then click SCAT Chat. The message names Docker Desktop even when you use Colima. |
| "Docker Desktop is not running." | You use Docker Desktop. Open it from your Applications folder, wait until it says it is running, then click SCAT Chat. |
| "Colima would not start." | Restart your Mac, then click SCAT Chat again. If it repeats, tell the person who set this up. |
| "Docker does not answer." | Restart your Mac, then click SCAT Chat again. |
| "SCAT Chat needs Tailscale ... not installed." | Install Tailscale and its command line as under "Install once", sign in, click SCAT Chat. |
| "Tailscale is not running or you are not signed in." | Open Tailscale from the menu bar, sign in, click SCAT Chat. |
| "Tailscale needs HTTPS switched on" | The HTTPS setting above; click Open the page. |
| "The public link did not start" | The Funnel setting above; click Open the page. |
| "Choose your vault" | Choose the folder that holds `scat.toml`. |
| "Your vault is in a folder that macOS protects" | Say Copy, or move the vault outside Documents, Desktop, Downloads and iCloud. |
| "I could not keep a new key in your keychain." | If macOS asked for permission, click Allow, then click SCAT Chat again. |
| "Fetching the server, once." or "Building the server, once." | Wait. Not an error. |
| "Building the server failed" | Check you are online, then click SCAT Chat again. |
| "The server would not start" | Close any other SCAT Chat, then click again. |
| "The server did not answer" or "stopped right after starting" | Click again; if it repeats, tell the person who set this up. |
| "Stopped, but I could not confirm:" followed by what it could not confirm, then "click SCAT Chat again, then Stop, or restart your Mac, to be sure." | Do that: click SCAT Chat again, then Stop, or restart your Mac. If it names the public link, open Tailscale and switch Funnel off. |
| "SCAT Chat is already running." | Click Stop in its window, or quit the app, then start again. |

If you use Docker Desktop and the first run fails in a way that table does not cover, that is the untested part:
send the person who set this up the exact words in the window.
