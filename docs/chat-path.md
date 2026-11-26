# The chat path

!!! tip "Your next step"
    Read "What the chat path is, and what it needs", then do "Install once". You do that one time per Mac. After that,
    every session runs the same way: start, connect the chat, use, stop, clean up.

The chat path lets you code a narrative by talking to an assistant in a chat window in your browser, with no
terminal in the coding itself. Obsidian stays where you read and decide. This page walks one session from start to
clean-up. Each numbered step names one outcome and says where you do it: **In the chat**, **In SCAT Chat** (the small Mac app
that runs the server), **In the menu bar** (SCAT Chat's coloured dot and its menu), **In Finder**, **In GitHub Desktop**, **In Obsidian**, **In Tailscale** or **In a terminal**.

!!! warning "What has and has not been tried"
    The launcher was run against Colima with a stand-in for Tailscale. A first connection to a chat worked in a
    lab run with lab material only. Version 0.1 is for the Mac only. **Docker Desktop is the untested alternative to
    Colima** and has not been run end to end with this launcher. Nobody has yet run the whole path as a coder
    following this page, so your first run is the real test. Where this page cannot vouch for a step, it says so. If
    a step fails and its message does not help, tell the person who set this up for you which step and what the
    message said.
    One more thing not checked: the launcher looks for the `docker` command in `/usr/local/bin`, `/opt/homebrew/bin`
    and Docker Desktop's own folder (`/Applications/Docker.app/Contents/Resources/bin`). If it says Docker is not
    installed although it is, that is the likely cause; tell the person who set this up.

If your project's data policy is strict (an AI platform that must keep nothing, or "approved chatbot only"), see
[Leave no trace](leave-no-trace.md). You do not need it for an ordinary session.

## What the chat path is, and what it needs

A small program, the server, runs on your own Mac, inside a container, and offers the tool's operations to a chat.
The chat's own service calls the server over the internet, so the server gets a public address for the time you are
working. Every request must carry a key; without it the server answers with a 401 status and a short "unauthorised"
message, and nothing else.

You need:

- A Mac that stays awake and online while you work (SCAT Chat keeps it awake while a session runs).
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

**What SCAT Chat is.** SCAT Chat is a small Mac app that runs the SCAT MCP server, the tool's front end for the chat.
It has no window of its own: while a session runs it is a coloured dot in the Mac's menu bar (the strip at the top of
the screen), with a menu under it. It starts the server, makes the public address and the session key, and stops them
again. **Where it is:** in your Applications folder, once you do the step below. That step puts a copy of the app
there. Nothing is installed system-wide: the copy is the whole app, and deleting it removes it.

Today the app is not a download. The person who set this up builds it from the `scat-kg-tools` repository with
`deploy/build-app.sh` and hands it to you. The built app is not kept in the repository. If no one has built it for you, ask the person who set up your tools;
this guide cannot build it for you.

1. **In Finder:** drag `SCAT Chat.app` into your Applications folder. You should see an app called SCAT Chat there,
   a copy of the one you were given.

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

The menu item's name differs between versions of the app: choose the one that installs the command line tool.

### 3. The one-time settings in your Tailscale account

The launcher never changes these itself. You will meet each of these when you first start SCAT Chat: if
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
**Open the page**, approve it, then start SCAT Chat again.

### 4. Open the app the first time

SCAT Chat is not signed with an Apple developer certificate, so macOS stops it the first time. It is not harmful:
it is unsigned. What you can check is that it is the file the person who set this up gave you.

1. **In Finder:** right-click (or Control-click) SCAT Chat.
2. **In Finder:** choose **Open**.
3. **In Finder:** choose **Open** again in the dialog. macOS asks only once.

If macOS offers no **Open** button, open System Settings, then Privacy and Security, scroll down and look for
SCAT Chat with an **Open Anyway** button. The names in System Settings differ between versions of macOS.

## Start a session

Colima needs no start by hand: SCAT Chat starts it. (With Docker Desktop, open it and wait for it to say running
first; the launcher does not start it.) The first start on a Mac has no remembered vault, so it differs from the later
ones; the steps say which.

1. **In Finder:** open SCAT Chat from Applications.
2. **In SCAT Chat:** at the first start on this Mac only, read the note: "SCAT Chat now lives in the menu bar, at the
   top of your screen, near the clock", and click **OK**. It is shown once per Mac. There is no window: the dot is
   grey while SCAT Chat starts, green while it runs and red when there is a problem.
