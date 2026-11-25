# UA-M walkthrough, chat path: the chief engineer's script

You run the chat journey, J1 to J10, as you would use it: no terminal from J5 on. The assistant helps and holds no
authority; you, the coder, decide; the tool checks. This script does not teach the journey. For each stage it gives
where to enter, the steps, what "done" looks like, what to record, and where to resume. The manual path has its own
script, [`walkthrough-manual.md`](walkthrough-manual.md); run that one first, or take its J1 to J4 here as already done.

**Pass (MISSION.md, UA-M):** you complete the journey on both paths from the documentation without help, and judge the
documentation clear and navigable and the journey clear. Anything you flag is fixed on `dev`, the candidate is
refreshed, and you resume from the affected stage.

## Docs fixes pending

Another unit is fixing five documentation defects (log D-098, ruling 3). This script points to where each fix will be.
Until they land, a mismatch on these is known and is not a new finding; once they land, it is.

1. The fingerprint view's command: the coding guide says it is not a `scat` command; the analysis guide and the CLI
   reference give `scat fingerprint`. On the chat path the assistant asks for it as "a fingerprint" (J9).
2. No command to run the notebook. The chat path does not use the notebook; this matters on the manual path (J9).
3. The solo trial (J2) has no section of its own; it will be in [Getting started](../docs/getting-started.md).
4. No way is shown to see which commit a tag pins; it will be in [coding](../docs/coding.md#lock-a-version). On the
   chat path, GitHub shows the commit beside the tag on the release (J10 step 4).
5. No no-terminal route (GitHub Desktop) for clone, commit, push and removing the example on the chat path. It will be
   in [the chat page](../docs/chat-path.md#lock-a-version) and the Getting started page. Until then, J5 steps 1 and 2
   and J10 step 3 are held gaps: do what you can and record how.

## How to split the walk into sittings and resume

- **Start page:** the Pages preview, <https://dynamicalsystemsgroup.github.io/scat-kg-tools/>. The chat page is
  [`chat-path.md`](../docs/chat-path.md), "Coding in a chat" in the navigation. Do not open `src/` or `tests/`. The
  links below go to the same pages in this repository, for checking this script.
- **Sittings.** Stop only at the end of a stage. Each "Start a session" and "Stop" is a boundary: the server, its
  address and its key do not survive a stop, so each sitting that uses the chat begins with a new session and ends with
  **Stop**.

| Sitting | Stages | Run by | You are done when |
|---|---|---|---|
| A. Discover to terms | J1 to J4 | you (take them from the manual walk if done) | answers written, and the AI answer allows the chat path |
| B. Set up | J5 | you; the sign-ins and installs are yours | a window says the server is running and the chat's check quotes `no problems`; then Stop |
| C. Plan and capture | J6, J7 | you | `plan.txt`, the example cleared, field notes for one scenario and one architecture |
| D. Code | J8 | you, with the assistant | every narrative is `done`, set by you in Obsidian |
| E. Analyse and hand over | J9, J10 | you, with the assistant | a version is locked and handed over, and Stop confirmed |

**The chat testers (UA-A, log D-098, ruling 4).** Three testers run the chat journey: two on Haiku and one on Sonnet.
Their sessions are run by the ACE, not by you, light and spaced, and inside your sittings: after you have signed in
(GitHub, Docker Desktop, the public-link service, the chat account) and started a session, the ACE drives one tester at
a time in the browser pane, with lab material only, and ends each tester with Stop and a new key. You do not write the
testers' answers. Their findings are dispositioned before your walk of the same stage. *(default: one tester session
live at a time; the ACE sets the order and spacing.)*

- **Resume.** Read the stage's **Resume** line and check that state. A chat sitting always begins with "Start a
  session" and "Connect the chat" (J5), because the key is new each session. Your vault is the record: its git history
  shows where you stopped.
- **Your own elicitation.** Use the elicitation, field notes and groups from the manual walk, or make a new one. Use
  your own words, not the worked example's. Field notes sent to the chat leave your machine: use lab material only,
  and settle AI use first (J4).
- **Failing.** Do not work around a failure. Record the page, the step, what you did, the exact words in the window,
  and what you expected. The launcher's table "When something goes wrong" in `chat-path.md` is the docs' answer; if
  your case is not in it, that is a finding.

## What needs your sign-ins (held for you)

No agent has run this path as a coder, and Docker Desktop has not been tried end to end with the launcher
([`chat-path.md`](../docs/chat-path.md), first warning). These need you:

1. **GitHub**: your account, to make the private repository and to publish a release.
2. **Docker Desktop**: the download, and the Mac password it asks for.
3. **The public-link service** ([Install once](../docs/chat-path.md#install-once) names it): signing in, and two
   one-time settings in its account. One of them publishes your Mac's name in a public record that cannot be erased;
   the page says to rename the Mac first if its name is private.
4. **The chat service**: your own account, and the address, transport and key added in its MCP settings.
5. **macOS**: the first open of SCAT Chat.app, which is unsigned.
6. **SCAT Chat.app itself**: today it is built by the person who set this up and handed to you, not downloaded.

**Held gaps in the docs** (record what you actually did; docs fix 5): the docs' website path ends in `git clone`, a
terminal command, and the chat page gives no clone-free way to get the vault onto the Mac; removing the example (J6)
and committing and pushing (J10) are given only as terminal commands.

---

## J1 Discover

**Enter.** Open <https://dynamicalsystemsgroup.github.io/scat-kg-tools/> ([`index.md`](../docs/index.md)).

**Steps.** Read the page. Find the chat path from the navigation ("Coding in a chat") and from [Where next](../docs/index.md#where-next).

**Done.** You can say what SCAT turns into what, and where the chat path starts.

**Record.** Broken web links; whether a newcomer who wants an assistant would find `chat-path.md`.

**Resume.** Nothing to resume; reopen the home page.

## J2 Try

**Enter.** [`flow.md`](../docs/flow.md#first-try), "First try", then
[`getting-started.md`](../docs/getting-started.md#1-create-your-private-repository), "1. Create your private
repository" (the solo trial will have a section of its own there, docs fix 3).

**Steps.** The solo trial is the manual script's J2, on the manual path (*default*, MISSION.md: J2 runs on the manual path). Take it as done there.
If you have not run it, run it first.

**Done.** One narrative of your own is `done` in a throwaway repository, and its fingerprint (Outgoing links panel and
its `Edges told` table) was seen in Obsidian.

**Record.** Point to the manual script's J2 notes.

**Resume.** As the manual script's J2.

## J3 Decide

**Enter.** [`flow.md`](../docs/flow.md#the-steps), the steps table, step 3, and the sentence after it, and the pointer to
"The chat path".

**Steps.** Read the table and the chat path's [What the chat path is, and what it
needs](../docs/chat-path.md#what-the-chat-path-is-and-what-it-needs). Decide whether you will
organise an elicitation, and whether with an assistant.

**Done.** You can state yes or no, and whether the assistant is in.

**Record.** Whether the page told you what the chat path costs you (installs, accounts, a Mac that stays awake).

**Resume.** Nothing to resume; reopen `flow.md`.

## J4 Set terms

**Enter.** [`data-and-consent.md`](../docs/data-and-consent.md#the-choices), "The choices", choice 5 first, then the
[Before you start](../docs/data-and-consent.md#before-you-start) checklist.

**Steps.** Answer the nine choices. For AI use, name which data the chat provider's service may see, as
[`chat-path.md`, "What leaves your machine"](../docs/chat-path.md#what-leaves-your-machine), says. Write the answers outside the vault.

**Done.** All nine boxes are ticked and the AI answer allows the chat path for the material you will send, or you stop
here.

**Record.** Whether you could answer choice 5 for the chat from the pages alone.

**Resume.** Open your answers file; redo from the first unticked box.

## J5 Set up

**Enter.** [`getting-started.md`](../docs/getting-started.md#1-create-your-private-repository), "1. Create your private
repository" (website path), then [`chat-path.md`](../docs/chat-path.md) from the top: [What the chat path is, and what
it needs](../docs/chat-path.md#what-the-chat-path-is-and-what-it-needs), [Install once](../docs/chat-path.md#install-once),
[Start a session](../docs/chat-path.md#start-a-session), [Connect the chat](../docs/chat-path.md#connect-the-chat).

**Steps.**
1. Create the repository **private** from `scat-kg-template` on the GitHub website: open
   <https://github.com/DynamicalSystemsGroup/scat-kg-template>, choose **Use this template**, then **Create a new
   repository**, set the visibility to **Private**. Get the vault onto your Mac and record how (see the held gaps).
   Keep it outside Documents, Desktop, Downloads and iCloud.
2. Open the folder in Obsidian as a vault (**Open folder as vault**, version 1.9 or later). Keep the example for now;
   J6 uses it.
3. Install once, in the page's order: SCAT Chat.app (step 0), a container runtime (step 1; Docker Desktop is the one
   with no terminal), the public-link service and its command line (step 2), its two account settings (step 3), the
   first open of the app (step 4).
4. Start a session: open Docker Desktop and wait for it to say running; open SCAT Chat; choose the folder that holds
   `scat.toml` (if it is in Documents, Desktop, Downloads or iCloud the launcher offers a copy: record what you chose);
   wait for the first build.
5. Connect the chat: in the chat's MCP settings add the address from the window (it ends in `/mcp`), the Streamable
   HTTPS transport, API key authentication, and the key from your clipboard.
6. Ask the assistant for a check of the whole vault. The page does not give this sentence; record the words you used.

**Done.**
- The repository is private on GitHub, and the folder is open as a vault in Obsidian.
- A window says "SCAT Chat is running." and shows an address, a key and your vault.
- The assistant's reply to the check quotes the tool's result, `no problems`, for the vault with the example in it.

**Record.** Every step the page could not vouch for (it says so), each launcher message you saw and whether the page's
table covered it, and the exact words of any failure. Anything you guessed.

**Resume.** Open Docker Desktop, open SCAT Chat, wait for "SCAT Chat is running.", paste the new key into the chat's
server entry, and ask for the check again. The one-time installs are not redone.

## J6 Plan

**Enter.** [`planning.md`](../docs/planning.md).

**Steps.** As the [manual script's J6](walkthrough-manual.md#j6-plan), with your J4 answers: sessions, groups within the
cap in `scat.toml`, participation terms, how the notes are kept, `plan.txt` in the vault folder. The cap demo
([Groups and the cap](../docs/planning.md#groups-and-the-cap)) is a command; in a session ask the assistant to make a
new group page named `harbour-crews` while the example's three groups fill the cap of 3, and expect it to be refused
and to quote the page's message. The page does not give this chat form; record what happened. When the plan is done,
clear the example ([Start your own content](../docs/getting-started.md#5-start-your-own-content), a terminal command;
docs fix 5) and record how.

**Done.** `plan.txt` exists and names the sessions, the groups within the cap, the participation terms and how the notes
are kept; the cap refusal appeared and nothing was created; the example is cleared and the check prints `no problems`.

**Record.** As the manual script's J6, and how you cleared the example.

**Resume.** `plan.txt` exists in the vault folder, and the example's pages are gone.

## J7 Capture

**Enter.** [`facilitate-scenarios.md`](../docs/facilitate-scenarios.md), then
[`facilitate-architectures.md`](../docs/facilitate-architectures.md).

**Steps.** As the [manual script's J7](walkthrough-manual.md#j7-capture): field notes for one scenario and one architecture, past, future or mixed. Put
them in a form the chat can take as an attachment (the mission calls this a collection; record what the chat calls it).

**Done.** Your field notes exist and can be attached to the chat.

**Record.** As the manual script's J7, and what file form you used.

**Resume.** Find your field notes.

## J8 Code

**Enter.** [`chat-path.md`, "The coding loop, in the chat and in
Obsidian"](../docs/chat-path.md#the-coding-loop-in-the-chat-and-in-obsidian), with [`coding.md`, "The coding
loop"](../docs/coding.md#the-coding-loop).

**Steps.** Start a session (J5 steps 4 and 5). Attach the field notes and ask the assistant to help you code the
narrative, naming it. Then, for each narrative:
1. Interpreting: tell the assistant what the notes say and answer what it asks. It decides nothing.
2. Authoring: it drafts the account in its reply; you edit it and paste it into the narrative page in Obsidian.
3. Coding: it proposes the nodes and links the account names; you confirm; it makes the missing pages and records
   each confirmed edge through the tool.
4. Reviewing: it runs the check on the narrative and its neighbours and quotes each problem. You read the page
   against your field notes.
5. Set `status: done` yourself in Obsidian. Try once to ask the assistant to set it; the server must refuse.

**Done.**
- One scenario and one architecture are `done`, set by you in Obsidian.
- Each edge is a row of its narrative's `Edges told` table, and the assistant typed no row by hand.
- A passing check was never taken as "the narrative is correct": you read the page.
- What the assistant recorded appeared in Obsidian (reopen a page if it looks stale).
- The assistant could not set `done`.

**Record.** Each place the assistant overreached or asked you to decide too little; how quickly Obsidian showed a
change; whether the three prompts (`code-a-narrative`, `explain-a-problem`, `review-before-done`) were offered;
every guess.

**Resume.** Start a session, connect the chat, and ask the assistant for the status of each page. Continue with the
first page not at `done`.

## J9 Analyse

**Enter.** [`chat-path.md`, "Views"](../docs/chat-path.md#views), with [`analysis.md`, "The four
views"](../docs/analysis.md#the-four-views).

**Steps.**
1. Ask the assistant for a fingerprint, an edge table, the layered view and a trace, naming your own narrative and node.
2. Ask it to export the edge tables, and open the files in the `views/` folder of the vault in Obsidian. The chat path
   does not use the notebook.
3. Interpret what you see. If it sends you back to your field notes, go round the loop again (J8).

**Done.** The four views came back in the chat; CSV and Markdown files are in `views/` and open in Obsidian; you can
say what one view told you, and no view told you a story or group is better.

**Record.** Whether the views arrived refused or clean; whether `views/` was versioned with the vault; what the
views read like.

**Resume.** `views/` holds files and the assistant reports a clean check.

## J10 Hand over

**Enter.** [`chat-path.md`, "Lock a version"](../docs/chat-path.md#lock-a-version) and
[Stop](../docs/chat-path.md#stop), with [`coding.md`, "Lock a version"](../docs/coding.md#lock-a-version); and your J4
release, licence and rights answers.

**Steps.**
1. Ask the assistant for a whole-vault check. Read the result yourself.
2. Open the vault in Obsidian and look at it as [`coding.md`, "Look at it in
   Obsidian"](../docs/coding.md#look-at-it-in-obsidian) says, including a concern's Backlinks panel (it lists the
   narratives that name the concern).
3. Commit and push your work, which the chat path gives no clicks for (the chat page's [Lock a
   version](../docs/chat-path.md#lock-a-version) says GitHub Desktop can, without giving its clicks; docs fix 5).
   Record what you used.
4. Take a hand-over case: a contract delivery, a paper submission or a class project hand-in. Decide, as the coder,
   that the model is finished. On github.com, open your repository, choose **Releases**, then **Draft a new release**,
   type a tag name such as `v1`, create the new tag, add a title and choose **Publish release**.
   Note the commit the release page shows for the tag, if it shows one (docs fix 4).
5. Hand it over to the recipient the case names.
6. Click **Stop** in the SCAT Chat window. Delete the server entry in the chat.

**Done.**
- The whole-vault check is clean and the vault is navigable in Obsidian.
- The release and its tag are on GitHub, in a repository that is still private, and you can name the tag, the commit it
  pins and the recipient.
- The window says "Stopped. The public link is off, the server is removed, your Mac may sleep again, the key was
  replaced, and your clipboard holds no key."

**Record.** The tag, the commit and the recipient; how you pushed; any wording of GitHub that differed from the page;
the Stop message, in full, if it was not the one above.

**Resume.** Check the repository's Releases on github.com. If the tag exists, you are done. If not, start a session and
redo step 4. If Stop did not confirm, do what the page says in "Stop".

---

## When you are done

Judge, in your own words: is the documentation clear and navigable, and is the chat journey clear? List each stage you
flagged, with your notes. The fixes go to `dev` and the candidate is refreshed. Delete any throwaway repository from
GitHub yourself.
