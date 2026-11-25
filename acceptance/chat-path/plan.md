# The chat-path sitting plan (WP20-G3, UA-A chat path)

This is the ACE's plan for running the three chat-path testers (two on Haiku, one on Sonnet: "most on Haiku", D-098)
in the chief engineer's sittings, light and human-paced, with lab material only. It is written now and run later.
Nothing here has been run. Words follow `GLOSSARY.md`.

| Tester | Model | Persona and brief | Comfort | Domain (invented) | Hand-over case |
|---|---|---|---|---|---|
| c1 | Haiku | `briefs/c1-neighbourhood-organiser-haiku.md` | at ease with websites and chat assistants | watering young street trees | contract delivery |
| c2 | Sonnet (control) | `briefs/c2-careful-organiser-sonnet.md` | new to all of it, careful and literal | a pantry's Saturday collection | paper submission |
| c3 | Haiku | `briefs/c3-hurried-organiser-haiku.md` | at home in chat, in a hurry, new to GitHub | a school walking bus | class project hand-in |

Counts: three testers, nine sittings (A, B and C each), all run by the ACE as the tester's hands in the chief engineer's
sittings. Each tester ends torn down, with its key rotated.

## How the work is split

| Who | Does | Never does |
|---|---|---|
| **The tester** (a fresh agent, on the model its brief names) | Reads the brief only. Each turn sends one request (READ, LOOK, SAY, DO, ASK A PERSON). Supplies the words typed to the chat assistant. Judges what comes back. Writes the report. | Sees a key, a password, the repository's files, `src/` or `tests/`. Has no browser. |
| **The ACE, as the tester's hands** | Drives the browser pane and the Mac's windows exactly as the tester requests, and pastes back what it sees, word for word. Keeps the run record. Runs the teardown checks. | Chooses a step, types words the tester did not give, explains the project to the tester, corrects the tester's words, enters a credential or key. |
| **The chief engineer** | Sign-ins, the app, the key, every setting in an account, the container runtime app, the public-link steps, committing and pushing in GitHub Desktop when the pages send a person there, and deciding what happens to the scratch repositories afterwards. | Is not asked questions during a stage except through the tester's ASK A PERSON. |

One tester at a time. Sittings are split by stage (below), and teardown follows every sitting that opened a session.

Deletions. The assistant in the chat holds no authority and deletes nothing. Every deletion in this plan (the chat's
server entry, test conversations and attached files, any file) is done by a person's hands: the ACE's, in the browser,
on the tester's word, or the chief engineer's. The assistant only advises.

The tester's model is its own. The assistant inside the chat is a separate choice: the chief engineer picks it once
and the ACE uses the same one for all three testers *(default)*, so any difference between the reports comes from the
tester and the persona, not the assistant. Record the choice in each report.

c2 differs from c1 in two things, comfort and model *(default)*. c3 differs from c1 in comfort only (same model).
If c1 and c2 differ, the ACE decides, and logs, whether a further run (c1's persona on Sonnet) is needed to tell the
docs from the user.

## Before the sitting

Do these once, before the first tester. Mark each as done with the real time (`date -Iseconds`).

1. **Candidate.** The Pages preview and the template pin the same commit; record it. **Relies on WP18's docs:** the
   preview must hold `chat-path/` and `reference/mcp/`. If either page is missing, stop: the candidate is wrong.
2. **Chief engineer, himself, once:** install what `chat-path` says, from the page and in its order, and record each
   step and what the window said. This is the first real run of the page by a coder.
   - The container runtime app the page names first is **untested** with this launcher (the page says so). If its
     install or the app's first start fails, record the exact words in the window. That is a WP18 finding, not a tester finding, and the
     sitting waits for the fix. The page's other runtime is the route that was run; fall back to it only if he chooses, and record
     that the page's default was not the one used.
   - SCAT Chat.app is built from the repository by the person who sets up and handed over. It is not signed: the page's right-click Open step is his.
   - The public-link service's install and sign-in are his. So are its one-time certificate step (rename the machine
     to a neutral name first, because the name is published permanently) and its approval to publish. The ACE never
     does these, and runs no command of that service during setup.
   - Lab material only. The chat account is his. He signs in to the chat and to GitHub in the browser pane himself.
3. **Chat.** In the chat, choose the assistant model and record it. Note whether the chat offers a collection for
   files; the briefs allow either.
4. **Evidence folder.** Create it outside this repository (see "Evidence") and start the run record.
5. **Clean slate.** No SCAT Chat window open, no server entry in the chat, no old scratch repository for these testers. If the chat holds an old server entry from the lab run, the chief engineer deletes it by hand.
6. **Brief check.** Run the checks in "Checks on the kit" below; all pass.
7. **Fresh testers.** Prepare three fresh agents, c1, c2 and c3, one at a time. Each gets its brief and the report
   template, and nothing else: no persona file, no README, no repository, no plan.