3. **In SCAT Chat:** at the first start, no vault is remembered, so a folder picker opens with the prompt "Choose your
   vault: the folder that holds your narratives (it has a file called scat.toml)." Choose the folder that holds
   `scat.toml`.
4. **In SCAT Chat:** at every later start it instead asks `Serve <vault>?`, naming the vault it remembers. Click
   **Use it**, or click **Choose another** and choose a different folder that holds `scat.toml` in the folder picker.
   It never serves a vault you have not just confirmed. If the remembered folder is gone, a note says so and the folder
   picker opens.
5. **In SCAT Chat:** wait. The first time it needs the internet to get the server. It fetches the published image
   for its version ("Fetching the server, once."), and when none is published yet, as with a candidate before its
   release, it builds the server on your Mac ("Building the server, once. The first time takes a few minutes."). Later
   sessions reuse it. The server runs as your own Mac user, set each time it starts, so it can read and write your vault.
6. **In the menu bar:** check that the dot is green. A notification then says "SCAT Chat is running. Click its dot in
   the menu bar: Copy address, then Copy key, and paste each into the chat." A problem shows as a red dot, a **Problem:** line in the menu and
   one alert, "SCAT Chat has a problem", that repeats the line (see "When something goes wrong").
7. **In the menu bar:** click the dot to open its menu. It shows State, Vault and Address lines, and **Copy address**,
   **Copy key**, **Change vault** and **Stop**. It never shows the key. Your Mac stays awake while SCAT Chat runs.

If your vault is in Documents, Desktop, Downloads or iCloud, the launcher offers to copy it to `~/SCAT/vault`.
Your original stays where it is. Work in the copy and bring edits back through git (commit and push from the copy,
pull in the original).

### Change vault

**Change vault** stops the server and starts it again, so the new session has a new session key. It asks for the vault
with the folder picker, not with `Serve <vault>?`. The chat's server entry still holds the old key, and the saved
agent's tool must be added again. Do these steps after the dot is green again.

If the stop inside Change vault could not be confirmed, the dot turns red and the alert "SCAT Chat has a problem" says
"Stopped, but I could not confirm:" and what. SCAT Chat stays open and does not start again. Choose **Stop** in the menu
to try again (see "Stop").

1. **In the menu bar:** click the dot, then click **Change vault**.
2. **In SCAT Chat:** choose the folder that holds `scat.toml` in the folder picker.
3. **In the menu bar:** check that the dot is green.
4. **In the menu bar:** open SCAT Chat's menu and click **Copy key**. A notification says "The key is on your
   clipboard."
5. **In the chat:** in **MCP Settings**, next to the server "SCAT", click **Edit**.
6. **In the chat:** paste the new key into the API key field.
7. **In the menu bar:** open SCAT Chat's menu and click **Copy address**. A notification says "The address is on your
   clipboard."
8. **In the chat:** if the address on your clipboard differs from the entry's address field, paste it there. If it is
   the same, leave the field as it is.
9. **In the chat:** save the entry.
10. **In the chat:** click **Connect** on the entry, and check that it shows connected.
11. **In the chat:** open the saved agent in the Agent Builder.
12. **In the chat:** remove the agent's tool that no longer works.
13. **In the chat:** add the server entry "SCAT" again as the agent's tool.
14. **In the chat:** save the agent.
15. **In any app:** copy a word from anywhere, so your clipboard no longer holds the key or the address.

The saved agent's tool is tied to the entry it was added from (see "Set up the skill and the saved agent"). Add it
again even though you only edited the entry.

## Connect the chat

Every session you add the address and the key to the chat. The key is new each session, so an entry from an earlier
session no longer works: you delete it at the end ("Clean up"), and add a new one now.

As an example, in inference.coop's chat (lab run, 24 and 25 November, with lab material only):

1. **In the chat:** in the bar of icons on the left, click **MCP Settings**.
2. **In the chat:** choose to add an MCP server.
3. **In the chat:** where the form asks for a name, type `SCAT`.
4. **In the menu bar:** open SCAT Chat's menu and click **Copy address**. A notification says "The address is on your
   clipboard." The address, which ends in `/mcp`, is now on your clipboard.
