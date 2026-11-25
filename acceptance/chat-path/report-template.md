# User-test report: the chat path

The tester writes this report as text, and the ACE (who ran the tester's hands) files it. The ACE saves each finished
report as `acceptance/reports/<round>-<persona>.md` (for example `wp20-chat-c1.md`) and keeps the evidence folder
(see `plan.md`, "Evidence") outside this repository. Never write a key, a password, a sign-in code or the chat's
address into a report: write `<address>`.

Fill in every section. Paste real output; a claim with none does not count (see "Void reports" at the end).

**Persona and model:** (persona file, the tester's model)
**Path:** the chat, no terminal
**Round, date and sitting(s):** (A, B, C; dates from the real clock)
**Docs source:** Pages URL, or local build of commit `<hash>` (a local build is recorded as known-weak)
**Candidate commit:** the commit the Pages preview and the template pin
**The chat:** provider and the assistant model chosen in the chat (recorded, not chosen by the tester)
**Material:** lab material only: yes/no. Nothing real was typed, attached or pasted: yes/no.
**Set up beforehand by the chief engineer, not from the pages** (list: installs, sign-ins, app, anything else), and
what each was called on the page that covers it, or "no page":

## 0. Cold-read answer

*Retained for reference. A missing answer here does not void a report (as in the manual path, D-052).*

> What style or reference do the pages evoke for you? Answer:

Pasted words from the page that made you say so:

Did any metaphor, image or phrase obscure an instruction? Page, short quote, what you took it to mean:

## 1. Stage by stage

Repeat this block for J1 to J10. If you did not reach a stage, write "not reached", and do not fill it in.

### J1 Find / J2 Try / J3 Decide / J4 Set terms / J5 Set up / J6 Plan / J7 Capture / J8 Code / J9 Analyse / J10 Hand over

- **Reached and done?** yes / no / partly. The stage's "Done" line, shown by pasted output or a screenshot file name.
- **Who did what:** the tester's words, the ACE's hands (browser and Mac, on the tester's request), the chief
  engineer's hands (sign-ins, the app, the key, anything a page says only a person may do). List every action the
  chief engineer took, with why.
- **Where I got stuck:** (page, step, what I was trying to do, how many tries)
- **What I guessed:** (every action the pages did not literally state; the guess, and why I had to make it)
- **Where the pages left me nowhere to go:** (page, step, what was missing)
- **Pasted output and screenshots:** (requests sent, what came back word for word, evidence ids from the log)
- **Findings from this stage:** F-n list, each rated per section 2.

## 2. Findings

| Id | Stage | Page and step | What happened | Guess? | Severity |
|---|---|---|---|---|---|
| F-1 | | | | yes/no | blocking / not blocking |

Severity:

- **Blocking:** the tester was stopped short of J10's end (a locked version named, with its commit and recipient, and a
  clean check), or a step on a page does not work as shown.
- **A step that only a person can do** (a sign-in, switching a setting on in an account, pasting the key) is not a
  finding in itself. A page that does not say so, or does not say which setting, is.
- **Not blocking:** everything else. Every guess is at least a not-blocking finding.

Every guess is a finding, even one that went well.

Findings about the assistant (it claimed something false, wrote something into the vault it should not have, or
offered to set a page finished) are findings against the chat path, rated on the same scale. Say what it said, word
for word.

## 3. End state

- The final whole-vault check, pasted. The status of every page you made. The views written into the vault folder.
- **Hand-over:** the tag, the commit it points at, the recipient the case names, and the screenshot file name of the
  GitHub page that shows the tag and commit.
- Did you reach the end with a clean check (zero errors) and a locked version? yes / no. If no, the stage you stopped at, and why.
- **Teardown** (filled in by the ACE from the run record): the stop message word for word; the public link off; the
  server gone; the key replaced; the chat's server entry deleted (by the hands, never the assistant); the chat's test conversations and attached files
  deleted (or what the chat does not let you delete); anything not confirmed.

## 4. Dispositions (filled in afterwards, by the ACE)

Each finding ends fixed and re-tested by a fresh tester, or accepted with a reason. Accepted findings go in the
reviewer's guide. The final round has no blocking finding.

| Id | Disposition | Fix (commit) and re-test (round, persona), or reason accepted |
|---|---|---|
| F-1 | fixed and re-tested / accepted | |

A report with no findings is checked by the ACE for plausibility, before it is accepted.

## Void reports

A report is **void** and is run again, with a fresh tester and, if the key was exposed, a rotated key, if any of these hold:

1. It reuses a name from the worked example, or from the documentation's own examples, for a page or a group of its
   own. (Names printed in the pasted output of the untouched template, or quoted from a page, are fine.) The ACE
   checks with the grep in `acceptance/README.md`, "Checking a report mechanically".
2. It makes a claim with no pasted output and no screenshot file name.
3. It says the tester read `src/` or `tests/`, or the record shows it did, or its hands did on its behalf.
4. It does not say which docs source it used, or does not list what the chief engineer set up beforehand.
5. The hands did something the tester did not ask for, or put words in the chat that the tester did not give (the
   run record shows each request and each action; an unlisted action voids the stage's evidence).
6. Anything real went to the chat: real names, real notes, a real address or a key in a message, or an attached file
   that was not from the brief's notes.
7. The run was not light and human-paced as `plan.md` says (more than one session open at once, the message cap
   exceeded, messages sent before the previous answer finished).
8. Teardown was not done after the tester, or its result is not recorded.

A key or an address found in a filed report is redacted by the ACE before filing, and the sitting's key is already
rotated by teardown. That alone does not void the report, but the ACE notes it.