## Per tester steps

Run c1 completely, tear down, then c2, then c3. For each tester, three sittings; a sitting ends only at a stage boundary and
only after teardown if a session was opened.

**Sitting A: J1 to J4. No session, no key.** The tester works from the Pages and GitHub's website only.

1. Record the start (real time), the tester's model, the candidate commit.
2. Give the tester its brief and the report template. Take its first request.
3. Loop: the tester sends one request; the hands do exactly that, paste back the result word for word (screenshot
   saved and named, see "Evidence"); log request, action, result and time in the run record. Never batch two requests.
4. J2: the chief engineer is signed in to GitHub in the browser pane. The hands do the website path of
   `getting-started`, as the tester asks, in his account, with the repository **private**, named by the tester. The
   hands never enter credentials. If GitHub asks for any, stop and ask him.
5. J4: the tester writes its nine answers in the report. Nothing is saved to the repository unless a page says where.
6. At J4's end the sitting stops (see "Resume").

**Sitting B: J5 to J7. One short session.**

1. Chief engineer: start SCAT Chat as the page says (open the container runtime app first if the page names it). **Relies on
   WP18's docs:** the window's words are the evidence; paste them. If a step fails, see "If a docs step fails".
2. The key is on his clipboard. **He** pastes it into the chat's server form (address, Streamable HTTPS, API key); the
   hands and the tester never see or type it. The hands fill the other fields as the tester asks.
3. J5: the tester reasons from the page; the hands get the repository onto the Mac as the page says (GitHub Desktop's
   Clone, with the Local path set outside Documents, Desktop, Downloads and iCloud). **Relies on WP18's docs:** the
   chat-path page's GitHub Desktop section. If the tester says the page does not say how, or a step fails as written,
   that is a finding; the chief engineer then does that step, recorded as "a person, because the page left nowhere to
   go". The vault is wherever the Local path points. The hands open that folder as a vault in Obsidian (computer use,
   if he has granted it; otherwise he does). Obsidian itself is UA-M's: the opening is shown by a listing of the folder,
   which holds the Obsidian settings.
4. J5's check runs on the untouched template through the chat: one message from the tester, the answer pasted. Then
   the chief engineer clicks **Stop** and the teardown below runs. J6 and J7 need no session.
   J5 then ends with the example removed, as the page's "Remove the example" step says, with no session open: the
   hands do it on the tester's requests (Show in Finder, drag the example's folders to the Trash, commit and push in
   GitHub Desktop). The assistant never deletes. The hands paste a listing of the folder showing them gone; if the page
   does not say how, that is a finding and the chief engineer does the step.
5. J6: the hands write the tester's plan words into the file `planning` names, in the vault folder.
6. J7: the hands turn the lab notes in the brief into files, exactly the notes and nothing else, and attach them to
   a new conversation in the chat (a collection if the chat offers one). One message asks the assistant what it can
   see. J7 needs the chat but not the server, so no session is open: the sitting ends with the J5 teardown already
   done. The server entry stays out of this conversation. The hands delete the conversation and the attached files at
   the end of the sitting, as far as the chat allows. The assistant is never asked to delete.

**Sitting C: J8 to J10. The long session.**

1. Chief engineer starts SCAT Chat again as the page says (this tests starting a second time). He updates the chat's
   server entry with the new key (the page says the old one stops working), or deletes it and adds it again.
2. J8: the tester takes one story and one design proposal round the coding loop. The assistant drafts in its reply;
   the tester edits it; the hands paste the tester's final words into the page in Obsidian or in the file; the
   assistant proposes and records; the check runs. **Setting a page finished is the tester's decision,** made after it
   has read the page; the hands set it, on its word, with a screenshot, in Obsidian. If the assistant offers to set
   it, or the server is asked, log what it said word for word as a finding (the page says the server refuses).
3. J9: the four views are asked of the assistant; the tester's reading is two sentences each; the written tables are
   shown in the vault folder (the hands list the folder). If a view sends the tester back to J8, it goes back.
