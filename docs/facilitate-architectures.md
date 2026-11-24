# Facilitating architectures

!!! tip "Your next step"
    Open the session by reading the Chatham House lines aloud, then ask the first proposer how the parts fit together and what the whole lets people do.

*Each proposer plays a design in turn, and you build on what you hear.*
{ .epigraph }

An architecture session is a round of designs, one proposer at a time. It hears how a proposed assembly of tools is put together, and which concerns it addresses. You
hold the room, much as a player in a jazz combo improvises on what the others play. A note-taker writes. This page runs you through the session stage by stage, then turns the notes into a
raw architecture page.

Nothing here is ranked, voted on or adjudicated. You never ask the room to pick a design, and you never ask a
proposer to defend a design against another.

## Before you start

- A plan: groups within your cap, a note-taker, and the people who will pitch. See [Planning](planning.md).
- A vault that passes its check, with the tools set up. See [Getting started](getting-started.md).
- Scenario sessions kept apart from this one, in a separate session or a clearly separate half. See
  [Facilitating scenarios](facilitate-scenarios.md).

## The stance

Two moves keep the whole session in time.

- **Yes, and.** Whatever is pitched is taken up and built on. You write it down as offered, then ask a question that
  adds to it. You never ask a question that tests it.
- **From this perspective.** Each pitch is tied to the group that proposes it and the practice it comes from: "from
  where the operators sit, ...". It is never the standard way.

Architectures are structural. They are parts and wholes: tools assembled to give people something to do, in service of
concerns. People are largely set aside. The same concern may come from several groups, and a design cannot say who
will adopt it. Concerns are the currency of the session.

Anyone with a design to pitch is a technologist for this session. That is a device, not a division of people.

## The stages

### 1. Opening

Do: say the Chatham House frame aloud. Say that today is for designs and the concerns they answer, and that several
designs may answer one concern.

Say:

```text
Whatever is said here can be used. Nobody is named; the
notes say which group a pitch comes from, never who gave
it. Today is for how things are put together, and what
worry each one is for. Yes, and: several designs can
answer one concern, and we will write down all of them.
```

Note-taker writes: the date, the session, and "Chatham House: groups, not individuals."

### 2. Eliciting

Do: ask one question at a time. Ask about parts and wholes, not people.

Say, in this order, one per turn:

```text
How do the parts fit together, and what does the whole
let people do? What worry or aim is this for? What does
this not address? Yes, and who else might hold that concern?
```

Note-taker writes: each part and how it joins the others. Each concern, on a line of its own and in the proposer's words, so it can
be matched with groups later. Each gap ("not addressed: ...") as a fact about the design, recorded without blame.
Who else might hold the concern, as an open question. The design cannot presume who will adopt it, and other groups'
answers are welcome later.

If someone begins telling the story that led to the design, take it up and write it down. Say:

```text
Yes, and thank you. We will note that story
for the scenario session.
```

The note-taker writes the design on its own, and the story as a separate account. A proposed design is its own note,
not a conclusion from a story.

"What does this not address?" is asked as an addition, never as a test of the design:

```text
Yes, and what else would you want it to cover?
```

The answer is a fact about the design, written without blame.

### 3. Taking up

Do: when a second design is pitched for the same concern, take it up as a companion. It is not a challenger.

Say:

```text
Yes, that answers it, and here is another way to answer
it?
```

Several designs for one concern, and several concerns for one design, are all welcome. No design is asked to justify
itself against another.

### 4. Placing in perspective

Do: tie each pitch to who proposes it and from what practice.

Say:

```text
From where the operators sit, how do the parts fit?
```

Note-taker writes: "From the point of view of <group> (about 14:05)" at the head of each pitch. Write a concern in the words of the
group that voiced it. Two groups may voice almost the same concern in different words. Write both, in their own words.
Do not merge them in the room. That is for a later reading.

### 5. Capturing

Do: the note-taker writes what was offered, before anyone reads meaning into it. Keep the design apart from the
stories that prompted it.

While the note-taker writes, say:

```text
Yes, that is being written down as you said it.
What else does it do?
```

If a proposer wants to revise a note, add the revision beneath and leave the first wording in place.

### 6. Closing

