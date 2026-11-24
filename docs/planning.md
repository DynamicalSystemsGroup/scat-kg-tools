# Planning

!!! tip "Your next step"
    Cluster the people you expect into stakeholder groups that fit under your cap.

Planning settles who takes part, and in what order, before the sessions start, so that every group gets a turn.

You are planning a facilitation event. Write your event plan: who takes part, in which session, in what order. Save it as a plain text file named `plan.txt` in your vault folder, outside the page folders. It is not a SCAT page, and the check does not read it. By the end you will have a short plan: which sessions hear stories, which hear
architectures, which groups are in the room, and how the notes will be kept.

Two words come up below. A **concern** is something a group cares about. An **affordance** is something a tool or arrangement lets someone do. The [home page](index.md) defines these and the other two kinds of thing, groups and technologies.

Nothing here is ranked, voted on or adjudicated. Your plan adds topics and voices; it never trades one off against
another.

## Before you start

- A vault of your own, set up and passing its check. See [Getting started](getting-started.md).
- A rough list of who might come, by role.

## Two kinds of session

SCAT hears the same ground from two sides. Keep the two apart, in separate sessions or in clearly separate halves of one
session.

| | Scenarios | Architectures |
|---|---|---|
| Looks at | people in a situation, doing things, over time | parts and wholes: tools assembled to give people something to do |
| Told by | actors: users, sponsors and other stakeholders | technologists: researchers, developers and operators |
| Technology | stays in the background; what is heard is what it lets people do | is the subject |
| People | are the subject | are set aside; a concern may come from several groups, and nobody can say who will adopt the design |
| Becomes | a raw scenario page | a raw architecture page |

"Actors" and "technologists" are a device for running a session, not a split of people. Most people are both. The same
person may tell a story in one session and pitch a design in the other, speaking from a different perspective each time.

Neither kind is the "real" one. The order you run them in is a choice about the day. It says nothing about which matters more.

Take past and future at separate times too. Run one session or block for what has happened and another for what could or will happen, each with its own block of scenarios and architectures. The [phrase list](facilitate-scenarios.md#past-or-future-one-at-a-time) shows how to tell them apart.

## Stakeholder groups and the cap

Every vault sets a cap on the number of stakeholder groups. It is one line in `scat.toml`, at the top of the vault
folder. The example vault sets it to 3:

```text
stakeholder_group_cap = 3
```

The cap exists because people enter the data as groups, never as individuals. A cap keeps groups large enough that
nobody can be picked out.

Cluster the people you expect into groups that fit under the cap:

1. List who is likely to come, by role. Never by name.
2. Group them by shared standpoint: what they look at the world from. Do not group by size or by who is loudest.
3. If more standpoints appear than the cap allows, widen a group's description so it holds them. Do not drop a
   standpoint. If widening still leaves more standpoints than the cap, your plan decides: you may raise `stakeholder_group_cap` in `scat.toml` if the plan allows it. See [a new group over the cap](coding.md#8-a-new-group-over-the-cap-scat-cap) for the exact steps.
4. If a role is filled by one identifiable person, widen the group around it. A group of one is a person.
5. Where it is unclear which group someone belongs to, ask them. A person may speak from more than one group.

An example, for a community tool-lending library and a cap of 3:

```text
Invited, by role: desk volunteers, the volunteers who keep the booking app running, borrowers,
the trustees, the people who fund the workshop.

Groups
  Operators         desk volunteers and the volunteers who keep the booking app running
  Borrowers         people who borrow tools
  Trustees and funders   the trustees, and the people who fund the workshop

"From where operators sit, we keep the desk open and the tools safe."
```

The group names here (Operators, Borrowers) are examples. Write your own groups, from your own invitees.

The last line is the test of a good group: a member would say it of themselves. If you cannot write it, the group
is not yet a standpoint.

The cap is a decision about the whole event, taken before it. The tools do not work around it. If you try to add a
group beyond the cap, this command refuses and prints the message below, and creates nothing:

```text
uv run scat stub --type stakeholder-group harbour-crews
```

It prints:

```text
refused scat.toml field `stakeholder_group_cap`: the vault is at its cap of 3 stakeholder groups, so a new group page (harbour-crews) would break SCAT-CAP; choose an existing group
  Fix: either link an existing group, or write `stakeholder_group_cap = 4` in scat.toml (the cap protects against identifying individuals; raise it only if the plan allows)
```

The example vault ships with three example groups, which fill a cap of 3. Keep the example while you plan, as a model. When the plan is done, clear the example pages: that is step 5 of Getting started, [Start your own content](getting-started.md#5-start-your-own-content). Do it before you add any page of your own, and before you code your own notes.

## Give every group room in every session

Invite every group, and give each one room to speak in every session.

- In scenario sessions, every group has a way to tell what it does. Plan a prompt for each group, worded from its own
  standpoint: "from where trustees and funders sit, ...". No group's wording is the neutral default.
- In architecture sessions, anyone who has a design to pitch is welcome. Groups that pitch nothing still have a place to
  say what concerns a design must meet.

When an invitee asks for a topic or a session, add it. Do not trade it off against another. Your own questions
as you plan add ("who else sees it this way?"); they do not test ("is that really a group?").

## Say Chatham House, aloud and on the page

Frame every session under the Chatham House rule, and do it twice: say it at the start, and write it on the page the
notes go on. Say this, or something like it:

```text
Whatever is said here can be used. Nobody is named, and
nobody is quoted by name. The notes say which group an
account comes from, never who gave it. A group is never
a stand-in for one person.
```

Tell participants three more things:

- what the notes are for: they become pages in a private vault, and you will bring each group its page so it can add or change anything;
- that they can ask for anything to stay in the room, and the notes will leave it out;
- that accounts can differ, and the differences are written down, not settled.

## Note where groups may share a concern

Before the event, look for places where two groups seem to share a concern but differ on others. These are things to
listen for. They are not conflicts to prevent or to settle. Write them as questions, not as findings.

## Prepare the notes

Raw notes are kept apart from any later reading of them. Capture comes first, and meaning comes later.

- **The vault.** Cloned, private, and passing its check:

    === "Python"

        ```python
        import scat_kg
        scat_kg.check()
        ```

    === "CLI"

        ```bash
        uv run scat check
        ```

  Both end with `no problems`.

- **A note-taker for each session.** Someone other than the facilitator, so the facilitator can listen. They write
  what was offered, in the speaker's words, headed by the group, with a rough time. Never a name. Both facilitation
  guides show what the notes look like.
- **One raw page for each story told or design pitched.** You make it with one command, after the session, from the
  notes. The guides show how: [scenarios](facilitate-scenarios.md), [architectures](facilitate-architectures.md).
- **A line on the notes page**: "Chatham House: groups, not individuals."

## Where next

Planned? Then facilitate. Both pages sit under "Facilitating" in the site menu; that menu label is not a page, so use these links:

- [Facilitating scenarios](facilitate-scenarios.md)
- [Facilitating architectures](facilitate-architectures.md)
- [Coding](coding.md), for after the session.