5. **In the chat:** paste the address into the server's address field.
6. **In the chat:** choose the Streamable HTTPS transport (the way the chat talks to a server over a secure web
   address).
7. **In the chat:** choose API key as the authentication.
8. **In the chat:** choose the header format the form offers for the key. The server accepts the key as an `X-API-Key`
   header or as an `Authorization: Bearer` header; choose either.
9. **In the menu bar:** open SCAT Chat's menu and click **Copy key**. A notification says "The key is on your
   clipboard." The key is now on your clipboard.
10. **In the chat:** paste the key into the API key field.
11. **In the chat:** tick the consent **I trust this application**. The form requires it: without it the entry cannot
    be saved.
12. **In the chat:** save.
13. **In the chat:** click **Connect** on the new entry. A new entry stays unconnected until you do.
14. **In the chat:** check that the entry "SCAT" shows connected. If it does not, check that the dot is green, then
    delete the entry and add it again with a fresh **Copy key**.
15. **In any app:** copy a word from anywhere, so your clipboard no longer holds the key.

Your chat's form may be worded differently. The fields are the same: address, transport, key, header format and the
consent. Where the chat asks for a name for the server, use one you will recognise, for example "SCAT".

Do not paste the key anywhere else: see "The session key".

## Set up the skill and the saved agent

A **skill** is a package of instructions the chat loads for the assistant. A **saved agent** is the chat's feature
that keeps an assistant set up for a purpose (its instructions, skills and tools) so a new chat starts from it. The
assistant is still the actor and holds no authority. The skill here carries the assistant's rules and the norms
from `skills/scat-coding/SKILL.md`; a saved agent that uses it saves you from setting the chat up by hand each time.
You do this once. What you set up stays in the chat after Stop (see "Clean up").

The live run used inference.coop's chat, which has Skills and an Agent Builder. Where a button's name is not given,
the step says what to look for.

1. **In a web browser:** open the skill file,
   <https://raw.githubusercontent.com/DynamicalSystemsGroup/scat-kg-tools/dev/skills/scat-coding/SKILL.md>.
2. **In a web browser:** select all (Cmd-A).
3. **In a web browser:** copy (Cmd-C). Keep the tab open.
4. **In the chat:** look for **Skills** (in the chat's menus or settings).
5. **In the chat:** choose to create a new skill.
6. **In the chat:** name it `scat-coding`.
7. **In the chat:** fill in the **Description**, which the form requires. Copy the text after `description:` in the
   file's first lines (it begins "Rules and habits for the assistant"), from the tab you kept open.
8. **In the chat:** paste the text you copied into the skill's text field. (If the form offers an upload instead, upload
   the file. If the chat does not accept the file as it stands, paste its text instead.)
9. **In the chat:** save the skill.
10. **In the chat:** open the **Agent Builder**.
11. **In the chat:** name the agent something you will recognise, for example "SCAT coder".
12. **In the chat:** choose a model in the agent's settings.
13. **In the chat:** add, as a tool, the server you added under "Connect the chat".
14. **In the chat:** add the chat's Ask User tool, if it offers one.
15. **In the chat:** choose the `scat-coding` skill as the agent's only skill.
16. **In the chat:** save the agent.
17. **In the chat:** open the Agent Builder and find its **Select** control. On inference.coop's instance, agents
    start from that Select, not from the model menu or from typing `@`.
18. **In the chat:** use **Select** to pick the agent. A new chat starts with it.

An agent's tool is tied to the server entry you chose when you saved it, and that tie does not survive deleting the
entry. The server's address and key change each session, and each session you add a new entry (as in "Connect the
chat"), so each session the saved agent's tool must be added again: open the agent in the Agent Builder, remove the
tool that no longer works, add the new entry, and save. This was seen on the lab run's old agent.

## Use

1. **In the chat:** start a chat with your saved agent (see "Set up the skill and the saved agent", above).
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

If your chat offers the server's three prompts (`code-a-narrative`, `explain-a-problem`, `review-before-done`),
`code-a-narrative` starts the loop.

### The coding loop, in the chat and in Obsidian

