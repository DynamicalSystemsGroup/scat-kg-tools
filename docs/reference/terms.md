# Terms

Where each term enters your plan, field notes, coding and analysis. Each entry gives a definition, its vault page
type (the vault is your folder of linked pages), its stage (plan, capture, code or analyse) and a check. Guides:
[Planning](../planning.md), [scenarios](../facilitate-scenarios.md),
[architectures](../facilitate-architectures.md), [Coding](../coding.md).

## Elicitation

A facilitated event: groups tell stories and pitch designs.

- **Vault:** none. The notes become [raw records](#raw-and-coded-records).
- **Stage:** plan.
- **Check:** before a session, have a written plan, your
  [stakeholder groups](#stakeholder-group), a note-taker per session, and a [clean check](#clean-check).

## Scenario

A story of people doing things over time.

- **Vault:** `scenario-raw`, `scenario-coded`. Coded, it links [groups](#stakeholder-group),
  [concerns](#concern), [affordances](#affordance).
- **Stage:** plan.
- **Check:** the plan gives each group a prompt.

## Architecture

An assembly of parts into tools that offer [affordances](#affordance).

- **Vault:** `architecture-raw`, `architecture-coded`. Coded, it links [concerns](#concern), affordances,
  [technologies](#technology).
- **Stage:** plan.
- **Check:** the plan keeps scenario and architecture sessions apart.

## Stakeholder group

A group the notes come from, named by role, never a person.

- **Vault:** `stakeholder-group`.
- **Stage:** plan.
- **Check:** the groups fit under the vault's cap.

## Concern

What a group cares about.

- **Vault:** `concern`.
- **Stage:** code.

## Affordance

What a tool or arrangement lets someone do.

- **Vault:** `affordance`.
- **Stage:** code.

## Technology

The thing that provides an affordance.

- **Vault:** `technology`.
- **Stage:** code.

## The three links

Each is one fact, on its own page.

- **Holds:** a group holds a concern. `heldby`, with `group` and `concern`.
- **Addressed by:** a concern is addressed by an affordance. `addresses`, with `concern` and `affordance`.
- **Attributed to:** an affordance is attributed to a technology. `attributes`, with `affordance` and `technology`.

So a concern reaches a technology only through an affordance: addressed by it, then attributed to the technology.

- **Stage:** code.
- **Check:** one page per pair; a coded page's lists do not make them.

## Conflict between concerns

Two concerns that pull against each other, recorded and never settled.

- **Vault:** the `conflicts` field on a `concern` page. One side counts for both.
- **Stage:** code.
- **Check:** each tension in the notes appears as a `conflicts` link.

## Raw and coded records

A raw record is the notes as told. A coded record restates them in plain words and links what they name.

- **Vault:** `scenario-raw` or `architecture-raw`; `scenario-coded` or `architecture-coded`. `raw` links a coded
  page to its raw page; `coded` links back.
- **Stage:** raw at capture; coded at code.
- **Check:** before coding, a raw page holds the notes as told, each account under its group, no names or links,
  and the [past or future mark](#past-or-future-mark).

## Status

How finished a page is: `stub` (just started), `draft` (being written) or `done` (the sign-off).

- **Vault:** the `status` field of every page except `class`.
- **Stage:** capture.
- **Check:** the author sets `done`; the tool does not check readiness. It needs every field and link the
  page type requires: `description` always, `timeframe` on a raw page, `raw` and the lists of what it names
  on a coded page.

## Past or future mark

Whether an account is real (`past`), intended but not yet real (`future`), or both (`mixed`).

- **Vault:** the `timeframe` field on `scenario-raw` and `architecture-raw`.
- **Stage:** capture.
- **Check:** every raw page has it.

## Clean check

A whole-vault read with zero errors. With nothing to report it prints "no problems". Warnings do not stop it.

- **Vault:** none.
- **Stage:** code; a gate before analyse.
- **Check:** analysis needs a clean check and `done` pages. The check tests structure, not content.
