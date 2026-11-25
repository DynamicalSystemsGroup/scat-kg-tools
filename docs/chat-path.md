# The chat path

!!! tip "Your next step"
    Read "What you need", then do "Install once". You do it one time per Mac.

The chat path lets you code a narrative by talking to an assistant in a chat window in your browser, with no
terminal. Obsidian stays where you read and decide.

!!! warning "What has and has not been tried"
    The launcher was run against Colima with a stand-in for Tailscale. A first connection to a chat worked in a
    lab run with lab material only. **Docker Desktop has not been tested end to end with this launcher yet**, and
    nobody has yet run the whole path as a coder following this page. Your first run is the real test. Where this
    page cannot vouch for a step, it says so. If a step fails and its message does not help, tell the person who
    set this up for you which step and what the window said. One more thing not checked: the launcher looks for the
    `docker` command only in `/usr/local/bin` and `/opt/homebrew/bin`. If Docker Desktop keeps it elsewhere, the
    launcher says Docker Desktop is not installed although it is; tell the person who set this up.

## What the chat path is, and what it needs

A small program, the server, runs on your own Mac and offers the tool's operations to a chat. The chat's own
service calls the server over the internet, so the server gets a public address for the time you are working.
Every request must carry a key; without it the server answers with a 401 status and a short "unauthorised" message, and nothing else.

You need:

- A Mac that stays awake and online while you work (the launcher keeps it awake while its window is open).
- A vault, as in [Getting started](getting-started.md), kept in a folder outside Documents, Desktop, Downloads and
  iCloud (macOS hides those from the server's container; the launcher offers a copy if yours is there).
- A container runtime: Docker Desktop, or Colima.
- Tailscale, with its command line.
- A chat that accepts an MCP server and an API key, and your own account there. This page uses
  inference.coop's chat as one example, because it is the one that was tried. Any chat that works with the
  OpenAI API and lets you add an MCP server should do; that has not been checked for any other.
- The app `SCAT Chat.app` (next section).

## The three actors

- The chat **helps**. The assistant drafts text, proposes nodes and links, and calls the tool's operations. It holds
  no authority.
- You, the coder, **decide**. You read, interpret, and set `done` yourself.
- The tool **checks**. It owns conformance: whether the vault fits the structure.

The server cannot set a narrative to `done` or move one out of `done`, so the assistant cannot, by construction.
The rules the assistant follows are in `contracts/assistant.md`.

## Install once

You do these steps one time. Each ends with what you should see.

### 0. Get SCAT Chat.app

Today the app is not a download. The person who set this up builds it from the `scat-kg-tools` repository with
`deploy/build-app.sh` and hands it to you. The built app is not kept in the repository. Put it in your
Applications folder. You should see an app called SCAT Chat there.

### 1. A container runtime

The server runs inside a container, a sealed box that can only reach the vault. Something on your Mac has to run
containers. Choose one.

**Docker Desktop (the default, with an installer you click through).**

1. Download Docker Desktop for Mac from Docker's site. Choose the version that matches your Mac's chip (Apple
   silicon or Intel; the Apple menu, then About This Mac, tells you which).
2. Open the downloaded file and drag Docker into Applications.
3. Open Docker from Applications. Accept its prompts, including any that ask for your Mac's password.
4. Wait until Docker says it is running. You should see the Docker icon in the menu bar at the top of your screen.

Docker Desktop is under Docker's own subscription terms, which some organisations must pay for. The terms are
at <https://www.docker.com/legal/docker-subscription-service-agreement/>.

Open Docker Desktop and wait for it to say running before you click SCAT Chat. The launcher does not start
Docker Desktop for you.

**Colima (an alternative, for coders comfortable with a terminal).** Colima has no graphical installer. It needs
Homebrew, the package manager from <https://brew.sh>. In Terminal, run these two commands, one at a time:

```text
brew install colima docker
colima version
```

You should see a version number from the second command. You do not start Colima yourself: SCAT Chat starts it
(the first start takes a minute). This is the route the launcher was run against.

Pick one runtime. If both are installed the launcher uses Colima.

### 2. Tailscale

Tailscale makes the public address.

1. Download the Tailscale app from <https://tailscale.com/download> and install it. Open it and sign in. You should
   see the Tailscale icon in the menu bar.
2. Put its command line in place. The Tailscale app has a menu item for installing the command line tool; look in
   its menu from the menu bar icon (its wording may differ by version). Choose it and accept any prompt. SCAT
   Chat needs the `tailscale` command and will say so if it is missing.

This page could not confirm the exact name of that menu item, so follow what your version of the app shows.

### 3. The one-time settings in your Tailscale account

The launcher never changes these itself. You will meet each of these when you first click SCAT Chat (step 4): if
one is missing, the launcher stops, says which, and offers to open the page. You may also do them now. Do not
change anything it does not name.

**HTTPS certificates.** What it does: gives your Mac a proper secure address. Why it is needed: the chat only
talks to secure addresses. **It publishes your Mac's name in a public record that cannot be erased.** If the name
has your name or anything private in it, rename the Mac in Tailscale first (the launcher's own words: Machines,
then Edit machine name; that is in Tailscale's admin page in a web browser, which the launcher's dialog opens), and
only then switch HTTPS on. The click: on the page the launcher opens, choose
Enable HTTPS. If it is missing the launcher says "Tailscale needs HTTPS switched on, once, before the public link
can work." Click **Open the page**.

**Funnel.** What it does: lets the internet reach the one address the launcher publishes. Why it is needed: the
chat's service has to reach your server. The click: on the page the launcher opens, approve Funnel (one click).
If it is missing, the launcher says "The public link did not start." and that Funnel is probably not allowed yet.
Click **Open the page**, approve it, then click SCAT Chat again.

### 4. Open the app the first time

SCAT Chat is not signed with an Apple developer certificate, so macOS stops it the first time. It is not harmful:
it is unsigned. What you can check is that it is the file the person who set this up gave you. Right-click (or
Control-click) the app and choose **Open**, then **Open** again in the dialog. macOS asks only once.

If macOS offers no **Open** button, open System Settings, then Privacy and Security, scroll down and look for
SCAT Chat with an **Open Anyway** button. This page could not check your version of macOS.

## Start a session

1. Open Docker Desktop and wait for it to say running (Colima needs nothing).
2. Open SCAT Chat. The first time, a window asks you to choose your vault: the folder that holds `scat.toml`. The
   launcher remembers it. (`change-vault` forgets it.)
3. The first time it builds the server, which takes a few minutes and needs the internet. A notification says
   "Building the server, once."
4. A window then says "SCAT Chat is running." and shows an address, a key, and the vault. The key is already on
   your clipboard. Your Mac stays awake while this window is open. Leave it open.

If your vault is in Documents, Desktop, Downloads or iCloud, the launcher offers to copy it to `~/SCAT/vault`.
Your original stays where it is. Work in the copy and bring edits back through git (commit and push from the copy,
pull in the original).

## Connect the chat

Every session you add the address and the key to the chat. The key is new each session, so the old entry stops
working; update it or delete it and add it again.

As an example, in inference.coop's chat (lab run, 24 and 25 November, with lab material only):

1. Open MCP settings and choose to add an MCP server.
2. Paste the address from the window. It ends in `/mcp`.
3. Choose the Streamable HTTPS transport, and API key as the authentication.
4. Paste the key (it is on your clipboard). Save.

Your chat's form may be worded differently. The fields are the same: address, transport, key.

Then start a conversation, attach your field notes, and say what you want. For example:

```text
Help me code the narrative "dry-july". My field notes are attached. Follow the coding loop and the assistant's rules
from the scat-kg server. Draft the account as text in your reply; I will paste it into Obsidian myself.
```

Whether your chat offers the server's three prompts (`code-a-narrative`, `explain-a-problem`, `review-before-done`)
was not tried. If it does, `code-a-narrative` starts the loop.

## The coding loop, in the chat and in Obsidian

This is the [coding loop](coding.md#the-coding-loop) with an assistant.

1. **Interpreting.** You give the field notes and name the narrative. The assistant asks about anything unclear; it
   does not decide.
2. **Authoring.** The assistant drafts the account as text in its reply. It does not write it into the vault. You
   read it, edit it, and paste it into the narrative page in Obsidian.
3. **Coding.** The assistant proposes the nodes and links the account names. You confirm. Then it makes the pages
   that are missing and records each edge you confirmed, by the tool's operations. It never types a table row by
   hand.
4. **Reviewing.** The assistant runs the check on the narrative and its neighbours, and quotes each problem as the
   tool reports it. A passing check means the structure fits. It does not mean the narrative is correct. You read
   the page in Obsidian and decide whether the account matches the notes.
5. **Done is yours.** You set `status: done` in Obsidian. The assistant never does, and the server refuses it if
   asked.

The server and Obsidian use the same folder, so what the assistant records appears in Obsidian. How quickly
Obsidian shows a change was not tried; if a page looks stale, reopen it. If you work in a copy (see above), the
same is true of that copy.

## Views

Ask the assistant for a view: a fingerprint, an edge table, the layered view or a trace. They come back as data in
the chat. To keep them, ask it to export the edge tables. That writes CSV and Markdown files into the `views/`
folder of your vault, which open in Obsidian like any file and are versioned with the rest.

## Lock a version

Locking a version is tagging a commit once the model is finished (see [Coding](coding.md#lock-a-version)). With
GitHub's features and no terminal:

**A GitHub Release, on the website.** Push your work first. Then open your repository on github.com, choose
**Releases**, then **Draft a new release**, then in the tag box type a name such as `v1` and choose the option to
create that new tag. Add a title and choose **Publish release**. The tag now names that commit.

**GitHub Desktop** can also commit, push and tag; this page does not give its clicks.

This was read in GitHub's documentation, not run by a coder, and GitHub's wording changes.

## Stop

Click **Stop** in the window, or quit SCAT Chat. Either does the same thing: the public link goes off, the server
is removed, your Mac may sleep again, the key is replaced, and your clipboard is cleared of the key. A message then
says "Stopped. The public link is off, the server is removed, your Mac may sleep again, the key was replaced, and
your clipboard holds no key."

If it says "Stopped, but I could not confirm:" followed by something, click SCAT Chat again, then Stop, or
restart your Mac. If it says the public link may still be on, open Tailscale and switch Funnel off. Delete the
server entry in your chat too; it no longer works.

Closing Docker Desktop is up to you; Stop does not quit it.

## What leaves your machine

Your field notes, and everything the assistant reads from your vault through the tool, go to the chat provider's
service and to the model provider behind it. Settle what is allowed before you begin: see
[Data, rights and consent](data-and-consent.md). If the terms do not allow it, code without the assistant, as in
[Coding](coding.md). The key protects the server only from people who do not have it.

## When something goes wrong

The launcher's messages, and what to do.

| The window says | Do this |
|---|---|
| "SCAT Chat needs Docker Desktop, which is not installed." | Install Docker Desktop as shown under "Install once" (or Colima with the docker command), then click SCAT Chat. |
| "Docker Desktop is not running." | Open Docker Desktop from your Applications folder, wait until it says it is running, then click SCAT Chat. |
| "Colima would not start." | Restart your Mac, then click SCAT Chat again. If it repeats, tell the person who set this up. |
| "Docker does not answer." | Restart your Mac, then click SCAT Chat again. |
| "SCAT Chat needs Tailscale ... not installed." | Install Tailscale and its command line as under "Install once", sign in, click SCAT Chat. |
| "Tailscale is not running or you are not signed in." | Open Tailscale from the menu bar, sign in, click SCAT Chat. |
| "Tailscale needs HTTPS switched on" | The HTTPS setting above; click Open the page. |
| "The public link did not start" | The Funnel setting above; click Open the page. |
| "Choose your vault" | Choose the folder that holds `scat.toml`. |
| "Your vault is in a folder that macOS protects" | Say Copy, or move the vault outside Documents, Desktop, Downloads and iCloud. |
| "Building the server failed" | Check you are online, then click SCAT Chat again. |
| "The server would not start" | Close any other SCAT Chat, then click again. |
| "The server did not answer" or "stopped right after starting" | Click again; if it repeats, tell the person who set this up. |
| "Stopped, but I could not confirm:" followed by what it could not confirm, then "click SCAT Chat again, then Stop, or restart your Mac, to be sure." | Do that: click SCAT Chat again, then Stop, or restart your Mac. If it names the public link, open Tailscale and switch Funnel off. |
| "SCAT Chat is already running." | Click Stop in its window, or quit the app, then start again. |

If you use Docker Desktop and the first run fails in a way that table does not cover, that is the untested part:
send the person who set this up the exact words in the window.