This is the [coding loop](coding.md#the-coding-loop) with an assistant. What is a rule and what is a norm is on the [norms](norms.md) page.

1. **In the chat:** answer what the assistant asks about anything unclear. This is *interpreting*; it decides nothing.
2. **In the chat:** read the account the assistant drafts as text in its reply. This is *authoring*. It does not
   write the account into the vault.
3. **In Obsidian:** paste the account into the narrative page, and edit it there.
4. **In the chat:** confirm or change the nodes and links the assistant proposes from the account. This is *coding*.
5. **In the chat:** let the assistant make the pages that are missing.
6. **In the chat:** let the assistant record each edge you confirmed, by the tool's operations. It never types a
   table row by hand.
7. **In the chat:** read the check the assistant runs on the narrative and its neighbours. This is *reviewing*. It
   quotes each problem as the tool reports it. A passing check means the structure fits. It does not mean the
   narrative is correct.
8. **In Obsidian:** read the page and decide whether the account matches the notes.
9. **In Obsidian:** set `status: done` yourself. The assistant never does, and the server refuses it if asked.

The server and Obsidian use the same folder, so what the assistant records appears in Obsidian. If a page
looks stale in Obsidian, reopen it. If you work in a copy (see above), the
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

**GitHub Desktop** commits and pushes, as shown under [your vault with no terminal](#your-vault-with-no-terminal-github-desktop). For tagging, use the release on the website, above. GitHub's wording changes: use the nearest name on your screen.

## The session key

The session key is the key the chat sends with every request, so the server answers only the chat you connected. It
exists for one session. Here is where it lives and what to do with it.

- **Where it lives.** SCAT Chat makes a new key at each start and keeps it in your Mac's login keychain. It is never
  written to a file in your vault or in the repository, and it is never put where another program on your Mac can
  read it from the process list.
- **Where it is shown.** SCAT Chat's menu shows the address and has **Copy address** and **Copy key** items, never the
  key. The key reaches your clipboard only when you choose **Copy key**.
- **At Stop.** Stop deletes the key from the keychain and clears your clipboard if it still holds the key. The alert
  says "the key was deleted".

Good practice, for the key:

- Paste it only into the chat's server entry (the API key field in the chat's MCP settings). Do not paste it into a
  message to the assistant, an email, a document or a note, and do not save it anywhere.
- Choose **Copy key** only when you are about to paste. After pasting, copy something else (a word from anywhere), so
  the clipboard no longer holds it.
- Do not screenshot or share your screen while you paste it.
- If you think the key has been seen by someone, choose **Stop** at once, then start again. A new session has a new
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

1. **In the menu bar:** open SCAT Chat's menu and click **Stop**. Stop switches off the public link, removes the server,
   lets your Mac sleep again, deletes the key from your keychain and clears your clipboard of the key. It shows the
   result in one alert.
2. **In SCAT Chat:** read the alert titled "SCAT Chat stopped". It says "Stopped. The public link is off, the server is
   removed, your Mac may sleep again, the key was deleted, and your clipboard holds no key." It is an alert, not a line
   in the menu.
3. **In SCAT Chat:** click **OK** on the alert. SCAT Chat quits, and its dot leaves the menu bar.
4. **In a web browser:** open the address that ended in `/mcp`. It should not load.

**When Stop could not confirm.** The alert is then titled "SCAT Chat has a problem" and says "Stopped, but I could not
confirm:" followed by what it could not confirm, then "choose Stop in the SCAT Chat menu to try again, or restart your
Mac, to be sure." SCAT Chat stays open, with a red dot. Do not open SCAT Chat again: that would start a new session.
Choose **Stop** in its menu again, or restart your Mac. If the public link may still be on, open Tailscale and switch Funnel off. If the public link could not be checked
because Tailscale was not found, install or open Tailscale and check it. If the server container is still there, restart
your Mac to be sure. If your Mac may stay awake, restart it to be sure. If the key could not be deleted, open Keychain
Access and delete the item named in the alert. If the key is still on your clipboard, copy something else over it.

**Two cases, two answers.** A problem while SCAT Chat is starting (a red dot and the alert "SCAT Chat has a problem",
with a message that ends "choose Stop in the SCAT Chat menu, then open SCAT Chat again") leaves SCAT Chat open: choose
**Stop**, fix the cause, then open SCAT Chat again. A Stop that could not confirm leaves it open too, but there you
choose **Stop** again and do not open SCAT Chat.

Colima keeps running after Stop; it is not in your way. Closing Docker Desktop, if you use it, is up to you.

## Clean up

Clean up the chat platform each time, even in a relaxed project: the server entry holds a key that no longer works,
so delete it rather than leave it. This section is the default flow: delete the server entry, and the rest is your
choice. If your data policy needs everything removed from the platform, follow [Leave no
trace](leave-no-trace.md), instead.

1. **In the chat:** in the bar of icons on the left, click **MCP Settings** (the last icon above your initials).
2. **In the chat:** next to the server you added ("SCAT"), click **Edit**.
3. **In the chat:** at the bottom left of the form, click the red **delete** button.
4. **In the chat:** confirm.

That is the clean-up the lab run did on 25 November. Delete only the server entry; the rest is optional:

- **A skill or a saved agent you set up stays** unless you remove it. Leave them for the next session, or remove them
  in the chat where you made them (look where you created
  them).
- **Your uploaded field notes and conversations** stay in the chat account until you delete them there. How long the chat
  provider keeps them is set by the provider: ask it, or read its terms. To delete an uploaded file and a conversation,
  look for a file library and the conversation's menu in the chat.
- **Your vault** is on your Mac and is not touched.

Next session, add the new server entry (see "Connect the chat"). A saved agent's tool does not survive deleting the
server entry it was tied to, so open the saved agent in the Agent Builder, remove the tool that no longer works, add
the new entry, and save (seen on the lab run's old agent).

## What leaves your machine

Your field notes, and everything the assistant reads from your vault through the tool, go to the chat provider's
service and to the model provider behind it. Settle what is allowed before you begin: see
[Data, rights and consent](data-and-consent.md). If the terms do not allow it, code without the assistant, as in
[Coding](coding.md). A strict policy can also ask that nothing stays on the platform afterwards: see
[Leave no trace](leave-no-trace.md). The key protects the server only from people who do not have it.

## When something goes wrong

SCAT Chat's messages, and what to do. A problem shows as a red dot, a **Problem:** line in the menu and one alert,
"SCAT Chat has a problem". The alert repeats the line. A message that ends "choose Stop in the SCAT Chat menu, then
open SCAT Chat again" is a problem at start: SCAT Chat is still open with a red dot. Choose **Stop**, fix the cause, then
open SCAT Chat again. The one exception is a Stop that could not confirm (last rows). Quotes below are the words SCAT Chat uses; long
ones are cut with "...".

| SCAT Chat says | Do this |
|---|---|
| "SCAT Chat needs a container runtime: Colima (recommended) or Docker Desktop. Neither is installed. ..." | Install Colima as shown under "Install once" (or Docker Desktop, untested). Then choose **Stop** in the SCAT Chat menu, then open SCAT Chat again. |
| "Colima would not start. Restart your Mac, then choose Stop in the SCAT Chat menu, then open SCAT Chat again. ..." | Do that. If it still fails, tell the person who set this up that Colima's start failed. |
| "Docker Desktop is not running. Open Docker Desktop from your Applications folder, wait until it says it is running, ..." | You use Docker Desktop. Do that, then choose **Stop** in the SCAT Chat menu, then open SCAT Chat again. |
| "Docker does not answer. Restart your Mac, then choose Stop in the SCAT Chat menu, then open SCAT Chat again." | Do that. |
| "SCAT Chat needs Tailscale, which makes the public link, and it is not installed. ..." | Install Tailscale and its command line as under "Install once", sign in, then choose **Stop** in the SCAT Chat menu, then open SCAT Chat again. |
| "Tailscale is not running or you are not signed in. Open Tailscale from the menu bar at the top of your screen, sign in, ..." | Do that, then choose **Stop** in the SCAT Chat menu, then open SCAT Chat again. |
| "Tailscale needs HTTPS switched on, once, before the public link can work." (a dialog with **Open the page** and **Close**), then "Nothing was started: HTTPS is not switched on in Tailscale yet" | The HTTPS setting above. Read the Mac's name the dialog shows, click **Open the page**, switch on Enable HTTPS, then choose **Stop** in the SCAT Chat menu, then open SCAT Chat again. |
| "The public link did not start." (a dialog with **Open the page** and **Close**), then "The public link did not start (Funnel is probably not allowed yet: ...)" | The Funnel setting above. Click **Open the page**, approve Funnel, then choose **Stop** in the SCAT Chat menu, then open SCAT Chat again. |
| "The vault folder I remembered is gone (...). Choose it again on the next screen." | Not an error. Choose the folder that holds `scat.toml` in the folder picker. |
| "No vault was confirmed, so nothing was started." or "No vault was chosen, so nothing was started." | You closed the question or the folder picker. Choose **Stop** in the SCAT Chat menu, then open SCAT Chat again and answer it. |
| "I cannot open that folder." | Choose **Stop** in the SCAT Chat menu, then open SCAT Chat again and choose your vault folder. |
| "Your vault is in ..., a folder that macOS keeps private from the server's container, so the server cannot read it there." (a question, "Make the copy now?", with **Copy** and **Cancel**) | Click **Copy**. Your original stays where it is. Or move the vault outside Documents, Desktop, Downloads and iCloud. |
| "Nothing was copied or started. ..." | You clicked **Cancel**. Move your vault outside Documents, Desktop, Downloads and iCloud, or choose **Stop** in the SCAT Chat menu, then open SCAT Chat again and click **Copy**. |
| "Your vault is in a folder that macOS protects, ... and ~/SCAT/vault already exists, so I will not copy over it." | Choose **Stop** in the SCAT Chat menu, then open SCAT Chat again and choose `~/SCAT/vault`, or a folder outside Documents, Desktop, Downloads and iCloud. |
| "The copy failed, so nothing was started. ..." | If macOS asked whether SCAT Chat may use your Documents folder, click Allow. Then choose **Stop** in the SCAT Chat menu, then open SCAT Chat again. |
| "Fetching the server, once." or "Building the server, once. The first time takes a few minutes." (a notification) | Wait. Not an error. |
| "Starting Colima, the program that runs the server's container. This can take a minute." or "Waiting for the server to answer." or "Switching on the public link." (a notification) | Wait. Not an error. |
| "Copied your vault to ~/SCAT/vault. Remember: edits made there must be pulled back through git." (a notification) | Not an error. See "Start a session". |
| "The server's recipe is missing from this copy of SCAT Chat. Download the app again." | Ask the person who set this up for a fresh copy of the app. |
| "Building the server failed. The last lines say: ..." | Check you are online, then choose **Stop** in the SCAT Chat menu, then open SCAT Chat again. |
| "I could not keep a new key in your keychain. ..." | If macOS asked for permission, click Allow. Then choose **Stop** in the SCAT Chat menu, then open SCAT Chat again. |
| "The server would not start: ..." | Make sure no other SCAT Chat is open and the port is free. Then choose **Stop** in the SCAT Chat menu, then open SCAT Chat again. |
| "The server stopped right after starting. Its last words: ..." | Choose **Stop** in the SCAT Chat menu, then open SCAT Chat again. If it repeats, tell the person who set this up. |
| "The server did not answer within ... seconds." or "The server answers but does not accept its own key." | Choose **Stop** in the SCAT Chat menu, then open SCAT Chat again. If it repeats, tell the person who set this up. |
| "SCAT Chat stopped unexpectedly." | Choose **Stop** in the SCAT Chat menu, then open SCAT Chat again. If it repeats, tell the person who set this up. |
| "SCAT Chat is already running. Click Stop in its menu (or quit the app) before starting it again." | Open its menu in the menu bar and choose **Stop**, then open SCAT Chat again. |
| "Stopped, but I could not confirm:" followed by what it could not confirm, then "choose Stop in the SCAT Chat menu to try again, or restart your Mac, to be sure." (the alert "SCAT Chat has a problem", after you chose Stop) | SCAT Chat stays open with a red dot. Choose **Stop** again, or restart your Mac. Do not open SCAT Chat again. Then the remedy for what it names: public link may still be on, open Tailscale and switch Funnel off; server container still there or your Mac may stay awake, restart your Mac; key could not be deleted, delete the named item in Keychain Access; key still on your clipboard, copy something else over it. |
| "SCAT Chat is running. Click its dot in the menu bar: Copy address, then Copy key, and paste each into the chat." or "The address is on your clipboard." or "The key is on your clipboard." (a notification) | Not an error. See "Connect the chat". |
| "SCAT Chat stopped" (an alert) | Not an error: Stop worked. See "Stop". |

If you use Docker Desktop and the first run fails in a way that table does not cover, that is the untested part:
send the person who set this up the exact words SCAT Chat showed.
