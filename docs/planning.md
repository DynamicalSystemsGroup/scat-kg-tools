# Planning

!!! tip "Your next step"
    Cluster the people you expect into groups that fit under your cap.

Planning settles who takes part, in which session, who writes the notes and what participants are told, before the first session. Save your event plan as a plain text file named `plan.txt` in your vault folder, outside the page folders. The check does not read it.

A **concern** is something a group cares about. An **affordance** is something a tool or arrangement lets someone do. The [home page](index.md) defines these and the other two kinds of thing.

Before you start, have a vault set up and passing its check ([Getting started](getting-started.md)), a rough list of who might come by role, and the participation terms answered as in [Data, rights and consent](data-and-consent.md).

## Two kinds of session

Scenarios hear people in a situation, doing things over time. Architectures hear how tools are assembled to give people something to do. Keep the two apart, in separate sessions or halves of one; one person can tell a story in one and pitch a design in the other. Take past and future apart too: see [Facilitating timeframe](facilitate-timeframe.md). Plan a prompt for each group in every scenario session, worded from its own standpoint ("from where trustees and funders sit, ..."), so no group's wording is the default. In architecture sessions, groups that pitch nothing still say what concerns a design needs to meet.

## Groups and the cap

Every vault sets a cap on the number of groups, one line in `scat.toml`. The example vault sets it to 3:

```text
stakeholder_group_cap = 3
```

The cap keeps groups large enough that nobody can be picked out. Cluster the people you expect to fit under it:

1. List who is likely to come, by role, never by name.
2. Group them by shared standpoint, what they look at the world from. Not by size or by who is loudest.
3. If more standpoints appear than the cap allows, widen a group's description so it holds them.
4. If one identifiable person fills a role, widen the group around it. A group of one is a person. Where it is unclear which group someone belongs to, ask them.

The test of a good group is a line a member would say of themselves: "From where operators sit, we keep the desk open and the tools safe." A group beyond the cap is refused, with this fix: link an existing group, or raise `stakeholder_group_cap` in `scat.toml` if the plan allows. Clear the example groups before you add pages of your own: [Start your own content](getting-started.md#5-start-your-own-content).

## Choose the attribution mode

The vault has one **attribution mode**: whether a narrative names the people it is attributed to. You choose it at set-up, before the first session, with one line in `scat.toml`, beside the cap. The template's line is the worked example's mode:

```text
attribution = "disallowed"
```

| Mode | A narrative | The vault holds |
|---|---|---|
| `required` | names its contributors before it is `done` | a contributor page for each person named |
| `optional` | names its contributors, or none | a contributor page for each person who chose to be named |
| `disallowed` | names no contributor; the Chatham House rule is this mode | no contributor page |

The mode is the same for every session and participant. The check refuses a vault with no mode, and the tools enforce yours: [Norms](norms.md#writing-together) and [Coding](coding.md#contributor-pages-and-attributed_to) say how. Changing it later flags pages written under the old one, so choose before you tell participants anything.

## A one-off online discussion

Fix the call link, a shared notes page and the note-taker before you invite. Pick one kind of session and one timeframe. Say the terms as the call opens and paste them at the top of the notes page. A recording is a second set of notes: match its settings to what you told people.

## A recurring discussion

The same people return, so set the terms and groups once and restate them briefly each time. Keep one dated notes page per session. Tell newcomers the terms before they speak. The cap holds across the whole series, so plan the groups for all of it.

## An in-person meetup

Plan the room: a table per group or one circle, a board for what comes up out of turn, and a seat for the note-taker beside the facilitator. Sign in by group, never by name, unless the mode is `required`. Turn the notes into one file per session within a day.

## A multi-day workshop

Give each kind of session its own block, and past and future separate blocks within it. Give every group a turn in each block, in an order set in the plan. Name a note-taker for each block, so nobody writes through every session. At the end of each day, collect that day's notes, and bring each group its own accounts the next morning to add to or change.

## State the participation terms, aloud and on the page

Frame every session under the participation terms agreed for the event: say them at the start, and write them on the page the notes go on. What you say follows from the attribution mode. The worked example's mode is `disallowed`, the Chatham House rule, so its script reads like this; yours says what you agreed:

```text
Whatever is said here can be used. Nobody is named, and
nobody is quoted by name. The notes say which group an
account comes from, never who gave it. A group never
stands for one person.
```

In `required` mode, tell participants that each account is written down with the name of the person who gave it:

```text
Whatever is said here can be used. Each account is written
down with the name of the person who gave it, and the notes
also say which group it comes from. A group never
stands for one person.
```

In `optional` mode, tell them that a name goes with an account only if its giver wants it:

```text
Whatever is said here can be used. If you want your name
with what you say, tell the note-taker, and it is written
with the account. If you say nothing, the account has no
name, only the group it comes from. A group never
stands for one person.
```

Also tell participants: the notes become pages in a private vault, and each group gets its page to add to or change; anything can stay in the room, and the notes leave it out; accounts can differ, and the differences are written down, not settled.

## Set the stage for facilitation and field notes

Before each event:

1. Check the vault passes, in either spelling:

    === "Python"

        ```python
        import scat_kg
        scat_kg.check()
        ```

    === "CLI"

        ```bash
        uv run scat check
        ```

2. Make the first line of the notes page the terms, for example "Attribution disallowed (Chatham House): groups, not individuals."
3. Note places where two groups seem to share a concern but differ on others. Write them as questions to listen for, not as findings.
4. Brief the facilitator and the note-takers together. The facilitator listens and asks; the note-takers write.

## Who takes field notes

Name a note-taker for every session before it starts, someone other than the facilitator. One is enough; take two for a large room. A note-taker writes what was offered in the speaker's words, headed by the group, with a rough time. In `disallowed` mode they write no name. In `required` mode they also write the name or handle, so the coder can make the contributor page. In `optional` mode they write a name only for a speaker who asked.

## Compiling several sets of field notes

With several note-takers, agree one layout before the event: the terms line first, then each group's account under its own heading, with a time, as the guides for [Narratives](narratives.md#what-good-field-notes-hold) show. Each note-taker keeps one file per session, named by date and session.

[Coding](coding.md) takes in one plain text file per story, with each group's account under its own heading, pasted as taken under the front matter of a narrative page. [The flow](flow.md) shows where that step sits. One named compiler therefore does this after each session:

1. Collect every file into one folder outside the vault.
2. For each story, merge the accounts of all note-takers into one file. Keep every account; where two differ, keep both wordings and mark the difference.
3. Drop anything withdrawn, and leave a line saying so.
4. Ask the note-takers to read the merged file and fix what is wrong.
5. Hand each merged file to the coder.

## Where next

- Under "Facilitating": [Narratives](narratives.md), [scenarios](facilitate-scenarios.md), [architectures](facilitate-architectures.md), [timeframe](facilitate-timeframe.md).
- [Coding](coding.md), after the session.
