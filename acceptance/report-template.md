# User-test report

Fill in every section. Paste real output; a claim with none does not count (see "Void reports" at the end).

**Persona and model:** (persona file, model name)
**Path:** Python session / command line
**Round and date:**
**Docs source:** Pages URL, or local build of commit `<hash>` (a local build is recorded as known-weak)
**Environment:** fresh home directory: yes/no. `uv` was preinstalled and the uv installer was not run: yes (state this
plainly; it is a known gap held for the chief engineer, log D-040 and D-041). Remote removed from the clone: yes/no.
Paste: `echo $HOME`, `which uv`, `uv --version`, `git remote -v` (empty).

## 0. Cold-read answer (R-15)

First, before any stage. In your own words and without looking for an expected answer:

> What style or reference do the pages evoke for you? Answer:

Pasted words from the page that made you say so:

Did any metaphor, image or phrase obscure an instruction? Page, short quote, what you took it to mean:

## 1. Stage by stage

Repeat this block for J1 to J7. If you did not reach a stage, write "not reached", and do not fill it in.

### J1 Find / J2 Create / J3 Set up / J4 Plan / J5 Capture / J6 Code / J7 Finish

- **Reached and done?** yes / no / partly. What "done" looked like, shown by output.
- **Where I got stuck:** (page, step, what I was trying to do, how long or how many tries)
- **What I guessed:** (every action the pages did not literally state; the guess, and why I had to make it)
- **Where the pages left me nowhere to go:** (page, step, what was missing)
- **Pasted output:** (the commands you ran and what they printed, exactly)
- **Findings from this stage:** F-n list, each rated per section 2.

## 2. Findings

| Id | Stage | Page and step | What happened | Guess? | Severity |
|---|---|---|---|---|---|
| F-1 | | | | yes/no | blocking / not blocking |

Severity:

- **Blocking:** the tester was stopped short of J7, or a command on a page does not work as shown.
- **The expected failure of the J7 push** (the isolated clone has no remote) is **not a finding and not blocking**. Paste it and move on.
- **Not blocking:** everything else. Every guess is at least a not-blocking finding.

Every guess is a finding, even one that went well.

## 3. End state

Paste the final whole-folder check, the status of every page you made, and `git log --oneline` of your work.
Did you reach J7 with a clean check (zero errors)? yes / no. If no, the stage you stopped at, and why:

## 4. Dispositions (filled in afterwards, by the ACE)

Each finding ends fixed and re-tested by a fresh tester, or accepted with a reason. Accepted findings go in the
reviewer's guide. The final round has no blocking finding.

| Id | Disposition | Fix (commit) and re-test (round, persona), or reason accepted |
|---|---|---|
| F-1 | fixed and re-tested / accepted | |

A report with no findings is checked by the ACE for plausibility, before it is accepted.

## Void reports

A report is **void** and is run again, with a fresh tester, if any of these hold:

1. It reuses a name from the worked example, or from the documentation's own examples, for a page or a group of
   its own. (Names printed in the pasted output of the untouched example, or quoted from a page, are fine.)
2. It makes a claim with no pasted output.
3. It says the tester read `src/` or `tests/`, or the output shows it did.
4. It does not state that `uv` was preinstalled, or does not say which docs source it used.
5. It has no cold-read answer, or the cold-read answer is given after the tester has seen any named expected answer.