Do: tell the room what happens to the notes, and ask whether anything should stay in the room. After the session, bring
each group its page, as a paper or screen copy, and add its corrections beneath the first wording.

Say:

```text
The notes become a page in a private vault.
After the session we will bring you the page,
and you can add or change anything on it.
Yes, and is there anything you want kept in the room?
```

Note-taker writes: anything a group asks to withdraw is left out of the notes, with a line saying that it was withdrawn and no
content.

## Holding disagreement, silence and interruption

Two designs that cannot live together are both written down. You may name the tension aloud and ask what each design
protects. You do not prefer one.

```text
These two cannot sit side by side. Yes, and what is each one protecting?
```

Note-taker writes: "Tension: ..." with both designs kept, each under its own group.

If a group stays quiet, do not take that as agreement. Write "no account offered" under that group. That is a gap you
record, not a result.

If someone is talked over, return to them:

```text
Yes, and we haven't yet heard what that looks like from
your side.
```

## Take the notes into a raw architecture page

Notes are taken under Chatham House: groups, no individuals, no attribution. A good set of notes looks like this:

```text
Chatham House: groups, not individuals.

From the point of view of Operators (about 14:05)
Pitch: a booking sheet, a shelf label for each tool, and a weekly check by two volunteers.
- Parts: the sheet records who has what; the label shows the tool's check date.
- Concern: "we cannot lend a tool we have not checked."
- Not addressed: tools that go missing between checks.
- Who else might hold this concern: open.

From the point of view of Trustees and funders (about 14:20)
Pitch: a monthly report from the sheet.
- Concern: "we need to know the workshop is used."
- Not addressed: safety checks.

Borrowers: no account offered.
```

Keep to the rules the notes carry:

- the group heads every pitch, and no name appears;
- technologies and parts are named freely, because this is structure;
- concerns are in the speaker's words, one per line;
- do not link other pages with `[[...]]`, and do not describe who will use a design as a conclusion. Coding adds the
  links.

Make the raw page with `scat stub`. It checks the name for you and writes the front matter, so you never hand-write
structure. Give it a name of lowercase letters, digits and hyphens.

=== "Python"

    ```python
    import scat_kg
    scat_kg.stub("booking-sheet-pitch", type="architecture-raw")
    ```

=== "CLI"

    ```text
    uv run scat stub --type architecture-raw booking-sheet-pitch
    ```

The tool prints:

```text
created architecture-raw/booking-sheet-pitch.md
```

The page is made, with status `stub`:

```text
---
type: architecture-raw
status: stub
title: "Booking sheet pitch"
---
```

Open the page in Obsidian and paste your notes under the front matter, as they were taken. Do not tidy them. Then
mark the page as a draft and check it:

=== "Python"

    ```python
    scat_kg.set_status("booking-sheet-pitch", "draft")
    scat_kg.check()
    ```

=== "CLI"

    ```text
    uv run scat set-status booking-sheet-pitch draft
    ```

    ```bash
    uv run scat check
    ```

Setting the status prints two lines:

```text
changed architecture-raw/booking-sheet-pitch.md
note: `status` set to draft (was stub)
```

The check prints this, from either tab:

```text
warning [SCAT-DRAFT-FIELD] architecture-raw/booking-sheet-pitch.md field `description`: missing (required once the page is done)
  Fix: add the line `description: "<one sentence you write>"` (author) before you set status: done
warning [SCAT-CONFLICT-BOTH] scenario-coded/notes-at-a-chatham-house-session-coded.md:11 field `concerns`: this record holds both [[anonymity]] and [[attribution]], which conflict (declared on [[anonymity]])
  Fix: none needed if both belong in this record. Holding both sides is allowed and is what the warning marks, a place where two concerns pull apart. If one was coded here by mistake, delete its line `- "[[anonymity]]"` or `- "[[attribution]]"` under `concerns`.
0 errors, 2 warnings
```

These warnings are a nudge, not a fault. The page is a draft. It is finished when you code it.
See [Coding](coding.md).

Obsidian's own page template for a raw architecture also exists, but it takes its name from whatever you type as the
file name. A name with capitals or spaces fails the check. `scat stub` is the one way, because it refuses a bad name
and says why.

## Where next

Where to go from here:

- [Coding](coding.md), to turn the raw page into a coded architecture.
- [Planning](planning.md), for the next event.