4. J10: clean whole-vault check through the chat. **Relies on WP18's docs:** saving and pushing from the Mac without a
   terminal, as the page's GitHub Desktop section says. If the tester says the page does not say how, or a step fails
   as written, that is a finding; the chief engineer then saves and pushes the work in GitHub Desktop at the tester's
   word. The hand-over is a locked version: the hands then draw the tag as the page gives, on github.com: Releases, Draft a new release, a new
   tag of the tester's name, Publish. No terminal is used. The hands read the tag and the commit it points at, note the
   recipient the hand-over case names (from the tester's words), and paste them back, with a screenshot, for the
   report. The tester stops the session by asking the person; the chief engineer clicks Stop. The deletions the page
   names (the chat's server entry, the test conversations and attached files) are done by the hands on the tester's
   word, never by the assistant.
5. Run the teardown, then the report is written by the tester and filed by the ACE.

### If a docs step fails

A step that fails as the page shows it is a **blocking** finding, recorded with the window's exact words. Do not fix
it on the spot. The sitting then does this:

1. The tester says where it is stuck. The hands paste the exact words on screen.
2. Try the page's own "When something goes wrong" table once, as the tester asks. If that works, record the step as
   "worked only with the table" (not blocking, a finding).
3. If it does not work, stop the tester at that stage ("not reached" for the rest), run teardown, and file the partial
   report. The ACE logs the defect before anyone fixes it, and the stage reruns with a fresh tester after the fix.
4. Do not retry a failing step in a loop. At most one retry of a step, and only after the table's advice.

## Pacing

The whole run is light and human-paced. These are the limits *(defaults)*:

- One tester, one session, one conversation at a time. Never two testers or two chat tabs in parallel.
- The hands send a message to the assistant only after the previous answer has finished arriving, has been read, and
  the tester has asked for the next one. At least 20 seconds between messages. No resends, no loops, no scripted
  sequences, no bursts; a failed message is not resent without the tester's word.
- At most 40 messages to the assistant per tester over the whole journey. Reaching 35 is a signal to stop and
  reckon: the tester says what is left, and the ACE ends the run honestly at the stage reached rather than exceed it.
- At most one file attachment batch per conversation (the lab notes), small text files only.
- No two testers are run on the same day, so the three are spread over at least three days *(default)*. Each
  tester's last sitting ends with teardown recorded before the next tester's first session.
- Each tester has its own sittings in the chief engineer's time; the ACE runs them as the hands and no other person
  or agent drives the chat.
- No load testing, no retry storms, no use of the chat for anything but the journey.
- Lab material only. If the tester or the assistant produces anything that looks real (a real person's name, a real
  address, a key), stop and tell the chief engineer; the run is void for that stage.

## Teardown and key rotation

After **every** sitting that opened a session, and at the end of each tester (the last sitting's teardown also covers the tester's whole run):

1. **Stop.** The chief engineer clicks **Stop** in the SCAT Chat window (or quits the app); the page says either does
   the same. The hands paste the stop message word for word. The expected words are the page's: "Stopped. The public
   link is off, the server is removed, your Mac may sleep again, the key was replaced, and your clipboard holds no
   key." **Relies on WP18's docs.** If it says "Stopped, but I could not confirm:", do what the page says (click
   SCAT Chat, then Stop, or restart the Mac); if the public link may still be on, the chief engineer switches the public link
   off in the service's app, as the page says. Record all of it.
2. **Confirm independently, once.** The ACE, with the chief engineer, shows that the container is gone and that the
   public link is off, with the checks the launcher's own stop message cannot give (for example the container
   runtime's list of running containers, and the public-link service's status). Paste the output. The ACE types these only as
   checks, never to change anything. **The key is rotated** by Stop; its replacement is not needed afterwards and the
   old one is never written down. Record that Stop reported the key replaced, and that the clipboard was cleared
   (the chief engineer pastes into a scratch text field and confirms it holds no key; the field is then emptied).
3. **Delete the chat's server entry** (the page says to; the hands do it, in the chat's settings, never the assistant), and the tester's test conversations and attached files, as
   far as the chat allows. Record what could not be deleted (the page for retention is silent; this is a known
   unknown).
4. **Leave the public-link settings as they are.** The certificate and publishing approvals stay enabled; the machine keeps its neutral name.
5. **Clipboard and windows.** Close the SCAT Chat window; close the chat tab; leave the container runtime app to the chief engineer.
6. **Scratch repositories.** The private repository stays, private, until the chief engineer decides to archive or
   delete it (his own act; the ACE does not delete a repository). Record its name only as `<repository>`.
7. **Verify next start.** At the start of the next sitting the window must show a fresh key; the ACE does not compare keys. Record that the old server entry stopped working
   (the chat reports a failed connection) if the chat shows it.

The run is not over, and no report is filed, until teardown is recorded.

## What to record

Keep a run record, one table per tester, filled as the sitting goes. Times from the real clock (`date -Iseconds`),
never invented. Columns: time, sitting, stage, who (tester / hands / chief engineer / chat assistant), request or
action, result (pasted, or evidence id), pacing (message count so far).

Also record, per tester: the candidate commit, the tester's model, the assistant model in the chat, what the chief
engineer did and why (every item), every message sent to the assistant (word for word) with the answer, every
window message from SCAT Chat (word for word), the teardown record, and the final tag, commit and recipient.

## Resume

A session can be split at any stage boundary. Each stage's entry point and what "done" looks like is the brief's
"Done:" line for the stage before it.

- **Between sittings** nothing is running: teardown has been recorded.
- **The tester across sittings.** Keep one tester conversation for the whole journey if the harness allows it. If
  it is lost, give a new agent the brief plus a **resume note** written by the ACE from the run record: "You are
  the tester c1. Stages J1 to J<k> are done. These are your earlier requests and the results: <the run record's
  rows, word for word>. Carry on at J<k+1>." The note adds nothing about the pages, the findings or the next step
  beyond what the run record holds. Record in the report that the tester was resumed, and where.
- **What the next sitting needs:** the stage reached (from the run record), the repository (private, kept), the
  vault folder on the Mac (kept), and the files the tester already made. The chat's earlier conversation is not
  needed: the vault holds the work.
- **Mid-stage interruption** (a crash, an outage): finish the request in progress, run teardown, and restart the
  stage from its beginning. Record the restart as a finding if a page said nothing about it.
- **Stopping early on purpose** (the message cap, a blocking failure): record the stage reached, run teardown, file
  the partial report ("not reached" for the rest).

## Evidence

Keep, outside this repository (it may show the chat's address and the machine's name, which are not for the public
repositories), in a folder named for the round and the tester:

- the run record (above), as a Markdown file;
- every screenshot, named `<tester>-J<stage>-<nn>.png`, listed in the run record with its time. At least one per
  stage; one of the repository page showing it private (J2); one of the SCAT Chat window each time it starts and
  stops (with the key area **not** in the screenshot: crop or hide it before saving); one of each chat answer the
  report quotes; one of the status of each page set finished; one of the tag and commit on GitHub (J10);
- every pasted text the tester received;
- the teardown record for each sitting, with the stop message word for word and the confirming checks pasted;
- the filed report, with `<address>` and `<repository>` in place of the real ones.

Only the filed report goes to `acceptance/reports/`. It names screenshot ids; the screenshots stay in the evidence
folder. Do not commit the evidence folder. If the chief engineer wants a screenshot in the reviewer's guide, he or
the ACE redacts it first.

## Void rules

A report is void and the tester is replaced and run again if any rule in `report-template.md`, "Void reports", holds.
In particular for this path: the hands never act beyond the tester's requests; no key appears anywhere but the clipboard and the chat's form; the run stayed
inside the pacing limits; teardown is recorded; and the names grep passes.

The ACE runs, on every filed report, the name grep in `acceptance/README.md` ("Checking a report mechanically"; the
list is kept from testers) and the checks below. A hit in a name the tester chose voids the report.

## Checks on the kit

Run these before the first sitting (the output pasted into the ACE's record):

1. The personas hold no tool vocabulary. The list, run as written, over `personas/` (and the briefs' "Who you are"
   text): `grep -n -i -w -E 'scat|scat-kg|node|edge|fingerprint|frontmatter|scenario|architecture|narrative|affordance|concern|technology|coder|vault|status|schema|mcp|cli|repl|clone|commit|push|branch|tag|pull request' personas/*`.
   It must be empty. Words natural to the person are allowed only because the persona states them: repository,
   GitHub, Obsidian, Terminal, link, page.
2. Each brief has J1 to J10, each with a "Done:" line, and names a hand-over case with its recipient.
3. The void grep of `acceptance/README.md`, run against each brief, is empty (the briefs must not use the
   worked example's names).
4. Every docs page a brief names exists in `docs/`.
5. The three briefs' domains (street trees, a pantry, a school walking bus) differ from one another, from the worked
   example, from the manual personas' domains (flood readiness, stall allocation, parts ordering), and from the range
   vault (the public case it rebuilds).
6. Three briefs exist, two name Haiku and one Sonnet; each brief names a different hand-over case.
7. The kit holds no private names or paths, and names no product beyond the pages and the mission (grep, pasted).

## What this plan relies on, and what it does not know

- It relies on WP18's docs (`docs/chat-path.md`, `docs/reference/mcp.md`) and on the launcher's messages as the page
  quotes them. Where a step in this plan says "Relies on WP18's docs", a wording change in the page needs the plan's
  step read again.
- Not yet shown by anyone, so each is a place the run can fail and the failure is evidence: the container runtime app with the
  launcher; the page's command-line step for the public link; whether the chat accepts the server's address; whether the chat
  offers a collection; whether the chat offers the server's prompts; how fast Obsidian shows what the server wrote;
  getting the repository onto the Mac without a terminal; committing and pushing from GitHub Desktop (the page's section for it was not run when written); the GitHub
  Release as the page describes it. These are open questions the run answers, not defects in the plan.
